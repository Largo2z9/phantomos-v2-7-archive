# Dependency Resolution & Gap-Filling Protocol (DRGFP)

> Doctrine canonique v2.38+. Comment chaque skill PhantomOS arbitre ses gaps amont (data manquante, source absente, corpus thin) sans bloquer le pipeline. 3 niveaux canoniques appliqués au Step 0bis.

## Le problème

Le pipeline P0→P5 (specs → mechanisms → benefits → audiences → angles → score → brief → visual) a une dépendance théorique séquentielle. En réalité, chaque skill rencontre des gaps amont :
- Brand fresh sans creative_zone défini
- Audience avec 1 verbatim au lieu de 5+
- spec.json sans visual_identity
- strategy.current_focus vide

Sans contrat canonique, chaque skill bricole différemment :
- Refus blocking (frustrant)
- Production silencieuse avec data inférée (dangereux)
- AskUserQuestion à chaque step (pénible)
- Auto-pull sans freshness check (silent corruption v2.36 finding A1)

DRGFP canonise le protocole.

## 3 niveaux canoniques

### L1 · Auto-fill silent
Skill détecte gap, auto-pull source authoritative dispo, procède silencieusement.

**Quand l'appliquer** : source disponible sans choix opérateur (URL produit Shopify, file system check, MCP connecté, sibling file existe).

**Required** :
- `auto_pull` strategy déclarée (ex `dual_path_inline_or_sibling`, `shopify_products_api`, `websearch_authoritative`)
- `freshness_ttl_days` int (TTL au-delà duquel L1 dégrade en L2 gate, defense contre stale data)
- Tag `_field_types: derived` sur output

**Exemples** :
- `compose-creative` · `spec.visual_identity` → fallback inline OR sibling file
- `profile-audience` · `profile.json` existing → brownfield seed read
- `produce-paid-angles` · `atlas canon copy` chargement → resources/canon/copy/

### L2 · Ask-operator gate
Skill détecte gap critique sans source auto-pullable, AskUserQuestion explicit avec 2-4 options binaires.

**Quand l'appliquer** : choix stratégique requis (force inféré · mining d'abord · upload source · scope élargi).

**Required** :
- `options[]` minItems 2 maxItems 4 (chaque option = action concrète, pas open-ended)
- Pas de production sans operator response explicit
- Override seulement si opérateur a déclaré force-mode dans tour précédent

**Exemples** :
- `produce-paid-angles` · `verbatim_quotes < 5` → 3 options (force inféré · mine-voc d'abord · hybride 1 ancré)
- `compose-creative` · `visual_identity partial` → 2 options (proxy palette + flag · attendre define-visual)
- `score-matrix` · `weight-dimensions absent` → 2 options (run weight-dimensions chain · scoring brut sans modulateurs)

### L3 · Degraded + flag
Skill produit output partial avec `validation_status: hypothesis` + `confidence: 0.X` + `_gaps[]` array surface.

**Quand l'appliquer** : output utile même partial, opérateur arbitre post-hoc, jamais refuser blocking.

**Required** :
- `fallback` strategy déclarée (ex `proxy brand_equity_level`, `last_known_good`, `infer_from_canon`)
- `confidence_default` 0.0-1.0 (typiquement 0.4-0.6 selon richesse fallback)
- Output flag visible operator-facing (translation table v2.37 : `validation_status: hypothesis` → `non testé · à valider`)

**Exemples** :
- `score-matrix` · `strategy_context absent` → fallback proxy `brand_equity_level` · confidence 0.6
- `compose-creative` · `creative_zone vide` → fallback proxy `brand_personality` · confidence 0.5
- `weight-dimensions` · `profile partial` → infer from `origin_axis` biais initiaux · confidence 0.5

## Routage binaire (default L1 > L3 > L2)

Pour chaque prerequisite identifié au Step 0bis :

```
1. Source auto-pullable + freshness OK ?  → L1
2. Sinon, output viable en degraded ?      → L3
3. Sinon (gap critique bloquant qualité)   → L2
```

Default préféré L1 > L3 > L2. **L2 seulement si vraiment besoin operator arbitrage**. Trop de L2 = pénible. Trop de L1 = silent corruption. Trop de L3 = output flou. Le mix correct est contextuel par prerequisite.

## Frontmatter SKILL.md déclaratif

Tout skill v2.38+ déclare ses prerequisites en frontmatter :

```yaml
---
name: produce-paid-angles
type: producer
isolation_scope: brand_only
confidence_propagation: min
prerequisites:
  - field: profile.verbatim_quotes
    threshold: 5
    level: L2
    options:
      - force_inferred
      - mine_voc_first
      - hybrid_one_anchored
  - field: brand.creative_zone
    level: L3
    fallback: proxy_brand_personality
    confidence_default: 0.6
  - field: resources/canon/copy/hooks
    level: L1
    auto_pull: read_canon_directory
    freshness_ttl_days: 365
---
```

Validé contre `resources/schemas/skill-prerequisites.schema.json` (v2.37) par `validate-resources` HR-19.

Cross-doc check : chaque `prerequisites[i].field` doit être référencé dans Step 0bis prose. Drift frontmatter ↔ Step 0bis = MAJOR finding (multi-source of truth interdit).

## Step 0bis prerequisite_check pattern

Tout skill v2.38+ ajoute Step 0bis qui scanne ses prerequisites et arbitre :

```markdown
### Step 0bis · Prerequisite check (DRGFP v2.38)

Avant production, scanner chaque prerequisite déclaré en frontmatter :

1. Lookup field path dans context (brand state, atlas, profile, etc.)
2. Si présent + freshness OK (si L1 freshness_ttl_days posé) → mark resolved silent
3. Si absent ou stale :
   - Si L1 → tenter auto_pull strategy, surface uniquement si fail
   - Si L2 → AskUserQuestion avec options[] declared, attend response
   - Si L3 → appliquer fallback, set confidence = confidence_default, ajouter à _gaps[]

Output Step 0bis = state map { field → resolved|fallback|gated|failed } + confidence_chain[] init.
```

## Operator surface (translation table v2.37)

Opérateur ne voit JAMAIS les noms `L1`, `L2`, `L3`, `prerequisites`, `_gaps[]`. Surface traduite :

| Interne | Operator-facing |
|---|---|
| L1 auto-fill | automatique |
| L2 gate | à toi de choisir |
| L3 degraded | partiel · à valider |
| prerequisites manquants | il manque · pour bien faire il faudrait |
| _gaps[] flagged | points à compléter |

## Compound failure mode evité

Sans DRGFP : 4 skills chain qui font tous L3 silent → output final non-évalué (red team v2.36 finding cumul confidence). Avec DRGFP + confidence-propagation v2.37 default `min` : confidence_chain[] propagé, audit trail visible, atlas vivant promotion gate require min(chain) >= 0.7.

3 doctrines couplées :
- DRGFP v2.38 (gap-filling)
- confidence-propagation v2.37 (algèbre cascade)
- canon-tool schema v1.1 v2.37 (attribution + decay)

= chain robuste sans pollution silencieuse.

## Cross-refs

- `resources/schemas/skill-prerequisites.schema.json` (v2.37 schema validation)
- `docs/system/confidence-propagation.md` (v2.37 algèbre cascade)
- `docs/system/canon-tool.schema.json` v1.1 (v2.37 attribution + decay)
- `docs/system/brand-isolation-doctrine.md` (v2.37 isolation_scope)
- `docs/system/operator-vocabulary-translation.md` (v2.37 jargon translation)
- `docs/system/skill-authoring-doctrine.md` (frontmatter triad enrichi)
