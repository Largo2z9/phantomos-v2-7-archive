# Audience Cartography Doctrine

> Spec technique rigoureuse pour skill authors qui maintiennent la cohérence du framework. Cross-ref operator doc · `docs/doctrine/audience-cartography-framework.md`.

## Status

Canonique v2.39+. Toute évolution future passe par doctrine governance (`docs/system/doctrine-governance.md`).

## Champs schema canon

profile.schema.json v1.3+ supporte 3 champs hiérarchie :

| Champ | Type | Enum | Description |
|---|---|---|---|
| `meta.scope` | string | broad / segment / micro | 3 niveaux MECE max |
| `meta.parent_slug` | string | (slug) | Slug parent dans hiérarchie · null pour broad racine |
| `meta.overlap_with` | array | (slugs) | Slugs des audiences cousines avec chevauchement signalé |

## Invariants à enforcer

### Invariant 1 · 3 niveaux maximum

Pas de sous-micro. Hiérarchie limitée à broad → segment → micro. validate-resources doit refuser un parent_slug sur une audience qui résulterait en niveau 4+.

### Invariant 2 · Pas d'orphelin segment

Tout segment doit avoir un parent_slug renseigné (vers broad). Sinon flag MAJOR finding "audience-orpheline détectée".

### Invariant 3 · Pas de cycle

`overlap_with` est non-cyclique. A overlap B + B overlap A est valide (symétrie). Mais A overlap B overlap C overlap A est cycle interdit (signaler MAJOR finding).

### Invariant 4 · Test 3/3 sur micro

Pour qu'une audience soit micro (sub-division segment), elle doit déclarer dans son frontmatter (ou structure) la justification 3/3 :
- `volume_remaining_estimate` (k actives minimum 20)
- `pitch_divergent: bool` (true)
- `offer_divergent: bool` (true)

Si 0/3 ou 1/3 → flag "audience-fantôme suspecte".

### Invariant 5 · Porte d'entrée explicite

Tout profile.json doit déclarer `meta.entry_door` enum [pain_driven · goal_driven · identity_driven]. Pas de mix · 1 porte dominante par audience.

## Validation pipeline

`validate-resources` skill v2.39+ doit ajouter Hard Rule :

```
HR-X · Audience cartography hierarchy validation

Pour chaque profile.json sous brands/{slug}/audiences/ :
1. meta.scope present + valid enum
2. Si scope=segment → parent_slug requis vers broad
3. Si scope=micro → parent_slug requis vers segment
4. overlap_with array · check no cycle
5. meta.entry_door requis + valid enum
6. Si scope=micro → frontmatter justification 3/3 (pitch + offer + volume)

Violations → MAJOR finding + suggested fix.
```

## Mutation gate

Skills qui mutent profile.json (profile-audience) v2.39+ doivent · avant write_to_context final :

1. Demander entry_door (Q1 framework)
2. Demander/inférer scope (Q2 framework)
3. Si scope=segment · demander parent broad
4. Si scope=micro · demander parent segment + justification 3/3
5. Optionnel · proposer overlap_with si chevauchements détectés

## Cross-refs

- `docs/doctrine/audience-cartography-framework.md` (operator-facing pédago)
- `docs/system/doctrine-governance.md` (process évolution)
- `resources/schemas/profile.schema.json` (schema canon)
- `.skills/skills/profile-audience/SKILL.md` (skill applicateur)
- `.skills/skills/validate-resources/SKILL.md` (skill enforceur)

## Évolutions futures (notes pour skill authors)

- v2.40+ envisager `meta.entry_door` schema enum strict
- v2.40+ envisager `meta.schwartz_stage_default` pour rendu vue cartographique
- v2.41+ envisager doctrine cartographie produits (mêmes patterns appliqués à products)
