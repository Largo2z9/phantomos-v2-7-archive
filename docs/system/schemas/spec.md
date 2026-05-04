# spec, schema produit

## Définition

Entité produit, matière brute factuelle. Vit dans `brands/{slug}/products/{product_slug}/spec.json`. Schema `resources/schemas/spec.schema.json` (v1.9).

## Pourquoi

Un produit a des faits vérifiables (ingrédients, mécanismes causaux, bénéfices, prix, contraintes réglementaires) qui doivent être encodés une fois et lus N fois par les skills downstream. Sans cette couche, chaque skill réinvente la roue ou hallucine. Spec capture la matière, les autres entités la transposent (offer la package, angle la stratégise, creative la met en scène). Ground truth pour toute production qui prétend parler du produit.

## Anatomie

| Champ | Type | Rôle | Source typique |
|---|---|---|---|
| `meta.slug` | string | Identifiant stable du produit | déclaré opérateur |
| `identity.product_category` | enum | physical / physical_electronic / digital / service | scrape ou opérateur |
| `identity.positioning` | string | Tagline factuel du produit | scrape page produit |
| `specs.composition[]` | array | Ingrédients structurés (pct, origin, INCI) | scrape + scrape étiquette |
| `specs.product_mechanism` | string | Mécanisme principal narratif | claim brand |
| `specs.mechanisms[]` | array | Mécanismes causaux atomisés (many-to-many) | scrape + raisonnement |
| `benefits[].chain` | array | Bénéfices avec chaîne functional → emotional | dérivé + verbatim_quotes |
| `problems_solved[]` | array | Pains adressés par le produit | VoM + raisonnement |
| `pricing` | object | Prix, devise, tier | scrape Shopify |
| `gift_economy` | object | DEPRECATED v2.29.0 | migré vers profile.buyer_user_split |

## Best practices

- Toujours adosser un claim numérique ou de mécanisme à un `verbatim_quotes[]` ou un `_source` (Trustpilot, étiquette, page produit).
- Utiliser `mechanisms[]` (many-to-many) quand un produit porte plusieurs mécanismes distincts. `product_mechanism` (string) reste pour le mécanisme dominant narratif.
- Tagger `_field_types` (observed / stated / derived / structured) sur les champs sensibles, c'est ce qui permet l'audit downstream.
- Pour ingrédients réglementés (cosmétique, food, pharma), remplir `inci`, `evidence_level` et `regulated_claim_status` sur les mécanismes.
- Append-only sur les champs sourcés. Si un fait change, log un nouvel item, ne réécris pas l'historique.

## Anti-patterns

| Symptôme | Pourquoi c'est un problème | Fix |
|---|---|---|
| Mécanisme produit dupliqué dans `product_mechanism` ET `mechanisms[]` | Drift de cohérence, skills downstream lisent une source ou l'autre | Choisir : `product_mechanism` pour le narratif dominant, `mechanisms[]` pour l'inventaire causal complet |
| Encoder l'audience cible dans `gift_economy` | gift_economy décrit l'audience (buyer ≠ user), pas le produit | Migrer vers `profile.buyer_user_split` |
| Claim numérique sans verbatim_quote | Triangulation impossible, hallucination probable | Sourcer ou flag `_field_types: stated` (claim brand non vérifié) |
| Bénéfice plat sans chaîne | Skills creative ne peuvent pas remonter functional → emotional | Remplir `benefits[].chain[]` au moins sur 2 niveaux |
| Promo brand-level encodée par produit | Drift, multiplie les écritures | Encoder dans `brand.json#promotions`, pas par spec |

## Interaction avec autres schemas

- spec ← lit ← brand (positioning, brand_equity_level pour calibrer le ton du spec output)
- spec → alimente → offer (chaque offer.json référence des produits par leurs slug spec)
- spec → alimente → angle (angle.formula.bridge.spec_activated pointe vers un mécanisme spec)
- spec → alimente → creative (creative cite le produit, ses bénéfices, ses claims)

## Signaux pour Claude (non prescriptifs)

- Opérateur parle de "mécanisme produit" ou "comment ça marche" → drill `spec.mechanisms[]` avant `brand.positioning`. Le mécanisme vit dans le spec.
- Mention pharma, cosmétique, EFSA, FDA, ingestible → check `evidence_level` et `regulated_claim_status` sur chaque mécanisme avant de produire un claim.
- Claim numérique cité par opérateur sans backing → triangulation requise (verbatim_quote, source, sample_size). Si rien, flag `incertain`.
- Bénéfice émotionnel cité sans chaîne functional sous-jacente → c'est probablement un angle, pas un bénéfice spec. Drill `benefits[].chain` ou propose à l'opérateur de migrer vers angle.
- Audience qui apparaît dans le spec → signal que l'opérateur confond product et profile. Repointer doucement vers `profile.json`.
- Ingrédient sans `pct` ni `class` sur un produit cosmétique ou nutrition → spec partiel, signal pour mine spec ou enrichissement.

## Cycle de vie

Créé par `setup-brand` (squelette) puis `snapshot-brand` (matière brute). Modifié par `mine-spec`, `learn-from-session`, `enrich-spec` via le mutation gate `write_to_context`. Lu par à peu près tout, `produce-paid-angles`, `analyze-copy`, `audit-meta-account`, `creative-strategist`, `decompose-creative`. Snapshot regen automatique sur mutation (build-brand-snapshot.py).
