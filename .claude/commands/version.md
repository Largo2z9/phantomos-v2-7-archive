---
name: version
description: Affiche la version courante du workspace + latest disponible + changelog summary. Pas de mutation, juste display.
version: v2.83.0
---

# /version · état version workspace

Slash command read-only. Affiche la version locale du workspace, la latest disponible sur le remote canon, le delta entre les deux et un résumé des derniers changelogs Keep-a-Changelog. Aucune mutation, aucun rsync, aucun backup. Juste display.

Pair canon avec `/update` · `/version` informe · `/update` agit.

## Sources de vérité (canon v2.83.0+)

| Source | Rôle | Quand lire |
|---|---|---|
| `_version.json` | version locale | toujours · Step 1 |
| `CHANGELOG.md` (Keep-a-Changelog) | résumé exécutif top 3 entries · sections Added/Changed/Removed/Fixed/Migration/Breaking | toujours · Step 4 |
| `docs/internal/releases/manifest/{version}-manifest.json` | détails structurés étendus par release | si opérateur veut deep dive · cross-ref pied |
| `docs/internal/project-journal.md` | narrative archive v2.83.0+ | si opérateur curieux mentionne contexte historique |

## Mode detection

| Argument | Routing |
|---|---|
| `/version` empty | current + latest + delta + changelog top 3 entries |
| `/version --history` | liste full versions historiques (toutes entrées CHANGELOG.md) |
| `/version --json` | output structuré JSON (pour intégration outils externes · rare) |

## Workflow

### Step 1 · Read version locale

```bash
LOCAL_VERSION=$(python3 -c "import json; print(json.load(open('_version.json'))['template_version'])")
LOCAL_RELEASED=$(python3 -c "import json; print(json.load(open('_version.json'))['released_at'])")
```

### Step 2 · Fetch latest

```bash
LATEST_TAG=$(gh api repos/Largo2z9/phantomos/releases/latest --jq '.tag_name' 2>/dev/null || echo "")
LATEST_DATE=$(gh api repos/Largo2z9/phantomos/releases/latest --jq '.published_at' 2>/dev/null | cut -d'T' -f1 || echo "")
```

Si fetch échoue (offline · rate-limit) · afficher `latest disponible · unknown (offline)` et continuer.

### Step 3 · Compute delta

Compter le nombre de releases intermédiaires entre `LOCAL_VERSION` et `LATEST_TAG`. Classifier le type dominant depuis les manifests JSON `docs/internal/releases/manifest/{version}-manifest.json` (champ `type` · additive · schema-bump · breaking · refactor). Manifest absent → fallback inférence depuis sections CHANGELOG (présence `### Breaking` ou `### Migration` → flag).

### Step 4 · Read changelog (Keep-a-Changelog parse)

Lire les 3 dernières entrées de `CHANGELOG.md`. Format canon strict ·

```
## [VERSION] · YYYY-MM-DD
### Added
- entry
### Changed
- entry
### Removed
- entry
### Fixed
- entry
### Migration
- entry
### Breaking
- entry
```

**Parse strict** ·
- Header release · `^## \[(\d+\.\d+\.\d+)\] · (\d{4}-\d{2}-\d{2})` → capture version + date
- Section header · `^### (Added|Changed|Removed|Fixed|Migration|Breaking|Notes)` → catégorie
- Bullet · `^- (.+)` → entry texte

Pour affichage opérateur (top 3 entries) · prendre top 3-5 bullets par version cumulés sections Added + Changed + Migration + Breaking en priorité (Removed + Fixed + Notes secondaire). Trim à 3-5 lignes total par version max.

### Step 5 · Render output canon

Iconographie ✓ ◐ ○ ✗ ⚠ + headers FR sobres + séparateurs ━━━ / ───. Sections Keep-a-Changelog affichées avec préfixe court · `+` Added · `~` Changed · `-` Removed · `✓` Fixed · `→` Migration · `⚠` Breaking.

## Format output canon

```
PhantomOS · état version
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Version locale       v2.82.1 (released 2026-05-19)
  Latest disponible    v2.83.0 (released 2026-05-19)
  Delta                1 step (additive · canon split CHANGELOG)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Changelog summary
  ────────────────────────────────────────────────────────────────
  v2.83.0 · 2026-05-19
           + NEW doctrine changelog-discipline (split canon)
           ~ CHANGELOG.md refactor Keep-a-Changelog (4270L → 90L)
           + NEW docs/internal/project-journal.md (narrative archive)

  v2.82.1 · 2026-05-19
           + Mapping diff v2.81.1 → v2.82.0
           + Runtime validation static canon 5 scenarios

  v2.82.0 · 2026-05-19
           ~ CLAUDE.md root refactor atomique 332L → 144L
           + NEW doctrine claude-md-discipline

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Pour mettre à jour · /update
  Détails étendus · docs/internal/releases/manifest/v2.83.0-manifest.json
  Historique complet · /version --history

  ✓ done · ◐ partiel · ○ todo · ✗ failed · ⚠ attention
```

## Format up-to-date (delta zéro)

Quand `LOCAL_VERSION == LATEST_TAG` ·

```
PhantomOS · état version
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Version locale       v2.83.0 (released 2026-05-19)
  Latest disponible    v2.83.0
  Delta                ✓ à jour

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Changelog summary
  ────────────────────────────────────────────────────────────────
  v2.83.0 · 2026-05-19
           + NEW doctrine changelog-discipline
           ~ CHANGELOG.md refactor Keep-a-Changelog
           + NEW project-journal archive

  v2.82.1 · 2026-05-19  Mapping diff + runtime validation
  v2.82.0 · 2026-05-19  CLAUDE.md root refactor atomique

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Détails étendus · docs/internal/releases/manifest/v2.83.0-manifest.json
  Historique complet · /version --history
```

## Format --history

Liste toutes les entrées CHANGELOG.md avec date + résumé 1 ligne (top bullet section Added ou Changed). Format ·

```
PhantomOS · historique versions
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  v2.83.0  2026-05-19  NEW doctrine changelog-discipline (split canon)
  v2.82.1  2026-05-19  Mapping diff v2.81.1 → v2.82.0
  v2.82.0  2026-05-19  CLAUDE.md root refactor atomique 332L → 144L
  v2.81.1  2026-05-19  NIVEAU LIVE thinking aloud canon
  v2.81.0  2026-05-18  NEW doctrine entry-arc-discipline
  ...
  v2.0.0   YYYY-MM-DD  ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Détail version · docs/internal/releases/manifest/v{X.Y.Z}-manifest.json
  Narrative archive · docs/internal/project-journal.md
  Mise à jour · /update
```

## Iconographie canon v2.79.2

| Icône | Sens |
|---|---|
| ✓ | done · validé · OK · à jour |
| ◐ | partiel · en cours · partial state |
| ○ | todo · pas encore fait |
| ✗ | failed · erreur · blocage |
| ⚠ | attention · warning · delta significatif |

## Préfixes Keep-a-Changelog canon

| Préfixe | Section CHANGELOG | Sens |
|---|---|---|
| `+` | Added | nouvelle feature · ajout canon |
| `~` | Changed | refactor · update existant |
| `-` | Removed | suppression · deprecate |
| `✓` | Fixed | bugfix · correction |
| `→` | Migration | migration auto v{X} → v{Y} |
| `⚠` | Breaking | breaking change · attention requise |

## Hard Rules runtime

- HR · JAMAIS de mutation (read-only strict)
- HR · TOUJOURS afficher delta explicite (steps + type dominant depuis manifest JSON)
- HR · TOUJOURS proposer `/update` en pied si delta > 0
- HR · TOUJOURS fallback gracieux si fetch latest échoue (offline · rate-limit)
- HR · TOUJOURS cross-ref manifest JSON en pied output si version cible existe
- HR · Iconographie canon v2.79.2 unique
- HR · Parse Keep-a-Changelog strict (regex header + section, pas de fuzzy match)

## Cross-refs canon

- `/update` · pair canon · pipeline mutation
- `docs/system/update-distribution-doctrine.md` v2.80.0 · doctrine racine pipeline update
- `docs/system/changelog-doctrine.md` v2.83.0 · doctrine split canon CHANGELOG vs project-journal vs manifests
- `CHANGELOG.md` · résumé exécutif Keep-a-Changelog (runtime consumable)
- `docs/internal/releases/manifest/{version}-manifest.json` · détails structurés par release (source de vérité deep dive)
- `docs/internal/project-journal.md` · narrative archive v2.83.0+ (contexte historique étendu)
- `_version.json` · version locale source
