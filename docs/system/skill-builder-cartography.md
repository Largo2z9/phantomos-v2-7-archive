# Skill-builder cartography — pattern for business-domain skills

> Guidance for building business-domain skills (audit, setup, roadmap, CRO, SEO, creative brief, competitor scan, etc.) in PhantomOS. Counters the anti-pattern "code the skill's method first, figure out where the data comes from later". The correct order is : map domain variables → identify gaps vs existing schema → extend the schema via `scaffold-extension` → THEN code the method.

## Why

A business-domain skill is a context consumer. If the context lacks the required granularity, the skill produces generic output. Example : an `audit-offers` that looks only at `offers.json` misses brand-level mechanics (GWP, shipping, referral, loyalty, funnels) — it misses 50% of the audit surface and returns flat recommendations.

The real PhantomOS moat : **structure grows with need**. Schemas extensible per domain, without adding core code. Skills consume structured data, not free text. For this to hold, cartography precedes method.

---

## The 5 phases of the pattern

### Phase 1 — Map domain variables

Exhaustively list everything that enters the expert judgment on the topic. For each variable, drill down to the atomic field an agent could read or write.

Example for `audit-offers` :

| Domain variable | Drill-down |
|---|---|
| Product offer | price, type (prepay/sub/bundle), cadence, quantity, discount, price_original |
| Brand-level promos | GWP thresholds, shipping rules, referral, loyalty, cart discounts |
| Positioning | niche, target audience, product time-to-value, acquisition phase |
| Competitive context | competitor offers, price anchoring, market category |
| Funnel | cart bumps, post-purchase, upsells, scarcity, urgency |
| Historical performance | AOV, LTV, conversion rate, subscription retention |

### Phase 2 — Identify gaps vs existing schema

For each variable in the cartography, check where it lives in the current schema. Three possible cases :

- **✅ Home exists cleanly** — variable lives in a native field (e.g., `spec.json#/pricing/price`)
- **⚠️ Home exists but incomplete** — an approximate field exists but doesn't capture the required granularity. Option : enrich the schema via sidecar `*.extensions.json`, OR flag as non-native and look for a custom home
- **❌ Orphaned** — no place in the current schema. Candidate for custom entity

### Phase 3 — 5-dimension gate (via scaffold-extension)

Before creating a custom entity, verify :

1. **Does the intent exist in core entities ?** Yes → route to core enrichment, not extension
2. **Can we extend sidecar `brand.extensions.json` or `{entity}.extensions.json` ?** Yes → sidecar, new entity not justified
3. **Can we map to a modified existing schema ?** Yes → modify core schema (breaking change — requires migration)
4. **Is a custom entity justified ?** (high cardinality, own lifecycle, scope different from core)
5. **Risk of redundancy with an existing entity ?** Check explicitly

All 5 pass → scaffold a custom entity.

### Phase 4 — Schema + instance proposal

scaffold-extension generates :

- `brands/{slug}/custom/{entity_name}/schema.json` — JSON Schema for the custom entity
- `brands/{slug}/custom/{entity_name}/{data}.json` — instance file to populate
- Validation rules + field types

The operator validates the schema before the instance is populated.

### Phase 5 — Registration in `index.json#/extensions[]`

```json
{
  "type": "custom_entity",
  "scope": "brand",
  "name": "commercial_mechanics",
  "schema": "brands/{slug}/custom/commercial_mechanics/schema.json",
  "instance": "brands/{slug}/custom/commercial_mechanics/mechanics.json",
  "cross_refs": [
    {"from": "reward.product_slug", "to": "brand.products_index[].slug"}
  ],
  "owner_skill": "snapshot-brand (detection) + capture-learning (manual enrichment)",
  "registered_at": "YYYY-MM-DD"
}
```

Registration = discovery contract for future skills. A skill like `audit-offers` can query `index.json → extensions[]` to know which custom entities to consume in addition to core entities.

---

## Worked example 1 — `commercial_mechanics` (Karacare)

**Context** : the Karacare snapshot detected 5 site-wide commercial mechanics (Spring Days GWP at 80€, free shipping at 69€, 15/15€ referral, loyalty points program, clone handles `*_sca_clone_freegift` for gift funnel). No home in `offers.json` (product scope only).

### Phase 1 — Cartography

Common variables across the 5 mechanics : trigger (cart/order/account condition), reward (type + value), scope (cart/order/account/product), active_from/to, source_urls.

Type-specific variables :
- GWP : `trigger.min_cart_value` + `reward.product_gift`
- Shipping : `trigger.min_cart_value` + `reward.free_shipping`
- Referral : `trigger.account_state` + `reward.discount_amount` (symmetric)
- Loyalty : `trigger.account_state` + `reward.points`
- Funnel clone : `trigger.product_required` + `reward.product_gift` (clone-linked)

### Phase 2 — Gap

No home in the 6 core entities (brand / product / offer / profile / learning / strategy). `brand.json` has a `commercial` block but the scope is too narrow. `offers.json` is product-scope only.

### Phase 3 — Gate

1. Does the intent exist in core ? No
2. Sidecar `brand.extensions.json` ? Bad fit — high cardinality, own lifecycle, frequent updates
3. Modify core schema ? Breaking change rejected
4. Custom entity justified ? Yes
5. Redundancy ? No, different from `offers` (cart/order-trigger vs SKU-prepay)

→ route-to-new-custom-entity.

### Phase 4 — Schema

`brands/karacare/custom/commercial_mechanics/schema.json` :

```json
{
  "_schema": "brand/custom/commercial_mechanic/1.0",
  "_version": "1.0",
  "type": "object",
  "required": ["mechanic_id", "type", "name", "active", "scope"],
  "properties": {
    "mechanic_id": {"type": "string", "pattern": "^MEC-[0-9]{3}$"},
    "type": {"enum": ["gwp", "shipping_rule", "referral", "loyalty", "funnel_clone", "cart_discount", "scarcity"]},
    "name": {"type": "string"},
    "active": {"type": "boolean"},
    "scope": {"enum": ["cart", "order", "account", "single_product"]},
    "trigger": {
      "type": "object",
      "properties": {
        "min_cart_value": {"type": "number"},
        "currency": {"type": "string"},
        "min_quantity": {"type": "integer"},
        "product_required": {"type": "array", "items": {"type": "string"}},
        "account_state": {"enum": ["referrer", "referee", "loyalty_member"]}
      }
    },
    "reward": {
      "type": "object",
      "properties": {
        "type": {"enum": ["product_gift", "discount_percent", "discount_amount", "free_shipping", "points", "credit"]},
        "value": {},
        "product_slug": {"type": "string"},
        "points_amount": {"type": "integer"}
      }
    },
    "active_from": {"type": "string", "format": "date"},
    "active_to": {"type": "string", "format": "date"},
    "source_urls": {"type": "array"},
    "notes": {"type": "string"}
  }
}
```

### Phase 5 — Registration

Registered in `brands/karacare/index.json#/extensions[]` (see Phase 5 of the main pattern).

### What this unlocks

A future `audit-offers` skill can now consume **both** :
- `offer_groups[].offers[]` → SKU-level analysis (prepay, cadences, discounts)
- `custom/commercial_mechanics/mechanics.json` → brand-level analysis (GWP thresholds, shipping, loyalty)

And cross both for a recommendation like : *"your Spring Days GWP at 80€ is too high vs estimated average cart X€ — 60% of carts don't reach it, you lose the anchoring effect"*. Business advice, not generic.

---

## Worked example 2 — [TO COMPLETE — high-stake candidate]

Three possible candidates, by order of business stake :

**A. Creative library** (high stake)
An entity tracking the creative library : concepts, angles, hooks, mediums, mentions per product/audience, performance per platform. Unlocks : `audit-creatives`, `brief-ads`, `competitor-creative-intelligence`, `angle-gap-detector`. Consumed by all creative/media skills.

**B. Funnel attribution** (medium-high stake)
Entity for tracking params, conversion paths, cart bumps, post-purchase, observed upsells. Unlocks : `audit-funnel`, `missing-upsell-detector`, `attribution-report`. More technical but critical for agency deliverables.

**C. Competitor intelligence** (medium stake)
Competitor entity with competitor-scoped creative library, positioning tracked over time, offer changes. Unlocks : `competitor-scan`, `positioning-drift`, `angle-steal`. Sensitive to data freshness.

**Decision log** : the choice of worked example 2 should reflect where the operator has the most current friction. Creative library is the likely pick if focus is media buying / agency.

---

## Anti-patterns to avoid

- **Dumping into `learnings.json`** — learnings = append-only facts, not a structured entity. If you have 5 structurally similar items, it's not a learning, it's a custom entity.
- **Overloading `brand.json`** — brand.json is identity, not catalog. If a field has cardinality N, it doesn't go directly in brand.json ; it goes into a sub-structure or a custom entity.
- **Polymorphic over-engineering** — a schema that accepts every input type via complex `oneOf` / `anyOf`. Beyond 3 distinct variants, split into separate entities.
- **Skipping Phase 1 cartography** — the most common mistake. Agent codes the method, then realizes 40% of the fields it wants to read don't exist, patches with free text. Output = generic.
- **Coding without registration** — a custom entity not registered in `index.json#/extensions[]` is invisible to other skills. De facto orphaned.

---

## When NOT to extend

- **One-off** — data a single skill consumes and that won't recur elsewhere. Put it as a skill argument, not an entity.
- **Temporary** — session context, not relevant next time. Use `session-state.md`.
- **External-only** — data that lives better in the external tool (e.g., analytics dashboards). Link via URL in learnings, do not duplicate.

---

## Cross-references

- `.skills/skills/scaffold-extension/SKILL.md` — the orchestrator implementing this pattern
- `docs/system/extending.md` — general extension doctrine
- `agent-design-guide.md` — building agents that consume custom entities
- D#330 (2026-04-19) — dual-mode scaffold-extension
- D#331 (2026-04-19) — "extend before create" rule
