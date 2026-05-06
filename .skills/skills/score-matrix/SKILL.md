---
name: score-matrix
version: 1.1.0
type: producer
recommended_model: sonnet
subagent_safe: true
mode: proposed
operator_facing: true
triggers_fr:
  - "score la matrice"
  - "priorise les territoires"
  - "matrice scoring"
  - "top territoires"
  - "where to test next"
triggers_en:
  - "score matrix"
  - "prioritize territories"
  - "matrix scoring"
  - "top territories"
disambiguates_against:
  - weight-dimensions: "weight-dimensions calcule pondérations dimensions audience → angle (input). score-matrix CONSOMME ces weights pour scoring final matrice."
  - produce-paid-angles: "produce-paid-angles produit des angles individuels. score-matrix priorise les COMBINAISONS audience × angle."
consumes:
  - brands/{slug}/audiences/*/profile.json (sub-clusters)
  - brands/{slug}/audiences/*/dimension_weights.json (weight-dimensions output)
  - brands/{slug}/angles/*.json (angles populated)
  - brands/{slug}/brand.json (modulateurs strategic_context · à ajouter v2.35 ou via brand_equity_level + creative_zone proxy)
  - resources/canon/copy/* (référentiels)
produces_proposals_for:
  - brands/{slug}/scoring/matrix-{date}.json (matrice scorée + top territoires)
permissions:
  reads: [brands/, resources/]
  writes: [brands/{slug}/scoring/matrix-{date}.json via write_to_context]
  emits_events: [matrix_scored, territories_prioritized]
pipeline:
  preconditions: ["audiences populées avec dimension_weights", "angles compatibles disponibles", "brand modulateurs disponibles ou défauts"]
  postconditions: ["matrice scorée Sub-cluster × Source d'angle", "top 3-5 territoires identifiés", "trous identifiés pour exploration"]
prerequisites:
  - field: audiences/*/dimension_weights.json
    level: L1
    auto_pull: read_weight_outputs
    freshness_ttl_days: 30
  - field: brand.strategic_context
    level: L3
    fallback: proxy_brand_equity_level
    confidence_default: 0.6
  - field: audiences/*/profile.json
    level: L1
    auto_pull: read_audiences_profiles
    freshness_ttl_days: 60
  - field: angles/*.json
    level: L1
    auto_pull: read_brand_angles_existing
    freshness_ttl_days: 90
---

# score-matrix

Producer skill operator-facing. Clôt la Phase 3 doctrine cartographie. Consomme `weight-dimensions` outputs (v2.33) + audiences profile + angles + brand modulateurs. Produit la matrice scorée Sub-cluster × Source d'angle (formule canon Notion : Impact × 3 + Vitesse × 2 + Signal × 1, modulé 0.5 à 2). Termine sur top territoires + trous + action recommandée.

Cohérence cross-skill : sourcing weights précomputés via `weight-dimensions`, sources d'angle alignées canon V3 (`creative-formula.md`), compatibilité awareness verrouillée doctrine canonical-matrix-reasoning.

## Hard Rules

### Step 0bis · Prerequisite check (DRGFP v2.38)

Avant construction grille (Step 1), scanner prerequisites :

1. Lookup `audiences/*/dimension_weights.json` → si présents → consume silent · sinon flag _gaps suggestion run weight-dimensions chain
2. Lookup `audiences/*/profile.json` → required, L1 silent (au moins 1 audience nécessaire)
3. Lookup `angles/*.json` brand existing → silent · cellules sans angle = trous détectés (signal output)
4. Lookup `brand.strategic_context` → si présent → modulateurs full · si absent → L3 degraded · proxy `brand_equity_level` · confidence 0.6 · flag _gaps

Output state map + confidence_chain[] init.

Cross-ref doctrine : `docs/system/dependency-resolution-protocol.md`.

### HR1 · Construire la grille

Lignes = sub-clusters audience (depuis `profile.json` par audience_slug, champ `sub_clusters[]`).
Colonnes = 5 sources d'angle canon V3 : `audience_derived`, `product_derived`, `category_derived`, `brand_derived`, `temporal_cultural`.
Cellule = territoire potentiel (sub_cluster × source).

Cardinalité maîtrisée (canon canonical-matrix-reasoning) : sub_clusters ≤ 5 max par scoring run, sources fixes 5. Total 25 cellules max default.
Si plus de 5 sub_clusters disponibles : surface warning operator + propose batch (run sur top 5 par taille audience, signaler les autres pour run suivant). Ne PAS scorer 6+ silently.

### HR2 · Vérifier compatibilité par cellule

Règle dure canon (canonical-matrix-reasoning) : `awareness_movement.in (angle) ≤ awareness_dominant (sub_cluster)`.
Pour chaque cellule :
- Lister angles du fichier `brands/{slug}/angles/*.json` dont `source_type` matche la colonne ET `awareness_movement.in ≤` awareness du sub_cluster.
- Si 0 angle activable : `compatibility = vierge`, score = 0, skip scoring (mais marquer comme trou potentiel HR5).
- Si 1+ angles activables : `compatibility = fort` (3+) | `moyen` (1-2), passer à HR3.

Ne JAMAIS skip cette règle. Cellule incompatible = 0 hard.

### HR3 · Calculer score brut Impact × Vitesse × Signal

Pour chaque cellule compatible, le LLM raisonne contextuellement (jamais hardcoder) sur 3 axes 0-10 :

**Impact (0-10) · coefficient × 3**
- Volume audience : taille relative du sub_cluster vs autres sub_clusters de la marque.
- Fit produit : croiser top dimensions du `dimension_weights.json` de cette audience avec bénéfices produit (`spec.json#benefits`).
- Score = moyenne pondérée volume + fit, échelle 0-10.

**Vitesse (0-10) · coefficient × 2**
- Asset dispo : packshot existe (`brand.json#visual_identity`) ? canon copy lookup direct sur la source ?
- Effort production estimé : low → 8, med → 5, high → 2.
- Score = combinaison asset_ready + effort_inverted.

**Signal (0-10) · coefficient × 1**
- Preuves observées : angles brand-side similaires déjà validés (`learnings.json#validations`) ?
- Concurrents performant sur cellule similaire (`brand.json#competitors` croisé avec source_angle) ?
- Canon `validations[]` entries pour mécaniques pertinentes.

`score_brut = Impact × 3 + Vitesse × 2 + Signal × 1` (max 60).

### HR4 · Appliquer modulateurs brand (4 axes)

Lookup `brand.json#strategic_context` (v2.35+) ou défaut via proxy.

| Axe | Valeur | Coefficient |
|---|---|---|
| stade_brand | launch | × 1.2 (territoires d'éducation marché) |
| | growth | × 1.0 (default) |
| | scale | × 0.9 (territoires éprouvés) |
| | mature | × 0.8 (préserve plutôt que test) |
| moment_strategique | pmf | × 1.3 (territoires d'apprentissage) |
| | scaling | × 0.9 (winners only) |
| | defense | × 0.8 (cellules brand_derived) |
| | repositionnement | × 1.2 (reframes radicaux) |
| contexte_marche | nascent | × 1.2 (territoires éducatifs) |
| | mature | × 1.0 |
| | hyper_sature | × 0.8 (sauf reframe différenciant) |
| etat_atlas | vide | × 1.3 (fast-learning, scoring tolérant) |
| | partiel | × 1.0 |
| | consolide | × 0.9 (critères durcis) |

Si `strategic_context` absent : proxy via `brand_equity_level` (low → × 1.1, medium → × 1.0, high → × 0.95) appliqué uniformément sur axe stade_brand, autres axes = × 1.0 default.

`coefficient_cumule = stade × moment × marche × atlas`, capped `[0.5, 2.0]`.
`score_dynamique = score_brut × coefficient_cumule`.

Ne JAMAIS appliquer modulateurs hors bornes 0.5-2.

### HR5 · Identifier top territoires + trous + cellules vierges

- **Top territoires** : 3-5 cellules avec `score_dynamique` le plus haut, rank descendant.
- **Trous à combler** : cellules `compatibility = vierge` MAIS sub_cluster fort (top 3 par taille) ET source d'angle naturellement riche pour la marque (heuristique : audience_derived et product_derived prioritaires si trous). Signal pour run `produce-paid-angles`.
- **Cellules vierges acceptables** : compatibilité possible mais 0 angle dispo sur sub_cluster faible → noter sans flagger.

### HR6 · Persist matrix-{date}.json via write_to_context

Format canonique :

```json
{
  "computed_at": "ISO8601",
  "brand_slug": "...",
  "modulators_applied": {
    "stade_brand": "growth",
    "moment_strategique": "scaling",
    "contexte_marche": "mature",
    "etat_atlas": "partiel",
    "coefficient_cumule": 1.0
  },
  "matrix": {
    "sub_clusters": ["..."],
    "sources_angle": ["audience_derived", "product_derived", "category_derived", "brand_derived", "temporal_cultural"],
    "cells": [
      {
        "sub_cluster": "...",
        "source_angle": "...",
        "compatibility": "fort|moyen|vierge",
        "angles_activables": ["ANG-01", "ANG-03"],
        "impact": 7,
        "vitesse": 6,
        "signal": 4,
        "score_brut": 37,
        "score_dynamique": 44,
        "rank": 1
      }
    ]
  },
  "top_territoires": [...],
  "trous_a_combler": [...]
}
```

Path : `brands/{slug}/scoring/matrix-{YYYY-MM-DD}.json`. Mode `proposed`. Émettre events `matrix_scored` puis `territories_prioritized`.

### HR7 · Output operator-facing matrice ASCII

Ne JAMAIS exposer JSON brut. Toujours rendre vue compacte lisible :

```
═══════════════════════════════════════════════════════════════
{BRAND} · MATRICE SCORÉE · {date}
═══════════════════════════════════════════════════════════════
Modulateurs : stade {x} · moment {y} · marché {z} · atlas {w} · coeff cumulé {n}

┌────────────────────────────┬────────┬────────┬────────┬────────┬────────┐
│ Sub-cluster                │ aud-d  │ prod-d │ cat-d  │ brand-d│ temp-c │
├────────────────────────────┼────────┼────────┼────────┼────────┼────────┤
│ {sub_cluster_1}            │ 55 🔥  │ 42     │ 38     │ 0      │ 28     │
│ {sub_cluster_2}            │ 48     │ 52 🔥  │ 0      │ 35     │ 0      │
└────────────────────────────┴────────┴────────┴────────┴────────┴────────┘

TOP 3 TERRITOIRES
  1. {sub_cluster} × {source}  · score {n}  · {angles activables}
  2. ...

TROUS DÉTECTÉS (compatibles mais aucun angle)
  - {sub_cluster} × {source}  · run produce-paid-angles ?

→ Action recommandée : tester top 1 (run produce-copy-brief) · OU explorer top 2 trou
```

Marquer 🔥 sur top 1 par ligne. `0` sur cellules vierges. Aucun em-dash dans tout le rendu (substituer par `·`, virgule, deux-points).

### HR8 · Anti-patterns

- Ne JAMAIS scorer sans `dimension_weights.json` précomputés. Si absent : abort + propose `weight-dimensions` d'abord.
- Ne JAMAIS skip awareness compatibility (HR2). Cellule incompatible = 0 hard, jamais scorée.
- Ne JAMAIS hardcoder Impact / Vitesse / Signal. LLM raisonne contextuellement à chaque run.
- Ne JAMAIS appliquer coefficient cumulé > 2.0 ou < 0.5. Cap obligatoire.
- Ne JAMAIS exposer JSON brut à l'opérateur. Toujours rendre vue ASCII HR7.
- Ne JAMAIS scorer 6+ sub_clusters silently. Warning + batch obligatoire (HR1).
- Ne JAMAIS éditer le JSON directement. Mutation gate `write_to_context` obligatoire.

## Cross-refs

- Doctrine canon Notion Stride-Up · formule scoring brut + modulateurs 4 axes
- `weight-dimensions` v1.0 · sibling producer, output `dimension_weights.json` consommé en HR3
- `creative-formula.md` V3 · 5 sources d'angle canoniques colonnes matrice
- `docs/system/canonical-matrix-reasoning.md` · cardinalité ≤ 5, awareness compatibility hard rule
- `docs/system/skill-authoring-discipline.md` · frontmatter triad + lifecycle
- `produce-paid-angles` · downstream sur trous détectés
- `produce-copy-brief` · downstream sur top territoire validé
