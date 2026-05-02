# Publishing Updates — Maintainer Doctrine

How to ship a clean PhantomOS update that testers can install without breaking their data.

---

## Core principle

**The maintainer declares clearly. The receiver's agent executes mechanically.** Ambiguity in the declaration = broken workspaces downstream. Every release ships with a machine-readable manifest that spells out each change by type.

---

## Template vs operator data

| Owned by maintainer (template) | Owned by operator (data) |
|---|---|
| `CLAUDE.md` | `brands/{slug}/` (user brands) |
| `docs/` | `operator/` |
| `.skills/skills/` (core + template) | `credentials.env` / `credentials_shared.env` |
| `resources/` | `brands/{slug}/learnings.json` |
| `brands/_TEMPLATE/` | `brands/{slug}/todos.md` |
| `brands/_EXAMPLE/` | `brands/{slug}/custom/` (user extensions) |
| `scripts`, `infra/` | `.skills/skills/custom/` (user skills) |
| `_version.json` | `/operator/installation.json → history[]` |

Template files: updates can freely overwrite (post-confirm for breaking). Operator data: **never** touched by an update.

---

## Change types

Every entry in `docs/releases/{version}-manifest.json → changes[]` declares one of:

### `doc-change` / `doc-added`

A markdown, JSON, or YAML template file. Safe overlay. Receiver agent overwrites or creates.

```json
{
  "type": "doc-change",
  "file": "CLAUDE.md",
  "action": "overwrite",
  "safe": true,
  "note": "Added disambiguation tie-breaker rule in Skills section."
}
```

### `infra-change` / `infra-added`

A Python script, Makefile, or build artifact. Often followed by a `post_step` that regenerates a derived file.

```json
{
  "type": "infra-added",
  "file": ".skills/build-brand-snapshot.py",
  "action": "create",
  "post_step": "python3 .skills/build-brand-snapshot.py --all",
  "safe": true
}
```

### `skill-added`

A new skill folder under `.skills/skills/{name}/`. Receiver copies. Manifest regenerates.

### `skill-renamed`

Folder rename + frontmatter `name:` update. Optionally keeps aliases so existing references still resolve.

```json
{
  "type": "skill-renamed",
  "from": "old-name",
  "to": "new-name",
  "aliases_to_keep": ["old-name"],
  "safe": true
}
```

### `skill-removed`

A skill is deprecated. Receiver moves to `.skills/skills/_archive/`, flags the operator with the alternative.

```json
{
  "type": "skill-removed",
  "skill": "deprecated-skill",
  "alternative": "new-skill-name",
  "safe": true
}
```

### `schema-bump`

A JSON schema version bumps (e.g. `brand.json` v2.1 → v2.2). **Requires a migration script**. Receiver delegates to `migrate-workspace` which walks affected files, applies the script, writes through the mutation gate. This is the only change type that touches operator data.

```json
{
  "type": "schema-bump",
  "schema": "brand.schema.json",
  "from_schema_version": "2.1",
  "to_schema_version": "2.2",
  "migration_script": "infra/migrations/brand-v2.1-to-v2.2.py",
  "affected_files_glob": "brands/*/brand.json",
  "safe": false,
  "requires_confirmation": true,
  "note": "Renamed identity.sector → identity.vertical. Added identity.maturity_stage."
}
```

### `breaking`

Any change that requires operator action beyond a migration script (e.g. manual data re-entry, scope change, trigger re-learning). The full `note` is surfaced to the operator for explicit confirmation before applying.

---

## Publishing checklist

Every release, in order:

1. **Bump `_version.json`** with the new `template_version`, `released_at`, and a pointer to the manifest.
2. **Write `docs/releases/{version}-manifest.json`** listing every change. One entry per change, typed precisely.
3. **For every `schema-bump`**: write the migration script under `infra/migrations/{schema}-v{from}-to-v{to}.py`. Test it on `_EXAMPLE` before shipping.
4. **Update `CHANGELOG.md`** with the human-readable summary (complements the machine manifest, not a replacement).
5. **Run `python3 .skills/build-manifest.py`** to refresh the skills manifest if any skill changed.
6. **Run the pre-release gate** (see next section) before commit.
7. **Commit and tag** the release.

---

## Pre-release gate

Before bumping `_version.json` and committing a release, every check below **must pass**. If any fails, you're still in Build mode — go fix it, re-check.

### Gate 1 — Template diff-clean
The `workspace-template/` tree has no references to R&D paths (`sandbox/`, `schemas/` as extended schemas, `research/` at the project-R&D level, `data-layer/`, `shared-resources/` when not promoted). Check:

```bash
grep -rE "sandbox/|05-projects/context-engine/(sandbox|schemas|research|data-layer)/" workspace-template/ --include="*.md" --include="*.json"
```

Zero matches expected. Any match = a Build-mode ref leaked into Release. Remove or rephrase before ship.

### Gate 2 — Every change is in the manifest
Run `git diff v{previous}..HEAD -- workspace-template/` and verify every changed file is declared in `docs/releases/{new_version}-manifest.json → changes[]`. Unlisted change = silent behavior change for testers. Either add to manifest with a real `note:` field, or revert.

### Gate 3 — Schema bumps have migration scripts
For every `schema-bump` entry in the manifest, the `migration_script` path must exist and be executable. Smoke-test it on `brands/_EXAMPLE/` locally before ship:

```bash
python3 infra/migrations/{schema}-v{from}-to-v{to}.py brands/_EXAMPLE/
```

Migration script missing or failing = release blocked.

### Gate 4 — Breaking changes explicitly confirmed
If `manifest.breaking == true` or any change has `requires_confirmation: true`, the `notes` field **must** spell out the operator action required. Vague `notes` = testers will either skip the update or brick their workspace.

### Gate 5 — Sync verified
After commit but before tag:

```bash
diff -rq workspace-template/ /Users/{user}/phantomos-alpha-test/
diff -rq workspace-template/ /Users/{user}/phantomos-test-clean/
```

Zero diffs expected. Any diff = the sync step was skipped and testers pulling from the clone repos get stale code.

### Gate 6 — CHANGELOG and _version agree
`CHANGELOG.md` top entry must match `_version.json → template_version` and `docs/releases/` must contain the corresponding `{version}-manifest.json`. Mismatch = one of the three was forgotten.

### Gate 7 — R&D hygiene check (weekly, not per-release)
Run `python3 05-projects/context-engine/hygiene-audit.py`. Parasitic files, top-level orphans, or stale+unreferenced items in the R&D zone won't block the release but should be cleaned before they accumulate.

---

---

## Anti-patterns

- **Ambiguous `note:` fields** — "misc fixes" tells the receiver's agent nothing. Be specific: what file, what behavior changed.
- **Missing migration script on schema-bump** — the receiver cannot infer the transformation. Ship the script or don't bump the schema.
- **Touching operator data in a non-schema-bump change** — every change type except `schema-bump` must be operator-data-safe by definition.
- **Chaining multiple breaking changes in one release** — split into separate versions so the operator can confirm each independently.
- **Renaming a skill without aliases** — existing references (in other skills, docs, awareness) break. Keep at least one release of alias before dropping.

---

## Bonus — auto-generating the manifest

`python3 .skills/build-update-manifest.py {from_version} {to_version}` diffs two git revs of the template and pre-fills the manifest at ~80%. You review and add the schema-bumps and breaking changes manually (the diff cannot infer schema semantics).

---

## Distribution to partners

Once a release is tagged, partners running PhantomOS locally need a way to know an update is available and a one-line command to install it. The maintainer choice for v2.10.x:

**Channel** — partners receive a single Slack DM (or email if no Slack) when a release ships. No mailing list, no auto-pull, no broadcast. The maintainer pings each partner directly. Manual but predictable.

**Notification template (maintainer side):**

> *PhantomOS v{X.Y.Z} dispo. Theme : {theme courte}.*
> *Run `update-workspace` skill quand tu veux. Migration auto sur tes données. Breaking changes : {none / surfacés au lancement}.*
> *Detail : `docs/releases/{version}-manifest.json` (lis-le si tu veux comprendre le diff avant de pull).*

**Partner-side flow:**

1. Receive notification.
2. In their workspace: `git pull` (if cloned from a git remote) or rsync from the source if shared by file.
3. In Claude Code: trigger `update-workspace` (FR: "mets à jour phantomOS" / EN: "update workspace").
4. Skill reads `_version.json` (current installed) vs new `_version.json` (target), finds all manifests between, applies each by type, surfaces a plain-language recap. Partner data untouched.

**What the partner does NOT need:**
- Reading every CHANGELOG entry between their installed version and target — `update-workspace` summarizes
- Manually running migration scripts — delegated to `migrate-workspace` automatically on schema-bump
- Worrying about credentials.env or learnings.json — explicitly preserved (see § Template vs operator data above)

**When a partner skips updates** (e.g. doesn't pull for 6 weeks): the next pull may bridge multiple releases. `update-workspace` handles N-step chained updates by reading all manifests in version order. No manual intermediate step required.

**Auto-update at session start** — out of scope for v2.10.x. Considered, deferred (server infra needed, low ROI vs manual notif on a 5-50 partner cohort).

---

## Related

- `_version.json` — current template version registry.
- `docs/releases/` — every release manifest lives here, one file per version.
- `infra/migrations/` — every schema migration script lives here.
- `.skills/skills/update-workspace/SKILL.md` — the receiver's installer.
- `.skills/skills/migrate-workspace/SKILL.md` — delegated schema migration.
- `operator/installation.json` — partner-local version state (initialized at first install, updated on every successful update-workspace run).
- `CHANGELOG.md` — human-readable companion to the machine manifests.
