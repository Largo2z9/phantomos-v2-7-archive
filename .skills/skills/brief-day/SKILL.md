---
name: brief-day
type: navigator
version: "1.0.0"
recommended_model: haiku
description: >
  Session-start orientation briefing. Reads workspace state across all brands
  and returns a tight operator-facing summary: portfolio health, pending validations,
  flags, suggested next actions. Zero deliverable, pure orientation.
  FR: "brief", "daily brief", "où j'en suis", "quoi de neuf", "fais-moi le point".
  EN: "brief", "daily brief", "what's up", "where am I", "status".
permissions:
  reads: [brand, product, offer, profile, learning, strategy]
  writes: []
  mode: none
  subagent_safe: true
pipeline:
  preconditions: at least one brand in brands/ (excluding `_`-prefixed)
  postconditions: none, read-only
---

# Skill: brief-day

**CRITICAL:** this is a Navigator, invoked directly by the operator for orientation. **NEVER** produce a deliverable. **NEVER** suggest deep work. **ALWAYS** stay in read-only summary mode.

## Tone

Chairman briefing a partner who just walked in. Zero jargon, zero file paths, zero JSON. Plain language, scannable in 30 seconds.

Posture adapted to context: if multi-brand operator (portfolio / agency) → portfolio-lead → principal. If solo brand → senior operator → founder. If early-stage → coach → builder.

---

## Step 1 — Scan workspace state (silent)

Read in parallel, no operator visibility:

- `brands/*/status.json` (exclude `_`-prefixed) for each brand: completeness level, last activity, flags
- `brands/*/pending-validations.md` for each brand: count unchecked items per section (context / access / enrichment / skill-candidates)
- `brands/*/todos.md` for each brand: `## In Progress` + `## P0/P1` top entries
- `brands/*/learnings.json` latest 3 entries (date, fact short)
- `operator/profile.json`: preferences.conversation_register, identity.profile, preferences.tracking
- `session-state.md` last 10 activity log lines if present

## Step 2 — Classify what matters (silent)

Bucket detected signals:

- **Brand health**: 1 line per brand — name, completeness level, days since last activity, flag count
- **Needs your call**: items in pending-validations marked critical or blocking (gate access missing on skills operator asked for, inferred audience not yet validated before planned deliverable, etc.)
- **Flags across portfolio**: cross-brand patterns (e.g. 3 brands missing Meta credentials, 2 brands with learnings_stale flag)
- **Next action suggestions** (2-3 max, ranked by impact)

## Step 3 — Deliver the brief

**ALWAYS** in executive format. 5-7 bullets max. **NEVER** dump raw data.

**Template** (adapt, never paste literally):

> **Portfolio health**
> - Karacare: Level 2 complete, last session 2 days ago. 1 flag (learnings_stale)
> - {brand B}: Level 1, last session today, clean
> - {brand C}: Level 1 draft, 4 days idle, `access_missing Meta`
>
> **Needs your call (2)**
> - Karacare inferred audience (Maghrebi/ME women) never validated, will contaminate next brief
> - {brand C} Meta access still pending client-side, blocking the audit you queued
>
> **Pattern I noticed**
> - 2 of your 3 brands miss Meta credentials. Worth batching a client outreach?
>
> **Suggested next**
> - Validate Karacare audience (15 min, unlocks brief-créa)
> - Or skip to {brand B} if you prefer momentum

**ALWAYS** close with smart suggests a/b/c/d using `AskUserQuestion` tool (load via `ToolSearch(select:AskUserQuestion)` if not loaded). Example options: *"Validate Karacare audience / Switch to {brand B} / Show full state of one brand / Other"*.

---

## Step 4 — What this skill NEVER does

- **NEVER** propose to run a Producer or Orchestrator skill without explicit operator request. Daily-brief orients, doesn't commit.
- **NEVER** expose file paths, field names, routing destinations, D# numbers.
- **NEVER** list all brands if portfolio > 5. Summarize: "{5 active, 2 need attention, see show-progress for full list}".
- **NEVER** give a brief longer than 10 bullets, regardless of workspace complexity. Pare down ruthlessly.

## Edge cases

- **Zero brands** → redirect: *"No brand configured yet. Run setup-brand or drop a URL."*
- **Single brand** → simpler format: health 1 line, needs-your-call 1-2 items, 1 next action
- **Operator just landed, no session-state.md** → treat as fresh start, mention "welcome back" once if > 3 days since last activity
- **Mode detected from operator/profile.json.preferences.conversation_register** → (1) grounded = more explanation of what each item means, (4) technical = pure bullet points zero fluff
