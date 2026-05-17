---
name: audit-google-pmax
type: orchestrator
version: "1.0.0"
recommended_model: sonnet
isolation_scope: brand
layer: production
description: >
  Audit complet PMAX (Performance Max) campaigns Google Ads. Couvre asset
  group score, audience signals, search themes, listing groups, conversion
  config, brand exclusions, value rules, negative keywords portfolio,
  account-level vs campaign-level conversions setup. Output 5 sections
  investigation-posture (Observé, Déduit, Inconnu, Leviers, Close).
  Step 0 bridge proactif canon v2.77 si Google Ads token absent.
  FR: "audit Google Ads", "audit PMAX", "check Performance Max", "audit Google".
  EN: "audit Google Ads", "audit PMAX", "Performance Max audit", "Google audit".
permissions:
  reads: ["brands/{slug}/", "resources/conventions/google-ads.json"]
  writes: ["brands/{slug}/audits/{date}_audit-google-pmax.md"]
  mode: interactive
  subagent_safe: true
extension_hooks:
  consumable_by: ["brand_entity"]
disambiguates_against:
  - "audit-meta-account : audit setup compte Meta (structure + delivery) vs audit-google-pmax : audit PMAX campaigns Google Ads spécifique."
  - "analyze-perf : diagnostic cross-platform multi-plateforme vs audit-google-pmax : audit setup Google PMAX spécifique."
  - "routine-perf : briefing quotidien rapide cross-platform vs audit-google-pmax : audit setup deep-dive Google PMAX."
---

# Skill: audit-google-pmax

Senior Google Ads media buyer PMAX deep-dive. Observational findings, not blame. Couvre les 7 dimensions canon PMAX (asset groups, audience signals, search themes, listing groups, value rules, brand exclusions, conversion config) + account-level (conversion goals, attribution, bidding learning state). Zero questionnaire format quand l'API est joignable.

## Expert methodology

**Canonical expert persona**: senior Google Ads strategist / PMAX specialist (10+ years), spécialisé sur compte e-commerce DTC.

**Framework**: 5-block diagnostic + investigation-posture canon (5 sections).

**Matrix** (applied to each block): *finding status (OK / Warning / Issue) × operational impact × recommended action*.

**Key variables**: asset group strength score, audience signals composition (1P/custom/demo), search themes (positive + negative), listing groups granularity, value rules count, brand exclusions list maintenance, conversion goals (primary vs secondary), attribution model, bidding strategy alignment, learning period state.

**Codified reference**: `resources/conventions/google-ads.json` must be present + complete (rate limits, OAuth scopes, endpoint patterns, GAQL operations, learned_rules). Si incomplet, Gate doc bloque execution.

---

## Step 0 · Gate access check (MANDATORY, bridge proactif canon v2.77)

**CRITICAL:** check Google Ads API access BEFORE starting the audit. **NEVER** fall back to questionnaire silently.

1. Read `brands/{slug}/credentials.env` (brand-specific) AND `credentials_shared.env` (workspace root). Look for: `GOOGLE_ADS_DEVELOPER_TOKEN`, `GOOGLE_ADS_CLIENT_ID`, `GOOGLE_ADS_CLIENT_SECRET`, `GOOGLE_ADS_REFRESH_TOKEN`, `GOOGLE_ADS_LOGIN_CUSTOMER_ID`, `GOOGLE_ADS_CUSTOMER_ID`.
2. Read `resources/conventions/google-ads.json`. Check `access.credential_keys`, `rate_limits`, `operations`, `learned_rules`. Si incomplete ou missing : Gate doc first (WebFetch official Google Ads API doc, fill convention) avant any API call.

**Branching** (AskUserQuestion canon si token absent) :

- **Token + customer_id + developer_token present + convention complete** : announce API mode, proceed Step 1.
  > *"API access OK pour {brand}. Je pull les données PMAX depuis Google Ads. 3-5 min, retour avec l'audit."*

- **Token absent** : AskUserQuestion canon 2 options :
  - (a) "Je te guide pour connecter Google Ads maintenant via connect-source (5 min, one-time, audits futurs instantanés et factuels)."
  - (b) "Je bascule en mode declarative interview (tu me donnes les données à la voix ou screenshots, je structure). Plus lent, dépend de ta mémoire du setup."

Default proactif proactif : (a) si l'opérateur a 5 min, sinon (b) sans bloquer.

---

## Step 1 · Account-level checks (API mode)

Read `brands/{slug}/brand.json` for name, language, stage. Read `platforms.google_ads` config si existant.

Pull via Google Ads API (respect rate limits convention, GAQL endpoints) :

**1.1 Conversion goals setup**
- GAQL : `SELECT customer_conversion_goal.category, customer_conversion_goal.origin, customer_conversion_goal.biddable FROM customer_conversion_goal`
- Check : 1 primary goal (purchase canonique e-commerce) + N secondary goals (ATC, view product, lead form).
- Issue si : >1 primary, ou purchase pas primary, ou secondary goals biddable=true sans intent.

**1.2 Attribution model**
- GAQL : `SELECT conversion_action.name, conversion_action.attribution_model_settings.attribution_model FROM conversion_action`
- Check : data-driven (recommandé si >300 conv/30j), vs last-click (legacy fallback), vs position-based.
- Issue si : last-click sur compte mature (>300 conv) avec data-driven dispo non-activé.

**1.3 Conversion setup (account-level vs campaign-level)**
- GAQL : `SELECT campaign.id, campaign.name, campaign.selective_optimization.conversion_actions FROM campaign WHERE campaign.advertising_channel_type = 'PERFORMANCE_MAX'`
- Check : account-level conversions = stratégie portfolio (recommandé default). Campaign-level conversions = test isolated (sous-conversion specific).
- Issue si : mix account-level + campaign-level sans intent documenté → confusion smart bidding signal.

**1.4 GA4 import + value adjustment**
- GAQL : `SELECT conversion_action.type, conversion_action.value_settings.default_value FROM conversion_action`
- Check : GA4 events importés (purchase, add_to_cart) + dynamic value (revenue) tracked. Static value = warning si e-commerce.

**1.5 Audience manager (1P data)**
- GAQL : `SELECT user_list.name, user_list.size_for_display, user_list.membership_status FROM user_list`
- Check : custom segments présents, 1P data lists (customer match, website visitors), retention period.
- Issue si : zéro 1P data list, custom segments seulement (signal qualité dégradé).

---

## Step 2 · Campaign-level PMAX audit

Pour chaque PMAX campaign active (`advertising_channel_type = PERFORMANCE_MAX`, `status IN ('ENABLED', 'PAUSED')`) :

**2.1 Asset groups**
- GAQL : `SELECT asset_group.id, asset_group.name, asset_group.status, asset_group.ad_strength FROM asset_group WHERE campaign.id = {id}`
- Check : count par campaign (canon : 1-3 asset groups par PMAX, thematic clusters distinct). Naming convention align convention `{LANG}-{Theme}`.
- Issue si : >5 asset groups par campaign (fragmentation budget) ou 1 seul (manque thematic differentiation).

**2.2 Asset group strength score**
- Field : `asset_group.ad_strength` (enum : POOR, AVERAGE, GOOD, EXCELLENT).
- Seuils canon : EXCELLENT (toutes assets max + variety), GOOD (80-100% filled), AVERAGE (60-80%), POOR (<60%).
- Issue si : POOR ou AVERAGE → 50% perf reach reduction observée. Action : compléter assets jusqu'à GOOD minimum.

**2.3 Listing groups (Shopping integration)**
- GAQL : `SELECT asset_group_listing_group_filter.case_value, asset_group_listing_group_filter.path FROM asset_group_listing_group_filter WHERE asset_group.id = {id}`
- Check : product grouping strategy (full catalog default vs custom segmentation par margin/category/perf).
- Issue si : full catalog sans exclusion produits loss-leader ou stock zéro.

**2.4 Search themes**
- GAQL : `SELECT campaign_search_term_insight.category_label FROM campaign_search_term_insight` (insight only, search themes set via Google Ads UI ou API mutation).
- Check : positive search themes (3-10 themes thematic), negative search themes (brand keywords, competitor brands, irrelevant intent, 20-50 negatives minimum).
- Issue si : zéro negative search themes → spend gaspillé sur intent off-target.

**2.5 Audience signals**
- GAQL : `SELECT asset_group_signal.audience FROM asset_group_signal WHERE asset_group.id = {id}`
- Check composition canon : 1P data 80% poids (customer match, website visitors, purchasers), custom segments 15% (search intent + URL visited), demographics 5% (age, gender, household income).
- Issue si : 1P data absent OU demographics-only audience signal (signal qualité faible).

**2.6 Brand exclusions**
- GAQL : `SELECT campaign.brand_safety_suitability, campaign_criterion.brand_list FROM campaign WHERE advertising_channel_type = 'PERFORMANCE_MAX'`
- Check : brand list maintained (own brand + variants + competitor brands), exclusions actives au campaign-level.
- Issue si : brand exclusions absentes (cannibalisation Search Brand campaign, spend gaspillé sur traffic owned).

**2.7 Value rules**
- GAQL : `SELECT conversion_value_rule.geo_location_condition, conversion_value_rule.device_condition, conversion_value_rule.audience_condition, conversion_value_rule.action FROM conversion_value_rule`
- Check : value rules par location (FR core market modifier +20%), device (mobile/desktop), audience (existing customer +/-30%).
- Issue si : zéro value rules sur compte mature avec target ROAS bidding (signal granularity perdu).

---

## Step 3 · Asset audit per asset group

Pour chaque asset group (limit top-3 plus actifs par campaign) :

- GAQL : `SELECT asset.id, asset.type, asset.text_asset.text, asset.image_asset.full_size.url FROM asset_group_asset WHERE asset_group.id = {id}`

Check assets count + variety par asset group :

| Asset type | Count canon | Issue threshold |
|---|---|---|
| Headlines (30 char max) | 5-15 | <5 = POOR strength penalty |
| Long headlines (90 char max) | 1-5 | 0 = warning |
| Descriptions (90 char max) | 1-5 | <2 = AVERAGE strength |
| Images (multiple ratios) | 1-20 | <3 = warning, no square = issue |
| Videos (10-30s recommended) | 0-5 | 0 = Google auto-generates (low quality) |
| Logos (square + landscape) | 1-5 | 0 logo landscape = issue placement |
| Sitelinks | 2-10 (campaign level) | <4 = warning |
| Callouts | 2-10 (campaign level) | <4 = warning |
| Structured snippets | 0-10 (campaign level) | optional |

Issue si : video absent (Google auto-genère depuis static = low quality) OU images <3 OU headlines <5.

---

## Step 4 · Conversion + bidding alignment

**4.1 Bidding strategy alignment stage business**

- GAQL : `SELECT campaign.bidding_strategy_type, campaign.maximize_conversions.target_cpa_micros, campaign.maximize_conversion_value.target_roas FROM campaign`

| Stade business | Bidding canon | Issue si |
|---|---|---|
| Stade 0 (<30 conv/30j) | Maximize Conversions (no target) | Target CPA/ROAS activé prématurément = no learning |
| Stade 1 (30-50 conv/30j) | Target CPA | Toujours Maximize Conversions sans target = volatilité |
| Stade 2 (>50 conv/30j) | Target ROAS | Target CPA persistant = perte d'optimisation value |

**4.2 Conversion lag setup**
- GAQL : `SELECT conversion_action.click_through_lookback_window_days, conversion_action.view_through_lookback_window_days FROM conversion_action`
- Check : click-through window 30-90j (default e-commerce), view-through 1-30j.
- Issue si : click-through <14j sur cycle achat considéré (>200€ AOV).

**4.3 Smart bidding learning period state**
- GAQL : `SELECT campaign.bidding_strategy_system_status FROM campaign WHERE advertising_channel_type = 'PERFORMANCE_MAX'`
- Check : status enum (LEARNING_NEW, LEARNING_BUDGET_CHANGE, LEARNING_BID_CHANGE, LEARNING_CONVERSION_TYPE_CHANGE, LEARNING_COMPOSITION_CHANGE, LIMITED_BY_BUDGET, MISCONFIGURED).
- Issue si : LEARNING_BID_CHANGE ou LEARNING_BUDGET_CHANGE actif >7j (sous-optimisation). Anti-pattern : changer bid strategy pendant learning = reset 7j.

---

## Step 5 · Output (5 sections investigation-posture canon)

Structure obligatoire (`docs/system/investigation-posture.md`) :

### Section 1 · Observé (faits sourcés API)

Format : table ou liste à puces. Chaque fait avec sa source (GAQL endpoint utilisé, snapshot date).

```
Observé · API pull Google Ads {customer_id} (YYYY-MM-DD)

- Conversion goals · {N primary} + {N secondary} (source : customer_conversion_goal)
- Attribution model · {model} (source : conversion_action.attribution_model_settings)
- PMAX campaigns actives · {N} (source : campaign.advertising_channel_type)
- Asset groups · {N total}, strength : {N EXCELLENT, N GOOD, N AVERAGE, N POOR}
- Audience signals · 1P data : {present/absent}, custom segments : {N}, demographics : {present/absent}
- Negative search themes · {N} (source : campaign_criterion.negative)
- Brand exclusions · {N entries} OR absent
- Value rules · {N} OR absent
- Bidding strategy actuelle · {strategy} (target = {value})
- Learning state · {LEARNING_* / running normal / LIMITED_BY_BUDGET}

Pas observé directement (ne pas affirmer) : qualité créative individuelle assets (jugement humain), search themes positifs sourcés (insight-only via API).
```

### Section 2 · Déduit (hypothèses confidence chain)

Chaque hypothèse présentée comme question opérateur, confidence + indicateurs explicites.

```
Déduit · {N} hypothèses à valider

H1 · {Finding example : asset group strength POOR plafonne reach 50%}
  Confidence · forte (5 indicateurs convergents : strength score POOR + assets count <seuils + learning state stable + delivery limited)
  Indicateurs · {liste sourcée}
  À valider · {question opérateur ouverte}

H2 · {Finding example : bidding strategy mismatch stade business}
  Confidence · moyenne (3 indicateurs : volume conv mensuel + target activé + variance ROAS)
  Indicateurs · {liste}
  À valider · {question}
```

### Section 3 · Inconnu (variables non observables)

```
Inconnu · {N} variables à creuser

1. Qualité créative assets individuelles (jugement humain) → review manuelle ou compose-creative
2. Search themes positifs configurés (API insight-only) → operator screenshot Google Ads UI
3. Stratégie portfolio account-level vs PMAX-spécifique → operator capture
4. Historique reset learning (changements bid récents) → operator capture timeline
```

### Section 4 · Leviers (drill-down options)

```
Leviers · {N} axes d'investigation prioritaires

Axe A · Asset strength uplift (lève H1)
  → compose-creative ou import-asset pour combler gaps assets
  → re-audit dans 14j post-mise à jour

Axe B · Bidding alignment (lève H2)
  → switch bid strategy + monitoring learning period 7j
  → audit re-check post-learning
```

### Section 5 · Close ouvert (UNE question macro)

```
{N} findings sur le PMAX. Pour ton plan d'action, lequel veux-tu creuser en priorité ?

A · Asset strength uplift ({impact summary})
B · Bidding alignment ({impact summary})
C · Audience signals composition ({impact summary})
D · Brand exclusions + negative search themes ({impact summary})

Reco macro · {A/B/C/D + rationale 1 ligne basé sévérité issues et stage business}.
```

### Persist audit file

Output archive : `brands/{slug}/audits/{YYYY-MM-DD}_audit-google-pmax.md` (markdown complet 5 sections + raw findings par block).

---

## Hard Rules

1. **NEVER** audit sans Step 0 access gate proactif canon v2.77. AskUserQuestion 2 options si token absent, JAMAIS questionnaire fallback silent.
2. **NEVER** affirmer une hypothèse comme un fait. Confidence chain explicit (forte/moyenne/faible/TRÈS faible) sur chaque finding Section 2.
3. **NEVER** présenter audience signals composition sans cross-référence 1P data 80% / custom 15% / demo 5% canon convention.
4. **NEVER** valider bid strategy sans cross-référence stade business (conv/30j). Maximize Conversions stade 0, Target CPA stade 1, Target ROAS stade 2.
5. **NEVER** clôturer audit sans Section 5 Close ouvert (UNE question macro). Opérateur arbitre drill-down, l'agent JAMAIS conclut unilatéralement.
6. **ALWAYS** persist audit final markdown dans `brands/{slug}/audits/{YYYY-MM-DD}_audit-google-pmax.md` (timestamped, append-only history).
7. **ALWAYS** flag learning state LEARNING_* actif >7j comme Issue (sous-optimisation, reset implicit du bidding).

---

## Anti-patterns

- **AP-1 · Audit superficiel sans asset group strength** : ignorer le `ad_strength` field PMAX = miss 50% du diagnostic (strength POOR plafonne reach 50%).
- **AP-2 · Ignore brand exclusions** : auditer PMAX sans check brand list maintenance = miss cannibalisation Search Brand + spend owned-traffic gaspillé.
- **AP-3 · Ignore negative search themes** : auditer PMAX sans cartographier negatives (brand + competitor + irrelevant) = miss 20-50% spend off-target.
- **AP-4 · Bidding alignment without stage** : recommander Target ROAS sur compte <50 conv/30j = no learning, volatility, perte budget.
- **AP-5 · Conclusion unilatérale sans close** : output audit complet "voici les actions" sans Section 5 question macro = ferme drill-down opérateur, violation investigation-posture canon.

---

## Cross-refs

- Master · `docs/system/contextual-intelligence.md` (master doctrine PhantomOS)
- Investigation posture · `docs/system/investigation-posture.md` (5 sections canon)
- Connectivity layering · `docs/system/connectivity-layering.md` (Layer 2 API Google Ads via skill)
- Skill sœur Meta · `.skills/skills/audit-meta-account/SKILL.md` (pattern miroir audit paid platform)
- Skill consumer perf · `.skills/skills/analyze-perf/SKILL.md` (drill-down post-audit possible)
- Convention · `resources/conventions/google-ads.json` (operations GAQL + learned_rules + rate_limits)
- Connect source · `.skills/skills/connect-source/SKILL.md` (Step 0 branching token absent fallback (a))
