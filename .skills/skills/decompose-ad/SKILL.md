---
name: decompose-ad
version: 1.2.0
type: producer
isolation_scope: brand_only
layer: 2
recommended_model: opus
reasoning_pattern: matrix-driven
matrix_mode: decomposing
description: >
  v1.2.0 (v2.32 alignment) : reads intent_mix (fallback intent if absent) + overlay_density (fallback craft_mode) + meta.validation_status accepts both shapes.
  Decompose une ad (benchmark concurrent OU créa marque interne) en fiche structurée
  selon l'équation compositionnelle v3.1 (NOYAU x CONTEXTE x MODIFIEURS) et persiste
  un instance creative.schema v1.2 brand-side. Reverse-engineering, pas génération.
  Inputs supportés : drop image dans le chat (mode primaire), pull TrendTrack via
  ad_id (`facebook_NNN`) ou URL Meta Ads Library, URL externe (Insta, LinkedIn,
  Reddit) via WebFetch + screenshot fallback. Output operator-facing : fiche v5
  S55 quatre sections (CE QUE L'AD MONTRE / RACONTE / DIAGNOSTIC / RÉUTILISATION)
  + bloc TAGS retrieval. Persist : brands/{slug}/competitive-intel/decomposed/{CRT-NN}.json
  pour benchmark, brands/{slug}/produced/{CRT-NN}.json pour créa interne. Path auto
  determiné par tags.source.
  FR: "decompose cette ad", "analyse cette créa", "que dit cette ad", "decompose",
  "reverse-engineer cette ad", "decompose cette pub".
  EN: "decompose this ad", "analyze this creative", "decompose", "reverse-engineer this ad".
permissions:
  reads: [brand, product, profile, learning, strategy, canon_copy, registries]
  writes: [creative, learning]
  emits_events: [coherence_check, mecanique_proposal_flag]
  mode: proposed
  subagent_safe: true
consumes:
  - path: resources/templates/creative-formula.md
    min_version: 3.1.0
  - path: resources/registries/creative-mechanics-registry.md
    min_version: 1.0.0
  - path: resources/schemas/creative.schema.json
    min_version: 1.2.0
  - path: resources/schemas/_shared/awareness-stage.json
    min_version: 1.0.0
  - path: resources/canon/copy/niveaux-schwartz/*.json
    min_version: 1.0.0
  - path: resources/canon/copy/hooks/*.json
    min_version: 1.0.0
  - path: resources/canon/copy/angles/*.json
    min_version: 1.0.0
  - path: resources/canon/copy/heuristiques-persuasion/*.json
    min_version: 1.0.0
  - path: brands/{slug}/brand.json
    min_version: 1.0.0
  - path: brands/{slug}/audiences/{audience}/profile.json
    min_version: 1.0.0
  - path: brands/{slug}/products/{product_slug}/spec.json#visual_identity
    min_version: 1.10.0
    note: visual identity assets (packshots, color_palette, container, content, label, distinctive_features) consumed for product fidelity in regen pipelines
produces_validations_for:
  - resources/canon/copy/hooks/*.json
  - resources/canon/copy/angles/*.json
  - resources/canon/copy/heuristiques-persuasion/*.json
produces_proposals_for:
  - brands/{slug}/competitive-intel/decomposed/{CRT-NN}.json
  - brands/{slug}/produced/{CRT-NN}.json
disambiguates_against:
  audit-meta-account: "route to audit-meta-account when operator wants to audit a full Meta account (KPI, structure campaigns, pixel, attribution), not a single ad. decompose-ad is one creative at a time."
  produce-paid-angles: "route to produce-paid-angles when operator wants to PRODUCE angles (forward generation from brand intelligence). decompose-ad is reverse-engineering on an existing ad."
  analyze-copy: "route to analyze-copy for long-form copy decomposition (VSL, sales letter, email). decompose-ad is single-ad creative, copy + visual + format coupled, equation v3.1."
  watch-competitors: "route to watch-competitors for ongoing surveillance of a competitor library. decompose-ad is one ad, deep, persisted to creatives."
pipeline:
  preconditions: brand exists with brand.json. Audience optional but recommended (lookup buyer_user_split + persona_archetype). TrendTrack mode requires TRENDTRACK_API_KEY in credentials_shared.env.
  postconditions: creative artifact persisted at competitive-intel/decomposed/ or produced/, conforme creative.schema v1.1, fiche markdown v5 returned to operator, mecanique flag emitted if registry gap detected.
---

# Skill: decompose-ad

> **Reverse-engineer an ad.** v1.1.0 · S55 fiche v5 · creative.schema v1.1 · équation v3.1 · D#391.

> **v1.1.0 (S55 v2.31 alignment)** : consume `spec.json#visual_identity` for product fidelity. Skill loads packshot clean URL + distinctive features in prompt to prevent label regression in regen (audit S55 : sans visual_identity, nano-banana-pro régresse un wordmark with brackets en variantes sans brackets ou caractères corrompus à chaque iter).

Decomposeur, not generator. Lit une ad (visuel + copy verbatim), applique l'équation compositionnelle v3.1, persiste un instance creative.schema brand-side, rend une fiche structurée à l'opérateur en langage clair. Le mécanisme reste invisible (pas de field paths, pas de scores numériques, pas de noms internes). L'opérateur voit une fiche quatre sections et un bloc tags retrieval.

## Tone

Posture éducateur + collègue senior. Pas inspecteur, pas pixel-counter. La fiche est dense mais lisible : phrases courtes, observable d'abord (Section 1), interprétation ensuite (Section 2), diagnostic franc (Section 3), réutilisation actionnable (Section 4). Aucun jargon plumbing, aucun nom de field JSON, aucun acronyme doctrine en surface. Si un texte n'est pas visible ou pas inférable, écrire `-` (jamais halluciner pour combler).

## Expert methodology

**Persona.** Senior creative strategist qui a décomposé dix mille ads paid social cross-typologies (info-produit, cosmétique, supplément, SaaS, DTC apparel, marketplace). Lit une ad comme un copywriter senior lit un sales letter : isole le pivot, nomme la mécanique, juge la cohérence chaîne descendante (audience → insight → angle → mécanique → craft).

**Framework.** Équation compositionnelle v3.1 stress-tested S55 (23 ads cross-typologies). NOYAU = invariant créa (mecanique × format × stop_scroller × ton). CONTEXTE = couches stratégiques branchables (angle × pain_point × persona × proof). MODIFIEURS = override situationnels (occasion × situation × offer × destination × produit × mix_pillar × campaign × regulatory × seasonality_trigger). Source canon : `resources/templates/creative-formula.md`.

**SSOT mécaniques.** `resources/registries/creative-mechanics-registry.md`. Free-string `mecanique_id` autorisé (pas hardcoded enum). Si aucune mécanique du registry ne fitte, utiliser `other` et flag mecanique_proposal pour graduation registry future.

---

## HR1 · Detect input mode

L'opérateur peut fournir l'input sous quatre formes. Detection auto :

| Input shape | Mode | Action |
|---|---|---|
| URL `api.trendtrack.io/...` ou ad_id `facebook_NNN` | trendtrack_pull | HR2 pipeline TrendTrack |
| URL `facebook.com/ads/library/?id=...` | trendtrack_pull | lookup ad_id, puis HR2 |
| URL externe (instagram.com, linkedin.com, reddit.com, tiktok.com, etc.) | manual_drop | WebFetch + screenshot fallback |
| Path local `/Users/.../*.{jpg,png,mp4}` | manual_drop | Read direct |
| Image droppée dans le chat | manual_drop | Read direct |

**Copy texte fourni en parallèle** (l'opérateur colle hook + body + CTA verbatim) → toujours prendre comme source de vérité, override toute lecture OCR du visuel.

**Source vs craft.** `tags.source` détermine le path de persist (HR8). Benchmark concurrent → `external_benchmark` ou `trendtrack_pull`. Créa produite par la marque opérée → `internal_production`. Drop manuel d'une ad inconnue → `manual_drop`.

---

## HR2 · Fetch + download (TrendTrack mode uniquement)

Skip si mode `manual_drop`.

1. `GET /v1/ads/{adId}` → details (content body, format, days_running, reach, spend, country). Cache headers : ETag respecté.
2. `GET /v1/ads/{adId}/media-url` → URL CDN signée.
3. Download local : `/tmp/decompose/{adId}.{jpg|mp4}`. Cache : si fichier déjà présent et taille match, skip download.
4. Si format `video` : extraire frame clé via `ffmpeg -ss 00:00:01 -i {file} -frames:v 1 {file}.jpg` (Step 1 frame). Si hook texte n'est visible qu'après plusieurs secondes, scan toutes les 2s jusqu'à frame avec densité texte la plus haute.
5. Credentials : lire `TRENDTRACK_API_KEY` depuis `credentials_shared.env` (ou `brands/{slug}/credentials.env` si surcharge). Absent → surface honnête à l'opérateur, propose mode `manual_drop` à la place.

---

## HR2bis · Lookup product visual identity (avant gen)

Si `mode == "internal_production"` ou `mode == "compose"` (skill `compose-creative` futur), ET si `target_brand` + `target_product_slug` connus :

1. Read `brands/{target_brand}/products/{target_product_slug}/spec.json#visual_identity`.
2. Si bloc présent et `packshots.primary_front` non-null :
   - Use `packshots.primary_front` comme `image_urls[0]` dans payload `nano-banana-pro/edit` (au lieu d'un screenshot d'ad bruité).
   - Inject `distinctive_features[]` dans le prompt en hard constraints (`MUST PRESERVE: ...`).
   - Inject `color_palette` hex codes dans le prompt (`exact colors: container_primary #..., label_background #...`).
   - Inject `label.wordmark_text` + `label.wordmark_typography_hint` (`label MUST read exactly "{wordmark_text}", never variants`).
   - Inject `content` (form, color, shape, quantity_visible).
3. Si bloc absent :
   - Surface warning à l'opérateur : "spec.json#visual_identity manquant. Render fidelity dégradée. Run skill `populate-visual-identity` (futur) ou drop ad screenshot manuel comme reference".
   - Continue avec ad screenshot bruité comme fallback.

Rationale : sans packshot clean en input, nano-banana-pro hallucine le label sous 2 iter (cf. audit S55 régression wordmark with brackets). Avec packshot + `distinctive_features` injecté, fidélité label peut atteindre 95%+.

---

## HR3 · Lire image + copy

1. Read tool sur le path local (image ou frame extraite).
2. Lire le copy verbatim fourni par l'opérateur (hook texte, body, CTA, primary text).
3. Si copy non fourni et OCR nécessaire, lire le visuel et extraire texte visible. Tagger ces extractions avec confiance basse internement (jamais surfacer le tag à l'opérateur).
4. **NEVER halluciner.** Si un slot n'est pas visible ou pas fourni (ex : pas de body texte sur une ad pure visuelle), écrire `-`. Modalité de la vérité non-dite peut être `formulee | implicite | absente`.

---

## HR4 · Decompose Section 1 · CE QUE L'AD MONTRE (observable, ground truth)

Aucune interprétation. Description objective, vocabulaire neutre.

| Champ | Contenu |
|---|---|
| Format | `static_image | carousel | video_short | video_long | reel | story | gif` |
| Hook visuel | Description objective de la première composition vue (ex : "split-screen avant/après corps féminin, fond crème, surimpression chiffre 12kg") |
| Hook texte | Verbatim. `-` si absent. |
| Body texte | Verbatim. `-` si absent. |
| CTA texte | Verbatim button label + texte autour. `-` si absent. |
| Branding visible | Logo position, packshot oui/non, couleur dominante, font dominant signal |
| Performance | TrendTrack data si dispo (days_running, reach estimé, spend estimé, score perf). `-` sinon. |

---

## HR5 · Decompose Section 2 · CE QUE L'AD RACONTE (interprété, équation v3.1)

Couche interprétation. Chaque inférence est ancrée dans observables Section 1.

**Cible.** Persona déduite. Si la marque opérée est l'auteur de l'ad et `audience_slug` connue, lookup `brands/{slug}/audiences/{audience}/profile.json` pour `buyer_user_split` + `persona_archetype`. Sinon inférer depuis observables (visuel persona, langage, références culturelles). Tag interne `observe / deduit / declare` jamais surfacé. Affichage opérateur : phrase plain language ("femme 30-45, post-partum, frustration retour silhouette pré-grossesse") ou `-` si pas inférable.

**Niveau conscience.** Schwartz 5 stages, source `resources/schemas/_shared/awareness-stage.json`. `unaware | problem_aware | solution_aware | product_aware | most_aware`. Affichage opérateur : phrase ("solution aware, sait que la slimming wear existe, compare les marques").

**Vérité non-dite.** Insight modalité `formulee | implicite | absente`. La vérité non-dite est l'insight psychologique sous l'angle (ex : "elle a honte de remettre son ancien jean et personne le sait"). Modalité formulée = l'ad le dit explicitement. Implicite = l'ad le sous-entend. Absente = l'ad ne touche pas l'insight, opère sur surface produit. Affichage opérateur : citation entre guillemets + modalité en parenthèse, ou `-` si absente.

**Angle d'attaque.** Triplet `levier × positionnement-contre × promesse`. Levier = quel ressort psychologique mobilisé (peur, désir, statut, appartenance, contrôle). Positionnement = contre quoi l'ad se positionne (statu quo, concurrent type, croyance limitante). Promesse = transformation visée. Affichage opérateur : phrase compacte ("vanité féminine post-partum × contre solutions long-terme lentes × silhouette retrouvée en 30 jours").

**Mécanique.** Référence registry `resources/registries/creative-mechanics-registry.md`. Free-string `mecanique_id`. Si aucune ne fitte → `other` + flag `mecanique_proposal` (HR8). Affichage opérateur : nom registry + 1 phrase explicative.

**Pivot du message.** Atome irréductible. Test "delta perf si retiré" : si on enlève cet élément, la créa perd >50% de son hook. Souvent un mot clé, un visuel signature, une stat chiffrée, un avant/après. Affichage opérateur : citation entre guillemets + 1 phrase de justification.

---

## HR5bis · Inject visual_identity in prompt (compose / regen phase)

S'applique en aval (skill `compose-creative` futur, ou regen phase d'un skill orchestrateur consommant decompose-ad output). Si `visual_identity` chargé via HR2bis, format prompt augmentation :

```
Use the EXACT product shown in the reference image. CRITICAL VISUAL FIDELITY:
- Container: {container.shape} {container.material} {container.cap_type}, {container.transparency}
- Content: {content.quantity_visible} {content.form} color {content.color_hex} {content.shape}
- Label: MUST read exactly '{label.wordmark_text}'. Sub-label: '{label.sub_label}'. Duration: '{label.duration_indicator}'.
- Color palette: container {color_palette.container_primary}, label background {color_palette.label_background}, label text {color_palette.label_text}.
- DISTINCTIVE FEATURES (do not modify):
  - {distinctive_features[0]}
  - {distinctive_features[1]}
  - ...
```

QC post-gen : valider chaque `distinctive_features[]` présent dans le render. Échec sur 1+ feature → flag à l'opérateur + propose re-gen avec prompt renforcé.

---

## HR5ter · Write v1.2 fields on persist (v2.32 alignment)

Quand le skill produit un output `creative.json` (HR8 persist), écrire les NOUVEAUX champs creative/1.2 en priorité, garder les anciens en lecture compat seulement.

**Champs nouveaux à écrire (output side) :**

- `intent_mix` (object) : `{primary, secondary?, weights?}`. Skip `weights` si pure (`primary` 100%). Si l'ad observée mélange (ex 60% DR + 40% brand-lift), encoder explicitement `weights: {DR: 0.6, Brand: 0.4}` (somme à 1.0 ± 0.05). Le champ legacy `intent` peut rester en miroir backward-compat (`intent_mix.primary` recopié), mais readers downstream préfèrent `intent_mix`.
- `execution.overlay_density` (number 0.0-1.0) : densité overlay verbal continue. 0.0 photo produit pure, 0.1-0.3 minimal mark / sparse badge, 0.4-0.7 hook + claim layered, 0.8-1.0 verbal-dominated dense.
- `execution.brand_mark_present` (bool) : logo/wordmark visible, orthogonal à `overlay_density`. Le legacy `craft_mode` peut rester en miroir (dérivé : `product_only` si density=0 et brand_mark_present=false ; `minimal_brand_mark` si density<0.3 et brand_mark_present=true ; `with_overlay` si density>=0.4).
- `meta.validation_status` (object composite) : écrire la forme `{status, confidence, confidence_source}` (validation-state.json). Pour décompo benchmark, default `{status: "hypothesis", confidence: 0.5, confidence_source: "default"}`. Pour créa interne avec test_results déjà présents, dériver confidence (`derived_from_test_results`).

**Lecture (input side) :**

- Si `intent_mix` absent sur un fichier existant → fallback `intent` (Hybrid → `{primary: DR, secondary: [Brand], weights: {DR: 0.5, Brand: 0.5}}`).
- Si `overlay_density` absent → fallback `craft_mode` (product_only → 0.0, minimal_brand_mark → 0.2, with_overlay → 0.6).
- Si `validation_status` est string (legacy) → l'accepter via oneOf, traiter comme `{status: <string>}`.

**Backward compat strict :** ne jamais supprimer les anciens champs en écriture, ne pas casser les fichiers v1.1 existants.

---

## HR6 · Decompose Section 3 · DIAGNOSTIC

**Cohérence chaîne descendante.** Audience → insight → angle → mécanique → craft. Chaque transition : `tient | tension | casse`. Affichage opérateur : verdict global ("✓ tient sur les 4 transitions" ou "⚠ tension entre angle et mécanique : l'angle promet rapidité, la mécanique installe long-terme").

**Score arrêt scroll.** Echelle 1-5. Subjectif mais ancré sur observables Section 1. Critères : densité visuelle première frame, contraste avec feed natif, rupture de pattern, charge cognitive immédiate, signature ton. Pas de moyenne pondérée surfacée, juste le verdict numérique + 1 phrase justification.

**Forces.** 3-5 bullets observables. Pas d'éloge vague ("bon hook"), nommer le mécanisme ("hook visuel split-screen avant/après en frame 1, rupture pattern feed natif, lecture du verdict en <1s").

**Risques.** 3-5 bullets. Légal (claims santé sans disclaimer, comparatif déloyal), brand (déconnexion ton vs identité, casting hors persona), audience (insight implicite mais audience trop chaud pour le décoder), execution (CTA mou, body trop chargé, branding noyé).

---

## HR7 · Decompose Section 4 · RÉUTILISATION + TAGS

**Amélioration.** 1-2 phrases actionnables. Ce qu'un copywriter senior changerait pour booster perf sans casser le NOYAU. Ex : "tester un hook texte qui formule explicitement l'insight au lieu de le laisser implicite, l'audience est encore problem-aware sur ce levier".

**Transposable sur.** 2-3 brands où le concept marcherait, avec adaptation 1-line par brand. Tirer de `brands/` actifs si dispo, sinon nommer typologies ("autre marque DTC apparel féminin", "supplément perte de poids féminin 35+").

**Concept-mère.** Générer `concept_id` pattern `cpt_{brand_slug}_{angle_short}_{NNN}`. Si l'ad est une variante d'un concept déjà encodé, lien `variant_of` + `variant_axis` (`photo_swap | promo_toggle | hook_swap | background_swap | persona_split`).

**Bloc TAGS retrieval.** Tous les axes du schema, snake_case strict :

```
brand              {brand_slug}
niche              {niche string}
audience           {audience_slug ou phrase}
mode               concept | template | asset
mecanique          {mecanique_id du registry}
intent             DR | Brand | Hybrid | Lead_gen | Retention | Awareness
audience_segment   B2C | B2B | B2B2C | DTC | marketplace
craft_mode         product_only | minimal_brand_mark | with_overlay
format             {format string}
trigger            {seasonality_trigger ou null}
geographie         {country code ou région}
performance        {days_running / spend bucket / null}
annee              {YYYY}
concept_id         {cpt_brand_angle_NNN}
variant_of         {concept_id parent ou null}
source             internal_production | external_benchmark | trendtrack_pull | manual_drop
```

---

## HR8 · Persist

1. Determine path. Si `tags.source ∈ {external_benchmark, trendtrack_pull}` → `brands/{slug}/competitive-intel/decomposed/{CRT-NN}.json`. Si `tags.source ∈ {internal_production, manual_drop}` ET la marque opérée est l'auteur déclaré de l'ad → `brands/{slug}/produced/{CRT-NN}.json`. Si `manual_drop` sur ad inconnue → `competitive-intel/decomposed/` par défaut.
2. Generate `creative_id`. Pattern `CRT-NN` (CRT-01, CRT-12, CRT-103). Lookup max existing ID dans le path target, increment.
3. Write via `write_to_context(field_path, value, source, confidence, mode="proposed")`. Conforme creative.schema.json v1.1 (tous les champs typés, `_schema_version: "creative/1.1"`, `_equation_ref` const v3.1).
4. **NEVER edit JSON directly via Edit/Write/NotebookEdit.** Mutation gate non-optionnel.
5. Si `mecanique_id == "other"` → emit event `mecanique_proposal_flag` avec payload `{observed_mecanique_signature, ad_creative_id, registry_gap_description}` pour graduation future du registry.
6. Trigger `validate-resources` silencieusement après write. Flag MAJOR/CRITICAL à l'opérateur si remonte.

---

## HR9 · Output operator-facing

Render fiche markdown selon format S55 fiche v5 (template ci-dessous). Vocabulaire opérateur uniquement, pas plumbing. Pas `intent: DR`, dire `Type de campagne : direct response info-produit`. Pas `craft_mode: product_only`, dire `Cadrage : produit seul, pas de surimpression marque`.

**No orphan output.** Terminer sur 1 reco actionnable, pas de menu (a)/(b)/(c). Reco ancrée sur ce qui vient d'être décomposé : transposer concept sur autre brand active, lancer `produce-paid-angles` sur l'audience matchée pour générer 5 variantes du NOYAU, ou flag mecanique_proposal pour enrichir le registry. Une reco forte, pas trois équivalentes.

### Fiche v5 template

```
═══════════════════════════════════════════════════════════════
{TITRE COURT} · {BRAND}
═══════════════════════════════════════════════════════════════
{type_produit} · {langue} · {annee}

───────────────────────────────────────────────────────────────
1 · CE QUE L'AD MONTRE (observable, ground truth)
───────────────────────────────────────────────────────────────
Format             {format}
Hook visuel        {description objective}
Hook texte         "{verbatim ou -}"
Body texte         "{verbatim ou -}"
CTA texte          "{verbatim ou -}"
Branding visible   {logo, packshot, couleur, font}
Performance        {trendtrack data ou -}

───────────────────────────────────────────────────────────────
2 · CE QUE L'AD RACONTE (interprété, équation v3.1)
───────────────────────────────────────────────────────────────
Cible              {persona phrase ou -}
Niveau conscience  {schwartz stage phrase}
Vérité non-dite    "{insight}" ({modalité}) ou -
Angle d'attaque    {levier · contre quoi · promesse}
Mécanique          {nom registry} · {1 phrase}
Pivot du message   "{atome}" · {1 phrase justif}

───────────────────────────────────────────────────────────────
3 · DIAGNOSTIC
───────────────────────────────────────────────────────────────
Cohérence chaîne   {verdict + 1 phrase}
Score arrêt scroll {N} / 5 · {1 phrase}
Forces             · {bullet}
                   · {bullet}
                   · {bullet}
Risques            · {bullet}
                   · {bullet}
                   · {bullet}

───────────────────────────────────────────────────────────────
4 · RÉUTILISATION
───────────────────────────────────────────────────────────────
Amélioration       {1-2 phrases actionnables}
Transposable sur   · {brand_1} · {adaptation}
                   · {brand_2} · {adaptation}
Concept-mère       {concept_id} {· variant_of: parent si applicable}

───────────────────────────────────────────────────────────────
TAGS RETRIEVAL
───────────────────────────────────────────────────────────────
{bloc tags 16 lignes snake_case}

───────────────────────────────────────────────────────────────
{1 reco actionnable contextuelle, 1-2 phrases}
```

---

## Anti-patterns

1. **Hallucinated insight.** Ad ne formule pas d'insight, modèle invente une vérité non-dite "punchy". Règle : modalité `absente` ou champ `-`. Mieux vaut une absence honnête qu'une fabrication.
2. **Forced mecanique.** Aucune des mécaniques registry ne fitte, modèle force le match le moins pire. Règle : `other` + flag `mecanique_proposal`. Le registry grandit par ces flags.
3. **Phantom navigation leak.** Imiter le style `/phantom` avec "→ Tape : decompose-next". Règle : 1 reco contextuelle en prose, pas de menu, pas de slash command surfacé.
4. **Field name leak.** Surface "intent: DR" ou "craft_mode: product_only" à l'opérateur. Règle : traduction systématique en langage métier ("type de campagne", "cadrage").
5. **Pixel-counting.** Sur-décomposer chaque détail visuel sans hiérarchiser (audit S55 anti-pattern). Règle : Section 1 reste haut niveau (5-7 observables clés), pas inventaire exhaustif. La densité est dans Section 2 interprétation.

### Anti-patterns v1.1 (visual_identity)

6. **Skip visual_identity lookup.** Ignorer `spec.json#visual_identity` et passer ad screenshot bruité comme reference (régression label garantie sous 2 iter).
7. **Hardcode distinctive_features dans le skill.** Modifier le prompt distinctive_features hardcodé dans le skill au lieu de lire `visual_identity` (drift inévitable cross-products).
8. **Trust nano-banana-pro to guess label.** Supposer que nano-banana-pro va deviner correctement le label sans hard constraint dans le prompt.
9. **Skip QC distinctive_features.** Skip la validation `distinctive_features[]` dans le QC post-gen.

---

## Edge cases

- **Video sans frame texte exploitable.** Extraire 3 frames (Step 1, milieu, fin), choisir celle avec densité texte la plus haute. Si toutes les frames sont pure visuel, accepter `Hook texte: -`.
- **Carousel multi-cartes.** Décomposer la carte 1 comme NOYAU principal, mentionner les cartes 2-N en `Notes` interne (pas surfacé Section 1). Si une carte ailleurs porte le pivot, déplacer en NOYAU et expliquer en Section 3.
- **Ad UGC / témoignage.** Persona = créateur, pas la marque. Levier souvent appartenance ou preuve sociale. Mécanique typiquement `testimonial_authentic` ou `peer_validation` (vérifier registry).
- **Ad bilingue ou code-switch.** Tagger langue dominante en TAGS, mentionner code-switch dans Section 1 Branding visible.
- **TrendTrack auth absent.** Surface honnête, ne pas tenter mock. Propose `manual_drop` comme fallback.

---

## Cross-refs

- Schema cible : `resources/schemas/creative.schema.json` v1.1 (D#391, audit Phase B v2.29.0).
- Équation : `resources/templates/creative-formula.md` v3.1 (stress-tested S55, 23 ads cross-typologies).
- SSOT mécaniques : `resources/registries/creative-mechanics-registry.md`.
- Schwartz stages : `resources/schemas/_shared/awareness-stage.json`.
- Audit S55 origine : D#391 (creative.schema absorption de 8 champs depuis angle.schema v1.1).
- Sibling skills : `produce-paid-angles` (forward generation), `analyze-copy` (long-form), `watch-competitors` (surveillance), `audit-meta-account` (full account audit).
- Visual identity schema : `resources/schemas/spec.schema.json#visual_identity` (v1.10+, S55 v2.31 extension).
- Audit visual fidelity : `decisions.md` D#392 (S55 audit régression label wordmark with brackets, prompt brand-side → trigger HR2bis + HR5bis).
