---
name: phantom
description: Cockpit PhantomOS. Sans arg, vue workspace (tous brands + état global). Avec un brand slug, vue détaillée du brand. Read-only.
---

# /phantom, cockpit

Vue synthétique du workspace PhantomOS. Lecture seule, aucune mutation. Read top to bottom before acting.

## Mode detection

Check the user's argument :

| Argument | Mode |
|---|---|
| empty (just `/phantom`), 0 brand encodé | **bootstrap** : message "tape /tour pour démarrer" |
| empty, 1 brand encodé | **brand** : cockpit du seul brand existant |
| empty, N brands encodés | **workspace** : vue multi-brand globale |
| `workspace` ou `all` | **workspace** : forcé en vue globale même si N=1 |
| brand slug (e.g. `/phantom onday`) | **brand** : cockpit détaillé du brand |

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
🟢 onday              L2     1P / 5A / 8An / 3T    last 14h
🟡 stepprs            L1     1P / 2A / 0An         last 6d
⚪ karacare           L2     1P / 4A / 5An         last 47d
```

### Cross-brand metrics

- **Total tests actifs** : somme des `tests actifs` de chaque brand (entries learnings.json type=test-result, status absent ou inconclusive ou fatigued).
- **Connected sources globales** : si `connected-sources.json` racine existe (sources cross-brand comme un Meta Business Manager partagé), lister les plateformes avec last_sync agrégé. Sinon dire "(per-brand only)".

### Next suggested workspace-level

3 propositions max, ordonnées par priorité. Sources :
- Brand dormant > 60j → suggérer "archiver ou réactiver".
- Tests fatiguing dans plusieurs brands → suggérer batch refresh.
- Operator profile incomplet → suggérer densification.
- Skill `audit-meta-account` (ou équivalent) jamais run sur un brand actif → suggérer un audit.
- Niveau de contexte global moyen sub-L2 → suggérer densification d'un brand prioritaire.

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

3 propositions max, ordonnées par priorité décisionnelle. Sources :
- Tests fatiguing → suggérer refresh angle ou nouveau test.
- Audiences avec sourcing incomplet → suggérer mine-audience ou source manuel.
- Stale > 14j sur entité critique → suggérer update.
- Niveau de contexte sub-L2 → suggérer enrichissement vers L2.
- Connected source non configurée mais pertinente → suggérer connection.

Format :
```
→ {action concrète}
→ {action concrète}
→ {action concrète}
```

Actions doivent toujours nommer un skill ou un objet précis. Pas de conseil générique.

---

## Constraints (tous modes)

- **Read-only.** Aucune mutation. Si l'opérateur demande ensuite de fix quelque chose, propose le skill approprié, ne fais pas la mutation toi-même.
- **One screen output.** Workspace mode : 30 lignes max. Brand mode : 40-50 lignes max.
- **Pas de jargon doctrine.** Pas de "SED", "CMR", "_field_types", "validation_status" en surface. Traduit en mots métier (validé / hypothèse / fatigué).
- **Honest staleness.** Si une entité n'a pas été touchée depuis 90j, dis-le. Si snapshot date > 1h, regenère silencieusement avant d'afficher.
- **Mode brand explicite gagne sur l'auto-détection.** `/phantom onday` force brand mode même si workspace a 1 brand.
- **Mode workspace forcé via `workspace` ou `all`.**
