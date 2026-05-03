---
name: snapshot-brand
type: producer
version: "1.0.0"
recommended_model: sonnet
reasoning_pattern: null
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

**Large catalogue (>1000 SKUs):** `products.json` is paginated 50 max per page; fully enumerating a 1000+ catalogue burns tokens and time. When the catalogue exceeds ~200 products (detected via collection counts in nav, or after first page if `products.json` returns 50 with continuation tokens), do NOT enumerate — sample: read pages 1, 2, and the most recent (sort by `published_at desc`) for hero candidates, surface the volume to the operator (*"this catalogue has 1000+ products, I'm sampling featured + hero, paste a specific URL if you want a different one"*), and let them choose. Snapshot remains one product per run.
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

**Product detail page scraping (HTML after API, always):**

Even if Shopify JSON returns the data, read the product page HTML to capture what the API doesn't see (note: this is HTML scraping in complement to the API, not the doctrinal Layer 2 of connected tools):

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

## Step 3 — Generate spec.json (delegated encoding)

Before generating, read `brands/{slug}/brand.json` → sections `tone_of_voice` and `positioning`.
If these fields are filled → use the brand tone and positioning to align the product description.
If `brand.json` is empty (first product) → generate from the page alone, without inference.

**Encoding is delegated to `encode-batch` (Haiku sub-agent) so the main thread stays responsive.**

Build the observations list from scraped data, then launch encode-batch via Task tool:

```
Task tool call:
  subagent_type: shared
  skill: encode-batch
  model: haiku
  prompt: |
    {
      "brand_slug": "{slug}",
      "target_entities": [
        {"file_path": "brands/{slug}/products/{product_slug}/spec.json", "schema": "resources/schemas/spec.schema.json"}
      ],
      "observations": [
        {"semantic_kind": "product_name", "raw_value": "{title}", "evidence": "scrape: products/{handle}.js title", "source": "scrape", "confidence_signal": "literal"},
        {"semantic_kind": "product_category", "raw_value": "{product_type}", "evidence": "scrape: product_type", "source": "scrape", "confidence_signal": "literal"},
        {"semantic_kind": "product_description", "raw_value": "{stripped body_html, max 500 chars}", "evidence": "scrape: body_html stripped", "source": "scrape", "confidence_signal": "literal"},
        ... one observation per non-null scraped field ...
      ],
      "default_mode": "proposed"
    }
```

Producer (snapshot-brand) extracts the semantic signals from the scrape. encode-batch maps each signal to a `field_path`, runs `write-to-context.py` per mutation, rebuilds the snapshot, runs `finalize-mutation-batch.py`. Returns a structured summary (not operator-facing).

Absolute rule: **never invent a field**. If the info isn't in the page → don't include the observation. No creative inference. encode-batch refuses unmapped `semantic_kind` values rather than guessing.

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

## Step 5 — Audience cartography (4 movements)

**Doctrinal contract.** Read `docs/system/audience-cartography.md` before authoring or modifying this step. Step 5 runs four operator-facing movements in order: (1) raw observations, (2) cartography axes, (3) hierarchy mère/sous-audiences, (4) hand-off pédagogique vers `mine-voc`. Single-axis classification or flat audience output is a regression to form-fill and a violation of contextual intelligence doctrine.

The agent does NOT extract `pain_points[]`, `psychology.beliefs_limiting[]`, `voice.key_expressions[]` from the product page. Those fields belong to `mine-voc` verbatim. snapshot-brand fills only the cartography skeleton listed in `audience-cartography.md § Field-level contract`.

### Movement 1 — Raw observations (operator-facing)

Before any classification, name what the page literally said. No interpretation, just observation with source. **Zero internal jargon in the operator output** : never say "Movement", "cartography axis", "validation_status", "hypothesis-grade", "field path". Plain words.

Format example:

> *"Voilà ce que la page m'a dit côté audience, brut.*
>
> *La marque s'adresse à des femmes (mention 'pour elle' visible plusieurs fois). Le mot 'chute' revient 8 fois dans la description. Le mot 'pousse' 4 fois. Pas d'âge cité, pas de profession, pas de contexte de vie. Les tags produit pointent sur biotine, post-grossesse, cheveux abîmés.*
>
> *Trois signaux clairs (femmes, chute, pousse), le reste est silencieux. Je vais te proposer plusieurs manières de découper là-dedans, et tu trancheras."*

If the page is thin, say so plainly:

> *"La page m'a quasiment rien dit côté audience : juste 'pour elle' et deux tags génériques. Tout ce que je vais proposer après est à prendre comme une hypothèse de travail, pas une vérité. Tu corrigeras."*

Movement 1 is **never skipped**. Empty observations are a valid output, and more useful than a fabricated profile.

### Movement 2 — Découpages possibles (operator-facing)

Propose 2 to 3 alternative ways to slice the audience. Always mark one as the default hypothesis with a one-line rationale tied to a Movement 1 observation. Always invite override. **Operator-facing language**: "manières de découper", "découpages", "axes". Never "cartography axes".

The three canonical axes (skill-author vocabulary, NOT operator vocabulary):

- **Pain-driven** — slice by emotional state. Dominant when pain register diverges by segment.
- **Situational** — slice by life moment / context. Dominant when the same pain has different trigger contexts.
- **Demographic / cultural** — slice by who they are. Rarely dominant for paid acquisition; usually a modulator within pain or situational.

Operator-facing format example:

> *"Trois manières de découper cette audience, je te les pose toutes les trois et tu me dis laquelle colle à ce que tu vois en perfs.*
>
> *(1) Découpage par ressenti : 'je veux pousser' (longueur, densité, projet beauté positif) vs 'je perds mes cheveux' (chute active, charge émotionnelle, urgence). C'est le découpage qui colle quand le registre copy diverge fort entre les deux états.*
>
> *(2) Découpage par moment de vie : 'post-grossesse' vs 'stress longue durée' vs 'saisonnier'. Adapté quand le même pain est déclenché dans des contextes très différents.*
>
> *(3) Découpage par profil : 'voilées' vs 'non voilées'. Adapté quand le casting créa et le canal d'acquisition divergent par profil.*
>
> *Mon hypothèse à corriger franchement : (1) découpage par ressenti, parce que la page parle à la fois de chute et de pousse avec deux registres distincts (urgence vs projet). Si tu vois autre chose en perfs, dis-le."*

Wait for the operator's choice before Movement 3.

### Movement 3 — Hierarchy proposée (operator-facing)

Once the operator picks an axis, propose 2 to 3 **groupes principaux** with 1 to 3 **sous-groupes** each. Skill-author terms: mother audiences and sub-audiences. **Operator-facing terms**: "groupe principal" et "sous-groupe", or just "groupe" et "sous". Never "mother audience", never `meta.parent_slug`, never "validation_status: hypothesis".

Operator-facing format example:

> *"Sur le découpage par ressenti que t'as choisi, voilà la structure que je propose, en deux niveaux.*
>
> *Groupe 1 : pousse-projet — longueur ou densité jugées insuffisantes, démarche beauté positive, pas d'urgence.*
> *  Sous-groupes : pousse-jeune-adulte (18-30, projet esthétique), pousse-recovery (post-coloration ou post-lissage, casse récente).*
>
> *Groupe 2 : chute-active — chute en cours, charge émotionnelle, urgence.*
> *  Sous-groupes : chute-post-grossesse (25-35, hormonal aigu), chute-hormonale-stress (22-32, diffuse longue durée), chute-traction (zones d'appui voile / tissages / tresses).*
>
> *Tous les sous-groupes sont à valider — c'est volontaire, ça veut dire qu'on les pose comme hypothèses de travail et qu'on les confirmera avec du vrai verbatim client juste après. Tu valides cette structure, ou tu veux qu'on en garde moins pour démarrer plus serré ?"*

Single-question gate. Wait for operator confirmation. Once confirmed, scaffold the audience folders (Step 6) and explicitly tell the operator they can visualize the result via `/phantom {brand_slug}`.

> *"Validé. Je grave les 5 audiences (2 groupes principaux + 3 sous-groupes). Tu peux les visualiser à tout moment en tapant `/phantom {brand_slug}` — ça te sort un cockpit avec la liste, le statut de chacune, et ce qu'il manque pour passer de l'hypothèse au validé."*

### Movement 4 — Hand-off vers mine-voc (operator-facing)

Before closing Step 5, explicitly tell the operator how the audience encoding will be **used next**. Anchors why the work matters and proposes the next skill. **Operator-facing language**: skill names are OK (the operator is learning the system), internal field names are NOT.

Format example:

> *"Voilà comment ces audiences vont servir à partir de maintenant.*
>
> *Ce qu'on vient de poser est volontairement minimal : un nom, un découpage, une hypothèse. Pas de pain_points détaillés, pas d'objections, pas de citations clientes. C'est exprès — ces fields-là, je ne vais pas les inventer depuis une page produit, ils doivent venir de ce que disent vraiment tes clientes.*
>
> *Deux skills enrichissent ça :*
>
> *mine-voc lit Trustpilot, les widgets onsite, les threads Reddit pertinents et remplit pour chaque sous-groupe les douleurs exactes (le vrai mot qu'elles utilisent), les objections récurrentes, les expressions clés. C'est ce qui passe les audiences de l'hypothèse à du validé sourcé. ~30 min en arrière-plan, tu n'attends pas.*
>
> *produce-paid-angles consomme ensuite ces audiences enrichies pour sortir un set d'angles ranked, prêt à brief créa. Sans mine-voc d'abord, les angles sortent au mot près de mon chapeau, pas de tes clientes — c'est pour ça que je recommande l'ordre.*
>
> *Tu as aussi `/phantom {brand_slug}` à tout moment pour voir ces audiences avec leur niveau d'enrichissement.*
>
> *Mon avis : on lance mine-voc maintenant et on enchaîne sur les angles. Si t'as une deadline créa cette semaine et tu pousses direct sur les angles en hypothèse, dis-le, on ajuste. Et si t'as déjà des données existantes (reviews exportées, analytics, retours SAV) à m'injecter avant mine-voc, donne-moi le fact le plus dense en 1-2 phrases — ça nourrit le mining."*

The closing question fuses three options: lance mine-voc maintenant, pousse direct sur angles, ou existe data à injecter d'abord.

### Movement gate (technical)

Stage the proposal once Movement 3 is confirmed by the operator (after they pick the hierarchy). Movement 1 and Movement 2 are conversational, not gated:

```bash
python3 .skills/stage-proposal.py \
  --brand {slug} \
  --checkpoint audience_q1q4_answered \
  --summary "Audience hierarchy: {N parents} ({slugs}) + {M sub-audiences} ({slugs}). Axis: {pain-driven|situational|demographic}."
```

The `checkpoint-resolver` hook resolves the pending:
- Confirmation (`"oui"`, `"go"`, `"valide"`) → `audience_q1q4_answered = true` → Step 6 write unlocked.
- Rejection (`"non"`, `"on revoit"`) → pending cleared, re-propose hierarchy.
- Free-form corrections (`"on enlève chute-traction"`) → no automatic resolve. Apply correction in memory, re-stage, re-ask.

**Writing `audiences/{slug}/profile.json` is blocked by write-to-context until `audience_q1q4_answered = true`.**

### Thin-page fallback

If Movement 1 returns near-empty observations AND the operator skips Movement 2 (e.g. *"je sais pas, propose"*) → ask **one** single question:

> *"En une phrase : à qui tu vends et quel problème tu résous pour eux ?"*

Extract one mother audience from the answer. Skip Movement 3's sub-audiences entirely. Mark the single audience `validation_status: "hypothesis"`. Move to Movement 4. Resilience over completeness when the page is empty.

**Final rule**: Do not create an audience folder if both Movement 1 observations and Movement 2 operator input are empty. Block the write, surface the gap, suggest the operator paste a brief or run mine-voc on a competitor.

---

## Step 6 — Generate profile.json (base, delegated encoding)

Fill `brands/{slug}/audiences/{audience_slug}/profile.json` with:
- What comes directly from the product page (gender apparent in copy, problem addressed in title/description)
- What comes from Q1-Q4 answers
- Nothing else

**Hierarchy = N audience folders.** The Step 5 hierarchy validated by the operator typically yields 2-3 mother audiences + 1-3 sub-audiences each = 4-12 audience folders to scaffold. Scaffold each one. Mother audiences carry `meta.parent_slug: null` and `meta.scope: "broad"`. Sub-audiences carry `meta.parent_slug: "{mother-slug}"` and `meta.scope: "segment"` (or `"micro"` for hyper-niches).

**Encoding delegated to `encode-batch`.** Producer assembles per-audience observations from Step 5 (label, slug, scope, parent_slug, validation_status, gender, age_range, primary_problem, namespace-prefixed tags) and ships one encode-batch call per audience. Sub-agent maps and writes; producer continues to Step 7 synthesis without blocking.

**Field-level contract.** snapshot-brand fills only the cartography skeleton (full doctrine in `docs/system/audience-cartography.md § Field-level contract`):

```
meta.name              → human-readable label
meta.slug              → kebab-case slug
meta.scope             → broad | segment | micro
meta.parent_slug       → null for mother, slug-of-mother for sub
meta.validation_status → "hypothesis"
meta.audience_type     → "primary" | "secondary"
meta.tags              → ["problem:hair-loss", "context:post-pregnancy", ...] (namespaced)
identity.gender        → male | female | all (only if explicit on page)
identity.age_range     → {min, max} (only if explicit on page)
pain.primary_problem   → one-line statement (only if explicit on page or operator-stated)
```

Everything else stays null until `mine-voc` (verbatim → pain_points[].formulation, objections[], voice.key_expressions[], psychology.beliefs_limiting[]) or operator-driven enrichment.

**Hard rule.** snapshot-brand NEVER fills `pain_points[]`, `psychology.beliefs_limiting[]`, `psychology.beliefs_facilitating[]`, `voice.key_expressions[]`, `objections[]`, `behavior.*`, `psychology.emotions[]`. Inferring those fields from a product page is hallucination, even when the page mentions emotional language. Those fields are mine-voc territory.

---

## Step 7 — Operator-facing synthesis (mandatory format)

Before writing the files, deliver one **4-6 sentence analytical paragraph** that names what this product *is*, what *segment of the market it occupies*, and what *load-bearing decision the operator will make next* on this product. Use the schemas you just filled as **analytical vocabulary**, not as bullet points.

The paragraph must answer in implicit order, woven into prose:

1. **What this product really is** — beyond the category label. (*"not a sun stick, an anti-age stick disguised as sunscreen"*)
2. **Who buys it and why** — pain + trigger + sophistication, in plain prose. Use `problems_solved`, `audience.pain.primary_problem`, `market_context.sophistication` as raw material.
3. **What the offer architecture suggests** — pricing tier, subscription presence, bundle logic if any. Use `offer_groups[].offers[]` as raw material.
4. **The 1-2 things you noticed that the operator likely did not** — flags, gaps between brand-stated and observation-based fields, market positioning surprises.

End with one of two close patterns, depending on operator signal:

**Default close (operator hasn't signaled they want to skip validation):**

> *"Save this snapshot, or want to correct anything?"*

**Trust-and-deepen close (operator has signaled they trust the synthesis and want to go deeper):**

If the operator's reply to the synthesis carries trust signals (*"ok ça me va"*, *"go"*, *"trust c'est bon"*, *"valide tout"*), or if they explicitly ask for more depth, offer the deepening paths via AskUserQuestion (4 substantive options):

> Where do you want to go from here?
> - Validate point by point (15 min, you correct as we go)
> - Voice of Customer — what your real customers say (15 min, mine-voc)
> - Voice of Market — what the niche conversation reveals (25 min, mine-vom)
> - Full deepening (VoC + VoM + cross-synthesis, ~45 min, deepen-brand-context)

If none of those, the operator can also pull `study-niche-marketdeepdive` standalone (45 min strategic memo) — propose it only on direct ask, NOT in the default option set (cost asymmetry per v2.9.0 architecture decision).

If the page was thin (`_snapshot.confidence_score` internal flag low), say so in prose inside the synthesis (*"the page didn't give me much beyond the basic spec — your hero benefits and the anti-age angle I'm inferring from product context, not direct copy"*) — never expose the score as a number, never list "missing fields" as a separate block.

**Hard rules for the synthesis:**
- **Pure prose only.** No bullet list, no field enumeration, no bold-section anchors (no `**Le pitch**\n...\n\n**La cible**\n...`), no numbered headings, no scores, no completion percentages, no "Marque. ... Hero. ... Audience. ..." templated paragraph openers.
- Use schema field semantics as nouns and verbs (e.g. *"the trigger is X"*, not *"trigger_primary: X"*).
- Never name a file, a path, a skill, a confidence number, or an internal flag.
- If a schema field is null, do not mention it. The synthesis is what was learned, not what was missed.
- Inferred attributes flagged inline with *"(à valider)"* or *"(I deduced this, validate when you can)"* — never as a separate "missing fields" block.
- **Three movements, one blank line between each, no titles.** Movement 1 = what this product really is + who buys it and why (1-3 sentences). Movement 2 = what the offer architecture suggests + the market position (1-3 sentences). Movement 3 = the 1-2 things you noticed the operator likely did not (1-3 sentences). The blank lines provide visual breathing room. The titles are implicit — the structure carries itself through what each paragraph names. **Never add a bold heading or a label to mark each movement.**

**Decisive test before sending:** read the synthesis as a stranger. If you see **bold section labels**, numbered headings, or `Field. content. Field. content.` templated openers, you reverted to form-fill. Rewrite as flowing prose where each paragraph names what it carries via its first sentence, not via a label above it.

**Behavior on operator response:**
- **Confirm** (*"yes"*, *"go"*, *"spot on"*, *"ok"*) → write spec.json + offers.json + profile.json.
- **Correction** (*"price is 39€"*, *"audience is more men"*) → apply, regenerate the synthesis incorporating the correction, ask again.
- **Never write files before explicit confirmation.**

Once saved, run three silent post-writes before talking:

1. **Append to `brands/{slug}/pending-validations.md § Context gate`** one `[ ]` line per inferred field that was stamped with `mode=proposed` during this run. Wording in the operator's language, plain-language source tag (`(inferred from site)`, `(deduced)`), never `source` / `confidence` / `mode` jargon. Typical entries: audience(s) inferred, positioning inferred, tone inferred, compliance gaps detected (e.g. missing contraindications on a medical device).
2. **Trigger `validate-resources` silently** on the brand. This refreshes `status.json` (completeness per entity, freshness stamps, `wedge_complete`), rebuilds `learnings-index.json` if present, and re-runs the snapshot digest. Surface its result only if it flags MAJOR/CRITICAL — otherwise stay silent.
3. **Run `finalize-mutation-batch`** — single bash command, replaces the prior LLM-based coherence check (which was systematically skipped under load):

   ```bash
   python3 .skills/finalize-mutation-batch.py --brand-slug {slug}
   ```

   Reads `_field_types`, inspects every mutation written in this run, runs structural checks (unmapped paths, manual derived writes, tone misclassification, missing entity files), emits a `coherence_check` event so `turn-end-audit` sees the loop closed.

   Exit code 2 = blocking issue → revise before shipping the summary. Exit code 0 with warnings = log them, ship. **Non-negotiable, mechanical, not skippable.**

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
- **Shopify JSON API priority** over HTML for product data. Do not scrape HTML if `/products/{handle}.js` returns 200. Exception: product detail page scraping (above-the-fold, reviews, quantity breaks) always runs in complement to the API.
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
- **`finalize-mutation-batch` is mandatory before any operator-facing summary.** Step 7 post-write #3 runs `python3 .skills/finalize-mutation-batch.py --brand-slug {slug}`. Mechanical Python primitive — no LLM negotiation, no skip path. Exit code 2 = blocking issue, MUST revise. Soft-prescribed `validate-output-coherence` LLM call (prior version) was skipped 100% of the time under load on the v2.7.1 stress test; this is the replacement.

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
