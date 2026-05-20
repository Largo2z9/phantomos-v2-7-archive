---
name: analyze-perf
type: producer
version: "1.0.0"
isolation_scope: brand
layer: production
recommended_model: sonnet
reasoning_pattern: investigation-posture
description: >
  Deep-dive diagnostic perf paid cross-platform (Meta + Google + TikTok +
  Shopify + TripleWhale + Klaviyo). Pull insights multi-jour (default 7-30j),
  cross-reference attribution windows (7d-click vs 1d-click vs view-through),
  diagnostic CPA / ROAS / COS / MER avec confidence chain canon, recos
  actionnables ranked impact vs effort. Sub-agent friendly (delegated heavy
  lift sonnet). Step 0 bridge proactif canon v2.77 si MCP/token absent.
  FR: "deep-dive perf", "analyse perf en profondeur", "diagnostic ROAS drop",
      "audit perf 30j", "investigation perf", "pourquoi le ROAS tombe",
      "creuse la perf", "analyse paid en profondeur".
  EN: "deep-dive perf", "perf analysis", "ROAS drop diagnostic",
      "30-day perf audit", "perf investigation", "why is CPA up".
permissions:
  reads: ["brands/{slug}/", "resources/conventions/*.json"]
  writes: ["brands/{slug}/perf-analysis/{date}_analyze-perf.md"]
  mode: interactive
  subagent_safe: true
pipeline:
  preconditions: brands/{slug}/brand.json must exist with at least one paid platform encoded in stack
  postconditions: diagnostic file persisted under brands/{slug}/perf-analysis/, optional capture-learning if pattern detected
extension_hooks:
  consumable_by: ["brand_entity", "creative_entity"]
disambiguates_against:
  routine-perf: "route to routine-perf when operator wants quick J-1 daily briefing (~5 min, flag binaire anomalies). analyze-perf is the deep-dive multi-day diagnostic (7-30j, profond, confidence chain, recos ranked)"
  audit-meta-account: "route to audit-meta-account when operator audits SETUP health (pixel, CAPI, structure, naming, attribution config). analyze-perf audits DELIVERY signals (CPA / ROAS / COS / MER multi-day cross-platform)"
  import-meta-results: "route to import-meta-results when operator wants raw data pulled + writing canon validations[]. analyze-perf consumes data already imported (or pulls it as side-effect) to produce diagnostic + recos actionnables"
---

# Skill: analyze-perf

Senior media buyer deep-dive diagnostic. Pulls multi-day signals across every paid platform encoded in the brand stack, triangulates attribution windows, separates observed delivery from inferred cause, ranks recommendations by impact vs effort. Sister skill to `routine-perf` (quick daily) and `audit-meta-account` (setup health). The skill produces a diagnostic file, never silently mutates campaigns.

## Expert methodology

**Canonical expert persona** · senior media buyer / account strategist 10+ years on Meta + Google + TikTok, fluent on attribution gap analysis (7d-click vs 1d-click vs view-through), MER triangulation cross-platform, creative fatigue detection, audience saturation curves, seasonality calibration.

**Framework** · investigation-posture 5 sections canon (Observed · Deduced · Unknown · Levers · Open close). Each section serves a role · Observed sources facts with confidence forte, Deduced flags hypotheses with confidence chain explicit, Unknown lists variables not observable from the current data pull, Levers ranks remediation options impact vs effort, Open close hands ONE macro question to the operator.

**Matrix** (applied per platform pulled) · *delivery metric (CPA / ROAS / COS / MER) × attribution window (7d-click / 1d-click / view-through / blended) × time slice (last 7 / 14 / 30 days vs prior period) × dimension (campaign / ad_set / ad / placement / age_gender)*. The matrix is internal reasoning surface only. The operator sees synthesis, not the raw cube.

**Key variables** · CPA reported per platform, ROAS reported per platform, COS per platform, blended MER (TW or computed), Shopify actual revenue, attribution gap (Meta-reported vs Shopify actual vs TW blended divergence), iCAC (incremental CAC if TW or external lift study), creative fatigue indicators (frequency, CTR decay, CPM drift), audience saturation indicators (reach saturation curve, LAL freshness).

**Codified reference** · `resources/conventions/meta-ads.json` for Meta API endpoints + rate limits + naming, `resources/conventions/google-ads.json` for Google, `resources/conventions/triplewhale.json` for TW MER, `resources/conventions/shopify.json` for actuals, `resources/conventions/klaviyo.json` for email/SMS contribution. If a convention is missing or incomplete for a platform in scope, Gate doc blocks execution until it is filled (read official doc via WebFetch, fill convention, then proceed).

---

## Step 0 · Gate access + bridge proactif canon v2.77

**CRITICAL** · check access on EVERY platform in scope BEFORE pulling data. NEVER silently fall back to declarative interview without offering bridge proactif first.

1. Read `brands/{slug}/credentials.env` and `credentials_shared.env` (workspace root). For each platform in scope, check the relevant credential keys per convention (e.g. `META_ACCESS_TOKEN` + `META_AD_ACCOUNT_ID` for Meta, `GOOGLE_ADS_DEVELOPER_TOKEN` + customer_id for Google, `TW_API_KEY` for TripleWhale, Shopify Admin API token, Klaviyo private API key).
2. Read each convention referenced in scope. If a convention is incomplete or missing → Gate doc first (WebFetch official doc, fill the convention) before any API call.

**Branching** (use AskUserQuestion when access is mixed) ·

- **All platforms in scope have tokens + conventions complete** → announce data mode, proceed to Step 1 ·
  > *"Accès OK pour {N platforms in scope}. Je pull les signaux multi-jour cross-platform en parallèle (3-5 min selon scope), je reviens avec le diagnostic en 5 sections."*

- **Subset of platforms has tokens, subset is missing** → AskUserQuestion 2 options ·
  - (a) "Je te guide pour connecter {missing platform} maintenant (2 min via `connect-mcp-server`), audit cross-platform complet ensuite"
  - (b) "Je tourne sur les {N platforms available}, je flag explicitement ce qui manque pour la triangulation"
  Default proactif proactif · (b) si l'opérateur a déjà 2+ platforms branchées (le diagnostic reste utile, juste flag les gaps), (a) si Meta SEUL et Shopify dispo (la triangulation Meta+Shopify est minimum viable).

- **Aucun token, aucune convention complète** → AskUserQuestion 2 options ·
  - (a) "Je te guide pour connecter Meta + Shopify minimum (5 min via `connect-mcp-server`), diagnostic factuel ensuite"
  - (b) "Je bascule en mode declarative · tu me dictes les chiffres par plateforme et période, je structure le diagnostic"
  Default proactif proactif · (a) si l'opérateur a le temps, sinon fallback (b) sans blocker.

**NEVER** dump tous les chiffres de l'opérateur dans un questionnaire form (a) avant d'avoir offert le data mode (b). Le data mode est toujours offert en premier.

---

## Step 1 · Scope sub-skills cartography (clarify scope)

The skill is multi-platform multi-period multi-lens. Before pulling, scope explicitly with the operator. ONE AskUserQuestion per dimension when ambiguous, never a 4-question form.

**Period** ·
- Default · last 7 days vs prior 7 days (week-over-week diagnostic, fastest pull, sharpest signal on creative fatigue or audience saturation).
- Option · last 14 days vs prior 14 days (mid-cycle).
- Option · last 30 days vs prior 30 days (cycle full, best signal on seasonality, lifecycle).
- Custom · operator-stated period (BFCM week, post-launch month, etc.).

**Platforms** ·
- Meta · always pull if `META_ACCESS_TOKEN` present (anchor platform for most DTC stacks).
- Google · pull if `google-ads.json` convention complete AND `GOOGLE_ADS_*` credentials present.
- TikTok · pull if `tiktok-ads.json` convention complete AND `TIKTOK_*` credentials present.
- Shopify · always pull if `SHOPIFY_*` credentials present (anchor for actuals triangulation).
- TripleWhale · pull if `triplewhale.json` convention complete AND `TW_API_KEY` present (the blended MER ground truth when available).
- Klaviyo · pull if `klaviyo.json` convention complete AND `KLAVIYO_PRIVATE_KEY` present (email/SMS contribution to MER).

**Lens** ·
- Global view · single page diagnostic, blended MER, no drill-down per platform (fastest, operator wants the macro state).
- Campaign-level · drill per campaign across platforms (operator wants to know which campaign is bleeding).
- Ad-set-level · drill per ad set within Meta (audience saturation focus).
- Creative-level · drill per ad / creative (creative fatigue focus, frequency + CTR decay).

**Metrics focus** ·
- CPA · cost per acquisition reported per platform.
- ROAS · revenue / spend per platform (reported, vs Shopify actual).
- COS · cost of sales (paid spend / revenue).
- MER · blended marketing efficiency ratio (total revenue / total marketing spend) when TW or computed.
- Contribution margin · if `brand.json` carries gross margin, compute contribution after COGS.
- Cohort retention · if Shopify carries customer cohort data, surface repeat rate per acquisition cohort.

If the operator says *"deep-dive perf"* without scoping → default scope is **last 7d vs prior 7d, all platforms with tokens, global view + campaign-level drill, CPA / ROAS / MER focus**. Announce the default in one sentence, offer one binary correction (*"je pars là-dessus ou tu veux ajuster la période / les plateformes ?"*), proceed silently if the operator validates.

---

## Step 2 · Pull cross-platform insights multi-jour

Pull in parallel via sub-agents when scope is wide (4+ platforms). One sub-agent per platform when the pull exceeds 90 seconds in main thread. Each sub-agent returns a structured payload, never raw API JSON dumped to operator.

**Meta Insights** (always pull when in scope) ·
- Endpoint per `meta-ads.json` `get_insights` · `GET /{ad_account_id}/insights` with `date_preset` or explicit `time_range`.
- Fields · `spend`, `impressions`, `clicks`, `actions`, `cost_per_action_type`, `purchase_roas`, `frequency`, `cpm`, `ctr`, `cost_per_thruplay`.
- Breakdown · `campaign_name`, `adset_name`, `ad_name`, `placement`, `age`, `gender` (one breakdown call per dimension, never combine 3+ breakdowns in one request, Meta API limit).
- Attribution windows · pull `7d_click,1d_view`, `1d_click`, `7d_click` explicitly per request (Meta defaults to 7-click_1d-view, but the gap analysis needs explicit windows).

**Google Ads** (if convention complete + credentials present) ·
- Campaign-type breakdown · Search vs PMAX vs Display vs Shopping (each behaves differently, never blend the four in one number).
- Fields · `cost_micros`, `conversions`, `conversions_value`, `impressions`, `clicks`, `search_impression_share` (Search only), `asset_group_strength` (PMAX only).
- Attribution model used per campaign (data-driven vs last-click), flag if mixed.

**Shopify orders** (always pull when in scope) ·
- Orders within period via Admin API per `shopify.json` convention.
- UTM attribution breakdown · `utm_source`, `utm_medium`, `utm_campaign`, `utm_content` (cross-reference Meta utm_template + Google utm_template per conventions).
- AOV, repeat rate (new vs returning), first-order revenue vs total revenue.

**TripleWhale blended MER** (if convention complete + credentials present) ·
- Blended MER across paid channels for the period.
- nCAC (new customer CAC) if available.
- Pixel-attributed revenue vs blended revenue (the gap between Meta-reported and TW-attributed is signal-rich).

**Klaviyo** (if convention complete + credentials present) ·
- Email + SMS revenue contribution within period (attributed via Klaviyo's own model).
- Flow vs campaign split.
- Subscriber growth in period (acquisition impact downstream).

**TikTok** (if convention complete + credentials present) ·
- Campaign-level spend, impressions, conversions, ROAS reported.
- Creative-level CTR + completion rate (the fatigue signal on TikTok is faster than Meta).

**Pull discipline** ·
- Respect rate limits per convention (Meta ~100k pts/h, sleep 0.5s between heavy calls per `meta-ads.json` `learned_rules`).
- Cache the raw pulls under `brands/{slug}/perf-analysis/_raw/{date}_{platform}.json` for audit trail (silent, never surfaced to operator).
- If a pull fails or partial → flag the gap explicitly in Section 1 Observed, NEVER infer data that was not pulled.

---

## Step 3 · Cross-réf attribution windows

The triangulation is what makes this skill different from a single-platform Meta report. The 3 signal sources MUST be reconciled before diagnosis.

**Three reconciliation pairs canon** ·

**Pair 1 · Meta 7d-click vs Meta 1d-click**
- Gap = view-through + delayed-click contribution.
- Wide gap (7d / 1d > 1.8) → audience has long consideration cycle, OR Meta over-claiming view-through.
- Narrow gap (7d / 1d < 1.2) → audience converts fast OR signal too thin for delayed.
- Surface in Observed section with both numbers, never collapse to one.

**Pair 2 · Meta-reported revenue vs Shopify actual revenue (period-matched)**
- Gap > 30% Meta over Shopify → attribution inflation (last-touch + view-through claiming organic / direct / email revenue).
- Gap > 30% Shopify over Meta → Meta under-reporting (iOS14 signal loss + pixel issues) OR strong organic + email pull.
- Gap < 15% → reasonable alignment, signal trustworthy.
- Surface as confidence modifier on every downstream metric · if gap > 30%, every Meta ROAS / CPA carries a `(confidence moyenne · attribution gap N%)` flag.

**Pair 3 · TW blended MER vs sum-of-platforms ROAS**
- TW blended MER says · "for every euro of total marketing spend, how much revenue came in".
- Sum-of-platforms ROAS adds reported ROAS per platform (double-counts overlapping conversions).
- TW blended is closer to reality on iOS14+ ; sum-of-platforms inflates by 15-30% typical.
- If TW absent · compute proxy blended MER = (Shopify total revenue in period) / (sum of Meta + Google + TikTok spend in period). Flag this is proxy not pixel-attributed.

**iCAC (incremental CAC)** · if external lift study OR holdout test data is available, surface iCAC vs reported CAC gap. If gap > 40% → reported CAC heavily over-claiming incrementality. If absent → flag in Unknown section as a high-value lever (lift study via Meta Conversion Lift or Geo holdout).

---

## Step 4 · Diagnostic 5 sections investigation-posture

The output is structured strictly in 5 sections, in this order. NEVER prose-blend. NEVER skip a section. NEVER reorder.

### Section 1 · Observé (faits sourcés chiffrés)

Format · table or bullet list. Each fact with its source (platform + period + attribution window). Cross-platform numbers grouped.

Example shape ·
```
Observé · pull cross-platform {date_period} (vs {prior_period})

Spend total période · {X} € (Meta {a}€ · Google {b}€ · TikTok {c}€)
  Source · Meta Insights + Google Ads API + TikTok Ads API · time_range pull

Revenue
  · Meta-reported (7d-click_1d-view) · {Y1} € · ROAS {Z1}
  · Shopify actual (UTM-attributed paid) · {Y2} € · ROAS {Z2}
  · TW blended MER · {M}
  · Gap Meta vs Shopify · {gap}% ({direction})

CPA reported
  · Meta · {A1} € (vs {A1_prior} prior period, delta {delta1}%)
  · Google · {A2} €
  · TikTok · {A3} €
  · Blended (Shopify orders / total spend) · {A_blended} €

Creative fatigue indicators (Meta, period)
  · Top spend ad · frequency {F}, CTR decay {decay}% vs first 7d, CPM drift {drift}%
  · {N} ads have frequency > 4 in period

Pas pullé directement (ne pas affirmer) · {platforms not in scope}, lift study data, gross margin if not in brand.json
```

Confidence par item · `sourced` (pull direct API), `derived` (computed from sourced inputs · ex blended MER proxy). Items déduits descendent en Section 2.

### Section 2 · Déduit (hypothèses avec confidence chain)

Each hypothesis presented as a question to the operator, with explicit confidence and converging / diverging indicators.

Example shape ·
```
Déduit · {N} hypothèses à valider

H1 · Creative fatigue sur l'ad principale {ad_name} explique le drop ROAS
  Confidence · moyenne
  Indicateurs · frequency 5.2 (vs 2.1 prior period) · CTR -45% sur 14j · CPM +28%
  À valider · Tu confirmes que cette ad porte le gros du spend ? Y a-t-il des nouvelles créa en cours ?

H2 · Attribution gap Meta vs Shopify s'élargit (signal pixel + iOS14)
  Confidence · forte
  Indicateurs · gap passé de 18% à 42% en 30j · revenue Shopify stable mais Meta-reported -22%
  À valider · CAPI events bien reçus ? Domain verification toujours OK ?

H3 · Audience saturation sur l'audience principale {audience}
  Confidence · TRÈS faible (intuition modèle sur reach curve, zéro data audience overlap)
  Indicateurs · reach cumulé {R} sur taille audience estimée {T}
  À valider · OBLIGATOIREMENT via Meta Audience Insights overlap + cohort analysis avant de baser une décision dessus.

H4 · Seasonality (post-pic saisonnier)
  Confidence · faible / projection
  Indicateurs · période en cours = J+14 après peak {event}, baseline historique {pattern}
  À valider · Y a-t-il un historique de saisonnalité encodé dans learnings.json sur cette brand ?
```

Confidence chain canon · `forte` (5+ convergents), `moyenne` (3-5 convergents), `faible` (1-2 partiels), `TRÈS faible` (intuition modèle sans support externe).

### Section 3 · Inconnu (variables non observables)

Explicit list of variables that decide the diagnostic but are not accessible from the data pulled. Never guess these, list them explicitly.

Example shape ·
```
Inconnu · {N} variables à creuser avant décision budget

1. Audience overlap entre Meta campaigns · pas accessible via API standard → Meta Audience Insights manual scan OU custom audience overlap report
2. Gross margin réelle (vs assumé 30%) → operator capture
3. Lift study / iCAC réel → Meta Conversion Lift OR Geo holdout test (~2 semaines)
4. Creative LTV (quel creative ramène quel cohort qualité) → Shopify cohort par UTM + LTV30/60/90
5. Compétitif paid (CPM market drift) → Meta Ads Library + benchmark sector
6. External macros (CPM trend platform-wide, iOS update impact) → public benchmarks
```

### Section 4 · Leviers (skills / actions ranked impact × effort)

Recos ranked, NOT exhaustive dump. Matrix impact × effort. Each lever names a skill, an action, or a source.

Example shape ·
```
Leviers · {N} axes ranked

Quick wins (impact moyen · effort faible)
  L1 · Pause les {N} ads avec frequency > 4 et CTR-decay > 30% → recompose-creative sur top 3 angles validés
       (action interne · 30 min · arrête la fuite immédiate)
  L2 · Vérifier CAPI dedup rate → audit-meta-account focus Block 1 Pixel
       (action interne · 15 min · répare l'attribution gap si dedup cassé)

Medium effort high impact (impact fort · effort moyen)
  L3 · Lancer 3 nouveaux creative tests sur {top_validated_angle} → produce-paid-angles + compose-creative
       (action interne · 2-3 jours setup + 7-14j test · refresh la flotte créative)
  L4 · Scaffold NEW audience extension {audience_underexplored} → scaffold-extension audience
       (action interne · 1-2 jours setup + 14-21j validation · ouvre nouvelle veine)

Heavy lift high impact (impact fort · effort fort)
  L5 · Lancer une lift study Conversion Lift Meta → flag à l'opérateur, ROI sur 6 mois
       (action externe · 2 semaines · lève iCAC réel, calibre budget réel)
```

NEVER more than 3 levers per impact band. NEVER mix levels in a flat list. The ranking IS the deliverable.

### Section 5 · Close ouvert (UNE question macro)

The output ends with ONE macro question on which axis to drill first. NEVER a flat menu of 4 levers. NEVER *"Want anything else?"*. The operator arbitrates.

Example shape ·
```
On a {N} axes d'investigation. Pour la suite de ton diagnostic, lequel veux-tu creuser en priorité ?

A · Quick wins (L1+L2 · ~45 min · arrête la fuite + répare attribution)
B · Refresh créatif (L3 via produce-paid-angles + compose-creative · setup 2-3j · vague nouveau)
C · Nouvelle audience (L4 via scaffold-extension · setup 1-2j · ouvre veine inexploitée)
D · Lift study (L5 · 2 semaines · lève iCAC réel · décision budget propre)

Reco macro · A en premier (arrête la fuite immédiate), puis B (refresh la flotte sur 7-14j). C et D arbitrent en fonction du résultat A+B.
```

The operator says `A` or `A+B` or other, the agent enchaînes via Task tool sur le skill correspondant. NEVER prose-improvise a creative brief after an analyze-perf · invoke `produce-paid-angles` ou `compose-creative` per skill-routing-discipline.

---

## Step 5 · Persist diagnostic file

Write the full diagnostic to `brands/{slug}/perf-analysis/{YYYY-MM-DD}_analyze-perf.md`. Mode `proposed` per `write_to_context` gate (the file is a diagnostic artifact, not a mutation of canon entities, but the path is encoded in permissions).

File shape ·
```
# Perf analysis · {brand_name} · {date_period}

> Pull cross-platform {date_period_iso} (vs {prior_period_iso}) · scope {platforms in scope} · lens {lens}

## Section 1 · Observé
{table / bullets per Step 4 Section 1}

## Section 2 · Déduit
{hypotheses per Step 4 Section 2}

## Section 3 · Inconnu
{variables per Step 4 Section 3}

## Section 4 · Leviers
{ranked recos per Step 4 Section 4}

## Section 5 · Close ouvert
{macro question + reco}

---

_Raw pulls cached under `brands/{slug}/perf-analysis/_raw/`. Conventions consumed · {list}. Generated by analyze-perf v1.0.0 on {timestamp}._
```

Silent write. Surface to operator · *"Diagnostic persisté sous `brands/{slug}/perf-analysis/{date}_analyze-perf.md`. {Section 5 macro question rappel}"*.

If `learnings.json` has zero entries on perf patterns AND a hypothesis with confidence forte emerged in Section 2 → propose `capture-learning` post-hoc as a backup path. Never auto-trigger.

---

## Hard Rules

**HR1 · Investigation-posture 5 sections obligatoire.** Tout output analyze-perf DOIT structurer en Observé / Déduit / Inconnu / Leviers / Close ouvert. Pas de prose mélangée. Pas de section skippée. Pas de réordering. Violation = bug skill, retry with explicit structure.

**HR2 · Confidence chain explicit.** Chaque hypothèse en Section 2 DOIT porter une étiquette `forte / moyenne / faible / TRÈS faible`. NEVER affirmer une hypothèse sans confidence. NEVER une hypothèse `TRÈS faible` ne peut servir de fondation à une décision budget · l'opérateur doit savoir explicitement quand on est sur du sable.

**HR3 · Cross-platform triangulation minimum 2 sources.** Le diagnostic ne ship JAMAIS sur Meta-only. Minimum · Meta + Shopify (attribution gap réel). Si Shopify absent → flag explicite Step 0 et offrir bridge. La triangulation est ce qui distingue analyze-perf de "lis ce que dit Meta Ads Manager".

**HR4 · Recos ranked impact × effort matrix · pas dump exhaustif.** Section 4 organise les leviers par bands (Quick wins · Medium · Heavy lift). Maximum 3 par band. JAMAIS un flat dump de 10 actions. Le ranking IS the deliverable.

**HR5 · Pre-emption.** "ROAS drop est rarement creative-only." Le skill DOIT toujours vérifier en parallèle · creative fatigue (frequency + CTR decay + CPM drift), audience saturation (reach curve + LAL freshness), attribution shift (Meta vs Shopify gap drift), seasonality (period vs historical baseline). Présenter Quick reco "change ta créa" sans avoir checké les 3 autres = bug. Présenter 1 cause comme certaine quand 3 hypothèses convergent = bug.

**HR6 · NEVER affirmation as fact on inferred data.** Le pull data API est `sourced`. La synthèse en Section 1 est `sourced` ou `derived` (clear marking). Toute affirmation en Section 2 porte explicitly son confidence level. Toute variable non pullée descend en Section 3 Inconnu. JAMAIS un fait sourcé mélangé avec une hypothèse moyenne dans la même phrase prose.

**HR7 · Sub-agent delegation when scope wide.** Si scope ≥ 4 plateformes OU pull total > 90 secondes attendu → délégation parallèle via Task tool, un sub-agent Sonnet par plateforme. Le main thread synthétise les payloads retournés, NEVER dump raw API JSON to operator. Cap parallèle 5 sub-agents per delegation-pattern.md.

**HR8 · Operator-facing language strict.** NEVER expose internal labels (`time_range`, `breakdowns`, `purchase_roas`, `cost_per_action_type`, JSON field paths) to the operator. Translate to plain language ("revenue Meta-reported", "CPA Meta", "frequency moyenne par ad"). NEVER expose internal codes (`META_ACCESS_TOKEN`, `MCP server`, `convention file`). NEVER zero em-dash (use period, parentheses, comma, two sentences, or middle dot ·).

---

## Anti-patterns

**AP-1 · Diagnostic Meta-only sans cross-platform.** Pulling Meta Insights + producing a CPA / ROAS verdict without checking Shopify actuals OR TW blended. The skill is precisely there to triangulate · Meta-only = use Meta Ads Manager directly.

**AP-2 · Synthèse complète sans drill-down.** Closing with *"Voici le diagnostic complet, voici les recos, à toi de jouer."* Violates Section 5 canon · the agent ALWAYS opens the door with ONE macro question, never closes with a complete synthesis.

**AP-3 · Ignore attribution window.** Pulling Meta default attribution (7d-click_1d-view) and treating it as ground truth without checking 1d-click + Shopify actual. Attribution gap is signal-rich · ignoring it = bug.

**AP-4 · Reco "change ta créa" sans vérifier 3 autres.** Pre-emption HR5 violation. ROAS drop = check 4 axes in parallel (creative · audience · attribution · seasonality). NEVER one-cause verdict.

**AP-5 · Flat dump of recommendations.** Section 4 should rank by impact × effort. A flat list of 8 actions = noise. Operator wants ONE priority axis (Quick wins arrête la fuite), not 8 todos.

**AP-6 · Improvisation prose vs skill execution downstream.** Operator validates lever B (refresh créatif) post-diagnostic. The agent prose-improvises 5 angles. Violation of skill-routing-discipline · invoke `produce-paid-angles` via Task tool, never freestyle.

**AP-7 · Persist sans surface macro question.** Writing the file under `brands/{slug}/perf-analysis/` silently and saying *"Diagnostic done."* without surfacing the Section 5 macro question. The operator must know WHERE to drill next, the persisted file is the audit trail not the operator interface.

---

## Cross-refs canon

- **`docs/system/investigation-posture.md`** · master doctrine, 5 sections canon obligatoire, confidence chain canon, anti-patterns AP-1 to AP-7 (extended here with AP-4 to AP-7 specific to perf domain).
- **`routine-perf` (sister skill)** · briefing quotidien rapide (J-1, ~5 min, flag binaire anomalies). When operator triggers *"brief perf"* or *"check perf"* (no "deep-dive" signal) → route routine-perf. When operator triggers *"ROAS drop"*, *"creuse la perf"*, *"audit 30j"* → route analyze-perf.
- **`audit-meta-account` (sister skill)** · audit SETUP health (pixel, CAPI, structure, naming, attribution config). When operator triggers *"audit Meta"*, *"check ma config Meta"* → route audit-meta-account. When operator triggers *"ROAS drop"*, *"perf paid"* → route analyze-perf. The two skills can chain · analyze-perf flags an attribution gap signal → reco lever points to audit-meta-account Block 1 Pixel.
- **`import-meta-results`** · pulls raw data + writes canon validations[]. analyze-perf consumes data already imported via this skill OR pulls it as side-effect. The two are NOT redundant · import-meta-results is the data layer ingestion, analyze-perf is the diagnostic layer on top.
- **`skill-routing-doctrine.md`** · NEVER prose-improvise downstream from an analyze-perf diagnostic. Lever validated by operator → invoke the corresponding skill via Task tool (`produce-paid-angles`, `compose-creative`, `recompose-creative`, `scaffold-extension`, `audit-meta-account`).
- **`docs/system/canonical-matrix-reasoning.md`** · the internal matrix (delivery metric × attribution window × time slice × dimension) is CMR-compliant · canon axes drawn from `meta-ads.json` + `google-ads.json` conventions, schema-grounded, combinatorial reasoning internal, synthesis canon-anchored in 5 sections.
- **`docs/system/contract-build.md`** · the skill is type `producer`, layer `production`, subagent_safe true · respects the orchestration gate when the operator chains analyze-perf → produce-paid-angles → compose-creative downstream.
- **`resources/conventions/meta-ads.json` · `google-ads.json` · `triplewhale.json` · `shopify.json` · `klaviyo.json` · `tiktok-ads.json`** · consumed per Step 0 + Step 2 pull discipline. If a convention is incomplete for a platform in scope, Gate doc blocks execution.
