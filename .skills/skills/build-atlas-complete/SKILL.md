---
name: build-atlas-complete
type: orchestrator
version: "1.3.0"
recommended_model: sonnet
reasoning_pattern: null
mode: proposed
operator_facing: true
subagent_safe: false
isolation_scope: brand_only
layer: territoire
description: >
  v1.3.0 (v2.67 territoire-pure refactor) · Steps 8-9 stripped (produce-copy-brief + compose-creative) · align doctrine `docs/system/territory-discipline.md` shipped v2.67. Orchestrator scope = territoire substrat only · productions briefs+créas via `creative-brief-composer` post-atlas downstream (separate skill, separate invocation). Output explicite · complete strategic atlas substrate (specs + offers + audiences + angles + territoires scorés). BREAKING · operators v1.x qui invoquaient pour briefs+créas doivent invoquer `creative-brief-composer` post-`build-atlas-complete`. Migration documentée CHANGELOG v2.67.0. Backward compat strict additif sur Steps 1-7 unchanged (territoire chain preserved).
  v1.2.0 (v2.64 ontologie sémantique pure · pain_points + objections sub-audience + frictions sub-product) · Phase 3 deepen-brand-context (chain mine-voc + mine-vom) écrit désormais dans sub-parent locations · `audiences/{a_slug}/pain_points/` + `audiences/{a_slug}/objections/` + `products/{p_slug}/frictions/` (owned natif par parent path). Backward compat strict additif · fallback top-level v2.63 + profile sub-fields v1.7 preserved.
  v1.1.0 (v2.63 ontologie pure · pain_points + objections collections top-level) · Phase 3 deepen-brand-context (chain mine-voc + mine-vom) écrit désormais dans 3 collections séparées (`pain_points/` + `objections/` + `frictions/`) plus `profile.json` clean (identity + psychology + voice + behavior + decision_process restent · pain_points + objections sub-fields legacy supprimés post-v2.63 nouvelles brands). Backward compat preserved (pre-v2.63 brands route fallback profile sub-fields legacy).
  v1.0.2 (v2.61 doctrine consume) · consumes: enrichi avec refs docs/doctrine/ NEW v2.60 (dtc-operator-playbook, audiences-cartography, angle-anatomy, hooks-method, breakthrough-advertising-5-stages). Skill peut consume ces doctrines canon pour informer production sans dépendre schemas exacts.
  Full-cycle atlas substrate builder. Chains the territoire canon pipeline end-to-end on a
  blank or partially-built brand to produce the complete strategic atlas substrate
  (specs + offers + audiences + angles + territoires scorés) from a single operator intent.
  Single chairman orchestrating specialized skills with explicit gates between phases.
  Resolves the Scenario 4 orchestration gap surfaced in Phase 1 audit, so the agent never
  freestyles strategic prose to fill a multi-skill atlas request.
  FR: "génère l'atlas complet de {brand}", "build atlas {brand}", "lance le pipeline complet", "construis tout pour {brand}", "atlas complet from scratch".
  EN: "build complete atlas", "generate full atlas {brand}", "build everything for {brand}", "run full pipeline", "full atlas from scratch".
triggers_fr:
  - "génère l'atlas complet"
  - "build atlas {brand}"
  - "lance le pipeline complet"
  - "construis tout pour {brand}"
  - "atlas complet from scratch"
triggers_en:
  - "build complete atlas"
  - "generate full atlas"
  - "build everything"
  - "run full pipeline"
  - "full atlas from scratch"
permissions:
  reads: [brand, product, offer, profile, learning, strategy]
  writes: [brand, product, offer, profile, learning, strategy]
  emits_events: [coherence_check, atlas_substrate_staged]
consumes:
  - brands/{slug}/brand.json
  - resources/schemas/spec.schema.json
  - resources/schemas/profile.schema.json
  - resources/schemas/angle.schema.json
  - resources/schemas/roadmap.schema.json
  - resources/catalogues/heuristiques-persuasion.json
  - resources/catalogues/niveaux-schwartz.json
  - resources/catalogues/formats-livrables.json
  - resources/catalogues/hooks.json
  - resources/catalogues/angles.json
  - path: docs/system/territory-discipline.md
  - path: docs/doctrine/dtc-operator-playbook.md
  - path: docs/doctrine/audiences-cartography-doctrine.md
  - path: docs/doctrine/angle-anatomy-doctrine.md
  - path: docs/doctrine/hooks-method-doctrine.md
  - path: docs/doctrine/breakthrough-advertising-5-stages.md
produces_proposals_for:
  - brands/{slug}/spec.json
  - brands/{slug}/products/*/offers.json
  - brands/{slug}/audiences/*/profile.json
  - brands/{slug}/audiences/*/pain_points/*.json
  - brands/{slug}/audiences/*/objections/*.json
  - brands/{slug}/products/*/frictions/*.json
  - brands/{slug}/pain_points/*.json (legacy v2.63 backward compat)
  - brands/{slug}/objections/*.json (legacy v2.63 backward compat)
  - brands/{slug}/frictions/*.json (legacy v2.63 backward compat)
  - brands/{slug}/angles/*.json
  - brands/{slug}/strategy.json
  - brands/{slug}/scoring/matrix-{date}.json
pipeline:
  preconditions: operator provides brand_slug AND (URL OR snapshot already completed). MCP tools available (facebook-graph optional, Notion optional).
  postconditions: |
    - brand structure fully populated across spec, offers, profile(s), angles
    - score-matrix territories ranked, top 3 axes créatifs selected
    - territories staged as proposals, ready for downstream production via creative-brief-composer (separate skill, separate invocation)
    - status.json updated, snapshot rebuilt, finalize-mutation-batch event emitted
    - learn-from-session flush proposed at end
disambiguates_against:
  onboard-brand: "route to onboard-brand when operator wants only the structural setup + snapshot + integrity check (no audiences/angles/briefs/créas). onboard-brand stops at the 'context loaded' gate."
  deepen-brand-context: "route to deepen-brand-context when operator wants only VoC + VoM mining on a snapshotted brand (no audiences/angles/briefs/créas downstream)."
  setup-brand: "route to setup-brand for initial identity/structure only."
  snapshot-brand: "route to snapshot-brand for URL scrape only on an existing brand."
  profile-audience: "route to profile-audience standalone when operator wants audiences only, not the full strategic atlas."
  score-matrix: "route to score-matrix standalone when atlas is already populated and operator wants only territory prioritization."
patch_notes:
  v1.3.0:
    - "v2.67 territoire-pure refactor · Steps 8-9 stripped (produce-copy-brief + compose-creative) · align doctrine territory-discipline.md. Orchestrator scope = territoire substrat only · productions briefs+créas via creative-brief-composer post-atlas downstream. BREAKING · operators v1.x qui invoquaient pour briefs+créas doivent invoquer creative-brief-composer post-build-atlas-complete. Migration documentée CHANGELOG v2.67.0. Backward compat strict additif sur Steps 1-7 unchanged (territoire chain preserved)."
  v1.0.0:
    - "Ship v2.56 · resolves Scenario 4 audit gap (Phase 1)"
    - "Chains 9 phases: setup → snapshot → deepen → profile → weight → angles → score → brief → créa"
    - "Explicit operator gates between Phases 4-5 and 6-7 (audience and angle validation)"
    - "Investigation Posture 5-section close (Observé / Déduit / Inconnu / Leviers / Close ouvert) mandatory"
    - "No raw numeric scoring exposed to operator (Compositional Cartography §7)"
  v1.0.1:
    - "v2.58 patch · canonical strategy.json path (was strategy/roadmap.json non-canon) · scoring matrix path aligned brands/{slug}/scoring/matrix-{date}.json (was strategy/score-matrix.json)"
    - "Closes dette technique runtime · strategy.schema v1.0 NEW shipped v2.58 canonical entity activée"
    - "produce-strategy v1.0.0 NEW orchestrator invokable en post-Phase 10 close si l'opérateur veut cadrer le focus Q{n} sur la brand atlas-complete · cycle stratégique distinct de la phase score-matrix"
  v1.0.2:
    - "v2.61 doctrine consume · consumes: enrichi avec refs docs/doctrine/ NEW v2.60 (dtc-operator-playbook, audiences-cartography, angle-anatomy, hooks-method, breakthrough-advertising-5-stages). Skill peut consume ces doctrines canon pour informer production sans dépendre schemas exacts."
  v1.1.0:
    - "v2.63 ontologie pure pain_points + objections collections top-level · Phase 3 deepen-brand-context (chain mine-voc + mine-vom) écrit désormais dans 3 collections séparées top-level (pain_points/ + objections/ + frictions/) plus profile.json clean (identity + psychology + voice + behavior + decision_process restent · sub-fields pain_points + objections legacy supprimés post-v2.63 nouvelles brands)"
    - "Downstream creative production phase · context.pain_point_ref canonical PNT-NN persisté dans creative.json downstream (cohérent v1.5)"
    - "Phase 6 produce-paid-angles consume v1.9 cohérent (lit pain_points/ + objections/ collections, persiste angle.lineage.pain_ref + objection_ref canonical)"
    - "Downstream copy brief phase consume v1.5 cohérent (sections Pain to activate + Objections to neutralize citent PNT-NN + OBJ-NN canonical IDs inline)"
    - "produces_proposals_for: enrichi avec pain_points/*.json + objections/*.json + frictions/*.json (NEW v2.63 top-level collections)"
    - "Backward compat strict · pre-v2.63 brands (legacy profile sub-fields) route fallback transparent, sub-skills route silently"
  v1.2.0:
    - "v2.64 ontologie sémantique pure pain_points + objections sub-audience + frictions sub-product · Phase 3 deepen-brand-context (chain mine-voc + mine-vom) écrit désormais dans sub-parent locations (audiences/{a_slug}/pain_points/ + audiences/{a_slug}/objections/ + products/{p_slug}/frictions/), owned natif par parent path"
    - "Downstream creative phase v1.6 · context.pain_point_ref canonical PNT-NN persisté depuis sub-audience canonical"
    - "Phase 6 produce-paid-angles consume v1.10 cohérent (lit sub-audience pain_points/objections, persiste angle.lineage.pain_ref + objection_ref canonical sub-audience)"
    - "Downstream copy brief phase consume v1.6 cohérent (sections Pain to activate + Objections to neutralize citent PNT-NN + OBJ-NN sub-audience canonical IDs inline)"
    - "produces_proposals_for: enrichi avec audiences/*/pain_points/*.json + audiences/*/objections/*.json + products/*/frictions/*.json (NEW v2.64 sub-parent locations)"
    - "Backward compat strict additif · fallback transparent top-level v2.63 + profile sub-fields v1.7 preserved · sub-skills route silently selon disponibilité"
---

# Skill: build-atlas-complete

**CRITICAL:** this is an **Orchestrator**. **YOU MUST NEVER** re-implement setup-brand, snapshot-brand, deepen-brand-context, profile-audience, weight-dimensions, produce-paid-angles, or score-matrix logic here. **YOU MUST** delegate to each existing skill in sequence via Task tool (when the subskill is `subagent_safe: true`) or inline invocation (when `subagent_safe: false`). Any deviation breaks the canon purity rule established by `onboard-brand`. **Scope v1.3.0 territoire-pure** · productions briefs+créas post-atlas via `creative-brief-composer` (separate skill, separate invocation). Voir `docs/system/territory-discipline.md`.

## Tone

Chairman orchestrating a territoire substrate pipeline that produces the complete strategic atlas substrate. Narrate each handoff in one operator-facing sentence ("structure prête… snapshot lancé… audiences cartographiées, deux gates devant nous… angles ranked…"). Operator never reads skill names, paths, field paths, scoring numbers, or Task tool mechanics. The pipeline is long (30-90 min depending on density), so heartbeat at each gate is non-negotiable.

---

## Expert methodology

**Canonical expert persona**: senior strategic director at a paid-acquisition agency, briefing a brand from blank URL to deployable territoire substrate in one sitting. Owns the chain, validates at each gate, lifts the operator's view to project altitude when uncertainty surfaces. Briefs+créas production handed off post-atlas to `creative-brief-composer`.

**Framework**: sequential territoire substrate chain, two mid-pipeline operator gates (audiences validated before angles, angles validated before scoring). Confidence chain propagated phase-by-phase per `docs/system/confidence-propagation.md`. Investigation Posture enforced on the final operator-facing synthesis per `docs/system/investigation-posture.md`. Scope discipline per `docs/system/territory-discipline.md` (v2.67).

**Matrix**:

| Phase | Skill delegated | Subagent? | Gate before next phase |
|---|---|---|---|
| 0. Pre-flight (DRGFP) | inline | n/a | brand_slug present, URL or snapshot ready, MCP layer detected |
| 1. Structure + identity | `setup-brand` | No (conversational) | brand.json filled with name + language + sector |
| 2. URL snapshot | `snapshot-brand` (Task) | Yes | spec.json + offers.json + profile.json draft at 60% |
| 3. Deepen context | `deepen-brand-context` (inline orchestrator) | No (chains its own subagents) | VoC Layer B + VoM Layer B + cross-signals synthesis delivered |
| 4. Audiences | `profile-audience` (Task per candidate) | Yes | Audiences mère + sub-clusters proposed, confidence chain explicit |
| **GATE A** | inline operator validate | n/a | Operator accepts / corrects audiences |
| 5. Weight dimensions | `weight-dimensions` (Task brand-wide) | Yes | Audience-angle compatibility scores pre-computed (internal) |
| 6. Paid angles | `produce-paid-angles` (Task per top-3 audience) | Yes | Angles ranked per audience (formula Obs+Tension+Reframe+Bridge) |
| **GATE B** | inline operator validate | n/a | Operator accepts / corrects ranked angles |
| 7. Score matrix | `score-matrix` (Task brand-wide) | Yes | Profil × Source d'angle matrix, top 3 axes créatifs selected |
| 8. Stage territories | inline (substrate review) | n/a | Territories staged as proposals, ready for downstream production |
| 9. Close | inline (Investigation Posture 5 sections) | No | Synthesis delivered, no orphan close, handoff to `creative-brief-composer` proposed |

**Variables tracked**:
- `url_available` (bool) · drives whether Phase 2 runs or skips with confidence degradation
- `audience_count_validated` (int) · caps Phase 6 and Phase 7 cardinality (top-3 per default)
- `axe_creatif_count_selected` (int) · caps Phase 7 scoring output (top-3 axes créatifs per default)
- `confidence_floor` (float internal) · propagates worst-case across phases; never surfaced
- `mcp_layer` (set: facebook-graph, notion, none) · drives Phase 3 source breadth

**Failure modes**:
- Phase 1 (setup-brand) aborts mid-flow → persist `brands/{slug}/session-state.md`, allow resume via `resume-session`. Never restart from zero.
- Phase 2 (snapshot) fails (URL 404, JS-heavy, paywalled) → degrade gracefully: skip Phase 2, surface confidence drop to operator, continue downstream phases with declared-only data.
- Phase 3 (deepen) returns thin material (no Reddit, no Trustpilot reviews available) → flag as "Inconnu" in final synthesis, propose `mine-voc` ticket as Lever.
- Gate A or B operator rejects all proposals → pause pipeline, route to standalone `profile-audience` or `produce-paid-angles` for manual rework, do not silently kill chain.
- Phase 7 (score-matrix) finds zero viable axe créatif → surface honestly, propose alternative routes (expand audiences, re-mine VoC for missed angles).

---

## Step 0 · Pre-flight (DRGFP)

Check operator provided minimum context. Apply Dependency Resolution & Gap-Filling Protocol L1 → L2:

- **brand_slug** required. If absent → ask via AskUserQuestion: *"Sur quelle marque je build l'atlas complet ?"*.
- **URL** or **existing snapshot**. If neither, mark `url_available = false` and warn confidence will degrade. If operator typed *"build atlas {brand}"* without URL on a blank workspace, ask once: *"Tu as une URL pour pré-remplir, ou je travaille en blind (purement déclaratif) ?"*.
- **MCP layer detection**: silent check `.mcp.json` for `facebook-graph` (Meta benchmarks) and `notion` (existing strategic memos). Populate `mcp_layer`. Surface only if operator asks.

Announce the pipeline (chairman posture, no jargon, no skill names):

> *"OK, atlas complet de {brand}. Pipeline territoire substrat · structure, scan, voix client+marché, audiences, angles paid, territoires scorés. Deux gates où tu valides au passage (audiences puis angles). 30 à 90 min selon la densité. Je pilote, tu valides aux gates. Une fois l'atlas posé, on enchaîne sur briefs+créas via `creative-brief-composer` sur l'axe créatif que tu choisis. Go ?"*

Hold for go-ahead, then proceed.

---

## Step 1 · Delegate `setup-brand` (inline, conversational)

**NEVER** spawn as subagent (`setup-brand.subagent_safe: false`). Invoke inline. Let it run its full conversational flow.

Pass context: operator-provided name/URL, detected profile (from `operator/profile.json`), language preference.

**Gate to Phase 2**: `brands/{slug}/brand.json` exists with `identity.name` and `identity.language` filled, OR operator explicitly deferred structure creation.

---

## Step 2 · Delegate `snapshot-brand` via Task tool

**If** `url_available = true` AND `snapshot-brand.subagent_safe: true`:

Spawn subagent via Task tool:
- `model: sonnet`
- Input: brand slug, URL
- Expected: `brands/{slug}/spec.json`, `brands/{slug}/products/{p}/offers.json`, `brands/{slug}/audiences/{a}/profile.json` drafts via stage-proposal pipeline

**CRITICAL · stage-before-ask is enforced through the subagent.** snapshot-brand SKILL.md mandates `.skills/stage-proposal.py` before any operator-facing proposal. This orchestrator inherits that rule by delegation. If the subagent ever skips staging and tries direct write, it hits the workflow gate. Do not retry a gated write; surface the gate message and wait for operator confirmation.

**Operator-facing line**:

> *"Je scanne le site pendant qu'on continue."*

Surface snapshot Step 7 synthesis paragraph when it returns (4-6 sentences, prose canon). Do not re-summarize.

**If `url_available = false`** → skip Phase 2, log `confidence_floor` drop, continue with declared-only context.

---

## Step 3 · Delegate `deepen-brand-context` (inline orchestrator)

`deepen-brand-context` is itself an orchestrator (`subagent_safe: false`). Invoke inline. It will spawn `mine-voc` + `mine-vom` subagents and run `cross-deepening-signals` synthesis.

Pass context:
- brand slug
- run mode: `silent` (this is a chain inside a larger chain · the orchestrator surfaces the cross-synthesis only, not each subskill's individual synthesis)

**Operator-facing line**:

> *"Je passe à la voix client + voix marché. ~45 min en arrière-plan."*

When deepen returns its cross-synthesis (3 movements, 18 sentences max per voice canon), surface it as-is to the operator. Do not re-summarize.

**v1.2.0 ontologie sémantique pure v2.64 · sub-parent locations.** Phase 3 deepen-brand-context (chain mine-voc + mine-vom) écrit désormais dans sub-parent locations (owned natif par parent path) ·

- `brands/{slug}/audiences/{a_slug}/pain_points/*.json` (PNT-NN entities · formulation + verbatim_quotes + emotion + trigger + severity + chain + confidence_chain · audience owner implicite via parent path, pas de array affected_audiences[])
- `brands/{slug}/audiences/{a_slug}/objections/*.json` (OBJ-NN entities · formulation + type + frequency + severity + lifecycle_stage + response_counter + derived_angle_refs · audience owner implicite)
- `brands/{slug}/products/{p_slug}/frictions/*.json` (FRC-NN entities · formulation + type + signals · product owner implicite via parent path · NEW canonical layer for product-bound frictions sub-product)
- `brands/{slug}/audiences/*/profile.json` clean (identity + psychology + voice + behavior + decision_process restent · sub-fields `pain_points[]` + `objections[]` legacy supprimés post-v2.64 nouvelles brands · backward compat lecture preserved si déjà présents)

Cohérent ontologie sémantique pure cross-skill · pain + objection appartiennent sémantiquement à une audience (owned natif par sub-parent path), friction appartient à un product. Pattern · l'appartenance précède le tracking · pas besoin de array affected_audiences[]/affected_products[] cross-reference quand le path déclare déjà l'owner.

**Backward compat strict additif** · fallback transparent top-level v2.63 (`pain_points/` + `objections/` + `frictions/` avec affected_audiences[]/affected_products[]) + profile sub-fields v1.7 preserved si brand brownfield.

**Gate to Phase 4**: cross-deepening-signals synthesis delivered, `audiences/*/pain_points/` + `audiences/*/objections/` + `products/*/frictions/` sub-parent collections populated, profile.json drafts enriched with verbatim_quotes (voice corpus) + audience candidates + sophistication_stage + market_vernacular.

---

## Step 4 · Delegate `profile-audience` via Task tool (per audience candidate)

`profile-audience` is `subagent_safe: true`. Spawn one subagent per audience candidate identified in Phase 3 cross-signals.

Cap parallel at 3 candidates (per delegation pattern §parallel limits). If Phase 3 surfaced >3 candidates, take top-3 by cross-signal strength.

For each candidate:
- `model: sonnet`
- Input: brand slug, audience candidate (mère hypothesis from cross-signals)
- Expected: full profile.json with mère audience + sub-clusters, confidence chain explicit per axis, observed/déduit/déclaré sourcing tags

**Operator-facing line**:

> *"Je cartographie les audiences candidates en parallèle."*

When all return, synthesize at orchestrator level into a single audience tableau (mère × sub-clusters × confidence chain). **NEVER** dump raw subagent output verbatim per delegation pattern §synthesis layer.

---

## GATE A · Operator validates audiences

**MANDATORY GATE** before Phase 5. Surface the audience tableau, then AskUserQuestion:

- "Valide les audiences proposées, je continue sur les angles"
- "Corrige/affine d'abord, j'ouvre un drill sur {audience X}"
- "Stop, je veux relancer la voix client avant"
- "Autre"

If operator picks corrige → route to standalone `profile-audience` with focus, hold orchestrator state in `session-state.md`, resume on operator signal.

If operator picks stop → pause chain, route to `mine-voc` standalone.

**NEVER** proceed to Phase 5 without explicit validation. Audiences gate the entire downstream because Phase 5-9 fan out per audience.

---

## Step 5 · Delegate `weight-dimensions` via Task tool (brand-wide)

`weight-dimensions` is `subagent_safe: true`, `operator_facing: false`. Single subagent, brand-wide.

- `model: sonnet`
- Input: brand slug, validated audiences from Gate A
- Expected: internal audience × angle compatibility scores written to brand state (not exposed)

**Operator-facing line**:

> *"Je pré-compute les compatibilités angle × audience."* (one line, no detail)

**NEVER** surface raw numeric scores to operator. Compositional Cartography §7 enforcement.

---

## Step 6 · Delegate `produce-paid-angles` via Task tool (per top-3 audience)

`produce-paid-angles` is `subagent_safe: true`. Spawn one subagent per top-3 validated audience.

For each audience:
- `model: sonnet`
- Input: brand slug, audience id, weight-dimensions output
- Expected: angles ranked per audience using formula Obs + Tension + Reframe + Bridge, sourced from VoC verbatims where possible

**Operator-facing line**:

> *"Je génère les angles paid pour chaque audience top."*

When all return, synthesize into a per-audience angles tableau. Surface the top angle per audience with a 1-line rationale anchored on observed tension. **NEVER** expose internal scoring numbers.

---

## GATE B · Operator validates angles

**MANDATORY GATE** before Phase 7. Surface the angles tableau, then AskUserQuestion:

- "Valide les angles top, je continue sur les territoires + briefs + créas"
- "Corrige/affine, un angle est off sur {audience X}"
- "Stop, je veux re-mine VoC avant de produire les briefs"
- "Autre"

Same rejection logic as Gate A. **NEVER** proceed to Phase 7 without explicit validation. Angles gate briefs+créas because Phase 8-9 fan out per priority angle.

---

## Step 7 · Delegate `score-matrix` via Task tool (brand-wide)

`score-matrix` is `subagent_safe: true`, `operator_facing: true`. Single subagent, brand-wide.

- `model: sonnet`
- Input: brand slug, validated audiences (Gate A), validated angles (Gate B), weight-dimensions output
- Expected: Profil × Source d'angle matrix scored via canonical scoring, top-3 axes créatifs selected

**Operator-facing line**:

> *"Je build la matrice complète et je remonte les axes créatifs prioritaires."*

When subagent returns, surface only the **top-3 axes créatifs named in operator language** with prose rationale per axe (1-2 sentences anchored on audience tension + angle source). **NEVER** expose the full matrix grid with raw numbers. Compositional Cartography §7.

**Disambiguation lexicon v2.67** · "axe créatif" (micro · output score-matrix) vs "territoire" (macro · substrat atlas). Surface "axes créatifs" pour l'output ranking en Step 7. Le territoire macro = l'atlas substrate entier. Voir `docs/system/territory-discipline.md`.

---

## Step 8 · Review & stage territories for downstream production

Territories prioritized (top-3 axes créatifs par score-matrix Step 7). Substrate complete. Atlas posé.

Next phase (outside this orchestrator) · materialize briefs + creatives via `creative-brief-composer` skill (separate invocation · operator chooses which axe créatif to materialize first).

**Operator-facing line**:

> *"Atlas substrat posé. 3 axes créatifs ranked. Prêt pour la phase production briefs+créas."*

---

## Step 9 · Close (Investigation Posture, 5 sections MANDATORY)

**CRITICAL**: this is a strategic deliverable orchestrator, not a setup orchestrator. Investigation Posture is mandatory per `docs/system/investigation-posture.md`. Five sections explicit:

### Observé
What the pipeline produced, sourced. Audiences validated at Gate A, angles validated at Gate B, top-3 axes créatifs selected by score-matrix. Quantify (number of audiences, number of angles per audience, number of axes créatifs ranked). Never expose scoring numbers.

### Déduit
Hypotheses with explicit confidence chain. Examples per atlas type:
- "L'audience mère **{name}** ressort comme prioritaire (confidence **forte** · convergence VoC + VoM)."
- "L'angle **{name}** sur l'audience **{name}** porte le plus de tension observée (confidence **moyenne** · verbatims solides mais sample size limité)."
- "L'axe créatif **{name}** combine audience à haut volume + angle peu exploité par les concurrents (confidence **moyenne** · projection à valider en test)."

Confidence chain: **forte** / **moyenne** / **faible** / **TRÈS faible**. Never invent confidence. Never present hypothesis as fact.

### Inconnu
Variables non observables sans test live ou data additionnelle. Examples:
- "Volume réel de l'audience mère sur Meta (non mesurable sans audience-builder test)."
- "Performance comparative des angles sur le marché actif (non mesurable sans déploiement budget test)."
- "Sensibilité prix au-delà du tier offers.json actuel (non mesurable sans split-test landing)."

### Leviers
Skills / actions / sources pour lever les inconnues. Examples:
- "Test campagne Meta sur l'audience mère + 2 angles top (skill `audit-meta-account` post-déploiement)."
- "Mine VoC additionnel sur source spécifique (skill `mine-voc --focus={axis}`)."
- "Refine angles si Gate B a laissé des hypothèses floues (skill `produce-paid-angles --focus={audience}`)."

### Close ouvert
**UNE seule question macro**. L'opérateur arbitre la prochaine direction (production briefs+créas downstream ou enrichissement territoire substrat). Example canonical v1.3.0:

> *"Sur quel axe créatif tu veux qu'on matérialise d'abord briefs + créas via `creative-brief-composer` · T1 · T2 · T3 ? Ou tu veux d'abord enrichir le territoire (mine-voc supplémentaire · profile-audience drill · etc.) ?"*

**NEVER** orphan close. **NEVER** flat menu. **NEVER** more than one question.

---

## Step 10 · Finalize

```bash
python3 .skills/finalize-mutation-batch.py --brand-slug {slug}
python3 .skills/build-brand-snapshot.py {slug}
```

Update status.json:
- `last_atlas_build_run`: timestamp
- `atlas_substrate_complete`: true
- `audiences_count`, `angles_count`, `axes_creatifs_count`
- emit `atlas_substrate_staged` event

Trigger `learn-from-session` batch (posture adaptive, operational/ship register): briefer 5-7 bullets max sur ce qui a été produit (territoire substrat, pas briefs+créas), close binaire ("1 arbitrage à faire" = Close ouvert macro, ou "RAS, atlas posé, prêt pour `creative-brief-composer`").

---

## Operator cartography (before Phase 0, if complex brief)

If the operator typed a minimal brief ("build atlas {brand}") without context, briefly cartograph the pipeline before executing (~5 lines, operator language, no system jargon):

> *"Analysé. Atlas substrat complet, voilà comment je vais piloter :*
> *• Je structure ta marque puis je scanne le site*
> *• Je dig voix client + voix marché*
> *• Je cartographie les audiences. **Premier gate** : tu valides*
> *• Je produis les angles paid ranked par audience. **Second gate** : tu valides*
> *• Je build la matrice complète et je remonte les top-3 axes créatifs ranked*
> *• Je clôture avec un drill-down · soit on enchaîne briefs+créas via `creative-brief-composer` sur l'axe que tu choisis, soit on enrichit le territoire d'abord"*

Then AskUserQuestion: *Go / Skip URL scan / Ajuste le pipeline (skip une phase) / Autre*.

---

## Guardrails

- **NEVER** run all phases sequentially blocking on one operator without heartbeat. Surface progress at each gate.
- **NEVER** skip Gate A or Gate B silently. Audiences gate angles, angles gate scoring. Skipping = fan-out on unvalidated hypotheses = wasted calls + low-quality atlas substrate.
- **NEVER** expose Task tool mechanics, subagent internals, or skill names to the operator ("I spawned profile-audience", "produce-paid-angles returned"). Say what it *does*: "je cartographie les audiences", "je génère les angles".
- **NEVER** re-implement subskill logic. If a subskill has a bug or gap, fix it there, not here. Pure orchestrator per `onboard-brand` precedent.
- **NEVER** expose raw scoring numbers, confidence floats, weight-dimensions matrix values, or internal field paths. Compositional Cartography §7 anti-pattern enforcement.
- **NEVER** freestyle prose for an output where a downstream skill exists. Skill routing canon v2.55 enforcement · invoke `produce-paid-angles`, never write angles in prose. The orchestrator delegates; it does not produce strategic content directly.
- **NEVER** produce briefs copy ou créas in this orchestrator (v1.3.0 territoire-pure scope). Briefs+créas materialization happens downstream via `creative-brief-composer` (separate skill, separate invocation). Voir `docs/system/territory-discipline.md`.
- **NEVER** dump raw subagent output verbatim. The orchestrator main is the synthesis layer per delegation pattern.
- **ALWAYS** persist `brands/{slug}/session-state.md` rolling update after each phase (crash resumption).
- **ALWAYS** propagate confidence chain phase-by-phase per `docs/system/confidence-propagation.md`. Worst-case floor wins on the final synthesis.
- **ALWAYS** apply Investigation Posture 5 sections on Step 9 close. The audit gap that triggered v1.0.0 was exactly this missing structured close.
- **ALWAYS** respect parallel cap (3 subagents per phase) and depth cap (1 · `deepen-brand-context` already chains its own subagents, that is depth-2 already authorized by the architecture).
- **ALWAYS** Brand isolation: this orchestrator operates `brand_only` per `docs/system/brand-isolation-discipline.md`. Cross-brand pulls (canon copy resources) are read-only references, never write to other brands.
- **One brand at a time.** No parallel atlas-build on multiple brands. Confuses Layer B mutation scoping.

---

## Cross-references

- `.skills/skills/onboard-brand/SKILL.md` · orchestrator pattern reference (purity rule, gate canon)
- `.skills/skills/deepen-brand-context/SKILL.md` · chained inline orchestrator (Phase 3)
- `.skills/skills/setup-brand/SKILL.md` · Phase 1
- `.skills/skills/produce-strategy/SKILL.md` · invokable en post-Phase 9 close si l'opérateur veut cadrer le focus Q{n} sur la brand atlas-complete (strategy.schema v1.0 canon shipped v2.58)
- `.skills/skills/snapshot-brand/SKILL.md` · Phase 2
- `.skills/skills/profile-audience/SKILL.md` · Phase 4
- `.skills/skills/weight-dimensions/SKILL.md` · Phase 5
- `.skills/skills/produce-paid-angles/SKILL.md` · Phase 6
- `.skills/skills/score-matrix/SKILL.md` · Phase 7
- `.skills/skills/creative-brief-composer/SKILL.md` · downstream production briefs+créas post-atlas (separate invocation, operator chooses axe créatif)
- `docs/system/territory-discipline.md` · NEW v2.67 · territoire-pure scope canon (build-atlas-complete = substrat territoire only, productions briefs+créas downstream)
- `docs/system/scope-extension-discipline.md` · SED-X v2.65 · skill scope boundaries discipline
- `docs/system/canonical-matrix-reasoning.md` · CMR · production discipline (95% quality on intersectional outputs)
- `docs/system/compositional-cartography.md` · §7 anti-pattern (no raw numeric scoring to operator) · implémentation domaine créatif de CMR
- `docs/system/investigation-posture.md` · 5-section close canon (Step 9 mandatory)
- `docs/system/confidence-propagation.md` · confidence chain algebra
- `docs/system/brand-isolation-discipline.md` · brand_only scope default
- `docs/system/skill-routing-discipline.md` · v2.55 routing canon (orchestrator delegates, never freestyles strategic prose)
- `docs/system/delegation-pattern.md` · model routing + parallel caps
- `docs/system/contract-build.md` · Build mode rules + Orchestration gate
- `docs/system/voice.md` · operator-facing prose canon (3 movements, no bold-section anchors on synthesis paragraphs)

---

## Verdict v1.3.0

v1.3.0 ship orchestrator territoire-pure · substrate atlas (specs + offers + profiles + angles + scoring + frictions + roadmap + strategy) end-to-end · productions briefs+créas via separate `creative-brief-composer` skill post-atlas downstream.
