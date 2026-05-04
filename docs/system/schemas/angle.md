# angle, schema couche stratégique

## Définition

Couche stratégique d'attaque, formule récursive Observation × Tension × Reframe × Bridge. Vit dans `brands/{slug}/angles/{ANG-N}.json`. Schema `resources/schemas/angle.schema.json` (v1.2). Post-v1.2, ne contient PLUS execution / intent / cta / mecanique / seasonality (migrés vers `creative.schema.json`, audit S55 D#391).

## Pourquoi

Capturer l'intention persuasive abstraite, transposable cross-formats. Un angle est jouable en VSL, en static, en thumbnail, en email, sans changer son ADN. Cette abstraction est ce qui permet la réutilisation et la production en série. Distinct de creative (instance déployée avec un format précis et une mécanique précise). Confondre les deux fait perdre la portabilité.

## Anatomie

| Champ | Type | Rôle | Source typique |
|---|---|---|---|
| `angle_id` | string | ANG-NN, stable, jamais réassigné | généré skill |
| `audience_slug` | string | Audience primaire de production | déclaré skill producer |
| `origin_axis` | enum | audience / product / category / brand / temporal-cultural | inféré contexte |
| `awareness_movement.in/out` | enum | Stage assumé au start, stage produit à la fin | raisonné skill |
| `lineage.*` | object | Refs canon copy (Schwartz, hook, framework) | light pass producer |
| `formula.observation/tension/reframe/bridge` | object | 4 atomes récursifs (light = summary, deep = atoms) | producer + decompose |
| `insight.modalité` | enum | formulé / implicite / absent | déduit ou validé |
| `compatibility[]` | array | Audiences compatibles (cross-audience reuse) | observé |
| `meta.validation_status` | enum | hypothesis → tested → validated → scaled → fatigued | learn-from-session |

## Best practices

- Light pass d'abord (summaries des 4 composants + lineage), deep pass uniquement quand l'angle entre en production (ROI sur l'effort de décomposition).
- Cohérence de la chaîne audience.awareness_dominant ≥ angle.awareness_movement.in. Si l'angle assume un stage plus avancé que l'audience, il ne joue pas.
- `lineage.*` doit pointer vers du canon réel (`resources/canon/copy/{layer}/{tool}.json`), pas du free text. C'est la traçabilité.
- `compatibility[]` se remplit par observation après tests, pas par hypothèse. Vide par défaut est correct.
- `insight` peut être `absent` (modalité), c'est un choix valide sur audience product-aware ou most-aware. Ne pas force-fit.

## Anti-patterns

| Symptôme | Pourquoi c'est un problème | Fix |
|---|---|---|
| Angle qui contient un CTA, un format, une mécanique | Confond angle (stratégie) et creative (instance) | Migrer vers creative.context et creative.execution |
| `pain_point` encodé dans angle | Le pain vit dans creative.context.pain_point ou profile.pain_points[] | Pointer vers la bonne entité |
| `insight.formulation` rempli alors que `modalité=absent` | Incohérence sémantique | Si formulation existe, modalité = implicite ou formulé |
| `awareness_movement.in > audience.awareness_dominant` | Angle joue sur un stage que l'audience n'a pas | Re-cibler audience ou reframe l'angle vers un stage plus tôt |
| `lineage.hook_canon_id` en free text au lieu d'un id canon | Brise la traçabilité, pas réutilisable | Pointer vers `resources/canon/copy/hooks/{id}.json` |

## Interaction avec autres schemas

- angle ← lit ← profile (audience.awareness_dominant, pain_points, voice)
- angle ← lit ← spec (formula.bridge.spec_activated, formula.bridge.benefit_served)
- angle → alimente → creative (creative.context.angle_ref pointe vers ANG-NN)
- angle → alimente → resources/canon/copy/* (lineage est le pont)

## Signaux pour Claude (non prescriptifs)

- Opérateur parle de format vidéo, hook visuel, mécanique CTA, durée, seasonality → drill `creative.schema`, pas angle. L'angle ne porte plus ces champs depuis v1.2.
- Demande "donne-moi un angle" sans audience définie → manque la fondation, angle est par-audience par construction. Propose d'abord setup audience.
- "L'angle a fonctionné en story mais pas en feed" → c'est un signal creative, pas angle. L'angle est format-agnostique, la variance vient du creative qui le décline.
- Insight absent sur 23 ads décomposées → normal, ~25% baseline empirique S55. Pas un bug.
- Plusieurs angles strictement identiques sur leurs 4 composants → soit dupes, soit l'opérateur a besoin d'une couche concept supérieure (à venir creative.concept_id).
- `validation_status: scaled` qui devient `fatigued` → signal pour produire un angle voisin (même origin_axis, reframe différent), pas pour relancer l'angle fatigué.

## Cycle de vie

Créé par `produce-paid-angles` (light pass : meta + lineage + formula summaries + insight déduit). Enrichi par `decompose-angle` (deep pass : atoms verbatim, source, sample_size, pivot_mechanism). Modifié par `learn-from-session` (test_results append, validation_status update). Lu par `creative-strategist`, `analyze-copy` (référence cross-check), `produce-creative-variants`. Pas de snapshot dédié, vit en lecture directe.
