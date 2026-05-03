# SOP ↔ Skill conversion flow

> How SOPs (methodology) and skills (execution) interact, convert, and compose. Canonical rules for knowing when an imported document becomes an SOP, when an SOP spawns skills, when a skill needs an SOP, and when the operator asks to convert one to the other.

## The 4 primitives reminded

| Type | Lives in | Role | Has logic? |
|---|---|---|---|
| **Mini-skill** | `.skills/skills/{name}/SKILL.md` + optional Python script | Atomic check or action. Reusable. | Yes (execution) |
| **Orchestrator skill** | `.skills/skills/{name}/SKILL.md` | Use case entry point. Reads SOPs, calls mini-skills. | Yes (orchestration) |
| **SOP** | `resources/sops/{name}.md` | Methodology: WHAT/ORDER/SEVERITY/WHICH-SKILL. | No (description only) |
| **Doc** | `docs/` or `resources/guides/` | Reference material, concepts, best practices. | No |

SOPs are resources (knowledge). Skills are code (execution). The line is clear.

---

## The 5 common scenarios

### Scenario A — Operator imports a methodology doc that has no matching skill

**Example** : operator drags in a PDF `"Guide audit landing page - 2026.pdf"` from a client or a past workshop.

**What the system does** :

1. `ingest-resource` skill detects the content matches an SOP pattern (numbered checks, sequence, verify/pass/fail structure).
2. Proposes to the operator : *"This looks like an audit methodology. Save as `resources/sops/audit-landing-page.md` (as SOP) or `brands/{slug}/sources/` (as raw reference)?"*
3. If operator confirms SOP path : `ingest-resource` extracts frontmatter (category, scope, platforms, scenarios), rewrites body in canonical SOP format per `sop.schema.json`.
4. Registers in `index.json#/sops[]`.

**Key**: no mini-skill exists yet to execute the checks. The SOP sits as pure knowledge until someone builds skills for it or executes manually.

### Scenario B — Operator wants to turn an existing SOP into an executable skill family

**Example** : operator has `resources/sops/audit-meta-global.md` with 40 checkpoints. Wants the system to actually run them.

**What the system does** :

1. Operator invokes `build-agent` skill (orchestrator, existing).
2. `build-agent` reads the SOP, identifies each checkpoint's mini-skill reference (or lack thereof), builds a plan :
 - For each checkpoint that names a `mini-skill:` reference → check if skill exists → if not, scaffold via `scaffold-skill-stub` with the checkpoint description as input
 - Build parent orchestrator `audit-meta-global` that reads the SOP and calls each mini-skill
3. Proposes the full plan to operator (N mini-skills to create, 1 orchestrator, estimated effort).
4. Operator validates → `build-agent` executes the scaffolding.

**Key**: the SOP is the blueprint. Skills are generated FROM the SOP, not the reverse.

### Scenario C — Operator creates a skill that implements a methodology implicitly

**Example** : operator asks `"crée un skill qui audite nos audiences Meta et me dit si elles sont bien configurées"`.

**What the system does** :

1. `build-agent` asks : *"Are we creating a single mini-skill (one check) or a full methodology (multi-check SOP + orchestrator)?"*
2. If single mini-skill → scaffold directly as `check-meta-audience-setup`, documented with rationale comments.
3. If multi-check → prompt operator : *"This will be an SOP (methodology) + skills (execution). Draft the SOP first so we can review the checkpoints, then generate skills from it?"*
4. Drafts `resources/sops/audit-audiences-meta.md` first.
5. Operator reviews SOP → approves → Scenario B kicks in to generate skills.

**Key**: even when the operator thinks in terms of "a skill", the underlying methodology is extracted to an SOP if it's multi-step.

### Scenario D — Existing skill needs an SOP (retroactive methodology extraction)

**Example** : `snapshot-brand` SKILL.md currently contains both methodology AND execution logic. Operator or maintainer wants to clean the separation.

**What the system does** :

1. Operator invokes `scaffold-extension` (data-first mode) or a new `extract-sop-from-skill` helper.
2. Reads the existing SKILL.md, identifies the methodology sections (steps, decision trees, hard rules) vs execution sections (exact commands, output format).
3. Proposes splitting into :
 - `resources/sops/snapshot-brand.md` with methodology
 - `.skills/skills/snapshot-brand/SKILL.md` reduced to execution + pointer to SOP
4. Operator reviews the proposed split.

**Key**: bidirectional conversion is supported. Legacy skills that embed methodology can be refactored.

### Scenario E — Orchestrator needs to discover which SOPs are relevant

**Example** : operator says *"audit complet sur northsense"*. `audit-global` orchestrator must find all relevant SOPs.

**What the system does** :

1. Orchestrator queries `index.json#/sops[]` with filters : `category: "audit"`, `scope: "single-brand"`, `platforms: brand's platforms`.
2. Lists matching SOPs : `audit-meta-global`, `audit-shopify-global`, `audit-tracking-global`, `audit-email-global`.
3. Runs precondition checks for each SOP (access tokens, data present). Skips SOPs with unmet preconditions, flags them.
4. Iterates surviving SOPs → calls their referenced mini-skills → aggregates findings.

**Key**: SOP discovery is metadata-driven. Orchestrators don't hardcode SOP names.

---

## Decision tree — where does this piece of knowledge go?

Operator is about to save something. Apply in order :

1. **Is it a one-shot answer, not reusable?** → Don't save as resource. Paste in conversation or add to `brands/{slug}/learnings.json` if brand-specific.

2. **Is it a conceptual explanation (the "what is X")?** → `docs/` or `resources/guides/`. No execution, pure reference.

3. **Is it a step-by-step methodology (the "how to do X")?** → `resources/sops/{name}.md`. With frontmatter matching `sop.schema.json`.

4. **Is it executable logic (the "run X")?** → `.skills/skills/{name}/SKILL.md`. Atomic action or orchestration.

5. **Does it describe both methodology AND execution?** → Split. SOP gets methodology, SKILL.md gets execution. They reference each other.

6. **Is it a platform rule or convention?** → `resources/conventions/{platform}.json`.

7. **Is it a reusable format or template?** → `resources/templates/{name}/`.

---

## The "who calls who" contract

```
Operator intent
 ↓
Orchestrator skill ──reads──→ SOP (methodology)
 ↓ ↓ describes
 calls which mini-skills
 ↓ ↓
Mini-skills ──consult─→ Docs (reference)
 ↓
Output to operator / disk / report
```

Rules :

- **Orchestrator never skips the SOP** — if an SOP exists for the use case, the orchestrator reads it. No hardcoded sequences in orchestrator code.
- **SOP never calls skills directly** — the SOP describes which skill to call; the orchestrator actually calls them. SOPs are passive documents.
- **Mini-skills never read SOPs** — mini-skills are atomic. They do their job. SOPs live above their concern.
- **Mini-skills can consult docs** — for "what is a healthy audience" reference, a mini-skill can read from `docs/` or `resources/guides/`.

---

## SOP lifecycle

SOPs are living documents. Their lifecycle :

1. **Draft** (`status: draft`) — proposed but not validated. Invocable only via explicit operator opt-in.
2. **Active** (`status: active`) — default. Orchestrators may invoke freely.
3. **Revision needed** (`status: revision`) — flagged by validate-resources (stale > 180d + no reviews) or by operator. Still usable but surfaced for review.
4. **Deprecated** (`status: deprecated` + `deprecated_since` + `replaced_by`) — don't invoke. Kept for audit trail and legacy reference.

Never delete an SOP — deprecate it. Preserves traceability for decisions that relied on older methodology.

---

## Example — `audit-meta-global` end-to-end

Reference implementation of the pattern :

- **SOP** : `resources/sops/audit-meta-global.md` (40+ checkpoints in 7 layers, shipped v2.6.17)
- **Orchestrator** : `.skills/skills/audit-meta-global/SKILL.md` (to build — reads the SOP, iterates checkpoints)
- **Mini-skills** : `check-pixel-deployment`, `check-capi-deployment`, `check-event-deduplication`, etc. (40+ to build — each atomic)
- **Docs referenced** : `docs/system/skill-builder-cartography.md` (when to scaffold new entity for checkpoints that need custom data)

Build order :

1. SOP ships first (done — see `resources/sops/audit-meta-global.md`).
2. Orchestrator `audit-meta-global` scaffolded — reads SOP, manages mini-skill fallback when absent.
3. Mini-skills scaffolded incrementally — P0 checkpoints first (tracking foundations), then P1, then P2/P3.
4. Each new mini-skill registered, SOP's checkpoint updated to reference it, orchestrator automatically uses it.

This progression lets the operator get partial audits (P0-only) from day 1, even before all 40 mini-skills exist. The SOP is the planning document that makes incremental shipping rational.

---

## Cross-references

- `resources/schemas/sop.schema.json` — SOP frontmatter validation schema
- `resources/sops/audit-meta-global.md` — reference SOP
- `.skills/skills/build-agent/SKILL.md` — for SOP → skill generation (Scenario B)
- `.skills/skills/scaffold-skill-stub/SKILL.md` — for mini-skill scaffolding
- `.skills/skills/ingest-resource/SKILL.md` — for doc → SOP classification (Scenario A)
- `docs/system/skill-architecture-redteam.md` — red team findings that motivated this separation
- `docs/system/skill-builder-cartography.md` — related pattern for scaffolding entities (not skills)
- `docs/system/extending.md` — general extension doctrine
