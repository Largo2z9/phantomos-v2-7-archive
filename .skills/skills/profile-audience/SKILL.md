---
name: profile-audience
version: 1.3.1
patch_notes:
  - "1.2.0 · v2.39+ · Step 0ter framework awareness (4 questions cartography pédagogie inline)"
  - "1.3.0 · v2.54 investigation posture refactor surface · audiences présentées comme hypothèses avec confidence chain explicite (TRÈS faible par défaut sans mine-voc · faible 1-2 indicateurs site · moyenne mine-voc partiel · forte mine-voc + analytics convergents). Operator output template HR6 + HR8 restructurés · chaque audience porte hypothèse / confidence / indicateurs sources / validation requise / anti-pattern à respecter. Skill termine sur close drill-down macro · lancer mine-voc maintenant vs valider intuitivement et continuer. Préserve mécanismes 8 dimensions Schwartz double-stage problem_map. Refacto uniquement la posture surface · présentation comme hypothèse vs persona analytique. Cross-ref docs/system/investigation-posture.md."
  - "1.3.1 · v2.55 audit consume canon matrices · consumes: enrichi (archetypes-voix, heuristiques-persuasion, creative-formula.md) + HR0bis NEW Load canon matrices force lecture batch via phantom-canon.py + cross-product canon × audience obligatoire en HR3 Dimensions 1/6/7 (canon_ref cité Layer A trace + profile.json#lineage). Aligne déclaration consumes: avec ce que les Steps lisent réellement. Anti-pattern banni · halluciner archetype ou biais audience-side sans mapping canon. Master doctrine ré-activé · PhantomOS reasons over a business universe, canon dormant = output générique averaged-LLM."
type: orchestrator
isolation_scope: brand_only
layer: 3
recommended_model: sonnet
subagent_safe: true
mode: proposed
operator_facing: true
description: Synthétise les outputs de mining (voc/vom/audience) en profil audience structuré 8 dimensions canon V3. Consume verbatims raw, produit profile.json conforme schema v1.3 avec validation gate operator. Ne mine pas, synthétise.
triggers_fr:
  - "profil audience"
  - "synthétise l'audience"
  - "8 dimensions audience"
  - "structure audience"
  - "cartographie sub-cluster"
triggers_en:
  - "profile audience"
  - "synthesize audience"
  - "8 dimensions"
  - "structure audience"
  - "map sub-cluster"
disambiguates_against:
  - mine-voc: "mine-voc capture verbatims clients (raw signals). profile-audience SYNTHÉTISE ces signals en profil 8-dim structuré."
  - mine-vom: "mine-vom capture vernaculaire marché. profile-audience consume les outputs des mining skills."
  - mine-audience: "mine-audience découvre des sub-clusters candidats. profile-audience structure un sub-cluster spécifique en 8 dimensions."
  - cartograph: "cartograph est READ-ONLY synthèse strategique. profile-audience WRITE (peuple profile.json)."
consumes:
  - brands/{slug}/audiences/_voc/* (mine-voc outputs)
  - brands/{slug}/audiences/_vom/* (mine-vom outputs)
  - brands/{slug}/audiences/{audience}/raw/* (mine-audience outputs)
  - resources/schemas/profile.schema.json (target)
  - resources/canon/copy/niveaux-schwartz/* (awareness stages reference · Schwartz double-stage Step Q3 + HR4)
  - resources/canon/copy/archetypes-voix/* (voix archetype matrice canon · cross-pollination identité audience HR3 Dimension 7)
  - resources/canon/copy/heuristiques-persuasion/* (biais cognitifs canon · informe purchase_driver HR3 Dimension 1 + objections psychology)
  - resources/canon/copy/creative-formula.md (8 dimensions canon V3 · contrat HR3)
produces_validations_for: []
produces_proposals_for:
  - brands/{slug}/audiences/{audience_slug}/profile.json
permissions:
  reads: [brands/, resources/]
  writes: [brands/{slug}/audiences/{slug}/profile.json via write_to_context]
  emits_events: [profile_proposal_created, profile_validated]
pipeline:
  preconditions:
    - "mine-voc OR mine-vom OR mine-audience a tourné"
    - "audience_slug défini"
  postconditions:
    - "profile.json conforme profile.schema v1.3"
    - "8 dimensions populated"
    - "operator validation gate passed"
prerequisites:
  - field: audiences/{slug}/profile.json
    level: L1
    auto_pull: brownfield_seed_read
    freshness_ttl_days: 90
  - field: audiences/{slug}/mining-outputs/
    level: L1
    auto_pull: read_mining_outputs
    freshness_ttl_days: 60
  - field: audiences/{slug}/verbatim_density
    threshold: 3
    level: L3
    fallback: infer_from_canon_archetype
    confidence_default: 0.5
  - field: resources/canon/copy/archetypes-voix
    level: L1
    auto_pull: read_canon_directory
    freshness_ttl_days: 365
---

# profile-audience

Synthétise un sub-cluster d'audience en profil 8 dimensions canon V3. Consume les outputs de mining et produit `profile.json` conforme `profile.schema v1.3`. Operator-facing avec validation gate avant write.

## Hard Rules

### Step 0bis · Prerequisite check (DRGFP v2.38)

Avant lecture mining outputs (Step 1), scanner prerequisites :

1. Lookup `audiences/{slug}/profile.json` brownfield existing → si présent + freshness 90d OK → seed corpus silent (HR2.5 v2.35 pattern)
2. Lookup mining outputs (mine-voc, mine-vom, mine-audience) → si présents → consume silent
3. Compter verbatim_density cumulé (existing seed + mining) → si < 3 → L3 degraded · fallback infer canon archetype · confidence 0.5 · flag _gaps
4. Lookup canon archetypes-voix → silent always (cross-brand canon read)

Output state map + confidence_chain[] init avec valeur dépendante de density actuelle.

Cross-ref doctrine : `docs/system/dependency-resolution-protocol.md`.

Note framework cartography · Step 0ter applique 4 questions framework (entry_door · scope · stade Schwartz · chevauchements). Cf `docs/doctrine/audience-cartography-framework.md`.

### Step 0ter · Framework awareness (v2.39+)

Application du framework cartography (4 questions canon · `docs/doctrine/audience-cartography-framework.md`).

Au début de la cartographie · poser Q1 explicit (porte d'entrée). Les 3 autres questions sont posées au fil du flow (Step 1 niveau · Step 4 stade · Step 7 chevauchements).

#### Q1 · Porte d'entrée

AskUserQuestion :

> Cette audience entre dans la catégorie {brand_category} par quelle porte ?
> 
> (a) Pain-driven · entre par un problème ressenti (ex chute, sec, gris)
> (b) Goal-driven · entre par une ambition (ex longueur pour mariage, summer hair)
> (c) Identity-driven · entre par qui elle est ou veut être (ex hijabi, sportive, mum)
> 
> 1 porte dominante. Si elle a 3 portes égales, c'est un mix mal séparé · à re-découper.

Persister dans meta.entry_door enum [pain_driven · goal_driven · identity_driven].

Si operator hésite ou répond "mix" → flag potential audience-redondante (Piège 2 framework) · suggestion · re-découper avant cartographier.

Operator-facing · jamais exposer "entry_door" brut. Dire "porte d'entrée" en surface.

#### Q2 · Niveau granularité (Step 1 mining)

Inférer scope automatiquement depuis :
- audience description scope (large/spécifique/hyper-niche)
- verbatim count + diversity (si forte diversité = broad ; concentrée = segment ; ultra-spécifique = micro)
- parent_slug détectable dans existing brand audiences

Si ambiguïté → AskUserQuestion :

> Niveau de granularité de cette audience ?
> 
> (a) Broad · audience mère, 500k+ actives, 1-3 par brand
> (b) Segment · poche définie, 100-500k actives, 5-15 par broad
> (c) Micro · hyper-niche, 20-100k actives, 0-3 par segment

Si micro → require justification 3/3 :
- volume_remaining_estimate (k actives)
- pitch_divergent (oui/non + en quoi)
- offer_divergent (oui/non + en quoi)

Si 0/3 ou 1/3 → refuse + suggestion "c'est une variation copy, pas une sous-audience".

Persister meta.scope + meta.parent_slug.

Operator-facing · dire "niveau" et "audience mère", jamais "scope" ni "parent_slug" brut.

#### Q3 · Stade Schwartz (Step 4 psychology block)

Au moment de remplir block psychology · inférer 2 axes Schwartz depuis verbatim + behaviour patterns :
- product-awareness (unaware → problem → solution → product → most-aware)
- emotional-maturity (niant · résigné · en recherche · combatif · acceptant)

Surface inference + AskUserQuestion validation :

> Stade Schwartz inféré pour cette audience :
> 
> Product-awareness : {inferred_stage_product}
> Emotional-maturity : {inferred_stage_emotional}
> 
> (a) Confirmer
> (b) Ajuster product-awareness
> (c) Ajuster emotional-maturity
> (d) Ajuster les deux

Persister psychology.awareness_stage_product + psychology.awareness_stage_emotional.

#### Q4 · Chevauchements (Step 7 write final)

Avant write_to_context final · scanner brand-side existing audiences pour chevauchements potentiels :
- Pain_points overlap (similarity threshold 0.6)
- Benefits overlap (similarity threshold 0.6)
- Identity narrative overlap (semantic similarity)

Surface les 1-3 audiences cousines détectées :

> J'ai détecté chevauchement potentiel avec :
> 
>   {audience_X} · pain similaire {pain_overlap} (~{score}% match)
>   {audience_Y} · benefit similaire {benefit_overlap} (~{score}% match)
> 
> (a) Confirmer ces chevauchements (write meta.overlap_with)
> (b) Ne pas signaler ces chevauchements
> (c) Ajouter d'autres chevauchements manuels

Persister meta.overlap_with[] array slugs.

Note pédagogique opérateur · les chevauchements ne disqualifient pas l'audience · ils révèlent les angles porteurs cousinés (cross-pollinisation copy). Operator-facing · dire "audiences cousines", jamais "overlap_with" brut.

### HR0bis · Load canon matrices (v2.55 routing systémique)

Avant HR1 (mining inputs), **force la lecture** des matrices canon copy déclarées en `consumes:`. Skill ne fonctionne pas en mode prose libre déduit de connaissance LLM · il consume canon. Si canon est dormant → output générique averaged-LLM, contourne le master doctrine `PhantomOS reasons over a business universe`.

Lecture batch via `python3 .skills/phantom-canon.py copy {layer}` pour chaque couche utilisée par ce skill ·

1. **`niveaux-schwartz`** · les 5 stages product_awareness + 5 stages emotional_maturity canoniques (Step Q3 + HR4 Schwartz double-stage). Cache en mémoire pour la durée du run.
2. **`archetypes-voix`** · 6+ archetypes canon (caregiver, sage, rebelle, amante, heros, homme-ordinaire). Cross-référencé en HR3 Dimension 7 (Identity Signals) pour mapper l'archetype audience-side à un archetype canon, pas inventer.
3. **`heuristiques-persuasion`** · biais cognitifs canon (loss-aversion, social-proof, scarcity, anchoring, reciprocity, authority, etc.). Cross-référencé en HR3 Dimension 1 (Purchase Driver) + Dimension 6 (Alternative Map · pourquoi insuffisant) pour informer le mapping psychology audience-side.
4. **`creative-formula.md` V3** · contrat 8 dimensions canon. Validé que les 8 dimensions HR3 mappent strictement aux 8 dimensions canon V3.

Pour chaque outil canon lu, garder en mémoire · `id, when_works[], when_avoid[], combines_with{}`. Ces contraintes filtrent quels archetypes/biais sont compatibles avec le contexte audience résolu en Step 0bis/0ter.

Cross-product canon × audience obligatoire en HR3 · chaque Dimension 1/6/7 cite explicitement le canon_ref utilisé (archetype_canon_id, biais_canon_id) dans Layer A trace + profile.json#lineage. Anti-pattern v2.55 banni · halluciner un archetype audience-side ("caregiver overprotecteur") sans le mapper au canon archetypes-voix.

### HR1 · Verify mining inputs available

Vérifier que `mine-voc` OR `mine-vom` OR `mine-audience` a tourné pour cette audience.
Si aucun mining n'a tourné, surface warning :

> Pas de signal mining disponible. Skill produira hypothesis-grade. Run mine-voc d'abord pour grade validated. Continuer ?

### HR2 · Load mining outputs

Read `brands/{slug}/audiences/_voc/{audience}/*` + `_vom/*` + `raw/*`.
Aggrégate verbatims, key_expressions, pain points raw, benefits raw.
Cache localement dans `/tmp/profile-audience/{audience}-mining-corpus.json`.

### HR2.5 · Read existing profile.json as seed corpus (brownfield)

v1.0.1 (v2.35 alignment) : HR2.5 brownfield seed (read existing profile.json as seed corpus, preserve validated entries) + HR7.1 merge strategy explicite (no auto-overwrite).

Si `brands/{slug}/audiences/{audience_slug}/profile.json` existe et contient déjà des entries (verbatims inliné, pain_points populés, voice.key_expressions, etc.) :

1. Read le profile.json existant comme seed
2. Extraire :
   - voice.key_expressions[] · verbatims pré-existants
   - pain_points[] · chains 3 niveaux pré-existants
   - benefits[] · chain functional/emotional/identity pré-existants
   - identity.* · démographie pré-existante
3. Merger avec mining corpus (HR2) si dispo
4. Marquer chaque entry source : `existing_profile` (seed) vs `mine_voc/vom/audience` (fresh mining)
5. Préserver `validation_status` existant des entries déjà validées (status >= validated)

HR2.5 garantit le skill fonctionne en mode brownfield (audience pré-amorcée par opérateur ou skill antérieur) sans écraser ni perdre l'existant.

### HR3 · Synthesize 8 dimensions

Pour chaque dimension, extraire/synthétiser depuis le corpus :

**Dimension 1 · Purchase Driver**
Identify dominant driver from verbatims : `pain | desire | status | utility | identity | mixed`.
Source verbatims supporting (sample_size).

**Dimension 2 · Problem Map**
Pain principal + frequency + intensity + context.
Décomposer en 3 niveaux : `surface` (ce qu'elle dit en premier) · `consequence` (impact quotidien) · `deep` (sens identitaire/existentiel).

**Dimension 3 · Benefit Stack**
Bénéfices cherchés rangés par ordre de priorité.
Chaîne `functional → emotional → identity`.

**Dimension 4 · Mechanism (audience-side)**
Comment la cible PENSE que la solution doit fonctionner.
Exemple : "elle pense que la repousse vient de la racine donc cherche traitement scalp" vs "elle pense que c'est génétique donc cherche transplant".

**Dimension 5 · Market Context**
Niveau Schwartz sophistication 1-5 (canon copy reference).
Awareness stage dominant : `unaware / problem_aware / solution_aware / product_aware / most_aware`.

**Dimension 6 · Alternative Map**
Autres solutions utilisées (concurrents, OTC, bricolage, abandons).
Pourquoi elles ne suffisent pas (verbatims).

**Dimension 7 · Identity Signals**
Marqueurs mode de vie observables (style, références culturelles, valeurs déclarées).

**Dimension 8 · Decision Process**
Path achat (recherche, comparaison, consultation, déclenchement).
Decision makers : `self / family / peers / influencer / professional`.
Trigger event qui déclenche l'achat.

### HR4 · Cross-validate Schwartz double-stage

Pour chaque sub-cluster, identifier :
- `product_stage` : niveau Schwartz produit-spécifique (ex `product_aware` sur une brand donnée)
- `emotional_stage` : niveau émotionnel orthogonal (ex `pain-active` vs `solution-seeking`)

Note : peut différer (cf D#384 multi-product binding · audit S55).

### HR5 · Identify pain_points 3 niveaux

Pour chaque pain principal, décomposer chaîne :
- `surface` : verbatim direct ("j'ai mal aux pieds en fin de service")
- `consequence` : impact quotidien ("je rentre épuisé, irritable")
- `deep` : sens identitaire ("j'envisage de changer de métier")

Tag verbatims sources pour chaque niveau.

### HR6 · Surface draft profile à operator (posture investigation, v2.54+)

**Doctrinal contract.** Présenter en posture **hypothèse**, pas conclusion analytique. Chaque audience structurée porte sa confidence chain explicite per `docs/system/investigation-posture.md`. Anti-pattern AP-2 doctrine BANNI · personas inventés présentés comme analytiques sans data verbatim client. Quand le mining n'a pas tourné (ou tourné partiellement), l'output doit signaler explicitement que l'audience est sur du sable.

**Confidence chain explicit par audience** ·

| Niveau confidence | Indicateurs requis | Formulation cible operator |
|---|---|---|
| `forte` | Mine-voc + analytics audience convergents + verbatims 10+ par pain principal | "Pattern confirmé · {audience}" |
| `moyenne` | Mine-voc partiel (5-10 verbatims) + indicateurs site convergents | "Hypothèse soutenue · {N} indicateurs" |
| `faible` | 1-2 indicateurs site OR opérateur déclaré sans mining | "Hypothèse à valider · {indicateur}" |
| `TRÈS faible` | Intuition modèle sur copy / partenaires / vocabulaire site, zéro verbatim client | "Intuition seulement · à valider OBLIGATOIREMENT avant utilisation stratégique" |

Default sans mine-voc · confidence `TRÈS faible`. Le skill DOIT explicitement flagguer ces audiences comme non-utilisables comme fondation à une décision budget / brief créa / positioning.

**Structure operator output par audience** ·

Pour CHAQUE audience proposée, structure obligatoire (anti-pattern · persona analytique présenté sans confidence chain) ·

- **Hypothèse identifiée · {nom audience court}** (titre)
- **Confidence** · {forte / moyenne / faible / TRÈS faible}
- **Indicateurs sources** · {ce qui justifie l'hypothèse · copy site / influence partners profile / déclaration opérateur / verbatims si mining tourné}
- **Validation requise** · {ce qui doit être fait pour upgrader à `forte` · ex "mine-voc sur Trustpilot + analytics audience"}
- **Anti-pattern à respecter** · si confidence `TRÈS faible`, flag explicite "OBLIGATOIREMENT à valider via mining client réel avant utilisation stratégique (décision budget / brief créa / positioning)"

Demander macro arbitrage :

> Voici les audiences structurées en hypothèses. Confidence chain visible par audience. Pour passer ces audiences de hypothèse `TRÈS faible` ou `faible` à `validée` · veux-tu lancer une écoute clients réelle maintenant (~8-12 min de mining sur Trustpilot + forums niche pour récupérer les vrais verbatims) ou tu valides intuitivement et on continue, en sachant que ce qui sera produit downstream (angles, brief créa) portera cette confidence-là ?

L'opérateur arbitre · `lance écoute clients` → trigger mine-voc silencieusement OR `valide et continue` → préserver les audiences en hypothèse + propager confidence chain downstream.

### HR7 · Persist via mutation gate

Une fois validé, `write_to_context` sur `brands/{slug}/audiences/{audience_slug}/profile.json`.
Conformité `profile.schema v1.3` obligatoire.
Source : `derived` (skill orchestrator) + tag verbatims sources.

### HR7.1 · Merge strategy explicite

Avant write_to_context :

1. Re-load profile.json actuel (state of truth at write time)
2. Pour chaque entry du draft skill :
   - Si entry source `existing_profile` + `validation_status >= validated` → preserve (skill ne touche pas)
   - Si entry source `mine_*` + entry n'existe pas dans current profile → append
   - Si entry source `mine_*` + entry existe dans current profile → flag conflict, surface à operator
3. Operator gate explicite si conflits détectés

### HR8 · Output operator-facing (close drill-down macro, v2.54+)

Vue lisible profile · chaque audience portée comme hypothèse avec confidence chain explicite per HR6 refactor.

**Close obligatoire · UNE question macro drill-down** (anti-pattern AP-5 doctrine · close affirmatif qui ferme la conversation `Je passe au next step ?` → BANNI).

Format close canonique v2.54 ·

> Pour passer ces audiences de hypothèse `TRÈS faible` à validée terrain, ce qui débloque la suite (angles paid, brief créa) avec une fondation sourcée ·
>
> A · Lance l'écoute clients maintenant ({~8-12 min} sur Trustpilot + forums niche · récupère les vrais verbatims · upgrade confidence à `moyenne` ou `forte` selon densité corpus)
> B · Valide intuitivement et on continue · ce qui sera produit downstream (angles, brief créa) portera la confidence `TRÈS faible` héritée (à tester avec budget calibré, pas all-in)
> C · Tu m'injectes des données existantes que t'as déjà (reviews exportées, analytics audience, retours SAV) en 1-2 phrases denses, je les intègre et on re-évalue confidence
>
> Mon avis · {recommandation macro adaptive · si verbatim_density < 3 → A en premier critique pour fondation downstream · sinon B valide si confidence `moyenne` déjà sur l'audience}.

L'opérateur arbitre macro. Pas de menu décoratif, UNE question avec reco.

**Anti-patterns surface operator** ·
- JAMAIS exposer `confidence` comme un nombre (0.6, 0.4) en surface. Qualitatifs uniquement (`TRÈS faible / faible / moyenne / forte`).
- JAMAIS exposer field path interne (`meta.entry_door`, `psychology.awareness_stage_product`, `validation_status: hypothesis`) en surface. Reformuler en langage métier.
- JAMAIS nommer skill (`mine-voc`, `produce-paid-angles`) en surface · routing silencieux à l'agent après choix opérateur.
- JAMAIS afficher persona inventé comme analytique (anti-pattern AP-2 doctrine). Toujours flaggué hypothèse avec confidence chain.

### HR9 · Anti-patterns

- Ne JAMAIS halluciner une dimension sans verbatims sources
- Ne JAMAIS poser une dimension à hypothesis sans tag `confidence < 0.5`
- Ne JAMAIS skip Schwartz double-stage check
- Ne JAMAIS auto-write sans operator validation gate
- Ne JAMAIS exposer JSON brut à l'opérateur

## Operator output template (v2.54 investigation posture)

Template canonique post-v2.54 · chaque audience portée comme hypothèse avec confidence chain explicite. Anti-pattern AP-2 doctrine BANNI · personas inventés présentés comme analytiques sans data verbatim.

```
{BRAND} · {AUDIENCE_SLUG} · HYPOTHÈSE STRUCTURÉE

Hypothèse identifiée · {nom audience court}
Confidence · {forte | moyenne | faible | TRÈS faible}
Indicateurs sources · {ce qui justifie · copy site / influence partners / déclaration opérateur / verbatims mine-voc si dispo}
Validation requise · {ce qui doit être fait pour upgrader · ex "mine-voc Trustpilot + analytics audience"}
{Si confidence TRÈS faible · ligne flag explicite "OBLIGATOIREMENT à valider avant utilisation stratégique (budget / brief créa / positioning)"}

─────────────────────────────────────────────

[1] Purchase driver (hypothèse)
  Dominant driver inféré  {driver}
  Indicateurs             {N} citations verbatim si dispo, OR signaux site si pas de mining
  À valider               {ce qui upgrade confidence sur ce driver}

[2] Problem map (hypothèse)
  Pain principal inféré  {pain}
  Fréquence              {frequency} ({confidence sur freq})
  Intensity              {intensity}
  Surface (1er niveau)   "{verbatim si dispo}" OR "à capturer via mining"
  Consequence (2e)       {consequence inférée}
  Deep (3e identitaire)  {deep_meaning inféré · confidence TRÈS faible si pas de mining}

[3] Benefit stack (hypothèse)
  Top bénéfices inférés
    1. {benefit_1} (functional → emotional → identity)
    2. ...
  Indicateurs              {sources mining si dispo}

[4] Mechanism · audience-side belief (hypothèse)
  La cible pense que la solution doit fonctionner via · {mechanism_belief}
  Confidence sur ce belief · {niveau}
  À valider                · {comment vérifier · ex "mine-voc reviews concurrence + forums"}

[5] Market context (déduit · confidence variable)
  Schwartz sophistication inféré  {1-5} ({confidence})
  Awareness stage dominant       {stage} ({confidence})
  Product awareness              {product/solution/problem/unaware}
  Emotional stage                {pain-active / solution-seeking / etc.}
  Indicateurs                    {sources mining OR signaux site}

[6] Alternative map (hypothèse)
  Solutions essayées avant inférées
    - {alt_1} · pourquoi insuffisant inféré · {reason}
    - {alt_2} · ...
  À valider · verbatims forums/reviews pour confirmer les vraies alternatives essayées

[7] Identity signals (hypothèse · confidence DEFAULT TRÈS faible sans data verbatim)
  Mode de vie inféré   {signals depuis copy + partners}
  Valeurs inférées     {values revendiquées site}
  Références inférées  {cultural_refs depuis ton + casting}
  À valider · mine-voc + scan vernaculaire forums niche

[8] Decision process (hypothèse)
  Path achat inféré    {path}
  Decision makers      {makers · confidence}
  Trigger event inféré {trigger}
  À valider · verbatims "comment as-tu connu" / "qu'est-ce qui t'a fait acheter"

─────────────────────────────────────────────

Close · UNE question macro drill-down

Pour upgrader cette audience de hypothèse {confidence actuelle} à validée terrain ·

A · Lance l'écoute clients (~8-12 min · mining Trustpilot + forums · récupère verbatims réels · upgrade à `moyenne` ou `forte`)
B · Valide intuitivement et continue · downstream porte confidence `{actuelle}` héritée
C · Injecte data existante (reviews exportées, analytics, retours SAV · 1-2 phrases denses)

Mon avis · {reco macro adaptive selon verbatim_density actuelle}.
```

**Hard rules template** ·
- Chaque dimension porte sa confidence par défaut quand pas de mining.
- Anti-pattern · présenter `[2] Problem map · Pain principal · "Je perds mes cheveux"` comme un fait alors que zéro verbatim n'a été récupéré. Toujours signaler "inféré" + indicateurs sources + à valider.
- Anti-pattern · close affirmatif (*"Tu valides en bloc ?"*) → BANNI. Toujours close drill-down macro avec UNE question A/B/C + reco.

## Cross-references

- `docs/system/investigation-posture.md` (v2.54 doctrine canon) · cartographier avant affirmer · confidence chain explicit · audiences comme hypothèses (TRÈS faible par défaut sans mine-voc) · close drill-down macro · opérateur arbitre.
- `docs/system/contextual-intelligence.md` · master doctrine, no orphan output, jargon zéro en surface.
- `docs/system/audience-cartography.md` · doctrinal contract cartography (mère / sous-audiences, 4 movements).
- `docs/doctrine/audience-cartography-framework.md` · 4 questions framework canon Step 0ter.
- `docs/system/confidence-propagation.md` · algèbre cascade confidence cross-skill (audience → angle → brief créa).
- `resources/canon/copy/niveaux-schwartz/*` (sophistication 1-5, awareness stages).
- `resources/schemas/profile.schema.json` v1.3 (`persona_archetype`, `buyer_user_split`, `purchase_driver` derived).
- `resources/canon/copy/creative-formula.md` V3 (8 dimensions canon).
- D#384 multi-product binding (audit S55) sur Schwartz double-stage.
