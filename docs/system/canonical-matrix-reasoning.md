# Canonical Matrix Reasoning (CMR) — Operating Doctrine

> Working draft — R&D zone, Build mode. To be reviewed, then promoted to `workspace-template/docs/system/canonical-matrix-reasoning.md` in Release mode. **CMR is a sub-pattern of execution of `contextual-intelligence.md` (CI)** — CI is the master doctrine ("the agent reasons over a business universe, never form-fills"); CMR is the concrete mechanism by which a *production* skill achieves CI when its output is intersectional.

---

## 0. Scope

**CMR concerns only production skills whose output is intersectional** — that is, whose quality depends on combining ≥2 independent levers that a senior practitioner stacks (audience × angle × awareness × proof, etc.).

**Outside CMR scope** — other valid production patterns coexist :
- *Sequential* (email cadence, VSL macro skeleton, launch narrative arc) — pipeline with optional internal sub-matrices, but the output structure is ordered, not combinatorial.
- *Deterministic* (lookup, format conversion, audit-pixel binary check) — single variable load-bearing, no matrix needed.
- *Narrative* (one-off creative draft, ad-hoc memo) — appropriate when the domain has no stable canon yet (capture as learnings first, matricize after pattern detection on ≥3 occurrences).

CMR does NOT mean "every skill should be matrix-driven". It means "when a skill is intersectional production, the matrix is the right primitive, and these are its invariants." Capture skills (`mine-voc` lensing, `snapshot-brand` field gathering), navigators (`session-search`, `query-context`), builders (`build-agent`, `scaffold-extension`), and orchestrators of procedural pipelines are not CMR territory.

The decision-aid in §8 governs when CMR applies.

---

## 1. Thesis

> **Schema posé + matrice canon = mécanisme de cohérence d'output. Cible 95% qualité, consistent, non générique.**

This is the production mechanism behind every producer, curator, and orchestrator skill in PhantomOS. It is a system, not an instinct. It does not depend on the talent of the operator who triggered the skill, nor on the variance of the underlying model. It produces outputs that are reproducible across sessions, defensible against a senior practitioner, and grounded in a stable canon — at a quality level that narrative prompting cannot reach.

The doctrine has two components and they are not separable.

**Schema** — the typed substrate. Entities, fields, enumerated axes, closed vocabularies, `_field_types`, `_version`. The schema constrains *what kinds of objects can exist* in the agent's reasoning space.

**Matrix** — the combinatorial reasoning surface laid over the schema. Orthogonal axes drawn from canonical sources (Schwartz, Cialdini, Hormozi, Porter, Christensen, Wardley, internal frameworks). The matrix structures *how the agent combines* those objects to produce an output.

Either component alone fails:
- Schema alone → form-fill rigidity. Well-typed but flat output. No intelligence — the agent fills cells, does not reason.
- Matrix alone (without canon-grounded schema) → combinatorial hallucination. Variables invented session-to-session, no stability, no compound effect across skills.
- Neither → narrative prose. Generic output, ~60–70% quality at best, high variance, irreproducible.
- **Both → canon-grounded × combinatorial × cross-session coherent.** This is the 95% target.

CMR is the doctrine that names this and codifies the conditions under which it holds.

---

## 2. The problem CMR addresses

A modern LLM, prompted narratively over an unstructured domain, produces output whose quality plateaus around 60–70% of senior-practitioner level. The plateau has three structural causes:

1. **Latent space averaging.** Without an explicit decomposition, the model interpolates over its training distribution. The output is a soft average of plausible answers — fluent, defensible, generic. It is precisely what a junior copywriter produces: nothing wrong, nothing remarkable.
2. **Path-dependency in autoregressive generation.** The first sentence anchors the rest. A free-form prompt produces output where the *first generated angle* shapes every subsequent one. The model cannot backtrack and explore the Pareto front of options — it commits to a local optimum from token 1.
3. **No compound effect across skills or sessions.** Without a stable canon shared across skills, every skill re-derives its variables from scratch. *Scepticism* in one skill is *trust gap* in another. The system never accumulates expertise — it relitigates it.

Standard mitigations (decision trees, rules engines, hand-tuned prompts) hit other walls. Decision trees force a deterministic path and lose the model's intelligence. Pure rules engines need rigidly typed input — they break on the semi-structured material of strategy and copy. Hand-tuned prompts produce one-off quality that cannot be replicated by a different operator on a different brand.

CMR is the third path: **canonical axes + LLM-as-resolver + internal combinatorics + canon-anchored synthesis**. Schema makes the substrate machine-validatable. Matrix makes the reasoning visible to the model as a structured space. The model interpolates *within* that space, not against the open latent.

---

## 3. The hypothesis

A skill that satisfies CMR conditions reaches reproducible 95% senior-practitioner quality. Quality here is operationalized along five axes:

- **Defensibility** — every claim in the output traces to a canonical source ID or a flagged inference. No anonymous assertion.
- **Specificity** — outputs are not interchangeable across brands. A `paid-angles` run on a DTC pilot brand does not look like the same run on a B2C pilot brand.
- **Consistency** — two operators triggering the same skill on the same brand state get equivalent outputs. The skill is not a function of the operator's prompting style.
- **Compound** — the skill consumes canon variables that other skills also consume. Investments in canon pay across the entire skill graph.
- **Auditability** — the reasoning trace (cells considered, scores, dimensions activated) is recoverable from a run. The output is not opaque generation.

The 95% target is not aspirational. `produce-paid-angles` already operates at this level on encoded brands. The live test on a DTC pilot brand and the cascade design across `paid-angles` → `copy-brief` → `analyze-copy` validate the mechanism in practice. CMR codifies what makes that work.

---

## 3.5 Hierarchy among PhantomOS disciplines

CMR does not sit in isolation. It depends on, and is depended upon by, sister disciplines. Presenting them as peer is misleading — there is a real ordering:

```
Frame test : Extractibility (Extractibility test) — transverse, not a doctrine but a constraint test
 │
MASTER : Contextual Intelligence (CI) — the agent reasons, never form-fills
 │
 ├─ SED (Schema Encoding Discipline) — substrate ; without rigorous schema, a matrix has nothing to range over
 │ └─ Required prerequisite of CMR
 │
 ├─ CMR (Canonical Matrix Reasoning) — production mechanism atop SED
 │ ↑ depends ontologically on SED ; "schema alone fails, matrix alone fails, both succeed"
 │
 └─ SAD (Skill Authoring Discipline) — meta-discipline that governs how skills consuming SED+CMR are built
 ↑ operates above SED and CMR (skills consuming both are governed by SAD)
```

**Three load-bearing relationships:**
1. **SED < CMR (prerequisite).** A skill cannot satisfy CMR invariants if its substrate schema is not rigorous. Encoding the brand domain (entities, fields, vocab, sourcing tags) comes first. Once the schema holds, the matrix can be laid over it. Conversely, a clean matrix on a sloppy schema produces well-typed garbage.
2. **CMR ⊂ CI (sub-pattern).** CI states the goal (intelligence over universe, not form-fill). CMR states the concrete mechanism by which a production skill achieves it on intersectional outputs. CMR doesn't replace CI — it operationalizes it for one class of tasks.
3. **SAD > {SED, CMR} (meta).** SAD governs the *creation and evolution* of skills consuming SED and CMR. It includes the decision-aid (when to apply CMR, when not), composition contracts between skills, lifecycle (Build/Release, hooks, updates).

**A fourth discipline — PTD (Provenance & Trust Discipline)** — is cross-cutting and partial-scope today (multi-operator authorship, canon-as-product, marketplace skills). It is drafted in `research/provenance-trust-discipline-scope-2026-04-26.md` (R&D zone) and will graduate to full doctrine in `docs/system/` when trigger conditions hit (2nd operator connected, 1st knowledge pack sold, 1st third-party skill).

Doctrine governance (how to amend, retract, resolve conflicts among the disciplines) lives in `doctrine-governance-2026-04-26.md` as a meta-process, not a doctrine.

---

## 4. Cognitive mechanism — why CMR works for an LLM

**4.1 Discrete decomposition replaces latent averaging.** A narrative prompt asks the model to solve the whole problem at once. CMR asks the model to make *N independent decisions over a structured space*: for each cell `(audience × awareness × emotion × placement)`, score on five lenses. Each decision is small, well-typed, locally optimizable. The aggregate output is the *Pareto front* of the structured space, not the autoregressive local optimum.

**4.2 Typed cells reduce token-level variance.** When the model must produce an object conforming to a cell shape (`{angle_id, bias_id, mode, verbatim_anchor}`), the typing acts as a generation constraint. High-variance positions (open prose) become low-variance positions (enum picks + tightly-bounded text spans). The places where hallucination usually creeps in — name a proof source, invent a verbatim, claim a statistic — are precisely the places where canon anchoring forbids invention.

**4.3 Compound expertise across skills via shared canon.** When `paid-angles`, `copy-brief`, `analyze-copy`, and `creative-audit` all read `proof-registry.md` and `awareness-angle-matrix.md`, the model receives a *transferred specialization* without any fine-tuning. Equivalent functionally to a domain-specific model, achieved through shared external canon. The cost of building one skill amortizes across the skill graph.

**4.4 Cardinality control = attention budgeting.** Empirically, in-context reasoning quality degrades past ~120 cells. CMR enforces a hard cap (5 axes max, ~150–200 post-filter cells, output cap 5–7). This is calibrated to the limits of Sonnet/Opus in-context attention. It is not arbitrary — it is the largest space that still produces coherent reasoning.

**4.5 Selective activation prevents form-fill collapse.** A naive multi-axis prompt forces the model to score every cell, which dilutes signal. CMR gates each axis behind a binary activation test (*"is this dimension load-bearing on this corpus?"*). The model can skip an axis with a one-line dismissal — *"no signal on placement, all sources are Reels"*. This is the doctrinal correction of MECE-fundamentalism: imperfect orthogonality is acceptable if non-load-bearing axes are explicitly dropped, not silently filled.

---

## 5. Minimum anatomy

A schema + matrix pair satisfies CMR if and only if it carries the following invariants:

| # | Invariant | Why it is load-bearing |
|---|---|---|
| 1 | **Canon variables externalized** in JSON or MD under `resources/frameworks/`, `registries/`, or `shared-resources/`. Versioned with `_version` semver. | Inline-prose canon drifts session-to-session and cannot be diffed, validated, or shared across skills. |
| 2 | **Axes orthogonal in intent** — for each pair, one cell where A varies and B holds is producible. Imperfect orthogonality is acceptable if explicitly flagged. | Correlated axes double-count signal and produce inflated scores. Most axis correlations are partial; the discipline is to name them, not pretend they don't exist. |
| 3 | **Cardinality cap: 5 axes max, 3–8 values per axis, ~150–200 cells max post-filter, output cap 5–7.** Beyond → split into sub-matrices with a parent index. | Past these bounds, attention dilutes and the matrix becomes a PowerPoint inventory. |
| 4 | **At least one axis sourced to the canonical literature *of the domain modeled*** — *not a universal canon*. For copywriting : Schwartz/Cialdini/Sugarman/Hormozi. For consulting : Porter/Christensen/Wardley/Moore. For coaching : Kegan stages, ICF competencies. The canon must be native to what the skill produces, not borrowed from another domain. Skill-author-derived variables must carry `derived: {reasoning}`. | Without domain-native sourcing, the matrix is a framework of invention. Borrowing the marketing canon for a consulting skill produces a marketing-flavored consulting output — confused identity, no compounding. The discipline is portable ; the canon is not. |
| 5 | **Modulator vs cell distinction.** A *modulator* axis transforms the expression of a cell (subtlety mode, register, lexical density). A *cell* axis changes the strategy itself (angle, mechanism). Modulators apply in a second pass and do not multiply cardinality. | This is the stroke that saves cardinality. Schwartz `subtlety_mode` as modulator turns 8×8×3 = 192 paralyzing cells into 64 cells × 3 modes = 64 reasonable choices. |
| 6 | **Selective activation via binary tests.** Each axis carries a 2/3 or 3/3 condition that determines whether it is load-bearing on the current corpus. Non-activated axes are skipped with one-line dismissal in the trace. | Form-fill is the dominant failure mode. Selective activation makes the skill prescriptive, not exhaustive. |
| 7 | **Cluster dedupe rule.** Formal similarity rule (same A AND same B → merge) before output. | Without dedupe, ranked outputs contain 2–3 paraphrases of the same point, masking diversity. |
| 8 | **Internal scoring, external synthesis.** Cartesian product, scores, dimensions activated live in Layer A trace (JSONL audit log, never auto-loaded). Operator output is prose synthesis + ranked table + mutations. **Score never exposed.** | Exposing scores reproduces the BCG matrix failure: the score becomes the decision, the operator stops reasoning. |
| 9 | **Triangulation rule.** Any claim that lands in the synthesis is grounded in ≥3 sources or verbatims. Singleton sources flagged as hypothesis. | Without triangulation, one outlier verbatim becomes a canonical claim. |
| 10 | **Output cap 5–7 items, prose synthesis + ranked table.** Never the full enumeration. | Above 7, human cognition shifts from comparison to overwhelm. The matrix is a reasoning space; the output is the trace of selection. |
| 11 | **Modulator macro extended.** Beyond `awareness × sophistication` (Schwartz default), `persona` and `lexical_register` are also modulators when present — they transform how cells are expressed without multiplying cardinality. Persona varies cross-block in `analyze-copy` led to silent voice drift (the audit caught it intuitively but not by rule) ; treating persona as modulator macro fixes it. | Without explicit modulator macro, persona/register are tagged per-block, and cross-block consistency is invisible to the agent. Modulator macro applies in second pass and constrains all cells to a coherent voice. |
| 12 | **Tempo / narrative_tension_curve dimension** (when output is a multi-block artifact: VSL, sales letter, sequence, deck). Values: `rising`, `plateau`, `falling`, `wave`. The matrix optimizes per cell ; without a tempo dimension, 5 blocks scoring max-intensity each become wall-of-noise. | Pacing is half of a winning script (Sugarman Slippery Slide, SUG-001). The classical CMR matrix codes the strategic levers per block but is silent on the *trajectory* of intensity/curiosity-load. The tempo dimension constrains the trajectory globally. |
| 13 | **Compatibility-rule transverse `voice_consistency_cross_block`.** Persona and register must hold within ±1 step across all blocks of a multi-block output ; deviation = MAJOR violation. | The matrix is per-cell-optimized ; per-output-coherence is not native. A senior copywriter never lets bloc 1 in `peer` and bloc 4 in `authority` ; the rule encodes this otherwise-tacit invariant. |

These thirteen invariants are the binary tests for whether a skill instantiates CMR. A skill missing two or more is not CMR-compliant — it is either form-fill (missing #5, #6, #8) or hallucination-prone (missing #4, #9) or voice-incoherent on multi-block output (missing #11, #12, #13).

---

## 6. Three modes — coding, generating, pipeline (+ hybrid)

CMR matrices come in three functional modes plus an explicit hybrid. The distinction is load-bearing because each mode has different rules.

**Coding mode** — input is unstructured corpus, output is classification. Each verbatim (Reddit thread, Trustpilot review, customer interview) is mapped to a cell in the matrix. Example: `mine-voc` codes verbatims along `theme × JTBD × awareness × pain category`. Coding allows multi-tag (a verbatim may belong to two cells), tolerates partial coverage (not every cell needs an instance), and validates by inter-coder reliability (would another senior practitioner code this the same way?).

**Generating mode** — input is encoded brand state, output is novel artifact (angle, hook, brief, audit). The model picks one cell (or a small ranked set of cells) and synthesizes the artifact from canon variables instantiated by brand-specific data. Example: `produce-paid-angles` generates 5 ranked angles from `pain × objection × emotion × placement` cells, anchored on encoded verbatims. Generating forces resolution (one cell chosen per output slot), demands cell-completeness for the active subset, and validates by acceptance (would a senior practitioner ship this?).

**Pipeline mode (V2)** — input traverses a sequence of matrices in a defined order, each constraining the next. Example domains: consulting hypothesis trees (issue tree → root cause → recommendations), executive synthesis (situation → complication → resolution), coaching arcs (developmental stage → blocker → growth move). The matrix is decomposition-descendant rather than one-shot combinatorial: each layer applies its own axes, validates at the node, and feeds the next layer. Pipeline mode is the third primitive that lets CMR scale to verticals beyond marketing — the marketing canon is generative-flavored ; consulting and coaching canons are pipeline-flavored. *Status: V2, scoped now, full rules to be authored when first non-marketing skill is built.*

**Hybrid (coding + generating fluide)** — a single skill performs coding *while pre-thinking* generating, mid-flow. A senior copywriter mining VoC already pre-pictures the angles ; rigid separation forces an artificial coding-then-generating split that wastes the operator's flow. `analyze-copy` is structurally hybrid (codes the script blocks AND generates correction recommendations in the same pass). Hybrid is **valid as a single skill** when the two modes share a context window and one informs the other ; the alternative (split into two chained skills) is preferable only when the two stages can run independently or when an orchestrator legitimately needs the intermediate output. *Acceptance criterion : the skill carries `matrix_mode: hybrid` in frontmatter, names the two modes it carries, and documents the seam where coding hands off to generating.*

**Frontmatter declaration mandatory.** Every CMR-compliant skill declares `matrix_mode: coding | generating | pipeline | hybrid` in its SKILL.md frontmatter. The downstream rules differ:

| Rule | Coding | Generating | Pipeline | Hybrid |
|---|---|---|---|---|
| Multi-tag per cell | Allowed | Forbidden — one cell per output slot | Allowed at codification layer, forbidden at synthesis layer | Allowed during coding sub-phase, forbidden during generating sub-phase |
| Partial coverage | Allowed | Forbidden for active subset | Allowed at codification, full at synthesis | Allowed during coding sub-phase, full during generating sub-phase |
| Output | Classified corpus + synthesis | Novel artifact + verbatim anchors | Sequenced decomposition tree + executive synthesis | Classified input + corrections / recommendations |
| Failure mode | Misclassification (recoverable) | Generic output (silent quality collapse) | Decomposition error cascading downstream | Coding ambiguity leaking into generated output (mitigation: declare seam) |
| Canon sourcing | Required for axis enums | Required for axis enums **and** cell anchors | Required for axis enums at every layer | Required at both layers, with explicit seam declaration |

Hybrid mode is the explicit middle ground. The historical "split if conflated" rule was too rigid — it treated the natural flow of a senior practitioner (code while pre-thinking generation) as an architectural defect. Hybrid acknowledges that a single skill can carry both modes if and only if the seam is documented and verbatim-anchor obligations of generating are preserved. **Default: keep simple skills single-mode ; allow hybrid only when the operator's flow demands it.**

---

## 7. Anti-patterns

The following failure modes recur across PhantomOS skills and external matrix systems. They are named here for refusal-by-default.

| Name | Symptom | Fix |
|---|---|---|
| **Form-fill cascade** | Agent fills every cell for completeness before reasoning. Output has `## Block 1 — / ## Block 2 —` structure. | Selective activation hard rule. Synthesis prose, not block enumeration. |
| **Score leakage** | Numbers (87/100, density 4.2/5) surfaced to operator. | Layer A trace only. Operator sees prose + ranked table. |
| **Latent matrix (cell-as-prose-only)** | The matrix exists in MD narrative ("consider X, Y, Z") with no externalized JSON enum. | Externalize axes + cells in JSON, MD becomes commentary. |
| **Authority laundering** | Cell claims canon ID (`BL-005`) but applies it incorrectly. | Sourcing audit: each cell carries `canon_ref` *and* the citation must be applicable. Senior review before canon promotion. |
| **Correlated axes silently treated as orthogonal** | "Audience" and "awareness_stage" vary together. Scores doubled. | Document correlation explicitly in canon. Either fuse axes or define mutual conditional activation. |
| **PowerPoint matrix (BCG-style)** | Output describes a quadrant ("you are a Cash Cow") rather than prescribing an action. | Synthesis prose closes on action, not label. `output_mode: prescriptive` enforced in canon. |
| **Static matrix on dynamic market** | Porter's 5 forces applied to a 12-month-old DTC category. | Selective activation gated by market maturity tests. Schwartz longitudinal pattern (T-3y / T0 / T+3y) for evolving axes. |
| **Cardinality blowup** | 5×5×5×5 = 625 cells, no filter, score on everything. | Hard cap 5 axes, 150 post-filter. If naturally larger, split or hierarchize. |
| **Singleton-as-canon** | One verbatim promoted as a brand truth. | Triangulation rule (≥3 sources). Singletons flagged as hypothesis. |
| **Frozen canon** | Matrix written 6 months ago, market drifted, still in use. | Versioning + invalidation triggers. Cache TTL on derived layers. |
| **Improvised weights** | Scoring weights (35/20/20/25) baked in skill prose. | Externalize weights in `*-scoring.md` or `*-weights.json`. Diffable. |
| **Frontmatter mode missing** | Skill mixes coding and generating in the same step. | Mandatory `matrix_mode` declaration. Split if conflated. |
| **No deprecation path** | Renaming an enum silently breaks all consumer skills. | Alias table in canon (`{deprecated: replacement, removed_in: vN}`). Migration scripts. |
| **No test fixtures** | Compatibility rules added without regression coverage. | Fixtures under `tests/canon/` with expected violations. |
| **Sourcing-mort** *(domain-flavored: copywriting)* | Cells too anchored in canon → audit-pass output that is theoretically correct but *sterile*. Audit score 9/10 ≠ ship-ready. | Cap `audit_pass_score` at 8/10 max ; reserve 9–10 for tested-in-market validation. Compliance with canon is necessary but not sufficient — the copy must still *bet*. |
| **Permutation-without-pivot** | 5 ranked angles that all paraphrase the same underlying fear (or pain, or dream). Cluster filter dedupes by surface-level (pain + objection + placement) but lets the same emotional driver pass through repeatedly. | Add `emotional_diversity_check` post-rank: enforce that the top N angles do not all collapse to the same emotional driver category. |
| **Voice drift cross-block** | Block 1 in `peer` register, block 4 in `authority` register — incoherent voice across a multi-block output. Per-cell scoring is silent on this. | Compatibility-rule transverse `voice_consistency_cross_block` (invariant #13). Persona / register hold within ±1 step across all blocks. |
| **Absence du risk_bet** | The matrix optimizes for the median (high-cluster cells, score-validated). A senior practitioner *bets* on the non-obvious angle that scores 75 but breaks the category. Median-only output is professionally safe and competitively flat. | Add an optional `risk_bet` slot in the ranked output (e.g. "5 safe + 1 bet"). Flag the bet explicitly with hypothesis-to-test. Allows breakthrough discovery without inflating the safe baseline. |
| **Tyrannie du verbatim-anchored** | Cells must always be verbatim-sourced ; copy that *invents* a phrase the audience would have said but never did is structurally refused. Schwartz invented "lazy man's way to riches" — no verbatim. The matrix would have refused him. | Introduce an opt-in `--mode=breakthrough` that suspends the verbatim-anchor floor *for one slot in the output*, requires the operator to declare a hypothesis, and routes the output cell to learnings post-test. See §10bis. |

---

## 8. Decision-aid for skill creation

When an operator (or skill author) considers building a new skill, CMR provides the binary tests. **A skill that does not pass §8.1 should not use a matrix; it should use a simpler primitive (lookup, classifier, single-axis ranker, narrative prompt).**

### 8.1 When to use CMR

A matrix is the right primitive when **at least three of the following hold**:

- The output combines ≥2 independent factors that a senior practitioner stacks (audience × angle, awareness × sophistication × subtlety, pain × objection × proof).
- The domain has a stable canonical literature (Schwartz, Cialdini, Sugarman, Hormozi, Porter, Christensen, internal frameworks ≥3 brands of validation).
- The skill will be reused across N ≥ 3 brands, with same axes and brand-specific values.
- The historical failure mode on this domain is "everything technically correct, output flat" — the signature of union-not-intersection reasoning.
- A senior practitioner would draw a 2-axis or 3-axis grid on a whiteboard to think through the problem.

### 8.2 When to NOT use CMR

- The task is deterministic (lookup, filter, rename, format conversion).
- A single variable is load-bearing (audit "does the pixel fire?" — binary check, not matrix).
- The domain is too young for stable canon (TikTok organic 2026 viral patterns — capture as learnings first, matricize after pattern detection on ≥3 occurrences).
- The output is a singular non-rankable recommendation ("name your brand").
- Cardinality cannot be brought below ~500 cells even after splits.
- The output is a strictly ordered sequence (email cadence, VSL macro skeleton, launch narrative arc) — use a pipeline with internal sub-matrices instead.

### 8.3 Prerequisites

Before constructing the matrix:

1. **Canon variables exist** in `resources/frameworks/` or `shared-resources/` with `_version` and source citations. If absent → the agent **proposes 2-3 canonical references** of the domain to the operator (default recommendation + alternatives), encodes them itself by fetching publicly available material, and does not ask the operator to name the references. The operator validates the agent's recommendation, never sources the bibliography. If the domain has no established canon (emerging field, niche too young), fall back to capture-then-matricize via `learnings.json` until a pattern emerges. Detail of the canon-discovery primitive : `scaffold-extension` Phase 2bis.
2. **Verbatim corpus density** sufficient for generating mode (≥5 key_expressions per audience encoded). If absent → run `mine-voc` first.
3. **Persona expert named** — who does this in real life? If no human role can be pointed to, the matrix is academic.
4. **Scoring framework written** — explicit weights or activation tests, not "the model judges". Externalized in `*-scoring.md`.
5. **Cell exemplars** — at least one example cell per load-bearing axis pair. The model interpolates against exemplars; without them it generates from prior.

### 8.4 How to select axes

- **Load-bearing test.** If the axis is removed, does the recommendation change? No → drop it.
- **Orthogonality test.** Take five distant cells. Would a senior practitioner produce five differentiated outputs? If two cells produce paraphrases → axes are correlated → fuse or hierarchize.
- **Modulator vs cell test.** Does the axis transform the expression (modulator → applies in second pass) or change the strategy (cell → multiplies cardinality)? Subtlety, register, lexical density = modulators by default.
- **Authority test.** Each axis cites a canon source (book + ID, framework + section). Skill-author-invented axes are suspect — challenge before accepting.
- **Conditional activation.** Define the binary test that determines whether the axis activates on the current corpus. Examples: `placement` activates if multi-platform stack present; `Crossing the Chasm` activates if niche < 5 years old.

### 8.5 Cardinality control

- 2×2 — top-level binary decisions. Tufte-correct if axes are genuinely load-bearing.
- 3×3 to 4×4 — sweet spot for decisional matrices.
- 5×5+ — only with cluster filter, output cap, and selective activation.
- Internal cartesian (paid-angles 4–5 dim) — acceptable if score never exposed and dedupe enforced.
- Stacked matrices (study-niche-marketdeepdive) — acceptable if each matrix is gated and a primary frame hierarchizes the synthesis.
- Beyond 200 post-filter cells — split into sub-matrices, build a parent index, route via orchestrator.

---

## 9. Operational requirements

CMR is a doctrine; operationally it imposes the following infrastructure conventions. These are not optional once a canon is consumed by ≥2 skills.

**9.1 Canon storage and versioning.** Canons live in `resources/frameworks/`, `shared-resources/`, or domain-specific folders. Each carries `_version` (semver), `_schema` URI, and a deprecation table for renamed enum values. Major version bumps require a migration script for consumers.

**9.2 Consumer contract.** Each skill declares in its frontmatter the canons it consumes and the minimum version: `consumes: [{path, min_version}]`. A canon major bump triggers a re-test list of consumer skills.

**9.3 Severity canon centralized.** `BLOCKER / MAJOR / MINOR`, `observé / déduit / déclaré / incertain`, and `canon_ref / derived` all live in `shared-resources/severity-canon.json` or equivalent. Each skill instances the canonical enum, does not redefine.

**9.4 Pre-built indexes for matrices with ≥3 consumers.** `_manifest.json` pattern applied to canon: a derived index regenerated after canon edits. Skills read the index, not the source files, at runtime.

**9.5 Test fixtures.** Each canon with rules (e.g. `compatibility-rules.json`) carries fixtures under `tests/canon/`. Adding a rule requires adding at least one positive and one negative fixture. Run via `python3 .skills/validate-canon.py`.

**9.6 Frontmatter declarations.** CMR-compliant skills declare:
- `reasoning_pattern: matrix-driven`
- `matrix_mode: coding | generating`
- `consumes: [...]`

These three fields make CMR-compliance machine-verifiable.

---

## 10bis. Breakthrough mode — escape hatch for invariant #4 / verbatim-anchor

A doctrine that locks copy production to verbatim-sourced cells produces 95% safely. It also forecloses the 1% breakthrough — Schwartz inventing "lazy man's way to riches", Halbert inventing "the most amazing diet secret of all time". These phrases were not in any verbatim ; they were *posited* by the writer as the phrase the audience would have said but had not yet articulated. They tested into legends.

A doctrine that excludes that move misses the upside of the very practitioners it claims to encode.

**Breakthrough mode** is the explicit, opt-in escape hatch. It is *not* a relaxation of CMR — it is a typed exception with traceability obligations.

### 10bis.1 Activation

- Opt-in only. The operator passes `--mode=breakthrough` (or equivalent skill argument) at invocation. Default is canonical CMR with all anchors enforced.
- Never default. Skills NEVER auto-trigger breakthrough mode. The operator's intent must be explicit because the operator is *betting*.

### 10bis.2 Constraints

- **One breakthrough cell per output slot, max.** A 5-angle output can carry at most 1 breakthrough angle ; a 6-section brief can carry at most 1 breakthrough section. Quantitative cap prevents the breakthrough mode from collapsing into "anything goes".
- **Hypothesis declared.** The operator must declare in plain language what the bet is and what would falsify it (e.g. *"hypothesis: this audience secretly fears X but never says it ; falsified if CTR < baseline by 30% in week 1"*).
- **Cell tagged `bet=true, anchor=null, hypothesis_to_test={text}`** in Layer A trace. Visible to subsequent skills and audits.
- **Routes to learnings post-test.** When the operator returns with results (CTR, conversion, qualitative response), the breakthrough cell is promoted to learnings (if validated) or marked superseded (if falsified). This closes the loop and prevents the doctrine from drifting silently.

### 10bis.3 What it is NOT

- Not a permission to ignore the canon. The other cells in the output remain fully anchored.
- Not a creative brainstorm mode. It is a *typed bet* with documented hypothesis and result-routing.
- Not a default. Skills that always operate in breakthrough mode are not CMR-compliant — they are unanchored generation, full stop.

### 10bis.4 Operator surface

The breakthrough cell, when present, surfaces in the output with a clear marker (e.g. *"Pari : [angle]. Hypothèse : [...]. À valider en test."*) — not buried in the trace, not surfaced as an equal. The operator sees the bet exists, knows it is opt-in, and can choose to ship it or hold it.

This pattern was named after live red-team feedback that the original draft of CMR was *too safe* for the highest tier of copy production. It encodes Schwartz's, Halbert's, and Suby's actual practice — not just the median senior — without dissolving the discipline that protects against hallucination at scale.

---

## 10. Annex — Cartography of existing PhantomOS instances

| Skill / Doc | Mode | Axes | Canon | CMR-compliance | Gap |
|---|---|---|---|---|---|
| `produce-paid-angles` | generating | 4–5 dynamic of 8 (`pain × objection × emotion × awareness × placement × proof × offer × vernacular`) | `paid-angle-scoring.md`, `angle-registry`, `proof-registry`, `awareness-angle-matrix`, `hook-formulas` | ✅ Reference implementation. All 10 invariants present. | Weights in MD prose — externalize to `weights.json`. |
| `produce-copy-brief` | generating (pipeline + sub-matrices) | audience × angle × channel × 6 sections × verbatim density | Same registries + `voc-coding.md`, `hook-quality-spec.md` | ✅ Pipeline with internal sub-matrices. Compliant. | Channel inferred at runtime — formalize as conditional activation. |
| `mine-voc` | coding | 4 lenses (theme × JTBD × awareness × pain category) | `voc-coding.md` | ✅ Closed typology, conditional lens 4 activation. | Layer A corpus not always written — enforce in Hard Rule. |
| `mine-vom` | coding | vernacular × sophistication × white-space + selective Porter | `vom-mining.md` | ✅ Selective activation explicit. | Same Layer A gap. |
| `study-niche-marketdeepdive` | generating (stacked) | Porter selective + PESTEL selective + Schwartz longitudinal + Crossing + Capital flow + Disruption | `market-deepdive.md` | ✅ Gated activation, primary frame, cap 3000 words. | High cardinality risk if cap fails — keep monitored. |
| `analyze-copy` v0.1 | generating + coding mixed | 12 dimensions × 17 blocks × 30 compatibility rules | `pattern-schema`, `block-vocabulary`, `compatibility-rules`, `architectures/`, `principles/` | ⚠️ No modulator macro. Axes flat. Cardinality 12×17 = 204 not modulated. | Promote Schwartz `awareness × sophistication` to modulator macro. Conditional activation on remaining 12 dims. |
| `angles-biases-matrix.md` (canon) | generating template | 8 angles × 8 biais × 3 subtlety modes | Schwartz, Cialdini, Sugarman, Hopkins, Halbert | ⚠️ Modulator (subtlety) correctly placed. Verbatim anchor missing on cells. Status/Belonging/Insider correlation not flagged. | Add `voc_id` requirement per cell. Document axis correlations explicitly. |
| `pattern-schema.json` + `compatibility-rules.json` | schema | 12 dim × 30 rules | Self-canonical | ✅ JSON Schema validatable. Severity tiered. | Test fixtures absent. |
| Canon convergence clusters C1–C10 | meta-matrix | 10 convergences × media × audience (latent) | INDEX.md cross-cuts | 📋 Not yet sacralized as a macro-matrix. | Canonize as macro-matrix that constrains sub-matrices. |
| `audit-meta-account` | generating | 5 blocks × statut × impact × action | Meta convention canon | ✅ MECE strict, prescriptive. | Sub-block cardinality — verify on next audit. |
| `score-product-fit` | generating | spec × profile × 3 scoring axes | Inline weights | ⚠️ Pondération hard-coded in SKILL.md. | Externalize to scoring framework. |

**Key takeaways from the cartography:**
- `paid-angles` is the reference. Use it as the template for any new producer skill.
- `analyze-copy` is the most mature gap — refactor with modulator macro before next ship.
- `angles-biases-matrix` needs verbatim anchoring before it becomes a footgun (operators copy template phrases as if they were sourced).
- The 10 convergence clusters (C1–C10) are an unexploited macro-matrix. Their canonization would constrain every sub-matrix in the copy domain.

---

## 11. Open tensions (to be resolved progressively)

1. **Static vs dynamic matrices.** Theoretical canon (Schwartz, Cialdini) → static, versioned slowly. Brand-specific applied matrices (paid-angles output) → dynamic, regenerated per run with cache TTL + invalidation. Working rule, to be validated on three more skills.

2. **Canon governance.** Adding an axis to `angle-registry`: who decides, on what evidence, with what migration path? Proposed rule: ≥2 brands demonstrating the need, ≥1 cell exemplar per existing axis pair, version bump, consumer re-test.

3. **Cross-brand learning.** Once `mine-vom` runs on 50 DTC brands, we have a dataset of "Porter forces actually activated by sub-vertical". Should this update activation priors (Bayesian update) or remain a static activation test? Risk: kills the per-brand activation test. Reward: faster, more accurate activation. To be addressed in v2.

4. **Macro-matrix canonization.** The C1–C10 convergence clusters are a macro-matrix in waiting. Canonize them now as a constraint layer, or keep them as descriptive pattern observations? Recommendation: canonize, with the explicit rule that any sub-matrix axis must map to ≥1 convergence cluster.

5. **Coding/generating boundary skills.** `analyze-copy` currently does both (codes the script blocks, generates correction recommendations). Split into two chained skills, or accept the hybrid? Working hypothesis: split at v0.2 if quality variance is observed.

6. **Severity canon centralization.** `BLOCKER/MAJOR/MINOR` is reproduced in three places. Centralize now (small refactor) or wait for a fourth instance (forces the consolidation by clear pattern)? Vote: now, while it is still a 3-call refactor.

---

## Amendment protocol

To amend this doctrine, follow the procedure documented in `docs/system/doctrine-governance.md` § Amendment : draft the change in a research note, register a new D# entry in `decisions.md` with explicit `[SUPERSEDES Dxxx]` annotation, patch the doctrine file with a changelog header, and surface a re-test list of consumer skills. Silent edits to a binding doctrine are refused by convention.

---

## 12. Cross-references

- `docs/system/contextual-intelligence.md` — sister doctrine. CI defines *what* the agent reasons over (the business universe). CMR defines *with what mechanism* (canon + matrix). When in conflict, CI wins on substantive judgment, CMR wins on production discipline.
- `CLAUDE.md` root § Master doctrine — to be amended with CMR as the named production mechanism behind Contextual Intelligence.
- `docs/system/voice.md` — operator-facing implications (no score leakage, no path leakage, no enum jargon).
- `docs/system/skill-builder-cartography.md` — to be updated with CMR decision-aid (§8) as the primary gate before scaffold.
- Canon files: `shared-resources/copywriting-canon/`, `resources/frameworks/`, brand-side `brands/{slug}/research/`.
- Reference skills: `produce-paid-angles` (template), `produce-copy-brief` (pipeline-with-sub-matrices), `mine-voc` (coding mode), `analyze-copy` (refactor target).

---

## 13. Status

- **Draft** — research zone, Build mode. To be reviewed by the maintainer, iterated, then promoted to `workspace-template/docs/system/canonical-matrix-reasoning.md` in Release mode.
- **Implementation roadmap** — Phase 3 of the cadrage: audit each producer/curator/orchestrator skill against §5 invariants, scope patches, ship v2.10.x batch.
- **First applications** — refactor `analyze-copy` with modulator macro. Patch `angles-biases-matrix` with verbatim anchoring. Canonize C1–C10 macro-matrix. Externalize `paid-angle-scoring` weights to JSON.

---

*Doctrine — internal review.*
