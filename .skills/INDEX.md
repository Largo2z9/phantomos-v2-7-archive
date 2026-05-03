# Skills index by operator intent

Operator-facing index of skills, grouped by what the operator wants to *do*, not by skill type or alphabetical order. Use this when an operator describes a goal in natural language without naming a skill.

The agent reads `_manifest.json` for routing details (frontmatter, triggers, model, subagent). This file is the human bridge from intent to skill name.

Last update : 2026-04-29.

---

## I want to set up a new brand or workspace

| Operator says | Skill to invoke |
|---|---|
| *"on commence sur une nouvelle marque"*, *"new brand"*, *"setup une marque"* | `setup-brand` (orchestrator that walks the 4-step pipeline) |
| *"juste fais le setup vite fait"*, *"onboard cette marque"* | `onboard-brand` (full pipeline shortcut) |
| *"je te donne l'URL, fais-moi un premier scan"* | `snapshot-brand` (URL → brief fiche défendable) |
| *"je veux comprendre ce que je tourne"*, *"quelle version j'ai ?"* | Read `_version.json` + `docs/product/variant-map.md` |

---

## I want to understand the audience or the market

| Operator says | Skill to invoke |
|---|---|
| *"qu'est-ce que disent les clients de cette marque"*, *"voice of customer"*, *"VoC"* | `mine-voc` |
| *"qu'est-ce qui se passe sur le marché", *"voice of market"*, *"VoM"* | `mine-vom` |
| *"identifie les audiences candidates"*, *"qui sont les acheteurs"* | `mine-audience` |
| *"approfondis le contexte de cette marque"*, *"deepen brand"* | `deepen-brand-context` (orchestrates VoC + VoM in parallel) |
| *"le produit fit avec cette audience ?"* | `score-product-fit` |
| *"étude de niche complète"*, *"market deep dive"* | `study-niche-marketdeepdive` |

---

## I want to produce a paid creative or copy

| Operator says | Skill to invoke |
|---|---|
| *"sors-moi des angles paid"*, *"angles for Meta ads"*, *"5 angles ranked"* | `produce-paid-angles` |
| *"écris-moi un brief copywriter"*, *"copy brief on this audience"* | `produce-copy-brief` |
| *"score cette offre", *"audit cette offre"*, *"l'offre tient ou pas ?"* | `score-product-fit` |

---

## I want to audit something

| Operator says | Skill to invoke |
|---|---|
| *"audit le setup Meta"*, *"check les comptes pubs"* | `audit-meta-account` |
| *"valide le workspace"*, *"check les ressources"*, *"y a quoi qui cloche"* | `validate-resources` |
| *"audit la cohérence cross-docs"* | (sub-agent Explore on demand, no shipped skill) |

---

## I want to capture or persist something

| Operator says | Skill to invoke |
|---|---|
| *"note ça"*, *"retiens que"*, *"capture ce learning"*, *"on a découvert que"* | `capture-learning` (single fact) |
| *"learn from session"*, *"persiste la session"*, *"end of day"* | `learn-from-session` (batch session capture) |
| *"exporte cette conversation"*, *"archive cette session"* | `export-session` |
| *"range ce document"*, *"range cette URL"*, *"ingest ça"* | `ingest-resource` |

---

## I want to extend or build something new

| Operator says | Skill to invoke |
|---|---|
| *"j'aimerais créer une automatisation"*, *"on va segmenter les étapes"*, *"je veux faire un workflow X"* | `scaffold-extension` (then a sub-skill for the specific output) |
| *"crée une extension"*, *"nouveau type de donnée"*, *"où je range cette donnée"* | `scaffold-extension` |
| *"tracker X au fil du temps"*, *"j'ai une donnée nouvelle à ranger"*, *"ajoute un sidecar"* | `scaffold-extension` |
| *"build un agent pour X"*, *"crée un skill custom"* | `build-agent` |

---

## I want to navigate or resume

| Operator says | Skill to invoke |
|---|---|
| *"où j'en suis ?"*, *"brief-moi sur où j'en étais"*, *"recap"* | `brief-day` |
| *"reprends"*, *"continue où on s'est arrêté"* | `resume-session` |
| *"qu'a-t-on dit sur X"*, *"cherche dans les sessions passées"* | `session-search` |

---

## I want to migrate or upgrade

| Operator says | Skill to invoke |
|---|---|
| *"upgrade le workspace"*, *"migre vers la nouvelle version"* | `migrate-workspace` |

---

## I want to connect an external tool

| Operator says | Skill to invoke |
|---|---|
| *"connect meta ads"*, *"ajoute shopify"*, *"branch klaviyo"* | `connect-source` (uses convention if shipped, scopes new platforms via `scope` skill) |
| *"connect un nouvel outil"*, *"add external source"* | `connect-source` (asks platform name, then routes) |
| *"qu'est-ce que j'ai connecté ?"*, *"liste mes sources"* | Read `operator/connected-sources.json` + `brands/{slug}/connected-sources.json` |

---

## When the intent is ambiguous

If the operator's phrasing matches multiple intents (e.g. *"audit le contexte de cette marque"* could be `validate-resources` or `deepen-brand-context`), read the `disambiguates_against` block in the manifest entry of each candidate. If still ambiguous after that, ask one `AskUserQuestion` with 2 to 3 candidates.

If no skill matches, do not invent one. Surface honestly that the requested operation does not have a shipped skill, and offer to scaffold one via `scaffold-extension` if it is structural enough to deserve persistence.

---

## Maintenance

This index is human-edited. Add an entry when :
- A new skill ships (add row in the matching section).
- An operator phrasing repeatedly fails to match an existing skill (add the phrasing to the trigger column).
- A skill is renamed, removed, or merged (update or delete the row).

The index does not replace the manifest. It complements it for the moment when the operator describes a goal without naming a skill.
