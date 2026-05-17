---
description: Vue d'oiseau spatiale sur une brand ou un projet. Recale instantanément après reprise. Rend visible zones acquises, en cours, non engagées, non cartographiées.
---

# /bird · vue d'oiseau projet

Slash command pointer vers `bird` skill. Recale l'opérateur en 5 secondes par une carte spatiale du territoire entier (pas un status report). Pair canon avec `/scope` (bird LIT la carte produite par scope).

## Mode detection

| Argument | Routing |
|---|---|
| `/bird` empty | vue macro composite, brand/projet actif (cascade détection · pwd → git → portfolio) |
| `/bird {nom}` | vue macro brand/projet nommé |
| `/bird all` | vue multi-brands (mini-territoires comparés cross-portfolio) |
| `/bird --zoom {zone}` | vue micro anatomie d'une zone scopée du projet courant |

## Invocation

Charger `.skills/skills/bird/SKILL.md` et suivre son workflow (1 détection brand · 2 chercher cartographie scope-map.md · 3 composer vue macro · 4 format output macro ou 5 micro --zoom ou 6 all).

**Hard rules à respecter (cf SKILL.md complet)** ·

- HR-1 · Output spatial obligatoire (grille ASCII, pas texte-only)
- HR-2 · Territoire d'abord, état après (zone vierge = même place qu'à 95%)
- HR-3 · Stabilité visuelle inter-sessions (positions zones constantes)
- HR-4 · Registre sobre institutionnel accessible (pas de métaphore ludique, pas de jargon brut)
- HR-5 · Révélation > confirmation (1 fois sur 3 doit révéler "ah merde j'avais oublié X")
- HR-6 · Zéro em-dash
- HR-7 · Investigation posture (zones étiquetées observé / déduit / déclaré / inconnu)
- HR-8 · Iconographie unifiée canon (✓ ◐ ○ ✗ ⚠ pour état · ▓░ pour complétion · zéro emoji couleur · légende au pied)

## Iconographie canon

Symboles uniques cohérents cross-commands opérateur-facing (cf `/phantom` pair canon) ·

| Symbole | Sens |
|---|---|
| `✓` | acquis · observé |
| `◐` | en cours · partiel |
| `○` | identifié · non engagé |
| `✗` | absent · non cartographié |
| `⚠` | alerte · attention requise |
| `▓░` | barre de complétion (visuel territoire) |
| `►` | position courante |
| `──▶` | dépendance entre zones |

Légende rendue au pied de chaque output (jamais en tête). Zéro emoji couleur (🔥 🟢 🟡 🔴 etc) où que ce soit dans l'output.

## Lexique opérateur

Substitutions canon pour rester accessible non-expert ·

| Interne | Opérateur-facing |
|---|---|
| données manquantes | (zone vide cartographiée) |
| fiche incomplète | (zone observée partielle) |
| spec incomplète | (entité encodée atomes manquants) |
| voix client manquante | (pas de verbatims sourcés) |
| tâche de fond | (skill en exécution silencieuse) |
| changement | (mutation entité) |
| alertes | (zones à surveiller) |
| action verbalisée | (jamais le nom du skill brut · *"creuser la zone"* pas *"scope X"*) |

`fog` reste canon `/bird` signature. Définition au pied de chaque output · *"fog = zone identifiée non engagée ou non cartographiée, point aveugle du territoire"*.

## Source de vérité

`/bird` LIT `brands/{slug}/scope-map.md` (artefact produit par `/scope`). Si absent · mode dégradé (zones déduites status.json + structure dossiers + commits récents), annoncer en bas de l'output et recommander `/scope {brand}` pour stabiliser le territoire.

## Cross-refs canon

- `/scope` · pair canon · PRODUIT la `brands/{slug}/scope-map.md` que `/bird` lit
- `docs/system/investigation-posture.md` · étiquettes observé / déduit / déclaré / inconnu utilisées pour catégoriser zones
- `.skills/skills/snapshot-brand/SKILL.md` v2.78.2 · sister consumer canon brand entity opérateur-facing
- `.skills/skills/profile-audience/SKILL.md` v2.78.2 · sister consumer matrice audience × pain × angle × stage
- `.skills/skills/brief-day/SKILL.md` · navigator macro cross-brands au start (vs bird qui zoome 1 brand)
- `.skills/skills/resume-session/SKILL.md` · reprise narrative thread actif (vs bird spatial macro)
