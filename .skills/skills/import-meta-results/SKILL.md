---
name: import-meta-results
type: capturer
version: "1.0.0"
recommended_model: haiku
isolation_scope: brand
layer: meta
description: >
  Pull Meta Insights par ad_id pour creatives produced (CRT-NN) · écrit
  dans validations[] canon-tools utilisés (formula · framework · archetype ·
  hook · objection · CTA) · alimente decay v2.37 attribution + N≥3 brands
  threshold auto-promote canon. Ferme la boucle produce → test → learn → promote
  opérée quotidiennement par skill dédié (vs ad-hoc manuel actuel). Step 0
  bridge proactif canon v2.77.
  FR: "import results Meta", "import perf ads", "feed atlas vivant",
      "alimente validations canon", "import meta perf", "pull insights canon".
  EN: "import Meta results", "import ad perf", "feed validations canon",
      "pull canon results", "import meta insights".
permissions:
  reads: ["brands/{slug}/creatives/produced/"]
  writes: ["resources/canon/copy/*/validations/{tool}.json", "learnings.json"]
  mode: silent
  subagent_safe: true
extension_hooks:
  consumable_by: ["creative_entity"]
disambiguates_against:
  - "analyze-perf · diagnostic deep-dive cross-platform multi-jour avec recos stratégiques
     vs import-meta-results · pull data brut écrit canon validations sans diagnostic"
  - "learn-from-session · capture learnings session-end full conversation scan
     vs import-meta-results · pull Meta runtime continuous par ad_id ciblé"
  - "audit-creative-fatigue · curator scan fatigue creative-level avec reco
     vs import-meta-results · capturer pull data brut alimente atlas vivant"
  - "routine-perf · briefing perf quotidien navigator output operator-facing
     vs import-meta-results · capturer silent écrit canon validations[] sans output verbose"
pipeline:
  preconditions: |
    brands/{slug}/brand.json exists.
    brands/{slug}/creatives/produced/ contient ≥1 CRT-NN.json avec canon-tools tagués
    (formula_used, framework_used, archetype_used, hook_used, objection_used, cta_used).
    Credentials Meta présents (credentials_shared.env OR brands/{slug}/credentials.env).
  postconditions: |
    Validations[] entries appendées resources/canon/copy/{layer}/{tool}.json par canon-tool utilisé.
    Decay v2.37 appliqué pré-promotion (filter entries stale).
    Si canon-tool atteint N≥3 brands validate threshold, signal auto-promote candidate flagué.
    Learnings.json entry append-only par creative importé (pattern reproductible v2.27).
---

# Skill: import-meta-results

Capturer silent qui pull Meta Insights par ad_id pour creatives produced brand-side, cross-réf canon-tools utilisés (formula, framework, archetype, hook, objection, CTA), écrit `validations[]` canon-tool par layer, alimente decay v2.37 + N≥3 brands threshold auto-promote. Ferme la boucle produce → test → learn → promote opérée quotidiennement. Layer meta (cross-brand canon-tool validation), mode silent (pas de verbose output operator-facing).

## Expert methodology

**Canonical expert persona**: pipeline engineer atlas vivant · ferme boucle produce → test → learn → promote canon. Daemon silent, pas analyst.

**Framework**: 5-step pipeline canon (list produced → pull Insights → cross-ref canon-tools → append validations[] → compute auto-promote signal) × decay v2.37 attribution × N≥3 brands threshold.

**Matrix** (applied per creative): *creative × canon-tools utilisés × perf metrics × validation entry par canon-tool*.

**Codified reference**: `docs/system/learn-from-session.md` Trigger 9 (canon validation routing v2.26+ + HR-Canon-V11 + HR-Canon-Decay), `resources/canon/copy/{layer}/*.json` (schema canon-tool/1.1), `creative.schema v1.2` (`formula_used`, `framework_used`, `archetype_used`, `hook_used` fields), `resources/conventions/meta-ads.json` (Insights endpoints).

---

## Step 0 · Gate access + bridge proactif canon v2.77 (MANDATORY)

**CRITICAL:** verify connectivity AVANT pull Meta Insights. **NEVER** silently fail on missing token. **NEVER** write validations[] sans data sourcée.

1. **Layer 1 MCP check.** Verify `facebook-graph` MCP connected via `claude mcp list`. Required pour Meta Insights pull par ad_id.
2. **Layer 2 credentials check.** Read `credentials_shared.env` (workspace) + `brands/{slug}/credentials.env` (brand). Required keys ·
   - `META_ACCESS_TOKEN` (token shared cross-brands)
   - `META_AD_ACCOUNT_ID` (brand-specific)
3. **Convention check.** Read `resources/conventions/meta-ads.json`. Si missing OR incomplete sur Insights endpoints, Gate doc canon avant call.

**Branching canon proactif v2.77** (AskUserQuestion via `ToolSearch(select:AskUserQuestion)`) ·

- **Tokens présents + MCP connecté** → silent proceed Step 1, mode capturer (pas annonce verbose) ·
  > *"Pull Meta results en cours · {N} creatives, ~30s. Je flag si quelque chose remonte sur atlas."*

- **Token absent / MCP absent** → AskUserQuestion 2 options ·
  - (a) "Je te guide pour connecter Meta maintenant (~2 min via connect-mcp-server). Future imports sont silent et continuous."
  - (b) "Skip pour cette fois · imports atlas vivant nécessitent Meta API. Reviens quand connecté."
  
  **Default proactif proactif** · proposer (a) si l'opérateur a le temps, fallback (b) sans blocker (capturer skip propre, pas erreur).

---

## Step 1 · List creatives produced ad_ids (last N days)

Read `brands/{slug}/creatives/produced/` directory · scan tous les `CRT-NN.json`.

Pour chaque CRT-NN.json ·

1. Parse · extraire `creative_id`, `meta.ad_id`, `meta.deployed_at`, canon-tools utilisés ·
   - `formula_used` (e.g. `"OTRB-NN"` Obs+Tension+Reframe+Bridge)
   - `framework_used` (e.g. `"PAS"`, `"BAB"`, `"QUEST"`)
   - `archetype_used` (e.g. `"ARC-NN"` archetype voice)
   - `hook_used` (e.g. `"curiosity-gap"`, `"stat-choc"`)
   - `objection_used` (e.g. `"pre-emption"`)
   - `cta_used` (e.g. `"soft-close"`)
2. Filter · ne garder que les creatives avec ·
   - `meta.ad_id` non-null (déployé Meta)
   - `meta.deployed_at` ≤ today - N days (default N=30j, override via param)
   - ≥1 canon-tool tagué (sinon rien à valider)
3. Buffer · liste `[{creative_id, ad_id, deployed_at, days_running, canon_tools: {formula, framework, archetype, hook, objection, cta}, audience_slug}]`.

Si zéro creative éligible → close silent · log à `session-state.md` activity log entry `"import-meta-results run · 0 creatives éligibles"`. Pas de output operator-facing verbose (mode silent canon).

---

## Step 2 · Pull Meta Insights par ad_id

Pour chaque creative buffered (max parallel 5, respect rate limit Meta canon meta-ads.json · 100k pts/h + 40 pts par ad active, sleep 0.5s entre calls) ·

Endpoint · `GET /{ad_id}/insights`

Params · `fields=spend,impressions,clicks,ctr,cpm,frequency,actions,cost_per_action_type,purchase_roas&date_preset=lifetime`

Aggregations locales agent par creative ·

- **spend** total lifetime
- **impressions** total
- **ctr** moyen
- **cpm** moyen
- **frequency** max
- **purchase_roas** (extract de `actions` array si `action_type=purchase`)
- **conversions** count (extract `actions` array `action_type=purchase`)
- **cpa** = spend / conversions (si conversions > 0)
- **days_running** = today - deployed_at

**Outcome classification canon** (pour validations[] entry) ·

| Metric trigger | Outcome |
|---|---|
| `purchase_roas >= target_stage` (lookup strategy.json) | `success` |
| `purchase_roas 0.7-1.0 × target_stage` | `neutral` |
| `purchase_roas < 0.7 × target_stage` | `failed` |
| `ctr < ctr_baseline_canon × 0.5` AND `spend > 200€` | `failed` (signal click-thru cassé) |
| `days_running > 30 AND ctr_decay < -40%` | `fatigued` |

Si `target_stage` non-lisible (strategy.json absent OR incomplete), fallback `outcome = "neutral"` + flag dans entry note `"outcome_uncertain_strategy_missing"`.

**NEVER** dump raw API output. Pre-process locally avant Step 3.

---

## Step 3 · Cross-réf canon-tools utilisés

Pour chaque creative + ses canon-tools tagués ·

Lookup mapping canon-tool → layer ·

| canon_tool field | Layer canon |
|---|---|
| `formula_used` | `resources/canon/copy/angles/{tool}.json` |
| `framework_used` | `resources/canon/copy/frameworks/{tool}.json` |
| `archetype_used` | `resources/canon/copy/archetypes-voix/{tool}.json` |
| `hook_used` | `resources/canon/copy/hooks/{tool}.json` |
| `objection_used` | `resources/canon/copy/heuristiques-persuasion/{tool}.json` (objection pattern) |
| `cta_used` | `resources/canon/copy/heuristiques-persuasion/{tool}.json` (CTA pattern) |

**Attribution layer mapping** (canon-tool/1.1 v2.37+ enum 10 valeurs) ·

| canon_tool field | attribution_layer enum |
|---|---|
| `formula_used` | `angle` |
| `framework_used` | `framework` |
| `archetype_used` | `archetype` |
| `hook_used` | `hook` |
| `objection_used` | `creative_execution` (objection layer dans body copy) |
| `cta_used` | `creative_execution` (CTA layer fin body) |
| `format.type` (si canon-tool format) | `format` |

Buffer par canon-tool · `[{tool_path, attribution_layer, creative_id, outcome, metrics, audience_slug}]`.

---

## Step 4 · Append validations[] par canon-tool

Pour chaque entry buffered Step 3, construire validation entry schema canon-tool/1.1 (v2.37+) ·

```json
{
  "validation_id": "VAL-{BRAND_UPPER}-{YYYYMMDD}-{counter}",
  "brand_slug": "{slug}",
  "audience_slug": "{audience_slug from creative.context.angle.audience_ref}",
  "outcome": "{success | neutral | failed | fatigued}",
  "attribution_layer": "{enum 10 valeurs canon-tool/1.1}",
  "validated_at": "{YYYY-MM-DD today}",
  "decay_ttl_days": 90,
  "metric_observed": "{ROAS | CTR | CPA selon outcome driver}",
  "metric_value": {value},
  "test_size": {impressions},
  "context_snapshot": {
    "audience_slug": "{audience_slug}",
    "platform": "meta",
    "season": "{Q1|Q2|Q3|Q4 derived from date}"
  },
  "captured_at": "{ISO date-time now}",
  "captured_by": "import-meta-results",
  "note": "{1-2 sentences contextual · ex 'CRT-NN ran 21d, ROAS 3.2 vs target 2.5 stage maintain, attribution hook curiosity-gap'}",
  "_isolation_boundary": "brand",
  "_promoted_from": "brands/{slug}/creatives/produced/{CRT-NN}.json"
}
```

**Write via `write_to_context`** (NEVER Edit/Write direct JSON) ·

- `field_path` · `resources/canon/copy/{layer}/{tool}.json#/validations[]`
- `mode` · `direct` (capturer silent, pas de proposal)
- `source` · `agent` (auto-tagged capturer)

**Append-only enforce** · jamais overwrite validations[] existantes. Si validation_id collision détectée (rare, même creative re-pulled même date), skip silent + log warning.

**HR-Canon-V11 enforcement** (v2.37+) ·

1. `attribution_layer` enum 10 valeurs obligatoire (hook, angle, framework, archetype, format, targeting, budget, creative_execution, timing, unknown).
2. `validated_at` date YYYY-MM-DD obligatoire.
3. `brand_slug` obligatoire (isolation boundary).
4. `decay_ttl_days` default 90.
5. `_isolation_boundary: "brand"` auto-set.

Si `attribution_layer = "unknown"` (ambiguïté canon-tool layer) → flag operator gate via AskUserQuestion avant write (propose 9 autres valeurs). Empêche pollution silencieuse atlas vivant.

---

## Step 5 · Apply decay v2.37 pré-promotion

Avant tout signal auto-promote (Step 6), apply decay filter sur validations[] existantes canon-tool ·

1. Filter entries où `today > (validated_at + decay_ttl_days)` → state `stale`.
2. Entries stale restent dans log (append-only, jamais effacées) mais ne comptent pas pour auto-promote N≥3 threshold.
3. Compte uniquement entries fresh + outcome ∈ {`success`, `validated`} + `min(confidence_chain) >= 0.7`.

HR-Canon-Decay (v2.37) respecté · empêche atlas canon copy d'absorber des winners anciens devenus obsolètes (red team A4 lock-in protection).

---

## Step 6 · Compute auto-promote signal

Pour chaque canon-tool venant de recevoir nouvelle validation entry ·

1. Read `resources/canon/copy/{layer}/{tool}.json#/validations[]` (full array post-write).
2. Apply decay filter Step 5 · garder entries fresh + outcome success/validated.
3. Compter brands distinctes (unique `brand_slug` values dans entries fresh success).
4. Threshold canon · `N >= 3 brands distinctes validate` → flag auto-promote candidate.

Si candidate flag hit ·

→ **NEVER** auto-promote silent. Operator gate obligatoire (anti-pattern silent promotion).

→ Buffer flag dans `learnings.json` entry append-only (sera processed par `learn-from-session` Trigger 9 next flush operator-gated) ·

```json
{
  "id": "LRN-{NNN}",
  "fact": "Canon-tool {layer}/{tool} validate N={count} brands distinct (success outcome, fresh post-decay)",
  "reasoning": "Pattern reproductible cross-brand observé via import-meta-results · auto-promote candidate vers canon doctrine (Trigger 9 operator gate next flush)",
  "scope": "workspace",
  "platform": "meta",
  "type": "behavior",
  "tags": ["canon-validation", "{layer}", "{tool}", "auto-promote-candidate"],
  "genericity": "sector",
  "status": "active",
  "_promote_candidate": true
}
```

`learn-from-session` Trigger 9 daemon picks up ce learning au prochain flush · surface AskUserQuestion operator pour gate promotion final.

---

## Step 7 · Persist learnings.json append-only (pattern reproductible v2.27)

Per creative importé, append entry `learnings.json` brand-side ·

```json
{
  "id": "LRN-{NNN}",
  "fact": "CRT-{NN} ran {days}j sur Meta · ROAS {value} · outcome {success|neutral|failed|fatigued}",
  "reasoning": "{root cause hypothesis · ex 'hook curiosity-gap performant audience X (ROAS 3.2 vs target 2.5), validation canon-tool layer hooks'}",
  "scope": "brand",
  "platform": "meta",
  "type": "test_result",
  "date": "{YYYY-MM-DD today}",
  "source": "import-meta-results",
  "tags": ["canon-validation", "{outcome}", "{layer canon-tool utilisé}", "{audience_slug}"],
  "status": "active",
  "genericity": "brand",
  "_canon_validations_appended": [
    "resources/canon/copy/{layer1}/{tool1}.json#/validations[VAL-...]",
    "resources/canon/copy/{layer2}/{tool2}.json#/validations[VAL-...]"
  ]
}
```

Write via `write_to_context` à `brands/{slug}/learnings.json#/entries[]`.

Pattern v2.27 reproductible · learning entry trace WHAT (creative results) + WHY (canon-tool attribution) + cross-ref pointer atlas vivant (canon validations[] appendées). Audit trail end-to-end produce → test → learn → promote.

---

## Hard Rules

- **HR1** · Step 0 bridge proactif canon v2.77 MANDATORY · jamais skip access check. Default proactif (a) connect-mcp-server, fallback (b) skip propre (capturer silent, pas blocker).
- **HR2** · Zéro mutation existing validations · append-only strict. Anti-pattern AP-overwrite BANNI (red team A11 mutation silent atlas).
- **HR3** · Canon decay respect v2.37 (HR-Canon-Decay) · filter entries stale pré-auto-promote compute. **NEVER** count stale entries dans N≥3 threshold.
- **HR4** · N≥3 brands threshold canon · auto-promote candidate flag uniquement quand 3+ brands distinctes validate (fresh + success). **NEVER** flag candidate avec N<3.
- **HR5** · Zéro auto-promote sans operator gate · candidate flag écrit `learnings.json` `_promote_candidate: true` · `learn-from-session` Trigger 9 daemon surface AskUserQuestion operator gate canon. **NEVER** write directement `resources/canon/copy/_doctrine/` ou promotion canon sans operator confirmation.
- **HR6** · HR-Canon-V11 schema v1.1 enforce strict (v2.37+) · `attribution_layer` enum 10 valeurs + `validated_at` + `brand_slug` + `decay_ttl_days` + `_isolation_boundary: "brand"`. Si `attribution_layer = "unknown"` → AskUserQuestion gate operator avant write.
- **HR7** · Mode silent canon · mode `silent` frontmatter. Output operator-facing minimal · 1 ligne announce Step 0 OK, 1 ligne summary close (`"Import done · {N} creatives, {M} validations appended, {K} auto-promote candidates flagged"`). **NEVER** verbose recap, **NEVER** 5 sections investigation-posture (curator/producer template, pas capturer).
- **HR8** · Write via `write_to_context` strict · **NEVER** Edit/Write direct sur `.json` files (mutation rule canon). Mode `direct` (capturer pas proposal flow).
- **HR9** · Brand isolation enforce · `_isolation_boundary: "brand"` auto-set sur validations[] entries. Cross-brand read interdit par défaut (red team A7 isolation). Override seulement operator gate explicit Trigger 9.
- **HR10** · Zéro em-dash dans tout output (limited operator-facing). Substituer par virgule, parenthèses, point, deux-points ou middle dot (·). Canon `no_em_dash` strict.
- **HR11** · Pattern v2.27 reproductible · learnings.json entry append-only par creative importé avec cross-ref pointer `_canon_validations_appended[]`. Audit trail end-to-end obligatoire.

---

## Anti-patterns

- **AP-1 · Overwrite validations** · agent remplace entry validations[] existante au lieu d'append. Anti-pattern HR2 BANNI. Pattern canon · append-only strict, validation_id unique générée incrémental.
- **AP-2 · Skip decay filter** · agent compte entries stale dans N≥3 threshold auto-promote. Anti-pattern HR3 BANNI. Pattern canon · decay filter v2.37 pré-compute.
- **AP-3 · Auto-promote silent** · agent promote canon-tool vers `resources/canon/copy/_doctrine/` ou modifie canon principal sans operator gate. Anti-pattern HR5 BANNI (red team A14 promotion sans gate). Pattern canon · candidate flag `learnings.json` · Trigger 9 daemon gate operator AskUserQuestion.
- **AP-4 · Verbose output operator-facing** · agent ship 5 sections investigation-posture pour un capturer silent. Anti-pattern HR7 BANNI. Pattern canon · 1 ligne announce + 1 ligne close, terse.
- **AP-5 · Direct Edit/Write JSON** · agent edit `learnings.json` ou `validations[]` via Edit/Write tools (bypass mutation gate). Anti-pattern HR8 BANNI. Pattern canon · `write_to_context` exclusive.
- **AP-6 · Attribution_layer "unknown" silent** · agent write entry avec `attribution_layer: "unknown"` sans gate operator. Anti-pattern HR6 BANNI. Pattern canon · AskUserQuestion 9 enum options avant write si layer ambigu.
- **AP-7 · Cross-brand read validations[]** · agent lit validations[] d'une autre brand pour compute insight brand active. Anti-pattern HR9 BANNI (red team A7 isolation). Pattern canon · scope `brand_only` enforced sauf override operator Trigger 9.
- **AP-8 · Skip learnings.json append** · agent écrit validations[] canon sans tracer dans `learnings.json` brand-side. Anti-pattern HR11 BANNI (audit trail cassé). Pattern canon · double-write append-only canon + learnings.
- **AP-9 · N<3 threshold bypass** · agent flag auto-promote candidate avec 2 brands ou 1 brand distinct. Anti-pattern HR4 BANNI. Pattern canon · N≥3 strict threshold.
- **AP-10 · Pull insights sur creative non-tagué canon-tools** · agent pull data pour CRT-NN sans aucun `formula_used` / `hook_used` / etc. Pattern canon · filter Step 1 ne garde que creatives avec ≥1 canon-tool tagué (sinon rien à valider).

---

## Cross-refs

- `docs/system/canonical-matrix-reasoning.md` · canon schema + matrix discipline (atlas vivant)
- `docs/system/contextual-intelligence.md` · master doctrine semantic vs mechanical layer
- `docs/system/confidence-propagation.md` · algèbre confidence cascade canon-tool validation
- `docs/system/brand-isolation-doctrine.md` · scope `brand_only` enforced default + canon copy exception
- `docs/system/extension-discovery-discipline.md` v2.75 · pipeline NEW entities auto-consommées
- `learn-from-session` Trigger 9 · daemon operator gate promotion canon validations[] cross-brand
- `audit-creative-fatigue` · sibling curator scan fatigue (vs capturer pull data ici)
- `analyze-perf` · sibling diagnostic deep-dive (vs capturer pull brut ici)
- `routine-perf` · sibling navigator briefing (vs capturer silent ici)
- `capture-learning` · sibling capturer one-off (vs continuous Meta runtime ici)
- `pacing-doctrine.md` v2.78 · seuils canon partagés cross-account
- `resources/conventions/meta-ads.json` · Insights endpoints + rate limits + learned_rules
- `resources/canon/copy/{hooks,frameworks,angles,archetypes-voix,heuristiques-persuasion}/*.json` · canon-tool schema v1.1 target write
- `creative.schema v1.2` · `formula_used`, `framework_used`, `archetype_used`, `hook_used`, `objection_used`, `cta_used` source fields
- `write_to_context` · canonical mutation gate (NEVER bypass)
