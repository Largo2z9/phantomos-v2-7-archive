---
name: phantom
description: Cockpit PhantomOS. Sans arg, vue workspace (tous brands + état global). Avec un brand slug, vue détaillée du brand. Read-only.
---

# /phantom, cockpit

Vue synthétique du workspace PhantomOS. Lecture seule, aucune mutation. Read top to bottom before acting.

## Mode detection

Navigation pattern is **terminal-like**: `/phantom` lands at the workspace level (even with a single brand), `/phantom {slug}` drills into a brand, `/phantom {slug} {entity}` zooms further into a specific entity within a brand. The operator learns the system the way they learn `cd` and `ls`: top-down, never short-circuited.

Check the user's argument :

| Argument | Mode |
|---|---|
| empty (just `/phantom`), 0 brand encodé | **bootstrap** : message "tape /tour pour démarrer" |
| empty, ≥1 brand encodé | **workspace** : always shows the workspace-level view, regardless of brand count. Operator drills explicitly via `/phantom {slug}`. |
| `workspace` or `all` | **workspace** : alias, same as empty when ≥1 brand exists |
| brand slug (e.g. `/phantom vitatone`) | **brand** : cockpit détaillé du brand |
| brand slug + entity (e.g. `/phantom vitatone audiences`) | **entity-drill** : zoom dense sur une entité spécifique du brand |
| brand slug + entity + item (e.g. `/phantom karacare audiences chute-active`) | **item** : preview d'un item unique (audience, angle, product) |
| `search {keyword}` (e.g. `/phantom search chute`) | **search** : grep cross-brand sur slugs, names, voc, learnings |
| `recent` ou `recent {N}` | **recent** : timeline des N dernières mutations (default 10) |
| `todo` | **todo** : vue agrégée des next-suggested cross-brand priorisés |
| `?` ou `help` | **help** : cheatsheet auto-générée de tous les modes |

---

## Mode bootstrap

```
PHANTOMOS · workspace vide
══════════════════════════════════════════════
Aucun brand encodé pour l'instant.

→ Tape /tour pour démarrer le setup d'un premier brand.
→ Tape /skills pour voir les capacités disponibles.
```

Stop ici.

---

## Mode workspace

Vue globale du workspace, multi-brand + opérateur + capacités.

### Sources à lire (read-only)

1. `operator/profile.json` → identité opérateur, register, contexts.
2. `operator/awareness.json` → tour status, concepts introduits.
3. `brands/` → liste des dossiers brand (ignorer ceux préfixés `_`).
4. Pour chaque brand : `brands/{slug}/_snapshot.md` (digest) + `brands/{slug}/status.json` (level).
5. `.skills/_manifest.json` → count skills shipped vs custom.
6. `session-state.md` racine → last session timestamp.
7. `connected-sources.json` racine (si existe) → sources globales connectées (cross-brand).

### Format de rendu workspace

```
PHANTOMOS WORKSPACE
══════════════════════════════════════════════
Operator        {operator_name_or_id}
Capacités       {N} skills ({M} custom)
Dernière session                {time_ago}

BRANDS ({count})
{brand_lines}

CROSS-BRAND
Tests actifs                    {total_active_tests}
Connected sources globales      {global_sources_summary}

NEXT SUGGESTED (priorité)
{suggested_actions}

→ Tape /phantom {brand_slug} pour drill sur un brand.
→ Tape /skills pour voir les capacités.
```

### Brand lines (mode workspace)

Une ligne compacte par brand, ordonnée par activité récente :

```
{icon} {slug}              L{level}    {entity_summary}    last {time_ago}
```

Icônes :
- `🟢` : actif (last session < 7j) et niveau ≥ L2
- `🟡` : actif mais sub-L2, ou L2+ mais inactif (7-30j)
- `⚪` : dormant (> 30j sans session)

`entity_summary` : count condensé "{products}P / {audiences}A / {angles}An / {tests}T". Skip si entité absente.

Exemples :
```
🟢 vitatone              L2     1P / 5A / 8An / 3T    last 14h
🟡 peaktrek            L1     1P / 2A / 0An         last 6d
⚪ northsense           L2     1P / 4A / 5An         last 47d
```

### Cross-brand metrics

- **Total tests actifs** : somme des `tests actifs` de chaque brand (entries learnings.json type=test-result, status absent ou inconclusive ou fatigued).
- **Connected sources globales** : si `connected-sources.json` racine existe (sources cross-brand comme un Meta Business Manager partagé), lister les plateformes avec last_sync agrégé. Sinon dire "(per-brand only)".

### Next suggested workspace-level

3 propositions max, ordonnées par priorité. **Each line MUST be a paste-ready command, not a conversational suggestion.** Format : *"→ Tape : `{exact natural-language command}` ({why, in one short clause})"*. The operator copies the back-tick content into the next prompt and the agent picks it up.

Sources :
- Brand dormant > 60j → *"→ Tape : `archive {slug}` ({slug} sans activité depuis {N} jours)"*
- Tests fatiguing dans plusieurs brands → *"→ Tape : `refresh angles fatigués sur {slug-le-plus-fatigué}` ({N} angles ROAS en chute)"*
- Operator profile incomplet → *"→ Tape : `densifie mon profil opérateur` (3 champs manquants : stack actuelle, register, contexte macro)"*
- Skill `audit-meta-account` jamais run sur un brand actif → *"→ Tape : `audit Meta sur {slug}` (token connecté, jamais audité)"*
- Niveau de contexte global moyen sub-L2 → *"→ Tape : `enrichis le contexte de {slug}` (L1, le brand le plus en retard)"*

Anti-pattern : *"→ Lancer un audit Meta dès que possible"* (passif, l'opérateur doit re-formuler). Always paste-ready, always specific.

---

## Mode brand

Vue détaillée d'un brand spécifique.

### Sources à lire (read-only, dans l'ordre)

1. `brands/{slug}/_snapshot.md` (digest 1-2KB pré-généré). Si absent, déclencher `python3 .skills/build-brand-snapshot.py {slug}` puis re-lire.
2. `brands/{slug}/status.json` → `wedge_complete`, `completeness_scores`, niveau de contexte L1/L2/L3.
3. `brands/{slug}/brand.json` → `meta.name`, `meta.sector`, `meta.updated`.
4. `brands/{slug}/products/` → liste, count, last update par produit.
5. `brands/{slug}/audiences/` → liste, count, validation_status par audience (hypothesis / tested / validated / scaled / fatigued), sourcing complétude.
6. `brands/{slug}/angles/` (si existe) → count par validation_status.
7. `brands/{slug}/strategy.json` → `meta.updated`.
8. `brands/{slug}/learnings.json` → count entries, count tests par status, tests actifs.
9. `brands/{slug}/connected-sources.json` (si existe) → liste plateformes connectées avec last_sync.
10. `brands/{slug}/session-state.md` (si existe) → last brand-scoped session.

### Format de rendu brand

```
PHANTOMOS · brand: {brand_name}
══════════════════════════════════════════════
Substrat        L{level}/L3   {progress_bar}  {pct}% encodé
Dernière session                 {time_ago}
Tests actifs                     {count} ({fatiguing_count} fatiguing)
Backlog                          {hypothesis_count} hypothèses

ENTITIES
{entity_status_lines}

CONNECTED SOURCES
{connected_sources_lines}

NEXT SUGGESTED (priorité)
{suggested_actions}
```

### Entity status lines (mode brand)

Pour chaque entité majeure, format :

```
{icon} {entity}     {detail}
```

Icônes :
- `✓` : entité encodée, fraîche (updated < 7 jours)
- `⚠` : entité encodée mais avec gaps ou stale (incomplete sourcing, validation pending, updated > 14 jours)
- `✗` : entité absente ou bloquante

Exemples :
- `✓ brand              updated 2d ago`
- `✓ products/main      updated 1w ago`
- `⚠ audiences          3 of 5 sourced (manque {missing_slug})`
- `⚠ angles             2 validated, 4 hypothèses, 2 fatigués`
- `✗ strategy           no Q2 update` (si stale > 90j)

Ordre d'affichage : brand, products, offers, audiences, angles, strategy, learnings.

### Audience hierarchy (mode brand)

When audiences are organized as mère / sous-audiences (introduced v2.19.0), expand the audiences row into an indented hierarchy view. Detect via `meta.parent_slug` in each `audiences/{slug}/profile.json`.

Format :

```
{icon} audiences         {N} groupes principaux + {M} sous-groupes
   ├─ {parent_slug}      {scope}    {validation_label}    {fields_filled_pct}
   │   ├─ {sub_slug}     {scope}    {validation_label}    {fields_filled_pct}
   │   └─ {sub_slug}     {scope}    {validation_label}    {fields_filled_pct}
   └─ {parent_slug}      {scope}    {validation_label}    {fields_filled_pct}
       └─ {sub_slug}     {scope}    {validation_label}    {fields_filled_pct}
```

`validation_label` translation (NEVER expose `validation_status` enum directly to the operator):
- `hypothesis` → `à valider`
- `tested` → `testée`
- `validated` → `validée`
- `scaled` → `scalée`
- `fatigued` → `fatiguée`

`fields_filled_pct` is a coarse completeness signal: count non-null fields in `pain_points[]`, `voice.key_expressions[]`, `psychology.beliefs_*`, `objections[]` divided by expected. Surface as `mining: vide` (0%), `mining: partiel` (1-50%), `mining: dense` (>50%). NEVER expose the percentage as a number.

Real example:

```
⚠ audiences           2 groupes + 5 sous-groupes (mining: vide)
   ├─ pousse-projet         groupe    à valider    mining: vide
   │   ├─ pousse-jeune-adulte  sous   à valider    mining: vide
   │   └─ pousse-recovery      sous   à valider    mining: vide
   └─ chute-active          groupe    à valider    mining: vide
       ├─ chute-post-grossesse  sous  à valider    mining: vide
       ├─ chute-hormonale-stress sous à valider    mining: vide
       └─ chute-traction        sous  à valider    mining: vide
```

If `mining: vide` on most sub-groups, the *Next suggested* block should propose `mine-voc` as priority 1.

If audiences exist but no parent_slug links (legacy flat structure), skip the hierarchy view and use the legacy single-line format.

### Connected sources lines (mode brand)

Pour chaque source, format :

```
{icon} {platform}        {status_detail}
```

Icônes :
- `✓` : connectée, last sync récent (< 7 jours)
- `⚠` : connectée mais sync stale (> 7 jours)
- `○` : non connectée mais pertinente

Exemples :
- `✓ Meta Ads            synced 2h ago`
- `⚠ Klaviyo             synced 9d ago`
- `○ TikTok Ads          not connected`

Si `connected-sources.json` absent : afficher *"(non configurées, voir /skills connect)"*.

### Next suggested (mode brand)

3 propositions max, ordonnées par priorité décisionnelle. **Each line MUST be a paste-ready command**, not a conversational suggestion. Format : *"→ Tape : `{exact natural-language command}` ({why, one short clause})"*. The operator copies the back-tick content into the next prompt.

Sources :
- Tests fatiguing → *"→ Tape : `refresh l'angle {angle_id}` (ROAS -42% sur 14j)"*
- Audiences avec mining vide → *"→ Tape : `lance mine-voc sur {slug}` (7 audiences en hypothèse, aucun verbatim encore)"*
- Stale > 14j sur entité critique → *"→ Tape : `mets à jour {entity}` (dernière modif il y a {N}j)"*
- Niveau sub-L2 → *"→ Tape : `densifie le contexte de {slug}` ({N} fields manquants critiques)"*
- Connected source non configurée mais pertinente → *"→ Tape : `connecte Meta Ads sur {slug}` (token attendu dans credentials.env)"*

Anti-pattern : *"→ Lancer mine-voc dès que possible"* (passif, vague). Always paste-ready, always specific. The single back-tick wrap is a visual contract · the operator knows that what's inside the back-ticks is what they paste back.

---

## Mode entity-drill

`/phantom {brand_slug} {entity}` zooms on one entity within the brand. Dense, no top-level KPIs, no connected sources, no other entity rows. The operator chose the entity so the rendering goes deeper than brand mode allows in 50 lines.

Supported entities: `audiences`, `angles`, `products`, `offers`, `strategy`, `learnings`.

### Common header (all entity drills)

```
PHANTOMOS · brand: {brand_name} · {entity}
══════════════════════════════════════════════
```

Then entity-specific body, then a single Next-suggested block specific to this entity (max 3 lines, paste-ready).

### `audiences` · full hierarchy + per-audience completeness detail

For each audience folder under `brands/{slug}/audiences/`:
- Indented per `meta.parent_slug` (mother audiences flat, sub-audiences indented one level).
- Per audience : `slug`, `scope`, `validation_label` (translated from `validation_status`), `pain_signal` (filled / empty), `voice_signal` (filled / empty), `objection_signal` (filled / empty), `last_updated`.

Format example :

```
{slug}                     {scope}    {validation_label}    pain: {filled|vide}    voice: {filled|vide}    obj: {filled|vide}    last {time_ago}
   ├─ {sub_slug}           ...
```

End with paste-ready next-suggested specific to audience gaps (mine-voc on missing pain, validate hypothesis blocks, merge low-signal sub-audiences, etc.).

### `angles` · list + status

Per angle in `brands/{slug}/angles/` :
- `angle_id`, `name`, `audience_target`, `status` (draft / live / fatigued / paused), `roas` if test_result exists, `last_updated`.

End with paste-ready commands : refresh fatigued, validate draft, archive paused.

### `products` · list + completeness per spec

Per product in `brands/{slug}/products/{slug}/spec.json` :
- `slug`, `name`, `category`, `pricing_filled` (yes/no), `mechanism_filled` (yes/no), `composition_filled` (yes/no), `last_updated`.

End with paste-ready : densify thinnest spec, snapshot a new product.

### `offers` · table per product

Per offer file `brands/{slug}/products/{p}/offers.json`, render the `offer_groups[].offers[]` :
- `offer_id`, `name`, `type` (single / subscription / bundle / quantity_break / prepay), `price`, `savings_pct`, `active`.

End with paste-ready : connect Shopify if missing, mark inactive offers, etc.

### `strategy` · current focus + Q-target snapshot

Read `strategy.json`. Render :
- Annual goals (1-line each).
- Current quarter focus.
- Last update timestamp.

End with paste-ready : update quarter focus, set new Q-target.

### `learnings` · last 10 entries

Per entry in `learnings.json#entries[]` (newest first, capped at 10) :
- `id`, `kind` (test_result / workaround / compliance / observation / decision_trace), `fact` (truncated to 1 line), `created_at`.

End with paste-ready : capture-learning on a recent observation, promote a learning to brand-level rule.

### Hard rule for entity-drill

If `{entity}` is unsupported (not in the list above), surface : *"Entité '{x}' pas reconnue. Disponibles : audiences, angles, products, offers, strategy, learnings. Tape `/phantom {brand}` pour la vue brand complète."*

---

## Mode item (niveau 3)

`/phantom {brand_slug} {entity} {item-slug}` zooms on ONE item inside an entity. Le rendering équivalent d'un *file preview* dans un Finder. Operator vient de drill quelque chose de spécifique : on déballe ce qu'on a, sans tout dump.

Header breadcrumb obligatoire :

```
workspace > {brand_slug} > {entity} > {item-slug}
══════════════════════════════════════════════
```

### Pour `audiences/{slug}`

Lecture : `brands/{brand}/audiences/{item-slug}/profile.json`. Rendering human-readable :

```
{NOM} · {scope} · {validation_label}
{Brève description si identity.description filled}

PROFIL
  Genre        {gender ou "non précisé"}
  Tranche      {age_range ou "non précisée"}
  Pain         {pain.primary_problem ou "à confirmer en mining"}
  Émotions     {psychology.emotions[] ou "vide"}
  Goals        {psychology.goals[] ou "vide"}

VOIX (sourcée)
  Vocabulaire à utiliser    {voice.vocabulary_to_use[] ou "vide"}
  Vocabulaire à éviter      {voice.vocabulary_to_avoid[] ou "vide"}
  Expressions clés          {N} captées (mining: {dense|partiel|vide})

PAIN POINTS
  {N} encodés ({M} sourcés). Top 3 par priorité affichés en 1 ligne chacun.

OBJECTIONS
  {N} encodées. Top 3 par fréquence affichées.

HIÉRARCHIE
  Parent: {parent_slug ou "(racine)"}
  Sous-audiences: {liste des sous-slugs ou "aucune"}

NEXT SUGGESTED (priorité)
  → Tape : `lance mine-voc sur {brand_slug} pour {item-slug}` (mining vide, prochaine étape logique)
  → Tape : `valide point par point l'audience {item-slug}` (corriger, rejeter, accepter)
  → Tape : `produce-paid-angles {brand_slug} sur {item-slug}` (passe à la production hypothesis-grade)
```

### Pour `angles/{id}`

Lecture : `brands/{brand}/angles/{id}.json` ou agrégat `brands/{brand}/angles.json`. Rendering :

```
{NOM_ANGLE} · {status} · {audience_target}
{Synopsis 1-2 phrases}

CIBLE              {audience_slug}
PROMESSE           {promise ou "non posée"}
PROOF / MÉCANIQUE  {mechanism ou "non posé"}
HOOKS              {N} testés, {M} live, {K} fatigués
TESTS              {ROAS si dispo, sinon "pas de test posté"}

NEXT SUGGESTED
  → Tape : `refresh l'angle {id}` ({raison liée au statut})
  → Tape : `produce-copy-brief {brand_slug} sur l'angle {id}` (passer en brief créa)
```

### Pour `products/{slug}`

Lecture : `brands/{brand}/products/{slug}/spec.json` + `offers.json`. Rendering :

```
{NOM_PRODUIT} · {category}
{Description 1-2 lignes}

PROMESSE          {promise.headline ou "non posée"}
MÉCANISME         {unique_mechanism.name ou "non posé"}
COMPOSITION       {N composants encodés / total attendus}
PROBLÈMES RÉSOLUS {N encodés}
BÉNÉFICES         {N encodés}
PRIX              {pricing.price} {currency}
OFFRES            {N actives} (cure 1m, 3m, 6m si dispo)

NEXT SUGGESTED
  → Tape : `densifie la spec {slug}` (champs manquants : {liste})
  → Tape : `audit l'offre {slug}` (vérifier cohérence prix/cure/économies)
```

### AskUserQuestion (mode item)

| Slot | Rôle |
|---|---|
| 1 | Action top-priority sur l'item (paste-ready) |
| 2 | Action 2 (paste-ready) |
| 3 | *"Drill {sibling}"* · un autre item du même entity-drill (typiquement le suivant alphabétique ou le voisin hiérarchique pour les audiences) |
| 4 | *"Retour {entity}"* · relance `/phantom {brand} {entity}` |

### Hard rule for item mode

Si `{item-slug}` n'existe pas, surface : *"Item '{x}' pas trouvé dans `{entity}` de `{brand}`. Disponibles : {liste des slugs trouvés}. Tape `/phantom {brand} {entity}` pour la vue entity complète."*

---

## Mode search

`/phantom search {keyword}` cherche le mot-clé cross-brand sur tous les champs textuels indexables (slugs, names, descriptions, voc.key_expressions, pain_points, learnings.fact, strategy.goals).

Implémentation : invoquer `python3 .skills/phantom-search.py "{keyword}"` qui retourne un JSON array `[{path, type, brand_slug, slug, field, snippet}]`.

Header breadcrumb :

```
workspace > search "{keyword}"
══════════════════════════════════════════════
{N} matches · cross-brand
```

Rendering : un block par match (cap 20 affichés, mention si plus existent) :

```
{type} · {brand_slug}/{slug}
  {snippet avec keyword en gras ou highlight}
  → Tape : `/phantom {brand_slug} {entity} {slug}` pour drill
```

Group par `brand_slug`. Ordre par pertinence (matches sur `meta.name` en haut, matches sur descriptions/snippets en bas).

### AskUserQuestion (mode search)

| Slot | Rôle |
|---|---|
| 1 | Drill 1er match (paste-ready `/phantom {brand} {entity} {slug}`) |
| 2 | Drill 2e match |
| 3 | Drill 3e match |
| 4 | *"Retour workspace"* · relance `/phantom` |

Si 0 match : empty state pédagogique : *"Aucun match pour '{keyword}'. Tape `/phantom search` avec un autre terme, ou `/phantom todo` pour voir ce qui est actif."* Pas d'AskUserQuestion dans ce cas.

---

## Mode recent

`/phantom recent` ou `/phantom recent {N}` (default N=10, max 50) liste les dernières mutations cross-brand en timeline lisible.

Implémentation : invoquer `python3 .skills/phantom-recent.py {N}` qui retourne un JSON array d'événements lus depuis `.phantom/context-engine-events.jsonl`.

Header breadcrumb :

```
workspace > recent
══════════════════════════════════════════════
Dernières {N} mutations · cross-brand
```

Rendering : un par ligne (compact) :

```
{time_ago}    {brand_slug}    {entity}    {action} {field_extrait}
                              → {reason si présent, sinon vide}
```

Exemple :
```
14h ago       karacare        audiences/chute-active     set meta.validation_status = "hypothesis"
                                                         → validated hierarchy
2d ago        vitatone        learnings                  append entry "test FB ad #3 ROAS 4.2"
6d ago        karacare        brand                      set positioning.tagline
```

### AskUserQuestion (mode recent)

| Slot | Rôle |
|---|---|
| 1 | Drill le brand le plus actif récent (paste-ready `/phantom {brand_slug}`) |
| 2 | Drill l'entity la plus modifiée (paste-ready `/phantom {brand_slug} {entity}`) |
| 3 | Drill un item du top match si pertinent |
| 4 | *"Retour workspace"* |

Si event log vide : *"Pas encore de mutations enregistrées. Reviens après ta première session de mining ou de snapshot."*

---

## Mode todo

`/phantom todo` agrège les next-suggested top-priority de tous les brands actifs (skip dormants > 60j sauf `--all`). Vue cross-brand des actions à faire.

Header breadcrumb :

```
workspace > todo
══════════════════════════════════════════════
{N} actions actives · {M} brands
```

Rendering (top 5 max) :

```
{priority_icon} [{brand_slug}] {action description}
   → Tape : `{paste-ready commande}` ({why})
```

`priority_icon` : `🔥` (urgent : tests fatigués, brand stale > 30j sur entité critique), `⚡` (à faire bientôt : audiences en mining vide, angles draft), `·` (peut attendre).

Exemple :
```
🔥 [vitatone] 2 angles ROAS en chute libre depuis 7j
   → Tape : `refresh les angles fatigués sur vitatone`

⚡ [karacare] 7 audiences en hypothèse, aucun verbatim encore
   → Tape : `lance mine-voc sur karacare`

⚡ [karacare] strategy.json sans focus Q2 posé
   → Tape : `pose le focus Q2 de karacare`

· [northsense] dormant depuis 47j, peut-être à archiver
   → Tape : `archive northsense`
```

### AskUserQuestion (mode todo)

| Slot | Rôle |
|---|---|
| 1 | Action 🔥 #1 (paste-ready) |
| 2 | Action ⚡ #2 (paste-ready) |
| 3 | *"Drill {brand_slug}"* du brand qui concentre le plus d'actions |
| 4 | *"Retour workspace"* |

Si 0 todo (workspace serein) : *"Tout est calme. Pas d'action urgente. Profite ou commence un nouveau brand."*

---

## Mode help (?)

`/phantom ?` ou `/phantom help` rend une cheatsheet auto-générée. Court, dense.

Format :

```
PHANTOMOS · /phantom cheatsheet
══════════════════════════════════════════════
NAVIGATION
  /phantom                       vue workspace (default)
  /phantom {brand}               cockpit du brand
  /phantom {brand} {entity}      drill dense sur une entité
  /phantom {brand} {entity} {item}   preview d'un item

UTILITAIRES
  /phantom search "{keyword}"    grep cross-brand
  /phantom recent [N]            timeline des N dernières mutations (default 10)
  /phantom todo                  next-suggested cross-brand priorisés
  /phantom ?                     cette cheatsheet

ENTITÉS DRILLABLES
  audiences, angles, products, offers, strategy, learnings

NAVIGATION RAPIDE
  Chaque rendering termine par 4 boutons cliquables (drill, drill latéral, action, retour parent).
  Slot 4 toujours = retour parent. Tu ne te perds jamais.

EXEMPLES CONCRETS
  /phantom karacare audiences chute-active
  /phantom search "post-grossesse"
  /phantom recent 20
```

Pas d'AskUserQuestion en mode help. C'est une référence, pas un point d'action.

---

## Empty states pédagogiques

Quand un rendering rencontre du vide, ne rends pas du vide · propose le next move concret. Toujours.

| Situation | Empty state output |
|---|---|
| Workspace mode, 0 brand | (déjà couvert par mode bootstrap) |
| Brand mode, 0 produit | *"Pas encore de produit encodé sur `{brand}`. Tape `snapshot {brand} avec {url}` pour scaffold le hero produit."* |
| Brand mode, 0 audience | *"Pas encore d'audience sur `{brand}`. Snapshot va proposer une cartographie. Sinon : `lance mine-voc sur {brand}` pour partir du verbatim client."* |
| Entity-drill audiences, 0 audience | *"Pas d'audience encodée. Tape `/phantom {brand}` puis snapshot le hero pour scaffold les groupes principaux."* |
| Entity-drill angles, 0 angle | *"Pas d'angle produit. Tape `produce-paid-angles {brand}` après mine-voc pour générer un set ranked."* |
| Entity-drill learnings, 0 entry | *"Pas de learning capturé. Tape `/learn-from-session` après une correction pour verrouiller la première règle."* |
| Entity-drill products, 0 produit | (idem brand mode 0 produit) |
| Entity-drill offers, 0 offer | *"Pas d'offre. Snapshot du hero produit scaffold les offres depuis l'API ou demande au pixel."* |
| Entity-drill strategy, 0 strategy | *"Pas de stratégie posée. Tape `pose le focus Q{n} sur {brand}` pour cadrer."* |
| Item mode, slug introuvable | (déjà couvert par hard rule item mode) |
| Search 0 match | (déjà couvert par mode search) |
| Recent log vide | (déjà couvert par mode recent) |
| Todo vide | (déjà couvert par mode todo) |

Hard rule : **toujours offrir un next move dans l'empty state**. Jamais juste *"rien à afficher"*.

---

## Status indicators enrichis

Étend la table d'icônes existante (mode brand, mode entity-drill, mode workspace) avec :

| Icône | Sens |
|---|---|
| `✓` | encodé, frais (< 7j) |
| `⚠` | encodé avec gaps ou stale (7-14j) |
| `✗` | absent ou bloquant |
| `○` | non connecté (sources) |
| `🔥` | stale critique (> 90j) ou tests en chute libre |
| `⏳` | mining ou sync en cours (background task active) |
| `🆕` | créé < 24h (highlight des derniers ajouts) |

Application : utiliser `🔥` quand un test ROAS chute ≥30% sur 14j ou quand un brand a > 90j sans activité. `⏳` quand `_mining_status: "running"` détecté ou un sub-agent background actif. `🆕` quand `meta.created_at` < 24h ou si jamais affiché à l'opérateur (track via `awareness.json#/items_seen[]`, futur P2).

---

## Footer hint discoverability

À la fin de chaque rendering (workspace, brand, entity-drill, item, search, recent, todo), juste avant l'AskUserQuestion, insérer une ligne subtle :

```
─────
`/phantom ?` pour voir tous les modes · `/phantom search` pour chercher
```

**Cap discoverability sans bruit.** Si l'opérateur a déjà tapé `/phantom ?` dans la session courante (track ephemeral), skip cette ligne. Sinon : présente, faible opacité visuelle.

---

## Constraints (tous modes)

- **Read-only.** Aucune mutation. Si l'opérateur demande ensuite de fix quelque chose, propose le skill approprié, ne fais pas la mutation toi-même.
- **One screen output.** Workspace mode : 30 lignes max. Brand mode : 40-50 lignes max. Entity-drill mode : 50 lignes max.
- **Pas de jargon doctrine.** Pas de "SED", "CMR", "_field_types", "validation_status" en surface. Traduit en mots métier (validé / hypothèse / fatigué).
- **Honest staleness.** Si une entité n'a pas été touchée depuis 90j, dis-le. Si snapshot date > 1h, regenère silencieusement avant d'afficher.
- **Workspace est le default.** `/phantom` sans argument lande toujours au niveau workspace (sauf bootstrap si 0 brand). L'opérateur drille explicitement via `/phantom {slug}`. Pattern terminal-like, jamais court-circuiter la navigation.
- **Drill par étape, pas en bloc.** `/phantom {slug}` montre le brand. `/phantom {slug} {entity}` zoome sur une entité. Évite de tout dump en une fois ; économie de contexte ET de lisibilité.
- **Next-suggested = paste-ready.** Toutes les actions surfacées dans NEXT SUGGESTED doivent être copiables verbatim dans le prompt suivant. Format : *"→ Tape : `{commande exacte}` ({why})"*. Jamais de conseil passif type *"Lancer mine-voc dès que possible"*.
- **Navigation cliquable systématique.** Chaque rendering `/phantom` (workspace, brand, entity-drill) se conclut PAR un AskUserQuestion natif qui propose la navigation suivante. Voir section *Navigation interactive* ci-dessous.

---

## Navigation interactive (AskUserQuestion)

Le terminal n'a pas de flèches haut/bas pour naviguer. AskUserQuestion compense : à chaque niveau, l'opérateur reçoit 4 options cliquables qui structurent la navigation comme dans un dossier imbriqué (drill plus profond, drill latéral, agir, remonter). Le rendering textuel reste · l'AskUserQuestion s'AJOUTE à la fin pour accélérer la navigation, jamais ne la remplace.

### Contrat universel des 4 options

Indépendamment du mode, le AskUserQuestion respecte la grammaire suivante :

| Slot | Rôle | Source de l'option |
|---|---|---|
| 1 | **Drill vertical** : aller plus profond dans la hiérarchie courante | mode-spécifique (voir tableaux ci-dessous) |
| 2 | **Drill vertical alternatif OU drill latéral** : autre branche au même niveau | mode-spécifique |
| 3 | **Action top-priority** : la 1re ligne de NEXT SUGGESTED (paste-ready, déclenche la commande au clic) | dérivée du même calcul que NEXT SUGGESTED |
| 4 | **Remonter d'un niveau OU exit** : navigation vers le parent | toujours présent, jamais omis |

**Hard rule.** Le slot 4 est toujours un retour vers le niveau parent (ou exit en workspace mode). L'opérateur sait qu'il peut toujours remonter en 1 click, même s'il s'est égaré.

### Workspace mode · slots concrets

| Slot | Question rendue (FR) |
|---|---|
| 1 | *"Drill {brand_le_plus_actif}"* (brand avec last_session le plus récent) |
| 2 | *"Drill {brand_en_alerte}"* (brand avec tests fatigués OU stale > 30j OU mining vide), ou si aucun : *"Drill {2e brand le plus actif}"* |
| 3 | NEXT SUGGESTED top-priority cross-brand (paste-ready commande) |
| 4 | *"Voir un autre brand / continuer"* (free-text fallback, l'opérateur peut taper `/phantom {autre_slug}`) |

**Cas N=1 brand** : slots 1 + 3 + 4 only (3 options visibles). Slot 2 omis car redondant.

### Brand mode · slots concrets

| Slot | Question rendue (FR) |
|---|---|
| 1 | *"Drill audiences"* (entity-drill audiences) |
| 2 | *"Drill {entity_la_plus_chargée}"* · celle avec le plus d'instances ou l'état le plus actif (typiquement `angles` ou `learnings`) |
| 3 | NEXT SUGGESTED top-priority sur ce brand (paste-ready commande) |
| 4 | *"Retour workspace"* (déclenche `/phantom`) |

### Entity-drill mode · slots concrets

| Slot | Question rendue (FR) |
|---|---|
| 1 | NEXT SUGGESTED top-priority spécifique à l'entité (paste-ready commande) |
| 2 | NEXT SUGGESTED 2e-priority sur la même entité (paste-ready commande) |
| 3 | *"Drill {entity_voisine}"* (autre entity-drill du même brand, choisie par pertinence : depuis audiences → angles, depuis angles → audiences, depuis products → offers, depuis learnings → strategy) |
| 4 | *"Retour {brand_slug}"* (déclenche `/phantom {brand_slug}`) |

### Saturation pattern

Si la session courante a déjà déclenché 3 AskUserQuestion `/phantom` dans les 5 dernières minutes, le 4e rendu désactive le AskUserQuestion (rendering text-only). L'opérateur est en mode exploration profonde et le pattern interactif devient du bruit. Re-active après 5 min sans `/phantom` ou après un autre type de skill exécuté.

### Formulation de l'AskUserQuestion

Présenter les 4 slots dans cet ordre fixe (drill primaire, drill secondaire, action, retour). Phrasing court, jamais explicatif. Exemple sur brand mode karacare :

```
question: "Tu veux faire quoi ?"
options:
- "Drill audiences (7 audiences à valider)"
- "Drill angles (5 hypothèses)"
- "Lance mine-voc sur karacare"
- "Retour workspace"
```

L'opérateur clique. L'agent exécute :
- Slots 1, 2 → relance `/phantom {slug} {entity}` ou `/phantom`
- Slot 3 → exécute la commande paste-ready (snapshot, mine-voc, audit, etc.)
- Slot 4 → relance `/phantom` (workspace) ou `/phantom {slug}` (brand) selon le niveau parent.

### Anti-patterns

- **5 options ou plus.** Cap dur à 4. Si plus de candidats existent, dégrader vers free-text fallback (slot 4).
- **Slot 4 absent.** L'opérateur doit toujours pouvoir remonter en 1 click. Jamais de cul-de-sac.
- **Action non-paste-ready dans slot 3.** Le slot action déclenche une commande exécutable, pas un conseil. *"Pense à mine-voc"* est un anti-pattern.
- **AskUserQuestion sans rendering text.** Le rendering reste TOUJOURS, l'AskUserQuestion vient APRÈS. Le rendering est l'information, l'AskUserQuestion est l'accélérateur de navigation.
