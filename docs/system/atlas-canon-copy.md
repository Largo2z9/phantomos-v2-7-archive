# Atlas Canon Copy

> **Note disambiguation v2.36** · "atlas" désigne 4 sens distincts en PhantomOS (cf `lexicon.md § Atlas, 4 senses MECE`). Ce document couvre le **sense 1 · atlas canon copy** (référentiel cross-brand doctrine copywriting, read-only, partagé tous brands). Pour la cartographie holistique data d'une brand spécifique (sense 4), voir `docs/system/atlas-brand.md`.

> **Note terminologique** : "atlas" désigne 3 concepts distincts en PhantomOS. Ce document couvre **Atlas Canon Copy** (référentiel cross-brand doctrine, sense 1). Pour atlas vivant brand-spécifique (sense 2) et atlas state modulator reporté (sense 3), consulter `lexicon.md § Atlas, 3 senses MECE`.

> Doctrine atlas canon copy. Référentiel typé partagé cross-brands. Fondation v2.26.0 (11 couches, 58 fiches seedées, schema `canon-tool/1.0`), boucle bidirectionnelle v2.27.0 (4 skills consume + feed). Décisions canon : D#382, D#383, D#391.

---

## 1 · Qu'est-ce que l'atlas canon copy

L'atlas canon copy est le référentiel typé des outils canoniques du copywriting (frameworks, hooks, archétypes, niveaux Schwartz, objections, etc.) que les skills consomment au lieu de les réinventer à chaque session. Une fiche par outil, schema standardisé `canon-tool/1.0`, location `resources/canon/copy/{layer}/{tool}.json`. Source canon : Schwartz, Cialdini, Halbert, Sugarman, Hormozi, Carlton, Jung, Boron. Objectif : un seul vocabulaire typé, partagé cross-brands, qui apprend de l'usage.

---

## 2 · Pourquoi l'atlas

Avant l'atlas, chaque skill producer reconstituait ses outils canon depuis le néant ou interpolait à partir de fragments épars dans des SKILL.md, des research notes, ou la mémoire du modèle. Conséquence : drift terminologique session-à-session, output non-traçable (pas de lignage canon), zéro compound sur la connaissance brand-side.

Avec l'atlas :
- Skills piochent dans un menu typé (`when_works`, `when_avoid`, `combines_with`, `anti_patterns`, `examples`).
- Output taggé avec les `canon_*_id` sélectionnés, lignage explicite.
- `validations[]` append-only transforme l'atlas générique en atlas vivant brand-spécifique au fil de l'usage. Après 2-3 mois de prod, le brand a son canon validé empiriquement (quel framework converti chez ce ICP, quel hook a fatigué, etc.).

Compound réel, pas slogan : la valeur monte avec le temps.

---

## 3 · 11 couches actuelles

| # | Couche | Quoi | Source canon |
|---|---|---|---|
| 1 | `frameworks` | Structures de copy (PAS, AIDA, BAB, FAB, QUEST, 4Ps) | Halbert · Sugarman |
| 2 | `hooks` | Patterns d'amorce (curiosity-gap, contrarian, etc.) | Sugarman · Hormozi |
| 3 | `angles` | Sources d'angle (audience-derived, product-derived, mechanism, etc.) | Schwartz |
| 4 | `niveaux-schwartz` | Conscience × sophistication, matrice 5x5 | Schwartz |
| 5 | `archetypes-voix` | 12 archétypes Jung (héro, sage, magicien, etc.) | Jung |
| 6 | `formules-titres` | Structures de titre canoniques | Carlton · Halbert |
| 7 | `objections` | Patterns d'objection + traitement canon | Sugarman · Cialdini |
| 8 | `construction-offre` | Structuration d'offre (value stack, irrésistibilité) | Hormozi |
| 9 | `leads` | Types de leads (offer-led, story-led, problem-led, etc.) | Schwartz · Boron |
| 10 | `formats-livrables` | Sales letter · VSL · email · ad · landing · etc. | Halbert · industrie |
| 11 | `heuristiques-persuasion` | Cialdini × 7 + dérivés | Cialdini |

Total v2.26.0 : 58 fiches seedées. Extension future via promotion canon (cf §6).

---

## 4 · Schema canon-tool/1.0

Référence : `resources/schemas/canon-tool.schema.json`. Champs canoniques :

| Champ | Rôle |
|---|---|
| `id` | Identifiant unique stable de la fiche (ex: `framework_pas`) |
| `principle` | Postulat canon en 1-2 phrases : pourquoi cet outil existe |
| `structure` | Forme de l'outil (étapes, blocs, ratios) |
| `gabarits[]` | Templates concrets utilisables tels quels |
| `when_works[]` | Conditions d'application : audience, niveau Schwartz, format, intention |
| `when_avoid[]` | Conditions de contre-indication explicites |
| `combines_with{}` | Outils canon compatibles (autres ids) avec note de combinaison |
| `anti_patterns[]` | Symptômes d'usage incorrect, traçables au runtime |
| `examples[]` | Cas concrets, idéalement sourcés (brand, campagne, résultat) |
| `validations[]` | Append-only. Outcomes empiriques captés brand-side (cf §5.2) |
| `lineage{}` | Sources canon (auteur, ouvrage, année), version de la fiche |

Toute mutation passe par le mutation gate ; `validations[]` est append-only par design (operator gate explicite).

---

## 5 · Bidirectional canon contract (skills ↔ canon)

Le contrat est bidirectionnel. Un skill qui touche un domaine canon DOIT consommer le canon, et SI il capture des outcomes, il DOIT proposer des promotions canon.

### 5.1 · Consume pattern (skills lisent canon)

Chaque skill producer/curator qui produit du copy charge les couches canon pertinentes en Step 0bis avant production. Implémentations de référence v2.27 :

| Skill | Étape | Couches consommées |
|---|---|---|
| `produce-paid-angles` | Step 0bis canon load · Step 11 LIGNAGE output | frameworks, hooks, angles, niveaux-schwartz, archetypes-voix |
| `produce-copy-brief` | Bloc LIGNAGE en tête + consume canon downstream | archetypes-voix, objections, leads, formats-livrables (lit lignage angle source) |
| `mine-voc` | Step 3 4-lens coding · canon tagging additif | niveaux-schwartz (`canon_schwartz_conscience_id`), `canon_emotion_id`, objections (`canon_objection_pattern_id`) sur chaque verbatim Layer A |

Output taggé : un brief produit liste explicitement `audience`, `schwartz_stage`, `hook_canon_id`, `framework_canon_id`, `angle_canon_id`, `archetype_canon_id`, `pain_extract`, `proof`, `cta`. Persistance brand-side : `brands/{slug}/angles/{ANG-N}.json`.

### 5.2 · Feed pattern (skills alimentent canon)

`learn-from-session` est le skill canonique de promotion canon. Quand une session capture un outcome (ROAS, fatigue créa, validation opérateur explicite, correction opérateur), le skill détecte quel outil canon a été utilisé en prod, et propose une entry dans `resources/canon/copy/{layer}/{tool}.json#/validations[]`.

Trois invariants :
1. **Operator gate explicite.** Jamais auto-promote. La promotion canon attend confirmation avant écriture.
2. **Append-only.** Les validations historiques persistent, datées, jamais réécrites. Drift visible dans le temps.
3. **Tracé canon → brand.** Chaque entry pointe le `canon_id` consommé, le brand, la session, et l'outcome.

Effet compound : `/phantom canon copy hooks curiosity-gap` rend la fiche canon + l'historique des validations brand-side du tenant. L'atlas générique devient atlas vivant.

---

## 6 · Mécanisme de l'atlas vivant

L'atlas vivant émerge mécaniquement du contrat bidirectionnel :

1. Skills consomment canon générique au démarrage (skill author n'invente rien).
2. Output produit en prod avec lignage canon explicite.
3. Outcomes captés (perf media, validation opérateur, correction).
4. `learn-from-session` propose promotion via `validations[]` (operator gate).
5. Prochaine session : skill recharge canon enrichi des validations brand-side.

Après 2-3 mois d'usage cohérent, un brand a un canon validé empiriquement, pas hérité aveuglément. C'est la valeur compound réelle. Les vues `matrix/copy-matrix/copy-map` (visualisation atlas vivant) sont différées tant que pas de données réelles ; D#391 acte la patience structurelle.

---

## 7 · Best practices

- Consommer canon TOUJOURS via canon read helpers, jamais hardcoder un outil dans un SKILL.md ou un script.
- Tagger output avec les `canon_*_id` consommés. Lignage absent = output non-traçable = bug.
- Si un outil canon manque, signaler à l'opérateur via candidat de promotion, pas hardcoder en local.
- Lire `when_avoid` avant de combiner deux outils. `combines_with` ne dispense pas du check de contre-indication.
- Filtrer la sélection canon par contexte (audience, niveau Schwartz, brand voice) avant de pousser au modèle, pas après.

---

## 8 · Anti-patterns

| Symptôme | Pourquoi c'est un problème | Fix |
|---|---|---|
| Skill génère copy from scratch sans Step 0bis canon load | Duplication du canon dans le code skill, drift terminologique inévitable | Charger canon en Step 0bis, piocher, tagger |
| `validations[]` écrites sans operator gate | Atlas pollué par hypothèses non validées, compound brisé | `learn-from-session` enforce operator confirm avant write |
| `canon_*_id` absents du LIGNAGE output | Impossible de tracer la composition, donc impossible de capter outcome | Schema producer enforce les champs canon dans Layer B |
| Hardcode d'un outil canon en local au lieu de read | Drift entre skill et canon, plus rien n'apprend | Canon read helpers obligatoires, refus convention-guard |
| Skip du Step 0bis canon load | Skill produit dans le néant, output générique | SAD § Bidirectional canon contract enforce Step 0bis |
| Lecture `combines_with` sans check `when_avoid` | Combinaison contradictoire shippée, output incohérent | Best practice §7, à terme hook lint |

---

## 9 · Roadmap atlas

- **v2.26.0** ✓ fondation 11 couches × 58 fiches seedées · schema `canon-tool/1.0` · D#382 D#383
- **v2.27.0** ✓ 4 skills consume + feed (produce-paid-angles, produce-copy-brief, mine-voc, learn-from-session) · D#391
- **v2.37.0** ✓ schema canon-tool v1.0 → v1.1 · attribution_layer + freshness/decay TTL + isolation boundary sur `validations[]` · adresse red team A1/A4/A5/A7. Cf §11.
- **Différé** : autres atlas (paid, brand, offer, funnel, cro, email, analytics, mining). Décision : on attend 2-3 mois de prod sur canon copy d'abord, on capitalise les patterns d'authoring atlas, on généralise ensuite.
- **Différé** : vues `matrix/copy-matrix/copy-map` tant que validations[] n'est pas peuplé en prod réelle.

---

## 11 · Schema v1.1 (v2.37+)

> Patch fondation 3 v2.37 · attribution layer + freshness/decay TTL + isolation boundary sur `validations[]`. Adresse red team findings A1 (stale data injection), A4 (atlas vivant runaway lock-in), A5 (validations failed sans attribution imputable), A7 (cross-brand contamination).

### 11.1 · Pourquoi v1.1

Schema v1.0 acceptait des entries `validations[]` sans imputabilité ni decay. Trois failles structurelles :

1. **A5 imputabilité.** `outcome: failed` sans `attribution_layer` pollue le canon · un échec ciblage est attribué à un échec de hook, le canon dégrade silencieusement.
2. **A4 lock-in.** Un winner précoce alimente `validations[]`, le skill suivant le privilégie, monoculture s'installe sans relecture des outcomes plus récents ou de signaux contradictoires fraîchement captés.
3. **A7 cross-contamination.** Un brand peut lire les `validations[]` d'un autre brand par défaut, le compound brand-side se mélange.

### 11.2 · 5 fields requis sur entries v1.1

| Field | Type | Rôle |
|---|---|---|
| `brand_slug` | string | Isolation boundary. Scope read = brand seul par défaut. Override via operator gate explicite uniquement. |
| `attribution_layer` | enum 10 valeurs (`hook`, `angle`, `framework`, `archetype`, `format`, `targeting`, `budget`, `creative_execution`, `timing`, `unknown`) | À quoi est attribué le signal. `unknown` autorisé mais déclenche AskUserQuestion gate avant write. Bloque pollution atlas vivant par signaux non-imputables. |
| `validated_at` | date `YYYY-MM-DD` | Date validation. Base du calcul decay. |
| `decay_ttl_days` | integer >= 30 (default 90) | TTL stale. Override par skill autorisé (ex 30 jours formats TikTok fast-decay, 180 jours benefit chains slow-decay). |
| `_isolation_boundary` | const `"brand"` | Auto-set on write. Enforce brand-only scope. |

### 11.3 · Backward compat lecture

Entries v1.0 existantes restent lisibles. Quand un consumer (skill, query) rencontre une entry v1.0 :
- `attribution_layer` absent → traité comme `"unknown"`, signalé en lineage.
- `validated_at` absent → fallback sur `captured_at` (v1.0 ISO date-time).
- `decay_ttl_days` absent → default 90 jours appliqué pour le calcul stale.
- `_isolation_boundary` absent → traité comme `"brand"`.

Mutation enforcement (refus de write) **seulement sur new writes v2.37+**. Migration entries v1.0 non requise · tolerance lecture additive.

### 11.4 · Decay filter au moment promotion

`learn-from-session` (et tout consumer canon) filtre `validations[]` au moment où elles influencent une décision (promotion canon, sélection top signal, recommandation skill) :

```
si today > (validated_at + decay_ttl_days) → entry stale
```

Stale entries restent dans le log (append-only) mais sont surfacées comme `state: stale` dans le recap operator. Si une stale entry était top signal pour une promotion, opérateur doit re-tester ou override explicite.

### 11.5 · Cross-ref

Doctrine confidence chain (propagation, min-chain, gate >= 0.7) → `docs/system/confidence-propagation.md`. Decay s'articule avec confidence chain pour le filtre eligibility de promotion canon.

---

## 12 · Cross-refs

- `resources/canon/copy/{layer}/{tool}.json` : location physique des fiches.
- `resources/schemas/canon-tool.schema.json` : schema fiche, source de vérité.
- `docs/system/skill-authoring-doctrine.md § Bidirectional canon contract` : pattern skill author obligatoire.
- `docs/system/canonical-matrix-reasoning.md` : doctrine production qualité 95% qui consomme atlas.
- `docs/system/schema-encoding-discipline.md` : substrate (mutation gate, append-only, sourcing tags) qui sous-tend `validations[]`.
- `decisions.md` D#382 (atlas fondation), D#383 (schema canon-tool/1.0), D#391 (boucle bidirectionnelle skills consume + feed).
