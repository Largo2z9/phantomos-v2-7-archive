# Changelog

> Auto-maintained by skills (ingest-resource, validate-resources, setup-brand).
> Never edit manually. Newest entries at top.

---

## v2.6.3 — 2026-04-19 — Disambiguation + brand-snapshot + update mechanism

**Action**: two perf patches + the bootstrap of the update distribution system. Cuts routing ambiguity, snapshot-first reduces brand state reload cost, and installs the machinery so future updates land cleanly on tester workspaces without losing data.

**Performance patches**:
- `disambiguates_against` field added to 5 skills with trigger collisions (setup-brand / onboard-brand / snapshot-brand on "setup/onboard", validate-resources / audit-meta-setup on "audit"). Each entry spells out the literal routing condition for sibling skills. Manifest generator captures and exposes.
- `brands/{slug}/_snapshot.md` digest system. `.skills/build-brand-snapshot.py` reads brand.json + products + audiences + offers + strategy and writes a 1-2KB plaintext digest. Agent reads one file for brand state queries instead of parsing 5+ JSONs. CLAUDE.md § Context DB directs agent to snapshot first. Mutation rule now mandates snapshot rebuild on any write to brand core files. Snapshots generated for `_TEMPLATE` and `_EXAMPLE`.

**Update mechanism bootstrap** (new):
- `_version.json` at template root — current template version registry.
- `/operator/installation.json` convention — receiver tracks its installed version + update history.
- `docs/releases/{version}-manifest.json` — per-release machine-readable change manifest. Types: `doc-change/added`, `skill-added/renamed/removed`, `schema-bump`, `infra-change/added`, `breaking`. Spells out every change for the receiver's agent.
- `update-workspace` skill (orchestrator, sonnet, subagent_safe: false) — installer. Reads installed version, finds applicable manifests, applies each change by type, delegates schema bumps to `migrate-workspace`. Safety guarantees: never touches `brands/{slug}/*` (except _TEMPLATE/_EXAMPLE), `operator/`, `credentials.env`, user-authored extensions under `brands/{slug}/custom/`, or custom skills under `.skills/skills/custom/`. Writes to `/operator/installation.json → history[]`.
- `docs/system/updates.md` — maintainer doctrine. Template-vs-operator data separation, change type reference, publishing checklist, anti-patterns.
- `.skills/build-update-manifest.py` — auto-generates a draft manifest from `git diff` between two refs. Pre-fills ~80% (doc/skill/infra classifications + renames). Maintainer reviews and manually adds schema-bumps + breaking flags.

**Rationale**: the testers come back in two weeks wanting the latest version. Without this mechanism, they'd either lose data (on a brute re-install) or miss the update entirely (on a conservative skip). The manifest format forces maintainer discipline and the receiver's agent executes mechanically with zero ambiguity.

---

## v2.6.2 — 2026-04-19 — Skill naming hygiene pass (11 renames)

**Action**: pre-distribution naming audit on 29 skills. 11 renamed for consistency (verb-noun convention, no agent suffixes, no standalone nouns, operator-recognizable vocabulary). 18 skills kept as-is. Trigger phrases untouched (operator natural language, not skill names).

**Renames applied**:
- `snapshot` → `snapshot-brand` (standalone noun → verb-noun)
- `daily-brief` → `brief-day` (verb-led)
- `audit-setup-meta` → `audit-meta-setup` (platform before scope, "audit the Meta setup" reads clean)
- `onboard-brand-full` → `onboard-brand` (dropped ugly `-full` suffix)
- `audience-miner` → `mine-audience` (dropped `-er` agent suffix)
- `competitor-watcher` → `watch-competitors` (dropped `-er` agent suffix)
- `product-audience-fit` → `score-product-fit` (added verb)
- `migrate-instance` → `migrate-workspace` (operator vocab: "workspace" used everywhere else)
- `validate-nomenclature` → `validate-naming` (dropped heavy jargon)
- `query-resource` → `query-context` (scope accuracy: queries the whole brand context)
- `check-existing-encoding` → `check-existing-coverage` (dropped internal jargon; "coverage" names what the 5-dim gate actually checks)

**Kept as-is**: scaffold family, build-agent, setup-brand, ingest-resource, validate-resources, capture-learning, learn-from-session, promote-learning, resume-session, analyze-extension-intent, propose-schema-draft, validate-schema-canon, check-cross-refs, register-and-flag, red-team.

**Ripple coverage**: 11 folder renames, frontmatter `name:` updated, cross-refs updated across CLAUDE.md + docs/ + catalogue + orchestrators (onboard-brand, resume-session, build-agent, scaffold-extension) + legacy `agent_id` stamps in mine-audience / score-product-fit / watch-competitors + session-state.md + tickets/README.md. Historical CHANGELOG entries (v2.4-v2.6.1) left untouched — renames document themselves in this entry.

**Rationale**: skill names become shared vocabulary. When the agent says *"je lance X"*, the operator needs to parse it instantly. Agent suffixes (-er, -watcher, -miner) and standalone nouns read as tool jargon ; verb-led names read as operator actions. Pass closed before first external testers touch the workspace.

---

## v2.6.1 — 2026-04-19 — scaffold-extension dual-mode (intent-first + data-first)

**Action**: `scaffold-extension` extended to accept both operator entry points on the same orchestrator, no new skill. Removes the need for a separate `integrate-variable` (rejected as redundant).

**Patched — `scaffold-extension/SKILL.md`**
- Added `Invocation context — two modes of entry` section. Intent-first (operator brings intention, empty structure created) vs data-first (operator brings concrete data, routed to existing or scaffolded and populated in a single flow). The five-dimension gate in Phase 2 is the pivot in both modes.

**Patched — `analyze-extension-intent/SKILL.md`**
- Method split to handle both entry modes. Data-first infers class/shape/population/cross-refs silently from the provided data, asks max one sharpening question on genuine ambiguity.
- Output schema now carries `entry_mode: "intent_first | data_first"` and `provided_data: {...}` (only populated in data-first mode, passed downstream to Phase 7).

**Patched — `scaffold-entity-files/SKILL.md`**
- Instance write logic now conditional on entry mode. Intent-first optionally writes an empty starter. Data-first **must** populate one or more instance files from `provided_data`, shape driving the count (`instance_per_item` → N files, `time_series` → 1 series file, `aggregate` → 1 aggregate file). `_field_types` marked `observed` for operator-provided values, `derived` for anything computed. Halts on schema mismatch.
- Sidecar path initialized from `provided_data` in data-first, empty in intent-first.

**Patched — `docs/system/extending.md`**
- Added `Two modes of invocation` subsection above `How to invoke`. Clarifies that the same skill covers both "I have an intention" and "I have a data block to range properly" — the gate decides between route-into-existing and scaffold-then-populate.

**Rationale**: the operator works in objectif + action, not in technical decision trees. A separate skill for data placement duplicated the gate logic and split the mental model. One orchestrator, two entry modes, same gate.

---

## v2.6.0 — 2026-04-19 — scaffold-extension orchestrator shipped + 9 sub-skills

**Action**: `scaffold-extension` shipped as a V1-operational orchestrator with nine single-responsibility sub-skills. Closes the gap between the canonical extension path (manual 4 steps) and automation. `build-agent` now delegates to `scaffold-extension` for simple-extension intents; keeps its generic architecture role for complex multi-skill workflows. All sub-skills typed correctly per `patterns.md § Skill Taxonomy` (eight curators, one producer, one builder).

**New skills — 10 files shipped**
- `scaffold-extension` (orchestrator, sonnet, subagent_safe: false) — runs inline in main session, composes nine sub-skills with operator-visible checkpoints.
- `analyze-extension-intent` (curator, sonnet) — three focused questions to structure the intent.
- `check-existing-encoding` (curator, haiku) — walks five dimensions (core / active-brand sidecars / active-brand custom / sibling-brand custom / shared resources). Returns verdict `route-to-*` | `partial-reuse` | `genuinely-new`. Blocks semantic duplication and routes scaffold to existing encoding when a match is found.
- `propose-schema-draft` (producer, sonnet) — generates canon-compliant JSON Schema draft.
- `validate-nomenclature` (curator, haiku) — reserved names check, kebab-case, MECE.
- `check-cross-refs` (curator, haiku) — verifies cross-refs resolve before scaffold.
- `validate-schema-canon` (curator, haiku) — pre-write canon compliance check, reuses `validate-resources` check 16 logic.
- `scaffold-entity-files` (curator, haiku) — writes schema + README + instance to `brands/{slug}/custom/` or sidecar to `brands/{slug}/{entity}.extensions.json`. Never touches `.skills/`.
- `scaffold-skill-stub` (builder, sonnet) — writes stub SKILL.md to `.skills/skills/custom/` if operator requested a populating skill. Typed builder because it writes into the meta-OS namespace.
- `register-and-flag` (curator, haiku) — registers custom entities in `index.json → extensions[]`, adds adoption todo to brand. Sidecars skip index (convention-discovered).

**Split of scaffold-files — MECE clean**
Previous design had a single `scaffold-files` sub-skill typed `curator` but touching both `brands/{slug}/custom/` (curator scope) and `.skills/skills/custom/` (builder scope). Per audit feedback, split into two sub-skills with precise typing:
- `scaffold-entity-files` — curator, writes to brand workspace only.
- `scaffold-skill-stub` — builder, writes to meta-OS (`.skills/skills/custom/`) only.

Each now has a single write target and a single type. Pipeline aligned with `patterns.md § Skill Taxonomy` rules without override justification.

**Delegation from `build-agent`**
`build-agent/SKILL.md` updated with a new section *"Delegation to `scaffold-extension`"*. Detection rule applied silently in Step 2b: if dissection concludes the intent is a simple-extension pattern (custom entity + optional populating skill, or sidecar), `build-agent` surfaces the routing to the operator and delegates. `build-agent` continues on any residual mission scope after `scaffold-extension` completes. Keeps each orchestrator narrow and composable.

**Doc updates**
- `docs/system/extending.md § Future` → `§ scaffold-extension — orchestrator (shipped V1.5)`. Table updated to list the two split sub-skills. Adoption-gate section replaced with *"How to invoke"* and *"Live execution pattern"* — reflects shipped status.
- `.skills/README.md` catalogue updated with 10 new entries.
- `CHANGELOG.md` entry — this one.

**Canonical reference unchanged**
`brands/_TEMPLATE/custom/_EXAMPLE/competitor_pricing/` remains the reference example. Now produced directly by `scaffold-extension` when the operator says *"scaffold a competitor pricing tracker"*, or cloneable manually for operators who prefer it.

**Still deferred to R&D** (unchanged from v2.5.0)
- Cross-ref runtime rot detection
- Sidecar semantic divergence resolver
- Schema version migration framework
- Hash-based mutation gate bypass detector
- Shared extension registry across workspaces (V2)
- Trigger namespacing for custom skills
- Index-inverted lookup for scale past 5 brands × 3 extensions
- File locking on `index.json` in `write_to_context` (Python infra)
- Empirical token benchmark
- Vertical packs (consulting-core, media-buyer-freelance, coach-expert-pack)
- Multi-operator V1.x

---

## v2.5.0 — 2026-04-19 — Extension layer V1 + parametric composition + craft articulation + cost honesty

**Action**: shipping the extension layer as V1 production-ready. Operators can now encode custom entities, sidecar schemas (including enriching core schemas without forking), custom skills, and external pipelines — all governed by conventions that keep extensions interoperable with the core. Two new canon concepts (*parametric composition*, *craft articulation*) elevated to prism status. Cost honesty installed across docs. Multi-agent red team run on extension layer, fixes applied tier 1 (doc) and tier 2 spec'd (enforcement).

**New — `docs/system/extending.md`**
- Four extension primitives: custom entities, sidecar schemas (with worked example enriching `brand.json` with financial fields), custom skills, external pipeline integrations.
- Three governance rules: declared schema, index registration, README with cross-references.
- Canonical 4-step path for V1 manual usage + copy-paste `_EXAMPLE/competitor_pricing/`.
- **"Registering a custom entity in `index.json`"** — full format with payload shape, `type`, `scope`, `schema`, `cross_refs`, `owner_skill`, `registered_at`.
- **"Writing to custom entities"** — `write_to_context` convention for custom field paths (`custom.{entity_type}.{instance_slug}.{field_name}`), mode direct vs proposed.
- **"Running `validate-resources` on extensions"** — natural language trigger, what it walks, output format.
- Future `scaffold-extension` orchestrator spec'd as 8 curator sub-skills (all typed as `curator` — earlier typings `navigator`/`capturer`/`builder` corrected per patterns.md § Skill Taxonomy).
- **"V1 known limits"** section — honest flags on runtime integrity partial coverage, concurrency as operator-responsibility, mutation gate convention-based, no cross-workspace registry, scale threshold (5 brands × 3 extensions), skill trigger collisions past 20+ custom.
- Adoption gate for orchestrator build: wait for 2-3 real manual extensions before codifying sub-skills.

**New — `brands/_TEMPLATE/custom/_EXAMPLE/competitor_pricing/`**
- Copy-paste-ready custom entity example. Time-series shape for competitor price tracking.
- `schema.json` (canon-compliant: `_version`, `_schema`, `_field_types`, required fields, enum constraints).
- `nike-airmax-97.json` instance with 3 observations.
- `README.md` with cross-ref doc, `write_to_context` example, `index.json` registration example.

**Scaffolded — `.skills/skills/custom/README.md`**
- Operator-built skills namespace with authoring conventions, mutation rules, reading/writing permissions.
- Pointers to `how-to-build-skills.md` and `agent-design-guide.md`.
- Promotion path to vertical packs or core.

**New — Prism 6 — Craft articulation**
- `docs/vision/prisms.md`. Top-3 cross-ecosystem prism from multi-agent fit audit. "The clarification forced by encoding" — forces operator to make tacit reasoning explicit.

**New — Prism 7 — Operational: parametric composition**
- The decomposition → atomic banks → matrix traversal pattern. Explicitly names that PhantomOS ships registries (`angle-registry`, `creative-mechanics-registry`, `proof-registry`, `awareness-angle-matrix`, `hook-formulas`) as a parameter space, not documentation.

**New canon terms — `lexicon.md`**
- `Extension`, `Custom entity`, `Sidecar schema` (with append-only discipline canonized), `Core namespace vs custom namespace` (corrected to match flat filesystem reality, custom as sub-folder), `Promotion threshold` (heuristic flag, not law).
- `Parametric composition` (new cluster anchor for the method).
- `Craft articulation` — now Prism 6 in the snippet library.
- `Agent`, `Sub-agent`, `Orchestrator`, `Workflow` — disambiguated and canonized.

**New — `docs/product/fit.md`**
- Honest ecosystem audit. Best fit, conditional fit, misfit explicited per profile. Built from 5-agent multi-ecosystem analysis. Consultant auto-replacement tension named with 3 mitigations. **Cost honesty section** — 5 structural reasons for token efficiency + where PhantomOS is more expensive + where more efficient + empirical benchmark pending.

**Hero rebalance across docs**
- Centralization + zero re-briefing becomes primary first-day payoff. Compound demoted to secondary. Applied in `README.md`, `docs/vision/prisms.md § Prism 2 (Cognitive — Centralized brand context)`, `.claude/commands/tour.md § Milestone 5`.

**Tour onboarding v2.4**
- State machine, 9 milestones, reflective close generation (not templated), live conversation register detection (renamed from `ia_level`), Batch 2 entry options, single-exit rule, named pivots, progressive anti-stagnation, soft cap global.

**Patched — `CLAUDE.md` (root) mutation rule**
- Rule updated to include extensions: "6 core entities **plus extensions (custom entities + sidecars)**". Post-write on `custom/` or `.extensions.json` auto-triggers `validate-resources` silently on that brand — governance shifted from opt-in to machine-enforced.

**Extended — `validate-resources/SKILL.md`**
- **Check 15** (V1.5) — Custom Entities Filesystem Walk: ensures every `brands/*/custom/*/` has schema + README + index entry, detects orphans.
- **Check 16** (V1.5) — Custom Schema Canon Validation: `_version`, `_schema`, `_field_types` required; sidecar `_extends` points to valid core; sidecar does not redefine core fields (append-only).
- **Check 17** (V1.5) — Reserved Names Collision: blocks `custom/brand`, `custom/product`, etc. at CRITICAL severity.
- **Check 18** (V1.5) — Sidecar Coherence: flags potential semantic divergence on neighbor fields (currency, locale, unit) as INFO, manual review.

**Deferred R&D (flagged in roadmap)**
- `scaffold-extension` orchestrator build — waits for 2-3 manual extensions from real operators before codification.
- Cross-ref runtime rot detection (renamed/deleted core entity still referenced by custom).
- Sidecar semantic divergence automated resolution.
- Schema version migration framework.
- Hash-based mutation gate bypass detector.
- Shared extension registry across workspaces (V2).
- Trigger namespacing for custom skills (past 20+).
- Index-inverted lookup for scale past 5 brands × 3 extensions.
- File locking on `index.json` in `write_to_context` (Python infra layer).
- Empirical token benchmark across 5 operators × 3 months.
- Vertical packs — consulting-core, media-buyer-freelance, coach-expert-pack.
- Multi-operator V1.x — RBAC, client dashboard, licensing layer, simultaneous-session handling.
- Workflow-decomposition methodology (scaffold-extension is the first live test).

---

## v2.4.0 — 2026-04-19 — Tour command + operator awareness tracking

**Action**: onboarding moved from monolithic WELCOME script to a slash-command state machine with milestones, live IA-level detection, and cross-session awareness tracking. Single source of truth for both first-run and replay.

**New — `.claude/commands/tour.md`**
- Executable tour as a slash command. Auto-triggered at first run when no brand is configured; replayable at any time via `/tour`.
- Mode detection from `/operator/awareness.json`: first-run, resume, or replay.
- Nine milestones as a state machine: entry hook, URL-or-description branch, blase, profile type, PhantomOS intro (3 calibrated paragraphs), skill concept planted, wow moment, close with 3 discovery paths + 1 action + implicit skip, optional first-skills offer.
- IA level **detected live from signals, never asked**. Four calibration profiles (novice, basic, comfortable, expert) driving vocabulary, analogy use, density, and presupposition across every milestone.
- Claude generates the actual prose at runtime within milestone substance requirements — no pre-written 4-variant templates. State-machine with flexible transitions rather than rigid decision tree.
- Voice canon 100% enforced: prose first, load-bearing terms, no coach-phrase, no triple-parallel, no em dash in operator replies, no decorative emoji.
- Exit signals (*skip, direct, configure*) bypass remaining milestones and trigger `setup-brand`.

**New — `/operator/awareness.json`**
- Cross-session awareness tracker. Counts sessions, logs concepts introduced, paths explored, first-skill offer attempts, brand validation state.
- Written on each milestone completion via `write_to_context`.
- Read at session start by the agent to calibrate register. Concepts already introduced are never re-defined. Paths already explored are recognized in replay mode.
- Schema versioned (`_version: "1.0"`, `_schema: "operator-awareness"`).
- Loaded on session start only, not on every request — optimized for context budget.

**New — `build-agent` guided-mission mode**
- `build-agent/SKILL.md` extended with invocation modes section. Direct mode (default) remains unchanged.
- **Guided-mission mode** added. Triggered by tour path (d) after setup-brand completes, or by opportune surface in later sessions if `first_skill_built = false` and `first_skill_offered < 3`.
- Walks the operator through decomposing a concrete mission (publish first Meta ad, set up reporting, etc.) into a skill graph with shared primitives. Builds each skill in order, explaining the decomposition logic.
- On completion, writes `first_skill_built = true` to awareness.
- The decomposition methodology is under active development — current mode walks each step explicitly with the operator and captures patterns for later codification in `resources/sops/`.

**Simplified — `WELCOME.md`**
- 280L script collapsed to a thin pointer (~15L). Describes the onboarding concept for contributors browsing the repo; delegates execution to `.claude/commands/tour.md`.
- Prevents duplication between WELCOME.md and the tour command.

**Patched — root `CLAUDE.md § FIRST ACTION`**
- Rule updated: no-brand case now triggers `.claude/commands/tour.md` instead of `WELCOME.md`.
- Added awareness load: `/operator/awareness.json` read on session start regardless of brand state, to calibrate register from prior knowledge.

**Deferred (next R&D project)**
- Workflow-to-skill-graph decomposition methodology. The ability to turn a mission (*"publish a first Meta ad"*) into an ordered list of skills with shared primitives is the core of `build-agent` guided-mission mode, but the generic method does not yet exist. To be built by iteration on 3 concrete test missions, extracting patterns, encoding into a `decompose-mission` skill or a pre-compilation step inside `build-agent` v2.

---

## v2.3.0 — 2026-04-19 — Doc surface restructure + voice canon + prisms + manifesto

**Action**: editorial layer added. Doc surface reorganized by audience (product / vision / system), writing canon formalized, public thesis translated EN and placed, canonical vocabulary written. Skills audited clean under the new canon. No behavioral change to the runtime.

**Post-ship hygiene pass — round 1** (same day, after 5-agent adversarial audit)
- Fixed 6 broken pointers in `docs/system/agent-contracts.md` and `docs/system/architecture.md` left behind by the reference.md split (pointed to dead `reference.md` and renamed `agent-cookbook.md`).
- Harmonized section naming across skills and system docs: `CLAUDE.md § Build before Execute`, `Build→Execute`, `Build before Execute — phase gates` all standardized to canonical `§ Build → Execute gates`.
- Fixed broken ref `CLAUDE.md § Ambient todo` in `setup-brand/SKILL.md` → `§ Build → Execute gates (Gate 4: Ambient todo)`.
- Fixed two self-violations of the voice canon's own anti-patterns: `prisms.md` L33 *"The moat compounds."* rewritten with mechanism; `manifesto.md` L141 *"capture the rent"* rewritten as specific claim about compounding assets.
- Moved `brands/_ARCHIVE/` out of the deployable template into `context-engine/_archive/workspace-template-legacy/` (legacy pilot data was shipping with the template).
- Added `_validation-report.json` to `.gitignore`, removed current artifact.
- `docs/README.md` — added `operator/profile.json` to the Runtime row of the four-types table and to the agent navigation line.

**Post-ship hygiene pass — round 2** (P1 external reader + P2 polish)
- `voice.md` — added fourth anti-pattern **Triple-parallel punchline** ("You talk, the agent writes. You correct..."). Added **Cross-surface rules** section distinguishing docs from runtime agent replies (em dash allowed in docs, banned in replies; emoji policy different).
- `voice.md` example block — removed *"Both versions carry energy"* vibey claim; kept only the mechanism explanation.
- `lexicon.md` — collapsed *"Capture discipline / capture reflex"* duplicate into single **Capture discipline** entry (two synonyms violated the precision test). Removed *"like an identifier in code"* decoration from the opening.
- `README.md` — added **Requirements** section justifying Claude Code dependency (not ChatGPT / Cursor, subscription needed, API inference). Calibrated *"fifteen minutes"* to *"from an empty clone to a first skill run"* with explicit condition.
- `docs/product/getting-started.md` — added **Context levels** table with what the agent can produce at each level and what fills it. Replaced the vague Level 1/2/3 one-liner. Added condition to the fifteen-minute metric.
- `docs/product/capabilities.md` — flagged the *"primitives connected"* list as **"None ships ready-made in V1"** upfront. Removed ambiguity between V1 shipped and V1.1/V2 planned.
- `CLAUDE.md` (root) — added pointer to `docs/system/voice.md` in the Reference section, so editors hit the canon before modifying any doc.
- `build-agent/SKILL.md` — added pointer to `docs/system/cookbook.md` before the generation step, pulling cookbook out of orphan status.
- `resources/README.md` — added **Folders at a glance** table listing all 11 subfolders with content and V1 population status. Closes the desync where `conventions/`, `schemas/`, `scripts/`, `guides/`, `catalogues/`, `frameworks/`, `sops/` were invisible in the index.
- Capitalization sweep — *"Agent Contract"* harmonized per lexicon canon across `README.md`, `docs/README.md`, `prisms.md`, `manifesto.md`.

**Post-ship hygiene pass — round 3** (closing the deferred list)
- `resources/schemas/offers.schema.json` → `offer.schema.json`. Renamed for consistency with the singular-noun convention of the other four schemas (`brand`, `spec`, `profile`, `strategy`). `resources/scripts/validate-all.py` L39 updated; CHANGELOG historical refs left intact.
- `.skills/AGENT-DESIGN-GUIDE.md` → `agent-design-guide.md`. `.skills/HOW-TO-BUILD-SKILLS.md` → `how-to-build-skills.md`. Harmonized with the `lowercase-with-dashes` naming convention of the rest of the doc surface. All refs updated across `CLAUDE.md`, `.skills/README.md`, `build-agent/SKILL.md`.
- `resources/README.md` fully rewritten in English. Body was French, only the top folder table was added in EN in round 2. Now aligned with the voice canon language policy (EN authoring, runtime adapts).
- `docs/product/guides/first-session-example.md` created — textual transcript of what a first PhantomOS session actually looks like, turn by turn (operator inputs and agent replies), through validation and first real deliverable. Partial answer to the external-reader audit's *"no concrete example, no demo"* finding. Screenshots and GIFs remain deferred until the operator produces them.

**Still deferred**
- Visual assets (screenshots, GIF, video tour) in `docs/product/`. Requires operator-produced material.

**Doc surface restructure**
- `docs/` reorganized into three subfolders by audience: `docs/product/` (operator-facing), `docs/vision/` (public narrative), `docs/system/` (contributor-facing). Each gets a `README.md` index.
- Root `docs/README.md` hubs the four doc types (product, vision, system, runtime) and navigates by audience.
- `docs/agent-cookbook.md` renamed → `docs/system/cookbook.md`.
- Runtime docs (`CLAUDE.md` files, `SKILL.md` files, `lexicon.md`) stay outside `docs/` where the harness expects them.

**Voice canon (new source of truth)**
- `docs/system/voice.md` — 8 principles governing every written artifact. Includes load-bearing vs refused terms, anti-patterns (claim without mechanism, coach punchline, unverifiable metric), register baseline (chairman punchy via expert insight), formatting conventions, onboarding posture.
- Language policy locked: all docs authored in EN, runtime adapts per operator language. No bilingual files.
- Name-drop policy: only in `docs/vision/manifesto.md`. Prisms, READMEs, product docs, skills stay name-drop-free.
- Naming discipline: *Name what recurs* — canonize a term only after three occurrences, shorter and more precise than its paraphrase, valid six months out.

**Prisms**
- `docs/vision/prisms.md` — six canonical framings (Economic, Cognitive, Entrepreneurial, Methodological, Strategic, Product) with audience and mechanism per framing. Red-teamed against four adversarial personas. Usable as snippets across the surface.

**Manifesto**
- `docs/vision/manifesto.md` — public thesis translated from FR to EN, voice-canon aligned, 219L. Sourced (HFS, MIT NANDA, Tavel, Karpathy, Lütke, Shipper, Palantir, Atlan, Acemoglu). Extract-ready for external formats.

**Lexicon**
- `lexicon.md` (workspace root) — canonical vocabulary clustered by domain: macro (agent economy, AaaS, Services-as-a-Software, Allocation Economy), method (encoding vs logging, Context Layering, Decision Trace, Skill Graph, Feedback Loop, process moat, capture discipline), workspace (Context DB, brand state), contracts (Agent Contract, Operator, mutation gate, append-only discipline, session continuity, operator-grade), skills (skill, taxonomy, model routing), governance (extractibility test, agnostic by test).
- Voice.md § Terminology canon now delegates definitions to `lexicon.md` rather than duplicating.

**Reference split**
- `docs/system/reference.md` (586L monolith) split into three domain-focused files:
  - `docs/system/architecture.md` (240L) — entities, field types, dependency graph, session relay, context budget, connectivity pattern, rules.
  - `docs/system/agent-contracts.md` (97L) — full `CLAUDE.md` specification: types (root, brand, template), loading mechanism, precedence model, write discipline, lifecycle, size policy.
  - `docs/system/patterns.md` (259L) — close variants, sharpening examples, context levels, model routing, skill taxonomy, skill philosophy.
- All cross-references updated across 15+ files (root `CLAUDE.md`, brand `_TEMPLATE/CLAUDE.md`, skills, READMEs) to point to the new granular sections.

**Rewrites (voice canon passes)**
- `README.md` (workspace root) — tightened to 36L, Prism 6 opening, earned strong terms (*runtime*, *operates*, *mutation gate*, *compound*). Audience navigation in closing.
- `docs/product/getting-started.md` — 201L → 74L (−63%). File structure tree moved to system reference; glossary moved to lexicon; FAQ reduced to five essentials.
- `docs/product/capabilities.md` — tightened, voice canon aligned, *context receptacle* wording replaced with plain reference, tone unified.
- `docs/vision/roadmap.md` — 223L → 171L. Shipped section killed and replaced with pointer to `CHANGELOG.md`. Roadmap is now Planned-only.

**Micro-fixes**
- `WELCOME.md` L121 — *"I am not your assistant who executes. I am the one who orchestrates"* → *"I am not your assistant who executes. I orchestrate."* Native English phrasing.
- `.skills/skills/red-team/SKILL.md` L248 — *"More powerful than a risk list"* → *"More revealing than a risk list"*. *Powerful* is a refused term per canon; *revealing* names the mechanism.

**Skills audit (18 skills, body pass)**
- Adversarial grep across all skill bodies against four violation classes: growth-coach terms, filler phrases, decorative emojis outside the one-off exception, name-drops.
- One violation fixed (red-team above). Zero other issues. Skill bodies already aligned with dense prompting conventions and voice canon — the canon codifies the pattern that was already in use.
- Frontmatter descriptions audited: all 18 follow verb + mechanism + trigger list structure. No rewrites required.

**Audited clean (no rewrite)**
- Root `CLAUDE.md` — runtime contract already aligned with dense prompting.
- `brands/_TEMPLATE/CLAUDE.md` — tight runtime template.
- `docs/system/cookbook.md` — technical system doc, code-heavy and appropriate.
- All 18 `SKILL.md` files.

**Flow discipline**
- Master-mirror flow inverted: `largo-kb/05-projects/context-engine/workspace-template/` is now the canonical source; `phantomos-alpha-test/` is the sync target (test deployment).
- Both copies remain bit-identical at session close.

**Files created or renamed**
- Created: `lexicon.md`, `docs/README.md`, `docs/product/README.md`, `docs/vision/README.md`, `docs/system/README.md`, `docs/system/voice.md`, `docs/system/agent-contracts.md`, `docs/system/patterns.md`, `docs/system/architecture.md`, `docs/vision/prisms.md`, `docs/vision/manifesto.md`, `docs/product/guides/` (empty, ready).
- Renamed: `docs/agent-cookbook.md` → `docs/system/cookbook.md`.
- Removed (content split): `docs/system/reference.md`.

---

## v2.2.0 — 2026-04-19 — Skill Taxonomy + Philosophy + Navigators

**Action**: structural layer added on top of v2.1.0. Six-typology skill taxonomy enforced, expert methodology discipline formalized, first Navigators shipped, build-agent rebuilt with silent dissection and operator-facing cartography.

**Skill Taxonomy (strict enforcement)**
- Six typologies formalized in `docs/system/reference.md § Skill Taxonomy`: `producer | curator | capturer | orchestrator | navigator | builder`. Each has a binary inclusion test and default technical contract (model, subagent_safe, write mode).
- Primary disambiguation Curator vs Navigator by **who invokes the skill** (other skill in pipeline = Curator ; operator direct = Navigator), not by output destination.
- All 17 skills tagged with `type:` in frontmatter retroactively.
- `validate-resources` gains check **13b — Skill Typology Enforcement**: blocking error if `type:` missing or invalid.
- `build-agent` gains **Step 4b — Determine skill typology**: mandatory before any SKILL.md generation.

**Skill Philosophy (codified expertise)**
- New section in `docs/system/reference.md § Skill Philosophy`: *"every skill embodies codified expertise, not improvised action"*. A skill incarnates a senior domain expert's framework, variables, matrix, thresholds, formulas.
- **Complexity gate** added: discipline applies to complex tasks only (framework applicable, business decisions, thresholds matter). Simple tasks (lookup, filter, rename) stay léger. Avoids over-engineering.
- Gate doc extended: if expert methodology missing from `resources/frameworks|catalogues|quality-specs|sops|conventions/` for a complex task, **STOP** generation, build the methodology artifact first.

**Navigators (category shipped empirically)**
- `daily-brief` — session-start orientation: portfolio health, pending validations, flags, suggested next actions. Haiku, subagent_safe. Zero deliverable, pure orientation.
- `resume-session` — clean resumption after absence: reconstructs last active thread from `session-state.md` + `pending-validations.md`, posture adaptive to register of previous session.
- Navigators category proven with 2 concrete skills instead of staying theoretical.

**Red-team skill adapted for PhantomOS**
- New `red-team` skill (Orchestrator): multi-expert adversarial panel (5-6 experts with business role × cognitive prism), Phase 0 scoping + Phase 0.5 implicit assumptions + Phase 1 solo analysis + Phase 2 cross-talk + Phase 3 Chairman verdict.
- PhantomOS-specific adaptations: frontmatter typed, Language policy EN + runtime translation, `AskUserQuestion` for Phase 0 scoping and mode + amplifier choice, archive output to `brands/{slug}/audits/YYYY-MM-DD-redteam-{subject}.md`, auto-trigger `capture-learning` on findings with confidence ≥ 8, append critical verdict items to `pending-validations.md`.
- Emoji policy: 🔴🟠🟡🔗⚡➕💡 kept as functional severity/reaction signals (per one-off tech state rule), not decorative.

**build-agent v2 (dissection + cartography + typology)**
- New **Step 2b**: complexity gate binary test first (simple vs complex), silent dissection of 10 dimensions (intent, usage context, data in/out, infrastructure deps, **expert methodology**, technical constraints, failure modes, evolution, overlap, ecosystem impact), operator cartography 4 lines max, `AskUserQuestion` with 4 actionable options.
- New **Step 3b**: three binary tests (Split → orchestrator? / Doc prerequisite? / Typology assignment?).
- New **Step 4b**: typology confirmation with operator before SKILL.md generation.
- Push-back obligation: if deep intent ≠ surface intent, skill must challenge before building.

**Orchestrator `onboard-brand-full`**
- First concrete Orchestrator demonstrating the pattern "one operator intent, pipeline delegation across N named skills".
- Chains 5 phases: `setup-brand` (inline) → `snapshot` (Task tool subagent) → `ingest-resource` (subagent, optional) → `validate-resources` (subagent) → Build chantiers close (inline, per operator profile).
- Proves the model routing + subagent_safe contract in a real orchestration case.

**Tickets for long deliverables**
- New convention: any skill with execution > 10 min, multi-session span, 2+ sub-skills orchestrated, or client-facing deliverable **MUST** open a ticket in `brands/{slug}/tickets/{YYYY-MM-DD}-{HHMM}-{slug}.md`.
- Format standardized in `brands/_TEMPLATE/tickets/README.md`: intent, plan, current state, log (append-only), cost estimate, blockers, output link.
- Operator interaction: `"where is ticket X" / "pause" / "resume" / "close"`.

**Operator contract hardened**
- New DO/NEVER rule: translate PhantomOS internal vocabulary to operator value. **NEVER** expose `convention`, `framework`, `SOP`, `quality-spec`, `catalogue`, `entity`, `field`, `schema` in architectural cartography to the operator. Say what it does for them.
- Applied throughout build-agent, red-team, and learn-from-session output.

**Decision Trace MANDATORY**
- `capture-learning` and `learn-from-session` now require non-empty `reasoning` field on every `learnings.json` entry. `fact` = WHAT, `reasoning` = WHY. Without the why, the learning is logged data, not codified knowledge.
- Push-back obligation on flush recap if operator cannot articulate the why.

**AskUserQuestion preferred over markdown a/b/c/d**
- Rule added in `CLAUDE.md § Smart suggests`: prefer native clickable tool, fallback to markdown only when tool unavailable. Same rules apply to both (4 options, (d) mandatory, diversification, 6-15 words).

**CLAUDE.md state**: 166 lines / ~18 KB (budget ≤220 lines / ≤20 KB). Magic keywords `CRITICAL / YOU MUST / NEVER / ALWAYS / MANDATORY` applied on load-bearing rules. Skills table extended with Subagent column, 17 skills listed.

**Updated**: CLAUDE.md, docs/system/reference.md, CHANGELOG.md, capture-learning/SKILL.md, learn-from-session/SKILL.md, build-agent/SKILL.md, audit-setup-meta/SKILL.md (rebuilt with Step 0 gate access + API mode + declarative fallback + taxonomy tagging), validate-resources/SKILL.md (check 13b), `.skills/skills/_TEMPLATE/SKILL.md` (type field added), all 17 skills tagged with `type:`, new `.skills/skills/daily-brief/`, new `.skills/skills/resume-session/`, new `.skills/skills/red-team/`, new `.skills/skills/onboard-brand-full/`, new `brands/_TEMPLATE/tickets/README.md`.

---

## v2.1.0 — 2026-04-18 — UX + hygiène

**Action** : passe UX majeure après audit multi-agent (5 personas + copy + nomenclature + cohérence). Alignement ton, règles cascadées, phase gates explicites.

**Onboarding**
- Switch mode 4 niveaux (novice / basic / comfortable / expert) en tout premier message. Adapte la pédagogie et la longueur du narratif.
- Narratif court (~120 mots) pour mode 3. Narratif standard (280 mots) réservé aux modes 1 et 2. Mode 4 skip tout.
- Ajout profil `dropshipper` au menu des 6 profils opérateur.

**Posture agent**
- Chairman qui orchestre, pas assistant qui exécute. 5 règles de raisonnement (scan 3 axes, tactique vs stratégique, env-aware, autorité humble, challenge).
- Smart suggests permanents `a/b/c/d` en daily-use (d obligatoire), format 6-15 mots, diversification obligatoire. Override 1-2 suggestions en onboarding guidé.
- Règle anti-tiret cadratin (`—` banni dans les réponses opérateur). Règle anti-emoji décoratif. Pass purge sur 11 fichiers (~29 emojis, ~43 termes jargon, ~81 tirets).

**Build avant Execute — 5 mécaniques**
1. Gate access check (token présent sinon accompagnement setup).
2. Gate contexte (inféré non validé = flag avant exploitation).
3. Todo ambiant (`brands/{slug}/pending-validations.md` comme buffer).
4. Détection skill-candidate (tâches récurrentes formalisées avant run).
5. Bascule Build → Execute (4 étapes : access, contexte, convention, confirm).
- Close post-scrape éclaté en 4 variants (solo-brand-live / early-founder / creator / agency-portfolio).

**Connectivité & conventions**
- Gate doc obligatoire avant tout setup de plateforme : l'agent lit la doc officielle (rate limits, scopes, pièges) et remplit `resources/conventions/{platform}.json` AVANT de toucher à un token.
- Ajout champs `rate_limits.*`, `access.oauth_scopes_required`, `access.app_review_required`, bloc `_doc_check` dans le template convention.

**Schema operator/profile.json**
- Nouveaux champs : `identity.profile` (enum 6 valeurs), `preferences.ia_level`, `preferences.os_tips_shown`, `preferences.tracking`.
- Renommage `anti_patterns_perso` → `anti_patterns`.

**Refactor structurel**
- Racine nettoyée : 4 fichiers conventions (README, CLAUDE, WELCOME, CHANGELOG) + Makefile + index.json.
- Nouveau sous-dossier `docs/` contenant reference.md (ex-ARCHITECTURE), roadmap.md, capabilities.md (ex-coverage), getting-started.md, agent-cookbook.md.
- README.md par sous-dossier pour `brands/` et `.skills/`.

**Taxonomie & nomenclature**
- Renommage `_field_types` : `raw` → `observed`, `declared` → `stated` (clarté sémantique sur la provenance des données). Appliqué dans `_TEMPLATE`, `_EXAMPLE`, `resources/schemas/`, `resources/conventions/`. Archives conservées avec l'ancien schema.
- Canonisation du terme "audience" (remplace "persona" et "clients types" dans le flow opérateur).

**Size Policy CLAUDE.md**
- Budget déclaré : root ≤ 20KB / 220 lignes, brand ≤ 8KB / 100 lignes.
- Check minimaliste dans `learn-from-session` (Trigger 6) : mesure de la taille à chaque flush batch, flag dans le récap si dépassement. Pas d'auto-split.
- Garde-fou pré-écriture : test d'addition cascadé (root / brand / skill / reference / welcome / convention).

**Skills**
- `setup-brand` Step 0 async via URL (défaut si URL disponible) avec lancement de `snapshot` en parallèle.
- Nouveau Step 5 (tour du workspace après demo-value). Steps intermédiaires 5-8 obsolètes supprimés.
- Routing explicite `capture-learning` (ponctuel) vs `learn-from-session` (batch).
- Triggers skills doublés FR/EN dans la table.

**Updated** : CLAUDE.md, WELCOME.md, README.md, setup-brand, learn-from-session, ingest-resource, build-agent, snapshot, validate-resources, brand templates, operator/profile.json, resources/conventions/_TEMPLATE.json, resources/schemas/spec.schema.json, docs/system/reference.md, docs/product/capabilities.md (renamed from coverage.md).

---

## v2.0.0 — 2026-04-18 — DEPLOYABLE

**Action**: PhantomOS V1.0 DEPLOYABLE — enforcement layer + first production skill + strategy enrichment
**Decisions**: D#304-313
**Smoke test**: 12/12 PASS

### Enforcement layer (D#307-312)
- **write_to_context()** enrichi : blacklist champs structurels (`_version`, `meta.slug`, `_schema`, `_field_types`, `_proposals`), 8/8 tests PASS
- **Permissions frontmatter** : 14 SKILL.md avec bloc `permissions: {reads, writes, mode}`. Source unique de vérité, discovery automatique. `.context-agents.yaml` → cache.
- **Agent_id calculé** : `{skill-name}@{version}`, jamais déclaré par le skill. Empêche le spoofing.
- **Auto-accept** : `config.json → proposal_review.auto_accept` (seuil configurable, default 0.8). Proposals basse confiance surfacées dans la conversation.
- **Proposals conversationnelles** : Session Relay Protocol enrichi. CLI review tué. Diff en français, jamais le mot "proposal".

### Production skill
- **audit-setup-meta v1.0** : 22 points, 5 blocs (Pixel, Structure compte, Campagnes, Catalogue, Règles). Mode déclaratif V1. Scoring maturité 1-5. Premier skill de production du template.

### Strategy enrichment
- **strategy.json v1.1** : pacing (budget tracking), variance_thresholds (alertes KPI), target_decomposition (annuel → daily). Template + Example (Lumya). Schema créé.

### Onboarding
- **Step 4 adaptatif** : détection profil opérateur → Meta Ads = audit-setup-meta, autre = brief stratégique express, pas de plateforme = fallback.

### Documentation
- **README** : Limitations V1 (6 points) + Modèle de menace V1 (single operator, local, trusted)

---

## v1.14.0 — 2026-04-10

**Action**: BRAND SCHEMA v2.1 — purchase_driver + audience_trees[] + driver_blend
**Files**: `resources/schemas/brand.schema.json` | `brands/stepprs/brand.json` | `brands/_TEMPLATE/brand.json` | `brands/_EXAMPLE/brand.json` | `brands/stepprs/products/*/offers.json` (11)
**Decisions**: D#243, D#244, D#246, D#248, D#249, D#250, D#251

S30d-close — Profile audience v2.1 foundations promoted to the brand schema:

- **`purchase_driver`** (enum: pain | desire | status | utility | identity | mixed) — brand-level default cascading to all audiences. Optional, backward-compat.
- **`audience_trees[]`** — optional primitive for two-sided marketplaces (supply × demand) where a single brand owns multiple distinct audience trees.
- **`driver_blend`** (object: primary | secondary | ratio) — required when `purchase_driver = "mixed"`, e.g. stepprs-padel (pain 60 + identity 40).

Live brand.json files bumped 1.5 → 2.1 with changelog entries. `_TEMPLATE` leaves `purchase_driver` absent (optional; users fill per brand). `_EXAMPLE` sets `purchase_driver: "pain"` for consistency with creme-eclat.

**Offers fix (R1 overnight audit)**: 11 stepprs offers.json were missing required `active` field. Auto-added `"active": true` per offer. All 13/13 offers now PASS. Fresh run of `resources/scripts/validate-all.py` reports CRITICAL/HIGH/MED/LOW = 0.

**Profile schema v2.1** reste en research/ tant que calibration empirique (D#247) pas faite. Brand-level primitives promues comme delta minimum non-bloquant.

---

## v1.13.0 — 2026-04-09

**Action**: SCHEMAS v1.8 — Batch 5 stress test gap closure (9 brands, full HIGH+MED+LOW)
**Files**: `brands/_TEMPLATE/products/_example/offers.json` | `brands/_TEMPLATE/products/_example/spec.json` | `resources/schemas/offers.schema.json` | `resources/schemas/spec.schema.json`
**Decisions**: D#165 → D#180

Batch 5 red-team stress test on 9 live DTC pilot brands (anonymized — covering skincare-subscription, outdoor apparel, porridge/granola, supplements, chicory beverage, clean beauty, haircare, sport nutrition, natural cosmetics) revealed 16 schema gaps across compliance, enrichment, and cross-category coverage. All closed in v1.8. Backward compatible — every new field optional.

**Design directive**: universal schemas, no category-level carve-outs. Outdoor apparel pilot and haircare pilot must fit v1.8 via existing/new optional fields, not vertical discriminators. Chicory pilot correctly identified as chicory food/beverage (not pet food).

### Spec v1.8 — HIGH (compliance-critical)

- **`specs.posology{recommended_daily_servings, serving_unit, timing, duration_recommended, max_daily_dose, notes}`** — EU/EFSA compliance for supplements, ingestibles, actives. `serving_unit` free string (gelule, capsule, scoop, ml, g, sachet, application, wash). Drives cure-based marketing and dosage disclosures. Null for non-regulated products.
- **`specs.contraindications{conditions[], medications[], age_min, age_max, pregnancy, breastfeeding, warnings[]}`** — regulated products (supplements, drugs, actives). `pregnancy` and `breastfeeding` enum: `safe|avoid|consult_doctor|contraindicated`. Powers safety disclosures, chatbot guardrails, ad-copy review. Supplement pilot driver.
- **`specs.nutrition_facts.allergens`** — added `oats` (14 EU + oats = 15 enum values). Captures porridge/granola pilots where oats is key allergen outside EU14.
- **`specs.nutrition_facts.allergen_sources[]`** — free-text secondary allergen sources (lanolin, gelatin, bee products, latex) not covered by enum. For cosmetics/supplements with derived ingredients.
- **`specs.nutrition_facts.nutri_score_grade`** — enum A-E. FR 2025+ regulatory for food marketing claims.
- **`specs.nutrition_facts.dietary_tags`** — extended enum: +`caffeine_free`, `bio`, `raw`, `chicory_based`, `clean_beauty`, `cruelty_free`. Covers chicory pilot (chicory_based), clean beauty pilot, food pilots (caffeine_free, bio, raw).
- **`specs.perishability.period_after_opening_months`** — EU Cosmetics Regulation PAO. Mandatory for cosmetics with shelf life >30 months. Haircare, natural cosmetics, clean beauty pilots driver.
- **`specs.perishability.expiry_date_required`** — boolean for DLC/EXP regulatory mandate.

### Spec v1.8 — MED (enrichment)

- **`specs.origin{country, region, facility, local_supply_pct, made_in_claim, supply_chain_transparency}`** — replaces free-text Made-In claims. `supply_chain_transparency: full|partial|opaque`. Powers Made-In filters and supply-chain storytelling. Natural cosmetics, sport nutrition, haircare pilots driver.
- **`specs.production_method{type, batch_size, frequency, method_notes}`** — `type` enum: `industrial|small_batch|artisanal|limited_batch|handmade|made_to_order`. Distinguishes mass production from craft. Clean beauty, haircare, chicory pilots driver.
- **`specs.preparation{cooking_required, method, time_minutes, temperature, serving_suggestions[]}`** — food requiring prep. `method`: infuse, blend, boil, microwave, add_water. Porridge, chicory (infusion) pilots driver.
- **`specs.external_databases{open_food_facts_id, yuka_id, inci_beauty_id, ciqual_id, ean, gtin}`** — cross-refs to third-party DBs. `additionalProperties` allowed for future integrations. Enables automated Yuka/INCI Beauty rating fetch.
- **`specs.target_suitability{skin_types[], hair_types[], body_areas[], use_cases[], demographics[]}`** — UNIVERSAL 'who is this for' container. `skin_types` enum (9 values), `hair_types` enum (12 values), body_areas/use_cases/demographics free-text. Replaces ad-hoc targeting fields. Works for ALL categories: cosmetics (hair_types), skincare (skin_types), apparel (body_areas + use_cases), supplements (demographics).
- **`specs.durability{warranty_years, warranty_type, repairable, spare_parts_available, repair_program, lifespan_estimate, repairability_index}`** — for durable goods. `warranty_type` enum: `limited|lifetime|conditional|commercial`. `repairability_index` = FR 2021+ electronics 0-10. Outdoor apparel pilot, circular-economy positioning.

### Spec v1.8 — LOW (structural refinements)

- **`specs.composition[]`** — now accepts structured objects `{ingredient, pct, organic_certified, class, origin, inci}` OR legacy strings (mix allowed). `class` enum: active|filler|preservative|fragrance|colorant|emulsifier|binder|other. `inci` for cosmetics. Powers ingredient transparency displays.

### Offers v1.8

- **`pricing.price_per_unit.unit`** — ENUM-LOCKED (was free string). Values: `serving|dose|day|week|month|100g|100ml|kg|liter|gelule|capsule|tablet|scoop|sachet|wash|use|application|ml|g|unit|meal|piece`. Cross-offer comparability requires canonical set. Adding new unit = schema update.
- **`contents.duration_type`** — enum `calendar|usage_days|servings`. Disambiguates "3-month cure" (calendar vs servings). Critical for supplements where 90 capsules could span 45-90 days depending on posology.
- **`contents.duration_servings`** — absolute serving count when `duration_type=servings`. Enables exact price_per_unit when calendar duration is ambiguous.
- **`contents.cure_metadata{cure_name, is_premade, target_concern, phases[]}`** — named assembled cures. `is_premade` = brand-curated vs user-assembled. `phases[]` for sequential cures (clean beauty 3-phase detox/rebuild/maintain). Skincare subscription pilot HB+CB, sport nutrition stacks.
- **`incentives.duration_tiers[{duration_months, discount_type, discount_value}]`** — discounts scaling with COMMITMENT LENGTH (not quantity). Ex: 1mo=0%, 3mo=10%, 6mo=15%. Distinct from `bulk_tiers` (quantity) and `subscription.intro_discount` (first-N-orders). Skincare subscription pilot cure pricing.
- **`incentives.loyalty{enabled, points_earning_rate, redemption_rule, tiers[], sign_up_bonus}`** — fidélité program. `tiers[{name, threshold, benefits[]}]` for VIP structures. Distinct from referral (bidirectional) and gifts.unlock_after_orders (milestone). Sport nutrition, natural cosmetics, haircare pilots driver.
- **`offers[].tags[]`** — free-text operator-defined routing/filtering tags. Ex: `cure_3_mois`, `starter_pack`, `seasonal_winter`, `influencer_box`, `vip_only`. Distinct from `type` (structural). Agents filter catalogs without parsing names.

### Rationale & Design Notes

- **Universal over vertical**: initial batch 5 synthesis proposed category-level discriminators (pet food enum, fashion vertical). Rejected. v1.8 uses universal optional fields that any brand can populate selectively. `target_suitability` is the canonical example — same container handles haircare, skincare, apparel, supplements.
- **Chicory pilot correction**: pet food analysis discarded. Pilot is chicory (food/beverage). `chicory_based` dietary tag added. Standard `nutrition_facts` + `preparation` + `origin` cover the vertical.
- **Compliance surface**: posology + contraindications + nutri_score + PAO + origin + allergen enum expansion = EU-ready baseline. Covers EFSA, Cosmetics Regulation, Nutri-Score 2025, EU14 allergen labeling.
- **No breaking changes**: all v1.8 fields optional or extend existing enums. Only `price_per_unit.unit` moves from free string to enum — but `anyOf` at the property level keeps v1.7 string form acceptable.

---

## v1.12.0 — 2026-04-09

**Action**: SCHEMAS v1.7 — Batch 4 stress test gap closure (offers + spec)
**Files**: `brands/_TEMPLATE/products/_example/offers.json` | `brands/_TEMPLATE/products/_example/spec.json` | `resources/schemas/offers.schema.json` | `resources/schemas/spec.schema.json`
**Decisions**: D#144 → D#152

Batch 4 red-team stress test (Typology, 900care, Asphalte, Kusmi Tea, Jimmy Joy) revealed 9 schema gaps across offers and spec. All closed in v1.7. Backward compatible — every new field is optional except the `product_refs` / `product_ids` `anyOf` constraint which accepts either.

### Offers v1.7

- **`product_refs[{slug, quantity}]`** — canonical multi-product link with per-product quantity. Replaces `product_ids[]` (kept as deprecated alias for v1.6 workspaces). Unblocks multi-quantity bundles (Kusmi pack = 2× detox + 1× green) which were impossible to model cleanly. Schema uses `anyOf` to accept either field during migration window.
- **`contents.prepay_type`** — discriminator (`supply` | `production`) when `is_prepay=true`. `supply` = pre-stocked, shipped immediately for X months of usage (Seed 3-month, Jimmy Joy bulk). `production` = manufactured after payment, delivery deferred (Asphalte pre-order). Impacts cashflow modeling and ad copy.
- **`contents.fulfillment_delay{min_days, max_days, reason}`** — pre-order, crowdfunding, made-to-order, seasonal batch, or out-of-stock restock. Null = standard 1-3 day fulfillment. Asphalte-killer: was previously buried in `fulfillment_notes` free text, unqueryable.
- **`pricing.price_per_unit`** refactored from free string to structured `{value, currency, unit}`. `unit` is lowercase_snake_case (`serving`, `day`, `100g`, `100ml`, `dose`, `use`, `wash`). Enables sort/compare across offers. String form still accepted for backward compat — validators coerce on read.
- **`subscription.churn_metrics{measured_churn_pct, avg_lifetime_orders, source, captured_at}`** — placeholder for measured retention (analytics, Recharge, Shopify, declared, estimated). Factual observation only, not a forecast. Null until measured. Used by perf agents to sanity-check LTV assumptions.
- **`incentives.variant_pricing_delta[]`** — per-variant premium/discount on the same offer (flavor upsell, size premium). Array of `{variant, delta, delta_type: fixed_amount|percentage}`. Jimmy Joy Choco Premium pattern. Empty array = flat pricing.
- **`gifting.recipient_email`** — boolean. True = digital gift delivery (code, gift card, download link) to recipient email. Distinct from `recipient_shipping` (physical). May combine for hybrid (physical item + email notification).

### Spec v1.7

- **`specs.nutrition_facts{serving_size, calories, macros, micros[], allergens[], dietary_tags[]}`** — for ingestible products (food, beverages, meal replacements, supplements). Enum-locked `allergens` (14 EU regulatory allergens) and `dietary_tags` (11 common certifications). Unblocks compliance checks (allergen disclosure) + dietary filtering in product discovery. Null if not ingestible.
- **`identity.co_creation{enabled, mechanism, community_size, input_collected[], iteration_cycle}`** — community-driven design BEFORE production. Distinct from `customizable` (individual buyer). Asphalte pattern: community votes on fabric/fit/color before each production run. Mechanisms: `vote | survey | iterative_feedback | crowdfunding`. Impacts messaging (belonging, insider status) and pre-order fulfillment logic.

### Breaking? No.

- `product_refs` + `product_ids` anyOf = either works. Skills should write `product_refs` going forward and mirror into `product_ids` during the migration window.
- All other additions are optional fields defaulting to `null` / `[]`.
- Existing v1.6 workspaces validate unchanged.

---

## v1.11.0 — 2026-04-04

**Action**: NEW SKILL — `snapshot` v1.0.0
**File**: `.skills/skills/snapshot/SKILL.md`

Skill d'onboarding produit depuis URL. Remplit spec.json + offers.json + bases profile.json en un run.

**Flow :** Pre-flight (brand existe ?) → URL validation → détection plateforme → scraping (Shopify JSON API first) → confidence scoring → spec.json → offers.json → 4 questions audience fermées → profile.json surface → output avec score + next steps.

**Décisions de design (issues UX stress test 6 agents) :**
- Shopify JSON `/products/{handle}.js` en priorité sur HTML scraping
- Confidence score (< 40% = bloquant, 40-70% = warning, ≥ 70% = OK)
- 4 questions audience fermées avec relance si réponse trop vague → null si toujours flou (zéro hallucination)
- `_snapshot` block de traçabilité dans spec.json + profile.json (source, confidence, missing fields)
- Typage automatique des offres depuis variant titles (prepay/bundle/single/subscription)
- `is_prepay` auto-calculé
- Routing setup-brand si brand.json absent
- Un produit par run (multi-produit = V2 orchestration)

**Scope intentionnellement exclu :** VoC/VoM, objections, pain chains, concurrents → ingest-resource.

---

## v1.10.0 — 2026-04-04

**Action**: OFFERS SCHEMA v1.5 — `contents.is_prepay`
**Files**: `brands/_TEMPLATE/products/_example/offers.json` | `Ressources/schemas/offers.schema.json`
**Decision**: D#143

**Ajout :** `contents.is_prepay: boolean | null`

Gap identifié sur un pilote skincare-subscription (audit réel) : bundle multi-produit + multi-mois (`type: "bundle"` + `contents.duration`) est sémantiquement un prepay mais n'est pas queryable comme tel — un agent filtrant `type == "prepay"` manque les bundles prépayés. `is_prepay: true` unifie les deux patterns pour la queryabilité. `type: "prepay"` reste pour single-product prepay, `type: "bundle"` reste pour multi-produit — `is_prepay` est le flag transversal.

---

## v1.9.0 — 2026-04-04

**Action**: OFFERS SCHEMA v1.4 — Patch Batch 2 P1 gaps
**Files**: `brands/_TEMPLATE/products/_example/offers.json` | `Ressources/schemas/offers.schema.json` | `brands/_EXAMPLE/products/creme-eclat/offers.json`
**Decision**: D#142

**Ajouts :**
- `subscription.reschedule: boolean` — déplacer la date de prochaine livraison sans annuler. Distinct de `skip` (suppression) et `pause` (gel). Source: Billie, Flamingo.
- `subscription.required: boolean|null` — true si subscription = seule option d'achat, false si one-shot disponible en parallèle. Null si non précisé. Source: Flamingo.

**_EXAMPLE Lumya OFR-03 mis à jour :** `reschedule: true`, `required: false` (Crème Éclat vendue aussi à l'unité OFR-01).

---

## v1.8.0 — 2026-04-04

**Action**: OFFERS SCHEMA — Validation Batch 2 (10 nouvelles verticales, 20 marques)
**Summary**: Stress-test v1.3 sur verticales non couvertes par Batch 1. Schema validé production-ready pour DTC standard (~70% des cas). 2 nouveaux gaps P1 identifiés. 4 gaps architecturaux V2 confirmés/renforcés. Décision D#141.

**Verdict couverture v1.3 :**
- ✅ Production-ready : Native, Lume, Hydrant (preset), Mejuri (gifting), Thrive trial auto-conversion
- ⚠️ Workaround acceptable : Billie/Flamingo (reschedule ≠ skip), Hydrant custom qty_per_variant, Skims (cohort_tiers), Nespresso (dual offer sans dependency link)
- ❌ V2 architectural : Oura/Whoop (hardware+sub), Prose/Curology (personalization), HelloFresh (intro cascade 3 paliers), Thrive/ClassPass (membership access-based)

**Nouveaux gaps P1 (v1.4 candidats) :**
- `subscription.reschedule: boolean` — déplacer la livraison vs l'annuler (Billie, Flamingo)
- `subscription.required: boolean` — subscription = seule option vs option parmi d'autres (Flamingo)

**Gaps V2 documentés (renforcés) :**
- `type: "membership"` — Thrive + ClassPass confirment Batch 1 (Typology, Fabletics). Poids critique.
- Hardware + subscription dual pricing model — Oura ($299 device + $5.99/mo mandatory), Whoop ($0 device inclus dans membership). Architecturalement incompatible sans refactor cross-schéma.
- `contents.personalization{}` — Prose/Curology : product_ids[] incompatible avec formules générées dynamiquement.
- `subscription.intro_phases[]` — HelloFresh cascade 60%→40%→20% sur 3 commandes distinctes. `intro_discount` single-value insuffisant.
- `offer.requires_offer_id` — dépendance starter kit → refill (Billie/Nespresso). Couche V2.

**Research** : `context-engine/research/offers-schema-mapping-batch2.md` (13 patterns, 10 verticales)

---

## v1.7.0 — 2026-04-04

**Action**: OFFERS SCHEMA v1.3 — Patch P1+P2 gaps (mapping complet 22 patterns réels)
**Summary**: Suite au mapping offre-par-offre contre le schema v1.2, 7 gaps P1/P2 patchés. Tous optionnels, rétrocompatibles.

**Changements offers.json (v1.2 → v1.3)**:
- `type` enum : ajout `"prepay"` — même produit, durée prépayée avec remise volume (distinct de bundle multi-produit)
- `contents.variant_selection.selection_rules` : `{min_items, max_items, eligible_skus[], cross_category}` pour variety packs customisables
- `subscription.trial.converts_to_offer_id` : pointeur vers l'offre post-trial (auto-conversion Bobbie)
- `subscription.shipping` : `{free: bool, threshold: number|null}` — free shipping comme bénéfice abonnement
- `subscription.intro_discount.then_price` : prix absolu post-intro (Hims $69 → $199)
- `incentives.gifts[].first_order_only` : boolean — welcome kit 1re commande uniquement
- `incentives.gifts[].unlock_after_orders` : loyalty milestone — cadeau débloqué après N commandes
- `urgency.early_access` : `{enabled, cohort, channels[], lead_days}` — early access VIP pour limited drops
- `payment_options.installments[].min_order_value` : BNPL conditionnel (Savage X Afterpay $30+)

**_EXAMPLE mis à jour** : OFR-04 ajouté (type prepay — Cure 6 mois Lumya). OFR-01 démontre `first_order_only`. OFR-03 démontre `unlock_after_orders`, `shipping.free`, `converts_to_offer_id`.

**Gaps V2 documentés (non implémentés)** : credit-based membership, skip_window, supply guarantee, type:membership
**Research mapping** : `context-engine/research/offers-schema-mapping.md` (22 patterns, 3 statuts)

---

## v1.6.0 — 2026-04-04

**Action**: OFFERS SCHEMA v1.2 — Market validation (23 marques DTC réelles, 10 agents)
**Summary**: 4 gaps mécaniques quasi-universels identifiés et patchés. Ajouts rétrocompatibles (champs optionnels). Décision D#139.

**Changements offers.json (v1.1 → v1.2)**:
- `subscription.skip` (bool) : client peut sauter une livraison sans résilier
- `subscription.pause` (bool) : client peut mettre l'abonnement en pause
- `subscription.frequency_options` (number[]) : fréquences proposées en jours (ex: [30, 60, 90])
- `subscription.intro_discount` (object|null) : réduction première(s) commande(s) — {type, value, applies_to_orders}
- `subscription.recurring_discount` (object|null) : réduction récurrente post-intro — {type, value}
- `contents.variant_selection` (object|null) : composition flavor/variant pour packs variety — {type: preset|custom, items[]}
- `incentives.referral` (object|null) : parrainage bidirectionnel — {enabled, referrer_reward{}, referee_reward{}}

**Gaps V2 documentés mais non implémentés** : credit-based membership (Fabletics), supply guarantee (Bobbie), eco-score (France), multi-channel pricing (Poppi), regulatory constraint flag

**Fichiers mis à jour**: `brands/_TEMPLATE/products/_example/offers.json`, `brands/_EXAMPLE/products/creme-eclat/offers.json`, `Ressources/schemas/offers.schema.json`
**Research**: `context-engine/research/offers-market-validation.md`

---

## v1.5.0 — 2026-04-04

**Action**: OFFERS SCHEMA OVERHAUL — Stress-test 22 scénarios + alignement extended schema
**Summary**: offers.json v1.1 — aligné sur le schema étendu (schemas/offer.json). Couverture : 20/22 scénarios e-commerce DTC réels. Décisions architecturales : bump/OPU = entité funnel future, pas attribut offre.

**Changements offers.json (v1.0 → v1.1)**:
- Nouveaux blocs : `subscription` (frequency, discount, commitment, `trial` complet), `incentives` (gifts[], discount détaillé, bulk_tiers[]), `gifting` (wrapping, message, recipient_shipping), `urgency` (limited_quantity, countdown, units_sold), `payment_options` (methods[], installments[])
- `pricing` enrichi : price_per_unit, price_comparison_note, savings_amount, savings_percent (derived)
- `contents` enrichi : duration, duration_unit, included_items[] avec discount_on_item
- `product_ids[]` : array (support bundles cross-produit)
- `placement` : product_page | email | retargeting uniquement — checkout_bump et post_purchase_upsell retirés (concepts funnel, entité séparée à venir)
- `type` enum révisé : single | bundle | subscription | gifting | seasonal | launch (trial, upsell, cross_sell supprimés — couverts par placement/subscription)
- `offer_id` convention : OFR-{NN}

**Décisions architecturales (D#134-138)**:
- Bump/post_purchase_upsell = architecture funnel, hors scope offre
- Pas de flag acquisition_eligible sur le produit — c'est le placement qui porte le contexte
- Clone-brand supprimé du backlog

**Fichiers mis à jour**: `brands/_TEMPLATE/products/_example/offers.json`, `brands/_EXAMPLE/products/creme-eclat/offers.json` (NEW — 3 offres réelles Lumya), `Ressources/schemas/offers.schema.json`

---

## v1.4.0 — 2026-04-04

**Action**: MEMORY SYSTEM OVERHAUL — Red team audit + 6-agent UX stress test
**Summary**: 3 critical fixes addressing the core memory/context management layer. Session relay, learnings lifecycle, and CLAUDE.md architecture redesigned based on 85 friction points identified across 6 user profiles (solo daily, multi-brand switcher, 20-brand power user, total novice, concurrent dual-agent, long-term decay).

**Fix #1 — Continuous Write + learn-from-session** (session relay v2):
- Session-state.md refactored: 3-block rotation → rolling activity log (max 30 lines, auto-maintained)
- Every skill that writes brand files auto-appends activity log line + updates status.json.last_activity
- NEW skill: learn-from-session v1.0.0 — semantic extraction at session end (learnings → learnings.json, decisions → Active Decisions, corrections → brand files, frictions → todos.md, open threads → session-state.md)
- Novice education: first-call explanation of how memory works
- No more "persist or die" — activity log captures context even without explicit session end

**Fix #2 — Learnings Lifecycle**:
- learnings.json schema extended: +id (LRN-{NNN}), +status (active/superseded/archived), +superseded_by, +genericity (brand-specific/sector/universal), +promoted_to
- validate-resources: new check 12b — contradiction detection (>60% tag overlap + opposing facts → auto-supersede), cross-brand promotion candidates → promote-backlog.json, staleness review (>180 days)
- NEW file: promote-backlog.json (workspace root) — structured backlog consumed by promote-learning
- promote-learning: new entry point C (from backlog), auto-cleanup after promotion
- ingest-resource: learnings entry structure now mandatory (10 fields documented)

**Fix #3 — CLAUDE.md Split + Context Budget**:
- NEW file: ARCHITECTURE.md — extracted Field Type System, Data Nature table, Dependency Graph
- CLAUDE.md: 207 → 112 lines (-46%). Sections compressed to 1-3 line summaries + renvois
- NEW section: Context Budget (brand ≤8k, cross-brand ≤15k, portfolio ≤20k tokens)
- validate-resources: new check 13 — CLAUDE.md size audit (root >150L or brand >80L → [SPLIT-CANDIDATE])

**Updated**: CLAUDE.md, ARCHITECTURE.md (NEW), brands/_TEMPLATE/*, brands/_EXAMPLE/*, ingest-resource, validate-resources, promote-learning, learn-from-session (NEW), promote-backlog.json (NEW)

---

## v1.3.0 — 2026-04-04

**Action**: P1 DELIVERY — Multi-brand, learning promotion, session relay, MCP server
**Summary**: All P1 roadmap items delivered. PhantomOS now supports multi-brand workflows, cross-brand querying, knowledge promotion, session continuity, and programmatic access via MCP.

**P1.1 — Cross-brand query** (query-resource v1.1.0):
- New scope `all_brands` with 3 query types: filter, compare, aggregate
- Filter: "quelles brands ont LTV > 500?" → scans all brands, returns matches
- Compare: "compare lumya vs moova" → side-by-side table (vertical, AOV, positioning, products, audiences, context level)
- Aggregate: "portfolio overview" → totals, revenue range, completeness distribution
- Performance guard: meta-first scan for >10 brands, max 20 brands per cross-brand query
- MCP tool definition updated with all_brands scope

**P1.2 — Learning promotion** (NEW skill: promote-learning v1.0.0):
- 6-step workflow: identify → evaluate genericity → route to KB → write via ingest-resource → tag promoted → summary
- Genericity test: brand-specific vs sector-generic vs universal
- Routing table: workarounds → conventions, patterns → catalogues, decisions → routing, principles → frameworks, procedures → sops
- Bidirectional tagging: `promoted_to` in learnings.json, `promoted_from` in KB resource
- Auto-detection: validate can flag cross-brand learning candidates (same platform + >60% tag overlap)

**P1.3 — Session relay hooks** (CLAUDE.md protocol):
- Mandatory read at session start: workspace-level + brand-level session-state.md
- Mandatory write at session end: rotate 3-session buffer, write decisions/changes/open threads
- Session end detection: explicit user command, /learn-from-session, context exhaustion
- Proactive open thread surfacing: "Dernière session : {focus}. Thread ouvert : {thread}."

**P1.4 — MCP server** (NEW: .skills/mcp/query-server.js):
- Full MCP protocol implementation (stdio JSON-RPC, MCP 2024-11-05)
- Handles: initialize, tools/list, tools/call
- Supports all 3 scopes: kb (scoring), brand (entity lookup), all_brands (filter/compare/aggregate)
- Zero dependencies (Node.js stdlib only)
- README with setup instructions in .skills/mcp/README.md
- Tested: initialize ✅, tools/list ✅, tools/call ✅

**Updated**: CLAUDE.md (skills table + session relay protocol), query-resource SKILL.md (v1.1.0)

---

## v1.2.0 — 2026-04-04

**Action**: UX OVERHAUL — Stress test fixes (15-agent simulation, S19-bis)
**Summary**: 3 critical fixes addressing 80% of friction points identified across 15 user profiles (beginner to expert, solo to 140-brand agency, FR/EN, e-com/SaaS).

**Fix #1 — Progressive Onboarding (3-tier system)**:
- CLAUDE.md: Replaced monolithic "Wedge Requirements" with 3-tier system (MVP → Enriched → Operational)
- CLAUDE.md: Added "Communication Rules" section — never say wedge/schema/slug to users, always show next step, tier framing, bilingual mode
- setup-brand: Onboarding brief now shows 3 levels with specific field guidance per tier
- validate-resources: Added "Context Level" tier-aware display per brand (Tier 1 = blocking, Tier 2-3 = suggestions)
- brands/_TEMPLATE/CLAUDE.md: Replaced "Wedge Docs" with "Context Levels" (3 tiers, checkboxes)
- brands/_EXAMPLE/CLAUDE.md: Updated to show Lumya's tier status (Tier 1 ✅, Tier 2 partial, Tier 3 ✅)

**Fix #2 — Post-Validate Bridge**:
- validate-resources: Added "Post-Validate Usage Guide" — shows concrete agent commands after validation (product descriptions, hooks, emails, briefs)
- README: Added "Étape 5 — Utiliser tes agents" section with example prompts
- Hard rule: validate NEVER ends without showing what to do next

**Fix #3 — Ingest Transparency**:
- ingest-resource: Added mandatory "Step 5 — Summary Output" — structured display of entities updated, fields written (✓), inferred (⚠), missing (✗), completeness %
- Confidence labeling: explicit/inferred/missing for every field written
- Completeness calculation documented per entity type
- Hard rule: ingest NEVER ends silently

**Cross-cutting**:
- README: Added bilingual English intro section with Claude Code link and entry instructions
- README: Added glossary (FR/EN) — brand, slug, ingest, validate, niveaux, KB, skills, schema
- README: Added FAQ entries: "Can't fill all fields?", "Where is Claude?"
- README: Removed "wedge" terminology from all user-facing text
- README: Updated from 4-step to 5-step onboarding (added "Utiliser tes agents")

---

## v1.1.0 — 2026-04-04

**Action**: RELEASE
**Summary**: First stable release. Full pipeline (setup → ingest → validate → query → migrate), 6 entity schemas, all-brands validation mode, credentials management, operational learnings.

**Skills**: setup-brand v1.0 | ingest-resource v1.1 (auto-create folders, products_index sync, multi-entity split, learnings/strategy routing) | validate-resources v1.1 (Next Actions, all-brands mode, learnings/strategy freshness) | query-resource v1.0 (MCP spec included) | migrate-instance v1.0
**Schemas**: brand, spec, profile, offers, learnings, strategy (JSON, aligned with _TEMPLATE)
**Brand template**: 6 entities (brand, product, offer, audience, learnings, strategy) + OS files (CLAUDE.md, config.json, status.json, todos.md, session-state.md, credentials.env)
**Credentials**: 2-level pattern — `credentials_shared.env` (workspace) + `brands/{slug}/credentials.env` (brand). All gitignored.
**Example**: Lumya (skincare, FR) — brand + 1 product + 1 audience + 4 learnings + strategy, intentionally missing offers to demo validate flags
