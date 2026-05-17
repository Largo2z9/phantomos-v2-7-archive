# Agent Contracts

> Files named `CLAUDE.md` are auto-injected into the system prompt on every session. This document is the full specification, types, loading mechanism, precedence, write discipline, lifecycle, size policy.

---

**Terminology.** Files named `CLAUDE.md` are **Agent Contracts**: permanent behavioral rules auto-injected by the Claude Code harness every session. They are NOT memory. The filename `CLAUDE.md` is imposed by the harness and cannot be renamed · only the conceptual naming in documentation uses "Agent Contract".

### Contract vs Memory vs Data vs Reference (disambiguation)

| Artifact | Nature | Loaded how ? | Written by | Lifecycle |
|---|---|---|---|---|
| **Agent Contract** (`CLAUDE.md`) | Permanent behavioral rules | Auto-injected in system prompt at session start | Operator + curated commits (via `write_to_context`) | Stable, edited rarely |
| **Memory** (`memory/*.md` + `MEMORY.md` index) | Cross-session souvenirs (user, feedback, project, reference) | Auto-loaded by harness memory system (index always in, entries on relevance) | Agent during conversation | Additive, evolves continuously |
| **Data** (`brand.json`, `profile.json`, Context DB) | Facts, state, structured brand knowledge | On-demand via skills (query-context, Read) | Skills (ingest, setup-brand, write_to_context) | Mutated on events |
| **Reference doc** (`docs/system/architecture.md`, `patterns.md`) | Deep technique, rationale, taxonomies | On-demand (agent reads when pointer hit) | Curated commits only | Stable, versioned |

Rule: if the agent needs it **every session** regardless of task → Contract. If it's a **fact about the operator/the brand/project state** → Memory or Data. If it's **"how we do X"** technique consulted occasionally → Reference.

### Contract types (taxonomy)

- **Root Agent Contract** · `workspace-template/CLAUDE.md`. Rules that apply to ALL brands / ALL sessions. Workspace-wide.
- **Brand Agent Contract** · `brands/{slug}/CLAUDE.md`. Rules scoped to one brand (ton override, client constraints, plateformes actives, scope opérateur).
- **Template Agent Contract** · `brands/_TEMPLATE/CLAUDE.md`. Never loaded. Cloned by `setup-brand` when provisioning a new brand. Contains placeholders `[À REMPLIR]`.

### Loading mechanism

- **Trigger**: Claude Code harness scans `cwd` at session start and resolves all `CLAUDE.md` up the tree.
- **Injection point**: concatenated into the **system prompt** (not user message) · invisible to the conversation but steers every response.
- **Hierarchy resolution**: workspace root CLAUDE.md loads always; a brand CLAUDE.md loads when cwd sits inside `brands/{slug}/`.
- **TTL**: session lifetime only. No cross-session caching beyond the standard Anthropic prompt cache (5 min TTL).
- **Context cost**: every byte consumes context window on every turn. Oversized contracts degrade long-session performance before any work is done.
- **Not reloaded mid-session** unless the operator restarts or `cd`s into a new scope.

### Precedence model (conflict resolution)

- **Proximity rule**: the contract closest to `cwd` wins for contextual behavioral rules (ton, posture, scope, client constraints).
- **Non-overridable root rules** (structural invariants, regardless of brand): mutation via `write_to_context`, access gates, anti-emoji, Build → Execute gates, Smart suggests a/b/c/d format, Operator contract DO/NEVER table.
- **Overridable root rules** (contextual defaults): ton baseline (chairman provocative) overridable by brand if client requires; language default overridable per brand; skill routing hints overridable if brand ships custom skills.
- **Conflict = design smell**: a rule that genuinely conflicts across levels usually means it's placed at the wrong level. Move up or down rather than patching an override.

### Write discipline (anti-drift)

Every edit to an Agent Contract YOU MUST respect:

1. **Dense prompting**, magic keywords CAPS (`CRITICAL`, `YOU MUST`, `NEVER`, `ALWAYS`, `MANDATORY`) only on load-bearing rules. Zero narration, zero "why" prose (why lives in this reference doc).
2. **ENRICH > CREATE**, before adding a section, check if an existing one covers ≥ 30% of the scope. If yes, enrich.
3. **Pointer > duplication**, if the info exists in a skill, schema, or reference section, point (`→ docs/system/architecture.md § X`), do not copy.
4. **Tables > bullets > prose**, for any enumerative rule (DO/NEVER, gates, entity mapping).
5. **Primacy / recency placement**, critical rules at the start OR end, never buried middle (lost-in-the-middle). Lookup-style routing (skills catalogue, refs) goes last.
6. **Zero internal jargon exposed**, terms like "convention", "framework", "SOP", "quality-spec" exist for the dev layer, not for operator-facing rules the agent will paraphrase.

### Lifecycle

- **Creation**: `setup-brand` clones `brands/_TEMPLATE/CLAUDE.md` → `brands/{slug}/CLAUDE.md` and fills placeholders from the setup interview.
- **Mutation**: through `write_to_context` gate (validates structure, budget, `Why:` capture). Direct `Edit` on a Contract by the agent is discouraged outside of a `write_to_context` flow · operator edits allowed.
- **Audit**: `learn-from-session` batch flush measures size + flags overflow. No auto-split.
- **Deprecation**: every section must carry a `> Why: {dated reason}` line. Absence or staleness of `Why:` triggers operator review.

### Size Policy

**Budget**: Root Agent Contract ≤ 20KB / 220 lines. Brand Agent Contract ≤ 8KB / 100 lines.

**Rationale**: Agent Contracts are auto-loaded every session. Every KB counts in the context window. Over the threshold, the agent loads noise for nothing every turn.

**Mechanism · minimal check.** The `learn-from-session` skill measures the size of the root Agent Contract (and the active brand Agent Contract) on every batch flush. If a file exceeds its budget, the agent adds a line in its final recap: *"Agent Contract at 235 lines, manual review recommended."* No subagent. No auto-split. No classification tags. Just a flag for the operator (or Phantom in a maintenance session) to arbitrate.

**Pre-write guardrail.** Before adding or modifying a section in any Agent Contract, the agent applies the **cascaded addition test**:

> *Does this rule apply to ALL brands / ALL sessions?*
> - Yes → Root Agent Contract (with size impact check)
> - No, brand-specific → Brand Agent Contract (`brands/{slug}/CLAUDE.md`)
> - No, methodology of a skill → `.skills/skills/{name}/SKILL.md`
> - No, rarely-consulted technical pattern → `docs/system/architecture.md`
> - No, contextual onboarding example → `WELCOME.md`
> - No, platform convention → `resources/conventions/{platform}.json`

The test prevents drift: every new rule is placed at the right level at write time, not retroactively cleaned.

**Per-block `Why:` capture** (being generalized). Each Agent Contract section should open with a line *"> Why: {concrete, dated reason}"*. Without the why, it's impossible to judge if a block is obsolete. Added progressively to new patches and to sections whose raison d'être is ambiguous.

**Typical externalization candidates** when an Agent Contract overflows:
- Technical patterns (connectivity, routing conventions, session relay) → `docs/system/patterns.md` (`architecture.md` / `patterns.md`)
- Contextual onboarding examples → `WELCOME.md`
- Brand-specific rules → Brand Agent Contract
- Skill methodology → its `SKILL.md`

**What must stay in the Root Agent Contract**:
- FIRST ACTION (session start logic)
- How You Operate (posture + plain-language rules)
- Build → Execute gates (active permanent rules)
- Skills table (routing to .skills/)
- Smart suggests format a/b/c/d (chairman format)
- Immediate pedagogy + OS tips (permanent UX rules)

---

