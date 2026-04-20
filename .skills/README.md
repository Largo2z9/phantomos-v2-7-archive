# .skills/

Specialized capabilities of the agent. Never read by the operator, triggered automatically by the agent when a request matches.

## Organization

- **`skills/{name}/SKILL.md`**. One capability = one folder. `SKILL.md` describes the trigger, methodology, inputs/outputs.
- **`_TEMPLATE/`**. Template to create a new skill. Used by `build-agent`.
- **`mcp/`**. MCP server for some integrations (internal, not exposed to the operator).
- **`agent-design-guide.md`** and **`how-to-build-skills.md`**. Internal docs for skill builders.

## References (read before building or modifying a skill)

- **Typology contract** (mandatory `type:` field, six typologies, binary tests, defaults): `docs/system/patterns.md § Skill Taxonomy`
- **Expert methodology rule** (codified expertise vs improvised action, complexity gate): `docs/system/patterns.md § Skill Philosophy`
- **Model routing** (subagent spawn decision, cost/latency trade-offs): `docs/system/patterns.md § Model Routing`

## Skills shipped

| Skill | Role | Type | Model | Subagent |
|---|---|---|---|---|
| `setup-brand` | Configure a new brand (Step 0-5) | orchestrator | sonnet | no |
| `snapshot-brand` | Quick scan of a brand or product from a URL | producer | sonnet | yes |
| `ingest-resource` | File a doc/pdf/link into the right entity | curator | sonnet | yes |
| `validate-resources` | Check consistency, completeness, typology enforcement | curator | haiku | yes |
| `query-context` | Search across brand context and shared resources | curator | haiku | yes |
| `capture-learning` | Note a one-off learning named by the operator | capturer | haiku | yes |
| `learn-from-session` | Silent batch extraction of learnings from the session | capturer | sonnet | no |
| `promote-learning` | Promote a brand-local learning into a cross-brand rule | curator | sonnet | yes |
| `migrate-workspace` | Upgrade an existing brand to the current template version | curator | sonnet | yes |
| `build-agent` | Build a new custom skill with dissection and operator cartography | builder | opus | no |
| `audit-meta-setup` | Structured audit of a Meta Ads account (API or declarative) | producer | sonnet | yes |
| `scaffold-extension` | Orchestrator — scaffold a new custom entity, sidecar, or custom skill via 9 sub-skills | orchestrator | sonnet | no |
| `analyze-extension-intent` | Sub-skill of scaffold-extension — capture intent (3 Q max) | curator | sonnet | yes |
| `check-existing-coverage` | Sub-skill — pre-build gate, 5-dimension check (core / sidecars / custom / cross-brand / shared resources) before scaffold | curator | haiku | yes |
| `propose-schema-draft` | Sub-skill — generate canon-compliant JSON Schema draft | producer | sonnet | yes |
| `validate-naming` | Sub-skill — enforce reserved names, kebab-case, MECE | curator | haiku | yes |
| `check-cross-refs` | Sub-skill — verify cross-refs resolve before scaffold | curator | haiku | yes |
| `validate-schema-canon` | Sub-skill — pre-write canon compliance check | curator | haiku | yes |
| `scaffold-entity-files` | Sub-skill — write schema + README + instance to `brands/custom/` | curator | haiku | yes |
| `scaffold-skill-stub` | Sub-skill — write SKILL.md stub to `.skills/skills/custom/` | builder | sonnet | yes |
| `register-and-flag` | Sub-skill — register in `index.json` + add adoption todo | curator | haiku | yes |
| `mine-audience` | Mine voice-of-market and propose audience enrichments | producer | sonnet | yes |
| `watch-competitors` | Watch competitor Meta ads and produce creative intel | producer | sonnet | yes |
| `score-product-fit` | Score product-audience fit and flag language gaps | producer | haiku | yes |
| `brief-day` | Session-start orientation, pending validations, next actions | navigator | haiku | yes |
| `resume-session` | Clean resumption after absence from `session-state.md` | navigator | haiku | yes |
| `red-team` | Multi-expert adversarial panel, stress test on a subject | orchestrator | sonnet | no |
| `onboard-brand` | End-to-end 4-step onboarding pipeline orchestrator | orchestrator | sonnet | no |

## Rule

The agent reads `SKILL.md` before executing, never from memory. If you want to understand what a skill actually does, open its `SKILL.md`.
