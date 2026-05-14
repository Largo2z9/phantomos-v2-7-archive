---
name: map-benefits
type: producer
version: "1.0.1"
isolation_scope: brand_only
layer: 2
recommended_model: sonnet
reasoning_pattern: null
operator_facing: true
patch_notes:
  v1.0.0: "v2.58 NEW · D#386 canon S55 mappers atomiques. Sub-skill atomique deep enrichment spec.benefits[] · chain functional → emotional → identity complete + v1.10 NEW fields activés (emotional_signal, latency_min/max, evidence_verbatim). Distinct mine-voc (qui mine verbatims pour anchor evidence_verbatim) ET snapshot-brand (light pass benefits surface). map-benefits structure deep chain compositionnelle canon doctrine compositional-cartography."
  v1.0.1: "v2.61 doctrine consume · consumes: enrichi avec refs docs/doctrine/ NEW v2.60 (pain-benefit-chain). Skill peut consume ces doctrines canon pour informer production sans dépendre schemas exacts."
description: >
  v1.0.1 (v2.61 doctrine consume) · consumes: enrichi avec refs docs/doctrine/ NEW v2.60 (pain-benefit-chain). Skill peut consume ces doctrines canon pour informer production sans dépendre schemas exacts.
  v1.0.0 (v2.58 D#386 NEW) · Sub-skill atomique cartographie deep enrichment des bénéfices produit `spec.benefits[]`. Chain compositionnelle functional → emotional → identity complete + v1.10 NEW fields (emotional_signal text · latency_min/max jours · evidence_verbatim[] anchored quotes). Distinct de mine-voc qui mine les verbatims Layer B · map-benefits structure deep chain et cross-link benefit ↔ mechanism ↔ audience. Distinct snapshot-brand light pass surface · map-benefits drill-down compositionnel. Invocable séparément par l'opérateur (`map-benefits ma-gelule`) ou orchestré par snapshot-brand.
  FR · "map-benefits {product}", "chaine fonctionnel-émotionnel-identitaire", "approfondis les bénéfices", "détaille la chain bénéfices".
  EN · "map benefits", "deep dive benefits chain", "detail benefit chain".
triggers_fr:
  - "map-benefits {product}"
  - "chaine fonctionnel-émotionnel-identitaire"
  - "approfondis les bénéfices"
  - "détaille la chain bénéfices"
  - "drill bénéfices produit"
  - "chain functional emotional identity"
triggers_en:
  - "map benefits"
  - "deep dive benefits chain"
  - "detail benefit chain"
  - "drill product benefits"
  - "functional emotional identity chain"
disambiguates_against:
  snapshot-brand: "snapshot-brand light pass surface (benefit titles + functional layer). map-benefits drill compositionnel deep chain functional → emotional → identity + NEW fields v1.10 (emotional_signal, latency, evidence_verbatim)."
  mine-voc: "mine-voc Layer B mine verbatims clients depuis Reddit/Trustpilot/forums (matière brute). map-benefits CONSUME les outputs mine-voc pour anchor evidence_verbatim[] par benefit. Pas le même verbe · mine-voc collecte, map-benefits structure."
  produce-paid-angles: "produce-paid-angles consume benefits chain pour générer angles ranked avec LIGNAGE. map-benefits est upstream · construit la chain de bénéfices qui alimente angles."
permissions:
  reads: [brand, product, audience]
  writes: [product]
  mode: proposed
  subagent_safe: true
consumes:
  - brands/{slug}/products/{p_slug}/spec.json
  - brands/{slug}/audiences/{a_slug}/profile.json
  - brands/{slug}/voc/*.json (output mine-voc Layer B)
  - resources/canon/copy/heuristiques-persuasion/*.json
  - resources/schemas/spec.schema.json
  - path: docs/doctrine/pain-benefit-chain-doctrine.md
produces_proposals_for:
  - brands/{slug}/products/{p_slug}/spec.json#/benefits
pipeline:
  preconditions:
    - "brand.json existe (brand setup_complete)"
    - "products/{p_slug}/spec.json existe avec spec.benefits[] light pass déjà cartographié (titles + functional layer minimum)"
  postconditions:
    - "spec.benefits[].chain complet functional + emotional + identity pour chaque benefit"
    - "spec.benefits[].emotional_signal + latency_min/max + evidence_verbatim[] enrichis (v1.10 fields)"
    - "spec.benefits[].audience_fit[] mapping derived depuis audiences profile.json"
    - "spec.benefits[] cross-linked avec spec.mechanisms[].triggered_by_specs"
    - "5-sections investigation-posture output operator-facing"
---

## Tone

Posture analyste compositional. L'opérateur veut creuser la chaîne fonctionnelle → émotionnelle → identitaire d'un produit pour nourrir angles + copy. Sortie structurée doctrine compositional-cartography, evidence anchor depuis verbatims sourcés, audience fit derived, gaps explicit.

---

# Skill · map-benefits

Sub-skill atomique de la famille `map-X` (D#386 canon S55). Deep-enrich `spec.benefits[]` après que le light pass existe · structure la chain compositionnelle complete functional → emotional → identity, active les NEW v1.10 fields (emotional_signal, latency_min/max, evidence_verbatim), cross-link benefit ↔ mechanism ↔ audience. Invocable en standalone ou orchestré par snapshot-brand quand le full pipeline tourne.

## Step 0 · DRGFP (preconditions check)

Avant tout drill, scanner prerequisites ·

1. Lookup `brands/{slug}/brand.json` → si absent → bloquer · *"La marque n'est pas configurée. Run setup-brand d'abord."*
2. Lookup `brands/{slug}/products/{p_slug}/spec.json` → si absent ou `spec.benefits[]` vide → bloquer · *"Pas de bénéfices light pass. Run snapshot-brand ou define-specs d'abord."*
3. Lookup `brands/{slug}/audiences/*/profile.json` → noter audiences disponibles pour mapping `audience_fit[]` (Step 5)
4. Lookup `brands/{slug}/voc/` → noter présence verbatims mine-voc Layer B pour anchor `evidence_verbatim[]` (Step 4)
5. Lookup `spec.mechanisms[]` → noter cross-refs `triggered_by_specs` pour Step 6 cross-link

Output state map · {N benefits déjà posés} · {N audiences profile.json dispo} · {voc Layer B dispo · oui/non} · {mechanisms enriched · oui/non}. Surface 1 ligne contextuelle ·

> *Map-benefits sur {product_name}. Light pass · {N benefits} déjà cartographiés. Matière pour drill · audiences {N profile.json} · verbatims VoC {oui/non} · mechanisms {N enriched}.*

## Step 1 · Classifier chain functional / emotional / identity

Pour chaque benefit dans `spec.benefits[]`, classifier les chaînons doctrine `docs/system/compositional-cartography.md` ·

- **Functional** · effet physique observable, mesurable, attribut produit direct · *"je dors mieux", "ma peau est hydratée", "je cours plus vite"*. Layer racine, ancré dans `spec.mechanisms[]`.
- **Emotional** · ressenti subjectif, expérience interne du bénéfice fonctionnel · *"je me sens reposé", "je me sens belle", "je me sens libre"*. Layer médian, dépend du functional pour exister.
- **Identity** · projection self-concept, qui devient l'utilisateur en consommant · *"je suis une bonne mère qui prend soin d'elle", "je suis l'athlète discipliné que j'admire"*. Layer sommet, dépend de emotional pour exister.

**Logique drill** ·

Pour chaque `benefit` dans `spec.benefits[]` ·

1. Lire `benefit` text + `chain[]` existing si présent (souvent juste functional layer rempli)
2. Classifier le layer existing · `level` ∈ `functional | emotional | identity`
3. Compléter les layers manquants par dérivation logique ·
   - Si `functional` seul existe → dériver emotional + identity en cascade
   - Si `emotional` seul → ancrer functional (pourquoi ce ressenti ?) + projeter identity
   - Si `identity` seul → drill back functional + emotional bridge
4. Output `chain[]` complet avec 3 entries ordered functional → emotional → identity ·

```json
"chain": [
  {"level": "functional", "formulation": "Sommeil plus profond et ininterrompu"},
  {"level": "emotional", "formulation": "Je me sens reposé, prête à attaquer la journée"},
  {"level": "identity", "formulation": "Je suis une mère qui prend soin d'elle en priorité"}
]
```

Stage via mutation gate ·

```bash
python3 .skills/write-to-context.py \
  --path "brands/{slug}/products/{p_slug}/spec.json#/benefits/{idx}/chain" \
  --value '[{"level":"functional","formulation":"..."},{"level":"emotional","formulation":"..."},{"level":"identity","formulation":"..."}]' \
  --source agent \
  --confidence 0.7 \
  --mode proposed \
  --reason "map-benefits classify chain compositional cartography canon"
```

**Hard rules chain** · doctrine compositional-cartography canon · functional ancré spec/mechanism (observable) · emotional + identity dérivés logique relation (pas hallucinés). Tagger `_field_types` per layer · `observed` (text light pass) | `derived` (cascade logique).

## Step 2 · Enrichir emotional_signal (v1.10 NEW field)

Cible · `spec.benefits[{idx}].emotional_signal` (text · expression client-side typique du ressenti émotionnel).

**Logique drill** ·

Pour chaque benefit, écrire en 1 phrase l'expression client-side qui matérialise le emotional layer · ce que l'utilisateur dirait à un ami pour décrire son expérience. Pas le copy brand (positionning), pas le bénéfice technique · l'utterance ressentie.

Exemples canoniques ·

- Benefit functional `Sommeil profond` → emotional_signal · *"Je dors enfin d'une traite"*
- Benefit functional `Confiance énergie` → emotional_signal · *"J'ai retrouvé mon mojo du matin"*
- Benefit identity `Mère présente` → emotional_signal · *"Je suis enfin présente avec mes enfants, pas une zombie épuisée"*

**Source priorité** ·

1. Verbatims mine-voc Layer B si dispo · cherche quote anchored qui matche le benefit (emotional_signal = quote condensée 1-line)
2. Sinon dérivation depuis chain.emotional.formulation (paraphrase client-side)
3. Q&A operator si gap critique (declared)

Stage via mutation gate sur `spec.benefits[{idx}].emotional_signal`.

**Hard rules emotional_signal** · 1 phrase, langage client (pas brand copy), source `verbatim` (anchored) > `derived` (paraphrase chain) > `declared` (operator). JAMAIS halluciner sans source.

## Step 3 · Enrichir latency_min / latency_max (v1.10 NEW fields)

Cible · `spec.benefits[{idx}].latency_min` (jours minimum avant effet observable) ET `spec.benefits[{idx}].latency_max` (jours maximum).

**Logique drill** ·

Cross-ref `spec.mechanisms[].time_window` si benefit cross-link via `mechanism.triggered_by_specs` ↔ `benefit` mapping (Step 6).

Enum `time_window` → conversion jours ·

- `immediate` → latency_min 0, latency_max 1
- `7d` → latency_min 5, latency_max 10
- `14d` → latency_min 10, latency_max 20
- `30d` → latency_min 20, latency_max 40
- `60d` → latency_min 45, latency_max 75
- `90d+` → latency_min 75, latency_max 120

Si pas de mechanism cross-link → sources alternatives ·

1. Datasheet founder · délai d'efficacité documenté
2. EFSA validation timing pour suppléments dosés
3. Verbatims mine-voc Layer B · quotes mentionnant "après X semaines"
4. Q&A operator (declared)

Stage via mutation gate.

**Hard rules latency** · cross-ref obligatoire mechanism.time_window si disponible (canon scientifique). JAMAIS inventer délai sans source.

## Step 4 · Attach evidence_verbatim[] (v1.10 NEW field)

Cible · `spec.benefits[{idx}].evidence_verbatim[]` (array quotes clients sourcées qui attestent du bénéfice).

**Logique drill** ·

Cross-ref `brands/{slug}/voc/` outputs mine-voc Layer B · pour chaque benefit, chercher 1-3 verbatims qui mentionnent ce bénéfice spécifique. Structure ·

```json
"evidence_verbatim": [
  {
    "text": "Après 3 semaines je dors d'une traite, c'est incroyable",
    "platform": "Trustpilot",
    "source_url": "https://www.trustpilot.com/reviews/..."
  },
  {
    "text": "Première fois depuis l'accouchement que je me sens reposée le matin",
    "platform": "Reddit r/Mommit",
    "source_url": "https://reddit.com/r/Mommit/..."
  }
]
```

**Source priorité** ·

1. mine-voc Layer B verbatims (gold standard · platform + source_url required)
2. Sources upload (testimonials photos, screenshots reviews)
3. Sites brand (testimonials section PDP scrapé · note source `brand-curated` confidence moyenne, peut être biaisé)
4. Q&A operator si paste manuel verbatims

Stage via mutation gate.

**Hard rules evidence_verbatim** · platform + source_url obligatoires pour chaque entry (traçabilité). JAMAIS inventer quote. Si pas de matière VoC → laisser `[]` vide + flag gap dans Section 3.

## Step 5 · Derive audience_fit[]

Cible · derive `audience_fit[]` (array slugs audiences pour qui ce benefit est primary).

**Logique drill** ·

Pour chaque benefit, cross-ref `brands/{slug}/audiences/*/profile.json` ·

1. Lire chaque `profile.json#/psychology/pain_points[]` + `psychology/benefits[]` per audience
2. Si le benefit produit matche un pain_point résolu OU un benefit prioritaire de l'audience → audience_fit gagne l'audience slug
3. Output array audience slugs ranked par fit strength (audience primary ranking 1 si pain_point top-3 résolu)

```json
"audience_fit": ["maman-postpartum", "femme-active-30-40"]
```

**Note** · audience_fit n'est PAS dans le schema v1.10 strict (à proposer schema bump v1.12 si validation Largo). Pour v1.0.0 map-benefits · stage en sidecar `spec.benefits.extensions.json#/{idx}/audience_fit` OU directement dans `spec.benefits[{idx}].tags[]` avec format `audience:{slug}` (backward compat hack).

Stage via mutation gate (path TBD selon arbitrage schema extension vs tags hack).

**Hard rules audience_fit** · derived from cross-ref pain_points + benefits per audience profile, pas inventé. Si zéro audience fit → ne pas stage (le benefit est generic, pas audience-segmented).

## Step 6 · Cross-link benefit ↔ mechanism triggered_by

Cible · cohérence triangulation benefit ↔ mechanism ↔ spec.

**Logique drill** ·

Pour chaque benefit, identifier quel(s) `spec.mechanisms[]` le déclenchent via `mechanism.triggered_by_specs[]` ↔ `benefit` mapping logique ·

1. Read `spec.mechanisms[]` array (output map-mechanisms si déjà tourné, sinon light pass snapshot)
2. Pour chaque mechanism, cross-ref `mechanism.name` + `mechanism.description` avec benefit text → si causal relation (mechanism produces benefit) → link
3. Optionnel · stage `spec.benefits[{idx}].triggered_by_mechanisms[]` (extension field v1.12 proposal) avec mechanism_ids

Si zéro mechanism enriched · flag gap · "map-mechanisms à lancer pour compléter la triangulation".

**Hard rules cross-link** · relation logique observable (mechanism cause → benefit effect). JAMAIS forcer cross-link si causal chain pas claire. Triangulation cohérente = benefit pointe vers mechanism qui pointe vers spec ingredient/feature.

## Step 7 · Synthesis · 5 sections investigation-posture

**Doctrinal contract** · output structuré 5 sections per `docs/system/investigation-posture.md`. Cartographier avant affirmer · jamais affirmer une hypothèse comme un fait · jamais halluciner verbatim · ouvrir le drill-down opérateur.

### Section 1 · Observé (chain compositionnelle)

> *Observé · drill spec.benefits sur {product_name} ({date}, {durée})*
>
> *Bénéfices chainés · {N benefits} sur 3 layers functional/emotional/identity*
> *  BNF-01 {benefit_name}*
> *    functional · {chain.functional}*
> *    emotional · {chain.emotional} · signal client · "{emotional_signal}"*
> *    identity · {chain.identity}*
> *    latency · {min}-{max} jours · source · {mechanism.time_window | datasheet | operator}*
> *    evidence · {N verbatims sourcés Trustpilot/Reddit/...}*
> *    audience_fit · {liste slugs}*
> *  ... (un bullet par benefit)*
>
> *Ratios chain · functional layer · {N/N} · emotional layer · {N/N} · identity layer · {N/N}*
> *Ratios v1.10 NEW fields · emotional_signal · {N/N} · latency · {N/N} · evidence_verbatim · {N/N}*

### Section 2 · Déduit (cohérence chain)

3-5 hypothèses derived from cross-checks · functional ancré mechanism canon · emotional + identity cohérence cascade · TOP emotional_signal anchor sourcé verbatim · ratio sain functional/emotional/identity équilibré.

> *Déduit · {N} cohérences à valider*
>
> *D1 · Chain cascade cohérente · {N/N} bénéfices ont les 3 layers chainés cascading · confidence forte*
>   À valider · si la formulation identity matche bien l'archetype voix marque dans `brand.json#tone_of_voice`
>
> *D2 · TOP emotional_signal anchored · {N/N} signals sourcés verbatim mine-voc (anchored) vs {N/N} dérivés chain · confidence forte si anchored majority*
>   À valider · si signals dérivés résonnent vraiment client-side ou si verbatim mining additionnel à creuser
>
> *D3 · Ratio functional/emotional/identity sain · {ratio} (ex 100/80/60) · confidence moyenne*
>   À valider · si distribution attendue pour ce type produit (commodity → ratio plat, lifestyle → identity-heavy)

### Section 3 · Inconnu (benefits sans evidence · gaps verbatim)

> *Inconnu · {N} bénéfices sans evidence_verbatim sourcé*
>
> *1. BNF-{xx} {benefit_name} · zéro verbatim VoC matché → mine-voc Layer B nécessaire (Trustpilot + Reddit niche)*
> *2. BNF-{yy} {benefit_name} · latency non sourcée mechanism · cross-ref EFSA ou datasheet founder*
> *3. ... (typiquement 2-5 benefits gap evidence sur drill standard)*

### Section 4 · Leviers (drill-down options · opérateur arbitre)

> *Leviers · {N} axes pour combler les gaps*
>
> *Axe A · Écoute clients Trustpilot + Reddit (lève evidence_verbatim {N benefits})*
> *  → action · "lancer mining verbatims ciblé sur {benefits sans evidence}" (25 min)*
>
> *Axe B · Mapping audiences (lève audience_fit {N benefits})*
> *  → action · "lancer profile-audience pour audiences manquantes, cross-ref pain_points" (30 min)*
>
> *Axe C · Cross-link mechanisms (lève latency + triangulation {N benefits})*
> *  → action · "lancer map-mechanisms pour drill biological target + time_window EFSA" (20 min)*
>
> *Axe D · Validation founder (lève emotional_signal {N benefits})*
> *  → action · "1 question opérateur sur expressions clients typiques · 5 min"*

### Section 5 · Close ouvert (UNE question macro)

> *Bénéfices `{product_name}` chainés sur {N benefits / total}. {ratio chain layers}. {N gaps evidence_verbatim restants}. Sur quoi tu veux qu'on continue · écoute clients pour verbatims, mapping mechanisms pour latency, ou audience fit complete ?*

## Hard rules · doctrine compositional-cartography canon

- **HR1 · Chain canon doctrine** · functional → emotional → identity cascade canon `docs/system/compositional-cartography.md`. JAMAIS inventer un layer sans ancrage cascade (emotional dépend functional, identity dépend emotional).
- **HR2 · Triangulation cross-ref obligatoire** · benefit ↔ mechanism ↔ audience cohérent. Si triangulation incohérente (mechanism qui ne cause pas benefit, audience pour qui pain_point pas résolu) → flag gap, ne pas forcer le cross-link.
- **HR3 · evidence_verbatim sourcing strict** · platform + source_url obligatoires per entry. JAMAIS halluciner quote. Si pas de matière VoC → array vide + flag mining Layer B nécessaire.
- **HR4 · emotional_signal langage client** · 1 phrase utterance ressentie, pas copy brand, pas bénéfice technique. Source priorité verbatim anchored > dérivation chain > declared operator.
- **HR5 · latency cross-ref mechanism.time_window** · si mechanism enrichi avec time_window enum (immediate, 7d, 14d, 30d, 60d, 90d+) → convertir en latency_min/max jours selon table canon. Si pas de mechanism cross-link → source EFSA / datasheet / operator declared.
- **HR6 · audience_fit derived** · derived from cross-ref audience pain_points + benefits matching. Pas inventé. Si zéro audience match → benefit generic, pas audience-segmented.
- **HR7 · Backward compat strict** · benefits existing chain layers ne sont PAS écrasés sauf validation operator. map-benefits ajoute layers manquants + active v1.10 NEW fields, ne réécrit pas silencieusement existing.
- **HR8 · Operator-facing rule** · JAMAIS exposer `_field_types`, `confidence` numerique, paths internes. Traduire en `observé / déduit / déclaré / incertain` si utile.
- **HR9 · Zéro em-dash** · `·`, `(,)`, `(.)`, `:` substituent partout.

## Anti-patterns à refuser

- AP-1 · Halluciner identity layer sans cascade depuis emotional (HR1 violation, compositional doctrine)
- AP-2 · Forcer cross-link benefit ↔ mechanism quand chain causale pas claire (HR2 violation)
- AP-3 · Inventer verbatim evidence "client typique pourrait dire X" sans platform + source_url (HR3 violation)
- AP-4 · Copy brand recyclé comme emotional_signal au lieu de langage client (HR4 violation)
- AP-5 · Latency arbitraire sans source mechanism/EFSA/datasheet/operator (HR5 violation)
- AP-6 · Stage audience_fit avec audiences hors profile.json scope brand (HR6 violation, fabrication)
- AP-7 · Écraser silencieusement chain existing sans operator validate (HR7 violation)
- AP-8 · Output prose narrative mélangeant Observé + Déduit comme assertions confiantes (5-sections doctrine canon violation)

## Cross-refs

- Schema target · `resources/schemas/spec.schema.json#/benefits` (v1.10 fields emotional_signal, latency_min/max, evidence_verbatim activés)
- Doctrine investigation · `docs/system/investigation-posture.md`
- Doctrine compositional cartography (chain canon functional/emotional/identity) · `docs/system/compositional-cartography.md`
- Doctrine production · `docs/system/canonical-matrix-reasoning.md`
- Doctrine substrate · `docs/system/schema-encoding-discipline.md`
- Canon refs psychology · `resources/canon/copy/heuristiques-persuasion/*.json`
- Canon refs niveaux conscience · `resources/canon/copy/niveaux-schwartz/*.json` (pour cross-ref identity layer avec Schwartz 5 stages)
- Sub-skill mine-voc (verbatims Layer B) · `.skills/skills/mine-voc/SKILL.md`
- Sub-skill profile-audience (audience pain_points + benefits pour audience_fit) · `.skills/skills/profile-audience/SKILL.md`
- Sub-skill map-mechanisms futur (cross-link benefit ↔ mechanism) · à venir
- Mutation gate · `write_to_context` (JAMAIS Edit/Write direct sur `.json`)
- Validation post-write · `validate-resources` (silent, flag MAJOR/CRITICAL)
- Sibling map-skills · `map-specs`, `map-mechanisms` (futur), `map-audiences` (futur), `map-angles` (futur)
- Orchestrateur · `snapshot-brand` (full pipeline brand cartographique appelle map-X en séquence)
- Downstream consumer · `produce-paid-angles` (consume benefits chain pour LIGNAGE)
- Downstream consumer · `produce-copy-brief` (consume benefits chain + evidence_verbatim pour sections proof)

## D#386 lineage

D#386 (2026-05-04, S55) · Architecture cartographie marketing · `snapshot-brand` orchestrateur + sub-skills `map-X` invocables séparément. Pattern Largo · *"snapshot lui donner la capacité d'appeler des sub-agents qui pourront être utilisés ponctuellement plus tard par l'utilisateur"*. map-benefits = extraction de logique snapshot-brand benefits section + drill compositionnel chain functional → emotional → identity + activation v1.10 NEW fields (emotional_signal, latency_min/max, evidence_verbatim). Distinct snapshot light pass (titles + functional surface) · map-benefits deep compositional cartography canon + triangulation cross-ref audience + mechanism. v1.10 NEW fields actifs (alignement v2.56 Notion stride-up parity).
