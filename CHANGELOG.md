# Changelog

All notable changes to PhantomOS workspace-template canon.

Format · [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning · [SemVer](https://semver.org/spec/v2.0.0.html).
Détails étendus par release · `docs/internal/releases/manifest/{version}-manifest.json`.
Archive narrative Largo · `docs/internal/project-journal.md`.
Doctrine canon · `docs/system/changelog-doctrine.md` (v2.83.0+).

## [2.87.0] · 2026-05-20
### Changed
- **SIMPLIFICATION ONBOARDING + COHÉRENCE CROSS-SURFACES** · tour.md v2.81.0 → v2.87.0 · architecture 4 milestones canoniques + close réflexif réutilisé partout
- `.claude/commands/tour.md` · 686L → 284L (**-59%**) · M1 splitter 4 portes + M2 first deliverable encadré (remonté position 2 court-circuite tunnel) + M3 close réflexif universel (slugs `volet:{nom}` · `drill:{territoire}` · `exit:setup` · `pivot:{volet}` · `build-skill:{territoire}`) + M4 replay évolutif
- `operator/awareness.json` · schema v1.0 → v1.1 · 5 fields NEW (`tour_entry_door` · `paths_skipped` · `first_deliverable_built` · `first_deliverable_skill` · `first_deliverable_validated_corrections`) + 1 type fix (`first_skill_built` false → null)
- NEW `operations/migrations/v2.87.0-awareness-schema-fields.py` · migration idempotent · backup horodaté · re-run safe (pattern miroir v2.42/v2.63/v2.64)
- `WELCOME.md` 15L → 17L · phrase canon v4 EN en tête + flow réécrit pour matcher architecture v2.87
- `README.md` 67L → 69L · phrase canon v4 EN exacte en tête section description + restructure progression
- `lexicon.md` 103L → 119L · 4 entrées NEW prepend avant Brand (`Workspace agentic` · `Skill` · `Porte d'entrée` · `Slug`)
### Notes
- **3 décisions Phase 1 tranchées Largo orchestrateur** ·
  1. Architecture 4 milestones validée (avec 2 caveats préservation arc substance Porte A via slugs M3 close)
  2. Matrice défauts deliverable par porte M2 validée (A=Stepprs pédagogique · B=brand opérateur · C=post-import · D=scan signaux)
  3. Phrase canon v4 validée (micro-ajustement `l'agent y raisonne et exécute`)
- **Phrase canon v4 littéralement identique cross 3 surfaces premier contact** (README L3 EN · WELCOME L3 EN · tour.md M1 FR+EN · lexicon entrée Workspace agentic)
- **Préservations 8/8 confirmées** · canons Vincent runtime + détection live registre + bypass URL pasted + awareness writes structurés + failure modes 3 cas + HR-OHD-2 zéro typage profil métier + prose conversationnelle native + politique FR/EN voice-doctrine v2.84.1 + ton premium zéro concurrent nommé
- Tests non-régression PASSÉS · build-manifest 81 skills + 92 jargon · build-brand-snapshot _EXAMPLE 24 lines · grep em-dash 0 cross 4 surfaces · migration script idempotent confirmé (workspace clean + legacy v1.0 → v1.1)
- **Phase 5 test runtime ISOLÉE v2.87.0bis** · discipline honnêteté gate distribution non négociable fatigué · pattern miroir isolations précédentes (v2.85.1bis · v2.85.4 brand-isolation REPORT v2.85.5 · v2.85.3 effort 3)
- D#466 captured · D#467 réservé v2.87.0bis · NEW memory canon `onboarding_simplified_v287` (architecture 4 milestones + phrase canon v4 + matrice défauts par porte)
- Backlog · v2.87.0bis test runtime workspace fresh phantom-test-v287 · distribution preparation (GitHub Releases + liste opérateurs + message invitation)

## [2.86.0] · 2026-05-20
### Changed
- **AUDIT CROSS-FILES FINAL** post-clôture chantier propagation contenu v2.85.5
- **~56 patches résiduels Discipline → Doctrine cross-files** · `docs/system/README.md` catalogue listings (~25) + `claude-md-doctrine.md` propagation oubli (9) + `changelog-doctrine.md` propagation oubli (3) + `compositional-cartography.md` titre oubli lot 1 corrigé (5) + 6 doctrines body cross-refs descriptors + `voice.md` ligne 104 catalogue + `canon.md` interne descriptors + `provenance-trust-discipline-scope.md` titre + footer + `doctrine-governance.md` table header + exemples futures doctrines
### Notes
- **3 décisions tranchées v2.86.0** ·
  1. **synthesis** · Option A · CONSERVÉ EN unified (48 occurrences architectural concept CMR/CI primitif · 0 patch)
  2. **Notion/Airtable mention operational-system §1** · CONSERVÉE (tableau Différenciation structurelle comparative · registre GitHub/Vercel autorisé · refactor structurel hors scope)
  3. **26ème doctrine périphérique** · 3 doctrines non-propagées réellement identifiées (claude-md + changelog · notion-bridge déjà conforme) + 1 oubli lot 1 (compositional-cartography titre) · TOUTES traitées v2.86.0
- Tests non-régression PASSÉS · build-manifest 81 skills + 92 jargon · build-brand-snapshot _EXAMPLE 24 lines · grep Discipline résiduel 0 (sauf 2 voice-doctrine descriptifs convention historique + 1 em-dash documentation interdiction · tous légitimes)
- **État chantier propagation contenu post-v2.86.0** · 27/28 doctrines cohérentes · ~203 patches cumulés cross chantier complete · 18 sprints v2.84.0 → v2.86.0 · 0 régression runtime cumulée
- D#465 captured · memory canon `doctrine_propagation_complete` enrichi audit final
- Backlog · v2.86.1 validation runtime 5 scénarios (GATE distribution) · v2.86.2 test discovery externe · distribution préparation

## [2.85.5] · 2026-05-20
### Changed
- **CLÔTURE chantier propagation contenu voice-doctrine v2.84.1** · `brand-isolation-doctrine.md` propagée (68L · 1 patch principal titre `Brand isolation discipline` → `Brand Isolation Doctrine` cohérence post-rename + capitalisation canon)
- **25/26 doctrines propagées cumulé** lots 1+2+3+4+5 · 1 doctrine restante périphérique chantier (notion-bridge OR doctrine-governance · backlog v2.86.x si nécessaire)
### Notes
- Sprint court 20-30 min wall-time · application STRICT cohérente lots 1-4 (Phase 1 lecture intégrale + Phase 2 édition critique + self-conformance + Phase 3 gate hygiène + Phase 4 ship)
- Tests non-régression PASSÉS · build-manifest 81 skills + 92 jargon · build-brand-snapshot _EXAMPLE 24 lines · grep em-dash 0 · grep Discipline résiduel 0
- **BILAN CHANTIER PROPAGATION CONTENU v2.84.1 → v2.85.5** ·
  - 17 sprints cumulés (1 doctrine NEW v2.84.0 + 3 propagations cross-files v2.84.1-v2.84.4 + 5 sprints rename v2.85.0.x + 5 sprints propagation contenu v2.85.1-v2.85.5)
  - 25/26 doctrines propagées
  - 147 patches cumulés cross 25 doctrines
  - 8094L total stable (2102+1457+2121+2346+68)
  - 0-1% compression structurelle cumulée (préservation stricte tenue 5 sprints)
  - 0 régression runtime cumulée
  - **Hypothèse VALIDÉE 5 lots consécutifs** · voice-doctrine propagée par ricochet plus largement qu'estimé · 3 vecteurs validés (doctrines créées sous discipline canon en amont + trilogie propagations v2.84.2-v2.84.4 + chantier rename v2.85.0.x)
- **Patterns systémiques identifiés** cross 5 lots ·
  - Discipline → Doctrine cohérence post-rename (115 patches cumulés)
  - Operational System cross-ref harmonisation systémique (cross 9-10 doctrines référençantes)
  - Generic discipline → doctrine systémique (meta-discipline · sub-discipline · etc.)
  - Cross-refs cassées avec dates obsolètes `-2026-04-26.md` corrigées
  - Anglicismes prose isolés patchés (skipée/négligée · explicit/explicite · capped/limitée · signaled/signalé · collapse/effondrent · operator/opérateur)
- **Garde-fous canons codifiés en memory canons** · cap 500L par doctrine (v2.85.1bis) · Phase 2.A lecture intégrale obligatoire (v2.85.1bis) · self-conformance Phase 2.C (v2.85.1bis) · scope strict voice-doctrine (Largo politique) · filter Haiku scoring main thread Sonnet (v2.85.3) · spot-check cross-refs entrantes producer central (v2.85.4)
- **Politique FR/EN consolidée canon** validée 5 lots · acronymes industrie EN + creative/operator/campaign FR + platform-specific EN + termes canon PhantomOS EN (canonical/load-bearing/Operator-facing)
- D#464 captured · NEW memory canon `doctrine_propagation_complete` (clôture officielle chantier) · memory canon `doctrine_propagation_progress` finalisé 25/26
- Backlog · v2.86.0 audit cross-files final + résolution synthesis (48 occurrences cumul) + Notion/Airtable mention operational-system §1 + 1 doctrine restante évaluation propagation

## [2.85.4] · 2026-05-20
### Changed
- **PROPAGATION VOICE-DOCTRINE LOT 4/4** · 6 doctrines opérationnelles éditées critique main thread Sonnet · `operational-system-doctrine` · `attribution-multitouch-doctrine` · `skill-routing-doctrine` · `engagement-disclosure-doctrine` · `onboarding-holistic-doctrine` · `update-distribution-doctrine`
- 2346L → 2346L (0% compression structurelle · scope strict voice-doctrine respecté · 4 lots consécutifs validés)
- 40 patches cumulés · 5 titres Discipline → Doctrine + body occurrences (Skill Routing · Engagement Disclosure · Onboarding Holistic · Update Distribution · Attribution Multitouch + 1 dans operational-system pour Operational System Discipline auto-référence) + 5 cross-refs `Operational System Discipline v2.71` → `système opérationnel (operational-system-doctrine.md)` harmonisées systémique + 1 frontmatter `update-distribution-discipline` → `-doctrine` + 4 cross-refs cassées corrigées dans operational-system (`audiences-cartography-doctrine.md` plural typo → `audience-cartography-doctrine.md` singular + `pain-benefit-chain-doctrine.md` inexistant → `pain-benefit-chain.md`)
### Notes
- Pré-flight Phase 1 · 1 sub-agent Haiku · 7 candidates inventoriées · filter main thread Sonnet · 0 doctrine effort 3 réel · cap 500L respecté (max 473L update-distribution · marge 27L)
- **Décision pré-flight** · brand-isolation-doctrine REPORTÉE v2.85.5 sprint court (68L · 1 patch principal · ~20-30 min) · cap strict 6 doctrines maintenu lot 4
- **Hypothèse VALIDÉE 4 lots consécutifs** · doctrines opérationnelles aussi conformes que doctrines racines (lot 1) + audience/creative (lot 2) + structurantes (lot 3). Pattern voice-doctrine propagation par ricochet confirmé sur cycle complet
- **Pattern systémique NEW lot 4** · `Operational System Discipline v2.71` → `système opérationnel (operational-system-doctrine.md)` harmonisé cross 5 doctrines référencantes (skill-routing · engagement-disclosure · onboarding-holistic + déjà patché lots 1+2 sur OCD + pacing)
- **Pattern cross-ref cassées corrigées** · operational-system-doctrine référençait 2 fichiers inexistants/typos (`audiences-cartography-doctrine.md` plural + `pain-benefit-chain-doctrine.md` non-existing) · corrigés cohérence cross-rename systémique
- Tests non-régression PASSÉS · build-manifest 81 skills + 92 jargon · build-brand-snapshot _EXAMPLE 24 lines · grep em-dash 0 cross 6 doctrines · grep Discipline résiduel 0
- **Spot-check operational-system cross-refs entrantes** · TOUS valides post-édition (CI ligne 146 · pacing 191/268/281/288 · OCD 375 → `operational-system-doctrine.md`) · cohérence cascade canonical préservée · scope strict respect règles canon 5 couches confirmé
- Monitor `synthesis` lot 4 · 2 occurrences (engagement-disclosure 2) · cumul lots 1+2+3+4 = 48 occurrences pour v2.86.0 audit cross-files résolution unifiée
- D#463 captured · memory canon `doctrine_propagation_progress` mis à jour (compteur 4/4 lots traités · 24/26 doctrines propagated · brand-isolation PENDING v2.85.5)
- Backlog · v2.85.5 sprint court brand-isolation (CLÔTURE 25/26 atteint) · v2.86.0 audit cross-files final + synthesis résolution + Notion/Airtable mention operational-system

## [2.85.3] · 2026-05-20
### Changed
- **PROPAGATION VOICE-DOCTRINE LOT 3/4** · 6 doctrines authoring + schema éditées critique main thread Sonnet · `skill-authoring-doctrine` · `schema-encoding-doctrine` · `extension-discovery-doctrine` · `scope-extension-doctrine` · `territory-doctrine` · `entry-arc-doctrine`
- 2121L → 2121L (0% compression structurelle · scope strict voice-doctrine respecté · patches mécaniques substitution/cohérence uniquement)
- 55 patches cumulés · 5 titres `Discipline → Doctrine` (preserve acronymes SAD/SED/SED-X) + 28 occurrences body Discipline → Doctrine cohérence post-rename + 4 cross-refs obsolètes avec dates retirées (`canonical-matrix-reasoning-2026-04-26.md` → sans date) + 4 cross-refs `Operational System Discipline v2.71` → `système opérationnel (operational-system-doctrine.md)` harmonisées + 5 patches generic `discipline → doctrine` (meta-discipline · sub-discipline · "an authoring discipline" · "single discipline that governs" · "another discipline") + 1 frontmatter `name: entry-arc-discipline → entry-arc-doctrine` + 1 cross-ref `onboarding-holistic-discipline → onboarding-holistic-doctrine` (4 occurrences replace_all)
### Notes
- Pré-flight Phase 1 · 1 sub-agent Haiku · 6 doctrines inventoriées · effort Haiku 2/2/2/2/3/3 · main thread filtre scoring · effort réel scope strict voice-doctrine = 2/6 (0 doctrine effort 3 réel · narratif structurel + termes canon "canonical"/"load-bearing" hors scope)
- Garde-fous PASSED · cap 500L respecté (max 458L entry-arc · marge 42L) · 0 isolation v2.85.3bis nécessaire
- **Hypothèse VALIDÉE 3 lots consécutifs** · doctrines structurantes (authoring + schema) aussi conformes que racines (lot 1) et audience + creative (lot 2). Voice-doctrine propagée par ricochet plus largement qu'estimé · violations majoritairement cosmétiques cohérence post-rename
- **Pattern systémique identifié** · 5 doctrines structurantes utilisaient `meta-discipline` / `an authoring discipline` / `parmi les disciplines` / `sub-discipline` génériques · patch cohérence canon `doctrine` systémique
- Tests non-régression PASSÉS · build-manifest 81 skills + 92 jargon · build-brand-snapshot _EXAMPLE 24 lines · grep em-dash 0 cross 6 doctrines · grep `Discipline` résiduel post-Phase 3 fix 0 (1 occurrence extension-discovery ligne 29 manquée Phase 2 fixed Phase 3)
- Monitor `synthesis` lot 3 · 2 occurrences (skill-authoring 1 + territory 1) · cumul lots 1+2+3 = 46 occurrences pour v2.86.0 audit cross-files résolution unifiée
- D#462 captured · memory canon `doctrine_propagation_progress` mis à jour (compteur 18/26 cumul · 3 lots SHIPPED · lot 4 PENDING)
- Backlog · v2.85.4 lot 4/4 opérationnelles · v2.86.0 audit cross-files final + résolution synthesis

## [2.85.2] · 2026-05-20
### Changed
- **PROPAGATION VOICE-DOCTRINE LOT 2/4** · 6 doctrines audience + creative éditées critique main thread Sonnet · `pain-benefit-chain` · `audience-cartography-doctrine` · `progressive-cartography-doctrine` · `creative-testing-doctrine` · `pacing-doctrine` · `visual-identity-doctrine`
- 1457L → 1457L (0% compression structurelle · scope strict voice-doctrine respecté · patches mécaniques substitution/cohérence uniquement)
- 30 patches cumulés · majoritairement `Discipline → Doctrine` cohérence post-rename v2.85.0.x (4 titres + 4 occurrences body) + franglais isolés (`skipée → négligée` · `explicit → explicite` · `capped → limitée` · `signaled → signalé` · `collapse → effondrent` · `operator → opérateur` prose FR) + 1 cross-ref `Operational System Discipline v2.71` → `système opérationnel (operational-system-doctrine.md)` (pacing-doctrine §8)
### Notes
- Pré-flight Phase 1 · 1 sub-agent Haiku · 6 doctrines inventoriées · effort 1 sur 2/6 + effort 2 sur 4/6 · garde-fous tous PASSÉS (cap 500L · max 379L · 0 isolation v2.85.2bis nécessaire)
- **Hypothèse pré-flight PARTIELLEMENT INFIRMÉE** · doctrines audience + creative v2.6x-v2.7x aussi conformes que doctrines récentes lot 1 (0.7-1.4 violations / 100L) · voice-doctrine propagée par ricochet plus largement qu'estimé (création sous discipline canon + trilogie v2.84.2-v2.84.4 + chantier rename v2.85.0.x)
- **Politique FR/EN consolidée** (validation Largo) · acronymes industrie EN préservés (CPM · CPA · ROAS · CTR · etc.) · termes traduits FR (creative→créative usage substantive · operator→opérateur prose FR) · technical platform-specific préservés EN (adset · copy · retargeting · landing page · buyer)
- Tests non-régression PASSÉS · build-manifest 81 skills + 92 jargon · build-brand-snapshot _EXAMPLE 24 lines · grep em-dash 0 cross 6 doctrines · grep `Discipline` résiduel titre interne 0
- D#461 captured · memory canon `doctrine_propagation_progress` mis à jour (compteur 12/26 cumul · lots 3-4 PENDING)
- Anglicisme `synthesis` (~10 occurrences lot 2 + 34 occurrences lot 1 déjà shipped) NON patché · cohérence cross-files prime sur patch unilatéral · question reportée v2.86.0 audit cross-files
- Backlog · v2.85.3 lot 3/4 authoring + schema · v2.85.4 lot 4/4 opérationnelles · v2.86.0 audit cross-files final + question synthesis

## [2.85.1] · 2026-05-20
### Changed
- **PROPAGATION VOICE-DOCTRINE LOT 1/4** · 6 doctrines racines + investigation éditées critique main thread Sonnet · `contextual-intelligence` · `investigation-posture` · `canonical-matrix-reasoning` · `compositional-cartography` · `decomposition-visibility-doctrine` · `output-clarity-doctrine`
- 2102L → 2083L (-1% · préservation stricte sémantique)
- 18 patches sprint initial cumulés · titres `Discipline → Doctrine` (cohérence post-rename v2.85.0.x) · Status DRAFT → SHIPPED canonical-matrix-reasoning · cross-ref `doctrine-governance-2026-04-26.md` corrigée · sections Position 5 couches compressées · bullets/sections narratives compressées
- **Fold v2.85.1bis** · audit honnêteté qualité post-sprint a révélé Phase 2.A lecture critique glissée sur 2/6 doctrines (DVD 668L + OCD 397L lues partiellement initialement) · sprint dédié v2.85.1bis lecture intégrale obligatoire DVD + OCD · 3 patches additionnels cohérence post-rename (DVD ligne 89 cross-ref Operational System Discipline → operational-system-doctrine.md · DVD ligne 295 skills decomposition-visibility-discipline → -doctrine · DVD ligne 527 narratif Decomposition Visibility Discipline → Doctrine)
### Notes
- Pré-flight Phase 1 · 1 sub-agent Haiku · 6 doctrines toutes en effort 1 (mineur) · ~15 violations totales · garde-fous tous PASSÉS
- **Apprentissage canon majeur** · doctrines racines + investigation déjà majoritairement conformes voice-doctrine (créées récemment v2.79.x-v2.82.x sous discipline canon · trilogie v2.84.2-v2.84.4 a aligné vocabulaire transverse · chantier rename v2.85.0.x touchait noms pas contenu) · compression réelle -1% vs briefing -30/-50% · préservation stricte sémantique > forced reduction
- **Apprentissage v2.85.1bis** · pré-flight conformité "majoritairement conforme" N'EST PAS un blanc-seing pour skip Phase 2.A lecture intégrale · NEW garde-fou canon lots 2-4 · cap 500L par doctrine dans un lot · doctrine candidate dépasse 500L → isoler en sprint dédié dès pré-flight (cohérent pattern LITE chantier rename + isolation decomposition-visibility v2.85.0.3a)
- Tests non-régression PASSÉS post v2.85.1bis · build-manifest 81 skills + 92 jargon · build-brand-snapshot _EXAMPLE 24 lines · grep em-dash 0 cross 6 doctrines · grep `*Discipline*` titre interne 0 cross 2 doctrines critiques (DVD + OCD)
- D#460 captured · memory canon `doctrine_propagation_progress` mis à jour (NEW garde-fou cap 500L lots 2-4 · 2/6 doctrines glissées v2.85.1 résolues v2.85.1bis)
- Backlog · v2.85.2 lot 2 audience + creative (doctrines plus anciennes v2.6x-v2.7x · compression réelle attendue plus proche briefing 10-20%)

## [2.85.0.3b] · 2026-05-20
### Changed
- **CLÔTURE CHANTIER RENAME · 21/21 doctrines renommées** · 2 dernières fichiers `*-discipline.md` → `*-doctrine.md` · `engagement-disclosure` · `schema-encoding` · alignment voice-doctrine v2.84.1 politique linguistique FR/EN canon COMPLET
- 147 cross-refs patches batch · 68 fichiers consumers patchés
### Notes
- Pré-flight ciblé Phase 1 · 1 sub-agent Haiku · garde-fous tous PASSÉS (174 cumulé < 250 · max 105 par doctrine < 150)
- Tests non-régression Phase 4 PASSÉS · build-manifest 81 skills · build-brand-snapshot _EXAMPLE 24 lines · grep résiduel 0 occurrence · spot-check 2 skills consumers (import-archive 4 refs · sync-notion-atlas 5 refs) ✓ · vérification 0 fichier `*-discipline.md` restant ✓
- **Bilan chantier rename 5 sprints v2.85.0 → v2.85.0.3b** · 21 doctrines renommées · 926 replacements cumulés (107 + 253 + 258 + 161 + 147) · 0 régression runtime
- D#459 captured · NEW memory canon `doctrine_rename_complete` (clôture officielle) · memory `v85_0_lite_lessons` mis à jour (calibration finale 5 lots)
- Pattern reproductible documenté pour sprints futurs refactor structurel cross-files (pré-flight + garde-fous + script Python batch + tests + spot-check + ship via PR)
- Prochain chantier · v2.85.1 propagation contenu voice-doctrine STRICT (qualitativement différent · pause cognitive obligatoire avant)

## [2.85.0.3a] · 2026-05-20
### Changed
- **Rename lot 4a/4** · isolation `decomposition-visibility-discipline.md` → `decomposition-visibility-doctrine.md` (doctrine la plus consommée du système · 12 skills consumer runtime) · **19/21 doctrines cumulées** renommées
- 161 cross-refs patches batch via script Python · 40 fichiers consumers patchés (12 skills + 5 doctrines sœurs + 4 slash commands + 5 manifests + 4 memory canons + R&D)
### Notes
- Pré-flight Phase 1 a révélé 2 garde-fous DÉPASSÉS sur lot 4 FULL · top doctrine 51.5% > cap 40% · replacements estimés 610 > cap 280 · décision Largo isolation v2.85.0.3a (decomposition-visibility seul) + v2.85.0.3b à venir (engagement-disclosure + schema-encoding)
- Tests non-régression INTENSIFS Phase 4 PASSÉS · build-manifest 81 skills · build-brand-snapshot _EXAMPLE 24 lines · spot-check 3 skills consumers (build-atlas-complete 13 refs · profile-audience 11 · mine-voc 8) tous OK
- 34 occurrences "decomposition-visibility-discipline" sans `.md` préservées en l'état (concept narrative · false positives intentionnels cohérents règle Phase 1.A initiale)
- Ratio observé lot 4a · 1.18:1 (190/161 · cohérent doctrine HIGH risk dense)
- Cumul 4 sprints rename · 19 doctrines · 779 replacements · 0 régressions
- D#458 captured · memory canon `v85_0_lite_lessons` mis à jour (lot 4a données)
- Backlog · v2.85.0.3b clôture chantier (engagement-disclosure + schema-encoding · 21/21 cumulé post-ship)

## [2.85.0.2] · 2026-05-20
### Changed
- **Rename lot 3/4** · 6 fichiers mid-stakes `*-discipline.md` → `*-doctrine.md` · `operational-system` · `onboarding-holistic` · `skill-routing` · `extension-discovery` · `progressive-cartography` · `update-distribution` · **18/21 doctrines cumulées** renommées
- 258 cross-refs patches batch · 85 fichiers consumers patchés
### Notes
- Pré-flight ciblé Phase 1 · 1 sub-agent Haiku · garde-fous PASSÉS (top doctrine 25.4% · replacements estimés 140)
- Tests non-régression Phase 3 PASSÉS · build-manifest 81 skills · build-brand-snapshot _EXAMPLE 24 lines · grep résiduel 0
- Ratio observé lot 3 · 1.05:1 (272/258 · plus dense qu'estimé 1.9:1 · pattern revisité pour lots futurs)
- Cumul 3 lots · 18 doctrines · 618 replacements · 0 régressions
- D#457 captured · memory canon `v85_0_lite_lessons` mis à jour
- Backlog · v2.85.0.3 lot 4/4 HIGH risk 3 doctrines (decomposition-visibility · engagement-disclosure · schema-encoding · validation runtime intensive obligatoire · lendemain matin frais)

## [2.85.0.1] · 2026-05-20
### Changed
- **Rename lot 2/4** · 6 fichiers mid-stakes `*-discipline.md` → `*-doctrine.md` dans `docs/system/` · `claude-md` · `skill-authoring` · `output-clarity` · `scope-extension` · `territory` · `entry-arc` · **12/21 doctrines cumulées** renommées
- 253 cross-refs patches batch via script Python · 75 fichiers consumers patchés (docs system + docs internal + manifests + skills + slash commands + CLAUDE.md root + memory canons + R&D)
### Notes
- Pré-flight ciblé Phase 1 · 1 sub-agent Haiku (~30s) · garde-fous tous PASSÉS (territory share 18% < cap 40% · replacements estimés 200 < cap 250 · false positives prose tolérables)
- Tests non-régression Phase 3 PASSÉS · build-manifest.py 81 skills + 92 jargon entries · build-brand-snapshot.py _EXAMPLE 24 lines · grep résiduel 0 occurrence (Round 1 suffisant)
- Calibration ratio cumulatif/replacements affinée · lot 1 = 2.4:1 (258/107) · lot 2 = 1.9:1 (477/253) · plus dense car mid-stakes runtime + sibling doctrines
- D#456 captured · memory canon `v85_0_lite_lessons` mis à jour
- Backlog · v2.85.0.2 lot 3/4 mid-stakes · v2.85.0.3 lot 4/4 HIGH risk (3 doctrines validation runtime intensive obligatoire · lendemain matin frais)

## [2.85.0] · 2026-05-20
### Changed
- **Rename lot 1/4** · 6 fichiers `*-discipline.md` → `*-doctrine.md` dans `docs/system/` · alignment naming convention voice-doctrine v2.84.1 politique linguistique FR/EN canon · `attribution-multitouch` · `brand-isolation` · `changelog` · `creative-testing` · `pacing` · `visual-identity`
- 107 cross-refs patches batch via script Python · 41 fichiers consumers patchés (docs system + docs internal + manifests + skills + slash commands + memory canons + R&D)
### Notes
- **Stratégie LITE** confirmée post-escalade garde-fous pré-flight Phase 1.A (3 sub-agents Haiku parallèle ont révélé 1066 cross-refs markdown + 170 non-markdown = ~1236 total · 6x estimation briefing 60-200) · scope réduit lot 1/4 (~258 refs cumulées) pour valider pattern · 15 doctrines restantes en lots dédiés v2.85.0.x sessions ultérieures
- Tests non-régression Phase 1.D PASSÉS · build-manifest.py 81 skills + 92 jargon entries · build-brand-snapshot.py _EXAMPLE 24 lines · grep résiduel 0 occurrence anciens noms
- 37 false positives "discipline" en prose préservés (concept doctrinal vivant · pas modifier)
- NEW `docs/internal/refactor/v2.85.0-rename-log.md` · journal sprint détaillé
- D#455 captured · 2 NEW memory canons (`doctrine_naming_canon` règle pérenne · `v85_0_lite_lessons` observations tactiques)
- Backlog v2.85.0.1-3 · 15 doctrines restantes en 3 lots successifs (lot 2 mid-stakes 6 · lot 3 mid-stakes 6 · lot 4 HIGH risk 3 doctrines avec validation runtime intensive)
- v2.85.1 propagation contenu reportée post-rename complet

## [2.84.4] · 2026-05-20
### Changed
- `README.md` · 4 patches mineurs application registre semi-public canon · acronymes DTC (ligne 3) et ROAS (ligne 9) développés à première occurrence · adjectif vague "Full honest audit" → "Detailed audit" (AP-VD-4) · cross-ref `docs/system/README.md` (doctrine interne leak) → `docs/system/extending.md` (cohérent allègement registre semi-public)
- `WELCOME.md` · audit conformity élevée pre-audit · ZÉRO patch structurel (15L très denses · em-dash zéro · acronymes universels · ton narratif allègement permis)
### Notes
- 3ème propagation downstream voice-doctrine v2.84.1 · trilogie de propagations doctrinales complétée (strict canon.md v2.84.3 + partiel lexicon.md v2.84.2 + semi-public README/WELCOME v2.84.4)
- Apprentissage cross-registres · voice-doctrine résiliente sur 3 registres canon distincts · doctrine guide application concrète selon registre cible · cadre canon validé via 3 propagations réelles
- D#454 captured

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
- NEW doctrine `changelog-doctrine.md` (cap 80L par release) · NEW `docs/internal/project-journal.md` (4270L préservés narrative archive)
### Changed
- `CHANGELOG.md` racine Keep-a-Changelog strict · `/version` + `/update` lisent CHANGELOG.md + manifests JSON
### Migration
- Ancien `CHANGELOG.md` 4270L → `docs/internal/project-journal.md`

## [2.82.1] · 2026-05-19
### Fixed
- Validation post-refactor v2.82.0 · zéro régression silencieuse · backward compat sémantique additive

## [2.82.0] · 2026-05-19
### Changed
- CLAUDE.md root refactor atomique 332L → 144L (-57%) · NEW doctrine `claude-md-doctrine.md` · NEW index `docs/system/README.md`

## [2.81.1] · 2026-05-19
### Added
- NIVEAU LIVE thinking aloud (DVD extension) · 7 skills consumers patched

## [2.81.0] · 2026-05-18
### Added
- NEW doctrine `entry-arc-doctrine.md` (4 portes MECE) · NEW skill `import-archive` · NEW M5b first deliverable

## [2.80.3] · 2026-05-18
### Changed
- /tour arc substance guidé (5 volets) · /about ton premium · HR-OHD-10 NEW

## [2.80.1] · 2026-05-18
### Changed
- /tour prose conversationnelle native (zero ASCII interface) · HR-OHD-9 NEW

## [2.80.0] · 2026-05-18
### Added
- NEW slash commands `/update` + `/version` · NEW doctrine `update-distribution-doctrine.md` · NEW migrations framework · GitHub Releases tags v2.65 → v2.79.5

## [2.79.5] · 2026-05-18
### Added
- NIVEAU 0 paramètres décomposés canon (DVD + EDD extensions) · 6 skills patched

## [2.79.4] · 2026-05-17
### Added
- NEW slash command `/about` · NEW doctrine `pain-benefit-chain.md` · /tour intro Vercel/GitHub-style

## [2.79.3] · 2026-05-17
### Added
- NEW doctrines `onboarding-holistic-doctrine.md` + `engagement-disclosure-doctrine.md` · /tour panorama 7 territoires · 6 orchestrators disclosure

## [2.79.2] · 2026-05-17
### Added
- NEW doctrine `output-clarity-doctrine.md` · /phantom + /bird + /breakdown refactor

## [2.79.1] · 2026-05-17
### Added
- NEW doctrine `decomposition-visibility-doctrine.md` (4 NIVEAUX matricial) · 4 skills patched

## [2.79.0] · 2026-05-17
### Added
- 3 NEW skills brand strategy (positioning-canvas · brand-voice · voice-consistency) · 6 Mark+Pearson archetypes

## [2.78.0] · 2026-05-17
### Added
- 5 NEW skills ops paid · 3 NEW doctrines (pacing · creative-testing · attribution-multitouch) · magic keyword cleanup 64 substitutions

## [2.77.0] · 2026-05-17
### Added
- NEW doctrine `skill-routing-doctrine.md` · NEW slash commands `/scope` + `/bird` · 697 em-dashes purgés

## [2.76.0] · 2026-05-16
### Changed
- /tour refactor pro-grade 10 patches (institutional voice + smart suggestions + dejargonisation)

## [2.75.1] · 2026-05-16
### Changed
- /tour Milestone 6 enriched (5 universal entry points + 3 canon principles)

## [2.75.0] · 2026-05-16
### Added
- NEW doctrine `extension-discovery-doctrine.md` · 4 orchestrators extension_hooks

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
- NEW doctrine mère `operational-system-doctrine.md` (ECR × Rules × Templates × Metrics × Rituals)

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
- NEW doctrine `progressive-cartography-doctrine.md` (4 phases · hypothesis confidence 0.5 valid)

## [2.67.0] · 2026-05-15
### Added
- NEW doctrine `territory-doctrine.md` · layer field 67 skills

## [2.66.0] · 2026-05-15
### Breaking
- sync-notion-atlas v1.x → v2.0.0 dual-direction sync (Phase B push runtime exec-ready)

## [2.65.0] · 2026-05-15
### Added
- NEW doctrine `scope-extension-doctrine.md` (canon élasticité opérateur)

Release tags · `https://github.com/Largo2z9/phantomos/releases/tag/v{version}`.
