---
name: routine-perf
type: navigator
version: "1.0.0"
recommended_model: sonnet
isolation_scope: brand
layer: production
description: >
  Briefing perf paid quotidien (2-3x/jour). Lit J-1 insights par account
  cross-plateformes (Meta + Google + Shopify + TripleWhale conv shippée),
  flags pacing curve, ROAS drop, frequency saturation, CPM drift, creative
  fatigue signals. Output 5 sections investigation-posture (Observé, Déduit,
  Inconnu, Leviers, Close ouvert) format founder-facing Slack/voix-friendly.
  Step 0 bridge proactif canon v2.77 (si MCP/token absent, AskUserQuestion
  guidage connect-mcp-server OR fallback declarative interview).
  FR: "fais la routine perf", "brief perf du jour", "pacing check",
      "où on en est aujourd'hui", "briefing perf".
  EN: "perf routine", "perf brief", "pacing check", "where are we today",
      "performance briefing".
permissions:
  reads: [brand, learning, strategy]
  writes: []
  mode: interactive
  subagent_safe: true
extension_hooks:
  consumable_by: ["brand_entity", "creative_entity"]
disambiguates_against:
  audit-meta-account: "audit-meta-account audite le setup health du compte Meta (config + structure + pixel + attribution). routine-perf brief la perf quotidienne (delivery + signal alert sur insights J-1)."
  analyze-perf: "analyze-perf deep-dive diagnostic cross-platform multi-jour avec recos stratégiques. routine-perf pull rapide briefing court 5 min cadence quotidienne."
  brief-day: "brief-day oriente l'opérateur sur l'état du brand (Identité + Inventaire + Atlas vivant). routine-perf focalisé spécifiquement sur l'état perf paid quotidien (insights J-1 + signaux alerte)."
pipeline:
  preconditions: brands/{slug}/brand.json exists ; credentials Meta/Google/Shopify/TW dropés en partie ou totalité dans credentials_shared.env OR brands/{slug}/credentials.env
  postconditions: si flag critique détecté, agent propose chain vers analyze-perf (deep-dive) ou audit-meta-account (si setup issue suspecte) ou recompose-creative (si fatigue creative)
---

# Skill: routine-perf

Briefing perf paid quotidien founder-facing. Cadence 2-3x/jour. Pull rapide J-1 insights cross-plateformes (Meta + Google + Shopify + TripleWhale si dispo), compute signals canon avec seuils chiffrés (pacing, frequency, CPM drift, ROAS, fatigue), retourne 5 sections investigation-posture format Slack/voix-friendly. Pas verbose, pas exhaustif. Briefing court actionnable.

## Expert methodology

**Canonical expert persona**: senior media buyer 7-fig running daily pacing routines, founder-facing chairman briefing posture.

**Framework**: 5-signal compute canon (pacing curve, frequency saturation, CPM drift, ROAS drop, creative fatigue) × J-1 cross-platform insights × investigation-posture 5 sections.

**Matrix** (applied to each signal): *threshold canon × current state × directional read (OK / Watch / Flag) × suggested next move*.

**Codified reference**: `resources/conventions/meta-ads.json` (Meta Insights endpoints + rate limits + learned_rules), `resources/conventions/google-ads.json` (GAQL search query patterns + cost_micros), `resources/conventions/shopify.json` (orders endpoints + AOV), `resources/conventions/triplewhale.json` (blended MER cross-channel). Si convention incomplète, Gate doc canon avant call.

---

## Step 0 · Gate access + bridge proactif canon v2.77 (MANDATORY)

**CRITICAL:** verify connectivity AVANT de pull. **NEVER** silently fail on missing token. **NEVER** improvise un brief sans data sourcée.

1. **Layer 1 MCP check.** Verify `facebook-graph` MCP connected via `claude mcp list`. Required for Meta Insights pull.
2. **Layer 2 credentials check.** Read `credentials_shared.env` (workspace) + `brands/{slug}/credentials.env` (brand-specific). Required keys per platform:
   - Meta: `META_ACCESS_TOKEN` + `META_AD_ACCOUNT_ID`
   - Google Ads: `GOOGLE_ADS_DEVELOPER_TOKEN` + `GOOGLE_ADS_REFRESH_TOKEN` + `GOOGLE_ADS_CUSTOMER_ID`
   - Shopify: `SHOPIFY_ADMIN_API_TOKEN` + `SHOPIFY_STORE_DOMAIN`
   - TripleWhale: `TRIPLEWHALE_API_KEY` + `TRIPLEWHALE_SHOP_ID`
3. **Convention check.** Read `resources/conventions/{meta-ads,google-ads,shopify,triplewhale}.json`. Si missing OR incomplete, Gate doc canon (WebFetch official doc, fill convention) avant tout call.

**Branching canon proactif v2.77** (AskUserQuestion via `ToolSearch(select:AskUserQuestion)`):

- **Tous tokens présents + MCP connecté** → announce, proceed Step 1A:
  > *"Connectivité OK. Je pull J-1 insights Meta + Google + Shopify + TW. 2-3 min, je reviens avec le briefing."*

- **Partiel** (e.g. Meta OK, Google manquant) → annonce coverage, proceed avec ce qui est dispo, flag explicit gap dans Section 1 Observé:
  > *"Meta + Shopify branchés. Google Ads + TW non-connectés. Je brief sur ce qu'on a, je flag les blind spots."*

- **Aucun token / MCP absent** → AskUserQuestion 2 options:
  - (a) "Je te guide pour connecter Meta maintenant (~2 min via connect-mcp-server). Briefing devient factuel et future routine est instant."
  - (b) "Je bascule en mode declarative interview (tu me donnes les chiffres clés à la voix, je structure)."
  
  **Default proactif proactif** · proposer (a) en premier si l'opérateur a le temps, fallback (b) si urgence briefing immediat.

---

## Step 1A · Pull J-1 insights cross-plateformes (API mode)

Read `brands/{slug}/brand.json` for: brand name, language, stage, current strategy focus (`strategy.json` si dispo pour MER targets par stage).

Pull en parallèle (respect rate limits conventions):

**1. Meta Ads** (facebook-graph MCP):
- Endpoint: `GET /{ad_account_id}/insights`
- Params: `fields=spend,impressions,clicks,actions,cost_per_action_type,purchase_roas,frequency,cpm,ctr&date_preset=yesterday&breakdowns=action_type` (puis variants `age_gender` et `publisher_platform` si granular needed)
- Aggregation: spend total, ROAS purchase, frequency max par adset, CPM moyen, top 3 ads par spend

**2. Google Ads** (Layer 2 API):
- Query GAQL: `SELECT campaign.id, campaign.name, campaign.advertising_channel_type, metrics.cost_micros, metrics.conversions, metrics.conversions_value, metrics.impressions, metrics.clicks FROM campaign WHERE segments.date DURING YESTERDAY`
- Split par advertising_channel_type: SEARCH vs PERFORMANCE_MAX
- Compute: cost (cost_micros / 1M), ROAS (conversions_value / cost), conversions count

**3. Shopify** (Layer 2 API):
- Endpoint: `GET /admin/api/{version}/orders.json?financial_status=paid&created_at_min={yesterday_start}&created_at_max={yesterday_end}&limit=250`
- Aggregation: orders count, revenue total, AOV (revenue / orders count), top UTM sources si attribution UTM-tagged

**4. TripleWhale** (Layer 2 API, si shippé):
- Endpoint: `POST /api/v2/tw-metrics/metrics-data`
- Params: `{ shop, start: yesterday, end: yesterday, metrics: ['ad_spend','revenue','blended_roas','cpa'] }`
- Aggregation: blended MER cross-channel (canonical attribution truth)

**NEVER** dump raw API output. Pre-process locally avant Step 2.

---

## Step 1B · Declarative mode (fallback only)

Announce explicit:
> *"Mode declarative. Donne-moi 5 chiffres clés J-1 à la voix ou par paste · Spend Meta total, ROAS Meta, Spend Google (Search + PMAX split si dispo), Revenue Shopify, Orders count. Je compute les signaux et te brief en 5 sections."*

**NEVER** form questionnaire structuré, **NEVER** 10 questions en série. Conversation libre opérateur paste les chiffres, agent structure.

---

## Step 2 · Compute signals canon (seuils chiffrés)

**Pacing curve** · daily spend vs target.
- Threshold canon: ±20% vs target daily (target = monthly_budget / 30 OR strategy.json daily_target).
- Read: si > +20% → flag "overpace" ; si < -20% → flag "underpace" ; sinon OK.

**Frequency saturation** · canon Meta.
- Threshold: max frequency par audience (adset) > 2.5 sur 7d.
- Read: > 2.5 → flag "frequency saturated" ; 2.0-2.5 → watch ; < 2.0 OK.

**CPM drift** · creative fatigue early signal.
- Threshold: CPM J-1 vs CPM J-7 (week-over-week delta) > +30%.
- Read: > +30% → flag "CPM drift, fatigue signal" ; 15-30% → watch ; < 15% OK.

**ROAS drop** · vs MER target par stage strategy.
- Threshold canon par stage:
  - Stage **scale** · target ROAS ≥ 1.5x
  - Stage **maintain** · target ROAS ≥ 2.5x
  - Stage **test** · target ROAS ≥ 3.5x (break-even higher pour test budget)
- Read: ROAS J-1 < target → flag "ROAS drop vs stage target" ; > target OK.

**Creative fatigue** · CTR decay 14-30j.
- Threshold: CTR J-1 vs CTR moyen 14j > -25% decay.
- Read: > -25% → flag "fatigue confirmed" ; -10 à -25% → watch ; < -10% OK.

**Output compute** · table interne agent {signal × status × current value × threshold × directional read}. **NEVER** surface table brute à l'opérateur, c'est intermediate computation.

---

## Step 3 · 5 sections investigation-posture output (operator-facing)

**Format Slack/voix-friendly** · briefing court actionnable, scannable 30s, voice-friendly si lu à haute voix. **NEVER** dump tableaux exhaustifs raw data.

### Section 1 · Observé (faits sourcés J-1)

Chiffres précis pulled, ancrés source. Liste à puces courte (5-8 lignes max).

Exemple:
```
Observé · J-1 (2026-05-16)

- Meta · 2 340€ spend, ROAS 2.1, frequency max 2.8 sur adset Broad-FR
- Google · 890€ spend (Search 620€ + PMAX 270€), ROAS Search 4.2, ROAS PMAX 1.4
- Shopify · 47 orders, 5 820€ revenue, AOV 124€
- TW blended · MER 1.8 (vs target stage maintain 2.5)
- Top ad Meta · CRT-12 (45% du spend, ROAS 2.4, CTR 1.9% vs 14j avg 2.4%)
```

### Section 2 · Déduit (hypothèses confidence chain)

Chaque flag posé comme hypothèse avec confidence + indicateurs. Pas affirmé comme fait.

Exemple:
```
Déduit · 3 flags

H1 · Pacing OK Meta, underpace Google PMAX (déduit confidence forte · spend Google PMAX 270€ vs target estimé 400€/jour)
H2 · Frequency saturation sur Broad-FR (confidence moyenne · 2.8 > seuil canon 2.5, mais sur 1 seul adset)
H3 · Creative fatigue early signal sur CRT-12 (confidence faible · CTR decay -21% sur 14j, pas encore -25% seuil, watch)
```

### Section 3 · Inconnu (variables non observables)

Variables critiques qu'on ne peut pas lever depuis insights J-1. Max 3-4 items.

Exemple:
```
Inconnu

- Cause root frequency saturation (audience overlap ? audience size décroît ? budget concentré sur 1 adset ?)
- ROAS Google PMAX 1.4 · sub-optimal pacing ou audience signals weak ?
- AOV 124€ vs target stratégie (à confirmer dans strategy.json)
```

### Section 4 · Leviers (drill-down skills/actions)

Pour chaque flag, quel skill ou action permet de driller. Max 3-4 leviers.

Exemple:
```
Leviers

- Frequency saturation Broad-FR → analyze-perf deep-dive sur l'adset (audience overlap + budget split)
- Creative fatigue CRT-12 → recompose-creative pour produire 2-3 variants (préserver le NOYAU)
- ROAS Google PMAX bas → audit-meta-account (oui setup issue souvent root cause sur PMAX, audit-google-pmax si dispo)
```

### Section 5 · Close ouvert (UNE question macro)

UNE question macro à l'opérateur. Pas synthèse fermée. Pas 4 questions.

Exemple:
```
Sur quel flag tu veux qu'on creuse en premier · frequency saturation, fatigue CRT-12, ou PMAX ?
```

Use `AskUserQuestion` tool pour smart suggests si pertinent · load via `ToolSearch(select:AskUserQuestion)` if not loaded. Options adaptive selon flags observés, **NEVER** options génériques pre-templated.

---

## Hard Rules

- **HR1** · JAMAIS affirmer une hypothèse comme un fait. Tout flag = hypothèse avec confidence chain explicite (forte / moyenne / faible / TRÈS faible). Anti-pattern AP-1 doctrine investigation-posture BANNI.
- **HR2** · JAMAIS clôturer la conversation avec synthèse complète. **ALWAYS** ouvrir drill-down via Section 5 close UNE question macro. Anti-pattern AP-5 BANNI.
- **HR3** · Seuils canon respectés strict: pacing ±20%, frequency 2.5 max, CPM drift +30% WoW, ROAS targets par stage (1.5x scale / 2.5x maintain / 3.5x test), fatigue CTR decay -25% sur 14j. **NEVER** improviser des seuils différents.
- **HR4** · Format Slack/voix-friendly · briefing court actionnable scannable 30s. **NEVER** dump tableaux exhaustifs raw data, **NEVER** verbose prose narrative, **NEVER** > 25-30 lignes total output operator-facing.
- **HR5** · Step 0 bridge proactif canon v2.77 MANDATORY · jamais skip access check. Default proactif (a) connect-mcp-server guidage, fallback (b) declarative interview. **NEVER** silently fail sur missing token.
- **HR6** · JAMAIS expose internal compute table {signal × threshold × value} à l'opérateur. Intermediate computation invisible. L'opérateur lit "Frequency saturation sur Broad-FR (confidence moyenne)", pas "frequency=2.8 > threshold=2.5".
- **HR7** · Zéro em-dash dans tout output. Substituer par virgule, parenthèses, point, deux-points ou middle dot (·). Canon `no_em_dash` strict.

---

## Output format example

**Briefing complet Stepprs (fictif, illustratif investigation-posture canon)**

```
Routine perf · Stepprs · J-1 (2026-05-16)

Observé
- Meta · 2 340€ spend, ROAS 2.1, freq max 2.8 (adset Broad-FR)
- Google · 890€ (Search 620€ ROAS 4.2 / PMAX 270€ ROAS 1.4)
- Shopify · 47 orders, 5 820€ revenue, AOV 124€
- TW blended · MER 1.8 (target stage maintain 2.5)
- Top ad Meta · CRT-12, 45% spend, CTR 1.9% vs 14j avg 2.4%

Déduit · 3 flags
H1 · Pacing Meta OK, underpace Google PMAX (confidence forte)
H2 · Frequency saturation Broad-FR à surveiller (confidence moyenne)
H3 · Creative fatigue CRT-12 early signal (confidence faible, watch)

Inconnu
- Cause root frequency saturation (overlap audience ? budget concentré ?)
- ROAS PMAX 1.4 · setup issue ou audience signals weak ?
- AOV 124€ aligné stage target ?

Leviers
- Frequency Broad-FR → analyze-perf deep-dive adset
- Fatigue CRT-12 → recompose-creative variants
- PMAX ROAS bas → audit-meta-account (root cause souvent setup)

Sur quel flag tu veux qu'on creuse en premier ?
```

**Briefing partiel coverage (Meta OK, Google manquant)**

```
Routine perf · Stepprs · J-1 (2026-05-16)

Observé · Meta + Shopify uniquement (Google + TW non-connectés)
- Meta · 2 340€ spend, ROAS 2.1, freq max 2.8 (Broad-FR)
- Shopify · 47 orders, 5 820€ revenue, AOV 124€

Déduit · 2 flags + 1 blind spot
H1 · Frequency saturation Broad-FR (confidence moyenne)
H2 · ROAS Meta 2.1 < stage maintain target 2.5 (confidence forte sur data Meta isolé)
Blind spot · pas de MER blended cross-channel sans TW

Inconnu
- Spend Google + PMAX (blind spot)
- MER blended cross-channel (TW non-connecté)
- Cause frequency saturation

Leviers
- Frequency → analyze-perf deep-dive adset Broad-FR
- ROAS sous target → analyze-perf cross-platform (mais besoin Google + TW connectés pour vue complète)
- Connecter Google Ads + TW → connect-mcp-server (gain · briefing complet next routine)

Tu veux qu'on creuse le flag frequency ou qu'on connecte Google + TW d'abord ?
```

---

## Anti-patterns

- **AP-1 · Dump exhaustif chiffres bruts** · agent ship tableau 30 lignes raw insights par campaign, ad, audience, age, gender, placement, device. Operateur scroll 5 min, perd le signal. Pattern canon · pre-process intelligence, surface uniquement flags + chiffres clés (5-8 lignes Section 1 max).
- **AP-2 · Synthèse close affirmative** · agent termine *"Le compte performe bien, RAS aujourd'hui, on continue."* Ferme la porte. Anti-pattern AP-5 doctrine investigation-posture BANNI. Pattern canon · UNE question macro Section 5 ouvre drill-down.
- **AP-3 · Skip Step 0 gate access** · agent freestyle un brief sans verifier MCP/tokens, invente des chiffres ou affirme sans data. Anti-pattern systémique. Pattern canon · Step 0 bridge proactif MANDATORY · 2 options canon (a) connect-guide ou (b) declarative.
- **AP-4 · Flags affirmés comme faits** · agent dit *"Le creative CRT-12 est fatigué."* Hypothèse présentée comme fait. Anti-pattern AP-1 doctrine investigation-posture BANNI. Pattern canon · *"Creative fatigue CRT-12 early signal (confidence faible · CTR decay -21% sur 14j)."*
- **AP-5 · Seuils improvisés** · agent invente threshold *"Frequency > 4 c'est saturated"* alors que canon est 2.5. Pattern canon · seuils HR3 strict respectés.
- **AP-6 · Verbose prose narrative** · agent écrit *"Aujourd'hui, on observe une tendance intéressante sur le compte Meta. Le spend est légèrement au-dessus de notre objectif quotidien, ce qui pourrait indiquer que..."*. Format Slack/voix violé. Pattern canon · briefing court actionnable, bullet points, chiffres précis, pas prose.
- **AP-7 · Internal compute table surface** · agent surface *"frequency=2.8 vs threshold=2.5"* avec valeurs raw. Pattern canon · l'opérateur lit le flag sémantique avec confidence chain, pas le compute interne.

---

## Cross-refs

- `docs/system/investigation-posture.md` (v2.54 doctrine canon) · 5 sections obligatoires Observé / Déduit / Inconnu / Leviers / Close ouvert · confidence chain explicite · anti-pattern AP-1 (affirmation hypothèse) et AP-5 (close fermé) BANNIS strict.
- `docs/system/skill-routing-doctrine.md` (v2.76+ canon) · routing 5 phases · disambiguation rules canon vs audit-meta-account + analyze-perf + brief-day.
- `docs/system/connectivity-layering.md` · 3 layers · Layer 1 facebook-graph MCP + Layer 2 Google Ads / Shopify / TripleWhale APIs callable via skills.
- `docs/system/contextual-intelligence.md` · master doctrine · no orphan output (close ouvert Section 5), trust the model on semantic layer, jargon zéro en surface.
- `docs/system/canonical-matrix-reasoning.md` · qualité output post-routing · cette skill consume matrices canon seuils (pacing, frequency, CPM, ROAS, fatigue).
- `resources/conventions/meta-ads.json` · Meta Insights endpoints + rate limits + learned_rules (call_to_actions OBLIGATOIRE, etc.).
- `resources/conventions/google-ads.json` · GAQL search query + cost_micros + PERFORMANCE_MAX channel type.
- `resources/conventions/shopify.json` · orders endpoint + Link header pagination + AOV compute.
- `resources/conventions/triplewhale.json` · blended MER cross-channel attribution canonical.
- `.skills/skills/audit-meta-account/SKILL.md` · skill sœur · audit setup health (config + structure + pixel) vs routine-perf briefing perf quotidienne (delivery + signal alert).
- `.skills/skills/analyze-perf/SKILL.md` · skill sœur · deep-dive cross-platform multi-jour avec recos stratégiques vs routine-perf pull rapide briefing court 5 min.
- `.skills/skills/brief-day/SKILL.md` · skill sœur · oriente état brand global vs routine-perf focalisé perf paid quotidienne.
- `.skills/skills/connect-mcp-server/SKILL.md` · invoked par Step 0 option (a) si MCP facebook-graph absent.
- `.skills/skills/recompose-creative/SKILL.md` · invoked par Section 4 Leviers si flag creative fatigue.
