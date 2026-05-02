# System docs

⚠️ **FOR CONTRIBUTORS AND CORE MAINTAINERS**

If you are using PhantomOS as a DTC paid acquisition operator, you don't need to read these docs. See [`docs/product/`](../product/) for operator guidance instead.

This section documents PhantomOS architecture, extension patterns, and internal disciplines that govern how skills and resources are designed.

## Architecture & specs

- **`architecture.md`** — technical architecture. Entities, field types, dependency graph, session relay, context budget, connectivity pattern, rules.
- **`agent-contracts.md`** — `CLAUDE.md` specification. Types (root, brand, template), loading mechanism, precedence, write discipline, lifecycle, size policy.
- **`patterns.md`** — operational patterns and taxonomies. Close variants, sharpening examples, context levels, model routing, skill taxonomy, skill philosophy.
- **`extending.md`** — the extension layer architecture. Custom entities, sidecar schemas, custom skills, external pipeline integrations, and the three governance rules that keep extensions interoperable.

## Skill lifecycle & composition

- **`skill-creation-protocol.md`** — protocol for creating skills. Detection signals, graduation matrix (specific / heavy / macro), three operator validation gates, extend_before_create discipline, rollback/sunset.
- **`skill-builder-cartography.md`** — when to scaffold a new custom entity before coding a skill. Cartography-first pattern : map domain variables, identify schema gaps, extend via scaffold-extension, THEN code the skill.
- **`sop-skill-conversion.md`** — how SOPs (methodology) and skills (execution) interact. The 5 conversion scenarios (doc → SOP, SOP → skills, skill → SOP, etc.). Decision tree "where does this knowledge go ?". Who-calls-who contract.
- **`skill-resource-discovery.md`** — runtime pattern for skills finding relevant knowledge from `resources/` without tagging. FTS5-based discovery, priority rule (brand > resource), 8-step execution flow, cost budget.

## Audits & red team

- **`skill-architecture-redteam.md`** — synthèse 50 scenarios stress-testing the skill architecture proposal. 7 convergent gaps identified, top-3 architecture weaknesses, decisions taken in response.

## Writing canon

- **`voice.md`** — the writing style canon. Every editor (human or agent) reads this before modifying any doc in the project. Includes the "heavy skill posture — always ask before cascade" rule.

## Build & release

- **`contract-build.md`** — rules when the agent is in Build mode (building new skills, extensions, orchestrators).
- **`contract-daily.md`** — rules in operator daily-use mode (smart suggests, learning capture, connectivity, pedagogy on demand).
- **`updates.md`** — template update mechanism. Version manifest format, compatibility rules, maintainer doctrine, anti-patterns.

## Cookbook & how-to

- **`cookbook.md`** — how to extend PhantomOS. Build a skill, write a SOP, wire a connector, ship a vertical pack.

## Who this is for

Contributors to the PhantomOS template — core maintainers, skill authors, workspace adopters who want to customize their instance. Also agents that need to read the architecture spec to operate correctly.

## Conventions

System docs are the densest surface of the project. Technical, specific, reference-grade. No marketing, no onboarding affect. Paragraphs carry reasoning ; tables carry rules ; code blocks carry truth.
