---
name: update-distribution-doctrine
description: Doctrine canon racine · pattern de mise à jour PhantomOS opérateur-facing. Preserve operator state · migrations versionnées · semver strict · backup + rollback canon.
type: doctrine
version: v2.80.0
status: shipped
---

# Update Distribution Doctrine · Operating Doctrine

> Canonique v2.80.0. Doctrine canon racine qui codifie le pattern de distribution et mise à jour PhantomOS opérateur-facing. L'opérateur reçoit les updates sans friction · preserve son contexte (brands · learnings · operator state · todos · credentials · session-state) · les migrations canon adaptent ses données aux nouvelles structures (BREAKING) sans intervention manuelle. Doctrine sœur de `engagement-disclosure-doctrine.md` v2.79.5 (disclosure pré-update cohérent), `decomposition-visibility-doctrine.md` v2.79.5+ (NIVEAU 0 paramètres update décomposés), `output-clarity-doctrine.md` v2.79.2 (iconographie + headers FR sobres dans rendu update), `territory-doctrine.md` v2.67 (substrate stable vs production runtime · l'update touche le substrate canon, jamais la production opérateur). Ferme le gap *"distribution updates PhantomOS manuelle (clone Largo2z9/phantomos + git pull) sans preserve operator state · sans check version · sans disclosure pré-update · sans migrations canon BREAKING · sans backup automatique · sans rollback path · risque opérateur perd brands à un update manuel · friction adoption forte"* flag systémique Sprint v2.80 post-audit Largo distribution pipeline canon (état actuel manuel · cible scalable jusqu'à 20-50 opérateurs sans friction · niveau pro shipped product).

---

## 1. Thèse fondatrice

> L'opérateur PhantomOS reçoit les updates sans friction. Son contexte (brands · learnings · operator state · todos · credentials · session-state) est preservé strict. Les migrations canon adaptent ses données aux nouvelles structures (BREAKING) sans intervention manuelle. Distribution = produit, pas bricolage.

**Définition canon update distribution** · ensemble des pratiques opérationnelles qui codifient le pipeline de mise à jour PhantomOS opérateur-facing. Pattern canon répond à 5 questions miroir opérateur ·

1. *"Mes brands sont préservées post-update ?"* (preserve operator state · rsync exclude strict)
2. *"Combien d'updates intermédiaires je rate ?"* (semver canon · liste versions intermédiaires explicit)
3. *"Mes données sont migrées automatiquement sur BREAKING ?"* (migrations canon · 4 méthodes idempotentes)
4. *"Je peux revenir en arrière si ça casse ?"* (rollback canon · backup pre-migration toujours préservé)
5. *"Je sais ce qui change avant de lancer ?"* (disclosure pré-update cohérent EDD v2.79.5+)

**Différenciation canon vs distribution alpha bricolée** ·

| Layer | Distribution alpha bricolée (clone + git pull manuel) | PhantomOS canon Update Distribution |
|---|---|---|
| Preserve operator state | absent (rsync écrase brands · operator · credentials) | canon strict (5 chemins exclus rsync update) |
| Check version | absent (opérateur ne sait pas sa version locale) | canon (`_version.json` lu pre-update) |
| Disclosure pré-update | absent (silent post-trigger) | canon (versions intermédiaires + backup + ETA + close binaire) |
| Migrations BREAKING | absent (opérateur fix manuellement) | canon (`migrations/{version}-{description}.py` 4 méthodes idempotentes) |
| Backup pre-migration | absent (perte données irreversible) | canon (`_archive/migrations/pre-{version}-{date}/` toujours préservé) |
| Rollback path | absent (opérateur captif post-update) | canon (slash command `/rollback {version}` toujours dispo) |
| Semver strict | drift permanent (PATCH labelled MINOR · etc) | canon (MAJOR · MINOR · PATCH selon type changement) |
| Changelog publique | absent (opérateur découvre changements en testant) | canon (CHANGELOG.md + GitHub Releases tags) |

Distribution alpha bricolée signale qu'un produit n'est pas terminé. Pipeline canon PhantomOS force la grammaire shipped product. C'est la différence entre dépôt git public (passive) et produit livrable scalable (operable).

Cette doctrine canonise le pattern systémique cross-versions de PhantomOS · scalable jusqu'à N opérateurs sans friction adoption.

---

## 2. Le problème résolu

Sans Update Distribution Doctrine canon ·

1. **Operator state écrasé silent.** Update manuelle (clone Largo2z9/phantomos + `git pull`) ne distingue pas fichiers canon (workspace-template structure) et fichiers opérateur (brands encodés · operator profile · credentials · session-state). Rsync naïf écrase brands. Opérateur perd 20-50h encoding workspace à un update mal exécuté. Risque irreversible.

2. **Asymétrie information version locale vs latest.** Opérateur ne sait pas sa version locale. Ne sait pas combien de versions intermédiaires entre sa version et latest. Ne sait pas si l'update contient BREAKING ou additive. Asymétrie permanente · decision update à l'aveugle.

3. **BREAKING sans migration · opérateur fix manuellement.** v2.63 + v2.64 ont introduit BREAKING (pain_points/objections sub-audience → top-level collections · sémantique pure). Opérateur post-update doit fix manuellement chaque audience pour adapter structure. Coût rework massif. Pattern canon migrations absent.

4. **Pas de backup · perte données irreversible.** Update fail mi-parcours OR migration fail OR opérateur regret update. Pas de backup pre-migration disponible. Données pre-update perdues. Pas de rollback path. Opérateur captif post-update.

5. **Update silencieuse · opérateur ne sait pas ce qui change.** Opérateur lance `git pull` · reçoit 50+ files modifiés · ne sait pas si NEW skill ajoutée OR doctrine refactor OR BREAKING migration nécessaire. Disclosure pré-update absent. Trust cassé.

6. **Version drift · changelog absent.** v2.79.1 patch (enforcement runtime) labelled comme MINOR alors que sémantique PATCH. Opérateur scan releases ne sait pas si v2.79.1 = patch hygiène OR feature majeure. Changelog publique absent · GitHub Releases tags absents. Opérateur découvre changements en testant post-update.

7. **Friction adoption forte · pas scalable.** État actuel pipeline manuel scale mal. 1-2 opérateurs supportés en mode artisanal · 20-50 opérateurs cible impossible sans pipeline canon shipped product. Distribution = goulot d'étranglement croissance.

Update Distribution Doctrine = doctrine canon qui ferme ces 7 gaps via 3 types changements canon + pipeline migrations idempotentes + semver strict + preserve operator state + backup + rollback + disclosure pré-update + GitHub Releases tags + changelog publique.

---

## 3. Pattern preserve operator state · rsync exclude strict

Tout fichier qui appartient à l'opérateur EXCLU du rsync update. Tout fichier canon (workspace-template structure) INCLUS dans rsync update. Pattern strict cross-versions.

**Chemins canon EXCLUS du rsync update** (operator state preserved) ·

| Chemin | Contenu opérateur | Raison exclusion |
|---|---|---|
| `brands/` | Marques encodées (sauf `_EXAMPLE/` canon pédagogique) | Travail opérateur · 20-50h encoding · perte irreversible |
| `operator/` | Profile · awareness · session-state · preferences · register | Identité opérateur · langue · register · prior knowledge state |
| `.phantom/` | Config locale runtime | Préférences agent · disclosure_preference · environment |
| `.workflow.json` | Workflow runtime config | État runtime entre sessions |
| `credentials.env` + `credentials_shared.env` | Tokens APIs (Meta · Google · Shopify · Klaviyo · GA4) | Credentials opérateur · jamais shipped canon |

**Chemins canon INCLUS dans rsync update** (canon refreshed) ·

| Chemin | Contenu canon | Update behavior |
|---|---|---|
| `docs/` | Doctrine canon · architecture · system docs | Refreshed cross-versions · NEW doctrines auto-shipped |
| `resources/` | Catalogues · routing · frameworks · SOPs · quality-specs · conventions · templates | Refreshed cross-versions · NEW resources auto-shipped |
| `.skills/` | Skills SKILL.md · manifest · scripts · learnings | Refreshed cross-versions · NEW skills auto-shipped |
| `.claude/commands/` | Slash commands templates | Refreshed cross-versions · NEW commands auto-shipped |
| `brands/_EXAMPLE/` | Cas pédagogique canonique Stepprs | Refreshed cross-versions · enrichi pédagogique |
| `lexicon.md` · `index.json` · `index.schema.json` · `_version.json` | Canon racine | Refreshed cross-versions · version bump |
| `README.md` · `WELCOME.md` · `CHANGELOG.md` · `CLAUDE.md` · `CONTRIBUTING.md` · `LICENSE` · `CODE_OF_CONDUCT.md` · `Makefile` | Doc projet | Refreshed cross-versions |

**Pattern canon binaire** · si fichier dans liste EXCLUSE → preserved strict. Si fichier dans liste INCLUSE → refreshed canon. Pas de zone grise. Pas de heuristique floue.

---

## 4. 3 types de changements canon

Tout changement canon classifié dans 3 types orthogonaux mesurables · `additive` · `transform` · `deprecate`. Type drive migration requirement, backward compat, et disclosure pre-update.

### Type 1 · ADDITIVE

Ajout NEW (skill · doctrine · slash command · field optionnel · resource template). Backward compat strict additif. Aucune migration nécessaire. Skill/doctrine devient disponible post-update. Opérateur peut l'utiliser OR l'ignorer.

**Exemples canon historiques** ·

- v2.65 NEW doctrine `scope-extension-doctrine.md` (additive · doctrine devient consommable)
- v2.69 NEW skill `trendtrack-enrich-brand` (additive · skill devient invokable)
- v2.70 NEW slash command `/breakdown stepprs` (additive · command devient triggerable)
- v2.75 NEW doctrine `extension-discovery-doctrine.md` (additive · pipeline NEW entities)
- v2.79.4 NEW slash command `/about` (additive · documentation deep PhantomOS)

**Backward compat** · strict. Code existant opérateur fonctionne identique pré-update et post-update. NEW entities consommables si opérateur les invoque · invisibles sinon.

### Type 2 · TRANSFORM

Réorganisation structure existante (e.g. v2.63 BREAKING `pain_points` sub-audience → top-level collections · sémantique pure). Migration script auto requis. Idempotent strict. Backup pre-migration obligatoire.

**Exemples canon historiques** ·

- v2.63 BREAKING `pain_points` + `objections` collections top-level (sémantique pure)
- v2.64 BREAKING `friction` sub-product field (sémantique pure)
- v2.66 BREAKING `sync-notion-atlas` dual-direction sync (Phase B push runtime exec-ready)

**Backward compat** · BREAKING. Code opérateur existant cassé si pas de migration. Migration script auto rétablit cohérence. Sans migration · workspace opérateur invalidé.

### Type 3 · DEPRECATE

Retrait skill/doctrine/field. Données préservées `_archive/legacy/` dans workspace opérateur. Skill marqué `deprecated: true` dans manifest. Notify opérateur explicit via disclosure pré-update.

**Pattern canon** ·

- Skill deprecated → frontmatter `deprecated: true` + `superseded_by: {skill_name}` + `deprecation_version: v{X.Y.Z}`
- Doctrine deprecated → header `[SUPERSEDED v{X.Y.Z}]` + redirection vers doctrine successor
- Field deprecated → migration archive `{entity}.legacy.json` dans brand workspace

**Backward compat** · graceful degradation. Code opérateur référençant deprecated fonctionne avec warning · pas crash. Pattern canon append-only · `decisions.md` style.

---

## 5. Semver canon strict

Versioning canon respecte semver strict (MAJOR.MINOR.PATCH) avec sémantique canon explicit · pas drift cross-versions.

### MAJOR · X.0.0

TRANSFORM significatif OR NEW slash command racine OR NEW concept canon racine. Type changement = TRANSFORM forcé OR ADDITIVE structurel.

**Exemples canon historiques** ·

- v2.0 (premier release canon)
- v2.80 (NEW doctrine racine update-distribution-doctrine + NEW slash commands /update + /version)

**Migration requirement** · obligatoire (TRANSFORM) OR shipped scaffold (ADDITIVE structurel).

### MINOR · X.Y.0

NEW skill · NEW doctrine canon · NEW feature additive. Type changement = ADDITIVE.

**Exemples canon historiques** ·

- v2.65 NEW doctrine scope-extension-discipline
- v2.67 NEW doctrine territory-discipline
- v2.68 NEW doctrine progressive-cartography-discipline
- v2.69 NEW skill trendtrack-enrich-brand + NEW slash command /breakdown
- v2.71 NEW doctrine mère operational-system-discipline (5 couches)
- v2.75 NEW doctrine extension-discovery-discipline
- v2.79 NEW Decomposition Visibility Doctrine + brand strategy frameworks

**Migration requirement** · aucune (ADDITIVE strict).

### PATCH · X.Y.Z

Hygiène · fix · enrichissement skill existing. Type changement = ADDITIVE micro OR TRANSFORM mineur backward-compat.

**Exemples canon historiques** ·

- v2.79.1 patch enforcement runtime DVD cross-slash commands (NEW HR-DVD-9)
- v2.79.2 patch hygiène + NEW doctrine output-clarity-discipline (release groupée MINOR sémantique mais labelled PATCH par convention release prior)
- v2.79.3 patch onboarding agnostique + engagement disclosure (release groupée MINOR sémantique)
- v2.79.4 patch refonte intro /tour + NEW slash command /about
- v2.79.5 patch intelligence compositionnelle pré-exécution

**Migration requirement** · aucune (PATCH strict).

**Pattern canon réservé** · si PATCH ship NEW doctrine canon racine (e.g. v2.79.2 ship output-clarity-discipline) · drift sémantique signal. Pattern correctif v2.80+ · doctrine canon racine = MINOR strict · PATCH = hygiène + enrichissement uniquement.

---

## 6. Pipeline migration canon

Migration script Python obligatoire par release contenant TRANSFORM. Pattern canon strict cross-migrations · idempotent + backup + rollback.

**Localisation canon** · `migrations/{version}-{description}.py`

**Exemples canon** ·

- `migrations/2.63-pain-objections-top-level.py`
- `migrations/2.64-friction-sub-product.py`
- `migrations/2.66-sync-notion-dual-direction.py`

**Schéma canon · 4 méthodes obligatoires** ·

```python
def check_required(workspace_path: str) -> dict:
    """Vérifie pre-conditions migration. Returns dict avec status + missing items."""
    pass

def run_transformation(workspace_path: str, backup_path: str) -> dict:
    """Exécute la migration. Backup pre-migration créé avant transformation. Returns dict avec status + items migrated + items skipped."""
    pass

def validate_state(workspace_path: str) -> dict:
    """Valide post-migration state. Schema check + integrity check. Returns dict avec status + violations."""
    pass

def rollback(workspace_path: str, backup_path: str) -> dict:
    """Restore pre-migration state depuis backup. Idempotent. Returns dict avec status + items restored."""
    pass
```

**Idempotence canon** · migration peut tourner 2x sans casser. Si run_transformation détecte état déjà migré (post-migration state present) · skip sans erreur. Pattern canon strict.

**Backup pre-migration obligatoire** · `_archive/migrations/pre-{version}-{date}/` créé avant transformation. Contenu complet workspace opérateur snapshot pre-update. Toujours préservé · jamais purgé · rollback path canon.

**Validation post-migration** · validate_state() retourne violations si state corrupt. Si violations · trigger rollback() automatique. Pattern canon fail-safe.

---

## 7. Disclosure pré-update canon

Cohérent `engagement-disclosure-doctrine.md` v2.79.5 (HR-EDD-1 5 triggers obligatoires) + NIVEAU 0 paramètres décomposés `decomposition-visibility-doctrine.md` v2.79.5+ (sister doctrine pre-exec).

**Pattern canon disclosure pré-update** · 5 éléments obligatoires ·

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
UPDATE PHANTOMOS · v{X.Y.Z} → v{X'.Y'.Z'}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ÉLÉMENT 1 · Version locale détectée
   Version actuelle · v{X.Y.Z}
   Date dernier update · {YYYY-MM-DD}

ÉLÉMENT 2 · Versions intermédiaires
   N versions entre locale et latest
   ─── v{X.Y.Z+1} · {type} · {description courte}
   ─── v{X.Y.Z+2} · {type} · {description courte}
   ─── ...
   Légende type · ✓ ADDITIVE · ◐ TRANSFORM · ⚠ DEPRECATE

ÉLÉMENT 3 · Migrations canon requises
   N migrations TRANSFORM détectées
   ─── migrations/{version}-{description}.py
   ─── ...
   Backup destination · _archive/migrations/pre-{version}-{date}/

ÉLÉMENT 4 · ETA estimé total
   Rsync canon · ~{X} secondes
   Migrations canon · ~{Y} minutes
   Total · ~{Z} minutes

ÉLÉMENT 5 · Confirmation
   OK · /update confirme
   J'attends · plus tard

Légende · ✓ done · ◐ in progress · ○ pending · ✗ failed · ⚠ attention
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**NIVEAU 0 paramètres décomposés pre-exec** · cohérent DVD v2.79.5+ HR-DVD-10. 6 éléments obligatoires si update contient TRANSFORM ·

1. Brand workspace cible · {slug ou all}
2. Entities cibles · {liste collections impactées}
3. Migrations chain · {ordre canon migrations}
4. Backup strategy · {chemin complet + retention policy}
5. Validation post-migration · {schema check + integrity check}
6. Rollback path · {slash command + ETA rollback}

**Pattern canon close binaire** · `OK /update confirme` · `J'attends plus tard`. Jamais opt-in default silent. Jamais menu 4+ options equal-weight. Cohérent HR-EDD-3.

---

## 8. Rollback canon

Pattern canon path retour si update fail OR opérateur regret update OR migration corruption.

**Backup canon préservé** · `_archive/migrations/pre-{version}-{date}/` toujours préservé post-update. Jamais purgé automatique. Opérateur peut restore à tout moment.

**Slash command canon** · `/rollback {version}` toujours dispo dans workspace opérateur. Pattern canon ·

```
/rollback v{X.Y.Z}
   ↓
Lit backup _archive/migrations/pre-{version}-{date}/
   ↓
Disclosure pré-rollback · cohérent EDD pattern
   ↓
Close binaire confirmation
   ↓
Si OK · restore complet workspace pre-update state
   ↓
Validation post-rollback · schema check + integrity check
   ↓
Update _version.json · revert to pre-update version
```

**Idempotence canon rollback** · `/rollback` peut tourner 2x sans casser. Si state déjà rollback (pre-update state present) · skip sans erreur. Pattern canon strict.

**État post-rollback** · strict identique pre-update. Brands · operator · credentials · session-state restored. Toute commit migration revert. Workspace opérateur identique snapshot pre-update.

---

## 9. GitHub Releases canon

Chaque release ship canon shipped product · pas dépôt git brut. Pattern canon · `_version.json` bump + `CHANGELOG.md` entry + git tag + GitHub Release publique.

**Git tags canon** · format `v{X.Y.Z}` strict. Pas de variantes (v2.79 · v2.79.0 · 2.79.0). Tag pointe commit release exact (`release {X.Y.Z} · v{X.Y.Z} · {date} · {description}`).

**GitHub Release notes canon** · parsé depuis CHANGELOG.md entry par version. Format ·

```markdown
## v{X.Y.Z} · {YYYY-MM-DD} · {sprint type}

**Type** · {MAJOR | MINOR | PATCH}
**Changements** · {N additive · M transform · K deprecate}

### Additive
- NEW skill {name} · {description}
- NEW doctrine {name} · {description}
- NEW slash command /{name} · {description}

### Transform
- BREAKING {description} · migration `migrations/{version}-{description}.py`

### Deprecate
- DEPRECATED {entity} · superseded by {entity_successor}

### Backward compat
- {strict additif | TRANSFORM migration required | DEPRECATE graceful}

### Migration path
- `/update` slash command (canon)
- Backup destination `_archive/migrations/pre-{version}-{date}/`
- Rollback path `/rollback v{X.Y.Z}`
```

**CHANGELOG.md template canon** · single source of truth versions. Parsé par release notes generator. Pattern append-only · jamais purgé.

---

## 10. Anti-patterns canon · 8 violations strict

### AP-UDD-1 · Update écrase brands/ ou operator/ silently

Rsync update naïf inclut `brands/` OR `operator/` dans sync. Opérateur perd encoding workspace 20-50h. Trust cassé irreversible. Pattern canon · 5 chemins canon EXCLUS strict (HR-UDD-1).

### AP-UDD-2 · BREAKING sans migration · opérateur fix manuellement

Release contient TRANSFORM mais pas de migration script shipped. Opérateur post-update doit fix manuellement chaque audience/product/offer pour adapter structure. Coût rework massif. Pattern canon · migrations canon `migrations/{version}-{description}.py` obligatoire BREAKING (HR-UDD-2).

### AP-UDD-3 · Migration tourne 2x · casse l'état

Migration script non-idempotent. Run 2x · état post-migration corrupt. Pattern canon · idempotence strict · check_required() détecte état déjà migré · skip sans erreur (HR-UDD-3).

### AP-UDD-4 · Pas de backup · perte données irreversible

Update fail mi-parcours OR migration fail OR opérateur regret update. Pas de backup pre-migration. Données pre-update perdues. Pattern canon · backup `_archive/migrations/pre-{version}-{date}/` obligatoire (HR-UDD-4).

### AP-UDD-5 · Update silencieuse · opérateur ne sait pas ce qui change

Agent lance update sans disclosure pré-update. Opérateur découvre 50+ files modifiés post-update sans contexte. Trust cassé. Pattern canon · disclosure pré-update cohérent EDD v2.79.5+ (HR-UDD-5).

### AP-UDD-6 · Pas de rollback · opérateur captif post-update

Update mal exécuté OR migration corrompue. Pas de rollback path. Opérateur captif. Pattern canon · slash command `/rollback {version}` toujours dispo + backup préservé (HR-UDD-6).

### AP-UDD-7 · Version drift · PATCH labelled MINOR · etc

Release classification incohérente. v2.79.2 PATCH ship NEW doctrine canon racine (sémantique MINOR strict). Drift permanent confuse opérateurs. Pattern canon · semver strict MAJOR/MINOR/PATCH selon type changement (HR-UDD-7).

### AP-UDD-8 · Changelog absent · opérateur découvre changements en testant

Release shipped sans CHANGELOG.md entry. GitHub Release notes absentes. Opérateur découvre changements en testant post-update. Pattern canon · CHANGELOG.md + GitHub Releases tags + release notes canon obligatoires (HR-UDD-8).

---

## 11. Hard Rules canon (HR-UDD-1 à HR-UDD-8)

### HR-UDD-1 · Tout update PRESERVE operator state

Rsync update EXCLUT strict 5 chemins canon · `brands/` · `operator/` · `.phantom/` · `credentials.env` + `credentials_shared.env` · `.workflow.json`. Routing automatique pipeline update lit liste exclusion canon pre-execution. Violation = bug invalid pattern canon (operator state écrasé).

### HR-UDD-2 · BREAKING change DOIT shipper migration script

Tout release contenant TRANSFORM (BREAKING) DOIT shipper migration script `migrations/{version}-{description}.py` avec 4 méthodes canon (check_required · run_transformation · validate_state · rollback). Pattern canon strict cross-versions. Violation = bug invalid pattern canon (opérateur fix manuellement).

### HR-UDD-3 · Migration script DOIT être idempotent

Migration script peut tourner 2x sans casser. check_required() détecte état déjà migré · skip sans erreur. Pattern canon strict. Violation = bug invalid pattern canon (migration corrompt state si re-run).

### HR-UDD-4 · Backup pre-migration OBLIGATOIRE

Avant toute transformation migration · backup pre-migration canon `_archive/migrations/pre-{version}-{date}/` créé. Snapshot complet workspace opérateur. Jamais purgé automatique. Toujours préservé. Violation = bug invalid pattern canon (perte données irreversible).

### HR-UDD-5 · Disclosure pré-update canon

Disclosure pré-update cohérent `engagement-disclosure-doctrine.md` v2.79.5 (5 éléments obligatoires · Version locale + Versions intermédiaires + Migrations canon requises + ETA estimé total + Confirmation). NIVEAU 0 paramètres décomposés pre-exec cohérent `decomposition-visibility-doctrine.md` v2.79.5+ HR-DVD-10 si update contient TRANSFORM (6 éléments obligatoires). Close binaire explicit. Violation = bug invalid pattern canon (update silencieuse).

### HR-UDD-6 · Rollback path canon

Slash command `/rollback {version}` toujours dispo dans workspace opérateur. Backup `_archive/migrations/pre-{version}-{date}/` toujours préservé. Idempotent. État post-rollback strict identique pre-update. Violation = bug invalid pattern canon (opérateur captif post-update).

### HR-UDD-7 · Semver strict

Versioning canon MAJOR.MINOR.PATCH strict. MAJOR = TRANSFORM significatif OR NEW slash command racine OR NEW concept canon racine. MINOR = NEW skill OR NEW doctrine canon racine OR NEW feature additive. PATCH = hygiène + fix + enrichissement skill existing strict. Si PATCH ship NEW doctrine canon racine · drift sémantique signal (pattern correctif v2.80+ · doctrine canon racine = MINOR strict). Violation = bug invalid pattern canon (version drift).

### HR-UDD-8 · GitHub Releases tags + changelog publique

Chaque release ship `_version.json` bump + `CHANGELOG.md` entry + git tag canon `v{X.Y.Z}` + GitHub Release publique avec release notes parsées CHANGELOG.md. Pattern canon strict. Violation = bug invalid pattern canon (opérateur découvre changements en testant).

---

## 12. Anti-Patterns canon (AP-UDD-1 à AP-UDD-8)

Voir §10 ci-dessus. Pattern miroir HR-UDD-1 à HR-UDD-8 enforcement runtime.

---

## 13. Cross-refs

- `engagement-disclosure-doctrine.md` v2.79.5 · disclosure pré-update cohérent (HR-UDD-5 cross-ref HR-EDD-1 + HR-EDD-2 + HR-EDD-3) · 5 éléments obligatoires · close binaire canon
- `decomposition-visibility-doctrine.md` v2.79.5+ · NIVEAU 0 paramètres update décomposés pre-exec (HR-UDD-5 cross-ref HR-DVD-10) · 6 éléments obligatoires sur update contenant TRANSFORM
- `output-clarity-doctrine.md` v2.79.2 · iconographie unique 5 symboles + headers FR sobres + density modérée respectés dans rendu update (HR-UDD-5 cross-ref HR-OCD-1 + HR-OCD-3 + HR-OCD-7 + HR-OCD-8)
- `territory-doctrine.md` v2.67 · substrate stable vs production runtime · l'update touche le substrate canon (workspace-template structure) jamais la production opérateur (brands encodés · operator state) · cross-ref HR-UDD-1
- `operational-system-doctrine.md` v2.71 · doctrine mère 5 couches · UDD opère Couche 1 (ECR · Encoder · Consommer · Réviser) + Couche 5 (Rituels release canon) · cumulatif canon
- `extension-discovery-doctrine.md` v2.75 · NEW entities ADDITIVE auto-consommées post-update · cohérent UDD type 1 ADDITIVE backward compat strict
- `update-workspace` skill existing · à wirer pipeline canon UDD v2.80
- `migrate-workspace` skill existing · à wirer pipeline canon UDD v2.80
- NEW slash command `/update` (Agent 2 sprint v2.80) · invoke pipeline canon UDD · disclosure + rsync + migrations + validation
- NEW slash command `/version` (Agent 2 sprint v2.80) · lit `_version.json` local · diff vs latest GitHub Releases · output canon
- NEW slash command `/rollback {version}` (à scaffolder sprint v2.80+) · invoke pipeline canon rollback UDD
- `doctrine-governance.md` · amendment process · supersession formalisée
- `CHANGELOG.md` template canon · single source of truth versions parsé par release notes generator

---

## 14. Position dans le système opérationnel

Update Distribution Doctrine est la couche racine DELIVERY canon · permet à PhantomOS de se déployer / updater / migrer professionnellement sans friction opérateur · scalable jusqu'à N opérateurs.

**Couche DELIVERY canon** · UDD opère AVANT runtime workspace opérateur. Pipeline canon · distribution Largo2z9/phantomos (canon source of truth) → update local workspace opérateur (rsync exclude strict) → migrations canon (TRANSFORM) → validation post-update → backup préservé. Cohérent territory-doctrine.md v2.67 (substrate stable vs production runtime).

**Couche AMONT cohérent EDD v2.79.5** · disclosure pré-update canon cohérent engagement-disclosure-doctrine.md sister doctrine. Pattern miroir · EDD couvre AMONT pré-engagement skill (disclosure runtime) · UDD couvre AMONT pré-engagement update (disclosure delivery). Cumulatifs canon · pas redondants.

**Couche RUNTIME cohérent OSD v2.71** · UDD opère Couche 1 (ECR · Encoder canon → Consommer post-update → Réviser via rollback si fail) + Couche 5 (Rituels release canon cadence opérationnelle). Pattern miroir doctrine mère operational-system-doctrine.md v2.71.

**Scalability canon** · pipeline UDD scalable jusqu'à N opérateurs. État actuel manuel (1-2 opérateurs) → état cible canon v2.80 (20-50 opérateurs sans friction). Distribution = produit, pas goulot d'étranglement croissance.

UDD est le GATE distribution canon · couche DELIVERY entre canon source of truth Largo2z9/phantomos et workspace opérateur runtime. Cohérent avec tickets system canon RUNTIME (`brands/{slug}/tickets/` tracking runtime) plus backup canon DELIVERY (`_archive/migrations/pre-{version}-{date}/` tracking delivery). Couches cumulatives multiplicatives · DELIVERY (UDD) + AMONT (EDD) + RUNTIME (tickets) + AVAL (rollback) = pattern engagement opérateur complet cross-versions.

---

## Status

- **Canonique v2.80.0.** Codifie pattern systémique distribution + update PhantomOS opérateur-facing identifié post-audit Largo distribution pipeline canon Sprint v2.80 (état actuel manuel clone Largo2z9/phantomos + git pull · sans preserve operator state · sans check version · sans disclosure pré-update · sans migrations canon BREAKING · sans backup automatique · sans rollback path · cible scalable jusqu'à 20-50 opérateurs sans friction · niveau pro shipped product).
- **Doctrine sœur** · engagement-disclosure-doctrine.md v2.79.5 (disclosure pré-update cohérent · sister doctrine AMONT) · decomposition-visibility-doctrine.md v2.79.5+ (NIVEAU 0 paramètres update décomposés pre-exec) · output-clarity-doctrine.md v2.79.2 (iconographie + headers FR sobres dans rendu update) · territory-doctrine.md v2.67 (substrate stable vs production runtime canon delimitation) · operational-system-doctrine.md v2.71 (doctrine mère 5 couches · UDD opère Couche 1 + 5) · extension-discovery-doctrine.md v2.75 (NEW entities ADDITIVE auto-consommées cohérent type 1).
- **Backward compat** · strict additif. Doctrine NEW n'override aucune existing. Pipeline distribution legacy pre-v2.80 (clone manuel) toléré jusqu'à patch · v2.80+ migration progressive enforce pipeline canon UDD via NEW slash commands `/update` + `/version` + `/rollback`. Skills existing `update-workspace` + `migrate-workspace` à wirer pipeline canon Sprint v2.80+.
- **First applications** · Sprint v2.80 NEW doctrine racine update-distribution-doctrine + NEW slash commands `/update` + `/version` (Agent 2 sprint v2.80) + GitHub Releases tags rétroactifs v2.65 → v2.79.5 sur Largo2z9/phantomos (Agent 1 sprint v2.80). Sprint v2.81+ NEW slash command `/rollback {version}` + scaffold migrations canon historiques v2.63 + v2.64 + v2.66 BREAKING + pipeline CI/CD GitHub Actions release automation.
- **Promotion criterion** · à reviewer après 5+ opérateurs onboard via pipeline canon UDD plus 1 audit cross-opérateur update adoption rate convergence plus learnings.json append patterns UDD adoption rate stable 90%+ plus zéro operator state écrasé cross 3+ updates consécutifs plus zéro captivité opérateur post-update cross 3+ rollback paths utilisés.

---
