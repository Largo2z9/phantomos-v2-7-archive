# System docs

Contributor-facing documentation. How PhantomOS works under the hood, how to extend it, how to write for it.

## Files

- **`voice.md`** — the writing style canon. Every editor (human or agent) reads this before modifying any doc in the project.
- **`architecture.md`** — technical architecture. Entities, field types, dependency graph, session relay, context budget, connectivity pattern, rules.
- **`agent-contracts.md`** — `CLAUDE.md` specification. Types (root, brand, template), loading mechanism, precedence, write discipline, lifecycle, size policy.
- **`patterns.md`** — operational patterns and taxonomies. Close variants, sharpening examples, context levels, model routing, skill taxonomy, skill philosophy.
- **`cookbook.md`** — how to extend PhantomOS. Build a skill, write a SOP, wire a connector, ship a vertical pack.
- **`extending.md`** — the extension layer architecture. Custom entities, sidecar schemas, custom skills, external pipeline integrations, and the three governance rules that keep extensions interoperable.

## Who this is for

Contributors to the PhantomOS template — core maintainers, skill authors, workspace adopters who want to customize their instance. Also agents that need to read the architecture spec to operate correctly.

## Conventions

System docs are the densest surface of the project. Technical, specific, reference-grade. No marketing, no onboarding affect. Paragraphs carry reasoning; tables carry rules; code blocks carry truth.
