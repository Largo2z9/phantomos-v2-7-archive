# Delegation Pattern

> When the agent delegates work to sub-agents (parallel, background, or sequential) to compress runtime, parallelize exploration, or reach synthesis without blocking the operator flow. Rules for *when* to delegate, *how* to brief, *which model* to invoke, *how* to surface, and *what* to do on failure.

---

## Why this pattern exists

Friction observed across sessions : the main agent attempts a multi-dimensional task (cross-prism audit, mass sweep, multi-source research, parallel skill chain) sequentially, in main thread, and either takes ten minutes blocking the operator or partially short-circuits to stay responsive. Both are wrong. The right move is to delegate.

The proactif posture requires the agent to autonomously decide when to fan out work to sub-agents, manage the parallelism, surface the right thing at the right time, and synthesize back into a coherent recommendation. The doctrine below codifies that decision-making so the agent does not improvise a different protocol every session.

This doctrine sits next to `autonomous-correction-pattern.md` (handling tool refusals) and `pattern-detection-triggers.md` (silent observation buffer). Together they form the runtime behavioral layer of Contextual Intelligence : self-correct, self-observe, self-delegate.

---

## When to delegate, when to do direct

The agent runs the following test before deciding.

**Delegate when** :
- Task estimated runtime exceeds 5 minutes in main thread
- Work decomposes naturally into independent dimensions (audit cross-prisms, sweep cross-files, parallel research on disjoint topics)
- A sub-skill or specialized agent has a better model match than the main thread (Haiku for mechanical sweep, Opus for deep architectural synthesis)
- The operator has signaled they want speed (chain announce + go) and the chain is predictable
- Search or exploration is needed across many files or web sources, where context budget would balloon if loaded inline
- The same logical operation must be applied across N items and can run in parallel (sweep all manifests, validate all skills, audit all docs)

**Do direct when** :
- Task takes under 2 minutes
- Sequential dependencies (output of step N feeds step N+1, no parallelism possible)
- Surgical edit on one or two lines with clear context already loaded
- Lookup of a single value or path
- The operator is mid-conversation and expects a quick turn

The 5-minute threshold is a heuristic, not a rule. The real test : *would parallelism reduce wall-clock time meaningfully, or does the work compress to roughly the same duration with delegation overhead added?*

---

## Background vs foreground

**Foreground (blocking)** when the result conditions the next operator-facing message. The agent waits for the sub-agent, then composes. Use for : single delegated task on the critical path, decision-point research, audit needed before a recommendation.

**Background (fire-and-forget with notification)** when the main agent can continue on adjacent work while the sub-agent runs. The runtime notifies the agent when the sub-agent completes ; the agent merges the result on receipt. Use for : multi-agent parallel cascades, slow sweeps, audits that complement (not block) the current operator turn.

Default to background when the agent has more than one task and the operator is not waiting on this specific result. Default to foreground when the agent has one task and the operator is on the line.

Never block the operator silently for more than 90 seconds in foreground without a heartbeat ("still on it, X seconds in"). If the foreground task is exceeding 90 seconds, convert to background and tell the operator the task is now async.

---

## Model choice per sub-agent

The model assignment is not arbitrary. It maps to the cognitive demand of the sub-task.

| Sub-agent task profile | Model | Why |
|---|---|---|
| Mechanical sweep, find-and-replace, lint, schema validation, regex pass | Haiku | Pattern matching, no reasoning load. Fast and cheap. |
| Audit, structured analysis, synthesis from one source, single-skill execution, draft generation | Sonnet | Default. Balanced reasoning and cost. |
| Multi-dimensional synthesis across heterogeneous sources, doctrine drafting, architectural arbitration, complex creative production | Opus | When reasoning is the bottleneck and the task tolerates higher cost. |

The agent picks the model based on the sub-task, not the parent task. A complex parent (e.g. cross-prism audit) may delegate to five Sonnet agents (one per prism) rather than five Opus agents, because each prism is a structured analysis on a single dimension.

If unsure, default to Sonnet. Never default to Opus for mechanical work.

---

## Surface protocol during delegation

What the operator sees while sub-agents run.

**At launch** : one short sentence announcing the plan. Number of sub-agents, scope, expected runtime if estimable. *"Je lance trois agents en parallèle (sweep noms, sweep em-dashes, audit cohérence). Synthèse à mesure."* Not a paragraph. Not a checklist. One line.

**During the run** : silence by default. The agent does not narrate the wait. The agent can continue on parallel work for the operator if any. If a single agent runs longer than expected (over 60 percent of estimate or absolute 5 minutes), surface a brief status update : *"sweep em-dashes encore en cours, retard léger, je reste dessus"*. Otherwise stay quiet.

**On each sub-agent completion** : one to two lines acknowledging the result, key finding if material, and the next step the agent is taking. Not the raw report. The synthesis. *"1/3 done, sweep noms clean (27 occurrences nettoyées). Je continue, em-dashes en cours, audit cohérence aussi."*

**At full chain completion** : a single synthesis message with the actionable output. Not a meta-summary of how it went, the actionable result. The operator should be able to act on the synthesis without reading the underlying agent reports.

**Anti-pattern** : dumping each sub-agent's full report verbatim into the operator chat. The agent main is the synthesis layer ; if the agent main just relays raw output, it has not earned its role.

---

## Limits

The agent operates within bounds that prevent runaway cost or chaos.

**Max parallel sub-agents** : five at a time. Anthropic API surface caps this practically. Beyond five, the agent queues the rest and launches as slots free up.

**Max delegation depth** : one level by default. A sub-agent does not sub-delegate to a sub-sub-agent unless the parent task explicitly authorizes a depth-2 chain. This prevents fan-out blowup.

**Cost awareness** : the agent considers token cost when picking the model and the sub-agent count. Five Opus agents on a mechanical sweep is a doctrine violation. Five Haiku agents on a complex synthesis is also wrong (the synthesis will be shallow). The model choice rule above prevents both.

**Time budget** : if a chain is taking more than 15 minutes wall-clock, the agent surfaces a checkpoint to the operator. The chain may continue, but the operator should know it is long and decide whether to interrupt or wait.

---

## Failure handling

Things go wrong. The agent has a protocol.

**Sub-agent timeout** : the runtime kills it and the agent receives a failure notification. The agent decides : retry once with the same prompt (cheap, sometimes works), retry with a different prompt (if the original was ambiguous), or abandon and surface the gap to the operator. Never silently swallow.

**Ambiguous result** : the sub-agent returns something the main agent cannot interpret cleanly. The agent does not propagate the ambiguity to the operator. It either re-prompts the sub-agent for clarification, or flags the ambiguity in the synthesis with a binary choice for the operator to resolve.

**Contradictory results across sub-agents** : two agents reach different conclusions on overlapping work. The main agent arbitrates if possible (one source is more authoritative, or one signal is stronger). If not arbitrable, surface the contradiction to the operator with the two paths as binary options. Never average or compromise into a third position the data does not support.

**Sub-agent refused or hit a hook** : same protocol as `autonomous-correction-pattern.md`. Read the refusal, map to known correction, retry once silently. Surface only if retry fails.

**Operator-side interruption** : if the operator interrupts mid-cascade with new direction, the agent stops the chain (where stoppable), summarizes what completed, and pivots. Never ignore an operator interruption to finish the chain on principle.

---

## Anti-patterns (named, banned)

| Anti-pattern | Symptom | Fix |
|---|---|---|
| **Run-away delegation** | Sub-agent sub-delegates to sub-sub-agent, costs balloon | Cap depth at 1 unless parent task explicitly authorizes depth-2 |
| **Background blackhole** | Sub-agent launched in background, never surfaced, operator forgets | Always surface on completion, even if the result is null |
| **Silence over 90 seconds in foreground** | Operator wonders if the agent crashed | Heartbeat, or convert to background and announce the switch |
| **Result dump** | Sub-agent returns 5000 words, agent main pastes verbatim | Synthesize before surfacing. The agent main is the synthesis layer. |
| **Premature delegation** | Quick task delegated unnecessarily, overhead exceeds gain | Apply the 2-minute / 5-minute test before delegating |
| **Wrong-model choice** | Opus for sweep, Haiku for synthesis | Match the model to the cognitive demand of the sub-task, not the parent task |
| **Parallel sub-agents on the same file** | Race condition, one overwrites the other | Allocate disjoint file scopes per sub-agent at briefing time |

---

## Examples

**Example 1, cross-prism audit in parallel.** Operator asks for a tone audit cross-PhantomOS. Agent identifies five orthogonal prisms (institutional posture, cross-doc coherence, neutrality, onboarding alignment, doctrine acronyms). Five Explore agents launched in parallel, each scoped to one prism, all in background. Agent main acks each completion in one line, retains the actionable. Final synthesis fuses verdicts and proposes a prioritized patch list.

**Example 2, mass sweep across files.** Need to remove confidential brand names from 200+ files. Agent spawns one general-purpose agent in background with a Python sweep brief. Agent main continues on adjacent work (writing the LICENSE, drafting CONTRIBUTING). On agent completion, verify post-sweep, commit.

**Example 3, onboarding skill chain.** Operator runs `onboard-brand`. The chain decomposes into setup-brand, snapshot-brand, ingest-resources, validate-resources. The four are sequential (each consumes the previous output), so foreground rather than background. Plan announced in one sentence, executed, synthesis at the end.

**Example 4, web research deep-dive.** Operator asks for the canonical references on a domain (CRO, retention email, B2B sales discovery). Agent identifies the domain, picks two or three canonical authors, spawns one general-purpose agent with WebFetch to extract the framework principles from public sources. Foreground if the operator is waiting on the encoded canon. Background if the encoding is part of a larger setup-extension flow.

---

## Hard rules

1. **Apply the delegation test before delegating.** Quick tasks stay in main thread. Long or parallel tasks delegate.
2. **Pick the model based on the sub-task, not the parent task.** Haiku mechanical, Sonnet analytical, Opus complex. Default Sonnet.
3. **Announce the plan in one sentence at launch.** No more, no less.
4. **Never dump raw sub-agent output to the operator.** Synthesize.
5. **Surface every sub-agent completion in one or two lines.** Never silent, never verbose.
6. **Cap parallel at five and depth at one** unless explicitly authorized otherwise.
7. **Allocate disjoint scopes per sub-agent** to avoid file race conditions.
8. **Never silently swallow a sub-agent failure.** Retry once, escalate honestly otherwise.
9. **Stop the chain on operator interruption.** Pivot to the new direction.
10. **Match cost to value.** Five Opus on a mechanical sweep is a doctrine violation.

---

## Cross-references

- `contextual-intelligence.md` : master doctrine, two-tier rule (mechanical strict, semantic trust). Delegation is part of the semantic layer trust.
- `autonomous-correction-pattern.md` : sister doctrine, what to do when a tool refuses. Used when a sub-agent hits a gate.
- `pattern-detection-triggers.md` : sister doctrine, silent observation buffer. Frictions in delegation (run-away, blackhole) are flagged here.
- `voice.md § Anti-patterns` : no orphan output, no dump, no narration of wait. Apply to surface protocol.
- `CLAUDE.md` root § Operator contract : binary line cascaded from this doctrine.

---

## Status

- **v1.0 doctrine**, operational. Co-doctrine with autonomous-correction-pattern and pattern-detection-triggers.
- **Mandatory** for any skill or orchestrator that may delegate to sub-agents (Task tool invocation).
- **First applications** : cross-prism audits, mass sweeps, onboarding chains, web research deep-dives.

---

## Amendment protocol

To amend this doctrine, follow the procedure documented in `doctrine-governance.md § Amendment` : draft the change in a research note, register a new D# entry in the project decisions log with explicit `[SUPERSEDES Dxxx]` annotation, patch the doctrine file with a changelog header, surface a re-test list of consumer skills.
