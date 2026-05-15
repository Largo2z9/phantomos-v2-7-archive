---
name: correct-skill
version: "1.0.0"
type: builder
recommended_model: sonnet
subagent_safe: false
isolation_scope: workspace_global
layer: meta
description: >
  Encodes a correction into an existing `SKILL.md` as a permanent Hard Rule.
  Invoke when the operator flags that a skill produced an incorrect output.
  The correction is durable, applies to every future invocation of that skill, in this workspace.
  Workspace_global because this skill mutates `.skills/skills/{target}/SKILL.md`, infrastructure surface.
  FR: "corrige le skill" "patch le skill" "ce skill s'est trompé" "encode la correction" "ajoute une hard rule".
  EN: "correct the skill" "patch the skill" "this skill got it wrong" "encode the correction" "add a hard rule".
argument-hint: "[skill-name] [short description of the error]"
allowed-tools: Read, Edit, Glob
disambiguates_against:
  create-skill: "create-skill creates a new SKILL.md from scratch. correct-skill patches an existing SKILL.md with a Hard Rule learned from operator correction."
  learn-from-session: "learn-from-session captures session-wide learnings into multiple destinations. correct-skill encodes a single targeted fix into one specific SKILL.md."
  capture-learning: "capture-learning is operator-named one-off (logbook). correct-skill is structural mutation on a skill's contract."
permissions:
  reads: [".skills/skills/"]
  writes: [".skills/skills/{target}/SKILL.md"]
  mode: direct
  subagent_safe: false
pipeline:
  preconditions:
    - "target SKILL.md exists"
    - "operator describes the error or pastes the bad output"
  postconditions:
    - "Hard Rule appended or merged into target SKILL.md"
    - "rule passes the testable-binary check"
    - "no prior Hard Rule made redundant by the new one (otherwise refactor)"
prerequisites:
  - field: target_skill.path
    level: L2
    options:
      - operator_named_skill
      - inferred_from_error_output
  - field: target_skill.SKILL.md
    level: L1
    auto_pull: read_target_skill_md
    freshness_ttl_days: 1
  - field: docs/system/skill-authoring-discipline.md
    level: L1
    auto_pull: read_canon_doctrine
    freshness_ttl_days: 365
  - field: runtime.error_message
    level: L3
    fallback: ask_operator_to_paste_bad_output
    confidence_default: 0.5
---

# Correct Skill, Corrections Encoder

Patches a specific `SKILL.md` with a permanent Hard Rule learned from an operator correction. The rule is cumulative and durable, every future invocation of that skill reads it.

## Hard Rules

### Step 0bis, Prerequisite check (DRGFP v2.38)

Before editing (Step 3), scan prerequisites:

1. Resolve `target_skill.path` (L2 gate if ambiguous, 2 options, operator_named_skill or inferred_from_error_output). The path resolves to `.skills/skills/{target}/SKILL.md`.
2. Read `target_skill.SKILL.md` to understand current structure, do not break what works.
3. Read `docs/system/skill-authoring-discipline.md` for the Hard Rule format canon.
4. If the operator did not paste the bad output, L3 fallback, ask once for a concrete example, confidence 0.5 if the operator declines.

Output a state map plus `confidence_chain[]` init dependent on whether the runtime error message is available.

Cross-ref doctrine, `docs/system/dependency-resolution-protocol.md`.

## Protocol

### Step 1, Read the full context

Before editing anything:
1. Read `.skills/skills/{target-name}/SKILL.md` entirely.
2. Detect if a `## Hard Rules` section already exists.
3. Understand the existing structure, the new rule must compose with it, not break it.

### Step 2, Identify the exact error

Extract from `$ARGUMENTS` or the conversation:

| Field | Description |
|---|---|
| **Error** | What the skill did wrong (output, interpretation, behaviour). |
| **Cause** | Why it happened (incorrect assumption, mis-parsed input, missing check). |
| **Correction** | What the skill MUST do instead. |
| **Binary test** | How to verify the rule is respected before producing output. |

Do not guess. If the error is fuzzy, ask for a concrete example of the incorrect output. If the operator pastes a stack trace or runtime error, parse the diagnosis embedded in the error first (cross-ref `docs/system/autonomous-correction-pattern.md`).

### Step 3, Encode the Hard Rule

**If `## Hard Rules` section is absent**, append it at the end of the SKILL.md.
**If section exists**, add the rule in the relevant sub-domain, or create a new sub-domain.

Required format:

```markdown
## Hard Rules (learned from corrections)

### [Short domain, e.g., "Output validation", "Data interpretation"]
- **[Rule in imperative]** [Why]. [Concrete violation to avoid: e.g., "Do not display X if Y"].
```

**Compression principles**:
- 1 rule = 1 specific violation. No generalities.
- The rule must be testable, "before displaying X, verify Y" → binary.
- Include the violation example if it helps pin the exact perimeter.

### Step 4, Validate before saving

Checklist:
- [ ] The rule prevents EXACTLY the described error (not too broad, not too narrow)
- [ ] An agent reading only this rule would know what to avoid, no extra context required
- [ ] The rule lives in the right SKILL.md (not in a learnings file, not in a todo)
- [ ] The rule is not already present in another form (deduplicate, refactor if overlap detected)
- [ ] Binary test stated explicitly in the rule body

### Step 5, Persist

Use `Edit` tool to apply the change. Verify the YAML frontmatter still parses cleanly (no accidental delimiter break). Trigger `validate-resources` silently if the workspace runs an integrity daemon, flag only MAJOR or CRITICAL output to the operator.

## Output operator-facing

Plain language. The operator sees, "the rule is encoded in {skill-name}, next time the skill runs it will refuse to repeat this error". The operator never sees the markdown diff or frontmatter details. The fix is durable, that is the contract.

## No orphan output

After encoding the rule, suggest one of:
- Test the corrected skill on a fresh input to confirm the fix
- Open a learnings entry if the same error pattern shows up across multiple skills
- Re-trigger the skill on the original failed input to validate the fix end-to-end

Recommend, do not menu.

---

*This skill evolves. Each correction encodes a permanent rule. Rules are cumulative.*
