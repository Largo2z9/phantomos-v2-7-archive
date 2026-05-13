# PhantomOS, canon interne

> **CONTEXT:** Vocabulaire complet du système (équipe et contributeurs). Contient les termes système, doctrines, disciplines, briques typées, méta-vocabulaire. Pas exposé à l'opérateur en surface produit.
> **OBJECTIVE:** Une seule définition par concept ; liens vers décisions et fichiers sources.
> **TYPE:** Reference interne, vivant.
> **AUDIENCE:** Équipe et contributeurs uniquement. Pour le vocabulaire opérateur, voir `lexicon.md` (slim, 13 termes user-facing).

---

## PhantomOS

Operating system multi-agents pour le métier d'une marque. Encode le savoir métier en substrat opérable, exécute les tâches sur demande, capitalise les apprentissages en continu.

## Context Engine

Moteur de données interne de PhantomOS. Entités JSON par marque, règles de qualité, pipelines de validation.

## Template

Version vierge déployable de PhantomOS, sous `workspace-template/` dans le repo R&D. Source de vérité pour toute release.

## Instance

Workspace PhantomOS déployé pour un opérateur. Cloné depuis le Template, enrichi à l'usage.

## Substrat

Savoir métier d'une marque encodé en objets typés persistants, sous `brands/{slug}/`. Lu par les agents pour raisonner. Permet la mémoire d'exécution.

## Connected source

Plateforme externe connectée à PhantomOS. Typée par catégorie : paid_ads (Meta, TikTok, Google), analytics (GA4, Shopify Analytics), ecommerce (Shopify, Stripe), email_sms (Klaviyo, Postscript), attribution (TripleWhale, Northbeam, Hyros), creative_intelligence (Atria, Foreplay, Motion). Porte type, plateforme, credentials, scope (per brand), sync status, dernier pull. Ajout S53 suite conversation externe operator / Claude bureau.

## Mémoire d'exécution

Capacité d'agir aligné hors session, à partir d'artefacts persistés et de règles régissant leur lecture et mutation. Émerge du substrat encodé.

---

## Canon métier, objets phares

Les 7 objets que l'opérateur encode pour une marque. Chacun a une définition stable, un mapping technique, et un statut de matérialisation.

### Produit

Spec d'un produit vendu : composition, mécanisme, claims, problème adressé, prix. Stocké dans `products/{slug}/spec.json`.

### ProductMap

Terrain typé des problématiques que le produit adresse. Brand-specific. Généré en mode neutre, sans filtre brand au remplissage. À matérialiser dans `products/{slug}/map.json`.

### Position de marque

Antagoniste explicite, distinctive promise, point de vue catégorie. Inclut Voice/Ton comme sous-objet typé (registres émotionnels, voix narratives, axiomes de langage, anti-patterns). À extraire de `brand.json` vers `brand-position.json`. Appliquée en filtre terminal après cartographie, pas en frame en amont.

### Carte audiences

Toutes les audiences potentielles pour la marque, typées récursivement (cluster L1, sub-cluster L2, sub-sub-cluster L3). Règle dure : non sourçable = pas une audience. Stockée dans `audiences/{slug}/profile.json`, à restructurer en hiérarchie L1/L2/L3.

### Carte angles

Tous les angles d'attaque possibles pour la marque. Schema : `angle.schema.json` v1.1+ (S55). Composition récursive `formula = Observation × Tension × Reframe × Bridge`, chaque composant avec `summary` (light pass) + atomes typés (deep pass : verbatim, source, sample_size, state_actual / state_desired / reason_blocked, perceptual_pivot, pivot_mechanism, spec_activated, benefit_served, promise_formulated). Origine typée par `origin_axis` (5 valeurs : audience-derived, product-derived, category-derived, brand-derived, temporal-cultural ; renommage v1.2 ex `source` polysémique). Mouvement explicite via `awareness_movement {in, out}` (règle compat dure : `awareness_in ≤ audience.awareness_dominant`). Cycle `meta.validation_status` : hypothesis → tested → validated → scaled → fatigued. Atomes additifs v1.1 : `intent` (DR / Brand / Hybrid / B2B_lead_gen), `mecanique` enum 16 valeurs, `insight` (modalité formulé/implicite/absent + status), `seasonality_trigger`. Indépendante des audiences au stockage, croisée à la production seulement. Matérialisée dans `brands/{slug}/angles/{ANG-N}.json`. Référence cross-doc : `docs/system/creative-formula.md`.

### Creative (concept vs instance vs variant)

Entité distincte de l'angle (en cours de matérialisation : `creative.schema.json`). Trois plans : **Concept** = objet intent persuasive (audience × insight × angle × mécanique), stable et transposable, identifié par `concept_id`. **Creative** = instance déployée d'un concept (1 créa = 1 fichier, statique / vidéo / UGC / advertorial). **Variant** = créa du même `concept_id` avec 1-2 variables changées. Encoded : `creative.schema.json#concept_id`, `#variant_of`, `#variant_axis`. Absorbe les blocs execution (format, ton, craft, cta), classification, atome irréductible. Référence cross-doc : `docs/system/creative-formula.md`.

### Stratégie

Goals annuels, focus mensuel, priorités. Stockée dans `strategy.json`.

### Apprentissages

Faits opérationnels append-only : workarounds, compliance, résultats de tests. Stockés dans `learnings.json`. Inclut TestResult typé pour chaque test instancié : `{hypothesis, metric, sample, duration, result, status}`. Permet la priorisation par validation lors de la composition de cellules.

---

## Canon métier, briques typées

Briques typées centralement, référencées par les schemas au lieu d'être redéclarées dans chaque objet. Règle dure : type uniquement ce qui circule entre objets.

### Pain

Souffrance identifiée. Profondeur typée par ChainNiveau : Pain, Symptom, Cause, Block. Circule dans Audience, Spec produit.

### Bénéfice

Gain identifié. Profondeur typée par ChainNiveau : Bénéfice, Outcome, Emotion, Identity. Circule dans Spec produit, Offer, Angle.

### JTBD

Tâche que l'audience cherche à accomplir (Job To Be Done). Circule dans Audience, Strategy.

### AwarenessStage

Niveau de conscience face au problème (Schwartz) : unaware, problem aware, solution aware, product aware, most aware. Fluide, contextuel, pas figé par sub-cluster. Circule dans Audience, Angle, Copy.

### ChainNiveau

Chaîne de profondeur d'une brique. Pain : Symptom, Cause, Block. Bénéfice : Outcome, Emotion, Identity. Optionnelle par défaut, obligatoire en mode défensif.

---

## Atlas brand (v2.36+)

Concept canonique upstream pour cartographie holistique data e-commerce d'une brand. Composé de 6 entités core (brand · spec · offers · profile · learnings · strategy) + 3 dérivés (angles · creatives produced · scoring matrix). Navigable via `/phantom` cockpit. Distinct de atlas canon copy (sense 1, cross-brand référentiel). Doctrine complète : `docs/system/atlas-brand.md`.

## Atlas canon copy (v2.26+)

Référentiel typé partagé du copywriting, ajouté en v2.26.0 comme infrastructure puis branché aux skills en v2.27.0 (atlas vivant). 11 couches × 58 fiches : frameworks, hooks, angles, niveaux-schwartz, archetypes-voix, formules-titres, objections, construction-offre, leads, formats-livrables, persuasion. Sources canoniques : Schwartz (Breakthrough Advertising), Cialdini, Halbert, Sugarman, Hormozi, Carlton, Jung. Storage : `resources/canon/copy/{layer}/{tool}.json`. Schema : `canon-tool/1.0`. **Mécanisme atlas vivant** : 4 skills (`produce-paid-angles`, `produce-copy-brief`, `mine-voc`, `learn-from-session`) **consomment** le canon (filtrage par `when_works/when_avoid/combines_with`) et **alimentent** via `validations[]` append-only (operator-gated promotion). L'atlas devient brand-spécifique au fil de l'usage. Doctrine complète : `docs/system/atlas-canon-copy.md`. Décisions : D#382 (fondation), D#383 (consume + feed).

## Mechanisms[] (spec)

Brique typée du produit, élargie en v2.28.0 de mono (`unique_mechanism` scalaire) à many (`spec.schema.json#mechanisms[]`). Chaque mécanisme : `mechanism_id` (MEC-NN), `name`, `description`, `target` (cible biologique / cognitive / comportementale), `mode_of_action` (cofactor, antioxidant, adaptogen, probiotic, coenzyme, regulator, stimulant, inhibitor, structural, delivery, other), `time_window` (immediate, 7d, 14d, 30d, 60d, 90d+), `evidence_level` (clinical_cited, efsa_validated, efsa_partial, anecdotal, mechanistic_only), `market_sophistication` (low, medium, high), `triggered_by_specs[]`. Many-to-many spec ↔ mécanisme ↔ bénéfice. Light pass : `name` + `description` par `snapshot-brand`. Deep pass : champs typés par `map-mechanisms` (à shipper). **Ne pas confondre avec Mécanique (creative)** = device structural narratif d'une créa (registry `creative-mechanics-registry.md`, ~25-29 fiches typées). Deux concepts disjoints, deux plans distincts (chaîne causale produit vs device narratif créa).

---

## Cellule

Unité de production d'un livrable. Croisement typé d'au moins Audience × Angle × Canal × Mécanique. Objet runtime composé à la production, pas stocké. L'artefact résultant (LP, ad, email) est sourcé vers les briques utilisées dans la cellule.

---

## Sourçabilité, provenance, triangulation

### Sourçabilité

Capacité d'une donnée à être tracée vers une source observable. Règle dure : non sourçable = pas une donnée.

### Provenance

Tag inline appliqué à chaque champ : `_source_meta = {origin, confidence, evidence, validation_status}`. Indique d'où vient la donnée et avec quelle confiance.

### Triangulation

Validation par croisement d'au moins 3 sources indépendantes. Tout champ load-bearing pour une décision en aval doit être triangulé.

---

## Propriétés émergentes

### Spécificité par construction

Le copy produit est reconnaissable par le client cible, pas générique. Test : masque le nom de la marque, est-ce reconnaissable ? Émerge automatiquement quand le substrat est rempli avec rigueur.

### Réutilisation

La même brique typée sert dans N livrables. Définie une fois, exploitée partout. Justifie économiquement l'effort d'encodage initial.

### Densification

Le substrat s'enrichit avec chaque opération. Compound effect métier. Plus tu opères, plus le substrat devient dense, plus les agents produisent avec pertinence.

---

## Garde-fous créativité

### Quota d'exploration

Ratio configurable de cellules produites en mode breakthrough vs cellules validées par TestResult. Par défaut 70% safe / 30% exploration. Empêche le système de tunnel-viser sur ce qui marche déjà.

### Breakthrough mode

Mode opt-in pour produire des cellules sans s'appuyer sur des TestResult existants. Hypothèse déclarée, testée, promue en validé ou marquée superseded selon résultat. Pattern existant doctrine CMR.

---

## Scope produit vs thèse (D#307)

| Niveau | Énoncé |
|--------|--------|
| **Produit (vendable)** | Workspace SMB digital-native. V1 validée DTC e-commerce. Packs verticaux (prosumer, SaaS, service, créateur) = roadmap V2+. |
| **Thèse (vision)** | Réceptacle agnostique d'encodage de métier pour l'ère agentique. Première incarnation : SMB digital-native. Vocation : tout métier opérable par agents. |
| **Discipline** | Test binaire d'extractibilité à chaque feature core : *"si je remplace 'brand' par 'matter/creator/account/venue', ça tient ?"* Oui → core. Non → isoler en vertical pack. |

---

## Doctrines

### Contextual Intelligence (CI)

Doctrine maître. L'agent raisonne sur l'univers business plutôt que de remplir des formulaires. Structure sert l'intelligence, pas l'inverse. Source : `workspace-template/docs/system/contextual-intelligence.md`.

### Schema Encoding Discipline (SED)

Sub-doctrine. Régit la rigueur d'encodage du substrat : mutations gated, _field_types, sourcing, triangulation, append-only. Prérequis dur de CMR. Source : `workspace-template/docs/system/schema-encoding-discipline.md`.

### Canonical Matrix Reasoning (CMR)

Sub-doctrine. Régit le mécanisme de production : schéma typé croisé avec matrice canon, sortie au seuil 95% qualité. Exploite les objets encodés par SED. Source : `workspace-template/docs/system/canonical-matrix-reasoning.md`.

### Skill Authoring Discipline (SAD)

Sub-doctrine méta. Régit la création et l'évolution des skills qui consomment SED et CMR. Source : `workspace-template/docs/system/skill-authoring-discipline.md`.

### Provenance & Trust Discipline (PTD)

Sub-doctrine scope-only. Régit l'authorship multi-opérateur, le canon comme produit, les skills marketplace. Activée sur triggers (2e opérateur connecté, 1er knowledge pack vendu, 1er skill tiers). Source R&D : `research/`.

### Doctrine Governance

Méta-process. Régit la promotion, l'amendement, la rétraction et la résolution de conflits entre doctrines. Source : `workspace-template/docs/system/doctrine-governance.md`.

**Audience.** Équipe et contributeurs. Pas opérateur (les noms et acronymes des doctrines ne doivent jamais apparaître en output operator-facing).

---

## Disciplines

### Encodage compositionnel

Représente tout objet métier comme une équation de variables typées, chacune décomposable en sous-objets typés. *"On ne décrit pas, on compose."* Source : `research/encodage-compositionnel-2026-05-01.md`.

### Compositionnel

Assemblage de variables par règles typées. Distinct de modulaire.

### Modulaire

Substitution d'une variable sans casser le reste. Distinct de compositionnel.

### Typage récursif

Chaque variable est un type qui se compose. Règle dure : *type uniquement ce qui circule.*

### Two-tier rule

Principe architectural CI. Couche mécanique = strict enforcement (mutations, schemas, paths, ops destructives). Couche sémantique = strict trust (audience, ton, claims, recommandations). Source : `workspace-template/CLAUDE.md`.

### Génération neutre

Remplir le substrat sans filtre brand au stade découverte. Anti biais de confirmation.

### Apprentissage par lancement

Construire le substrat par opération réelle (ship rough, observe, refine), pas seulement en amont.

### Séparation des voix

Distinguer le ton agent (doctrine `voice.md`) du ton copy produit (DR, voix de marque, registre vente). Couche de voix dédiée par output à construire.

---

## Pipeline métier (verbes ordonnés)

### Cartographier

Couvrir l'ensemble d'un champ pour identifier toutes les variables avant de plonger. Méthode d'exhaustivité préalable.

### Conceptualiser

Nommer précisément chaque variable identifiée. Sortir du flou.

### Modéliser

Poser la structure typée des concepts. Output : un schema.

### Processiser

Transformer un concept modélisé en étapes exécutables. Output : une SOP ou un skill.

### Systémiser

Intégrer un process dans le système global. Connecter aux autres objets, aux skills, aux conventions.

### Anatomie

Décomposer un objet en parties typées. Outil transversal de modélisation, mobilisé pendant l'étape modéliser.

---

## Patterns d'évolution

### Cycle de validation

Lifecycle d'un objet testable : `hypothesis, tested, validated, scaled, fatigued`. Trait transverse applicable à toute audience, hook, angle ou format. Transition gated par un test instancié, pas par changement d'humeur.

### Cycle de maturation

Lifecycle de remplissage d'un objet du substrat : `rough, refined, mature`. Transition par enrichissement et triangulation.

### Modes d'effort

Trois niveaux d'investissement choisis pour une opération : rapide, robuste, défensif. Initialement actés pour l'onboarding, transposables à toute opération.

---

## Vocabulaire externe (D#308)

Termes à employer en comm externe (tweet, LinkedIn, pitch, README). Cohérent avec "context engineering" (Lütke, Karpathy) mais plus spécifique.

### Context Layering

Construire couche par couche l'environnement dans lequel l'agent raisonne. Variante granulaire de "context engineering".

### Decision Trace

Raisonnement loggé derrière une correction, pas seulement la correction. Transforme les learnings de "quoi" en "pourquoi". Champ `reasoning` ou `trace` dans `learnings.json`.

### Skill Graph

Nœuds atomiques interconnectés, lecture par index, traversée sélective. Catalogues, routing, cross-refs par ID.

### Feedback Loop

Agent propose, opérateur corrige, Decision Trace loggée, graphe enrichi, agent propose mieux. Définit le compound effect.

---

## Contexte, analyse, production (D#237)

Le Context Engine porte l'intention stratégique et l'état stable. Les rapports d'analyse (audit, VoC, gaps) sont transitoires, ne remplacent pas les JSON sans arbitrage. Chaîne : Contexte, Analyse (livrables markdown), Décision (humain), Production (agents qui lisent le contexte). Les mutations effectives du contexte suivent D#252.

---

## Profondeur de contexte (L1 / L2 / L3)

Trois niveaux de remplissage du substrat. Documentés pour les opérateurs dans `workspace-template/GETTING_STARTED.md`.

### Niveau 1 (MVP)

Les agents peuvent travailler avec un minimum structuré.

### Niveau 2 (enrichi)

Contenu ciblé et différencié par marque.

### Niveau 3 (opérationnel)

Pilotage opérationnel. Contexte utilisable pour décisions et exécution fine.

La mémoire d'exécution s'épaissit en montant les niveaux.

---

## Cartographie anti-flou

Reformulations à appliquer quand un terme flou apparaît dans une discussion.

- *"L'IA a oublié"* : contexte non chargé ou non écrit dans un fichier ou une entité. Pas une défaillance magique du modèle.
- *"Base de connaissance"* (flou) : préciser. Faits produit (entités), learnings opérationnels, SOPs (KB layer), ou rapport d'analyse (hors DB).
- *"Agent qui écrit dans les JSON"* (brut) : D#252, écriture médiée, traçable, souvent en proposal jusqu'à revue.

---

## Extension layer (D#326-332)

### Extension

Toute addition construite par l'opérateur au-dessus du core workspace : custom entity, sidecar schema, custom skill, external pipeline. Suit 3 règles : schema déclaré, registered ou discovered, README documentant le purpose. Source : `workspace-template/docs/system/extending.md`.

### Custom entity

Nouveau type de donnée scopé par marque, sous `brands/{slug}/custom/{entity_type}/`. Schema canon-compliant + instances + README. Enregistrée dans `index.json → extensions[]`. Découverte par `query-resource`.

### Sidecar schema

Extension append-only de champs sur une entité core, sans modifier le schema core. Fichier `brands/{slug}/{entity}.extensions.json` adjacent au core. `_extends` déclaré. Jamais override ni remove, ajoute uniquement. Mergé avec le core au runtime. Découvert par convention.

### Core namespace vs custom namespace

Skills shippés sous `.skills/skills/{name}/`, maintenus par releases template. Skills opérateur sous `.skills/skills/custom/{name}/`, intacts aux upgrades. Même discipline sur les ressources.

### Gate 5 dimensions

Séquence de check appliquée par `check-existing-encoding` avant tout scaffold : core entities, active-brand sidecars, active-brand custom entities, sibling-brand custom entities, shared resources. Match = route-to-existing. No match = genuinely-new.

### Promotion threshold

Heuristique pour juger si une extension custom mérite promotion vers vertical pack ou core : même pattern chez 3+ marques avec schemas convergents. Décision finale manuelle.

### Parametric composition

Génération par traversée de banques curées (angles, mécaniques, formats, preuves, hooks) plutôt que génération libre à la demande. Nommée en S31 après D#308. Formalisée dans `prisms.md § Prism 7`.

---

## Méta-vocabulaire du canon

Hiérarchie des règles qui structurent le canon. Du plus haut (orientation) au plus appliqué (accord local).

### Doctrine

Principe raisonné qui oriente toutes les décisions d'un domaine. Exemple : Contextual Intelligence.

### Discipline

Pratique appliquée qui sert une doctrine. Exemple : Encodage compositionnel sert l'intelligence contextuelle.

### Règle dure

Invariant non-négociable, gardé par hook ou refus runtime. Exemple : *non sourçable = pas une donnée*, mutation gate.

### Convention

Accord local stable, modifiable par décision. Exemple : `snake_case` en JSON, conventions par plateforme.

---

## Références

- **D#129** : Two-layer memory model (`decisions.md`).
- **D#252** : Write contract, event log, proposal mode (`decisions.md`, `research/spec-write-to-context.md`).
- **D#237** : Contexte ≠ analyse ≠ production (`decisions.md`).
- **D#326-332** : Extension layer V1 + scaffold-extension + dual-mode + étendre-avant-créer (`decisions.md`, `workspace-template/docs/system/extending.md`).
- **État produit** : `project-state.md` (vision, 3 couches, 6 entités).
- **Onboarding** : `workspace-template/GETTING_STARTED.md` (niveaux 1 à 3).

---

*Mise à jour 2026-05-04 (S55). Ajouts post audit nomenclature + releases v2.26-v2.28.1 : Carte angles réécrite (formula récursive Obs × Tension × Reframe × Bridge, origin_axis 5 valeurs, awareness_movement, validation_status, atomes additifs v1.1) ; entité Creative (concept vs instance vs variant) ; section Atlas canon copy (11 couches × 58 fiches, mécanisme atlas vivant via validations[]) ; section Mechanisms[] spec (many v2.28, distinction nette vs Mécanique creative). Refs : D#382, D#383, D#391.*

*Dernière mise à jour : 2026-05-02 (S53). Renommé `lexicon.md` en `canon.md` pour distinguer canon interne (audience équipe et contributeurs, 58 entrées système + doctrines + disciplines + briques typées + méta-vocabulaire) du nouveau `lexicon.md` slim (audience opérateur DTC paid, 13 termes user-facing). Ajout `Connected source` au canon (générique multi-plateformes : paid ads + analytics + ecommerce + email + attribution + creative intelligence). Split déclenché par conversation externe operator / Claude bureau qui a flag : "darkwriting" (over-documentation sans visibilité), lexicon inflation (35+ termes pour audience qui n'en comprend que 15-18), exposition acronymes doctrine en surface utilisateur, Voie A enrichie (DTC paid acquisition exclusivement V1 avec plateforme extensible pour autres métiers), moratoire sur nouvelle doctrine tant que pas d'opérateur DTC externe en prod. Historique S51 + S52 préservé : Lot 1 système (6) + Lot 2A doctrines (6) + Lot 2B disciplines (8) + Lot 2C pipeline métier (6) + Lot 4 réécriture sections existantes + Lot 5 patterns d'évolution (3) + Lot 6 méta-vocabulaire (4) + Lot 3A canon métier (24 entrées) avec audit Red Team 6 perspectives appliqué.*
