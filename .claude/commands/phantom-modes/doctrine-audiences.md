## Mode doctrine audiences

`/phantom doctrine audiences` rend le framework cartographie audiences (4 questions pédagogiques). Operator-facing, accessible toujours.

Lecture · `docs/doctrine/audience-cartography-framework.md`.

Format :

```
workspace > doctrine > audiences
══════════════════════════════════════════════
Cartographier les audiences · 4 questions

Q1 · Porte d'entrée
   Une audience entre dans ta catégorie par 1 de 3 portes :
     par un problème       elle ressent une douleur (chute, sec, gris)
     par un objectif       elle vise une ambition (longueur, mariage)
     par qui elle est      elle se définit par son identité (hijabi, sportive, mum)
   Une vraie audience a 1 porte dominante.

Q2 · Niveau de granularité
   Hiérarchie 3 niveaux max :
     audience mère      grand public, large       1-3 par brand
     poche              définie, ciblée           5-15 par audience mère
     niche              hyper-spécifique          0-3 par poche
   Pour descendre d'un niveau · 3/3 requis (volume + hook différent + offre différente)

Q3 · Où elle en est dans son parcours
   2 axes modulateurs (pas 5 audiences mais 5 façons de lui parler) :
     ce qu'elle sait du produit         découvre → maîtrise tout
     où elle en est émotionnellement    nie → résigne → cherche → combat → accepte

Q4 · Chevauchements
   Aucune audience ne vit en isolation.
   Les audiences cousines révèlent les angles porteurs cross-pollinisables.

Pièges à éviter
   audience-fantôme       sous-division sans hook ni offre différents
   audience-redondante    2 audiences, en réalité même persona
   audience-orpheline     audience définie sans audience mère claire

Loi de Pareto
   80% du revenue brand vient de 2-3 audiences activées, jamais 7.
   Cartographier sert à prioriser, pas à activer toutes.

Le résumé en 1 phrase
   Une audience, c'est une porte d'entrée + un niveau de granularité +
   un stade dans le parcours. Ses chevauchements révèlent les angles porteurs.

Actions prioritaires
  · `/phantom {brand} audiences` (vue brand-side)
  · `cartographier une nouvelle audience` (lance le skill)
  · `voir le cours complet` (doctrine pédago étendue)
```

Cross-ref doctrine complète (backend, instructions agent) · `docs/doctrine/audience-cartography-framework.md`. Ne pas exposer ce path à l'opérateur ; pointer vers `voir le cours complet`.

### Post-render filter (v2.42+)

Avant émission, appliquer le filtre jargon `.skills/_jargon_bank.json` selon le contrat universel défini dans `phantom.md § Post-render jargon filter`. Si un token jargon résiduel reste détectable hors backticks code (ex : "Schwartz" non substitué en "où elle en est dans son parcours"), substitution forcée via `apply_jargon_filter(output_text, locale="fr")`.
