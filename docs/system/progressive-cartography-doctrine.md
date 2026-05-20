# Progressive Cartography Doctrine · Operating Doctrine

> Canonique v2.68+. Codifie le phasing progressif du territoire posage par niveaux de profondeur, avec validations light entre paliers et enrichissement continu non-bloquant. Doctrine sœur de Territory Doctrine (TD v2.67), Investigation Posture (IP), Compositional Cartography (CC), Schema Encoding Doctrine (SED), Scope Extension Doctrine (SED-X), Canonical Matrix Reasoning (CMR), Contextual Intelligence (CI). Évite anti-pattern "dump synthesis d'un bloc" + "Q&A questions premature" canon CI.

---

## 1. Thesis

> Le territoire se pose progressivement par niveaux de profondeur, avec validations light (gates 1-2 secondes binaires) entre chaque palier, et enrichissement continu non-bloquant en background.

Quatre phases ordonnées · **Phase 1 Macro confirmation light** (scrape produit + offer + brand identity high-level · synthesis 3-5 lignes · 2 min wall) · **Phase 2 Drilling autonome** (PDP details + reviews verbatims tagged + offers detail + funnel signals · synthesis 5 sections investigation-posture · 5-10 min wall) · **Phase 3 Cartographie audiences hiérarchique** (arbre parent/enfants · confidence chain par audience · 15-20 min wall) · **Phase 4 Enrichissement continu non-bloquant** (mode listening passive · opérateur drop insight first-party à tout moment · agent stage proposed automatique · cartographie en background).

Entre chaque phase · **gate light** · 1-2 secondes confirmation binaire opérateur. Jamais Q&A verbeux multi-questions. Template canon · *"Phase X done. Voici ce que j'ai trouvé · {synthesis 3-5 lignes}. Tu valides ou tu corriges ?"*.

Pour opérateur expert (≥3 brands setup OR config explicit) · **mode skip / fast-track** auto-validation par défaut, gates surface seulement si ambiguïté détectée.

Ce contrat est cassé si ·
1. Skill territoire dump Phase 1+2+3+4 synthesis d'un bloc sans gates intermédiaires (saturation opérateur)
2. Skill pose Q&A questions opérateur avant ou après scrape sans avoir drill-down autonome (violation CI "No questionnaire before action")
3. Gate verbeux multi-questions au lieu de 1 binaire light (anti-friction)
4. Skill Phase 4 enrichissement bloque flow principal en attente insight opérateur (violation non-bloquant)
5. Fast-track default activé pour première fois opérateur (violation onboarding · perd repère)

Progressive Cartography Doctrine codifie phasing 1-4 + gates light + fast-track opt-in + enforcement runtime via decision-aid skill authors.

---

## 2. Le problème Progressive Cartography Doctrine résout

Avant doctrine ·

1. **Dump synthesis d'un bloc canon actuel.** `snapshot-brand v1.3.1` Step 7 dump synthesis 5 sections investigation-posture (Observé · Déduit · Inconnu · Leviers · Close ouvert) d'un coup, post-scrape complet. Saturation opérateur · pas de validation à grain fin. Si base produit/offre wrong, opérateur doit tout corriger en bulk sans avoir pu corriger tôt. Cause root · pas de phasing progressif avec gates intermédiaires.

2. **Q&A questions audience post-scrape premature.** `snapshot-brand v1.3.1` Step 7 pose 4 Q&A questions cartographie audiences post-scrape (typologie, hiérarchie, pondération, drill-down). Anti-pattern · agent doit drill-down autonome puis présenter hypothèses confidence chain, opérateur valide en bulk. Violation CI "No questionnaire before action" master doctrine.

3. **Pattern réel d'usage opérateur non codifié.** Observation empirique pilots (Stride-Up · we-bet · etc.) · opérateur valide naturellement par paliers (macro produit OK → on drill PDP → audiences arbre OK → enrichissement continu). Pattern existait dans usage mais pas dans canon doctrinal. Skill authors freestyle dump synthesis sans hiérarchie palier.

4. **Pas de gate light canon.** Skills territoire mélangent gates light (binaire validation) avec Q&A questions verbeux (4 ouvertes). Aucune doctrine canon distinguant les deux patterns. Confusion mental model skill author.

5. **Enrichissement first-party bloquant.** Opérateur veut drop insight à tout moment ("ajoute friction X · nos clients Y ont objection Z") sans bloquer flow principal. Canon actuel mute substrat directement violation mutation gate OR bloque flow en attente confirmation. Pas de pattern "agent listening passive · stage proposed automatique".

6. **Fast-track multi-brand agency manquant.** Opérateur agency multi-brand (≥3 brands setup) refait gates Phase 1-3 à chaque onboard. Friction inutile · opérateur expert connaît le pattern. Pas de mode skip canon.

Progressive Cartography Doctrine = doctrine canon qui ferme ces gaps.

---

## 3. Phase 1 · Macro confirmation light

**Scope.** Scrape produit + offer + brand identity high-level. Pas de drill PDP details, pas de reviews mining, pas de funnel signals deep.

**Indicateurs canon** ·
- Nom brand + tagline + positioning 1-liner
- Catégorie produit principal (active offer)
- Offer mécanique top-level (subscription · one-shot · bundle)
- Tone voice high-level (premium · accessible · expert · etc.)
- Audience apparente high-level (B2C · B2B · niche · mass)

**Output template canon** ·

```
Voici ce que j'ai compris de ton produit · offre · positionning ·

- Produit · {nom + catégorie + mécanique 1-liner}
- Offre · {pricing model + value prop top-level}
- Positionning · {tagline + différenciation high-level}
- Audience apparente · {profil top-level}
- Tone · {3 adjectifs}

Tu valides ou tu corriges quelque chose ?
```

**Durée cible** · 2 min wall (scrape + synthesis).

**Validation operator** · bulk corrige/confirme. Pas de drill-down forcé. Opérateur peut juste dire *"OK"* OR *"corrige le tone, c'est plutôt premium qu'accessible"*.

**Gate light Phase 1 → Phase 2** · *"On creuse Phase 2 (PDP details + reviews + offers + funnel) ?"*

**Anti-pattern Phase 1** · dump 5 sections investigation-posture, Q&A questions audience, drill PDP. Phase 1 = high-level macro uniquement.

---

## 4. Phase 2 · Drilling autonome

**Scope.** PDP details + reviews verbatims tagged + offers detail + funnel signals + trust badges + cross-sells.

**Drill-down strategies canon** ·
- Reviews scrape (Trustpilot · Judge.me · Loox · Yotpo) · verbatims tagged par pain/benefit/objection
- FAQ scrape · objections identifiées
- Cross-sells + bundles · mécaniques offer
- Trust badges + social proof · positionning credibility
- Funnel signals · landing page structure · CTAs · pop-ups · exit-intents
- Pricing tier comparison · si multiple offers

**Output synthesis 5 sections investigation-posture** (canon `investigation-posture.md`) ·

```
## Observé (faits sourcés)
- {fait 1 + source URL}
- {fait 2 + source URL}
- ...

## Déduit (hypothèses confidence chain)
- {hypothèse 1} · forte / moyenne / faible / TRÈS faible
- {hypothèse 2} · ...

## Inconnu
- {variable non observable 1}
- {variable non observable 2}

## Leviers
- {skill / action / source 1 pour lever inconnue}
- ...

## Close ouvert
{UNE question macro · opérateur arbitre où creuser}
```

**Durée cible** · 5-10 min wall (drill + synthesis).

**Validation operator** · bulk corrige/confirme. Opérateur peut drill un point spécifique s'il veut (*"creuse le funnel exit-intent"*) ou juste valider bulk.

**Gate light Phase 2 → Phase 3** · *"On attaque Phase 3 audiences hiérarchique ?"*

**Anti-pattern Phase 2** · skip Phase 1 validation, dump Phase 3 audiences arbre directement, Q&A questions premature avant drill-down autonome.

---

## 5. Phase 3 · Cartographie audiences hiérarchique parent/enfants

**Scope.** Agent propose arbre N audiences PARENT (mères) + sous-audiences ENFANTS (sous-poches) en arbre canonique. Pattern reference `map-audiences` canon 3 niveaux (broad / segment / micro) + 4 questions framework canon (Pour qui · Contre quoi · Pourquoi maintenant · Pourquoi nous).

**Confidence chain par audience.** Chaque audience proposée porte confidence (forte / moyenne / faible / TRÈS faible) sourcée par signaux observés (reviews verbatims tagged · funnel signals · positionning brand).

**Output structuré arbre canon (ASCII art OR table)** ·

```
Audience MÈRE 1 · {nom} (confidence forte · sourcée reviews + positionning)
├── Sous-poche 1.1 · {nom} (confidence moyenne · sourcée FAQ + verbatims)
├── Sous-poche 1.2 · {nom} (confidence faible · hypothèse drill-down requis)
└── Sous-poche 1.3 · {nom} (confidence TRÈS faible · spéculation)

Audience MÈRE 2 · {nom} (confidence forte)
├── Sous-poche 2.1 · {nom} (confidence moyenne)
└── Sous-poche 2.2 · {nom} (confidence faible)
```

OR format table équivalent (mère + sous-poches + confidence + sourcing).

**Durée cible** · 15-20 min wall (cartographie + arbre + confidence chain).

**Validation operator** · bulk drop/add. *"Drop sous-poche 1.3 · ajoute MÈRE 3 segment {X}"*. Pas de Q&A questions ouvertes.

**Gate light Phase 3 → Phase 4** · *"On enrichit Phase 4 continu (drop insights first-party à tout moment) ?"*

**Anti-pattern Phase 3** · audiences flat list sans hiérarchie, confidence chain manquante, Q&A questions framework ouvertes pré-arbre.

---

## 6. Phase 4 · Enrichissement continu non-bloquant

**Scope.** Mode "agent listening passive". Opérateur drop insight first-party à tout moment (*"ajoute friction X"* · *"nos clients Y ont objection Z"* · *"on a observé que tier premium veut bénéfice W"*). Agent stage proposed automatique via mutation gate canon (mode `proposed`). Cartographie en background sans interrompre flow principal.

**Patterns triggers Phase 4** ·
- Opérateur prononce *"ajoute"* · *"nos clients"* · *"j'ai observé"* · *"on a remarqué"* · *"y'a aussi"*
- Agent détecte insight first-party non encore en substrat
- Agent stage proposed via `write_to_context(field_path, value, source="operator_stated", confidence=0.95, mode="proposed")`
- Visible via `brands/{slug}/pending-validations.md` pour review batch ultérieure

**Pattern non-bloquant** ·
- Pas de validation operator requise immédiate
- Pas d'interruption flow principal
- Agent continue tâche en cours (brief · creative · audit · etc.) pendant absorption insight
- Confirmation 1-liner discrète post-stage *"Noté · audience X enrichie friction Y, à valider en batch"*

**Durée** · open-ended. Continu cross-sessions. Pas de wall time cap.

**Validation operator** · différée. Batch review via `pending-validations.md` ultérieurement. Opérateur peut valider en bulk *"valide tout"* OR drop un par un.

**Anti-pattern Phase 4** · agent bloque flow principal en attente confirmation, mute substrat directement sans mutation gate, surface validation immédiate forcée operator, Q&A questions sur insight drop ("Pour quelle audience ? Quel niveau ?").

---

## 7. Mode skip / fast-track

**Trigger fast-track auto** ·
- Opérateur ≥3 brands setup complet (compté via `operator/profile.json#stats.brands_setup_count`)
- OR explicit flag `--fast-track` au lancement skill
- OR config `/operator/profile.json#preferences.auto_validate_after_n_brands: true`

**Comportement fast-track** ·
- Phases 1-3 auto-validation par défaut (agent skip gates light)
- Synthesis présentée en bulk final post-Phase 3 (toutes phases agrégées)
- Gates surface uniquement si ambiguïté détectée (confidence faible OR inconsistance OR contradiction signaux)

**Anti-friction opérateur agency multi-brand.** Pattern observé · opérateur expert connaît le flow, gates Phase 1-3 ajoutent friction inutile à chaque onboard nouveau brand. Fast-track libère cycle.

**Anti-pattern fast-track default** · activer fast-track pour première fois opérateur. Onboarding violation · opérateur perd repère, ne sait pas où il en est, ne comprend pas le phasing. Fast-track = **opt-in opérateur expert uniquement** (config OR flag · jamais default).

**Phase 4 jamais fast-track** · enrichissement continu non-bloquant reste actif par construction. Pas de skip applicable.

---

## 8. Pattern gates light

**Pattern canon.** 1-2 secondes confirmation binaire opérateur entre phases. Jamais Q&A verbeux multi-questions.

**Template canon strict** ·

```
Phase X · {nom} done. Voici ce que j'ai trouvé · {synthesis 3-5 lignes}.

Tu valides ou tu corriges quelque chose ?
```

Pas plus. Si opérateur veut drill un point spécifique, il le dit (*"creuse le funnel exit-intent"*). Pas via 4 questions ouvertes pré-fabriquées.

**Variantes acceptées** ·
- *"OK / on continue"* → opérateur valide bulk, agent passe Phase suivante
- *"Corrige X"* → agent ajuste, re-présente synthesis raffinée, re-gate
- *"Drill Y"* → agent fait drill spécifique sur point demandé, présente raffinement, re-gate
- *"Skip"* → opérateur fast-track manuel sur cette phase, agent enchaîne sans gate suivante

**Anti-patterns gates** ·
- Gate qui demande 4 questions opérateur (*"Quelle typologie ? Quelle hiérarchie ? Quelle pondération ? Quel drill-down ?"*) au lieu de 1 binaire light
- Gate ouvert *"Qu'est-ce que tu en penses ?"* (non actionnable · operator doit faire l'effort de structurer feedback)
- Gate omis (skip Phase 1 → Phase 2 sans confirmation · violation phasing)

---

## 9. Skills implémentation actuelle

Mapping skills canon → phases progressive cartography ·

| Skill | Phase couverte | Version cible |
|---|---|---|
| `snapshot-brand` | Phases 1+2 (macro + drilling) | v1.4.0+ patch v2.68 |
| `map-audiences` | Phase 3 (hiérarchique parent/enfants déjà canon · 3 niveaux mère + sous-poches · 4 questions framework canon) | v1.2.0+ existing canon |
| `mine-voc` + `mine-vom` + `profile-audience` | Phase 4 (enrichissement par audience · verbatims · objections) | v1.0+ existing |
| `build-atlas-complete` | Orchestre Phases 1-4 avec gates light | v1.4.0+ patch v2.68 |
| NEW candidate `enrich-territory` mode passive listening | Phase 4 spécifique drop insights first-party | v2.68+ skill stub |
| OR extension `scaffold-extension` intent-mode absorber insights | Phase 4 alternative implementation | v2.68+ extension |

**Patches v2.68+ requis** ·
- `snapshot-brand v1.4.0` · split Step 7 dump en Phases 1+2 avec gates light, supprimer 4 Q&A questions audience post-scrape (Phase 3 délégué `map-audiences`)
- `build-atlas-complete v1.4.0` · orchestrer Phase 1 (snapshot-brand macro) → gate → Phase 2 (snapshot-brand drilling) → gate → Phase 3 (map-audiences hiérarchique) → gate → Phase 4 (listening passive)
- NEW skill `enrich-territory` OR extension `scaffold-extension` · mode passive listening capture insights first-party Phase 4

---

## 10. Anti-patterns canonisés

### Anti-pattern 1 · Q&A questions premature

Agent pose 3-4 questions avant scrape OR post-scrape sans avoir drill-down autonome. Exemple canon actuel `snapshot-brand v1.3.1` Step 7 · 4 Q&A questions audience (typologie · hiérarchie · pondération · drill-down) post-scrape sans avoir proposé arbre confidence chain.

**Violation** · CI master doctrine "No questionnaire before action".

**Pattern canon** · agent drill-down autonome puis présente hypothèses confidence chain · opérateur valide en bulk. Questions à l'opérateur uniquement si ambiguïté irréductible non résolvable par drill.

### Anti-pattern 2 · Dump synthesis d'un bloc

Skill dump Phase 1+2+3+4 synthesis d'un coup post-scrape complet. Saturation opérateur · pas de validation à grain fin · si la base produit/offre est wrong, l'opérateur doit tout corriger en bulk sans avoir pu corriger tôt.

**Violation** · Progressive Cartography Doctrine thesis Section 1.

**Pattern canon** · phasing 1-4 avec gates light intermédiaires. Validation grain fin permet correction précoce, évite re-cartographie complète sur base wrong.

### Anti-pattern 3 · Gates verbeux multi-questions

Gate qui demande 4 questions opérateur au lieu de 1 binaire light. Exemple · *"Quelle typologie ? Quelle hiérarchie ? Quelle pondération ? Quel drill-down ?"*.

**Violation** · anti-friction Section 8.

**Pattern canon** · 1-2 secondes confirmation binaire opérateur. Template *"Tu valides ou tu corriges quelque chose ?"*. Opérateur drill point spécifique s'il veut, sur initiative propre.

### Anti-pattern 4 · Enrichissement bloquant

Agent attend opérateur insight avant continuer flow principal. Exemple · opérateur drop *"ajoute friction X"* mid-flow brief, agent bloque sur Q&A questions ("Pour quelle audience ? Quel niveau ?") au lieu de stage proposed automatique.

**Violation** · Phase 4 canon non-bloquant Section 6.

**Pattern canon** · agent stage proposed automatique via mutation gate, confirmation 1-liner discrète, continue flow principal. Validation différée batch via `pending-validations.md`.

### Anti-pattern 5 · Fast-track default

Agent skip gates pour tout opérateur. Première fois opérateur perd repère, ne sait pas où il en est, ne comprend pas le phasing.

**Violation** · onboarding Section 7.

**Pattern canon** · fast-track = opt-in opérateur expert uniquement. Trigger explicite (≥3 brands setup OR `--fast-track` flag OR config). Default = gates Phase 1-3 actives.

---

## 11. Decision-aid Q1-Q4 pour skill authors

Avant d'ajouter NEW skill territoire OR refactor existing, applique ce decision-aid ·

```
Q1 · Skill produit synthesis territoire (snapshot · drill · audiences · enrichissement) ?
   OUI → respecter phasing 1-4 progressive
        - Phase 1 macro confirmation light ?
        - Phase 2 drilling autonome ?
        - Phase 3 cartographie audiences hiérarchique ?
        - Phase 4 enrichissement continu non-bloquant ?
        OR documenter raison contraire (cas exceptionnel · justification canon)
   NON → Q2

Q2 · Skill pose des questions opérateur ?
   OUI → vérifier qu'agent ne peut PAS drill-down autonome avant
        - Drill possible via scrape ? → banni Q&A premature, faire drill puis synthesis
        - Drill impossible (ambiguïté irréductible) ? → 1 question max, binaire light
   NON → Q3

Q3 · Skill chain plusieurs sub-skills territoire (orchestrator) ?
   OUI → inserter gates light entre paliers
        - Gate Phase 1 → Phase 2 ?
        - Gate Phase 2 → Phase 3 ?
        - Gate Phase 3 → Phase 4 ?
        - Fast-track trigger respecté (config OR flag) ?
   NON → Q4

Q4 · Skill mode enrichissement Phase 4 (capture insights first-party) ?
   OUI → pattern non-bloquant
        - Stage proposed automatique via mutation gate ?
        - Pas d'attente confirmation operator immédiate ?
        - Validation différée batch via pending-validations.md ?
        - Confirmation 1-liner discrète post-stage ?
   NON → flag à doctrine maintainers pour évaluation (cas non couvert · candidat sprint dédié)
```

**Tie-breaker overlap.** Si Q1-Q3 ambiguous (e.g. skill `produce-paid-angles` chain audiences + angles mais ne fait pas Phase 1 macro) → règle `phasing applicable` prime · skill chain partial = appliquer phasing aux phases couvertes uniquement. Pas forcé tout 1-4 si scope skill restreint.

---

## Position dans le système opérationnel 5 couches

Progressive cartography opère sur 2 couches du système opérationnel (cf
`operational-system-doctrine.md`) · couche 5 (rituels · cadence par
phases avec gates light entre paliers) · couche 2 (règles · gates light
binaire valide/corrige sont des heuristiques de décision canon).

Le phasing 4 phases (Macro · Drilling · Audiences hiérarchique ·
Enrichissement continu) est le rituel canon d'encodage d'un nouveau brand
dans PhantomOS.

---

## 12. Cross-references

- `territory-doctrine.md` (TD v2.67) · sister doctrine · territoire vs production vs meta layers · base distinction layer territoire qui se pose progressivement
- `investigation-posture.md` (IP) · 5 sections close synthesis canon pattern · Phase 2 drilling output canon strict
- `compositional-cartography.md` (CC) · cycle produce → test → learn → promote · pattern référence cycle Phase 4 enrichissement validé → substrat
- `schema-encoding-doctrine.md` (SED) §3 · Spatial vs Temporal encoding · territoire = spatial · phasing progressif pose spatial layer
- `scope-extension-doctrine.md` (SED-X v2.65) · sister doctrine pattern miroir 13 sections canon-style · pattern reproductible
- `canonical-matrix-reasoning.md` (CMR) · 95% quality intersectional outputs · production layer canon · Phase 1-3 territoire feed CMR production downstream
- `contextual-intelligence.md` (CI) · master doctrine · "No questionnaire before action" anti-pattern · CI master rule enforced par phasing progressif (drill avant questions)
- `skill-authoring-doctrine.md` (SAD) · skill type taxonomy · frontmatter triad · phasing aware skills patches v2.68+
- `doctrine-governance.md` · amendment process append-only D# verrouillé

**Skill authors patches v2.68+ candidates** ·
- `snapshot-brand v1.4.0` · split Step 7 dump en Phases 1+2 avec gates light · supprimer 4 Q&A questions audience post-scrape · délégation Phase 3 à `map-audiences`
- `build-atlas-complete v1.4.0` · orchestrer Phases 1-4 avec gates light · fast-track trigger respecté
- NEW skill `enrich-territory` mode passive listening OR extension `scaffold-extension` intent-mode · Phase 4 capture insights first-party
- `map-audiences` v1.2.0+ existing canon · Phase 3 déjà conforme (3 niveaux hiérarchique · 4 questions framework canon) · pas de patch requis

---

## 13. Status

- **Canonique v2.68+.** Codifie le pattern phasing progressif territoire posage. Doctrine sœur TD v2.67 · IP · CC · SED · SED-X · CMR · CI.
- **First applications** · `snapshot-brand v1.4.0` patch (split Step 7 · supprimer Q&A premature) · `build-atlas-complete v1.4.0` orchestrer phases avec gates · NEW skill `enrich-territory` candidate Phase 4 listening passive.
- **Backward compat** · strict additif · doctrine NEW n'override aucune existing. Skills pré-v2.68 sans phasing flag à patcher (sprint dédié migration). Aucun break runtime.
- **Promotion criterion** · à reviewer après 3+ skills shipped avec phasing canon (validate-output-coherence enforcement v2.70 candidate).
- **Pattern reproductible cross sessions opérateur** · onboard nouveau brand (gates Phase 1-3 actives) OR enrichissement brand mature (Phase 4 listening passive continu).

---

*Doctrine canonique skill-author-facing et opérateur-facing pédagogique (Sections 7-8 accessibles). Codifie phasing progressif territoire posage avec gates light + fast-track + Phase 4 non-bloquant. Pattern miroir TD 13 sections canon-style. Enforce decision-aid skill authors Q1-Q4 patches v2.68+.*
