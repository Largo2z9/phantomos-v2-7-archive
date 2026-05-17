---
description: Cartographie un sujet flou (LEARN ou BUILD) en carte de paramètres décidables. Questions guidées + output dual markdown + Excalidraw + décisions actionnables.
---

# /scope · cartographe des paramètres décidables

Slash command pointer vers `scope` skill. Transforme une intention floue en carte des paramètres décidables. Pair canon avec `/bird` (scope CRÉE la carte, bird LIT la carte).

## Mode detection

| Argument | Routing |
|---|---|
| `/scope` empty | demander le sujet à scoper (1 question), puis charger skill scope |
| `/scope {sujet}` | charger skill `scope` avec sujet (auto-détection LEARN ou BUILD) |
| `/scope {sujet} --learn` | force mode LEARN (pédagogie domaine) |
| `/scope {sujet} --build` | force mode BUILD (scoping construction système) |
| `/scope {sujet} --matrix=canonical` | force matrice canonique au lieu de génération dynamique |
| `/scope {sujet} --for-skill={nom}` | mode pré-requis create-skill (carte → SKILL.md derrière) |

## Invocation

Charger `.skills/skills/scope/SKILL.md` et suivre son protocole d'exécution (Phase 1 reformulation · Phase 2 questions guidées · Phase 3 cartographie · Phase 4 output dual · Phase 5 persistence).

**Hard rules à respecter (cf SKILL.md complet)** ·

- Toujours questions guidées Phase 2 avant carto (jamais skip)
- Output dual systématique · markdown structuré 5 sections canon (Observé · Déduit · Inconnu · Leviers · Close ouvert) + Excalidraw checkpoint
- Bloc final "Prochaines décisions actionnables" (3 max) non-négociable
- Génération dynamique des axes par défaut, matrice canonique uniquement sur demande explicite
- Zéro em-dash
- Calibrage complexité requête (brief court = mode léger 4-5 axes)

## Persistence

Si le scope est structurant pour une brand active, proposer persistence dans `brands/{slug}/scope-map.md` (path canonique consommé par `/bird`).

## Cross-refs canon

- `docs/system/investigation-posture.md` · doctrine mère du format output 5 sections
- `docs/system/canonical-matrix-reasoning.md` · schema + matrice canon (si scope produit matrice canonique invocable)
- `/bird` · pair canon · LIT la carte produite par `/scope`
- `.skills/skills/create-skill/SKILL.md` · downstream consumer du scope `--for-skill`
