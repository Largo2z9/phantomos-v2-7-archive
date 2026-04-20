---
name: learn-from-session
type: capturer
version: "1.0.0"
recommended_model: sonnet
description: >
  Extracts and persists knowledge acquired during a session. Scans the conversation,
  identifies what was learned/decided/corrected, and routes to the right files.
  Two trigger modes:
  1. EXPLICIT — Triggers: "learn", "session close", "persist", "fin de session", "enregistre ce qu'on a fait", "save session". EN: "learn", "session close", "persist", "save what we learned".
  2. PROACTIVE — The agent detects ≥1 learning signal during the session (operator correction, API workaround, strategic decision, compliance rule) and proposes unprompted: "I've noted some things to persist. Want me to save them?" If confirmed → run this skill.
permissions:
  reads: [brand, product, profile, learning, strategy]
  writes: [learning]
  mode: proposed
  subagent_safe: false
pipeline:
  preconditions: none
  postconditions: run validate-resources to reconcile if major changes
---

# Skill: Learn From Session

## Tone

Plain-language summary. Zero paths, zero JSON, zero routing destinations. The operator sees strategic decisions, not technical writes.

Capture semantically at session end. No manual writing needed, conversation contains all learnings.

Responsibility: scan full conversation → extract persistable elements → classify → route → write via ingest-resource or direct update.

---

## CRITICAL: Executive briefing posture — adapted to session context

**YOU MUST** present the flush recap to the operator in a **superior-to-decider briefing format**. The operator is the decider, you are the operational lead reporting up. They do not want the technical inventory of what you captured, they want to know what changes and whether any decision needs their arbitrage.

**ALWAYS detect the session context first, pick the right posture**:

| Session dominant register | Posture |
|---|---|
| Strategic / product / architecture | CTO → CEO |
| Operational / execution / ship | Project lead → founder |
| Creative / copy / brief review | CD → client |
| Debug / technical deep-dive | Senior engineer → lead |
| Audit / review / diagnostic | Auditor → stakeholder |
| Research / exploration | Head of research → sponsor |

Posture drives register and priorities. A CTO says *"1 tech arbitrage: activate model routing or wait?"*. A project lead says *"3 items shipped, 1 blocker on access tokens, next up: test on Karacare"*. A CD says *"3 concepts delivered, 1 needs your call on tone"*.

**ALWAYS apply, regardless of posture**:

- **MAX 5-7 strategic bullets.** Each bullet = one decision taken OR one arbitrage needed. **NEVER** more.
- **Frame every bullet as decision or impact**, never as "what I captured".
  - ❌ *"Captured 8 decisions, 3 operator preferences, 2 open threads, 1 friction"*
  - ✅ *"Template switched to EN, agent adapts at runtime (done). Model routing ready to activate (1 prerequisite to test). Rest: applied, RAS."*
- **NEVER expose** file paths, skill names, field names, D# numbers, routing destinations, enum values, JSON shapes in the briefing. Those write silently to the right files.
- **ALWAYS close with one of two formats**:
  - *"1 arbitrage to make: [concise question]. OK?"* — when one decision needs the operator. **PREFER `AskUserQuestion` tool** (load via `ToolSearch(select:AskUserQuestion)` if not loaded) to render the arbitrage as native clickable options (e.g. *Ship now / Wait / Discuss*). Fallback to plain question if tool unavailable.
  - *"All applied, RAS."* — when everything is mechanical, no decision needed. No tool needed.
- **NEVER** ask the operator to validate the routing plan (destinations, files, format). They trust the system. Write silently after the briefing is acknowledged.
- **Tone**: the superior reporting up. Direct, zero jargon, zero details below the decision level. Match the register to the posture detected.

After briefing + green light (or correction on the arbitrage), execute the full persistence writes silently according to the routing table below. **YOU MUST NEVER** paste the raw technical recap in the conversation.

This rule **overrides** any "detailed recap with plain-language fact list" pattern that may appear later in this skill. The operator has flagged that format as indigestible. Executive briefing first, technical writing silent.

---

---

## Triggers — batch mode, not incremental

**Critical principle**: the agent **captures continuously** in session memory, but **only proposes persistence at specific triggers**. Not every turn, that pollutes.

### Trigger 1 — End of structuring Step
End of setup-brand Step 5 (workspace tour, operator has seen value) or after first real deliverable produced (audit done, brief delivered, diag completed). Not at Step 4, which is only a Build chantier switch.

### Trigger 2 — Every 3-5 turns of dense conversation
During an active work session (ingest, audit, brief, production), track the number of turns since last flush. At turn 3-5, check: *are there at least 2 valuable learnings in the buffer?* If yes, propose. If no, wait.

### Trigger 3 — End of session (terminal signal)
The operator says *"later", "ok thanks", "I'm out", "tomorrow"*, visibly closes the terminal (short message without question). If buffer not empty → propose a final flush.

### Trigger 4 — Explicit request
Verbal triggers: *"learn", "save", "enregistre", "fin de session", "persist", "save session", "session close"*.
EN: *"learn", "save what we learned", "session close", "persist"*.

### Trigger 5 — Minimal auto-persist (anti-loss on crash)
Every 5 turns, write a rolling line to `session-state.md` Activity Log with the 2-3 latest captured facts, even without confirmation. It's read-minimal, not structured learnings — allows recovery on brutal closure.

### Trigger 6 — CLAUDE.md size check on every batch flush
At every batch flush (Trigger 1 to 4), measure the size of root `CLAUDE.md` and of each active `brands/{slug}/CLAUDE.md`. Budgets: root ≤ 220 lines, brand ≤ 100 lines. If a file exceeds, add ONE line at the end of the flush recap: *"ℹ CLAUDE.md at {N} lines (budget 220), manual review recommended."* No auto-split, no structured proposal. Just a flag for the operator to arbitrate later. See `docs/system/agent-contracts.md § Size Policy` for the pre-write guardrail.

## Flush format — recap before writing

When a trigger fires, **before writing**, the agent shows a plain-language recap:

> *I captured X things since earlier:*
> *1. {fact 1 in 1 operator line}*
> *2. {fact 2 in 1 operator line}*
> *3. {fact 3 in 1 operator line}*
> *4. {fact 4 in 1 operator line}*
>
> *File it? (say "yes" for all, or correct if I got it wrong.)*

The operator can:
- *"Yes"* / *"Go"* → all written to the right files (operator/profile.json, brands/{slug}/learnings.json per routing)
- Targeted correction → *"drop #3, #4 isn't that, it was actually X"* → the agent adjusts the buffer, redisplays, re-asks
- *"Not now"* / *"Skip"* → buffer preserved, propose at next trigger
- *"Stop tracking"* → deactivate tracking for the session (rule set in `/operator/profile.json → preferences.tracking: "off"`)

## Critical distinction — where it goes

Each buffer entry must be **routed to the right file** based on what it concerns:

| Learning type | Destination |
|------------------|-------------|
| Operator preference (tone, style, tools tested, personal anti-patterns) | `/operator/profile.json` |
| Operational brand fact (API workaround, compliance rule, creative pattern that works) | `brands/{slug}/learnings.json` |
| Structural brand correction (tone, positioning, audience objection) | `brands/{slug}/brand.json` or `profile.json` direct (via ingest-resource) |
| Strategic decision | `session-state.md → Active Decisions` |
| Product friction / workflow bug | `todos.md → ## Flags` |

**Never mix**: an operator info does not go into brand.learnings, a brand fact does not go into operator/profile. Cross-contamination = structural bug.

---

## Step 1 — Receive & Scan Conversation (explicit trigger mode)

User triggers skill with: "learn", "fin de session", "persist", "save session", "enregistre ce qu'on a fait", "session close", etc.

Agent scans ENTIRE conversation (from start to present) and extracts:
- **Factual learnings**: API behaviors, workarounds, account quirks, test results, compliance rules
- **Structural decisions**: Product choices, audience segmentation, pricing decisions, tone rules
- **Strategic corrections**: Changes to strategy, positioning, target, constraints
- **Frictions & improvements**: Bugs, confusions, workflow issues flagged for todos.md
- **Open threads**: Unresolved questions, blocked work, pending actions

---

## Step 2 — Classify & Route

### Category: Factual Learnings

Scoped learnings — tied to the brand, platform, or account. Route to `brands/{slug}/learnings.json`.

**Entry structure** (append to `entries[]`):
```json
{
  "id": "LRN-{counter}",
  "date": "YYYY-MM-DD",
  "fact": "{1-line factual WHAT}",
  "reasoning": "{WHY it's true, what caused it, what it reveals — MANDATORY non-empty}",
  "platform": "{meta | shopify | klaviyo | google | none}",
  "tags": ["tag1", "tag2"],
  "source": "{conversation summary or 'session-{date}'}",
  "status": "active"
}
```

**CRITICAL: `reasoning` is MANDATORY.** This is the **Decision Trace** (see D#308 + docs/system/architecture.md § Canonical vocabulary). `fact` = WHAT happened, `reasoning` = WHY it happened. **YOU MUST NEVER** write `reasoning: ""`, `reasoning: null`, or generic fillers ("n/a", "observed", "noted"). If the operator's session context doesn't yield a clear why, push back during flush recap: *"Le fait #N je l'ai capturé, mais je n'ai pas le pourquoi. Qu'est-ce qui l'a causé ?"*. Degraded mode only if operator explicitly skips: `reasoning: "[captured without rationale — revisit on first application]"`.

Examples:
- ❌ `fact: "Meta pixel triggers 2s delay on iOS Safari"`, `reasoning: ""`
- ✅ `fact: "Meta pixel triggers 2s delay on iOS Safari"`, `reasoning: "Account-specific bug, not global — same pixel code works on 3 other brands without delay. Likely related to this account's Business Manager region or app approvals. Reported to Meta support, waiting on ticket response."`
- ✅ `fact: "Retinol cream @ 30€+ encounters 18% more objections than @ 25€"`, `reasoning: "Price bracket crossed a perceptual threshold — 25€ positioned as accessible premium vs 30€ perceived as mass-pharma territory. Confirmed across 4 creative variants, same copy, only price differed."`

Route via **ingest-resource** (Step 3B, learnings.json) if >3 entries to add. If single entry, append directly + update status.json.last_activity.

### Category: Structural Decisions

Key decisions made this session — move from activity log to Active Decisions in session-state.md.

**Format in session-state.md Active Decisions**:
```
- {Decision}: {chosen option} (reason: {1-line}) | date: YYYY-MM-DD
```

Examples:
- `- Audience main: femmes-40-55 (problem_aware) — highest purchase intent signal | date: 2026-04-03`
- `- Never say "rejuvenate": DGCCRF rule, tested with legal | date: 2026-04-03`

**No API call needed** — direct append to `session-state.md` Active Decisions section.

### Category: Strategic Corrections

Corrections to brand identity, tone, strategy, or positioning. Route via **ingest-resource** to the appropriate target:
- Tone correction → `brand.json.tone_of_voice`
- Positioning shift → `brand.json.positioning`
- Strategy update → `strategy.json`

Example trigger: "We realized our audience doesn't want 'youth' but 'skin health'" → ingest-resource → update profile pain_points + brand positioning.

### Category: Frictions & Improvements

Bugs, confusions, workflow issues. Route to `todos.md` → `## Flags` section.

**Format**:
```
- [FRICTION] {Issue}: {description} → {suggested action}
```

Examples:
- `[FRICTION] session-state.md rotation: Manual process error-prone → Need continuous auto-append`
- `[FRICTION] Learnings mapping: Hard to find which learning applies to which audience`
- `[FRICTION] Setup-brand: Asks for competitor URLs but never uses them → Remove or clarify use case`

### Category: Operator Context (workspace-level, cross-brand)

**Critical distinction**: what concerns *the operator themselves* (you, the user of the workspace) is cross-cutting and does NOT live in a brand folder. Route to `/operator/profile.json` at workspace root.

**4 sub-categories to detect:**

#### 4a. Identity & background
Signals: mentions of their role, years of experience, macro context.
- *"I have 10 years in performance marketing"* → `identity.experience_years: 10`, `identity.role: "performance marketer"`
- *"I work at a growth agency in Paris"* → `identity.context_macro: "agency growth Paris"`
- *"I'm an ex-marketer, launching my brand 3 months ago"* → `identity.context_macro`, `identity.role: "ex-marketer → DTC founder"`

#### 4b. Stack history (tools tested/abandoned)
Signals: mentions of tools used, abandoned, still active.
- *"I tried Lindy, dropped it after 3 weeks, too no-code for my needs"* → append to `stack_history[]`: `{tool: "Lindy", status: "abandoned", verdict: "too no-code", lessons: "avoid no-code flows for my use case"}`
- *"I use ClickUp daily"* → `stack_history[]`: `{tool: "ClickUp", status: "active", verdict: "daily driver"}`
- *"ChatGPT Enterprise + custom GPTs, that's my base"* → 2 active entries.

#### 4c. Work preferences
Signals: observed behavior + explicit statements.
- Constant use of short sentences → `preferences.communication_style: "concise"`
- *"I always answer in bullets"* → `preferences.response_length: "bullets"`
- *"I work evenings, not mornings"* → `preferences.work_hours: "evening"`
- *"I hate long answers"* → add to `anti_patterns_perso`
- Technical questions on JSON/architecture → `preferences.technical_level: "advanced"`
- Confusion on technical terms → `preferences.technical_level: "beginner"`
- Dominant language → `preferences.language`

#### 4d. Expectations & personal anti-patterns
Signals: what they expect from PhantomOS, what they structurally hate.
- *"If it saves me 30% time on briefs, I'm in"* → `expectations.success_criteria`
- *"I hate tools that ask 15 questions before producing anything"* → `anti_patterns_perso[]`
- *"No third-party cloud for my data, non-negotiable"* → `expectations.deal_breakers`

**Write mechanism**: via `write_to_context()` to `/operator/profile.json → {section}.{field}`. Mode `proposed` — the operator validates before write. This validation is quick (*"Noted for your profile: you tried Lindy and dropped it. OK?"*), not a long recap.

**NEVER** route these signals to `brands/{slug}/learnings.json` — they concern the operator, not the brand. Cross-contamination = structural bug.

---

### Category: Brand-specific Preferences (scoped to one brand)

If the signal concerns *one specific brand* (e.g. *"for brand X, I use a more corporate tone, different from my other brands"*), write to `brands/{slug}/config.json → operator_preferences_for_this_brand`. Rare — most operator preferences are cross-cutting and go to `/operator/profile.json`.

**Threshold**: only write when a pattern is observed ≥3 times in a session. One-off signals don't qualify.

**Examples:**
- Operator corrects 3 times with "shorter" → propose: "I noticed you prefer short answers. Note this for future sessions?"
- Operator edits JSON directly twice → propose: "You seem comfortable with technical files. Note your level to adapt my explanations?"

### Category: Open Threads

Unresolved questions, blocked work, next actions. Add to `session-state.md` → `## Open Threads` section or mark existing ones [RESOLVED].

**Format**:
```
- {Thread}: {status (pending | blocked | in_progress)} — {next action}
```

Examples:
- `- offers.json creation for creme-eclat: pending — blocked on marketing decision`
- `- 2nd audience (femmes-25-35): in_progress — segment research underway`

**Resolved threads** — mark `[RESOLVED {YYYY-MM-DD}]` instead of deleting:
```
- [RESOLVED 2026-04-03] Old thread title — resolved by doing X
```

---

## Concrete examples — routing by signal

Real examples of signals detected in session and their exact destination:

| Session signal | Type | Destination |
|---|---|---|
| Operator corrects the tone of a hook ("too corporate, be more direct") | Strategic correction | `brand.json → tone_of_voice` via ingest |
| Meta API error subcode 1487664, call_to_actions missing | Factual learning | `learnings.json` via capture-learning |
| "My max COS is 14%, above that we cut" | Structural decision | `strategy.json → constraints` via ingest + session-state Active Decisions |
| Operator says "shorter" 3 times in the session | Operator preference | `config.json → operator.response_length_preference` (mode: proposed) |
| "We launched the -20% first order offer this week" | New data | `products/{slug}/offers.json` via ingest |
| Operator systematically rephrases your outputs in bullet points | Operator preference (≥3 signals) | `config.json → operator.communication_style` (mode: proposed) |
| "Meta pixel triggers 2s delay on Safari iOS, specific to our account" | Factual learning (scoped) | `learnings.json` tags: ["meta-ads", "pixel", "ios"] |
| "Finally our main audience isn't 25-35 but 35-50" | Strategic correction | `audiences/{slug}/profile.json → demographics` via ingest |
| Agent generated an incorrect UTM, operator corrects the format | Convention learned | `resources/conventions/{platform}.json → learned_rules[]` OR `learnings.json` if brand-specific |
| "We tested pain vs desire angle, desire wins 2:1 on our audience" | Factual learning (test result) | `learnings.json` tags: ["creative-testing", "angle", "results"] |

**Ambiguous case — decision rule:**
- General API limitation (affects all accounts) → `learnings.json` + tag `promote_candidate` for future promotion into shared convention
- Account-specific limitation (config, access tier) → `learnings.json` without promote tag
- Operator preference (style, format) → `config.json → operator`
- Platform rule learned (naming, UTM, workaround) → `resources/conventions/{platform}.json → learned_rules[]` if the convention exists, otherwise `learnings.json`

---

## Step 3 — Execution Paths

### Path A: Factual Learnings → ingest-resource

If >1 learning extracted:

1. Collect all learnings as structured JSON (see Step 2 format)
2. Call **ingest-resource** with:
   - Content: learnings array
   - Destination: `brands/{slug}/learnings.json`
   - Action: append to entries[]
3. ingest-resource returns summary + updates status.json.last_activity

### Path B: Session-State Direct Updates

For decisions, open threads, resolved threads: **write directly to session-state.md** (no ingest-resource call).

1. Read `session-state.md`
2. Append to appropriate section (Active Decisions | Open Threads)
3. For resolved threads, prepend `[RESOLVED YYYY-MM-DD]` to the thread line
4. Update timestamps

### Path C: Strategic Corrections → ingest-resource

If positioning, tone, or strategy changed:

1. Identify which file(s) to update (brand.json | strategy.json | profile.json)
2. Call **ingest-resource** with the corrected content
3. Let ingest-resource handle merge, field_types validation, status.json update

### Path D: Frictions → todos.md

1. Read `todos.md`
2. Append to `## Flags` section (auto-maintained by validate-resources, but agent can pre-populate)
3. Format: `- [FRICTION] {issue}`

---

## Step 4 — Novice Education (First Call Only)

If this is the brand's first learn-from-session call:

Display a brief explanation in operator language (no file names, no paths, no jargon):

```
How I keep the memory of your sessions

While we work, I capture silently. At the end of a session, or when you say "later" or "learn", I file what deserves to be kept:

1. Concrete facts learned (platform rules, test results, compliance) → filed in your brand's memory.
2. Structural decisions (audience segmentation, internal rules, pricing) → marked as active.
3. Strategic corrections you made (tone, positioning, audience) → applied directly to your brand.
4. Frictions you flagged (bugs, workflows to improve) → added to your todos.
5. Open questions → listed for next session.

Nothing is lost. Even if you leave without a signal, I keep a rolling trace to pick up cleanly next time.
```

Show once per brand, then suppress on subsequent calls.

---

## Step 5 — Output Summary + Validate Handoff

After execution, display structured summary to user:

```
Session captured — {brand}

{N} item(s) persisted:

1. Learnings ({count})
   ✓ {1-line learning 1}
   ✓ {1-line learning 2}

2. Decisions ({count})
   ✓ {1-line decision 1}

3. Corrections ({count})
   ✓ {1-line correction 1} → {file}

4. Frictions ({count})
   ✓ {1-line friction 1} → todos.md

5. Threads ({count} open, {count} resolved)

Next session: context auto-restored from session-state.md.
```

Then **always propose validate**:

```
Want me to validate the workspace now?
→ Checks consistency of what was saved tonight + runs CHANGELOG rotation.
(say "go" or "later")
```

- If "go" / "yes" / "ok" → trigger `validate-resources` immediately.
- If "later" / silence → close cleanly:
  ```
  OK. Launch "validate" when you're ready, ideally before the next session.
  ```

**Effort/value ratio**: validate after learn = 30 seconds, zero friction. Best moment — operator is already in closing mode, and validate runs CHANGELOG rotation + learnings index rebuild + todos flags in a single pass.

---

## Hard Rules

- **Dedup before appending** — before adding a new learning to learnings.json, scan existing `entries[].fact` for semantic overlap (same platform + same behavior described). If match found → skip, do not add duplicate. If similar but different nuance → add with a `see_also: ["LRN-XX"]` pointer. Never create two entries saying the same thing.
- **Never delete learnings or decisions** — only archive (mark status: "superseded" for learnings, prepend [RESOLVED] for threads)
- **Always scan full conversation** — don't just look at recent messages
- **Classify semantically, not syntactically** — user may not say "this is a learning" explicitly. You infer.
- **Respect _field_types** — never inject strategy into brand.json context fields
- **Route via ingest-resource for shared resource changes** — maintain integrity
- **Direct write only for session-state.md updates** — those are append-only logs
- **Novice education once per brand** — suppress on repeat calls
- **Always show what was learned** — summary is mandatory, not optional
- **If conflict detected** (two opposing facts/decisions), surface to user: "Decision X contradicts Y. Which version is correct?" — wait for clarification before writing
