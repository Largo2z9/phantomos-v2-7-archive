# Scope Extension Discipline (SED-X) · Operating Doctrine

> Working draft canon v2.65+. Sister discipline of SED (Schema Encoding), SAD (Skill Authoring), CMR (Canonical Matrix Reasoning). Codifies how PhantomOS workspace extends with NEW scope (brand · produit · audience · doctrine · bridge tool · custom entity) without breaking architectural integrity.

---

## 1. Thesis

> Le PhantomOS workspace est conçu pour scaling additif. Scope extension = trigger naturel opérateur · scaffolding auto via canon pattern · zéro friction architecturale pour extensions normales · breaking changes réservés sprints dédiés avec migration scripts idempotents.

L'opérateur ne devrait jamais avoir à connaître les schemas ou skills pour étendre son workspace. Il déclare l'intent ("nouvelle brand" · "snapshot ce 2e produit" · "lance mine-voc nouvelle audience") · l'agent route via skill canonical · les mutations stagées via gate · workspace s'auto-organise via path structure miroir des schemas.

Ce contrat est cassé si ·
1. Operator hand-edit JSON pour ajouter scope (bypass mutation gate · skip event log · corrupt audit trail)
2. Skill fork dédié au lieu d'extend skill existing (cardinality dispersion · maintenance dette)
3. Custom entity ad-hoc sans `scaffold-extension` canonical (drift extension layer)
4. NEW canonical entity shipped sans schema · sans doctrine · sans skill consume cross-link (orphan)

SED-X codifie les 7 patterns canonicaux d'extension + 4 mécanismes auto-update runtime + limites architecturales.

---

## 2. Le problème SED-X résout

Sans discipline d'extension scope ·

1. **Drift architectural cumulé** · 6 mois post-ship, workspace incohérent · 12 audiences encodées 3 façons différentes · 4 schemas redondants · 8 skills overlap. Cause · pas de pattern canon pour évaluer "comment ajouter ce nouveau X?".

2. **Operator confusion** · "comment j'ajoute un 2e produit?" → réponses différentes selon contexte session (parfois snapshot-brand · parfois ingest-resource · parfois hand-edit). Cause · pas de cartographie canonical des entry points par type d'extension.

3. **Skill fork inutile** · besoin d'ajouter `filter-angles-by-persona` skill car produce-paid-angles "fait pas exactement ce qu'on veut". Cause · pas de doctrine canon "extend_before_create" applied rigoureusement.

4. **Custom entity ad-hoc** · operator ajoute `brands/{slug}/competitors/` direct (hand-edit) car `scaffold-extension` skill pas connu. Cause · extension layer canon pas codifié comme discipline.

SED-X = doctrine canon qui ferme ces gaps.

---

## 3. Les 7 patterns canon d'extension scope

Table exhaustive par type d'extension · trigger opérateur naturel · skill canonical à invoker · effort · backward compat.

### Pattern 1 · NEW brand client (multi-brand workspace scaling)

| Aspect | Détail |
|---|---|
| Trigger opérateur | "ajoute nouvelle brand X" · "setup brand newclient avec URL Y" |
| Skill canonical | `setup-brand` → `snapshot-brand` chain auto |
| Effort | 5-10 min scrape |
| Auto-update workspace | `brands/{new_slug}/` scaffold auto via mutation gate · `/phantom` workspace mode rend N brands en barres comparées |
| Backward compat | Strict additif · existing brands intactes |
| Anti-pattern | Hand-edit `brands/` directly · skip mutation gate · skip business_model auto-detection |

### Pattern 2 · NEW produit dans brand existante

| Aspect | Détail |
|---|---|
| Trigger opérateur | "snapshot ce 2e PDP URL" · "ingest catalog CSV" · "ajoute le produit XYZ" |
| Skill canonical | `snapshot-brand --mode=product-add` OR `ingest-resource` |
| Effort | 5-15 min |
| Auto-update | `brands/{slug}/products/{new_product}/` scaffold spec + offers + funnel · cross-refs angles/creatives/learnings update auto via canonical IDs |
| Backward compat | Strict additif |
| Anti-pattern | Edit `products/` direct · skip schema validation · skip business_model alignment |

### Pattern 3 · NEW audience post-mining

| Aspect | Détail |
|---|---|
| Trigger opérateur | "mine-voc sur nouvelle audience X" · "cartographie audience Y" |
| Skill canonical | `mine-voc` OR `map-audiences` OR `profile-audience` |
| Effort | 20-30 min mining minimum (verbatim density floor v2.36 ≥ 5) |
| Auto-update | `audiences/{new_aud}/profile.json + pain_points/ + objections/` scaffold sub-parent canonical (v2.64 sémantique pure) · validation_status hypothesis · canonical IDs PNT-NN/OBJ-NN incrémental cross-brand |
| Backward compat | Strict additif · existing audiences intactes |
| Anti-pattern | Inventer audience sans VoC (HR4.5 v2.36 gate strict) · skip cartography 3 niveaux mère/sous-poche |

### Pattern 4 · NEW business_model post-pivot

| Aspect | Détail |
|---|---|
| Trigger opérateur | Re-snapshot post-launch · operator declare "on lance aussi un service" |
| Skill canonical | `snapshot-brand` Step 2bis re-run (v1.3.1+) OR `setup-brand --update business_model` |
| Effort | 5 min |
| Auto-update | `brand.json#identity.business_model` update via mutation gate · `/phantom` rendering adapte auto WORKSPACE NAVIGATION (DTC → hybrid ajoute Réseau cliniques section · service-only skip products · etc.) |
| Backward compat | Strict additif via fallback default DTC implicite pour brands pre-v2.57 |
| Anti-pattern | Hand-edit brand.json · skip business_model_signals capture · skip re-detection auto |

### Pattern 5 · NEW custom entity hors-canon

| Aspect | Détail |
|---|---|
| Trigger opérateur | "j'ai besoin de tracker les concurrents séparément" · "scaffold competitors entity" |
| Skill canonical | `scaffold-extension` (canonical extension layer) |
| Effort | 15-30 min Q&A |
| Auto-update | `brands/{slug}/custom/{entity}/` + sidecar `{entity}.extensions.json` schéma operator-defined · `/phantom` rendering surface custom section |
| Backward compat | Strict additif · zéro canon impact |
| Anti-pattern | Custom entity hand-edit direct · sans scaffold-extension · drift extension layer governance |

### Pattern 6 · NEW data source externe

| Aspect | Détail |
|---|---|
| Trigger opérateur | "ingest ce PDF founder" · "pull mon Notion vers Phantom" · "import Drive folder reviews" |
| Skill canonical | `ingest-resource` OR `sync-notion-atlas` (Layer 1 MCP) OR `import-asset` |
| Effort | 10-20 min selon source size |
| Auto-update | Stage proposals canoniques distribuées dans 11 collections via mapping intelligent · validate-resources silent post-stage · pending-validations.md operator arbitre |
| Backward compat | Strict additif |
| Anti-pattern | Import data sans mapping canonical · zéro mutation gate · zéro validation_status tagging |

### Pattern 7 · NEW bridge tool externe

| Aspect | Détail |
|---|---|
| Trigger opérateur | "sync Linear/Airtable/ClickUp" · "import slack channel" |
| Skill canonical | NEW skill `sync-{tool}-atlas` (pattern miroir sync-notion-atlas) + NEW doctrine `{tool}-bridge-doctrine.md` |
| Effort | 4-6h sprint dédié par tool nouveau |
| Auto-update | Layer 1 MCP cohérent connectivity-layering · pattern reproductible cross-tools · doctrine bridge documente mappings canonical |
| Backward compat | Strict additif · NEW skill n'override aucun · MCP opt-in |
| Anti-pattern | Fork sync-notion-atlas code · au lieu de reproduire pattern. Skip doctrine bridge. |

---

## 4. Les 4 mécanismes auto-update workspace runtime

Mécanismes système-side qui font que workspace s'auto-organise post-extension scope ·

### Mécanisme 1 · Manifest regen auto post-skill add

`build-manifest.py` régénère `.skills/_manifest.json` post-NEW skill add. Routing fallback systémique v2.56+ scan triggers FR + EN immediatement opérationnel sans patch CLAUDE.md root. NEW skill discoverable auto.

### Mécanisme 2 · Mutation gate distribué

`write-to-context.py --mode=proposed` sur tout NEW entry stagée · pending-validations.md propose à l'opérateur (accept/reject/correct par lot ou drill). Cohérence canonical IDs (PNT-NN/OBJ-NN/etc.) incrémental cross-brand managed automatiquement.

### Mécanisme 3 · /phantom rendering adaptive miroir storage path

`/phantom` mode brand 5 sections (Header + EN COURS + WORKSPACE NAVIGATION adaptive + ACTIONS + DRILL) rend storage path structure auto. NEW collection sub-folder visible immédiatement dans drill parent (cf v2.64 sémantique pure pattern). Pas de patch rendering needed pour NEW scope.

### Mécanisme 4 · Cross-refs canonical résolvent

NEW canonical IDs s'inscrivent automatiquement dans cross_refs des autres entités · drill 360° expose auto (cf v2.64 drill audience/product 360°). Validation runtime cross-refs intégrité via validate-resources skill.

---

## 5. Limites architecturales · non-auto

3 cas où extension scope nécessite intervention humaine + sprint dédié, pas auto ·

### Limite 1 · Refonte schema breaking (v2.x → v3.x)

Pattern · schema bump majeur change structure (e.g. profile.schema v1.7 → v2.0 BREAKING v2.63 · move pain_points sub-folder v2.64). Nécessite migration script idempotent + bump release dédiée + skills patches paths update. Pas auto.

Mécanisme · doctrine governance (cf `doctrine-governance.md`) + amendment process append-only D# verrouillé.

### Limite 2 · Doctrine canon pivot conceptuel

Pattern · doctrine canon SED/CMR/SAD/CC change concept fondamental (e.g. compositional-cartography ajout 5e arbre cross-vertical). Nécessite sprint refactor cross-skills + tous documents qui referencent + cross-refs canonical IDs update. Pas auto.

Mécanisme · doctrine-governance amendment process · supersession formalisée · cross-refs tracées.

### Limite 3 · Cross-brand inheritance (canon copy promotion)

Pattern · learning brand-specific (e.g. winner pattern Sentage angles) émerge canonical cross-brand (promote vers `resources/canon/copy/` shared). Nécessite skill `learn-from-session` Trigger 7 manuel + N≥3 brands validation cross. Semi-auto (trigger detection + operator validation).

Mécanisme · canon-tool schema v1.1 attribution + decay v2.37 · validations[] append-only + N-brand threshold.

---

## 5bis. Hiérarchie SED-X parmi les disciplines

SED-X ne sit pas en isolation. Position relative dans le graphe canon ·

```
Frame test · Extractibility (transverse · contrainte)
 │
MASTER · Contextual Intelligence (CI) · agent reasons, never form-fills
 │
 ├─ SED (Schema Encoding Discipline) · substrate
 │   └─ Prérequis ontologique de CMR, SAD, SED-X
 │
 ├─ CMR (Canonical Matrix Reasoning) · production mechanism
 │
 ├─ SAD (Skill Authoring Discipline) · skill creation discipline
 │
 ├─ SED-X (Scope Extension Discipline) · NEW · how to extend workspace scope
 │   ↑ consomme SED (schemas) + SAD (skills) + CMR (production patterns)
 │   ↑ étendue via doctrine-governance pour cas BREAKING
 │
 └─ CC (Compositional Cartography) · creative production discipline
```

**3 relations load-bearing** ·

1. **SED < SED-X** (prerequisite). Sans SED rigoureux (mutation gate, _field_types, _version semver, sourcing tags), SED-X n'a pas de substrate à étendre. Pattern 5 (custom entity) repose sur extension layer canon SED. Patterns 1-4 et 6-7 reposent sur core schemas SED versionnés.

2. **SAD < SED-X** (prerequisite). Sans SAD (skill type taxonomy, composition contracts, frontmatter triad), les NEW skills shipped sous Pattern 7 (bridge tool) ou via extension Pattern 5 (`scaffold-extension`) drift hors-canon. SED-X demande SAD-compliance sur toute NEW skill créée.

3. **SED-X ⊂ CI** (sub-pattern). CI déclare le but (agent reasons, jamais form-fill). SED-X opérationnalise ce but pour le cas concret du scaling additif scope. Sans SED-X, l'extension scope dérive en form-fill (operator hand-edit, agent improvise).

**Distinction avec autres disciplines** · CMR concerne la *production intersectionnelle* (paid-angles, copy-brief). SED-X concerne l'*extension structurelle workspace* (NEW brand, NEW entity, NEW bridge). CC concerne la *composition créative* (4 arbres + matrice). SED-X est complémentaire, pas overlap.

---

## 6. Anti-patterns

### Anti-pattern 1 · Hand-edit JSON direct sous brands/

**NEVER** edit `brands/{slug}/*.json` direct via Edit/Write/NotebookEdit. Bypass mutation gate · skip audit trail · corrupt proposal/acceptance workflow · break canonical IDs cohérence. Mutation gate `write-to-context.py --mode=proposed` non-optional.

### Anti-pattern 2 · Skill fork au lieu d'extend (extend_before_create violation)

Si besoin d'ajouter feature à un skill existant, prefer patch (nouveau mode/phase/input conditionnel) à fork. Skill fork standalone justifié SEULEMENT si ·
- Logic métier complexe non-réductible à orchestrator step
- Trigger opérateur distinct fréquent
- Cardinality élevée nécessitant boucle dédiée

Sinon · `extend_before_create` canon (cf CLAUDE.md root rule).

### Anti-pattern 3 · Custom entity hors scaffold-extension

Pour entité custom hors-canon (ex `competitors`, `partnerships`, `events`), invoke `scaffold-extension` canonical skill · operator-defined schema sidecar · governance preserved. JAMAIS scaffold custom entity ad-hoc.

### Anti-pattern 4 · NEW canonical entity orphan

NEW schema shipped sans skill consume cross-link · sans doctrine update · sans entry SED §13 schema evolutions registry · sans mention CLAUDE.md root architecture · est un orphan. Pattern canon · ship doit inclure schema + skill(s) consume + doctrine + registry.

### Anti-pattern 5 · NEW bridge tool sans pattern reproductible

NEW bridge tool externe (Linear/Airtable/etc.) shipped sans suivre pattern sync-notion-atlas + notion-bridge-doctrine miroir. Code fork = maintenance dette · doctrine fragmentée. Pattern canon · doctrine `{tool}-bridge-doctrine.md` + skill `sync-{tool}-atlas` cohérent.

---

## 7. Decision-aid pour skill author

Avant d'ajouter NEW scope, applique ce decision-aid ·

```
Q1 · L'extension est-elle couverte par un pattern canon SED-X (7 patterns) ?
   OUI → invoke skill canonical correspondant · ship
   NON → Q2

Q2 · Est-ce un cas custom (entity hors-canon) ?
   OUI → invoke scaffold-extension · operator-defined schema sidecar
   NON → Q3

Q3 · Est-ce un cas canonical NEW (justifie NEW schema + skill) ?
   OUI → sprint dédié · schema + skill + doctrine + SED §13 + cross-refs cross-link
   NON → Q4

Q4 · Est-ce un cas BREAKING (refonte schema majeur · doctrine pivot · cross-brand promotion) ?
   OUI → doctrine-governance amendment process · sprint dédié · migration script
   NON → flag à doctrine maintainers pour évaluation
```

---

## 7bis. Operational requirements

SED-X est une doctrine · opérationnellement elle impose les conventions infrastructure suivantes pour ship cohérent. Non-optionnel dès qu'une extension scope ship sur production workspace.

**7bis.1 Pattern coverage check pre-ship.** Avant tout ship NEW scope, le skill author confirme (commit message ou learn-from-session entry) lequel des 7 patterns §3 couvre l'intent · OR justifie explicitement pourquoi aucun pattern canon ne s'applique (déclenche Q3-Q4 du decision-aid §7).

**7bis.2 Mutation gate non-optional sur tout scope add.** Patterns 1-6 mutent state via `write_to_context()` mode=proposed. Pattern 7 mutent via NEW skill qui elle-même respecte mutation gate. JAMAIS hand-edit JSON sous `brands/`, `operator/`, `resources/canon/`.

**7bis.3 Schema canonical validation post-extension.** Post-ship NEW scope (entité, schema, custom entity), trigger `validate-resources` silently. MAJOR/CRITICAL findings flag à l'opérateur. Patterns auto-update (§4) émettent validation events post-mutation gate flush.

**7bis.4 Cross-refs canonical IDs préservés.** NEW canonical IDs (PNT-NN, OBJ-NN, FRC-NN, ANG-NN, etc.) incrémental cross-brand managed via allocator scan existing collection. JAMAIS re-assignation. SED §13 schema evolutions registry doit recevoir entry append-only pour tout NEW scope canonical.

**7bis.5 Doctrine ship requirement.** Pattern 7 (NEW bridge tool) requiert NEW doctrine `{tool}-bridge-doctrine.md` shipped en parallèle de NEW skill `sync-{tool}-atlas`. Skill orphan sans doctrine = refusé par convention. Pattern reproductible miroir `notion-bridge-doctrine.md` (cf D#391 atlas vivant canon).

**7bis.6 Manifest regen post-skill add.** `build-manifest.py` régénéré post-NEW skill add (`.skills/_manifest.json` triggers FR + EN). Routing fallback systémique scan immédiatement opérationnel sans patch CLAUDE.md root. Mécanisme §4.1.

**7bis.7 SED §13 schema evolutions registry append-only.** Tout NEW canonical entity / schema bump / patch additif doit créer entry sous SED §13 avec semver bump, diff summary, design decisions sourçables (D# verrouillés).

**7bis.8 Backward compat strict additif par défaut.** Patterns 1-7 sont strict additif par construction. Exception · Limite 1 (refonte schema breaking) requiert migration script idempotent + sprint dédié + bump release. Pas auto.

---

## Position dans le système opérationnel 5 couches

SED-X est la méthodologie canon d'extension de scope PhantomOS vers
un nouveau domaine. Elle applique l'ECR (couche 1 du système opérationnel
cf `operational-system-discipline.md`) en amont · test d'éligibilité
(le domaine passe les 3 critères hiérarchie · auto-similarité ·
interdépendance multiplicative ?), choix du pattern parmi les 4 canon,
décomposition MECE.

Sans ECR upfront, scope extension freelance produit doctrine fragmentaire
non-MECE. Avec ECR, scope extension produit doctrine systématique.

---

## 8. Cross-references

- `schema-encoding-discipline.md` (SED) · substrate sub-doctrine · schemas + mutation gate + _field_types
- `skill-authoring-doctrine.md` (SAD) · skill creation discipline · type taxonomy · composition contracts
- `canonical-matrix-reasoning.md` (CMR) · production 95% quality
- `compositional-cartography.md` (CC) · cartographier + composer outputs créatifs
- `extending.md` · extension layer canon · custom entities · sidecars
- `notion-bridge-doctrine.md` · bridge external tool canon pattern reproductible
- `doctrine-governance.md` · amendment process · supersession formalisée
- `contextual-intelligence.md` (CI) · master doctrine
- `provenance-trust-discipline-scope.md` (PTD scope) · multi-operator · canon-as-product · marketplace

SED-X sister discipline · pattern d'extension scope codifié canon technique. Distinct CI (master) · SED (substrate) · CMR (production) · SAD (authoring) · PTD (provenance).

---

## 8bis. Open tensions

À résoudre progressivement avec retour terrain ·

1. **Pattern 5 (custom entity) vs Pattern 3 (NEW audience) overlap.** Si l'opérateur veut tracker une "audience-like" entity mais non-canonical (ex `prospect_cohorts`, `partner_audiences`), Pattern 3 (canonical audience via mine-voc) vs Pattern 5 (scaffold-extension custom) overlap. Working rule · si l'entity se compose dans les 4 arbres CC (Spec/Audience/Angle/Roadmap), c'est Pattern 3. Sinon Pattern 5. À valider sur 3 cas terrain.

2. **Pattern 7 (bridge tool) effort estimate.** "4-6h sprint dédié par tool" basé sur sync-notion-atlas (référence) · mais varies selon complexité tool (Linear ≠ ClickUp ≠ Slack channels). Working rule · effort estimate par tool est dans la doctrine bridge dédiée (`{tool}-bridge-doctrine.md`). À calibrer post-2e bridge ship.

3. **Limite 3 (cross-brand inheritance) threshold N≥3 brands.** Validation cross-brand pour canon copy promotion fixé à N≥3 brands min (canon-tool schema v1.1 attribution + decay v2.37). Working rule · N≥3 valide pour pattern recurring · mais N=2 strong correlation peut justifier promotion early avec flag "tentative canon". À codifier formellement quand 3e brand ship canon copy.

4. **Mécanisme 3 (/phantom rendering adaptive) edge cases.** Storage path miroir auto-update fonctionne pour patterns canonical (sub-audience, sub-product). Custom entities Pattern 5 visible via custom section, mais drill depth limité à 1 niveau. Working rule · si custom entity nest 2+ niveaux (ex `competitors/{slug}/ads/{ad_id}.json`), drill depth check est responsabilité de l'opérateur. À auto-detect post-feedback terrain.

5. **Pattern 4 (business_model pivot) frequency.** Re-snapshot post-pivot fréquence empirique sub-jour à mois. Working rule · pivot rare donc Q&A manuel via setup-brand --update justifié. Si fréquence ↑ (par ex N≥5 pivots/an workspace), introduire `update-business-model` skill dédié. À monitorer.

6. **SED-X overlap avec doctrine-governance.** SED-X §5 Limites architecturales (refonte schema, doctrine pivot, cross-brand promotion) reference doctrine-governance amendment process. Boundary · SED-X codifie *quels* cas trigger doctrine-governance · doctrine-governance codifie *comment* le processus s'exécute. À réviser quand doctrine-governance ship v2+.

---

## 9. Amendment protocol

Cf `doctrine-governance.md § Amendment`. Toute évolution SED-X passe par D# verrouillé append-only + supersession formalisée + cross-refs re-tracées dans skills consume.

---

## 10. Status

- **Draft v0.1 v2.65** · research zone, Build mode.
- **Promotion criterion** · à reviewer après 5+ ship extension scope live (NEW brand · NEW custom entity · NEW bridge tool · etc.) avec retour terrain validé.
- **First applications** · patterns 1-7 codifiés depuis v2.55 sprint massif (8 releases v2.55-v2.64 ont shippé extensions via patterns canon).

---

*Doctrine canonique skill-author-facing. Sister of SED · CMR · SAD · CI master. Codifies the 7 canonical patterns of scope extension + 4 auto-update mechanisms + architectural limits.*
