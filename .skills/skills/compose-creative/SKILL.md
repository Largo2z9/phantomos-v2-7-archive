---
name: compose-creative
version: 1.0.0
type: producer
recommended_model: opus
subagent_safe: true
mode: proposed
operator_facing: true
reasoning_pattern: matrix-driven
matrix_mode: composing
description: >
  v1.0.0 (v2.34 ship production loop). Pendant FORWARD de decompose-ad (qui est REVERSE).
  Génère une créa (visuel via fal.ai nano-banana-pro/edit + brief copy markdown S55 fiche v5)
  depuis un brief structuré ancré dans canon × profil audience × angle × brand visual_identity.
  Assemblage compositionnel selon équation v3.1 (NOYAU x CONTEXTE x MODIFIEURS).
  Persiste creative.schema v1.2 + JPG local + brief markdown.
  Inputs supportés : (audience_slug, angle_id, product_slug optional), ou hypothèse from
  scratch ("produit angle pour kara post-grossesse" sans angle_id, le skill propose 2-3
  angles depuis profile.json + canon copy).
triggers_fr:
  - "compose une créa"
  - "produis un visuel"
  - "génère une créa pour"
  - "creative pour cette audience"
  - "matérialise l'angle"
triggers_en:
  - "compose a creative"
  - "generate a visual"
  - "produce creative for"
  - "materialize the angle"
disambiguates_against:
  decompose-ad: "decompose-ad fait du REVERSE (analyse ad existante). compose-creative fait du FORWARD (génère depuis brief)."
  produce-paid-angles: "produce-paid-angles produit des ANGLES (stratégie textuelle). compose-creative produit la CRÉA finale (visuel + brief copy)."
  produce-copy-brief: "produce-copy-brief écrit un BRIEF copy. compose-creative orchestre brief + visuel ensemble."
  recompose-creative: "recompose-creative ADAPTE une créa existante (variant). compose-creative produit ex nihilo."
consumes:
  - path: brands/{slug}/angles/{angle_id}.json
    min_version: 1.2.0
    note: angle source (formula Obs+Tension+Reframe+Bridge + lineage canon)
  - path: brands/{slug}/audiences/{audience_slug}/profile.json
    min_version: 1.0.0
    note: 8 dimensions + Schwartz + persona
  - path: brands/{slug}/brand.json
    min_version: 1.0.0
    note: brand_equity_level + creative_zone (curseur copy/visual)
  - path: brands/{slug}/products/{product_slug}/spec.json#visual_identity
    min_version: 1.10.0
    note: packshots clean + color_palette + distinctive_features (S55 v2.31 extension)
  - path: resources/canon/copy/hooks/*.json
    min_version: 1.0.0
  - path: resources/canon/copy/mecaniques/*.json
    min_version: 1.0.0
  - path: resources/canon/copy/archetypes-voix/*.json
    min_version: 1.0.0
  - path: resources/canon/copy/formules-titres/*.json
    min_version: 1.0.0
  - path: resources/templates/creative-formula.md
    min_version: 3.1.0
  - path: resources/registries/creative-mechanics-registry.md
    min_version: 1.0.0
  - path: resources/schemas/creative.schema.json
    min_version: 1.2.0
produces_validations_for:
  - resources/canon/copy/hooks/*.json
  - resources/canon/copy/mecaniques/*.json
  - resources/canon/copy/archetypes-voix/*.json
produces_proposals_for:
  - brands/{slug}/produced/{CRT-N}.json
  - brands/{slug}/produced/{CRT-N}.jpg
  - brands/{slug}/produced/{CRT-N}.md
permissions:
  reads: [brand, product, profile, angle, learning, strategy, canon_copy, registries]
  writes: [creative]
  emits_events: [creative_composed, visual_generated, brief_written, mecanique_proposal_flag]
pipeline:
  preconditions: "angle.json existe avec lineage canon. profile.json 8 dimensions populated. spec.json#visual_identity populated avec primary_front packshot. credentials FAL_API_KEY présent dans credentials_shared.env."
  postconditions: "creative.json conforme creative.schema v1.2 persisté. JPG local persisté dans produced/. brief markdown S55 fiche v5 forward rendu à l'opérateur. Validation silencieuse via validate-resources."
---

# Skill: compose-creative

> **Compose a creative forward.** v1.0.0 · S55 fiche v5 forward · creative.schema v1.2 · équation v3.1 · pendant FORWARD de decompose-ad.

Producer, not decomposer. Lit (angle × audience × brand × product visual_identity × canon copy), applique l'équation compositionnelle v3.1 en mode forward, génère un visuel via fal.ai nano-banana-pro/edit, écrit un brief copy markdown S55 fiche v5, persiste un creative.schema v1.2 brand-side. Le mécanisme reste invisible (pas de field paths, pas de scores numériques, pas de noms internes). L'opérateur voit une fiche quatre sections forward, un JPG local, et un bloc tags retrieval.

## Tone

Posture créateur senior + collègue stratège. Pas inspecteur, pas générateur aveugle. La fiche est dense mais lisible : phrases courtes, projection visuelle d'abord (Section 1), pourquoi ça raconte ça (Section 2), diagnostic prédictif honnête (Section 3), tags retrieval. Aucun jargon plumbing, aucun nom de field JSON, aucun acronyme doctrine en surface. Si un slot manque (visual_identity absent, profile incomplet), surface honnête et propose le skill prérequis à run d'abord.

## Expert methodology

**Persona.** Senior creative director qui a composé dix mille créas paid social cross-typologies. Lit un brief comme un copywriter senior lit un canon : isole le NOYAU (mécanique × format × stop_scroller × ton), branche le CONTEXTE (angle × pain_point × persona × proof), applique les MODIFIEURS (intent_mix × audience_segment × craft_mode × overlay_density × brand_mark_present × cta).

**Framework.** Équation compositionnelle v3.1 stress-tested S55. Source canon : `resources/templates/creative-formula.md`. SSOT mécaniques : `resources/registries/creative-mechanics-registry.md`. Free-string `mecanique_id` autorisé.

**Pattern partagé avec decompose-ad.** Mode forward (input = brief stratégique, output = creative). Mode reverse = decompose-ad (input = ad existante, output = fiche). Cohérence cross-skill obligatoire sur fiche v5 layout.

---

## HR1 · Detect input mode + load pre-requisites

L'opérateur peut fournir l'input sous trois formes. Detection auto :

| Input shape | Mode | Action |
|---|---|---|
| `(audience_slug, angle_id, product_slug)` explicite | forward_direct | Load tous les pre-requis, pipeline complet |
| `(audience_slug, angle_id)` sans product_slug | forward_direct | Lookup product principal de la marque, pipeline complet |
| `(audience_slug, product_slug)` sans angle_id | hypothesis_from_scratch | Skill propose 2-3 angles depuis profile.json + canon copy avant de composer |

**Read pre-requisites obligatoires :**

1. `brands/{slug}/angles/{angle_id}.json` (formula + lineage canon).
2. `brands/{slug}/audiences/{audience_slug}/profile.json` (8 dimensions + Schwartz + persona).
3. `brands/{slug}/brand.json` (creative_zone + brand_equity_level + tone_of_voice).
4. `brands/{slug}/products/{product_slug}/spec.json#visual_identity` (packshots clean + color_palette + distinctive_features + label.wordmark_text).
5. `resources/canon/copy/*` (hooks, mecaniques, archetypes-voix, formules-titres).
6. `resources/registries/creative-mechanics-registry.md` (SSOT mécaniques).

**Pre-requis manquants gate :**

- `visual_identity` absent ou `packshots.primary_front` null → surface warning, suggest `define-specs` à run d'abord. Refuse de composer (régression label garantie).
- `profile.json` incomplet (moins de 6 dimensions sur 8) → surface warning, suggest `profile-audience` à run d'abord. Continue si l'opérateur insiste mais flag confidence basse.
- `angle.json` absent et mode `hypothesis_from_scratch` → propose 2-3 angles candidats depuis profile.json problem_map + canon copy formules-titres, demande validation avant de composer.
- `FAL_API_KEY` absent → surface honnête, refuse de composer, suggest connect-source pour configurer la credential.

---

## HR2 · Apply équation v3.1 compositionnelle

Assembler creative.schema v1.2 selon NOYAU × CONTEXTE × MODIFIEURS.

**NOYAU (invariant créa) :**

- `mecanique` : choisir parmi `creative-mechanics-registry` SSOT en cohérence avec `angle.formula` + `profile.market_context`. Free-string `mecanique_id` autorisé. Si aucune mécanique ne fitte → `other` + flag `mecanique_proposal` (HR7).
- `format` : default `static_image` ratio 4:5 (Meta feed) sauf override opérateur (`carousel`, `video_short`, `reel`, `story`).
- `stop_scroller` :
  - `hook_layer` (verbal) pulled depuis `angle.formula.observation` summary, formulé en 1 phrase courte.
  - `visual_layer` (description scène) depuis `angle.formula.tension` + `audience.problem_map`, descriptif visuel objectif.
- `ton` : depuis `brand.tone_of_voice` + `audience.identity_signals`, croisé.

**CONTEXTE (couches stratégiques branchables) :**

- `angle_ref` : `angle_id` source (lineage canon préservé).
- `pain_point` : depuis `profile.problem_map` + tag verbatims sources si dispo.
- `persona` : depuis `profile` (type + buyer_user_split snapshot cache).
- `proof` : depuis `spec.problems_solved` + `audience.benefit_stack`.

**MODIFIEURS (override situationnels) :**

- `intent_mix` (multi-weighted) : depuis `brand.creative_zone` + `angle.intent` fallback. Si pure (`primary` 100%), skip `weights`. Si mélange (ex 60% DR + 40% Brand), encoder explicitement (`weights: {DR: 0.6, Brand: 0.4}`, somme à 1.0 ± 0.05).
- `audience_segment` : depuis `profile` (B2C default).
- `craft_mode + overlay_density + brand_mark_present` : depuis `brand.creative_zone` curseur.
  - `overlay_density` (0.0-1.0) : 0.0 photo produit pure, 0.1-0.3 minimal mark, 0.4-0.7 hook + claim layered, 0.8-1.0 verbal-dominated.
  - `brand_mark_present` (bool) : logo/wordmark visible, orthogonal à overlay_density.
  - `craft_mode` legacy mirror : `product_only` si density=0 et brand_mark_present=false ; `minimal_brand_mark` si density<0.3 et brand_mark_present=true ; `with_overlay` si density>=0.4.
- `cta` : modalité explicite depuis `angle.formula.bridge.promise` + `offer.json` si applicable.

---

## HR3 · Génération visuelle via fal.ai nano-banana-pro/edit

Pipeline image gen :

1. Récupère packshot clean URL depuis `spec.visual_identity.packshots.primary_front`.
2. Construis prompt structuré :
   - Référence DNA visuel angle (mécanique narrative + scène depuis HR2 NOYAU).
   - Hard constraints `visual_identity` (non-négo) :
     - Container : `{container.shape} {container.material} {container.cap_type}, {container.transparency}`.
     - Content : `{content.quantity_visible} {content.form} color {content.color_hex} {content.shape}`.
     - Label : `MUST read exactly '{label.wordmark_text}'. Sub-label: '{label.sub_label}'. Duration: '{label.duration_indicator}'.`.
     - Color palette : `container {color_palette.container_primary}, label background {color_palette.label_background}, label text {color_palette.label_text}.`.
     - Distinctive features : `MUST PRESERVE: {distinctive_features[0]}. {distinctive_features[1]}. ...`.
   - Atmosphère depuis `brand.creative_zone` + `audience.identity_signals`.
   - Format `4:5 vertical Meta feed` default.
3. POST `https://fal.run/fal-ai/nano-banana-pro/edit` avec `image_urls=[packshot_url]` + `prompt=<above>`. Auth header `Authorization: Key ${FAL_API_KEY}`.
4. Download résultat dans `/tmp/compose-creative/{brand}-{crt_id}.jpg`.
5. Move final vers `brands/{brand}/produced/{CRT-N}.jpg`.

**Retry logic label preservation :**

- Si gen retourne visuel avec label régressé (wordmark différent du `label.wordmark_text`), retry max 2 fois avec prompt renforcé `"PRESERVE EXACTLY label artwork from reference image. Wordmark text MUST be '{label.wordmark_text}' character-for-character. NO variants, NO substitutions."`.
- Si toujours régressé après 3 iter total, flag warning à l'opérateur + persiste avec note `"label compositing externe recommandé v2.35"`.

**QC post-gen :**

- Valider chaque `distinctive_features[]` présent dans le render (lecture image + cross-check description).
- Valider color_palette dominantes match (hex tolérance ±15%).
- Échec sur 1+ feature → flag à l'opérateur + propose re-gen avec prompt renforcé.

---

## HR4 · Génération brief markdown S55 fiche v5 forward

Format opérateur-facing structuré (équivalent decompose-ad output, mode forward).

**Section 1 · CE QUE LA CRÉA VA MONTRER** (projection visuelle objective)

| Champ | Contenu |
|---|---|
| Format | `static_image | carousel | video_short | reel | story` + ratio + langue |
| Hook visuel | Description scène depuis HR2 NOYAU stop_scroller.visual_layer |
| Hook texte | Verbatim généré, max 8 mots, formule depuis canon hooks |
| Body | Description body description (si présent) |
| CTA texte | Verbatim button label + texte autour |
| Branding | Logo position, packshot oui/non, couleur dominante (hex), font signal |
| Visuel généré | Path local `/tmp/compose-creative/{...}.jpg` → `produced/{CRT-N}.jpg` |

**Section 2 · CE QUE LA CRÉA RACONTE** (intention stratégique)

| Champ | Contenu |
|---|---|
| Cible | Phrase plain language depuis profile (persona type + buyer_user_split) |
| Niveau conscience | Schwartz double-stage (entrée + sortie visée) |
| Vérité non-dite | Insight depuis angle.formula.observation+tension, modalité formulee/implicite/absente |
| Angle d'attaque | Levier × positionnement-contre × promesse depuis angle.formula synthèse |
| Mécanique | Nom registry + 1 phrase explicative |
| Pivot du concept | Atome irréductible entre guillemets + 1 phrase justification |

**Section 3 · DIAGNOSTIC PRÉDICTIF**

- Cohérence chaîne : audience → insight → angle → mécanique → craft. Chaque transition `tient | tension | casse`. Verdict global + 1 phrase.
- Score arrêt-scroll prédit : 1-5, ancré sur observables Section 1 (densité visuelle, contraste feed, rupture pattern, charge cognitive, signature ton).
- Forces : 3-5 bullets observables (pas d'éloge vague, nommer le mécanisme).
- Risques : 3-5 bullets (légal, brand, audience, execution).

**Section TAGS RETRIEVAL** : tous les axes du schema, snake_case strict.

---

## HR5 · Persist creative.json + JPG + markdown

Conforme creative.schema v1.2 :

- `_schema_version: "creative/1.2"`.
- `_equation_ref` const v3.1.
- `intent_mix` (multi-weighted depuis HR2). Champ legacy `intent` mirror backward-compat.
- `execution.overlay_density` (0.0-1.0 numérique) + `execution.brand_mark_present` (bool). Champ legacy `craft_mode` mirror dérivé.
- `meta.validation_status` (object composite) : `{status: "hypothesis", confidence: 0.5, confidence_source: "default"}` (créa pas encore testée en prod).
- `meta.test_results[]` empty (sera populé après campagne live).
- `performance.longevity_signal` vide (pas encore en prod).
- `tags.source: "internal_production"`.
- `tags.concept_id` : nouveau `cpt_{brand_slug}_{angle_short}_{NNN}` ou `variant_of: {parent_concept_id}` si dérivé.

**Mutation gate :**

1. Generate `creative_id`. Pattern `CRT-NN`. Lookup max existing ID dans `brands/{slug}/produced/`, increment.
2. Write via `write_to_context(field_path, value, source, confidence, mode="proposed")`. **NEVER edit JSON directly via Edit/Write/NotebookEdit.**
3. Persist JPG : move `/tmp/compose-creative/{brand}-{crt_id}.jpg` → `brands/{brand}/produced/{CRT-N}.jpg`.
4. Write brief markdown : `brands/{brand}/produced/{CRT-N}.md` (format S55 fiche v5 forward).
5. Si `mecanique_id == "other"` → emit event `mecanique_proposal_flag` avec payload `{observed_mecanique_signature, ad_creative_id, registry_gap_description}`.
6. Trigger `validate-resources` silencieusement post-write. Flag MAJOR/CRITICAL à l'opérateur si remonte.

---

## HR6 · Output operator-facing

Render fiche markdown selon format S55 fiche v5 forward (template ci-dessous). Vocabulaire opérateur uniquement, pas plumbing. Pas `intent_mix: {primary: DR}`, dire `Type de campagne : direct response`. Pas `overlay_density: 0.6`, dire `Cadrage : hook + claim layered sur packshot`.

**No orphan output.** Terminer sur 1 reco actionnable forte ancrée sur ce qui vient d'être composé.

- Confidence ≥ 0.5 + chaîne cohérente : suggest tester maintenant (plateforme + audience cible recommandée).
- Confidence < 0.5 (hypothèse non-validée) : suggest A/B avec 2 angles concurrents (run `compose-creative` sur angle alternatif).
- Variantes du concept : suggest `recompose-creative` pour photo_swap / hook_swap / persona_split.
- Visual_identity packshot manque : lien vers run `define-specs`.

Une reco forte, pas trois équivalentes.

---

## HR7 · Anti-patterns

1. **Compose sans visual_identity.** Régression label garantie sous 2 iter (audit S55 `kara[care]` → `karacare`). Refuse de composer si `packshots.primary_front` absent.
2. **Hardcoded mécanique.** Modifier le prompt mécanique hardcodé dans le skill au lieu de lookup canon registry SSOT. Drift inévitable cross-products.
3. **Skip angle.formula validation.** NOYAU sans angle = creative null. Refuse de composer si `angle.json` absent ou `formula` vide.
4. **Direct write produced/.** Mode `proposed` non-optionnel. Mutation gate via `write_to_context` obligatoire.
5. **Regen >3 iter pour label preservation.** Basculer compositing externe v2.35, ne pas brûler API budget en boucle.
6. **JSON brut leak.** Surface `intent_mix: {primary: DR, weights: {DR: 0.6}}` à l'opérateur. Règle : traduction systématique en langage métier.
7. **Plumbing leak.** Surface `field_path`, `source`, `confidence`, `mode` à l'opérateur. Règle : opérateur voit `observé / déduit / déclaré / incertain`, jamais numbers.
8. **Doctrine name leak.** Surface `canonical-matrix-reasoning`, `Contextual Intelligence`, `Schema Encoding Discipline` à l'opérateur. Règle : opérateur sent les effets, pas les noms.
9. **Hypothesis from scratch sans validation.** Mode `hypothesis_from_scratch` propose 2-3 angles candidats AVANT de composer, jamais compose direct sur angle inventé.
10. **Phantom navigation leak.** Imiter `/phantom` avec "→ Tape : compose-next". Règle : 1 reco contextuelle en prose, pas de menu, pas de slash command surfacé.

---

## Operator output template

### Fiche v5 forward template

```
═══════════════════════════════════════════════════════════════
{BRAND} · COMPOSE CREATIVE · {CRT-N}
═══════════════════════════════════════════════════════════════
{audience_slug} · angle {angle_id} · {date}

───────────────────────────────────────────────────────────────
1 · CE QUE LA CRÉA VA MONTRER
───────────────────────────────────────────────────────────────
Format             {format} · {ratio} · {language}
Hook visuel        {scene_description}
Hook texte         "{hook_text}"
Body               {body_description ou -}
CTA texte          "{cta_text}"
Branding           {brand_visibility}
Visuel généré      /tmp/compose-creative/{...}.jpg → produced/{CRT-N}.jpg

───────────────────────────────────────────────────────────────
2 · CE QUE LA CRÉA RACONTE
───────────────────────────────────────────────────────────────
Cible              {audience_summary depuis profile}
Niveau conscience  {schwartz double-stage}
Vérité non-dite    "{insight}" ({modalité}) ou -
Angle d'attaque    {levier · contre quoi · promesse}
Mécanique          {nom registry} · {1 phrase}
Pivot du concept   "{atome_irreductible}" · {1 phrase justif}

───────────────────────────────────────────────────────────────
3 · DIAGNOSTIC PRÉDICTIF
───────────────────────────────────────────────────────────────
Cohérence chaîne   audience → insight     {tient | tension | casse}
                   insight → angle        {tient | tension | casse}
                   angle → mécanique      {tient | tension | casse}
                   mécanique → craft      {tient | tension | casse}
Score prédictif    {N} / 5 · {1 phrase}
Forces             · {bullet}
                   · {bullet}
                   · {bullet}
Risques            · {bullet}
                   · {bullet}
                   · {bullet}

───────────────────────────────────────────────────────────────
TAGS RETRIEVAL
───────────────────────────────────────────────────────────────
brand              {brand_slug}
niche              {niche}
audience           {audience_summary}
mode               {concept | template | asset}
mecanique          {registry_id}
intent_mix         primary={primary} secondary={secondary[]} weights={...}
craft_mode         density={overlay_density} mark={brand_mark_present}
format             {format}
trigger            {evergreen | seasonal trigger}
geographie         {geo}
annee              {year}
concept_id         {cpt_id}
variant_of         {parent_concept_id ou null}
source             internal_production

───────────────────────────────────────────────────────────────
{1 reco actionnable contextuelle, 1-2 phrases}
```

---

## Edge cases

- **Hypothesis from scratch (pas d'angle_id).** Skill propose 2-3 angles candidats depuis `profile.problem_map` + `canon/copy/formules-titres`. Demande validation opérateur AVANT pipeline gen. Ne compose jamais sur angle inventé sans gate.
- **Multi-products brand.** Si `product_slug` absent et marque a 2+ produits, demande choix opérateur (1 question AskUserQuestion). Ne devine pas.
- **Visual_identity partiel.** `primary_front` présent mais `distinctive_features[]` vide → continue, flag confidence dégradée. `primary_front` absent → refuse.
- **fal.ai API down ou rate limit.** Surface honnête, propose retry ETA + path manuel (compositing externe). Ne tente pas mock.
- **Label régressé après 3 iter.** Persiste creative.json + JPG avec note `label_compositing_required: true` dans meta. Flag à l'opérateur, suggest v2.35 compositing externe.
- **Concept variant.** Si opérateur déclare "comme CRT-12 mais hook différent", set `variant_of: {parent_concept_id}` + `variant_axis: hook_swap`. Lineage préservé.

---

## Cross-refs

- Schema cible : `resources/schemas/creative.schema.json` v1.2 (D#391, audit Phase B v2.29.0 + v2.32 alignment).
- Équation : `resources/templates/creative-formula.md` v3.1 (stress-tested S55, 23 ads cross-typologies).
- SSOT mécaniques : `resources/registries/creative-mechanics-registry.md`.
- Schwartz stages : `resources/schemas/_shared/awareness-stage.json`.
- Visual identity schema : `resources/schemas/spec.schema.json#visual_identity` (v1.10+, S55 v2.31 extension).
- Audit visual fidelity : `decisions.md` D#392 (S55 audit régression label `kara[care]`).
- Sibling skills : `decompose-ad` (REVERSE pattern, fiche v5 layout source), `produce-paid-angles` (forward angles textuels), `produce-copy-brief` (brief copy seul), `recompose-creative` (variant existant), `define-specs` (visual_identity prerequisite), `profile-audience` (profile prerequisite).
- Doctrines : `docs/system/canonical-matrix-reasoning.md` (production discipline), `docs/system/skill-authoring-discipline.md` (frontmatter triad), `docs/system/contextual-intelligence.md` (operator-facing rule absolue).
