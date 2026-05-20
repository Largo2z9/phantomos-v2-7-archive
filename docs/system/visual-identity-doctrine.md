# Visual Identity Discipline

> Doctrine canonique v2.43+. Sources canoniques haute résolution pour génération fidèle creatives. Catalog assets + logo SVG + wordmark pattern validation. Cross-ref `compositional-cartography.md` v2.42 (équation v3.1 NOYAU × CONTEXTE × MODIFIEURS), `schema-encoding-discipline.md` (mutation rule + sourcing tags), `canonical-matrix-reasoning.md` (production 95%).

## Le problème

PhantomOS génère creatives via fal.ai (compose-creative skill). Sans sources canoniques haute résolution, la génération dérive. Packshots flous. Logos régressés. Wordmarks broken (un wordmark with brackets retourné en variantes sans brackets, caractères corrompus, séparateurs altérés). Le schéma v1.0 référençait uniquement les packshots via URL CDN externe (`packshots.primary_front`, `packshots.cdn_paths[]`) , dépendance fragile sur qualité variable Shopify CDN et résolutions hétérogènes.

Conséquences observées en cycle USAGE post v2.42 ship ·
- Wordmark with brackets drift sur 30%+ des gens compose-creative
- Couleurs label régressées (bordeaux dévié vers brun)
- Packshot front net mais composite logo overlay flou (vectoriel absent en input)
- Lifestyle gen totalement inventé (pas de référence catalog)

## Doctrine canon v2.43

Tout produit cible production creative doit avoir trois piliers obligatoires en place ·

### 1. Catalog assets canon (produit-level)

Path · `brands/{slug}/products/{slug}/assets/`

Contenu minimal ·
- 4 packshots canoniques (front, back, 3/4, top)
- Résolution ≥ 2000×2000
- Fond transparent prioritaire (permet composite flexible). Fallback fond blanc pur `#FFFFFF`.
- Formats supportés · PNG (préféré, transparence), JPG (fond blanc), WEBP (moderne)
- Lifestyle optionnel · `packshot-lifestyle-*.png` (table petit-déj, main qui prend gummy, contexte usage)

Référence schema · `resources/schemas/visual_identity.schema.json` v1.1 · `assets_canonical{}` block.

### 2. Logo SVG brand (brand-level)

Path · `brands/{slug}/assets/logo.svg` + `brands/{slug}/assets/logo-variants/`

Variantes canoniques ·
- `primary` · logo standard couleur
- `monochrome_black` · aplat pour fonds clairs
- `monochrome_white` · aplat pour fonds sombres
- `horizontal` · layout horizontal (header, banner)
- `vertical` · layout vertical (avatar, packaging)
- `icon` · pictogramme isolé sans wordmark

Source vectorielle propre obligatoire. Permet overlay PIL post-gen précis caractère par caractère (préserve brackets `[care]`, accents typographiques, kerning custom).

Référence schema · `visual_identity.schema.json` v1.1 · `logo_svg{}` block.

Pointer brand-level · `brand.json` · `_assets_canonical_path: "assets/"` (référence catalog brand-level).

### 3. Wordmark pattern regex (validation runtime)

Path · `visual_identity.json` produit · `wordmark_pattern` field

Strict validation wordmark caractère par caractère post-gen compose-creative. Regex compilée runtime ·
- Match wordmark détecté OCR creative gen → pass
- Broken (drift caractère) → trigger HR3.4 retry compose-creative avec contrainte renforcée

Exemples ·
- Wordmark with brackets · `^example\[brand\]$` (brackets mandatory autour du segment central)
- Marque sans brackets simple · `^[A-Z][a-z]+\+?$` (capital first, optionnel +)
- Marque avec espace · `^ENERGIZE GUMMIES$`

## Consumers

- **compose-creative** skill v2.43+ · HR1.4 priorité `assets_canonical.packshot_*` local > `packshots.cdn_paths[]` URL CDN externe. Si assets canon absent ou flag `_fallback_to_cdn: true` actif → dégrade vers CDN URL (warning logged `assets_canonical_missing` ou `assets_canonical_fallback_active`).
- **compose-overlay-text** skill v2.43 NEW · PIL post-gen composite logo SVG overlay + sub-text crisp avec accents préservés. Consomme `logo_svg.path` + `logo_svg.variants[]`.
- **decompose-ad** skill · reverse-engineering peut référencer `assets_canonical` pour fidélité analyse comparative gen vs canon.

## Migration brand pré-v2.43

Pour chaque brand existant ·

| Étape | Action | Path |
|---|---|---|
| 1 | Créer dossier produit-level | `brands/{slug}/products/{slug}/assets/` |
| 2 | Upload sources canon haute résolution (4 packshots min) | `assets/packshot-canonical-{front,back,3-4,top}.{png,jpg,webp}` |
| 3 | Créer dossier brand-level | `brands/{slug}/assets/` |
| 4 | Upload logo SVG + variantes | `assets/logo.svg` + `assets/logo-variants/logo-{variant}.svg` |
| 5 | Upgrade `visual_identity.json` v1.0 → v1.1 | Ajout `_schema_version: "visual_identity/1.1"` + `assets_canonical{}` block + `logo_svg{}` block + `wordmark_pattern` regex |
| 6 | Patch `brand.json` | Ajout `_assets_canonical_path: "assets/"` pointer brand-level |

Backward compat strict · les writers anciens continuent à lire `packshots.cdn_paths[]` URL CDN sans erreur. Le block `assets_canonical` est additif optionnel.

## Fallback graceful

Si `assets_canonical` absent OU tous les slots ont `_fallback_to_cdn: true` ·
- compose-creative warning logged `assets_canonical_missing`
- Dégrade automatiquement vers `packshots.primary_front` + `packshots.cdn_paths[]`
- Quality flag déposé `learnings.json` · pattern `gen_quality_degraded_no_canonical` pour audit cross-session
- Operator-facing · zéro exposition technique (`assets_canonical`, `_fallback_to_cdn` jamais surfacés). Operator voit · `source haute résolution manquante, gen dégradée. Upload packshot studio recommandé.`

## Cross-refs

- `resources/schemas/visual_identity.schema.json` v1.1 · schema canon
- `.skills/skills/compose-creative/SKILL.md` HR1.4 (v2.43+) · priorité local source
- `.skills/skills/compose-overlay-text/SKILL.md` v2.43 NEW · PIL composite consumer
- `docs/system/compositional-cartography.md` v2.42 · équation v3.1 NOYAU × CONTEXTE × MODIFIEURS
- `docs/system/schema-encoding-discipline.md` · mutation rule + sourcing tags `_canonical: true|false`, `_fallback_to_cdn: true|false`
- `docs/system/canonical-matrix-reasoning.md` · production 95% intersectional outputs
- `docs/system/operator-vocabulary-translation.md` · jamais exposer `assets_canonical`, `_fallback_to_cdn`, `wordmark_pattern` côté operator. Mapping · `catalog assets`, `source manquante`, `validation wordmark`.

## Anti-patterns

- Ne pas upload sources canon prétextant "le CDN suffit". Le CDN n'est pas une source canon, c'est un fallback.
- Ne pas hardcoder le wordmark dans le prompt compose-creative. Regex `wordmark_pattern` est la validation runtime, le wordmark vit dans `label.wordmark` + canonical SVG.
- Ne pas exposer `_canonical: false` ou `_fallback_to_cdn: true` côté operator brut. Translation operator-facing · `source haute résolution manquante, à uploader`.
- Ne pas confondre `assets_canonical` (produit-level, packshots) avec `logo_svg` (brand-level OU produit override rare). Les deux blocs sont distincts, complémentaires.
