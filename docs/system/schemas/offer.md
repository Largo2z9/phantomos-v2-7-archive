# offer, schema offre commerciale

## Définition

Structure d'offre par produit, v2.0 DRAFT avec `offer_groups[]` et inheritance 2-niveaux (group → offer). Vit dans `brands/{slug}/products/{product_slug}/offers.json` une fois validée. Schema `resources/schemas/offer.schema.json`. Breaking changes vs v1.8 : flat `offers[]` wrapped dans `offer_groups[]` avec attribute inheritance.

## Pourquoi

Un même produit a souvent plusieurs configurations commerciales (single, bundle 3-pack, abonnement, GWP) qui partagent des modificateurs (urgence, garantie, free ship). v1.8 dupliquait ces modificateurs sur chaque offre. v2.0 introduit `offer_groups[]` pour partager les attributs et hériter par défaut, override ponctuel sur l'offre. Encode une fois, varie ce qui doit varier.

## Anatomie

| Champ | Type | Rôle | Source typique |
|---|---|---|---|
| `meta.product_slug` | string | Produit auquel l'offers.json se rattache | déclaré |
| `offer_groups[]` | array | Groupes d'offres avec attributs partagés | structurel |
| `offer_groups[].shared` | object | Attributs partagés (garantie, urgence, payment plan) | déclaré |
| `offer_groups[].offers[]` | array | Offres individuelles dans le groupe | déclaré |
| `offers[].offer_id` | string | OFF-NN, stable | généré |
| `offers[].product_refs[]` | array | REQUIRED, identité produit explicite par offre (pas hérité) | déclaré |
| `offers[].pricing` | object | Prix, devise, % off, comparé à | déclaré |
| `offers[].bundle` | object | Composition bundle (qty, gift items) | déclaré |
| `offers[].urgency` | object | Deadline, scarcity, social proof | déclaré |

## Best practices

- Standalone offer = group de 1, c'est valide. La structure `offer_groups[]` est obligatoire même pour une seule offre, ça évite les exceptions downstream.
- Attributs partagés → `offer_groups[].shared`. Override ponctuel → champ explicite sur l'offre. Merge rule : objects deep-merge, arrays replace.
- `product_refs[]` REQUIRED sur chaque offre, jamais hérité du group. Évite les ghost-offer bugs (offre sans produit identifié).
- Promotions brand-level (free ship 69€+, GWP threshold) → vivent dans `brand.json#promotions`, pas dans offer.json. Offer.json porte les modificateurs spécifiques à l'offre (% off, bundle, durée).
- Group cohérent par fonction commerciale (single SKUs, bundles, subscription tiers). Ne pas mélanger un single et un abonnement dans le même group.

## Anti-patterns

| Symptôme | Pourquoi c'est un problème | Fix |
|---|---|---|
| Modificateurs (garantie, urgence) dupliqués sur chaque offre | Brise l'intérêt de v2.0, drift à la moindre modif | Migrer vers `offer_groups[].shared`, override ponctuel uniquement |
| Inheritance ignoré, `offer_groups[].shared` vide alors qu'attributs identiques entre offres | Architecture v2.0 sous-utilisée | Refactoriser, déplacer le commun vers shared |
| `product_refs[]` hérité de group.shared | Ghost-offer bugs, identité produit ambiguë | Toujours explicite par offre, jamais hérité |
| Free ship brand-wide encodé dans offer.json | Multiplie l'écriture, drift vs brand.promotions | Encoder dans `brand.json#promotions`, offer ne touche pas |
| Bundle sans composition détaillée (qty, items) | Skills creative ne peuvent pas en parler factuellement | Remplir `bundle.composition[]` avec qty et product slug |

## Interaction avec autres schemas

- offer ← lit ← brand (promotions cascadent comme modificateurs additifs au moment du rendu)
- offer ← lit ← spec (product_refs pointe vers spec.meta.slug, l'offre habille la matière spec)
- offer → alimente → creative (creative.context.offer_ref pointe vers OFF-NN, hooks et CTA reflètent l'offre active)
- offer → alimente → angle (angle.formula.bridge.promise_formulated peut citer un avantage offer)

## Signaux pour Claude (non prescriptifs)

- Opérateur dit "promo de fin d'année free ship dès 69€" → c'est brand-level, encoder dans `brand.json#promotions`, pas par offer.
- Bundle 3-pack mentionné sans composition → drill `bundle.composition[]`, sans ça aucun skill creative ne peut produire un copy factuel.
- Plusieurs offres avec la même garantie 30 jours → signal pour migrer vers `offer_groups[].shared.guarantee`.
- "On lance une offre subscribe & save" → probable nouveau group dédié, avec ses attributs partagés (récurrence, save %, lock-in).
- Offre avec `% off` ≥ 50% sur produit positionné premium → tension brand_equity_level vs offer aggressivité, signal pour challenger doucement.
- Offer en `draft` depuis >30j → flag stale, soit ship soit archive.

## Cycle de vie

Créé par `setup-offer` ou `snapshot-brand` (squelette draft depuis pricing scrape). Enrichi par `enrich-offer`, `learn-from-session`, `decompose-creative` (offre observée dans une ad). Modifié via mutation gate uniquement. Lu par `creative-strategist`, `produce-paid-angles` (bridge.promise_formulated), `analyze-copy` (cross-check offer mentionnée vs offer encodée). Snapshot regen sur mutation.
