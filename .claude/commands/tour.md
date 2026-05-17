---
name: tour
description: PhantomOS onboarding and workspace presentation. Runs automatically at first session when no brand exists; replayable at any time via /tour. Update v2.64 · ontologie sémantique pure · pain_points + objections sub-folder OWNED audiences/{slug}/ (expression subjective audience-specific) · frictions sub-folder OWNED products/{slug}/ (usage produit-specific) · SUPPRESSION top-level brand-wide drills v2.63 (devenus redondants · drill audience expose tout natif) · drill 360° via `/phantom {brand} audiences {slug}` et `/phantom {brand} products {slug}`. Update v2.62 · onboarding refresh post-v2.56→v2.61 sprint · 4 NEW orchestrators (build-atlas-complete · produce-paid-matrix · creative-brief-composer · sync-notion-atlas) + 7 NEW skills D#386 mappers + business_model auto-detection adaptive · doctrine layer pro métier introduite Milestone 5.
---

# Tour · PhantomOS Onboarding

Executable instructions for the agent. This command handles both first-run onboarding and replay presentation. Read top to bottom before acting.

---

## Mode detection (first action)

Before anything else, read `/operator/awareness.json` and `/operator/profile.json`.

| Condition | Mode |
|---|---|
| `awareness.json` missing OR `tour_status = "not_started"` | **first-run** |
| `tour_status = "in_progress"` | **resume** |
| `tour_status = "completed"` AND brand exists | **replay** |

Mode drives which milestones apply, which elements are collected, and which are skipped. Do not re-ask what is already in the profile.

---

## conversation register calibration (live detection, never asked)

Detect from signals in the operator's first two turns. Never ask explicitly.

| Signal | Level |
|---|---|
| Asks basic concept questions (*"c'est quoi un agent"*, *"comment ça marche exactement"*) | grounded |
| Mentions ChatGPT or Claude casually, no technical terms | standard |
| Uses terms like *agent*, *context*, *prompt*, *token* naturally | dense |
| Uses terms like *context window*, *tool calls*, *system prompt*, *MCP* | technical |
| Ambiguous or no signal yet | default to **standard** |

The level calibrates vocabulary, analogy use, density, and presupposition across the tour. Update the assumption as more signals come in. Never say out loud *"you're at level X"*.

Calibration effects:

| Level | Vocabulary | Analogies | Density |
|---|---|---|---|
| grounded | everyday words, avoid *workspace*, *agent contract*, *context layering* | one per paragraph, concrete scenarios | longer, slower |
| standard | introduce canon terms with 1-sentence gloss | optional | medium |
| dense | canon terms direct with 4-5 word gloss | skip | dense |
| technical | technical shorthand, no pedagogy | never | minimal |

---

## Milestones (state machine)

Every tour hits these in order. Milestones can fuse when a single operator turn covers two, or reorder if the operator pulls on a thread early. Never skip without explicit operator signal.

### Milestone 1. Entry hook

**First-run**: open with a value-proposition statement (one paragraph, institutional register), then present three outcome-driven entry paths. The operator picks based on the outcome they want, not on whether they have a URL. Do not force engagement, the operator may be in evaluation mode and not ready to configure anything.

**Opening prose (institutional sober, no casual fillers)**:

> Bienvenue dans PhantomOS.
>
> PhantomOS encode ton univers business pour qu'un agent agisse aligné sans re-briefing à chaque session. Workspace pour ton quotidien d'opérateur · sur paid acquisition, copywriting, audit, stratégie, ou un autre métier que tu décides de faire rentrer.
>
> Avant d'agir, trois entrées possibles selon ton intent.

Present the three options in one message using `AskUserQuestion` tool. **Pass exactly 3 options, not 4.** Do not add a filler *"Type something"* or *"Other"* as a 4th, the tool renders a native free-text escape automatically. Adding a 4th explicit escape creates a visible doublon in the UI.

Option substance (formulation adapts to detected operator language). Outcome-driven, never mental-state-only:

- (a) **Configurer une marque maintenant** · tu as une URL ou une description · l'agent scrape et construit le territoire
- (b) **Comprendre le système d'abord** · cas concret via la marque pédagogique Stepprs · 20 à 30 min · configuration plus tard
- (c) **Les deux en parallèle** · l'agent t'explique pendant que le profil se construit (walk-through guidé)

**Mode inference from the choice**:
- Path (a) → ask for URL or short description in the next turn, enter **url-path** or **conversational-path** mode based on the answer.
- Path (b) → enter **discovery-only** mode (skip Milestone 4, proceed to Milestone 5 directly).
- Path (c) → enter **conversational-path** mode with lower engagement pressure (the agent explains while profile builds organically through conversation).

Markdown fallback only if `AskUserQuestion` is unavailable: use a/b/c (no (d) Other, the operator can always type freely without a menu item).

Wait for response. Capture signals from the reply: language, profile hints (*"j'ai une agence"*, *"je gère mes boutiques"*), conversation register cues, and which branch selected.

**Three operating modes** flow from this choice:
- Path (a) → **url-path mode** (scrape async + live conversation)
- Path (b) → **conversational-path mode** (2-3 questions build profile manually)
- Path (c) → **discovery-only mode** (no configuration, tour focuses entirely on workspace exploration)

**Replay**: short acknowledgement + entry to recap.

> Bienvenue back. Que veux-tu revisiter ?

Skip to Milestone 8 directly in replay mode.

### Milestone 2. Mode branch

**Path (a) · url-path mode**:
1. Launch `snapshot-brand` as a subagent via Task tool. Do not wait.
2. Announce in one turn what is happening AND collect operator context in flowing prose, not as separate questions:

   > *"Scan en cours, 3 à 5 minutes. Pendant le scan, j'auto-détecte aussi le modèle business de la marque (DTC pure, service, hybrid clinique+produit, subscription, marketplace) depuis les signaux URL (locations physiques, services pages, products pages, pricing tiers). Ça calibrera l'arborescence du workspace ensuite. Pendant que le scrape tourne, deux éléments aident à calibrer. D'abord, quel est le use case ici, ta propre marque, un client, un portefeuille agency, un test ? Ensuite, le stack que tu connecterais à ce workspace si tu continues (Shopify, Meta Ads, Klaviyo, Notion, Slack, Drive, autres) ?"*

3. Capture both answers, write to `/operator/profile.json → identity.profile` and `/operator/profile.json → context.stack[]` via `write_to_context`. The Milestone 4 profile-type question becomes already-answered.
4. **Smart suggestion sector-adaptive (post-scan signals)** · une fois le snapshot prêt et le secteur détecté (e-com Shopify · service B2B · SaaS · DTC clinique · autre), l'agent compose `AskUserQuestion` 3 options stack-adaptées contextual ·
   - Secteur Shopify e-com détecté → 3 options · *"Connecte Meta Ads d'abord"* + *"Connecte Klaviyo email"* + *"Connecte Shopify analytics"*
   - Secteur service B2B / SaaS → 3 options · *"Connecte LinkedIn Ads"* + *"Connecte CRM (HubSpot · Pipedrive)"* + *"Connecte analytics web (GA4 · Plausible)"*
   - Secteur DTC clinique / médical → 3 options · *"Connecte Meta Ads"* + *"Connecte CRM clinique"* + *"Connecte Google Ads"*
   - Secteur autre / signal flou → bypass `AskUserQuestion`, proceed Milestone 3 directement.
5. Proceed to Milestone 3 + Milestone 5/6 in parallel with the scrape.

### Pattern canon · URL e-com pasted déclenche proactive chain

Quand l'opérateur paste une URL e-com (Shopify · brand homepage · PDP) en premier message · l'agent DOIT déclencher proactive chain canon ·

1. Lancer scrape URL en async (background via Task tool snapshot-brand)
2. EN PARALLÈLE · poser les 2-3 questions setup minimal (langue · scope solo/équipe/agency)
3. Quand setup Q&A done · synthese scrape déjà prêt · enchaîner Phase 1 macro confirmation immédiate

Anti-pattern · attendre setup Q&A complet avant lancer scrape (séquentiel · perd 1-2 min wall-time inutile). Canon CLAUDE.md root "Proactive multi-skill deployment" · obvious chain ≥2 sub-skills = deploy silently parallèle.

Mode fast-track opérateur expert (post-N brands setup OR flag explicit) skip ces 2-3 questions · use defaults from /operator/profile.json + auto-validate.

**Path (b) · conversational-path mode**:
1. Ask 2 to 3 targeted questions in sequence (one per turn): sector, hero product or core service, rough audience. Keep questions tight, conversational.
2. Use these answers to build the operator's profile in live conversation (the synthesis turn in this path is demonstrated understanding rather than scraped pre-fill).
3. Proceed to Milestone 3 between questions.

**Path (c) · discovery-only mode**:
1. No scrape, no profile-building questions. The operator has signaled they want to understand before configuring.
2. Skip Milestone 4 (profile type, not needed for evaluation).
3. Proceed directly to Milestone 3 (blase) in a natural turn, then Milestone 5 (PhantomOS intro), Milestone 6 (skill concept), and Milestone 8 (close).
4. The synthesis turn (Milestone 7) is reframed: instead of delivering a scrape result, the synthesis comes from the first discovery path the operator picks at the close. Expansions are richer in discovery-only mode · the agent can spend more time on each axis since no scrape validation is pending.
5. Close adapted: the action option (d) becomes *"OK I'm in, let's configure a brand now"* instead of *"Configure my brand now"* (the operator had none to start with).

Write the selected mode to `/operator/awareness.json` as a transient field `tour_mode: "url" | "conversational" | "discovery"` to inform the rest of the session.

### Milestone 3. Blase (operator first name or chosen handle)

**Ask early, within the same turn that announces the scrape and asks for context (Milestone 2 path-a) when possible.** The blase is a low-cost capture that should not appear as a post-script after the synthesis turn. If the operator already dropped their name in Milestone 1 or 2, skip this milestone entirely.

Wording, woven into the natural turn (never standalone):

> *"...by the way, how should I call you?"*

If forgotten before the synthesis turn lands → ask in the same turn that delivers the synthesis, in the opening hook, not as a closing line. Never end the synthesis turn with a name request; that flattens the moment.

Write to `/operator/profile.json → identity.name` via `write_to_context`.

**Smart suggestion conditional · Path (b) conversational-path OR (c) discovery-only.**

- Path (a) url-path → skip ce smart suggestion (le synthesis turn natif Milestone 7 post-snapshot fournit l'effet attendu sans démo extérieur).
- Path (b) conversational-path OR Path (c) discovery-only → après capture blase, l'agent compose `AskUserQuestion` 3 options pour proposer un cas concret pédagogique avant de continuer ·
  - *"Veux-tu voir un cas pédagogique avant qu'on continue · `/breakdown stepprs principe` · 30 min"*
  - *"Continue directement sans démo, je préfère explorer mon contexte"*
  - *"Montre-moi d'abord les capacités du système (Milestone 5)"*

Le 3ème slot route directement vers Milestone 5 si sélectionné. Free-text escape natif géré par `AskUserQuestion`.

### Milestone 4. Profile type

**Skipped in discovery-only mode.** Profile type is not collected until the operator actually moves to configure a brand.

In url-path and conversational-path modes: if the operator already signaled their profile in Milestone 1 (*"je suis agency"*, *"je lance ma marque"*), skip the question and confirm in passing. Otherwise, one question:

> Are you running your own brand, working for clients, monetizing an audience, or testing products short-term?

Capture as `solo | agency | creator | early | dropshipper | portfolio`. Write to `/operator/profile.json → identity.profile`.

### Milestone 5. Ce que PhantomOS peut faire pour toi (capacités-MENU)

**First-run + replay** · présenter les capacités PhantomOS comme MENU plutôt que doctrine forcée. L'opérateur choisit son axe d'entrée selon son intent (déjà détecté Milestone 1-4 · operator profile · stack · use case).

**Tone canon** · "voici ce qui peut t'intéresser maintenant · choisis ton entrée". Institutionnel sérieux + accessible, pas sales-bro, pas growth-coach. Voice canon 100% (prose first, load-bearing terms, pas de triple-parallel, pas d'em-dash).

**Format opérateur · USP killer top + 6 capacités bullets + scope élastique.** L'output Milestone 5 suit ce squelette en semi plain text (pas tableaux ASCII boxes · pas headers ═══) ·

```
**Voici ce que PhantomOS te change au quotidien.**

Tu encodes ton territoire de marque une fois. Identité, audiences, produits, angles, offres. Toutes tes productions suivantes (briefs, pubs, audits) s'y ancrent automatiquement. Coût d'une nouvelle production baisse drastiquement à mesure que le territoire s'enrichit.

**Six capacités câblées out-of-the-box, ouvre celle qui te parle d'abord.**

- **Cartographier une marque** · scrape automatique + cartographie audiences hiérarchique + composition produit + angles compositionnels
- **Décomposer et adapter une créa concurrente** · isole ce qui fait performer · adapt à ta marque · variant en 25 min vs 45
- **Produire des briefs copy et variants visuels** · alignés sur ton territoire · ready Meta/TikTok
- **Auditer un compte Meta Ads** · dimensions canoniques · diagnostic structuré
- **Synchroniser avec Notion** · pull/push 10 collections territoire
- **Étendre le système** · ajouter un type d'objet, un domaine, une source, un skill custom · méthode canon te guide

**Élasticité du système.** Le système accueille bien au-delà du paid acquisition · copywriting, audit, stratégie, domotique, perso, hobby, n'importe quel métier que tu décides de faire rentrer. Tu encodes ton territoire métier · les capacités opèrent dessus.
```

**Mapping skills sous le capot (jamais surfacé operator-facing)** ·

- Cartographier une marque → `build-atlas-complete` chain 9 sub-skills (snapshot → deepen → profile-audience → produce-paid-angles → score-matrix → produce-copy-brief → compose-creative)
- Décomposer et adapter une créa concurrente → `decompose-ad` · `adapt-from-competitor`
- Produire des briefs copy et variants visuels → `produce-copy-brief` · `creative-brief-composer` · `compose-creative`
- Auditer un compte Meta Ads → `audit-meta-account` · `routine-perf` · `analyze-perf`
- Synchroniser avec Notion → `sync-notion-atlas` (11 collections, Phase A pull-only)
- Étendre le système → `scaffold-extension` · `create-skill`

**Outils externes · proposition mesurée.** Plusieurs de ces capacités lisent tes comptes externes (Meta Ads, Calendar, Notion, Supabase, Shopify, autres). Tu peux les brancher maintenant si tu veux tester immédiatement, ou plus tard quand un skill en aura besoin · l'agent te guidera au moment opportun (2 minutes par outil). Pour brancher maintenant · *"connecte mes outils"*.

**Adaptation profil détecté Milestone 1-4 · `AskUserQuestion` reflectively composed.** Après le bloc 6 capacités, l'agent compose 3 options prioritaires selon profil détecté (pas les 6 plates · fold les autres derrière le free-text natif) ·

- Profil paid manager / agency / DTC media buyer → 3 options · *"Cartographier une marque"* + *"Auditer un compte Meta Ads"* + *"Décomposer une créa concurrente"*
- Profil copywriter / content strategist → 3 options · *"Produire des briefs copy et variants"* + *"Cartographier une marque"* + *"Décomposer une créa concurrente"*
- Profil ecom owner / founder → 3 options · *"Cartographier une marque"* + *"Auditer un compte Meta Ads"* + *"Synchroniser avec Notion"*
- Profil domain expert hors marketing / vibecoder / curieux / évaluation → bypass `AskUserQuestion`, route directement vers `/breakdown stepprs principe` (synthesis turn cas concret).

Le 4ème slot `AskUserQuestion` reste toujours *"Pas sûr · montre-moi un cas concret"* (route `/breakdown stepprs principe`). Free-text escape natif géré par `AskUserQuestion`, ne pas ajouter de 5ème option manuelle. Les capacités non listées dans les 3 prioritaires restent accessibles via free-text ou `/skills` plus tard.

**Anti-pattern** · NE PAS forcer la trajectoire copywriting cartographie en premier sur novice complet. C'est dense (frameworks canon copywriting accessibles), trop lourd pour onboarding initial. Les frameworks se découvrent progressivement au fur et à mesure des usages, jamais comme axe imposé.

**Skip Milestone 5 conditional** · si Path (c) discovery-only depuis Milestone 1-2, skip ce milestone directement (l'opérateur ne veut pas configurer, juste comprendre). Aller à Milestone 6 (skill concept + universal entry point) puis Milestone 8 (close + recap).

**Cross-refs canon enrichis** ·
- `/breakdown stepprs principe` (cas concret synthesis turn, vitrine pédagogique).
- `/skills` (catalogue navigable des capacités, à tout moment).
- 6 capacités cross-référencent skills existing canon (build-atlas-complete, produce-paid-matrix, creative-brief-composer, score-matrix, decompose-ad, adapt-from-competitor, profile-audience, produce-paid-angles, produce-copy-brief, audit-meta-account, routine-perf, analyze-perf, sync-notion-atlas, scaffold-extension).

Add concepts covered to `awareness.concepts_introduced` (incluant `capabilities_menu`, `paid_acquisition`, `decompose_ad`, `copywriting_cartography`, `audit_performance`, `notion_sync`, `extension`, `elastic_scope` selon ce que l'opérateur a sélectionné).

### Milestone 6. Skill concept + universal entry point

Split en deux micro-moments distincts (6a + 6b) pour éviter la surcharge cognitive (Miller's 7±2 max · 13 unités attention monolithique = bannies). Format semi plain text + bullets sobres (pas blockquotes prose continue · pas headers ═══).

#### Milestone 6a · Concept de skill + 1 commande critique Path-aware

Format opérateur ·

```
**Concept canon · skills.** Tu décris ton intent en français normal · l'agent route vers le bon skill · pas de syntaxe à mémoriser. Skills tournent sur ta donnée encodée, pas sur knowledge générale.

**Commande critique selon ton chemin.**
```

Suivi d'UNE seule commande critique Path-aware ·

- Path (a) action → *"`/skills` pour découvrir le catalogue navigable des capacités quand tu en auras besoin"*
- Path (b) discovery → *"`/breakdown stepprs principe` pour voir tout ça en cas concret · 30 min lecture séquentielle ou drill par chapitre"*
- Path (c) mixte → *"`/phantom {brand}` pour cockpit état de ta marque · read-only · sans risque à explorer"*

**Différenciation canon · à injecter juste après le concept skills, 2-3 lignes ·**

```
**Différenciation canon.**
- Notion stocke du texte indexable.
- Airtable structure des données interrogeables.
- SOPs documentent des process humains.
- PhantomOS opère sur ton univers business via un agent. Trois piliers · territoire stable, productions runtime à la demande, extensibilité canon.
```

#### Milestone 6b · Quatre autres commandes via smart suggestion

Après le concept skills + différenciation, l'agent enchaîne avec les 4 autres commandes complémentaires (use cases distincts · découverte progressive) ·

```
**Quatre autres commandes t'accompagnent dans la durée. Tu les découvriras au fil des besoins.**

- `/tour` · revisiter cet onboarding à tout moment
- `/lexicon` · vocabulaire qui débloque les bons skills quand tu prompts (important onboarding et rappel à 6 mois)
- `/breakdown stepprs` · vitrine pédagogique via cas concret réel
- `/skills` · catalogue navigable des capacités (recherche par intent)
- `/phantom {brand}` · cockpit état d'une marque active
```

**Smart suggestion adaptive après le bloc 4 commandes** · *"Tu veux que je te montre une de ces commandes maintenant, ou on continue ?"* L'opérateur choisit binaire · démo immédiate d'une commande OR continuer Milestone 7+.

#### Three principes canon · post-Milestone 6 conditional

**Path (a) action directe** · SKIP les 3 principes canon ici (just-in-time canon · revelation deferred quand pertinent runtime · pas dump upfront). L'opérateur veut configurer, pas philosopher.

**Path (b) discovery + Path (c) mixte** · 3 principes maintenus mais format bullets condensés (pas blockquotes prose) ·

```
**Trois principes de fond.** Tu n'as pas à les mémoriser, juste savoir qu'ils existent.

- **Territoire stable vs production runtime.** Ce qui définit ta marque ne bouge presque pas. Ce qui se génère change chaque semaine. Compound effect.
- **Intelligence contextuelle, pas formulaires.** Système raisonne via variables paramétrées. Tu décris ton intent, l'agent décompose et construit.
- **Cinq couches + extensibilité.** Modèle, règles, templates, métriques, rituels, plus une couche d'extensibilité canon. Système reproductible, pas Notion enrichi.

Pour voir tout ça concrètement (30 min cas réel) · `/breakdown stepprs principe`.
```

#### Universal entry point · two-sided integration

Explain the two-sided universal entry point in flowing sentences (post-6a, post-6b, post-principes). Do not use the phrase *"single nerve center"* (metaphor without load-bearing). Stick to operational description. Example tone:

> One more thing worth knowing, because it avoids a confusion later. This folder is the same reference point across every Claude interface you might use. If you run Claude Code in your terminal, the web app at claude.ai, or the desktop app, all of them read this workspace when you open it. No re-setup when you move between them. And on the other side, whatever tools you already work with (Google Drive, Sheets, Gmail, Calendar, Notion, ClickUp, your paid media platforms, your analytics stack, your CRM), they connect here on demand when a skill needs them. The tools stay where they are. The workspace operates across them.

**Banned cadences**: triple-parallel constructions (*"one X, one Y, one Z"*, *"Drive, Sheets, Gmail"* as rhetorical list), slogan endings (*"the workspace becomes the nerve center"*, *"operates across them on demand"* in isolation). Lists of tools inside the prose are factual, not rhetorical · avoid the rhythmic feel.

**Pattern naming sans demander le slug du skill.** L'opérateur n'a pas besoin de connaître le nom du skill : il dit son intent en français normal, l'agent route. Mention possible en passing si l'opérateur est dense/technique et veut un aperçu opérationnel. Table illustrative (interne, jamais surfacée frontale en menu) :

| Trigger naturel | Skill cible |
|---|---|
| *"lance le pipeline complet pour {brand}"* | `build-atlas-complete` chain 9 sub-skills auto |
| *"matrice paid {brand}"* | `produce-paid-matrix` top-3 territoires |
| *"brief créa sur l'angle qui ressort top"* | `creative-brief-composer` brief + N variants |
| *"sync mon Notion vers Phantom"* | `sync-notion-atlas` 11 collections Notion → PhantomOS |
| *"creuse les mécanismes du sérum C15"* | `map-mechanisms` 7 deep fields canon EFSA |
| *"décompose l'angle ANG-04"* | `decompose-angle` 11 atoms canon formula |
| *"pose le focus Q3 de {brand}"* | `produce-strategy` Q&A annual_goals + constraints |
| *"cartographie les audiences brand-wide"* | `map-audiences` 3 niveaux + 4 questions |
| *"drill audience complète {slug}"* | `/phantom {brand} audiences {slug}` (vue complète de l'audience · profile + pain + objections) |
| *"drill product complet {slug}"* | `/phantom {brand} products {slug}` (vue complète du produit · spec + offers + funnel + frictions) |

Add `skill`, `universal_entry_point`, and `tool_stack_integration` to `awareness.concepts_introduced`.

**Smart suggestion drill commandes (post v2.76.0 split 6a + 6b).** Après 6a (skill concept + 1 commande critique Path-aware · `/skills` ou `/phantom` selon profil détecté Milestone 1-4), l'agent compose `AskUserQuestion` 3 options · drill direct sur une des 4 autres commandes complémentaires OR continuer ·

- *"Montre-moi `/breakdown stepprs principe` · cas concret pédagogique 30 min"*
- *"Montre-moi `/lexicon` · vocabulaire opérateur-facing"*
- *"Continue vers la suite, je drill les commandes plus tard via `/skills`"*

Adaptation selon profil ·
- Paid manager / agency → 3 options prioritaires · *"Montre `/breakdown stepprs principe`"* + *"Montre `/skills` catalogue"* + *"Continue"*
- Copywriter / content strategist → 3 options · *"Montre `/lexicon`"* + *"Montre `/breakdown stepprs principe`"* + *"Continue"*
- DTC owner / founder → 3 options · *"Montre `/phantom {brand}` cockpit état"* + *"Montre `/breakdown stepprs principe`"* + *"Continue"*

Free-text escape natif géré par `AskUserQuestion`, ne pas ajouter de 4ème option manuelle.

### Milestone 7. Synthesis turn

**URL path**: when snapshot-brand returns, come back at a natural break in the conversation.

Surface the **synthesis paragraph** that snapshot-brand Step 7 generated (4-6 sentences using filled schemas as analytical vocabulary, ce que le produit est vraiment, qui l'achète et pourquoi, ce que l'architecture d'offre suggère, les 1-2 éléments que l'opérateur n'a probablement pas remarqués). Do not re-summarize, do not enumerate. End with:

> *"Want to validate and correct, or keep exploring first?"*

Never produce a separate "1-2 lines" or bracketed list summary. The synthesis paragraph IS the synthesis turn.

**Pose les bases de la suite après la synthèse, AVANT la question de validation.** Une phrase qui pose le pattern de correction, mentionne `/phantom {brand}` comme outil de visualisation, et introduit le statut "à valider" que l'opérateur va voir partout dans le système. Exemple ton :

> *"Tu peux valider, corriger ou rejeter point par point ce que je viens d'encoder, je retiens. La commande `/phantom {brand_slug}` ouvre à tout moment la vue arborescente : produits, audiences avec leur statut, offres. Le statut 'à valider' que tu verras un peu partout est volontaire : c'est une hypothèse de travail à confirmer avec du verbatim client juste après, pas une vérité plaquée depuis la page."*

Cette phrase pose en bloc : (a) le pattern de correction, (b) `/phantom {brand}`, (c) le statut "à valider", (d) l'invitation implicite au mining VoC qui suivra. La phrase précède la question *"Want to validate and correct, or keep exploring first?"* (qui devient l'ouverture vers la suite, pas un orphan close).

**Smart suggestion post-synthesis · adaptative profile-driven.** Après la synthèse paragraph + base phrase, l'agent compose `AskUserQuestion` 3 options adaptées profil détecté (Milestone 1-4) · drill différencié selon intent ·

- Profil paid manager / agency / DTC media buyer → 3 options · *"Drill 1 angle paid vers brief copy ready"* + *"Drill audience pour mining VoC verbatim"* + *"Drill matrice paid scoring top-3 territoires"*
- Profil copywriter / content strategist → 3 options · *"Drill brief copy sur l'angle qui ressort"* + *"Drill cartographie audiences profile"* + *"Drill décomposition angle 11 atoms canon"*
- Profil DTC owner / founder → 3 options · *"Drill cohérence brand validation"* + *"Drill matrice paid scoring"* + *"Drill sync Notion atlas existant"*
- Profil curieux / évaluation → 3 options · *"Drill cas pédagogique `/breakdown stepprs principe`"* + *"Drill validation/correction synthesis"* + *"Continue explorer sans drill"*

Free-text escape natif géré par `AskUserQuestion`, ne pas ajouter de 4ème option manuelle. Les autres axes restent accessibles via free-text ou Milestone 8 close.

**Hard rule: do NOT cascade Milestones 5/6 (PhantomOS introduction + skill concept) immediately after the synthesis turn.** The synthesis must land alone. Re-pitching what PhantomOS is right after the synthesis dilutes the moment and reads as agent self-explanation. Milestones 5/6 belong **before** the scrape returns (during the scan window) or are **skipped entirely** if the operator signaled in Milestone 1/2 they already understand the model. If 5/6 were not delivered before Milestone 7, defer them to Milestone 8 expansions or to the operator's next pull. Never glue them to the synthesis turn.

**Snapshot failure modes · fallback messaging.** Snapshot-brand may fail or return thin data. Three failure cases, three operator-facing handlings (always honest, always offers a path forward · never ends on apology):

- **URL 404 / DNS error / paywalled** → *"L'URL ne répond pas (404 / accès restreint / DNS introuvable). Si tu as une autre URL pour cette marque ou si tu peux me transmettre la home en texte, je repars dessus. Sinon bascule vers le mode conversational : tu me décris la marque en deux lignes et je construis depuis tes réponses."*
- **JS-heavy SPA / scraping incomplet** → *"Le site est rendu côté JavaScript et le scraper accède à peu de contenu au-delà des balises de base. J'ai capté {X éléments} mais la moitié manque. Trois options : transmets-moi le copy hero + 2-3 prix dans le chat, connecte Chrome MCP pour un scrape complet, ou bascule vers le mode conversational."*
- **Page trop fine (sub-confidence threshold)** → *"La page est trop légère pour auto-snapshot ({score} %). Pas de quoi générer une fiche utile. Trois questions courtes suffisent à calibrer : qu'est-ce que ce produit fait concrètement, qui l'achète, quel format / cure. Réponds, je construis."*

Never close the synthesis turn on a pure apology ("désolé, j'ai pas pu"). Always pair the failure with a path the operator can take in the next turn.

**Conversation path**: when the 2-3 profile questions are answered, deliver a synthesis.

> Based on what you told me, here is what I already see: [one-paragraph synthesis of positioning, product, audience]. I can already calibrate outputs on this. If you want, we enrich from here.

**Discovery path**: no scrape to return, no profile to synthesize. The synthesis is deferred to the first expansion picked at Milestone 8 · the agent can spend more time on the chosen axis since no validation is pending. Skip the synthesis-announcement turn in this mode.

Write `awareness.first_brand_validated = false` (still pending validation) and `first_brand_drafted = true` (conceptual marker · operator has material to validate). In discovery-only mode, set `first_brand_drafted = false` (no draft yet).

### Milestone 8. Close · reflectively generated, not templated

Present as native `AskUserQuestion` tool call with **exactly 4 substantive options**. Options are **reflectively composed** on each close based on the specific operator, the conversation so far, and the canon, not picked from a fixed 4-slot template. The goal is that every close feels tailored to the moment, not drawn from a menu that looks the same regardless of what was said.

**Safety net prose, placed immediately before the first close** (once only, never repeated on subsequent closes):

> If anything I say feels too abstract or goes too fast, say so at any moment. I adjust.

This legitimizes register downshift without forcing the operator to signal weakness via a menu item.

#### Reflective close generation · how to compose the 4 options

Before composing any close, the agent runs an internal reasoning step (extended thinking if available). **This reasoning is silent, not exposed to the operator.** The reasoning addresses, in order:

1. **What the operator has revealed so far.** Their language, their concerns, their hesitations, their profile (from `/operator/profile.json`), their conversation register, what they questioned and what they accepted without challenging.
2. **What has already been covered.** Read `/operator/awareness.json → paths_explored` and `concepts_introduced`. The close never proposes angles already exhausted.
3. **What angles in the canon are most pertinent for THIS operator at THIS moment.** Consult `lexicon.md`, `docs/vision/prisms.md`, `docs/vision/manifesto.md`, `docs/product/capabilities.md`, `docs/system/audience-cartography.md`. Pick angles that resonate with the operator's signaled concerns, not the generic set.
4. **What pivot or broadening would serve them.** Decide the right mix per close: all dig-deeper, mix of dig-deeper and reorient, lateral only · whatever serves this specific conversation. Not a fixed ratio.
5. **Compose 4 options** · one action, three others reflectively composed. Each written in the operator's language, calibrated to detected conversation register, voice-canon compliant.

#### Non-negotiable constraints (always true regardless of reflection)

- **Exactly 4 options.** No more, no less. The native free-text escape handles anything else. Never add *"Other"*, *"Type something"*, *"Chat about this"*.
- **One of the 4 is always action.** The exit path to `setup-brand` or equivalent must always be visible. Only one action option, never two.
- **All 4 options are substantive.** No fillers, no *"tell me more"*, no placeholder phrasing.
- **Voice canon 100%.** Prose first. Load-bearing terms. No coach-phrase, no triple-parallel, no decorative metaphor, no em dash in operator-facing replies.
- **Named angles, never mechanism labels.** When an option covers a topic, name the topic the operator will discover, not the operation. Never *"Pivot to (c)"*, *"Try another angle"*, *"Explore something else"*.
- **Never repeat a covered angle verbatim.** If `paths_explored` already includes *integrity*, do not offer *integrity* again in the same session's close options. Compose fresh angles.

#### Canon archetypes · inspiration, not mandatory slots

The agent draws from these archetypes when composing options, but is not obligated to include any of them in any given close. They are **angles frequently pertinent**, not a checklist:

- **Centralization and zero re-briefing** · the immediate first-day payoff.
- **Integrity and trust of encoding** · the anxiety that the system misinterprets.
- **Time and payback curve** · the business question of break-even.
- **Data ownership and portability** · the lock-in and exit question.
- **Frontier with existing process** · what this replaces vs complements.
- **Extension and skill creation** · how the operator builds their own capabilities.
- **Dependency and long-term bet** · model drift, platform risk, durability.
- **Compound and process moat** · the second-order gain, only for operators already convinced of the first-order one.
- **Lateral reorient** · a genuine "what am I probably not asking" angle, context-specific.
- **Pipeline DTC paid acquisition (textuel)** · comment `/build-atlas-complete {brand}` chain 9 sub-skills auto from blank URL (setup → snapshot → deepen-brand-context → profile-audience → weight-dimensions → produce-paid-angles → score-matrix → produce-copy-brief → compose-creative) avec gates opérateur entre phases, OR séquentiel manuel snapshot → mine-voc → produce-paid-angles → produce-copy-brief si l'opérateur préfère contrôle drill par drill. Le système cartographie audiences avec leurs pain points et objections en hiérarchie, et les frictions vivent côté produit. Drill par audience expose la vue complète (profile + pain + objections), drill par produit expose la vue complète (spec + offers + funnel + frictions). Pertinent quand l'opérateur a signalé un profil paid manager / agency / DTC media buyer en Milestone 1, 2 ou 4.
- **Pipeline DTC visuel + copy complet** · comment `creative-brief-composer` chain produce-copy-brief + compose-creative ensemble (brief + N variants visuels sur l'angle sélectionné), OR séquentiel snapshot → mine-voc → produce-paid-angles → produce-copy-brief → craft-packshot/import-asset → compose-creative pour passer d'une URL à une créa visuel + brief copy prête à shipper sur Meta, branding et photo produit pixel-exact. La photo produit canon et les assets brand (logo, badges) sont préparés une fois et réutilisés sur chaque pub suivante, plus de dérive visuelle d'une ad à l'autre. Pertinent quand l'opérateur a signalé un profil DTC paid / agency / e-com en Milestone 1, 2 ou 4 et veut voir jusqu'où la pipeline va (créa shippable, pas juste brief).
- **Matrice paid scorée top-3 territoires** · `produce-paid-matrix` orchestrator chain produce-paid-angles + weight-dimensions + score-matrix pour passer d'un brand snapshot à une matrice angles × audiences scorée, top-3 territoires prioritaires extraits avec rationale. Pertinent quand l'opérateur arrive avec un compte déjà testé et veut prioriser où concentrer l'allocation budget, ou quand un consultant veut un livrable client structuré.
- **Sync Notion ↔ PhantomOS** · `sync-notion-atlas` Layer 1 MCP pull-only Phase A, importe 11 collections Notion (brands, products, audiences, angles, etc.) vers le workspace PhantomOS pour les opérateurs qui ont déjà un atlas Notion buildé et veulent le faire vivre dans Phantom sans rebuilder. Pertinent quand l'opérateur signale un setup Notion existant en Milestone 2.

The agent composes from these OR generates fresh angles from the conversation. The list is not exhaustive.

#### Expansion after selection

Once the operator picks one of the 4 options, the agent delivers an expansion of 60 to 120 seconds of reading, calibrated to the detected conversation register. The expansion is itself reflectively composed, pulling from the relevant canon sections (`lexicon.md`, `docs/vision/manifesto.md`, `docs/product/capabilities.md`, `docs/system/agent-contracts.md`, `docs/system/architecture.md`, `docs/system/patterns.md`), never a pre-written block.

After the expansion, write the chosen angle name to `awareness.paths_explored` (lowercase slug, e.g. `centralization`, `integrity`, `payback`, `ownership`, `compound`). Action option writes `action` and ends the tour via `setup-brand` trigger.

### Post-expansion close · same reflective generation

After every expansion, the agent generates a new 4-option close using the same reflective reasoning as above. The context is updated: the just-delivered expansion is now part of what's been covered, and that angle joins `paths_explored`. The next close must take that into account.

**Additional rules specific to post-expansion closes**:

- **Show the map without hiding behind anonymous pivots.** If the operator is still interested in exploring, the close should make other relevant angles **visible by name**, not under labels like *"Pivot to X"*. Operator sees what's on offer.
- **Single exit still applies.** One action option, never two exits.
- **Go-deeper vs reorient mix is reflective.** The agent decides per close whether this moment calls for deeper exploration of the current topic or surfacing a new angle, based on operator signal, not a fixed ratio.

#### Session-level counters the agent tracks in its own state

These are ephemeral, not written to `awareness.json`:

- `current_topic` · the angle of the most recent expansion.
- `current_topic_cycles` · consecutive expansions on the same topic without reorienting.
- `total_expansions` · cumulative expansions since the tour started.

Counters reset when the operator picks an angle different from the current topic (`current_topic_cycles` to 0) or when the tour ends (all to 0).

#### Progressive anti-stagnation

When the operator keeps picking go-deeper on the same topic without reorienting:

| `current_topic_cycles` | Behavior |
|---|---|
| 1 | Normal close, no nudge. |
| 2 | Before the close, agent slips one line: *"Other angles are still there whenever you want to switch."* |
| 3 | In the reflective composition, the agent **deliberately shifts the ratio** toward reorient options. Fewer go-deeper, more named pivots. The map becomes louder. |
| 4+ | Explicit check in prose before the close: *"We've gone deep on [topic name]. Still useful, or worth switching angle?"* Composition favors reorient angles heavily. |

#### Progressive global soft cap

Applies on `total_expansions` across all topics:

| `total_expansions` | Behavior |
|---|---|
| 1-4 | Normal, no nudge. |
| 5 | Agent adds a single sentence in the entête of the next close: *"We've covered a lot of ground. The setup is about fifteen minutes whenever you want to jump in."* No change to the 4 options. |
| 8+ | Stronger ambient nudge: *"Worth mentioning, you can stop the tour here and come back with `/tour` later. Exploring on a configured brand is usually more concrete."* |

Both nudges are prose entête, not menu options. They never force. They keep the action path visible without closing exploration.

**Anti-collapse rule.** Never collapse into a bare *"configure now / stop"* close. The reflective generation must always produce 4 substantive options until the operator picks action or exits via free-text.

### Milestone 9. First-skills offer (conditional, end of tour only)

If operator reached the end of the tour AND first-skill has not been built (`awareness.first_skill_built = false`) AND first_skill_offered count < 3:

**Prose hook (intro avant AskUserQuestion)** ·

> One last thing. Tu peux construire ton premier skill via une mission concrète · 30 à 60 minutes · tu finis avec un skill réel exécuté sur ta donnée et la méthode pour en construire d'autres.

**AskUserQuestion 4 options reflectively composed selon profil détecté Milestones 1-4** · l'agent compose 4 missions adaptées (pas les 7 plates · fold les autres derrière le free-text natif) ·

- Profil paid manager / agency / DTC media buyer → 4 options · *"Pipeline complet marque blank en 30 min (`build-atlas-complete`)"* + *"Matrice paid scorée top-3 territoires (`produce-paid-matrix`)"* + *"Décomposition d'un angle en 11 atoms (`decompose-angle`)"* + *"Lancement immédiat, ou report ultérieur ?"*
- Profil copywriter / content strategist → 4 options · *"Brief créa + variants sur l'angle qui ressort (`creative-brief-composer`)"* + *"Décomposition d'un angle en 11 atoms (`decompose-angle`)"* + *"Pipeline complet marque blank en 30 min (`build-atlas-complete`)"* + *"Lancement immédiat, ou report ultérieur ?"*
- Profil DTC owner / founder → 4 options · *"Pipeline complet marque blank en 30 min (`build-atlas-complete`)"* + *"Sync Notion existant vers Phantom (`sync-notion-atlas`)"* + *"Pose du focus Q3 brand-wide (`produce-strategy`)"* + *"Lancement immédiat, ou report ultérieur ?"*
- Profil curieux / évaluation → 4 options · *"Drill mécanismes d'un produit canon EFSA (`map-mechanisms`)"* + *"Pipeline complet marque blank en 30 min (`build-atlas-complete`)"* + *"Décomposition d'un angle en 11 atoms (`decompose-angle`)"* + *"Lancement immédiat, ou report ultérieur ?"*

Free-text escape natif géré par `AskUserQuestion`. Les autres missions (build-atlas-complete, produce-paid-matrix, creative-brief-composer, sync-notion-atlas, map-mechanisms, decompose-angle, produce-strategy) non listées dans les 4 prioritaires restent accessibles via free-text.

If accepted → trigger `build-agent` in guided-mission mode.
If declined → `awareness.first_skill_offered += 1`. Do not push again this session. Future sessions can surface the offer again when pedagogically opportune (first mention of a platform, first *"can you do X"* to which no skill responds), up to the cap.

---

## Awareness writes

On each milestone completion, write to `/operator/awareness.json` via `write_to_context`:

| Event | Field updated |
|---|---|
| Tour entered | `tour_status = "in_progress"`, `sessions_count += 1`, `tour_last_run = today` |
| Blase collected | (written to `profile.json`, not awareness) |
| Profile type collected | (written to `profile.json`) |
| Concept named in intro | `concepts_introduced += [concept]` |
| Path (a/b/c) expanded | `paths_explored += [path_name]` |
| First-skills offered | `first_skill_offered += 1` |
| First-skills built | `first_skill_built = true` |
| Brand validated after setup | `first_brand_validated = true` |
| Tour completed (operator picked action or explicitly closed) | `tour_status = "completed"` |

---

## Replay mode specifics

When `tour_status = "completed"` and operator calls `/tour`:

- Skip blase collection and profile type (already in `profile.json`).
- Short intro · one paragraph recap of what PhantomOS is and the shift, calibrated to the level already recorded.
- Close with adapted options:
  - *"Configure another brand"*
  - *"Re-explore one of the three discovery paths"* (show which paths in `awareness.paths_explored` and which are still untouched)
  - *"Build your first skills if not done yet"* (only if `first_skill_built = false`)
  - *"Just refreshing"* · accompanied in prose by a one-line reminder of the daily commands : *"au passage · `/phantom` pour la vue d'état du workspace, `/skills` pour la liste des fonctions, `/learn-from-session` pour verrouiller une règle après une correction."*

Do not write tour_status back to in_progress on replay. Replay does not consume milestones, it surfaces knowledge.

---

## Constraints (non-negotiable)

- **Voice canon 100%.** Prose first, load-bearing terms only (stateful, runtime, encode, operate, contract), refused terms banned (powerful, supercharge, intelligent, seamless). No coach-phrase, no triple-parallel punchline (*"X becomes Y. A becomes B. C becomes D."*, *"Drive, Sheets, Gmail"* as rhetorical rhythm). See `docs/system/voice.md`.
- **No section headers in operator-facing output.** The tour milestones are internal structure for the agent. The output to the operator flows as conversation, not as a labeled document. Never copy milestone names (*"What PhantomOS is"*, *"The shift"*, *"Universal entry point"*) into the agent reply as bolded titles. The operator sees prose, the agent internally knows which milestone it is hitting.
- **No decorative metaphor.** Banned metaphors in operator-facing speech: *nerve center*, *command center*, *single source of truth* (as slogan), *your second brain*. Describe what the workspace does operationally, do not reach for evocative nouns.
- **Register downshift on signal.** Any operator expression of confusion, hesitation, or request for simpler language triggers an immediate drop of register. Do not preface with *"sure, let me explain more simply"* or *"no problem, I'll slow down"* (that signals weakness and is condescending). Just do it, silently. The safety net prose before Milestone 8 close legitimizes this ahead of time · the operator knows they can ask, and they don't need to justify it when they do.
- **AskUserQuestion option count.** 2 to 4 **substantive** suggestions depending on the milestone (3 at Milestone 1, 4 at Milestone 8 closes). **Never** pad with filler options like *"Type something"*, *"Other"*, *"Chat about this"*, *"Ask me anything else"*. The tool renders its own free-text escape natively · adding an explicit one creates a visible doublon in the UI and contradicts the no-friction principle. The (d) Other rule from root CLAUDE.md applies only to markdown fallback, not to `AskUserQuestion`.
- **Runtime rules in replies.** No em dashes in operator-facing replies (period, comma, or two sentences). No decorative emoji. Operator language matches detected input. See `CLAUDE.md § Operator contract`.
- **One thread question per turn**, +1 sharpening if operator signal is dense. Never two sharpenings in a row. See `CLAUDE.md § Questions protocol`.
- **Never expose file paths, field names, function names** (*write_to_context*, *Task*, *WebFetch*) in operator-facing replies.
- **Respect conversation register detection continuously.** If signals contradict the initial assumption, update silently and re-calibrate next turns.
- **Mutation gate.** All writes to `profile.json` and `awareness.json` go through `write_to_context(field_path, value, source, confidence, mode)`. Never edit JSON directly.

---

## Exit signals

At any point, if the operator says *skip*, *direct*, *on configure*, *pass à l'action*, or equivalent, bypass remaining tour milestones, trigger `setup-brand`, write `tour_status = "completed"` with the milestones not hit logged as `paths_skipped`.

If the operator expresses fatigue (*"on reprendra"*, *"pas aujourd'hui"*, *"plus tard"*), save state as `tour_status = "in_progress"` with current milestone index so a future `/tour` call resumes. Offer a clean close: *"Got it. Come back with /tour anytime."*

---

## Related canon

- `lexicon.md` · canonical vocabulary to use verbatim
- `docs/system/voice.md` · writing register and anti-patterns
- `docs/vision/prisms.md` · angles to pull from for path expansions
- `docs/vision/manifesto.md` · source for thesis depth (path b and c)
- `docs/product/capabilities.md` · source for path a
- `.skills/skills/setup-brand/SKILL.md` · triggered by path d
- `.skills/skills/build-agent/SKILL.md` · triggered by first-skills offer
