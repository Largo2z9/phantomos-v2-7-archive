## Mode item (niveau 3)

`/phantom {brand_slug} {entity} {item-slug}` zooms on ONE item inside an entity. Le rendering équivalent d'un *file preview* dans un Finder. Operator vient de drill quelque chose de spécifique : on déballe ce qu'on a, sans tout dump.

Header breadcrumb obligatoire :

```
workspace > {brand_slug} > {entity} > {item-slug}
══════════════════════════════════════════════
```

### Pour `audiences/{slug}`

Lecture : `brands/{brand}/audiences/{item-slug}/profile.json`. Rendering human-readable :

```
{NOM} · {scope} · {validation_label}
{Brève description si identity.description filled}

PROFIL
  Genre        {gender ou "non précisé"}
  Tranche      {age_range ou "non précisée"}
  Pain         {pain.primary_problem ou "à confirmer en mining"}
  Émotions     {psychology.emotions[] ou "vide"}
  Goals        {psychology.goals[] ou "vide"}

VOIX (sourcée)
  Vocabulaire à utiliser    {voice.vocabulary_to_use[] ou "vide"}
  Vocabulaire à éviter      {voice.vocabulary_to_avoid[] ou "vide"}
  Expressions clés          {N} captées (mining: {dense|partiel|vide})

PAIN POINTS
  {N} encodés ({M} sourcés). Top 3 par priorité affichés en 1 ligne chacun.

OBJECTIONS
  {N} encodées. Top 3 par fréquence affichées.

HIÉRARCHIE
  Parent: {parent_slug ou "(racine)"}
  Sous-audiences: {liste des sous-slugs ou "aucune"}

APPLIQUÉ AUX PRODUITS
  {applies_to_products joint par ", " ou "(brand-wide, pas de produit ciblé)"}

NEXT SUGGESTED (priorité)
  → Tape : `lance mine-voc sur {brand_slug} pour {item-slug}` (mining vide, prochaine étape logique)
  → Tape : `profile-audience {brand_slug} sur {item-slug}` (synthèse 8 dimensions canon V3)
  → Tape : `valide point par point l'audience {item-slug}` (corriger, rejeter, accepter)
  → Tape : `produce-paid-angles {brand_slug} sur {item-slug}` (passe à la production hypothesis-grade)
```

### Pour `angles/{id}`

Lecture : `brands/{brand}/angles/{id}.json` ou agrégat `brands/{brand}/angles.json`. Rendering :

```
{NOM_ANGLE} · {status} · {audience_target}
{Synopsis 1-2 phrases}

CIBLE              {audience_slug}
PROMESSE           {promise ou "non posée"}
PROOF / MÉCANIQUE  {mechanism ou "non posé"}
HOOKS              {N} testés, {M} live, {K} fatigués
TESTS              {ROAS si dispo, sinon "pas de test posté"}

NEXT SUGGESTED
  → Tape : `refresh l'angle {id}` ({raison liée au statut})
  → Tape : `produce-copy-brief {brand_slug} sur l'angle {id}` (passer en brief créa)
```

### Pour `products/{slug}`

Lecture : `brands/{brand}/products/{slug}/spec.json` + `offers.json` + scan `brands/{brand}/audiences/*/profile.json` pour filtrer celles dont `meta.applies_to_products` contient `{slug}` (fallback sur `meta.product_id` legacy). Rendering :

```
{NOM_PRODUIT} · {category}
{Description 1-2 lignes}

PROMESSE          {promise.headline ou "non posée"}
MÉCANISME         {unique_mechanism.name ou "non posé"}
COMPOSITION       {N composants encodés / total attendus}
PROBLÈMES RÉSOLUS {N encodés}
BÉNÉFICES         {N encodés}
PRIX              {pricing.price} {currency}
OFFRES            {N actives} (cure 1m, 3m, 6m si dispo)

AUDIENCES (qui achètent ce produit)
{audience_lines}

NEXT SUGGESTED
  → Tape : `densifie la spec {slug}` (champs manquants : {liste})
  → Tape : `audit l'offre {slug}` (vérifier cohérence prix/cure/économies)
```

`audience_lines` : un par audience filtrée :
```
  · {audience_slug}    {scope}    {validation_label}    {applies_to_count} produits ciblés
```

`applies_to_count` : `mono` si `len(applies_to_products) == 1`, `cross-product (N)` si > 1, `legacy` si vide mais `product_id` set, `brand-wide` si vide. Permet à l'opérateur de voir quelles audiences sont spécifiques à ce produit vs partagées.

Si aucune audience ne cible ce produit : *"Aucune audience taggée sur ce produit. Tape `tag audience X sur {slug}` pour binder, ou laisse en brand-wide."*

### AskUserQuestion (mode item)

| Slot | Rôle |
|---|---|
| 1 | Action top-priority sur l'item (paste-ready) |
| 2 | Action 2 (paste-ready) |
| 3 | *"Drill {sibling}"* · un autre item du même entity-drill (typiquement le suivant alphabétique ou le voisin hiérarchique pour les audiences) |
| 4 | *"Retour {entity}"* · relance `/phantom {brand} {entity}` |

### Hard rule for item mode

Si `{item-slug}` n'existe pas, surface : *"Item '{x}' pas trouvé dans `{entity}` de `{brand}`. Disponibles : {liste des slugs trouvés}. Tape `/phantom {brand} {entity}` pour la vue entity complète."*

---
