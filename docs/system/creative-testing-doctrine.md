# Creative Testing Discipline · Operating Doctrine

> Canonique v2.78+. Doctrine canon qui codifie le protocole creative testing (3x3 matrix · win/kill seuils chiffrés · refresh cadence) au-delà du *"polish 1 angle"* ou *"test 50 variants random"*. Doctrine sœur de `pacing-doctrine.md` (axe 4 CTR decay · refresh cadence 21j) et `attribution-multitouch-doctrine.md` (cadrage mesure post-test). Ferme le gap *"creative testing framework canon manquant"* flag P0 Sprint v2.78 Agent media buyer. Substrat consommé par `produce-paid-angles` (génération variants) · `compose-creative` (composition variants) · `creative-brief-composer` (brief test plan) · `analyze-perf` (diagnostic win/kill) · `routine-perf` (monitoring tests).

---

## 1. Thèse fondatrice

> Creative testing est protocole, pas instinct. 3x3 matrix canon + win/kill seuils chiffrés = test plan reproductible cross-account, refresh cadence 21j sweet spot.

**Définition creative testing canon** · ensemble structuré de variants creative déployés simultanément ou séquentiellement, mesurés contre seuils chiffrés canon win/kill, pour identifier le top-performer ROAS-validated avant scaling spend. Creative testing répond à 4 questions canon ·

1. *"Quel angle/hook/visual marche ?"* (axe 1 · matrix 3x3 variants)
2. *"Quand kill un loser ?"* (axe 2 · kill seuils chiffrés)
3. *"Quand reinforce un winner ?"* (axe 3 · win seuils chiffrés)
4. *"Quand refresh le pool ?"* (axe 4 · refresh cadence 21j)

**Différenciation canon vs gut feeling** ·

| Layer | Polish 1 angle | Test 50 random | Creative Testing Discipline canon |
|---|---|---|---|
| Diversification | absent · 1 angle hyper-poli | over · 50 variants noise | structuré · 3x3 matrix 27 variants MECE |
| Win/kill seuils | subjectifs · gut feeling | absent · vibes only | chiffrés canon ROAS×spend×days |
| Refresh cadence | jamais · creative use until death | tous les 7j panic mode | 21j sweet spot canon stage-aware |
| Stage alignment | absent · même action toutes stages | absent · over-test scale | stage canon test wide · scale focus winners |
| Audit trail | absent · pas extractible | absent · noise non-traçable | learnings.json append-only · validation_status |

Creative Testing Discipline n'est pas une checklist. C'est la grammaire structurée qui transforme variant testing chaotique en protocole reproductible avec audit trail.

---

## 2. Le problème résolu

Sans Creative Testing Discipline canon ·

1. **Over-test polish 1 angle.** Buyer s'attache à 1 angle gagnant historique · polish 10 variants visuels de ce même angle · diversification absente · audience saturation rapide · ROAS dégrade silencieusement.

2. **Under-test diversification.** Buyer test 50 variants random sans structure · noise pipeline · pas de canon win/kill · output dispersé · pas extractible learnings.

3. **Pas canon shared cross-buyer.** Chaque buyer applique son protocole. Compte transféré · drift methodology · output multi-buyer impossible sans canon.

4. **Skills produce-paid-angles + compose-creative + creative-brief-composer sans substrat doctrinal.** Skills production ship variants mais sans canon partagé doctrinal · chaque skill ré-invente test matrix dans frontmatter · drift maintenance dette.

5. **Win/kill seuils gut feeling.** *"ROAS pas top, je kill"* (à quel ROAS ? après combien de spend ? après combien de jours ?). Sans canon chiffré · kill trop tôt (learning incomplet) OR kill trop tard (waste budget).

6. **Refresh cadence ad-hoc.** Refresh à 7j panic mode OR jamais (until death). Pas de canon 21j sweet spot · waste budget OR audience saturation cumulative.

Creative Testing Discipline = doctrine canon qui ferme ces 6 gaps via 3x3 matrix + win/kill chiffrés + refresh cadence canon + stage alignment.

---

## 3. Le principe canon · 3x3 testing matrix

Pattern canon · 3 axes × 3 variants = 27 variants test matrix MECE. Deux configurations canon selon stage ·

### Configuration A · angle × hook × visual (early stage validation)

3 angles différents × 3 hooks différents × 3 visuals différents = **27 variants**.

Usage canon · audience NEW non-validée. Diversification large pour identifier signal angle gagnant.

Matrix exemple ·

| Angle | Hook 1 | Hook 2 | Hook 3 |
|---|---|---|---|
| A1 (pain functional) | Visual 1 · Visual 2 · Visual 3 | Visual 1 · Visual 2 · Visual 3 | Visual 1 · Visual 2 · Visual 3 |
| A2 (pain identity) | idem 9 cellules | idem | idem |
| A3 (pain emotional) | idem | idem | idem |

### Configuration B · angle × audience × visual (post-validation scale)

3 angles validés × 3 audiences segments × 3 visuals = **27 variants**.

Usage canon · angle gagnant identifié early stage · scale stage diversification audience. Test combien d'audiences l'angle scale.

Matrix exemple ·

| Angle validé | Audience seg 1 | Audience seg 2 | Audience seg 3 |
|---|---|---|---|
| A1 (winner) | Visual 1 · 2 · 3 | Visual 1 · 2 · 3 | Visual 1 · 2 · 3 |
| A2 (challenger) | idem | idem | idem |
| A3 (control) | idem | idem | idem |

### Cardinality cap canon

27 variants max par test batch. Au-delà · noise pipeline · cap dur doctrine. Sous 9 variants · cap insuffisant · pas de signal statistique fiable.

### MECE check canon

3 angles MECE (pain functional × pain identity × pain emotional · cf `pain-benefit-chain.md`). 3 hooks MECE (problem-led × benefit-led × identity-led · cf `hook-registry`). 3 visuals MECE (lifestyle × demo product × UGC · cf `creative-mechanics-registry`).

Anti-pattern · 3 variants du même angle (pas MECE · drift output). Pattern canon · variant axe = orthogonal aux 2 autres axes.

---

## 4. Seuils win/kill chiffrés canon · table

Pattern canon win/kill seuils ROAS × spend × days ·

| Condition | Seuil ROAS | Seuil spend | Seuil days | Action canon |
|---|---|---|---|---|
| **Win** | ≥ breakeven × 1.2 | ≥ 3× CPM | ≥ 7 jours | reinforce · scale spend 1.5x |
| **Watch** | breakeven × 0.9 - 1.2 | ≥ 2× CPM | ≥ 5 jours | maintain · monitor 48-72h |
| **Kill** | < breakeven × 0.7 | ≥ 1× CPM | ≥ 3 jours | kill variant · re-allocate budget |

**Lecture canon** · les 3 seuils (ROAS · spend · days) doivent être respectés simultanément AVANT action. Kill prématuré (spend < 1× CPM OR days < 3) · learning insuffisant · décision biaisée. Win prématuré (spend < 3× CPM OR days < 7) · over-confidence · scale sur signal noise.

**Breakeven canon** · ROAS minimum couvrir coût + marge. Calculé par brand · stocké `brand.json#financials.breakeven_roas`.

**CPM canon** · moyenne 30 jours de l'account. Stocké `_snapshot.md` ou recalculé runtime.

**Pattern canon spend velocity stage** ·

- Stage test · 80% spend daily allocation reinforce winners post-test · 20% nouveaux tests
- Stage scale · 90% reinforce winners · 10% defensive tests
- Stage saturation · re-test mandatory · 50% winners · 50% nouveaux angles

---

## 5. Refresh cadence canon · 21j sweet spot

**Rationale 21j sweet spot canon** ·

- < 14j · learning phase non finie · refresh waste partial signal · over-test
- 14j · minimum acceptable · creative-fatigue signal warning canon (cf `pacing-doctrine.md` axe 4)
- 21j · sweet spot canon · audience seen creative ~2.5 fois · CTR decay -20-25% · refresh optimal avant CTR effondré
- 30j · max acceptable · CTR decay -40% canon critical · refresh mandatory · auction punit
- > 30j · creative dead · CPM auction blow up · waste budget continu

**Stage alignment refresh** ·

| Stage | Cadence canon | Rationale |
|---|---|---|
| test | 14-21j minimum stricte | learning incomplet sous 14j · over-test sur 21j+ |
| maintain | 21j sweet spot canon | steady state optimal |
| scale | 14-21j cadence stricte | scale audience consomme creative vite |
| saturation | 7-14j re-test mandatory | re-validation post-decay forcée |

**Trigger refresh canon** ·

1. CTR decay -20% vs J0 (signal warning canon pacing axe 4)
2. CPM drift +30% WoW (signal compound creative fatigue)
3. Frequency saturation > 2.5 sur audience canon
4. 21 jours écoulés depuis lancement creative (cadence sweet spot)

Trigger compound (2+ signaux simultanés) · refresh mandatory immédiat · pas attendre 21j sweet spot.

---

## 6. Stage alignment · test wide vs scale focus

Test discipline canon n'est PAS uniforme cross-stages ·

### Stage test (audience NEW non-validée)

- Test matrix · Configuration A canon (angle × hook × visual · 27 variants)
- Budget allocation · 100% test · zero scale
- Win seuils tolérants · ROAS ≥ breakeven × 1.1 + spend ≥ 2× CPM (lower bar canon learning)
- Kill seuils strict · ROAS < breakeven × 0.7 + spend ≥ 1× CPM + days ≥ 3
- Refresh cadence · 14-21j strict (learning phase)

### Stage scale (angle validé · audience scaling)

- Test matrix · Configuration B canon (angle × audience × visual · 27 variants)
- Budget allocation · 80% reinforce winners · 20% nouveaux tests defensive
- Win seuils strict · ROAS ≥ breakeven × 1.3 + spend ≥ 5× CPM + days ≥ 10 (high bar canon scale)
- Kill seuils strict · ROAS < breakeven × 0.8 + spend ≥ 2× CPM + days ≥ 5
- Refresh cadence · 14-21j strict (audience consomme vite)

### Stage saturation (pool fatigué · re-test mandatory)

- Test matrix · Configuration A canon NEW angles · 50% pool refresh
- Budget allocation · 50% surviving winners · 50% nouveaux angles
- Win seuils tolérants · ROAS ≥ breakeven × 1.1 (re-validation lower bar)
- Refresh cadence · 7-14j re-test (escape saturation)

---

## 7. Cross-refs

- `pacing-doctrine.md` v2.78 · doctrine sœur · axe 4 CTR decay + refresh cadence 21j canon consumed (alignment cross-doctrine)
- `attribution-multitouch-doctrine.md` v2.78 · doctrine sœur · cadrage mesure post-test · ROAS attribution stage-aware miroir
- `compositional-cartography.md` v3.1 · équation NOYAU × CONTEXTE × MODIFIEURS · pattern ECR couche 1 instance créative · 3x3 matrix instance pattern compositional
- `pain-benefit-chain.md` · 4 chains canon (functional/identity/emotional/aspirational) · alimente axe angle MECE matrix §3
- `audience-cartography.md` v2.64 · cartographie audiences segments · alimente axe audience Configuration B matrix
- `operational-system-doctrine.md` v2.71 · doctrine mère 5 couches · cette doctrine instance multi-couches (2 Règles · 3 Templates · 4 Métriques)
- `extension-discovery-doctrine.md` v2.75 · pattern miroir frontmatter · skills test-aware peuvent déclarer `extension_hooks` consume NEW creative entities
- `skill-routing-doctrine.md` v2.77 · routing canon · skills test consume via mapping CLAUDE.md + manifest scan
- `investigation-posture.md` · 5 sections rigueur · skills analyze-perf ship output observé/déduit/inconnu/leviers/close ouvert

**Skills consumers v2.78+** ·

- `produce-paid-angles` · génération variants angles · consume 3x3 matrix §3 + pain-benefit-chain axes MECE
- `compose-creative` · composition variants visuels · consume Configuration A/B canon
- `recompose-creative` · adaptation creative existant · consume refresh trigger canon §5
- `creative-brief-composer` · brief test plan · consume matrix 3x3 + win/kill seuils §4
- `decompose-ad` · reverse-engineering ad concurrente · consume matrix MECE pour identifier angle/hook/visual axes
- `analyze-perf` · diagnostic win/kill · consume seuils §4 ROAS×spend×days + stage alignment §6
- `routine-perf` · monitoring tests · consume seuils chiffrés + refresh cadence triggers §5
- `audit-creative-fatigue` (futur v2.79+) · audit pool creative state · consume refresh cadence canon

---

## Hard Rules

**HR-CREATIVE-1.** Test matrix DOIT respecter 3x3 = 27 variants max canon. JAMAIS > 27 variants single batch (noise pipeline · cap dur doctrine).

**HR-CREATIVE-2.** Test matrix DOIT respecter MECE par axe · 3 angles orthogonaux ≠ 3 variants du même angle. Anti-pattern · over-polish 1 angle déguisé en testing.

**HR-CREATIVE-3.** Win/kill action requiert 3 seuils simultanés canon · ROAS × spend × days. JAMAIS kill sur ROAS isolé sans days ≥ 3 + spend ≥ 1× CPM. JAMAIS scale sur ROAS isolé sans days ≥ 7 + spend ≥ 3× CPM.

**HR-CREATIVE-4.** Refresh cadence canon stage-aware §6. JAMAIS refresh < 14j stage test (over-test waste) NI > 30j stage maintain (CTR effondré · auction punit).

**HR-CREATIVE-5.** Stage detection canon FIRST AVANT test plan. Test stage configuration A (angle × hook × visual). Scale stage configuration B (angle × audience × visual). JAMAIS configuration cross-stage drift.

**HR-CREATIVE-6.** Trigger refresh compound (2+ signaux simultanés · cf §5) · refresh mandatory immédiat. JAMAIS attendre 21j sweet spot quand compound signal hit. Auction punit retard.

---

## Anti-patterns

### Anti-pattern 1 · Over-polish 1 angle

Buyer s'attache à 1 angle gagnant historique · polish 10 variants visuels du même angle · diversification absente · audience saturation rapide. Pattern canon · matrix 3x3 MECE force 3 angles orthogonaux · diversification structurelle.

### Anti-pattern 2 · Test 50 variants random

Buyer ship 50 variants random sans structure axe · noise pipeline · pas canon win/kill · output non-extractible learnings.json. Pattern canon · matrix 3x3 = 27 variants cap canon + MECE par axe.

### Anti-pattern 3 · Kill prématuré

Variant killed après 1 jour ROAS faible · learning insuffisant · décision biaisée · waste budget exploration. Pattern canon · 3 seuils simultanés mandatory (ROAS × spend ≥ 1× CPM × days ≥ 3).

### Anti-pattern 4 · Scale prématuré

Variant scaled après 2 jours ROAS bon · over-confidence · scale sur signal noise · audience saturation rapide. Pattern canon · 3 seuils simultanés mandatory win (ROAS × spend ≥ 3× CPM × days ≥ 7).

### Anti-pattern 5 · Refresh trop tôt OR trop tard

Refresh creative à 7j (learning phase non finie) OR 45j (CTR effondré). Pattern canon · 21j sweet spot canon · 14j minimum · 30j max · stage-aware §6.

### Anti-pattern 6 · Configuration cross-stage drift

Stage test ship Configuration B (angle × audience × visual) · audience non-validée · audience axis noise · learning angle impossible. Pattern canon · Configuration A early stage · Configuration B post-validation scale.

### Anti-pattern 7 · MECE cassé par axe

Matrix 3x3 avec 3 hooks identiques juste différemment formulés · MECE cassé · output dispersé. Pattern canon · 3 hooks MECE problem-led × benefit-led × identity-led (cf hook-registry).

---

## Lexique

- **Matrix 3x3** · 3 axes × 3 variants = 27 variants test cap canon §3.
- **Configuration A** · angle × hook × visual · early stage validation.
- **Configuration B** · angle × audience × visual · post-validation scale.
- **Win seuil canon** · ROAS ≥ breakeven × 1.2 + spend ≥ 3× CPM + days ≥ 7.
- **Kill seuil canon** · ROAS < breakeven × 0.7 + spend ≥ 1× CPM + days ≥ 3.
- **Watch seuil canon** · ROAS breakeven × 0.9-1.2 + spend ≥ 2× CPM + days ≥ 5 · monitor 48-72h.
- **Breakeven** · ROAS minimum couvrir coût + marge · brand.json#financials.breakeven_roas.
- **CPM canon** · moyenne 30 jours account.
- **Sweet spot refresh** · 21j canon maintain stage · stage-aware §5.
- **Trigger refresh compound** · 2+ signaux simultanés (CTR decay · CPM drift · frequency · 21j cadence) · refresh mandatory immédiat.
- **Stage test** · audience NEW non-validée · learning phase.
- **Stage scale** · angle validé · audience scaling phase.
- **Stage saturation** · pool fatigué · re-test mandatory.

---

## Status

- **Canonique v2.78+.** Doctrine canon · ferme gap *"creative testing framework manquant"* flag P0 Sprint v2.78 Agent media buyer.
- **Doctrine sœur** · pacing-doctrine.md (axe 4 CTR decay consume cadence canon) · attribution-multitouch-doctrine.md (cadrage mesure post-test) · operational-system-doctrine.md v2.71 (doctrine mère 5 couches).
- **Backward compat** · strict additif · doctrine NEW n'override aucune existing. Skills legacy pre-v2.78 conservent test logic inline jusqu'à patch · v2.78+ migration progressive consume canon.
- **First applications** · produce-paid-angles v2.78 (génération matrix 3x3) · compose-creative v2.78 (composition Configuration A/B) · creative-brief-composer v2.78 (brief test plan) · analyze-perf v2.78 (diagnostic win/kill canon).
- **Promotion criterion** · à reviewer après 3+ skills creative-aware migrated consume canon + 1 audit cross-account test patterns convergence + learnings.json append creative testing patterns.

---

*Doctrine canonique skill-author-facing + media-buyer-facing. Canonise 3x3 testing matrix MECE + win/kill seuils chiffrés (ROAS × spend × days) + refresh cadence 21j sweet spot canon + stage alignment (test wide · scale focus · saturation re-test). Ferme gap structurel *"creative testing instinct sans protocole"*. Pattern miroir compositional-cartography.md (équation NOYAU × CONTEXTE × MODIFIEURS · ECR couche 1) et pacing-doctrine.md (axe 4 CTR decay refresh canon).*
