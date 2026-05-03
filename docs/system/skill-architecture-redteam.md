# Skill architecture red team — 50-scenario synthesis

> Red team audit run through 5 independent agents on the proposed PhantomOS skill architecture (4-level taxonomy + creative library 3-layer). Goal : stress the proposal before implementation. 50 scenarios covering day-to-day agency / edge cases / cross-brand scale / diagnostic / generative production. Source of truth for the architecture decisions that follow.

> **Subsequent architecture decisions** :
> - SOPs (methodologies) live in `resources/sops/` (existing location inside the resources architecture, not a new directory)
> - Level above brands = `_workspace/` (agnostic to operator profile — agency / solo / multi-brand manager), not `_agency/`
> - Canonical separation skills (execution) vs SOPs (methodology) vs docs (reference) — see `docs/system/sop-skill-conversion.md`
> - Worked example : `resources/sops/audit-meta-global.md` (40+ checkpoints, 7 layers, expert-grade)

## Architecture under test

**4-level taxonomy** :
- Orchestrator — operator-invokable via natural language
- Domain skill — operator or orchestrator invokable
- Sub-skill — callable only by other skills, no operator-facing triggers
- Primitive — Python script, no SKILL.md

**Creative library 3 layers** :
- Layer 1 — Decomposition schema (universal, owner-agnostic)
- Layer 2 — Library instances (owner-flagged us/competitor)
- Layer 3 — Transforms / remix (swap_audience / swap_product / swap_proof)

**Proposed skills** : audit-creatives, brief-ads, competitor-creative-intel, test-matrix-generator (orchestrators) ; decompose-ad, remix-ad, import-competitor-ad (domain) ; angle-gap-detector, awareness-coverage-mapper, proof-diversity-checker, hook-pattern-classifier, fatigue-detector (sub) ; write-to-context, memory-index, build-brand-snapshot (primitives).

---

## Convergent findings (3+ agents agree)

### GAP #1 — Sub-skill rigidity (4 agents)

Day-to-day + edge cases + cross-brand + diagnostic report the same tension : several proposed "sub-skills" are in fact legitimate operator entry points. Examples :

- "Which ads are fatigued on cherico ?" → operator expects fatigue-detector direct
- "List awareness gaps" → angle-gap-detector direct
- "Which hook patterns are scaling ?" → hook-pattern-classifier direct

**Verdict** : the binary sub vs domain distinction is insufficient. Either add a sub→domain promotion criterion (e.g., ≥3 standalone invocations/month) or make every sub-skill dual-surface via an `operator_facing: true|false` flag.

### GAP #2 — Orchestration contract undefined (5 agents)

Every agent hit the same limit : the taxonomy defines the levels but not the **orchestration patterns**. Missing :

- **Fan-out** : `audit-creatives` on 5 brands in parallel — who spawns the subagents ?
- **Pipe** : `audit → brief` chaining — who passes what to the next ?
- **Batch** : `decompose-ad × 20 ads at once` — input[] contract or external loop ?
- **Aggregate** : composing N subagent outputs into a single ranked/filtered report

**Verdict** : need a documented `orchestration primitives` layer — not just "it's an orchestrator" but "how an orchestrator fans out / pipes / aggregates / batches". Otherwise every orchestrator reinvents.

### GAP #3 — Missing `_workspace/` layer (cross-brand agent, devastating)

Current architecture caps at **N=3-5 brands** before collapse. No layer above `brands/{slug}/` for :

- **Canonical registries** : creators, competitors, conventions (today duplicated per brand)
- **Shared taxonomies** : angles, hooks, awareness stages, claims, verticals (ontology drift per brand)
- **Portfolio index** : SQLite sync on core entities for cross-brand filter/compare/rank
- **Learning promotion** : mechanism to promote a local learning → workspace-level convention

**Scenarios blocked** : portfolio AOV rollup, cross-brand hook transplant, shared creator registry, bulk competitor import dedup, cross-brand angle comparison.

**Verdict** : `_workspace/` layer is **P0 blocker** for multi-brand adoption. Without it, PhantomOS = solo workspace, not workspace OS.

### GAP #4 — Structured data gaps = moat fails (generative agent, devastating)

Generative audit : **60% of outputs would be ChatGPT-equivalent** without :

- `brand_voice_axes` (sliders formal/premium/technical/friendly) instead of brand voice stored as prose
- `audience_segments` enriched (cultural codes, objections, jargon, morphology) instead of flat persona
- `offers` typed entity with stack structure instead of offers.json prose
- `proof_assets` library (reviews, studies, testimonials, referenceable) instead of loose text
- `compliance_rules` per brand (claims allowed/banned) instead of tacit convention

**Verdict** : the "zero re-briefing moat" is theoretical until these entities exist. These 5 entities are **P0 foundation** — without them the creative library produces generic output.

### GAP #5 — Events.jsonl underutilized (diagnostic agent)

Current events.jsonl = mutations to brand/operator JSON only. Missing :

- Guardrail blocks (who/what/when/why refused)
- Skill versioning (skill_version_hash, prompt_hash, input snapshot) for bug reproduction
- Daily perf snapshots per ad/offer
- Structured profile edits (actor, before/after hash, rationale, triggering_session)

**50% of operator "why" questions undiagnosable** today. No need for a `diagnose-X` skill family — this is an **indexing problem, not a reasoning problem**.

### GAP #6 — Missing query + action layer (day-to-day agent)

Architecture covers ingestion (import/decompose) and analysis (audit/detect) but **nothing for** :

- `query-creative-library` — read Layer 2 with filters (top performers, by angle, by owner)
- `recommend-creative-action` — post-analysis decision layer (cut/refresh/scale/kill)
- `compare-ads` pairwise — why ad A works vs ad B flops (cross-brand causal)

**Verdict** : without query + action layers, the operator bypasses the skills and freestyles their questions → loss of context persistence.

### GAP #7 — Layer 3 transforms orphaned (day-to-day agent)

Transforms (swap_audience / swap_product / swap_proof) = a "layer" described but **never mapped** to skill / primitive / data.

- Primitives (pure functions) ?
- Sub-skills ?
- Internal fields of `remix-ad` ?

**Verdict** : decide. Recommendation = **primitives** (pure functions), `remix-ad` = domain composing the transforms. Matches the existing write-to-context = primitive pattern.

---

## Categorical findings (1-2 agents)

### Taxonomy rigidity (edge cases)
Operators bend skills — batch mode, skip gates, conditional field selection. Fix : every skill accepts standard modifier params (`--fields`, `--skip-gate`, `--batch`, `--dry-run`).

### Introspection skills (edge cases)
"What is angle-gap-detector ?" "Why does this skill use Meta Ad Library ?" Zero queryable skill metadata. Fix : manifest schema with `description + rationale + design_decisions + prereqs`.

### Live skill modification (edge cases)
"Add a step to audit-creatives" — permanent (commit) vs one-shot (session) indistinct. Fix : `/skills edit` flow with approval gate.

### Owner-biased naming (day-to-day)
`import-competitor-ad` violates the Layer 1 "owner-agnostic" principle. Rename `import-ad(owner: us|competitor)`.

### Compliance collision (cross-brand)
Remixing an ad northsense → freshbite-foods silently ignores compliance claims (supplements ≠ food). Fix : `compliance-gate` primitive before brief output.

### Portfolio orchestrator tier missing (cross-brand)
5th level above orchestrator : `portfolio-*` skills that fan out to brand orchestrators, aggregate with stats + outlier detection. Not just "loop single-brand orchestrator N times" (context explodes linearly).

### Lifecycle pillar absent (generative)
Creative library focus on ads. **Nothing** on LP, email sequences, content calendars, media plans. Every new brand reinvents in Sheets/Notion → moat fail on retention/strategic layers.

### Dimensional rollups missing (diagnostic + generative)
decompose-ad tags dimensions (angle, hook, creator, offer_type) but **nothing aggregates** performance over time by dimension. "Which one works best ?" = manual reconstruction every time.

---

## Actionable priorities

### P0 — Blockers before shipping creative library

1. **Scaffold missing core entities** — `brand_voice_axes`, `audience_segments` enriched, `offers` typed, `proof_assets`, `compliance_rules`. Without these, moat fails. Scaffold-extension candidate × 5.
2. **Decide the sub-skill model** — explicit promotion criterion OR dual-mode `operator_facing`. Document in agent-design-guide.
3. **Orchestration contract** — separate doc defining fan-out / pipe / batch / aggregate patterns. All orchestrators reference it.
4. **Layer 3 transforms = primitives** — decision documented, no recurring debate.
5. **Rename owner-agnostic** — `import-competitor-ad` → `import-ad`, `competitor-creative-intel` → `creative-intel` with an owner filter.

### P1 — Architecture scale

6. **`_workspace/` layer** — `_workspace/taxonomies/`, `_workspace/entities/` (creators, competitors), `_workspace/portfolio/index.db`, `_workspace/conventions/`. Blocker beyond N=3 brands.
7. **Portfolio orchestrator tier** — 5th level, `portfolio-*` skills with subagent fan-out.
8. **Canonical schemas + extension** — minimal core (offer, creative, creator, mechanic) + `_extra` brand-specific field for portfolio queries.
9. **Learning promotion mechanism** — `promote-learning` skill : local brand learning → `_workspace/conventions/` versioned.
10. **Events.jsonl enrichment** — guardrail_block, skill_version_hash, perf_snapshot, profile_edit structured events.

### P2 — Observability + query/action layers

11. **Query-library skill** — read Layer 2 with filters (top, by angle, by owner, temporal).
12. **Recommend-action skill** — post-analysis decision layer (cut/refresh/scale/kill).
13. **Compare-ads pairwise skill** — causal diff between 2 ads.
14. **Dimensional rollups** — angle_stats / creator_stats / offer_type_stats materialized tables.
15. **Standard modifier params** — `--fields`, `--skip-gate`, `--batch`, `--dry-run` on all skills.

### P3 — Scope expansion (lifecycle pillar)

16. **LP decomposition** — `lp_decompositions` mirroring `ad_decompositions`.
17. **Email sequences** — `email_templates`, `email_sequences`, `customer_journeys` entities.
18. **Test matrices entity** — log hypothesis/result for feedback loop.
19. **Media plans entity** — `channel_benchmarks`, `launch_phases` templates.
20. **Client deliverables** — structured output schema + `client_profile.comms_style`.

---

## Open decisions (to resolve)

| # | Decision | Options | Preliminary recommendation |
|---|---|---|---|
| D1 | Sub-skill model | Rigid (sub invisible) / dual-mode flag / promotion criterion | Dual-mode `operator_facing: true|false` by default |
| D2 | Orchestration primitives | Ad-hoc per orchestrator / central doc + helpers / framework | Central doc `orchestration-patterns.md` + optional helpers |
| D3 | `_workspace/` layer | Skip V1 / scaffold ready V1 / later | Scaffold empty V1 structure, populate as needed |
| D4 | Layer 3 transforms | Primitives / sub-skills / internal | Primitives (pure functions) |
| D5 | Core entity additions | Ship 5 at once / incremental / per need | Incremental (brand_voice_axes first — touches all skills) |
| D6 | Portfolio orchestrator tier | New level / reuse existing orch with flag | New level `type: portfolio-orchestrator` explicit |

---

## Annex — 50 scenarios condensed

### Day-to-day (10)
Weekly creative audit → orchestrator `audit-creatives` ✓ | Brief 5 ads on sleep angle → gap `brief-writer` missing | Import 12 competitor screenshots → bulk contract to define | Compare hooks us/Kara/competitor → `snapshot-portfolio` missing | Test matrix 3×2×2 → Layer 3 transforms unclear | "Best ad this month" → `query-creative-library` missing | Prep client review → mode param internal/client | Ad works A flops B → `compare-ads` missing | Onboard new brand → rename owner-agnostic | Fatigue check → sub invocable direct missing.

### Edge cases (10)
Audit+brief hybrid → pipe contract | Cross-brand compare → fan-out primitive | Meta-query skills → introspection | Temporal recall → `recall` skill | Underspecified → Expert Relay to formalize | Batch decompose → input[] contract | Sub-skill direct invocation → `--skip-gate` | Live skill edit → `/skills edit` flow | Conditional field select → `--fields` param | Rationale introspection → `design_decisions[]` manifest.

### Cross-brand / scale (10)
Portfolio angle compare → shared taxonomies | Cross-brand hook transplant → voice adapter | Portfolio AOV rollup → `_workspace/portfolio/kpis` | Cross-brand creative transplant → compliance-gate | Bulk 50 competitor ads → `_workspace/competitors/` dedup | Portfolio health audit → `portfolio-health-scan` orchestrator | Shared creator entity → `_workspace/entities/creators/` | Learning promotion → `promote-learning` skill | Portfolio filter query → portfolio index DB | Bulk offer audit → stats + outlier detection.

### Diagnostic (10)
Ad drop investigation → `diagnose-ad-drop` orchestrator + perf_snapshot events | Temporal awareness recall → FTS5 + structured index | Schema decision history → decisions.md strict template | Angle test history → angle-performance-rollup | Guardrail block recall → events.jsonl enrichment | Remix lineage → `parent_ad_id` + `trace-lineage` | Creator hook performance → creator_id capture + rollup | GWP lifecycle → offers table structured | Snapshot bug reproduction → skill_version_hash events | Positioning audit trail → profile_edit events structured.

### Generative (10)
3 hook variants audience → `audience_segments` enriched | Full brief product×audience → `compliance_rules` | Test matrix 4×4 → `test_matrices` entity | Premium product copy → `brand_voice_axes` | Editorial calendar → `content_calendars` + `content_pillars` | UGC script from competitor → remix-ad mode `ugc-script` | Welcome email sequence → `email_sequences` entity (greenfield) | Media plan 30k€ → `media_plans` + `channel_benchmarks` | Duo LP → `lp_decompositions` + `proof_assets` | Exec summary → `client_deliverables` structured.

---

## Meta-observation

**The original creative library (ad_decompositions + remix) survives the red team, but reveals that PhantomOS v1 under-scopes the agency moat.** The real agency value requires :

- 5 missing core entities (voice axes / audiences enriched / offers typed / proof / compliance)
- `_workspace/` layer for multi-brand
- Full lifecycle pillar (LP / email / content / media plans)
- Enriched observability (diagnosable events)

Without those foundations, `audit-creatives` and `brief-ads` produce generic output. With them, PhantomOS becomes **the real agency orchestration layer** (vs "a Claude Code workspace template").
