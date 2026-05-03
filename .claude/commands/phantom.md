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
