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
| `canon` | **canon-index** : liste des atlas du métier disponibles (workspace-level, transversal aux brands) |
| `canon {atlas}` | **canon-layers** : liste des couches d'un atlas (ex: `/phantom canon copy`) |
| `canon {atlas} {layer}` | **canon-tools** : liste des outils d'une couche (ex: `/phantom canon copy hooks`) |
| `canon {atlas} {layer} {tool}` | **canon-tool-card** : fiche détaillée d'un outil canon (ex: `/phantom canon copy hooks curiosity-gap`) |
| `{brand} briefs` | **briefs-drill** : DB Briefs créatifs (liste, statut, lien angle source) |
| `{brand} tests` | **tests-drill** : DB Tests live + résultats observés + verdict winner_proxy |
| `{brand} matrix` | **matrix-drill** : output `score-matrix` (matrice scorée + top territoires + trous) |
| `{brand} atlas` | **atlas-overview** : vue d'ensemble atlas brand (synthèse 6 entités + dérivés) |
| `doctrine` | **doctrine** : rend doctrine cartographie compositionnelle (méthode + équation V3.1) |
| `doctrine audiences` | **doctrine-audiences** : framework cartographie audiences (4 questions) |
| `{brand} audiences` | **audiences-tree** : arbre hiérarchie audiences + chevauchements |
| `{brand} products {p_slug} mechanisms` | **mechanisms-drill** : array `mechanisms[]` typé depuis `spec.json` |
| `{brand} products {p_slug} benefits` | **benefits-drill** : array `benefits[]` (chain functional/emotional/identity) |

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

SUGGESTIONS DAEMON (smart-suggest learn-from-session Trigger 8)
{daemon_patterns_or_silence}

→ Tape /phantom {brand_slug} pour drill sur un brand.
→ Tape /skills pour voir les capacités.
```

`daemon_patterns_or_silence` lit le buffer pattern-detection (cross-skills, recurring frictions, decision reversals, encoded fact drift). Si présents, lister 1-3 patterns détectés sous forme paste-ready. Sinon afficher *"aucune suggestion daemon active"*. Source : `docs/system/pattern-detection-triggers.md`.

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
Cartographie    {level}/3 niveaux   {progress_bar}  {pct}% rempli
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

### Audience binding par produit (mode brand)

Chaque audience peut être taggée avec `meta.applies_to_products[]` (slugs de produits qu'elle vise). Lors du rendering de la ligne audiences en mode brand, ajouter un breakdown par produit :

```
⚠ audiences           7 (5 sur hair-boost, 3 sur cellule-boost, 0 brand-wide)
```

Audiences avec `applies_to_products` vide = brand-wide (visible sur tous les produits). Audiences avec plusieurs slugs comptent dans plusieurs colonnes du breakdown. Si seul `meta.product_id` (legacy) est présent, le lire comme `[product_id]` pour le breakdown.

### Audience hierarchy (mode brand)

When audiences are organized as mère / sous-audiences (introduced v2.19.0), expand the audiences row into an indented hierarchy view. Detect via `meta.parent_slug` in each `audiences/{slug}/profile.json`.

Format :

```
{icon} audiences         {N} audiences mères + {M} poches
   ├─ {parent_slug}      mère      {validation_label}    {fields_filled_pct}
   │   ├─ {sub_slug}     poche     {validation_label}    {fields_filled_pct}
   │   └─ {sub_slug}     poche     {validation_label}    {fields_filled_pct}
   └─ {parent_slug}      mère      {validation_label}    {fields_filled_pct}
       └─ {sub_slug}     poche     {validation_label}    {fields_filled_pct}
```

`validation_label` translation (NEVER expose `validation_status` enum directly to the operator):
- `hypothesis` → `à valider`
- `tested` → `testée`
- `validated` → `validée`
- `scaled` → `scalée`
- `fatigued` → `fatiguée`

`fields_filled_pct` is a coarse completeness signal: count non-null fields in `pain_points[]`, `voice.key_expressions[]`, `psychology.beliefs_*`, `objections[]` divided by expected. Surface as `témoignages: vide` (0%), `témoignages: partiels` (1-50%), `témoignages: denses` (>50%). NEVER expose the percentage as a number.

Real example:

```
⚠ audiences           2 audiences mères + 5 poches (témoignages: vide)
   ├─ pousse-projet         mère     à valider    témoignages: vide
   │   ├─ pousse-jeune-adulte  poche  à valider    témoignages: vide
   │   └─ pousse-recovery      poche  à valider    témoignages: vide
   └─ chute-active          mère     à valider    témoignages: vide
       ├─ chute-post-grossesse  poche à valider    témoignages: vide
       ├─ chute-hormonale-stress poche à valider   témoignages: vide
       └─ chute-traction        poche à valider    témoignages: vide
```

If most poches show `témoignages: vide`, the *Next suggested* block should propose `récupère les témoignages clients` as priority 1.

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
- Audiences avec témoignages vide → *"→ Tape : `récupère les témoignages clients sur {slug}` (7 audiences à valider, aucun témoignage encore)"*
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
- Per audience : `slug`, `scope`, `validation_label` (translated from `validation_status`), `pain_signal` (filled / empty), `voice_signal` (filled / empty), `objection_signal` (filled / empty), `applies_to` (produits ou `brand-wide`), `last_updated`.

Format example :

```
{slug}                     {scope}    {validation_label}    pain: {filled|vide}    voice: {filled|vide}    → {applies_to}    last {time_ago}
   ├─ {sub_slug}           ...
```

`applies_to` formatting (lit `meta.applies_to_products[]`, fallback sur `meta.product_id` legacy si vide) :
- non-empty → liste les slugs séparés par virgule (ex: `→ hair-boost, cellule-boost`)
- empty + product_id null → `→ brand-wide`
- empty + product_id set (legacy) → `→ {product_id}` avec astérisque

End with paste-ready next-suggested : mine-voc sur missing pain, drill par produit `/phantom {brand} products {p}` pour filtrer, valider hypothesis blocks, merge low-signal sub-audiences.

### Filtrage par produit (entity-drill audiences)

Si l'opérateur tape `/phantom {brand} products {p_slug}` (item mode produit, voir plus bas), la fiche produit liste automatiquement les audiences dont `applies_to_products` contient `{p_slug}`. Pas de mode séparé `/phantom {brand} {product} audiences` (cap CLI à 3 niveaux). Le drill par produit se fait via item-mode produit.

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

> **Split externe v2.36** : full spec rendering (audiences/{slug}, angles/{id}, products/{slug}) + AskUserQuestion + hard rule → `.claude/commands/phantom-modes/item.md`. Lire ce fichier quand l'opérateur tape `/phantom {brand} {entity} {item}`.

`/phantom {brand_slug} {entity} {item-slug}` zooms on ONE item inside an entity. Le rendering équivalent d'un *file preview* dans un Finder. Operator vient de drill quelque chose de spécifique : on déballe ce qu'on a, sans tout dump.

Bref : 3 entités drillables (`audiences/{slug}`, `angles/{id}`, `products/{slug}`), header breadcrumb obligatoire, AskUserQuestion 4 slots (action 1 / action 2 / drill sibling / retour entity), hard rule sur slug introuvable. Spec complète dans le split.

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

CANON DU MÉTIER (workspace-level)
  /phantom canon                 atlas du métier (copy, et autres à venir)
  /phantom canon copy            11 couches de copywriting
  /phantom canon copy hooks      6 outils de hook
  /phantom canon copy hooks curiosity-gap   fiche détaillée

ENTITÉS DRILLABLES
  audiences, angles, products, offers, strategy, learnings

NAVIGATION RAPIDE
  Chaque rendering termine par 4 boutons cliquables (drill, drill latéral, action, retour parent).
  Slot 4 toujours = retour parent. Tu ne te perds jamais.

EXEMPLES CONCRETS
  /phantom karacare audiences chute-active
  /phantom search "post-grossesse"
  /phantom recent 20
  /phantom canon copy frameworks pas

ROUTING SKILLS
  Par intention (je veux X) ? consulter `.skills/INDEX.md` (skills par objectif)
  State-driven (je veux voir l'état Y) ? rester ici dans /phantom
```

Pas d'AskUserQuestion en mode help. C'est une référence, pas un point d'action.

---

## Mode canon (atlas du métier, workspace-level)

> **Split externe v2.36** : full spec → `.claude/commands/phantom-modes/canon.md`. Lire ce fichier quand l'opérateur tape `/phantom canon[...]`. 4 sous-modes (`canon`, `canon {atlas}`, `canon {atlas} {layer}`, `canon {atlas} {layer} {tool}`), impl `python3 .skills/phantom-canon.py [atlas] [layer] [tool]`, AskUserQuestion 4 slots (drill voisin / drill couche / applique au brand / retour parent).

---

## Mode briefs-drill

`/phantom {brand} briefs` rend la DB Briefs créatifs (briefs produits via `produce-copy-brief`). Workspace tabular, parité Notion Stride-Up.

Lecture : `brands/{brand}/briefs/*.json` (ou agrégat `brands/{brand}/briefs.json`).

Header breadcrumb :

```
workspace > {brand} > briefs
══════════════════════════════════════════════
{N} briefs · {N_draft} draft · {N_shipped} shipped · {N_validated} validated

BRIEFS RÉCENTS
  [BRF-03] · 2026-05-06 · ANG-01 · post-grossesse · draft
  [BRF-02] · 2026-05-04 · ANG-02 · stress hormonal · shipped
  [BRF-01] · 2026-04-28 · ANG-04 · croissance-projet · validated
  ...

NEXT SUGGESTED
  → Tape : `produce-copy-brief sur {brand} ANG-XX` (générer brief sur angle non-couvert)
  → Tape : `audit briefs > 30j sans test` (briefs stale à promote ou archiver)
```

Format ligne : `[brief_id] · {created_at} · {angle_id_source} · {audience_slug} · {status}`. Cap 10 plus récents. Cross-ref atlas via lien `angle_id_source` (drillable).

---

## Mode tests-drill

`/phantom {brand} tests` rend la DB Tests live + résultats observés + verdict `winner_proxy`.

Lecture : `brands/{brand}/learnings.json#entries[]` filtré sur `kind: test_result`.

Header breadcrumb :

```
workspace > {brand} > tests
══════════════════════════════════════════════
{N} tests · {N_live} live · {N_fatigued} fatigués · {N_winners} winners

TESTS RÉCENTS
  [TST-08] · live · BRF-03 · ANG-01 · ROAS 3.2 · spend 412€ · winner_proxy: pending
  [TST-07] · fatigued · BRF-02 · ANG-02 · ROAS 1.4 (-38% 14j) · winner_proxy: no
  [TST-06] · winner · BRF-01 · ANG-04 · ROAS 4.7 · scaled · winner_proxy: yes
  ...

NEXT SUGGESTED
  → Tape : `refresh les angles fatigués sur {brand}` ({N} tests en chute)
  → Tape : `promote winner TST-06 → angle scaled` (test confirmé, mettre à canon brand)
```

Format ligne : `[test_id] · {status} · {brief_id} · {angle_id} · ROAS {value} · {spend} · winner_proxy: {yes|no|pending}`. Cap 10 plus récents.

---

## Mode matrix-drill

`/phantom {brand} matrix` rend la priorisation des territoires (sous-groupes × source d'angle + top territoires + trous).

Lecture (backend, paths agent) : `brands/{brand}/matrix/latest.json` (output `weight-dimensions` + `score-matrix`).

Header breadcrumb :

```
workspace > {brand} > priorisation
══════════════════════════════════════════════
Facteurs d'ajustement : stade {growth} · marché {mature} · historique {partiel}
Coefficient cumulé : {1.1}

┌───────────────────────────┬──────┬──────┬──────┬──────┬──────┐
│ Sous-groupe audience      │ aud  │ prod │ cat  │ brand│ temp │
├───────────────────────────┼──────┼──────┼──────┼──────┼──────┤
│ chute-post-grossesse      │ 55🔥 │ 42   │ 38   │ 0    │ 28   │
│ croissance-projet         │ 48   │ 52🔥 │ 0    │ 35   │ 0    │
│ stress-hormonal           │ 32   │ 28   │ 41🔥 │ 0    │ 22   │
└───────────────────────────┴──────┴──────┴──────┴──────┴──────┘

TOP 3 TERRITOIRES
  1. chute-post-grossesse × angle audience       · 55  · ANG-01, ANG-03
  2. croissance-projet × angle produit           · 52  · ANG-04
  3. stress-hormonal × angle catégorie           · 41  · ANG-02

TROUS DÉTECTÉS
  · angle brand sur chute-post-grossesse (0)
  · angle catégorie sur croissance-projet (0)
  · angle moment sur croissance-projet (0)

NEXT SUGGESTED
  → Tape : `génère un brief copy sur le top-1` (chute-post-grossesse × angle audience, score 55)
  → Tape : `crée des angles publicitaires {brand} pour combler le trou angle brand sur chute-post-grossesse`
```

Icône `🔥` sur la cellule top par row. Légende colonnes (sources d'angle) : aud (depuis l'audience), prod (depuis le produit), cat (depuis la catégorie), brand (depuis la brand), temp (depuis un moment / saison).

---

## Mode atlas-overview

`/phantom {brand} atlas` rend la vue d'ensemble brand (synthèse 6 entités core + 3 dérivées + historique brand). Pédagogique pour onboarding nouveau opérateur.

Lecture (backend, paths agent) : `brands/{brand}/_snapshot.md` + `brand.json` + counts par entité.

Header breadcrumb :

```
workspace > {brand} > atlas
══════════════════════════════════════════════
MATIÈRE BRAND {BRAND_NAME} · vue d'ensemble

MATIÈRE BRAND (6)
  brand           ✓ identité posée · territoire créatif défini · niveau de notoriété {faible|moyen|fort}
  produits ({N}) {product_slug_1} · {product_slug_2}
  audiences ({N}) {audience_slug_1} · {audience_slug_2} · ... · {audience_slug_N}
  offres          {N} offres configurées
  apprentissages  {N} entrées · {N_canon} promues en référence
  stratégie       focus {month_year} : {strategy.current_focus}

PRODUCTIONS DÉRIVÉES (3)
  angles produits          {N}
  visuels produits         {N}
  priorisation territoires dernière exécution : {date}

HISTORIQUE BRAND (ce qui a marché)
  Accroches validées        {N}
  Structures testées        {N}
  Styles validés            {N}
  Angles validés            {N}
  Formats validés           {N}

NEXT SUGGESTED
  → Tape : `/phantom {brand} matrix` (priorisation des territoires)
  → Tape : `/phantom doctrine` (méthode du système)
```

Cross-ref backend (instructions agent) : `docs/system/atlas-brand.md`. Slug brand en majuscules dans header. Ne pas exposer ce path à l'opérateur.

### Mode atlas-overview · empty state (brand fresh)

Si `brands/{brand}/_snapshot.md` indique tout à 0 (pas d'audiences cartographiées, pas de produits, pas d'angles), le mode atlas bascule sur empty state distinct au lieu de la vue 0/0/0/0 décourageante.

Format empty state :

```
workspace > {brand}
══════════════════════════════════════════════
On démarre {BRAND_NAME}.

Tu veux commencer par où ?

  (a) Importer la matière qui existe (URL produit, brief PDF, deck founder)
  (b) Mining audience initial (qui sont tes clients, qu'est-ce qu'ils disent)
  (c) Cartographier ton offre (produits, mécanismes, bénéfices)
  (d) Dis-moi ton point de départ, je m'adapte
```

Pas de "MATIÈRE ACTUELLE 0/0/0/0/0". Pas de "SIGNAL FORT" inventé. Posture propose action concrète.

**Trigger detection** : `audiences count = 0 AND products count = 0 AND angles count = 0` → empty state. Sinon vue normale (même si brand partial · audiences ok mais 0 angles reste vue normale degraded).

---

## Mode doctrine

`/phantom doctrine` rend la méthode du système (cartographie + composition). Equivalent Notion "Méthode & Doctrine". Vue pédago, workspace-level (transversal aux brands).

Lecture (backend, paths agent) : `docs/system/atlas-brand.md` + `resources/templates/creative-formula.md`.

Header breadcrumb :

```
workspace > doctrine
══════════════════════════════════════════════
MÉTHODE DU SYSTÈME · cartographier + composer

Vue d'ensemble · arbres de connaissance + priorisation + facteurs d'ajustement + boucle d'apprentissage

PARCOURS EN 6 ÉTAPES
  Étape 1 démarrage          démarre une nouvelle brand · cartographie initiale · pose les specs
  Étape 2 produit            mécanismes · bénéfices · problèmes résolus
  Étape 3a audience          récupère témoignages clients · cartographie audience (8 dimensions)
  Étape 3b angle             crée des angles publicitaires (Observation + Tension + Reframe + Bridge)
  Étape 4 priorisation       calcule les priorités d'audience · priorise les territoires
  Étape 5 brief              génère un brief copy
  Étape 6 visuel             crée un visuel · adapte un visuel existant · décompose une pub existante

RECETTE CRÉATIVE
  créa = NOYAU (mécanique × format × stop scroll × ton)
       × CONTEXTE (angle × douleur × persona × preuve)
       × MODIFICATEURS (occasion · offre · destination · etc.)

7 PILIERS DU SYSTÈME
  Le système repose sur 7 piliers internes (encodage rigoureux, production qualité,
  création de skills, traçabilité, cartographie compositionnelle, gouvernance, intelligence contextuelle).
  Tu en sens les effets, tu n'as jamais à les nommer.

BOUCLE D'APPRENTISSAGE (historique brand vivant)
  produire → tester → capturer ce qu'on a appris → tests passés cumulés sur la bibliothèque

NEXT SUGGESTED
  → Tape : `/phantom canon` (bibliothèque métier · 11 chapitres copy)
  → Tape : `/phantom {brand} atlas` (vue brand-side de la méthode appliquée)
```

Détails complets (backend) : `resources/templates/creative-formula.md`. Source méthode (backend) : `docs/system/atlas-brand.md`.

---

## Mode doctrine audiences

> **Split externe** : full spec rendering du framework cartographie audiences (4 questions Q1-Q4 + pièges + Pareto) → `.claude/commands/phantom-modes/doctrine-audiences.md`. Lire ce fichier quand l'opérateur tape `/phantom doctrine audiences`.

Bref : framework pédagogique 4 questions (porte d'entrée, granularité, Schwartz, chevauchements). Operator-facing, workspace-level. Cross-ref · `docs/doctrine/audience-cartography-framework.md`.

---

## Mode audiences-tree

> **Split externe** : full spec rendering de l'arbre audiences brand-side (hiérarchie + chevauchements + gaps détectés + dégradation gracieuse) → `.claude/commands/phantom-modes/audiences-tree.md`. Lire ce fichier quand l'opérateur tape `/phantom {brand} audiences`.

Bref : iterate `brands/{brand}/audiences/*/profile.json`, extract `meta.scope` + `meta.parent_slug` + `meta.overlap_with`, render arbre indenté par porte d'entrée + ligne chevauchements + bloc gaps. Override le mode entity-drill générique pour l'entité `audiences`. Le drill per-audience reste mode item via `/phantom {brand} audiences {slug}`.

---

## Mode mechanisms-drill

`/phantom {brand} products {p_slug} mechanisms` rend l'array `mechanisms[]` typé depuis `spec.json`.

Lecture : `brands/{brand}/products/{p_slug}/spec.json#mechanisms[]`.

Header breadcrumb :

```
workspace > {brand} > products > {p_slug} > mechanisms
══════════════════════════════════════════════
{N} mécanismes typés

MEC-01 modulation cortisol stress
  cible           SN central, surrenales
  mode action     adaptogène
  fenêtre         21-30j
  preuve          clinique citée
  sophistication  faible
  triggered_by    KSM-66

MEC-02 ...

NEXT SUGGESTED
  → Tape : `map-mechanisms {brand}/{p_slug}` (deep pass enrichissement mécanismes)
  → Tape : `densifie spec {p_slug}` (champs manquants si présents)
```

Format par mécanisme : id + nom court, puis 6 champs (cible, mode action, fenêtre, preuve, sophistication, triggered_by). Si `mechanisms[]` vide : empty state *"Pas de mécanisme encodé. Tape `map-mechanisms {brand}/{p_slug}` pour scaffold depuis la fiche produit."*

---

## Mode benefits-drill

`/phantom {brand} products {p_slug} benefits` rend l'array `benefits[]` (chain functional → emotional → identity).

Lecture : `brands/{brand}/products/{p_slug}/spec.json#benefits[]`.

Header breadcrumb :

```
workspace > {brand} > products > {p_slug} > benefits
══════════════════════════════════════════════
{N} bénéfices encodés (chain functional/emotional/identity)

BEN-01 cheveux denses visibles
  layer         functional
  trigger       MEC-01
  fenêtre       60-90j
  preuve        photo before/after
  audience_fit  chute-active, chute-post-grossesse

BEN-02 confiance retrouvée
  layer         emotional
  trigger       BEN-01
  ...

BEN-03 identité jeune mère épanouie
  layer         identity
  trigger       BEN-02
  ...

NEXT SUGGESTED
  → Tape : `map-benefits {brand}/{p_slug}` (deep pass enrichissement chain)
  → Tape : `audit benefits sans audience_fit` (benefits orphelins)
```

Format par benefit : id + nom court, puis 5 champs (layer, trigger, fenêtre, preuve, audience_fit). Layer = `functional|emotional|identity`. Si `benefits[]` vide : empty state similaire à mechanisms.

---

## Empty states pédagogiques

Quand un rendering rencontre du vide, ne rends pas du vide · propose le next move concret. Toujours.

| Situation | Empty state output |
|---|---|
| Workspace mode, 0 brand | (déjà couvert par mode bootstrap) |
| Brand mode, 0 produit | *"Pas encore de produit encodé sur `{brand}`. Tape `snapshot {brand} avec {url}` pour scaffold le hero produit."* |
| Brand mode, 0 audience | *"Pas encore d'audience sur `{brand}`. Snapshot va proposer une cartographie. Sinon : `lance mine-voc sur {brand}` pour partir du verbatim client."* |
| Entity-drill audiences, 0 audience | *"Pas d'audience encodée. Tape `/phantom {brand}` puis snapshot le hero pour scaffold les groupes principaux."* |
| Entity-drill angles, 0 angle | *"Pas d'angle produit. Tape `crée des angles publicitaires {brand}` après récupération des témoignages pour générer un set priorisé."* |
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
