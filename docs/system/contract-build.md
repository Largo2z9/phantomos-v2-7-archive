# Contract · Build & Execute

> **Load this doc when:** the agent is about to trigger a `type: builder` or `type: orchestrator` skill, or switch from Build mode to Execute mode on a deliverable.
> **Otherwise:** ignore. The root `CLAUDE.md` loads this on demand via pointer.

---

## Orchestration gate

**CRITICAL**: the main agent is an active orchestrator, not a passive dispatcher.

**Before triggering any build/scaffold skill** (`build-agent`, `scaffold-extension`, any skill with `type: builder` or `type: orchestrator`), verify the intent cannot already be served by existing structures. Apply the five-dimension check (core entities / active-brand sidecars / active-brand custom entities / sibling-brand custom entities / shared resources). If any dimension matches, **route to that structure** instead of building new. Scaffold only when genuinely new. The dedicated sub-skill `check-existing-coverage` runs this check inside `scaffold-extension`, but the main agent **YOU MUST** apply the same discipline before every build decision.

**For multi-skill workflows**, maintain a session-level coordination map in memory:
- Which skill has which scope (reads/writes declared in its permissions)
- Which wrote to which path during this session
- Which cross-refs were touched

If two skills in the same workflow target the same path with conflicting modes (one proposed, one direct), **YOU MUST** surface the conflict to the operator before executing the second. **NEVER** let two skills step on each other silently.

**Routing rule for capture vs build**: apply the three binary tests before invoking a skill:
1. Capture (existing fact) or construct (new structure/behavior)? → capture skills vs build skills
2. If capture: one fact or whole session? → `capture-learning` vs `learn-from-session`
3. If construct: data structure or skill behavior? → `scaffold-extension` vs `build-agent`

Full matrix → `docs/system/patterns.md § Capture & Build routing`.

---

## Build → Execute gates

**IMPORTANT: NEVER** switch to Execute without clearing every applicable gate.

| # | Gate | Trigger | Action |
|---|---|---|---|
| 1 | Access | Skill needs external platform | **CRITICAL:** check `credentials.env` (brand) + `credentials_shared.env` (workspace) for token BEFORE anything else. Missing → **NEVER** start interview/questionnaire fallback silently. Present 2 options: *"Audit Meta needs API access. Either you give me a System User token (5 min, I walk you through), or we do declarative interview mode (less reliable, slower). Which?"*. Token present → use API directly, deliver factual audit, never ask questions the API can answer. |
| 2 | Doc | Platform untouched before | **YOU MUST** read official doc via WebFetch, fill convention (rate limits, scopes, pitfalls) BEFORE touching a token. |
| 3 | Context | Skill consumes inferred fields | If not human-validated, flag in output, offer review. Soft friction: operator insists → deliver + flag "⚠ based on unvalidated X". |
| 4 | Ambient todo | Post scrape/setup/ingest | Append detected items to `brands/{slug}/pending-validations.md`. Surface in (b)/(d) suggests. **NEVER** force. |
| 5 | Skill-candidate | Task long/recurring | Propose formalization as documented plan BEFORE run. Refused → flag in pending-validations. |

**Execute switch protocol** (operator requests a deliverable):
1. Access check → 2. Context check → 3. Convention check → 4. Plain-language summary + explicit confirm → run → flush `learn-from-session`.

**Close variants by profile** (solo-brand-live / early-founder / creator-led / agency-portfolio) → `docs/system/patterns.md § Close Variants`.
