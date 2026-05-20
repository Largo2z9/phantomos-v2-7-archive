# Brand Isolation Doctrine

> Doctrine canonique v2.37+. Empêche cross-contamination data multi-brand. Critique pour usage agency multi-clients.

## Le problème

PhantomOS workspace héberge plusieurs brands `brands/{slug}/`. Sans fence explicite, un skill curieux peut lire `brands/*/learnings.json`, `brands/*/audiences/*/profile.json`, ou `brands/*/_snapshot.md` pour signal "pattern X marche partout". Tentation forte (signal cross-brand semble = signal robuste) mais :

1. **Privacy violation** · agence client A ne consent pas à ce que ses data alimentent le signal apporté à client B
2. **Segmentation business** · positionnement brand-spécifique dilué par signal cross-brand générique
3. **Confidentialité contractuelle** · NDAs agency typiques interdisent cross-pollination
4. **Atlas vivant pourri** · validations brand-spécifiques deviennent signaux universels faux

## Doctrine canonique

**Default obligatoire : `_isolation_boundary: brand` enforced.**

Tout skill consume-existing OU producer qui lit data brand-side a un scope **brand-only** par défaut. Lecture `brands/{other_slug}/**` interdite sans operator gate explicit AskUserQuestion.

**Exception canonique** : atlas canon copy (`resources/canon/copy/`) est cross-brand par design (sense 1, doctrine partagée copywriting). Lecture libre depuis n'importe quelle brand.

## Implementation

### Skill frontmatter

Tout skill v2.37+ déclare son scope :

```yaml
---
name: produce-paid-angles
type: producer
isolation_scope: brand_only  # default · enforced
...
---
```

Override autorisé si justifié :

```yaml
isolation_scope: cross_brand_with_gate  # Require AskUserQuestion explicit operator avant cross-brand read
isolation_scope: workspace_global  # Réservé infrastructure skills (validate-resources, hygiene-audit)
```

### Runtime enforcement

`mutation-gate` (ou script equivalent) intercepte tout `Read` ou `Glob` sur `brands/{slug}/` :

1. Skill courant a scope `brand_only` ?
2. Path requested = `brands/{current_brand}/**` ? → autorisé silent
3. Path requested = `brands/{other}/**` ? → REFUS + log + AskUserQuestion gate explicit
4. Path requested = `resources/canon/**` ? → autorisé silent (cross-brand par design)

### Validations[] cross-brand

Atlas vivant validations[] sont brand-spécifiques. Toute entrée a `brand_slug` field requis (Patch 3 v2.37 schema v1.1). Lecture cross-brand interdite par défaut. Promotion vers atlas canon copy (cross-brand) require operator gate + min N≥3 brands distinctes ayant validé même pattern.

## Operator surface

Opérateur ne voit JAMAIS les noms `brand_only`, `_isolation_boundary`, `isolation_scope` brut. Surface traduite si refus :

> "Cette donnée est sur une autre brand (X). Tu veux que je la lise ? (a) oui, juste pour cette session · (b) non, reste sur Y · (c) explique-moi pourquoi tu en as besoin"

## Cross-refs

- `docs/system/atlas-canon-copy.md` (sense 1 cross-brand par design)
- `docs/system/atlas-brand.md` (sense 4 brand-specific)
- `docs/system/confidence-propagation.md` (atlas vivant feed isolation enforcement)
- `resources/schemas/skill-prerequisites.schema.json` (frontmatter validation)
