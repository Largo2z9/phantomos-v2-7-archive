---
name: validate-resources
type: curator
version: "1.1.0"
recommended_model: haiku
reasoning_pattern: null
description: >
  Audits workspace integrity: shared resources + brand context files.
  Detects orphaned files, broken references, schema violations, stale entries,
  duplicate IDs, index drift, and brand status inconsistencies.
  FR: "validate" "audit ressources" "check KB" "health check" "vérifie la cohérence" "audit workspace" "intégrité".
  EN: "validate" "audit resources" "check KB" "health check" "audit workspace" "integrity check".
permissions:
  reads: [brand, product, offer, profile, learning, strategy]
  writes: []
  mode: none
  subagent_safe: true
pipeline:
  preconditions: ingest-resource should have run at least once
  postconditions: none — agents can query after validate
disambiguates_against:
  audit-meta-account: "route to audit-meta-account when operator says 'audit' + platform context (Meta Ads), that's a platform-specific audit, not a workspace integrity check"
---

## v2.32 alignment (creative.schema v1.2)

- `meta.validation_status` accepts `oneOf [legacy ref | composite ref]`. Both shapes valid, no blocking on either. String form (legacy `validation-status.json`) and object form (`validation-state.json` with `status` + `confidence` + `confidence_source`) both pass.
- Pas de blocking validation sur la présence de `intent` vs `intent_mix` : les deux acceptables. Idem `craft_mode` vs (`overlay_density` + `brand_mark_present`). Backward compat additif strict.
- Flag MINOR (non-blocking) si un fichier `creative.json` v1.2 schema-version ne porte ni `intent_mix` ni `intent` (gap réel d'encoding). Idem si ni `overlay_density` ni `craft_mode`.

## Tone

Résultats en langage courant. Pas de codes de check, pas de noms de fichiers. "Ta fiche produit est complète" — pas "spec.json passes check 11b." Gaps = opportunités, jamais des erreurs.

# Skill: Validate Resources

Garbage collection + integrity checks for the full workspace.
Covers both `Ressources/` (shared KB) and `brands/` (context DB + OS).

---

## Checks — Shared Resources (run all)

### 1. Index ↔ Filesystem Sync

- Scan all `.json` files in `Ressources/{type}/` folders
- Compare against `index.json.resources[]`
- Flag: **orphan files** (on disk, not in index)
- Flag: **ghost entries** (in index, file missing)
- **Auto-fix**: Add orphans with `[UNVALIDATED]` tag. Remove ghosts.

### 2. Schema Validation

- For each resource JSON, validate against `Ressources/schemas/{type}.schema.json`
- Flag: **schema violations** (missing required, wrong types, pattern mismatches)
- **Report only**

### 3. ID Uniqueness

- Collect all catalogue entry IDs across all catalogues
- Flag: **duplicate IDs**, **prefix collisions**
- Check `index.json.id_prefixes` matches actual prefixes
- **Report only**

### 4. Broken References

- Read `refs` fields in every resource
- Check every referenced ID/path exists
- Flag: **broken outbound refs**, **missing inbound refs**
- **Auto-fix**: Add missing inbound refs

### 5. Staleness Detection

- Check `meta.updated` on all resources
- Flag: not updated in >90 days as **potentially stale**
- Flag: 0 inbound refs → **possibly obsolete**
- **Report only**

### 6. Ramification Check

- Catalogues with `entries.length > 12` → flag
- SOPs with `steps.length > 20` → flag
- **Report only**

### 7. Stats Integrity

- Recount `stats.by_type` and `stats.total_resources`
- **Auto-fix** if drifted

---

## Checks — Brand Context (per brand)

### 8. Wedge Completeness

- Check existence and non-empty status of wedge docs:
  - `brand.json` — meta.name filled? market.competitors has at least 1 entry?
  - At least 1 `products/{slug}/spec.json` with meta.name filled
  - At least 1 `audiences/{slug}/profile.json` with meta.name filled
- Extended checks (not blocking for wedge, but flagged):
  - `offers.json` exists for at least 1 product? If missing → flag `offers_missing` (degrades acquisition/piloting)
  - `strategy.json` has annual_goals? If empty → flag `strategy_empty` (degrades piloting)
  - `credentials.env` exists? If missing → flag `credentials_missing` (degrades platform access)
- **Update `status.json`**: Set `wedge_complete` true/false (core 3 only). Extended flags in `status.json.flags[]`.

### 9. Entity Completeness

- For each context file, check % of required fields filled vs empty
- Classify: `empty` (0%) | `draft` (<30%) | `partial` (30-80%) | `complete` (>80%)
- `learnings.json`: `empty` if 0 entries, `active` if ≥1 entry (no partial — it's append-only)
- `strategy.json`: `empty` if no goals, `draft` if goals only, `complete` if goals + monthly_targets + current_focus
- **Update `status.json.completeness`**

### 10. Freshness

- Check `meta.updated` or `updated` on every brand file
- Flag files not updated in >90 days
- `learnings.json`: check `entries[-1].date` (latest entry). No entries in >90 days → flag `learnings_stale`
- `strategy.json`: check `monthly_targets[-1].month`. If latest month is >2 months behind current → flag `strategy_stale`
- **Update `status.json.freshness`**

### 11. Cross-Reference Validation

- `profile.pain_points[].ref` → must exist in `spec.problems_solved[].problem_id` (iterate array)
- `profile.benefits[].ref` → must exist in `spec.benefits[].benefit_id` (iterate array)
- `offers.offer_groups[].offers[].product_refs[].slug` → must exist in `brand.products_index[].slug` (v2 schema — offers are NESTED under `offer_groups[]`, each offer has `product_refs[]`; legacy `offers.meta.product_slug` is v1.x only)
- `profile.meta.product_id` (if set) → must match a product slug in `products/`
- Flag: **broken cross-refs**
- **Report only** (data loss risk)

**Offer counting — always iterate `offer_groups[].offers[]`** (v2 schema). Example:
```python
count = sum(len(g.get("offers", [])) for g in offers_doc.get("offer_groups", []))
```
Never count via flat `offers_doc.get("offers", [])` — that's the legacy v1.x path and returns 0 on v2 files, producing the false "offers missing" flag. If a brand still has a v1.x flat-offers file, the count legitimately is 0 under v2 expectation; flag it as schema-migration-pending, not as missing data.

### 11b. _field_types Consistency

- Every top-level section in JSON must have at least one entry in `_field_types`
- No `_field_types` key should reference a field path that doesn't exist in the file
- Derived fields (`_field_types` = "derived") should not be empty when raw source fields are filled
- Flag: **unmapped fields**, **orphaned type entries**, **empty derived fields**
- **Report only**

### 12b. Learnings Lifecycle

- Scan `learnings.json.entries[]` dans chaque brand
- Détecter contradictions : si deux entries ont >60% tag overlap + dates différentes + facts sémantiquement opposés → marquer l'ancienne comme `status: "superseded"`, `superseded_by: "{newer_id}"`
- Cross-brand : si mode all-brands, détecter learnings similaires (même platform + >60% tag overlap) dans 2+ brands → ajouter au `promote-backlog.json`
  - Candidat structure :
    ```json
    {
      "learning_id": "LRN-001",
      "brand_slug": "glowco",
      "fact": "...",
      "tags": [...],
      "genericity": "sector",
      "tag_overlap_pct": 78,
      "matching_brands": ["glowco", "nestra"],
      "suggested_resource_type": "convention",
      "suggested_target": "conventions/meta-ads.json",
      "priority": "high",
      "flagged_date": "2026-04-04"
    }
    ```
- Flag learnings avec `status: "active"` + `date` > 180 jours → flag `[REVIEW]` (potentiellement obsolète)
- **Entrées actives > 200** → ajouter dans `todos.md → ## Flags` :
  ```
  [STORAGE] learnings.json {brand} : {N} entrées actives — recommandé de passer les plus vieilles à status:"archived".
  Tri suggéré : garder toutes les entries < 180 jours + les entries avec tags platform/compliance quel que soit l'âge.
  ```
  Ne jamais archiver automatiquement — décision opérateur uniquement.
- **Auto-fix** : marquer les contradictions. Écrire `promote-backlog.json`.

### 11c. Learnings Index Rebuild

- Lire `brands/{slug}/learnings.json`
- Pour chaque entry avec `status: "active"` → écrire dans `learnings-index.json` :
  ```json
  { "id": "LRN-001", "scope": "platform", "platform": "meta", "type": "workaround", "tags": ["ads", "creation"], "summary": "première phrase du fact tronquée à 80 chars" }
  ```
- Exclure les entries `status: "superseded"` ou `status: "archived"`
- **Auto-fix** : réécrire `learnings-index.json` entier à chaque validate (source of truth = learnings.json)

### 12. Update Todos Flags

- Collect all flags from checks 8-11 and 15-18
- Write to `brands/{slug}/todos.md` → `## Flags` section
- Remove resolved flags (issue no longer present)
- **Auto-maintained**: operator doesn't edit Flags section

### 13b. Skill Typology Enforcement

**CRITICAL:** scan every `.skills/skills/{name}/SKILL.md` frontmatter. **YOU MUST** validate:

- `type:` field present and non-null
- value is exactly one of: `producer | curator | capturer | orchestrator | navigator | builder`

**If missing, null, or invalid** → raise **blocking error**, not warning:
```
[SKILL-TYPE-INVALID] .skills/skills/{name}/SKILL.md → `type:` missing or invalid. Required: one of {producer, curator, capturer, orchestrator, navigator, builder}. See docs/system/patterns.md § Skill Taxonomy for binary tests.
```

**If present but contract suspicious** (e.g. `type: curator` with `recommended_model: opus` without a justification YAML comment next to the overridden field) → warning:
```
[SKILL-TYPE-OVERRIDE-UNJUSTIFIED] .skills/skills/{name}/SKILL.md → overrides default contract without justification. Expected: `# override: <reason>` YAML comment next to the overridden field.
```

**Rationale**: with skill count growing over time, unenforced taxonomy drifts to irrelevance. Blocking validation keeps the typology load-bearing. See `docs/system/patterns.md § Skill Taxonomy § Enforcement`.

---

### 13. CLAUDE.md Size Audit

- Scan all `CLAUDE.md` files: root + all `brands/{slug}/`
- Flag: root CLAUDE.md > 150 lines → `[SPLIT-CANDIDATE]`
- Flag: brand CLAUDE.md > 80 lines → `[SPLIT-CANDIDATE]`
- **Report only** — suggest which sections to extract to docs/system/architecture.md or brand-specific docs
- Recommend target sections for extraction: verbose sections (Tiers, Session Relay, Communication Rules, Rules)

### 14. Update Status Timestamps

- Update `status.json.last_activity` to current ISO timestamp (since validate produces output impact)
- No session-state.md activity log entry needed (validate is read-heavy, not write-heavy on brand content)

### 15. Custom Entities — Filesystem Walk (V1.5)

Extends check 1 to the extension layer.

- Walk every `brands/*/custom/*/` folder. For each entity type directory:
  - Verify presence of `schema.json`. Missing → `MAJOR: custom entity {type} has no schema.json`.
  - Verify presence of `README.md`. Missing → `MINOR: custom entity {type} has no README.md`.
  - Verify the type has an entry in `index.json → extensions[]`. Missing → `MAJOR: custom entity {type} not registered in index`.
- Walk `index.json → extensions[]`. For each registered entry:
  - Verify the referenced folder and schema file exist on disk. Missing → `MAJOR: orphan extension entry {type} in index`.

### 16. Custom Schema Canon Validation (V1.5)

Extends check 2 to custom entity schemas.

- For every `brands/*/custom/*/schema.json`:
  - Verify it declares `_version`, `_schema`, `_field_types`. Missing → `MAJOR: custom schema violates canon`.
  - Validate every instance file in the same folder against this schema. Instance violation → `MAJOR: instance {file} violates schema {type}`.
- For every sidecar `brands/*/*.extensions.json` and `brands/*/{products,audiences}/*/*.extensions.json`:
  - Verify `_extends` field points to a valid core entity name.
  - Verify sidecar does not redefine fields already present in the core schema (append-only discipline). Override → `MAJOR: sidecar redefines core field {name}`.

### 17. Reserved Names Collision (V1.5)

Blocks custom entity names that would collide with core.

- Reserved names (case-insensitive): `brand`, `product`, `offer`, `profile`, `learnings`, `strategy`.
- Scan every `brands/*/custom/{type}/` folder name. Match against reserved list → `CRITICAL: reserved name collision on custom entity {type}`.
- Also scan `index.json → extensions[].type` for the same check.

### 18. Sidecar Coherence (V1.5 — flag only)

Flags potential sidecar semantic divergence with the core entity.

- For every sidecar, list field names that could be semantic neighbors to core fields (heuristic match on substring or lexical similarity — `currency`, `locale`, `timezone`, `unit`, `language`, etc.).
- Output as `INFO: sidecar field {x} may overlap with core field {y}, review manually`.
- This check flags, does not block. Automated resolution of semantic divergence is pending V1.x.

---

## Output Format

```
## Validation Report — {date}

### Verdict
{Une ligne. Toujours en premier. En langage opérateur, jamais de jargon technique.}

Prêt. Tu peux bosser sur {brand}.
Utilisable mais incomplet. Il manque {X} avant de lancer {action}.
Pas utilisable tel quel. {raison en une phrase + action immédiate}.

Exemples :
Prêt. Tu peux bosser sur Glowco.
Utilisable mais incomplet. Il manque le problème principal du client avant de lancer une campagne Meta.
Pas utilisable tel quel. Ta fiche marque est vide. Lance setup-brand pour configurer la marque.
```

Tout ce qui suit (Summary, Auto-Fixed, Manual Action Required...) est affiché après le verdict. L'opérateur voit la réponse à "est-ce que je peux bosser ?" en premier, le détail technique en second.

---

```

### Résumé
- Ressources partagées analysées : {N}
- Fichiers brand analysés : {N}
- Problèmes trouvés : {N} ({N} corrigés automatiquement, {N} à faire)
- Niveau 1 complet : {oui/non par brand}

### Auto-Fixed
- [fix] {description}

### Points à corriger manuellement
- [données manquantes] {description opérateur — ex: "un champ n'est pas catalogué dans la fiche produit {produit}"} — {action exacte}
- [référence cassée] {description — ex: "le profil audience référence un problème qui n'existe pas dans la fiche produit"} — vérifier que {ID} est bien présent dans {entité concernée en français}
- [données vieilles] {entité concernée en français — ex: "stratégie Glowco"} pas mise à jour depuis {date} — ingest des mises à jour si disponibles
- [à décomposer] {ressource concernée en français} : {N} entrées, dépasse la limite recommandée — à découper en sous-listes si tu veux améliorer les performances
- [fichier trop long] {fichier concerné en français} : {N} lignes — certaines sections peuvent être externalisées

→ **Règle absolue** : aucun path fichier, aucun code technique (`schema_11b`, `wedge_incomplete`, `_field_types`…). Toujours décrire le problème en termes métier + l'action concrète pour le régler.

### Statut par brand
- {brand}: Niveau 1 {complet/incomplet} | {N} points à corriger

### Learnings Health
- {brand}: {N} active | {N} superseded | {N} archived | {N} candidates for promotion
- Contradictions detected: {list}
- Review needed: {learnings > 180 days}

### Context Level (tier-aware)

Niveau de contexte : {brand}
  Niveau 1 (MVP)    : {complet | X/3 éléments manquants}
  Niveau 2 (Enrichi): {complet | X éléments optionnels à ajouter}
  Niveau 3 (Opérationnel): {complet | disponible quand tu auras des ventes}

Tier 1 checks (= wedge):
- brand.json: meta.name + positioning.value_proposition + tone_of_voice.style filled
- ≥1 spec.json: meta.name + pricing.price + benefits (≥1) + problems_solved (≥1) filled
- ≥1 profile.json: meta.name + demographics (≥1 field) + pain_points (≥1) filled

Tier 2 checks (non-blocking, suggestions):
- benefits[].chain or pain_points[].chain filled on any entity
- brand.market.competitors has ≥1 entry
- ≥1 offers.json exists with ≥1 entry in `offer_groups[].offers[]` (v2 schema — see § 11 counting rule)
- tone_of_voice has banned_words or frequent_words

Tier 3 checks (non-blocking, contextual):
- financials has ≥2 non-null fields
- strategy.json has ≥1 annual_goal
- seasonality has peak_periods

### Next Actions
For each missing element, include the exact phrase the operator should say:
- "{brand}: brand incomplete" → Dis "Ingest ces infos sur {brand}" et ajoute : {liste des champs manquants}
- "{brand}: offers empty" → Dis "Ingest cette offre pour {product}" et décris : prix, type d'offre, dates
- "{brand}: audience missing" → Dis "Ingest ce profil client pour {brand}" et décris : qui ils sont, leurs problèmes, leurs objections
- "{brand}: stale" → Dis "Ingest ces mises à jour pour {brand}" et ajoute les infos récentes
- "broken-ref" → Vérifier que les IDs référencés existent (ex: PROB-01 dans spec.json si profile.json le référence)

Use plain language. No technical jargon. Each action = one sentence starting with "Dis" + the exact words to type.

**Tier framing rule**: Present Tier 2/3 gaps as opportunities ("pour améliorer la qualité"), never as errors. Only Tier 1 gaps are flagged as blocking.
```

Append report to CHANGELOG.md.

**CHANGELOG.md rotation** : après append, compter le nombre d'entrées `## v` dans CHANGELOG.md.
- Si ≤ 50 → rien à faire.
- Si > 50 → déplacer les entrées les plus anciennes (au-delà de 50) dans `CHANGELOG_archive.md` (append en bas, jamais supprimer). Conserver les 50 plus récentes dans CHANGELOG.md. Signaler : "CHANGELOG archivé — {N} entrées déplacées vers CHANGELOG_archive.md."

---

## Post-Validate Usage Guide

After reporting, if `wedge_complete = true` for at least one brand, append a **usage bridge** to the output. This is the single most important UX moment — the user just invested 15-30 min and needs to know what to do next.

### When wedge_complete = true:

```
Contexte prêt. Tes agents peuvent travailler.

Essaie maintenant :
→ "Écris une description produit pour {product_name}"
→ "Génère 5 hooks publicitaires pour {audience_name}"
→ "Rédige un email de lancement pour {brand_name}"
→ "Analyse mes concurrents et propose un angle de différenciation"
→ "Prépare un brief créa pour une campagne Meta"

Tes agents puisent automatiquement dans le contexte que tu viens de configurer.
Pas besoin de re-expliquer ta marque — c'est déjà fait.

Pour enrichir plus tard : "Ingest [nouvelles infos] pour {brand_name}"
Pour vérifier la santé : "Validate {brand_name}"
```

Replace `{product_name}`, `{audience_name}`, `{brand_name}` with actual values from the brand data.

### When wedge_complete = false:

```
Contexte incomplet. Tes agents peuvent travailler, mais la qualité sera limitée.

Ce qui manque :
{list from Next Actions section}

Une fois complété, tes agents pourront :
→ Générer du contenu ciblé (hooks, descriptions, emails)
→ Analyser tes concurrents avec le bon contexte
→ Piloter tes campagnes avec les bons KPIs
```

### Hard rule: ALWAYS display the usage bridge. Never end validation without showing what comes next.

---

## Modes

### Default: Single brand

Operator says "validate {brand}" or "health check {brand}" → run checks 1-14 on that brand + checks 15-18 on its extensions + shared resources.

### All brands mode

Operator says "validate all", "validate everything", "health check global", or "workspace status" → run checks on ALL brands:

1. List all brand slugs: scan `brands/*/brand.json` (skip `_TEMPLATE/`, `_EXAMPLE/`)
2. Run checks 1-7 (shared resources) — once
3. Run checks 8-14 per brand, plus checks 15-18 on each brand's extensions
4. Aggregate results into `workspace-status.json` (root level):

```json
{
  "generated": "2026-04-04T12:00:00Z",
  "template_version": "1.1.0",
  "brands_count": 3,
  "brands": {
    "{slug}": {
      "wedge_complete": true,
      "completeness_summary": "brand:complete, products:2/3 complete, audiences:1/2 partial",
      "flags_count": 2,
      "stale_files": 0
    }
  },
  "shared_resources": {
    "total": 12,
    "orphans": 0,
    "ghosts": 0,
    "schema_violations": 1
  },
  "health": "healthy | degraded | critical"
}
```

**Health rules:**
- `healthy` = all brands wedge_complete + 0 critical flags
- `degraded` = at least 1 brand incomplete OR >0 schema violations
- `critical` = >50% brands incomplete OR broken cross-refs in multiple brands

5. Print summary table in report output:

```
### Workspace Overview
| Brand | Wedge | Flags | Stale |
|-------|-------|-------|-------|
| acme  | ok    | 0     | 0     |
| xyz   | ko    | 3     | 1     |

Health: degraded
```

**workspace-status.json is auto-maintained by validate only.** Same authority rule as brand status.json.

---

## Hard Rules

- **Never delete files** — only flag
- **Auto-fix only safe ops**: index sync, inbound refs, stats, status.json, workspace-status.json, todos flags
- **Schema violations and duplicates** = report only
- **Run ALL checks every time** — no partial validation (mode incrémental = V2)
- **Validate = autorité unique** sur status.json, workspace-status.json, cross-refs, et stats. Aucun autre skill n'écrit dans ces fichiers.
- **Brand status.json is the only file validate writes in brands/** (+ todos.md flags)
- **workspace-status.json is the only cross-brand aggregation file** — lives at workspace root

---

## v1.8 Validation Rules (2026-04)

Le schéma v1.8 est backward-compatible. Les contraintes additionnelles à vérifier :

**spec.json v1.8 :**
- `specs.composition[]` accepte string OR objet structuré (anyOf). Si objet, `ingredient` requis.
- `specs.posology.recommended_daily_servings` — number si présent
- `specs.contraindications.age_min/max` — integer ≥ 0 si présent
- `nutrition_facts.nutri_score_grade` — enum ["A","B","C","D","E"] ou null
- `nutrition_facts.allergens[]` — enum EU14 + "oats" (nouvelle valeur)
- `dietary_tags[]` — enum étendue (caffeine_free, bio, raw, chicory_based, clean_beauty, cruelty_free en plus)
- `perishability.period_after_opening_months` — number si cosmétique

**offers.json v1.8 :**
- `contents.duration_type` — enum ["calendar","usage_days","servings"] si présent
- `pricing.price_per_unit.unit` — enum-locked à 22 valeurs (gram, kg, ml, l, serving, dose, day, month, piece, meter, m2, load, wash, application, capsule, tablet, sachet, bottle, pack, count, portion, unit)
- `incentives.duration_tiers[].duration_months` — integer > 0
- `incentives.loyalty.tiers[]` — structure libre si présent

**Règle :** Un instance en v1.7 doit aussi valider sous v1.8 (backward compat). Si échec → flagger comme régression.

**Stamping:** read expected `_version` values from `brands/_TEMPLATE` (living source of truth) and verify each file in a fresh instance matches the corresponding entity. Current values (2026-04-23): `brand.json _version=2.1`, `products/{slug}/spec.json _version=1.8`, `products/{slug}/offers.json _version=2.0`, `audiences/{slug}/profile.json _version=1.2`. Never hardcode "1.8" as a universal version — each entity has its own schema line. The field is `_version`, not `_template_version` (legacy terminology drift).
