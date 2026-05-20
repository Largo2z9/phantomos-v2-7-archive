# Attribution Multitouch Discipline · Operating Doctrine

> Canonique v2.78+. Doctrine canon qui codifie le cadrage attribution multi-touch stage-dependent (7d-click vs 1d-click vs view-through · Meta-reported vs Shopify actual vs TripleWhale blended · iCAC vs CAC vs MER) au-delà du *"Meta dit ROAS 3 donc on est rentable"*. Doctrine sœur de `pacing-doctrine.md` (mesure pacing stage-aware) et `creative-testing-doctrine.md` (ROAS attribution post-test). Ferme le gap *"attribution multi-touch canon manquant"* flag P0 Sprint v2.78 Agent media buyer. Substrat consommé par `analyze-perf` (cross-référence Sheets + Meta + Shopify) · `routine-perf` (monitoring stage-aware) · `audit-setup` (vérifie attribution windows tracking) · `audit-meta-account` (attribution audit canon) · `audit-google-pmax` (attribution GA4 cross-canon).

---

## 1. Thèse fondatrice

> Attribution multi-touch est cadrage stage-dependent, pas one-size-fits-all. Choix attribution window canon dépend du stage (test/maintain/scale), du canal (Meta/Google/Klaviyo), et du métier brand (DTC repeat vs one-shot). Reconciliation cross-platform est mandatoire, jamais source unique vérité.

**Définition attribution canon** · mécanisme qui assigne une conversion à un (ou plusieurs) point(s) de contact dans le parcours utilisateur. Attribution répond à 4 questions canon ·

1. *"Quelle fenêtre attribution choisir ?"* (axe 1 · attribution windows canon par canal)
2. *"Quelle source de vérité prend la décision ?"* (axe 2 · Meta vs Shopify vs TripleWhale reconciliation)
3. *"Quelle métrique ROAS/CAC pivot ?"* (axe 3 · iCAC vs CAC vs MER mapping canon)
4. *"Comment varier le cadrage selon stage ?"* (axe 4 · stage-dependent attribution canon)

**Différenciation canon vs Meta-only blind trust** ·

| Layer | Meta-only trust | Shopify-only trust | TripleWhale blended | Attribution Multitouch Discipline canon |
|---|---|---|---|---|
| Source vérité | Meta reported | Shopify UTM | TW blended pivot | reconciliation 3 sources canon |
| Window canon | 7d-click default Meta | 30d UTM Shopify | 30d view + 7d click TW | stage-dependent canon § 4 |
| Stage awareness | absent · même window | absent | absent | test/maintain/scale calibré |
| iCAC vs CAC | confusion | absent | partial | mapping canon §6 |
| MER target | absent | absent | partial | stage canon 1.5x/2.5x/3.5x |

Attribution Multitouch Discipline n'est pas un choix idéologique (Meta vs Shopify vs TW). C'est la grammaire structurée qui aligne attribution window + source vérité + métrique pivot + stage stage-aware en canon partagé.

---

## 2. Le problème résolu

Sans Attribution Multitouch Discipline canon ·

1. **Meta-reported sur-estime systémique.** Buyer trust Meta ROAS 3.5 · scale spend · Shopify révèle ROAS réel 1.8 · perte budget · client signale décalage. Pattern Meta · 7d-click + 1d-view double-counting + cross-device over-credit + iOS 14.5 modeling gap.

2. **Shopify UTM sous-estime systémique.** Buyer trust Shopify UTM ROAS 1.2 · kill campaigns rentables · perte revenue · Meta révélé driver brand search + direct. Pattern Shopify · UTM stripping iOS Safari + last-click only + direct/organic over-credit.

3. **TripleWhale blended pivot mal calibré.** Buyer trust TW blended ROAS 2.5 · ignore stage-dependent calibration · scale stage attribution different vs test stage · over-confidence drift.

4. **iCAC vs CAC vs MER confusion.** Buyer report CAC 25€ · ignore organic contribution 30% · iCAC réel 35€ · margin négative · client réalise post-month-end · trust cassé.

5. **Attribution windows mismatch cross-canal.** Meta 7d-click + Klaviyo 30d view + Shopify 30d UTM · pas de reconciliation canon · output dispersé · diagnostic impossible.

6. **Skills analyze-perf + routine-perf + audit-meta-account sans substrat doctrinal.** Skills cross-référence sans canon partagé doctrinal · chaque skill ré-invente reconciliation logic inline · drift maintenance dette.

Attribution Multitouch Discipline = doctrine canon qui ferme ces 6 gaps via 3 axes (windows · sources · métriques) + stage alignment.

---

## 3. Le principe canon · stage-dependent attribution choice

Pattern canon · attribution choice n'est PAS fixe. Calibre selon stage maturité ·

### Stage test (audience NEW · learning phase)

- Attribution window canon · **7d-click Meta only** (réactif · capture signal direct response)
- Source vérité · **Meta-reported** acceptable (volume insuffisant pour reconciliation fiable)
- Métrique pivot · **CAC reported Meta** (CAC iCAC pas encore calculable · learning phase)
- MER target canon · **3.5x** (test stage tolérant · learning overhead absorbé)
- Rationale · learning phase requiert signal réactif · cross-platform reconciliation noise sur petits volumes

### Stage maintain (audience validée · steady state)

- Attribution window canon · **7d-click Meta + 30d UTM Shopify reconciled**
- Source vérité · **TripleWhale blended** (canon pivot · ou équivalent post-purchase survey)
- Métrique pivot · **iCAC** (incremental CAC · ajustement uplift organic baseline)
- MER target canon · **2.5x** (maintain steady state · marge stable)
- Rationale · steady state stable permet reconciliation fiable · iCAC pivot évite over-credit Meta

### Stage scale (audience scaling · aggressive ramp)

- Attribution window canon · **view-through (1d-view Meta) + 7d-click weighted reconciled**
- Source vérité · **Shopify UTM + post-purchase survey** (canon pivot strict · brand awareness scaling)
- Métrique pivot · **MER blended** (cross-channel attribution lift)
- MER target canon · **1.5x** (scale aggressive · margin compressed acceptable)
- Rationale · scale phase ajoute view-through brand awareness · Shopify pivot évite Meta over-credit auction inflation

### Stage saturation (pool fatigué · re-validation)

- Attribution window canon · **30d view-through + 7d-click weighted** (long-tail brand awareness capture)
- Source vérité · **post-purchase survey + Shopify UTM** (canon strict saturation phase)
- Métrique pivot · **MER + iCAC compound**
- MER target canon · **2.0x** (rebuild margin · saturation pricing power)

---

## 4. Attribution windows canon · table par canal

Pattern canon · chaque canal a window default + window canon stage-aware ·

| Canal | Window default | Window canon stage test | Window canon stage maintain | Window canon stage scale |
|---|---|---|---|---|
| **Meta Ads** | 7d-click + 1d-view (default Meta API) | 7d-click only | 7d-click + 1d-view | 7d-click + 1d-view + view-through weighted |
| **Google Ads / PMAX** | data-driven default | 7d-click last-click | data-driven 7d-click | data-driven 30d-click |
| **Klaviyo Email** | 5d-click default | 5d-click | 5d-click + 30d view (newsletter touchpoint) | 5d-click + 30d view weighted |
| **Shopify Analytics** | 30d UTM last-click | 30d UTM | 30d UTM + post-purchase survey | 30d UTM + post-purchase survey weighted |
| **TripleWhale** | 30d view + 7d click | 7d-click only (filter view-through noise) | 30d view + 7d click blended | 30d view + 7d click + post-purchase survey |
| **GA4** | data-driven 30d | data-driven 7d | data-driven 30d | data-driven 90d (long-tail brand awareness) |

**Lecture canon** · attribution window varies par canal AND par stage. Skill `analyze-perf` cross-référence windows canon avant cross-calculation. JAMAIS comparer Meta 7d-click direct avec Shopify 30d UTM · windows mismatch noise.

---

## 5. Cross-platform reconciliation pattern · Meta vs Shopify vs TripleWhale

Pattern canon · 3 sources vérité · reconciliation mandatory stage maintain+ ·

### Meta-reported (canal-side)

- Source · Meta Ads Manager + Meta API conversions
- Strengths · réactif (7d-click immediate) · ad-level granularity · auction signal capture
- Weaknesses · sur-estime systémique · cross-device over-credit · iOS 14.5 modeling gap · view-through inflation
- Trust level canon · **stage test acceptable** · **stage maintain+ requires reconciliation**

### Shopify actual (e-comm-side)

- Source · Shopify Analytics + UTM tracking + post-purchase survey
- Strengths · source vérité revenue brut · last-click strict · post-purchase honest signal
- Weaknesses · sous-estime systémique · UTM stripping iOS Safari · last-click only · direct/organic over-credit · pas ad-level granularity
- Trust level canon · **stage scale+ pivot canon** · **stage test insuffisant volume**

### TripleWhale blended (pivot canon)

- Source · TripleWhale (ou équivalent · Northbeam · Polar · Wicked Reports) · blended cross-channel
- Strengths · reconciliation cross-channel · post-purchase survey integration · stage-aware models
- Weaknesses · dépend qualité config opérateur · garbage in garbage out · modeling opacity
- Trust level canon · **stage maintain pivot canon** · **stage test optionnel**

### Reconciliation pattern canon stage maintain+

```
1. Pull Meta-reported ROAS (canal-side · 7d-click + 1d-view)
2. Pull Shopify actual ROAS (e-comm-side · 30d UTM last-click)
3. Pull TripleWhale blended ROAS (pivot · 7d click + 30d view)
4. Calculate divergence canon · 
   - Meta vs Shopify gap > 30% · flag investigation tracking
   - Meta vs TW gap > 20% · flag attribution model drift
   - Shopify vs TW gap > 20% · flag UTM tracking break
5. Pivot decision canon stage-aware · stage maintain = TW blended · stage scale = Shopify + survey
6. Audit trail · annotate output `attribution_source: TW_blended` + `divergence_meta_shopify: 0.25`
7. Operator drill 360° reconciliation rationale
```

**Anti-pattern · single source trust.** Meta-reported trust isolé · sur-estime systémique · scale waste. Pattern canon · reconciliation mandatory stage maintain+.

---

## 6. iCAC vs CAC vs MER · formulae canon

Pattern canon · 3 métriques canon CAC/MER · usage stage-aware ·

### CAC (Customer Acquisition Cost) reported

- **Formula canon** · `CAC = total_ad_spend / new_customers_reported_canal`
- **Source** · canal-side (Meta · Google · etc.)
- **Usage canon** · stage test (volume insuffisant iCAC) · pacing daily flag
- **Limite canon** · sur-estime efficacité paid · ignore organic baseline contribution

### iCAC (Incremental CAC)

- **Formula canon** · `iCAC = total_ad_spend / (new_customers_total - baseline_organic_new_customers)`
- **Source** · brand-side post-purchase survey + historical baseline organic
- **Usage canon** · stage maintain+ canon pivot · margin réel · vrai paid contribution
- **Trigger calculation** · post-month-end OR rolling 30d baseline
- **Limite canon** · requires baseline organic mesurable (≥ 90 jours data canon)

### MER (Marketing Efficiency Ratio)

- **Formula canon** · `MER = total_revenue / total_marketing_spend (all channels blended)`
- **Source** · brand-side Shopify total revenue / spend total (paid + content + influencer + etc.)
- **Usage canon** · stage scale canon pivot · cross-channel attribution lift · margin compressed acceptable
- **Stage target canon** · 3.5x test · 2.5x maintain · 1.5x scale (cf §3)
- **Limite canon** · cross-channel attribution opaque · pas ad-level granularity

### Mapping canon usage

| Stage | Métrique pivot canon | Rationale |
|---|---|---|
| test | CAC reported Meta | volume insuffisant iCAC · learning phase tolérant |
| maintain | iCAC (incremental) | steady state stable · margin réel · vrai paid contribution |
| scale | MER blended | cross-channel lift · margin compressed acceptable · brand awareness contribution |
| saturation | MER + iCAC compound | rebuild margin · saturation pricing power |

---

## 7. Cross-refs

- `pacing-doctrine.md` v2.78 · doctrine sœur · mesure pacing stage-aware · attribution windows alignment cross-doctrine
- `creative-testing-doctrine.md` v2.78 · doctrine sœur · ROAS attribution post-test · win/kill seuils consume attribution canon
- `operational-system-discipline.md` v2.71 · doctrine mère 5 couches · cette doctrine instance multi-couches (2 Règles · 4 Métriques)
- `investigation-posture.md` · 5 sections rigueur · skills attribution-aware (analyze-perf · audit-meta-account) ship output structuré observé/déduit/inconnu/leviers/close ouvert
- `confidence-propagation.md` · audit trail algèbre cascade confidence · attribution divergence cross-platform préserve confidence chain
- `skill-routing-discipline.md` v2.77 · routing canon · skills attribution consume via mapping CLAUDE.md + manifest scan
- `connectivity-layering.md` · 3 layers canon · Meta API + Google Ads API + Shopify API · attribution data sources cross-platform
- `notion-bridge-doctrine.md` v2.57+ · bidirectionnel pull/push · attribution data sync canon
- `brand-isolation-doctrine.md` · canon copy cross-brand · attribution baseline organic brand-specific isolation

**Skills consumers v2.78+** ·

- `analyze-perf` · diagnostic deep · consume reconciliation pattern §5 + métriques canon §6 + stage alignment §3
- `routine-perf` · monitoring stage-aware · consume windows canon §4 + métriques pivot stage-aware §6
- `audit-meta-account` · audit Meta · consume Meta attribution canon §3 + reconciliation pattern §5
- `audit-google-pmax` · audit PMAX · consume Google attribution canon §3 + GA4 windows §4
- `audit-setup` · vérifie tracking attribution-ready · pixels + conversions windows alignés canon §4

---

## Hard Rules

**HR-ATTRIB-1.** Skills attribution-aware (analyze-perf · routine-perf · audit-meta-account · audit-google-pmax) DOIVENT consume canon windows §4 + métriques §6 via cross-ref doctrine, JAMAIS inventer attribution inline frontmatter.

**HR-ATTRIB-2.** Output skill attribution-aware DOIT taguer stage canon explicit (test/maintain/scale) + source vérité canon (Meta/Shopify/TW) + window canon (7d-click/30d UTM/blended) AVANT recos. Sans tags · output hors-contexte · trust cassé.

**HR-ATTRIB-3.** Stage maintain+ requiert reconciliation 3 sources canon (Meta + Shopify + TW). JAMAIS source unique trust stage maintain+. Stage test acceptable Meta-only.

**HR-ATTRIB-4.** iCAC pivot canon stage maintain+. JAMAIS report CAC reported Meta isolé stage maintain+ · sur-estime · margin négative silencieuse.

**HR-ATTRIB-5.** MER target stage-aware canon (3.5x test · 2.5x maintain · 1.5x scale · 2.0x saturation). JAMAIS MER target uniform cross-stages · margin drift.

**HR-ATTRIB-6.** Divergence Meta vs Shopify > 30% · flag investigation tracking mandatory. JAMAIS ignore divergence > 30% · tracking break OR attribution drift signal critical.

**HR-ATTRIB-7.** Attribution windows mismatch cross-canal · JAMAIS comparer direct (Meta 7d-click vs Shopify 30d UTM). Pattern canon · reconciliation window-aware §4 + audit trail divergence annotation.

---

## Anti-patterns

### Anti-pattern 1 · Meta-only blind trust stage maintain+

Buyer trust Meta ROAS 3.5 stage maintain · scale spend · Shopify révèle ROAS réel 1.8 · perte budget · client signale post-month-end. Pattern canon · reconciliation 3 sources mandatory stage maintain+.

### Anti-pattern 2 · Shopify-only blind trust stage scale

Buyer trust Shopify UTM ROAS 1.2 stage scale · kill campaigns rentables · Meta révélé driver brand search + direct · revenue lost. Pattern canon · stage scale pivot Shopify + post-purchase survey · pas Shopify isolé.

### Anti-pattern 3 · TW blended uniform cross-stages

Buyer trust TW blended ROAS 2.5 uniform · ignore stage-dependent calibration · scale stage attribution different vs test stage · over-confidence drift. Pattern canon · stage-aware pivot canon §3.

### Anti-pattern 4 · iCAC vs CAC vs MER confusion

Buyer report CAC 25€ stage maintain · ignore organic contribution 30% · iCAC réel 35€ · margin négative · trust cassé. Pattern canon · iCAC pivot canon stage maintain+ · CAC reported uniquement stage test.

### Anti-pattern 5 · Attribution windows mismatch cross-canal

Compare direct Meta ROAS (7d-click + 1d-view) vs Shopify ROAS (30d UTM) sans reconciliation windows. Windows mismatch · noise · diagnostic impossible. Pattern canon · windows canon §4 cross-canal alignment + reconciliation pattern §5.

### Anti-pattern 6 · Single source trust sans audit trail

Skill ship output attribution sans annotation source canon (Meta/Shopify/TW) + window canon (7d-click/30d UTM). Opérateur drill 360° impossible. Pattern canon · audit trail mandatory `attribution_source` + `attribution_window` annotation output.

### Anti-pattern 7 · Stage agnostic attribution

Application uniforme attribution window cross-stages (e.g. 7d-click stage scale · ignore view-through brand awareness contribution). Pattern canon · stage detection FIRST · windows stage-aware §3 SECOND.

---

## Lexique

- **7d-click** · attribution window 7 jours post-click · Meta default canon stage test.
- **1d-view** · attribution window 1 jour post-impression · Meta view-through canon stage maintain+.
- **30d UTM** · attribution window 30 jours UTM last-click · Shopify default canon.
- **View-through** · attribution post-impression sans click · capture brand awareness scaling.
- **CAC** · Customer Acquisition Cost reported canal-side · formula §6 · canon stage test.
- **iCAC** · Incremental CAC · ajustement uplift organic baseline · formula §6 · canon stage maintain+.
- **MER** · Marketing Efficiency Ratio · revenue / total marketing spend blended · formula §6 · canon stage scale+.
- **MER target canon** · 3.5x test · 2.5x maintain · 1.5x scale · 2.0x saturation §3.
- **Reconciliation 3 sources** · Meta-reported + Shopify actual + TripleWhale blended · pattern canon §5 mandatory stage maintain+.
- **Post-purchase survey** · brand-side honest attribution · *"comment nous avez-vous trouvés ?"* · canon scaling stage.
- **Divergence threshold canon** · Meta vs Shopify > 30% · flag investigation tracking · §5.
- **Stage test** · audience NEW non-validée · CAC pivot · 3.5x MER target · 7d-click only.
- **Stage maintain** · audience validée steady state · iCAC pivot · 2.5x MER target · reconciliation 3 sources.
- **Stage scale** · audience scaling phase · MER pivot · 1.5x target · view-through weighted reconciled.
- **Stage saturation** · pool fatigué · MER + iCAC compound · 2.0x target.

---

## Status

- **Canonique v2.78+.** Doctrine canon · ferme gap *"attribution multi-touch canon manquant"* flag P0 Sprint v2.78 Agent media buyer.
- **Doctrine sœur** · pacing-doctrine.md (mesure pacing stage-aware) · creative-testing-doctrine.md (ROAS attribution post-test) · operational-system-discipline.md v2.71 (doctrine mère 5 couches).
- **Backward compat** · strict additif · doctrine NEW n'override aucune existing. Skills legacy pre-v2.78 conservent attribution logic inline jusqu'à patch · v2.78+ migration progressive consume canon.
- **First applications** · analyze-perf v2.78 (cross-référence reconciliation) · routine-perf v2.78 (monitoring stage-aware) · audit-meta-account v2.78 (Meta attribution canon) · audit-google-pmax v2.78 (Google attribution canon).
- **Promotion criterion** · à reviewer après 3+ skills attribution-aware migrated consume canon + 1 audit cross-account reconciliation patterns convergence + learnings.json append attribution divergence patterns.

---

*Doctrine canonique skill-author-facing + media-buyer-facing. Canonise cadrage attribution multi-touch stage-dependent · 3 axes (windows canon par canal · reconciliation 3 sources · métriques iCAC/CAC/MER) + stage alignment (test/maintain/scale/saturation). Ferme gap structurel *"Meta-reported blind trust sur-estime systémique"*. Pattern miroir pacing-doctrine.md (stages alignment cross-doctrine) et creative-testing-doctrine.md (win/kill ROAS attribution canon).*
