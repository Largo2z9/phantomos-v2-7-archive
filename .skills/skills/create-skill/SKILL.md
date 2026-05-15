---
name: create-skill
version: "1.0.0"
type: builder
recommended_model: sonnet
subagent_safe: false
isolation_scope: workspace_global
layer: meta
description: >
  Meta-skill, generates SKILL.md files conformant to the workspace authoring discipline.
  Knows frontmatter triad (name, type, triggers), DRGFP prerequisites schema, isolation_scope rules,
  hard rules pattern, scenario routing, framework cross-ref, subagent delegation contracts.
  Produces dense, multi-phase skills aligned with `docs/system/skill-authoring-discipline.md`.
  Workspace_global because this skill writes to `.skills/skills/` directory, infrastructure surface.
  FR: "crée un skill" "génère un skill" "nouveau skill" "scaffold skill" "skill creator".
  EN: "create skill" "generate skill" "new skill" "scaffold skill" "skill creator".
argument-hint: "[skill-name] [objective in 1-2 sentences]"
allowed-tools: Read, Write, Glob, Grep, AskUserQuestion, Skill
disambiguates_against:
  correct-skill: "create-skill creates a new SKILL.md from scratch. correct-skill patches an existing SKILL.md with a Hard Rule learned from operator correction."
  scope: "scope maps the parameters of a domain or system (read-only cartography). create-skill generates the final SKILL.md. Pattern, create-skill may invoke scope in Phase 0 if the topic is domain-specific."
  build-agent: "build-agent constructs a runtime agent (multi-skill assembly + brand binding). create-skill authors a single skill spec file."
permissions:
  reads: [".skills/", "resources/", "docs/"]
  writes: [".skills/skills/{name}/SKILL.md"]
  mode: direct
  subagent_safe: false
pipeline:
  preconditions:
    - "operator names the target skill"
    - "operator states the objective"
  postconditions:
    - "SKILL.md written at `.skills/skills/{name}/SKILL.md`"
    - "frontmatter passes PyYAML strict parse"
    - "manifest regenerated via `python3 .skills/build-manifest.py`"
prerequisites:
  - field: .skills/_manifest.json
    level: L1
    auto_pull: read_existing_manifest
    freshness_ttl_days: 7
  - field: docs/system/skill-authoring-discipline.md
    level: L1
    auto_pull: read_canon_doctrine
    freshness_ttl_days: 365
  - field: resources/schemas/skill-prerequisites.schema.json
    level: L1
    auto_pull: read_schema_canon
    freshness_ttl_days: 365
  - field: skill.target_name
    level: L2
    options:
      - operator_provided
      - inferred_from_objective
  - field: skill.scope_cartography
    level: L3
    fallback: skip_scope_proceed_phase_1
    confidence_default: 0.6
---

# Skill Creator, Meta-Skill

Generates a `SKILL.md` file that conforms to the workspace authoring discipline. The output is a runtime artifact, not a draft, the manifest builder must parse it without warnings on first build.

## Hard Rules

### Step 0bis, Prerequisite check (DRGFP v2.38)

Before collecting specs (Phase 1), scan prerequisites:

1. Read `.skills/_manifest.json` to know what skills already exist. If a sibling with the same intent already exists, refuse and propose `correct-skill` or extension instead (extend_before_create discipline, cross-ref `docs/system/skill-creation-protocol.md`).
2. Read `docs/system/skill-authoring-discipline.md` to align type taxonomy, frontmatter triad, composition contracts, lifecycle.
3. Read `resources/schemas/skill-prerequisites.schema.json` for the prerequisites contract (L1/L2/L3 fields, required keys per level).
4. Confirm `skill.target_name` with operator if ambiguous (L2 gate, 2 options: operator_provided or inferred_from_objective).
5. Optional, propose `scope` cartography (L3 fallback if operator skips, proceed direct to Phase 1).

Output a state map of inputs available plus `confidence_chain[]` init.

Cross-ref doctrine, `docs/system/dependency-resolution-protocol.md`.

### Step 0ter, Scope domaine, proposed if relevant

Before collecting specs, evaluate semantically if the requested skill targets a non-trivial domain where the operator would benefit from upstream cartography.

#### Detection heuristic (model judgement, not hardcoded list)

Does the requested skill target:
- A business domain with established frameworks the operator does not master frontally (PMAX, multi-touch attribution, CRO methodology) ?
- A technical system with blind parameters (an agent that consumes a specific API, a pipeline with multi-dep) ?
- An operational workflow with industry-known edge cases (audit setup, conversion tracking) ?

If YES on at least one dimension, propose scope.
If NO (meta-skill, extension of an existing skill, simple wrapper, purely technical automation), skip Step 0ter, jump to Phase 1.

#### Proposition (AskUserQuestion)

Required format:

```
question: "Before generating the SKILL.md for {name}, run scope on the {inferred topic} domain ?"
options:
  - "Yes, scope LEARN first (Recommended)" for skills where the operator learns while building
  - "Yes, scope BUILD first" for skills where the technical envelope matters
  - "No, I already have the mental map" skip Step 0ter, go Phase 1
  - "No, it's a meta-skill or wrapper" skip Step 0ter, go Phase 1
```

Default reco, LEARN if topic is business domain, BUILD if topic is a system with clear inputs/outputs.

#### If operator validates scope

Invoke `scope` via Skill tool, args `"{topic} --{learn|build} --for-skill={name}"`. The `--for-skill` flag adapts the cartography to the skill case, skip architecture axis, add SKILL.md convention axis, terminate on "next decisions for the skill".

At the end of scope, consume the produced map as enriched input for Phase 1, mapped axes become frameworks to reference, hard rules to encode, fail modes to document.

#### If operator skips

Start Phase 1 directly. No insisting.

## Phase 1, Collect specs

From `$ARGUMENTS` or the conversation, extract:

| Info | Required | Example |
|---|---|---|
| Skill name | Required | `routine-perf` |
| Objective (1-2 sentences) | Required | "Daily/weekly anomaly detection on Meta accounts" |
| Invocation trigger | Recommended | "routine weekly check" |
| Tools required | Recommended | Read, Bash, Glob, Grep |
| Workspace files to reference | Recommended | `resources/canon/`, `brands/{slug}/`, `docs/system/` |
| Workflow type | Recommended | execution, analysis, routing |
| Auto or manual invocation ? | Optional | `disable-model-invocation: true` if manual only |
| Target `isolation_scope` | Recommended | brand_only, cross_brand_with_gate, workspace_global |

If info missing, ask. Do not invent.

## Phase 2, Detect skill type and apply the right pattern

| Type | Pattern | Reference |
|---|---|---|
| **Execution** | Scenario routing, inputs table, execute (MCP/tools), verification | producer skill examples |
| **Analysis** | Identity, data access, protocol (steps), frameworks table, output format, hard rules | curator skill examples |
| **Routing** | Input classification, intent detection, route dispatch, sub-workflow delegation | orchestrator pattern |
| **Workflow** | Prereq, sequential phases, validation checkpoints, output structure | hybrid pattern |

Cross-ref the typology canon, `docs/system/skill-authoring-discipline.md § Type taxonomy`.

## Phase 3, Generate the SKILL.md

### Required structure

```yaml
---
name: lowercase-with-dashes
version: "1.0.0"
type: producer | curator | capturer | orchestrator | navigator | builder
recommended_model: sonnet | haiku | opus
subagent_safe: true | false
isolation_scope: brand_only | cross_brand_with_gate | workspace_global
description: >
  1-2 sentences. Concrete, not vague. Includes scope + what the skill produces.
  FR: "trigger phrase 1" "trigger phrase 2".
  EN: "trigger phrase 1" "trigger phrase 2".
allowed-tools: [restricted list, only what is needed]
# Optional:
# disable-model-invocation: true  if manual only
# argument-hint: "[expected format]"  if structured arguments
disambiguates_against:
  sibling-skill: "explanation of when to pick this vs sibling-skill"
prerequisites:
  - field: ...
    level: L1 | L2 | L3
    ...
---
```

### Conventions (absolute)

**Format**:
- Markdown with `##` headers for main sections
- Tables for inputs, scenarios, frameworks (never lists when a table is clearer)
- Code blocks for action chains and output examples

**Tone**:
- Plain language with technical precision (do not gloss over precision for the sake of accessibility)
- Direct, no fluff. Each line carries info.
- Imperative ("Read", "Execute", "Never"), not suggestive ("you could", "it would be nice to")

**Depth**:
- Minimum 3 substantive sections (no 20-line skill)
- Each phase or step has, objective, concrete action, expected output
- If the skill interacts with data, specify exact sources (paths, MCP tools, scripts)
- If the skill produces output, give exact format with example
- **v0.1 calibration**: simple v0.1 skill, 60-100 lines, 4-6 essential sections, 3-5 max hard rules. Reference existing canon (domain cartography, framework canon) rather than duplicate. Do not over-spec from the start, the skill evolves via `correct-skill`. Dense mode (200+ lines, 8+ sections) only if operator explicitly requests "exhaustive" or if scope `--for-skill` ran in validated exhaustive mode.

**Patterns to integrate as needed**:

1. **Hard Rules** (for skills that evolve through corrections):
```markdown
## Hard Rules

### [Domain]
- **[Rule]** [Explanation]. [Violation example to avoid].

---
*This skill evolves. When the operator corrects an error, the correction is encoded as a Hard Rule above. Rules are cumulative and permanent.*
```

2. **Scenario Routing** (multi-scenario skills):
```markdown
| Scenario | Entry point | Expected input |
|---|---|---|
| **[Scenario A]** | [Condition] | [What operator provides] |
```

3. **Framework Cross-Ref** (skills that lean on canon):
```markdown
| Framework | Location | When |
|---|---|---|
| [Name] | `[relative path in workspace]` | [Trigger condition] |
```

4. **Subagent Delegation** (for skills that delegate heavy reads):
```markdown
Delegate to `explore-codebase` (haiku subagent):
- [Heavy read task]
- Expected output, [structured format]
Main thread reasons on the synthesis, never reads raw files.
```

5. **Prerequisites block** (DRGFP v2.38+, mandatory in frontmatter):
```yaml
prerequisites:
  - field: ...
    level: L1
    auto_pull: ...
    freshness_ttl_days: 30
```
Each level has required keys (L1 requires `auto_pull` + `freshness_ttl_days`, L2 requires `options`, L3 requires `fallback` + `confidence_default`). Schema at `resources/schemas/skill-prerequisites.schema.json`.

## Phase 4, Validate

Checklist before delivery:

- [ ] YAML frontmatter complete (`name`, `type`, `description`, `allowed-tools`, `isolation_scope`)
- [ ] `name` in `lowercase-with-dashes`
- [ ] `description` concrete (not "handles stuff")
- [ ] `allowed-tools` restrictive (no "all tools")
- [ ] `isolation_scope` declared (defaults to `brand_only` if omitted, but explicit silences the warning)
- [ ] `prerequisites[]` valid against schema `resources/schemas/skill-prerequisites.schema.json`
- [ ] Cross-doc check, every prerequisite `field` in frontmatter is referenced in Step 0bis prose
- [ ] `disambiguates_against` declared if siblings exist
- [ ] Minimum 3 substantive sections
- [ ] Tables for inputs, scenarios, frameworks (no lists when table is possible)
- [ ] Output format specified with example
- [ ] Workspace paths in relative form (from workspace root)
- [ ] Direct, imperative tone
- [ ] No repetition of info already in prerequisite files (point, do not copy)

## Phase 5, Write the file

Write to `.skills/skills/{name}/SKILL.md`.

Then regenerate the manifest:
```
python3 .skills/build-manifest.py
```

Verify the new skill appears in `.skills/_manifest.json` with the correct `name`, `type`, `triggers`, and `disambiguates_against` entries. If the manifest builder warns on YAML parse, fix the frontmatter and rebuild.

If the skill is an operator that shares a base with others (media buying core, audit shared spec), add the prerequisite read of the base file in the frontmatter `prerequisites[]` plus Step 0bis prose.

## Output operator-facing

Plain language. The operator sees, "the skill {name} is ready, manifest updated, you can invoke it via {trigger phrase}". The operator never sees jargon (`frontmatter triad`, `DRGFP`, `isolation_scope`, `manifest entry`). Internal mechanics stay internal.

## No orphan output

Close with a contextual next-step proposal. After a `create-skill` completes, useful next moves are typically:
- Test the skill on a sample input
- Trigger `validate-resources` to confirm no integrity drift
- Document the skill role in the operator-facing capabilities map if it is operator-invokable

Recommend, do not menu.
