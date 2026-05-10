## Mode audiences-tree

`/phantom {brand} audiences` rend l'arbre des audiences cartographiées + chevauchements visuellement. Vue brand-side application du framework cartography. Override le mode entity-drill générique pour l'entité `audiences` (le drill détaillé per-audience reste accessible via `/phantom {brand} audiences {slug}` mode item).

Lecture · iterate `brands/{brand}/audiences/*/profile.json` + extract `meta.scope`, `meta.parent_slug`, `meta.overlap_with`, top pain (pain_points[0].formulation), validation_status.

Format :

```
workspace > {brand} > audiences
══════════════════════════════════════════════
ARBRE AUDIENCES {BRAND} · {N} cartographiées

PROBLEM-DRIVEN (chute)
  ├── chute-active                     [broad]      hypothèse
  │     ├── chute-post-grossesse       [segment]    hypothèse · 1 verbatim seed
  │     ├── chute-stress-hormonal      [segment]    hypothèse · 0 verbatim
  │     └── chute-traction             [segment]    hypothèse · 0 verbatim
  │
GOAL-DRIVEN (croissance)
  ├── croissance-projet                [segment]    hypothèse
  ├── pousse-jeune-adulte              [segment]    hypothèse
  └── pousse-recovery                  [segment]    hypothèse
  ⚠ audience-orpheline · pas de broad parent croissance

CHEVAUCHEMENTS DÉCLARÉS
  chute-post-grossesse  ↔  chute-stress-hormonal
  chute-stress-hormonal ↔  chute-active
  pousse-jeune-adulte   ↔  croissance-projet

GAPS DÉTECTÉS (post application framework)
  ⚠ 7/7 audiences sans entry_door déclarée
  ⚠ 1 audience-orpheline (croissance broad manquante)
  ⚠ 0 audience-fantôme · OK
  ⚠ chevauchements à confirmer (déclarés vs détectés via mining)

NEXT SUGGESTED
  → Tape : profile-audience {brand} sur chute-post-grossesse (drill prioritaire)
  → Tape : `/phantom doctrine audiences` (revoir framework)
  → Tape : créer broad croissance manquant (audience-orpheline)
```

Dégrade gracieusement · si `meta.parent_slug` + `meta.overlap_with` vides sur toutes les audiences, rendre liste à plat avec note *"relations non posées · tape `/phantom doctrine audiences` pour voir le framework, puis pose parents et chevauchements"*. Si aucune audience encodée, renvoyer vers empty state entity-drill standard.

Cross-ref · `docs/doctrine/audience-cartography-framework.md`.
