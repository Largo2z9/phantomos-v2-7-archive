# PhantomOS variants

PhantomOS ships as a workspace template that an operator clones and operates on. Two distinct surfaces exist : the workspace template itself, and the operator's own instance once the template is cloned and filled.

This document is the single source of truth for variant detection. Read it on demand when the operator asks *"qu'est-ce que je tourne ?"*, *"version ?"*, or when a skill behaves differently than expected.

---

## The two surfaces

| Surface | Path | Audience |
|---|---|---|
| **Template** | This repository, cloned at workspace root. | The operator who clones to start a new workspace. |
| **Operator instance** | The cloned workspace + the operator's own brands, learnings, custom skills, credentials. | The operator who runs PhantomOS day to day. |

The template ships clean : doctrine, skills library, brand template, operator extensions layer, KB shared resources, vision docs, getting-started guide, conventions for the supported external platforms. Once cloned, the operator fills `brands/{slug}/`, connects sources, captures learnings, and the workspace becomes the operator's own.

---

## Variant detection at session start

The agent should detect a few signals about the workspace state at session start.

1. **`_version.json`** at workspace root. Always present. The `template_version` field gives the shipped doctrine version.
2. **`brands/`** content. If only `brands/_TEMPLATE/` and `brands/_EXAMPLE/` exist, the operator hasn't started yet. If at least one real brand folder exists, the workspace is active.
3. **`operator/profile.json`** state. If `identity.name` or `identity.profile` is filled, the operator has been onboarded.

The agent encodes the detected state in `operator/awareness.json` for persistence.

---

## When the operator asks the question

If the operator types something like *"qu'est-ce que je tourne ?"*, *"version ?"*, *"je suis sur quoi ?"*, the agent runs the detection above and answers in plain language. Example reply :

> *"Tu tournes sur PhantomOS template, version {X}, avec {N} brand(s) configuré(s). Le kit DTC paid acquisition est livré, doctrine et skills opérateur disponibles."*

Adapt the language to the detected register (tu/vous, FR/EN). Surface the version + what's filled + what's not. No menu, no questionnaire.

---

## When upstream updates

The template ships incremental releases. To update :

1. `git pull` (if cloned from git) or rsync the new template files into the workspace folder.
2. In Claude Code, *"update workspace"*. The `update-workspace` skill reads installed version vs target, applies every change.

The operator's brand data, captured learnings, custom skills, and credentials are preserved end to end. Only template files (skills, docs, schemas) are updated. Skipping multiple releases is fine. The skill handles N-step chained updates.

---

## Cross-references

- `docs/system/agent-contracts.md` for size policy and Agent Contract spec.
- `_version.json` for the current doctrine version.
- `CHANGELOG.md` for release history human-readable.
- `docs/internal/releases/manifest/` for technical release manifests (contributors).
