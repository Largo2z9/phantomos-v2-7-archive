---
name: update
description: Mise à jour du workspace PhantomOS vers la dernière version canon. Preserve tes brands + operator state. Migrations automatiques pour BREAKING changes. Backup + rollback canon.
version: v2.80.0
---

# /update · mise à jour workspace canon

Slash command pointer vers le pipeline d'update PhantomOS. Synchronise les fichiers canon (skills · doctrines · commands · templates) depuis `Largo2z9/phantomos` vers ton workspace local, sans toucher à tes brands, ton operator state ou ta config.

## Mode detection

| Argument | Routing |
|---|---|
| `/update` empty | check version locale vs latest · propose update si delta · disclosure pré-update NIVEAU 0 |
| `/update --check` | just check, no apply · affiche version locale + latest + delta + plan théorique |
| `/update --force` | re-apply current version (cas debug rare · workspace désynchronisé) |
| `/update --rollback {version}` | revert vers backup `_archive/migrations/pre-{version}-{date}/` |

## Workflow canon

### Step 1 · Detect versions

Lire version locale + fetch latest tag depuis remote canon.

```bash
LOCAL_VERSION=$(python3 -c "import json; print(json.load(open('_version.json'))['template_version'])")
LATEST_TAG=$(gh api repos/Largo2z9/phantomos/releases/latest --jq '.tag_name' 2>/dev/null || echo "")
```

Si `gh` indisponible · fallback `git ls-remote --tags https://github.com/Largo2z9/phantomos.git | tail -1`.

### Step 2 · Construire plan migration

Si `latest > local` · lister tous les manifests intermédiaires depuis `docs/internal/releases/manifest/`.

Pour chaque step · capturer le type (additive · schema-bump · breaking · refactor) depuis le manifest.

```
Versions à apply ·
v2.79.5 → v2.80.0
- additive (NEW slash commands /update + /version + doctrine update-distribution)
- additive (NEW migrations framework)
```

### Step 3 · Disclosure pré-update canon (EDD v2.79.5 + NIVEAU 0)

Avant tout backup ou rsync · poser les paramètres décomposés. Format canon ·

```
/update · mise à jour workspace
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Paramètres posés
  ────────────────────────────────────────────────────────────────
  Version locale       v2.79.4
  Version latest       v2.80.0
  Migrations           1 step (v2.79.4 → v2.80.0 · additive)
  Type changement      Additive · zéro impact data
  Brands préservées    1 (mykara-care)
  Operator state       préservé (awareness · session-state · todos)
  Backup destination   _archive/migrations/pre-v2.80.0-2026-05-18/

  Plan
  ────────────────────────────────────────────────────────────────
  1. Backup brands/ + operator/ + .phantom/ vers _archive/migrations/
  2. Rsync canon workspace-template (exclude operator state)
  3. Apply migration scripts si BREAKING (additive ici · skip)
  4. Validate state post-update
  5. Confirm + cleanup temp

  ETA           ~30-60 secondes (additive · pas de transform)
  Implication   Tes brands + operator state préservés strict
  Livrable      Workspace v2.80.0 · brands intacts · backup dispo

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  OK pour update ? ou tu rollback un autre jour ?
```

Attendre confirmation explicite avant de continuer (sauf `--force` qui short-circuite).

### Step 4 · Backup operator state

Rsync sélectif vers `_archive/migrations/pre-v{X.Y.Z}-{date}/` · ne backup QUE ce qui appartient à l'opérateur.

```bash
BACKUP_DIR="_archive/migrations/pre-${LATEST_TAG#v}-$(date +%Y-%m-%d)"
mkdir -p "$BACKUP_DIR"
rsync -a \
  --include='brands/***' \
  --include='operator/***' \
  --include='.phantom/***' \
  --include='.workflow.json' \
  --include='credentials*.env' \
  --include='todos.md' \
  --exclude='*' \
  ./ "$BACKUP_DIR/"
```

Confirmer taille backup + chemin avant rsync canon.

### Step 5 · Apply update (rsync canon depuis remote)

Cloner remote canon en `/tmp` · checkout tag latest · rsync vers workspace en excluant strict tout l'operator state.

```bash
TMP_DIR="/tmp/phantomos-update-$$"
git clone https://github.com/Largo2z9/phantomos.git "$TMP_DIR"
cd "$TMP_DIR"
git checkout "$LATEST_TAG"
cd -
rsync -a --delete \
  --exclude='.git' \
  --exclude='.DS_Store' \
  --exclude='credentials_shared.env' \
  --exclude='credentials.env' \
  --exclude='brands/' \
  --exclude='operator/' \
  --exclude='.phantom/' \
  --exclude='.workflow.json' \
  --exclude='_archive/' \
  "$TMP_DIR/" ./
rm -rf "$TMP_DIR"
```

Les exclusions sont strictes · zéro fichier opérateur ne doit être écrasé. Si un fichier est ambigu (canon ET opérateur · ex `todos.md` racine) · privilégier la version opérateur.

### Step 6 · Apply migrations si BREAKING

Pour chaque step intermédiaire `> LOCAL_VERSION && <= LATEST_TAG` · si manifest indique `type: schema-bump` ou `breaking` · run le script de migration correspondant.

```bash
for MIGRATION in $(ls migrations/*.py 2>/dev/null | sort); do
  MIG_VERSION=$(basename "$MIGRATION" .py | cut -d- -f1)
  if [[ "$MIG_VERSION" > "$LOCAL_VERSION" && "$MIG_VERSION" <= "${LATEST_TAG#v}" ]]; then
    python3 "$MIGRATION" --apply
  fi
done
```

Sur additive · skip (rien à transformer). Sur schema-bump · déléguer à skill `migrate-workspace` pour chaque brand.

### Step 7 · Validate state post-update

Run `validate-resources` canon · vérifier intégrité brands + operator state + cohérence `_version.json`.

```bash
python3 .skills/skills/validate-resources/validate.py --all 2>&1 | tail -20
```

Si validation échoue · proposer rollback automatique vers backup créé Step 4.

### Step 8 · Confirm output canon

Format final ·

```
✓ Workspace updated v2.79.4 → v2.80.0
✓ Brands préservées (1) · operator state préservé
✓ Backup disponible · _archive/migrations/pre-v2.80.0-2026-05-18/
✓ Rollback path · /update --rollback v2.79.4

Changelog summary v2.80.0 ·
· NEW /update slash command (toi maintenant)
· NEW /version slash command
· NEW doctrine update-distribution-discipline
· NEW migrations framework

Légende ·
✓ done · ◐ partiel · ○ todo · ✗ failed · ⚠ attention
```

## Mode --rollback

`/update --rollback {version}` revert canon ·

1. Detect backup dans `_archive/migrations/pre-{version}-*/`
2. Disclosure pré-rollback (paramètres · plan · implications)
3. Rsync inverse backup → workspace
4. Update `_version.json` vers version cible
5. Confirm + suggest validation

## Iconographie canon v2.79.2

| Icône | Sens |
|---|---|
| ✓ | done · validé · OK |
| ◐ | partiel · en cours · partial state |
| ○ | todo · pas encore fait |
| ✗ | failed · erreur · blocage |
| ⚠ | attention · warning · friction |

Légende systématique au pied de tout output structuré.

## Hard Rules runtime

- HR · TOUJOURS backup avant apply (Step 4 non-négociable)
- HR · TOUJOURS preserve operator state (rsync exclude strict · `brands/` · `operator/` · `.phantom/` · `.workflow.json` · `credentials*.env`)
- HR · TOUJOURS valider post-update (Step 7 non-négociable)
- HR · TOUJOURS proposer rollback path dans output final
- HR · TOUJOURS disclosure pré-update NIVEAU 0 (cohérent EDD v2.79.5) avant tout rsync
- HR · TOUJOURS attendre confirmation explicite (sauf `--force` ou `--check`)
- HR · JAMAIS écraser un fichier opérateur ambigu sans demander
- HR · JAMAIS commit auto post-update · l'opérateur décide

## Cross-refs canon

- `docs/system/update-distribution-discipline.md` v2.80.0 · doctrine racine update pipeline
- `docs/system/engagement-disclosure-discipline.md` v2.79.5 · disclosure pattern NIVEAU 0
- `.skills/skills/update-workspace/SKILL.md` · skill orchestrator sous-jacent
- `.skills/skills/migrate-workspace/SKILL.md` · skill schema migration brand-by-brand
- `/version` · pair canon · affiche état version sans muter
- `docs/system/updates.md` · changelog complet historique
