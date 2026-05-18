---
name: version
description: Affiche la version courante du workspace + latest disponible + changelog summary. Pas de mutation, juste display.
version: v2.80.0
---

# /version · état version workspace

Slash command read-only. Affiche la version locale du workspace, la latest disponible sur le remote canon, le delta entre les deux et un résumé des derniers changelogs. Aucune mutation, aucun rsync, aucun backup. Juste display.

Pair canon avec `/update` · `/version` informe · `/update` agit.

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

Compter le nombre de releases intermédiaires entre `LOCAL_VERSION` et `LATEST_TAG`. Classifier le type dominant (additive · schema-bump · breaking · refactor) depuis les manifests si dispo.

### Step 4 · Read changelog

Lire les 3 dernières entrées de `CHANGELOG.md` (ou `docs/system/updates.md` selon convention canon courante).

### Step 5 · Render output canon

Iconographie ✓ ◐ ○ ✗ ⚠ + headers FR sobres + séparateurs ━━━ / ───.

## Format output canon

```
PhantomOS · état version
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Version locale       v2.79.4 (released 2026-05-17)
  Latest disponible    v2.80.0 (released 2026-05-18)
  Delta                1 step (additive · NEW slash commands)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Changelog summary
  ────────────────────────────────────────────────────────────────
  v2.80.0 · NEW pipeline update + migrations canon
           · /update + /version slash commands
           · doctrine update-distribution-discipline
           · framework migrations versionnées

  v2.79.5 · intelligence compositionnelle pré-exécution
           · NIVEAU 0 paramètres décomposés

  v2.79.4 · hygiène BUILD + split onboarding /tour + /about

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Pour mettre à jour · /update
  Historique complet · /version --history

  ✓ done · ◐ partiel · ○ todo · ✗ failed · ⚠ attention
```

## Format up-to-date (delta zéro)

Quand `LOCAL_VERSION == LATEST_TAG` ·

```
PhantomOS · état version
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Version locale       v2.80.0 (released 2026-05-18)
  Latest disponible    v2.80.0
  Delta                ✓ à jour

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Changelog summary
  ────────────────────────────────────────────────────────────────
  v2.80.0 · NEW pipeline update + migrations canon
           · /update + /version slash commands
           · doctrine update-distribution-discipline

  v2.79.5 · intelligence compositionnelle pré-exécution
  v2.79.4 · hygiène BUILD + split onboarding

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Historique complet · /version --history
```

## Format --history

Liste toutes les entrées CHANGELOG.md avec date + résumé 1 ligne. Format ·

```
PhantomOS · historique versions
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  v2.80.0  2026-05-18  NEW pipeline update + migrations canon
  v2.79.5  2026-05-18  intelligence compositionnelle pré-exécution
  v2.79.4  2026-05-17  hygiène BUILD + split onboarding /tour + /about
  v2.79.3  2026-05-17  ...
  ...
  v2.0.0   YYYY-MM-DD  ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Détail version · cat docs/system/updates.md
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

## Hard Rules runtime

- HR · JAMAIS de mutation (read-only strict)
- HR · TOUJOURS afficher delta explicite (steps + type dominant)
- HR · TOUJOURS proposer `/update` en pied si delta > 0
- HR · TOUJOURS fallback gracieux si fetch latest échoue (offline · rate-limit)
- HR · Iconographie canon v2.79.2 unique

## Cross-refs canon

- `/update` · pair canon · pipeline mutation
- `docs/system/update-distribution-discipline.md` v2.80.0 · doctrine racine
- `docs/system/updates.md` · changelog source de vérité
- `_version.json` · version locale source
