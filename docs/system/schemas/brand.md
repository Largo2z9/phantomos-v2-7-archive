# brand, schema racine

## Définition

Entité brand racine. Identité, positionnement, ton, financials, market context, brand_equity_level, creative_zone. Vit dans `brands/{slug}/brand.json`. Schema `resources/schemas/brand.schema.json` (v2.2). Source de vérité pour tout ce qui calibre les skills à l'échelle marque.

## Pourquoi

Tous les enfants (spec, profile, angle, creative) lisent du contexte brand pour calibrer leur output. Sans cette racine, chaque skill devine le ton, le niveau de notoriété, la zone créative viable. Brand encode une fois, les skills lisent N fois. Particulièrement critique pour `brand_equity_level` (curseur copy/visual) et `creative_zone` (zone observée empiriquement après N créas décomposées).

## Anatomie

| Champ | Type | Rôle | Source typique |
|---|---|---|---|
| `meta.slug` | string | Identifiant brand stable | déclaré opérateur |
| `meta.stage` | enum | launch / growth / scale / mature / decline | déclaré + observé |
| `purchase_driver` | enum | pain / desire / status / utility / identity / mixed | déclaré ou inféré |
| `driver_blend` | object | Resolution rules quand purchase_driver=mixed | déclaré |
| `audience_trees[]` | array | Marketplaces multi-sided (creators+readers, hosts+guests) | déclaré |
| `identity.*` | object | Mission, vision, story, personality, values | scrape + opérateur |
| `positioning.*` | object | Value prop, différenciation, claims | scrape + opérateur |
| `tone_of_voice.*` | object | Registre, attributs, do/don't | observé + opérateur |
| `financials.*` | object | Pricing position, AOV, CAC cible, marges | déclaré |
| `competitors[]` | array | Concurrents directs, indirects | observé + opérateur |
| `brand_equity_level` | enum | low / medium / high (canon V3 §4.3) | déclaré + observé |
| `creative_zone` | object | min/max/dominant sur curseur copy-visual 0-10 | observé empirique |
| `promotions` | array | Promos brand-level (free ship 69€+, GWP threshold) | déclaré |

## Best practices

- Declared positioning + observed positioning : opérateur déclare son positionnement voulu, skills d'audit creative observent ce qui sort réellement. Les deux co-existent, le delta est un signal.
- `creative_zone` se remplit à mesure que `decompose-creative` traite des ads. <10 créas = hypothèse, log `_observed_on_n_creatives`.
- Promotions structurelles (free ship threshold, GWP brand-wide) vivent dans `brand.json#promotions`, pas dans chaque offer.json. Évite la duplication.
- `brand_equity_level` calibre le curseur. low → besoin hook + angle + proof empilés. medium → hook ou angle peuvent porter seuls. high → logo seul suffit.
- Marketplace ou two-sided → setup `audience_trees[]` AVANT de créer les profiles. Sinon les profiles ne savent pas à quel arbre rattacher leur driver.

## Anti-patterns

| Symptôme | Pourquoi c'est un problème | Fix |
|---|---|---|
| Confondre `brand_equity` (perception cible, positioning) et `brand_equity_level` (canon V3 niveau low/med/high) | Deux concepts distincts qui se télescopent | brand_equity_level = niveau objectif de reconnaissance, positioning = ce qu'on veut être perçu |
| Promo encodée par produit alors qu'elle est brand-wide | Drift, multiplie les écritures, source de vérité éclatée | Migrer vers `brand.json#promotions`, lire depuis là |
| `creative_zone` rempli avec <5 créas décomposées | Hypothèse qui passe pour observation | Tagger `_observed_on_n_creatives`, signaler hypothesis-grade |
| `purchase_driver: mixed` sans `driver_blend` | Resolution rules absentes, downstream casse | Remplir driver_blend (primary, secondary, ratio) |
| Marketplace sans `audience_trees[]` | Profiles enfants ne savent pas hériter de quel driver | Setup audience_trees d'abord (slug, side, monetization, driver) |

## Cascade purchase_driver

`purchase_driver` est un champ canonique avec cascade brand → audience_tree → profile. Trois niveaux, un seul résolu lu par les producers downstream.

- **Niveau 1, brand-wide** : `brand.purchase_driver` (default pour toutes les audiences de la brand).
- **Niveau 2, tree-level** (marketplaces only) : `brand.audience_trees[].purchase_driver` override le default brand pour toutes les audiences rattachées à ce tree (ex creators side vs readers side, hosts vs guests).
- **Niveau 3, audience-level** : `profile.purchase_driver` (résolu, `_field_types: derived`). Calculé depuis la cascade brand → tree (si la audience est rattachée à un tree) → null si non résolu. Skills doctrine : lire `profile.purchase_driver` d'abord (canon résolu), fallback `brand.audience_trees[{tree}].purchase_driver` puis `brand.purchase_driver` si null.
- **Mécanisme regen** : toute mutation de `brand.purchase_driver` ou `brand.audience_trees[].purchase_driver` re-déclenche la résolution sur les profiles concernés via mutation gate (skill `recompute-derived-fields` ou hook équivalent). Profile `purchase_driver` n'est jamais édité manuellement (champ derived).
- **Cross-refs** : `resources/schemas/brand.schema.json` (canonique), `resources/schemas/profile.schema.json` (résolu derived), `docs/system/architecture.md § Cascade rules` (pattern générique), `docs/system/field-types.md` (sémantique derived).

## Interaction avec autres schemas

- brand → alimente → spec (positioning, tone calibrent les outputs spec)
- brand → alimente → profile (purchase_driver cascade sauf override, audience_trees structure les profiles marketplaces)
- brand → alimente → angle (brand_equity_level calibre l'optionalité du concept dans l'angle)
- brand → alimente → creative (creative_zone calibre le curseur copy/visual, promotions injectent les modificateurs brand-level)
- brand → alimente → offer (promotions brand-level cascadent dans les offer outputs)

## Signaux pour Claude (non prescriptifs)

- `brand_equity_level: low` → besoin de stacker hook + angle + proof dans tout output creative. Logo nu ne fait rien.
- `brand_equity_level: high` → option "concept only" devient viable (Apple, Liquid Death). Skills creative peuvent proposer des outputs minimalistes.
- Promotion mentionnée par opérateur (free ship, GWP) sans encodage brand → drill `promotions[]`, propose encodage.
- Marketplace mentionné (Substack, Airbnb, Etsy) → check `audience_trees[]`. Si vide, c'est probablement la première chose à setup.
- Concurrent cité par opérateur sans encodage → propose `competitors[]` ajout, c'est du contexte qui ressort souvent dans angles category-derived.
- Stage `decline` ou `mature` sur brand qui claim positioning innovation → tension brand_strategy vs brand_stage, signal pour challenger.

## Cycle de vie

Créé par `setup-brand` (squelette identité + positioning hypothesis) puis `snapshot-brand` (matière scrape). Modifié par `enrich-brand`, `learn-from-session`, `decompose-creative` (creative_zone observé) via mutation gate. Lu par à peu près tout skill, c'est la racine. Snapshot regen sur mutation.
