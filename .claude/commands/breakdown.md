---
name: breakdown
description: Démontre les doctrines PhantomOS via le cas Stepprs (brand pédagogique foot care DTC). 7 topics drillables · principe · composition · vocabulaires · angles · audiences · investigation · production. Ordre suggéré 1 à 7 = parcours complet (~20 min). Drill direct possible sur tout topic.
---

# `/breakdown stepprs {topic}` · vitrine pédagogique PhantomOS

Slash command qui démontre chaque doctrine PhantomOS via le cas concret Stepprs (brand fictive foot care DTC encodée canon dans `brands/_EXAMPLE/`). L'agent sourcing les fichiers Stepprs live à chaque invocation, pas dump statique.

**Cible** · opérateur marketeur, créa, stratège paid qui veut comprendre comment PhantomOS structure le savoir métier et produit des outputs reproductibles. Ton institutionnel sérieux, accessible, zéro jargon plumbing.

## Mode detection

| Argument | Mode |
|---|---|
| empty (`/breakdown stepprs`) | **index** · liste les 7 topics + parcours suggéré + diagramme cartographique |
| topic name (e.g. `/breakdown stepprs composition`) | **drill** · génère la fiche du topic sourçant Stepprs live |
| invalid topic | **redirect** · liste les 7 topics valides en 1 ligne, demande choix |

## Mode index, default

Si l'opérateur tape `/breakdown stepprs` sans arg, sortir exactement ceci (rendu fidèle, pas paraphrase) ·

```
══════════════════════════════════════════════════════════════════════
PARCOURS PHANTOMOS · démontré via cas Stepprs
══════════════════════════════════════════════════════════════════════

FONDEMENT          MÉCANIQUE            APPLICATION              OUTPUT
─────────          ─────────            ───────────              ──────

1. principe   →    2. composition  →    4. angles           →    7. production
   substrat          4 couches             formula OTRB              brief copy
   vs production     chainage              7 angles dérivés          en 5 min

                   3. vocabulaires →    5. audiences
                      mécanismes           hiérarchie
                      typés canon          vs targeting

                                       6. investigation
                                          5 sections IP
                                          rigueur output

  POURQUOI           COMMENT C'EST        COMMENT ÇA               CE QUE
  PHANTOMOS          CONSTRUIT            S'APPLIQUE               ÇA DONNE
  EXISTE             STRUCTURELLEMENT     AU RAISONNEMENT          AU LIVRABLE
                                          MARKETING

Ordre suggéré · 1 → 7 (parcours complet, ~20 min lecture)
Drill direct · /breakdown stepprs {topic}
══════════════════════════════════════════════════════════════════════
```

## Mode drill · génération fiche topic

Pour chaque topic, appliquer le format output canonique ci-dessous, en sourçant les fichiers Stepprs spécifiques au topic (cf section "Topic guides").

### Format output canonique (5 sections, ordre strict)

```
══════════════════════════════════════════════════════════════════════
CAS STEPPRS · {titre topic}
══════════════════════════════════════════════════════════════════════

LIVRABLE OBTENU EN {durée}
  {Output concret produit par la mécanique. Pour le topic "principe",
   le livrable est un raisonnement clair. Pour "composition", c'est un
   brief copy. Pour "production", c'est un brief copy + variants visuels.
   Pour les autres, choisir l'output le plus tangible.}

CE QUI LE REND POSSIBLE
  {Diagramme cartographique ASCII des relations entre éléments, ou
   tableau structuré si plus lisible. Toujours visuel, jamais prose
   linéaire pure.}

PROPRIÉTÉ STRUCTURELLE
  {1 à 2 lignes · ce qui rend cette mécanique unique vs un Notion ou
   un Airtable. La propriété qui fait la différence reproducibilité.}

LECTURE OPÉRATEUR
  {2 à 3 lignes · comment appliquer ce principe sur sa propre brand.
   ROI implicite, pas pitch.}

EXPLORER
  → {action next 1}        /{slash command}
  → {action next 2}        /{slash command}
  → Topic suivant parcours /breakdown stepprs {topic+1}
```

**Règles strictes pour l'agent** ·
- Zéro file path exposé (pas `audiences/workers-shifts/profile.json#field`)
- Zéro field name JSON exposé (pas `_meta.cross_narrative_notes`, `emotional_signal`, `evidence_verbatim`)
- Zéro acronyme doctrine non-traduit (OTRB peut rester car court mais expliqué dans le topic "angles", SED CMR SAD jamais exposés)
- Verbatims sourcés conservés littéralement, jamais paraphrasés
- Zéro em-dash
- Ton institutionnel, mesuré, jamais sales-bro
- Fiche ~30 lignes max, livrable en tête, drill en fin

## Topic guides · ce que l'agent doit produire par topic

### 1. principe · substrat vs production

**Concept démontré** · PhantomOS encode le savoir métier d'une marque en substrat stable (territoire) qui survit aux sessions et alimente la production runtime à la demande. Économie cognitive massive, pas une CRM enrichie.

**Files Stepprs à sourcer**
- `brands/_EXAMPLE/brand.json` (identity + driver_blend + brand_equity)
- `brands/_EXAMPLE/status.json` (`is_example: true`, validation_status)
- `brands/_EXAMPLE/README.md` (canon vs réel section)

**Livrable concret en tête** · raisonnement opérateur clair sur un cas Stepprs réel. Exemple · "Pour produire 1 nouvelle créa Stepprs, l'opérateur n'a pas besoin de re-explorer composition produit, audiences, angles, proofs. Tout est encodé. Il pioche dans le substrat, génère, valide."

**Diagramme à proposer** · vue 2 layers · TERRITOIRE (stable, encodé 1 fois) au-dessus, PRODUCTION (volatil, runtime, multiple) en dessous, avec flèche de consommation.

**Propriété structurelle** · le substrat survit aux sessions cross-skills cross-opérateurs. Notion stocke du texte. PhantomOS encode du raisonnement.

### 2. composition · 4 couches chaînage

**Concept démontré** · Compositional Cartography v3.1. Composition physique du produit → mécanismes typés canon → bénéfices chainés → angles formula OTRB. Multiplication par composition, pas duplication d'idées brutes.

**Files Stepprs à sourcer**
- `brands/_EXAMPLE/products/massage-insoles/spec.json` (composition, mechanisms, benefits)
- `brands/_EXAMPLE/angles/ANG-01.json` à `ANG-07.json` (7 angles dérivés)

**Livrable concret en tête** · brief copy d'angle plantar-fasciitis généré en 5 min (Hook + Mécanisme + Bénéfice + Proof + CTA), sourcé du substrat composition.

**Diagramme à proposer** ·
```
COMPOSITION   →   MÉCANISMES   →   BÉNÉFICES   →   ANGLES
physique          typés canon       chainés          OTRB

top               cushioning        confort         hero
middle            pressure-redist   moins fatigue   audience
base              arch-support      relief PF       category
                  shock-absorb      moins lombaire  product

3 entrées         4 mécanismes      5 bénéfices    7 angles
```

**Propriété structurelle** · 3 entrées physiques produisent 7 angles par composition. Le travail créatif se concentre sur les angles, pas sur la redéfinition de la matière première à chaque session.

### 3. vocabulaires · registres canon fermés

**Concept démontré** · PhantomOS impose des vocabulaires fermés (mécanismes typés, awareness levels, sophistication levels, lead types) plutôt que freestyle. La contrainte produit la reproducibilité.

**Files Stepprs à sourcer**
- `brands/_EXAMPLE/products/massage-insoles/spec.json` (mécanismes typés depuis registre canon)
- `resources/registries/` (registres canon disponibles · `creative-mechanics-registry.md`, `angle-registry.md`, `proof-registry.md` à citer)
- `resources/catalogues/` (catalogues canon complémentaires si présents)

**Livrable concret en tête** · 2 versions d'un même mécanisme produit · freestyle ("soutien dynamique adaptatif") vs canon ("arch support + pressure redistribution"). Montrer comment le canon permet à un autre skill (decompose-ad, produce-paid-angles) de raisonner sans interprétation.

**Diagramme à proposer** · tableau comparatif freestyle vs canon sur 2 ou 3 attributs Stepprs concrets.

**Propriété structurelle** · les vocabulaires fermés sont l'équivalent d'un schéma SQL pour le raisonnement créatif. Sans eux, chaque session redéfinit, rien ne s'accumule.

### 4. angles · formula OTRB appliquée

**Concept démontré** · Formula OTRB (Observation + Tension + Reframe + Bridge). Tout angle paid Stepprs suit cette structure stricte. Reproducible cross-skill, lisible cross-session.

**Files Stepprs à sourcer**
- `brands/_EXAMPLE/angles/ANG-01.json` (hero Michelle, le pilote)
- `brands/_EXAMPLE/angles/ANG-02.json` à `ANG-07.json` (6 variations sur 5 origin_axis)

**Livrable concret en tête** · ANG-01 décomposé en 4 cases OTRB, montrant comment chaque case est ancrée sur le substrat (audience composite, verbatim sourcé, mécanisme typé, garantie).

**Diagramme à proposer** ·
```
ANG-01 hero Michelle
─────────────────────────────────────────────────
O · Observation : verbatim Trustpilot sourcé
T · Tension     : insight douleur articulée
R · Reframe     : mécanisme produit positionné
B · Bridge      : CTA + garantie
```

Lister rapidement les 7 angles + origin_axis (audience, product, category, brand, temporal-cultural).

**Propriété structurelle** · 7 angles distribués 5 axes = couverture créative par construction, pas par inspiration aléatoire.

### 5. audiences · cartographie hiérarchique vs targeting paid

**Concept démontré** · Cartographie audience parent/enfants (substrat stable, N segments documentés) ≠ targeting ad runtime (production decision, M campagnes, M ≤ N). Canon v2.69.1.

**Files Stepprs à sourcer**
- `brands/_EXAMPLE/audiences/workers-shifts/profile.json` (mère + 3 sous-poches)
- `brands/_EXAMPLE/audiences/chronic-pain-45/profile.json` (mère + 2 sous-poches)
- `brands/_EXAMPLE/learnings.json` LRN-0002 (pattern cross-narrative observed)
- `brands/_EXAMPLE/README.md` section canon vs réel

**Livrable concret en tête** · décision stratégique opérationnelle · "Stepprs cartographie 7 segments mais diffuse 1 hero cross-audience. Voilà pourquoi et comment décider sur ta propre brand."

**Diagramme à proposer** ·
```
CARTOGRAPHIE (substrat)        TARGETING PAID (production)
──────────────────────         ──────────────────────────
workers-shifts (mère)
  nurses-12h                   ┐
  warehouse-10h                ├──→  1 hero Michelle
  hospitality-retail           │     (combine 2 mères
                               │      en 1 testimonial)
chronic-pain-45 (mère)         │
  plantar-fasciitis            │
  heel-pain-general            ┘

7 segments documentés          1 ad copy, 27 marchés EU
```

**Propriété structurelle** · cartographier sert à comprendre le terrain. Le targeting paid est une décision séparée, libre, informée par la cartographie.

### 6. investigation · 5 sections IP appliquées

**Concept démontré** · Tout output stratégique PhantomOS (synthèse audience, angle, brief copy, audit perf) sort en 5 sections explicites · Observé, Déduit, Inconnu, Leviers, Close ouvert. Pas de prose libre, pas d'affirmation sans confidence chain.

**Files Stepprs à sourcer**
- `brands/_EXAMPLE/audiences/workers-shifts/profile.json` (vérifier si profil contient déjà cette structure · sinon montrer comment elle s'applique au runtime)
- `brands/_EXAMPLE/learnings.json` (pattern captured avec sourcing)
- `brands/_EXAMPLE/products/massage-insoles/frictions/FRC-01.json` (friction documentée avec verbatim)

**Livrable concret en tête** · une synthèse audience workers-shifts présentée en 5 sections IP, montrant comment chaque assertion porte son sourcing.

**Diagramme à proposer** · tableau 5 sections avec exemple Stepprs concret par section ·

```
OBSERVÉ      verbatims Trustpilot, reviews Amazon, scrape PDP
DÉDUIT       trigger commun, vocabulaire shared, severity tier
INCONNU      saisonnalité achat, fréquence remplacement
LEVIERS      mine-voc sur Reddit r/nursing, mine-vom forums podiatres
CLOSE OUVERT "On creuse le segment hospitality-retail ou on
              valide d'abord le hero Michelle sur la mère ?"
```

**Propriété structurelle** · l'agent n'invente jamais une persona analytique. Il observe, déduit avec confidence chain, flag les inconnus, propose leviers, garde la conversation ouverte.

### 7. production · brief copy en 5 min

**Concept démontré** · Le substrat encodé alimente la production runtime. Un brief copy ou une variation créative se génère en 5 min, pas en 1 heure, parce que le travail cognitif a été fait au setup.

**Files Stepprs à sourcer**
- `brands/_EXAMPLE/products/massage-insoles/spec.json` (composition, mechanisms, benefits)
- `brands/_EXAMPLE/audiences/workers-shifts/profile.json` (audience visée hero)
- `brands/_EXAMPLE/angles/ANG-01.json` (angle hero)
- `brands/_EXAMPLE/products/massage-insoles/offers.json` (offer + guarantee)

**Livrable concret en tête** · brief copy complet généré sur cible audience workers-shifts angle ANG-01, avec Hook + Body + Proof + CTA + variants visuels, sourcé du substrat. Ne pas inventer, citer.

**Diagramme à proposer** · arbre de provenance du brief ·

```
BRIEF COPY
├── Hook         ← audience.trigger + audience.vocabulaire
├── Body         ← spec.mechanism + spec.benefit chained
├── Proof        ← angle.observation (verbatim sourcé)
├── CTA          ← offer.guarantee + offer.cta_canon
└── Variants     ← creative-mechanics-registry × 3 variations
```

**Propriété structurelle** · la production runtime est presque mécanique. Le travail intellectuel a été fait une fois au setup. La créa devient un acte de composition, pas d'invention.

## Anti-patterns à éviter dans toute fiche

- Dump prose continue sans diagramme
- Acronymes doctrine non-traduits exposés (SED, CMR, SAD, SED-X, etc.)
- Field paths JSON exposés (`audiences/workers-shifts/profile.json#field`)
- Ton sales-bro ou tabloid ("L'erreur que la plupart font", "Faux.", etc.)
- Fiche au-delà de 35 lignes
- Em-dash

## Cross-refs

- Brand pédagogique source · `brands/_EXAMPLE/` (foot care DTC fictive Stepprs)
- Doctrines démontrées (référence skill-author) · `docs/system/territory-discipline.md` · `docs/system/compositional-cartography.md` · `docs/system/schema-encoding-discipline.md` · `docs/system/canonical-matrix-reasoning.md` · `docs/doctrine/audiences-cartography-doctrine.md` · `docs/doctrine/angle-anatomy-doctrine.md` · `docs/system/investigation-posture.md`
- Slash command frères · `/tour` (onboarding) · `/skills` (navigable menu) · `/phantom` (state cockpit)
