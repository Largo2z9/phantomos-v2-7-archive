---
name: changelog-discipline
description: Doctrine canon · pattern CHANGELOG.md Keep-a-Changelog convention · cap 80L par release · sections atomiques · 3 sources vérité distinctes (CHANGELOG public · project-journal interne · manifests JSON détails)
type: doctrine
version: v2.83.0
status: shipped
---

# Changelog Discipline · Operating Doctrine

> Canonique v2.83.0. Doctrine canon racine qui codifie le pattern canon pour le `CHANGELOG.md` workspace-template PhantomOS. Résumé exécutif Keep-a-Changelog strict · sections atomiques · cap 80 lignes par release entry. Narrative cognitive Largo vit dans `docs/internal/project-journal.md`. Détails structurés étendus vivent dans `docs/internal/releases/manifest/{version}-manifest.json`. Doctrine sœur de `claude-md-doctrine.md` v2.82.0 (même pattern anti-inflation forme · test de suppression obligatoire · capacité attention bornée). Ferme le gap *"CHANGELOG.md racine dérive en narrative doctrinale par release · 4270L vs cible ~1150L · 3-4× sur-dimensionné · founder's curse répété (justification complète au lieu de delta concis) · audit externe Claude Web v2.82.1 flag systémique"*.

---

## 1. Thèse fondatrice

> Le `CHANGELOG.md` racine workspace-template est un résumé exécutif Keep-a-Changelog. Pas un journal narratif Largo. Pas une cartographie doctrinale. Pas un manifest détaillé. 3 sources de vérité distinctes · le CHANGELOG sert l'opérateur runtime plus le contributeur externe en 5 à 10 secondes de scan, pas en 10 minutes de lecture.

**Définition canon CHANGELOG.md** · fichier d'historique release format Keep-a-Changelog (`https://keepachangelog.com/`) consommé par opérateurs runtime via `/version` et `/update` slash commands plus `push-phantomos.sh` release gate plus contributeurs externes scan rapide. Format atomique (1 item = 1 ligne · pas paragraphe). Cap 80 lignes par release. Sections canoniques uniquement (Added · Changed · Removed · Fixed · Migration · Breaking).

**Différenciation 3 sources vérité distinctes** ·

| Source | Public cible | Format | Cap taille | Fonction |
|---|---|---|---|---|
| `CHANGELOG.md` racine | opérateur runtime + contributeur externe | Keep-a-Changelog strict atomique | 80L par release | résumé exécutif scan rapide |
| `docs/internal/project-journal.md` | Largo founder | narrative libre | zéro cap | archive cognitive symbolique |
| `docs/internal/releases/manifest/{version}-manifest.json` | release engineering | JSON structuré | détails étendus | audit_amont · patches_structurels · files_patched · backlog · rollback_strategy |

Le CHANGELOG canon répond à 4 questions miroir ·

1. *"Chaque release entry tient-elle en ≤80 lignes lisibles en 5-10 secondes ?"* (cap taille runtime consumable)
2. *"Les sections respectent-elles le canon Keep-a-Changelog (Added · Changed · Removed · Fixed · Migration · Breaking) sans variations floues ?"* (sections atomiques · zéro Notes/Misc/Other)
3. *"Chaque item tient-il en 1 ligne sans paragraphe ni justification doctrinale ?"* (atomicité · founder's curse externalisé)
4. *"Le contenu détaillé étendu vit-il dans manifest JSON plutôt qu'inline ?"* (CHANGELOG pointe · n'explique pas)

CHANGELOG narratif signale que le mainteneur écrit pour lui-même (archivage cognitif · justification complète releases passées). CHANGELOG canon signale que le mainteneur écrit pour opérateur runtime · capacité scan bornée · ROI mesurable par ligne. C'est la différence entre journal personnel (passif) et résumé exécutif release (operable).

---

## 2. Le problème résolu

Sans Changelog Discipline canon ·

1. **Founder's curse répété par release.** Chaque release devient justification doctrinale complète au lieu de delta concis. Le mainteneur explique *pourquoi* la doctrine existe (déjà dans le fichier doctrine) au lieu de signaler *quoi* a changé. Audit externe Claude Web sur PhantomOS v2.82.1 flag 4270L CHANGELOG vs cible ~1150L · 3-4× sur-dimensionné systémique.

2. **Capacité scan opérateur dépassée silencieusement.** Le CHANGELOG sert le runtime via `/version` `/update` slash commands plus le contributeur externe scan rapide. Entry release >80L casse cette fonction · l'opérateur doit lire 10 minutes au lieu de scanner 10 secondes. Le mainteneur ajoute par accumulation · perception qu'ajouter c'est documenter · réalité c'est diluer.

3. **3 sources vérité dupliquées sans hiérarchie claire.** Sans canonisation, la même info (rationale doctrinale · narrative Largo · détails structurels) vit simultanément dans CHANGELOG + project-journal + manifest JSON. Mainteneur ne sait plus quoi mettre où. Drift inévitable · 3 versions divergentes du même changement après quelques releases.

4. **Sections non-canoniques (Notes · Misc · Other · TODO · Doctrine) leak structure floue.** Keep-a-Changelog définit 6 sections canoniques strict. Toute variation casse parsing automatisé (release notes generators · CI gates) plus dégrade scan rapide opérateur (sections floues = signal faible).

---

## 3. Sections atomiques canon Keep-a-Changelog

6 sections canoniques uniquement. Zéro variation tolérée.

| Section | Trigger | Exemples atomiques |
|---|---|---|
| **Added** | NEW skills · NEW doctrines · NEW commands · NEW capabilities | `Skill /audit-pmax (audit Performance Max Google Ads · 7 dimensions)` |
| **Changed** | existing modifié (skill bump · doctrine extension · command refactor) | `Doctrine claude-md-discipline v2.81 → v2.82.0 (3 HR ajoutés post-audit externe)` |
| **Removed** | skills/doctrines/commands retirés (deprecation) | `Skill /old-audit-perf retiré (remplacé par /audit-perf v2)` |
| **Fixed** | bugfixes · régressions corrigées | `Fix manifest JSON parse error sur version 2.79.5 (escape char dans description)` |
| **Migration** | BREAKING changes avec migration path · cross-ref scripts | `BREAKING · skills v1 schema → v2 schema · cf migration-scripts/v1-to-v2.sh` |
| **Breaking** | BREAKING changes sans migration auto (rare · nécessite opérateur action) | `BREAKING · supprime alias /old-perf · opérateurs doivent rewrite invocations` |

**Hiérarchie sémantique** · Added > Changed > Removed > Fixed > Migration > Breaking. Ordre canon dans chaque release entry. Sections vides omises (pas de section vide visible).

---

## 4. Pattern entry release · 3-5 lignes max par section

Pattern canon strict ·

```markdown
## [VERSION] · YYYY-MM-DD

### Added
- Item 1 (1 ligne · pas paragraphe)
- Item 2

### Changed
- Item 1

### Fixed
- Item 1

[etc]
```

**Règles atomiques entry** ·

- 1 item = 1 ligne (zéro paragraphe inline)
- Cap 80 lignes total entry release (toutes sections cumulées)
- Cross-ref manifest JSON optionnel à la fin si détails étendus pertinents · pas obligatoire par release
- Cross-ref doctrine concernée pour rationale (pointer · pas justification inline)
- Date ISO format `YYYY-MM-DD`
- Version SemVer strict (`https://semver.org/`)

**Exemple canon entry release** ·

```markdown
## [2.83.0] · 2026-05-17

### Added
- Doctrine changelog-discipline (canon CHANGELOG Keep-a-Changelog · cap 80L · 4 HR strict)
- Doctrine claude-md-discipline v2.82.0 (anti-inflation CLAUDE.md root)
- Split CHANGELOG racine vs project-journal interne (3 sources vérité distinctes)

### Changed
- CHANGELOG.md racine refactor narrative → Keep-a-Changelog strict
- docs/system/README.md doctrine inventory bump (changelog-discipline ajouté)

### Migration
- Détails manifest JSON · cf docs/internal/releases/manifest/2.83.0-manifest.json
```

---

## 5. Anti-patterns canon

4 anti-patterns canonisés · test de suppression appliqué pre-ship strict.

1. **AP-CHL-1 · Sections non-canoniques.** Toute section autre que Added · Changed · Removed · Fixed · Migration · Breaking (Notes · Misc · Other · TODO · Doctrine · Internal · Reflection). Casse parsing automatisé + dégrade scan rapide opérateur.

2. **AP-CHL-2 · Entry release >80 lignes.** Sur-dimensionnement systémique · narrative doctrinale leak · founder's curse répété. Audit v2.82.1 flag 4270L total vs cible 1150L · 3-4× drift.

3. **AP-CHL-3 · Justification doctrinale inline.** Phrases type *"cette doctrine existe parce que..."* + brand positioning + rationale complète + analogie cognitive. Vivent dans fichier doctrine concerné (`docs/system/{doctrine}.md`) · pas dans CHANGELOG. CHANGELOG signale *quoi* change · pas *pourquoi* la doctrine existe.

4. **AP-CHL-4 · Duplication entre 3 sources vérité.** Le même contenu (rationale · narrative · détails structurels) dupliqué entre CHANGELOG + project-journal + manifest JSON. Drift inévitable post-quelques releases · 3 versions divergentes du même changement. CHANGELOG pointe vers manifest pour détails · project-journal indépendant (narrative Largo · pas miroir CHANGELOG).

---

## 6. Hard Rules canon

4 Hard Rules strict · test de suppression appliqué pre-ship.

- **HR-CHL-1** · `CHANGELOG.md` racine workspace-template · convention Keep-a-Changelog strict · sections canoniques uniquement (Added · Changed · Removed · Fixed · Migration · Breaking). Zéro variation tolérée.
- **HR-CHL-2** · Cap 80 lignes par release entry total (toutes sections cumulées). Au-delà · externaliser détails vers `docs/internal/releases/manifest/{version}-manifest.json` ou `docs/internal/project-journal.md` selon nature.
- **HR-CHL-3** · Zéro narrative doctrinale dans CHANGELOG. Justifications doctrinales → fichier doctrine concerné (`docs/system/{doctrine}.md`). Journal cognitif Largo → `docs/internal/project-journal.md`. CHANGELOG pointe · n'explique pas.
- **HR-CHL-4** · 3 sources de vérité distinctes · CHANGELOG public (résumé exécutif) · project-journal interne (narrative cognitive) · manifest JSON (détails structurés étendus). Zéro duplication entre les 3 sources.

**Test de suppression appliqué pre-ship** ·

- Si retire HR-CHL-1 · sections non-canoniques (Notes · Misc · Other) possibles · casse parsing automatisé release notes generators + CI gates · vrai gap structurel.
- Si retire HR-CHL-2 · taille entry release dérive sans plafond · narrative doctrinale leak inéluctable · audit v2.82.1 prouve ce point · vrai gap mesurable.
- Si retire HR-CHL-3 · founder's curse répété par release · justification complète au lieu de delta concis · scan rapide opérateur cassé · vrai gap fonctionnel.
- Si retire HR-CHL-4 · duplication entre 3 sources · drift inévitable post-quelques releases · 3 versions divergentes du même changement · vrai gap maintenabilité.

4 HR atomiques tous justifiés par erreur concrète identifiable. Zéro HR vague ou couvert par autre HR.

---

## 7. Cross-références

- `docs/system/claude-md-doctrine.md` v2.82.0 · doctrine sœur · même pattern anti-inflation forme + test de suppression obligatoire
- `docs/system/output-clarity-doctrine.md` v2.79.2 · standards Vercel/GitHub-grade outputs opérateur-facing · cohérent ton canon
- `docs/system/update-distribution-doctrine.md` v2.80.0 · consumer CHANGELOG via `/version` `/update` slash commands runtime
- `docs/internal/project-journal.md` · journal narratif Largo · archive cognitive · zéro cap
- `docs/internal/releases/manifest/{version}-manifest.json` · détails structurés étendus par release
- `https://keepachangelog.com/` · convention externe canon
- `https://semver.org/` · versioning canon

---

## 8. Position dans le système opérationnel

CHANGELOG canon = couche racine résumé exécutif release. Sœur de `claude-md-doctrine.md` (anti-inflation forme · root workspace-template). Consommée par `/version` plus `/update` slash commands runtime plus `push-phantomos.sh` release gate plus contributeurs externes scan rapide.

**Status** · Doctrine canon shipped v2.83.0 · 4 HR-CHL + 4 AP-CHL enforcés strict · test de suppression appliqué pre-ship documenté section 6.
