---
name: validate-brand-voice-consistency
type: curator
version: "1.0.0"
recommended_model: sonnet
isolation_scope: brand
layer: production
description: >
  Scan cross-touchpoint brand outputs (paid creatives produced/{CRT-NN}.json
  copy + organic posts si existing + CRM email sequences si existing + UI
  microcopy landing si existing + PDP if existing) · score voice axes
  alignment vs brand.json#/tone_of_voice canon (Nielsen Norman 4D · 4
  axes scoring -5 à +5) · surface drift cross-touchpoint avec corrections
  sourcées brand voice chart canon. Curator scan automatique post-shipped
  outputs. Output 5 sections investigation-posture + drift severity scoring
  (consistent · soft drift · medium drift · critical drift) + corrections
  proposées per touchpoint. Step 0 bridge proactif canon v2.77 si brand
  voice chart non shipped (define-brand-voice prerequisite).
  FR: "validate brand voice", "check voice consistency", "scan voice drift",
      "audit voice cross-touchpoint", "verify brand voice".
  EN: "validate brand voice", "check voice consistency", "scan voice drift",
      "voice audit cross-touchpoint", "verify brand voice".
permissions:
  reads: ["brands/{slug}/brand.json", "brands/{slug}/creatives/", "brands/{slug}/organic/", "brands/{slug}/email-sequences/", "brands/{slug}/landing/", "brands/{slug}/brand_voice_chart.md"]
  writes: ["brands/{slug}/audits/{date}_voice-consistency.md"]
  mode: interactive
  subagent_safe: true
extension_hooks:
  consumable_by: ["brand_entity", "creative_entity"]
disambiguates_against:
  - "analyze-copy · audit copy single touchpoint avec 12 dimensions tagging
     vs validate-brand-voice-consistency · scan cross-touchpoint multi-source"
  - "audit-creative-fatigue · détection fatigue performance creative-level
     vs validate-brand-voice-consistency · drift voice tonality cross-touchpoint"
  - "define-brand-voice · produce voice chart upstream
     vs validate-brand-voice-consistency · scan validation downstream post-shipped"
pipeline:
  preconditions: |
    brands/{slug}/brand.json exists.
    brands/{slug}/tone_of_voice non-empty (style + register minimum).
    Au moins UN touchpoint shipped pour scan (creatives/produced/ OR organic/ OR email-sequences/ OR landing/ OR products/{slug}/copy.md).
  postconditions: |
    Audit markdown persisté brands/{slug}/audits/{YYYY-MM-DD}_voice-consistency.md.
    Si drift severity >= medium, reco trigger recompose-creative OR define-brand-voice update surfacée operator.
    Si confidence finding >= 0.7, propose chain capture-learning silent.
---

# Skill: validate-brand-voice-consistency

Scanner cross-touchpoint cohérence brand voice. Pull paid creatives copy + organic posts + CRM email sequences + UI microcopy landing + PDP, score voice axes alignment (Nielsen Norman 4D · 4 axes -5 à +5) vs `brand.json#/tone_of_voice` canon. Surface drift severity cross-touchpoint avec corrections sourcées. Curator scan downstream post-shipped outputs, ne produit pas copy variants (recompose-creative downstream).

## Expert methodology

**Canonical expert persona**: senior brand strategist, brand voice consistency monitoring cross paid + organic + CRM + UI.

**Framework**: Nielsen Norman Group 4D voice scoring canon × per-touchpoint sampling × drift severity classification (consistent · soft · medium · critical) × do_lexicon / dont_lexicon adherence check × corrections sourcées brand voice chart.

**Matrix** (applied per sample): *voice axis × score sample × score canon · drift delta · severity threshold · directional read*.

**Codified reference**: `brand.schema.json#/tone_of_voice` (canon style + register + banned_words + frequent_words), `docs/system/investigation-posture.md` (5 sections obligatoires), `brand_voice_chart.md` shipped via `define-brand-voice` upstream (4D axes scoring + do/don't lexicon).

---

## Step 0 · Gate access + bridge proactif canon v2.77 (MANDATORY)

**CRITICAL:** verify brand voice chart shipped AVANT scan touchpoints. **NEVER** silently degrade sans signaling à l'opérateur. **NEVER** improviser voice axes canon sans source brand voice chart.

1. **brand.json#/tone_of_voice presence check.** Verify `brands/{slug}/brand.json` exists AND `tone_of_voice` non-null (style + register minimum).
2. **voice_axes 4D check.** Read `brands/{slug}/brand_voice_chart.md` si exists. Verify 4 axes Nielsen Norman scoring canon présents (funny↔serious, formal↔casual, respectful↔irreverent, enthusiastic↔matter-of-fact). Voice chart shipped → ground truth complète. Voice chart absent → degraded mode signaled.
3. **do_lexicon / dont_lexicon check.** Read brand.json#/tone_of_voice.banned_words + brand.json#/tone_of_voice.frequent_words. Si voice chart shipped, read voice_chart do_lexicon + dont_lexicon sections additional canon.

**Branching canon proactif v2.77** (AskUserQuestion via `ToolSearch(select:AskUserQuestion)`) ·

- **Voice chart shipped (voice_axes 4D + do/don't lexicon canon)** → announce, proceed Step 1 ·
  > *"Brand voice chart canon shipped pour {brand}. Je scan les touchpoints cross paid/organic/CRM/UI et compare aux 4 axes voice canon. 2-3 min, je reviens avec l'audit drift cross-touchpoint."*

- **Voice chart non shipped (brand.json#/tone_of_voice basic existing)** → AskUserQuestion 2 options ·
  - (a) "Je te guide pour shipper le voice chart canon via define-brand-voice upstream (~5 min · voice_axes 4D + do/don't lexicon). L'audit devient factuel sourced canon."
  - (b) "Je bascule en degraded mode · scan vs brand.json#/tone_of_voice.style/register basic existing. Output flag confidence faible (pas de canon 4D pour reference)."

  **Default proactif** · proposer (a) si l'opérateur veut audit rigoureux, fallback (b) si urgence scan immediate.

---

## Step 1 · Cross-touchpoint scan list

Scan brand-side, list tous les touchpoints shippés audit-ables ·

**Paid creatives** ·
- Path · `brands/{slug}/creatives/produced/`
- Files · `CRT-NN.json` chacun
- Extraction · `copy_outputs.headlines[]`, `copy_outputs.descriptions[]`, `copy_outputs.ctas[]` (per creative)
- Count · N creatives scanned avec copy_outputs non-null

**Organic posts** ·
- Path · `brands/{slug}/organic/`
- Files · si existing (Twitter · LinkedIn · TikTok · Instagram captions)
- Extraction · post body + captions
- Count · N posts scanned

**CRM email sequences** ·
- Path · `brands/{slug}/email-sequences/`
- Files · si existing (welcome series, abandoned cart, post-purchase, etc.)
- Extraction · subject lines + email body
- Count · N emails scanned

**UI microcopy landing** ·
- Path · `brands/{slug}/landing/`
- Files · si existing
- Extraction · headlines + subheadlines + CTAs + tooltips + error messages
- Count · N landing pages scanned

**PDP product copy** ·
- Path · `brands/{slug}/products/{product_slug}/copy.md`
- Files · si existing
- Extraction · product description + benefits + features copy
- Count · N PDPs scanned

**Buffer** · table interne agent `{touchpoint_type, file_path, samples_count, sample_excerpts[]}`. Si zéro touchpoint shippé OR moins de 2 touchpoints → close cleanly · *"Audit cross-touchpoint nécessite minimum 2 touchpoints shippés. Actuellement {N} dispo. Reviens quand tu auras shipped plus de outputs."*

---

## Step 2 · Voice axes scoring per touchpoint sample

Pour chaque sample buffered, scoring 4D Nielsen Norman canon ·

**Axe 1 · Funny ↔ Serious** (-5 à +5)
- -5 · très funny (humor dominant, memes, irreverent)
- 0 · neutre
- +5 · très serious (formal, factual, gravitas)

**Axe 2 · Formal ↔ Casual** (-5 à +5)
- -5 · très formal (vouvoiement, structures complexes, jargon technique)
- 0 · neutre
- +5 · très casual (tutoiement, contractions, langue parlée)

**Axe 3 · Respectful ↔ Irreverent** (-5 à +5)
- -5 · très respectful (déférent, prudent, conventional)
- 0 · neutre
- +5 · très irreverent (provocateur, anti-establishment, edgy)

**Axe 4 · Enthusiastic ↔ Matter-of-fact** (-5 à +5)
- -5 · très enthusiastic (exclamations, emphase, hyperbole)
- 0 · neutre
- +5 · très matter-of-fact (sobre, descriptive, sans amplification)

**Per-touchpoint aggregation** · moyenne arithmétique des samples du touchpoint per axis. Output internal · table `{touchpoint × axe × score_avg × variance × n_samples}`.

**Comparison vs canon** · si `brand_voice_chart.md` shipped → read voice_axes canon values. Si pas shipped (degraded mode) → infer canon depuis `brand.json#/tone_of_voice.register` + `style` (mapping basic · casual → axe 2 = +3, formal → axe 2 = -3, etc.). Flag confidence dégradée.

---

## Step 3 · Drift detection canon

Per axis per touchpoint, compute drift severity ·

**Formula** · `drift_delta = abs(score_touchpoint - score_canon)`

**Seuils canon** ·

| Drift delta | Severity | Signification |
|---|---|---|
| `≤ 1` | **Consistent** | Cohérent canon, tolérance bruit échantillonnage |
| `2-3` | **Soft drift** | Warning, surveiller mais non-bloquant |
| `4-5` | **Medium drift** | Flag medium, corrections recommandées prochaine production |
| `≥ 6` | **Critical drift** | Contradiction voice canon, corrections urgentes (recompose-creative trigger candidate) |

**Per-touchpoint global drift score** · max(drift_delta across 4 axes). Severity touchpoint = severity du max axis.

**Compound drift detection** · 2+ axes en medium drift simultanés sur même touchpoint → upgrade severity → critical (drift cumulatif).

**Cross-touchpoint drift detection** · si même axis drift >= medium sur 2+ touchpoints distincts → flag systemic (issue brand voice training cross-team, pas touchpoint isolé).

**Output compute internal** · table `{touchpoint × axe × score × canon × delta × severity}`. **NEVER** surface table brute à l'opérateur, intermediate computation invisible.

---

## Step 4 · Do/don't lexicon violations scan

**banned_words detection** ·
- Source canon · `brand.json#/tone_of_voice.banned_words[]` + voice_chart dont_lexicon (si shipped)
- Scan · regex case-insensitive sur tous samples buffered
- Output · table `{touchpoint × banned_word × occurrences × sample_excerpts}`

**Missing key_expressions detection** ·
- Source canon · si voice_chart shipped, read do_lexicon key_expressions[]
- Scan · count occurrences cross-touchpoint
- Flag · si key_expression absent dans 80%+ touchpoints scanned → voice drift (canon vocabulary non-adopted)

**do_lexicon adherence check** ·
- Source canon · voice_chart do_lexicon[] (si shipped)
- Scan · ratio words from do_lexicon présents vs total words sample
- Severity ·
  - `ratio ≥ 15%` · canon adopté
  - `ratio 5-15%` · partial adoption
  - `ratio < 5%` · canon non-adopté (warning)

**Aggregation** · score per touchpoint = banned_words count + key_expressions miss count + do_lexicon ratio. Contribute to severity classification Step 3.

---

## Step 5 · 5 sections investigation-posture output (operator-facing)

Format founder-facing scannable. **NEVER** dump tableaux exhaustifs raw data, **NEVER** verbose prose narrative, **NEVER** > 30 lignes total output.

### Section 1 · Observé (faits sourcés)

Liste compacte par touchpoint scanné, chiffres précis ancrés source.

```
Observé · audit voice consistency {brand_humain} ({date})

Scan · {N} touchpoints shippés ({list types})
- Paid creatives · {N} CRT scannés, {M} samples copy (headlines + descriptions + CTAs)
- Organic posts · {N} posts scannés (Twitter + Instagram captions)
- CRM emails · {N} séquences scannées ({M} subject lines + bodies)
- UI landing · {N} pages scannées (headlines + CTAs)
- PDP · non shippé pour le moment

Canon référence · brand_voice_chart.md shipped ({voice_axes 4D + do/don't lexicon canon)
```

### Section 2 · Déduit (drift severity findings · confidence chain)

Chaque flag drift posé comme hypothèse avec confidence + indicateurs sources. Pas affirmé comme fait.

```
Déduit · {N} flags drift + {N} touchpoints consistent

H1 · Paid creatives drift critical Axis 1 (Funny↔Serious)
  Score canon · -2 (légèrement funny)
  Score samples paid · +4 (matter-of-fact serious)
  Delta · 6 → critical
  Confidence · forte (15/15 samples convergents)
  Reco · recompose-creative sur CRT-12, CRT-08, CRT-15 (variant_axis = copy_tone_swap)

H2 · CRM emails drift medium Axis 2 (Formal↔Casual)
  Score canon · +3 (casual)
  Score samples CRM · -1 (formal-neutre)
  Delta · 4 → medium
  Confidence · moyenne (8/12 samples convergents, variance élevée séquence-à-séquence)
  Reco · onboarding copywriter CRM voice chart canon

Organic posts · consistent (drift ≤ 1 sur 4 axes)
UI landing · consistent (drift ≤ 1 sur 4 axes)

Banned words violations · 3 occurrences "medical-grade" detected (CRT-08, CRT-15, email welcome-3)
```

### Section 3 · Inconnu (variables non observables)

Variables critiques qu'on ne peut pas lever depuis scan brand-side. Max 3-4 items.

```
Inconnu

- Intent drift volontaire vs accidental (test sérieux nouveau segment ? OR junior copywriter pas calibrated ?)
- Performance impact drift (drift = perf better OR worse ? → cross-ref creatives metrics + email open rates)
- Drift cumulatif temporal (drift récent dernière prod ? OR historic baseline ?)
```

### Section 4 · Leviers (drill-down skills/actions)

Pour chaque flag, quel skill/action permet de driller ou agir. Max 3-4 leviers.

```
Leviers

- Critical drift CRT-12/CRT-08/CRT-15 → recompose-creative variant_axis=copy_tone_swap (préserve concept, recalibre voice)
- Medium drift CRM emails → define-brand-voice update si voice chart needs refresh
- Cross-touchpoint coaching → audit-creative-fatigue side-check (drift signal fatigue compound ?)
- Performance correlation → analyze-perf cross-référence drift vs CTR/CVR
```

### Section 5 · Close ouvert (UNE question macro)

UNE question macro à l'opérateur. Pas synthèse fermée.

```
Sur les 3 creatives critical drift Axis 1, on lance recompose-creative maintenant ou tu valides d'abord la cause root (junior copywriter ? OR test délibéré nouveau ton ?) ?
```

Use `AskUserQuestion` tool pour smart suggests si pertinent (load via `ToolSearch(select:AskUserQuestion)` if not loaded). Options adaptive selon flags, **NEVER** options génériques pre-templated.

---

## Step 6 · Persist audit markdown

Write audit markdown à `brands/{slug}/audits/{YYYY-MM-DD}_voice-consistency.md`. Sections obligatoires ·

1. **Scope** · N touchpoints scannés, M samples total, canon référence (voice chart shipped OR degraded mode brand.json basic).
2. **Summary table per touchpoint** · colonnes `touchpoint | samples | axis 1 delta | axis 2 delta | axis 3 delta | axis 4 delta | severity`.
3. **Drift severity scoring per axis** · pour chaque axe Nielsen Norman canon (Funny↔Serious, Formal↔Casual, Respectful↔Irreverent, Enthusiastic↔Matter-of-fact), canon score + per-touchpoint scores + critical drift detected list.
4. **Do/don't lexicon adherence** · banned words detected (count + samples), key expressions missing (count + touchpoints), do_lexicon adoption ratio per touchpoint.
5. **Corrections proposées per touchpoint** · per touchpoint flagé, evidence sample + fix direction sourcée canon.
6. **Skills triggers recommandés** · recompose-creative variant_axis=copy_tone_swap pour critical drift, define-brand-voice update si voice chart refresh systemic, audit-creative-fatigue side-check correlation.
7. **Cross-refs** · brand_voice_chart.md, investigation-posture.md, recompose-creative, define-brand-voice.

**NEVER** Edit/Write JSON directly. Markdown audit OK direct write (audit log, not entity). Append-only (suffix `_2` si re-run same date).

---

## Step 7 · Capture-learning silencieux si confidence finding >= 0.7

Si UNE finding au moins atteint confidence forte (≥ 0.7 dans confidence chain canon) ET outcome explicit (drift confirmed cross-touchpoint, pas hypothèse faible) ·

→ Trigger silencieux `capture-learning` avec entry ·

```json
{
  "fact": "Drift voice consistency {severity} sur {touchpoint_type} {brand} ({axis} delta {value} vs canon)",
  "reasoning": "{root cause hypothesis from audit · ex 'copywriter junior pas calibrated voice chart' OR 'test délibéré tone shift non-documenté'}",
  "scope": "brand",
  "type": "behavior",
  "tags": ["voice-consistency", "{drift_axis}", "{touchpoint_type}"],
  "genericity": "brand"
}
```

Cross-ref · `learn-from-session Trigger 9` daemon peut promouvoir cette finding cross-brand canon validations[] si N≥3 brands valident même pattern drift voice cross-touchpoint.

---

## Hard Rules

- **HR1** · 5 sections investigation-posture output obligatoire (Observé / Déduit / Inconnu / Leviers / Close ouvert). Anti-pattern AP-5 doctrine investigation-posture BANNI (synthèse close affirmative).
- **HR2** · Drift severity seuils canon chiffrés strict · `≤ 1` consistent, `2-3` soft, `4-5` medium, `≥ 6` critical. **NEVER** improviser des seuils différents.
- **HR3** · Per-touchpoint scoring obligatoire (pas global brand level only). Chaque touchpoint évalué indépendamment avant aggregation cross-touchpoint.
- **HR4** · do_lexicon / dont_lexicon adherence check obligatoire dans audit. banned_words detection + key_expressions miss + do_lexicon ratio computed per touchpoint.
- **HR5** · Persist audit markdown à `brands/{slug}/audits/{date}_voice-consistency.md` mandatory (pas only conversation output). Append-only (suffix `_2` si re-run same date).
- **HR6** · Recos trigger skills downstream explicit · recompose-creative (variant_axis=copy_tone_swap pour critical drift) OR define-brand-voice update (medium drift systemic). **NEVER** recos vagues "améliorer la cohérence".
- **HR7** · Step 0 bridge proactif canon v2.77 MANDATORY · jamais skip voice chart shipped check. Default proactif (a) define-brand-voice upstream, fallback (b) degraded mode signaled. **NEVER** silently degrade.
- **HR8** · JAMAIS affirmer drift comme un fait. Tout flag = hypothèse avec confidence chain explicite (forte / moyenne / faible / TRÈS faible). Anti-pattern AP-1 doctrine investigation-posture BANNI.
- **HR9** · JAMAIS trigger recompose-creative silent sans operator gate. Audit propose reco, operator décide trigger. Mode `interactive` (pas `direct`).
- **HR10** · JAMAIS expose internal compute table {axis × score × delta} brute à l'opérateur. Intermediate computation invisible. L'opérateur lit "Paid creatives drift critical Axis 1 (confidence forte)", pas "score=+4 vs canon=-2, delta=6 > threshold=6".
- **HR11** · Zéro em-dash dans tout output. Substituer par virgule, parenthèses, point, deux-points ou middle dot (·). Canon `no_em_dash` strict.
- **HR12** · Format founder-facing scannable 30s, max 30 lignes output operator-facing. **NEVER** dump tableaux exhaustifs raw data, **NEVER** verbose prose narrative.

---

## Anti-patterns

- **AP-1 · Scan global brand level only** · agent évalue voice consistency sans granularité per-touchpoint. Pattern canon · per-touchpoint scoring obligatoire avant aggregation cross-touchpoint (HR3).
- **AP-2 · Drift detection sans seuils chiffrés** · agent dit *"drift détecté"* sans quantifier delta vs canon. Anti-pattern HR2 BANNI. Pattern canon · seuils chiffrés strict (`≤ 1` / `2-3` / `4-5` / `≥ 6`).
- **AP-3 · Output verbose sans synthèse actionnable** · agent ship 80 lignes prose narrative analyse drift. Pattern canon · format founder-facing scannable 30s, max 30 lignes operator-facing (HR12).
- **AP-4 · Recos vagues "améliorer la cohérence"** · agent dit *"recalibrer voice cross-touchpoint"* sans trigger skill explicit. Pattern canon · recos trigger skills downstream explicit (recompose-creative variant_axis=copy_tone_swap, define-brand-voice update) (HR6).
- **AP-5 · Skip Step 0 gate voice chart** · agent assume voice chart shipped et compute drift vs canon inexistant. Pattern canon · Step 0 bridge proactif canon v2.77 MANDATORY (HR7).
- **AP-6 · Affirme drift comme fait** · agent dit *"Les creatives sont incohérents."* Hypothèse présentée comme fait. Anti-pattern AP-1 doctrine investigation-posture BANNI. Pattern canon · *"Drift Axis 1 confirmed CRT-12 (confidence forte · 15/15 samples convergents)"* (HR8).
- **AP-7 · Skip Section 5 close ouvert** · agent ferme audit avec synthèse complète sans question. Anti-pattern AP-5 doctrine investigation-posture BANNI. Pattern canon · UNE question macro Section 5.
- **AP-8 · Dump exhaustif raw data** · agent ship table 50 lignes par touchpoint × 4 axes × N samples. Pattern canon · pre-process intelligence, surface uniquement findings synthétisés (HR10).
- **AP-9 · Trigger recompose-creative silent** · agent invoque recompose-creative direct post-audit sans operator gate. Anti-pattern HR9 BANNI. Pattern canon · audit = curator scan + reco, recompose = producer action operator-validated.
- **AP-10 · Compound drift ignoré** · agent flag chaque axis isolément sans détecter compound (2+ axes medium simultanés). Pattern canon · upgrade severity → critical si compound drift detected (Step 3).

---

## Cross-refs

- `docs/system/investigation-posture.md` · 5 sections obligatoires output stratégique
- `docs/system/canonical-matrix-reasoning.md` · matrix-driven drift compute
- `docs/system/skill-routing-doctrine.md` · skill routing canon (analyze-copy single-touchpoint, validate-brand-voice-consistency cross-touchpoint)
- `define-brand-voice` · upstream prerequisite (produce voice chart 4D axes + do/don't lexicon)
- `produce-positioning-canvas` · sister Sprint v2.80 (brand positioning canvas cross-référencé voice cohérence)
- `recompose-creative` · downstream trigger (variant_axis=copy_tone_swap pour critical drift creatives)
- `analyze-copy` · sister single-touchpoint deep audit (12 dimensions tagging vs cross-touchpoint scan ici)
- `audit-creative-fatigue` · sibling curator scan (creative-level fatigue vs voice tonality cross-touchpoint ici)
- `learn-from-session` Trigger 9 · daemon promote cross-brand canon validations[] si pattern N≥3 brands
- `capture-learning` · downstream silent capture findings confidence forte
- `brand.schema.json#/tone_of_voice` · canon référence (style + register + banned_words + frequent_words)
- `creative.schema v1.2` · variant_axis enum reference (copy_tone_swap downstream recompose-creative)

---

*This skill evolves. When the operator corrects an audit verdict, the correction is encoded via `correct-skill` as a Hard Rule above. Rules are cumulative and permanent.*
