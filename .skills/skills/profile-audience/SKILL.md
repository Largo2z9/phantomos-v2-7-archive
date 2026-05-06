---
name: profile-audience
version: 1.1.0
type: orchestrator
recommended_model: sonnet
subagent_safe: true
mode: proposed
operator_facing: true
description: Synthétise les outputs de mining (voc/vom/audience) en profil audience structuré 8 dimensions canon V3. Consume verbatims raw, produit profile.json conforme schema v1.3 avec validation gate operator. Ne mine pas, synthétise.
triggers_fr:
  - "profil audience"
  - "synthétise l'audience"
  - "8 dimensions audience"
  - "structure audience"
  - "cartographie sub-cluster"
triggers_en:
  - "profile audience"
  - "synthesize audience"
  - "8 dimensions"
  - "structure audience"
  - "map sub-cluster"
disambiguates_against:
  - mine-voc: "mine-voc capture verbatims clients (raw signals). profile-audience SYNTHÉTISE ces signals en profil 8-dim structuré."
  - mine-vom: "mine-vom capture vernaculaire marché. profile-audience consume les outputs des mining skills."
  - mine-audience: "mine-audience découvre des sub-clusters candidats. profile-audience structure un sub-cluster spécifique en 8 dimensions."
  - cartograph: "cartograph est READ-ONLY synthèse strategique. profile-audience WRITE (peuple profile.json)."
consumes:
  - brands/{slug}/audiences/_voc/* (mine-voc outputs)
  - brands/{slug}/audiences/_vom/* (mine-vom outputs)
  - brands/{slug}/audiences/{audience}/raw/* (mine-audience outputs)
  - resources/schemas/profile.schema.json (target)
  - resources/canon/copy/niveaux-schwartz/* (awareness stages reference)
produces_validations_for: []
produces_proposals_for:
  - brands/{slug}/audiences/{audience_slug}/profile.json
permissions:
  reads: [brands/, resources/]
  writes: [brands/{slug}/audiences/{slug}/profile.json via write_to_context]
  emits_events: [profile_proposal_created, profile_validated]
pipeline:
  preconditions:
    - "mine-voc OR mine-vom OR mine-audience a tourné"
    - "audience_slug défini"
  postconditions:
    - "profile.json conforme profile.schema v1.3"
    - "8 dimensions populated"
    - "operator validation gate passed"
prerequisites:
  - field: audiences/{slug}/profile.json
    level: L1
    auto_pull: brownfield_seed_read
    freshness_ttl_days: 90
  - field: audiences/{slug}/mining-outputs/
    level: L1
    auto_pull: read_mining_outputs
    freshness_ttl_days: 60
  - field: audiences/{slug}/verbatim_density
    threshold: 3
    level: L3
    fallback: infer_from_canon_archetype
    confidence_default: 0.5
  - field: resources/canon/copy/archetypes-voix
    level: L1
    auto_pull: read_canon_directory
    freshness_ttl_days: 365
---

# profile-audience

Synthétise un sub-cluster d'audience en profil 8 dimensions canon V3. Consume les outputs de mining et produit `profile.json` conforme `profile.schema v1.3`. Operator-facing avec validation gate avant write.

## Hard Rules

### Step 0bis · Prerequisite check (DRGFP v2.38)

Avant lecture mining outputs (Step 1), scanner prerequisites :

1. Lookup `audiences/{slug}/profile.json` brownfield existing → si présent + freshness 90d OK → seed corpus silent (HR2.5 v2.35 pattern)
2. Lookup mining outputs (mine-voc, mine-vom, mine-audience) → si présents → consume silent
3. Compter verbatim_density cumulé (existing seed + mining) → si < 3 → L3 degraded · fallback infer canon archetype · confidence 0.5 · flag _gaps
4. Lookup canon archetypes-voix → silent always (cross-brand canon read)

Output state map + confidence_chain[] init avec valeur dépendante de density actuelle.

Cross-ref doctrine : `docs/system/dependency-resolution-protocol.md`.

### HR1 · Verify mining inputs available

Vérifier que `mine-voc` OR `mine-vom` OR `mine-audience` a tourné pour cette audience.
Si aucun mining n'a tourné, surface warning :

> Pas de signal mining disponible. Skill produira hypothesis-grade. Run mine-voc d'abord pour grade validated. Continuer ?

### HR2 · Load mining outputs

Read `brands/{slug}/audiences/_voc/{audience}/*` + `_vom/*` + `raw/*`.
Aggrégate verbatims, key_expressions, pain points raw, benefits raw.
Cache localement dans `/tmp/profile-audience/{audience}-mining-corpus.json`.

### HR2.5 · Read existing profile.json as seed corpus (brownfield)

v1.0.1 (v2.35 alignment) : HR2.5 brownfield seed (read existing profile.json as seed corpus, preserve validated entries) + HR7.1 merge strategy explicite (no auto-overwrite).

Si `brands/{slug}/audiences/{audience_slug}/profile.json` existe et contient déjà des entries (verbatims inliné, pain_points populés, voice.key_expressions, etc.) :

1. Read le profile.json existant comme seed
2. Extraire :
   - voice.key_expressions[] · verbatims pré-existants
   - pain_points[] · chains 3 niveaux pré-existants
   - benefits[] · chain functional/emotional/identity pré-existants
   - identity.* · démographie pré-existante
3. Merger avec mining corpus (HR2) si dispo
4. Marquer chaque entry source : `existing_profile` (seed) vs `mine_voc/vom/audience` (fresh mining)
5. Préserver `validation_status` existant des entries déjà validées (status >= validated)

HR2.5 garantit le skill fonctionne en mode brownfield (audience pré-amorcée par opérateur ou skill antérieur) sans écraser ni perdre l'existant.

### HR3 · Synthesize 8 dimensions

Pour chaque dimension, extraire/synthétiser depuis le corpus :

**Dimension 1 · Purchase Driver**
Identify dominant driver from verbatims : `pain | desire | status | utility | identity | mixed`.
Source verbatims supporting (sample_size).

**Dimension 2 · Problem Map**
Pain principal + frequency + intensity + context.
Décomposer en 3 niveaux : `surface` (ce qu'elle dit en premier) · `consequence` (impact quotidien) · `deep` (sens identitaire/existentiel).

**Dimension 3 · Benefit Stack**
Bénéfices cherchés rangés par ordre de priorité.
Chaîne `functional → emotional → identity`.

**Dimension 4 · Mechanism (audience-side)**
Comment la cible PENSE que la solution doit fonctionner.
Exemple : "elle pense que la repousse vient de la racine donc cherche traitement scalp" vs "elle pense que c'est génétique donc cherche transplant".

**Dimension 5 · Market Context**
Niveau Schwartz sophistication 1-5 (canon copy reference).
Awareness stage dominant : `unaware / problem_aware / solution_aware / product_aware / most_aware`.

**Dimension 6 · Alternative Map**
Autres solutions utilisées (concurrents, OTC, bricolage, abandons).
Pourquoi elles ne suffisent pas (verbatims).

**Dimension 7 · Identity Signals**
Marqueurs mode de vie observables (style, références culturelles, valeurs déclarées).

**Dimension 8 · Decision Process**
Path achat (recherche, comparaison, consultation, déclenchement).
Decision makers : `self / family / peers / influencer / professional`.
Trigger event qui déclenche l'achat.

### HR4 · Cross-validate Schwartz double-stage

Pour chaque sub-cluster, identifier :
- `product_stage` : niveau Schwartz produit-spécifique (ex `product_aware` sur kara)
- `emotional_stage` : niveau émotionnel orthogonal (ex `pain-active` vs `solution-seeking`)

Note : peut différer (cf D#384 multi-product binding · audit S55).

### HR5 · Identify pain_points 3 niveaux

Pour chaque pain principal, décomposer chaîne :
- `surface` : verbatim direct ("j'ai mal aux pieds en fin de service")
- `consequence` : impact quotidien ("je rentre épuisé, irritable")
- `deep` : sens identitaire ("j'envisage de changer de métier")

Tag verbatims sources pour chaque niveau.

### HR6 · Surface draft profile à operator avec validation gate

Présenter en vue opérateur structurée par dimension (8 sections claires).
Demander :

> Voici l'audience structurée. Tu valides en bloc, ou tu veux affiner une dimension ?

### HR7 · Persist via mutation gate

Une fois validé, `write_to_context` sur `brands/{slug}/audiences/{audience_slug}/profile.json`.
Conformité `profile.schema v1.3` obligatoire.
Source : `derived` (skill orchestrator) + tag verbatims sources.

### HR7.1 · Merge strategy explicite

Avant write_to_context :

1. Re-load profile.json actuel (state of truth at write time)
2. Pour chaque entry du draft skill :
   - Si entry source `existing_profile` + `validation_status >= validated` → preserve (skill ne touche pas)
   - Si entry source `mine_*` + entry n'existe pas dans current profile → append
   - Si entry source `mine_*` + entry existe dans current profile → flag conflict, surface à operator
3. Operator gate explicite si conflits détectés

### HR8 · Output operator-facing

Vue lisible profile + next-step :
- Pas d'angles produits → suggest `produce-paid-angles`
- Sub-cluster `validation_status: hypothesis` (default), suggest A/B test
- Si confidence low (peu de verbatims), warn et suggest plus de mining

### HR9 · Anti-patterns

- Ne JAMAIS halluciner une dimension sans verbatims sources
- Ne JAMAIS poser une dimension à hypothesis sans tag `confidence < 0.5`
- Ne JAMAIS skip Schwartz double-stage check
- Ne JAMAIS auto-write sans operator validation gate
- Ne JAMAIS exposer JSON brut à l'opérateur

## Operator output template

```
═══════════════════════════════════════════════════════════════
{BRAND} · {AUDIENCE_SLUG} · DRAFT PROFILE
═══════════════════════════════════════════════════════════════

[1] PURCHASE DRIVER
  Dominant driver  {driver}
  Source verbatims {n} citations

[2] PROBLEM MAP
  Pain principal   {pain}
  Fréquence        {frequency}
  Intensity        {intensity}
  Surface          "{verbatim}"
  Consequence      {consequence}
  Deep             {deep_meaning}

[3] BENEFIT STACK
  Top bénéfices recherchés
    1. {benefit_1} (functional → emotional → identity)
    2. ...

[4] MECHANISM (audience-side belief)
  La cible pense que la solution doit fonctionner via : {mechanism_belief}

[5] MARKET CONTEXT
  Schwartz sophistication  {1-5}
  Awareness stage          {stage}
  Product awareness        {product/solution/problem/unaware}
  Emotional stage          {pain-active / solution-seeking / etc.}

[6] ALTERNATIVE MAP
  Solutions essayées avant
    - {alt_1} : pourquoi insuffisant : {reason}
    - {alt_2} : ...

[7] IDENTITY SIGNALS
  Mode de vie  {signals}
  Valeurs      {values}
  Références   {cultural_refs}

[8] DECISION PROCESS
  Path achat       {path}
  Decision makers  {makers}
  Trigger event    {trigger}

→ Tu valides en bloc, tu affines une dimension, ou tu poses une question ?
```

## Cross-references

- `resources/canon/copy/niveaux-schwartz/*` (sophistication 1-5, awareness stages)
- `resources/schemas/profile.schema.json` v1.3 (`persona_archetype`, `buyer_user_split`, `purchase_driver` derived)
- `resources/canon/copy/creative-formula.md` V3 (8 dimensions canon)
- Notion Stride-Up cartographie audience (doctrine sœur)
- D#384 multi-product binding (audit S55) sur Schwartz double-stage
