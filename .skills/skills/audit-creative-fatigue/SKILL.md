---
name: audit-creative-fatigue
type: curator
version: "1.0.0"
recommended_model: sonnet
isolation_scope: brand
layer: production
description: >
  Scan creatives produced/{CRT-NN} brand-side, pull Meta Insights par ad_id,
  détecte fatigue signaux canon (CTR decay 14-30j · CPM rise +30% week-over-week
  · frequency saturation >2.5 · ROAS decay). Flag à operator avec reco trigger
  recompose-creative (variant_axis hook_swap OR background_swap). À scale c'est
  le killer #1 paid media. Cross-refs pacing-discipline.md v2.78.
  Step 0 bridge proactif canon v2.77.
  FR: "audit fatigue créa", "check creative fatigue", "fatigue scan ads",
      "creative refresh check", "audit fatigue creatives", "scan fatigue".
  EN: "audit creative fatigue", "creative fatigue scan", "ad fatigue check",
      "scan creative fatigue", "fatigue audit".
permissions:
  reads: ["brands/{slug}/creatives/", "brands/{slug}/produced/"]
  writes: ["brands/{slug}/audits/{date}_creative-fatigue.md"]
  mode: interactive
  subagent_safe: true
extension_hooks:
  consumable_by: ["creative_entity"]
disambiguates_against:
  - "audit-meta-account · audit setup compte (pixel + CAPI + structure + attribution)
     vs audit-creative-fatigue · audit fatigue creatives produced spécifique"
  - "routine-perf · briefing perf quotidien cross-platform 5 signaux mix
     vs audit-creative-fatigue · scan creative-level fatigue dédié drill"
  - "analyze-perf · diagnostic deep-dive cross-platform multi-jour
     vs audit-creative-fatigue · scan ciblé creatives produced brand-side"
  - "recompose-creative · produce variant créa adaptée downstream
     vs audit-creative-fatigue · upstream curator détecte fatigue, propose trigger"
pipeline:
  preconditions: |
    brands/{slug}/brand.json exists.
    brands/{slug}/creatives/produced/ contient ≥1 CRT-NN.json (audit-able).
    Credentials Meta présents (credentials_shared.env OR brands/{slug}/credentials.env).
  postconditions: |
    Audit markdown persisté brands/{slug}/audits/{date}_creative-fatigue.md.
    Si fatigue level >= warning, reco trigger recompose-creative surfacée operator.
    Si confidence finding >= 0.7, propose chain capture-learning silent.
---

# Skill: audit-creative-fatigue

Scanner fatigue creatives produced brand-side. Pull Meta Insights par ad_id, compute signaux canon (CTR decay 14-30j, CPM rise WoW, frequency saturation, ROAS decay), classifie fatigue level, propose trigger recompose-creative avec variant_axis pertinent. À scale, fatigue créa = killer #1 paid media. Curator scan + flag, ne produit pas variantes (recompose-creative downstream).

## Expert methodology

**Canonical expert persona**: senior creative strategist 7-fig accounts, daily creative fatigue monitoring loop.

**Framework**: 4-signal compute canon (CTR decay slope, CPM rise %, frequency saturation, ROAS decay) × creative-level granularity × fatigue classification (fresh / stable / warning / critical) × variant_axis reco (hook_swap si CTR decay, background_swap si CPM rise).

**Matrix** (applied per creative): *signal canon × current value × seuil canon × fatigue contribution × directional read*.

**Codified reference**: `docs/system/pacing-discipline.md` (seuils canon 4 axes), `resources/conventions/meta-ads.json` (Insights endpoints + rate limits), `creative.schema v1.2` (variant_axis enum). Si convention incomplète, Gate doc canon (WebFetch official doc + fill) avant pull.

---

## Step 0 · Gate access + bridge proactif canon v2.77 (MANDATORY)

**CRITICAL:** verify connectivity AVANT pull Meta Insights. **NEVER** silently fail on missing token. **NEVER** invent fatigue signals sans data sourcée.

1. **Layer 1 MCP check.** Verify `facebook-graph` MCP connected via `claude mcp list`. Required pour Meta Insights pull par ad_id.
2. **Layer 2 credentials check.** Read `credentials_shared.env` (workspace) + `brands/{slug}/credentials.env` (brand). Required keys ·
   - `META_ACCESS_TOKEN` (token shared cross-brands)
   - `META_AD_ACCOUNT_ID` (brand-specific)
3. **Convention check.** Read `resources/conventions/meta-ads.json`. Si missing OR incomplete sur Insights endpoints (rate limits, breakdowns, fields), Gate doc canon avant call.

**Branching canon proactif v2.77** (AskUserQuestion via `ToolSearch(select:AskUserQuestion)`) ·

- **Tokens présents + MCP connecté** → announce, proceed Step 1 ·
  > *"Connectivité Meta OK. Je scan les creatives produced pour {brand} et pull les insights par ad_id. 2-3 min, je reviens avec l'audit fatigue."*

- **Token absent / MCP absent** → AskUserQuestion 2 options ·
  - (a) "Je te guide pour connecter Meta maintenant (~2 min via connect-mcp-server). L'audit devient factuel et future audits sont instant."
  - (b) "Je bascule en mode declarative · tu me donnes les chiffres clés par creative (CTR J-1, CTR avg 14j, CPM J-1, CPM J-7, frequency, days_running) à la voix ou paste. Je structure l'audit."
  
  **Default proactif proactif** · proposer (a) si l'opérateur a le temps, fallback (b) si urgence audit immediate.

---

## Step 1 · List creatives produced (scan brand-side)

Read `brands/{slug}/creatives/produced/` directory · list tous les `CRT-NN.json` files.

Pour chaque CRT-NN.json ·

1. Parse · extraire `creative_id`, `concept_id`, `meta.ad_id` (si déployé sur Meta), `meta.deployed_at`, `format.type`, `format.ratio`, `tags.source`.
2. Filter · ne garder que les creatives avec `meta.ad_id` non-null ET `meta.deployed_at` non-null (creatives non-déployés Meta non-auditables ici).
3. Buffer · liste `[{creative_id, ad_id, deployed_at, days_running, concept_id}]`.

Si zéro creative déployé Meta → close cleanly · *"Aucun creative déployé sur Meta brand-side pour le moment. Audit fatigue non-applicable. Reviens quand tu auras des ads en live."*

---

## Step 2 · Pull Meta Insights par ad_id

Pour chaque creative buffered (max parallel 5, respect rate limit Meta canon meta-ads.json) ·

Endpoint · `GET /{ad_id}/insights`

Params · `fields=spend,impressions,clicks,ctr,cpm,frequency,actions,cost_per_action_type,purchase_roas&date_preset=last_30d&breakdowns=&time_increment=1`

Aggregations locales agent ·

- **CTR par jour** sur 30 derniers jours · array `[{date, ctr}]`
- **CPM par jour** sur 30 derniers jours · array `[{date, cpm}]`
- **Spend cumulé** total 30j
- **Days_running** = `today - deployed_at`
- **Frequency current** · max sur 7d window
- **ROAS daily** sur 30j (si purchase_roas dispo) · array `[{date, roas}]`

**NEVER** dump raw API output. Pre-process locally avant Step 3.

---

## Step 3 · Compute fatigue signals canon

Pour chaque creative, compute 4 signaux canon ·

**Signal 1 · CTR decay slope** (axe 4 pacing-discipline) ·
- Compute · CTR moyen J-1 à J-3 vs CTR moyen J-12 à J-14.
- Formula · `decay_pct = (ctr_recent - ctr_baseline) / ctr_baseline × 100`
- Seuils canon ·
  - `decay_pct < -25%` → fatigue confirmed
  - `decay_pct -10% à -25%` → watch
  - `decay_pct > -10%` → OK
- Contribution fatigue · si confirmed, primary reco variant_axis = `hook_swap` (CTR decay = hook usé).

**Signal 2 · CPM rise week-over-week** (axe 3 pacing-discipline) ·
- Compute · CPM moyen J-1 à J-7 vs CPM moyen J-8 à J-14.
- Formula · `rise_pct = (cpm_recent - cpm_previous) / cpm_previous × 100`
- Seuils canon ·
  - `rise_pct > +30%` → CPM drift critical
  - `rise_pct +15% à +30%` → watch
  - `rise_pct < +15%` → OK
- Contribution fatigue · si critical, primary reco variant_axis = `background_swap` (CPM rise = visual usé, audience désengage).

**Signal 3 · Frequency saturation** (axe 2 pacing-discipline) ·
- Compute · max frequency sur 7d window.
- Seuils canon Meta ·
  - `frequency > 4.0` → audience fatigue critical
  - `frequency 2.5 - 4.0` → saturation signal
  - `frequency 1.8 - 2.5` → normal
  - `frequency ≤ 1.8` → optimal
- Contribution fatigue · si > 4.0, reco escalation `audience_swap` (audience saturée, dépasse capacité variant_axis hook/background).

**Signal 4 · ROAS decay** (axe 4 contribution downstream) ·
- Compute · ROAS moyen J-1 à J-7 vs ROAS moyen J-15 à J-21.
- Formula · `roas_decay = (roas_recent - roas_baseline) / roas_baseline × 100`
- Seuils canon ·
  - `roas_decay < -30%` → conversion fatigue
  - `roas_decay -15% à -30%` → watch
  - `roas_decay > -15%` → OK
- Contribution fatigue · ROAS decay confirme fatigue (lagging indicator vs CTR leading).

**Output compute** · table interne agent `{creative_id × 4 signals × current value × seuil canon × directional read}`. **NEVER** surface table brute à l'opérateur, intermediate computation invisible.

---

## Step 4 · Classify fatigue level

Pour chaque creative, classifier fatigue level basé sur `days_running` + signaux ·

| Days running | Fatigue level | Trigger |
|---|---|---|
| < 14 jours | **fresh** | aucune action, laisse learning phase finir |
| 14-21 jours | **stable** | OK si signaux verts, watch si 1+ signal jaune |
| 21-30 jours | **warning** | recompose-creative recommandé si 2+ signaux rouges OR 1 signal critical |
| > 30 jours | **critical** | recompose-creative MANDATORY, sinon ROAS coffin |

**Cross-signal logic** ·

- **CTR decay confirmed** (signal 1 rouge) ET **days_running >= 14** → warning (au minimum)
- **CPM rise critical** (signal 2 rouge) ET **days_running >= 14** → warning (au minimum)
- **Frequency > 4.0** (signal 3 critical) → critical regardless days_running (audience cap hit)
- **2+ signaux rouges simultanés** → critical regardless days_running (compound fatigue)

**Variant_axis reco principle** ·

- Si CTR decay primary signal → reco `hook_swap`
- Si CPM rise primary signal → reco `background_swap`
- Si frequency saturation (> 4.0) → reco escalation `audience_swap` (recompose-creative variant_axis = new_audience)
- Si 2+ signaux compound → reco compound variant (hook_swap + background_swap, deux passes recompose-creative séquentielles)

---

## Step 5 · 5 sections investigation-posture output (operator-facing)

Format founder-facing scannable. **NEVER** dump tableaux exhaustifs raw data, **NEVER** verbose prose narrative, **NEVER** > 30 lignes total output.

### Section 1 · Observé (faits sourcés par creative)

Liste compacte par creative auditée, chiffres précis ancrés source Meta Insights.

```
Observé · audit fatigue {brand_humain} ({date})

Scan · {N} creatives déployés Meta sur les 30 derniers jours
- CRT-12 · 31j running, CTR J-1 1.4% vs avg 14j 2.1% (-33%), CPM J-7 28€ vs J-14 19€ (+47%), freq 3.2
- CRT-08 · 18j running, CTR J-1 2.8% vs avg 14j 2.7% (+4%), CPM stable, freq 2.1
- CRT-15 · 8j running, learning phase (data insufficient pour decay compute)
```

### Section 2 · Déduit (hypothèses confidence chain)

Chaque flag fatigue posé comme hypothèse avec confidence + indicateurs sources. Pas affirmé comme fait.

```
Déduit · 2 flags fatigue + 1 fresh

H1 · CRT-12 fatigue critical (confidence forte · 31j running + CTR decay -33% confirmé + CPM rise +47% critical + freq 3.2 saturation)
  Compound fatigue · hook usé ET visual usé
  Reco · recompose-creative deux passes (hook_swap d'abord, puis background_swap sur la variante hookée)

H2 · CRT-08 stable mais watch (confidence moyenne · 18j running, signaux verts mais freq 2.1 approche seuil 2.5)
  Reco · monitor 7 jours, si freq dépasse 2.5 → recompose-creative variant_axis hook_swap

CRT-15 · fresh, learning phase (8j running, data insufficient pour audit)
```

### Section 3 · Inconnu (variables non observables)

Variables critiques qu'on ne peut pas lever depuis Insights J-1. Max 3-4 items.

```
Inconnu

- Cause root frequency saturation CRT-12 (audience overlap avec CRT-08 ? budget concentré ?)
- Variantes A/B déjà testées sur concept CRT-12 (lookup creatives/{concept_id}/variants/)
- Seuil ROAS break-even brand-specific (à lire dans strategy.json)
```

### Section 4 · Leviers (drill-down skills/actions)

Pour chaque flag, quel skill/action permet de driller ou agir. Max 3-4 leviers.

```
Leviers

- Fatigue critical CRT-12 → recompose-creative CRT-12 variant_axis=hook_swap (préserve concept, change accroche)
- Audience overlap CRT-12 vs CRT-08 → analyze-perf deep-dive sur les deux adsets
- Watch CRT-08 freq → monitor 7j via routine-perf daily
```

### Section 5 · Close ouvert (UNE question macro)

UNE question macro à l'opérateur. Pas synthèse fermée.

```
Sur CRT-12 critical, on lance le recompose maintenant ou tu valides d'abord la cause root frequency saturation ?
```

Use `AskUserQuestion` tool pour smart suggests si pertinent (load via `ToolSearch(select:AskUserQuestion)` if not loaded). Options adaptive selon flags, **NEVER** options génériques pre-templated.

---

## Step 6 · Persist audit markdown

Write audit markdown à `brands/{slug}/audits/{YYYY-MM-DD}_creative-fatigue.md` ·

Format ·

```markdown
# Audit Creative Fatigue · {brand} · {YYYY-MM-DD}

## Scope
Scan · {N} creatives déployés Meta sur 30 derniers jours

## Findings par creative

### CRT-NN
- Days running · {N}j
- Fatigue level · {fresh|stable|warning|critical}
- Signaux ·
  - CTR decay · {pct}% ({status})
  - CPM rise WoW · {pct}% ({status})
  - Frequency · {value} ({status})
  - ROAS decay · {pct}% ({status})
- Confidence finding · {forte|moyenne|faible|TRÈS faible}
- Reco · {variant_axis recommandé OR no action}

## Priority list (top 5 by severity)
1. CRT-NN · critical · recompose-creative {variant_axis}
2. ...

## Cross-refs
- pacing-discipline.md v2.78 (seuils canon respectés)
- recompose-creative downstream consumer
```

**NEVER** Edit/Write JSON directly. Markdown audit OK direct write (audit log, not entity).

---

## Step 7 · Capture-learning silencieux si confidence finding >= 0.7

Si UNE finding au moins atteint confidence forte (≥ 0.7 dans confidence chain canon) ET outcome explicit (creative fatigué validé par audit, pas hypothèse faible) ·

→ Trigger silencieux `capture-learning` avec entry ·

```json
{
  "fact": "Creative CRT-{NN} sur {brand} fatigue confirmed à {N} jours running (CTR decay {pct}% + CPM rise {pct}% + freq {value})",
  "reasoning": "{root cause hypothesis from audit · ex 'hook saturated cross-audience, CPM rise indique visual désengage' OR 'audience size décroît, frequency saturation cap hit'}",
  "scope": "brand",
  "platform": "meta",
  "type": "behavior",
  "tags": ["creative-fatigue", "{variant_axis_recommandé}", "{format_type}"],
  "genericity": "brand"
}
```

Cross-ref · `learn-from-session Trigger 9` daemon peut promouvoir cette finding cross-brand canon validations[] si N≥3 brands valident même pattern fatigue.

---

## Hard Rules

- **HR1** · Step 0 bridge proactif canon v2.77 MANDATORY · jamais skip access check. Default proactif (a) connect-mcp-server, fallback (b) declarative. **NEVER** silently fail sur missing token.
- **HR2** · Seuils canon `docs/system/pacing-discipline.md` respectés strict · CTR decay -25%, CPM rise +30% WoW, frequency 2.5/4.0, ROAS decay -30%. **NEVER** improviser des seuils différents.
- **HR3** · 5 sections investigation-posture output obligatoire (Observé / Déduit / Inconnu / Leviers / Close ouvert). Anti-pattern AP-5 doctrine investigation-posture BANNI (synthèse close affirmative).
- **HR4** · JAMAIS affirmer fatigue comme un fait. Tout flag = hypothèse avec confidence chain explicite (forte / moyenne / faible / TRÈS faible). Anti-pattern AP-1 doctrine BANNI.
- **HR5** · JAMAIS trigger recompose-creative silent sans operator gate. Audit propose reco, operator décide trigger. Mode `interactive` (pas `direct`).
- **HR6** · JAMAIS expose internal compute table {signal × threshold × value} brute à l'opérateur. Intermediate computation invisible. L'opérateur lit "CRT-12 fatigue critical (confidence forte)", pas "ctr_decay=-33% > threshold=-25%".
- **HR7** · Zéro em-dash dans tout output. Substituer par virgule, parenthèses, point, deux-points ou middle dot (·). Canon `no_em_dash` strict.
- **HR8** · Format founder-facing scannable 30s, max 30 lignes output operator-facing. **NEVER** dump tableaux exhaustifs raw data, **NEVER** verbose prose narrative.
- **HR9** · variant_axis reco respecte mapping canon · CTR decay → hook_swap, CPM rise → background_swap, frequency > 4.0 → audience_swap, compound → séquentiel hook_swap puis background_swap.
- **HR10** · Audit persiste markdown à `brands/{slug}/audits/{date}_creative-fatigue.md`, append-only (jamais écrase audit antérieur même date · suffix `_2` si re-run).

---

## Anti-patterns

- **AP-1 · Refresh sans data** · agent recommande `recompose-creative` sur creative non-déployé OR sans 14j data Meta Insights, basé sur intuition LLM. Pattern canon · refresh require data sourcée fatigue confirmed.
- **AP-2 · Ignore fatigue > 30j** · agent skip creative > 30j running car "data trop ancienne". Pattern canon · > 30j = critical, MANDATORY recompose même si data partial.
- **AP-3 · Trigger refresh sans operator gate** · agent invoque `recompose-creative` direct post-audit. Pattern canon · audit = curator scan + reco, recompose = producer action operator-validated.
- **AP-4 · Seuils improvisés** · agent invente *"CTR decay -15% = fatigue"* alors que canon est -25%. Anti-pattern HR2 BANNI.
- **AP-5 · Affirme fatigue comme fait** · agent dit *"CRT-12 est fatigué."* Hypothèse présentée comme fait. Anti-pattern AP-1 doctrine investigation-posture BANNI. Pattern canon · *"Fatigue confirmed CRT-12 (confidence forte · 3 signaux convergents)"*.
- **AP-6 · Skip Section 5 close ouvert** · agent ferme audit avec synthèse complète sans question. Anti-pattern AP-5 doctrine investigation-posture BANNI. Pattern canon · UNE question macro Section 5.
- **AP-7 · Dump exhaustif raw data** · agent ship table 50 lignes par creative × 4 signals × 30 days. Pattern canon · pre-process intelligence, surface uniquement findings synthétisés (3-5 creatives max par audit batch).
- **AP-8 · Variant_axis impromptu** · agent recommande variant_axis arbitraire (ex `format_swap` sur CTR decay). Pattern canon · mapping HR9 strict respecté.

---

## Cross-refs

- `docs/system/pacing-discipline.md` v2.78 · seuils canon 4 axes pacing chiffrés
- `docs/system/investigation-posture.md` · 5 sections obligatoires output stratégique
- `docs/system/canonical-matrix-reasoning.md` · matrix-driven fatigue compute
- `recompose-creative` · downstream consumer (variant_axis hook_swap, background_swap, audience_swap)
- `routine-perf` · sibling pacing daily briefing (includes fatigue signal mix 5-signal canon)
- `analyze-perf` · sibling diagnostic deep-dive cross-platform multi-jour
- `audit-meta-account` · sibling setup audit (config + structure, vs creative-level fatigue ici)
- `learn-from-session` Trigger 9 · daemon promote cross-brand canon validations[] si pattern N≥3 brands
- `capture-learning` · downstream silent capture findings confidence forte
- `resources/conventions/meta-ads.json` · Insights endpoints + rate limits + learned_rules
- `creative.schema v1.2` · variant_axis enum reference
