---
name: snapshot-brand
type: producer
version: "1.0.0"
recommended_model: sonnet
description: >
  Automatically fills spec.json, offers.json and the base of profile.json
  from a product URL. Scrapes the page, asks 4 closed questions about the audience,
  computes a completeness score, and lists missing fields.
  Scope: one product per run. Does not replace VoC/VoM, it complements them.
  FR: "snapshot", "snapshot ce produit", "remplis le workspace", "onboard ce produit",
  "crée la fiche produit depuis l'URL", "remplit spec.json depuis le site".
  EN: "snapshot", "snapshot this product", "populate workspace from URL", "onboard product".
permissions:
  reads: [brand]
  writes: [product, offer, profile]
  mode: proposed
  subagent_safe: true
pipeline:
  preconditions: brands/{slug}/ must exist (run setup-brand if needed)
  postconditions: run validate-resources to check completeness, ingest-resource to enrich
disambiguates_against:
  setup-brand: "route to setup-brand when operator wants manual guided setup without URL scraping"
  onboard-brand: "route to onboard-brand when operator wants the full multi-step pipeline from scratch, not just a URL scrape"
---

## Tone

Present the results as a product summary, not a data dump. "Here's what I found on your product", not "spec.json filled at 73%".
---

# Skill: Snapshot

Fills spec.json + offers.json + base of profile.json from a product URL.
One run = one product. Shopify JSON API prioritized over HTML. Zero hallucination: if a field is not in the page or the operator's answers, it stays `null`.

Relation to other skills:
- **setup-brand** → creates the structure. Snapshot fills it.
- **ingest-resource** → deep enrichment (VoC, arguments, competitors). Snapshot = surface.
- **validate-resources** → to run after, to check quality.

---

## Step 0 — Pre-flight: check workspace state

Before anything, two checks:

**Check 1 — Does the brand exist?**
Check that `brands/{slug}/brand.json` is filled (`identity.name` field non-empty).
- If empty or absent → tell the operator: "The brand isn't configured yet. Run `setup-brand` first, then come back here." Stop.
- If filled → continue.

**Check 2 — Product already snapshotted?**
Check if `brands/{slug}/products/{product_slug}/spec.json` exists and has `meta.slug` filled.
- If yes → flag: "This product already has a sheet. Update it (merge) or start fresh?" Wait for reply. Merge = keep existing non-null fields, overwrite with new scraped values. Fresh = overwrite everything.
- If no → continue.

---

## Step 1 — Product URL

Ask:
> "URL of the product to snapshot?"

**URL type detection before validation:**

| URL type received | Behavior |
|---|---|
| Product URL (`/products/{handle}`, `/p/`, `/shop/product/`) | Go direct → Step 2 |
| Brand or homepage URL (`example-brand.com`, `example-brand.com/`) | Read HTML navigation FIRST (see "Hero detection" below). Only if nav gives no clear signal → try `{base_url}/products.json?limit=50` to list the catalogue. |
| Collection URL (`/collections/{handle}`) | Try `{collection_url}/products.json?limit=50`. List products. Same flow as brand URL. |
| Ambiguous URL (can't type) | Ask: "Is this the URL of a specific product or the brand homepage?" |

One run = one product. If the operator wants several, relaunch the skill for each.

**Hero detection — always before API:**

When the URL is a homepage or brand URL → read the page HTML to detect the product highlighted in the navigation:
- Dedicated tab with visual emphasis (color, position) → strong hero signal
- Product on homepage banner or "featured" → medium signal

⚠️ Some hero products are **not returned by the** Shopify API (`products.json`). The HTML nav is the source of truth for hero, not the API.

**Mandatory confirmation before scraping — stage + ask:**

After detection, stage the proposal BEFORE asking the operator. The stage call records that a confirmation is pending; the next operator turn flows through the `checkpoint-resolver` hook and promotes the checkpoint based on the literal text of their reply.

**Order of operations** (hard rule):

1. Call stage-proposal with the detected product:
   ```bash
   python3 .skills/stage-proposal.py \
     --brand {slug} \
     --checkpoint confirmed_products \
     --product-slug {detected product slug} \
     --summary "Hero detected: {product name} — {url}"
   ```
2. Show the operator:
   ```
   I detected as hero product: {detected product name}
   URL: {product url}

   Is this the product you want to snapshot? Or prefer another one?
   ```
3. **Wait for the operator turn.** The `checkpoint-resolver` hook reads their reply and resolves the pending proposal:
   - `"oui"`, `"yes"`, `"go"`, `"ok"`, `"valide"` etc. → `confirmed_products` gains `{slug}` → Step 2 unlocked.
   - `"non"`, `"no"`, `"pas bon"`, correction like `"non, it's X"` → rejection logged, pending cleared → re-detect, re-stage with the corrected product, re-ask.
   - Free-form correction without confirm/reject marker (`"Hair Boost"`) → no automatic resolution. Clear pending manually by re-staging with the corrected slug (pending existing blocks new stage — surface gracefully to the operator).
4. **Never start scraping until stage-proposal is resolved.** Writing `products/{slug}/spec.json` or `products/{slug}/offers.json` without the slug in `confirmed_products` is blocked by the write-to-context gate.

**Validate the retained product URL:**
- Accessible (HTTP 200) → continue
- HTTP 301/302 → follow redirect, flag: "URL redirects to [new URL]. Is this the right product?"
- HTTP 403/401 or redirect to /login → stop cleanly:
  ```
  Protected page (member access required).
  Options:
  1. Provide a public URL of the product
  2. Paste the page content manually
  3. Use a Shopify API key if you have one
  ```
- HTTP 404 → "URL not found. Check the URL and relaunch."

---

## Step 2 — Platform detection + scraping

**Shopify detection** (in this order):
1. URL contains `.myshopify.com` or `/products/` → Shopify likely
2. Try `{base_url}/products/{handle}.js` → if HTTP 200 + valid JSON → **SHOPIFY CONFIRMED**
3. Try `{collection_url}/products.json?limit=50` for the catalogue if needed

**If Shopify confirmed → scrape the Shopify JSON**:
```
GET {base_url}/products/{handle}.js
```
Extract:
- `title` → spec.name
- `body_html` (strip HTML) → spec.description_raw
- `product_type` → spec.category
- `variants[]` → each variant = a candidate offer in offers.json
  - `variant.price` (in cents → divide by 100)
  - `variant.compare_at_price` (crossed price if non null)
  - `variant.title` (e.g. "3 months", "6 bottles")
  - `variant.available`
- `selling_plan_groups[]` → if present: subscription detected, note `subscription_detected: true`
- `tags[]` → note for categorization

**If non-Shopify → HTML scraping**:
Extract from HTML (in this order of priority):
1. `<script type="application/ld+json">` (structured data Product schema) → priority
2. Open Graph tags (`og:title`, `og:description`, `og:price:amount`)
3. `<h1>` → product name
4. Price: patterns `€X`, `$X`, `X.XX €` in the DOM
5. Description: `<meta name="description">` + first visible paragraph

**Layer 2 — product page HTML (after API, always):**

Even if Shopify JSON returns the data, read the product page HTML to capture what the API doesn't see:

| Element | HTML location | Target field |
|---|---|---|
| Trust badges / authority claims ("Clinically Tested", "Podiatrist Recommended") | Title zone → ATC | spec.proofs.authority |
| Review count displayed | Reviews widget (Judge.me, Loox, Okendo) | `_snapshot.reviews_displayed` |
| Quantity break selector (1 pair / 2 pairs / 3 pairs…) | Offer section, before ATC | offers.json — type `quantity_break` |
| Urgency / bonus ("OFFER ENDS SOON", "FREE eBook") | ATC zone | offers.json — `urgency`, `bonus_included` |
| Payment methods | Footer or ATC zone | brand.json — market confirmation |

⚠️ **WebFetch limit**: WebFetch returns only static HTML. Front-end apps (quantity breaks, review widgets) are rendered via JavaScript after load, invisible to WebFetch. If these elements are suspected but not visible in HTML → note `[app-rendered — requires Chrome capture]` and continue. Never invent unconfirmed price tiers.

**Review triangulation — 3 sources, always note provenance:**

| Source | How to get it | What it measures |
|---|---|---|
| Native Shopify | `products/{handle}.js` metafields | Reviews on this specific product |
| Onsite app (Judge.me, Loox…) | HTML page — displayed widget | Aggregated reviews cross-product, potentially imported |
| Trustpilot | `trustpilot.com/review/{domain}` | Independent verified reviews |

Rule: always note all 3 in `_snapshot.reviews_sources`. Never use the highest number without noting its source, the on-page number may come from an app with imported reviews (unverified). Significant gap between sources = flag `[review_source_conflict]` in `_snapshot`.

**Confidence score calculation** after scraping:
```
Expected spec.json fields: name, category, price, description, ingredients/composition, format/size
Score = (fields_non_null / 6) × 100

≥ 70% → proceed normally
40-69% → proceed with warning, list missing fields
< 40% → INCOMPLETE, list blocking questions before continuing
```

If score < 40%: the page doesn't have enough info to generate a useful sheet. Display:

```
Page too thin for auto-scan.

Your product page doesn't contain enough info (score: {X}/100).
Answer these questions and I'll build the sheet from your answers:

1. What problem does your product concretely solve?
2. Who is it for?
3. What's the mechanism or key ingredient?
4. What's the format / size / cure duration?
```

Wait for answers. Generate spec.json from answers + partial scraped data. Do not save an empty spec.json.

---

## Step 3 — Generate spec.json

Before generating, read `brands/{slug}/brand.json` → sections `tone_of_voice` and `positioning`.
If these fields are filled → use the brand tone and positioning to align the product description.
If `brand.json` is empty (first product) → generate from the page alone, without inference.

Fill `brands/{slug}/products/{product_slug}/spec.json` with scraped data.

Absolute rule: **never invent a field**. If the info isn't in the page → `null`. No creative inference.

Fields filled from scraping:
```json
{
  "meta": {
    "slug": "{product_slug}",
    "updated": "{today}"
  },
  "identity": {
    "name": "{title}",
    "category": "{product_type or inferred}",
    "format": "{extracted from variant title or description}"
  },
  "pricing": {
    "price": {main price},
    "price_original": {compare_at_price or null},
    "currency": "{EUR|USD detected}"
  },
  "description": "{stripped body_html, max 500 chars}",
  "_snapshot": {
    "source_url": "{url}",
    "scraped_at": "{datetime}",
    "platform": "shopify|html",
    "confidence_score": {0-100},
    "missing_fields": ["{field1}", "{field2}"]
  }
}
```

The `_snapshot` block is a technical block (non-schema official). Documents data provenance for traceability. Never manually deleted.

---

## Step 4 — Generate offers.json

Each Shopify variant = one candidate offer.

**Automatic typing logic** (apply in order):
0. **Group variants by price** before typing. If all variants share the same price → **1 single offer**. Variants (sizes, colors) are selection options, not distinct commercial offers. Never create N offers for N size/color variants at the same price.
1. If `selling_plan_groups` detected → at least one `type: "subscription"` offer
2. If variant title contains "mois", "month", "months", "cure" → `type: "prepay"` + fill `contents.duration`
3. If variant title contains several different products (e.g. "2 HB + 1 CB") → `type: "bundle"` + fill `contents.included_items`
4. If a single variant without explicit duration, or group of variants same price without duration → `type: "single"`
5. If `compare_at_price > price` → compute `savings_percent` and `savings_amount`

Fill `brands/{slug}/products/{product_slug}/offers.json` using the v2 `offer_groups[]` shape. Group-of-1 is valid and is the default for single-product offer files — only split into multiple groups if offers share distinct defaults (shipping, returns, warranty, payment_methods, active_window).

```json
{
  "_schema": "offers",
  "_version": "2.0",
  "meta": {
    "product_slug": "{product_slug}",
    "scope": "pre_cart",
    "updated": "{today}"
  },
  "offer_groups": [
    {
      "group_id": "GRP-01",
      "name": "Default group",
      "active": true,
      "shared": {
        "pricing": {
          "model": "one_shot",
          "currency": "{EUR|USD}"
        },
        "tags": []
      },
      "offers": [
        {
          "offer_id": "OFR-01",
          "name": "{variant.title}",
          "type": "{auto typing}",
          "product_refs": [
            {"slug": "{product_slug}", "quantity": {extracted or 1}}
          ],
          "pricing": {
            "model": "one_shot",
            "price": {variant.price / 100},
            "price_original": {variant.compare_at_price / 100 or null},
            "savings_percent": {computed or null},
            "currency": "{EUR|USD}"
          },
          "contents": {
            "quantity": {extracted or null},
            "unit_name": {extracted or null},
            "duration": {extracted or null},
            "duration_unit": {extracted or null},
            "is_prepay": {true if prepay or multi-month bundle, else null}
          },
          "subscription": null,
          "active": {variant.available},
          "tags": []
        }
      ]
    }
  ]
}
```

**Hard rules:**
- `_version: "2.0"` is mandatory. Never write `_version: "1.x"` or omit it.
- Always wrap offers in `offer_groups[].offers[]`. A flat `offers[]` at root is the legacy v1.x shape and is rejected by validate-resources.
- Use `product_refs: [{slug, quantity}]`, not legacy `product_ids: [slug]`.
- Group-of-1 is the default for single-product offer files. Only add more groups when shared defaults genuinely differ.

If subscription detected (selling_plan_groups): create a `type: "subscription"` offer with subscription fields filled to null (to complete via ingest-resource).

**App-driven quantity break (frequent case):**

If the HTML page shows a quantity selector with tiered prices (1 unit / 2 units / 3 units…) but the API returns a flat price identical on all variants → the price structure is handled by a front-end app (Bundler, Bold Bundles, custom script). The API doesn't see it.

Behavior:
- Create an offer `type: "quantity_break"` with `pricing.tiers: null` and note `_snapshot.offer_note: "quantity_break app detected — tiers not accessible via API, requires HTML/Chrome capture"`
- Never invent unconfirmed price tiers
- Flag to the operator: "I detected a per-quantity price structure on the page, but it's handled by an app I can't read automatically. Can you confirm the tiers? (e.g. 1 pair = X€, 2 pairs = Y€ each…)"

**Geo-detection — note currency context:**

Price scraping always in a known context. The API returns the base currency (USD/GBP). The site may display a different currency based on geo.
- Always note the API currency (`_snapshot.api_currency`) and displayed currency if different (`_snapshot.display_currency`)
- Flag `[geo_detection_active]` if the two differ

---

## Step 5 — Audience detection + operator validation

**First infer from the page**, then ask for confirmation. Never start blank.

### Step 5A — Inference from product page

Extract audience signals present in the scraped copy (Step 2):

| Signal | Source | Target field |
|--------|--------|-------------|
| Mentions of gender ("for her", "men's", "for women") | body_html, title | demographic.gender |
| Mentions of age or life stage ("60+", "kids", "active adults") | body_html, tags | demographic.age_range |
| Explicit problem in title or description ("foot pain", "plantar fasciitis") | title, body_html | pain.primary_problem |
| Use context ("after long hours standing", "gym", "daily wear") | body_html | pain.context |
| Product tags | tags[] | additional signals |

Build an **audience proposal**:
```
label       : {inferred or null}
gender      : {inferred or null}
age_range   : {inferred or null}
problem     : {inferred or null}
context     : {inferred or null}
```

Absolute rule: if no clear signal in the page → leave null. Do not invent.

### Step 5B — Stage + present the proposal + correct

Stage the proposal before presenting:

```bash
python3 .skills/stage-proposal.py \
  --brand {slug} \
  --checkpoint audience_q1q4_answered \
  --summary "Audience proposal: {label} — {gender}, {age_range}, problem: {problem}"
```

Display to the operator:
```
I detected on the page:
→ Audience: {label or "not detected"}
→ Gender: {gender or "not specified"}
→ Age: {age_range or "not specified"}
→ Main problem: {problem or "not specified"}
→ Use context: {context or "not specified"}

Close to your customers? Correct what's wrong, add what's missing.
(Examples: "more women 35-55", "real problem is foot fatigue", "add: they are nurses")
```

**Wait for the operator turn.** The `checkpoint-resolver` hook resolves the pending:
- Confirmation (`"oui"`, `"spot on"`, `"yes that's it"`) → `audience_q1q4_answered = true` → Step 6 write unlocked.
- Rejection (`"non"`, `"not my customers"`) → pending cleared, re-infer, re-stage.
- Free-form corrections (`"more women 35-55"`) → no automatic resolve. Apply the correction in memory, re-stage the updated proposal, re-ask.

If the operator says "I don't know" or doesn't answer on a field → keep null, DO NOT invent.

**Writing `audiences/{slug}/profile.json` is blocked by write-to-context until `audience_q1q4_answered = true`.**

### Step 5C — Unique complementary question (if data missing)

If after 5B fields `gender` AND `primary_problem` are still null → ask **one single question**:
> "In one sentence: who's your ideal customer and what problem do you solve for them?"

Extract gender + problem + age_range from the free answer. If still imprecise → null.

### Step 5D — Existing data

> "Do you have data on your customers, reviews, analytics, support returns? If yes, give me the most important fact in 1-2 sentences."
→ If yes with concrete fact → note in `data.operateur_note`
→ If no → `data.data_available: false`

**Final rule**: Do not create an audience folder if `gender` AND `primary_problem` are both null after 5B + 5C. Not enough to identify an audience.

---

## Step 6 — Generate profile.json (base)

Fill `brands/{slug}/audiences/{audience_slug}/profile.json` with:
- What comes directly from the product page (gender apparent in copy, problem addressed in title/description)
- What comes from Q1-Q4 answers
- Nothing else

```json
{
  "meta": {
    "slug": "{audience_slug}",
    "updated": "{today}"
  },
  "identity": {
    "label": "{inferred or corrected by operator}",
    "demographic": {
      "gender": "{5A/5B or null}",
      "age_range": "{5A/5B or null}"
    }
  },
  "pain": {
    "primary_problem": "{5A/5B or null}",
    "trigger_primary": null
  },
  "data": {
    "data_available": "{5D boolean}",
    "operateur_note": "{5D fact or null}"
  },
  "_snapshot": {
    "source": "snapshot skill v1.0",
    "completion_level": "surface — enrich with ingest-resource + VoC",
    "missing": ["objections", "pain_chain", "psychographic", "awareness_level"]
  }
}
```

Fields intentionally left empty (for ingest-resource after):
- `psychology.objections[]`
- `psychology.awareness_level`
- `pain.chain[]`
- `behavior.*`

---

## Step 7 — Operator validation before save

Before writing the files, show a summary of what will be saved:

```
Here's what I extracted for {product_name}, confirm before I save:

Product  : {name} — {price}€ — {category}
Offers   : {N} offers detected ({types})
Audience : {label} — {gender}, {age_range}
Problem  : {primary_problem}

Score    : {score}/100

{if score < 70}
Missing fields: {field1}, {field2}
→ They stay empty. You can add them with "ingest".

Good? Want to change anything before I save?
```

- **If the operator confirms** ("yes", "go", "spot on", "ok") → write spec.json + offers.json + profile.json.
- **If the operator corrects** ("price is 39€", "audience is more men") → apply the correction, reshow the modified summary, wait for confirmation.
- **Never write files before explicit confirmation.**

Once saved, run two silent post-writes before talking:

1. **Append to `brands/{slug}/pending-validations.md § Context gate`** one `[ ]` line per inferred field that was stamped with `mode=proposed` during this run. Wording in the operator's language, plain-language source tag (`(inferred from site)`, `(deduced)`), never `source` / `confidence` / `mode` jargon. Typical entries: audience(s) inferred, positioning inferred, tone inferred, compliance gaps detected (e.g. missing contraindications on a medical device).
2. **Trigger `validate-resources` silently** on the brand. This refreshes `status.json` (completeness per entity, freshness stamps, `wedge_complete`), rebuilds `learnings-index.json` if present, and re-runs the snapshot digest. Surface its result only if it flags MAJOR/CRITICAL — otherwise stay silent.

Then propose enrichment without waiting:

```
Saved.

Want to enrich now?
Paste anything: brief, customer reviews, positioning doc, support returns.
I sort and file automatically.

(Nothing now → say "later".)
```

- If the operator pastes content → **trigger ingest-resource immediately** on that content.
- If "later" / "no" / silence → close:
  ```
  OK. Run "validate" when you're ready to check consistency.
  ```

---

## Hard Rules

- **Stage before asking — always.** Hero confirmation (Step 1) and audience confirmation (Step 5B) MUST call `.skills/stage-proposal.py` before showing the question to the operator. The checkpoint-resolver hook promotes checkpoints from the literal operator reply — agent self-declaration is not accepted. Writes to `products/*/spec.json`, `products/*/offers.json`, `audiences/*/profile.json` are blocked by the write-to-context workflow gate until checkpoints resolve.
- **Never invent** a field not present in the page or answers. Null > approximation.
- **Hero detection = nav HTML first, API second.** Some hero products are absent from `products.json`. The site nav is the source of truth, read the homepage HTML before any API call when the URL is a brand URL.
- **Confirmation before scraping — always.** Show the detected product to the operator and wait for an explicit "go" before starting the scraping. Never assume.
- **Shopify JSON API priority** over HTML for product data. Do not scrape HTML if `/products/{handle}.js` returns 200. Exception: Layer 2 (above-the-fold, reviews, quantity breaks) always runs in complement to the API.
- **Review triangulation mandatory.** Capture the 3 sources separately (native Shopify, onsite app, Trustpilot). Never use a single number without noting its source. Significant gap = flag `[review_source_conflict]`.
- **Quantity breaks = app-driven, invisible to API.** If HTML shows per-quantity price tiers but API is flat → `type: "quantity_break"`, tiers null, ask the operator. Never invent tiers.
- **Geo-detection.** API currency ≠ display currency → note both, flag `[geo_detection_active]`.
- **Confidence score mandatory**. If < 40% → block before saving spec.json, ask for missing fields.
- **4 audience questions in order**, wait for each answer. Never skip, never merge.
- **If Q1 too vague after follow-up** → `null`, no inference. Same for every question.
- **Never overwrite brand.json**. This skill doesn't touch brand.json.
- **Setup-brand first**. If `brands/{slug}/` doesn't exist → stop and route to setup-brand.
- **One product per run**. Multi-product = relaunch the skill for each product.
- **`_snapshot` block always present** in spec.json and profile.json. Documents provenance.
- **Do not create audience folder** if Q1 + Q2 are both null, not enough to identify audience.
- **Write modes.** Never call `write_to_context` on a whole file path with `mode=proposed` — the proposal wrapper stamps `_proposed/_source/_confidence` at the root object and corrupts consumers. Always scaffold the file in `mode=direct` (full structure with null placeholders), then stamp inferred fields one by one with `mode=proposed` using a JSONPointer fragment (e.g. `file.json#/pricing/price`). The tool enforces this guard since 2.6.20.
- **Offers.json = v2 `offer_groups[]` only.** Never write the legacy flat `offers[]` at root. `_version: "2.0"` is mandatory. Single-product files use a group-of-1. Use `product_refs: [{slug, quantity}]`, not `product_ids`.

---

## v1.8 Field Awareness (2026-04)

The `_TEMPLATE` is at v1.8. When scraping a product page, you must look for and fill these new fields if the info is present. Null > invention.

**spec.json — blocks to populate when applicable:**

- `specs.composition[]` — structured list (ingredient, pct, organic_certified, class, origin, inci). Accepts string for legacy too.
- `specs.posology` — recommended_daily_servings, serving_unit, timing, duration_recommended, max_daily_dose, notes. Relevant: supplements, skincare, cures.
- `specs.contraindications` — conditions[], medications[], age_min/max, pregnancy, breastfeeding, warnings[]. Relevant: supplements, cosmetics, food.
- `specs.origin` — country, region, facility, local_supply_pct, made_in_claim, supply_chain_transparency.
- `specs.production_method` — type, batch_size, frequency, method_notes. Relevant: artisanal, made-to-order.
- `specs.preparation` — cooking_required, method, time_minutes, temperature, serving_suggestions[]. Relevant: food.
- `specs.external_databases` — open_food_facts_id, yuka_id, inci_beauty_id, ciqual_id, ean, gtin.
- `specs.target_suitability` — skin_types[], hair_types[], body_areas[], use_cases[], demographics[]. Relevant: beauty, skincare.
- `specs.durability` — warranty_years, warranty_type, repairable, spare_parts_available, repair_program, lifespan_estimate, repairability_index. Relevant: apparel, hardware, electronics.
- `nutrition_facts.allergen_sources[]` — allergen → ingredient source mapping.
- `nutrition_facts.nutri_score_grade` — A-E enum (FR 2025+).
- `perishability.period_after_opening_months` — PAO (cosmetics EU mandatory).
- `perishability.expiry_date_required` — boolean.

**New dietary_tags available:** caffeine_free, bio, raw, chicory_based, clean_beauty, cruelty_free.
**Allergen "oats" added to the EU14 enum.**

**offers.json — new fields:**

- `contents.duration_type` — calendar | usage_days | servings.
- `contents.duration_servings` — number.
- `contents.cure_metadata` — cure_name, is_premade, target_concern, phases[]. Relevant: pre-built cures.
- `incentives.duration_tiers[]` — discount per engagement (1/3/6/12 months).
- `incentives.loyalty` — loyalty program (points, tiers, sign_up_bonus).
- `offer_groups[].offers[].tags[]` — free tags at offer level (v2 schema; legacy `offers[].tags[]` is v1.x).

**Automatic stamping:** each entity file carries its own `_version` field matching the schema it was built against. Current baseline (read live from `_TEMPLATE`): `brand.json _version=2.1`, `products/{slug}/spec.json _version=1.8`, `products/{slug}/offers.json _version=2.0`, `audiences/{slug}/profile.json _version=1.2`. After a fresh scaffold via `cp -r _TEMPLATE brands/{slug}`, these values are inherited automatically. Never hardcode version expectations — always read from `_TEMPLATE` first.
