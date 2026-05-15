---
name: analyze-extension-intent
type: curator
version: "1.0.0"
recommended_model: sonnet
layer: meta
reasoning_pattern: null
description: >
  Sub-skill of scaffold-extension. Captures operator intent for a new extension and
  extracts structured attributes: entity class (custom entity / sidecar / skill-only),
  data shape (time-series / instance-per-item / aggregate), population mechanism
  (manual / scraper / derived), declared cross-references. Three focused questions max.
  Invoked by scaffold-extension Phase 1. Not intended for direct operator invocation.
  FR: "analyse l'intent extension" "capture l'intent" "extension intent".
  EN: "analyze extension intent" "capture extension intent" "extension intent".
permissions:
  reads: [brand]
  writes: []
  mode: none
  subagent_safe: true
pipeline:
  preconditions: operator has expressed intent to build an extension
  postconditions: structured intent object returned to orchestrator
---

# Skill: Analyze Extension Intent

Captures and structures the operator's intent for a new extension.

## Method

Ask at most three focused questions, one per turn, calibrated to the conversation register:

1. **Nature of the data** — *"Ce que tu veux stocker, c'est plutôt une observation qui évolue dans le temps, des items distincts que tu ajoutes au fil, ou un enrichissement de ce que tu as déjà sur cette marque ?"*
2. **Source and cadence** — *"Tu le rempliras toi-même à la main, un skill va le remplir automatiquement (scraper, API pull), ou c'est calculé à partir d'autres données ?"*
3. **Cross-references** — *"Ça pointe vers quoi dans ton workspace ? Un produit précis ? Une audience ? Une offre ? Rien de précis ?"*

Skip questions that are already answered by the operator's opening message.

## Method — Mode data-first

Si l'opérateur fournit une donnée structurée (bloc JSON, tableau, liste de variables avec valeurs), inférer silencieusement :

- **Class** — si donnée = une liste d'observations sur même sujet avec évolution temporelle possible → time-series custom entity. Si donnée = plusieurs items distincts avec attributs parallèles → instance-per-item custom entity. Si donnée = champs qui enrichissent un concept brand existant → sidecar. Si donnée = un fait simple → route vers capture-learning (pas scaffold).
- **Shape** — inférée de la structure de la donnée.
- **Cross_refs** — scanner la donnée pour détecter les slugs/IDs qui pointent vers core entities (`product_slug`, `audience_slug`, `offer_id`).
- **Proposed_name** — inféré du contenu thématique ou demandé en 1 question si ambigu.

Poser maximum **une question** à l'opérateur, et uniquement sur ce qui reste ambigu après l'inférence (typiquement : population mechanism future — *"ça, ça va venir de toi manuellement, ou un skill va le pull automatiquement ?"*).

La donnée fournie est conservée dans le contexte pour Phase 7 (scaffold-entity-files) qui la populera directement en tant qu'instance(s) dans le fichier créé.

## Output

Return a structured intent object to the orchestrator:

```
{
  "class": "custom_entity | sidecar | skill_only | route-to-capture-learning",
  "shape": "time_series | instance_per_item | aggregate",
  "population": "manual | scraper | derived",
  "cross_refs": ["product_slug", "audience_slug", ...],
  "proposed_name": "{operator_provided_or_suggested}",
  "scope": "brand | workspace",
  "entry_mode": "intent_first | data_first",
  "provided_data": { /* populated only in data_first mode, passed to Phase 7 */ }
}
```

## Hard rules

- Three questions maximum across all turns of this phase.
- Never ask for field names here — schema drafting happens in Phase 3.
- Never ask for technical format (JSON, shape, etc.) — the skill infers from the conceptual answer.
