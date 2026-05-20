---
name: claude-md-discipline
description: Doctrine canon racine · pattern canon pour TOUT CLAUDE.md (root workspace-template + pillars + brand). Instructions atomiques impératives · 3 CRITICAL/YOU MUST max · zéro versioning inline · zéro narrative doctrinale · zéro inventaire pollution. Test de suppression obligatoire avant ajout règle.
type: doctrine
version: v2.82.0
status: shipped
---

# Claude.md Discipline · Operating Doctrine

> Canonique v2.82.0. Doctrine canon racine qui codifie le pattern canon pour TOUT fichier `CLAUDE.md` PhantomOS (root workspace-template plus pillars `00-meta/` `01-marketing/` `02-ai/` `03-product/` `04-brand/` `05-projects/` `06-agency/` plus project `context-engine/` `abyss/build/` plus brand `brands/{slug}/`). Instructions atomiques impératives uniquement. Doctrines détaillées vivent dans `docs/system/*.md`. Versioning vit dans `CHANGELOG.md`. Inventaires détaillés vivent dans `docs/system/README.md`. Le CLAUDE.md root pointe, n'explique pas. Doctrine sœur de `voice.md` (registre prose · cohérent atomicité impératif), `output-clarity-doctrine.md` v2.79.2 (standards Vercel/GitHub-grade outputs opérateur-facing · cohérent forme canon), `operational-system-doctrine.md` v2.71 (mère 5 couches · CLAUDE.md fait partie de la couche templates). Ferme le gap *"CLAUDE.md root workspace-template viole ses propres règles · 9 problèmes structurels (taille dépassée · inflation marqueurs priorité · règles-sandwich · méta-doctrine · chevauchements MECE · versioning inline · pollution narrative · point-médian listes plates · auto-références cycliques) · LLM ignore uniformément les règles au-delà capacité attention ~150-200 instructions distinctes · negative ROI territory"* flag systémique Sprint v2.82 post-audit externe Claude Web sur CLAUDE.md root v2.81.1.

---

## 1. Thèse fondatrice

> CLAUDE.md est un fichier d'instructions opérationnelles pour LLM runtime, PAS un manifeste doctrinal pour humains. Instructions atomiques impératives uniquement. Doctrines détaillées vivent dans `docs/system/*.md`. Versioning vit dans `CHANGELOG.md`. Inventaires détaillés vivent dans `docs/system/README.md`. Le CLAUDE.md root pointe, n'explique pas.

**Définition canon CLAUDE.md** · fichier d'instructions opérationnelles auto-loaded par Claude Code en runtime. Format atomique impératif (1 règle = 1 instruction · max 2 lignes). Test de suppression obligatoire avant chaque ajout · *"si je retire cette ligne, quelle erreur concrète Claude fait ?"*. Réponse vague → la ligne sort. CLAUDE.md canon répond à 4 questions miroir ·

1. *"Chaque ligne est-elle reformulable en `Claude doit X` / `Claude ne doit pas X` / `Claude vérifie X` ?"* (atomicité impératif · zéro narrative doctrinale)
2. *"Le fichier respecte-t-il la taille canon de son niveau (root 150 · pillar 100 · project 120 · brand 80) ?"* (capacité attention LLM runtime)
3. *"Les marqueurs de priorité (CRITICAL + YOU MUST + IMPORTANT cumul ≤3 · NEVER majuscules ≤10) restent-ils parcimonieux ?"* (inflation détruit signal priorité)
4. *"Les doctrines détaillées vivent-elles dans `docs/system/*.md` plutôt qu'inline ?"* (CLAUDE.md pointe · n'explique pas)

**Différenciation canon vs CLAUDE.md narratif** ·

| Layer | CLAUDE.md narratif (anti-pattern) | PhantomOS canon Claude.md Discipline |
|---|---|---|
| Format | prose doctrinale humain-facing | instructions atomiques impératives LLM-facing |
| Taille root | 200-300+ lignes (capacité attention LLM dépassée) | ≤150 lignes strict |
| Marqueurs priorité | CRITICAL × 7 · YOU MUST × 8 · NEVER × 30 (inflation) | CRITICAL + YOU MUST + IMPORTANT cumul ≤3 · NEVER ≤10 |
| Versioning | v2.55/v2.79.5/v2.81.1+ inline partout | zéro version inline · vit dans CHANGELOG.md |
| Doctrines détaillées | inline expanded dans CLAUDE.md | externalisées vers `docs/system/*.md` · pointer unique |
| Inventaire doctrines | 24 entries en prose détaillée | pointer unique vers `docs/system/README.md` |
| Brand positioning | présent ("PhantomOS does not fill forms") | absent · vit dans surface marketing |
| Justifications | emballées avec instruction (règles-sandwich 4-5 lignes) | externalisées vers doctrine concernée |
| Auto-références | cross-refs cycliques inline + externe | inline OU doc externe · jamais les deux |
| Test ROI ajout règle | absent · ajout par accumulation | test de suppression obligatoire avant ajout |

CLAUDE.md narratif signale que le mainteneur écrit pour humain (collègue mainteneur · lecteur curieux). CLAUDE.md canon signale que le mainteneur écrit pour LLM runtime · capacité attention bornée · ROI mesurable par instruction. C'est la différence entre manifeste doctrinal (passif) et fichier d'instructions opérationnelles (operable).

Cette doctrine canonise le pattern systémique cross-CLAUDE.md PhantomOS. Tout `CLAUDE.md` root · pillar · project · brand respecte les 4 tailles canon par niveau plus les 8 Hard Rules canon plus les 8 anti-patterns canonisés.

---

## 2. Le problème résolu

Sans Claude.md Discipline canon ·

1. **Capacité attention LLM dépassée silencieusement.** Documenté Anthropic · le modèle ignore uniformément une partie des règles au-delà de ~150-200 instructions distinctes. CLAUDE.md root workspace-template v2.81.1 dépasse 200+ instructions denses · zéro signal opérationnel sur cette dégradation. Mainteneur ajoute règles par accumulation · perception qu'ajouter c'est renforcer · réalité c'est diluer. Negative ROI territory.

2. **CLAUDE.md root viole ses propres règles.** v2.81.1 fixe règle interne *"Root `CLAUDE.md` ≤150 lignes"* et dépasse cette règle dans le même fichier. Incohérence auto-référentielle · perte de crédibilité système · le mainteneur ne sait pas si le fichier doit être respecté littéralement ou non. Audit externe Claude Web a flag ce point en premier.

3. **Inflation marqueurs priorité détruit signal.** v2.81.1 contient CRITICAL × 7 · YOU MUST × 8 · IMPORTANT × 2 · NEVER en majuscules × 30+. Documenté Anthropic · au-delà du seuil cumulé, le modèle ignore tous les marqueurs uniformément. *"Tout est critique"* signifie *"rien n'est critique"*. Priorité perdue · agent traite chaque instruction au même poids · décisions sub-optimales runtime.

4. **Règles-sandwich emballent l'instruction.** Pattern récurrent · 4-5 lignes de justification + brand positioning + bénéfice opérateur + cross-ref + 1 instruction noyée au milieu. Le modèle doit extraire l'instruction · cognitif waste runtime · risque erreur extraction · ROI instruction dégradé.

5. **Méta-doctrine et brand positioning leak.** Phrases type *"PhantomOS does not fill forms · PhantomOS does not ask 47 questions"* sont brand positioning marketing · vivent dans surface landing/about. *"L'opérateur apprend la posture experte en regardant"* est justification doctrinale · vit dans doctrine concernée. Aucune n'est instruction opérationnelle reformulable `Claude doit X` · pollution narrative.

6. **Versioning inline crée maintenance burden.** v2.55/v2.79.5/v2.81.1+ disséminés partout dans CLAUDE.md root signifient que chaque release implique mise à jour cross-référence du fichier. Drift garanti · références obsolètes garanties · zéro valeur ajoutée pour runtime. Versions vivent dans CHANGELOG.md · frontmatters doctrines · manifest releases.

7. **Inventaire 24 doctrines détaillé en prose pollue.** v2.81.1 expose 24 doctrines avec versions, descriptions, cross-refs cycliques inline. ~30 lignes denses qui dupliquent `docs/system/README.md`. Le modèle lit deux fois la même info · capacité attention gaspillée · maintenance burden doublé.

8. **Sections dupliquées fragmentent mental model.** Skill routing apparaît dans 5 sections distinctes (Master rule · Skill routing · Investigation posture · Mutation rule · Skills). Mental model fragmenté · agent doit reconstruire le pattern · erreurs d'application. Pattern canon · 1 section consolidée + sous-règles.

9. **Auto-références cycliques inutiles.** *"Doctrine reference · `docs/system/contextual-intelligence.md`"* + *"Sub-doctrines index · `docs/system/README.md`"* + *"Full canon · `docs/system/skill-routing-doctrine.md`"* multipliés par section. Claude ne suit pas cross-refs en runtime · soit l'info est inline (et l'instruction est complète) · soit elle vit dans doc externe (et le pointer suffit) · jamais les deux dans le même bloc.

Claude.md Discipline = doctrine canon qui ferme ces 9 gaps via 4 tailles canon par niveau + atomicité stricte + marqueurs priorité parcimonieux + zéro versioning inline + zéro narrative doctrinale + zéro inventaire détaillé + format atomique impératif + 8 Hard Rules canon + 8 anti-patterns canonisés + test de suppression obligatoire.

---

## 3. Taille canon par niveau · 4 paliers stricts

Tout `CLAUDE.md` respecte taille canon par niveau ·

| Niveau | Fichier | Taille canon | Rationale |
|---|---|---|---|
| Root | `workspace-template/CLAUDE.md` | ≤150 lignes | capacité attention LLM runtime · auto-loaded en premier · doit rester scannable |
| Pillar | `{pillar}/CLAUDE.md` (`00-meta/` `01-marketing/` etc) | ≤100 lignes | contexte pillar plus restreint que root · sub-routing vers child CLAUDE.md possible |
| Project | `05-projects/{project}/CLAUDE.md` | ≤120 lignes | contexte projet spécifique · build vs release modes · vocabulaire dédié |
| Brand | `brands/{slug}/CLAUDE.md` | ≤80 lignes | contexte brand-specific · règles instance · le plus restreint |

**Test de suppression canon obligatoire avant tout ajout de règle** ·

> *"Si je retire cette ligne, quelle erreur concrète Claude fait ?"*

- Réponse spécifique et observable (*"Claude écrit JSON directement au lieu d'utiliser `write_to_context`"*) → la ligne reste
- Réponse vague (*"Claude perd contexte"* · *"Claude est moins aligné"* · *"l'opérateur ne comprend pas"*) → la ligne sort
- Réponse type *"Claude ne sait plus que cette doctrine existe"* → externaliser vers `docs/system/README.md` index, supprimer la ligne CLAUDE.md

**Mécanisme de croissance contrôlée** ·

- Toute proposition d'ajout passe le test de suppression avant inclusion
- Toute règle inline >2 lignes déclenche externalisation vers doctrine concernée
- Toute section >20 lignes déclenche consolidation ou externalisation
- Toute violation taille canon déclenche audit immédiat (sortir narrative · externaliser doctrines · supprimer inventaire détaillé)

---

## 4. Atomicité stricte · 1 règle = 1 instruction

Format canon obligatoire ·

- 1 règle = 1 instruction reformulable `Claude doit X` / `Claude ne doit pas X` / `Claude vérifie X`
- Max 2 lignes par règle
- Justification externalisée vers doctrine concernée si pèse >1 ligne
- Bullets / tirets une instruction par ligne (recommandation Anthropic explicite)
- Tableau DO / NEVER autorisé canon pour règles binaires opérateur contract

**Anti-pattern règle-sandwich détaillé** ·

```
[ANTI-PATTERN]
- Pre-engagement disclosure obligatoire on `type: orchestrator` OR duration >5min OR 
  spans sessions OR 2+ sub-skills OR producer heavy paid. PhantomOS does not fill forms 
  silently. The operator deserves to know before committing 5 minutes. Without disclosure 
  the operator quits early in 5 profiles out of 6 (cas Abyss central · base tracking-GTM 
  centralisée). Full canon · `docs/system/engagement-disclosure-doctrine.md` v2.79.5.
```

5 lignes · 1 instruction noyée dans brand positioning + cas usage + cross-ref + version inline. Pattern correctif ·

```
[CANON]
- Pre-engagement disclosure obligatoire sur skill orchestrator OR durée >5min OR spans 
  sessions OR 2+ sub-skills OR producer heavy paid
```

2 lignes · 1 instruction atomique impérative. Justification externalisée vers `engagement-disclosure-doctrine.md`. Version inline supprimée (vit dans frontmatter doctrine).

---

## 5. Marqueurs de priorité parcimonieux · seuils canon

Marqueurs priorité canon strict ·

- **CRITICAL + YOU MUST + IMPORTANT** cumul ≤3 par CLAUDE.md (root · pillar · project · brand)
- **NEVER en majuscules** ≤10 par CLAUDE.md
- **DO / NEVER tableau** autorisé canon (regroupe ≤15 paires binaires sans inflation marqueurs)
- Au-delà des seuils, le modèle ignore tous les marqueurs uniformément (documenté Anthropic)

**Mécanisme de calibration** ·

1. Pour chaque CRITICAL / YOU MUST / IMPORTANT candidat, demander · *"Si Claude ignore cette règle, quelle est la sévérité observable ?"*
2. Sévérité catastrophique (perte data · destructive op silencieuse · violation gate persistante) → marqueur justifié
3. Sévérité modérée (output sub-optimal · erreur récupérable) → impératif simple sans marqueur
4. Sévérité faible (préférence stylistique · convention non-load-bearing) → règle sort ou externalisée

**Anti-pattern inflation** ·

```
[ANTI-PATTERN v2.81.1]
- CRITICAL: check `brands/` for real brand folders
- YOU MUST read `.claude/commands/tour.md` NOW
- IMPORTANT: master rule applies before any other gate
- Doctrine reference · `docs/system/contextual-intelligence.md`
- CRITICAL: never edit `.json` under `brands/`
- YOU MUST mutate via `write_to_context`
- IMPORTANT: rebuild snapshot after write to core files
- CRITICAL: pre-engagement disclosure obligatoire
- YOU MUST signal background subagent completion
```

9 marqueurs cumul · seuil ≤3 violé · le modèle ignore uniformément. Pattern correctif · ne garder marqueurs que sur 3 règles maximum dont la violation est catastrophique. Les autres deviennent impératifs simples (*"Claude check `brands/`"* · *"Claude mutate via `write_to_context`"*).

---

## 6. Zéro versioning inline

Règle canon stricte · aucun marqueur version (v2.55 · v2.79.5 · v2.81.1+ · etc) ne vit dans CLAUDE.md ·

- Versions vivent dans `CHANGELOG.md`
- Versions vivent dans frontmatters des doctrines (`docs/system/*.md`)
- Versions vivent dans `_version.json` workspace-template
- Versions vivent dans manifest releases (`docs/releases/{version}-manifest.json`)

**Rationale** ·

- Le CLAUDE.md est valide ou pas · son contenu ne change pas avec la version
- Les changements sémantiques shippent via doctrine plus skill plus surface ad-hoc · pas via réécriture CLAUDE.md
- Versioning inline crée maintenance burden cross-référence à chaque release
- Drift garanti · références obsolètes garanties · zéro valeur ajoutée runtime

**Exception canon** · le frontmatter du CLAUDE.md (s'il en a un) peut contenir `version` pour signal canonicité globale. Le contenu du fichier n'expose aucune version inline.

---

## 7. Zéro narrative doctrinale

Test mental canon obligatoire pour chaque phrase ·

> *"Cette phrase est-elle reformulable en `Claude doit X` / `Claude ne doit pas X` / `Claude vérifie X` ?"*

- Oui → la phrase reste (atomicité impératif)
- Non → la phrase sort (externalisée vers doctrine concernée OU surface marketing)

**Catégories canonisées de narrative doctrinale à externaliser** ·

| Catégorie | Exemple | Destination canon |
|---|---|---|
| Brand positioning | *"PhantomOS does not fill forms"* | landing page · `/about` · brand surface |
| Justification doctrinale | *"L'opérateur apprend la posture experte en regardant"* | doctrine `docs/system/*.md` concernée |
| Cas d'usage narratif | *"cas Abyss central · base tracking-GTM centralisée"* | doctrine ou `learnings.json` brand |
| Thèse philosophique | *"Clarté = un produit, pas un nice-to-have"* | doctrine fondatrice (thèse fondatrice section) |
| Storytelling release | *"v2.81 a flag systémique post-test live"* | CHANGELOG.md · release notes |
| Pédagogie mainteneur | *"Le mainteneur ajoute règles par accumulation"* | `docs/system/README.md` ou wiki contributeur |

**Anti-pattern narrative leak** ·

```
[ANTI-PATTERN v2.81.1]
Mono-arc conversational disqualifie 5 profils sur 6. PhantomOS does not fill forms 
silently. Multi-entry tuilé visuellement équivalent débloque adoption pour profils 
non-creative. Adoption se joue dans ce gap critique. Opérateur quitte session après 
`/tour` sans avoir produit · friction adoption forte · workspace abandoned avant premier 
wow effect honnête.
```

Aucune phrase reformulable en `Claude doit X`. C'est de la prose doctrinale qui justifie l'existence de la doctrine `entry-arc-doctrine.md`. Pattern correctif · cette prose vit dans `entry-arc-doctrine.md § 2 Le problème résolu`. Le CLAUDE.md ne contient que `Claude propose les 4 portes MECE post-tour (canon entry-arc-doctrine.md)`.

---

## 8. Zéro inventaire détaillé

Règle canon stricte · l'inventaire des N doctrines (24 actuellement) avec versions / descriptions / cross-refs vit dans `docs/system/README.md`. Le CLAUDE.md root contient un pointer unique vers cet index.

**Pattern canon** ·

```
[CANON]
## Doctrines

Index complet · `docs/system/README.md`
```

2 lignes · pointer unique · maintenance burden zéro.

**Anti-pattern v2.81.1** ·

```
[ANTI-PATTERN]
## Doctrines

- `contextual-intelligence.md` v2.79+ · master doctrine canon agentic
- `decomposition-visibility-doctrine.md` v2.79.5+ · 4 niveaux matriciels
- `engagement-disclosure-doctrine.md` v2.79.5 · disclosure pré-engagement
- `entry-arc-doctrine.md` v2.81.0 · multi-entry 4 portes post-tour
- `onboarding-holistic-doctrine.md` v2.80.3 · panorama 360° pré-tour
- `operational-system-doctrine.md` v2.71 · mère 5 couches
- `output-clarity-doctrine.md` v2.79.2 · standards Vercel/GitHub-grade
- `pacing-doctrine.md` · rythme outputs stage filter ARR
- `voice.md` · registre · ton · anti-patterns prose
- [...14 more entries...]
```

~30 lignes denses · duplique `docs/system/README.md` · maintenance burden doublé · capacité attention gaspillée. Pattern correctif · pointer unique vers index canon.

---

## 9. Format atomique impératif · règles de forme

Règles de forme canon strict ·

- Bullets / tirets une instruction par ligne (recommandation Anthropic explicite)
- Remplacer · point-médian par tirets quand utilisé en liste structurelle plate
- Garder · point-médian acceptable en prose ou cross-refs intra-paragraphe (cohérent voice canon)
- Sections H2 sobres FR ou EN selon contexte fichier (cohérent `output-clarity-doctrine.md` HR-OCD-3)
- Tableau DO / NEVER autorisé canon pour règles binaires opérateur contract
- Tableau Entity / File / Contains autorisé canon pour reference data structurée
- Code blocks (```) pour patterns canon stricts (file paths · commands · structures)
- Quotes (>) pour thèses fondatrices ou citations doctrinales · usage parcimonieux

**Anti-pattern point-médian liste plate** ·

```
[ANTI-PATTERN]
- Read `.skills/_manifest.json` first for routing · FR+EN triggers · disambiguates_against · model · path
```

5 facts disjoints empilés sur 1 ligne via point-médian. Cognitif scan impossible. Pattern correctif ·

```
[CANON]
- Read `.skills/_manifest.json` first for routing (FR+EN triggers, disambiguates_against, model, path)
```

OU mieux ·

```
[CANON]
- Read `.skills/_manifest.json` first for routing
  - FR+EN triggers
  - disambiguates_against canon
  - recommended_model
  - path
```

Le point-médian reste valide pour cross-refs intra-paragraphe (*"Doctrine sœur de `voice.md` (registre prose) · `output-clarity-doctrine.md` (standards Vercel/GitHub-grade)"*) mais sort des listes plates structurelles.

---

## 10. Anti-patterns canon

Catalogue canon strict ·

- CLAUDE.md > taille canon par niveau (root > 150 · pillar > 100 · project > 120 · brand > 80)
- Marqueurs priorité × 10+ (inflation détruit l'attention · seuil canon dépassé)
- Versioning inline (v2.X.Y disséminé dans CLAUDE.md · vit ailleurs)
- Inventaire détaillé doctrines en prose (24 entries duplique `docs/system/README.md`)
- Narrative doctrinale (brand positioning · justifications · thèses philosophiques · storytelling release)
- Règles-sandwich (4-5 lignes méta pour 1 instruction noyée)
- Sections dupliquées (skill routing × 5 sections au lieu d'1 consolidée)
- Auto-références cycliques (Claude ne suit pas cross-refs en runtime · inline OU externe pas les deux)
- Ajout de règles sans test de suppression (accumulation silencieuse · dilution attention)
- Mélange registre prose humain-facing et instruction LLM-facing (mainteneur écrit pour mauvais lecteur)

---

## 11. Hard Rules canon (HR-CMD-1 à HR-CMD-8)

### HR-CMD-1 · Taille canon respectée par niveau

Tout CLAUDE.md respecte taille canon par niveau · root ≤150 lignes · pillar ≤100 lignes · project ≤120 lignes · brand ≤80 lignes. Violation déclenche audit immédiat (sortir narrative · externaliser doctrines · supprimer inventaire détaillé · consolider sections dupliquées). Violation persistante = bug invalid CLAUDE.md canon.

### HR-CMD-2 · Marqueurs priorité parcimonieux

CRITICAL + YOU MUST + IMPORTANT cumul ≤3 par CLAUDE.md. NEVER en majuscules ≤10 par CLAUDE.md. Au-delà des seuils, le modèle ignore tous les marqueurs uniformément (documenté Anthropic). Mécanisme calibration canon obligatoire (test sévérité observable). Violation = bug invalid CLAUDE.md canon.

### HR-CMD-3 · Zéro versioning inline

Aucun marqueur version (v2.X.Y) ne vit dans CLAUDE.md. Versions vivent dans `CHANGELOG.md` plus frontmatters doctrines plus `_version.json` plus manifest releases. Exception canon · frontmatter du CLAUDE.md (si présent) peut contenir version pour canonicité globale. Le contenu du fichier n'expose aucune version inline. Violation = bug invalid CLAUDE.md canon.

### HR-CMD-4 · Zéro narrative doctrinale

Test mental canon obligatoire pour chaque phrase · *"reformulable en `Claude doit X` / `Claude ne doit pas X` / `Claude vérifie X` ?"*. Non → phrase sort (externalisée vers doctrine concernée OU surface marketing). 6 catégories canonisées à externaliser · brand positioning · justification doctrinale · cas d'usage narratif · thèse philosophique · storytelling release · pédagogie mainteneur. Violation = bug invalid CLAUDE.md canon.

### HR-CMD-5 · Zéro inventaire détaillé doctrines

L'inventaire des N doctrines avec versions / descriptions / cross-refs vit dans `docs/system/README.md`. Le CLAUDE.md root contient pointer unique vers cet index. Économie ~30 lignes denses sur CLAUDE.md root. Maintenance burden divisé par 2. Violation = bug invalid CLAUDE.md canon.

### HR-CMD-6 · Atomicité stricte

1 règle = 1 instruction reformulable `Claude doit X`. Max 2 lignes par règle. Justification externalisée vers doctrine concernée si pèse >1 ligne. Bullets / tirets une instruction par ligne (recommandation Anthropic explicite). Tableaux DO / NEVER autorisés canon pour règles binaires. Violation = bug invalid CLAUDE.md canon.

### HR-CMD-7 · Sections consolidées

Une fonction = une section. Skill routing canon dans 1 section consolidée plus sous-règles, pas dispersé dans 5 sections (Master rule · Skill routing · Investigation posture · Mutation rule · Skills). Mental model cohérent agent runtime. Pattern miroir output-clarity-discipline HR-OCD-3 headers sobres. Violation = bug invalid CLAUDE.md canon.

### HR-CMD-8 · Test de suppression obligatoire avant ajout

Toute proposition d'ajout passe le test de suppression canon · *"si je retire cette ligne, quelle erreur concrète Claude fait ?"*. Réponse spécifique et observable → la ligne reste. Réponse vague → la ligne sort. Mécanisme de croissance contrôlée canon. Empêche accumulation silencieuse · dilution attention · violation taille canon par dérive. Violation = bug invalid CLAUDE.md canon.

---

## 12. Anti-patterns canon (AP-CMD-1 à AP-CMD-8)

### AP-CMD-1 · CLAUDE.md > taille canon par niveau

Root CLAUDE.md > 150 lignes · pillar > 100 · project > 120 · brand > 80. Capacité attention LLM runtime dépassée silencieusement. Le modèle ignore uniformément les règles au-delà de ~150-200 instructions distinctes (documenté Anthropic). Pattern correctif · HR-CMD-1 enforcement runtime · audit immédiat sortie narrative · externalisation doctrines · suppression inventaire détaillé.

### AP-CMD-2 · Inflation marqueurs priorité

CLAUDE.md contient CRITICAL × 7 · YOU MUST × 8 · IMPORTANT × 2 · NEVER × 30+. Seuils canon HR-CMD-2 dépassés. Le modèle ignore tous les marqueurs uniformément. *"Tout est critique"* signifie *"rien n'est critique"*. Priorité perdue · agent traite chaque instruction au même poids · décisions sub-optimales runtime. Pattern correctif · HR-CMD-2 calibration sévérité observable obligatoire.

### AP-CMD-3 · Versioning inline dans CLAUDE.md

v2.55 · v2.79.5 · v2.81.1+ disséminés partout dans CLAUDE.md. Chaque release implique mise à jour cross-référence du fichier. Drift garanti · références obsolètes garanties · zéro valeur ajoutée runtime. Pattern correctif · HR-CMD-3 enforcement runtime · versions vivent dans CHANGELOG.md plus frontmatters doctrines plus _version.json plus manifest releases.

### AP-CMD-4 · Narrative doctrinale dans CLAUDE.md

CLAUDE.md contient brand positioning (*"PhantomOS does not fill forms"*) · justifications doctrinales (*"L'opérateur apprend la posture experte en regardant"*) · thèses philosophiques (*"Clarté = un produit, pas un nice-to-have"*) · storytelling release (*"v2.81 a flag systémique post-test live"*). Aucune phrase reformulable `Claude doit X`. Pollution narrative cible mauvais lecteur (humain mainteneur · pas LLM runtime). Pattern correctif · HR-CMD-4 test mental obligatoire · externalisation 6 catégories canonisées.

### AP-CMD-5 · Inventaire 24 doctrines en prose détaillée

CLAUDE.md root expose ~30 lignes denses listant 24 doctrines avec versions, descriptions, cross-refs cycliques. Duplique `docs/system/README.md`. Maintenance burden doublé · capacité attention gaspillée · 30 lignes de plus en violation taille canon par niveau. Pattern correctif · HR-CMD-5 enforcement runtime · pointer unique vers `docs/system/README.md` index.

### AP-CMD-6 · Règles-sandwich (4-5 lignes méta pour 1 instruction)

Pattern récurrent · 4-5 lignes de justification + brand positioning + bénéfice opérateur + cross-ref + 1 instruction noyée au milieu. Le modèle doit extraire l'instruction · cognitif waste runtime · risque erreur extraction · ROI instruction dégradé. Pattern correctif · HR-CMD-6 atomicité stricte · 1 règle = 1 instruction · max 2 lignes · justification externalisée.

### AP-CMD-7 · Sections dupliquées fragmentent mental model

Skill routing apparaît dans 5 sections distinctes (Master rule · Skill routing · Investigation posture · Mutation rule · Skills). Mutation rule disséminée dans 3 sections. URL intake mélangé dans 2 sections. Mental model fragmenté · agent doit reconstruire le pattern · erreurs d'application. Pattern correctif · HR-CMD-7 sections consolidées · 1 fonction = 1 section + sous-règles.

### AP-CMD-8 · Auto-références cycliques inline + externe

Bloc combine *"Doctrine reference · `docs/system/contextual-intelligence.md`"* + *"Sub-doctrines index · `docs/system/README.md`"* + *"Full canon · `docs/system/skill-routing-doctrine.md`"* dans la même section. Claude ne suit pas cross-refs en runtime · soit l'info est inline (instruction complète) · soit elle vit dans doc externe (pointer suffit) · jamais les deux. Pattern correctif · HR-CMD-1 + HR-CMD-6 · choisir un mode unique par règle.

---

## 13. Cross-refs

- `contextual-intelligence.md` · master doctrine canon agentic · CLAUDE.md est la surface où la doctrine devient instruction LLM runtime
- `output-clarity-doctrine.md` · standards Vercel/GitHub-grade outputs opérateur-facing · cohérent atomicité plus headers sobres plus density modérée applicable forme CLAUDE.md
- `operational-system-doctrine.md` · mère 5 couches · CLAUDE.md fait partie de la couche templates plus rituels (load au démarrage de session)
- `voice.md` · registre prose plus ton plus anti-patterns prose · cohérent atomicité impératif plus zéro narrative doctrinale
- `docs/system/README.md` · index canon doctrines · pointer canon depuis CLAUDE.md root plus enforcement HR-CMD-5
- `CHANGELOG.md` · versioning canon plus zéro version inline CLAUDE.md plus enforcement HR-CMD-3
- `doctrine-governance.md` · amendment process plus supersession formalisée · cohérent maintenance CLAUDE.md cross-version

---

## 14. Position dans le système opérationnel 5 couches

Claude.md Discipline opère sur 3 couches du multiplicatif Operational System Discipline v2.71 ·

**Couche 3 · Templates (raccourcis combinaisons gagnantes).** 4 tailles canon par niveau (root 150 · pillar 100 · project 120 · brand 80) plus format atomique impératif plus tableau DO/NEVER plus marqueurs priorité parcimonieux sont templates canon réutilisables cross-CLAUDE.md PhantomOS. Pattern miroir `resources/templates/*` canon plus `output-clarity-doctrine.md` Couche 3 templates iconographie plus headers FR.

**Couche 2 · Règles (heuristiques décision).** 8 Hard Rules canon strict (HR-CMD-1 à HR-CMD-8) sont heuristiques décision canon · *"si CLAUDE.md alors 4 tailles canon par niveau plus 6 standards de forme obligatoires"* enforcement runtime cross-CLAUDE.md. Pattern miroir `output-clarity-doctrine.md` 8 Hard Rules canon plus `decomposition-visibility-doctrine.md` 9 Hard Rules.

**Couche 5 · Rituels (cadence opérationnelle).** Test de suppression canon obligatoire avant chaque ajout règle · audit immédiat violation taille canon · externalisation systémique narrative doctrinale plus inventaire détaillé · consolidation sections dupliquées. Rituel canon mainteneur par modification CLAUDE.md. Pattern miroir `output-clarity-doctrine.md` enforcement runtime canon plus `voice.md` editor checklist before commit.

Claude.md Discipline est la couche racine FORME canon · permet à PhantomOS de maintenir tous les CLAUDE.md dans la capacité d'attention LLM runtime sans dégrader le suivi des règles. Doctrine sœur de `voice.md` (registre prose plus ton plus anti-patterns prose) et `output-clarity-doctrine.md` (standards rendu opérateur-facing). Cette doctrine s'applique au CLAUDE.md lui-même, pas aux outputs opérateur (qui relèvent de `output-clarity-doctrine.md`).

---

## Status

- **Canonique v2.82.0.** Codifie discipline forme cross-CLAUDE.md PhantomOS identifiée post-audit externe Claude Web sur CLAUDE.md root workspace-template v2.81.1 (9 problèmes structurels redteam audit · taille violée · inflation marqueurs priorité · règles-sandwich · méta-doctrine · chevauchements MECE · versioning inline · pollution narrative · point-médian listes plates · auto-références cycliques). Ferme gap *"CLAUDE.md root viole ses propres règles · LLM ignore uniformément les règles au-delà capacité attention ~150-200 instructions distinctes · negative ROI territory"* plus enforcement runtime obligatoire cross-CLAUDE.md root plus pillars plus projects plus brands.
- **4 tailles canon par niveau.** Root ≤150 lignes · pillar ≤100 lignes · project ≤120 lignes · brand ≤80 lignes. Capacité attention LLM runtime respectée. Mécanisme de croissance contrôlée canon via test de suppression obligatoire avant ajout règle.
- **8 Hard Rules canon (HR-CMD-1 à HR-CMD-8) plus 8 anti-patterns canonisés (AP-CMD-1 à AP-CMD-8).** Enforcement runtime cross-CLAUDE.md. Test de suppression obligatoire avant chaque ajout règle. Marqueurs priorité parcimonieux (CRITICAL + YOU MUST + IMPORTANT cumul ≤3 · NEVER ≤10).
- **Doctrine sœur** · `output-clarity-doctrine.md` v2.79.2 (standards Vercel/GitHub-grade outputs opérateur-facing · cohérent forme canon) · `voice.md` (registre prose plus ton plus anti-patterns prose · cohérent atomicité impératif) · `operational-system-doctrine.md` v2.71 (mère 5 couches · CLAUDE.md fait partie templates plus rituels).
- **Backward compat** · strict additif · doctrine NEW n'override aucune existing. CLAUDE.md legacy pre-v2.82.0 conservent conventions jusqu'à patch · v2.82.0+ migration progressive enforce 4 tailles canon par niveau plus 8 Hard Rules.
- **First applications** · Sprint v2.82.0 patches parallèle CLAUDE.md root workspace-template (sortie narrative + externalisation inventaire 24 doctrines vers `docs/system/README.md` + suppression versioning inline + calibration marqueurs priorité ≤3) plus pillars `00-meta/CLAUDE.md` plus `01-marketing/CLAUDE.md` plus brand `brands/_EXAMPLE/CLAUDE.md` migration progressive enforce 8 Hard Rules canon.
- **Promotion criterion** · à reviewer après 5+ CLAUDE.md patched canon-conformes plus 1 audit cross-niveau (root + pillar + project + brand) convergence plus learnings.json append patterns Claude.md Discipline adoption rate stable 90%+ plus zero violation taille canon par niveau persistante 3+ sprints consécutifs.

---

*Doctrine canonique skill-author-facing plus mainteneur-facing plus agent-facing. Canonise 4 tailles canon par niveau (root 150 · pillar 100 · project 120 · brand 80) plus 8 Hard Rules canon strict (HR-CMD-1 à HR-CMD-8) plus 8 anti-patterns canonisés (AP-CMD-1 à AP-CMD-8). Ferme gap structurel *"CLAUDE.md root workspace-template viole ses propres règles · 9 problèmes structurels audit externe Claude Web v2.81.1"* via HR-CMD-1 à HR-CMD-8 enforcement runtime plus test de suppression obligatoire avant ajout règle. Pattern miroir output-clarity-doctrine.md (8 Hard Rules canon · standards Vercel/GitHub-grade outputs opérateur-facing) plus voice.md (registre prose · ton · anti-patterns prose) plus operational-system-doctrine.md (mère 5 couches · CLAUDE.md fait partie templates plus rituels).*
