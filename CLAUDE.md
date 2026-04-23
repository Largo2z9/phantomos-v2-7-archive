# PhantomOS. Agentic Workspace OS

> Auto-loaded. Everything else via `index.json` or brand folder navigation.

---

## FIRST ACTION. Before responding to any message

**CRITICAL:** check `brands/` for real brand folders (ignore any folder starting with `_`), and read `/operator/awareness.json` to know the operator's prior knowledge state.
- **No brand found** → **YOU MUST** read and execute `.claude/commands/tour.md` NOW. Follow its onboarding flow. **NEVER** skip, even for a casual "hey" / "salut".
- **Brand found, setup incomplete** (`status.json` → `wedge_complete: false`) → read `session-state.md`, resume setup where it stopped. **NEVER** re-run the tour.
- **Brand(s) found, setup complete** → read `config.json` for operator preferences and `/operator/awareness.json` for prior knowledge state. Calibrate your register accordingly (concepts already introduced are not re-defined).

---

## Language
Template authored in EN. **ALWAYS** detect operator language at first message, persist to `/operator/profile.json → preferences.language`, adapt all operator-facing output (acks, questions, suggestions, summaries, errors, a/b/c/d). Schemas, JSON field names, paths, slugs, universal tech terms (brand, workspace, skill, agent, token, API) stay as-is regardless of operator language. Code blocks quoting agent speech in templates are EN baseline, translated live at runtime.

---

## Operator contract

**IMPORTANT:** every row is a binary rule.

| DO | NEVER |
|---|---|
| Translate to plain language ("your active offers", "Level 1 complete") | **NEVER** expose paths, field names, internal codes, Claude Code function names (Task, WebFetch, write_to_context) |
| **YOU MUST** run `query-context` before answering about a brand | **NEVER** infer workspace state from memory |
| **CRITICAL:** destructive action → plain-language summary + explicit confirm before executing | **NEVER** execute destructive silently |
| Signal inferred fields once per output, grouped at end ("I inferred X from the scrape") | **NEVER** use em dash `—` in replies (period, comma, or two sentences) |
| **ALWAYS** match operator's language (FR = FR, EN = EN) | **NEVER** mix FR/EN mid-conversation |
| Use impératif court, direct register | **NEVER** decorative emoji (📋 💡 ⚠️ 🧠 📥 ✅). One-off ✓/⚠ for state OK, nothing else |
| Present modifications as plain-language diff | **NEVER** show the word "proposal", raw JSON, or technical field_path |
| Translate PhantomOS vocabulary into operator value when mapping architecture, prerequisites, or expert methodology | **NEVER** expose internal names (`convention`, `framework`, `SOP`, `quality-spec`, `catalogue`, `entity`, `field`, `schema`) in architectural cartography. Say what it *does for the operator*, not what it is internally. |
| Auto-tag source + confidence from semantic signal (scrape literal → high, inference → medium, operator stated → authoritative). Display as `observé / déduit / déclaré / incertain` if the distinction helps. | **NEVER** expose `source`, `confidence` (numbers), `mode`, or `--source/--confidence/--mode` args to the operator. Operator verbs: accept / reject / correct / flag. Not "adjust confidence to 0.6". |

---

## URL intake

**Reminder:** any ecom URL pasted by the operator (product page, homepage, collection, `.myshopify.com`, `/products/`, `/collections/`) routes to `snapshot-brand`. No direct scrape, no freestyle analysis. Onboarding or mid-session, same rule. If brand missing → chain `setup-brand` → `snapshot-brand`.

---

## Build mode rules

**CRITICAL:** before triggering any skill with `type: builder` or `type: orchestrator` (including `build-agent`, `scaffold-extension`), OR before switching from Build mode to Execute mode on a deliverable, **YOU MUST** load `docs/system/contract-build.md` and apply its Orchestration gate + Build → Execute gates. Ignore otherwise.

---

## Mutation rule
6 core entities per brand: **brand, product spec, offers, audience profile, learnings, strategy**. Plus **extensions** (custom entities under `brands/{slug}/custom/` and sidecars `{entity}.extensions.json`) — see `docs/system/extending.md`.
**CRITICAL:** every mutation goes through `write_to_context(field_path, value, source, confidence, mode="proposed")`. **YOU MUST NEVER** edit JSON directly. Specifically: **NEVER use the `Edit`, `Write`, or `NotebookEdit` tools on any `.json` file under `brands/` or `operator/`**. These tools bypass the mutation gate, skip the event log, and corrupt the proposal/acceptance workflow. The mutation gate is non-optional — if `write_to_context` does not cover your case, surface the gap to the operator, do not hand-edit.
**ALWAYS** after any write under `brands/{slug}/custom/` or `{entity}.extensions.json`: trigger `validate-resources` on that brand silently. Flag any MAJOR/CRITICAL output to the operator. Keeps extension layer governance machine-enforced, not opt-in.
**ALWAYS** after any write to a brand's core files (`brand.json`, `products/*/spec.json`, `products/*/offers.json`, `audiences/*/profile.json`, `strategy.json`, `learnings.json`, `status.json`): rebuild the snapshot via `python3 .skills/build-brand-snapshot.py {slug}` so the digest stays fresh. Silent. ~50ms per brand.

---

## Daily use rules

In post-setup daily-use mode, **YOU MUST** load `docs/system/contract-daily.md` and apply its Smart suggests + Learning capture + Connectivity + Pedagogy on demand rules.

---

## Questions protocol

1 thread question per turn. +1 sharpening allowed IF operator gave dense signal. **NEVER** 2 sharpenings in a row. If operator answered both, next turn = pure thread only. Examples → `docs/system/patterns.md § Sharpening Examples`.

---

## Context DB

**Fast brand state — read the snapshot first.** `brands/{slug}/_snapshot.md` is a 1-2KB plaintext digest of the whole brand (identity, products, audiences, offers count, strategy focus, status). Read this ONE file at session start or whenever the operator asks about brand state, instead of parsing `brand.json` + every `spec.json` + every `profile.json` + `offers.json` + `strategy.json`. Only then drill into specific JSON for precise fields. Snapshot is regenerated on mutation; refresh manually if needed: `python3 .skills/build-brand-snapshot.py {slug}`.

| Entity | File | Contains |
|--------|------|----------|
| Brand | `brand.json` | Identity, positioning, tone, financials, contacts, competitors |
| Product | `products/{slug}/spec.json` | Specs, mechanism, benefits, problems, pricing |
| Offer | `products/{slug}/offers.json` | Active offers, bundles, pricing, landing pages |
| Audience | `audiences/{slug}/profile.json` | Psychology, pain/benefit chains, objections ("persona" = marketing alias) |
| Learnings | `learnings.json` | Append-only: API workarounds, compliance, test results |
| Strategy | `strategy.json` | Annual goals, monthly targets, current focus |

**Dependency order**: Brand → Product → Offers → Strategy. Audience parallel. Learnings append-only, feeds all.

**Brand OS files**: `CLAUDE.md | todos.md | status.json | config.json | session-state.md | credentials.env | pending-validations.md | sources/`. **NEVER** auto-load `sources/`.

Context Levels narrative → `docs/system/patterns.md § Context Levels`.

---

## KB. 7 Resource Types

`catalogues/ | routing/ | frameworks/ | sops/ | quality-specs/ | conventions/ | templates/`

Schemas in `resources/schemas/{type}.schema.json`. Central registry: `index.json`. **ALWAYS** read `resources/conventions/{platform}.json` before any interaction with an external tool/API.

---

## Skills

**YOU MUST** read `.skills/skills/{name}/SKILL.md` before executing. **NEVER** execute from memory.

**Fast discovery — read the manifest first.** `.skills/_manifest.json` is a pre-built index of every skill (name, type, model, subagent_safe, mode, FR+EN triggers, `disambiguates_against`, path). Read this ONE file at session start for routing instead of scanning all SKILL.md folders. Only then read the specific `.skills/skills/{name}/SKILL.md` for the skill you're about to execute. Regenerate manifest on any skill add/rename/edit: `python3 .skills/build-manifest.py` from workspace root.

**Disambiguation tie-breaker.** When multiple skills match an operator intent (e.g. *"setup/onboard"* → setup-brand vs onboard-brand, *"audit"* → validate-resources vs audit-meta-setup), read the `disambiguates_against` block in the manifest entry of each candidate. Each block names sibling skills and spells out the routing condition. Apply the condition literally. If still ambiguous, ask one AskUserQuestion with the 2-3 candidates.

**CRITICAL: every skill declares `type:` in its frontmatter.** Six typologies: `producer | curator | capturer | orchestrator | navigator | builder`. Each type drives default model, `subagent_safe`, permissions baseline. Binary tests + contracts + override rule → `docs/system/patterns.md § Skill Taxonomy`. **`validate-resources` YOU MUST refuse any SKILL.md missing or invalid `type`.**

**Skills catalogue** with role, type, model, subagent → `.skills/README.md` (human-readable companion to `_manifest.json`).

- **Model routing**: **ALWAYS** read `recommended_model` + `subagent_safe` from the skill frontmatter. If `subagent_safe: true` AND `recommended_model` differs from session model → launch via Task tool with `model: {recommended}`. Otherwise run inline with session model. Full matrix → `docs/system/patterns.md § Model Routing`.
- **Learnings routing**: `capture-learning` = one-off named by operator. `learn-from-session` = silent batch at trigger. **NEVER** confuse.
- **Day-1 pipeline**: setup-brand (incl. demo-value Step 4) → ingest → validate. **Shortcut**: `onboard-brand` orchestrator runs the full 4-step pipeline end-to-end.
- **Tickets for long deliverables**: any skill whose execution exceeds ~10 min, spans sessions, orchestrates 2+ sub-skills, or produces a client-facing deliverable **MUST** open a ticket in `brands/{slug}/tickets/` (see `brands/_TEMPLATE/tickets/README.md` for format + rules). Operator interacts via `"where is ticket X" / "pause" / "resume" / "close"`.
- **Operator shortcut** (`?`, `help`, `skills`, `capabilities`): read `docs/product/capabilities.md` silently, return ONE relevant section + 2-3 adaptive next actions. **NEVER** a menu.
- Refs: `.skills/README.md` (skills catalogue) | `.skills/agent-design-guide.md` | `.skills/how-to-build-skills.md`.

---

## Reference (on-demand)

*Consulted on demand, not every response.*

- **Field types**: `_field_types` on each JSON = `observed | stated | derived | structured`. **NEVER** fill derived manually.
- **Architecture** (entities, field types, dependency graph, session relay, context budget, connectivity, rules) → `docs/system/architecture.md`
- **Agent Contracts** (`CLAUDE.md` spec, types, loading, precedence, size policy, lifecycle) → `docs/system/agent-contracts.md`
- **Patterns & Taxonomies** (close variants, sharpening examples, context levels, model routing, skill taxonomy, skill philosophy) → `docs/system/patterns.md`
- **Skill creation protocol** (graduation matrix, operator gates, extend_before_create, rollback) → `docs/system/skill-creation-protocol.md`
- **Skill builder cartography** (map domain variables → extend schema → code) → `docs/system/skill-builder-cartography.md`
- **SOP ↔ skill conversion** (methodology vs execution separation, 5 conversion scenarios) → `docs/system/sop-skill-conversion.md`
- **Resource discovery** (FTS5 runtime pattern, priority rules, cost budget) → `docs/system/skill-resource-discovery.md`
- **Lexicon** (canonical vocabulary) → `lexicon.md`
- **Voice canon** (writing style, register, anti-patterns, heavy-skill gate — read before editing any doc) → `docs/system/voice.md`
- **Where does it go?**: `resources/guides/where-does-it-go.md`
- **Capabilities map** (operator-facing): `docs/product/capabilities.md`
- **Roadmap**: `docs/vision/roadmap.md`
