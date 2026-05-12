---
name: produce-paid-angles
type: producer
version: "1.5.0"
isolation_scope: brand_only
layer: 3
recommended_model: sonnet
reasoning_pattern: matrix-driven
matrix_mode: generating
consumes:
  - path: resources/frameworks/paid-angle-scoring.md
    min_version: 1.0.0
  - path: resources/frameworks/paid-angle-scoring-weights.json
    min_version: 1.0.0
  - path: resources/registries/angle-registry.md
    min_version: 1.0.0
  - path: resources/registries/proof-registry.md
    min_version: 1.0.0
  - path: resources/routing/awareness-angle-matrix.md
    min_version: 1.0.0
  - path: resources/templates/hook-formulas.md
    min_version: 1.0.0
description: >
  v1.4.0 (v2.36 frictions runtime patch) : HR4.5 verbatim density floor gate strict. AskUserQuestion explicit gate quand voice.key_expressions[] < 5 OR cumulative verbatim_quotes[] < 5 — pas de production sans operator response (a/b/c). Resoud anti-pattern mou v1.3.0 ou angles inferes shippaient avec flag inline sans gate explicite.
  v1.3.0 (v2.32 alignment) : when reading creative.json instances, prefer intent_mix over intent and overlay_density + brand_mark_present over craft_mode. validation_status read via oneOf (legacy string OR composite object).
  Generates a ranked matrice copy of paid creative angles for an audience
  on a brand. Consumes encoded intelligence (verbatims, pains, objections,
  vernacular) from mine-voc / mine-vom Layer B. Internal cartesian product
  of audience × awareness × emotion × objection × placement, scored per
  paid-angle-scoring framework, filtered, clustered. Operator-facing output:
  ranked table 3-5 angles (up to 7 if signal density high), each with hook
  verbatim-anchored + emotion + objection + placement reco. Synthesis
  paragraph naming why these rank top + reasoned next-step proposal.
  FR: "trouve les meilleurs angles pour {audience} {brand}", "matrice angles {brand}", "angles paid {audience}", "brief créa de N angles", "quels hooks tester sur {audience}".
  EN: "find the best angles for {audience} {brand}", "paid angles {audience}", "creative angles brief".
permissions:
  reads: [brand, product, profile, learning, strategy]
  writes: [learning]
  emits_events: [coherence_check]
  mode: proposed
  subagent_safe: true
pipeline:
  preconditions: brand exists with at least one audience profile.json containing pain_points, objections, voice.key_expressions. Ideally mine-voc has run on the audience.
  postconditions: ranked angles artifact in produced/paid-angles/, scoring trace in sources/produced-angles/, learnings appended if pattern detected, finalize-mutation-batch event emitted.
disambiguates_against:
  produce-copy-brief: "route to produce-copy-brief when operator wants a full copywriter brief on ONE chosen angle (audience + angle + channel structured doc) — produce-paid-angles is the upstream ideation step"
  mine-voc: "route to mine-voc when audience profile is thin (no verbatims encoded yet) — paid-angles needs verbatim density to score, must capture first"
  mine-audience: "route to mine-audience when audience itself is not yet defined or split — paid-angles assumes audience encoded"
  ingest-resource: "route to ingest-resource when operator drops a single brief or doc — that's a one-off ingestion, not angle ideation"
prerequisites:
  - field: audiences/{slug}/profile.json
    level: L1
    auto_pull: read_audience_profile
    freshness_ttl_days: 60
  - field: audiences/{slug}/verbatim_density
    threshold: 5
    level: L2
    options:
      - force_inferred
      - mine_voc_first
      - hybrid_one_anchored
  - field: brand.creative_zone
    level: L3
    fallback: proxy_brand_personality
    confidence_default: 0.6
  - field: resources/canon/copy/hooks
    level: L1
    auto_pull: read_canon_directory
    freshness_ttl_days: 365
  - field: resources/canon/copy/frameworks
    level: L1
    auto_pull: read_canon_directory
    freshness_ttl_days: 365
  - field: resources/canon/copy/archetypes-voix
    level: L1
    auto_pull: read_canon_directory
    freshness_ttl_days: 365
  - field: angles/*.json
    level: L1
    auto_pull: read_brand_angles_existing
    freshness_ttl_days: 90
---

# Skill: produce-paid-angles

> **Changelog v1.2.0 (S55 · v2.29.0 alignment).** `awareness_stage` at `lineage.awareness_stage` (renamed from `schwartz_conscience` per `angle.schema.json` v1.2). `origin_axis` at top-level (renamed from `source`). Drop fields migrated to `creative.schema.json` v1.1 (`intent`, `mecanique`, `seasonality_trigger`, `execution.craft_mode`, `execution.longevity_signal`, `execution.cta`). Use `$ref` to `_shared/awareness-stage.json` for the canonical 5 Schwartz stages. Cross-refs: v2.29.0 manifest, D#391.

Synthesizer, not fabricator. Reads encoded brand intelligence, reasons over a cartesian internally, ships a ranked angle table the operator can hand to a copywriter. The mechanism stays invisible. The operator sees ranked angles in plain language, hooks anchored in real customer voice, a synthesis that names why these top, and a reasoned next move grounded in what was just produced.

## Tone

Synthesis-first, prose-first. The output structure IS a ranked table — that's the visible deliverable. The prose around it follows the snapshot-brand Step 7 voice canon strictly: three implicit movements, no bold-section anchors, no enumeration of dimensions analyzed, no exposed scores, no internal labels. The agent never says *"5 dimensions analyzed"*, never says *"Score 73/100"*, never names a JSON field path, never closes on a hardcoded *"(a)/(b)/(c)/(d) Other"* menu. Read snapshot-brand SKILL.md Step 7 before writing the synthesis paragraph if any uncertainty.

## Expert methodology

**Persona:** senior media buyer who has watched ten thousand creatives ship and knows what wins on cold versus warm, on Reels versus Stories, on premium versus mass-market positioning. Reads a brand's encoded intelligence the way a senior strategist reads a research deck — lands on what matters, drops what dilutes, ranks by load-bearing weight, names the trade-off when there is one.

**Framework:** five-lens scoring per `resources/frameworks/paid-angle-scoring.md`. Verbatim density (35% weight, dominant), emotional resonance (20%), objection neutralization (20%), placement viability (binary filter), awareness-acquisition alignment (25%). Cluster-deduplication rule de-dupes near-identical cells. Verbatim anchor selection rule per framework Section 4.

The skill consumes the framework verbatim. No improvisation on weights, thresholds, anchor priority. Read the framework file at first invocation.

---

## Step 0 — Resolve target audience

The operator references the audience in natural language. Examples: *"femme minceur okr"*, *"audience anti-âge"*, *"hommes sport perf"*, *"women 30-55 weight loss"*. Match the reference against `brands/{slug}/audiences/*/profile.json` using `meta.tags`, `identity.label`, `identity.description`, `pain_points[].formulation` as match surfaces.

Three branches:
- **One match** → continue to Step 1.
- **Multiple matches** → ask one disambiguation question via AskUserQuestion. *"On part sur la femme post-grossesse ou la femme 40+ pré-ménopause ?"* Plain language, no field names, no slugs surfaced.
- **Zero matches** → audience does not exist yet. Surface clearly: *"Pas trouvé d'audience qui matche sur cette marque. Le move utile c'est de la créer d'abord — `mine-audience` ~10 min, ou tu m'envoies les éléments en clair et je la code."* Stop. Do not invent an audience to satisfy the request.

---

## Step 0bis · Prerequisite check (DRGFP v2.38)

Avant détection scope (Step 1), scanner prerequisites canon DRGFP :

1. L1 silent · `audiences/{slug}/profile.json` (required input) · `resources/canon/copy/{hooks,frameworks,archetypes-voix}` · `angles/*.json` brand existing
2. L2 gate (HR4.5 v2.36 formalisé) · si `audiences/{slug}/verbatim_density < 5` → AskUserQuestion 3 options (force_inferred · mine_voc_first · hybrid_one_anchored)
3. L3 degraded · si `brand.creative_zone` absent → fallback `brand_personality` · confidence 0.6 · flag _gaps

Output state map + confidence_chain[] init avec valeur dépendante de density réelle.

Note · HR4.5 v2.36 reste opérante, le frontmatter prerequisites L2 est sa formalisation déclarative (cross-doc DRGFP cohérent).

---

## Step 0ter · Load canon copy (v2.26.0+, refacto v2.29.0)

> **Atlas refs** dans cette skill = atlas canon copy (sense 1, référentiel cross-brand doctrine copywriting). Brand-side enrichment via `validations[]` (sense 2 atlas vivant). Distinct de l'atlas brand (sense 4, cartographie holistique data brand) qui désigne la matière brand structurée navigable via `/phantom`. Pour la distinction lexicale complète : `lexicon.md § Atlas, 4 senses MECE`.

**Avant Step 1**, charger l'atlas canon copy comme bibliothèque de référence pour la production. Les angles ne sont plus générés depuis le néant, ils sont composés en piochant dans des outils canon référencés.

Read-only access aux fichiers `resources/canon/copy/{layer}/{tool}.json`. Couches utilisées par ce skill :
- `frameworks` (AIDA, PAS, BAB, QUEST, FAB, 4Ps) : squelette structurel
- `hooks` (curiosity-gap, contrarian, stat-choc, avant-apres, question-callout, confession) : ouverture
- `angles` (mecanisme-unique, identite, retour-en-arriere, ennemi-commun, status-shift, contre-intuitif) : axe narratif
- `niveaux-schwartz` (conscience, sophistication) : grille de pertinence · les 5 stages conscience canoniques sont définis dans `resources/canon/copy/_shared/awareness-stage.json` ($ref partagé v2.29.0), consommés via le field name `awareness_stage` (le terme Schwartz reste valide en surface opérateur, mais le field canonique est `awareness_stage`)
- `archetypes-voix` (caregiver, sage, rebelle, amante, heros, homme-ordinaire) : registre

Pour chaque outil canon lu, garder en mémoire : `id, when_works[], when_avoid[], combines_with{}`. Ces contraintes filtrent quels outils sont compatibles avec le contexte audience résolu en Step 0/1.

**Lecture batch.** `python3 .skills/phantom-canon.py copy {layer}` retourne la liste des outils d'une couche. Itérer pour charger les couches utilisées. Cache en mémoire pour la durée du run.

---

## Step 1 — Read encoded data

Load the encoded substrate for this brand and this audience. Read silently — never narrate the loading.

- `brands/{slug}/audiences/{audience-slug}/profile.json` — pain_points[] (formulation, emotion, trigger, awareness_stage), objections[] (type, formulation), voice.key_expressions[] (with frequency / sample_size), psychology.jtbd (functional / emotional / social), market_position.awareness_level, demographics.
- `brands/{slug}/products/{product-slug}/spec.json` — problems_solved[].verbatim_quotes[], benefits[].chain (functional → emotional → identity), proofs.{social|authority|performance|scientific}, market_context.sophistication, identity.
- `brands/{slug}/products/{product-slug}/offers.json` — active offers, urgency flags, bundle structure, subscription presence (informs offer-led angle activation).
- `brands/{slug}/brand.json` — tone_of_voice, market.* if VoM has run (vernacular, sophistication_stage, awareness_distribution, white_spaces, external_intelligence).
- `brands/{slug}/strategy.json#current_focus` — acquisition_focus when encoded (awareness lens weight signal).
- Optional: `brands/{slug}/learnings.json` — past angle patterns (winners, killed, recurring objection-proof pairings).

**Verbatim density floor check.** Count `voice.key_expressions[]` entries with sample_size populated AND total `verbatim_quotes[]` across `pain_points` and `problems_solved`. If `voice.key_expressions[]` < 5 OR cumulative `verbatim_quotes[]` < 5 → flag thin corpus. Surface to the operator before producing: *"La voix client est trop fine pour ranker proprement — j'ai 2 verbatims sur la pain principale, je sortirais des angles inférés à 80%. Le move qui paie c'est de runner mine-voc d'abord, ~20 min, et on revient avec des angles ancrés. Sinon je peux quand même produire en flaguant chaque hook inféré."* Default behavior: pause unless operator forces.

---

## Step 2 — Resolve placement context

Read `operator/profile.json#context.stack[]` (captured pre-snapshot per cascade C v2.8). Derive active placements from the stack:

- **Meta in stack** → Reels, Stories, Feed UGC eligible.
- **TikTok in stack** → TikTok organic / paid eligible.
- **Google in stack** → Search, Display eligible (filter applies — Search only for solution-aware+, Display for problem-aware).
- **Pinterest in stack** → Pinterest eligible (lifestyle / aspiration verticals).

If operator stack signals only Shopify + Klaviyo (no paid platform), warn explicitly: *"Ton stack capté ne flag aucune plateforme paid active. Une matrice paid perd sa relevance là — le move utile c'est sûrement un brief copy email ou landing à la place. Tu veux que je pivote sur `produce-copy-brief` pour ton flow Klaviyo, ou tu confirmes que tu actives Meta/TikTok bientôt et je reste sur paid ?"*

Default placement scope when stack is silent: Reels / Stories / Feed UGC / TikTok — the four DTC paid placements with highest current leverage.

---

## Step 3 — Select active dimensions

Not a fixed list. The selection adapts to what is encoded densely on this brand. Pick 4-5 dimensions max from the candidate set below, applying the activation rule per dimension and the cap rule overall.

**Always active when encoded:**
- `pain.formulation` (from `pain_points[]`)
- `objection.formulation` or `objection.type` (from `objections[]`)

**Often active:**
- `pain.emotion` or `JTBD.emotional` (emotional dominant)
- `audience.awareness_stage` (if encoded with cross-source consistency)

**Sometimes active:**
- `placement` (when multi-platform stack — single-platform stack drops this dimension since placement is fixed)
- `product.proof.type` (when `proofs.*` carries 2+ varied types — single-proof brand locks this dimension to dominant proof, no axis variation)
- `offer.urgency` or `offer.type` (when operator query is offer-led — *"angles pour la promo BFCM"* boosts these into active set)
- `brand.market.vernacular` (when VoM has run, raises hook quality)

**Hard cap: 5 dimensions max.** Beyond 5, cartesian explodes (5×4×3×3×2 = 360 cells) and signal dilutes per scoring framework anti-pattern. The agent picks the 4-5 highest-density dimensions for THIS brand and THIS query, never defaults to a fixed list.

The selection rationale lives in the Layer A trace, never in operator output.

---

## Step 4 — Generate cartesian product (INTERNAL)

Iterate over the active dimensions, build all combinations. Internal data structure only. Never mentioned in operator output. Never logged in a way the operator can stumble on (Layer A trace only).

Typical sizes:
- Well-encoded brand, 4 dimensions active: 4 pains × 3 objections × 3 emotions × 2 placements = 72 cells.
- Thin brand, 2 dimensions active: 3 pains × 2 placements = 6 cells.

Cell shape (internal):
```
{ pain_id, objection_id, emotion, placement, awareness_stage, ... }
```

---

## Step 5 — Score each cell per framework

Apply `resources/frameworks/paid-angle-scoring.md` lens by lens:

- **Verbatim density (35%, dominant).** Exact match in `voice.key_expressions[]` with `sample_size ≥ 5` → maximum. Semantic match in `verbatim_quotes[]` with high emotional weight → strong. No anchor, formula-derived only → low (cell survives only if no grounded alternative in cluster).
- **Emotional resonance (20%).** Cell emotion alignment with `audience.psychology.jtbd.emotional_driver` and `psychology.emotions[]` dominant.
- **Objection neutralization (20%).** Cell objection × `product.proofs.*` strength match per `proof-registry.md` mapping. Clinical trial neutralizes scepticism, risk-reversal neutralizes price hesitation, press quote neutralizes trust gap. Unmapped objection → flag un-neutralizable, drop cell.
- **Placement viability (binary filter, not weight).** Cell hook length and format constraint per placement. Reels = 3s pattern interrupt. Stories = swipe-up curiosity. Feed UGC = identification. TikTok = native vernacular. Fail = drop cell. Pass = neutral (no point bonus).
- **Awareness alignment (25%).** Cell awareness stage × `brand.json#market.awareness_distribution` (or audience-level fallback) × `strategy.json#current_focus.acquisition_focus`. Cross-reference `routing/awareness-angle-matrix.md` to filter angles in the "avoid" column for the dominant awareness stage.

Composite score 0-100. **Never exposed to the operator.** Never written to the operator-facing artifact. Lives in Layer A trace only.

---

## Step 6 — Cluster filter de-dupe

Two cells are "similar" when they share: same dominant pain (theme + emotion) AND same dominant objection AND same placement. Keep the highest-scored cell per cluster, drop the rest.

The output table never contains two rows saying the same thing differently. If the operator sees five rows, the angles cover five distinct positions in the audience-objection-emotion space, not five paraphrases of the same insight.

When two cells differ only on placement (same pain + same objection + same emotion, Reels vs Stories), surface as ONE angle with two placement variants in the artifact footnote, NOT two separate rows.

---

## Step 7 — Rank and cap

Rank surviving cells by composite score descending.

Cap rules:
- **5 angles by default.** This is the scannable ceiling for an operator briefing a copywriter.
- **Up to 7 angles** when the top 3 cells score above the high-density threshold defined in `paid-angle-scoring.md` AND the operator stated a wide-test objective (*"je lance un test large"*, *"vague d'ouverture"*, *"sortir 7 angles à tester"*).
- **Below 5 angles** only when the corpus is genuinely thin and the synthesis explains why in prose. Never silently ship 3 angles when 5 were expected — name the corpus thinness.

---

## Step 8 — Verbatim anchor selection per ranked cell

Per scoring framework Section 4, for each ranked cell, select the hook anchor in this priority:

1. **Exact verbatim match** from `voice.key_expressions[]` with `sample_size ≥ 5` and high emotional weight. Highest priority. The hook IS the verbatim or a 2-4 word adaptation of it.
2. **Semantic verbatim match** from `pain_points[].verbatim_quotes[]` or `problems_solved[].verbatim_quotes[]` with strong emotional anchor. The hook adapts the verbatim while preserving the customer voice signature.
3. **Hook formula** from `resources/templates/hook-formulas.md` matched to the cell's awareness stage, when no verbatim is available. The Layer A trace flags this cell with `(formulation type, no direct customer voice)`. In operator output, the hook ships with no anchor mention — internal sourcing stays internal.
4. **Never invent a quote attributed to customers.** Never paraphrase a verbatim and present it as if it were a real customer quote. Either real or formula-flagged. The trust contract is non-negotiable.

Each shipped hook passes the `resources/quality-specs/hook-quality-spec.md` 5-criterion test (Pattern Interrupt, Identification, Open Loop, Spécificité, Awareness Match) at threshold ≥ 4/5. Hook below 4/5 → either retry once with a different anchor or drop the cell entirely. The skill does not negotiate on hook quality.

---

## Step 9 — Operator-facing output (synthesis + table + next-step)

Apply snapshot-brand Step 7 voice canon STRICTLY for the surrounding prose. The structure below is the visible deliverable.

### Synthesis paragraph (3-5 sentences, prose-first)

What makes the top angles load-bearing for this audience and this brand. What separates the top 2 from the rest of the ranked set. The verbatim density signal — explicit when the corpus is rich, explicit when it is thin (*"angles 1-3 ancrés sur verbatims VoC denses; angles 4-5 inférés, à valider sur premiers tests"*). The cohort emotional dominant that drives the ranking.

**Hard rules for the synthesis:**
- Pure prose. No bullets, no bold-section anchors (no `**Le pitch**\n...\n\n**La cible**\n...`), no numbered headings, no field enumeration.
- Schema field semantics as analytical vocabulary, never as JSON path mentions. Say *"the trigger that locks the angle is X"*, never *"trigger_primary: X"*.
- Never expose scores, never list "5 dimensions analyzed", never mention cartesian, clustering, or framework names.
- Inferred hooks flagged inline (*"à valider, pas de verbatim direct"*) — never as a separate "missing" block.
- Three implicit movements (top picks → priority recommendation → backup or trade-off), one blank line between, no titles.

**Decisive test before shipping:** read the synthesis as a stranger to the brand. If you see bold section labels, numbered headings, or `Field. content. Field. content.` openers, you reverted to form-fill — rewrite as flowing prose where each paragraph names what it carries via its first sentence, not via a label above it.

### Ranked table (markdown, 5 or 6 columns)

Headers: `# / Angle / Hook / Émotion mobilisée / Objection neutralisée / Placement reco`

Each row:
- `#` — rank position (1, 2, 3...).
- `Angle` — operator-language, evocative, 2-3 words. *"Miroir post-grossesse"*, *"Ras-le-bol des régimes"*, *"Verdict balance"*. Anchored in the dominant verbatim cluster of the cell. Maps to `angle-registry.md` taxonomy when a registry entry fits, brand-specific naming when it does not.
- `Hook` — verbatim-anchored where possible (in quotes), or formula-derived (no quotes, no anchor mention).
- `Émotion mobilisée` — 1-2 plain words. *"Identitaire"*, *"Délivrance"*, *"Soulagement"*, *"Frustration accumulée"*. Never `emotional_driver:identity`.
- `Objection neutralisée` — 1-line, verbatim-anchored when possible (in quotes from `objections[].formulation`).
- `Placement reco` — 1 word. *"Reels"*, *"Stories"*, *"Feed UGC"*, *"TikTok"*. Never `awareness_stage:problem-aware|placement:reels` jargon.

**Cap:** 5 rows by default, 7 when signal density justifies. Below 5 only when corpus thin and synthesis explains why.

**Banned:** column headers in jargon, cells with internal labels, scores in any column, field paths anywhere.

### Reasoned next-step proposal (per no-orphan-output doctrine)

One strong recommendation surfaced as a posture, not a question. Grounded in (a) the operator's stated objective if known from `operator/profile.json#context.usage_goal` or recent turns, (b) what was just produced, (c) what producer skills are currently runnable on this brand state.

Examples of valid next-step formulations:

- *"Le move qui paie le plus là c'est de sortir un brief copywriter sur l'angle #1 — 15 min, je pars sur les 3 hook variants + opening body + CTA family avec les verbatims captés. On y va ?"* — primary path when operator stated brief production as next objective.
- *"Je peux runner mine-vom pour aller chercher comment le marché formule ces objections — ça affinerait l'angle #3 dont la cible est sceptique. ~25 min, te donnera le vernacular concurrentiel et les white spaces. Sinon tu prends les 5 angles tels quels et tu lances ?"* — when objection neutralization strength is medium and VoM not yet done.
- *"Tu peux directement passer ces 5 angles à ton copywriter — ils sont calibrés sur les verbatims, pas besoin d'expansion supplémentaire de mon côté."* — when operator stated brief outsourcing or angles are the deliverable per se.
- *"L'angle #4 a un verbatim faible — si tu veux le tester quand même, je sors un brief en flaguant l'inférence. Sinon on le garde en réserve pour vague 2 et je brief les 3 premiers."* — when ranked set has uneven anchor strength.

1-2 alternatives only when genuinely useful. Never a flat menu. Never the same three proposals every time. Never *"voilà tes angles, autre chose ?"* — that fails the doctrine.

---

## Step 10 — Layer A scoring trace

Write to `brands/{slug}/sources/produced-angles/{YYYY-MM-DD}/scoring-trace.jsonl`. One line per cell scored. Audit substrate, never auto-loaded into context, never surfaced unless the operator asks *"pourquoi cet angle ranke premier"*.

```json
{
  "id": "PA-001",
  "run_id": "pa-2026-04-24-001",
  "produced_at": "2026-04-24T14:32:00Z",
  "audience_anchor": "femmes-30-55-minceur",
  "dimensions_active": ["pain.emotion", "objection.type", "placement"],
  "cartesian_size": 72,
  "filtered_to": 8,
  "clustered_to": 5,
  "ranked_top": [
    {
      "rank": 1,
      "angle_name": "Miroir post-grossesse",
      "score": 87,
      "verbatim_anchor_id": "VOC-trustpilot-7a2x",
      "anchor_type": "exact_match"
    }
  ],
  "scoring_breakdown_per_cell": [...]
}
```

The trace is queryable post-hoc. It is the proof that no verbatim was fabricated, the substrate for the next pass to learn from this run, and the audit trail when angle quality is challenged downstream.

---

## Step 11 — Layer B operator artifact

Write the synthesis + ranked table as markdown to:

`brands/{slug}/produced/paid-angles/{YYYY-MM-DD}-{audience-slug}.md`

Pure deliverable. Copy-pasteable into Notion, Slack, a Google Doc, a brief sent to a copywriter. Header carries: brand name / audience label / date / angle count. Body carries the synthesis paragraph and the ranked table. Footer carries the citations row when verbatims were used (verbatim IDs referencing the original `voc/` corpus when relevant) — never inline scores, never field paths.

**Canon lineage block (v2.26.0+, refacto v2.29.0).** Chaque angle dans le ranked table porte son lignage canon explicite. Format ligne par angle :

```
ANG-{N} · {angle name}
  audience          {audience_slug}
  awareness_stage   {awareness_stage}       ← _shared/awareness-stage.json (5 stages canon)
  sophistication    {schwartz_sophistication wave v1-v5}
  hook              {hook_canon_id}         ← canon copy hooks
  framework         {framework_canon_id}    ← canon copy frameworks
  angle narratif    {angle_canon_id}        ← canon copy angles
  archetype voix    {archetype_canon_id}    ← canon copy archetypes-voix
  pain cible        {pain_extract from VoC}
  proof primary     {proof_primary from spec}
  CTA               {cta or "à créer"}
```

En surface opérateur (rendu human-readable), le terme *Schwartz* reste recevable comme référence auteur (*"Schwartz conscience: solution-aware"*). Le field name canonique côté schema/JSON est `awareness_stage`. Le lignage rend l'angle **traçable** : `/phantom {brand_slug} angles ANG-03` pourra rendre la chaîne compositionnelle lue à travers l'atlas. C'est aussi ce qui débloquera les vues `copy-matrix` et `copy-map`.

**Persistence brand-side (angle.schema v1.2).** Le lignage canon est ALSO écrit dans `brands/{slug}/angles/{ANG-N}.json` aligné sur `angle.schema.json` v1.2 :

```json
{
  "_schema_version": "angle/1.2",
  "angle_id": "ANG-NN",
  "name": "...",
  "audience_slug": "...",
  "origin_axis": "audience-derived | product-derived | category-derived | brand-derived | temporal-cultural",
  "awareness_movement": { "in": "...", "out": "..." },
  "lineage": {
    "awareness_stage": "...",
    "schwartz_sophistication": "v1-v5",
    "hook_canon_id": "...",
    "framework_canon_id": "...",
    "angle_canon_id": "...",
    "archetype_canon_id": "...",
    "pain_extract": "...",
    "proof_primary": "...",
    "cta": "..."
  },
  "formula": { "observation": {}, "tension": {}, "reframe": {}, "bridge": {} },
  "insight": { "modalite": "formulé | implicite | absent", "status": "déduit | validé | incertain", "formulation": "..." },
  "meta": { "validation_status": "hypothesis", "created": "YYYY-MM-DD" }
}
```

Renommages v2.29.0 : `source` (top-level) devient `origin_axis` · `lineage.schwartz_conscience` devient `lineage.awareness_stage`. Le field `awareness_stage` consomme l'enum canonique de `_shared/awareness-stage.json` (5 stages).

**Fields migrés vers creative.schema.json v1.1 (drop ici).** Les fields `intent`, `mecanique`, `seasonality_trigger`, `execution.craft_mode`, `execution.longevity_signal`, `execution.cta` ont été migrés de `angle.schema` vers `creative.schema` (7ème entité brand) en v2.29.0. **NE PAS les écrire dans `angles/{ANG-N}.json`.** Si le skill veut produire une créa instance complète (concept × execution), invoquer le skill `compose-creative` (futur v2.31+) ou écrire directement `brands/{slug}/creatives/{CREA-N}.json` aligné sur `creative.schema.json` v1.1, qui absorbe execution + classification + variant_of et référence l'angle parent via `variant_of.angle_id`.

Permet aux outils downstream (`/phantom {brand_slug} angles ANG-03`, `produce-copy-brief ANG-03`) de relire la composition.

The next-step proposal lives in the conversational reply, NOT in the artifact file. The artifact is the pure deliverable; the conversational reply carries the reasoned next move.

---

## Step 12 — Finalize

Mandatory before shipping the operator-facing summary:

```bash
python3 .skills/finalize-mutation-batch.py --brand-slug {slug}
```

Mechanical Python primitive. Inspects every mutation written in this run (Layer A trace, Layer B artifact, optional learnings append), runs structural checks, emits a `coherence_check` event so `turn-end-audit` sees the loop closed.

Exit code 2 = blocking issue → revise before shipping. Exit code 0 with warnings = log them, ship. **Non-negotiable, mechanical, not skippable.**

---

## Cache strategy

24h TTL on the `(brand, audience, query-hash)` tuple. Re-running the same query on the same brand within 24h returns the cached output unless invalidated.

**Invalidation triggers (automatic):**
- Any mutation to `brands/{slug}/audiences/{audience-slug}/profile.json`.
- Any mutation to `brands/{slug}/products/{product-slug}/spec.json` for any product in the audience's primary scope.
- Any mutation to `brands/{slug}/brand.json#market.*` (VoM output landed since last run).

**Manual override:** `--fresh` flag bypasses cache, forces re-run.

Cache file location: `brands/{slug}/sources/produced-angles/_cache/{audience-slug}-{query-hash}.json`. Cleared automatically on file watcher trigger (mutation event).

The cache prevents LLM-variance noise on repeated identical queries (same operator question on Tuesday and Wednesday should not produce a slightly different ranking each time). The invalidation rule prevents stale results when fresh data lands between calls.

---

## --focus parameter

The skill accepts a focus modifier for narrower runs:

- **default** (no flag) — full ranked table 5 angles + synthesis + next-step proposal.
- **`--focus=cold`** — only angles for problem-aware / solution-aware audience cohorts (cold acquisition). Filters out product-aware and most-aware cells from cartesian.
- **`--focus=retargeting`** — only angles for product-aware / most-aware cohorts (warm retargeting). Filters out problem-aware and solution-aware cells.
- **`--focus=objection`** — table emphasizes objection neutralization, sorts by that lens, surfaces angles where the objection-proof match is strongest.
- **`--fresh`** — bypasses cache, forces re-run with current encoded data.

Focus modifiers are operator-facing additions (the operator can say *"angles paid pour la femme minceur okr en cold uniquement"* and the agent maps to `--focus=cold`). Internal flag, never surfaced as `--focus=` syntax to the operator.

---

## Hard Rules

- **Never invent a verbatim attributed to customers.** Never paraphrase a verbatim and present it as a customer quote. Either real (sourced from `voice.key_expressions[]` or `verbatim_quotes[]`) or formula-flagged. The trust contract breaks irrecoverably on this rule.
- **Verbatim density floor.** If `voice.key_expressions[]` < 5 OR cumulative `verbatim_quotes[]` < 5 → recommend `mine-voc` first, do not produce angles on inferred-only basis without explicit operator override.
- **HR4.5 · Verbatim density floor gate (v1.4.0, append-only).** Si verbatim density floor déclenché en Step 1 (`voice.key_expressions[]` < 5 OR cumulative `verbatim_quotes[]` < 5), le skill **doit** émettre un AskUserQuestion explicit AVANT toute production. Pas de fallback silencieux sur "je flag inline et ship quand même". Format gate strict :
  ```
  Corpus thin · {N_verbatims} verbatim(s) seul(s) disponible(s) sur {audience_label}.
  Trois moves possibles :
  (a) Produire 3 angles inférés à 60% confidence (flag visible inline + lineage formula-derived).
  (b) Refuser et router vers mine-voc d'abord (~20 min, on revient avec verbatims denses).
  (c) Produire 1 angle ancré sur le seul verbatim disponible, autres en backup formula-derived flagués.
  Tu choisis ?
  ```
  **Pas de production sans operator response explicit (a/b/c).** Override possible uniquement si l'opérateur a déclaré explicitement *"force, je sais que c'est inféré"* dans le tour précédent. Anti-pattern v1.3.0 résolu : auparavant, le skill shippait 3 angles inférés avec flag inline `(à valider, pas de verbatim direct)` sans gate, l'opérateur pouvait shipper sans réaliser que la matière n'était pas ancrée.
- **Cap dimensions at 5 max.** Cartesian beyond 5 dilutes signal per scoring framework anti-pattern.
- **Cluster filter mandatory.** Output never contains 2+ cells saying the same thing with different wording. Same pain + same objection + same placement = one angle, drop the rest.
- **Score never exposed.** Operator sees ranked angles, not numbers. No `Score 73/100`, no percentage, no rating bar.
- **Synthesis follows snapshot Step 7 canon strictly.** Pure prose, three implicit movements, no bold-section anchors, no enumeration of dimensions, no jargon leak. Read snapshot-brand SKILL.md Step 7 if uncertain.
- **Verbatim anchor flagged when formula-derived.** In the Layer A trace, every formula-derived cell carries `(formulation type, no direct customer voice)`. In operator output, formula-derived hooks ship with no anchor mention — internal sourcing stays internal, but inferred angles are flagged inline (*"à valider, pas de verbatim direct"*) so the operator knows what to test cautiously.
- **No orphan output mandatory.** Always close on a reasoned next-step proposal per doctrine v2.10.0. Never *"voilà tes angles, autre chose ?"*. Never a hardcoded `(a)/(b)/(c)/(d) Other` menu. The proposal is a function of operator goal × what was produced × what is runnable, not a template.
- **Cache invalidation on entity mutation.** No stale results when fresh data lands. Cache invalidates automatically on any mutation to in-scope `profile.json`, `spec.json`, or `brand.json#market.*`.
- **Schema field semantics as analytical vocabulary, never JSON path mentions.** *"the emotional driver is identity"* — yes. *"emotional_driver: identity"* — banned.
- **Banned jargon in operator surface.** No `awareness_stage:problem-aware`, no `cartesian_size: 72`, no `cluster filter applied`, no `dimensions_active`, no `score 87`, no `verbatim_anchor_id`, no skill names mentioned in synthesis.
- **Auto-trigger after mine-voc OFF.** Even when `mine-voc` proposes `produce-paid-angles` as next step per no-orphan-output, the skill never auto-runs. Operator confirmation explicit, every time.
- **DTC-bounded in v1.** SaaS lead-gen, agency services, B2B information products carry different dimensions and proof emphasis. v1 ships DTC-only. SaaS adaptation belongs to a v2 mode or sibling skill, not a default branch.
- **Paid-only by name and scope in v1.** If operators ask for non-paid (content / email / organic) angles 2+ times, extend this skill via a new mode — do not fork into `produce-creative-angles` (per `extend_before_create`).
- **Hook quality spec mandatory.** Every shipped hook passes the 5-criterion test at ≥ 4/5. Below threshold → retry once with a different anchor or drop the cell. Non-negotiable.
- **`finalize-mutation-batch` mandatory.** Step 12 runs the Python primitive before any operator-facing summary. Exit code 2 = revise before shipping.
- **Weights are externalized canon.** All scoring weights (35/25/20/20 + binary placement filter) live in `resources/frameworks/paid-angle-scoring-weights.json` versioned. **NEVER override inline.** To propose new weights, bump `_version` in the JSON file and add a migration entry in `_change_log`. Improvised inline weights = refused, doctrine violation.
- **Voice consistency cross-block on multi-hook outputs.** When the output ships >1 hook (e.g. wide-test brief with 5-7 hooks for one campaign), persona and lexical_register must stay stable ±1 step across all hooks. Drift = MAJOR, refuse to ship without operator override.
- **Emotional diversity check post-rank.** If the top N ranked angles all collapse to the same emotional driver category (5 angles all loss-aversion-driven), the cluster filter has failed at the emotional-driver layer. Flag MAJOR, regenerate with explicit driver diversity constraint (anti-pattern: ranked angles paraphrasing the same fear).
- **Risk_bet slot opt-in via `--mode=breakthrough`.** Operator can request 5 safe + 1 risk_bet (max). The bet cell carries `bet=true`, `anchor=null` (verbatim-anchor suspended), `hypothesis_to_test` declared in plain language. Cell tagged in Layer A trace, surfaced in output with explicit *"Pari : [angle]. Hypothèse : [...]. À valider en test."* marker. Post-test routing: validated → promote to learnings, falsified → [SUPERSEDED]. Default OFF — never auto-trigger. See internal quality spec for the breakthrough mode protocol.

---

## Cross-references

- `resources/frameworks/paid-angle-scoring.md` — analytical canon. Mandatory read at first invocation. Codifies the five-lens scoring and the cluster-deduplication rule.
- `resources/registries/angle-registry.md` — angle taxonomy reference (14 angle types). Cell labels map to registry entries when possible.
- `resources/registries/proof-registry.md` — objection-neutralization mapping (which proof type defuses which objection).
- `resources/templates/hook-formulas.md` — fallback hook library (15 patterns) when verbatim is thin.
- `resources/quality-specs/hook-quality-spec.md` — 5-criterion hook quality test. Mandatory threshold ≥ 4/5 before shipping any hook.
- `resources/routing/awareness-angle-matrix.md` — awareness-angle pairing, used to filter cells in the "avoid" column for the dominant awareness stage.
- `.skills/skills/snapshot-brand/SKILL.md` — voice canon source for Step 9 synthesis. Read before writing the synthesis paragraph if any uncertainty.
- `.skills/skills/mine-voc/SKILL.md` — upstream Layer B source. Provides the verbatim density that ranking depends on.
- `.skills/skills/mine-vom/SKILL.md` — optional upstream. Vernacular and white-space signals raise hook quality and unlock the market dimension.
- `.skills/skills/produce-copy-brief/SKILL.md` — downstream production skill. Operator picks an angle from the ranked table → `produce-copy-brief` turns it into a hook variant set + body opening + CTA family.
- `.skills/finalize-mutation-batch.py` — mandatory Step 12 primitive.
- `.skills/write-to-context.py` — canonical mutation channel for any write to `learnings.json` if a pattern is detected during the run.
- `docs/system/contextual-intelligence.md` — master doctrine. No orphan output rule, contextual reasoning, anti-patterns.
- `docs/system/voice.md` — voice canon, register, banned phrases.
- `resources/canon/copy/_shared/awareness-stage.json` · `$ref` partagé v2.29.0, 5 stages Schwartz canoniques. Source unique consommée par `lineage.awareness_stage` dans `angle.schema.json` v1.2.
- `resources/schemas/angle.schema.json` (v1.2) · schema cible persistance brand-side. Renommages : `source` devient `origin_axis`, `lineage.schwartz_conscience` devient `lineage.awareness_stage`. 8 fields migrés vers creative.
- `resources/schemas/creative.schema.json` (v1.1, NEW) · 7ème entité brand. Absorbe `intent`, `mecanique`, `seasonality_trigger`, `execution.*`, classification, `variant_of`. Si production créa instance complète, écrire ici (skill `compose-creative` v2.31+ ou direct).
- v2.29.0 manifest + D#391 · refacto angle/creative split, gouvernance schemas.

---

## Example output — okr probiotique minceur

What the operator sees in the terminal after triggering *"trouve les meilleurs angles paid pour la femme minceur okr"*:

---

Sur la femme minceur okr, ce qui sort en premier c'est trois ressorts qui ne se chevauchent pas: le miroir post-grossesse qui touche l'identitaire, le ballonnement permanent qui touche l'inconfort quotidien, et le ras-le-bol des régimes qui touche la délivrance. Les deux suivants — le verdict balance et la confiance retrouvée — élargissent sur la projection sociale et sur l'angle bénéfice direct, utiles si tu testes large.

Le move premier sur ton lancement jeudi c'est l'angle miroir en Reels: verbatim dense, objection scepticisme neutralisée par tes avis Trustpilot, format Reels qui matche ton stack. L'angle ballonnement en Stories est le backup à promouvoir si le miroir fatigue après une semaine. Garde le ras-le-bol des régimes pour une vague 2, il convertit moins haut mais retient plus longtemps.

| # | Angle | Hook | Émotion mobilisée | Objection neutralisée | Placement reco |
|---|---|---|---|---|---|
| 1 | Miroir post-grossesse | "Je ne pouvais plus voir mon reflet" | Identitaire | "J'ai déjà tout essayé" | Reels |
| 2 | Ballonnement permanent | "Toujours ballonnée, le ventre gonflé même à jeun" | Inconfort quotidien | "Trop cher pour 1-3 kg" | Stories |
| 3 | Ras-le-bol des régimes | "Frustration, échec, culpabilité, la boucle de tous les régimes" | Délivrance | "C'est juste du marketing" | Feed UGC |
| 4 | Verdict balance | "Le moment où tu montes sur la balance et tu sais déjà" | Anticipation négative | "Ça marche pour les autres, pas pour moi" | Reels |
| 5 | Confiance retrouvée | "Remettre la robe que tu as rangée il y a 2 ans" | Aspiration projetée | "Je vais reprendre dès que j'arrête" | TikTok |

*(angles 1-3 ancrés sur verbatims VoC denses; angles 4-5 inférés, à valider sur premiers tests)*

Le move utile derrière ça c'est de sortir un brief copywriter sur l'angle miroir pour ton lancement jeudi: 15 min, je pars sur les 3 hook variants + opening body + CTA family. On y va, ou tu préfères que je creuse la voix marché sur le segment minceur d'abord (mine-vom, ~25 min, te donnera le vernacular concurrentiel et les white spaces) ?

---

The same skill on a vitamin-C serum brand for women 28-42 with hyperpigmentation surfaces different dimensions: `pain.trigger` becomes load-bearing (post-pill, post-pregnancy, post-summer triggers), `objection.type` foregrounds *scepticisme actifs* over *prix*, the white-space dimension from VoM (post-rétinol routines, layering anxiety) becomes a primary axis. Output shape stays identical (five rows, plain language, hooks anchored in customer voice, synthesis above, next-step below) but no row repeats from the okr output. That non-repetition is the proof the skill reasons over the brand and does not template.

On a fashion brand the skill degrades gracefully: `pain.emotion` thins (fashion is more desire-driven than pain-driven), so active dimensions shift to `audience.JTBD.social`, `product.benefit.identity`, `brand.market.sophistication_stage`, and `placement`. The synthesis names the shift in prose (*"sur cette poche fashion la matière sort moins sur les pains que sur l'identité projetée, donc les angles ranked travaillent plus sur le statut et la projection que sur la résolution d'un problème"*) and the table holds.
