# Extension Discovery Discipline · Operating Doctrine

> Canonique v2.75+. Doctrine canon qui ferme le gap d'auto-consommation entre extensions scaffolded et orchestrateurs production. Doctrine sœur de SED-X (méthodologie ECR amont scaffold), Territory Discipline (substrat couche 1 lieu où NEW entities vivent), Operational System Discipline v2.71 (doctrine mère 5 couches). Codifie le contrat `extension_hooks` frontmatter + manifest registry scan runtime + `consumable_by` pattern qui permet aux orchestrateurs production de consommer automatiquement les NEW entities scaffolded via `scaffold-extension` v1.2.0 Phase 9.

---

## 1. Thèse fondatrice

> L'extension ne sert à rien si elle n'est pas consommée.

PhantomOS scaffold NEW entities via `scaffold-extension` v1.2.0 selon méthodologie ECR (doctrine SED-X v2.71). Mécanisme amont rigoureux · Q&A operator-defined schema · sidecar `{entity}.extensions.json` · governance preserved · canonical IDs cohérence cross-brand. Mais aval, les 4 orchestrateurs production canon (score-matrix · produce-paid-matrix · creative-brief-composer · build-atlas-complete) ont hard-coded entity types dans frontmatter `consumes`. Zéro lecture `_manifest.json` ou `_extensions.json` runtime. NEW entities scaffolded sont registered correctement mais NOT auto-consumed.

Ce gap est structurel · l'opérateur scaffold une `video-script` entity custom dans son workspace, mais `creative-brief-composer` ne sait pas qu'elle existe au runtime. Extension dead-end · scaffold consommé seulement si l'opérateur patch manuellement le frontmatter de chaque orchestrateur production.

Extension Discovery Discipline ferme ce gap via 3 mécaniques canon ·

1. **Frontmatter `extension_hooks`** · NEW canon field optional dans orchestrateurs production qui déclare quels entity types le skill peut consommer via discovery runtime, au-delà du hard-coded canon `consumes`.

2. **Manifest registry scan Step 0** · DRGFP pre-flight enrichi · scan `_extensions.json` au runtime · match `consumable_by` field avec skill name · match `entity_type` avec `extension_hooks` · inclut NEW entities dans inputs Phase 1 pipeline.

3. **Field canon `consumable_by`** · NEW field dans `_extensions.json` per entity registered · enum liste orchestrateurs production consommables · auto-detection à scaffold Phase 9 · operator validation gate accept proposed OR adjust.

Pattern canon · scaffolding amont (SED-X) + discovery runtime (cette doctrine) = boucle complète zéro friction. NEW entity scaffolded today consumable next invocation sans patch manuel.

---

## 2. Le problème résolu

Sans Extension Discovery Discipline ·

1. **Extension dead-end.** Operator scaffold NEW entity (e.g. `video-script`, `competitor-analysis`, `landing-variant`) via canonical `scaffold-extension`. Entity registered correctement, sidecar schema valide, mutation gate cohérent. Mais orchestrateurs production ne savent pas qu'elle existe. Scaffold gaspillé.

2. **Friction runtime opérateur.** L'opérateur scaffold `video-script` puis demande à `creative-brief-composer` de produire un brief multi-format. Skill ignore silencieusement la NEW entity car frontmatter `consumes` hard-coded sur `[creative_entity, audience_entity]` canonical. Opérateur ne comprend pas pourquoi son extension n'est pas utilisée.

3. **Patch manuel chaque orchestrateur.** Pour activer consommation, opérateur doit éditer frontmatter de N orchestrateurs production. Anti-pattern · bypass mutation gate · skip audit trail · friction architecturale · drift maintenance dette.

4. **Discovery silent sans validation.** Si discovery activé naïvement (scan tout `_extensions.json` et inclure), opérateur perd contrôle sur quelles extensions alimentent quel skill. Risque · noise pipeline · output dégradé · trust cassé.

5. **`consumable_by` auto-detection absente.** Sans intelligence à scaffold Phase 9, opérateur doit déclarer manuellement quels orchestrateurs consomment NEW entity. Friction onboarding · charge cognitive · drift naming.

Extension Discovery Discipline = doctrine canon qui ferme ces 5 gaps via contrat structurel + auto-detection + validation gate.

---

## 3. Pattern `extension_hooks` frontmatter

NEW canon field optionnel dans frontmatter orchestrateurs production. Liste enum entity types acceptés via discovery runtime, au-delà du hard-coded canonical `consumes`.

**Syntaxe canon** ·

```yaml
---
name: creative-brief-composer
type: orchestrator
consumes: [creative_entity, audience_entity, brief_entity]
extension_hooks: [creative_entity, audience_entity, brief_entity]
---
```

**Sémantique** ·

- `consumes` · hard-coded entity types canonical (legacy comportement v2.74.x).
- `extension_hooks` · NEW field enum entity types acceptés via discovery runtime. Si NEW entity scaffolded a `entity_type` matching un hook, l'orchestrateur peut la consommer additionnellement.

**Default empty.** Orchestrateurs legacy v2.74.x non patchés conservent `extension_hooks: []` implicite (zéro discovery). Opt-in explicit · skill author déclare quels entity types le skill peut canoniquement intégrer.

**Cardinality.** `extension_hooks` enum cap 5 entity types max par orchestrateur. Au-delà · split orchestrateur OR justification documentée. Évite noise pipeline.

**Cohérence sémantique.** Entity types listés dans `extension_hooks` doivent être canoniquement compatibles avec output du skill. Anti-pattern · déclarer `creative_entity` dans `extension_hooks` d'un skill score-matrix dont output est ranking audience-angle (cross-type drift).

---

## 4. Manifest registry scan Step 0

DRGFP pre-flight enrichi · scan `_extensions.json` OR `_manifest.json#extensions` au runtime pre-flight (Step 0 DRGFP) pour discover NEW entities scaffolded avec `consumable_by` matching le skill courant.

**Flow canon Step 0** ·

```
1. Skill invoked · read frontmatter consumes + extension_hooks
2. Open _extensions.json (or _manifest.json#extensions)
3. For each registered NEW entity ·
   - Match consumable_by includes skill_name
   - Match entity_type ∈ extension_hooks
4. If both match · include entity in pipeline inputs Phase 1
5. Log discovery audit trail · skill_name + entity_id + entity_type
6. Proceed Phase 1 with enriched inputs
```

**Read location.** `_extensions.json` au workspace root (ou `_manifest.json#extensions` selon convention scaffold-extension v1.2.0+ Phase 9). Pattern manifest miroir `.skills/_manifest.json` · pre-built registry index, regenerated post-scaffold via `build-manifest.py` (ou équivalent extension scan).

**Performance.** Scan registry est O(N entities registered) par invocation · cap workspace réaliste ~50 NEW entities · cost négligeable (< 50ms manifest parse + match). Pas de perf concern.

**Cache.** Registry scan cacheable per-session si invariant entre invocations consécutives. Bust cache post-`scaffold-extension` Phase 9 register.

**Fallback.** Si `_extensions.json` absent ou corrupt · skill log warning · fallback comportement legacy hard-coded `consumes`. JAMAIS panic-fail · backward compat strict.

---

## 5. Field canon `consumable_by` registry

NEW field dans `_extensions.json` per NEW entity registered via `scaffold-extension` v1.2.0+ Phase 9 register-and-flag.

**Syntaxe canon** ·

```json
{
  "entities": {
    "video-script": {
      "entity_type": "creative_entity",
      "scope": "brand",
      "data_shape": "instance-per-item",
      "consumable_by": ["creative-brief-composer", "build-atlas-complete"],
      "registered_at": "2026-05-16",
      "version": "1.0.0"
    }
  }
}
```

**Sémantique** ·

- `consumable_by` enum liste orchestrateurs production qui peuvent consommer cette entity au runtime via discovery scan.
- Auto-detection à scaffold Phase 9 (cf §10 decision-aid Q1-Q3).
- Operator validation gate (AskUserQuestion) · accept proposed OR adjust manually OR set empty (entity isolated, no auto-consume).

**Append-only mutability.** `consumable_by` mutable via operator opt-in post-scaffold (e.g. opérateur réalise plus tard qu'une entity custom devrait alimenter NEW orchestrateur). Append-only via mutation gate, jamais hand-edit JSON.

**Empty `consumable_by`.** Valid · entity registered mais isolée du discovery. Pattern · entity opérator-only consultative (e.g. tracking interne, hors-pipeline production). Discovery scan skip.

**Cross-scope behavior.** Entity scope `brand` consumable_by enum filtre orchestrateurs brand-only OR cross-scope (cf §10 Q2). Entity scope `workspace` consumable_by ouvert cross-brand orchestrateurs. Entity scope `operator` limitée operator-facing skills.

---

## 6. Pipeline contract orchestrateurs production

Step 0 DRGFP enrichi par contrat canonical 6 étapes ·

1. **Pre-flight scan** · open `_extensions.json` au runtime · O(N entities).

2. **Match `consumable_by` field** · filter entities où `consumable_by.includes(skill_name)` · candidat consumption.

3. **Match `entity_type` ∈ `extension_hooks`** · filter entities où `entity_type` ∈ frontmatter `extension_hooks` du skill courant · double validation.

4. **Include NEW entities dans inputs Phase 1** · entities matching deux conditions ajoutées au pipeline · cohérence cardinality cap (cf §3).

5. **Output enrichi avec lineage extension consommée** · output skill annote dans audit trail `extensions_consumed: [entity_id_1, entity_id_2]`. Operator traçabilité.

6. **Validation_status propagation** · si NEW entity consommée a `validation_status: hypothesis`, propage hypothesis confidence vers output (cf `confidence-propagation.md` algèbre cascade).

**Anti-pattern · skip Step 0.** Orchestrateur production qui skip Step 0 pre-flight ignore NEW entities consciemment · breaking promesse opérateur. Doctrine canon · Step 0 non-optional dès v2.75.

**Anti-pattern · pollution inputs sans match.** Inclure NEW entities dans inputs sans double match (`consumable_by` + `extension_hooks`) · pollue pipeline · noise output. Doctrine canon · double match strict.

---

## 7. Skills concernés v2.75.0

4 orchestrateurs production canon cibles pour patches v2.75.0 (déclaration `extension_hooks` frontmatter + Step 0 manifest scan implementation) ·

### 7.1 `score-matrix`

**Output canon** · ranking audience × angle scoring avec internal score.

**`extension_hooks` proposed** · `[audience_entity, angle_entity, creative_entity]`. Accept NEW custom entities scoring-compatible · e.g. `competitor-segment` entity opérator-defined.

**Use case canon** · opérateur scaffold `competitor-segment` entity custom. Re-invoke `score-matrix` · pipeline inclut entities discovered · scoring matrix élargie avec ranking competitor segments.

### 7.2 `produce-paid-matrix`

**Output canon** · top-3 territoires paid DTC (angles ranked + audiences scored).

**`extension_hooks` proposed** · `[angle_entity, audience_entity, territory_entity]`. Accept NEW custom entities paid-compatible · e.g. `angle-variant` entity post-test, `audience-segment-merged` entity.

**Use case canon** · opérateur scaffold `landing-variant` entity post-A/B test. Re-invoke `produce-paid-matrix` · pipeline intègre landing-variants comme territoires alternatifs paid scorables.

### 7.3 `creative-brief-composer`

**Output canon** · brief copy + variants visuels Meta-ready sur angle sélectionné.

**`extension_hooks` proposed** · `[creative_entity, audience_entity, brief_entity, format_entity]`. Accept NEW custom entities creative-compatible · e.g. `video-script` entity, `static-variant` entity, `ugc-template` entity.

**Use case canon** · opérateur scaffold `video-script` entity custom multi-format. Re-invoke `creative-brief-composer` · pipeline produit brief multi-format incluant video scripting comme livrable canonical.

### 7.4 `build-atlas-complete`

**Output canon** · pipeline atlas complet (specs + audiences + angles + briefs + créas) from blank.

**`extension_hooks` proposed** · `[creative_entity, audience_entity, brief_entity, format_entity, angle_entity]` (cap 5 max). Accept NEW custom entities cross-types · atlas enrichi avec entities scaffolded.

**Use case canon** · opérateur scaffold 3 entities custom (`video-script` + `competitor-segment` + `landing-variant`) phase pré-launch. Re-invoke `build-atlas-complete` · atlas final intègre toutes entities discovered · output enrichi vs legacy hard-coded.

---

## 8. Anti-patterns canonisés

### Anti-pattern 1 · Extension dead-end

NEW entity scaffolded via `scaffold-extension` Phase 9 mais orphan · zéro `consumable_by` proposed · zéro orchestrateur production sait qu'elle existe. Scaffold gaspillé. Pattern canon · auto-detection §10 Q1-Q3 propose `consumable_by` proposed default · operator accept OR adjust · jamais empty implicite sauf opt-in opérateur.

### Anti-pattern 2 · Hard-coded entity types frontmatter sans hook canon

Orchestrateur production v2.74.x ship avec frontmatter `consumes: [...]` hard-coded · zéro `extension_hooks` opt-in. NEW entities scaffolded ignorées silencieusement. Pattern canon · orchestrateurs production v2.75+ déclarent `extension_hooks` explicit pour opt-in discovery. Legacy v2.74.x non-affectés mais flag à doctrine maintainer pour patch.

### Anti-pattern 3 · Manifest scan absent runtime

Skill ship avec `extension_hooks` déclaré mais zéro Step 0 pre-flight scan `_extensions.json` runtime. NEW entities matching ignorées silencieusement. Pattern canon · Step 0 DRGFP enrichi (cf §6 pipeline contract) non-optional dès v2.75.

### Anti-pattern 4 · `consumable_by` non-déclaré au scaffold

`scaffold-extension` Phase 9 ship NEW entity registered sans `consumable_by` field. Opérateur doit patcher manuellement chaque orchestrateur consommateur. Pattern canon · Phase 9 register-and-flag inclut decision-aid Q1-Q3 (cf §10) qui propose `consumable_by` auto-detection · operator validation gate.

### Anti-pattern 5 · Discovery sans validation gate

Discovery activé naïvement (scan tout `_extensions.json` et inclure automatiquement) sans operator awareness. Opérateur perd contrôle. Pattern canon · double match (`consumable_by` + `extension_hooks`) + audit trail `extensions_consumed` annoté output · opérateur traçabilité full.

### Anti-pattern 6 · Cardinality `extension_hooks` au-delà 5

Orchestrateur déclare `extension_hooks` 8+ entity types · pipeline noise · output dégradé · MECE cassé. Pattern canon · cap dur 5 hooks max par orchestrateur. Au-delà · split orchestrateur OR justification documentée doctrine maintainer.

---

## 9. Cycle d'apprentissage canon

**Boucle complète scaffold → consume zéro friction** ·

```
1. Opérateur trigger scaffold-extension (e.g. "scaffold video-script entity")
2. Phase 9 register-and-flag invoke decision-aid Q1-Q3 (cf §10)
3. Auto-detection propose consumable_by enum (e.g. [creative-brief-composer, build-atlas-complete])
4. Operator validation gate AskUserQuestion ·
   - Accept proposed (default)
   - Adjust manually (add/remove orchestrateurs)
   - Set empty (entity isolated, no auto-consume)
5. _extensions.json registry write append (mutation gate proposed mode)
6. Operator review pending-validations.md, accept persist
7. Next orchestrateur invocation (e.g. /creative-brief-composer ANG-12) ·
   - Step 0 pre-flight scan _extensions.json
   - Match consumable_by + extension_hooks (double validation)
   - Include video-script entity in Phase 1 inputs
   - Pipeline produces output enriched
   - Audit trail annotates extensions_consumed: [VID-01]
8. Operator output enriched zéro patch manuel
```

**Pas de friction runtime.** Pas de patch manuel chaque orchestrateur. Pas de drift maintenance. Pattern canon · scaffolding intelligent (SED-X amont) + discovery intelligent (cette doctrine runtime) = boucle complète.

**Audit trail traçable.** Tout output orchestrateur post-consumption annote `extensions_consumed: [entity_ids]` · opérateur drill 360° lineage extension. Pattern miroir confidence_chain (cf `confidence-propagation.md`).

---

## 10. Décision-aid Q1-Q3 pour scaffold-extension Phase 9

Quand `scaffold-extension` v1.2.0+ Phase 9 register-and-flag, déterminer `consumable_by` proposed auto-detection via 3 questions ·

```
Q1 · entity_type matche quel orchestrateur production canon ?
   - creative_entity → creative-brief-composer + build-atlas-complete
   - audience_entity → score-matrix + produce-paid-matrix + build-atlas-complete
   - angle_entity → produce-paid-matrix + score-matrix + build-atlas-complete
   - brief_entity → creative-brief-composer + build-atlas-complete
   - format_entity → creative-brief-composer
   - territory_entity → produce-paid-matrix
   - autre (custom, hors-canon) → proposer empty, demande operator decision

Q2 · scope (brand/operator/workspace) limite quels orchestrateurs ?
   - scope: brand → tous orchestrateurs (brand-scoped)
   - scope: operator → skills operator-facing seulement (skip orchestrateurs production)
   - scope: workspace → cross-brand orchestrateurs (multi-brand workspace)

Q3 · data_shape compatible quel pattern orchestrateur ?
   - instance-per-item → orchestrateurs item-level (creative-brief-composer, score-matrix)
   - aggregate → orchestrateurs aggregate-level (build-atlas-complete, produce-paid-matrix)
   - time-series → orchestrateurs time-aware (skip canon orchestrateurs v2.75)
```

**Output** · `consumable_by` enum proposed = intersection(Q1 matches, Q2 filter, Q3 compatibility).

**Validation AskUserQuestion** · opérateur accept proposed (default), OR adjust manually (add/remove), OR set empty (entity isolated).

**Edge case Q1 custom entity_type hors-canon** · auto-detection propose empty, demande operator decision explicit. Opérateur décide quels orchestrateurs (s'il y en a) consomment NEW custom entity. Documenté dans `_extensions.json` per-entity comment field.

---

## 11. Backward compat strict additif

Extension Discovery Discipline est strict additif par construction. Garanties ·

**11.1 Frontmatter `extension_hooks` optional default empty.** Orchestrateurs legacy v2.74.x non-patchés conservent comportement hard-coded `consumes` · zéro discovery · zéro régression. Opt-in explicit · skill author déclare `extension_hooks` quand prêt.

**11.2 Field `consumable_by` NEW additif dans `_extensions.json`.** Schema sidecar `_extensions.json` v1.2.0+ append-only · NEW field `consumable_by` per entity registered. Entities pré-v2.75 registered sans field · still valid · scan match skip (consumable_by absent ≠ match).

**11.3 NEW entities pré-v2.75 still consumable manually.** Opérateur peut patcher manuellement frontmatter `consumes` d'un orchestrateur pour inclure pre-v2.75 entity. Anti-pattern (cf §8.4) mais pas blocking. Workspace continuité préservée.

**11.4 Orchestrateurs production v2.74.x non-affectés.** Sans `extension_hooks` déclaré, comportement legacy strict · zéro Step 0 manifest scan · zéro discovery. Workspace pre-v2.75 fonctionne identique post-doctrine ship.

**11.5 Migration path v2.75 → v2.76+.** Sprint patch progressif · v2.75.0 ship doctrine + patches 4 orchestrateurs canon. v2.76+ patch additional orchestrateurs (mine-voc, profile-audience, etc.) selon priorité opérateur. Pas de breaking migration.

---

## 12. Position dans le système opérationnel 5 couches

Extension Discovery Discipline opère sur 3 couches simultanément du multiplicatif Operational System Discipline v2.71 ·

**Couche 2 · Règles (heuristiques décision).** `extension_hooks` frontmatter discipline de décision orchestrateur consume · double match strict `consumable_by` + `entity_type` · Step 0 DRGFP enrichi heuristique pre-flight. Pattern miroir `dependency-resolution-protocol.md` L1+L2+L3 gap-filling.

**Couche 4 · Métriques (boucles feedback).** `consumable_by` registry traçabilité lineage extension consommée · `extensions_consumed` audit trail output annoté · operator drill 360° lineage. Pattern miroir `confidence-propagation.md` audit trail confidence_chain.

**Couche 5 · Rituels (cadence opérationnelle).** `scaffold-extension` Phase 9 register-and-flag rituel canon · auto-detection Q1-Q3 + operator validation gate · cadence onboarding NEW entity. Pattern miroir `learn-from-session` Trigger 8 smart-suggest daemon (cf `pattern-detection-triggers.md`).

**Doctrines sœurs canon** ·

- **SED-X (scope-extension-doctrine.md)** · méthodologie ECR amont scaffold · 7 patterns canon extension scope · doctrine sœur prerequisite. Extension Discovery Discipline opère aval de SED-X · scaffolding amont (SED-X) + discovery runtime (cette doctrine) = boucle complète.
- **Territory Discipline** · substrat couche 1 lieu où NEW entities vivent · territoire = sub-folder workspace path miroir storage. NEW entities discovered alimentent territoire enrichi.
- **Operational System Discipline v2.71** · doctrine mère 5 couches · cette doctrine est instance multi-couches (2 + 4 + 5).

---

## 13. Cross-references

- `operational-system-doctrine.md` v2.71 · doctrine mère 5 couches multiplicatives · grammaire unificatrice PhantomOS
- `scope-extension-doctrine.md` (SED-X) · méthodologie ECR amont scaffold · 7 patterns canon extension scope · doctrine sœur prerequisite
- `compositional-cartography.md` v3.1 · équation NOYAU × CONTEXTE × MODIFIEURS · pattern ECR couche 1 instance créative
- `canonical-matrix-reasoning.md` (CMR) · schema + matrice canon production 95% qualité · pattern compose intersectional outputs
- `scaffold-extension` v1.2.0+ Phase 9 register-and-flag · upstream skill qui register NEW entities avec `consumable_by` auto-detection (cf §10 decision-aid Q1-Q3)
- `confidence-propagation.md` · algèbre cascade confidence cross-skill · pattern audit trail miroir `extensions_consumed` annotation output
- `dependency-resolution-protocol.md` (DRGFP) · règle canon couche 2 · L1+L2+L3 gap-filling pre-flight Step 0 enrichi
- `pattern-detection-triggers.md` · registre canonique 8 triggers learn-from-session · pattern miroir rituel cadence couche 5
- `schema-encoding-discipline.md` (SED) · substrate ontologique · `_extensions.json` sidecar schema validation · mutation gate `consumable_by` field append-only
- `skill-authoring-doctrine.md` (SAD) · skill creation discipline · frontmatter `extension_hooks` NEW field validation · type taxonomy producer/orchestrator opt-in discovery
- `doctrine-governance.md` · amendment process append-only D# verrouillé · cette doctrine entry registry append-only post-ship

**Skills concernés v2.75.0 (downstream consumers patches)** ·

- `score-matrix` · patch frontmatter `extension_hooks: [audience_entity, angle_entity, creative_entity]` + Step 0 manifest scan implementation
- `produce-paid-matrix` · patch frontmatter `extension_hooks: [angle_entity, audience_entity, territory_entity]` + Step 0 manifest scan implementation
- `creative-brief-composer` · patch frontmatter `extension_hooks: [creative_entity, audience_entity, brief_entity, format_entity]` + Step 0 manifest scan implementation
- `build-atlas-complete` · patch frontmatter `extension_hooks: [creative_entity, audience_entity, brief_entity, format_entity, angle_entity]` (cap 5 max) + Step 0 manifest scan implementation

**Future v2.76+** ·
- Patch additional orchestrateurs (mine-voc, profile-audience, snapshot-brand Movement 4) selon priorité opérateur
- Audit complet orchestrateurs canon v2.75+ · classification `extension_hooks` opt-in coverage
- NEW field validation `extension_hooks` enum via `validate-resources` skill (warning level jusqu'à v2.77 puis enforcement)

---

## Status

- **Canonique v2.75+.** Doctrine canon · ferme gap d'auto-consommation extensions scaffolded vs orchestrateurs production hard-coded.
- **Doctrine sœur** · SED-X (scope-extension-doctrine.md méthodologie ECR amont) · Territory Discipline (substrat couche 1) · Operational System Discipline v2.71 (doctrine mère).
- **Backward compat** · strict additif · doctrine NEW n'override aucune existing. `extension_hooks` frontmatter optional default empty. `consumable_by` field NEW additif `_extensions.json` v1.2.0+.
- **First applications** · patches 4 orchestrateurs canon v2.75.0 (score-matrix · produce-paid-matrix · creative-brief-composer · build-atlas-complete). Decision-aid §10 Q1-Q3 applicable scaffold-extension v1.2.0+ Phase 9. Pipeline contract §6 applicable Step 0 DRGFP enrichi tous orchestrateurs production opt-in.
- **Promotion criterion** · à reviewer après 5+ NEW entities scaffolded avec `consumable_by` auto-detection appliqué + 3+ orchestrateurs invoke avec discovery successful + 1 audit systémique gap orchestrateurs production restants.

---

*Doctrine canonique skill-author-facing. Canonise contrat extension_hooks + manifest registry scan + consumable_by pattern. Ferme gap structurel v2.74.x audit READ-ONLY Patch 5. Pattern miroir scope-extension-doctrine.md (méthodologie ECR amont) et territory-doctrine.md (substrat couche 1).*
