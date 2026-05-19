# Changelog

All notable changes to PhantomOS workspace-template canon.

Format · [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning · [SemVer](https://semver.org/spec/v2.0.0.html).
Détails étendus par release · `docs/internal/releases/manifest/{version}-manifest.json`.
Archive narrative Largo · `docs/internal/project-journal.md`.
Doctrine canon · `docs/system/changelog-discipline.md` (v2.83.0+).

## [2.84.3] · 2026-05-20
### Changed
- `docs/internal/canon.md` refonte STRICT voice-doctrine v2.84.1 · 413L → 149L (-64%) · 2ème propagation downstream cadre canon · application reference-grade intégrale (P1-P5 + AP-VD-1à8 + FR/EN + casse + paramétrage + conventions typographiques)
### Added
- NEW section canon `Sens canon du mot 'canon'` · 7 sens MECE documentés (S1 doctrine verrouillée · S2 archétype pédagogique · S3 seuil CMR 95% · S4 formule OTRB · S5 référentiel partagé · S6 copy validée · S7 terminologie normalisée FR) avec marqueurs contextuels et exemples typiques · DÉSAMBIG-2 confirmé (polysémie documentée, pas rename)
- NEW `docs/internal/refactor/v2.84.3-preflight.md` · pré-flight consolidé 3 sub-agents Haiku parallèle (cartographie sens + cross-refs entrantes 32 + sortantes 39)
### Fixed
- Ref cassée · `docs/system/creative-formula.md` (path drift) → `resources/templates/creative-formula.md`
- Ref cassée · `GETTING_STARTED.md` (fichier absent) retirée et pointée vers `docs/README.md`
### Notes
- Audit ancres runtime · zéro skill runtime ne référence directement `docs/internal/canon.md` (5 skills + phantom slash-command pointent vers d'autres `*-canon.md` distincts) · seule ancre formelle préservée `§ Atlas brand` (référencée depuis `atlas-brand.md:78`)
- D#453 captured · NEW memory canon `canon_md_strict_canon`
- Backlog DÉSAMBIG-1.5 noté · rename ciblé S4 dominant ~1066 occurrences si polysémie insuffisante à l'usage (sprint dédié 8-12h post-distribution)

## [2.84.2] · 2026-05-20
### Changed
- `lexicon.md` user-facing refonte · 175L → 103L (-41%) · 1ère propagation downstream voice-doctrine v2.84.1 · application partielle scope (b) · FR/EN canon (opérateur, décomposition, etc) · AP-VD-4 adjectifs vagues retirés · AP-VD-6 zéro nom doctrine canon leaké · P1 précision dense · P3 phrases courtes · em-dash zéro · `vous`/`votre marque` registre opérateur préservés
### Removed
- DRGFP + Confidence propagation + Atlas 4 senses MECE + Lineage + Origin_axis + Schwartz entrées (jargon doctrinal surface opérateur ou specs internes R&D)
- Preamble CONTEXT/OBJECTIVE/TYPE/AUDIENCE/CANON INTERNE (overengineered) · footer narrative S53/S55 (versioning inline)
- Refs `docs/system/*-discipline.md` doctrines internes 6× (violations AP-VD-6)
### Notes
- 25 entrées core préservées (Brand, Produit, Offre, Audience, Persona, Pain point, Tension, Insight, JTBD, Angle, Axe créatif, Concept/Creative/Variant, Mécanique/Mechanism, Awareness, Atome irréductible, Landing page, Campagne, Test, Résultat, Apprentissage, Positioning, Territoire, Connected source)
- D#452 captured · cadre canon voice-doctrine v2.84.1 testé via propagation réelle

## [2.84.1] · 2026-05-19
### Changed
- `voice-doctrine.md` v2.84.0 → v2.84.1 · 5 patches post-audit Claude Web · NEW mini-section Registres canon (3 registres reference-grade · semi-public · runtime opérateur) · NEW section Conventions typographiques (séparateurs canon `·` `\|` `→` `↔` · em-dash interdit) · notes (rename pending v2.85.0+) cross-refs `*-discipline.md` · notes transparence P4 spécialise P1 + AP-VD-1/2/7 applications négatives · AP-VD-3 précision distinction AP-VD-8 · 150L pile sous cap claude-md-discipline 150
### Notes
- 21 fichiers `*-discipline.md` identifiés à renommer `*-doctrine.md` · sprint v2.85.0 dédié (cross-refs sibling + CLAUDE.md root + manifest skills)
- Rejet drift audit · frontmatter `***` était hallucination · file utilise déjà `---` YAML standard

## [2.84.0] · 2026-05-19
### Added
- NEW doctrine `voice-doctrine.md` · ton canon artefacts internes · 5 principes wording (P1-P5) · politique FR/EN canon (opérateur · décomposition · cartographie · territoire · doctrine vs discipline) · conventions casse (NOYAU/CONTEXTE/MODIFIEURS · NIVEAU 0/1-4/LIVE plafond 5-10) · famille paramétrage NEW (axe variable · paramétrage · paramétrer · pair canon cartographier ↔ paramétrer) · 8 anti-patterns (AP-VD-1 à AP-VD-8) · exception README/WELCOME semi-public
### Changed
- `docs/system/README.md` index · ajout `voice-doctrine` en Authoring infrastructure · `claude-md-discipline` + `changelog-discipline` listés (rattrapage) · count 24 → 27 doctrines
### Migration
- Aucune (cadre canon posé · pas de propagation lexicon/canon/doctrines existantes dans ce sprint · réécritures dédiées v2.84.x+)

## [2.83.0] · 2026-05-19
### Added
- NEW doctrine `changelog-discipline.md` (cap 80L par release) · NEW `docs/internal/project-journal.md` (4270L préservés narrative archive)
### Changed
- `CHANGELOG.md` racine Keep-a-Changelog strict · `/version` + `/update` lisent CHANGELOG.md + manifests JSON
### Migration
- Ancien `CHANGELOG.md` 4270L → `docs/internal/project-journal.md`

## [2.82.1] · 2026-05-19
### Fixed
- Validation post-refactor v2.82.0 · zéro régression silencieuse · backward compat sémantique additive

## [2.82.0] · 2026-05-19
### Changed
- CLAUDE.md root refactor atomique 332L → 144L (-57%) · NEW doctrine `claude-md-discipline.md` · NEW index `docs/system/README.md`

## [2.81.1] · 2026-05-19
### Added
- NIVEAU LIVE thinking aloud (DVD extension) · 7 skills consumers patched

## [2.81.0] · 2026-05-18
### Added
- NEW doctrine `entry-arc-discipline.md` (4 portes MECE) · NEW skill `import-archive` · NEW M5b first deliverable

## [2.80.3] · 2026-05-18
### Changed
- /tour arc substance guidé (5 volets) · /about ton premium · HR-OHD-10 NEW

## [2.80.1] · 2026-05-18
### Changed
- /tour prose conversationnelle native (zero ASCII interface) · HR-OHD-9 NEW

## [2.80.0] · 2026-05-18
### Added
- NEW slash commands `/update` + `/version` · NEW doctrine `update-distribution-discipline.md` · NEW migrations framework · GitHub Releases tags v2.65 → v2.79.5

## [2.79.5] · 2026-05-18
### Added
- NIVEAU 0 paramètres décomposés canon (DVD + EDD extensions) · 6 skills patched

## [2.79.4] · 2026-05-17
### Added
- NEW slash command `/about` · NEW doctrine `pain-benefit-chain.md` · /tour intro Vercel/GitHub-style

## [2.79.3] · 2026-05-17
### Added
- NEW doctrines `onboarding-holistic-discipline.md` + `engagement-disclosure-discipline.md` · /tour panorama 7 territoires · 6 orchestrators disclosure

## [2.79.2] · 2026-05-17
### Added
- NEW doctrine `output-clarity-discipline.md` · /phantom + /bird + /breakdown refactor

## [2.79.1] · 2026-05-17
### Added
- NEW doctrine `decomposition-visibility-discipline.md` (4 NIVEAUX matricial) · 4 skills patched

## [2.79.0] · 2026-05-17
### Added
- 3 NEW skills brand strategy (positioning-canvas · brand-voice · voice-consistency) · 6 Mark+Pearson archetypes

## [2.78.0] · 2026-05-17
### Added
- 5 NEW skills ops paid · 3 NEW doctrines (pacing · creative-testing · attribution-multitouch) · magic keyword cleanup 64 substitutions

## [2.77.0] · 2026-05-17
### Added
- NEW doctrine `skill-routing-discipline.md` · NEW slash commands `/scope` + `/bird` · 697 em-dashes purgés

## [2.76.0] · 2026-05-16
### Changed
- /tour refactor pro-grade 10 patches (institutional voice + smart suggestions + dejargonisation)

## [2.75.1] · 2026-05-16
### Changed
- /tour Milestone 6 enriched (5 universal entry points + 3 canon principles)

## [2.75.0] · 2026-05-16
### Added
- NEW doctrine `extension-discovery-discipline.md` · 4 orchestrators extension_hooks

## [2.74.1] · 2026-05-16
### Fixed
- Cleanup parasites (doublons Stepprs · refs canon paths · 255 em-dashes éliminés)

## [2.74.0] · 2026-05-16
### Added
- NEW slash command `/lexicon` (13 magic keywords canon) · decompose-ad FIT AVEC TA BRAND

## [2.73.0] · 2026-05-16
### Added
- NEW skill `adapt-from-competitor` · decompose-ad v2.0.0 grille ANATOMIE 3 niveaux

## [2.72.1] · 2026-05-16
### Fixed
- /tour Milestone 6 ligne 208 · 3 cohérence corrections

## [2.72.0] · 2026-05-16
### Added
- NEW skill `produce-decomposition-ecr` · ECR runtime methodology · anti-hallucination canon `_EXAMPLE/`

## [2.71.1] · 2026-05-16
### Added
- breakdown.md topics 11 intelligence + 12 apprentissage (transverse dimensions)

## [2.71.0] · 2026-05-16
### Added
- NEW doctrine mère `operational-system-discipline.md` (ECR × Rules × Templates × Metrics × Rituals)

## [2.70.0] · 2026-05-16
### Added
- NEW slash command `/breakdown stepprs {topic}` (vitrine pédagogique · 7 topics)

## [2.69.1] · 2026-05-16
### Changed
- _EXAMPLE/stepprs UX live patch (3 layers · 9 frictions captured)

## [2.69.0] · 2026-05-16
### Added
- NEW skill `trendtrack-enrich-brand` (Market Intelligence Layer first runtime brick)

## [2.68.0] · 2026-05-15
### Added
- NEW doctrine `progressive-cartography-discipline.md` (4 phases · hypothesis confidence 0.5 valid)

## [2.67.0] · 2026-05-15
### Added
- NEW doctrine `territory-discipline.md` · layer field 67 skills

## [2.66.0] · 2026-05-15
### Breaking
- sync-notion-atlas v1.x → v2.0.0 dual-direction sync (Phase B push runtime exec-ready)

## [2.65.0] · 2026-05-15
### Added
- NEW doctrine `scope-extension-discipline.md` (canon élasticité opérateur)

Release tags · `https://github.com/Largo2z9/phantomos/releases/tag/v{version}`.
