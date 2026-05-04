# profile, schema audience

## Définition

Entité audience. Macro (cluster, sub-cluster) + persona (detail psychologique, voix, objections). Vit dans `brands/{slug}/audiences/{slug}/profile.json` ou `brands/{slug}/audiences/{tree-slug}/{slug}/profile.json` pour brands marketplaces (audience_trees[]). Schema `resources/schemas/profile.schema.json`.

## Pourquoi

La psychologie audience est la matière la plus réutilisée par les skills (angle, creative, copy, audit). Sans entité dédiée, chaque skill réinvente le persona, les pains drift, la voix devient générique. Profile centralise pour permettre la cohérence cross-skills et l'évolution append-only à mesure que le VoM s'accumule.

## Anatomie

| Champ | Type | Rôle | Source typique |
|---|---|---|---|
| `meta.slug` | string | Identifiant audience | déclaré opérateur |
| `meta.scope` | enum | macro / sub-cluster / persona | calibré skill |
| `meta.validation_status` | enum | hypothesis / observed / validated | learn-from-session |
| `psychology.awareness_dominant` | enum | unaware → most-aware (Schwartz) | mine-voc + raisonné |
| `psychology.sophistication` | enum | v1 → v5 | mine-voc + raisonné |
| `pain_points[]` | array | Pains structurés (intensity, frequency, verbatim) | mine-voc |
| `benefits[]` | array | Bénéfices recherchés, miroir des pains | mine-voc |
| `objections[]` | array | Frictions à l'achat, contre-arguments | mine-voc |
| `decision_process` | object | Triggers, recherche, comparaison | déduit + observé |
| `voice.key_expressions[]` | array | Verbatims signature de l'audience | mine-voc |
| `buyer_user_split` | object | Quand buyer ≠ user (gift, B2B-to-end-user) | déclaré ou observé |
| `persona_archetype` | string | Archetype Jung / 16personalities si pertinent | inféré |

## Best practices

- Hypothesis-grade (jamais minée VoM) → run `mine-voc` avant de produire des angles. Angle sur audience hypothèse fait peser le risque sur la première campagne.
- Awareness_dominant explicite et sourcé. C'est le champ le plus consulté par les producers downstream.
- 8 schémas detection à appliquer pendant mine-voc (Purchase Driver, Problem Map, Decision Drivers, Sophistication Stage, Voice Markers, Objection Map, Status Game, Identity Anchor). Cf `audience-cartography.md`.
- `key_expressions[]` doit contenir des verbatims, pas des reformulations. Si l'audience dit "j'en ai marre de me sentir lourde", garde-le mot pour mot.
- `buyer_user_split` quand pertinent (cadeau, parents pour enfants, achat pro pour terrain). Permet aux skills creative de décider si on parle au buyer ou à l'user.

## Anti-patterns

| Symptôme | Pourquoi c'est un problème | Fix |
|---|---|---|
| Audience hypothesis-grade > 30j sans VoM mining | Hypothèse qui se solidifie en fact par négligence | Flag dans pending-validations, run mine-voc |
| buyer et user fondus en un seul persona quand le contexte est gift | Skills creative ne savent pas à qui parler | Split via `buyer_user_split.buyer` et `.user` |
| `key_expressions[]` reformulé en propre | Perd la voix native, skills creative outputtent du copy générique | Verbatim only, sourcer Trustpilot/Reddit/interview |
| pain_points sans intensity ni frequency | Skills ne savent pas prioriser | Tagger au minimum intensity (low/med/high) |
| Sub-cluster créé avant que le macro ait été validé | Architecture audience qui drift, sub n'hérite pas correctement | Valider macro d'abord, sub vient en raffinement |

## Champs derived

- `profile.purchase_driver` est `_field_types: derived`. Source : cascade brand → audience_tree (si la audience est rattachée à un tree marketplace) → profile. Skills lecture : prendre `profile.purchase_driver` d'abord (canon résolu), fallback `brand.audience_trees[{tree}].purchase_driver` puis `brand.purchase_driver` si null. Ne jamais éditer manuellement (derived). Recompute automatique via mutation gate à chaque mutation de la cascade amont (`brand.purchase_driver` ou `brand.audience_trees[].purchase_driver`). Voir `docs/system/schemas/brand.md § Cascade purchase_driver` pour la doctrine canonique et `docs/system/field-types.md` pour la sémantique derived.

## Interaction avec autres schemas

- profile ← lit ← brand (purchase_driver cascade brand → tree → profile, audience_trees pour marketplaces)
- profile → alimente → angle (audience_slug, awareness_dominant, pain_points)
- profile → alimente → creative (audience cible, voix native)
- profile ← alimente ← `mine-voc` outputs (verbatims sourced Reddit, Trustpilot, YouTube)

## Signaux pour Claude (non prescriptifs)

- Opérateur dit "mon audience" sans avoir setup → profile manquant, propose `setup-audience` avant tout producer.
- Audience hypothesis-grade et l'opérateur veut produire angles → flag silencieux, propose `mine-voc` d'abord, ne refuse pas mais signale le risque.
- Discussion qui tourne autour de pains très spécifiques → drill `pain_points[]`. Si le pain n'y est pas, c'est un trou VoM.
- Mention "le client final n'est pas l'acheteur" → drill `buyer_user_split`. Si vide, propose encodage.
- Voix qui sonne corporate dans les outputs creative → check `voice.key_expressions[]`, probablement vide ou reformulé.
- Audience avec awareness_dominant unaware sur catégorie mature → bizarre, signal pour challenger soit l'audience soit le market_position brand.

## Cycle de vie

Créé par `setup-audience` (squelette hypothesis) puis enrichi par `mine-voc` (verbatims, pains, objections, voice). Modifié par `learn-from-session` (validation_status, ajout verbatims) via mutation gate. Lu par `produce-paid-angles`, `creative-strategist`, `analyze-copy`, `audit-copy`. Snapshot regen sur mutation.
