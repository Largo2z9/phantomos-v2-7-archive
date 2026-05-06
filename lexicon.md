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

Un axe d'attaque marketing. Composé via une formule récursive Observation × Tension × Reframe × Bridge (chaque composant typé en sous-atomes). Origine typée par `origin_axis` (5 valeurs : audience-derived, product-derived, category-derived, brand-derived, temporal-cultural). Indépendant des audiences au stockage, croisé à la production. Schema : `angle.schema.json` v1.1+. Détails : `docs/system/creative-formula.md`.

## Creative

Une publicité produite : statique, vidéo, UGC, advertorial. Instance déployée d'un Concept (objet intent persuasive). Liée à un angle, à une mécanique créa (témoignage, démonstration, before-after, etc.) et à une audience cible. Performance trackée (CTR, CPM, ROAS).

## Concept vs Creative vs Variant

Concept = objet intent persuasive (audience × insight × angle × mécanique). Stable, transposable. Identifié par `concept_id`. Creative = instance déployée d'un concept (1 créa = 1 fichier). Variant = créa du même `concept_id` avec 1-2 variables changées. Encoded : `creative.schema.json#concept_id`, `#variant_of`, `#variant_axis`.

## Insight

Vérité non-dite verbalisée. Phrase que la cible pense mais n'a jamais entendue formulée. Distinct de pain_point (problème observable), tension (gap actuel/désiré), JTBD (job hiré au produit). Quatre plans MECE. Modalité : formulé · implicite · absent. Status : déduit (light pass) · validé (deep pass via VoC) · incertain. Encoded : `creative.schema.json#context.insight` + `angle.schema.json#insight`.

## Pain_point

Problème observable subi par l'audience. Visible dans verbatims VoC. Distinct de insight (révélation). Composant CONTEXTE de la formule canon V3 (`docs/system/creative-formula.md` §4.2).

## Tension

Gap entre état actuel et état désiré. Composant de la formule angle (Observation × Tension × Reframe × Bridge). Sous-atomes : `state_actual`, `state_desired`, `reason_blocked`. Distinct d'insight (qui verbalise la tension).

## JTBD (Jobs To Be Done)

Job que la cible "embauche" le produit pour accomplir. Framework Christensen. Distinct de pain_point (problème) et insight (vérité non-dite).

## Mécanique (creative)

Device structural narratif d'une créa. Ex : testimonial, before-after, problem_solution, comparison, demo, statement, curiosity_teaser, emotional_reframe. Source : `creative-mechanics-registry.md` (SSOT, ~25-29 fiches typées). Référencé par `creative.schema.json` et `angle.schema.json` par id (free string). **Ne pas confondre avec Mechanism (spec)** = chaîne causale produit (ex KSM-66 → cortisol).

## Mechanism (spec)

Chaîne causale entre une spec produit et un bénéfice. Champ typé : `target`, `mode_of_action`, `time_window`, `evidence_level`, `market_sophistication`, `triggered_by_specs[]`. Schema : `spec.schema.json#mechanisms[]` (v2.28 : mono → many). **Ne pas confondre avec Mécanique (creative)**.

## Atlas canon copy

Référentiel typé partagé de 11 couches × 58 fiches du copywriting (frameworks, hooks, angles, niveaux-schwartz, archetypes-voix, formules-titres, objections, construction-offre, leads, formats-livrables, persuasion). Sources : Schwartz, Cialdini, Halbert, Sugarman, Hormozi, Carlton, Jung. Storage : `resources/canon/copy/{layer}/{tool}.json`. Schema : `canon-tool/1.0`. Skills consume + feed via `validations[]` (atlas vivant brand-spécifique). Doctrine : `docs/system/atlas-canon-copy.md`. Releases : v2.26.0 (fondation) + v2.27.0 (skills branchés).

## Atlas, 4 senses MECE

Quatre acceptions cohabitent. Lever ambiguïté avant tout output opérateur.

### 1. Atlas canon copy (référentiel cross-brand, v2.26)
Référentiel typé partagé, 11 couches × 58 fiches. Read-only ship. Doctrine copywriting partagée tous brands. Source : `docs/system/atlas-canon-copy.md`. Storage : `resources/canon/copy/{layer}/{tool}.json`. Schema : `canon-tool/1.0`.

### 2. Atlas vivant brand-spécifique (boucle validations, v2.27)
Mécanique compound · journal d'usage local enrichi par chaque output skill via `validations[]` append-only. Pas un référentiel, une trace empirique. Promotion via `learn-from-session` operator gate. Transforme atlas canon générique en atlas-validé brand-spécifique au fil de l'usage.

### 3. Atlas state modulator (reporté D#390)
Futur modulateur visuel d'état couche représentation. **PAS shippé v2.32**. Gated sur skill matrice représentation visuelle future. Ne pas exposer opérateur tant que non livré. Concept structurellement validé (vide/partiel/consolidé) mais sans implémentation code.

### 4. Atlas brand · cartographie holistique data e-commerce (v2.36)
La somme structurée audiences + products + angles + creatives + scoring + verbatims + tests d'une brand. Concept canonique upstream pour désigner toute la matière data e-commerce d'une brand. Équivaut Notion Stride-Up "Données Atlas" canonical UI label. Rendu via `/phantom kara` (mode brand) qui surface les 6 entités brand (brand · spec · offers · profile · learnings · strategy) + creatives produced + matrice scorée. Doctrine : `docs/system/atlas-brand.md`.

**Distinction critique** :
- Sense 1 (atlas canon copy) = référentiel cross-brand doctrine copywriting (read-only, partagé)
- Sense 2 (atlas vivant) = mécanique compound validations[] DANS l'atlas brand
- Sense 3 (atlas state) = modulateur reporté
- **Sense 4 (atlas brand) = la cartographie elle-même** d'une brand spécifique (sa data holistique)

## Atome irréductible

Élément (mot, image, structure) sans lequel l'ad meurt. Test : *"si je retire/change cet atome, mesure-t-on un delta de performance ?"* Doctrine S55. Encoded : `creative.schema.json#atome_irreductible {element, delta_si_change}`. Distinct de `perceptual_pivot` (sous-couche `formula.reframe`) et `stop_scroller` (binôme hook + visual canon V3). Trois plans distincts.

## Awareness stage

Niveau de conscience (Schwartz) : unaware · problem-aware · solution-aware · product-aware · most-aware. 5 stages canoniques. Présent dans : `profile.schema` (`audience.market_position.awareness_level`), `angle.schema` (`lineage.awareness_stage` + `awareness_movement.in/out`), canon copy (`niveaux-schwartz/conscience.json`). Aligned cross-schemas (audit S55).

## Schwartz

Eugene Schwartz, Breakthrough Advertising (1966). Auteur du framework awareness × sophistication 5×5 utilisé canon copy. Le concept canonique est `awareness` (l'état de conscience), pas `schwartz` (l'auteur). Field name canonique : `awareness_stage` (pas `schwartz_conscience`).

## Persona vs Audience

Audience = canon. Cible globale, niveau macro. Stockée : `profile.schema.json`. Persona = alias surface opérateur (autorisé en mode parlé), avec sous-rôles buyer/user quand split (B2B, cadeau, pet, kids).

## Origin_axis (angle)

Source de l'angle : audience-derived · product-derived · category-derived · brand-derived · temporal-cultural. 5 valeurs canon V3. Renommage v1.2 (était `source` racine, polysémique). Distinct de `formula.observation.source` (citation Trustpilot/Reddit).

## Lineage

Chaîne d'IDs canon référencés par un output de skill. Data layer. Ex : `angle.lineage = {hook_canon_id, framework_canon_id, archetype_canon_id, ...}`. Distinct de l'intégrité compositionnelle (semantic layer doctrine) et de la validation chaîne (check mécanique `validate-resources`).

## Confidence propagation (v2.37+)

Algèbre canonique de propagation confidence cross-skill. Default `min` (defensive, conservative). Override par skill via frontmatter `confidence_propagation: {min|multiplicative|weighted_avg|passthrough|local_only}`.

Empêche data loss silencieux du signal d'incertitude sur chain 4+ skills (red team finding A2 v2.36).

Audit trail visible via `confidence_chain[]` (validation-state.json composite v2.32+).

Doctrine complète : `docs/system/confidence-propagation.md`.

## Dependency Resolution & Gap-Filling Protocol (DRGFP) (v2.38+)

Doctrine canonique gap-filling appliquée au Step 0bis de chaque skill PhantomOS. 3 niveaux : L1 auto-fill silent (source authoritative dispo) · L2 ask-operator gate (choix stratégique requis) · L3 degraded + flag (output partial avec confidence). Routage binaire default L1 > L3 > L2.

Frontmatter SKILL.md déclaratif `prerequisites[]` validé schema v2.37. Step 0bis prerequisite_check scanne et arbitre.

Empêche silent corruption (L1 sans freshness), ask fatigue (L2 cumul), output flou (L3 sans audit trail). Couplé confidence-propagation v2.37 + canon-tool schema v1.1.

Doctrine complète : `docs/system/dependency-resolution-protocol.md`.

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

*Dernière mise à jour : 2026-05-04 (S55). Enrichissement post audit nomenclature S55 + releases v2.26-v2.28.1 : ajout 14 entrées (Concept vs Creative vs Variant, Insight, Pain_point, Tension, JTBD, Mécanique creative, Mechanism spec, Atlas canon copy, Atome irréductible, Awareness stage, Schwartz, Persona vs Audience, Origin_axis, Lineage). Distinctions MECE explicites : pain_point ≠ tension ≠ insight ≠ JTBD (4 plans), Mécanique creative ≠ Mechanism spec (2 plans disjoints), atome_irreductible ≠ perceptual_pivot ≠ stop_scroller (3 plans), Concept ≠ Creative ≠ Variant. Source : largo-kb decisions.md D#382, D#383, D#391.*

*S53 (2026-05-02). Lexicon opérateur slim créé en split du canon interne. 13 termes user-facing, vocabulaire métier classique DTC paid acquisition. Aucun jargon interne PhantomOS imposé. Canon complet déplacé dans `canon.md` pour audience équipe et contributeurs.*
