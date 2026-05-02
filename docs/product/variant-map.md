# PhantomOS variants

Four PhantomOS variants exist in distinct repositories. Each is a runtime environment for a different audience and ships a different set of skills, resources, and integrations. The agent should detect which variant it runs on at session start and adjust accordingly.

This document is the single source of truth for the variant matrix. Read it on demand when the operator asks *"qu'est-ce que je tourne ?"*, *"quelle version je suis ?"*, or when a skill behaves differently than expected.

---

## The four variants

| Variant | Repository | Audience | Status |
|---|---|---|---|
| **Master internal** | `largo-kb/05-projects/context-engine/workspace-template/` (private, monorepo internal) | Largo and direct collaborators only. The copy authoring source of truth. | active, edited continuously |
| **Public template** | `Largo2z9/phantomos-template` (private GitHub, share by invite) | External operators, partners, investors. Ships clean without business-perso signals. | active |
| **Abyss extension** | `Largo2z9/phantom-os-abyss` (private GitHub) | Growth partners working alongside the Abyss data infrastructure (cockpit + Supabase + Airbyte). | active, info-only mode |
| **Cockpit-pack addon** | local `~/dev/phantom-os-abyss-cockpit-pack/` for now, future private repo | Growth partners once the Abyss back-end is multi-operator ready. | held, not distributed yet |

---

## What ships in each variant

| Component | Master | Public | Abyss | Cockpit-pack |
|---|---|---|---|---|
| Core doctrine `docs/system/` | yes | yes | yes | n/a (addon, no doctrine) |
| Skills library `.skills/skills/` core | yes | yes | yes | n/a |
| Brand template `brands/_TEMPLATE/` | yes | yes | yes | n/a |
| Operator extensions layer `operator/extensions/` | yes | yes | yes | n/a |
| KB shared resources `resources/` | yes | yes | yes | n/a |
| Vision docs `docs/vision/` (manifesto, positioning, prisms, roadmap) | full | allégé (no offering-deployment, manifesto §7 reformulé, fit consultant tension neutralisé) | allégé | n/a |
| `offering-deployment.md` (commercial business plan) | yes | no | no | n/a |
| `ABYSS.md` (Abyss extension layer description) | n/a | n/a | yes | n/a |
| `infra/*.md` Abyss SOPs (per-platform access guides) | no | no | yes | n/a |
| `.skills/skills/onboard-client/` (cockpit-bridge skill) | no | no | no | yes |
| `scripts/` (Airbyte provisioner, Supabase regen, Snap ingest, etc.) | no | no | no | yes |

---

## Variant detection at session start

The agent should detect which variant runs on the current workspace. Three signals, in order of reliability :

1. **`_version.json`** at workspace root. Always present. The `template_version` field gives the doctrine version. Master and public diverge, Abyss diverges separately.
2. **`ABYSS.md`** at workspace root. Present only on the Abyss variant. If found, the agent is on `phantom-os-abyss`.
3. **`scripts/onboard-brand.mjs`** at workspace root. Present only when the cockpit-pack has been dropped in. If found, the agent is on `phantom-os-abyss + cockpit-pack`. Without it, Abyss layer is in info-only mode.

The agent encodes the detected variant in `operator/context.json#workspace_variant` for persistence and reference by skills that have variant-specific behavior.

---

## Variant-specific behavior

**Master.** Full doctrine including business-perso content. Used for authoring, never shipped externally.

**Public template.** Doctrine without business-perso signals. Skills library is the same as master minus offering-deployment references. Used as the starting point for any external operator (StrideUp, partners, etc.).

**Abyss.** Public template plus the Abyss layer (info-only without the cockpit-pack). The `ABYSS.md` declares what the layer covers, what is operational, what is held until the cockpit-pack ships. SOPs in `infra/*.md` are read-only references usable without the cockpit infrastructure.

**Cockpit-pack added on Abyss.** Once the cockpit-pack is dropped onto the Abyss workspace, the cockpit-side automations become operational. The `onboard-client` skill, the Airbyte provisioner, the Supabase regen, and the Snap manual ingest all become available. Architecture rule applies : cockpit provisions and displays, workspace acts ; communication via Supabase tables, never direct HTTP.

---

## When the operator asks the question

If the operator types something like *"qu'est-ce que je tourne ?"*, *"version ?"*, *"je suis sur quoi ?"*, the agent runs the detection above and answers in plain language. Example reply :

> *"Tu tournes sur PhantomOS public template, version 2.11.5 doctrine, sans la couche Abyss. Le kit DTC marketing est shipped, la doctrine technique est complète, les skills opérateur sont disponibles. Pas de cockpit-side automation puisque tu n'as pas l'addon Abyss installé."*

Adapt the language to the detected register (tu/vous, FR/EN). Surface the variant + version + what's available + what's not. No menu, no questionnaire.

---

## When upstream updates

The master is edited continuously. The public template syncs on validated releases (manual discipline, no auto-pipeline). The Abyss variant is wired as downstream of the public template via `git remote add upstream`. Updates merge cleanly because the Abyss layer is additive.

When a new doctrine version ships in master :
1. Sync to public template (manual cherry-pick or rsync without `--delete`).
2. Public template pushes to GitHub.
3. Abyss variant operators pull from upstream when they want the latest.
4. Cockpit-pack stays at its own cadence (independent versioning, not tied to doctrine).

---

## Cross-references

- `docs/system/agent-contracts.md` size policy and Agent Contract spec.
- `_version.json` current doctrine version.
- `ABYSS.md` (only on Abyss variant) Abyss layer scope and operational status.
- `~/dev/phantom-os-abyss-cockpit-pack/README.md` (when distributed) install instructions for the cockpit pack.
