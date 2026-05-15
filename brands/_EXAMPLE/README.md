# `_EXAMPLE` · Brand pédagogique fictive Stepprs

> Mock brand fictive · **foot care insoles DTC** inspirée de stepprs.com. Vitrine canon PhantomOS v2.68 pour comprendre à quoi ressemble un territoire de marque bien posé. **NE PAS MODIFIER.** Ignored par `FIRST ACTION` canon (folder prefix `_`).

## Pourquoi cet exemple existe

PhantomOS encode le savoir métier d'une marque en substrat stable (territoire) qui survit aux sessions et alimente la production à la demande (briefs · creatives · ad copy). Cet `_EXAMPLE` te montre comment se traduit ce principe en JSON concrets · annotations canon-aware · cross-refs résolus.

Lis-le avant ta première brand · puis reviens-le consulter quand tu te demandes "à quoi ça doit ressembler quand c'est bien posé".

## Par où commencer · ordre de lecture suggéré

| # | Fichier | Ce que ça démontre |
|---|---|---|
| 1 | `brand.json` | Identity · positioning · purchase_driver · driver_blend · brand_equity_level · creative_zone · competitors · awareness_distribution. Le **squelette stable** de la marque. |
| 2 | `products/massage-insoles/spec.json` | Spec produit avec **4 arbres compositional cartography v3.1** · composition (3 couches) → 4 mécanismes typés → 5 benefits chained avec emotional_signal + latency + evidence_verbatim |
| 3 | `products/massage-insoles/offers.json` | Offer_groups[] · 1 standalone + 3 bundles volume tiered + 3 bundles thématiques + guarantees + shipping rules |
| 4 | `audiences/workers-shifts/profile.json` (mère) puis `nurses-12h/` `warehouse-10h/` `hospitality-retail/` (sous-poches) | Pattern **parent/enfants canon v2.64 sémantique pure**. Mère pose scope général · sous-poches héritent + spécificity_modifiers (trigger · context · vocab spécifiques). |
| 5 | `audiences/chronic-pain-45/profile.json` (mère) puis `plantar-fasciitis-diagnosed/` `heel-pain-general/` (sous-poches) | Démontre **awareness divergence dans le tree** · mère `solution_aware` · sous-poches `product_aware` vs `problem_aware` selon trigger. |
| 6 | `audiences/*/pain_points/PNT-*.json` + `objections/OBJ-*.json` | **Sub-collections canon v2.64** · pain shared = stocké mère · pain spécifique = stocké sous-poche. Chain `surface → consequence → deep` · severity discriminante + tier marker primary/secondary. Cross-refs `mechanisms_addressed[]` + `benefits_served[]`. |
| 7 | `products/massage-insoles/frictions/FRC-*.json` | **Friction sub-product canon v2.64** · friction usage produit · cross-refs `affected_audiences[]` + `affected_pain_points[]` + `mechanisms_workaround[]`. |
| 8 | `angles/ANG-*.json` | **Compositional cartography v3.1 · formula OTRB** · Observation + Tension + Reframe + Bridge · lineage (hook · framework · archetype) + compatibility + cross_refs canonical. 7 angles distribués sur 5 origin_axis (audience · product · category · brand · temporal-cultural). |
| 9 | `roadmap.json` | **4ème arbre canon** · phases timeline + mix axes weighted + production_status + relations cross-entités denormalized. |
| 10 | `status.json` | Niveau de complétion canon + flag `is_example: true`. |

## Doctrines canon démontrées · mapping fichier → doc

| Fichier | Doctrine canon démontrée | Doc reference |
|---|---|---|
| Tous JSON | Substrat stable canonisé · territoire de marque | `docs/system/territory-discipline.md` (v2.67) |
| `brand.json` `spec.json` | Compositional cartography v3.1 · 4 arbres + matrice + modulateurs | `docs/system/compositional-cartography.md` |
| `audiences/*/profile.json` parent/enfants | Sub-audience sémantique pure v2.64 | `docs/system/schema-encoding-discipline.md` |
| `pain_points/PNT-*.json` chain surface→consequence→deep | Pain-benefit chain doctrine v2.60 | `docs/doctrine/pain-benefit-chain-doctrine.md` |
| `objections/OBJ-*.json` tier + severity discriminante | Objections mapping doctrine | `docs/doctrine/objections-mapping-doctrine.md` |
| `angles/ANG-*.json` formula OTRB | Angle anatomy doctrine + canonical-matrix-reasoning | `docs/doctrine/angle-anatomy-doctrine.md` + `docs/system/canonical-matrix-reasoning.md` |
| `audiences/*/` cartography parent/enfants 3 niveaux | Audiences cartography doctrine + map-audiences skill canon | `docs/doctrine/audiences-cartography-doctrine.md` |
| `_meta.is_example` + ignored canon | FIRST ACTION canon · folders prefix `_` ignored | `CLAUDE.md` root workspace-template |

## Ce que tu peux copier · ce que tu ne dois pas copier

**Copie le squelette** ·
- Structure des dossiers (`brands/{slug}/products/{p}/` · `audiences/{a}/pain_points/PNT-XX.json` · etc.)
- Pattern des `_field_types` riche per field (stated/observed/derived/structured)
- Annotations `$comment` quand un choix est non-trivial (positionning · pain category · etc.)
- Cross-refs canonical IDs (PNT-XX · OBJ-XX · FRC-XX · ANG-XX) entre les fichiers

**Ne copie pas** ·
- Mock data financials (revenue $1.2M/mois · LTV $65 · etc. inventés pédagogie)
- Verbatims clients (Mike Kowalski · Dean H · etc. captés du scrape Stepprs · pas applicable à ta marque)
- Audience labels (workers-shifts · chronic-pain-45 · etc. spécifiques Stepprs)

## Annotations canon-aware

Chaque fichier porte ·
- `$comment` racine explicite "EXEMPLE pédagogique · vitrine canon X"
- `_meta.is_example: true` (gate canon supplémentaire)
- `_meta.example_canon_showcased[]` · liste explicite des doctrines canon démontrées
- `_field_types` riche per field
- `validation_status: "validated"` (par construction pédagogique · pas via test ROAS réel)

## Pour aller plus loin

- **Construire ta brand** · lance `/onboard-brand` (chain `setup-brand` → `snapshot-brand` → `validate-resources`) ou `/build-atlas-complete {brand_slug}` (chain progressive cartography v2.68 · gates light entre paliers Phase 1 Macro → Phase 2 Drilling → Phase 3 Audiences hiérarchique → Phase 4 Enrichissement)
- **Doctrine territoire substrat** · `docs/system/territory-discipline.md`
- **Doctrine progressive-cartography** · `docs/system/progressive-cartography-discipline.md`
- **Catalogue skills canon** · `.skills/README.md` + `.skills/_manifest.json`
