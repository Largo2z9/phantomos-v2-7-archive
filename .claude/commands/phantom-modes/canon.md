# Mode canon (référence métier, workspace-level)

> Split externe de `/phantom canon` depuis `phantom.md` v2.36 (cap 1000 lignes dépassé). Référencé depuis phantom.md root via lien.

`/phantom canon` ouvre la **bibliothèque métier**, navigable comme un catalogue d'outils standards. Workspace-level, pas brand. La bibliothèque est consultée par les skills de production (crée des angles publicitaires, génère un brief copy, récupère les témoignages clients) et navigable directement par l'opérateur pour apprendre / piocher / valider.

Implémentation backend (Lecture agent) : invoquer `python3 .skills/phantom-canon.py [atlas] [layer] [tool]` qui retourne un JSON. L'agent rend selon le mode.

## canon-index (`/phantom canon`)

Header breadcrumb :

```
workspace > canon
══════════════════════════════════════════════
Bibliothèque métier · {N} domaines disponibles
```

Rendering : un domaine par ligne avec count chapitres + outils.

```
✓ copy             11 chapitres · 58 outils    (squelettes, accroches, angles, persuasion, niveaux conscience, voix, titres, objections, offres, leads, formats)
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
Copywriting · 11 chapitres
```

Rendering : un chapitre par ligne avec count outils + 1-line description :

```
✓ squelettes                     6 outils   structures de pièce (AIDA, PAS, BAB, QUEST, FAB, 4Ps)
✓ accroches                      6 outils   ouvertures 3 sec (écart de curiosité, contrepied, stat choc, ...)
✓ angles                         6 outils   axes narratifs (mécanisme unique, identité, ennemi commun, ...)
✓ leviers de persuasion          7 outils   ressorts cognitifs (Cialdini × 7)
✓ niveaux conscience             2 outils   où elle en est dans son parcours + maturité du marché
✓ voix de marque                 6 outils   registres (protecteur, sage, rebelle, amante, héros, ...)
✓ formules titres                6 outils   patterns headlines (4U, how-to, listicle, secret, commande, question)
✓ objections                     4 outils   patterns de gestion (feel-felt-found, reframe, anticipation, comparaison)
✓ construction offre             4 outils   architectures d'offre (ancre-leurre, bundle, garantie, urgence)
✓ leads                          5 outils   types d'ouverture (par offre, par mécanique, par histoire, par problème, par preuve)
✓ formats livrables              6 outils   types de livrable (UGC-ad, VSL, landing, séquence email, statique, advertorial)
```

## canon-tools (`/phantom canon copy hooks`)

Header breadcrumb :

```
workspace > canon > copy > accroches
══════════════════════════════════════════════
Accroches · ouvertures 3 sec · 6 outils
```

Rendering : un outil par ligne avec id, name, et 1-line principle.

```
· écart-curiosité      Crée un écart entre ce que le lecteur sait et ce qu'il devrait savoir.
· contrepied           Prend le contre-pied d'une croyance dominante de l'audience.
· stat-choc            Ouvre sur une stat surprenante qui valide implicitement la douleur.
· avant-après          Ouvre sur le contraste visuel ou narratif avant/après.
· question-cible       Pose une question qui qualifie l'audience cible.
· confession           Ouvre sur un aveu personnel qui crée connexion + preuve.
```

## canon-tool-card (`/phantom canon copy hooks curiosity-gap`)

Header breadcrumb :

```
workspace > canon > copy > accroches > écart-curiosité
══════════════════════════════════════════════
Accroche · écart-curiosité                  catégorie : accroches
```

Rendering complet de la fiche :

```
Principe
  {principle, 1-3 phrases}

Structure
  {structure}

Gabarits
  · {gabarits[0]}
  · {gabarits[1]}
  ...

Quand ça marche
  · {when_works[0]}
  · {when_works[1]}
  ...

Quand éviter
  · {when_avoid[0]}
  ...

Va bien avec
  · squelettes : {combines_with.frameworks join}
  · angles : {combines_with.angles join}
  · émotions : {combines_with.emotions join}
  · formats : {combines_with.formats join}

À éviter
  · {anti_patterns[0]}
  ...

Exemples
  · {examples[0]}
  ...

Tests passés cumulés
  {N tests cumulés brand-side. Si 0 : "(aucun test confirmé. Sera ajouté quand learn-from-session capture un test concluant)"}
  Sinon liste : "{brand_slug}/{audience_slug} → {outcome} · {metric} · {captured_at}"

Origine
  Source : {lineage.source}
  Référence : {lineage.references join}
```

## AskUserQuestion (mode canon)

| Slot | Rôle |
|---|---|
| 1 | Explorer un outil voisin pertinent (lit `combines_with` côté backend, surface intitulé "va bien avec X") |
| 2 | Explorer un autre outil du même chapitre |
| 3 | Action : *"Appliquer cet outil à un brand"* (si brand actif détecté, déclenche le skill crée des angles publicitaires pour ce brand avec l'outil pré-sélectionné) |
| 4 | Retour parent (chapitre, domaine, ou workspace selon niveau) |

## Empty state canon

Si le domaine demandé n'existe pas : *"Domaine '{x}' pas encore disponible. Disponibles · copy. Pour la liste complète · `/phantom canon`."*

Si le chapitre demandé n'existe pas : suggérer les chapitres existants.

Si l'outil demandé n'existe pas : suggérer les outils existants dans le chapitre.

## Post-render filter (v2.42+)

Avant émission, appliquer le filtre jargon `.skills/_jargon_bank.json` selon le contrat universel défini dans `phantom.md § Post-render jargon filter`. Les fiches canon mappent déjà beaucoup de termes (`hooks → accroches`, `frameworks → structures`, `gabarits`, `combines_with → va bien avec`), mais le filtre garantit que tout token résiduel (`atlas vivant`, `canon-tool`, `archetype voix`, `confidence_chain`) hors backticks code soit substitué via `apply_jargon_filter(output_text, locale="fr")`.
