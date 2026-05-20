# Pacing Doctrine · Operating Doctrine

> Canonique v2.78+. Doctrine canon qui codifie les seuils chiffrés partagés du pacing media buyer (spend variance · frequency saturation · CPM drift · creative fatigue) au-delà du gut feeling subjectif. Doctrine sœur de `creative-testing-doctrine.md` (cycle test/refresh) et `attribution-multitouch-doctrine.md` (cadrage mesure post-pacing). Ferme le gap *"seuils pacing inventés ad-hoc"* flag P0 Sprint v2.78 Agent media buyer. Substrat consommé par `routine-perf` (pacing daily) et `analyze-perf` (diagnostic deep) et `audit-google-pmax` (PMAX pacing).

---

## 1. Thèse fondatrice

> Pacing est le métier quotidien du media buyer. Seuils canon partagés cross-account = action proactive vs reactive. Le gut feeling sans chiffres ancrés dérive en biais cognitifs cross-session.

**Définition pacing canon** · ensemble des mesures opérationnelles qui surveillent l'évolution dans le temps des inputs (spend) et des signaux d'usage (frequency · CPM · CTR) d'un compte ou d'une campagne media buying. Pacing répond à 4 questions canon ·

1. *"Le spend respecte-t-il la cible ?"* (axe 1 · spend variance)
2. *"L'audience est-elle saturée ?"* (axe 2 · frequency)
3. *"Le coût d'impression dérive-t-il ?"* (axe 3 · CPM drift)
4. *"Les créatives s'usent-elles ?"* (axe 4 · creative fatigue · CTR decay 14-30j)

**Différenciation canon vs gut feeling** ·

| Layer | Gut feeling | Pacing Doctrine canon |
|---|---|---|
| Seuils | subjectifs · session-to-session drift | chiffrés partagés cross-account |
| Trigger alerte | reactive · client signale | proactive · seuil canon hit |
| Mémoire cross-session | absent · re-décide chaque review | learnings.json append-only |
| Cohérence team | absent · chaque buyer son barème | canon partagé team |
| Action stage-aware | absent · même action toutes stages | stage canon (test/maintain/scale) calibrée |

Pacing Doctrine n'est pas une checklist statique. C'est la grammaire chiffrée qui permet à l'opérateur (humain ou agent) de surveiller un compte à fréquence sans réinventer la barème chaque session.

---

## 2. Le problème résolu

Sans Pacing Doctrine canon ·

1. **Drift seuils ad-hoc.** Chaque buyer (ou chaque session agent) invente ses seuils dans la prose : *"frequency haute"* (3 ? 5 ?), *"CPM en hausse"* (10% ? 30% ?), *"creative fatiguée"* (7j ? 21j ?). Drift session-to-session · output dispersé · trust cassé client.

2. **Subjective gut feeling.** Sans canon chiffré, le buyer pivote sur instinct cumulatif qui dérive avec la fatigue cognitive, le mood, ou la pression client. Pas d'audit trail rétrograde · pas de learnings extractibles.

3. **Pas canon partagé team.** Chaque buyer agence applique ses propres seuils. Compte transféré entre buyers · drift d'opinion silencieux. Multi-buyer workflow impossible sans canon.

4. **Skills routine-perf + analyze-perf + audit-google-pmax sans substrat doctrinal.** Sprint v2.78 ship 3 skills monitoring pacing mais sans canon partagé doctrinal · chaque skill ré-invente seuils dans frontmatter · drift maintenance dette · scaling impossible.

5. **Stage alignment absent.** Pacing test stage (audience nouvelle · CPM élevé OK car learning) traité comme pacing scale stage (audience validée · CPM stable canon). Confusion seuils cross-stage · over-react sur learning phase.

Pacing Doctrine = doctrine canon qui ferme ces 5 gaps via 4 axes chiffrés + stages alignment + trigger patterns explicit.

---

## 3. Le principe canon · 4 axes pacing chiffrés

Pacing canon décompose en 4 axes orthogonaux measurables ·

### Axe 1 · Spend variance (alignment vs target)

Variance entre spend daily réel et target budget canon. Mesure si la livraison budget respecte la cible.

**Formula canon** · `variance_pct = (spend_actual - spend_target) / spend_target × 100`

**Seuils canon** ·

| Variance | État | Action canon |
|---|---|---|
| ±10% | normal | aucune action |
| ±20% | warning | flag + monitor 24-48h |
| ±40% | critical | drill diagnostic immédiat · pause/scale/reallocation |

### Axe 2 · Frequency saturation (par audience)

Nombre moyen de fois où un utilisateur cible voit l'ad sur la fenêtre canon (7j Meta · learning period PMAX).

**Seuils canon Meta** ·

| Frequency | État | Action canon |
|---|---|---|
| ≤ 1.8 | optimal | scaling possible |
| 1.8 - 2.5 | normal | maintain |
| > 2.5 | saturation signal | flag + refresh creative |
| > 4.0 | audience fatigue critical | swap audience ou kill ad set |

**Seuils canon Google PMAX** ·

| Frequency | État | Action canon |
|---|---|---|
| ≤ 3.0 | optimal learning | maintain |
| 3.0 - 5.0 | normal | monitor |
| > 5.0 | saturation campaign learning period | refresh listing groups ou audience signals |

### Axe 3 · CPM drift (week-over-week)

Évolution du CPM hebdomadaire vs semaine précédente. Indicateur précoce creative fatigue ou auction shift.

**Formula canon** · `cpm_drift_pct = (cpm_week_current - cpm_week_previous) / cpm_week_previous × 100`

**Seuils canon** ·

| Drift WoW | État | Action canon |
|---|---|---|
| ±15% | normal volatility | aucune action |
| +30% | creative fatigue signal | flag refresh creative + audit auction |
| +50% | critical drift | drill diagnostic immédiat · pause + refresh |
| -30% | unusual gain | drill diagnostic · vérifier tracking + scaling opportunity |

### Axe 4 · Creative fatigue · CTR decay (14-30j threshold canon)

Évolution du CTR sur la durée de vie d'une création. Indicateur direct fatigue audience-creative match.

**Seuils canon CTR decay vs J0** ·

| Âge creative | CTR vs J0 | État | Action canon |
|---|---|---|---|
| 14 jours | -20% | warning · creative fatigue signal | flag refresh |
| 21 jours | sweet spot canon refresh | refresh recommandé | swap creative |
| 30 jours | -40% | critical creative fatigue | kill creative · refresh mandatory |

**Refresh cadence canon** · 21 jours sweet spot. Pas trop tôt (gaspillage spend test résiduel). Pas trop tard (CTR effondré · CPM auction punit).

---

## 4. Seuils chiffrés canon · table consolidée

Table maître canon · 4 axes × 3 niveaux d'alerte ·

| Axe | Métrique | Normal | Warning | Critical |
|---|---|---|---|---|
| 1 · Spend variance | % vs target | ±10% | ±20% | ±40% |
| 2 · Frequency Meta | par audience 7j | ≤ 1.8 | 1.8 - 2.5 | > 4.0 |
| 2 · Frequency PMAX | learning period | ≤ 3.0 | 3.0 - 5.0 | > 5.0 |
| 3 · CPM drift WoW | % vs week-1 | ±15% | +30% | +50% |
| 4 · CTR decay J0 | % vs lancement | ≤ -10% | -20% (14j) | -40% (30j) |
| 4 · Creative refresh | âge sweet spot | < 14j | 14-20j | > 30j (21j sweet spot canon) |

**Lecture canon** · un axe en warning isolé · monitor. Deux axes en warning simultanés · drill diagnostic. Un axe en critical · action immédiate (pause/refresh/swap). Cumul d'axes warning sur même asset · refresh mandatory.

**Anti-pattern table.** Re-inventer seuils dans chaque skill frontmatter. Pattern canon · skills `routine-perf` + `analyze-perf` + `audit-google-pmax` consume cette table via cross-ref doctrine.

---

## 5. Stages alignment · test / maintain / scale

Pacing seuils ne sont PAS uniformes cross-stages. Le canon stage-aware ·

### Stage test (audience nouvelle · learning phase)

- Spend velocity canon · 1.5x scale signal (vs baseline)
- Variance tolérée · ±30% (vs ±20% maintain)
- Frequency tolérée · > 2.5 acceptable (learning · pas saturation tant que ROAS pas stabilisé)
- CPM drift tolérance · +50% acceptable (auction learning)
- Creative refresh · 14j minimum (donner temps à creative de learner)

### Stage maintain (audience validée · steady state)

- Spend velocity canon · 2.5x baseline · stable
- Variance tolérée · ±20% canon
- Frequency tolérée · 1.8 - 2.5 canon
- CPM drift tolérance · ±15% canon
- Creative refresh · 21j sweet spot canon

### Stage scale (audience scaling · post-validation)

- Spend velocity canon · 3.5x baseline · ramp aggressive
- Variance tolérée · ±10% strict (variance signale auction punit scaling)
- Frequency tolérée · ≤ 2.5 strict (saturation tue ROAS scale)
- CPM drift tolérance · ±15% strict
- Creative refresh · 14-21j cadence stricte (scale audience consomme creative vite)

**Pattern canon stage detection** · skill `routine-perf` détecte stage via 7-day rolling avg vs target + signal validation_status learnings.json. `analyze-perf` consume stage canon pour calibrer recommendations.

---

## 6. Patterns trigger alert canon

Pattern canon · *"1 warning si X · critical si Y"* explicit cross-axe ·

**Pattern 1 · Spend overshoot test stage** · variance +25% sur audience test · 1 warning. Si +50% · critical · drill kill audience ou re-allocation. Trigger skill `analyze-perf` audit budget allocation.

**Pattern 2 · Frequency saturation Meta** · frequency 2.8 sur audience scale · 1 warning. Si > 4.0 · critical · swap audience ou refresh creative immédiat. Trigger skill `routine-perf` flag refresh.

**Pattern 3 · CPM drift double signal** · CPM +35% WoW + CTR -25% sur même creative · 2 warnings simultanés · critical compound. Pattern canon creative fatigue confirmée · trigger refresh mandatory (skill `creative-brief-composer` ou `recompose-creative`).

**Pattern 4 · Stage stage drift** · audience taggée scale stage mais frequency dérive > 2.5 + CPM drift > +30% · pattern canon *"scale stage qui passe en maintain"* · trigger recalibration target (skill `analyze-perf`).

**Pattern 5 · PMAX learning saturation** · frequency PMAX > 5.0 + asset score < 4/5 · trigger refresh listing groups + audience signals (skill `audit-google-pmax`).

---

## 7. Cross-refs

- `creative-testing-doctrine.md` v2.78 · doctrine sœur · cycle test/refresh consume seuils CTR decay axe 4 + refresh cadence 21j canon
- `attribution-multitouch-doctrine.md` v2.78 · doctrine sœur · cadrage mesure post-pacing · attribution stage-aware miroir stages pacing test/maintain/scale
- `operational-system-doctrine.md` v2.71 · doctrine mère 5 couches · cette doctrine instance multi-couches (2 Règles · 4 Métriques · 5 Rituels)
- `investigation-posture.md` · 5 sections rigueur · skills pacing-aware (routine-perf · analyze-perf) ship output structuré observé/déduit/inconnu/leviers/close ouvert
- `skill-routing-doctrine.md` v2.77 · routing canon · skills consume pacing canon via mapping CLAUDE.md + manifest scan
- `confidence-propagation.md` · audit trail algèbre cascade confidence · seuils chiffrés canon préservent confidence cross-skill
- `extension-discovery-doctrine.md` v2.75 · pattern miroir frontmatter discovery · skills pacing-aware peuvent déclarer `extension_hooks` pour consume NEW pacing entities scaffolded
- `connectivity-layering.md` · 3 layers canon · MCP Meta + APIs Google Ads · pacing data sources

**Skills consumers v2.78+** ·

- `routine-perf` · pilotage quotidien · consume axes 1-4 + stage alignment + patterns trigger (alertes binaires flags)
- `analyze-perf` · diagnostic deep · consume canon pour cross-référencer Sheets + Meta + Shopify · stage canon calibre recos
- `audit-google-pmax` · audit PMAX · consume frequency PMAX seuils canon §3 + listing groups refresh patterns
- `audit-meta-account` · audit Meta · consume frequency Meta + CPM drift canon §3
- `audit-setup` · vérifie tracking pacing-ready · pixels + conversions windows alignés stage

---

## Hard Rules

**HR-PACING-1.** Skills pacing-aware (routine-perf · analyze-perf · audit-google-pmax · audit-meta-account) DOIVENT consume seuils canon de §3-§5 via cross-ref doctrine, JAMAIS inventer seuils inline frontmatter.

**HR-PACING-2.** Output skill pacing-aware DOIT taguer stage canon explicit (test/maintain/scale) AVANT recos. Sans tag stage · recos hors-contexte · trust cassé opérateur.

**HR-PACING-3.** Variance spend > ±40% · action immédiate canon (pause/scale/reallocation). JAMAIS *"monitor"* sur critical · le canon distingue warning (monitor) de critical (action).

**HR-PACING-4.** Refresh creative cadence 21j sweet spot canon. JAMAIS refresh < 14j (gaspillage learning) OR > 30j (CTR effondré). Sauf exception documentée stage canon (test stage tolère 14-21j strict).

**HR-PACING-5.** Frequency saturation Meta > 4.0 · action mandatory swap audience OR kill ad set. Frequency PMAX > 5.0 · refresh listing groups OR audience signals. JAMAIS attendre amélioration spontanée · auction punit.

**HR-PACING-6.** CPM drift +50% WoW · critical immédiat. Drill diagnostic AVANT pause (vérifier auction shift vs creative fatigue vs tracking break). Pause sans drill · perte budget learning.

---

## Anti-patterns

### Anti-pattern 1 · Seuils ad-hoc session-to-session

Buyer (ou agent) invente seuils inline *"frequency haute"* sans chiffre canon. Drift output session-to-session · trust cassé · learnings non-extractibles. Pattern canon · table §4 source unique vérité · skills consume via cross-ref.

### Anti-pattern 2 · Stage agnostic seuils

Application uniforme seuils maintain stage sur audience test stage · over-react sur learning phase · kill audience prématuré · waste budget exploration. Pattern canon · stage detection FIRST · seuils stage-aware §5 SECOND.

### Anti-pattern 3 · Warning treated as critical

Variance ±25% (warning) traité comme critical (action immédiate). Over-reactive · perte budget steady state. Pattern canon · warning = monitor 24-48h · critical = action immédiate. Distinction binaire canon.

### Anti-pattern 4 · Critical treated as warning

Variance ±45% (critical) traité comme warning (monitor). Under-reactive · budget gaspillé · client signale avant buyer. Pattern canon · critical = action mandatory · jamais monitor.

### Anti-pattern 5 · Refresh trop tôt OR trop tard

Refresh creative à 7j (trop tôt · learning phase non finie) OR 45j (trop tard · CTR effondré). Pattern canon · 21j sweet spot canon · 14j minimum stage test · 30j max stage maintain.

### Anti-pattern 6 · CPM drift sans drill diagnostic

CPM +60% WoW pause silent sans drill auction vs creative vs tracking. Diagnostic fail · même creative re-launched · re-drift. Pattern canon · drill FIRST (auction shift / creative fatigue / tracking break / event broadcasting Meta) · action SECOND.

---

## Lexique seuils canon

- **Variance** · écart % spend actual vs target. Seuils ±10%/±20%/±40% canon §3 axe 1.
- **Frequency** · moyenne impressions/utilisateur cible sur fenêtre canon (7j Meta · learning period PMAX). Seuils Meta ≤1.8/2.5/4.0 canon. Seuils PMAX ≤3.0/5.0 canon.
- **CPM drift WoW** · évolution % CPM hebdo vs semaine précédente. Seuils ±15%/+30%/+50% canon.
- **CTR decay** · évolution % CTR vs J0 lancement creative. Seuils 14j/21j/30j canon.
- **Sweet spot refresh** · 21 jours canon · sweet spot maintain stage. Cadence aware stages (14j test · 21j maintain · 14-21j scale).
- **Stage test** · audience learning phase · seuils tolérants canon §5.
- **Stage maintain** · audience validated steady state · seuils canon strict §3-§4.
- **Stage scale** · audience scaling phase · seuils strict canon §5.
- **Spend velocity** · 7-day rolling avg vs target. Multiplicateurs canon 1.5x test · 2.5x maintain · 3.5x scale.

---

## 8. Position dans le système opérationnel 5 couches

Pacing Doctrine opère sur 3 couches simultanément du système opérationnel (`operational-system-doctrine.md`) ·

**Couche 2 · Règles (heuristiques décision).** Seuils chiffrés canon §3-§4 + patterns trigger alerte §6 + stage detection §5 sont heuristiques de décision canon · *"si variance > ±40% alors action immédiate"*. Pattern miroir `dependency-resolution-protocol.md` L1+L2+L3 gap-filling pre-flight.

**Couche 4 · Métriques (boucles feedback).** Skills pacing-aware capture metrics runtime cross-session (variance · frequency · CPM drift · CTR decay) · alimente learnings.json append-only · audit trail traçable. Pattern miroir `confidence-propagation.md` audit trail.

**Couche 5 · Rituels (cadence opérationnelle).** Pacing canon rituel daily via `routine-perf` · weekly via `analyze-perf` deep diagnostic · pre-ship via `audit-meta-account` + `audit-google-pmax`. Cadence stage-aware embedded canon.

---

## Status

- **Canonique v2.78+.** Doctrine canon · ferme gap *"pacing seuils ad-hoc"* flag P0 Sprint v2.78 Agent media buyer.
- **Doctrine sœur** · creative-testing-doctrine.md (cycle test/refresh consume seuils axe 4) · attribution-multitouch-doctrine.md (cadrage mesure post-pacing) · operational-system-doctrine.md v2.71 (doctrine mère 5 couches).
- **Backward compat** · strict additif · doctrine NEW n'override aucune existing. Skills legacy pre-v2.78 conservent seuils inline jusqu'à patch · v2.78+ migration progressive consume canon.
- **First applications** · routine-perf v2.78 (pilotage quotidien) · analyze-perf v2.78 (diagnostic deep) · audit-google-pmax v2.78 (PMAX pacing) consume canon §3-§5 via cross-ref.
- **Promotion criterion** · à reviewer après 3+ skills pacing-aware migrated consume canon + 1 audit cross-account seuils convergence + learnings.json append pacing patterns.

---

*Doctrine canonique skill-author-facing + media-buyer-facing. Canonise 4 axes pacing chiffrés (spend variance · frequency · CPM drift · CTR decay) + stage alignment (test/maintain/scale) + patterns trigger explicit. Ferme gap structurel *"gut feeling sans canon partagé"*. Pattern miroir investigation-posture.md (rigueur réponse) et operational-system-doctrine.md (couches 2+4+5 multiplicatives).*
