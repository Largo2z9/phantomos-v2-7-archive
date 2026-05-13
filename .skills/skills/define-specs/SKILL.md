---
name: define-specs
version: 1.1.0
type: orchestrator
recommended_model: sonnet
subagent_safe: true
mode: proposed
operator_facing: true
triggers_fr:
  - "définis les specs"
  - "crée la fiche produit"
  - "remplis le produit"
  - "spec produit"
  - "qu'est-ce que le produit"
  - "cartographie le produit"
triggers_en:
  - "define specs"
  - "create product card"
  - "populate product"
  - "product spec"
  - "what is the product"
  - "map the product"
disambiguates_against:
  snapshot-brand: "snapshot-brand fait le scrape URL pur (auto). define-specs orchestre snapshot + Q&A operator + sources upload pour produits sans URL ou champs non-scrapés."
  cartograph: "cartograph est READ-ONLY (synthèse strategique). define-specs WRITE (peuple spec.json)."
  propose-schema-draft: "propose-schema-draft crée nouveau schema canon (R&D). define-specs peuple un spec.json existant pour une brand."
consumes:
  - resources/schemas/spec.schema.json
  - resources/schemas/spec.schema.json#visual_identity
  - brands/{slug}/brand.json
  - resources/canon/copy/*
  - skills.snapshot-brand
  - skills.ingest-resource
produces_validations_for: []
produces_proposals_for:
  - brands/{slug}/products/{product_slug}/spec.json
permissions:
  reads: [brands/, resources/]
  writes: [brands/{slug}/products/{slug}/spec.json via write_to_context]
  emits_events: [spec_proposal_created, spec_validated, spec_persisted]
pipeline:
  preconditions:
    - "brand.json existe"
    - "product slug défini ou disponible"
  postconditions:
    - "spec.json conforme spec.schema v1.10"
    - "operator validation gate passed"
prerequisites:
  - field: product.url
    level: L1
    auto_pull: shopify_products_api
    freshness_ttl_days: 7
  - field: operator.input_mode
    level: L2
    options:
      - url_provided
      - manual_qa
      - sources_upload
  - field: products/{slug}/sources/
    level: L1
    auto_pull: read_uploaded_files
    freshness_ttl_days: 30
  - field: products/{slug}/spec.json
    level: L1
    auto_pull: read_existing_spec_brownfield
    freshness_ttl_days: 90
---

## Description

`define-specs` est l'orchestrateur Phase 1 (Spec/Mécanisme/Bénéfice) qui peuple un `spec.json` produit en combinant trois sources de matière brute : auto-pull URL via `snapshot-brand`, ingestion de docs opérateur via `ingest-resource`, et Q&A guidé pour les gaps non-scrapés. La spec produit est le socle factuel qui alimente toute la chaîne downstream (audiences, angles, briefs copy). Skill hybride : aucun champ n'est écrit sans validation gate explicite de l'opérateur.

Posture : éducateur + collègue. Tu rassembles la matière, tu proposes l'assemblage, l'opérateur valide ou corrige. Jamais d'auto-write silencieux. Jamais d'hallucination de champ sans source.

## Hard Rules

### Step 0bis · Prerequisite check (DRGFP v2.38)

Avant detection input mode (Step 1), scanner prerequisites :

1. Lookup `product.url` (operator-fournie ou pré-existante brand) → si présente + freshness 7d OK → L1 auto_pull Shopify silent
2. Lookup `products/{slug}/spec.json` brownfield existing → si présent + freshness 90d OK → read as seed silent
3. Lookup `products/{slug}/sources/` upload files → si présents + freshness 30d OK → ingest-resource silent
4. Si aucun des 3 résolus → L2 gate operator avec 3 options (url_provided / manual_qa / sources_upload)

Output state map des inputs disponibles + confidence_chain[] init.

Cross-ref doctrine : `docs/system/dependency-resolution-protocol.md`.

### HR1 · Detect input mode

Au démarrage, identifier le mode selon ce que l'opérateur fournit :

- **URL produit (Shopify, site brand) seule** → `mode: auto_pull`
- **Pas d'URL mais sources fournies (PDF brief, deck founder, CSV)** → `mode: source_ingest`
- **Ni URL ni sources** → `mode: q_and_a`
- **Combinaison de 2 ou 3 sources** → `mode: hybrid` (lance les 3 et merge)

Surface au démarrage en une phrase :
> "J'ai détecté [URL / sources / rien]. Je vais [auto-pull / ingest / Q&A guidé / les 3 en parallèle]. OK ?"

Confirmer le mode avant de lancer les sub-skills.

### HR2 · Auto-pull (mode auto_pull ou hybrid)

Si URL produit fournie :

1. Spawn `snapshot-brand` sub-skill via Task tool avec l'URL en input
2. Récupérer le draft `spec.json` populated retourné
3. Cache local dans `/tmp/define-specs/{brand}-{product}-snapshot.json`
4. Identifier les champs remplis vs vides depuis le snapshot output

Tagger la source des champs remplis comme `observed` (scrape literal).

### HR3 · Source ingest (mode source_ingest ou hybrid)

Si sources opérateur fournies (PDF, deck, CSV) :

1. Spawn `ingest-resource` sub-skill via Task tool avec les paths sources
2. Extraire les données structurables (specs, ingrédients, claims, dimensions, pricing)
3. Cache local dans `/tmp/define-specs/{brand}-{product}-sources.json`
4. Cross-référencer avec snapshot output si mode `hybrid`

Tagger la source des champs comme `structured` (inferred from documents).

### HR4 · Q&A guidé (mode q_and_a ou hybrid pour combler gaps)

Pour chaque section `spec.schema` majeure non-couverte par auto-pull/sources, poser 1 à 2 questions concises. Sections cibles :

- `identity` (catégorie, niche, type, positionnement, tagline)
- `specs` (matériaux, composition, dimensions, format)
- `mechanisms[]` (cible biologique/cognitive, mode action, fenêtre temporelle, niveau preuve)
- `benefits[]` (chaîne functional → emotional → identity)
- `problems_solved[]` (pain résolus + verbatims)
- `pricing` (prix, currency, modèle)
- `visual_identity` (packshots URLs, color_palette hex, label wordmark, distinctive_features)

Règle dure : **JAMAIS plus de 3 questions par tour**. Privilégier batch question (regrouper champs proches dans un seul prompt). Tagger les réponses comme `declared`.

### HR5 · Assemble draft spec.json

Merge les outputs `auto_pull` + `source_ingest` + `q_and_a` en un draft unique conforme `spec.schema v1.10`.

Tagger chaque champ dans `_field_types` selon sa source :

- `observed` (auto-pull scrape literal)
- `declared` (operator Q&A)
- `structured` (inferred from multiple sources / docs)

Résolution conflit : si 2 sources donnent valeurs différentes pour un même champ, priorité `observed > declared > structured`. Flagger le conflit dans la section "GAPS DÉTECTÉS" du surface.

### HR6 · Surface draft à operator avec validation gate

Présenter le draft `spec.json` en format opérateur-facing (template ci-dessous). **Pas de JSON brut**. Vue lisible avec sections groupées.

Demander explicitement :
> "Voici la fiche produit assemblée. Tu valides en bloc, tu corriges un champ, ou tu poses une question ?"

- Si operator confirms en bloc → HR7
- Si operator corrige → boucle Q&A ciblée sur les champs corrigés, puis re-surface
- Si operator pose question → répondre, puis re-demander validation

### HR7 · Persist via mutation gate

Une fois validé, écrire via `write_to_context` sur `brands/{slug}/products/{product_slug}/spec.json`.

- `source = "operator_validated"`
- `confidence` dépend du `_field_types` de chaque champ
- `mode = "proposed"` (le mutation gate gère le commit)

Trigger `validate-resources` silencieusement post-write. Flagger seulement les MAJOR/CRITICAL à l'opérateur.

### HR8 · Output operator-facing

Vue lisible spec posée + next-step proposal contextuel :

- Si `snapshot-brand` n'a pas tourné dans la session et URL était disponible → propose-le pour enrichir
- Si `audiences/` vide → suggérer `map-audiences` (futur skill v2.33)
- Si produit a un Shopify URL mais `visual_identity` manque → suggérer packshot pull dédié

Format no-orphan-output : 1 reco forte + 1 ou 2 chemins backup si genuinely useful.

### HR9 · Anti-patterns

- **JAMAIS** auto-write sans operator validation gate (HR6)
- **JAMAIS** poser plus de 3 questions par tour
- **JAMAIS** halluciner des specs sans source explicite (auto-pull, doc, ou operator stated)
- **JAMAIS** skip le mode hybrid si les 3 sources sont disponibles
- **JAMAIS** exposer JSON brut à l'opérateur dans le surface draft
- **JAMAIS** exposer `source`, `confidence` (numbers), ou `_field_types` raw. Traduire en `observé / déduit / déclaré / incertain` si la distinction aide
- **JAMAIS** utiliser em dash dans output

## Operator output template (HR6 surface)

```
═══════════════════════════════════════════════════════════════
{brand_humain} · Fiche produit · {product_name}
═══════════════════════════════════════════════════════════════

Identité
  Catégorie         {category} (observé)
  Niche             {niche}
  Type              {type}
  Tagline           {tagline} (déclaré)
  Positionnement    {positioning}

Specs
  Matériaux         {materials}
  Composition       {composition}
  Format            {format}
  Volume / Quantité {volume}

Mécanismes (chaîne causale spec → bénéfice)
  · {mechanism_1.name} · cible {target} · fenêtre {time_window}
  · {mechanism_2.name} ...

Bénéfices (chaîne functional → emotional → identity)
  BNF-01 {benefit_name}
    functional   {chain.functional}
    emotional    {chain.emotional}
    identity     {chain.identity}
  ...

Problèmes résolus
  PRB-01 {problem} (verbatim sources : {n})
  ...

Pricing
  Prix          {price} {currency}
  Modèle        {pricing_model}

Identité visuelle
  Packshot      {packshot_url} (observé Shopify)
  Couleurs      container {hex} · label {hex} · content {hex}
  Label         {wordmark} · {sub_label}
  Distinctive   {features[]}

Gaps détectés
  · {champ_1} : pas couvert (proposer Q&A ?)
  · {champ_2} : conflit auto-pull vs operator (résoudre ?)

Validation requise · valider en bloc, corriger un champ, ou poser une question ?
```

## Cross-refs

- Schema target : `resources/schemas/spec.schema.json` (v1.10+ avec `visual_identity`)
- Sub-skill auto-pull : `.skills/skills/snapshot-brand/SKILL.md`
- Sub-skill ingest : `.skills/skills/ingest-resource/SKILL.md`
- Doctrine production : `docs/system/canonical-matrix-reasoning.md`
- Doctrine substrate : `docs/system/schema-encoding-discipline.md`
- Doctrine authoring : `docs/system/skill-authoring-discipline.md`
- Mutation gate : `write_to_context` (jamais Edit/Write direct sur `.json`)
- Validation post-write : `validate-resources`
