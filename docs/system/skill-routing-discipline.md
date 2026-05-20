# Skill Routing Discipline · Operating Doctrine

> Canonique v2.76+. Doctrine canon qui codifie comment l'agent route une requête opérateur vers le bon skill (ou chaîne de skills) en utilisant le manifest registry pré-buildé, le champ `disambiguates_against`, la posture investigation, et le slash command `/scope` comme filet de sécurité. Doctrine sœur de `canonical-matrix-reasoning.md` (qualité output post-routing) et `investigation-posture.md` (rigueur réponse). Ferme le gap entre intent opérateur exprimé en langage naturel et invocation skill canon zéro freestyle.

---

## 1. Thèse fondatrice

> L'agent ne freestyle JAMAIS quand un skill canon existe. Le routing est un protocole, pas une improvisation.

PhantomOS ship 70+ skills typés (producer, curator, capturer, orchestrator, navigator, builder, shared) qui consomment les matrices canon (hooks, angles, heuristiques-persuasion, creative-mechanics-registry, niveaux-schwartz, formats-livrables) restées dormantes en mode prose libre. Mais l'agent LLM, sans discipline routing stricte, dérive vers freestyle prose comme premier réflexe sur tout output stratégique demandé. Résultat · matrices canon ignorées · output dégradé · qualité 60% au lieu de 95% (cf `canonical-matrix-reasoning.md` § cohérence schema + canon).

Skill Routing Discipline ferme ce gap structurel via protocole strict 5 phases ·

1. **Mapping explicite first.** Agent scan d'abord le mapping output → skill verrouillé dans `CLAUDE.md` § Skill routing (v2.55 baseline · 20+ entrées canon).

2. **Manifest registry scan second.** Si aucun mapping explicite ne match, agent scan `.skills/_manifest.json` pre-built index (triggers FR + EN par skill · `disambiguates_against` field · `subagent_safe` flag · `recommended_model` field).

3. **Disambiguation rules third.** Si 2+ skills matchent, agent lit `disambiguates_against` field de chaque candidate et applique la condition littérale. Si encore flou, AskUserQuestion avec 2-3 options.

4. **`/scope` fallback fourth.** Si l'opérateur engage un sujet précis SANS skill clair en mapping ET sans match manifest, agent invoque `/scope {sujet}` AVANT freestyle prose. `/scope` cartographie paramètres décidables et termine sur décisions actionnables · transforme intention floue en route opérable.

5. **Freestyle last resort.** Uniquement si `/scope` confirme zéro skill canon ne s'applique (rare · candidat backlog `create-skill` flag à l'opérateur).

Pattern canon · scan manifest first (canonical) + disambiguation rules (explicit) + /scope fallback (safety net) + freestyle last resort (rare) = boucle complète zéro friction routing. NEW skills shipped par `create-skill` immédiatement consumable next invocation sans patch manuel mapping CLAUDE.md.

---

## 2. Le problème résolu

Sans Skill Routing Discipline ·

1. **Freestyle prose réflexe.** Agent reçoit demande stratégique (e.g. *"produis-moi un angle paid sur cette audience"*), commence à improviser une matrice angle from scratch en prose libre, ignore `produce-paid-angles` skill canon qui consume formula Obs+Tension+Reframe+Bridge + registry angle-mechanics + niveaux-schwartz. Output dégradé · qualité 60% au lieu de 95%.

2. **Skill mis-trigger.** Agent invoque le mauvais skill (e.g. `decompose-ad` pour un brief copy alors que `produce-copy-brief` est canon). Friction runtime opérateur · output hors-scope · trust cassé.

3. **Skill sibling créé sans nécessité.** Agent face à un besoin proche d'un skill existant propose un skill frère NEW au lieu d'étendre l'existant (memory canon `extend_before_create`). Fragmente mental model opérateur · duplique logique de gate · drift maintenance.

4. **`/scope` non-déclenché sur intention floue.** Opérateur engage sujet précis ("aide-moi à comprendre paid media DTC scaling") sans skill clair en mapping. Agent freestyle prose pédagogique au lieu d'invoquer `/scope` qui cartographie paramètres décidables. Opérateur reçoit prose verbose sans décisions actionnables.

5. **Disambiguation rules ignorées.** 2+ skills matchent (setup-brand vs onboard-brand · validate-resources vs audit-meta-account). Agent pick au hasard ou via heuristique freestyle au lieu de lire `disambiguates_against` field manifest. Routing inconsistent · drift session-to-session.

Skill Routing Discipline = doctrine canon qui ferme ces 5 gaps via protocole structurel + manifest scan canon + `/scope` fallback + AskUserQuestion gate.

---

## 3. Mapping explicite output → skill

Première étape canon · mapping output → skill verrouillé dans `CLAUDE.md` § Skill routing (v2.55 baseline). 20+ entrées canon couvrant les outputs stratégiques fréquents ·

**Outputs stratégiques mappés canon** ·

- Output audiences (personas, segments, cartographie) → `profile-audience`
- Output angles paid (formula Obs+Tension+Reframe+Bridge) → `produce-paid-angles`
- Output brief copy (écrit court ou long, structure persuasion) → `produce-copy-brief`
- Output visual creative (composition pub) → `compose-creative`
- Output adaptation creative existant → `recompose-creative`
- Output reverse-engineering ad concurrente → `decompose-ad`
- Output brand state ou état workspace → `brief-day`
- Output snapshot brand depuis URL → `snapshot-brand`
- Output canonical packshot → `craft-packshot`
- Output import asset brand → `import-asset`
- Output VoC verbatims mining → `mine-voc`
- Output cartographie produit → `define-specs`
- Output audit performance compte Meta → `audit-meta-account`
- Output prioritisation territoires → `score-matrix`
- Output learning persistence → `learn-from-session` ou `capture-learning`
- Output pipeline atlas complet (specs + audiences + angles + briefs + créas) → `build-atlas-complete`
- Output matrice paid DTC (angles ranked + audiences scored + top-3 territoires) → `produce-paid-matrix`
- Output brief créa + variants visuels sur angle sélectionné → `creative-brief-composer`
- Output sync Notion ↔ PhantomOS (pull / push / scaffold) → `sync-notion-atlas`
- Output scoping intention floue (LEARN ou BUILD) → `/scope`

**Sémantique mapping** ·

- Mapping verrouillé canon · l'agent ne change pas le mapping en cours de session.
- Mapping append-only · NEW skills shippés par `create-skill` ajoutés au mapping via amendment doctrine (cf `doctrine-governance.md` append-only D# verrouillé).
- Mapping ≠ exhaustif · couvre les outputs fréquents · fallback manifest scan canon pour outputs périphériques (cf §4).

**Routing exception · conversation libre.** Questions, clarifications, debug, doctrine discussion restent en prose libre. La règle Skill Routing Discipline s'applique au contenu stratégique livré, pas au dialogue conversationnel.

---

## 4. Manifest registry scan canon

Deuxième étape canon · si zéro mapping explicite ne match l'intent opérateur, agent scan `.skills/_manifest.json` (pre-built index regenerated post-skill add/edit via `.skills/build-manifest.py`).

**Structure manifest canon v2.67+** ·

```json
{
  "skills": [
    {
      "name": "produce-paid-angles",
      "type": "producer",
      "model": "sonnet",
      "subagent_safe": true,
      "mode": "ranked",
      "layer": "production",
      "triggers": {
        "fr": ["produis angles paid", "génère angles", "angle paid DTC"],
        "en": ["produce paid angles", "generate angles", "DTC paid angle"]
      },
      "disambiguates_against": {
        "produce-paid-matrix": "produce-paid-angles produit angles isolés ; produce-paid-matrix produit matrice angles × audiences scorée."
      },
      "path": ".skills/skills/produce-paid-angles/SKILL.md"
    }
  ]
}
```

**Flow canon scan manifest** ·

```
1. Agent scan manifest registry · O(N skills) · cap 70+ skills réaliste · cost négligeable (< 50ms parse + match).
2. For each skill · match triggers FR + EN avec intent opérateur (semantic match · keyword overlap).
3. If exactly 1 skill matches · invoke via Task tool si subagent_safe + recommended_model différent, sinon inline.
4. If 2+ skills match · proceed §5 disambiguation rules.
5. If 0 skills match · proceed §6 /scope fallback.
```

**Read location.** `.skills/_manifest.json` au workspace root. Pattern manifest miroir · pre-built registry index, regenerated via `python3 .skills/build-manifest.py` post-skill add/rename/edit/archive.

**Performance.** Scan registry O(N skills) cap workspace réaliste 70+ skills · cost négligeable. Pas de perf concern.

**Cache.** Registry scan cacheable per-session si invariant entre invocations consécutives. Bust cache post-`create-skill` ship OR post-skill archive.

**Fallback.** Si `_manifest.json` absent ou corrupt · agent log warning · fallback comportement legacy mapping CLAUDE.md only · JAMAIS panic-fail. Backward compat strict.

---

## 5. Disambiguation rules

Troisième étape canon · si 2+ skills matchent triggers (mapping OR manifest), agent applique `disambiguates_against` field littéralement.

**Pattern canon `disambiguates_against`** · NEW frontmatter field skill SKILL.md (registered manifest field) qui name sibling skills et spell out la routing condition.

**Syntaxe canon** ·

```yaml
---
name: setup-brand
type: builder
disambiguates_against:
  onboard-brand: "setup-brand setup 1 étape isolée (e.g. brand.json scaffold); onboard-brand orchestrate 4-step pipeline complete day-1."
  snapshot-brand: "setup-brand requires explicit operator init; snapshot-brand triggers automatiquement sur URL ecom pasted."
---
```

**Flow canon disambiguation** ·

```
1. Agent collect candidate skills (e.g. setup-brand, onboard-brand match "setup" intent).
2. Read disambiguates_against field de chaque candidate · extract routing conditions.
3. Apply condition littéralement (e.g. "operator demande pipeline complet day-1 → onboard-brand").
4. If condition unambiguous · invoke matched skill.
5. If condition ambiguous OR contradictory · proceed §6 AskUserQuestion gate.
```

**Pattern miroir extension_hooks.** `disambiguates_against` field canon frontmatter pattern miroir `extension_hooks` field (cf `extension-discovery-discipline.md` §3). NEW canon fields opt-in v2.76+ · backward compat strict pour skills legacy sans field déclaré.

**Cardinality.** `disambiguates_against` enum cap 3 sibling skills max. Au-delà · split skill OR refactor mapping CLAUDE.md pour clarifier scope. Évite drift routing tree complexity.

**AskUserQuestion gate.** Si après disambiguation rules application 2+ skills restent ambigus, agent invoke AskUserQuestion avec 2-3 options labelled (e.g. *"audit pixel + tracking → audit-setup ; audit performance budget allocation → audit-meta-account ; audit copy creative → analyze-copy"*). Opérateur arbitre routing final.

---

## 6. `/scope` fallback canon

Quatrième étape canon · si l'opérateur engage sujet précis sans skill clair en mapping ET sans match manifest, agent invoque `/scope {sujet}` AVANT freestyle prose.

**Pattern canon `/scope`** · slash command shipped v2.76+ workspace-template canon. Transforme intention floue (sujet macro à apprendre OU système à construire) en carte des paramètres décidables.

**Flow canon scope fallback** ·

```
1. Agent detect intent flou · operator engage sujet précis ("aide-moi à comprendre paid media DTC scaling")
2. Mapping explicite scan · zéro match
3. Manifest registry scan · zéro skill triggers match
4. Agent invoke /scope {sujet} via slash command
5. /scope cartographie paramètres décidables · output dual (Excalidraw spatial + markdown drill)
6. /scope termine sur décisions actionnables · operator arbitre prochaine étape
7. Decision actionnable → skill canon mappé OR backlog create-skill flag
```

**Modes /scope canon · LEARN vs BUILD** ·

- **LEARN mode** · pédagogie domaine. Opérateur veut comprendre paramètres d'un sujet macro avant de l'engager (e.g. *"scope paid media DTC scaling"*). Output · cartographie variables structurelles + heuristiques décision + parcours pédagogique.
- **BUILD mode** · scoping construction. Opérateur veut construire système opérationnel encodé (e.g. *"scope agent setup pour social media monitoring"*). Output · cartographie scope opérable + dépendances + skills consumables.

**Anti-pattern `/scope` sur-déclenché.** `/scope` n'est PAS le réflexe par défaut. Procrasti garde-fou · agent invoque `/scope` UNIQUEMENT quand mapping + manifest scan ont échoué AND opérateur engage sujet précis flou. Sinon · skill canon mappé OR conversation libre (cf §3 exception).

**Pattern miroir /bird.** Doctrine sœur · `/bird` (slash command shipped v2.76+) lit la carte produite par `/scope`, ne la crée pas. Pattern canon · `/scope` produit cartographie (mining cognitif) · `/bird` consomme cartographie (orientation territoire). Cross-ref §13.

---

## 7. Freestyle last resort

Cinquième étape canon · uniquement si `/scope` confirme zéro skill canon ne s'applique au sujet (rare · candidat backlog `create-skill` flag).

**Flow canon last resort** ·

```
1. /scope output cartographie paramètres décidables
2. Agent constate · aucun skill canon mappé OR manifest ne couvre l'output stratégique demandé
3. Agent flag gap explicit à l'opérateur · "Ce besoin n'a pas de skill canon. On peut soit (a) freestyle prose maintenant et créer le skill plus tard via create-skill, soit (b) créer le skill d'abord pour matrices canon consumées."
4. Operator arbitre · accept freestyle now (rare) OR invoke create-skill first (default canon)
5. If freestyle accepted · agent ship prose avec disclaimer "skill canon TBD · output non-canonical · qualité 60-70% sans matrice"
6. If create-skill invoked · agent scaffold NEW skill via meta-skill canonical · ship next invocation matrices consumed
```

**Anti-pattern · freestyle silent.** Agent freestyle prose stratégique sans flag gap à l'opérateur · trust cassé · opérateur ne sait pas que le skill canon manque. Pattern canon · gap flag MANDATORY avant freestyle.

**Anti-pattern · freestyle systémique.** Agent freestyle par défaut sur outputs stratégiques au lieu d'invoquer skill canon mappé. Output dégradé · matrices canon ignorées · qualité 60% au lieu de 95% (cf `canonical-matrix-reasoning.md`).

**Decision-aid `create-skill` vs freestyle** · agent recommande `create-skill` si ·

- Output stratégique récurrent (opérateur va le demander à nouveau dans 3+ sessions).
- Pattern composable avec matrices canon existantes (registry angle-mechanics, niveaux-schwartz, etc.).
- Cohérence cross-session critique (e.g. brand-level analysis, audience profiling).

Agent recommande freestyle now si ·

- One-off question ad-hoc (jamais demandé à nouveau).
- Pattern ne consume aucune matrice canon existante (output prose verbal).
- Cohérence cross-session non-critique (e.g. debug technical, discussion doctrine).

---

## 8. Anti-patterns canonisés

### Anti-pattern 1 · Freestyle prose réflexe sur output stratégique

Agent reçoit demande stratégique (audience, angle, brief copy, etc.) et freestyle prose libre au lieu d'invoquer skill canon mappé. Output dégradé · matrices canon (hooks, angles, niveaux-schwartz, registry angle-mechanics) ignorées · qualité 60% au lieu de 95%. Pattern canon · scan mapping CLAUDE.md FIRST · si match · invoke skill canon via Task tool · jamais freestyle si match canon.

### Anti-pattern 2 · Skill mis-trigger

Agent invoque le mauvais skill (e.g. `decompose-ad` pour un brief copy alors que `produce-copy-brief` est canon). Pattern canon · disambiguation rules application littérale via `disambiguates_against` field manifest · AskUserQuestion gate si encore flou · jamais pick au hasard.

### Anti-pattern 3 · Skill sibling créé sans nécessité

Agent face à un besoin proche d'un skill existant propose un skill frère NEW au lieu d'étendre l'existant. Pattern canon `extend_before_create` (memory verrouillé) · vérifier d'abord si skill existant peut être étendu (nouveau mode, nouvelle phase, input conditionnel) AVANT de proposer skill frère · skill frère duplique souvent logique de gate et fragmente mental model opérateur.

### Anti-pattern 4 · `/scope` sur-déclenché par défaut

Agent invoque `/scope` comme premier réflexe sur toute demande au lieu d'utiliser mapping + manifest scan d'abord. Procrasti pattern · opérateur reçoit cartographie quand il voulait action directe. Pattern canon · `/scope` UNIQUEMENT quand mapping + manifest scan ont échoué AND opérateur engage sujet précis flou · garde-fou anti-procrasti respecté.

### Anti-pattern 5 · Freestyle silent sans gap flag

Agent freestyle output stratégique sans flag à l'opérateur que skill canon manque. Trust cassé · opérateur ne sait pas la qualité dégradée vs canonical. Pattern canon · gap flag MANDATORY avant freestyle · propose `create-skill` si récurrent OR accept freestyle avec disclaimer si one-off.

### Anti-pattern 6 · Manifest scan absent runtime

Agent ship avec connaissance mapping CLAUDE.md hardcoded mais zéro scan `.skills/_manifest.json` runtime. NEW skills shippés par `create-skill` ignorés silencieusement (mapping CLAUDE.md pas encore amended). Pattern canon · manifest scan systémique fallback v2.56+ couvre les NEW skills non-encore mappés.

### Anti-pattern 7 · Disambiguation rules ignorées

Agent face à 2+ skills matchant pick au hasard ou via heuristique freestyle au lieu de lire `disambiguates_against` field manifest. Routing inconsistent · drift session-to-session. Pattern canon · `disambiguates_against` lecture mandatory AND application littérale · AskUserQuestion fallback si encore flou.

---

## 9. Cycle d'apprentissage canon

**Boucle complète intent opérateur → skill canon zéro friction** ·

```
1. Opérateur ship demande stratégique (e.g. "produis-moi un angle paid sur audience workers-shifts")
2. Agent scan mapping explicite CLAUDE.md (§3) · match "output angles paid" → produce-paid-angles
3. Agent verify subagent_safe + recommended_model (manifest field)
4. Agent invoke produce-paid-angles via Task tool model: sonnet · subagent foreground
5. produce-paid-angles consume formula Obs+Tension+Reframe+Bridge + registry angle-mechanics + niveaux-schwartz
6. Output canonical 95% qualité retourné à agent main
7. Agent main synthesize output operator-facing register adapted (cf voice canon)
8. Operator review · accept proposed OR adjust OR challenge
9. If challenge ambigu · /scope fallback (e.g. operator demande "explore variants angle") · operator arbitre
10. Next invocation · agent learn pattern · routing canonical zéro friction
```

**Pas de friction routing.** Pas de freestyle réflexe. Pas de skill mis-trigger. Pattern canon · mapping FIRST + manifest scan SECOND + disambiguation THIRD + /scope FALLBACK + freestyle LAST RESORT = boucle complète zéro friction.

**Audit trail traçable.** Tout invocation skill canon annote audit log `routing_path: [mapping_match | manifest_match | disambiguation_applied | scope_fallback | freestyle_last_resort]` · opérateur drill 360° lineage routing decision. Pattern miroir `extensions_consumed` annotation (cf `extension-discovery-discipline.md` §6).

**Pattern miroir CMR.** Cycle d'apprentissage routing pattern miroir `canonical-matrix-reasoning.md` cycle validation atlas vivant · routing canon UPSTREAM (cette doctrine) + matrice canon DOWNSTREAM (CMR) = qualité output 95% bout-en-bout.

---

## 10. Decision-aid Q1-Q3 pour routing strict

Quand agent reçoit demande stratégique opérateur, déterminer routing optimal via 3 questions ·

```
Q1 · L'output demandé match-il un mapping explicite CLAUDE.md ?
   - Oui · invoke skill canon mappé via Task tool (subagent_safe + recommended_model verified)
   - Non · proceed Q2

Q2 · Scan _manifest.json registry · combien de skills match les triggers FR+EN ?
   - 1 skill match · invoke via Task tool
   - 2+ skills match · proceed Q3
   - 0 skills match · proceed /scope fallback §6

Q3 · Disambiguation rules canon · `disambiguates_against` field lecture
   - Condition unambiguous · invoke matched skill
   - Condition ambiguous · AskUserQuestion gate avec 2-3 options labelled
   - Condition contradictory · flag amendment doctrine (cf doctrine-governance.md)
```

**Output** · routing decision = mapping_match OR manifest_match OR disambiguation_resolved OR scope_fallback OR freestyle_last_resort (jamais 2+ simultaneously).

**Validation AskUserQuestion** · uniquement si Q3 disambiguation rules application laisse ambiguity résiduelle. Opérateur arbitre routing final · agent execute.

**Edge case Q1 mapping ambigu** · si demande operator match 2+ entries mapping explicite (rare · mapping conçu MECE), agent flag amendment doctrine pour clarifier scope mapping · backlog `doctrine-governance.md`.

---

## 11. Backward compat strict additif

Skill Routing Discipline est strict additif par construction. Garanties ·

**11.1 Mapping CLAUDE.md verrouillé v2.55 baseline préservé.** 20+ entries mapping output → skill verrouillées canon · skills legacy v2.55-v2.74 routing comportement identique post-doctrine ship. Aucune régression routing.

**11.2 Field `disambiguates_against` NEW additif manifest.** Schema manifest v2.67+ append-only · NEW field optional per skill registered. Skills pré-v2.76 sans field déclaré · still valid · disambiguation skip vers AskUserQuestion gate fallback (cf §5).

**11.3 Manifest scan canonical v2.56+ préservé.** Fallback systémique manifest existait déjà v2.56+ baseline · cette doctrine canonise + structure le pattern, n'override pas l'existant. Backward compat strict.

**11.4 `/scope` fallback NEW v2.76+.** Slash command shipped workspace-template v2.76+ · skills pré-v2.76 routing fallback comportement freestyle prose default (legacy). v2.76+ default · scope fallback canon AVANT freestyle. Migration path · opérateurs v2.55-v2.75 upgrade gain scope fallback layer · pas de breaking.

**11.5 Migration path v2.76 → v2.77+.** Sprint patch progressif · v2.76.0 ship doctrine + /scope + /bird slash commands canon. v2.77+ extend disambiguates_against field coverage skills additionnels (audit-google-pmax, audit-setup, etc.) selon priorité opérateur. Pas de breaking migration.

---

## 12. Position dans le système opérationnel 5 couches

Skill Routing Discipline opère sur 3 couches simultanément du multiplicatif Operational System Discipline v2.71 ·

**Couche 2 · Règles (heuristiques décision).** Skill Routing Discipline canon EST une heuristique de décision · mapping FIRST → manifest SECOND → disambiguation THIRD → /scope FALLBACK → freestyle LAST RESORT. Pattern miroir `dependency-resolution-protocol.md` L1+L2+L3 gap-filling Step 0bis canon v2.38+.

**Couche 4 · Métriques (boucles feedback).** Routing audit trail `routing_path: [...]` annoté output · opérateur traçabilité full · operator drill 360° lineage routing decision. Pattern miroir `extensions_consumed` annotation (cf `extension-discovery-discipline.md` §6) et `confidence_chain` (cf `confidence-propagation.md`).

**Couche 5 · Rituels (cadence opérationnelle).** Routing rituel canon agent par invocation · scan mapping + manifest + disambiguation systémique chaque demande stratégique. Pattern miroir `learn-from-session` Trigger 8 smart-suggest daemon (cf `pattern-detection-triggers.md`).

**Doctrines sœurs canon** ·

- **Canonical Matrix Reasoning (CMR)** · qualité output post-routing · doctrine sœur DOWNSTREAM · skill canon invoqué produit output 95% via schema + matrice canon · routing canon UPSTREAM + matrice canon DOWNSTREAM = qualité bout-en-bout.
- **Investigation Posture** · 5 sections rigueur réponse · doctrine sœur post-skill · skill canon ship output structuré observé/déduit/inconnu/leviers/close ouvert · routing canon + posture investigation = qualité réponse strategique.
- **Extension Discovery Discipline** · pattern miroir frontmatter discovery · `extension_hooks` field pattern miroir `disambiguates_against` field · backward compat strict additif identique · NEW canon fields opt-in v2.76+.

---

## 13. Cross-references

- `canonical-matrix-reasoning.md` (CMR) · qualité output post-routing · doctrine sœur DOWNSTREAM · schema + matrice canon production 95% qualité
- `investigation-posture.md` · 5 sections rigueur réponse post-skill · doctrine sœur drill-down · observé/déduit/inconnu/leviers/close ouvert
- `extension-discovery-discipline.md` · pattern miroir frontmatter canon · `extension_hooks` field miroir `disambiguates_against` field · backward compat strict identique
- `operational-system-discipline.md` v2.71 · doctrine mère 5 couches multiplicatives · cette doctrine instance multi-couches (2 + 4 + 5)
- `dependency-resolution-protocol.md` (DRGFP) · pattern miroir heuristique L1+L2+L3 gap-filling pre-flight
- `confidence-propagation.md` · audit trail pattern miroir `routing_path` annotation
- `skill-authoring-doctrine.md` (SAD) · `disambiguates_against` frontmatter field validation · type taxonomy producer/curator/orchestrator routing eligibility
- `schema-encoding-discipline.md` (SED) · substrate ontologique · `disambiguates_against` field append-only mutation gate manifest
- `pattern-detection-triggers.md` · 8 triggers learn-from-session · pattern miroir rituel cadence couche 5
- `doctrine-governance.md` · amendment process append-only D# verrouillé · cette doctrine entry registry append-only post-ship

**Slash commands canon v2.76+** ·

- `/scope` (shipped v2.76+) · cartographie paramètres décidables · LEARN vs BUILD modes · fallback routing canonical step 4
- `/bird` (shipped v2.76+) · vue d'ensemble territoire · consomme cartographie /scope · orientation reprise session

**Registry canon** ·

- `.skills/_manifest.json` · pre-built registry index regenerated via `python3 .skills/build-manifest.py` post-skill add/edit/rename/archive
- `CLAUDE.md` § Skill routing mapping verrouillé v2.55 baseline · 20+ entries canon

**Future v2.77+** ·

- Extend `disambiguates_against` field coverage skills additionnels (audit-google-pmax, audit-setup, analyze-perf, etc.) selon priorité opérateur
- Audit complet routing patterns post-/scope adoption · classification freestyle last resort frequency
- NEW field validation `disambiguates_against` enum via `validate-resources` skill (warning level jusqu'à v2.78 puis enforcement)

---

## Status

- **Canonique v2.76+.** Doctrine canon · codifie protocole routing strict 5 phases · mapping FIRST → manifest SECOND → disambiguation THIRD → /scope FALLBACK → freestyle LAST RESORT.
- **Doctrine sœur** · Canonical Matrix Reasoning (qualité output DOWNSTREAM) · Investigation Posture (rigueur réponse post-skill) · Extension Discovery Discipline (pattern miroir frontmatter canon).
- **Backward compat** · strict additif · doctrine NEW n'override aucune existing. Mapping CLAUDE.md v2.55 baseline préservé. `disambiguates_against` field NEW additif manifest v2.76+. `/scope` fallback NEW v2.76+ default · skills pré-v2.76 freestyle fallback legacy.
- **First applications** · routing canonical 70+ skills shipped workspace-template v2.76+. Decision-aid §10 Q1-Q3 applicable agent main thread chaque demande stratégique. Pipeline routing §6 applicable tous skills production opt-in `disambiguates_against` declaration.
- **Promotion criterion** · à reviewer après 10+ skills additionnels patched avec `disambiguates_against` field + 5+ `/scope` invocations successful fallback routing + 1 audit systémique routing patterns frequencies (mapping_match vs manifest_match vs scope_fallback vs freestyle_last_resort).

---

*Doctrine canonique skill-author-facing + agent-facing. Canonise protocole routing strict 5 phases · scan manifest FIRST · disambiguation rules · /scope fallback · freestyle last resort. Ferme gap structurel agent LLM freestyle réflexe vs skill canon production. Pattern miroir extension-discovery-discipline.md (frontmatter canon discovery) et canonical-matrix-reasoning.md (qualité output DOWNSTREAM).*
