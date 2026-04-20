---
name: scaffold-extension
type: orchestrator
version: "1.0.0"
recommended_model: sonnet
description: >
  Orchestrator for building a new extension in PhantomOS (custom entity, sidecar, or custom skill).
  Composes nine single-responsibility sub-skills for intent capture, schema drafting, naming
  validation, cross-reference checking, canon validation, file scaffolding, and index registration.
  Respects the three governance rules of the extension layer: declared schema, registered-or-discovered,
  README documenting purpose.
  Triggers:
    FR: "crée une extension", "ajoute un custom entity", "scaffold extension", "nouveau type de données",
        "ajoute un sidecar", "track X cross sessions", "scaffold"
    EN: "scaffold extension", "create custom entity", "new data type", "add sidecar",
        "scaffold a tracker for X", "build extension"
permissions:
  reads: [brand, resource, index]
  writes: [brand.custom, brand.extensions, index, skill.custom, brand.todos]
  mode: direct
  subagent_safe: false
pipeline:
  preconditions: workspace deployed, docs/system/extending.md present, validate-resources skill available
  postconditions: extension registered + validated + operator informed
---

# Skill: Scaffold Extension

Orchestrator for scaffolding a new extension in the workspace. Covers custom entities, sidecar schemas, and the optional custom skill stub that populates the entity. Composed of nine single-responsibility sub-skills executed in strict sequence, with operator-visible checkpoints between phases.

See `docs/system/extending.md` for the extension layer architecture. See `docs/system/patterns.md § Skill Taxonomy` for type definitions.

---

## Invocation context — two modes of entry

**Mode intent-first** — operator apporte une **intention** sans donnée en main. *"Je voudrais tracker mes concurrents Meta dans le temps."* Le skill crée la structure (schema + dossier + README + stub skill optionnel), vide. L'opérateur peuple plus tard.

**Mode data-first** — operator apporte une **donnée concrète** issue de son travail opérationnel (analyse, rapport, extraction structurée). *"Voici ma marge de contribution par channel sur Q1, range-la proprement."* Le skill parse la donnée, applique le gate 5-dimensions, et soit route vers l'existant (pas de scaffold), soit crée la structure ET peuple avec la donnée apportée en un seul flow.

Le gate `check-existing-coverage` en Phase 2 est le pivot. Dans les deux modes, la même logique :

- Si la donnée ou l'intention matche une entité core existante → route vers write_to_context sur cette entité, **aucun scaffold**.
- Si match sur sidecar ou custom entity existante → écrit dans l'existant, nouvelle instance ou enrichissement sidecar, **pas de nouveau scaffold**.
- Si match partiel avec un shared resource → scaffold une structure minimale qui cross-ref la ressource plutôt que dupliquer.
- Si genuinely new → scaffold complet. En mode data-first, le scaffold est suivi immédiatement du populate avec la donnée apportée.

**Invocation déclenchée par** :

- Opérateur dit *"scaffold", "crée une extension", "ajoute un sidecar", "range cette donnée", "intègre ce bloc dans mon contexte"*.
- `build-agent` Step 2b détecte un intent de type simple-extension et délègue.
- Main agent orchestration gate (voir `CLAUDE.md § Orchestration gate`) détecte qu'une requête opérateur nécessite soit un enrichissement structurel, soit l'intégration d'une variable opérationnelle.

---

## Pipeline

Execute the nine sub-skills in order. After each phase, surface a one-line status to the operator (unless the phase is silent by design). Halt at any phase if the operator refuses or if a validator returns a blocking error.

### Phase 1 — `analyze-extension-intent`

Capture the operator's intent. Classify: custom entity / sidecar / both / skill-only. Extract attributes: data shape (time-series / instance-per-item / aggregate), expected population mechanism (manual / scraper / derived), cross-references to core entities. Three focused questions maximum.

Output: structured intent object consumed by downstream phases.

### Phase 2 — `check-existing-coverage`

Run the pre-build analysis gate. Walks five dimensions in order: core entities, existing sidecars on the active brand, existing custom entities on the active brand, custom entities on sibling brands, shared resources. Returns a verdict :

- `route-to-*` → scaffold halts. The main agent routes the operator to the existing structure. The new extension is not needed.
- `partial-reuse` → scaffold proceeds but Phase 3 schema draft uses the matched references as `cross_refs` or ID pointers rather than duplicating fields.
- `genuinely-new` → scaffold proceeds with full scope.

Surface the verdict to the operator with the matched target (if any). Operator can override — force scaffold if they have a reason to duplicate — but the default is respect the gate.

### Phase 3 — `propose-schema-draft`

Generate a canon-compliant JSON Schema draft for the custom entity (or sidecar). Follows `_version`, `_schema`, `_field_types` conventions. Uses patterns from `resources/schemas/` as structural reference. Integrates the cross-references and reused banks identified in Phase 2.

Operator sees the schema, approves or adjusts.

### Phase 4 — `validate-naming`

Verify the proposed entity type name. Blocks collision with core entity names (see `validate-resources` check 17). Enforces kebab-case, MECE with existing extensions in `index.json`, no duplicate.

If collision detected, propose alternative names and re-prompt.

### Phase 5 — `check-cross-refs`

Walk every declared cross-reference in the schema. Verify target core entities exist in the current workspace. Flag references that cannot resolve. Prevents broken refs at creation rather than at runtime.

Halts if any cross-ref is unresolved; operator must fix or drop the ref.

### Phase 6 — `validate-schema-canon`

Validate the draft schema against canon requirements (reuses logic of `validate-resources` check 16 applied pre-write). Checks `_version`, `_schema`, `_field_types` enum, required fields, no override of core fields for sidecars.

Halts on any schema canon violation.

### Phase 7 — `scaffold-entity-files`

Write the physical files to disk via `write_to_context`:
- `brands/{slug}/custom/{entity_type}/schema.json` (or `brands/{slug}/{entity}.extensions.json` for sidecar).
- `brands/{slug}/custom/{entity_type}/README.md` (canonical structure: purpose, cross-refs, field conventions).
- Empty or example instance file if requested.

For sidecars, only the `.extensions.json` file is written (no README, no folder — sidecars are discovered by convention).

### Phase 8 — `scaffold-skill-stub` (conditional)

If the intent includes a skill that populates the extension (common for scrapers, watchers, pipelines), generate a SKILL.md stub in `.skills/skills/custom/{skill_name}/`. The stub declares frontmatter (type, recommended_model, permissions referencing the new extension), a Tone section, and the pipeline skeleton. The operator fills in the execution logic afterward, or delegates to `build-agent` for the body.

Skipped if the operator does not need a populating skill (manual-only tracking, pure sidecar enrichment).

### Phase 9 — `register-and-flag`

For custom entities: add an entry to `index.json → extensions[]` via `write_to_context`, with `type`, `scope`, `schema` path, `cross_refs`, `owner_skill`, `registered_at`. For sidecars: skip (sidecars are convention-discovered, not registered — see `docs/system/extending.md`).

Add a flag entry to `brands/{slug}/todos.md → ## In Progress` tracking the adoption of the new extension (first data capture, first query).

Auto-triggered `validate-resources` runs post-write via the mutation rule in root CLAUDE.md, covering checks 15-18. Silent unless MAJOR or CRITICAL.

---

## Output to operator

After Phase 9 completes successfully, surface a concise recap in operator language:

> *"Ton `{type}` est prêt sur `{brand_slug}`. Forme validée. {N} champs, {N} références vers ton contexte existant. {Un petit skill '{name}' a été ajouté — tu le rempliras avec `build-agent` / à la main / je peux t'aider maintenant.} Tu peux commencer à l'utiliser en disant `{trigger phrase}`."*

Never expose file paths, JSON structure, or internal field names. The operator owns the extension conceptually, not technically.

---

## Halt conditions

- Phase 4 blocking collision without operator-approved alternative
- Phase 5 broken cross-ref without operator-approved drop
- Phase 6 schema canon violation without operator-approved fix
- Operator refuses any intermediate checkpoint

On halt, write nothing. The workspace remains in its previous state. Resume is possible later by re-invoking with the same intent.

---

## Hard rules

- Mutation gate on every write. Never direct JSON edits.
- Schema canon compliance is non-negotiable (checks 16, 17 are CRITICAL severity).
- Operator language throughout. Internal vocabulary (field_path, schema, index.json) never leaks to the operator surface.
- One thread question per turn across all phases.
- Voice canon 100%. No triple-parallel, no coach-phrase, no decorative metaphor.

---

## Related canon

- `docs/system/extending.md` — extension layer architecture, three governance rules.
- `docs/system/patterns.md § Skill Taxonomy` — type definitions.
- `docs/system/agent-contracts.md` — mutation gate rules.
- `brands/_TEMPLATE/custom/_EXAMPLE/competitor_pricing/` — canonical reference example.
- `.skills/skills/validate-resources/SKILL.md § Checks 15-18` — post-write integrity checks.
- `.skills/skills/build-agent/SKILL.md` — delegates here for simple extension intents.
