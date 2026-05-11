## Mode audiences-tree

`/phantom {brand} audiences` rend l'arbre des audiences cartographiées + chevauchements visuellement. Vue brand-side application du framework cartography. Override le mode entity-drill générique pour l'entité `audiences` (le drill détaillé per-audience reste accessible via `/phantom {brand} audiences {slug}` mode item).

Lecture · iterate `brands/{brand}/audiences/*/profile.json` + extract `meta.scope`, `meta.parent_slug`, `meta.overlap_with`, `meta.entry_door`, top pain (pain_points[0].formulation), validation_status. Mapping interne vers vocabulaire operator : `scope: broad/mother` → `[mère]`, `scope: segment/sub` → `[poche]`, `scope: micro` → `[niche]` ; `entry_door` parmi (problem, goal, identity) → `PAR UN PROBLÈME`, `PAR UN OBJECTIF`, `PAR QUI ELLE EST` ; `validation_status: hypothesis` → `à valider`.

Format :

```
workspace > {brand} > audiences
══════════════════════════════════════════════
ARBRE AUDIENCES {BRAND} · {N} cartographiées ({N_mother} mères + {N_sub} sous-groupes)

PAR UN PROBLÈME (chute) · porte d'entrée non posée
  ├── chute-active                     [mère]       à valider · {N} témoignages
  │     ├── chute-post-grossesse       [poche]      à valider · {N} témoignages
  │     ├── chute-stress-hormonal      [poche]      à valider · {N} témoignages
  │     └── chute-traction             [poche]      à valider · {N} témoignages
  
PAR UN OBJECTIF (croissance) · porte d'entrée non posée
  └── croissance-projet                [mère]       à valider · {N} témoignages
        ├── pousse-jeune-adulte        [poche]      à valider · {N} témoignages
        └── pousse-recovery            [poche]      à valider · {N} témoignages

CHEVAUCHEMENTS DÉCLARÉS
  aucun chevauchement posé · relations cousines à mapper

POINTS À COMPLÉTER
  ⚠ {X}/{N} audiences sans porte d'entrée déclarée
  ⚠ {N} audience-orpheline · {OK ou détail mère manquante}
  ⚠ {N} audience-fantôme · {OK ou détail}
  ⚠ Verbatims clients à consolider (mining encore léger)
  ⚠ Chevauchements à poser entre audiences

NEXT SUGGESTED
  → Tape : `récupère les témoignages clients` (consolider verbatims, mining)
  → Tape : `pose les portes d'entrée` (qualifier les audiences)
  → Tape : `voir le cours complet` (revoir le framework)

─────
`/phantom ?` pour voir tous les modes · `/phantom search` pour chercher
```

Dégrade gracieusement · si `meta.parent_slug` + `meta.overlap_with` vides sur toutes les audiences, rendre liste à plat avec note *"relations non posées (audiences à plat sans hiérarchie). Consulter le cours complet pour comprendre comment les structurer."*. Si aucune audience encodée, renvoyer vers empty state entity-drill standard.

### Post-render filter (v2.42+)

Avant émission, appliquer le filtre jargon `.skills/_jargon_bank.json` selon le contrat universel défini dans `phantom.md § Post-render jargon filter`. Le rendu peut sortir verbatim si le mapping interne -> operator-facing du rendering ci-dessus est déjà appliqué (cf vocabulaire `mère/poche/niche`, `à valider`, `par un problème`, `audience-fantôme/orpheline`, `témoignages`). Si un token jargon résiduel reste détectable hors backticks code, substitution forcée via `apply_jargon_filter(output_text, locale="fr")`.
