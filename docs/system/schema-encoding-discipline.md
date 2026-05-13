# Schema Encoding Discipline (SED) — Operating Doctrine

> Working draft — R&D zone, Build mode. To be reviewed, then promoted to `workspace-template/docs/system/schema-encoding-discipline.md` in Release mode. **SED is the substrate sub-doctrine of `contextual-intelligence.md` (CI).** Without rigorous schema encoding, the matrix-driven reasoning of CMR has nothing to range over and the agent's intelligence has no stable ground.

---

## 1. Thesis

> **Encoding rigor is the precondition of every other discipline in PhantomOS.**

A workspace is a knowledge container. The agent reasons over what is encoded in it — entities, fields, sources, vocabulary, lifecycle. If the encoding is sloppy (free-text where enums should be, untracked sources, unversioned schemas, mutations that bypass the gate), every downstream skill inherits the noise. The matrix in CMR cannot select cells correctly when the schema is ambiguous. The recommendations in CI are unreliable when the substrate they rest on is unverifiable. The skills authored under SAD become brittle because the canon they consume drifts session-to-session.

SED names what it takes to keep the substrate clean: typed fields, externalized canon, append-only history, gated mutations, sourcing tags, triangulation, lifecycle hygiene. None of these are individually surprising — they exist scattered across `field-types.md`, `architecture.md`, `extending.md`, hooks, conventions, and the `_field_types` system. SED consolidates them into one named discipline so that a skill author can ask, "am I encoding this correctly?" and have a single place to check.

---

## 2. The problem SED addresses

Without an encoding discipline, three kinds of silent failure accumulate:

1. **Sloppy substrate poisons reasoning.** A field tagged `derived` but actually filled by an operator's stated value, an entity referenced by inconsistent slugs, a canon variable inlined in skill prose rather than externalized — each is a small drift. Cumulatively they make the agent's reasoning unreliable in ways that don't surface as bugs but as creeping inconsistency.
2. **Mutations bypass the gate.** A direct `Edit` on a brand JSON skips the audit trail, breaks the proposal/acceptance workflow, and corrupts the event log. The hooks (`mutation-guard.py`, `convention-guard.py`) catch the obvious cases ; without a doctrine that names and explains them, the rules feel arbitrary and accumulate exceptions.
3. **The temporal layer drifts independently of the spatial layer.** Entities (brand, product, audience, offers, learnings, strategy) describe what the brand *is*. But what the workspace has *learned*, *observed*, *captured over time* — events, learnings lifecycle, operator awareness, session traces — is a parallel encoding with its own discipline. Without naming this Memory & Observability sub-corpus inside SED, it falls between the cracks.

SED is the answer: a single discipline that governs how the substrate gets and stays rigorous.

---

## 3. Two layers of encoding

SED encodes along two orthogonal axes:

**Spatial encoding** — the entities, fields, schemas, vocabularies, sourcing that describe the brand domain at any point in time. Six core entities (brand, product, offer, audience, learnings, strategy) plus extensions (custom entities, sidecars, registries). Versioned per-entity (`_version`), typed per-field (`_field_types`), enumerated where canon allows (closed vocabularies in JSON Schema enums).

**Temporal encoding** — what changes over time, what was observed, what was captured. Append-only logs (`decisions.md`, `learnings.json`, `session-log.md`, `events.jsonl`), operator memory (`/operator/profile.json`, `/operator/awareness.json`), narrative memory (`session-state.md`, snapshots), the three-layer memory system (entity / operator / narrative).

Both layers are SED territory. The spatial layer was historically the focus (the schemas, the field types) ; the temporal layer was scattered. SED consolidates both.

---

## 4. Minimum anatomy

A workspace satisfies SED if and only if it carries the following invariants:

| # | Invariant | Why it is load-bearing |
|---|---|---|
| 1 | **Six core entities + extensions, each with `_version` semver and `_field_types` tagging.** | Without versioning, schema evolution silently breaks consumers. Without `_field_types`, the agent cannot distinguish a fact from an inference, an observation from a declaration. |
| 2 | **Mutation gate non-optional.** Every write to brand/operator JSON goes through `write_to_context(field_path, value, source, confidence, mode)`. Direct `Edit/Write/NotebookEdit` on these files is refused by `mutation-guard.py`. | Bypassing the gate corrupts the proposal/acceptance workflow, skips the audit trail, and breaks the event log. Errors here are silent and persistent. |
| 3 | **Sourcing tags per field.** Every value carries `source` (observed / stated / structured / derived) and `confidence` (or qualitative tier). Auto-tagged from semantic signals at write time. | The operator and downstream skills need to distinguish what was scraped, declared, computed, or inferred. Without sourcing, every field looks equally authoritative. |
| 4 | **Closed vocabularies where canon exists** — enums in JSON Schema, lookup tables in registries, no free-text where a controlled vocabulary applies. | Free-text fields drift across brands and skills. *"rassurant"* in one workspace is *"reassuring"* in another is *"warm-authoritative"* in a third. The agent cannot compose across instances when vocab is open where it shouldn't be. |
| 5 | **Triangulation rule for load-bearing claims.** Any field that affects a downstream decision must be sourced from ≥3 independent inputs (verbatims, observations, operator confirmations) before being treated as canonical. Singletons are flagged as hypothesis. | Without triangulation, one outlier becomes a brand truth. CMR's verbatim-anchor rule depends on this — at the SED layer, sourcing must already be triangulation-aware. |
| 6 | **Append-only logs** for `decisions.md`, `learnings.json`, `session-log.md`, `events.jsonl`. Invalidation is `[SUPERSEDED Sxx]`, never deletion. | Editing history corrupts auditability. The cost of carrying superseded entries is one line of suffix ; the cost of losing the trail is unrecoverable. |
| 7 | **Snapshot / manifest regen post-mutation.** After any write to entity JSONs, regenerate `_snapshot.md` and any derived indexes (`_manifest.json`). Materialized-view pattern, not on-demand recompute. | Operators read the snapshot, not the full JSON tree. If snapshot is stale after a mutation, the operator and the agent operate on different views. |
| 8 | **Validation runtime** — `validate-resources`, `validate-naming`, `validate-all.py` run silently after writes, surface MAJOR/CRITICAL findings, ignore MINOR by default. | Invariants enforced at write-time prevent the workspace from drifting into invalid states. Surfaced selectively to avoid noise. |
| 9 | **Conventions plateforme** declared in `resources/conventions/{platform}.json`. Auto-loaded before any platform interaction. | Each external tool/API has its own conventions (Meta, Klaviyo, Shopify). Encoding them once in versioned conventions prevents skill-by-skill rediscovery. |
| 10 | **Extension layer governance** — custom entities under `brands/{slug}/custom/`, sidecars `{entity}.extensions.json`. Extensions follow same `_version` + `_field_types` rules as core. | Without governance, extensions drift faster than core. Extension layer is the most likely place to violate SED if discipline is not explicit. |

---

## 5. Sub-corpus — Memory & Observability

The temporal layer of SED has its own structure. Three memory layers, never mixed:

**Layer 1 — Entity memory** (`brands/{slug}/`). Spatial encoding. What the brand *is*. Mutated through the gate. Read by skills that produce, audit, recommend.

**Layer 2 — Operator memory** (`/operator/profile.json`, `/operator/awareness.json`). What we know about the *operator using the workspace*. Their identity, role, calibrated register, prior knowledge state, concepts already introduced. Persists across sessions.

**Layer 3 — Narrative memory** (`session-log.md`, `events.jsonl`, `session-state.md`, snapshots). What *happened*. The trail of sessions, mutations, decisions, learnings. Read by `session-search` for cross-session recall.

**Strict separation rule**: layers do not mix. An operator preference does not live in a brand JSON. A brand fact does not live in operator memory. A narrative event does not overwrite either. This separation is what makes the workspace forkable, the operator portable, and the audit trail intact.

**Lifecycle of `learnings.json`** — append-only, with `id / status / superseded_by / genericity / promoted_to`. Promotion path: brand-specific learning → cross-brand pattern → canon candidate. Staleness review at >180 days. `promote-backlog.json` tracks candidates.

**Events log** (`events.jsonl`) — schema includes `actor_id` (operator or agent), `action_type` (mutation / skill_invoked / hook_refused / checkpoint_resolved / etc.), `field_path`, `before`/`after`, timestamp. Read by `session-search`, audited by `turn-end-audit.py`.

**Awareness encoding** — `concepts_introduced[]` in `operator/awareness.json` tracks what has been explained to this operator. Calibrates the agent's register session-to-session. The agent never re-explains a concept the awareness file says is known.

---

## 6. Anti-patterns

| Name | Symptom | Fix |
|---|---|---|
| **Direct Edit on brand JSON** | An author bypassing `write_to_context` because "the gate doesn't cover my case". | Surface the gap to the maintainer. Extend the gate. NEVER hand-edit. |
| **Free-text where canon exists** | `tone: "rassurant et chaleureux mais pas trop direct"` instead of `tone: ["reassuring", "warm"]` from a controlled vocabulary. | Externalize the vocabulary in a registry, switch the field to enum. |
| **Untyped field** | A field carrying value but no `_field_types` tag. | Tag at write time. The agent cannot reason about provenance otherwise. |
| **Singleton-as-canon** | One verbatim, one operator declaration → brand truth. | Triangulation rule. Singletons flagged as hypothesis. |
| **Snapshot drift** | Operator asks "what's the brand status?" — agent reads JSONs directly because snapshot is stale. | Hard rule: rebuild snapshot after every write to entity JSON. |
| **Memory cross-contamination** | An operator preference written into brand JSON ("operator prefers concise output" — wrong layer). | Strict separation enforcement. The memory layer is determined by the *subject* of the fact, not the *trigger* of the write. |
| **Learnings overwrite** | A learning "corrected" by editing the original entry. | Append-only. New entry [SUPERSEDES Lxxx]. Old entry retains for audit. |
| **Schema drift** | Custom extension diverges from core schema patterns (no `_version`, no `_field_types`). | Extension layer governance — same rules as core. |
| **Convention drift** | Skill-author hardcodes a Meta API field name that conflicts with `resources/conventions/meta.json`. | Always read conventions before platform interaction. |
| **Validation noise** | Every MINOR finding surfaced to the operator → operator stops reading the audit. | Surface MAJOR/CRITICAL only. MINOR routes to a backlog. |

---

## 7. Decision-aid for skill creation

Skills authored under SAD must respect SED at the substrate level. Specifically:

**Before writing a new field or entity**, the skill author asks:
1. Is there an existing entity / sidecar / extension that already encodes this? (extend > create — see SAD)
2. What is the canonical type of this value (observed / stated / structured / derived)?
3. Is there a closed vocabulary that should constrain the field?
4. Will this field be load-bearing for downstream decisions? If yes → triangulation rule applies, version with `_version`, source-tag mandatory.
5. Is this spatial (entity) or temporal (event/learning/awareness)? Wrong layer = corruption.
6. Does this require an extension layer entry (custom entity / sidecar) or a core entity update? Core update requires schema bump + migration.

**Before writing a hook**, the skill author asks:
1. Is this enforcement *mechanical* (refuses an invalid state) or *semantic* (challenges model judgment)? Per CI, mechanical is enforceable, semantic is not.
2. Does this hook write to disk? If yes → must go through the mutation gate, must emit an event, must be auditable.

---

## 8. Operational requirements

**8.1 Schema versioning.** `_version` semver per entity / per canon file. Major bump requires migration script for consumers. Minor bump is backward-compatible enum extension. Patch is comment / clarification.

**8.2 Mutation gate enforcement.** `mutation-guard.py` blocks `Edit/Write/NotebookEdit` on `brands/**/*.json` and `operator/**/*.json`. Whitelist for explicit operator-tooling that goes through `write_to_context`. Refusals are logged.

**8.3 Sourcing tags auto-applied.** At write time, the source is inferred from the calling context (scrape literal → observed, operator declaration → stated, computation → derived, model inference → flagged inferred with confidence). The operator never sees `source` / `confidence` numbers — only `observé / déduit / déclaré / incertain` if relevant.

**8.4 Append-only enforcement.** `decisions.md` and `learnings.json` are append-only by hook. Edits to past entries are refused unless explicit `[SUPERSEDED]` annotation.

**8.5 Triangulation surfaced.** When a field is load-bearing but sourced from a single input, the agent flags it as hypothesis in operator-facing output ("à valider — basé sur 1 source").

**8.6 Snapshot regen automatic.** Post-write hook (`post-write-flush.py`) rebuilds `_snapshot.md` and any derived indexes within ~50ms of mutation.

**8.7 Validation runtime selective surfacing.** MAJOR/CRITICAL → flag operator. MINOR → backlog. CRITICAL → may halt operation.

**8.8 Extension governance.** Custom entities + sidecars validated by `validate-schema-canon` against same standards as core. New extension requires (a) schema declared, (b) `_version` set, (c) README explaining purpose, (d) registry entry.

**8.9 Convention precedence.** Platform conventions (`resources/conventions/`) take precedence over skill defaults. Conflict → conventions win.

**8.10 Memory layer separation.** Hooks refuse cross-layer writes (an operator preference attempted in a brand JSON is rejected with redirect). Three layers, never mixed.

---

## 9. Anti-cartography (what SED does NOT cover)

To prevent scope creep, SED explicitly does NOT cover:

- **The reasoning over the substrate** (CMR territory — production with intersectional matrices).
- **The creation of new skills consuming the substrate** (SAD territory — authoring discipline).
- **The trust / provenance / multi-tenant attribution of who wrote what** (PTD territory — full doctrine pending trigger conditions).
- **The agent's communication style** (CI Surface contract sub-corpus — voice, close, sharpening).
- **The vision / extractibility test** (Extractibility frame test).

When in doubt about whether a rule is SED or another discipline, ask: *"is this about how data gets and stays well-encoded ?"* If yes, SED. If no, route elsewhere.

---

## 10. Open tensions

1. **`_field_types` enum extensibility.** The four canonical values (observed / stated / structured / derived) cover most cases, but boundary cases recur (a value computed from multiple observed inputs — derived ? structured ?). Working rule: derived = computed by deterministic function, structured = inferred by model. To be validated on three more brands.

2. **Triangulation rule cardinality.** "≥3 sources" works for verbatims (mine-voc easily produces dozens). It is harder for operator declarations (1 founder = 1 source, by definition). Working rule: operator declaration counts as 1 source ; needs corroboration from 2 other types (observed scrape + derived inference, for example) to become canonical. Singletons stay flagged as hypothesis.

3. **Layer separation and analytics.** Cross-layer queries (e.g. "for this brand, what concepts has this operator already mastered?") cross the entity / operator boundary. Read-only cross-layer is allowed by query primitives ; write-side is forbidden. To be codified explicitly.

4. **Memory layer for shared (cross-brand) learnings.** A pattern observed across 5 brands is canon-candidate, not brand-specific learning. Where does it live? Working rule: in `shared-resources/learnings-canon/` after promotion via `promote-learning`. Until promotion, lives in each brand's `learnings.json` flagged as cross-brand candidate.

5. **Extension layer maturity.** Custom entities are validated, but their *quality* (are they well-modeled?) is harder to enforce mechanically. SAD red-team checks help. Open question: should SED enforce extension review by ≥1 senior before promotion to runtime?

6. **PTD overlap.** When PTD ships full, it will introduce `_provenance` blocks and `actor_id` attribution that touch every entity write. SED today carries the substrate ; PTD will carry the trust layer atop. Boundary to be redrawn at PTD draft promotion.

---

## 11. Cross-references

- **`contextual-intelligence.md`** — master doctrine ; SED is the substrate sub-discipline that keeps CI's reasoning honest.
- **`canonical-matrix-reasoning-2026-04-26.md`** — CMR depends on SED ontologically (no schema → no matrix). SED invariants 3 (sourcing) and 5 (triangulation) feed CMR invariants 4 (canon sourcing) and 9 (triangulation rule) directly.
- **`skill-authoring-discipline-2026-04-26.md`** — SAD governs how skills consume the SED substrate. SAD reads SED, not the inverse.
- **`provenance-trust-discipline-scope-2026-04-26.md`** *(R&D zone, lives in `research/` until promotion triggers hit)* — PTD will extend SED with provenance/trust at the multi-tenant scale. The same R&D-zone caveat applies to the other doctrine drafts referenced above with the `2026-04-26` date suffix.
- **`field-types.md`** — canonical reference for the four `_field_types` values. Source of truth, SED chapter that points to it.
- **`extending.md`** — extension layer rules ; SED chapter that contextualizes them in the broader discipline.
- **`architecture.md`** — entity dependency graph, context budget, structural reference ; pre-existing input to SED.
- **Hooks** — `mutation-guard.py`, `convention-guard.py`, `post-write-flush.py`, `turn-end-audit.py` — operational enforcement of SED invariants.

---

## Amendment protocol

To amend this doctrine, follow the procedure documented in `docs/system/doctrine-governance.md` § Amendment : draft the change in a research note, register a new D# entry in `decisions.md` with explicit `[SUPERSEDES Dxxx]` annotation, patch the doctrine file with a changelog header, and surface a re-test list of consumer skills. Silent edits to a binding doctrine are refused by convention.

---

## 12. Status

- **Draft v0.1** — research zone, Build mode, .
- **Promotion criterion** — to be reviewed by the maintainer, then promoted to `workspace-template/docs/system/schema-encoding-discipline.md` once cross-references with CMR / SAD / PTD scope are validated and the 11 sub-disciplines previously scattered are confirmed consolidated.
- **First applications** — patches to extension layer governance, sourcing-tag enforcement on legacy brand JSONs, triangulation-rule surface in `validate-resources` output.

---

## 13. Schema evolutions registry

Registre canonique des évolutions schemas par release. Toute mutation `resources/schemas/*.json` doit apparaître ici (bump version, NEW schema, patch additif, $ref refactor). Append-only.

### v2.56 (2026-05-12) · Notion stride-up alignment

Driver · audit Phase 1 quantifie gap 70% coverage Notion 11 collections workspace `Onday`. PhantomOS implémente la doctrine `compositional-cartography.md` (4 arbres + matrice + modulateurs), Notion stride-up en est l'instance opérationnelle de référence. Bloc 1 comble 2 schemas manquants + 5 patches additifs, backward compat strict (toutes properties optional, validation existing instances OK).

| Schema | Action | Version | Diff |
|---|---|---|---|
| `friction.schema.json` | NEW | v1.0 | NEW entity. FRC-NN id pattern. Category enum (physical/emotional/friction_ux/logistical/cognitive). severity_score 1-10. customer_evidence[]. cross_refs vers objection_ids[] + pain_point_ids[]. Storage `brands/{slug}/frictions/{FRC-NN}.json`. Cross-ref doctrine compositional-cartography §"État atlas · couverture verbatims". |
| `roadmap.schema.json` | NEW | v1.0 | NEW entity. RDM-{brand_slug} id pattern. phases[] (phase_id, name, dates, status, priorities[]). mix[] (mix_id, weight 0-1, axis enum [audience, angle, product, funnel, creative]). production_status[]. relations cross-refs angles/audiences/products/creatives. Storage `brands/{slug}/roadmap.json` (brand-wide). |
| `spec.schema.json` | patch additif | v1.9 → v1.10 | benefits.items.properties · `emotional_signal` (string) + `latency_min`/`latency_max` (integer jours) + `evidence_verbatim[]`. mechanisms.items.properties · `duration` (string délai d'effet). meta · `validation_status` ($ref `_shared/validation-status.json`). |
| `profile.schema.json` | patch additif | v1.4 → v1.6 | pain_benefit_chain.items · `pain_category` enum (physical/emotional/friction_ux/logistical/cognitive/social_status, cohérent friction.schema). objections.items enrichi · `severity_score` 1-10 + `response_counter` (string) + `derived_angle_refs[]`. |
| `offer.schema.json` | patch additif | v2.1 → v2.2 | meta · `validation_status` ($ref `_shared/validation-status.json`). |
| `brand.schema.json` | patch additif | v2.2 → v2.3 | meta · `validation_status` ($ref `_shared/validation-status.json`). |

**Décision design SED-side** · NE PAS dupliquer `meta.source / meta.confidence` sur chaque schema. Le pattern `_field_types` per-field (observed/stated/derived/structured · cf section 5 + `field-types.md`) couvre déjà la sémantique source canon. Seul `meta.validation_status` est ajouté en composite uniforme (hypothesis/tested/validated/scaled/fatigued) via `$ref _shared/validation-status.json`, parce qu'il indique l'état de validation terrain (orthogonal à source canonique).

**Décision design SED-side · pas de objection.schema dédié** · 60% fragmenté volontaire. Doctrine compositional-cartography §4 confirme · objection n'est pas un arbre cartographique standalone, elle est consumée par profile (terrain audience) + angle (lever neutralization). Enrichissement profile.objections suffit. Anti-pattern cardinality dispersion évité.

**Activation runtime** · brief.schema v1.0 (shippé v2.42, orphan jusqu'à v2.56) activée via produce-copy-brief v1.4.0 Step 6bis. Storage canonical migré vers `brands/{slug}/briefs/{BRF-NN}.md`. Legacy path `produced/copy-briefs/` deprecated mais lecture backward compat.

**Bridge sync external (Layer 1 MCP)** · schemas v2.56 sont consommés par `sync-notion-atlas` skill v1.0.0 (pull-only MVP Phase A) pour synchronisation bidirectionnelle PhantomOS ↔ Notion workspace. Doctrine canonique de ce bridge · `docs/system/notion-bridge-doctrine.md`.

---

*Doctrine — consolidates 11 previously-scattered sub-disciplines (mutation rule, _field_types, _version semver, sourcing tags, triangulation, validation runtime, append-only conventions, snapshot/manifest regen, conventions plateforme, extension layer, memory & observability) into one named discipline. Sister to CMR, SAD, PTD scope under CI master.*
