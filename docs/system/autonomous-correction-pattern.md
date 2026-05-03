# Autonomous Correction Pattern

> When a tool refuses an action, the agent diagnoses the refusal reason and self-corrects. It never asks the operator *"what should I do?"* on a refusal that contains its own diagnosis.

---

## Why this pattern exists

Friction observed across sessions : an agent attempts a write through `write_to_context`, the mutation gate refuses with an explicit error (missing `_field_types` tag, confidence above operator-only ceiling, schema enum violation, source classifier rejection). Instead of reading the error message and adjusting, the agent surfaces the failure to the operator and asks for guidance.

This is a violation of the contextual intelligence doctrine. The agent has all the information it needs to self-correct — the refusal message *is* the diagnosis. Asking the operator transforms a 5-second internal correction into a 2-minute interruption that breaks the flow and erodes trust.

Autonomous correction is the explicit pattern for handling tool refusals. It applies to every gated primitive : `write_to_context`, `mutation-guard`, `convention-guard`, `validate-resources`, `finalize-mutation-batch`, hooks PreToolUse refusals, schema enum mismatches.

---

## The protocol

When a tool, hook, or primitive refuses an action, the agent runs the following loop **silently**, without operator-facing surface, until either resolution or genuine ambiguity :

**Step 1 — Read the refusal message.**
Every gate refuses with a structured error (exit code, refusal reason, expected values). Parse the reason as primary input.

**Step 2 — Map refusal to known correction.**
Common patterns :
- *"argument --source: invalid choice"* → enum constraint, agent picked wrong value, retry with valid value from the enum
- *"confidence=1.0 is operator-only; agent writes max 0.9"* → ceiling violation, retry with 0.9
- *"_field_types required, got null"* → missing typing, infer from semantic context, add tag, retry
- *"schema enum mismatch on {field}"* → invalid value, retry with allowed enum value
- *"unmapped_path"* → path not in schema, check for path migration / extend
- *"hook refused write to brand JSON"* → direct edit attempt, route through `write_to_context`

**Step 3 — Auto-retry with corrected input.**
Apply the correction silently. The first retry is autonomous. The operator does not see the refusal nor the correction.

**Step 4 — If correction succeeds → continue the flow without surface.**
The operator never knows there was a refusal. Layer A trace records the correction for audit ; Layer B operator output is unaffected.

**Step 5 — If correction fails twice OR diagnosis is genuinely unclear → surface to operator with framed options.**
Not *"what should I do?"*. Always *"the gate refused for reason X. Two paths : either A (apply correction Y on input Z), or B (alternative interpretation). Which interpretation is correct ?"*. The operator gets to choose between concrete options, never asked to diagnose.

**Step 6 — Log the pattern.**
After 3 occurrences of the same refusal type within 7 days → flag as candidate for canon enum extension or schema patch. Pattern routes to `correct-skill` [backlog, not shipped] for permanent integration.

---

## Hard Rules

1. **Never ask "what should I do?" on a refusal that contains its own diagnosis.** Read the error, map it, retry.
2. **Never re-try with identical input.** Identical retry = identical refusal = wasted call. Always adjust before retry.
3. **Never panic-surface a single refusal.** First retry is autonomous. Surface only if retry fails or diagnosis is ambiguous.
4. **When surfacing is necessary, always frame as binary or ternary options.** Never open-ended *"how should I handle this ?"*. The operator picks between concrete paths.
5. **Always keep the refusal trace internal.** Layer A logs the refusal + correction. Operator output stays clean unless human input is genuinely required.
6. **Pattern surveillance is mandatory.** ≥3 same-type refusals within 7 days → log as `category: system_friction` learning, route to `correct-skill` [backlog, not shipped] candidate.
7. **The agent is responsible for understanding the system, not the operator.** When a hook refuses, that is information the agent must process — never delegated to the operator who is not supposed to know the gate exists.

---

## Anti-patterns

| Name | Symptom | Fix |
|---|---|---|
| **Refusal panic-surface** | Operator-facing message *"the gate refused, what should I do?"* | Self-diagnose from error message, retry with correction. Surface only if retry fails. |
| **Identical retry loop** | Tool refuses, agent retries with same input, infinite loop. | Always parse refusal → adjust input → then retry. |
| **Method-asking** | *"How should I encode this field?"* on a refusal that already names the constraint. | The error message names the constraint. Apply it. |
| **Operator as debugger** | The operator is shown internal plumbing (path errors, enum names, hook names) and asked to interpret. | Plumbing stays internal. If human input is required, translate to plain choice options. |
| **Silent failure** | Refusal swallowed, agent proceeds as if write succeeded, downstream skills consume corrupted state. | After autonomous correction loop exits, either succeed cleanly or escalate honestly — never silent ignore. |

---

## Examples

**Example 1 — Source classifier rejection**

Refusal received : *"argument --source: invalid choice: 'system' (choose from 'agent', 'import', 'inference', 'operator', 'scrape')"*.

Agent action : recognize this is the source classifier enum. The agent attempted `--source system`, which is not in the valid enum. The closest semantic match for the intended write is `--source agent`. Retry with `--source agent`. Operator never sees the refusal.

**Example 2 — Confidence ceiling violation**

Refusal received : *"confidence=1.0 is operator-only; agent writes max 0.9"*.

Agent action : recognize this is the operator-only ceiling. Retry with `--confidence 0.9`. Operator never sees the refusal.

**Example 3 — Field types missing**

Refusal received : *"mutation-guard: _field_types required on path X, got null"*.

Agent action : recognize the field is missing typing. Infer the type from semantic context : a value scraped from the brand site is `observed`, a value declared by the operator in conversation is `stated`, a value computed deterministically is `structured`, a value inferred by model reasoning is `derived`. Apply the right tag, retry write.

**Example 4 — Genuine ambiguity (rare)**

Refusal received : *"schema enum mismatch on `audience.psychographic_segment`, expected one of [A, B, C, D, E], got 'Z'"*. The agent inferred `Z` from the operator's conversational hint, but `Z` is not in the enum. The 5 enum values are not obviously synonymous with the operator's hint.

Agent action : retry would need a guess. Surface to operator with framed choice : *"For the segment label, the closest matches in the canon are A, B, or D. From what you said, 'A' fits best. Confirm or pick one of the other two ?"* — operator picks. Never ask *"how should I label this ?"*.

---

## Cross-references

- `contextual-intelligence.md § Two-tier rule` — mechanical-strict layer is exactly where this pattern applies
- `voice.md § Anti-patterns` — *"Stack-trace-as-explanation"* and *"Plumbing leak to operator"* are violated by panic-surfacing refusals
- `canonical-matrix-reasoning.md § Hard Rules` — failure mode declared per-skill should reference this pattern
- `delegation-pattern.md` — sister doctrine ; when a sub-agent hits a gate, the autonomous correction protocol applies inside the sub-agent first, surface to main only on retry failure
- Validates internal audit : *"Trou 1 — Quand un outil refuse une action, l'agent panique au lieu de se débrouiller"*

---

## Status

- **Doctrine v1.0** — operational. Mandatory for all skills consuming gated primitives.
- **First applications** : `mutation-guard` refusals, `write_to_context` enum classifier, `validate-resources` flagged outputs, hook PreToolUse refusals.
- **Future extension** : pattern detection daemon (P1 backlog) will pre-flag recurring refusal patterns before they accumulate to `correct-skill` [backlog, not shipped] threshold.
