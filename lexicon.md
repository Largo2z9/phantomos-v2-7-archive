# PhantomOS, lexicon opérateur

> **CONTEXT:** Vocabulaire user-facing pour opérateurs DTC paid acquisition. Termes métier classiques que l'opérateur utilise déjà dans son langage quotidien.
> **OBJECTIVE:** Réduire la friction de découverte produit. Pas de vocabulaire interne PhantomOS imposé.
> **TYPE:** Reference user-facing, slim.
> **AUDIENCE:** Opérateurs DTC paid (founder solo, agency operator, growth lead).
> **CANON INTERNE:** Voir `canon.md` (57+ entrées système, doctrines, disciplines, briques typées, méta-vocabulaire) pour les contributeurs et l'équipe.

---

## Brand

La marque que l'opérateur encode dans PhantomOS. Slug, identité courte, contacts, finances, concurrents. Stockée dans `brands/{slug}/brand.json`.

## Connected source

Plateforme externe connectée à PhantomOS pour pull data (analytics, perf, conversions) ou push assets (LP, ads, emails). Typée par catégorie : paid ads (Meta, TikTok, Google Ads), analytics (GA4, Shopify Analytics), e-commerce (Shopify, Stripe), email/SMS (Klaviyo, Postscript), attribution (TripleWhale, Northbeam), creative intelligence (Atria, Foreplay).

*Full taxonomy and field reference : `docs/internal/canon.md`.*

## Audience

Une cible identifiée pour la marque. Profil psychographique, pains, bénéfices, jobs to be done. Sourcée par observation (verbatims, reviews, threads) ou inférence. Hiérarchisable en cluster, sub-cluster, sub-sub-cluster.

## Angle

Un axe d'attaque marketing. 4 types : Observation (un constat sourcé), Tension (un conflit interne audience), Reframe (un changement de cadrage), Bridge (un pont du connu vers la solution). Indépendant des audiences au stockage, croisé à la production.

## Creative

Une publicité produite : statique, vidéo, UGC, advertorial. Liée à un angle, à une mécanique créa (témoignage, démonstration, podcast, skit, etc.) et à une audience cible. Performance trackée (CTR, CPM, ROAS).

## Campagne

Structure paid sur une plateforme (Meta, TikTok, Google Ads). Contient ad sets (audiences) et ads (creatives). Track par budget, métriques de perf, objectif (acquisition, retargeting, retention).

## Landing page

Page d'atterrissage du trafic paid. Variantes typées : advertorial (entrée par la voix audience, pivot produit à 50% scroll), comparative (vs concurrents), capture (lead magnet), classique (PDP enrichie).

## Test

Une hypothèse instanciée pour validation. Format typé : hypothèse, métrique, sample minimum, durée, règle de décision. Sans test instancié, "validated" n'est que cosmétique.

## Résultat

Sortie chiffrée d'un test. Métrique mesurée (CTR, CR, ROAS, CAC, LTV), valeur observée, baseline, delta. Statut : validated, invalidated, inconclusive, fatigued.

## Apprentissage

Fait opérationnel append-only retenu d'un test ou d'une opération. Workaround, compliance, résultat de test, observation. Réutilisable cross-marques pour densifier la stratégie.

## Positioning

Position de marque sur le marché. Antagoniste explicite (contre quoi la marque se définit), distinctive promise (sa promesse unique), point de vue catégorie. Inclut voice et ton.

## Produit

Ce que la marque vend. Composition, mécanisme, claims, problème adressé, prix. Référence dans toutes les opérations paid (creatives, LP, audiences ciblées).

## Offre

Comment un produit est présenté commercialement : prix, bundle, gifting, subscription, refill. Plusieurs offres possibles par produit. Vit sous le produit dans l'arborescence.

---

*Dernière mise à jour : 2026-05-02 (S53). Lexicon opérateur slim créé en split du canon interne. 13 termes user-facing, vocabulaire métier classique DTC paid acquisition. Aucun jargon interne PhantomOS imposé. Canon complet (57+ entrées système, doctrines, disciplines, briques typées, méta-vocabulaire) déplacé dans `canon.md` pour audience équipe et contributeurs.*
