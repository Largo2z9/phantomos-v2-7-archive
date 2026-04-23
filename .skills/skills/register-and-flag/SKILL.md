---
name: register-and-flag
type: curator
version: "1.0.0"
recommended_model: haiku
description: >
  Sub-skill of scaffold-extension. Registers a newly scaffolded custom entity in
  `index.json → extensions[]` and adds a tracking entry to `brands/{slug}/todos.md`.
  Sidecars are skipped (convention-discovered, not indexed). Final step of the orchestrator
  pipeline before operator-facing confirmation.
  Invoked by scaffold-extension Phase 9.
permissions:
  reads: [index, brand]
  writes: [index, brand.todos]
  mode: direct
  subagent_safe: true
pipeline:
  preconditions: files scaffolded (Phase 7), optional skill stub created (Phase 8)
  postconditions: extension registered, adoption todo flagged, post-write validate-resources auto-triggered
---

# Skill: Register and Flag

Closes the scaffold pipeline by registering the new extension in the central index and flagging it for adoption in the brand's todos.

## Method

### Step 1 — Index registration (custom entities only)

For custom entities, append an entry to `index.json → extensions[]` via `.skills/write-to-context.py`:

```json
{
  "type": "{entity_type}",
  "scope": "{brand | workspace}",
  "schema": "brands/{slug}/custom/{entity_type}/schema.json",
  "cross_refs": [{"field": "...", "target": "..."}],
  "owner_skill": "custom:{skill_name} | null",
  "registered_at": "{iso8601_now}"
}
```

For sidecars, skip this step entirely. Sidecars are convention-discovered (see `docs/system/extending.md`), not registered.

### Step 2 — Adoption flag in todos

Add an entry to `brands/{slug}/todos.md → ## In Progress`:

> *"[ ] Add your first entry to `{entity_type}` — created today. Capture at least one in the next 7 days to confirm the shape works. If blocked, revisit the setup."*

Two weeks later, if no instances exist, a future `validate-resources` run will flag the extension as `[UNUSED]` candidate for review.

### Step 3 — Post-write auto-validate

The root CLAUDE.md mutation rule automatically triggers `validate-resources` on the brand after any write to `custom/` or `.extensions.json`. This step does not re-trigger explicitly — just notes the expectation so the orchestrator can surface the result.

## Output to orchestrator

```
{
  "indexed": true | false,
  "todo_added": true,
  "validate_result": "passed | flagged | critical",
  "flags": []
}
```

## Hard rules

- Mutation gate on all writes.
- Sidecars never indexed. If the orchestrator passes a sidecar here by mistake, skip indexing and return `indexed: false`.
- Never write to index without matching schema file existing on disk (prevents ghost entries).
- Never create the todos.md entry if one with the exact same extension name already exists (idempotent).
