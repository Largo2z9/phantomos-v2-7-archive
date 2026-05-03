# Skill Authoring Discipline (SAD) — Operating Doctrine

> Working draft — R&D zone, Build mode. To be reviewed, then promoted to `workspace-template/docs/system/skill-authoring-discipline.md` in Release mode. **SAD is the meta-discipline above SED + CMR.** It governs how skills consuming the substrate (SED) and the production mechanism (CMR) are created, evolve, compose, and fail safely. Without SAD, skill authors re-invent gates session-to-session, doctrines drift in the absence of governance, and the system depends on Largo's mental arbitration to stay coherent.

---

## 1. Thesis

> **A skill is a contract, not a script.**

Every skill PhantomOS ships obeys an implicit contract: it declares what kind of skill it is (taxonomy), what it consumes (canon, schemas, prior skills), what it produces (artifacts, mutations, traces), and what invariants it holds (CMR-compliance or explicit no-matrix declaration, sourcing rules, surface contract). When the contract is implicit, skill authors guess at the gates. When the contract is explicit, skill authors compose reliably across the workspace.

SAD names the contract. It absorbs the cartography of skill authoring (`skill-builder-cartography.md`), the creation protocol with its graduation matrix (`skill-creation-protocol.md`), the red-team posture for skill design (`skill-architecture-redteam.md`), the resource discovery pattern (`skill-resource-discovery.md`), the SOP-to-skill conversion methodology (`sop-skill-conversion.md`), and the skill taxonomy + model routing rules (`patterns.md`). It adds three rules previously implicit: **frontmatter triad** (CMR-compliance machine-verifiable), **Skill Composition Contract** (how skills chain stably), and **Failure doctrine** (what happens when a skill violates its contract at runtime).

It also absorbs as a sub-corpus the system-level concerns that govern *the workspace as it lives* — hooks, Build vs Release, updates, provider-agnostic dimension. These touch every skill but are not skill-internal ; they are the lifecycle envelope around skills.

---

## 2. The problem SAD addresses

Without an authoring discipline, three failure modes accumulate:

1. **Skill proliferation without governance.** A skill author with a fresh idea creates a sibling skill instead of extending an existing one. The catalogue bloats, mental model fragments, gates duplicate. Pattern named in `skill-creation-protocol.md` (extend > create), but isolated. Without SAD as a chapeau, the rule is easy to ignore.
2. **Implicit contracts break composition.** A producer skill outputs a structure that the next skill in the chain expects ; if either drifts independently, the chain breaks silently. No `consumes:` declaration ties them ; no version compatibility check fires.
3. **Failure modes are unhandled.** A skill that violates a CMR invariant at runtime (score leakage, missing modulator, axes correlation untreated) does so silently. Largo notices in review, files a `correct-skill` [backlog, not shipped] ticket. The doctrine is enforced human-in-the-loop, not systemically.

SAD fixes all three: by codifying authoring rules, by formalizing composition contracts, by introducing a failure doctrine that routes invariant violations automatically.

---

## 3. Three layers of authoring

SAD operates at three layers:

**Layer 1 — Single skill authoring.** What makes one skill well-formed. Frontmatter declarations, type taxonomy (producer / curator / capturer / orchestrator / navigator / builder / shared), CMR-compliance binary, hard rules, persistence pattern, model routing.

**Layer 2 — Skill composition.** How skills chain reliably. `consumes:` declaration, output contract for downstream consumers, orchestrator patterns, ticket lifecycle for long deliverables.

**Layer 3 — System lifecycle (sub-corpus).** How the whole skill ecosystem evolves over time. Hooks, Build/Release governance, updates mechanism, provider-agnostic dimension, deprecation paths.

The doctrine is layered because the answers differ at each layer. *"Should this be a skill?"* is layer 1. *"Should this skill chain into that one?"* is layer 2. *"Should this hook fire on every workspace mutation or only some?"* is layer 3.

---

## 4. Minimum anatomy — what makes a skill SAD-compliant

A skill satisfies SAD if and only if it carries:

| # | Invariant | Why it is load-bearing |
|---|---|---|
| 1 | **`type:` declared** in frontmatter, valid taxonomy member (producer / curator / capturer / orchestrator / navigator / builder / shared). | Type drives default model, subagent_safe, permissions baseline. Type-missing skills are refused by `validate-resources`. |
| 2 | **CMR-compliance frontmatter triad** — `reasoning_pattern: matrix-driven` (or `null` for explicit no-matrix), `matrix_mode: coding | generating | pipeline | hybrid` (when matrix-driven), `consumes: [{path, min_version}]`. | Makes CMR-compliance machine-verifiable. Skills without `reasoning_pattern` declared fail the SAD check. |
| 3 | **Disambiguation declared** when triggers overlap with sibling skills. `disambiguates_against: {skill_name: routing_condition}` block in frontmatter. | When 2+ skills match an operator intent, the manifest entry's `disambiguates_against` resolves the routing. Without it, the agent guesses. |
| 4 | **Hard rules numbered and explicit.** Each Hard Rule is a one-line, refusable invariant ("audit ≠ rewrite", "verbatim anchor required per cell", "score never exposed"). | Implicit rules drift. Numbered rules are auditable, refusable by hooks, traceable to violations. |
| 5 | **Persistence path declared** when the skill writes artifacts. `Persistence: brands/{slug}/audits/{date}-{id}.md` or equivalent. | Operators expect to find what was produced. Skills that write nowhere or to ad-hoc paths break the workflow. |
| 6 | **Operator-facing language** — no doctrine acronyms (CI / SED / CMR / SAD / PTD), no internal jargon (`field_path`, `_field_types`, `mode=proposed`), no path leaks except for legitimate references. | Per CI surface contract. Acronym leak in operator output = violation. |
| 7 | **`extend_before_create` honored.** New skill author confirms (in commit message or capture-learning entry) that no existing skill could be extended (new mode, new phase, conditional input) before creating a sibling. | Sibling skills duplicate gate logic and fragment operator mental model. Pattern validated S31 (`integrate-variable` rejected for `scaffold-extension` dual-mode). |
| 8 | **Output declared** — what the skill returns to the agent vs writes to disk. Layer A (audit trace) vs Layer B (operator output) separation explicit when the skill is matrix-driven. | Without explicit output declaration, the agent guesses at consumption. Downstream skills break. |
| 9 | **Failure mode declared** — what happens when a Hard Rule is violated at runtime (refuse, fall back, surface to operator, route to `capture-learning`). | The default is silent failure. Explicit failure mode prevents that. |
| 10 | **`recommended_model` + `subagent_safe`** declared. Routing matrix per `patterns.md § Model Routing`. | Skills run on the wrong model produce wrong-cardinality outputs. Subagent-unsafe skills launched in subagents corrupt state. Both must be machine-checkable. |

---

## 5. Skill Composition Contract

When skills chain (orchestrator → sub-skill, producer → capturer, paid-angles → copy-brief → analyze-copy), the composition is fragile by default. SAD codifies what makes chains stable.

**5.1 — `consumes:` declaration mandatory.** Every skill that reads from another skill's output, or from a canon file, declares the source path and minimum compatible version : `consumes: [{path: "shared-resources/copywriting-canon/frameworks/angles-biases-matrix.md", min_version: "1.0.0"}]`. A canon major version bump triggers a re-test list of consumer skills, surfaced in the upgrade flow.

**5.2 — Output contract stable.** A producer skill declares its output schema (Layer B operator output) and treats it as a public interface. Breaking changes require a major version bump and migration path for consumers.

**5.3 — Orchestrator patterns.** Four canonical orchestration patterns (named in `skill-architecture-redteam.md`):
- *Sequential pipe* — A → B → C, each consuming the prior. Default for chain-style production.
- *Fan-out* — A produces N inputs, B…M run in parallel on each. Used for multi-audience exploration.
- *Batch aggregate* — N independent runs collapsed into a single synthesis. Used for cross-brand learning.
- *Conditional branch* — A produces a routing signal, B *or* C runs based on it. Used for skill disambiguation flows.

Each pattern has its own composition rules, declared in the orchestrator's SKILL.md.

**5.4 — Ticket lifecycle for long deliverables.** Any skill whose execution exceeds ~10 min, spans sessions, orchestrates 2+ sub-skills, or produces a client-facing deliverable opens a ticket in `brands/{slug}/tickets/`. Operator interacts via `where is ticket X` / `pause` / `resume` / `close`. Skill is responsible for emitting events the ticket consumes.

**5.5 — Backwards compatibility.** A skill chain that was working continues to work after either skill in the chain is upgraded — unless the upgrade is a major version bump, in which case the migration path is explicit.

---

## 6. Failure doctrine — what happens when a Hard Rule is violated at runtime

Doctrines that lack a failure mode rely on Largo's review to catch violations. At scale (20+ operators, hundreds of skill invocations per day), this breaks.

**6.1 — Invariant-violation hook.** A new hook (`invariant-violation-detector.py`) inspects skill outputs at end-of-turn. It looks for canonical violations:
- Score leakage (numbers like `87/100` or `density: 4.2/5` in operator-facing output)
- Modulator missing (multi-block output without `voice_consistency_cross_block` check)
- Verbatim anchor missing (generating mode without `voc_id` per cell)
- Frontmatter CMR incomplete (matrix-driven skill without `matrix_mode` or `consumes`)
- Persona drift (multi-block output where persona varies > 1 step)

**6.2 — Routing on violation.**
- *Mechanical violation* (frontmatter missing, schema invalid) → refuse, surface to operator with redirect.
- *Semantic violation* (style drift, score leak) → log as `capture-learning` candidate, surface to Largo as flag, do not block operator output.

**6.3 — Cumulative pattern detection.** When the same skill produces ≥3 violations of the same type within a 7-day window, the violation graduates to a *pattern* and is auto-routed to `correct-skill` [backlog, not shipped] for hard rule integration.

**6.4 — Operator transparency.** Operator sees only relevant flags ("audit-pass score plafonné à 8/10 — copy needs market validation before promoted to 9-10"). Internal mechanics (which rule, which violation count, which routing) stay in Layer A trace.

---

## 7. Sub-corpus — System Lifecycle & Enforcement

The temporal dimension of the skill ecosystem. How the whole system evolves and stays consistent.

**7.1 — Hooks transverses.** Six active hooks today (mutation-guard, convention-guard, budget-warn, checkpoint-resolver, post-write-flush, turn-end-audit) + invariant-violation-detector to add. Each hook is mechanical (refuses an invalid state ; never debates the model). Hooks are versioned semver, manifested in `.claude/hooks/_manifest.json`.

**7.2 — Build vs Release governance.** Two strict modes (codified in project `CLAUDE.md`). Build mode = R&D, touches `research/`, `sandbox/`, `schemas/`, project docs. Release mode = ships to `workspace-template/`, requires manifest, version bump, sync to derived workspaces. Cross-mode commits are refused.

**7.3 — Update mechanism.** `_version.json` per workspace, `docs/releases/{version}-manifest.json` per release, `update-workspace` orchestrator skill, `docs/system/updates.md` doctrine. Type taxonomy: doc / skill-added / renamed / removed / schema-bump / infra / breaking. Migration scripts mandatory for breaking.

**7.4 — Provider-agnostic dimension.** Skills declare `recommended_model` per provider class (Sonnet / Opus / Gemini / Codex). When provider-agnostic full doctrine ships, model-class mapping is centralized. Today, default Anthropic class ; other providers fall back gracefully.

**7.5 — Catalogue size hygiene.** When the skill catalogue exceeds 60 skills, the `?` shortcut response shifts from listing to *recommendation* (one skill recommended in context, not a menu). Threshold codified to anticipate operator overwhelm.

**7.6 — Deprecation path.** A skill marked for retirement enters a `[DEPRECATED Sxx]` window of ≥30 days, during which consumers must migrate. After window, removal. Refusal of new consumer adoption during deprecation window is enforced by the manifest builder.

---

## 8. Anti-patterns

| Name | Symptom | Fix |
|---|---|---|
| **Sibling skill before extension** | Author creates `produce-vsl-skeleton` next to `produce-copy-brief` instead of extending the latter with a `--mode=vsl` argument. | `extend_before_create` rule + commit message check. |
| **Frontmatter incomplete** | Skill missing `type`, or matrix-driven skill missing `matrix_mode`, or no `consumes` block. | `validate-resources` refuses. CMR-compliance machine-verifiable. |
| **Implicit composition** | Skill A's output structure consumed by skill B without `consumes:` declaration. | Mandatory `consumes:` triad. |
| **Catalogue jargon-stack** | 80 skills, 80 names, operator overwhelmed. | Catalogue size hygiene + `?` shortcut shift to recommendation. |
| **Silent failure** | Skill violates a Hard Rule, output ships anyway, no flag. | Invariant-violation hook + cumulative pattern detection. |
| **Acronym leak in operator output** | "This skill applies CMR sub-pattern of CI to produce..." | Operator-facing rule (CI surface contract). Hooks scan for acronyms in user-facing strings. |
| **Skill type missing** | Skill author forgets to declare `type:`. | `validate-resources` refuses CRITICAL. |
| **Sub-skill exposed as orchestrator** | A sub-skill with `subagent_safe: false` accidentally invoked at top level. | `recommended_model` + `subagent_safe` matrix in `patterns.md § Model Routing`. |
| **Build/Release cross-contamination** | Commit touches both `research/` and `workspace-template/`. | Pre-commit hook refuses ; project CLAUDE.md enforces. |
| **Deprecation without window** | Skill removed without `[DEPRECATED]` window, consumers break overnight. | Deprecation governance — minimum 30-day window. |

---

## 9. Decision-aid — when authoring a new skill

The skill author asks, in this order:

1. **Is there an existing skill that already covers this intent ?** Search `_manifest.json` triggers + descriptions. If yes → either route to that skill or propose an extension.
2. **Is this a producer (intersectional output) ?** If yes → CMR applies, plan the matrix structure first (axes, modulator, cardinality, sourcing). Frontmatter `reasoning_pattern: matrix-driven`.
3. **What type ?** Run the binary tests in `patterns.md § Skill Taxonomy`. Type drives default model + subagent_safe + permissions.
4. **What does it consume ?** Canon files, prior skills, brand entities. Declare `consumes:` with minimum versions.
5. **What does it produce ?** Layer A trace structure. Layer B operator output. Persistence path.
6. **What are the Hard Rules ?** Numbered, refusable, traceable.
7. **What is the failure mode ?** Per Hard Rule, what happens at violation.
8. **Operator-facing surface ?** Language adapted, no acronyms, no jargon, no path leaks.
9. **Disambiguation ?** If the trigger overlaps with another skill, declare `disambiguates_against`.
10. **Run red-team checklist** from `skill-architecture-redteam.md` before commit.

---

## 10. Cross-references

- **`contextual-intelligence.md`** — master doctrine. SAD operationalizes the surface contract of CI for every skill that ships.
- **`canonical-matrix-reasoning-2026-04-26.md`** — CMR. SAD's CMR-compliance frontmatter triad is the machine-verifiable bridge between SAD authoring and CMR invariants.
- **`schema-encoding-discipline-2026-04-26.md`** — SED. Skills must respect SED at the substrate layer (mutation gate, sourcing tags, triangulation, layer separation).
- **`provenance-trust-discipline-scope-2026-04-26.md`** *(R&D zone, lives in `research/` until promotion triggers hit)* — PTD scope. When PTD ships full, SAD will extend with third-party authoring rules (signing, provenance, sandbox).
- **`doctrine-governance-2026-04-26.md`** — meta-process for amending SAD itself.
- **`skill-builder-cartography.md`** — pre-existing input. Domain vars → schema → code mapping.
- **`skill-creation-protocol.md`** — pre-existing input. Graduation matrix, gates, extend-first.
- **`skill-architecture-redteam.md`** — pre-existing input. Anti-patterns, design invariants.
- **`skill-resource-discovery.md`** — pre-existing input. FTS5 runtime + priority rules.
- **`sop-skill-conversion.md`** — pre-existing input. Methodology vs execution separation.
- **`patterns.md`** — pre-existing input. Skill taxonomy + Model routing.
- **`skill-authoring-toolkit.md`** — optional companion. Names the prompt engineering patterns that the doctrines apply implicitly (dense prompting principles, magic keywords curated, interaction patterns, upstream questioning). Levers not constraints. Cross-ref to `largo-kb/02-ai/prompting/` for full library.
- **`extending.md`** — extension layer rules ; SED chapter that SAD references for custom skills.
- **Hooks** — `mutation-guard`, `convention-guard`, `budget-warn`, `checkpoint-resolver`, `post-write-flush`, `turn-end-audit`, `invariant-violation-detector` (to add).

---

## 11. Open tensions

1. **Failure doctrine cumulative threshold.** "≥3 violations of the same type within 7 days = pattern" is a working rule, not validated. To be tuned after first month of invariant-violation-detector live.

2. **Sub-corpus System Lifecycle scope.** Hooks, Build/Release, updates, provider-agnostic — all genuinely belong here, but the sub-corpus risks growing into its own doctrine. Boundary: anything that touches the workspace as it *lives* over time = SAD lifecycle. Anything brand-side temporal = SED memory & observability. Boundary may need re-arbitration.

3. **Third-party skill authoring.** When community contributions ship (cf PTD scope), SAD will need a "third-party authoring" section — signing, provenance, sandbox canon namespace. Drafted in PTD scope today, will move to SAD when PTD graduates.

4. **Catalogue threshold for `?` shortcut.** "60 skills" is approximate. Real threshold is when operators report overwhelm. To be measured, not declared.

5. **Skill Composition Contract versioning.** Today implicit. Should each producer skill version its output schema explicitly (so consumers can target a specific version) ? Adds overhead. Working rule: version the canon, version the skill ; output schema follows the skill version. Re-arbitrate if breaking changes recur.

6. **Failure doctrine + CI semantic-trust tension.** CI says "trust the model on semantic, in-session memory fixes". Failure doctrine says "detect semantic violations and route to capture-learning". These are not in conflict (semantic violations CAN be detected mechanically — score leakage, missing modulator are syntactically detectable), but the boundary needs articulation.

---

## Amendment protocol

To amend this doctrine, follow the procedure documented in `docs/system/doctrine-governance.md` § Amendment : draft the change in a research note, register a new D# entry in `decisions.md` with explicit `[SUPERSEDES Dxxx]` annotation, patch the doctrine file with a changelog header, and surface a re-test list of consumer skills. Silent edits to a binding doctrine are refused by convention.

---

## 12. Status

- **Draft v0.1** — research zone, Build mode, .
- **Promotion criterion** — to be reviewed by Largo, then promoted to `workspace-template/docs/system/skill-authoring-discipline.md` once cross-references with CI / SED / CMR / PTD scope are validated and the 5 pre-existing skill-* docs are confirmed consolidated as referenced inputs (not deprecated, kept as detail references).
- **First applications** — frontmatter triad pass on 6 CMR-adjacent skills, mass `reasoning_pattern: null` declaration on 49 non-matrix skills, invariant-violation-detector hook draft, catalogue size measurement.

---

*Doctrine — consolidates 5 previously-scattered skill-* docs (skill-builder-cartography, skill-creation-protocol, skill-architecture-redteam, skill-resource-discovery, sop-skill-conversion) + patterns.md skill sections + sub-corpus System Lifecycle & Enforcement (hooks, Build/Release, updates, provider-agnostic). Sister to SED, CMR, PTD scope under CI master.*
