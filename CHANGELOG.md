# Changelog

> Auto-maintained by skills (ingest-resource, validate-resources, setup-brand).
> Never edit manually. Newest entries at top.

---

## v2.22.0 — 2026-05-03 — /phantom navigation interactive (AskUserQuestion)

**Why this release.** Le CLI n'a pas de flèches haut/bas pour naviguer dans une arborescence comme dans un explorateur de fichiers. v2.21 a posé la navigation terminal-like (`/phantom`, `/phantom {slug}`, `/phantom {slug} {entity}`), mais chaque pas demandait à l'opérateur de re-taper la commande. Friction inutile sur un workflow de cockpit que l'opérateur consulte 5-10 fois par session.

**What shipped.**

- **`AskUserQuestion` ajouté à la fin de chaque rendering `/phantom`.** 4 options cliquables structurées comme un explorateur de dossier imbriqué. Slot 1 : drill vertical primaire. Slot 2 : drill alternatif ou latéral. Slot 3 : action top-priority (paste-ready, déclenchée au clic). Slot 4 : *Retour {parent}* (toujours présent, jamais omis).
- **Slots concrets par mode** :
  - Workspace : drill brand actif, drill brand en alerte, action cross-brand top, *Voir un autre brand*
  - Brand : drill audiences, drill {entity la plus chargée}, action top sur ce brand, *Retour workspace*
  - Entity-drill : action top sur l'entité, action 2 sur l'entité, drill entité voisine, *Retour {brand}*
- **Saturation pattern.** Si la session a déjà déclenché 3 AskUserQuestion `/phantom` dans les 5 dernières minutes, le 4e rendering désactive l'AskUserQuestion (text-only). L'opérateur est en deep-exploration, le pattern devient bruit. Re-active après 5 min idle ou après un autre skill.

**Hard rule** : le rendering textuel reste TOUJOURS, l'AskUserQuestion s'ajoute APRÈS. L'AskUserQuestion accélère, ne remplace pas.

**Breaking changes.** None.

**Operator impact.** Friction navigation tombe à 1 click. `/phantom` → click *Drill karacare* → brand mode → click *Drill audiences* → entity-drill → click *Lance mine-voc sur karacare* → l'agent exécute. À tout moment slot 4 = retour parent. Le typing libre reste possible.

---

## v2.21.0 — 2026-05-03 — /phantom navigation terminal-like

**Why this release.** Live test on phantomos-test surfaced a navigation regression: `/phantom` with a single brand was auto-jumping to brand mode (intended convenience), short-circuiting the operator's mental model. The operator never learned that a workspace level exists distinct from a brand level. Plus, the NEXT SUGGESTED blocks were conversational suggestions instead of runnable commands, forcing the operator to re-formulate every recommendation before acting.

**What shipped.**

- **Workspace mode is the default.** `/phantom` (no arg) always lands at workspace level if ≥1 brand exists. The operator drills explicitly via `/phantom {slug}`. Mirrors terminal navigation : you `cd` into a folder rather than land in it without choosing.
- **New mode entity-drill** : `/phantom {slug} {entity}` zooms on one entity within a brand. Supported entities : `audiences`, `angles`, `products`, `offers`, `strategy`, `learnings`. Brand mode caps at 50 lines and gives a summary across all entities ; entity-drill goes deeper on the chosen one (full audience hierarchy with mining state per slot, full angles list with status and ROAS, full per-product spec completeness map, etc.).
- **NEXT SUGGESTED ships paste-ready commands** across all modes. Format : *"→ Tape : `lance mine-voc sur karacare` (7 audiences en hypothèse, aucun verbatim encore)"*. Single back-tick wrap as visual contract : what's inside is what the operator pastes back. Zero re-formulation cost between seeing the suggestion and running it.
- **Em-dashes swept** from `phantom.md` per voice canon (replaced with `:` or `·` per context).

**Breaking changes.** `/phantom` with no arg no longer auto-drops into brand mode when only one brand exists. Single-brand operators see one extra step (`/phantom` → `/phantom {slug}`) but learn the navigation explicitly.

**Operator impact.** Cockpit feels like a terminal. `/phantom` = `ls workspace`. `/phantom {slug}` = `cd` into a brand. `/phantom {slug} audiences` = drill into the audiences of that brand. Operator learns the structure naturally. NEXT SUGGESTED actions are always copy-paste runnable.

---

## v2.20.0 — 2026-05-03 — Onboarding bases reposées

**Why this release.** Live test on phantomos-test surfaced that the tour was evoking the compound (*"ce que tu corriges devient une règle"*) without naming `/learn-from-session`. It introduced skills (Milestone 6) without naming `/phantom`. The wow synthesis (Milestone 7) was strong but left the operator without a correction pattern, without a visualization tool, without a frame for the *à valider* status they were about to see across the system. Onboarding finished, operator had no concrete handles.

**What shipped.**

- **Milestone 5 names `/learn-from-session`.** One paragraph after the centralization payoff frames the command as the manual lock when a point matters. Compound mechanism stops being abstract.
- **Milestone 6 names `/phantom` alongside `/skills`.** Both positioned as repeatable commands the operator can run anytime. `/phantom` framed as *"cockpit de visualisation, read-only, pas de risque"* to invite exploration without anxiety.
- **Milestone 7 adds a bridge paragraph** between the synthesis and the validation question. Introduces in one block: the correct/reject/validate pattern, `/phantom {brand_slug}` for tree visualization, and the *à valider* status as deliberate hypothesis-grade signal awaiting mine-voc confirmation.
- **Milestone 8 close gains the Pipeline DTC archetype.** Reflective close composer now has snapshot → mine-voc → produce-paid-angles → produce-copy-brief as a coherent value chain to surface when the operator profile is paid manager / agency / DTC media buyer. `audience-cartography.md` added to the silent reasoning step's source list.
- **Replay mode close** ends the *Just refreshing* option with a one-line reminder of the three daily commands so operators returning briefly leave with concrete next moves.

**Tour length** : 388 → 401 lines, well under the 450-line cap.

**Breaking changes.** None.

**Operator impact.** First-session onboarding hands over three concrete commands and a vocabulary frame instead of leaving the operator with abstract concepts. Replay sessions surface the daily commands explicitly. Paid profiles see a Pipeline DTC angle in the reflective close.

---

## v2.19.1 — 2026-05-03 — Audience cartography wording polish

**Why this patch.** Live operator feedback after v2.19.0: operator-facing copy was leaking skill-author vocabulary (*"cartography axis"*, *"mother audience"*, *"hand-off pédagogique"*, *"validation_status: hypothesis"*, *"hypothesis-grade"*). Too clinical, too internal. Skill-author structure was solid, the surface needed plain language.

**What shipped.**

- **`snapshot-brand` Step 5 operator-facing examples rewritten in plain language.** *"manières de découper"* instead of *"cartography axes"*. *"groupe principal"* / *"sous-groupe"* instead of *"mother audience"* / *"sub-audience"*. *"à valider"* instead of *"hypothesis"*. *"hypothèse de travail"* instead of *"hypothesis-grade"*. The four Movement section headers stay in the skill file as structure for skill authors, but never leak in operator output.
- **Movement 3 closing now mentions `/phantom {brand_slug}`** so the operator can visualize the encoded audiences anytime as a tree, not have to re-query.
- **`/phantom` mode brand extended with hierarchical audience tree.** Renders the mère/sous structure with translated validation labels (`à valider` / `testée` / `validée` / `scalée` / `fatiguée`) and a coarse mining state (`vide` / `partiel` / `dense`). Never exposes `validation_status` enum or numeric percentages.

**Breaking changes.** None.

**Operator impact.** Snapshot conversation feels less clinical. The cockpit `/phantom {brand}` renders the audience cartography as a tree, matching the structure the operator just agreed to in Step 5.

---

## v2.19.0 — 2026-05-03 — Audience cartography (4 movements)

**Why this release.** Live test on the phantomos-test workspace surfaced a dominant friction in `snapshot-brand` Step 5: the agent collapsed what should have been seven audiences (2 mothers + 5 sub-audiences for Karacare) into a single flat *femmes-cheveux-fragiles* profile. The operator had to spend 6+ minutes manually rebuilding the cartography (proposing axes, hierarchy, sub-segmentation) that the agent should have proposed autonomously. Symptom of a deeper bug : Step 5 was form-fill, not cartography.

**What shipped.**

- **`docs/system/audience-cartography.md` doctrine added.** Governs the contract for audience-mapping behavior across snapshot-brand, mine-voc, produce-paid-angles. Names the four movements, the three canonical axes (pain-driven, situational, demographic), the field-level contract, and the anti-patterns.
- **`snapshot-brand` Step 5 rewritten as 4-movement audience cartography.** Movement 1 raw observations (never skipped, exposes thin pages), Movement 2 cartography axes (always 2-3 alternatives, default hypothesis tied to a Movement 1 observation), Movement 3 hierarchy mère/sous-audiences (default hierarchical, not flat), Movement 4 hand-off pédagogique vers mine-voc (anchors why the encoding matters, proposes the next skill).
- **`snapshot-brand` Step 6 updated to scaffold N audience folders.** Mother audiences carry `meta.parent_slug: null` and `meta.scope: "broad"`. Sub-audiences carry `meta.parent_slug: "{mother-slug}"` and `meta.scope: "segment"` (or `"micro"` for hyper-niches). All sub-audiences `meta.validation_status: "hypothesis"` until mine-voc enriches them.
- **Field-level contract enforced.** snapshot-brand fills only the cartography skeleton (`meta.*`, `identity.gender`, `identity.age_range`, `pain.primary_problem`). `pain_points[]`, `psychology.beliefs_*[]`, `voice.key_expressions[]`, `objections[]` are mine-voc territory. Inferring those from a product page is hallucination and is now explicitly forbidden.
- **`CLAUDE.md` Reference list extended** with a pointer to `audience-cartography.md`.

**Breaking changes.** snapshot-brand now produces N audience folders (typically 4-12) instead of 1. Skills downstream that assumed exactly one audience per snapshot run must iterate. mine-voc and produce-paid-angles already handle multi-audience input. Custom skills referencing *"the audience"* from snapshot output must be reviewed.

**Operator impact.** Snapshot of a new brand delivers a structured cartography conversation instead of a fill-in-the-blanks form. Operator picks the cartography axis they see in performance data, gets a hierarchy proposed by default, and lands on Movement 4 with an explicit invitation to mine-voc. The 6-minute manual re-classification observed in the karacare live test becomes a 2-3 turn agent-driven proposal.

---

## v2.18.0 — 2026-05-03 — encode-batch sub-skill (responsiveness)

**Why this release.** Producer skills (snapshot-brand, ingest-resource) encoded 15-50 mutations sequentially in the main thread, blocking 60-120s. Operator perception : the agent "grinds through fields". Cognitive split : extracting semantic signals from a scrape is Sonnet-grade work ; mapping `semantic_kind` → `field_path` is Haiku-grade mechanical work. This release pulls the mechanical half into a sub-agent.

**What shipped.**

- **`encode-batch` sub-skill added.** Shared, Haiku, `subagent_safe: true`, `operator_facing: false`. Receives N observations (semantic_kind + raw_value + evidence + source + confidence_signal) from a producer. Loads the target schemas + existing files. Maps each observation to a `field_path` via canonical table. Runs `write-to-context.py` per mutation. Rebuilds snapshot once at end. Runs `finalize-mutation-batch.py` once at end. Returns a structured JSON summary to the caller. Refuses unmapped `semantic_kind` rather than guessing.
- **`snapshot-brand` Step 3 + Step 6 patched.** Spec.json generation (Step 3) and profile.json base (Step 6) now delegate the N-mutation encoding to encode-batch via Task tool. Producer assembles observations from scrape + Q1-Q4 answers, ships the payload, continues to Step 7 synthesis without blocking.
- **`ingest-resource` Step 3B patched.** Encoding via encode-batch when batch >5 mutations. Inline `write-to-context.py` still acceptable for ≤5 mutations (sub-agent overhead not worth it).
- **`.skills/_manifest.json` regenerated.** encode-batch indexed (42 skills total).

**Performance.** snapshot-brand 25-mutation run target : 5-15s synthesis on operator side instead of 60-120s sequential. Encoding runs in background as Haiku sub-agent. Operator sees a one-line footnote (e.g. *"27 mutations encoded in background, all green"*) instead of watching field-by-field grind.

**Breaking changes.** None.

**Operator impact.** Snapshot-brand and ingest-resource feel materially faster. If finalize-mutation-batch flags a blocking issue, producer surfaces it before close.

---

## v2.17.0 — 2026-05-03 — Canon cleanup + schema standardization

**Why this release.** Recent build sessions (S50 → S54) inscribed multiple briques typées at the canon (Tension, Pain, Bénéfice, JTBD, Trigger, Alternative, AwarenessStage, ChainNiveau) and drafted matching R&D schemas, but never finished the migration into the template. Audit revealed 3 canon entries with zero schema instance + zero skill consumer + zero brand instance, an enum-case split between R&D (kebab) and template (snake) blocking future $ref refactor, and 0% description coverage on the two most critical schemas. This release reconciles canon with implementation reality.

**What shipped.**

- **Canon trimmed from 8 to 5 briques typées.** `docs/internal/canon.md` drops Tension, Alternative, Trigger entries (never instantiated, never consumed). Final canon: Pain, Bénéfice, JTBD, AwarenessStage, ChainNiveau.
- **R&D draft schemas deleted** matching the dropped canon entries: `schemas/types/tension.schema.json`, `alternative.schema.json`, `trigger.schema.json`.
- **Snake_case enum convention enforced across R&D schemas.** Migrated kebab-case enum values to snake_case in `awareness-stage.schema.json` (problem-aware → problem_aware, etc.), `pain.schema.json` + `benefice.schema.json` (spec-produit → spec_produit), `_source-meta-fragment.json` (operator-statement → operator_statement, third-party → third_party), `chain-niveau.schema.json`, `learnings.schema.json` (test-result → test_result, decision-trace → decision_trace), `audience-v2.schema.json`, `product-map.schema.json` (brand-filtered → brand_filtered), `brand-position.schema.json` (voix-off → voix_off), `resources/schemas/sop.schema.json` (3 enums migrated). Resolves the WS-vs-R&D split that blocked future type extraction in $ref form.
- **Title casing standardized EN Title Case.** `AwarenessStage` → `Awareness Stage`, `Bénéfice` → `Benefit`, `ChainNiveau` → `Chain Niveau`, `Position de marque` → `Brand Position`. Matches template baseline EN convention.
- **100% description coverage on profile + spec schemas.** `resources/schemas/profile.schema.json` documents 12 top-level fields. `resources/schemas/spec.schema.json` documents 17 top-level fields. Pre-cleanup coverage was 0%.
- **`cartograph` gains `--incomplete` mode.** New row in Modes table: `cartograph --learn brand=<slug> --incomplete` allows partial cartograph in brand mode without `wedge_complete: true` requirement. Outputs partial synthesis READ-ONLY with explicit warning + 3 prioritized completion decisions.
- **`snapshot-brand` polished.** Renamed in-skill section "Layer 2 — product page HTML" → "Product detail page scraping" to avoid collision with the doctrinal "Layer 2 = APIs callable through skills" defined in root `CLAUDE.md § Connected tools`. Added large-catalogue (>200 SKUs) sampling rule: instead of full enumeration of `products.json`, read pages 1, 2, recent-published, surface volume to operator, invite specific URL paste.
- **Typo fix in `_TEMPLATE` audience example.** `brands/_TEMPLATE/audiences/_example/profile.json` line 70: `'awareness:solution-aware'` → `'awareness:solution_aware'`. Aligns example with snake_case enum convention.
- **Stress test panel run.** 5-expert backdoor stress test (DTC operator, DR copywriter, brand strategist, schema architect, media buyer) scored 32.75/50 (threshold 35/50). NO-GO threshold not met; ship accepted with documented limitations. Full report: `05-projects/context-engine/research/stress-test-cleanup-2026-05-03.md` (R&D side, not template).

**Documented limitations (panel feedback).**

- **Tension treated as runtime composition pattern, not stored brique.** Convergence 3/4 experts flagged Tension drop as load-bearing for cold-acquisition DR copy. Resolution: Tension is a pattern of inference (composition of `psychology.core_desire` + `psychology.beliefs_limiting` + `pain_points[].emotion`), not a stored type. Pattern documentation in framework (e.g. `voc-coding.md`) deferred to a future cold-copy production cycle.
- **Antagonist concept roadmap'd.** Brand strategist (25/50) flagged absence of typed positioning narrative brique. Currently lives unstructured in `brand.json#/positioning/differentiation`. Future extraction in `antagonist.schema.json` deferred to a brand-strategy session.
- **`audit-meta-account` v1.1 covers ~70% of Meta health checks.** Missing CBO/ABO, DSA, Advantage+, multi-account. Roadmap'd v1.2.
- **`produce-launch-bundle` orchestrator deferred.** Operators must currently chain `mine-voc → produce-paid-angles → produce-copy-brief` manually.

**Breaking changes.**

- Any R&D draft consumer (none currently — drafts were uninstantiated) referencing kebab-case enum values must migrate to snake_case.
- Canon entries Tension, Alternative, Trigger removed. No template skill was consuming them.

**Operator impact.** None visible. Internal doctrine cleanup. Operators continue to see the same skill behaviors. Cartograph gains an explicit partial-output mode for early-stage brands.

---

## v2.16.0 — 2026-05-03 — Language doctrine amendment

**Why this release.** Audit revealed 63 template files with FR-authored quoted agent-speech examples (illustrative *"the agent might say…"* snippets in skills, commands, doctrine). The previous rule (*"code blocks quoting agent speech in templates are EN baseline, translated live at runtime"*) was not enforced in practice and produced no operator-facing effect, runtime adapts to operator language regardless. The constraint had no value, only false debt.

**What shipped.**

- **`CLAUDE.md` § Language amended.** Quoted agent-speech examples inside skills, commands, and doctrine may now be authored in FR or EN. Template prose (doctrine, system docs, README, vision, product docs) remains EN baseline. Manifest trigger phrases stay bilingual FR + EN by design.

**Breaking changes.** None.

**Operator impact.** None. Quoted examples continue to render in operator language at runtime.

---

## v2.15.1 — 2026-05-03 — Cross-doc cohérence cleanup

**Why this release.** Post 2.15.0 audit surfaced 5 stale cross-references between docs and skills. No behavioral change, no schema bump. Cohérence patch only.

**What shipped.**

- **Skill rename swept** : `audit-meta-setup` → `audit-meta-account` references closed in `.skills/INDEX.md`, `.skills/README.md`, `.skills/_manifest.json`, `.skills/skills/validate-resources/SKILL.md`, `.skills/skills/connect-source/SKILL.md`.
- **Release manifest path fixed** : template `README.md` pointed to `docs/releases/{version}-manifest.json`. Real path is `docs/internal/releases/manifest/{version}-manifest.json`.
- **Ghost skill flagged** : `correct-skill` was described as shipped in `docs/system/autonomous-correction-pattern.md`, `docs/system/pattern-detection-triggers.md`, `docs/system/skill-authoring-discipline.md`. Marked `[backlog, not shipped]` inline.
- **Lexicon pointer added** : `Connected source` entry in `lexicon.md` now points to `docs/internal/canon.md` for full definition.
- **Manifest regenerated** : `.skills/_manifest.json` rebuilt post rename sweep.

**Breaking changes.** None.

**Operator impact.** None. Documentation cohérence only.

---

## v2.15.0 — 2026-05-03 — Privacy and surface cleanup

**Why this release.** Pre-broader-release pass to remove from the public template anything specific to a downstream extension and to anonymize any real client brand name still appearing in examples or doc text.

**What shipped.**

- **Real client names anonymized.** All real client brand slugs replaced with fictional names across examples, doc text, skill outputs, and internal manifests. 9 brand identifiers swept across 34 files. Canonical fictional names used in shipped examples : northsense, vitatone, peaktrek, glowco, nestra, freshbite-foods, shellbrand, skyfloat, acmeflow.
- **Downstream-extension-specific skill removed from public template.** `connect-cockpit` skill (data plumbing to a downstream cockpit dashboard) no longer ships in the public template. Lives in the corresponding downstream extension repository instead.
- **`docs/product/variant-map.md` simplified.** Now focuses on template versus operator instance, no longer exposes the existence of private downstream extensions or addons.
- **Manifest cleanup.** `.skills/_manifest.json` regenerated post connect-cockpit removal. Disambiguation references to connect-cockpit swept across sibling skills.

**Breaking changes.**

- `connect-cockpit` skill removed from the public template (only relevant to downstream extension users, who have the skill via that extension's repository).
- Hardcoded brand slug references in custom workflows need to update to the new canonical fictional names.

**Operator impact.** Public template surface clean of real client identifiers and downstream-specific skills. Day-1 reading no longer surfaces private business context.

---

## v2.14.0 — 2026-05-02 — Cleanup post-audit Red Team

**Why this release.** Audit Red Team multi-perspective on the operator-facing surface revealed referenced skills that did not exist, internal jargon leaking to operator docs, manifesto starting with theory before reaching the DTC use case, and missing standard GitHub canon files. This release closes those gaps before broader release.

**What shipped.**

- **Skill renamed** : `audit-meta-setup` → `audit-meta-account` (clearer name for operators). All references updated across README, CLAUDE.md, /phantom command, severity-canon, and 3 doctrine files.
- **Ghost skill references dropped** : `generate-handoff`, `produce-offer-scoring`, `correct-skill` were referenced in INDEX.md and disambiguations but never shipped. References removed.
- **Manifesto restructured** : section 7 now opens with the concrete DTC paid acquisition case, then generalizes. Previously DTC was buried at the end after 7 sections of theory.
- **Multi-operator workaround** : new section in `docs/product/fit.md` documenting the 2 to 5 person agency workflow (one workspace per client brand owned by senior operator, juniors consume read-only, workspace handoff at retainer end).
- **Empirical proof reframed** : `docs/product/fit.md` cost honesty section points to an on-demand `benchmark-tokens` skill (planned) for per-operator measurement on real workspaces.
- **Stubs added** : `operator/connected-sources.json` (workspace scope), `brands/_TEMPLATE/connected-sources.json` (brand scope), `brands/_TEMPLATE/angles/README.md` (entity stub).
- **GitHub canon added** : `LICENSE` (MIT), `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md` (Contributor Covenant 2.1), `.github/ISSUE_TEMPLATE/` (bug + feature), `.github/PULL_REQUEST_TEMPLATE.md`.
- **`docs/internal/` formalized** : explicit FOR CONTRIBUTORS banner, `docs/internal/README.md` table of contents, release manifests moved from `docs/releases/*.json` to `docs/internal/releases/manifest/*.json`. `docs/releases/README.md` redirects to root CHANGELOG and the internal manifests folder.
- **Internal session and decision references swept** from 16 files in `docs/system/` (sessions Sxx, decisions Dxxx, "drafted Sxx", "R&D zone Build mode" labels removed).
- **Architecture rephrased** : `docs/system/architecture.md` "agnostic receptacle for encoding any business domain" replaced by "extensible substrate for encoding any operator domain that an agent can operate on, DTC paid acquisition is the current incarnation".
- **Temporal hedging swept** : "currently / today / aujourd'hui" removed from README, fit.md, positioning-pitch.md, offering-deployment.md (~9 occurrences).

**Breaking changes.**

- Skill rename `audit-meta-setup` → `audit-meta-account` (workflows or scripts referencing the old name need update).
- Release manifests moved : direct links to `docs/releases/X-manifest.json` should now point to `docs/internal/releases/manifest/X-manifest.json`.

**Operator impact.** Surface more credible : referenced skills resolve, doctrine jargon hidden behind clear contributor banners, manifesto reaches the DTC operator immediately, agency workflows documented. Day-1 experience does not break on missing files.

---

## v2.10.1 — 2026-04-26 — Production layer #2: produce-copy-brief

**Why this release.** Cascade #2 of the production-layer roadmap. After produce-paid-angles (v2.10.0), the natural next surface is the copywriter brief — operator picks one ranked angle and gets a per-channel brief composed from the same encoded brand intelligence.

**What shipped.**
- `produce-copy-brief` (producer Sonnet, subagent_safe, ~425 lines). 8-step pipeline: resolve audience+angle+channel → read encoded data → verbatim density floor → map sections per voc-coding lenses → hook variants (4-tier anchor priority) → brief composition (800-1200 words) → Layer A trace + Layer B artifact → finalize-mutation-batch.
- 4 focus modes: `default | hooks | objections | ctas | fresh`. Brief format pulled from `operator/profile.json#preferences.brief_format` with brand-specific override.
- 5 architectural decisions encoded (S39 batch triage): channel inferred from operator stack + brand current_focus (never hardcoded Meta-as-default), hook examples = 3 hook-only, brief 800-1200 / 1500 ceiling, multi-offer = active offer inline in CTAs, brief artifact never pasted twice (write to file, surface synthesis only).

**Operator impact.** Natural cascade: paid-angles → pick the angle → copy brief on that angle, channel-aware, verbatim-anchored, format-respected.

---

## v2.10.0 — 2026-04-25 — Production layer #1: produce-paid-angles + no-orphan-output doctrine

**Why this release.** Intelligence layer (v2.9.x) encoded the brand. Production layer turns that intelligence into operator-shippable artifacts. First skill: paid creative angles, ranked, hook-anchored from voc verbatims. Doctrine: no producer surface should ever leave the operator in the void.

**What shipped.**
- `paid-angle-scoring.md` framework (147 lines). 5 lenses (verbatim density 35%, emotional resonance 20%, objection neutralization 20%, placement viability filter, awareness alignment 25%), aggregation formula, cluster filter, 4-tier verbatim anchor priority, 6 anti-patterns.
- `produce-paid-angles` (producer Sonnet, subagent_safe, ~430 lines, 15 Hard Rules). Cartesian product internal, 5-lens scoring, cluster filter, ranked top 5 (cap 7), markdown table operator-facing with reasoned next-step close.
- `CLAUDE.md` master doctrine: **No orphan output rule** added. Every producer / curator / orchestrator significant output ends with a contextual reasoned next-step proposal, never a flat menu, never a hardcoded template.
- 5 architectural decisions encoded (S39 batch triage): hook granularity = headline-only, default count = 5, auto-trigger after mine-voc = OFF, cache 24h TTL, sister content/email = NOT in v1.

**Operator impact.** "Trouve les meilleurs angles pour [audience]" returns a ranked matrice, hooks anchored verbatim from voc corpus. Every producer skill from now on closes with a reasoned next move.

---

## v2.9.1 — 2026-04-25 — Manifest discovery fix: trigger format FR:/EN:

**Why this release.** Manifest builder regex expects `FR:` / `EN:` delimiters. v2.9.0 ship used `FR triggers:` / `EN triggers:` which did not parse. 4 deepening skills had empty triggers in `_manifest.json`, breaking trigger-based discovery.

**What shipped.**
- Trigger format fix in `mine-voc`, `mine-vom`, `study-niche-marketdeepdive`, `deepen-brand-context` (`cross-deepening-signals` already correct, no triggers as sub-skill).
- `_manifest.json` regenerated, triggers now extracted correctly.

**Operator impact.** Phrases like "mine voc", "creuse la voix client", "deep-dive niche" route correctly to the deepening skills.

---

## v2.9.0 — 2026-04-25 — Intelligence layer: 3 deepening skills + orchestrator + cross-synthesis

**Why this release.** Snapshot Step 7 (v2.8.3) closed with two paths: validate-or-correct. Operator needed a third: "trust the synthesis, go deeper." This release ships the deepening surface as standalone producer skills + an orchestrator that adds real cross-synthesis value (not a wrapper).

**What shipped.**
- 3 frameworks codified, consumed as analytical vocabulary (never as section headers): `voc-coding.md` (143 lines), `vom-mining.md` (150 lines), `market-deepdive.md` (124 lines).
- `mine-voc` (producer Sonnet, ~330 lines). Step 0 first-party data ask, source scrape (native widgets via Chrome MCP, Trustpilot, Sephora, Reddit, app stores), 4-lens coding, two-layer output (JSONL corpus + routed mutations to spec.json verbatim_quotes[] and profile.json voice.key_expressions[]). 4 `--focus` modes.
- `mine-vom` (producer Sonnet, ~290 lines). Competitor integrity check, niche definition lock, source crawl, `external_intelligence[]` cap 5-7 per run. 4 `--focus` modes. 7d cache.
- `study-niche-marketdeepdive` (orchestrator Sonnet, ~430 lines). Long-running 30-60 min strategic deep-dive. Mandatory ticket lifecycle. 12 steps. Memo 4-6 pages with `[MKT-NNN]` citations. 6-9 month re-run cadence. Standalone-only — never auto-chained.
- `deepen-brand-context` (orchestrator Sonnet, 199 lines). Chains `mine-voc → mine-vom → cross-deepening-signals`. AskUserQuestion 4-paths Step 0.
- `cross-deepening-signals` (sub-skill Sonnet, subagent_safe, operator_facing: false, 167 lines). Read-only. 3 mandatory cross-checks: audience candidate × market presence, vocabulary shift × current vernacular, white-space × channel signals. Output: 3-movement synthesis paragraph + JSON return contract.
- `snapshot-brand` Step 7 enriched: trust-and-deepen close (4 paths AskUserQuestion).
- D#357 locks 4 architectural decisions: `--focus` parameter, orchestrator with real cross-skill synthesis, Step 0 first-party data ask universal, free format for first-party imports.

**Operator impact.** Four paths after snapshot synthesis instead of two. Three depths available: VoC alone (~15 min), VoM alone (~25 min), full deepening chain with cross-synthesis (~45 min).

---

## v2.8.3 — 2026-04-25 — Revert v2.8.2 bold anchors, back to pure prose 3 movements

**Why this release.** Live test on a DTC pilot + Largo feedback: bold-section anchors ("**Le vrai pitch**", "**La cible logique**") feel template-flavored and visually heavy regardless of content quality. v2.8.2 was an over-correction. Pivot back to v2.8.1 pure-prose 3-movements format, with explicit ban added to prevent future drift.

**What shipped.**
- `snapshot-brand` Step 7 hard rules: pure prose only, explicit ban on bold-section anchors, numbered headings, templated paragraph openers. 3 movements with blank lines, NO titles. Each paragraph names what it carries via its first sentence.
- Decisive test before sending: "if you see bold section labels or templated openers, you reverted to form-fill — rewrite as flowing prose."

**Operator impact.** Snapshot Step 7 returns to v2.8.1 reading experience. Cleanest pattern observed to date. Doctrine clarification: structure carries itself through prose, not through scaffolding.

---

## v2.8.2 — 2026-04-25 — Adaptive named anchors in snapshot Step 7 (REVERTED in v2.8.3)

**Why this release.** Largo flagged that pure-prose synthesis (v2.8.1) lacks scaffolding for fast scanning, but a fixed template would re-import the form-fill anti-pattern. Compromise attempted: 2-4 adaptive named anchors per snapshot, agent chooses based on what is load-bearing for THIS product in THIS niche.

**What shipped.**
- `snapshot-brand` Step 7: 2-4 adaptive bold anchors with open canonical list ("Le vrai pitch", "La cible logique", "L'angle commercial", "Ce que tu n'as peut-être pas vu", etc., + free-form). Hard limits: never empty, never template-flavored, never the same 4 anchors every brand.
- Stress test harness: `research/synthesis-stress-test/scenarios.json` (10 scenarios) + `run.py` (Anthropic SDK) + `results.md` author verdict. Findings: 9/10 syntheses produced real insights, anchor diversity strong, 100% doctrine compliance in simulation.

**Operator impact.** Brief — bold anchors visible during the v2.8.2 window only. Reverted within hours by v2.8.3 after the live DTC pilot test failed Largo's taste test ("pas fan des anchors en gras"). Stress test harness retained as future evaluation primitive.

---

## v2.8.1 — 2026-04-25 — Cascade A micro-patches from live test on a wellness pilot

**Why this release.** Live wellness pilot test confirmed Cascade A v2.8.0 holds under load. Three micro-frictions surfaced and patched.

**What shipped.**
- `snapshot-brand` Step 7: "three movements + blank line between each" rule. Movement 1 = what it really is + who buys. Movement 2 = offer architecture. Movement 3 = 1-2 things noticed. Same density, breaks wall-of-text.
- `tour` Milestone 3 (blasé question): explicit rule to ask early, woven into context-capture turn. Never as post-script closing the wow turn.
- `tour` Milestone 7 url-path: hard rule against cascading Milestones 5/6 (PhantomOS intro + skill concept) immediately after the wow synthesis. Re-pitching dilutes the wow.

**Operator impact.** Synthesis paragraph reads cleaner. Blasé question lands at the right moment. Wow synthesis no longer diluted by reflexive PhantomOS re-pitch.

---

## v2.8.0 — 2026-04-25 — Cascade A + C: synthesis-first across producer / orchestrator surfaces

**Why this release.** First execution pass on the audit-v2.7.4-prompting roadmap. Producer surfaces still recapped as form-fill ("here's what I found in 8 fields"). Bundle: synthesis-first analytical paragraph using schemas as vocabulary, not as section headers. Plus pre-snapshot context capture so the wow lands in a context-aware operator state.

**What shipped.**
- `snapshot-brand` Step 7: form-fill recap → 4-6 sentence analytical paragraph using schemas (`problems_solved`, `audience.pain`, `market_context.sophistication`, `offer_groups[].offers[]`) as vocabulary. Single confirm question. No score, no field list, no missing-fields block. Inferred attributes flagged inline.
- `tour` Milestone 7 url-path + `setup-brand` Step 4 + `onboard-brand` Phase 2: cascade the same synthesis vocabulary across surfaces. Onboard drops "I keep going with integrity check" announcement (validate runs silently).
- `tour` Milestone 2 path-(a): pre-snapshot context capture. Use-case (own brand / client / agency portfolio / test) + stack (Shopify / Meta Ads / Klaviyo / Notion / Slack / Drive / others) collected in flowing prose, written to `operator/profile.json#identity.profile + context.stack[]`.

**Operator impact.** Day-1 onboarding starts with two flowing context questions before scrape, no URL-first ambush. Snapshot returns as consultant's read on the brand, not as field-list recap.

---

## v2.7.4 — 2026-04-25 — Master doctrine: Contextual Intelligence locked

**Why this release.** S37 confirmed the recurring pattern across v2.7.1-3: narrative MANDATORY rules in SKILL.md get skipped 100% under load, mechanical hooks/wrappers hold 100%. Architectural conclusion formalized as PhantomOS master doctrine. D#356.

**What shipped.**
- `docs/system/contextual-intelligence.md` (114 lines) — canonical doctrine. Thesis (PhantomOS reasons over a business universe, does not fill forms). Two-tier rule: mechanical layer = strict enforcement; semantic layer = strict trust. Decisive test for any new rule/hook/gate. 7 named anti-patterns.
- `CLAUDE.md` root: new "Master doctrine" section at top, before FIRST ACTION. Two-tier rule + decisive test surfaced runtime.
- `docs/system/voice.md`: opens with contextual-intelligence reference.

**Operator impact.** None directly. All future architectural decisions must pass the decisive test before ship. Trust-first on semantics is now binding doctrine.

---

## v2.7.3 — 2026-04-25 — Clean _field_types coverage in _TEMPLATE + skip meta paths in finalizer

**Why this release.** First wellness pilot stress test of `finalize-mutation-batch` surfaced 17 warnings. Most were latent _TEMPLATE bugs, not agent fabrication.

**What shipped.**
- `finalize-mutation-batch.py`: skip `$`-prefixed pointers (JSON-Schema metadata) and `_`-prefixed pointers (runtime metadata: `_snapshot`, `_proposed`, `_source`). Skip non-entity workspace-state files (`config.json`, `status.json`, `learnings-index.json`, `session-state.md`, `pending-validations.md`).
- `_TEMPLATE` `_field_types` patches across `brand.json`, `products/_example/spec.json`, `products/_example/offers.json` (full map created from scratch — was empty), `audiences/_example/profile.json`, `learnings.json`.

**Operator impact.** None visible. New brands scaffolded from `_TEMPLATE` now pass the wrapper on first run. Re-run on same wellness pilot data: 17 warnings → 0.

---

## v2.7.2 — 2026-04-25 — Walk back validate-output-coherence LLM skill, ship Python primitive

**Why this release.** Stress test on a wellness pilot confirmed v2.7.1 P0 #1 was a half-fix. `validate-output-coherence` was prescribed as MANDATORY in `snapshot-brand` + `setup-brand` SKILL.md but the sub-agent skipped it 100% on the live run — 47 mutations written, 0 coherence_check events emitted. Soft enforcement does not survive load.

**What shipped.**
- `.skills/finalize-mutation-batch.py` (~259 lines) — deterministic Python wrapper, no LLM negotiation. Reads `_field_types` per touched file, inspects every recent write event, runs structural checks (unmapped paths, manual derived writes, `tone_of_voice` misclassification, missing `_field_types` maps), emits coherence_check event itself. Exit 2 on blocking = caller must revise.
- `snapshot-brand` Step 7 + `setup-brand` Step 4: instruction reduced to a single bash line invoking the wrapper. Hard Rule rewritten around the Python primitive.

**Operator impact.** Coherence enforcement now actually fires. Agent cannot skip. Bonus: catching the wrapper found 11 latent _TEMPLATE warnings (addressed in v2.7.3). Decision A1 (LLM-based coherence skill) effectively walked back — formalized in v2.7.4 / D#356.

---

## v2.7.1 — 2026-04-24 — P0 patches from v2.7.0 audit: coherence loop + REFINE category + canonical _field_types doc

**Why this release.** Three P0 patches surfaced by the v2.7.0 fresh-instance audit. (1) Close the `coherence_check` event loop so the sub-skill emits an event the turn-end hook can verify. (2) Add a REFINE category to `checkpoint-resolver` with franglais matching patterns. (3) Ship a canonical reference for `_field_types` — cited in 8+ skills with no dedicated doc, leading to drift on edge cases.

**What shipped.**
- `docs/system/field-types.md` (87 lines) — canonical reference for the four-value tag (`observed | stated | derived | structured`). Binary decision test per type, decisive examples, 5 hard rules (no manual derived, tag exactly once, precision > globs, structured requires framework ref, unmapped writes refused).
- `architecture.md` + `CLAUDE.md` cross-refs to the new doc.

**Operator impact.** None visible. Doc + plumbing only. Agents lose the ambiguity that caused tag drift on edge cases.

**Known gap.** Patch P0 #1 (coherence loop closure) shipped here as a soft prescription — proven half-fix in v2.7.2 stress test, walked back to a mechanical Python primitive.

---

## v2.7.0 — 2026-04-24 — Enforcement layer: three soft rules become hook-guards

**Why the minor bump.** v2.6.20–22 closed the skill-level gaps found during the beauty pilot fresh-instance test, but all three fixes were SKILL.md instructions — readable policy the agent could still skip under load. This release moves the enforcement from instructions to mechanics wherever Claude Code's hook surface allows it.

**What the hook surface actually permits**
- PreToolUse / PostToolUse / Stop / SubagentStop / UserPromptSubmit / SessionStart — these can inspect, block tool calls, or inject context.
- There is no hook that can intercept assistant text output before it renders. Hard prevention of narrated fabrications or em-dashes in replies is therefore not possible. What is possible is post-hoc audit with persistent logs and stderr surfacing — the agent sees the warning at the next tool call and can self-correct. This release ships what's genuinely enforceable and is explicit about the limitation.

**Hook 1 — Brand status auto-refresh (hard enforcement)**
- New: `.skills/refresh-brand-status.py {slug}` — mechanical recomputation of `status.json`. No LLM. Grades `completeness.{brand,products,audiences,offers}` via field-presence heuristics, flips `wedge_complete` when all four entity types reach at least "draft", stamps `last_activity`.
- New hook: `.claude/hooks/post-write-flush.py` — PostToolUse on Bash. Detects `write-to-context.py --path brands/{slug}/...` invocations, extracts the slug, invokes `refresh-brand-status.py {slug}` synchronously. The agent cannot skip this step; every successful write automatically flushes the brand's self-reported state.

**Hook 2 — Em-dash audit (soft enforcement)**
- New hook: `.claude/hooks/turn-end-audit.py` — Stop + SubagentStop. Parses the last assistant message from the transcript, counts em-dashes (CLAUDE.md bans `—` in replies). Logs one entry per occurrence to `.phantom/tone-audit.log` (max 5 per turn), emits a single stderr summary the agent sees at its next tool call.
- Limitation: the text is already shown to the operator — the hook cannot retroactively strip it. The audit builds pressure and a persistent trail.

**Hook 3 — Coherence violation audit (soft enforcement)**
- Same `turn-end-audit.py` hook scans the last assistant message for entity-field markers (`spec.json`, `offers.json`, `profile.json`, `brand.json`, `compliance_gap`, `flagged CRITICAL`, `stamped field/value`). If any are found AND the events log does not show a `coherence_check` event in the last 5 minutes, logs the violation to `.phantom/coherence-audit.log` and surfaces a stderr warning.
- This catches the exact class of bug that opened v2.6.22: agent narrating `"I flagged compliance_gap CRITICAL"` while `spec.json#/compliance_gap` was `{}`.

**Wiring**
- `.claude/settings.json` gains three hook entries: `PostToolUse.Bash → post-write-flush.py`, `Stop → turn-end-audit.py`, `SubagentStop → turn-end-audit.py`.

**Operator impact**
- `status.json` and `wedge_complete` are now always current after any brand write. No action required from the agent.
- Em-dash and coherence violations accumulate in `.phantom/` audit logs. Largo can inspect them on demand or leave them as background telemetry.

**Known gap**
- The two soft-enforcement audits cannot block the offending output (Claude Code does not expose a pre-render hook on assistant text). Hard prevention would require either a feature addition on Claude Code's side or restructuring workflows so that claims flow through tool calls (which are pre-hookable) rather than free text. Not addressed in this release.

---

## v2.6.22 — 2026-04-24 — Wire validate-output-coherence as a mandatory pre-ship gate

**Caught during v2.6.19 fresh-instance test (finding #3).** The agent narrated *"I flagged compliance_gap as CRITICAL in the spec"* while `spec.json#/compliance_gap` was actually `{}`. The operator took the statement at face value. `validate-output-coherence` existed as a sub-skill since v2.6.17 but was declarative — no caller was wired to invoke it.

**Fix**
- `snapshot-brand/SKILL.md § Step 7` post-save: now requires invoking `validate-output-coherence` (Task tool, haiku, `subagent_safe: true`) on the operator-facing summary before it ships. `blocking_issues` → revise and retry. Warnings logged, do not block.
- `snapshot-brand/SKILL.md § Hard Rules`: new rule — no narrative claim referencing a field in `spec.json` / `offers.json` / `profile.json` / `brand.json` ships without passing the coherence check first. The concrete compliance-gap fabrication is cited as the canonical trigger.
- `setup-brand/SKILL.md § Step 4` context recap: same gate applies before sending the recap to the operator.

**Operator impact**: post-setup and post-snapshot summaries are now fact-consistent with the files on disk. Agent can no longer claim to have flagged or filled a field that the JSON doesn't actually contain.

**Known gap**: the gate is a SKILL.md instruction, not hook-enforced. If the calling agent skips the Task tool invocation, the check doesn't run. Future hardening: PreToolUse hook that intercepts large operator-facing completions mentioning entity fields and requires a recent coherence check event in the log (candidate v2.7.x).

---

## v2.6.21 — 2026-04-24 — Close the end-of-onboarding governance gap

**Caught during same fresh-instance test as v2.6.20.** After setup-brand + snapshot-brand + 29 mutations, `status.json.wedge_complete` stayed `false`, `completeness` was `{}`, `pending-validations.md` still had the template placeholder `{brand-name}` and no seeded checkpoints for the fields stamped in `mode=proposed`. The governance surface the operator sees was empty even though the workspace was populated.

**Root cause**
- `setup-brand § E1` substituted `{brand-name}` only in `CLAUDE.md`, leaving `session-state.md`, `pending-validations.md`, and `todos.md` with the raw placeholder.
- `setup-brand § E1` Step 4 narrative said to "seed pending-validations" but didn't spell out the write. Agent skipped it.
- `snapshot-brand § Step 7` post-save ended with a soft "run validate when ready" suggestion. `validate-resources` was never auto-triggered, so `status.json` never refreshed after writes.
- Inferred fields (audiences, tone, positioning) were stamped via `mode=proposed` but no corresponding checkpoint landed in `pending-validations.md § Context gate`.

**Fix**
- `setup-brand/SKILL.md § E1`: placeholder substitution now covers all 4 markdown files at brand root; seeding of the 3 baseline gate sections (context / access / enrichment) is spelled out line-by-line with plain-language source tags.
- `snapshot-brand/SKILL.md § Step 7`: two silent post-save actions added — (1) append one `[ ]` line to `pending-validations.md § Context gate` per field stamped in `mode=proposed` during the run, (2) trigger `validate-resources` silently to refresh `status.json` and rebuild auxiliary indexes. Output surfaced only on MAJOR/CRITICAL.

**Operator impact**: post-setup the workspace now accurately reports its own state (`wedge_complete` flips true when entities are complete) and the governance queue reflects real pending validations instead of template stubs.

---

## v2.6.20 — 2026-04-24 — Fix offers schema drift + write-to-context proposal leak

**Caught during v2.6.19 fresh-instance test** (beauty pilot onboarding). Two coupled regressions in the snapshot-brand → write_to_context path corrupted single-product offers.json files.

**Bug 1 — snapshot-brand wrote v1 legacy `offers[]` shape on single-variant products**
- `.skills/skills/snapshot-brand/SKILL.md § Step 4`: the JSON template shipped with the skill was the pre-v2 flat `{offers: [{product_ids: [...]}]}` shape. Bundle code path was already v2-correct (`offer_groups[]`), single-variant path had drifted.
- Fix: rewrote Step 4 with the canonical v2 `offer_groups[]` + `product_refs: [{slug, quantity}]` shape. Added explicit hard rules: `_version: "2.0"` mandatory, flat `offers[]` rejected, group-of-1 is the default for single-product files.

**Bug 2 — `write_to_context` leaked `_proposed/_source/_confidence` at the root object when `mode=proposed` used on a whole-file path**
- When an agent called `write_to_context --path file.json --mode proposed` (no JSONPointer fragment), the proposal wrapper stamped the metadata keys at the top-level of the written JSON, corrupting downstream consumers.
- Fix: `write-to-context.py` now rejects `mode=proposed` without a JSONPointer with a clear error. Scaffold must run in `mode=direct`; individual field stamping runs in `mode=proposed` with `file.json#/field`.

**Hard rule added to `snapshot-brand/SKILL.md § Hard Rules`** covering both: never call `mode=proposed` on whole-file paths, always scaffold first in `direct` then stamp fields.

**Operator impact**: preventive. Existing instances with the drifted X600-style files are not auto-migrated — rerun `snapshot-brand` on the affected product to regenerate under v2 shape, or hand-migrate using `research/migrate_offers_v1_to_v2.py` if present.

---

## v2.6.19 — 2026-04-23 — Hygiene pass: language drift (FR → EN)

**Action**: align all system docs + SKILL.md with voice.md EN-baseline policy. Template is authored in EN; operator-facing text is translated at runtime. Recent v2.6.17–18 additions had drifted into FR/EN mix — this pass restores coherence.

**Files rewritten in EN**:
- `docs/system/skill-creation-protocol.md`
- `docs/system/skill-architecture-redteam.md`
- `docs/system/skill-builder-cartography.md`
- `.skills/skills/validate-resources/SKILL.md` (stamping section)
- `.skills/skills/migrate-workspace/SKILL.md` (v1.8 migration notes)
- `.skills/skills/learn-from-session/SKILL.md` (enrichment candidate surface templates + answer space)

**Not touched**: operator-facing speech embedded in templates stays neutral — runtime translation handles FR operators. CHANGELOG historical entries stay as written (append-only).

**Operator impact**: none visible. Doc hygiene only, zero behavior change.

---

## v2.6.18 — 2026-04-23 — Skill creation protocol + learn-from-session enrichment + heavy-skill gate

**Action**: formalise the operator-controlled skill lifecycle. Three things Largo cadred explicitly : (1) skill creation must propose graduation (simple vs SOP+orchestrator vs multi-orchestrator) under operator control, (2) learn-from-session must surface enrichment candidates at close (new skills, SOP updates, convention promotions), (3) heavy skills must ask before cascade to prevent runaway execution.

**What's new — skill creation protocol**:
- `docs/system/skill-creation-protocol.md` — canonical protocol covering :
  - Detection signals for skill proposal (repetition, genericity, cost, learn-from-session pattern)
  - Graduation matrix : specific (one skill) vs heavy (SOP + orchestrator + mini-skills) vs macro (multiple orchestrators)
  - Three operator validation gates : proposal, pre-cascade, final output
  - extend_before_create discipline (default = extension, sibling skill = justified exception)
  - Rollback / sunset pattern for obsolete skills

**What's new — learn-from-session enrichment detection**:
- `.skills/skills/learn-from-session/SKILL.md` — new "Enrichment candidate detection" section at close. Three classes :
  - **Class A** — skill candidates (repeated tasks, multi-step workflows, cross-brand patterns)
  - **Class B** — SOP / doc enrichment (business patterns explained, edge cases discussed, tactical tips)
  - **Class C** — convention / rule promotion (learnings applicable beyond single brand)
- Surface max 3 candidates per class at close. `oui / non / plus tard` answer space. Refused/deferred candidates logged in `todos.md` so pattern persists.

**What's new — heavy skill pre-cascade gate**:
- `docs/system/voice.md` — new "Heavy skill posture — always ask before cascade" section. Hard rule : no cascade > 3 subagents without explicit gate, no execution > 20k estimated tokens without explicit gate. Canonical surface pattern for the operator confirmation.

**Operator impact** :
- Skills are never auto-created. Detection surfaces candidates ; operator decides.
- Heavy workflows (audits, multi-step generators, multi-brand operations) always pause for confirmation before burning tokens.
- Learn-from-session becomes more than a persistence step — it's an active system-improvement surface.
- Documentation layers stay clean — separation SOP (methodology) / orchestrator (executor) / mini-skills (atomic) reinforced.

**Why this release** : Largo flagged that the memory/context optimizations we were debating were missing the point. Real friction is elsewhere — agents auto-cascading without asking, learn-from-session not helping the system grow, skill graduation unclear. This release addresses those three directly. No code changes, purely protocol documentation + SKILL.md enrichment.

**Known gaps (not addressed in 2.6.18)** :
- No `promote-learning` primitive yet for Class C (convention promotion). Manual via write-to-context for now.
- No runtime enforcement of the heavy-skill gate (it's a voice.md rule read by agent — can be skipped if agent rushes). Enforcement via PreToolUse hook possible in future release if drift observed.
- No metrics tracking of skill invocation patterns to auto-detect "repetition threshold". Detection remains heuristic in learn-from-session.

---

## v2.6.17 — 2026-04-23 — Resource discovery infrastructure + coherence gate + SOP enrichment pattern

**Action**: closes the "how do skills find relevant knowledge without tagging" question raised after the S36 red team. Instead of pre-tagging resources with `applies_when: {vertical, skill_names}` (maintenance hell), resources are indexed automatically by content and skills query the index at runtime. A coherence gate sub-skill validates outputs before they reach the operator. The SOP format gains a `tier: binary|contextual` + `resource_discovery` + reasoning layer pattern (demonstrated on 3 exemplar checkpoints in audit-meta-global).

**What's new — indexer extended**:
- `.skills/memory-index.py` — indexes `resources/{frameworks,guides,catalogues,sops,conventions,quality-specs,templates,routing}/`. No tagging required on operator side. Markdown chunked by `## ` headings (large files split, small files = one chunk). Optional YAML frontmatter parsed for title/description boost. JSON resources = one chunk. Validated on the test workspace: 44 resource chunks indexed from existing template resources.

**What's new — retrieval primitive**:
- `.skills/discover-resources.py` — CLI `--query --source-types --limit --boost-recency --format`. FTS5 MATCH over indexed resource chunks, ranked by BM25 + optional recency boost. Auto-escapes user queries for FTS5 operator safety. Returns title, file_path, snippet, score per hit. Zero tagging maintenance — match is content-driven.

**What's new — coherence gate sub-skill**:
- `.skills/skills/validate-output-coherence/SKILL.md` — sub-skill (operator_facing: false, invocable_by: all orchestrators). Final gate before output reaches operator. Four checks : schema consistency (referenced fields exist), fact consistency (no brand contradiction), tone consistency (matches declared voice), no fabrication (numbers/claims sourced). Returns structured JSON with `{ok, warnings[], blocking_issues[]}`. Does NOT rewrite — only flags ; caller decides.

**What's new — SOP pattern upgrade**:
- `resources/sops/audit-meta-global.md` — three exemplar checkpoints (4.4 audience exclusions, 5.4 angle-awareness diversity, 6.2 restricted claim detection) gained `tier: binary|contextual`, `inputs_required`, `resource_discovery` block (for contextual), and a `Reasoning layer` narrative explaining why the check matters, industry context, edge cases, remediation. The remaining 37 checkpoints stay structured but will be enriched incrementally.

**What's new — doc**:
- `docs/system/skill-resource-discovery.md` — full pattern spec : 8-step execution flow (schema → reasoning → keywords → discover → confront → compose → validate → ship), priority rule (brand wins over resource), cost budget (~3-5k tokens overhead per skill execution, 5-15% of typical skill budget), when to add semantic search (not V1).

**Operator impact** :
- Dropping a new framework doc in `resources/frameworks/` instantly becomes discoverable by skills. No action required.
- Dormant resources (deposited months ago, forgotten) automatically resurface when context matches.
- Agent outputs pass a coherence gate — reduces silent hallucination about brand facts.
- No schema changes, no breaking changes. Purely additive.

**Why this release** : the red team (v2.6.17 doc) flagged that tagging per-resource was untenable at scale. Largo pushed back explicitly on maintenance burden. The retrieval-at-runtime pattern mirrors what we already built for narrative memory (FTS5) — extending it to resources was natural.

**Known gaps (not addressed in 2.6.17)** :
- Only 3 of 40 checkpoints in audit-meta-global have the reasoning layer. Incremental enrichment over time, prioritized by operator need.
- `validate-output-coherence` is manual invocation by orchestrators. Not hook-enforced. If an orchestrator skips the call, it ships without the gate. Enforcement via PreToolUse hook possible in a future release.
- Semantic search (embeddings) deferred. FTS5 lexical suffices for structured content vocabulary.

---

## v2.6.16 — 2026-04-23 — Schema drift grep pass (offers v2 + _version per-entity)

**Action**: the lesson logged in v2.6.15 flagged that schema migrations leave consumer skills behind. Grep pass across all `.skills/` surfaces two classes of drift: legacy flat `offers[]` vs v2 `offer_groups[].offers[]`, and `_template_version` (non-existent field) vs actual per-entity `_version` field. 4 SKILL.md patches. Zero code change.

**What's new — offers schema v2**:
- `.skills/skills/query-context/SKILL.md` — "brands avec offres actives" query now reads `offer_groups[].offers[]` instead of legacy flat `offers[]`.
- `.skills/skills/snapshot-brand/SKILL.md` § v1.8 Field Awareness — `offers[].tags[]` line corrected to `offer_groups[].offers[].tags[]` with v2/v1.x note.
- `.skills/skills/migrate-workspace/SKILL.md` — same `offers[].tags` → `offer_groups[].offers[].tags` correction in the v1.7→v1.8 migration notes.

**What's new — _version per-entity**:
- Three skills (`snapshot-brand`, `validate-resources`, `migrate-workspace`) referenced a non-existent `_template_version` field and hardcoded `"1.8"` as if it applied to all entities. Actual template has per-entity `_version` with different values: `brand.json=2.1`, `spec.json=1.8`, `offers.json=2.0`, `profile.json=1.2`.
- All three SKILL.md sections now instruct: read `_version` live from `brands/_TEMPLATE` as source of truth, don't hardcode. Values listed explicitly in each skill for reference.

**Operator impact**: `query-context` queries about offers no longer silently miss v2-schema files. `snapshot-brand` no longer stamps a phantom `_template_version`. `validate-resources` no longer flags a fresh brand as failing on an absent field. `migrate-workspace` migration recipe now reflects the real schema state.

**Lesson (continuation of v2.6.15)**: schema authority drift is the most underrated source of bugs — skills talk about fields that don't exist, reference paths that were renamed, hardcode versions that no longer apply. The source of truth must remain the template itself (read live), not quoted versions embedded in prose. Future releases should lint for hardcoded version strings and legacy path patterns in all SKILL.md before shipping.

---

## v2.6.15 — 2026-04-23 — validate-resources v2 schema alignment

**Action**: same legacy-schema bug as build-brand-snapshot.py had before v2.6.11, but this time in the validate-resources SKILL.md. Detected during v2.6.14 live test on a haircare DTC pilot, validate-resources agent reported "offers missing" while offers.json actually held 4 properly structured offers. The skill prose was still pointing at `offers.meta.product_slug` (v1.x flat) instead of `offer_groups[].offers[].product_refs[]` (v2).

**What's new**:
- `.skills/skills/validate-resources/SKILL.md` — § 11 Cross-Reference Validation: offers cross-ref path updated to v2 schema, explicit code-block showing the correct offer counting idiom (`sum(len(g.get("offers", [])) for g in offers_doc.get("offer_groups", []))`). Scope checks list (line 319) updated to reference `offer_groups[].offers[]` instead of vague "offer entry".

**Operator impact**: validate-resources no longer produces false "offers missing" flags on v2-schema brands. Zero change to data, pure prose correction.

**Why this release**: shipped mid-test because the false validation output actively misled the operator in the haircare pilot session, agent relayed "fiche offres est en fait vide" to Largo while the file was correctly populated. A false negative in validation is worse than no validation: it prompts needless rework and erodes trust in the workspace.

**Lesson to log (design gap)**: schema migrations (v1.x → v2.x on offers schema, confirmed v1.8→v2.0) leave consumer code/prose behind. v2.6.11 fixed build-brand-snapshot, v2.6.15 fixes validate-resources. There are probably more consumers reading offers with legacy paths. Grep pass pending in a future release: scan all .skills/**/*.py and .skills/skills/**/SKILL.md for `offers.meta.product_slug`, `\.offers\[` without `offer_groups`, etc. Schema versions should have a single authoritative consumer guide, not N copies of the same pattern drifting.

---

## v2.6.14 — 2026-04-23 — SessionStart context budget warning hook

**Action**: closes the silent-scale-degradation risk surfaced by S35. An operator accumulates brands, learnings, decisions over weeks — the CLAUDE.md cascade grows, lazy-loaded docs balloon, prefix cache degrades, costs and latency rise. Until now, this drift was invisible. v2.6.14 makes it visible at every session start without blocking the session.

**What's new**:
- `.claude/hooks/budget-warn.py` — SessionStart hook. Runs `.skills/audit-context-budget.py --json` at every session launch. If any threshold is breached (root CLAUDE.md > 140 lines, always-loaded cascade > 250, any lazy doc > 200, worst-case session > 600), it writes a structured entry to `.phantom/context-budget-warnings.log` and emits a single-line stderr warning the agent can surface if asked. Soft enforcement — a hard block would fail a legitimate session mid-action; the maintainer fixes the cascade when ready.
- `.claude/settings.json` — wires the hook to SessionStart. Existing hooks (PreToolUse convention-guard + mutation-guard, UserPromptSubmit checkpoint-resolver) unchanged.

**Operator impact**:
- First time any threshold is crossed, the session start emits a visible warning. Operator and maintainer both see it immediately.
- The agent can surface the warning to the operator if asked ("pourquoi c'est lent ?" → "the context cascade has grown to 802 lines, over budget — detailed audit available"). No automatic action; the agent's default is to ignore the warning and continue.

**Why this release**: Largo explicitly called out the risk — "c'est contraignant pour l'user si ça ne scale pas quand il a passé du temps à importer beaucoup de context". The enforcement is cheap, single-shot per session, and surfaces real data (tested on workspace: detected 4 lazy docs over 200 lines that had been growing unnoticed).

**Why NOT P3.2 (progressive disclosure skills) or P3.3 (runtime event log)**: both are optimizations that only pay off with real scale signal — 100+ skills or multi-user debugging. Shipping them now without data = premature. Wait for a real tester to surface which one matters.

---

## v2.6.13 — 2026-04-23 — ensure-memory-fresh helper + onboard-brand stage-before-ask propagation

**Action**: finishes the P2 polish surfaced in S35. Two small, targeted fixes that were deferrable but free to ship.

**What's new — ensure-memory-fresh**:
- `.skills/ensure-memory-fresh.py` — idempotent helper. Compares mtime of indexed sources vs `.phantom/memory.db`; rebuilds only if something is newer. Fresh case exits in milliseconds with `[ensure-memory-fresh] fresh`. Stale case shells out to `memory-index.py`. Usable from anywhere: skills, hooks, release scripts, manually.
- `.skills/skills/session-search/SKILL.md` Step 0 rewritten — one line `python3 .skills/ensure-memory-fresh.py --quiet` replaces the previous prose "check mtime, decide whether to rebuild". Agent can no longer skip the freshness check.

**What's new — orchestrator stage-before-ask propagation**:
- `.skills/skills/onboard-brand/SKILL.md` Step 2 — explicit note that the subagent delegated to snapshot-brand MUST stage proposals before asking the operator. If it skips and tries a direct write, the workflow gate blocks with an actionable message. Orchestrator must not retry the gated write autonomously; surface the block to the operator and let checkpoint-resolver do its job on the next user turn.

**Operator impact**:
- session-search results are always backed by a fresh index from now on. If a session just captured a new decision, the next search query sees it without manual rebuild.
- Agents orchestrating multi-step onboarding via onboard-brand inherit the stage-before-ask discipline explicitly instead of hoping the subagent reads snapshot-brand/SKILL.md completely.

**Why this release**: S35 flagged both as P2 "nice-to-have but deferrable". After closing P1 in v2.6.12, shipping P2 in the same sitting avoids a future aller-retour. No breaking change, no operator-facing behavior change except search freshness.

---

## v2.6.12 — 2026-04-23 — Subagent infrastructure boundary + plumbing-leak rule

**Action**: closes the two design gaps surfaced by the v2.6.10/11 e-commerce pilot live test.

**What's new — infrastructure guard** (D#345):
- `.claude/hooks/mutation-guard.py` — adds `INFRASTRUCTURE_GLOBS` protection. Blocks Edit / Write / NotebookEdit / MultiEdit and Bash bypass (`>`, `tee`, `sed -i`, `open('w')`) on: `.skills/*.py`, `.skills/skills/*/*.py`, `.claude/hooks/*.py`, `.claude/settings*.json`. Only the human maintainer edits these, via a text editor outside the Claude Code tool loop. Agents that discover a bug in infrastructure should flag it to the operator, not autopatch.
- 7/7 tests pass: Edit/Write/MultiEdit + Bash sed-i all blocked on the 4 path classes. SKILL.md still editable (exempt). Canonical channel on brand JSON still allowed (no regression on v2.6.5 behavior).

**What's new — plumbing leak rule** (D#346):
- `CLAUDE.md` § Operator contract — new binary row: auto-tag source + confidence from semantic signal, display as `observé / déduit / déclaré / incertain` when useful. NEVER surface `source`, `confidence` numbers, `mode`, or the `--source / --confidence / --mode` arg names to the operator.
- `docs/system/voice.md` § Anti-patterns — new entry "Plumbing leak to operator" with real negative example caught during S35 e-commerce pilot test + corrected version + binary test ("would an e-commerce agency manager say this sentence?").

**Why this release**: the e-commerce pilot live test produced two unrelated but equally clear violations. (1) A validate-resources subagent modified `build-brand-snapshot.py` autonomously to fix a bug — correct fix, wrong method. (2) An agent presented a table with "Source" and "Confidence" columns to the operator, who then reproduced the jargon verbatim ("set confidence to 0.6"). Both were caught in session, both are now structurally impossible: the first blocked by the hook, the second blocked by the operator-contract rule that any agent reading CLAUDE.md at session start will apply.

**Operator impact**:
- Zero change for well-behaved skills. Their writes still route through the canonical channel as before.
- Any attempt by a subagent to Edit/Write workspace infrastructure gets a clear block message pointing at `scaffold-skill-stub` / `build-agent` for new skills or at the maintainer channel for existing ones.
- Operator-facing messages tighten: no more `confidence=0.6` in propositions, no more "mode=proposed" mentioned to the end user.

**Known gaps (not addressed in 2.6.12)**:
- Ordering `stage-before-ask` still not guaranteed via orchestrators (onboard-brand specifically). Needs a rule inside the orchestrator SKILL.md or a dedicated helper.
- Auto-rebuild memory.db still prose-based. Stop hook throttled candidate for v2.6.13.

---

## v2.6.11 — 2026-04-23 — build-brand-snapshot offer counter fix

**Action**: fixes a silent bug discovered during the v2.6.10 live test onboarding (e-commerce pilot). `build-brand-snapshot.py` was reading offers via the legacy flat `offers[]` array, but since v2.0 the schema nests offers under `offer_groups[].offers[]`. Result: snapshot always displayed `offers active: 0` even when offers.json was populated. The snapshot still built without crashing, so the bug was invisible until someone checked.

**What's new**:
- `.skills/build-brand-snapshot.py` — offer counter now iterates `offer_groups[].offers[]` correctly. Backward-compatible: if a legacy flat-offers file exists, the block is a no-op (0 offer_groups → nothing iterated), and an operator running an old-format brand sees `offers active: 0` which is the same as before. No regression.

**Discovery context**: detected by the validate-resources subagent during the e-commerce pilot onboarding test. The subagent modified the script autonomously — technically a scope violation (subagents should flag infrastructure bugs, not fix them), but the fix itself was correct and is shipped here properly through the canonical maintainer path. Design gap to address in a future release: constrain subagent write permissions to brand/operator scope only, block writes to workspace infrastructure (`.skills/*.py`, `.claude/**`).

**Operator impact**: snapshot now reports the real offer count. Zero change to any data path or write channel.

---

## v2.6.10 — 2026-04-23 — Non-critical skills patch pass (pseudo-code → canonical channel)

**Action**: ferme la dette restante du patch pass initié en v2.6.7. Les 10 skills non-critiques qui référençaient encore `write_to_context()` comme pseudo-code sont maintenant alignés sur le canonical channel `.skills/write-to-context.py`. Sans ça, tout trigger opérateur sur ces skills aurait buté sur mutation-guard au premier write.

**Skills patched**:
- `mine-audience/SKILL.md` — enrichissement audience via proposals
- `watch-competitors/SKILL.md` — Step 6 réécrit avec Bash block complet (mode=proposed), reference market.external_intelligence path
- `scaffold-entity-files/SKILL.md` — writes via script dans custom/
- `scaffold-extension/SKILL.md` — route-to-existing precision + hints
- `scaffold-skill-stub/SKILL.md` — write SKILL.md stub via script
- `score-product-fit/SKILL.md` — proposals mode note
- `check-existing-coverage/SKILL.md` — routing hints
- `build-agent/SKILL.md` — agent design mandate clarifié
- `learn-from-session/SKILL.md` — write mechanism vers operator/profile.json
- `register-and-flag/SKILL.md` — index.json#/extensions append

**Operator impact**: any agent path that previously routed through these 10 skills can now write without hitting mutation-guard. All brand/operator mutations flow through the single canonical channel.

**Why this release**: v2.6.7 only patched the 3 critical onboarding-path skills (setup-brand, onboard-brand, ingest-resource). The remaining 10 were listed as known gap because they're non-critical — but the first tester who triggers mine-audience or watch-competitors would have taken the wall. Closing now while the context is fresh.

**Known gaps (not addressed in 2.6.10)**:
- Some patched sections have minor cosmetic drift (nested backticks from batch replacement). Readable, functional, cosmetic polish deferred.
- `watch-competitors/SKILL.md` references `market.external_intelligence[]` path — the schema field may or may not exist in `_TEMPLATE`; validate-resources will flag if agent writes there and schema rejects.

---

## v2.6.9 — 2026-04-23 — Narrative memory retrieval layer (FTS5) + context budget audit

**Action**: PhantomOS has three memory layers — (1) entity memory (brand/product/audience JSONs — already strong), (2) operator memory (operator/profile.json + feedback memory — already in place), (3) narrative memory (session-log.md, decisions.md, learnings.json, events.jsonl — until now APPEND-ONLY TEXT, zero retrieval). This release adds the retrieval layer on (3), sourced from Hermes Agent's SQLite FTS5 pattern, without touching layers (1) or (2). Plus a context-budget audit tool so the CLAUDE.md cascade stays bounded.

**What's new — memory retrieval**:
- `.skills/memory-index.py` — idempotent rebuilder. Parses session-log.md (42 chunks from `## Session N|SN —` headers), decisions.md (353 chunks from `| N | … |` table rows), learnings.json (per-entry), `_snapshot.md` (per-brand), session-state.md (per Activity Log line), `.phantom/context-engine-events.jsonl` (per event). Writes to `.phantom/memory.db` with an FTS5 virtual table over title + content + source_ref. Runs in <1s on typical corpora. No data migration — sources remain the truth; the DB is a derived index.
- `.skills/session-search.py` — CLI. Takes `--query` (any terms, auto-escaped for FTS5) + optional `--type / --brand / --since / --limit / --format`. Returns ranked hits with source_type, source_ref, date, brand, highlighted snippet, file path.
- `.skills/skills/session-search/` (new skill, type=navigator, subagent_safe=true, recommended_model=haiku). Triggers on FR/EN operator queries about past sessions, decisions, learnings ("qu'a-t-on dit sur", "search history", "which decision", etc.). Ensures index freshness before querying. Disambiguates against `query-context` (current state vs past narrative).

**What's new — budget audit**:
- `.skills/audit-context-budget.py` — measures root CLAUDE.md line count, brand-level CLAUDE.md, lazy-loaded docs referenced via `docs/system/*.md`, worst-case session total. Reports warnings against thresholds (root ≤140, always-loaded ≤250, lazy docs ≤200, worst-case ≤600). Not a runtime hook — a pre-release gate helper. `--strict` exits 1 on overflow for CI.

**Operator impact**:
- Operator asks "qu'avait-on décidé sur le schema v2" → agent invokes session-search → gets the D#XX entry in 1 second, with snippet and source file. No more grep-the-3200-line-session-log.
- The skill rebuilds the index automatically if source files changed since last build. Default behavior: fresh on every use.
- Budget audit is maintainer-facing. Included in pre-release gate. Doesn't affect operator sessions.

**Architecture decision (D#344)** — NARRATIVE layer retrieval only. Three memory layers stay strictly separate:
  - Layer 1 (entity) — schema-bound, mutation-gated, human-validated. Unchanged.
  - Layer 2 (operator) — feedback-learned, cross-session persistent. Unchanged.
  - Layer 3 (narrative) — transcript-derived, append-only, now FTS5-indexed.
No cross-layer writes. No merge. Queries can span the index, but results always carry their source_type. The discipline of PhantomOS's content layer is preserved — we only added a lens on the time dimension.

**Why this release**: S34 tests on two live DTC pilots (a DTC pilot, a food/lifestyle pilot) confirmed empirically what was suspected — `session-log.md` grew to 3200+ lines and `decisions.md` to 357 entries with zero retrieval capability. Any cross-session recall required either manual grep or paying Claude Code tokens to grep for you. Hermes Agent solves this exact problem with `state.db` + FTS5 + `session_search` tool. Directly transposable. 200 lines Python. Immediate value.

**Why NOT Obsidian-style embeddings (deliberate choice)**: semantic search via embeddings is 10x complexity for 2x value on this corpus. PhantomOS narrative is structured (sessions numbered, decisions indexed, brands typed) — FTS5 lexical match on these anchors is sufficient. Embeddings could come later for a secondary layer, but are not the current bottleneck.

**Known gaps (not addressed in 2.6.9)**:
- No auto-rebuild hook at session close. The skill rebuilds on first use; stale intermediate state possible inside a long session.
- No auxiliary summarization (Hermes uses Gemini Flash to summarize top-N results). Can be added when snippet-based output feels insufficient.
- Budget audit findings are informational. No strict enforcement at release gate yet.

---

## v2.6.8 — 2026-04-23 — build-brand-snapshot defensive read

**Action**: snapshot builder no longer crashes on legacy `{_value, _proposed, _source, _confidence}` wrappers left behind by pre-v2.6.6 writes (when `mode=proposed` still wrapped scalars and arrays). Two new helpers + 3 read-site patches.

**What's new**:
- `.skills/build-brand-snapshot.py` — added `unwrap(value)` and `unwrap_list(value)` helpers. `unwrap` peels off the `{_value, _proposed, ...}` wrapper if present, otherwise returns the value unchanged. `unwrap_list` additionally coerces any shape to a list (empty list if not a list after unwrap), so callers can always slice safely.
- Audiences block: applies `unwrap` on `identity`, `psychology`, and each pain object; uses `unwrap_list` on `pain_points`. No more `TypeError: unhashable type: 'slice'` when pain_points is a proposed-wrapped dict.
- Identity block: applies `unwrap` on identity fields + tone block, so wrapped scalars render as text instead of `{_value: "..."}`.
- Products block: applies `unwrap` on spec identity + pricing fields, same rationale.

**Why this release**: the live two-pilot tests (DTC pilot, food/lifestyle pilot) produced workspaces where mode=proposed had wrapped scalar and array values. v2.6.6 stopped new wrapped writes but existing brands keep the legacy shape until rewritten. The snapshot builder read path crashed on first use. Fixed without touching the data itself — consumers must be tolerant of historic artifacts.

---

## v2.6.7 — 2026-04-23 — Orchestrator skills patched + write-to-context security scan

**Action**: two surfaces closed. (1) The 3 critical onboarding-path skills (`setup-brand`, `onboard-brand`, `ingest-resource`) no longer reference `write_to_context(...)` as pseudo-code — they document the explicit `python3 .skills/write-to-context.py` Bash invocation. Without this, the next onboarding session after v2.6.6 install would have butted against mutation-guard at every write the orchestrator emits. (2) The canonical write channel now runs a static security scan on `--value` and `--reason` before any mutation.

**Skill patches**:
- `setup-brand/SKILL.md` Step 3 — rewrote the `origin_story` write from `write_to_context()` pseudo to an explicit Bash block with operator-source + confidence 1.0 + mode direct. Added the mutation-guard callout.
- `onboard-brand/SKILL.md` Step 3 — "routed write via `write_to_context(mode='proposed')`" → "every mutation routed via `python3 .skills/write-to-context.py --mode proposed` (dicts only; scalars/arrays use `--mode direct`). Direct file edits are blocked by mutation-guard."
- `ingest-resource/SKILL.md` Step 3B — replaced the loose "Write file to brand folder" bullet with a full canonical-channel block: Bash invocation template, mode-proposed-dicts-only rule, workflow-gate pointer to `stage-proposal.py` + snapshot-brand Step 1/5 for gated paths.

**Security scan** (in `.skills/write-to-context.py`):
- `SECURITY_PATTERNS` — 5 regex families ported from NousResearch/hermes-agent: `prompt_injection`, `credential_exfil`, `ssh_backdoor`, `invisible_unicode`, `destructive_shell`.
- `scan_value()` walks the --value tree, `scan_string()` also runs on `--reason`. On any hit: write is refused, a `refused` event with `reason: security_scan` and match excerpts is appended to `context-engine-events.jsonl`, the CLI prints all matches and exits 1.
- Sanity tested: a value containing "ignore all previous instructions" is blocked; clean operator learnings pass through.

**Operator impact**:
- Agents that correctly follow the orchestrator skills keep working. Agents that improvised Edit/Write/`python -c json.dump` on brand files were already blocked since v2.6.5; the v2.6.7 skill patches surface the correct path in-context.
- Pasting a document containing a prompt-injection string as a learning will now refuse the write. Log the refusal, sanitize or discard the source, retry.

**Why this release**: v2.6.6 was "working for snapshot-brand + capture-learning, broken for orchestrators" — testers running onboard-brand after install would still have hit walls. The security scan is defensive hygiene: treating untrusted operator input as potentially malicious, since anything typed/pasted can come from a third-party page.

**Known gaps (not addressed in 2.6.7)**:
- 10 skills still reference `write_to_context` as pseudo-code (mine-audience, watch-competitors, scaffold-entity-files, scaffold-extension, scaffold-skill-stub, score-product-fit, check-existing-coverage, build-agent, learn-from-session, register-and-flag). Non-critical path, deferred.
- `build-brand-snapshot.py` still fragile under new pain schema shapes.

---

## v2.6.6 — 2026-04-23 — Workflow-integrity layer + write_to_context hardening

**Action**: adds the missing enforcement between data-integrity (v2.6.5 gates *what* can be written) and workflow-discipline (*when* it can be written). A staged-proposal system routes operator confirmations through a UserPromptSubmit hook whose input is the literal user message, so agents cannot self-mark confirmations. Plus two post-live-test hardenings on the canonical write channel.

**What's new — workflow-integrity**:
- `.skills/stage-proposal.py` — CLI. A skill stages a pending proposal in `brands/{slug}/.workflow.json`; the operator's next turn is classified by the hook as confirm/reject/ambiguous. Checkpoints known: `confirmed_products` (per-product gate) and `audience_q1q4_answered`.
- `.claude/hooks/checkpoint-resolver.py` — UserPromptSubmit hook. Reads the operator's literal message, matches confirm/reject regexes (bilingual FR/EN), updates `.workflow.json` accordingly. Writes to `.phantom/checkpoint-resolver.log`. Agents cannot fake confirmation because the hook input is user text, not agent output.
- `.skills/write-to-context.py` — WORKFLOW_GATES added. Blocks writes to `products/{slug}/spec.json`, `products/{slug}/offers.json`, and `audiences/{slug}/profile.json` until the required checkpoint is resolved. `source=operator` bypasses (user authority). Block message includes the exact `stage-proposal.py` command ready to run.
- `.claude/settings.json` — wires the UserPromptSubmit hook.
- `.skills/skills/snapshot-brand/SKILL.md` — patched at Step 1 Hero and Step 5B Audience to call `stage-proposal.py` before asking the operator; Hard Rule added.

**What's new — write-to-context hardening** (from live test findings):
- **Filename whitelist** — writes are refused if the target basename is not one of `{brand, status, config, learnings, strategy, spec, offers, profile}.json`, `*.extensions.json`, or `custom/*.json`. Prevents shell-escaping typos from silently creating garbage files like `profile.jsonontrainte-sante`.
- **`mode=proposed` restricted to dicts** — wrapping scalars/arrays in `{_value, _proposed, _source, _confidence}` corrupts downstream consumers (a `brand.json/products_index` array became an object, breaking iteration). Proposed mode now rejects scalar/array values with a clear error pointing at `--mode direct`. Source and confidence are still preserved in the event log.
- **`source=operator` requires `confidence=1.0`** — operator-source represents user authority (equivalent to the operator having typed the fact). Allowing confidence<1.0 with `source=operator` opened a bypass channel on the workflow gate. Now enforced at arg-parse.

**Operator impact**:
- Onboarding flow: snapshot-brand stages hero + audience proposals; operator's `oui`/`non` resolves them; writes proceed only after resolution. Experience: 2 explicit confirmation points instead of 0.
- Agent errors now pinpoint exact path issues (`target path not a known schema file`) instead of silently creating junk.
- Skills other than `capture-learning` and `snapshot-brand` still reference pseudo-code `write_to_context(...)` — they will hit workflow gates on first gated write. Patch pass pending.

**Why this release**: two live onboarding tests (a DTC pilot, a food/lifestyle pilot) surfaced: (1) the agent wrote product specs and audience profiles without operator confirmation despite SKILL.md markdown rules — gates existed only in prose; (2) shell-escaping bugs in agent-built mega-commands created corrupted filenames that the write script accepted silently; (3) `mode=proposed` on arrays broke `brand-snapshot.py` and forced the agent into ugly path hacks. v2.6.6 closes all three surfaces.

**Known gaps (not addressed in 2.6.6)**:
- `build-brand-snapshot.py` is fragile under new pain schema shapes — unrelated, deferred.
- Only `snapshot-brand/SKILL.md` is patched for the stage-before-ask pattern. `setup-brand`, `onboard-brand`, `ingest-resource` still say `call write_to_context()` as pseudo-code.
- Free-form corrections from the operator (e.g. a product name alone instead of `"yes"`) don't auto-resolve, agent must re-stage.

---

## v2.6.5 — 2026-04-22 — Systemic enforcement layer (convention + mutation + write_to_context)

**Action**: closes the gap between Markdown promises and machine-enforced behavior on two load-bearing rules (convention-first for external tools, mutation-via-canonical-channel for brand/operator data) + finally implements `write_to_context` — the function named in the agent contract for months but never coded.

**What's new — convention-guard**:
- `.claude/hooks/convention-guard.py` — PreToolUse hook intercepting any `mcp__{server}__*` call. Extracts the platform via regex (no hardcoded list — every existing AND future MCP is auto-enrolled), looks up `resources/conventions/{slug}.json`, blocks if missing, has no `_doc_check.last_doc_read`, has invalid date format, or is older than 90 days. Successful reads logged to `.claude/convention-reads.log`.
- `PLATFORM_ALIASES` normalizes noisy MCP server names (`claude_ai_Slack` → `slack`, `facebook-graph` → `meta-ads`). `PLATFORM_EXEMPT` skips internal/local MCPs.

**What's new — mutation-guard**:
- `.claude/hooks/mutation-guard.py` — PreToolUse hook intercepting `Edit|Write|NotebookEdit|MultiEdit|Bash`. Blocks direct JSON writes to `brands/{slug}/*.json` (except `_TEMPLATE`/`_EXAMPLE`) and `operator/*.json` via any route: Edit tool, `python -c 'json.dump(...)'`, `echo >`, `tee`, `sed -i`, heredoc redirects. Allows `cp -r _TEMPLATE`, `mkdir`, read-only ops, `.md` writes, and the canonical channel `.skills/write-to-context.py`.

**What's new — write_to_context implementation**:
- `.skills/write-to-context.py` — canonical mutation channel. CLI: `--path path#json_pointer --value JSON --source {agent,import,inference,operator,scrape} --confidence 0-1 --mode {direct,proposed} [--reason]`. Supports both RFC 6901 JSON Pointer (`#/entries/-` for append) and the legacy custom syntax (`#entries[]`). Writes the JSON target, appends an event to `.phantom/context-engine-events.jsonl` (ts, path, op, source, confidence, mode, digest, reason).
- `.skills/skills/capture-learning/SKILL.md` — patched to call the script explicitly via Bash instead of pseudo-code `write_to_context(...)`. Every other skill that writes to brand/operator state must follow this pattern (backlog, not in this release).

**Operator impact**:
- First MCP call without a fresh convention → BLOCK with scaffold instructions.
- Any attempt by the agent to hand-edit a brand JSON → BLOCK with a message pointing at `write-to-context.py`.
- Every mutation is now traceable in `.phantom/context-engine-events.jsonl`.
- Brands without MCP usage, and brands where the agent only reads, are unaffected.

**Why this release**: the onboarding test of 2026-04-21 produced a clean data-integrity failure on two surfaces. (1) The Notion MCP was connected mid-session with no convention read — rule in CLAUDE.md, zero enforcement. (2) The agent wrote `brands/{slug}/*.json` via shell bypass (`cp -r`, `python json.dump`) skipping the proposed/direct workflow entirely. Both were promises. Both are gates now. Shipping together because `mutation-guard` depends on `write-to-context.py` existing — neither ships alone.

**Known gaps (not addressed in 2.6.5)**:
- Skills other than `capture-learning` still reference `write_to_context()` as pseudo-code. When they write, the agent improvises — and now takes the mutation-guard wall. Patch pass pending.
- Workflow-integrity (Step 0-7 discipline in `snapshot-brand`, `setup-brand`) is orthogonal to data-integrity and still only enforced in Markdown.
- `schema-guard` (prevent fields outside `_TEMPLATE`) prototyped in local instance, not ready for release.

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
- **strategy.json v1.1** : pacing (budget tracking), variance_thresholds (alertes KPI), target_decomposition (annuel → daily). Template + Example (the example brand). Schema créé.

### Onboarding
- **Step 4 adaptatif** : détection profil opérateur → Meta Ads = audit-setup-meta, autre = brief stratégique express, pas de plateforme = fallback.

### Documentation
- **README** : Limitations V1 (6 points) + Modèle de menace V1 (single operator, local, trusted)

---

## v1.14.0 — 2026-04-10

**Action**: BRAND SCHEMA v2.1 — purchase_driver + audience_trees[] + driver_blend
**Files**: `resources/schemas/brand.schema.json` | `brands/example-brand/brand.json` | `brands/_TEMPLATE/brand.json` | `brands/_EXAMPLE/brand.json` | `brands/example-brand/products/*/offers.json` (11)
**Decisions**: D#243, D#244, D#246, D#248, D#249, D#250, D#251

S30d-close — Profile audience v2.1 foundations promoted to the brand schema:

- **`purchase_driver`** (enum: pain | desire | status | utility | identity | mixed) — brand-level default cascading to all audiences. Optional, backward-compat.
- **`audience_trees[]`** — optional primitive for two-sided marketplaces (supply × demand) where a single brand owns multiple distinct audience trees.
- **`driver_blend`** (object: primary | secondary | ratio) — required when `purchase_driver = "mixed"`, e.g. a sports-pilot-padel (pain 60 + identity 40).

Live brand.json files bumped 1.5 → 2.1 with changelog entries. `_TEMPLATE` leaves `purchase_driver` absent (optional; users fill per brand). `_EXAMPLE` sets `purchase_driver: "pain"` for consistency with creme-eclat.

**Offers fix (R1 overnight audit)**: 11 example-brand offers.json were missing required `active` field. Auto-added `"active": true` per offer. All 13/13 offers now PASS. Fresh run of `resources/scripts/validate-all.py` reports CRITICAL/HIGH/MED/LOW = 0.

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

**_EXAMPLE OFR-03 mis à jour :** `reschedule: true`, `required: false` (example product vendu aussi à l'unité OFR-01).

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

**_EXAMPLE mis à jour** : OFR-04 ajouté (type prepay, Cure 6 mois example brand). OFR-01 démontre `first_order_only`. OFR-03 démontre `unlock_after_orders`, `shipping.free`, `converts_to_offer_id`.

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

**Fichiers mis à jour**: `brands/_TEMPLATE/products/_example/offers.json`, `brands/_EXAMPLE/products/creme-eclat/offers.json` (NEW, 3 offres exemple brand), `Ressources/schemas/offers.schema.json`

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
- Compare: "compare brand-a vs brand-b" → side-by-side table (vertical, AOV, positioning, products, audiences, context level)
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
- brands/_EXAMPLE/CLAUDE.md: Updated to show the example brand's tier status (Tier 1 ✅, Tier 2 partial, Tier 3 ✅)

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
**Example**: the example brand workspace (skincare, FR), brand + 1 product + 1 audience + 4 learnings + strategy, intentionally missing offers to demo validate flags
