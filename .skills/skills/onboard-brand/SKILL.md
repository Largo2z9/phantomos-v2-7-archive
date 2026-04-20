---
name: onboard-brand
type: orchestrator
version: "1.0.0"
recommended_model: sonnet
description: >
  Full-cycle brand onboarding orchestrator. Chains setup-brand (identity + structure)
  → snapshot (URL scan, background) → ingest-resource (docs collected during setup)
  → validate-resources (integrity check) → close with Build chantiers variant per profile.
  Single operator intent, delegated pipeline across 4 specialized skills.
  FR: "onboard cette brand", "fais le full setup", "onboarding complet", "configure tout depuis zéro".
  EN: "full onboarding", "onboard brand end to end", "full setup pipeline".
permissions:
  reads: [brand, product, offer, profile, learning, strategy]
  writes: [brand, product, offer, profile, learning]
  mode: proposed
  subagent_safe: false   # this is the pilot, it orchestrates subagents
pipeline:
  preconditions: operator provides brand URL or brand name + intent to onboard from scratch
  postconditions: |
    - brand structure created and populated at level 1-2
    - pending-validations.md filled with Build chantiers per operator profile
    - learn-from-session flush proposed at end
disambiguates_against:
  setup-brand: "route to setup-brand when operator wants only the initial structure/identity, not the full 4-step pipeline"
  snapshot-brand: "route to snapshot-brand when operator wants just URL scraping on an already-configured brand (not a full onboarding)"
---

# Skill: onboard-brand

**CRITICAL:** this is an **Orchestrator**. **YOU MUST NEVER** re-implement setup-brand, snapshot, ingest-resource, or validate-resources logic here. **YOU MUST** delegate to each existing skill in sequence via Task tool (when the subskill is `subagent_safe: true`) or inline invocation (when `subagent_safe: false`).

## Tone

Chairman orchestrating a 4-step pipeline. Narrate each handoff briefly to the operator ("scan launching in background... structure built... validation pass..."). **NEVER** expose technical paths or field names. Keep the operator informed of progress without overloading.

---

## Expert methodology

**Canonical expert persona**: senior onboarding consultant setting up a new client from zero to operational in one sitting.

**Framework**: sequential pipeline with async parallelization where possible. Each phase has a gate before proceeding.

**Matrix**:

| Phase | Skill delegated | Subagent? | Gate before next phase |
|---|---|---|---|
| 1. Structure + identity | `setup-brand` | No (conversational) | Brand folder created, brand.json has name + language + sector |
| 2. URL snapshot (parallel) | `snapshot-brand` | Yes (Task tool) | Product + offers + audience draft filled at 60% |
| 3. Context enrichment | `ingest-resource` (if operator pasted docs during 1-2) | Yes (Task tool) | Ingested docs routed to correct entities |
| 4. Integrity check | `validate-resources` | Yes (Task tool) | Zero blocking errors, flags surfaced |
| 5. Build chantiers close | inline (see CLAUDE.md § Build → Execute gates) | No | Operator chose a/b/c/d |

**Variables tracked**:
- `profile` (solo-brand-live / early-founder / creator-led / agency-portfolio / dropshipper / portfolio) — drives Build chantiers variant at close
- `url_available` (bool) — drives whether Phase 2 runs or is skipped
- `docs_pasted_during_setup` (list) — drives Phase 3 routing

**Failure modes**:
- setup-brand fails mid-flow (operator abandons) → save partial state in `brands/{slug}/session-state.md`, allow resume
- snapshot fails (URL 404, JS-heavy, paywalled) → degrade to Phase 3/4 without pre-fill, flag confidence drop
- validate-resources finds blocking errors → present to operator, let them fix before Phase 5 close

---

## Step 0 — Pre-flight

Check operator provided minimum context:
- Brand name OR URL
- Profile hint (if not, infer from context; if still ambiguous, ask once via AskUserQuestion)

If neither name nor URL → ask via AskUserQuestion: *"To onboard, I need either your brand name or the URL of its site. Which do you have?"*.

Announce the pipeline briefly (chairman posture):

> *"OK, full onboarding. I'm going to chain 4 steps: structure, scan, enrichment, integrity check. Then Build chantiers. 5-10 min total depending on what you already have. I pilot, you validate at each gate. Let's go."*

---

## Step 1 — Delegate to `setup-brand` (inline, conversational)

**NEVER** spawn as subagent (`setup-brand.subagent_safe: false`). Invoke inline. Let it run its flow (Step 0-5 depending on URL availability).

Pass context: operator-provided name/URL, detected profile, language preference from `operator/profile.json`.

**Gate to Phase 2**: `brands/{slug}/brand.json` exists with `identity.name` and `identity.language` filled, OR operator explicitly deferred structure creation.

---

## Step 2 — Delegate to `snapshot-brand` via Task tool (parallel)

**If** URL available AND `snapshot-brand.subagent_safe: true` (verified in frontmatter):

Spawn subagent with Task tool:
- `model: sonnet` (per snapshot frontmatter)
- Input: brand slug, URL
- Expected output: `products/{slug}/spec.json`, `products/{slug}/offers.json`, `audiences/{slug}/profile.json` drafts

**While snapshot runs**, continue conversation with operator (ask about any pasted docs, clarify intent, etc.). **NEVER** block the operator waiting for snapshot.

**When snapshot returns** at a natural conversation break:
> *"Snapshot done. [1-2 lines: hero product detected, audience inferred, offers found]. I keep going with integrity check."*

**If URL absent** → skip Phase 2.

---

## Step 3 — Delegate to `ingest-resource` via Task tool (if applicable)

**If** operator pasted docs (briefs, competitor links, past campaigns data) during Steps 1-2:

Spawn subagent via Task tool for each pasted doc:
- `model: sonnet`
- Input: doc content, target brand slug, auto-detection or hint for entity (brand/product/audience/learning/strategy)
- Expected: routed write via `write_to_context(mode="proposed")`

**If no docs pasted** → skip Phase 3.

---

## Step 4 — Delegate to `validate-resources` via Task tool

Always run, even if Phases 2-3 skipped. Subagent:
- `model: haiku` (per validate-resources frontmatter, `subagent_safe: true`)
- Input: brand slug
- Expected output: integrity report (blocking errors vs flags vs warnings)

**If blocking errors**:
> *"Integrity check flagged [N] blocking issues. [1-2 lines summary, operator language]. I hold Phase 5 until we resolve them. Want me to walk you through?"*
→ AskUserQuestion: *"Fix now (guided) / Skip and accept technical debt / Abort onboarding"*.

**If only warnings or flags** → surface them as ambient todos in `pending-validations.md`, continue to Phase 5.

---

## Step 5 — Close with Build chantiers (inline, per profile)

**CRITICAL**: **NEVER** propose deliverables here. This is a Build close, not an Execute close.

Read operator profile from `operator/profile.json → identity.profile`. Pick the variant from `docs/system/patterns.md § Close Variants`:
- solo-brand-live
- early-founder
- creator-led
- agency-portfolio
- dropshipper (default to solo-brand-live variant if not explicitly templated)

Render the 4-option close via AskUserQuestion, adapted to the profile.

Then trigger learn-from-session batch (posture adaptive, operational/ship register likely for this orchestrator): brief the operator on what was shipped across the 4 phases, 5-7 bullets max, close with "1 arbitrage" (usually the Build chantier pick) or "All applied, RAS".

---

## Operator cartography (before Phase 1, if complex)

If the operator provided minimal context but URL is available, briefly cartograph the pipeline before executing (~4 lines, operator language, no system jargon):

> *"Analysé. Voilà comment je vais onboarder :*
> *• Je construis la structure de ta marque pendant qu'on parle*
> *• Je scanne ton site en arrière-plan, ça pré-remplit 60% du contexte*
> *• Si tu as des docs en plus (brief, screenshots, comptes passés), je les range au fil*
> *• Je passe un check d'intégrité à la fin, je te remonte ce qui cloche*
> *• On close sur les chantiers à construire avant tout livrable"*

Then AskUserQuestion: *Go / Skip scan (pas d'URL) / Ajuste le pipeline / Autre*.

---

## Guardrails

- **NEVER** run all 4 phases sequentially blocking — Phases 2 and 3 parallelize with the conversation.
- **NEVER** expose Task tool mechanics or subagent internals to the operator ("I spawned a subagent", "validate-resources ran in a subprocess"). Say what it *does*: "I scanned your site", "I checked integrity".
- **NEVER** re-implement subskill logic. If a subskill has a bug, fix it there, not here.
- **ALWAYS** surface blocking integrity errors before Phase 5 close. Never close on a broken state.
- **ALWAYS** persist `brands/{slug}/session-state.md` rolling update after each phase (for crash resumption).
