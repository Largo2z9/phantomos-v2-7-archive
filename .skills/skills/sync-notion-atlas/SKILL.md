---
name: sync-notion-atlas
type: orchestrator
version: "1.1.0"
isolation_scope: brand_only
layer: 1
recommended_model: sonnet
subagent_safe: false
mode: proposed
operator_facing: true
reasoning_pattern: null
patch_notes:
  v1.1.0: "v2.58 coverage extend · friction.{current_workarounds, resolution_state, cross_refs.*} mapping enrichi · roadmap.{mix[], relations} mapping + denormalized view auto-computed. Closes 4 orphans audit v2.57. Phase B push toujours stubbée v2.58. Backward compat strict additif."
  v1.0.0: "v2.57 Phase A pull-only MVP shipped. Bridge Notion → PhantomOS pour les 11 collections canon stride-up (Produits, Specs, Mécanismes, Bénéfices, Personae, Pain Points, Angles, Objections, Frictions usage, Roadmap, Full funnel Meta). Mappings canon docs/system/notion-bridge-doctrine.md. Mutation gate strict (write-to-context.py mode=proposed) + isolation_scope brand_only. Phase B push + Phase C diff stubbés mais inactifs v1.0.0. Cross-ref doctrines · notion-bridge-doctrine.md (source canon) · compositional-cartography.md §4 mappings · brand-isolation-discipline.md · investigation-posture.md (5 sections close) · schema-encoding-discipline.md (mutation rule + _field_types)."
description: >
  v1.1.0 (v2.58 coverage extend) · friction.{current_workarounds, resolution_state, cross_refs.*} mapping enrichi · roadmap.{mix[], relations} mapping + denormalized view auto-computed. Closes 4 orphans audit v2.57. Phase B push toujours stubbée v2.58.
  v1.0.0 baseline Phase A pull-only MVP. Synchronise un workspace Notion (canvas
  stride-up avec 11 collections canon · Produits, Specs, Mécanismes, Bénéfices,
  Personae, Pain Points, Angles, Objections, Frictions usage, Roadmap, Full funnel
  Meta) vers les entités canon PhantomOS d'une brand existante. Mode
  --mode=pull {notion_url} (Phase A v2.57). Modes --mode=push (Phase B post-MVP
  v2.58) et --mode=diff (P2 deferred v2.59) stubbés mais pas implémentés v1.0.0.
  Mutation gate strict (write-to-context.py mode=proposed), isolation_scope
  brand_only, stateless idempotent. Source of truth canon = PhantomOS, Notion = UI
  optionnelle mirror.
  FR: "sync notion atlas {brand_slug}" "pull notion vers phantom" "import notion vers {brand_slug}" "synchronise mon notion avec phantom" "tire mon atlas notion dans phantom".
  EN: "sync notion atlas" "pull notion to phantom" "import from notion" "sync workspace from notion".
permissions:
  reads: [brand, product, offer, profile, angle, friction, roadmap, creative]
  writes: [product, offer, profile, angle, friction, roadmap, creative]
  mode: proposed
  subagent_safe: false
pipeline:
  preconditions: |
    brands/{slug}/brand.json non-empty · MCP Notion connecté côté Claude Code
    opérateur (verify via claude mcp list) · schemas canon présents
    (brand/spec/offer/profile/angle/friction/roadmap/creative).
  postconditions: |
    validate-resources triggered silently post toutes stages · pending-validations.md
    enrichi · opérateur arbitre accept/reject/correct par collection ou batch.
consumes:
  - brand.schema
  - spec.schema
  - offer.schema
  - profile.schema
  - angle.schema
  - roadmap.schema
  - friction.schema
  - creative.schema
produces_proposals_for:
  - brands/{slug}/products/{p}/spec.json
  - brands/{slug}/products/{p}/offers.json
  - brands/{slug}/audiences/{a}/profile.json
  - brands/{slug}/angles/{ANG-NN}.json
  - brands/{slug}/frictions/{FRC-NN}.json
  - brands/{slug}/roadmap.json
  - brands/{slug}/creatives/{CRT-NN}.json
  - brands/{slug}/funnel.json
triggers_fr:
  - "sync notion atlas {brand_slug}"
  - "pull notion vers phantom"
  - "import notion vers {brand_slug}"
  - "synchronise mon notion avec phantom"
  - "tire mon atlas notion dans phantom"
triggers_en:
  - "sync notion atlas"
  - "pull notion to phantom"
  - "import from notion"
  - "sync workspace from notion"
disambiguates_against:
  snapshot-brand: "route to snapshot-brand quand l'opérateur fournit une URL e-commerce brand (scrape direct PDP / homepage / collection). sync-notion-atlas est UPSTREAM différent · pull depuis workspace Notion structuré opérateur, pas scrape brand publique. Pas la même source, pas la même richesse data."
  import-asset: "route to import-asset pour assets visuels individuels (logo, badges, mascotte) ou par auto_multi sur une brand URL. sync-notion-atlas couvre la data structurée canon des 11 collections, pas les assets binaires."
  ingest-resource: "route to ingest-resource pour docs ponctuels (brief PDF, transcript interview, copy doc, reviews export). sync-notion-atlas couvre le workspace Notion systémique 11 collections inter-reliées, pas l'enrichissement par document isolé."
---

## Tone

Présenter le sync comme un acte d'ingestion structuré, jamais comme un data dump. *"J'ai cartographié ton workspace Notion · 9 collections sur 11 attendues détectées, X rows pulled, Y propositions stagées"*, JAMAIS *"sync-notion-atlas pull executed at 0.73 confidence on 47 rows"*. Le bridge est un mécanisme, pas un héros. L'opérateur voit l'effet (proposals stagées en cours de validation), jamais la plomberie.

---

# Skill: Sync Notion Atlas

Bridge Notion → PhantomOS Phase A pull-only MVP. Synchronise les 11 collections canon stride-up d'un workspace Notion vers les entités canon PhantomOS d'une brand existante via le mutation gate strict (`write-to-context.py --mode=proposed`).

PhantomOS = source of truth canonique. Notion = UI optionnelle mirror. Le bridge est asymétrique par design (cf. `docs/system/notion-bridge-doctrine.md § Le principe canon`).

Phase A v1.0.0 ship · `--mode=pull` uniquement. `--mode=push` deferred v2.58. `--mode=diff` deferred v2.59.

---

## Step 0 · DRGFP prerequisite check (L1 silent · L2 gate · L3 degraded)

Avant toute opération, run le canon DRGFP `docs/system/dependency-resolution-protocol.md` ·

**L1 silent** (input prerequisites) ·
- `brand_slug` fourni en argument ?
- `notion_workspace_url` fourni en argument ?
- `brands/{brand_slug}/brand.json` existe ET `identity.name` non-empty ?

Si NON sur l'un de ces 3 · refuse to ship · surface en clair · *"Il me manque {ce_qui_manque} pour démarrer. Brand existante requise (lance setup-brand si besoin), URL workspace Notion requise."*. Stop.

**L2 gate** (Layer 1 MCP infrastructure check, cf. `docs/system/connectivity-layering.md`) ·
- MCP Notion connecté côté opérateur ? Verify via `claude mcp list` OR test ping silencieux avec `mcp__claude_ai_Notion__notion-search` (query trivial).
- Si refus / non-réponse / MCP absent · AskUserQuestion explicit ·

```
Le bridge Notion a besoin du serveur MCP Notion configuré côté ton Claude Code.
Je ne le vois pas actif sur ta session.

(a) Setup MCP Notion d'abord · je te guide via connect-mcp-server
(b) Abort · on reprend quand tu auras le MCP en place
(c) Use cached snapshot si dispo · si un sync Notion antérieur a déjà tourné, on lit le snapshot local
```

Pas de fallback silencieux. Le bridge requiert MCP actif.

**L3 degraded** (schemas canon v2.56+ requis) ·
- Verify presence de `resources/schemas/friction.schema.json` + `resources/schemas/roadmap.schema.json` + `resources/schemas/brief.schema.json`. Ces schemas sont v2.56+ pré-requis pour Phase A.
- Si absents · workspace-template stale détecté · flag explicite à l'opérateur · *"Le template workspace est antérieur à v2.56. Les schemas friction.schema + roadmap.schema sont requis pour le sync Phase A. Mets à jour le workspace via update-workspace avant de relancer."*. Refuse to ship. DRGFP gate strict.

Si Step 0 passe (3 checks L1 silent + L2 MCP actif + L3 schemas présents) · continue.

---

## Step 1 · Notion canvas discovery

**Goal** · cartographier la structure Notion (canvas root + 11 collections candidates) avant tout query massif.

**Sub-step 1.1 · Canvas root fetch** ·

```
mcp__claude_ai_Notion__notion-fetch
  url: {notion_workspace_url}
```

Retrieve canvas root + structure descendante (databases, pages enfants).

**Sub-step 1.2 · Collections matching** ·

```
mcp__claude_ai_Notion__notion-search
  query_filter: {parent canvas root id}
```

Pour chacune des 11 collections canon attendues, match par titre (case-insensitive, fuzzy léger acceptable) ·

| Collection canon attendue | Variantes acceptées (FR + EN) |
|---|---|
| Produits | Produits, Products, Product Catalogue |
| Specs | Specs, Specifications, Caractéristiques |
| Mécanismes | Mécanismes, Mechanisms, Mecaniques |
| Bénéfices | Bénéfices, Benefits, Avantages |
| Personae | Personae, Audiences, Personas, Audience Segments |
| Pain Points | Pain Points, Douleurs, Pains |
| Angles | Angles, Angles produits, Strategic Angles |
| Objections | Objections, Freins |
| Frictions usage | Frictions usage, Frictions, Usage Frictions |
| Roadmap | Roadmap, Roadmap angles/audiences, Planning |
| Full funnel Meta | Full funnel Meta, Funnel Meta, Meta Funnel, Full Funnel |

**Sub-step 1.3 · Surface cartography à l'opérateur** ·

Format opérateur-facing (5 sections investigation-posture, mini-cycle Step 1) ·

> *Observé · canvas Notion `{nom_canvas}` cartographié ({date}, {durée_scan}).*
>
> *{N} collections sur 11 attendues détectées ·*
> *{liste matched · pour chaque · nom Notion détecté ↔ collection canon}*
>
> *Non-détectées ({M}) · {liste unmatched · collections canon manquantes dans Notion}*
>
> *On continue le pull sur les {N} collections détectées, ou tu valides la cartographie d'abord (genre · ajuster un nom Notion pour matcher, ou confirmer que la collection manquante n'existe pas vraiment) ?*

**Sub-step 1.4 · AskUserQuestion si corpus thin** ·

Si `N < 8` (moins de 8 collections sur 11 matched) · AskUserQuestion explicit ·

```
Cartographie Notion thin · {N}/11 collections détectées seulement.
Les non-détectées · {liste}.

Risque · pull partiel, certaines entités PhantomOS resteront vides
(frictions / roadmap / angles selon manquantes).

(a) Continue quand même · pull les {N} détectées, accept que {M} entités PhantomOS restent à null
(b) Pause · tu mets à jour Notion (rename + create) puis on relance
(c) Schema map override · si tes collections ont des noms custom non-canon, donne-moi le mapping manuel
```

Pas de pull silent sur corpus thin. L'opérateur arbitre.

Si `N >= 8` · continue silent vers Step 2 (cartographie suffisante).

---

## Step 2 · Collections query

**Goal** · pour chaque collection matched Step 1, pull les rows.

**Sub-step 2.1 · Per-collection query** ·

Pour chaque collection matched (dict `{collection_name → notion_db_id}`) ·

```
mcp__claude_ai_Notion__notion-query-database-view
  database_id: {notion_db_id}
```

Stocker en mémoire dict ·

```
collections_data = {
  "Produits": [row1, row2, ...],
  "Personae": [row1, row2, ...],
  ...
}
```

**Sub-step 2.2 · Cap corpus large** ·

Cap 200 rows par collection pour Phase A MVP. Si une collection retourne > 200 rows ·

> *La collection {nom} a {X} rows. Je cap à 200 pour ce sync v1.0.0 (Phase A MVP). Tu veux que je pull les 200 premières ({ordre Notion natif), ou tu préfères filtrer (par date, par status, autre) ?*

L'opérateur arbitre. Cap respecté.

**Sub-step 2.3 · No-op si collection vide** ·

Si une collection matched retourne 0 rows · note `{collection_name: []}` silent, continue. Pas de stage de proposal vide. L'opérateur le verra dans la synthèse Step 6.

---

## Step 3 · Mapping Notion vers PhantomOS canon

**Goal** · pour chaque row Notion pullée, appliquer le mapping canon documenté dans `docs/system/notion-bridge-doctrine.md § Mappings cross-platform`.

### Table de mapping résumée (canon)

| Collection Notion | Schema PhantomOS | Storage Path |
|---|---|---|
| Produits | `spec` + `offer` | `brands/{slug}/products/{p}/spec.json` + `offers.json` |
| Specs | `spec.composition` + `spec.specs.*` | subfields spec.json (group by product cross-ref) |
| Mécanismes | `spec.mechanisms[]` | subfield spec.json |
| Bénéfices | `spec.benefits[]` (emotional_signal + latency v2.56) | subfield spec.json |
| Personae | `profile` (audience-level entity) | `brands/{slug}/audiences/{a}/profile.json` |
| Pain Points | `profile.pain_benefit_chain[]` + `pain_category` v2.56 | subfield profile.json |
| Angles produits | `angle` | `brands/{slug}/angles/{ANG-NN}.json` |
| Objections | `profile.objections[]` enrichi v2.56 + xref `angle.tension` | subfields profile.json + angle.json |
| Frictions usage | `friction` NEW v2.56 (v1.1.0 · enrichi `current_workarounds`, `resolution_state`, `cross_refs.{objection_ids, pain_point_ids}`) | `brands/{slug}/frictions/{FRC-NN}.json` |
| Roadmap | `roadmap` NEW v2.56 (v1.1.0 · enrichi `mix[]`, `relations.{angle_ids, audience_slugs, product_slugs, creative_ids}` denormalized view) | `brands/{slug}/roadmap.json` (singleton) |
| Full funnel Meta | `creative` + `funnel` | `brands/{slug}/creatives/{CRT-NN}.json` + `funnel.json` |

Full doctrine canon + cohérence cross-collections (relations Notion devenant cross_refs PhantomOS) · `docs/system/notion-bridge-doctrine.md`.

### Mappings enrichis v1.1.0 (Phase A coverage extend)

#### Frictions usage · enrichments v1.1.0

Quand collection Notion `Frictions usage` est query, mapper additionnellement vers ·

| Notion property | PhantomOS field | Type |
|---|---|---|
| `Workarounds` ou `Solutions actuelles client` (multi-text) | `friction.current_workarounds[]` | array text |
| `Statut résolution` (select) | `friction.resolution_state` | enum [unresolved · in_progress · resolved · accepted] |
| `Cross-ref objections` (relation → Objections, multi) | `friction.cross_refs.objection_ids[]` | array (OBJ-NN canonical IDs) |
| `Cross-ref pain points` (relation → Pain Points, multi) | `friction.cross_refs.pain_point_ids[]` | array (PNT-NN canonical IDs v1.7 NEW) |

Stage chaque field via write-to-context.py mode=proposed (cf. Step 4 patterns). Pour `cross_refs.*`, résoudre les relations Notion vers PhantomOS IDs canonical (OBJ-NN + PNT-NN) avant stage.

#### Roadmap · enrichments v1.1.0

Quand collection Notion `Roadmap [angles/audiences]` porte property `Mix axis` (select · audience · angle · product · funnel · creative) + property `Weight` (number 0-1), mapper vers `roadmap.mix[]` array.

Post-mapping rows roadmap, computer aggregat denormalized auto-computed · collecter tous les `phase.priorities[].angle_ids` + tous les `production_status[].entity_id` → group by entity_type → populate `roadmap.relations.{angle_ids, audience_slugs, product_slugs, creative_ids}`. Vue denormalized auto-générée post Step 4, pas operator-fournie.

### Tags universels mapping (épistemic)

Les 3 tags universels stride-up Notion mappent sur l'encodage épistemic PhantomOS (cf. `docs/system/schema-encoding-discipline.md`) ·

| Notion (select/text property) | PhantomOS field |
|---|---|
| `source` = `observed` | `_field_types: "observed"` per-field concerné |
| `source` = `inferred` | `_field_types: "derived"` per-field |
| `source` = `declared` | `_field_types: "stated"` per-field |
| `source` empty / null | `_field_types: "stated"` (default défensif) |
| `confidence` qualitatif `forte` | `meta.confidence: 0.9` (numeric, jamais surface opérateur) |
| `confidence` qualitatif `moyenne` | `meta.confidence: 0.7` |
| `confidence` qualitatif `faible` | `meta.confidence: 0.5` |
| `confidence` qualitatif `TRÈS faible` | `meta.confidence: 0.3` |
| `confidence` empty / null | `meta.confidence: 0.7` (default défensif pull Notion, à valider) |
| `validation_status` = `hypothesis` | `meta.validation_status: "hypothesis"` (via `_shared/validation-status.json` enum) |
| `validation_status` = `tested` | `meta.validation_status: "tested"` |
| `validation_status` = `validated` | `meta.validation_status: "validated"` |
| `validation_status` = `scaled` | `meta.validation_status: "scaled"` |
| `validation_status` = `fatigued` | `meta.validation_status: "fatigued"` |
| `validation_status` empty / null | `meta.validation_status: "hypothesis"` (default défensif) |

### Per-row mapping execution

Pour chaque row d'une collection ·

1. Lire row Notion → extract properties (title, fields custom, relations).
2. Map vers le schema PhantomOS cible (table ci-dessus).
3. Build l'objet JSON cible respectant le schema canon (validate-resources friendly).
4. Si row Notion a un champ vide (property null / empty) → laisser le champ PhantomOS vide / null. **JAMAIS** inférer pour combler. Notion = source of truth en mode pull. Hard rule absolue.
5. Compute confidence + _field_types selon tags universels (table ci-dessus).
6. Capture lineage · ajouter `_source: "sync-notion-atlas"` + `_notion_row_id: "{notion_row_id}"` + `_synced_at: "{ISO timestamp}"` pour traçabilité.

### Edge cases canonisés (cf. notion-bridge-doctrine.md § Edge cases)

- **Property type mismatch** (Notion `select` vs schema attend `multi_select`) · flag explicitement Section 4 synthesis, ne mute pas silencieusement. Opérateur arbitre.
- **Row Notion avec field schema-extension custom** (field qui n'existe pas dans canon PhantomOS) · flag, propose `scaffold-extension` post-sync. Pas d'invention.
- **Notion workspace structure non-canonique** (collection avec nom custom) · check si `~/notion-mappings/{brand_slug}.json` override existe (v2.60+ deferred). Sinon fallback détection heuristique Step 1. Si toujours non-matched · AskUserQuestion mapping manuel.

---

## Step 4 · Stage proposals via mutation gate

**Goal** · pour chaque entité PhantomOS construite Step 3, stage la mutation via le mutation gate canonique `write-to-context.py --mode=proposed`.

**Anti-pattern absolu** · JAMAIS hand-edit JSON sous `brands/{brand_slug}/`. JAMAIS bypass write-to-context. JAMAIS d'`Edit/Write/NotebookEdit` sur les `.json` brand-side (refusé runtime par mutation-guard PreToolUse hook). Toute mutation via write-to-context (`docs/system/schema-encoding-discipline.md § Mutation rule`).

### Stage execution pattern

Pour chaque entité buildée Step 3 ·

**Pattern A · Scaffold file (si entité brand-new, fichier inexistant)** ·

```bash
python3 .skills/write-to-context.py \
  --path "brands/{brand_slug}/{entity_path}#" \
  --value '{full canonical JSON respecting schema, with null placeholders for missing fields}' \
  --source agent \
  --confidence 0.7 \
  --mode direct
```

Mode `direct` requis pour scaffold initial (le mode `proposed` est rejected sur les writes-whole-file car corrompt les consumers ; cf. snapshot-brand Hard Rules § Write modes). Le scaffold pose la structure complète avec null placeholders.

**Pattern B · Stamp inferred fields (post-scaffold)** ·

Pour chaque field dont la valeur provient d'un row Notion ·

```bash
python3 .skills/write-to-context.py \
  --path "brands/{brand_slug}/{entity_path}#/{field_pointer}" \
  --value '{scalar or dict value}' \
  --source import \
  --confidence {0.9 | 0.7 | 0.5 | 0.3 selon Notion confidence qualitatif} \
  --mode proposed
```

Mode `proposed` stamp les `_proposed: true` + `_source: "import"` + `_confidence: N` au niveau du field, permet à l'opérateur d'accept/reject par mutation via `pending-validations.md` workflow.

`--source import` valeur enum (cf. write-to-context.py `VALID_SOURCES`), réservée aux ingestions externes structurées comme Notion.

### Pattern C · Stage enrichments v1.1.0 (Phase A coverage extend)

**C.1 · friction.current_workarounds[] + resolution_state** ·

```bash
python3 .skills/write-to-context.py \
  --path "brands/{brand_slug}/frictions/{FRC-NN}.json#/current_workarounds" \
  --value '["{workaround_1}","{workaround_2}"]' \
  --source import \
  --confidence 0.8 \
  --mode proposed

python3 .skills/write-to-context.py \
  --path "brands/{brand_slug}/frictions/{FRC-NN}.json#/resolution_state" \
  --value '"unresolved"' \
  --source import \
  --confidence 0.8 \
  --mode proposed
```

**C.2 · friction.cross_refs.{objection_ids, pain_point_ids} cross-DB resolution** ·

Quand collection Notion porte cross-relations (e.g. friction page mentionne objections OR pain_points via relation Notion), résoudre vers PhantomOS IDs canonical (OBJ-NN + PNT-NN v1.7 NEW). Stage ·

```bash
python3 .skills/write-to-context.py \
  --path "brands/{brand_slug}/frictions/{FRC-NN}.json#/cross_refs/objection_ids" \
  --value '["OBJ-01","OBJ-03"]' \
  --source agent \
  --confidence 0.8 \
  --mode proposed

python3 .skills/write-to-context.py \
  --path "brands/{brand_slug}/frictions/{FRC-NN}.json#/cross_refs/pain_point_ids" \
  --value '["PNT-02","PNT-05"]' \
  --source agent \
  --confidence 0.8 \
  --mode proposed
```

**C.3 · roadmap.mix[] mapping (axis + weight)** ·

```bash
python3 .skills/write-to-context.py \
  --path "brands/{brand_slug}/roadmap.json#/mix" \
  --value '[{"mix_id":"MIX-01","weight":0.4,"axis":"audience","target_id":"...","rationale":"..."}]' \
  --source agent \
  --confidence 0.8 \
  --mode proposed
```

**C.4 · roadmap.relations denormalized view auto-computed** ·

Post-mapping rows roadmap (Step 3 + Step 4 Patterns A-B-C.3 staged), computer aggregat denormalized · collecter tous les `phase.priorities[].angle_ids` + tous les `production_status[].entity_id` → group by entity_type → populate `roadmap.relations`. Stage ·

```bash
python3 .skills/write-to-context.py \
  --path "brands/{brand_slug}/roadmap.json#/relations" \
  --value '{"angle_ids":["ANG-01","ANG-03"],"audience_slugs":["..."],"product_slugs":["..."],"creative_ids":["CRT-12"]}' \
  --source agent \
  --confidence 0.9 \
  --mode proposed \
  --reason "Denormalized view auto-computed"
```

Vue denormalized auto-générée, pas operator-fournie. Permet drill-down rapide cross-entités sans re-parser phase.priorities[] runtime.

### Delegation à encode-batch (Haiku) pour batches > 5 mutations

Pour les collections volumineuses (typiquement Personae 5-20 rows × 10 fields = 50-200 mutations, ou Angles 10-30 rows × 5 fields), la délégation à `encode-batch` est canonique (cf. ingest-resource SKILL.md pattern) ·

```
Task tool invocation ·
- subagent_type: shared
- skill: encode-batch
- model: haiku
- prompt: |
    {
      "brand_slug": "{brand_slug}",
      "target_entities": [
        {"file_path": "brands/{brand_slug}/audiences/{a}/profile.json", "schema": "resources/schemas/profile.schema.json"},
        ... une entrée par audience à scaffolder ...
      ],
      "observations": [
        {"semantic_kind": "audience_name", "raw_value": "{notion_row.title}", "evidence": "notion row {row_id} title", "source": "import", "confidence_signal": "literal"},
        ... une observation par row Notion par field non-null ...
      ],
      "default_mode": "proposed"
    }
```

Le sub-agent Haiku map chaque `semantic_kind` → `field_path`, run `write-to-context.py` par mutation, rebuild snapshot, run `finalize-mutation-batch.py`. Retourne summary structuré (`mutations_count`, `files_touched`, `unmapped`, `finalize_exit_code`).

Pour batches ≤ 5 mutations (typiquement Roadmap singleton), inline `write-to-context.py` direct acceptable.

### Stage all or none discipline (partial)

Si une mutation individuelle échoue (validate fail intermédiaire, refus sécurité write-to-context, schema mismatch détecté in-flight) · log l'erreur, flag dans Section 4 synthesis, **continue le batch** sur les autres mutations. Pas de rollback automatique des mutations déjà stagées (anti-pattern destructive · l'opérateur arbitre via pending-validations.md ce qu'il retient).

---

## Step 5 · Trigger validate-resources silently

Post toutes les stages Step 4 · invoke `validate-resources` skill (haiku subagent_safe true) pour integrity check structural cross-brand.

```
Task tool invocation ·
- subagent_type: shared
- skill: validate-resources
- model: haiku
- prompt: "Run validate-resources on brand={brand_slug}. Silent unless MAJOR/CRITICAL findings."
```

Si MAJOR / CRITICAL errors remontés · flag explicitement dans Section 3 (Inconnu) ou Section 4 (Leviers) synthesis · l'opérateur sait que certaines entités stagées ont des problèmes structurels à traiter avant accept.

Si zero finding ou seulement MINOR · continue silent vers Step 6 (la synthèse Step 6 mentionnera la validation passée OK).

---

## Step 6 · Synthesis 5-section investigation-posture operator-facing

Output final canonique respectant `docs/system/investigation-posture.md` (5 sections explicites, jamais fusionnées en prose).

### Section 1 · Observé (faits sourcés)

Format structuré, faits avec ancrage source. Pas de prose narrative.

Exemple cible ·

> *Observé · pull Notion `{nom_canvas}` ({date}, {durée_total_sync})*
>
> *{N_collections} collections cartographiées sur 11 attendues ·*
> *  • Produits · {X1} rows pulled → {Y1} spec.json + {Z1} offers.json stagés*
> *  • Personae · {X2} rows pulled → {Y2} profile.json stagés (audiences)*
> *  • Pain Points · {X3} rows pulled → {Y3} pain_benefit_chain entries stagés (subfield profile.json)*
> *  • Angles · {X4} rows pulled → {Y4} angle.json stagés (ANG-NN)*
> *  • Objections · {X5} rows pulled → {Y5} objections entries stagés (subfield profile.json + xref angle.tension)*
> *  • Frictions usage · {X6} rows pulled → {Y6} friction.json stagés (FRC-NN)*
> *  • Roadmap · {X7} rows pulled → 1 roadmap.json singleton stagé (RDM-{brand_slug})*
> *  • Full funnel Meta · {X8} rows pulled → {Y8} creative.json stagés (CRT-NN) + funnel.json maj*
> *  • Specs · {X9} rows pulled → fields {Y9} composition + specs subfields stagés cross-product*
> *  • Mécanismes · {X10} rows pulled → fields mechanisms[] stagés cross-product*
> *  • Bénéfices · {X11} rows pulled → fields benefits[] stagés cross-product*
>
> *Total · {N_proposals} mutations stagées via le mutation gate (write-to-context mode=proposed) sous brands/{brand_slug}/*
>
> *Tags universels Notion détectés cross-rows ·*
> *  • Tag `source` renseigné sur {pct_source}% des rows*
> *  • Tag `confidence` renseigné sur {pct_confidence}% des rows*
> *  • Tag `validation_status` renseigné sur {pct_status}% des rows*
>
> *Pas observé directement (ne pas affirmer) · contenu réel des reviews clients sourçant les pain points encodés Notion · qualité du verbatim {sourced/inferred/declared} par row · perfs paid des creatives Full funnel Meta encodés Notion · réalité terrain des frictions usage vs hypothèses ops.*

### Section 2 · Déduit (hypothèses avec confidence chain)

Hypothèses sur la qualité du corpus Notion pullé. JAMAIS affirmation. Confidence chain qualitatif (`forte / moyenne / faible / TRÈS faible`).

Exemple cible (adapter selon corpus réel) ·

> *Déduit · {N} hypothèses qualité corpus Notion*
>
> *H1 · Qualité épistemic du corpus Notion*
> *  Confidence · {forte si pct_tags > 70%, moyenne si 40-70%, faible si < 40%}*
> *  Indicateurs · tags universels renseignés sur {pct_global}% rows cross-collections · {N_rows_observed} rows tag source=observed (sourced verbatim), {N_rows_inferred} inferred, {N_rows_declared} declared*
> *  À valider · Tu confirmes que le tagging Notion reflète la réalité (sourced = vraiment verbatim Trustpilot/reviews, pas posé par défaut) ?*
>
> *H2 · Audiences encodées Notion = data-driven vs hypothèses*
> *  Confidence · {selon pct audiences avec validation_status >= "tested"}*
> *  Indicateurs · {N_audiences_tested} audiences sur {N_total} avec validation_status >= tested · {N_audiences_hypothesis} encore en hypothesis*
> *  À valider · Les audiences en hypothesis ont-elles déjà du verbatim mining client réel derrière, ou ce sont des cartographies ops sans data terrain ?*
>
> *H3 · Cohérence cross-collections relations Notion ↔ cross_refs PhantomOS*
> *  Confidence · {selon validate-resources output}*
> *  Indicateurs · {N_cross_refs_resolved} relations Notion mappées sur cross_refs PhantomOS, {N_cross_refs_unresolved} non-résolues (target id absent ou mal nommé)*
> *  À valider · {liste cross_refs unresolved si applicable}*
>
> *(... adapter selon corpus pullé · skipper H2/H3 si data non significative ...)*

### Section 3 · Inconnu (variables non observables)

Liste explicite des variables que le sync Notion ne peut pas lever.

Exemple cible ·

> *Inconnu · {N} variables à creuser*
>
> *1. Collections non-matched ({M}/11) · {liste collections canon manquantes dans Notion} → soit pas peuplées Notion-side (l'opérateur arbitre s'il les crée), soit nom Notion non-canon (schema map override)*
> *2. Qualité verbatim sourcing pain points encodés · sans audit des sources Notion (Trustpilot exports, reviews capture, interview transcripts), impossible de savoir si `source: observed` Notion = vrai verbatim ou tag posé par défaut → audit via mine-voc cross-référence*
> *3. Audiences réelles paid Meta vs cartographiées Notion → audit via audit-meta-account si compte Meta dispo*
> *4. Frictions réelles client vs hypothèses ops encodées Frictions usage → cross-référence support tickets + reviews verbatim*
> *5. Viability roadmap (capacité atelier, capacité paid, calendrier réel) → operator capture*
> *6. {liste validate-resources MAJOR/CRITICAL findings si applicable}*

### Section 4 · Leviers (options drill-down · opérateur arbitre)

Pour chaque inconnue importante, quel skill / action permet de la lever.

Exemple cible ·

> *Leviers · {N} axes d'investigation prioritaires*
>
> *Axe A · Validation workflow pending-validations (lève Inconnu 6 + cohérence générale)*
> *  → Workflow opérateur classique · review batch des {N_proposals} mutations stagées via pending-validations.md, accept/reject/correct par collection ou batch (10-15 min par collection si tu reviews finement, 5 min si tu accept tout en bulk)*
> *  → Si certaines mutations ont validate-resources MAJOR flag, traiter d'abord ces ones (corriger Notion + re-pull, ou correct PhantomOS-side via stage-proposal correction)*
>
> *Axe B · Upgrade confidence corpus Notion thin (lève H1)*
> *  → Si tags universels Notion peu renseignés (<40%), recommander mining client réel pour upgrade · écoute Trustpilot + reviews onsite + threads sectoriels (~30 min) puis re-tag Notion-side avant re-sync*
> *  → Audit compte paid Meta si dispo, cross-référence audiences réelles vs hypothèses Notion*
>
> *Axe C · Re-sync si Notion mis à jour (lève {variables temporelles})*
> *  → Sync stateless idempotent · re-run `/sync-notion-atlas {brand_slug} --mode=pull {notion_url}` à tout moment quand Notion update. Les mutations re-stagées remplacent les pending non-accept.*
>
> *Axe D · Phase B push (PhantomOS → Notion) post-MVP*
> *  → Disponible v2.58 prévue · expose state PhantomOS encodé en UI Notion navigable pour client review ou collab agency. Pas v1.0.0 actuel.*

### Section 5 · Close ouvert (UNE question macro)

UNE question macro priorité drill-down. Reco macro explicite. JAMAIS menu plat.

Exemple cible ·

> *On a {N_proposals} mutations stagées sous brands/{brand_slug}/, prêtes à valider. Pour la suite, tu préfères ·*
>
> *A · Accept all en batch maintenant ({~5 min} bulk validation via pending-validations.md, puis tu reviens si correction nécessaire post-coup)*
> *B · Review par collection ({~10-15 min par collection × {N_collections}} pour audit fin avant accept)*
> *C · Drill-down sur une collection problématique d'abord (genre · {nom collection avec validate-resources MAJOR si applicable}, ~10 min)*
>
> *Mon avis · {recommandation macro contextualisée}. Si le tagging Notion est solide (Section 1 montre pct_tags > 60%), A en bulk économise du temps. Si la cartographie est récente / pas validée terrain, B par collection donne le contrôle. Si validate-resources a flagué du MAJOR, C en priorité sur la collection concernée.*

L'opérateur dit `A` / `B` / `C` ou autre, l'agent enchaîne le drill-down sur l'axe choisi (cycle itératif respect 5 sections).

### Hard rules cross-section synthèse (cf. investigation-posture.md)

- **5 sections explicites, jamais fusionnées en prose continue.** Anti-pattern AP-6 doctrine.
- **JAMAIS exposer confidence numeric à l'opérateur.** Confidence chain qualitatif uniquement (`forte / moyenne / faible / TRÈS faible`).
- **JAMAIS nommer le skill interne en surface opérateur** (`mine-voc`, `audit-meta-account`, `pending-validations.md` interne = OK si présenté comme workflow, pas comme path technique).
- **JAMAIS clôturer avec affirmation** (*"Voilà, sync terminé. Autre chose ?"*) · close ouvert toujours UNE question macro drill-down.
- **JAMAIS inventer data Notion pour combler les vides.** Si la collection Frictions est vide Notion-side, la Section 1 dit *"Frictions · 0 rows, pas peuplé Notion-side"*. JAMAIS générer des frictions de placeholder.

---

## Workflow opérateur

### Invocation Phase A (v1.0.0)

```
/sync-notion-atlas {brand_slug} --mode=pull {notion_workspace_url}
```

Exemple ·

```
/sync-notion-atlas stepprs --mode=pull https://notion.so/workspace/abc123def456
```

### Modes deferred (v1.0.0 stubs)

Si l'opérateur invoque `--mode=push` ou `--mode=diff` v1.0.0 ·

> *Sync-notion-atlas v1.0.0 = Phase A pull-only MVP shipped v2.57. Mode `--mode=push` (PhantomOS → Notion) prévu Phase B v2.58. Mode `--mode=diff` (compare sans muter) deferred P2 v2.59.*
>
> *Pour pull · `/sync-notion-atlas {brand_slug} --mode=pull {notion_url}`*

Pas de fallback silencieux. Refuse cleanly avec roadmap d'évolution.

---

## Phase B spec v2.58 · scaffold-create canonical Notion workspace

> **Status** · spec rigoureuse documentée v2.57, implémentation runtime v2.58. Le skill DOIT pouvoir générer le système Notion canon (11 collections + relations + tags universels + canvas wrapper) miroir de stride-up Onday template, from blank, sur n'importe quel parent Notion. Phase B = `--mode=push` from PhantomOS state, OR `--mode=scaffold` from blank brand (sans state à populer).

### Invocation Phase B

```
/sync-notion-atlas {brand_slug} --mode=push {notion_parent_url}
/sync-notion-atlas {brand_slug} --mode=scaffold {notion_parent_url}
```

- `push` · brand `brands/{brand_slug}/` existe avec state populé → scaffold structure + populate rows depuis entities PhantomOS.
- `scaffold` · brand vierge OR pré-onboarding → scaffold structure vide (canon empty workspace, opérateur populate Notion-side ensuite OR run sync pull plus tard).

### Pipeline Phase B

**Step 1 · Canvas root page creation**

`notion-create-pages` sous `{notion_parent_url}` ·

- Title · `Phantom OS · {brand_name}` (icon 🧠)
- Content · template canvas Onday-style ·
  - 3 colonnes (callouts) · Base de données (mention sub-page Data Client) · Liens utiles (placeholder URLs drive assets + créas) · Espace Client (sub-page Suivi des créas)
  - Callout `Opérations / lancements` avec table months (5 colonnes mois, rows Events + Budget vides à remplir opérateur)
  - 2 databases inline (Roadmap + Full funnel Meta · cf Step 3)
  - Sub-page `Données Atlas` (header documentation cartographie)

**Step 2 · Données Atlas wrapper sub-page**

`notion-create-pages` sous canvas root ·

- Title · `🧠 Data Client, {brand_name}` (icon #️⃣)
- Content · documentation header explicative (cf Onday template) ·
  - Section "Comment lire l'ensemble · 3 zones reliées (Produit · Audiences · Angles)"
  - Section "Les 6 DBs en un coup d'œil" (table DB ↔ Réponse)
  - Section "Comment naviguer" (workflow 4 étapes Persona → Pain Points → Angles → Formule)
  - Section "Tags universels (sur toutes les DBs)" (Source / Confidence / Validation status)
- Inline les 9 databases canon Data Client (cf Step 3)

**Step 3 · 11 databases creation**

`notion-create-database` × 11, chacune avec properties canonical alignées schemas PhantomOS + tags universels par défaut + relations cross-DB. Schémas détaillés ·

#### 3.1 · Produits (canon spec.identity + offers résumé)
- `Nom produit` (title)
- `Slug` (text, url-safe)
- `Niche` (select)
- `Positioning` (text)
- `Active offer summary` (text · price + urgency)
- Tags universels (cf section 3.12)

#### 3.2 · Specs (canon spec.composition + spec.specs)
- `Spec name` (title)
- `Type` (select · composition / dosage / certification / packaging / origin / regulatory)
- `Value` (text)
- `Produit` (relation → Produits)
- Tags universels

#### 3.3 · Mécanismes (canon spec.mechanisms[])
- `Mécanisme name` (title)
- `Description physiologique` (text rich)
- `Duration / délai d'effet` (text · ex "4-6 semaines")
- `Produit` (relation → Produits, multi)
- Tags universels

#### 3.4 · Bénéfices (canon spec.benefits[] v1.10)
- `Bénéfice name` (title)
- `Chain level` (select · functional / emotional / identity)
- `Emotional signal` (text · ressenti spécifique exprimé client-side)
- `Latency min (jours)` (number)
- `Latency max (jours)` (number)
- `Evidence verbatim` (text rich · multi-line quotes VoC)
- `Produit` (relation → Produits)
- `Mécanisme` (relation → Mécanismes)
- Tags universels

#### 3.5 · Personae (canon profile.identity + psychology)
- `Persona label` (title)
- `Slug` (text, url-safe)
- `Awareness stage` (select · unaware / problem-aware / solution-aware / product-aware / most-aware)
- `Demographics` (text rich)
- `JTBD primary` (text · "Retrouver un corps que je reconnais sans me battre")
- `Produit principal` (relation → Produits)
- Tags universels

#### 3.6 · Pain Points (canon profile.pain_benefit_chain[] v1.6)
- `Pain formulation` (title · customer language)
- `Category` (select · physical / emotional / friction_ux / logistical / cognitive / social_status)
- `Emotion` (text)
- `Trigger` (text · moment déclencheur)
- `Verbatim quotes` (text rich · cite VoC avec sample_size en parenthèses)
- `Persona` (relation → Personae)
- `Bénéfice servi` (relation → Bénéfices · backward chain)
- Tags universels

#### 3.7 · Angles produits (canon angle.json v1.2)
- `Angle name` (title)
- `Angle ID` (text · pattern ANG-NN)
- `Origin axis` (select · audience-derived / product-derived / category-derived / brand-derived / temporal-cultural)
- `Awareness stage in` (select · 5 stages canon)
- `Awareness stage out` (select · 5 stages canon)
- `Formula Observation` (text)
- `Formula Tension` (text)
- `Formula Reframe` (text)
- `Formula Bridge produit` (text)
- `Hook canon ID` (text · ref canon copy hooks)
- `Framework canon ID` (text · ref canon copy frameworks)
- `Archetype voix canon ID` (text · ref canon copy archetypes-voix)
- `Pain extract` (text · quote anchored)
- `Proof primary` (text · type proof retenu)
- `CTA` (text)
- `Persona cible` (relation → Personae)
- Tags universels

#### 3.8 · Objections (canon profile.objections[] v1.6 enrichi)
- `Objection formulation` (title)
- `Type` (select · price / scepticism / fit / urgency / trust / status / risk)
- `Lifecycle` (select · awareness / consideration / decision / post-purchase)
- `Severity score` (number 1-10)
- `Response counter` (text · formulation neutralization testée)
- `Persona` (relation → Personae, multi)
- `Angle dérivé` (relation → Angles produits, multi · angles qui exploitent cette objection comme tension)
- Tags universels

#### 3.9 · Frictions usage (canon friction.schema v1.0 NEW)
- `Friction name` (title · short label)
- `Friction ID` (text · pattern FRC-NN)
- `Category` (select · physical / emotional / friction_ux / logistical / cognitive)
- `Severity score` (number 1-10)
- `Customer evidence` (text rich · verbatims usage friction)
- `Current workarounds` (text · ce que les clients font pour contourner)
- `Resolution state` (select · unresolved / workaround_present / patched / fixed)
- `Affected products` (relation → Produits, multi)
- `Affected audiences` (relation → Personae, multi)
- `Cross-ref objections` (relation → Objections, multi)
- `Cross-ref pain points` (relation → Pain Points, multi)
- Tags universels

#### 3.10 · Roadmap [angles/audiences] (canon roadmap.schema v1.0 NEW)
- `Phase name` (title)
- `Phase ID` (text)
- `Dates` (date range start + end)
- `Status` (select · draft / in-progress / shipped / paused / killed)
- `Mix axis` (select · audience / angle / product / funnel / creative)
- `Weight` (number 0-1)
- `Production status` (select · spec'd / in-production / shipped / iterating)
- `Priorities (top 3)` (text rich · bullets)
- `Angles refs` (relation → Angles produits, multi)
- `Audiences refs` (relation → Personae, multi)
- `Products refs` (relation → Produits, multi)
- `Creatives refs` (relation → Full funnel Meta, multi)
- Tags universels

#### 3.11 · Full funnel Meta (canon creative.json + funnel.json)
- `Creative name` (title)
- `Creative ID` (text · pattern CRT-NN)
- `Format` (select · image / carousel / story / reel / vsl / landing / email / sms / ad_copy / blog)
- `Funnel stage` (select · TOF / MOF / BOF / retargeting / lifecycle)
- `Intent mix primary` (select · DR / Brand / Hybrid / B2B_lead_gen)
- `NOYAU mécanique` (text · ref creative-mechanics-registry)
- `Hook` (text · verbatim quoted)
- `CONTEXTE angle` (relation → Angles produits)
- `CONTEXTE persona` (relation → Personae)
- `Status` (select · live / paused / killed / draft)
- `Test data` (text · CTR / CVR / spend snapshot opt)
- Tags universels

#### 3.12 · Tags universels (par défaut sur les 11 DBs)
- `Source` (select · observed / inferred / declared) · default empty (operator-side ou pull-side)
- `Confidence` (number · 0 à 1)
- `Validation status` (select · hypothesis / tested / validated / scaled / fatigued)

Mapping vers PhantomOS ·
- Notion `Source` ↔ PhantomOS `_field_types` (observed↔observed · inferred↔derived · declared↔stated)
- Notion `Confidence` ↔ PhantomOS `confidence` numeric direct
- Notion `Validation status` ↔ PhantomOS `meta.validation_status.state` enum direct

**Step 4 · Populate rows (mode push uniquement, skip mode scaffold)**

Pour chaque entité dans `brands/{brand_slug}/`, `notion-create-pages` dans la database correspondante avec mapping inverse PhantomOS → Notion.

- `spec.json` → 1 row Produits + N rows Specs / Mécanismes / Bénéfices (subfields éclatés)
- `audiences/{slug}/profile.json` → 1 row Personae + N rows Pain Points + N rows Objections
- `angles/{ANG-NN}.json` → 1 row Angles produits
- `frictions/{FRC-NN}.json` → 1 row Frictions usage
- `roadmap.json` → N rows Roadmap (par phase)
- `creatives/{CRT-NN}.json` → 1 row Full funnel Meta

**Step 5 · Cross-link relations (post-populate)**

Post Step 4, second pass · `notion-update-page` pour set relations entre rows. Pattern · pour chaque row PhantomOS porte des cross_refs (e.g. profile.pain_points → friction_ids, angle.formula → objection_id), résoudre vers Notion page IDs et set property relation.

**Step 6 · Synthesis output 5 sections investigation-posture**

- **Observé** · workspace Notion créé sous `{notion_parent_url}`, URL canvas root + 11 DBs IDs · row counts populés par DB · `pct_relations_linked` (% relations cross-DB résolues correctement).
- **Déduit** · qualité scaffold dépend de qualité state PhantomOS source · si entités sparse (peu de cross_refs), Notion populé pauvre · si dense (cross_refs riches), Notion riche en relations.
- **Inconnu** · adoption Notion-side opérateur (utilisera-t-il la UI Notion vs PhantomOS canon ?) · si Notion édité après scaffold, drift PhantomOS ↔ Notion à diff via Phase C v2.59.
- **Leviers** · re-run push si PhantomOS évolue (mode idempotent, met à jour pages existantes par ID) · scaffold complémentaire (canvas template Onday-style complet · Liens utiles / Suivi des créas / Opérations table) en patch v2.58.1 ou v2.59 si besoin.
- **Close ouvert** · UNE question macro · *"Workspace Notion canon créé sous {URL}. Tu veux que je share l'URL à ton client / collab pour review, OU on enchaîne sur la table Opérations / lancements à populer manuellement post-scaffold, OU on stop ici et tu inspectes ?"*

### Tags universels par défaut (Step 3.12)

Sur chaque database scaffold, properties tags universels créés avec ces options select par défaut ·

```
Source · observed (green) · inferred (yellow) · declared (blue)
Validation status · hypothesis (gray) · tested (yellow) · validated (green) · scaled (purple) · fatigued (red)
```

Confidence est number 0-1, pas select. Permet de stocker la valeur numeric agent-side et l'opérateur Notion peut filter / sort dessus.

### Hard rules Phase B spécifiques

- **Idempotent par PhantomOS entity ID.** Re-run push update les pages Notion existantes par `phantom_entity_id` (stocké en property texte caché type "PhantomOS ID"). JAMAIS création duplicate. Pattern · query Notion par phantom_entity_id property → si match update, sinon create.
- **No silent overwrite Notion-side edits.** Si page Notion existe ET a été éditée Notion-side depuis dernier sync (timestamp `last_edited_time` > `last_synced`), flag conflict dans Section 4 Leviers, propose Phase C diff v2.59 avant overwrite.
- **Canvas wrapper template fidèle Onday-style.** Step 1 + Step 2 scaffold le wrapper canvas (3 colonnes callouts + Opérations table + Données Atlas page header) MIROIR de stride-up Onday template. Reproductible cross-clients pour Abyss collectif.
- **Mode scaffold blank-only.** Si `brand_slug` a state populé, refuse `--mode=scaffold` (anti-pattern · scaffold blank doit pas effacer Notion existant). Propose `--mode=push` à la place. Mode scaffold uniquement quand brand vierge ou pre-onboarding.

### Workflow post-Phase B

1. Largo run `--mode=push brand-active` · workspace Notion peuplé scaffold from PhantomOS state · partage URL au client / collab.
2. Client / collab édite Notion-side (corrections, enrichissements, validation status update).
3. Largo run `--mode=pull` plus tard pour rapatrier les edits Notion → PhantomOS.
4. Cycle bidirectionnel opérationnel.

### Évolutions futures Phase B+

- **v2.58.1 · canvas template extended** · Liens utiles populé (drive URLs si dispo dans brand config) · Suivi des créas sub-page populated · Opérations table avec dates auto-générées (12 prochains mois rolling).
- **v2.59 · `--mode=diff`** · compare state PhantomOS vs Notion, surface deltas operator-facing en 5 sections, accept-all / per-collection / cherry-pick.
- **v2.60 · multi-Notion sources aggregation** · 1 PhantomOS brand pulled from N Notion workspaces (Abyss collectif scaling · N clients Notion → 1 atlas PhantomOS).

---

### Workflow post-sync (opérateur arbitre)

1. Synthesis Section 5 propose le drill-down macro (A / B / C).
2. Si A · opérateur va dans `brands/{slug}/pending-validations.md`, bulk accept (workflow standard PhantomOS).
3. Si B · opérateur review collection par collection, accept/reject/correct par mutation, agent peut driller sur une collection si besoin.
4. Si C · agent drille sur la collection problématique (re-cycle 5 sections sur le focus).

Le sync ne ferme pas la conversation. Il ouvre le workflow validation classique PhantomOS.

### Re-sync

Stateless idempotent. Re-run `/sync-notion-atlas {brand_slug} --mode=pull {notion_url}` à tout moment quand Notion mis à jour. Les mutations re-stagées remplacent les pending non-accept (write-to-context mode=proposed gère le merge / overwrite per-field). Idempotent par design.

---

## Hard rules

- **Mutation gate strict.** TOUT write via `python3 .skills/write-to-context.py`. JAMAIS `Edit/Write/NotebookEdit` sur les `.json` sous `brands/{brand_slug}/`. Bypass = refusé runtime par mutation-guard PreToolUse hook + corrupt proposal/acceptance workflow. Doctrine canon · `docs/system/schema-encoding-discipline.md § Mutation rule`.
- **isolation_scope brand_only.** Le sync n'affecte QUE `brands/{brand_slug}/`. JAMAIS workspace-global, JAMAIS cross-brand. 1 brand par invocation. Pour sync brand A + brand B · 2 invocations distinctes. Doctrine canon · `docs/system/brand-isolation-discipline.md`.
- **Stateless idempotent.** Re-run identique = même résultat. Notion = source of truth en mode pull, PhantomOS canonical write via gate. Idempotent par design (les mutations re-stagées remplacent les pending non-accept).
- **No scoring leak.** JAMAIS expose confidence numeric à l'opérateur. Use qualitatif `forte / moyenne / faible / TRÈS faible` per investigation-posture canon. Confidence numeric reste agent-side / encoded JSON / consumers internes.
- **No em-dash.** Canon style strict (cf. CLAUDE.md root · *no em-dash global*). Substitute par middle dot ·, parenthèses, virgule, point, deux-points. Zero em-dash en operator surface, code comments, prose interne, output schema description, partout.
- **Stage all or none (partial).** Si validate-resources MAJOR sur une entité stagée · flag dans Section 3 / Section 4 synthesis, **continue le batch** sur les autres. Pas de rollback automatique (anti-pattern destructive). L'opérateur arbitre via pending-validations.md.
- **No invented data.** Si row Notion a champ vide (property null / empty) · le champ PhantomOS reste vide / null. JAMAIS d'inférence pour combler. Notion = source of truth en mode pull. Hard rule absolue, parité doctrinale `snapshot-brand § Never invent`.
- **No-orphan output.** Close drill-down macro UNE question, JAMAIS menu plat (a/b/c/d equal-weight), JAMAIS *"voilà fait, autre chose ?"*. Reco macro explicite avec rationale 1 ligne. Doctrine canon · `contextual-intelligence.md § No orphan output`.
- **Backward compat strict additif.** Skill NEW v2.57, n'override aucun existant. Phases B (push) + diff stubbées mais inactives v1.0.0. Invocation `--mode=push` ou `--mode=diff` refuse cleanly avec roadmap d'évolution.
- **Operator-facing rule absolue.** JAMAIS nommer doctrine names (Compositional Cartography, Schema Encoding Discipline, Investigation Posture, DRGFP), acronymes, paths internes (`brands/{slug}/.workflow.json`, `write-to-context.py`, `validate-resources` interne), enum brut (`isolation_scope`, `_field_types`, `_source`) en surface opérateur. L'opérateur voit l'effet (proposals stagées prêtes à valider), JAMAIS la plomberie.
- **MCP Notion gate strict.** Pas de fallback silencieux si MCP absent · refuse cleanly Step 0 L2 gate avec 3 options AskUserQuestion (setup MCP / abort / cached snapshot). Pas de pseudo-pull depuis fake source.
- **No bidirectionnel auto-sync.** Phase A pull-only · jamais de push silencieux post-pull. L'opérateur invoque explicitement chaque sync. Anti-pattern · auto-loop Notion ↔ PhantomOS sans gate operator.
- **JAMAIS de bridge mutation cross-brand.** Un sync = un brand. JAMAIS de pull data depuis Notion brand A vers brand B (anti-pattern AP-4 notion-bridge-doctrine.md).

---

## Cross-references

### Doctrine canon
- `docs/system/notion-bridge-doctrine.md` · source canon doctrine bridge bidirectionnel (mappings, edge cases, anti-patterns, layer 1 positioning)
- `docs/system/compositional-cartography.md` · 4 arbres compositionnels + matrice canon + modulateurs que les 11 collections Notion stride-up implémentent (§4 mappings table)
- `docs/system/brand-isolation-discipline.md` · isolation_scope brand_only enforcement (default obligatoire, privacy multi-clients agency)
- `docs/system/investigation-posture.md` · 5 sections close synthesis canon (Observé / Déduit / Inconnu / Leviers / Close ouvert)
- `docs/system/schema-encoding-discipline.md` · mutation rule canon (write-to-context.py only) + `_field_types` enum + sourcing tags
- `docs/system/connectivity-layering.md` · Layer 1 MCP servers (Notion MCP positioning)
- `docs/system/dependency-resolution-protocol.md` · DRGFP L1/L2/L3 prerequisite checks Step 0

### Schemas canon consumés
- `resources/schemas/brand.schema.json` · brand identity (read-only, sync n'affecte pas brand.json)
- `resources/schemas/spec.schema.json` · produits + specs + mechanisms + benefits
- `resources/schemas/offer.schema.json` · offers v2 (offer_groups[])
- `resources/schemas/profile.schema.json` · personae + pain_benefit_chain + objections
- `resources/schemas/angle.schema.json` · angles produits (ANG-NN)
- `resources/schemas/friction.schema.json` · NEW v2.56 frictions usage (FRC-NN)
- `resources/schemas/roadmap.schema.json` · NEW v2.56 roadmap singleton (RDM-{slug})
- `resources/schemas/creative.schema.json` · creatives Full funnel Meta (CRT-NN)
- `resources/schemas/funnel.schema.json` · funnel global brand
- `resources/schemas/_shared/validation-status.json` · enum validation_status canon

### Skills pattern miroir + downstream
- `.skills/skills/snapshot-brand/SKILL.md` · pattern miroir scrape + map + stage (URL e-commerce brand vs URL workspace Notion · UPSTREAM différent)
- `.skills/skills/ingest-resource/SKILL.md` · pattern délégation encode-batch Haiku pour batches > 5 mutations
- `.skills/skills/encode-batch/SKILL.md` · sub-agent Haiku canonical pour scaler les mutations
- `.skills/skills/validate-resources/SKILL.md` · integrity check post-stage (Step 5)
- `.skills/skills/connect-mcp-server/SKILL.md` · setup MCP Notion (route Step 0 L2 gate option a)
- `.skills/skills/scaffold-extension/SKILL.md` · route post-sync pour fields Notion custom non-canon

### Infrastructure scripts
- `.skills/write-to-context.py` · mutation gate canonical (mode direct pour scaffold, mode proposed pour stamp inferred fields)
- `.skills/stage-proposal.py` · checkpoint gate workflow (non utilisé Phase A · réservé checkpoints `audience_q1q4_answered` + `confirmed_products` snapshot-brand)
- `.skills/build-brand-snapshot.py` · rebuild snapshot post-mutations (silent ~50ms)
- `.skills/finalize-mutation-batch.py` · coherence check post-batch (mechanical Python primitive)

### Layer 1 MCP config
- `.mcp.json.example` · entry `notion` server Layer 1 documenté (credentials ref `NOTION_API_KEY`)

---

## Verdict

Skill `sync-notion-atlas` v1.0.0 ship le bridge Notion → PhantomOS Phase A pull-only MVP, mutation gate strict via write-to-context.py mode=proposed, isolation brand_only, 5 sections close investigation-posture, MCP Notion gate L2 explicite · Phases B push + diff stubbées pour évolution v2.58+ sans casser v1.0.0.
