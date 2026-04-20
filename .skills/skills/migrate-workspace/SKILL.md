---
name: migrate-workspace
type: curator
version: "1.0.0"
recommended_model: sonnet
description: >
  Migrates an existing brand instance to match a newer template version.
  Compares instance structure against target template, generates a diff,
  proposes safe modifications (add fields, rename, deprecate). Never deletes data.
  Triggers: "migrate", "upgrade brand", "align with template", "check drift",
  "template version mismatch".
permissions:
  reads: [brand, product, offer, profile, learning, strategy]
  writes: [brand, product, offer, profile, learning, strategy]
  mode: direct
  subagent_safe: true
pipeline:
  preconditions: brand must exist (setup-brand completed). Target template version known.
  postconditions: validate-resources should run after migration to verify integrity.
---

## Tone

Explique les changements en langage courant : ce qui sera ajouté, ce qui change, ce qui ne bouge pas. Confirmer avant d'appliquer. Jamais de diff technique brut.

# Skill: Migrate Instance

Safely brings an existing brand instance in line with a newer template version.
Handles field additions, renames, restructuring, and deprecations — without data loss.

---

## When to Use

- Template has been updated (new fields, renamed sections, structural changes)
- Operator says "migrate", "upgrade brand", "align with template"
- validate-resources flags `_version` mismatch between instance and template
- Operator deploys a brand from an older template and needs to catch up

---

## Step 1 — Detect Version Gap

1. Read `brands/{slug}/brand.json._version` (instance version)
2. Read `brands/_TEMPLATE/brand.json._version` (target version)
3. Compare. If same → report "already up to date", exit.
4. Repeat for all entity files: spec.json, offers.json, profile.json

Output: list of files with version gaps.

---

## Step 2 — Generate Structural Diff

For each file with a version gap:

1. Read the instance file
2. Read the corresponding _TEMPLATE file
3. Compare structure (keys at all nesting levels):
   - **Added fields**: present in template, absent in instance
   - **Removed fields**: present in instance, absent in template (potential deprecation)
   - **Renamed fields**: heuristic — same position + similar name (fuzzy match)
   - **Type changes**: field was string → now object, array → now nested, etc.
   - **_field_types changes**: new entries, removed entries, type reclassifications

4. Check CHANGELOG.md for `[BREAKING]` tags between instance version and target version

Output: structured diff per file.

---

## Step 3 — Propose Migration Plan

For each diff item, classify and propose action:

| Diff Type | Action | Risk |
|-----------|--------|------|
| Added field (non-required) | Add with empty/default value | None |
| Added field (required) | Add empty + flag in todos.md | Low |
| Renamed field | Copy value to new key, keep old as `_deprecated_{old_name}` | Low |
| Restructured (flat → nested) | Remap values to new structure | Medium |
| Removed field | Keep as `_deprecated_{name}`, do NOT delete | None |
| Type change | Transform value if safe, flag if ambiguous | Medium |
| _field_types update | Merge new entries, keep existing | None |

**Present plan to operator before executing.** Format:

```
## Migration Plan — {brand} → v{target}

### Safe (auto-apply)
- brand.json: Add `social_media.tiktok` (empty)
- brand.json: Add `seasonality.events[]` (empty array)
- spec.json: Update `_field_types` (3 new entries)

### Needs Review
- brand.json: `tone` → `tone_of_voice` (rename — will copy value)
- profile.json: `triggers[]` restructured to `decision_process.triggers[]` (remap)

### Breaking Changes
- [BREAKING] brand.json: `kpis` section removed in v2.0 — will move to `_deprecated_kpis`

Apply safe changes now? (y/n)
Apply reviewed changes after confirmation? (one by one)
```

---

## Step 4 — Execute Migration

After operator approval:

1. **Backup**: Copy current file to `brands/{slug}/sources/_pre-migration_{filename}_{date}.json`
2. **Apply safe changes**: Add empty fields, merge _field_types
3. **Apply reviewed changes**: One by one, with operator confirmation
4. **Bump `_version`** in migrated files to match target
5. **Log in CHANGELOG.md**: `[MIGRATION] {brand} migrated from v{old} to v{new} — {N} fields added, {N} renamed, {N} deprecated`
6. **Update status.json**: clear version-mismatch flags

---

## Step 5 — Post-Migration Validation

1. Run validate-resources on the migrated brand
2. Report any new flags introduced by migration
3. Flag any required fields that are now empty (added during migration but need data)

---

## Hard Rules

- **Never delete data.** Removed fields → `_deprecated_{name}`. Operator decides when to truly purge.
- **Never overwrite non-empty fields** unless the operator explicitly approves.
- **Always backup before migrating.** Pre-migration snapshot-brand in `sources/`.
- **One brand at a time.** No batch migration without explicit operator request.
- **Present plan before executing.** Never auto-apply "Needs Review" or "Breaking Changes".
- **CHANGELOG is mandatory.** Every migration logged with version, date, and field-level detail.
- **_TEMPLATE is read-only.** Migration reads _TEMPLATE for comparison, never writes to it.

---

## Batch Mode (optional, operator-triggered)

Operator says "migrate all brands" or "batch migration":

1. List all brands (same scan as validate --all)
2. Generate migration plan per brand
3. Present consolidated summary: "3 brands need migration, 2 safe-only, 1 has breaking changes"
4. Execute per-brand with individual confirmation for breaking changes
5. Update workspace-status.json after all migrations

---

## v1.7 → v1.8 Migration Path (2026-04)

**100% backward compatible.** Aucune migration destructive requise.

**Changements v1.8 :**
- spec.json : +8 blocs optionnels (composition, posology, contraindications, origin, production_method, preparation, external_databases, target_suitability, durability)
- spec.json : +`nutrition_facts.allergen_sources`, +`nutri_score_grade`, +`perishability.period_after_opening_months`, +`perishability.expiry_date_required`
- spec.json : +6 dietary_tags, +"oats" dans allergens
- offers.json : +`contents.duration_type`, +`duration_servings`, +`cure_metadata`, +`incentives.duration_tiers`, +`loyalty`, +`offers[].tags`

**Étapes migration :**
1. Bumper `_template_version` → "1.8" dans spec.json et offers.json de chaque produit.
2. Ajouter les entries `_field_types` et `_changelog` depuis `_TEMPLATE/products/_example/`.
3. Ne PAS toucher aux données existantes. Les nouveaux blocs restent à null jusqu'à prochain snapshot.
4. Validation : relancer validate-resources, doit passer sans erreur.

**Pas besoin de re-snapshot.** Les instances v1.7 restent valides en v1.8. Enrichissement opt-in au prochain refresh.
