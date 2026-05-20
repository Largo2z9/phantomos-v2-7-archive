---
name: adapt-from-competitor
type: orchestrator
version: "1.0.0"
recommended_model: sonnet
subagent_safe: true
isolation_scope: brand_only
layer: production
reasoning_pattern: matrix-driven
matrix_mode: composing
description: >
  Orchestrator pour adapter une créa concurrente décomposée à la brand opérée.
  Consume creative.json sub-couche depuis decompose-ad v2.0.0 (NOYAU preserved
  + CONTEXTE adaptable + MODIFIEURS situationnels), pré-remplit le contexte
  brand opérateur (audience cartographiée matching + pain_point canonical
  matching + verbatim Trustpilot auto-pick + spec composition matching +
  offer.canon), propose 3 paths flow opérateur (variant complet · 1 axe seul ·
  enregistre pattern registry).
  Pipeline 5 phases · load competitor + brand context, match canonical refs,
  operator gate isolation variables, chain produce-copy-brief brand-side,
  optionnel compose-creative variant.
  Output operator-facing 100% humain · canon résonne back-end · zero raw field
  name · zero registry ID exposé · zero acronyme doctrine.
  FR · "adapte cette créa concurrente", "adapt-from-competitor", "adapter cette
  ad à ma brand", "reprendre cette pub".
  EN · "adapt from competitor", "adapt this ad to my brand", "rework this ad".
permissions:
  reads: [resource, brand, competitive-intel]
  writes: [brand]
  mode: proposed
  subagent_safe: true
  external_apis: []
allowed-tools: Read, Glob, Grep, AskUserQuestion, Skill, Task
isolation_scope: brand_only
matrix_mode: composing
disambiguates_against:
  decompose-ad: "decompose-ad reverse-engineer 1 ad concurrente en fiche v5 + grille variables 3 niveaux ANATOMIE. adapt-from-competitor consume cet output + adapte à la brand opérée via chain orchestrator."
  recompose-creative: "recompose-creative adapte UNE créa interne brand-side (produced/{CRT-N}.json) sur 1 axis variant explicite. adapt-from-competitor adapte depuis UNE créa CONCURRENTE décomposée (competitive-intel/decomposed/{CRT-NN}.json) avec multi-axes (audience + pain + proof + mécanisme + offer simultanément, NOYAU preserved strict)."
  creative-brief-composer: "creative-brief-composer orchestrator produit brief copy + variants visuels depuis angle interne brand (ANG-NN). adapt-from-competitor orchestrator chain produit brief copy + variants depuis créa concurrente décomposée + adaptation contexte brand. adapt-from-competitor upstream invoke creative-brief-composer downstream après isolation variables."
pipeline:
  preconditions:
    - decompose-ad v2.0.0+ output disponible · creative.json v1.2 sub-couche persisted dans competitive-intel/decomposed/
    - brand canonical cartographié (audiences + pain_points + objections + proofs + offers + spec composition)
  postconditions:
    - operator decision logged · path A variant complet OR path B 1 axe seul OR path C registry promotion
    - downstream skill invoked (produce-copy-brief OR compose-creative OR promote-mecanique)
---

# Skill · Adapt From Competitor

Orchestrator pour adapter une créa concurrente décomposée à la brand opérée. Phase 2 du flow décompose créa concurrente · Phase 1 (decompose-ad v2.0.0) a produit la fiche v5 + grille variables 3 niveaux ANATOMIE. L'opérateur a dit "oui je veux l'adapter". Ce skill prend le relais.

## Tone

Posture stratège marketing senior · "voici comment on rend cette créa tienne". Pas inspecteur, pas pixel-counter. L'opérateur a déjà vu la décomposition · ici on entre dans la décision d'adaptation. Sections directes, options claires, 3 paths flow opérateur. Aucun jargon plumbing, aucun nom de field JSON, aucun acronyme doctrine en surface.

## Expert methodology

**Persona** · senior media buyer + creative strategist qui a adapté des centaines de créas concurrentes top performer sur ses propres brands. Sait isoler ce qui doit rester stable (NOYAU · ce qui fait performer) vs ce qui doit être adapté (CONTEXTE · ce qui rend la créa "tienne") vs ce qui se situe selon la campagne (MODIFIEURS).

## Pipeline

### Phase 1 · Load competitor + brand context

Read inputs ·

- `competitive-intel/decomposed/{CRT-NN}.json` (creative.json v1.2 sub-couche depuis decompose-ad v2.0.0) · NOYAU + CONTEXTE + MODIFIEURS encoded fields canon
- `brands/{slug}/brand.json` (identity · positioning · driver_blend · brand_equity · creative_zone)
- `brands/{slug}/audiences/*/profile.json` (cartographie audience hiérarchique)
- `brands/{slug}/audiences/*/pain_points/*.json` (PNT-NN canonical)
- `brands/{slug}/audiences/*/objections/*.json` (OBJ-NN canonical)
- `brands/{slug}/products/*/spec.json` (composition + mechanisms)
- `brands/{slug}/products/*/offers.json` (offers + guarantees · offer.canon)

Halt si decompose-ad output absent OR brand not cartographié (cf DRGFP canon).

### Phase 2 · Match canonical refs (silent back-end)

Match competitor CONTEXTE refs sur brand canonical · scoring algorithm ·

- `audience_segment` competitor vers matching AUD-NN brand cartographié (similarity score 0-1 sur profile.pain_points + profile.triggers + profile.demographics)
- `context.pain_point_ref` competitor vers matching PNT-NN brand canonical (similarity sur surface + consequence + deep)
- `context.proof_type` competitor vers matching proof-registry ID brand (e.g. competitor "social-proof-narrative" vers brand verbatim Trustpilot canonical OR best-seller-badge selon proof available)
- `context.product_mechanism_ref` competitor vers matching spec.composition + spec.mechanisms brand
- `context.offer_ref` competitor vers matching offers.canon brand (e.g. competitor "60-day refund" vers brand offer.guarantees.refund_window)

Output canonical refs matched · pré-rempli pour Phase 3 operator gate.

### Phase 3 · Operator gate isolation variables (AskUserQuestion · 3 paths)

Surface canonical output opérateur-facing ·

```
══════════════════════════════════════════════════════════════════════
ADAPTER · CRT-NN à ta brand {ton_slug}
══════════════════════════════════════════════════════════════════════

  Mécanique source · [label humain mécanique narrative]
  Ce qu'on garde · 5 éléments du noyau (la mécanique narrative · le format ·
  la phrase d'accroche · l'élément pivotal · l'équilibre copy/visuel)

CE QUI EST PRÉ-REMPLI DEPUIS TON TERRITOIRE

  Audience visée         · [label humain audience matching · ex "infirmières
                           12h shifts · workers-shifts cartographié"]
  Douleur adressée       · [label humain pain_point matching · ex "fatigue
                           plantaire 10h+ debout"]
  Verbatim de preuve     · [label humain · ex "3 candidats depuis ton
                           Trustpilot · auto-pick top"]
  Mécanisme produit      · [label humain · ex "compression arche TPU +
                           amortissement gel multi-couche"]
  CTA et garantie        · [label humain · ex "ta garantie 60 jours canon"]

CHOISIS TON FLOW

  → Variant complet · brief copy + variants visuels Meta-ready
    NOYAU preserved + CONTEXTE adapté · produit brief copy en 5-10 min

  → Tester 1 axe spécifique avant brief complet
    isole 1 dimension · audience seule OR pain seule OR proof seule
    OR mécanisme seul · 3-5 min

  → Garder l'analyse · enregistrer le pattern dans le registry pour plus tard
    pas de brief variant maintenant · pattern observée stockée
    creative-mechanics-registry pour réutilisation future
```

Operator choice · A · B · C (via AskUserQuestion tool).

### Phase 4 · Chain downstream selon path

**Path A · Variant complet** ·

- Task tool invoke `produce-copy-brief` avec context · NOYAU preserved + CONTEXTE adapté brand-side + MODIFIEURS opérateur-choice
- Sub-skill produit brief copy + variants visuels Meta-ready
- Persist `brands/{slug}/produced/{CRT-M}.json` (NEW creative.json instance brand-side)
- variant_of · CRT-NN competitor source (lineage canon)

**Path B · 1 axe spécifique** ·

- AskUserQuestion second-level · "quel axe isoler ?" (audience · pain · proof · mécanisme produit · CTA)
- Task tool invoke `recompose-creative` v1.2.2+ avec variant_axis · single dimension explicit (cf HR1 recompose-creative)
- Sub-skill produit creative variant 1 axe seul
- Note · recompose-creative actuel exige source interne · si gap source competitive-intel, fallback Path A simplifié 1 axe

**Path C · Registry promotion** ·

- Pas de brief variant maintenant
- Log mécanique observée dans `learnings.json` brand · candidate promotion vers `creative-mechanics-registry.md` après N validations cross-brand
- Halt skill · opérateur peut re-invoque adapt-from-competitor plus tard

### Phase 5 · Synthesis 5 sections investigation-posture

Toute output stratégique adapt-from-competitor termine par synthese 5 sections IP (cf doctrine investigation-posture · canon CLAUDE.md root) ·

- Observé · {ce qui était dans la créa concurrente · fields canon résonance}
- Déduit · {match canonical refs brand · scoring + confidence chain}
- Inconnu · {variables non-matchable · gaps refs brand · à creuser}
- Leviers · {sub-skills disponibles · produce-copy-brief · compose-creative · promote-mecanique}
- Close ouvert · {opérateur arbitre · path final OR adjust}

## Hard Rules

### HR1 · Input mandatory creative.json v1.2 sub-couche

adapt-from-competitor v1.0.0 REQUIRES decompose-ad v2.0.0+ output preserved dans competitive-intel/decomposed/{CRT-NN}.json. Halt si absent. Re-prompt decompose-ad sur source ad concurrente.

### HR2 · Brand context required

Brand cartographié (audiences + pain_points + objections + proofs + offers + spec composition) REQUIRED. Halt si brand not setup (cf snapshot-brand + setup-brand + build-atlas-complete upstream).

### HR3 · NOYAU preserved strict

5 éléments NOYAU (mécanique · format · phrase d'accroche · élément pivotal · équilibre copy/visuel · cf decompose-ad v2.0.0 Section 4 ANATOMIE) INCHANGÉS dans variant brand-side. Modifier le NOYAU casse la créa · violation canon · refus orchestrator.

### HR4 · CONTEXTE adapté brand-side canonical

5 refs CONTEXTE (audience · pain · proof · mécanisme · CTA) adaptées via matching canonical refs brand. Pas freelance · matching score required >0.6 sinon AskUserQuestion alternative.

### HR5 · MODIFIEURS opérateur-choice

5 modifieurs (canal · saisonnalité · ton · destination · offer attachée) opérateur-choice via AskUserQuestion (Phase 3 path A). Plusieurs valeurs possibles selon campagne cible.

### HR6 · Output opérateur-facing 100% humain

ZERO raw field name (audience_segment · context.pain_point_ref · etc.). ZERO registry ID exposé (mecanique-registry IDs · proof-registry IDs · angle-registry IDs). ZERO acronyme doctrine. Labels humains accessibles uniquement. Canon résonne back-end via creative.json sub-couche · cross-skill reproducibilité.

### HR7 · Lineage canon variant_of

Variant brand-side `brands/{slug}/produced/{CRT-M}.json` PERSISTED avec `variant_of: "CRT-NN-competitor"` (cf creative.schema v1.2 field). Lineage canon · traçabilité full · cycle apprentissage couches op-system v2.71.

## Cross-refs

- `docs/system/operational-system-doctrine.md` v2.71 (équation maître canonisée · 5 couches grammar)
- `docs/system/compositional-cartography.md` v3.1 (équation v3.1 canon)
- `docs/system/canonical-matrix-reasoning.md` (schema + matrice canon)
- `docs/system/investigation-posture.md` (5 sections IP synthese)
- Upstream sibling · `decompose-ad` v2.0.0+ (produces creative.json v1.2 sub-couche)
- Downstream sub-skills · `produce-copy-brief` (Path A) · `recompose-creative` v1.2.2+ (Path B fallback) · `promote-mecanique` future (Path C)

## Related canon

- `creative-mechanics-registry.md` (mecanique IDs canoniques · résonance back-end)
- `angle-registry.md` (angle IDs canoniques)
- `proof-registry.md` (proof IDs canoniques)
- `brands/{slug}/_snapshot.md` (brand state digest pré-load Phase 1)
