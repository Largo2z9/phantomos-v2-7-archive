# Mode canon (atlas du métier, workspace-level)

> Split externe de `/phantom canon` depuis `phantom.md` v2.36 (cap 1000 lignes dépassé). Référencé depuis phantom.md root via lien.

`/phantom canon` ouvre l'**atlas du métier**, navigable comme une bibliothèque d'outils standards. Workspace-level, pas brand. Le canon est consulté par les skills de production (`produce-paid-angles`, `produce-copy-brief`, `mine-voc`) et navigable directement par l'opérateur pour apprendre / piocher / valider.

Implémentation : invoquer `python3 .skills/phantom-canon.py [atlas] [layer] [tool]` qui retourne un JSON. L'agent rend selon le mode.

## canon-index (`/phantom canon`)

Header breadcrumb :

```
workspace > canon
══════════════════════════════════════════════
Atlas du métier · {N} atlas disponibles
```

Rendering : un atlas par ligne avec count couches + tools.

```
✓ copy             11 couches · 58 outils    (frameworks, hooks, angles, persuasion, Schwartz, voix, titres, objections, offres, leads, formats)
○ paid             à venir
○ brand            à venir
○ offer            à venir
○ funnel           à venir
○ cro              à venir
○ email            à venir
○ analytics        à venir
○ mining           à venir
```

## canon-layers (`/phantom canon copy`)

Header breadcrumb :

```
workspace > canon > copy
══════════════════════════════════════════════
Atlas copywriting · 11 couches
```

Rendering : une couche par ligne avec count outils + 1-line description :

```
✓ frameworks                     6 outils   squelettes de pièce (AIDA, PAS, BAB, QUEST, FAB, 4Ps)
✓ hooks                          6 outils   ouvertures 3 sec (curiosity-gap, contrarian, stat-choc, ...)
✓ angles                         6 outils   axes narratifs (mécanisme-unique, identité, ennemi-commun, ...)
✓ heuristiques-persuasion        7 outils   leviers cognitifs (Cialdini × 7)
✓ niveaux-schwartz               2 outils   conscience + sophistication
✓ archetypes-voix                6 outils   registres de marque (caregiver, sage, rebelle, amante, héros, ...)
✓ formules-titres                6 outils   patterns de headlines (4U, how-to, listicle, secret, commande, question)
✓ objections                     4 outils   patterns de gestion (feel-felt-found, reframe, pre-emption, comparaison)
✓ construction-offre             4 outils   architectures d'offre (anchor-decoy, bundle-stack, garantie, urgence)
✓ leads                          5 outils   types de lead (offer-led, mechanism-led, story-led, problem-led, proof-led)
✓ formats-livrables              6 outils   types de livrable (UGC-ad, VSL, landing, email-séquence, ad-statique, advertorial)
```

## canon-tools (`/phantom canon copy hooks`)

Header breadcrumb :

```
workspace > canon > copy > hooks
══════════════════════════════════════════════
Hooks · ouvertures 3 sec · 6 outils
```

Rendering : un outil par ligne avec id, name, et 1-line principle.

```
· curiosity-gap        Crée un écart entre ce que le lecteur sait et ce qu'il devrait savoir.
· contrarian           Prend le contre-pied d'une croyance dominante de l'audience.
· stat-choc            Ouvre sur une stat surprenante qui valide implicitement le pain.
· avant-apres          Ouvre sur le contraste visuel ou narratif avant/après.
· question-callout     Pose une question qui qualifie l'audience cible.
· confession           Ouvre sur un aveu personnel qui crée connexion + proof.
```

## canon-tool-card (`/phantom canon copy hooks curiosity-gap`)

Header breadcrumb :

```
workspace > canon > copy > hooks > curiosity-gap
══════════════════════════════════════════════
HOOK · curiosity-gap                  famille: hooks
```

Rendering complet de la fiche, sections en majuscules :

```
PRINCIPE
  {principle, 1-3 phrases}

STRUCTURE
  {structure}

GABARITS
  · {gabarits[0]}
  · {gabarits[1]}
  ...

QUAND ÇA MARCHE
  · {when_works[0]}
  · {when_works[1]}
  ...

QUAND ÉVITER
  · {when_avoid[0]}
  ...

COMBINE BIEN AVEC
  · frameworks: {combines_with.frameworks join}
  · angles: {combines_with.angles join}
  · emotions: {combines_with.emotions join}
  · formats: {combines_with.formats join}

ANTI-PATTERNS
  · {anti_patterns[0]}
  ...

EXEMPLES
  · {examples[0]}
  ...

VALIDATIONS
  {N validations brand-side. Si 0 : "(aucune validation prod encodée. À promouvoir via learn-from-session quand un test confirme)"}
  Sinon liste : "{brand_slug}/{audience_slug} → {outcome} · {metric} · {captured_at}"

LINEAGE
  Source : {lineage.source}
  Référence : {lineage.references join}
```

## AskUserQuestion (mode canon)

| Slot | Rôle |
|---|---|
| 1 | Drill un voisin pertinent (combines_with référencé) |
| 2 | Drill un autre outil de la même couche |
| 3 | Action : *"Applique cet outil à un brand"* (si brand actif détecté, déclenche `produce-paid-angles {brand} avec hook={tool_id}`) |
| 4 | Retour parent (couche, atlas, ou workspace selon niveau) |

## Empty state canon

Si l'atlas demandé n'existe pas : *"Atlas '{x}' pas encore seedé. Disponibles : copy. Tape `/phantom canon` pour la liste complète."*

Si la couche demandée n'existe pas : suggérer les couches existantes.

Si l'outil demandé n'existe pas : suggérer les outils existants dans la couche.
