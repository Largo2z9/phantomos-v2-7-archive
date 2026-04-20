# Agent Design Guide. PhantomOS

**Status**. Permanent reference.
**Audience**. The `build-agent` skill, skill builders, advanced operators.
**TL;DR**. A good agent does one thing, does it well, and touches nothing without permission.

---

## Taxonomy and Philosophy references

Before designing any skill, read these two sections in `docs/system/architecture.md`. They are load-bearing contracts.

- **`docs/system/patterns.md § Skill Taxonomy`**. Every SKILL.md must declare a `type:` field in its frontmatter. Exactly one of six typologies. `validate-resources` refuses any skill without it (check 13b).
- **`docs/system/patterns.md § Skill Philosophy`**. Every skill embodies codified expert methodology, not improvised LLM action. A complexity gate decides when full expert dissection applies versus a light skill.

The rest of this guide is the design layer that sits on top of those two contracts.

---

## When to build an agent

Build an agent only if all 3 conditions are met.

1. **The task repeats.** If you do it once, a prompt is enough. An agent automates what comes back.
2. **Input is defined.** You know what the agent will read on each run. If input changes unpredictably each time, it is too early.
3. **Output has a stable shape.** A report, a list of proposals, a JSON file. Not "something useful".

**If even one condition is missing. Do not build. Refine first.**

---

## When NOT to build an agent

Frequent traps.

**"I want an agent that does everything."**
That does not exist. What does everything does everything poorly. Decompose into agents that do one thing each.

**"I want an agent that decides for me."**
Agents propose. The operator decides. An agent that takes irreversible decisions alone is a risk, not a tool.

**"I want an agent that updates data in real time."**
PhantomOS is not designed for real time. Agents run on demand or on cron. Freshness is managed with `status.json`, not continuous agents.

**"It is a task I do very rarely."**
A well-written prompt is faster to maintain than an agent for a monthly or one-off task.

**"Available context is insufficient."**
If the Context Engine does not yet contain the right data for the agent to be precise, building now produces noise. Enrich context first.

**"The required expert methodology is not codified."**
If a senior domain expert would apply a specific framework or matrix, and that methodology is missing from `resources/frameworks|catalogues|quality-specs|sops|conventions/`, build the methodology artifact first (via `ingest-resource` + WebFetch on authoritative sources), then build the skill that consumes it. See Skill Philosophy.

---

## The 5 properties of a good agent

### 1. Single responsibility
One agent = one responsibility. Not two. If you describe it with "and", it is probably two agents.

- Bad. "Agent that analyzes performance and generates creative briefs and updates strategy"
- Good. `analyze-perf` / `generate-brief` / `update-strategy`. Three separate, composable agents.

### 2. Declared input
The agent knows exactly what it reads before starting. No mid-run discovery.

- Bad. The agent searches for "anything that could help" in the workspace.
- Good. Step 1 of SKILL.md lists every file read and why.

### 3. Deterministic output
For the same input, the agent always produces the same kind of output (same structure, same format). Content varies, shape does not.

- Bad. "The agent produces a report or a JSON or sometimes a list depending on what it judges relevant"
- Good. "The agent always produces a markdown file with sections X, Y, Z"

### 4. Propose, never impose
By default, any agent that mutates the Context Engine writes in proposal mode (`_proposed: true`). The operator reviews and validates. Direct mutations are reserved to humans.

Single exception. An agent flagged `confidence: 1.0` and declared `human:*` may write directly. No other case.

### 5. Graceful degradation
If a source is missing, if an API does not answer, if a file does not exist yet, the agent continues with what it has and flags what is missing. It does not crash, does not block, does not hallucinate.

---

## Architecture. 1 agent or several

### Swiss knife rule

If the agent needs more than 3 distinct "expertises" to complete its task, it is several agents.

Examples.
- Read Meta metrics + compare to targets. 1 agent (`analyze-perf`).
- Read metrics + identify trends + draft creative brief + propose budget changes. 4 agents.

### When an orchestrator is needed

An orchestrator is justified if:
- Output of one agent is input to another.
- Execution order is critical.
- The operator wants to trigger the whole pipeline from a single trigger.

An orchestrator does nothing itself. It sequences only. Zero domain logic in the orchestrator.

```
Orchestrator weekly-review
  -> runs analyze-perf (output: metrics report)
  -> passes the report to generate-insights (output: actionable insights)
  -> passes the insights to propose-actions (output: proposals into the Context Engine)
```

### When one agent is enough

- Task is linear. Read then process then produce.
- No complex conditional step.
- Intermediate output has no standalone value.

---

## The contract with the Context Engine

Every agent that interacts with the Context Engine respects this contract without exception.

### What an agent may read freely
- All JSON entities (`brand.json`, `spec.json`, `profile.json`, `offers.json`, `strategy.json`, `learnings.json`)
- `status.json`, `config.json`
- Source files in `brands/{slug}/sources/` (on explicit request only)
- Past outputs in `outputs-index.json`
- Existing skills in `.skills/skills/`

### What an agent may write (with constraints)
- **Only via `write_to_context()`.** Never direct JSON write.
- Always in proposal mode (`_proposed: true`) unless explicit exception.
- Confidence between 0.0 and 0.9 for automatic agents. 1.0 is human only.
- Every mutation is logged in `context-engine-events.jsonl`. Non-negotiable.

### What an agent never touches
- `credentials.env`. Never read, never written.
- `decisions.md`. Read OK, write forbidden for agents.
- Files of other brands without explicit permission.
- The event log itself (`context-engine-events.jsonl`).

---

## Frequent anti-patterns

### The chatty agent
Agent that explains what it will do, explains what it is doing, explains what it did. Output = 80% meta, 20% value.
Fix. Clear Steps in SKILL.md. The agent produces, it does not comment.

### The agent that hallucinates context
Agent that assumes missing info ("I assume target ROAS is 3x") rather than flagging it is absent.
Fix. Explicit Hard Rule. "If [data] is missing, flag and stop this step. Never assume."

### The monolith agent
One SKILL.md of 500 lines that does everything. Impossible to maintain, impossible to reuse.
Fix. Decompose. Each agent should fit on one screen.

### The overwriting agent
An agent that writes directly in a live Context Engine field without going through `write_to_context()`.
Fix. Forbidden by D#252. Hard rule in any SKILL.md that mutates data.

### The infinite loop agent
An agent that calls the same tool with the same arguments in a loop, with no step limit and no "no-progress" rule. In production, burns API quotas overnight and generates 5-figure bills.
Fix. Standard Hard Rule in every SKILL.md that calls external tools:
```
- **Max iterations**. Stop after N steps with no new signal.
- **Never repeat** the same tool call with the same arguments.
```

### The agent with no output format
An agent whose result changes shape on every run. Consumer agents (reading its output) cannot rely on it.
Fix. Mandatory "Output Format" section in every SKILL.md.

### The too-ambitious v1
A v1 that tries to cover everything. Fails at everything. A v1 should do the minimum valuable thing, perfectly.
Fix. Define the minimum viable scope. Everything else is v2.

---

## Evaluating an agent before calling it "ready"

Two production-research metrics (2026) to use before any real deployment.

**pass@k**. Probability that at least one run out of k succeeds. Useful to validate the agent *can* succeed.

**pass^k**. Probability that *all* k runs succeed. This is the production metric. An agent that succeeds 7 out of 10 is not a production agent.

Practical rule. Before plugging an agent into a real workflow, run the same task 3 times on different data. If the 3 successful runs are not consistent in shape and reliability, not ready.

---

## Patterns that work well on PhantomOS

These patterns are proven. Draw from them rather than reinvent.

| Pattern | Description | Example |
|---------|-------------|---------|
| **Collect -> Analyze -> Propose** | Pull data, identify insights, write proposals into the Context Engine | `analyze-perf`, `mine-audience` |
| **Read -> Generate -> Push** | Read context, generate deliverable, push to external tool | `routine-looker`, `generate-brief` |
| **Audit -> Flag -> Todo** | Scan workspace state, identify anomalies, create actionable tasks | `validate-resources`, `freshness-checker` |
| **Ingest -> Parse -> Enrich** | Receive raw resource, analyze, propose enrichments to entities | `ingest-resource` |
| **Orchestrate -> Sequence -> Collect** | Call N agents in order, collect outputs, produce aggregate result | `onboard-brand` |

---

## Recommended agents to build (examples, not shipped)

These agents are natural Context Engine use cases. Examples of what operators can build with `build-agent`. Not finished specs, starting points.

| Agent | What it does | Pattern |
|-------|--------------|---------|
| `brief-generator` | Generate a creative brief from brand context + latest performance | Read -> Generate -> Push |
| `freshness-checker` | Detect stale entities (last update > 60 days) and create todos | Audit -> Flag -> Todo |
| `trend-watcher` | Watch Google Trends + Reddit on brand themes | Collect -> Analyze -> Propose |

Note. `mine-audience`, `watch-competitors`, `score-product-fit` were on this list in earlier releases. They are now **shipped** in `.skills/skills/`. Use them as reference implementations when designing new Producer-type skills.
