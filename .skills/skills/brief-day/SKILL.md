---
name: brief-day
type: navigator
version: "1.1.0"
recommended_model: haiku
reasoning_pattern: null
description: >
  Session-start orientation briefing. Reads workspace state across all brands
  and returns a tight operator-facing summary: portfolio health, pending validations,
  flags, suggested next actions. Zero deliverable, pure orientation.
  FR: "brief", "daily brief", "où j'en suis", "quoi de neuf", "fais-moi le point".
  EN: "brief", "daily brief", "what's up", "where am I", "status".
permissions:
  reads: [brand, product, offer, profile, learning, strategy, visual_identity]
  writes: []
  mode: none
  subagent_safe: true
pipeline:
  preconditions: at least one brand in brands/ (excluding `_`-prefixed)
  postconditions: none, read-only
patch_notes:
  v1.0.0: "v2.39 ship navigator briefing. Read silencieux status.json + pending-validations + todos + learnings + profile + session-state cross-brands · classify health/needs-call/flags/next · output exécutif 5-7 bullets max + AskUserQuestion close. Anti-pattern strict · jamais propose Producer/Orchestrator skill sans demande explicite, jamais file paths/D# en surface, jamais brief >10 bullets quel que soit complexité portfolio."
  v1.1.0: "v2.51 enrichment · État brand info système 3 niveaux descriptif (pull-not-push cohérent v2.50). Section État brand structurée Identité (setup-once · setup brand + audiences) / Inventaire (produits avec spec+photo officielle + assets brand-level logo/badge/mascotte/pattern) / Atlas vivant (angles testés + campagnes encodées par usage terrain). Chaque item · label langage métier opérateur (photo officielle pas packshot, brand pas slug) + état OK/pas encore renseigné + hint passif si pertinent (récupérable depuis ton site / à drop manuellement / se construit au fil des campagnes). Sous-section optionnelle À noter max 2 items gaps fort impact downstream · drop si brand en très bon état. Strict no · pourcentage, level N, completion %, capability menu, jamais nommer skills (craft-packshot, import-asset), jamais flags techniques (_canonical, _validated_by_operator). Posture descriptive neutre · opérateur lit, comprend, décide. Bridge schema visual_identity v1.2 nouveaux slots (assets_canonical · logo_canonical + badge_canonical + mascotte_canonical + pattern_canonical)."
---

# Skill: brief-day

**CRITICAL:** this is a Navigator, invoked directly by the operator for orientation. **NEVER** produce a deliverable. **NEVER** suggest deep work. **ALWAYS** stay in read-only summary mode.

## Tone

Chairman briefing a partner who just walked in. Zero jargon, zero file paths, zero JSON. Plain language, scannable in 30 seconds.

Posture adapted to context: if multi-brand operator (portfolio / agency) → portfolio-lead → principal. If solo brand → senior operator → founder. If early-stage → coach → builder.

---

## Step 1 — Scan workspace state (silent)

Read in parallel, no operator visibility:

- `brands/*/status.json` (exclude `_`-prefixed) for each brand: completeness level, last activity, flags
- `brands/*/pending-validations.md` for each brand: count unchecked items per section (context / access / enrichment / skill-candidates)
- `brands/*/todos.md` for each brand: `## In Progress` + `## P0/P1` top entries
- `brands/*/learnings.json` latest 3 entries (date, fact short)
- `brands/*/brand.json` for each brand: `identity.brand_name` (display label), `audiences_index` (count + labels mère/sous), `_validated_by_operator` gates set
- `brands/*/products/*/spec.json` for each brand: product count + display name + spec completeness flag
- `brands/*/products/*/visual_identity.json` (if present) for each brand × product: `assets_canonical.packshot_front._canonical` presence + `_validated_by_operator` gate
- `brands/*/visual_identity.json` brand-level (if present): `assets_canonical.logo_canonical` / `badge_canonical{}` / `mascotte_canonical` / `pattern_canonical{}` slots filled vs empty
- `brands/*/angles/` or `learnings.json` angle hypotheses: count tested vs validated terrain
- `brands/*/_snapshot.md` digest for fast read fallback if granular JSONs missing
- `operator/profile.json`: preferences.conversation_register, identity.profile, preferences.tracking
- `session-state.md` last 10 activity log lines if present

## Step 2 — Classify what matters (silent)

Bucket detected signals:

- **Brand health**: 1 line per brand — name, completeness level, days since last activity, flag count
- **Needs your call**: items in pending-validations marked critical or blocking (gate access missing on skills operator asked for, inferred audience not yet validated before planned deliverable, etc.)
- **Flags across portfolio**: cross-brand patterns (e.g. 3 brands missing Meta credentials, 2 brands with learnings_stale flag)
- **Next action suggestions** (2-3 max, ranked by impact)

## Step 2bis — Compose État brand · info système (silent, then surface)

**Quand surface.** Si l'opérateur a une seule brand active OU est focalisé sur une brand (last activity < 7 jours, ou brand explicitement mentionnée). Sinon, prefer le format portfolio multi-brands de Step 3 standard et garde l'état brand pour drill explicite.

**Hiérarchie 3 niveaux** (ordre canonique, jamais inversé) :

### Niveau 1 — Identité brand (setup-once)

Ce qui définit qui est la brand. Setup une fois, stable ensuite.

- **Setup** · "complet" (si `wedge_complete: true`) OR "partiel" (si `draft`/`partial`) OR "pas encore engagé" (si `empty`)
- **Audiences** · "N mappées (1 mère, N-1 sous-audiences)" si `audiences_index` populé. Sinon "pas encore mappées · se construit avec setup-brand"

### Niveau 2 — Inventaire produits & assets (ajouts continus)

Ce dont la brand dispose pour produire des créa. Bouge avec chaque ajout.

- **Produits** · "N (Display Name A, Display Name B, +K)" si N≤3 nommer tous, sinon top 3 + "+K autres". Pour chaque produit hero (top 2-3) :
  - "{Display Name} · spec complète · photo officielle prête" si `spec.json` `complete` AND `visual_identity.assets_canonical.packshot_front._canonical: true`
  - "{Display Name} · spec complète · pas encore de photo officielle" + hint passif "récupérable depuis ton site OU à drop" si spec OK mais packshot absent
  - "{Display Name} · spec partielle" si spec incomplète
- **Assets brand** (brand-level, cross-products) :
  - **Logo** · "OK" si `visual_identity.assets_canonical.logo_canonical.path` présent. Sinon "pas encore renseigné · récupérable depuis ton site"
  - **Badges** · "N renseignés ({slug_humain_A}, {slug_humain_B})" si `badge_canonical{}` non-vide. Sinon "pas encore renseignés"
  - **Mascotte** · "OK" si présente, "pas applicable" si brand n'a pas de mascotte selon identité (default), "pas encore renseignée" si brand a mascotte récurrente mais slot vide
  - **Patterns** · "N renseignés" si `pattern_canonical{}` non-vide. Sinon "pas encore renseignés"

### Niveau 3 — Atlas vivant (earned par usage)

Ce que la brand a appris en lançant des campagnes. Se construit avec le temps, pas avec setup.

- **Angles testés** · "N hypothèses · K validés terrain" si `angles/` populé OR `learnings.json` contient angle_hypothesis entries. Sinon "0 angles encodés · se construit au fil des campagnes"
- **Campagnes lancées** · "N résultats encodés" si `learnings.json` contient campaign_result entries. Sinon "0 résultats encodés · se construit au fil des campagnes"

### Sous-section optionnelle — "À noter (si pertinent pour toi)"

Max **2 items** courts, gaps fort impact downstream. Posture info, jamais push. Drop entièrement si brand en très bon état.

Triggers acceptables (signal → 1-line surface) :
- Produit avec spec complète mais pas de photo officielle → "Tu n'as pas encore de photo officielle pour {Display Name} · sur tes prochaines pubs {Display Name}, le produit peut bouger légèrement."
- 0 résultats campagnes encodés ET angles testés > 0 → "0 résultats campagnes encodés · pour l'instant tes angles sont en hypothèse, le système ne peut pas encore prioriser ce qui marche vs ce qui rate."
- Logo brand absent ET >1 produit avec photo officielle → "Pas de logo brand renseigné · tes pubs ne pourront pas être brandées pixel-exact tant que ce n'est pas là."
- Audiences inférées jamais validées ET deliverable planifié → "Tes audiences sont inférées mais pas validées · ce qui sera produit pour elles peut dériver."

**Jamais** dépasser 2 items. **Jamais** nommer skill en surface (`craft-packshot`, `import-asset`, `setup-brand`, etc.). **Jamais** flag technique (`_canonical`, `_validated_by_operator`, `audiences_index`). **Jamais** injonction (`tu dois`, `il faut`, `complete ceci`).

## Step 3 — Deliver the brief

**ALWAYS** in executive format. 5-7 bullets max for portfolio summary. **NEVER** dump raw data. Si focus mono-brand ou single-brand workspace, surface l'État brand 3 niveaux composé en Step 2bis à la place du Portfolio health.

**Template portfolio multi-brands** (adapt, never paste literally):

> **Portfolio health**
> - Northsense: Level 2 complete, last session 2 days ago. 1 flag (learnings_stale)
> - {brand B}: Level 1, last session today, clean
> - {brand C}: Level 1 draft, 4 days idle, `access_missing Meta`
>
> **Needs your call (2)**
> - Northsense inferred audience (Maghrebi/ME women) never validated, will contaminate next brief
> - {brand C} Meta access still pending client-side, blocking the audit you queued
>
> **Pattern I noticed**
> - 2 of your 3 brands miss Meta credentials. Worth batching a client outreach?
>
> **Suggested next**
> - Validate Northsense audience (15 min, unlocks brief-créa)
> - Or skip to {brand B} if you prefer momentum

**Template focus mono-brand** (adapt, never paste literally) :

> **État brand · Glowco**
>
> Identité
>   Setup · complet
>   Audiences · 3 mappées (1 mère, 2 sous-audiences)
>
> Inventaire
>   Produits · 3 (Cell Boost, Glow Boost, +1)
>     Cell Boost · spec complète · photo officielle prête
>     Glow Boost · spec complète · pas encore de photo officielle (récupérable depuis ton site OU à drop)
>   Assets brand
>     Logo · pas encore renseigné · récupérable depuis ton site
>     Badges · pas encore renseignés
>     Mascotte · pas applicable
>     Patterns · pas encore renseignés
>
> Atlas vivant
>   Angles testés · 5 hypothèses · 0 validés terrain
>   Campagnes lancées · 0 résultats encodés
>
> À noter (si pertinent pour toi)
>   - Tu n'as pas encore de photo officielle pour Glow Boost · sur tes prochaines pubs Glow Boost, le produit peut bouger légèrement.
>   - 0 résultats campagnes encodés · pour l'instant tes angles sont en hypothèse, le système ne peut pas encore prioriser ce qui marche vs ce qui rate.

**ALWAYS** close with smart suggests a/b/c/d using `AskUserQuestion` tool (load via `ToolSearch(select:AskUserQuestion)` if not loaded). Example options: *"Validate Northsense audience / Switch to {brand B} / Show full state of one brand / Other"*.

---

## Step 4 — What this skill NEVER does

- **NEVER** propose to run a Producer or Orchestrator skill without explicit operator request. Daily-brief orients, doesn't commit.
- **NEVER** expose file paths, field names, routing destinations, D# numbers.
- **NEVER** list all brands if portfolio > 5. Summarize: "{5 active, 2 need attention, see show-progress for full list}".
- **NEVER** give a brief longer than 10 bullets, regardless of workspace complexity. Pare down ruthlessly.
- **NEVER** surface pourcentage, "X/Y completed", "level N", capability menu ("tu peux faire X") dans l'État brand section. Posture descriptive info-system, pas push.
- **NEVER** nommer un skill (`craft-packshot`, `import-asset`, `setup-brand`, `mine-voc`, etc.) en surface dans l'État brand ou la sous-section À noter. Le système est invisible, l'opérateur ne lit que langage métier.
- **NEVER** flag technique en surface (`_canonical`, `_validated_by_operator`, `assets_canonical`, `audiences_index`, `wedge_complete`). L'opérateur lit "photo officielle prête" pas "packshot canonical validated".
- **NEVER** injonction dans l'État brand (`tu dois`, `il faut`, `complete ceci`, `manque ceci`). Soft offer indirecte uniquement : "récupérable depuis ton site" (= hint passif).
- **NEVER** plus de 2 items dans la sous-section À noter. Si rien à signaler, drop entièrement la sous-section.

## Edge cases

- **Zero brands** → redirect: *"No brand configured yet. Run setup-brand or drop a URL."*
- **Single brand** → format État brand 3 niveaux (Step 2bis), pas de Portfolio health. Plus sous-section À noter max 2 items si pertinent. Drop section À noter entièrement si brand en très bon état.
- **Brand fraîchement setup, 0 produits encore** → Identité OK, Inventaire `Produits · pas encore renseigné · se construit avec ajout produit`, Atlas vivant `0 angles encodés · se construit au fil des campagnes`. Pas de sous-section À noter (rien d'actionnable encore).
- **Brand sans visual_identity.json** → tous slots assets brand `pas encore renseigné · récupérable depuis ton site` (logo, badges, patterns) ou `pas applicable` (mascotte default).
- **Operator just landed, no session-state.md** → treat as fresh start, mention "welcome back" once if > 3 days since last activity
- **Mode detected from operator/profile.json.preferences.conversation_register** → (1) grounded = more explanation of what each item means, (4) technical = pure bullet points zero fluff
