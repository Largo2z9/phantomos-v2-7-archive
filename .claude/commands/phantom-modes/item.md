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
{nom} · {scope} · {validation_label}
{Brève description si identity.description filled}

Profil
  Genre        {gender ou "non précisé"}
  Tranche      {age_range ou "non précisée"}
  Pain         {pain.primary_problem ou "à confirmer en mining"}
  Émotions     {psychology.emotions[] ou "vide"}
  Goals        {psychology.goals[] ou "vide"}

Voix (sourcée)
  Vocabulaire à utiliser    {voice.vocabulary_to_use[] ou "vide"}
  Vocabulaire à éviter      {voice.vocabulary_to_avoid[] ou "vide"}
  Expressions clés          {N} captées (mining : {dense|partiel|vide})

Pain points
  {N} encodés ({M} sourcés). Top 3 par priorité, 1 ligne chacun.

Objections
  {N} encodées. Top 3 par fréquence.

Hiérarchie
  Parent : {parent_slug ou "(racine)"}
  Sous-audiences : {liste des sous-slugs ou "aucune"}

Appliqué aux produits
  {applies_to_products joint par ", " ou "(brand-wide, pas de produit ciblé)"}

Actions prioritaires
  · `lance mine-voc sur {brand_slug} pour {item-slug}` (mining vide, prochaine étape logique)
  · `profile-audience {brand_slug} sur {item-slug}` (synthèse 8 dimensions canon V3)
  · `valide point par point l'audience {item-slug}` (corriger, rejeter, accepter)
  · `produce-paid-angles {brand_slug} sur {item-slug}` (passer à la production hypothesis-grade)
```

### Pour `angles/{id}`

Lecture : `brands/{brand}/angles/{id}.json` ou agrégat `brands/{brand}/angles.json`. Rendering :

```
{nom_angle} · {status} · {audience_target}
{Synopsis 1-2 phrases}

Cible              {audience_slug}
Promesse           {promise ou "non posée"}
Preuve / mécanique {mechanism ou "non posé"}
Hooks              {N} testés, {M} live, {K} fatigués
Tests              {ROAS si dispo, sinon "pas de test posté"}

Actions prioritaires
  · `refresh l'angle {id}` ({raison liée au statut})
  · `produce-copy-brief {brand_slug} sur l'angle {id}` (passer en brief créa)
```

### Pour `products/{slug}`

Lecture : `brands/{brand}/products/{slug}/spec.json` + `offers.json` + scan `brands/{brand}/audiences/*/profile.json` pour filtrer celles dont `meta.applies_to_products` contient `{slug}` (fallback sur `meta.product_id` legacy). Rendering :

```
{nom_produit} · {category}
{Description 1-2 lignes}

Promesse          {promise.headline ou "non posée"}
Mécanisme         {unique_mechanism.name ou "non posé"}
Composition       {N composants encodés / total attendus}
Problèmes résolus {N encodés}
Bénéfices         {N encodés}
Prix              {pricing.price} {currency}
Offres            {N actives} (cure 1m, 3m, 6m si dispo)

Audiences (qui achètent ce produit)
{audience_lines}

Actions prioritaires
  · `densifie la spec {slug}` (champs manquants : {liste})
  · `audit l'offre {slug}` (vérifier cohérence prix/cure/économies)
```

`audience_lines` : un par audience filtrée :
```
  · {audience_slug}    {scope}    {validation_label}    {applies_to_count} produits ciblés
```

`applies_to_count` : `mono` si `len(applies_to_products) == 1`, `cross-product (N)` si > 1, `legacy` si vide mais `product_id` set, `brand-wide` si vide. Permet à l'opérateur de voir quelles audiences sont spécifiques à ce produit vs partagées.

Si aucune audience ne cible ce produit : *"Aucune audience taggée sur ce produit. Pour binder · `tag audience X sur {slug}`, sinon laisser en brand-wide."*

### AskUserQuestion (mode item)

| Slot | Rôle |
|---|---|
| 1 | Action top-priority sur l'item (paste-ready) |
| 2 | Action 2 (paste-ready) |
| 3 | *"Explorer {sibling}"* · un autre item du même entity-drill (typiquement le suivant alphabétique ou le voisin hiérarchique pour les audiences) |
| 4 | *"Retour {entity}"* · relance `/phantom {brand} {entity}` |

### Hard rule for item mode

Si `{item-slug}` n'existe pas, surface : *"Item '{x}' introuvable dans `{entity}` de `{brand}`. Disponibles · {liste des slugs trouvés}. Pour la vue entity complète · `/phantom {brand} {entity}`."*

### Post-render filter (v2.42+)

Avant émission, appliquer le filtre jargon `.skills/_jargon_bank.json` selon le contrat universel défini dans `phantom.md § Post-render jargon filter`. Substitution forcée via `apply_jargon_filter(output_text, locale="fr")` si un token résiduel reste hors backticks (typique sur ce mode : `validation_status`, `pain_points`, `applies_to_products`, `winner_proxy`, `ROAS` reste tech detail acceptable).

---
