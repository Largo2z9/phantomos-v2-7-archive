---
description: Vue d'oiseau spatiale sur une brand ou un projet. Recale instantanément après reprise. Rend visible zones acquises, en cours, non engagées, non cartographiées.
---

# /bird · vue d'oiseau projet

Slash command pointer vers `bird` skill. Recale l'opérateur en 5 secondes par une carte spatiale du territoire entier (pas un status report). Pair canon avec `/scope` (bird LIT la carte produite par scope).

## Mode detection

| Argument | Routing |
|---|---|
| `/bird` empty | vue macro composite, brand/projet actif (cascade détection · pwd → git → portfolio) |
| `/bird {nom}` | vue macro brand/projet nommé |
| `/bird all` | vue multi-brands (mini-territoires comparés cross-portfolio) |
| `/bird --zoom {zone}` | vue micro anatomie d'une zone scopée du projet courant |

## Invocation

Charger `.skills/skills/bird/SKILL.md` et suivre son workflow (1 détection brand · 2 chercher cartographie scope-map.md · 3 composer vue macro · 4 format output macro ou 5 micro --zoom ou 6 all).

**Hard rules à respecter (cf SKILL.md complet)** ·

- HR-1 · Output spatial obligatoire (grille ASCII, pas texte-only)
- HR-2 · Territoire d'abord, état après (zone vierge = même place qu'à 95%)
- HR-3 · Stabilité visuelle inter-sessions (positions zones constantes)
- HR-4 · Registre sobre institutionnel accessible (pas de métaphore ludique, pas de jargon brut)
- HR-5 · Révélation > confirmation (1 fois sur 3 doit révéler "ah merde j'avais oublié X")
- HR-6 · Zéro em-dash
- HR-7 · Investigation posture (zones étiquetées observé / déduit / déclaré / inconnu)
- HR-8 · Decomposition Visibility territoire-level obligatoire post-grille (canon v2.79+, 4 niveaux matriciels)

## Decomposition Visibility territoire-level (canon v2.79+)

Après affichage vue d'ensemble territoire brand (zones acquises · en cours · non engagées · non cartographiées), rendu obligatoire matriciel territoire-level canon `docs/system/decomposition-visibility-discipline.md` v2.79+. Pattern miroir `build-atlas-complete` v1.6.0 Phase Atlas Visibility, adapté vue d'ensemble territoire (pas build complet).

### NIVEAU 1 · Décomposition produit territoire-level

Vue d'ensemble produits encoded territoire · table compacte cross-products status encoded vs manquant ·

```
PRODUITS ENCODÉS dans le territoire
PRODUCT             SPECS          MÉCANISMES        BÉNÉFICES 3 couches
[product-1]         encoded        encoded           functional · emotional · identity
[product-2]         encoded        partial           functional only (gap emotional/identity)
[product-N]         absent         absent            non cartographié
```

Status canon · `encoded` (entité présente atomes complets) · `partial` (entité présente atomes incomplets) · `absent` (entité non cartographiée territoire).

### NIVEAU 2 · Many-to-many territoire-level

Matrice ASCII cross-atlas vue d'ensemble · quelle douleur encoded affecte quelle audience encoded territoire ·

```
                       Audience-1    Audience-2    Audience-3   Audience-N
                       (slug)        (slug)        (slug)       (slug)
PNT-01 [pain encoded]     ✓✓ P (sourced)   ·       ✓ S (hyp)      ·
PNT-02 [pain encoded]        ·         ✓✓ P (hyp)     ·         ✓ S (sourced)
PNT-NN [pain absent]      gap          gap          gap         gap
```

Légende canon · `✓✓ P` PRIMARY · `✓ S` SECONDARY · `·` NONE · `gap` non cartographié territoire. Status `(sourced)` verbatims présents · `(hyp)` hypothèse confidence 0.5 valide (canon `progressive-cartography-discipline.md`).

### NIVEAU 3 · Positionnement filtre stage business territoire-level

Stage business détecté · table canon vue d'ensemble territoire ·

```
STAGE détecté            [early | growth | scale | inconnu]
ARR signal               [range ou flag inconnu]

AUDIENCE PRIORITAIRE     [audience slug + rationale 1 ligne]
GAPS TERRITOIRE          [3 gaps à combler · ex audience-N profile manquant ·
                          PNT-NN non sourcé · stage signal absent]
SKILLS DOWNSTREAM        [routes possibles · ex `/scope {zone}` · `profile-audience` ·
                          `mine-voc --focus={pain}` · `audit-meta-account`]
```

**HR · Stage business filter territoire-level obligatoire si signal détectable.** Stage inconnu acceptable seulement si zéro signal · NEVER inventer.

### NIVEAU 4 · Méthode pédagogique verbale territoire-level

Verbaliser ce que vue d'ensemble montre cross-territoire · l'opérateur sait COMMENT le territoire a été lu ·

> *"J'ai lu le territoire {brand} en 4 niveaux canon ·*
> *1. Décomposition produits · {N} produits encoded · {N} partials · {N} absents*
> *2. Many-to-many · {N} pains × {M} audiences (matrix encoded/sourced/hypothèse · gaps territoire visibles)*
> *3. Stage business · {stage détecté} → audience prioritaire {slug} · gaps territoire identifiés*
> *4. Navigation · zones complétées · zones en cours · zones manquantes. Skills downstream recommandés · {liste}*
>
> *Vue d'ensemble est lecture, pas construction · pour creuser une zone use `/scope {zone}` · pour construire l'atlas complet use `build-atlas-complete`."*

**HR · Méthode pédagogique verbale territoire-level obligatoire.** Skip = opérateur ne sait pas comment la lecture territoire a été menée · navigation downstream aveugle.

## Source de vérité

`/bird` LIT `brands/{slug}/scope-map.md` (artefact produit par `/scope`). Si absent · mode dégradé (zones déduites status.json + structure dossiers + commits récents), annoncer en bas de l'output et recommander `/scope {brand}` pour stabiliser le territoire.

## Cross-refs canon

- `/scope` · pair canon · PRODUIT la `brands/{slug}/scope-map.md` que `/bird` lit
- `docs/system/decomposition-visibility-discipline.md` v2.79+ · canon racine 4 niveaux matriciels (territoire-level vs product-level v2.78.2)
- `docs/system/investigation-posture.md` · étiquettes observé / déduit / déclaré / inconnu utilisées pour catégoriser zones
- `.skills/skills/build-atlas-complete/SKILL.md` v1.6.0 · Phase Atlas Visibility product-level miroir reproductible (bird = territoire-level lecture · build-atlas-complete = product-level construction)
- `.skills/skills/snapshot-brand/SKILL.md` v2.78.2 · sister consumer canon decomposition visibility (Movement 3-4 product-level)
- `.skills/skills/profile-audience/SKILL.md` v2.78.2 · sister consumer matrice audience × pain × angle × stage
- `.skills/skills/brief-day/SKILL.md` · navigator macro cross-brands au start (vs bird qui zoome 1 brand)
- `.skills/skills/resume-session/SKILL.md` · reprise narrative thread actif (vs bird spatial macro)
