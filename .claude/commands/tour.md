---
name: tour
version: v2.81.0
description: Onboarding PhantomOS multi-entry 4 portes (A conversationnel · B brand-first · C import existant · D progressif libre) · M5b first deliverable encadré · canons Vincent runtime (slugs `exit:setup` · `pivot:{volet}` dans AskUserQuestion options · single action option toujours visible) + ton premium (zéro concurrent nommé) + prose native (zéro interface ASCII, réservée aux slash commands `/phantom` `/bird` `/breakdown` `/about`). Refonte v2.81.0 · M1 splitter 4 portes via AskUserQuestion explicit (slugs `arc:substance` `setup:brand` `import:archive` `explore:free`) avec bypass URL collée passive vers Porte B. M2 arc substance corps Porte A uniquement (pivot cross-subject + exit setup canon Vincent runtime). M3 drill territoire conditional Porte A post-M2. M4 setup brand hub commun B/C/A-sortie (calibration disclosure pré-engagement par porte). NEW M5b first deliverable encadré (skill canon lancé 5-15 min · livrable concret à l'écran · validation point par point · awareness write `first_deliverable_built`). M6 ton premium auditté (zéro concurrent nommé). M9 dégradé en option opt-in post-tour (pas Milestone séquentiel · seulement si `first_deliverable_built = true`). Conserve v2.80.1 prose native + v2.79.3 panorama agnostique + zéro typage profil métier initial (HR-OHD-2). Mémoire canon Largo · `feedback_no_em_dash`, `feedback_no_jargon_to_operator`, `feedback_no_overengineer`, `feedback_response_length`, `feedback_onboarding_native_prose`, `largo_cognitive_profile` (matriciel = SLASH COMMANDS, pas onboarding).
---

# Tour · PhantomOS Onboarding

Executable instructions for the agent. This command handles both first-run onboarding and replay presentation. Read top to bottom before acting.

**Doctrine de référence** · `docs/system/onboarding-holistic-discipline.md` (v2.79.3 · panorama 360° agnostique · zéro typage profil métier initial · HR-OHD-2). Si un orchestrator est appelé en aval (`setup-brand` · `onboard-brand`) · cross-ref `docs/system/engagement-disclosure-discipline.md` (v2.79.3 · disclosure pré-engagement).

**Posture de rendu canon v2.80.1.** L'onboarding (`/tour` + premiers messages opérateur) est en **prose conversationnelle native**. Zéro interface ASCII (pas de boxes `━━━` `═══` `─────`, pas de tableau territoires structuré, pas de légende iconographie au pied). Le pattern matriciel ASCII reste réservé aux slash commands `/phantom` `/bird` `/breakdown` `/about`. L'onboarding doit ressembler à une intro humaine naturelle, comme un opérateur senior accueille un nouvel arrivant.

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

## Conversation register calibration (live detection, never asked)

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

### Milestone 1 · Bienvenue + splitter 4 portes MECE

**First-run** · ouvrir par un accueil court qui dit **ce qu'est PhantomOS** de façon dense mais brève (3-5 lignes max), puis **immédiatement** poser un `AskUserQuestion` 4 options explicit (les 4 portes MECE A/B/C/D) qui calibre l'onboarding au profil opérateur. **Jamais** un pavé, **jamais** une amorce amputée qui saute direct au choix de territoire sans avoir dit ce qu'est le système. **Jamais** demander *"tu fais quoi"* / *"ton métier"* / *"ton rôle"* / *"ton profil"* (canon HR-OHD-2). `/about` reste le backup pour qui veut le détail exhaustif d'un coup · le mentionner en une ligne, jamais le substituer à `/tour`.

**Rendu opérateur · prose conversationnelle native (language opérateur FR/EN détecté, jamais codé en dur). Zéro box ASCII. Zéro tableau structuré. Zéro légende au pied. Chaque tour court, jamais un pavé.**

**FR version** · pattern de prose à rendre (accueil 3-5 lignes) ·

```
Bienvenue dans PhantomOS. C'est un workspace où vit ton opération DTC. Tu encodes ta marque une fois (produits, audiences, stratégie, learnings), et le système raisonne, exécute et apprend dessus avec toi à travers les sessions. Sur tout ce qui est stratégique il montre sa réflexion et tu corriges point par point, il retient. Chaque sortie validée enrichit ta connaissance pour la suite.

Comment tu veux qu'on démarre ?
```

**EN version** · pattern of prose to render (welcome 3-5 lines) ·

```
Welcome to PhantomOS. It's a workspace where your DTC operation lives. You encode your brand once (products, audiences, strategy, learnings), and the system reasons, executes and learns on it with you across sessions. On anything strategic it shows its reasoning and you correct point by point, it remembers. Every validated output enriches your knowledge for what's next.

How do you want to start ?
```

Puis poser **immédiatement** `AskUserQuestion` 4 options explicit · **les 4 portes MECE**. Slugs runtime nommés dans options pour routing déterministe ·

| Option label opérateur | Slug runtime | Routing |
|---|---|---|
| *"Explication guidée"* (FR) / *"Guided walkthrough"* (EN) | `arc:substance` | Milestone 2 (arc substance corps Porte A) |
| *"Configurer une marque maintenant"* (FR) / *"Configure a brand now"* (EN) | `setup:brand` | Milestone 4 (setup brand hub · Porte B canonique) |
| *"Importer ce qui existe déjà"* (FR) / *"Import what already exists"* (EN) | `import:archive` | Milestone 4 (setup brand hub · Porte C post-import) |
| *"Juste explorer"* (FR) / *"Just explore"* (EN) | `explore:free` | Milestone 8 close reflectively generated (Porte D · free-text mode · pattern detection) |

**Description courte sous chaque option** (rendu prose · pas obligatoire si l'opérateur identifie tout seul) ·

- **Porte A · arc substance** · *"On déroule pourquoi ça existe, comment ça raisonne, ce qui le distingue, le cycle, les 7 territoires. Tu pilotes, je distille un volet à la fois."*
- **Porte B · brand-first** · *"URL Shopify, landing, ou tu décris ta marque. Je snapshot et on encode la marque ensemble. 15-30 min cycle complet."*
- **Porte C · import existant** · *"Tu as déjà des assets, docs, Notion, APIs branchables. On importe et on encode depuis ce qui existe."*
- **Porte D · explore libre** · *"Tu prompts ce que tu veux, je détecte les patterns au fil. Pas de chemin imposé."*

**FIRST ACTION canon préservée · bypass URL collée passive vers Porte B.** Si l'opérateur paste une URL e-com (`.myshopify.com`, `/products/`, `/collections/`, ou homepage e-com détectée) **pendant** Q1 ou **avant** de répondre à Q1 → bypass direct Porte B (slug `setup:brand`), lancer `snapshot-brand` en async (background), setup minimal en parallèle (langue · scope solo/équipe/agency · pas de question profil métier), synthèse Milestone 7. L'agent ne re-pose pas la question 4 portes.

**Statut canon par territoire (référence interne · ne pas surfacer comme jargon · ne pas rendre en tableau opérateur · sert à alimenter le volet territoires de l'arc Porte A)** ·

| Territoire | Statut | Skills core shipped (illustratif) | Skills NEW backlog |
|---|---|---|---|
| Creative & Copy Production | shipped solid | `produce-paid-angles`, `produce-copy-brief`, `compose-creative`, `creative-brief-composer`, `decompose-ad`, `decompose-angle` | extensions possibles via `create-skill` |
| Tracking & GTM | open territoire | aucun skill shipped | NEW backlog v2.80 · invocable freestyle prose ou via skill backlog explicite |
| Media Buy & Performance | shipped solid | `audit-meta-account`, `analyze-perf`, `routine-perf`, `score-matrix`, `brief-day`, `produce-paid-matrix` | |
| Brand Strategy | shipped solid | positioning canvas, voice 4D Nielsen Norman, archetypes 12/12 Mark+Pearson, purpose Moore (skills brand canon shipped v2.65-v2.79) | |
| Ops & Workflow | partiel | todos · setup · onboard-brand · scaffold-extension | extensions à venir |
| Business Pilotage | partiel | aucun skill shipped · invocation freestyle prose dispo | NEW backlog v2.79.x · unit economics, WBR, cohort retention |
| Lifecycle & CRO | partiel | aucun skill shipped · invocation freestyle prose dispo | NEW backlog v2.81+ · email flows, upsell, LTV |

**Transparency canon · le panorama narratif ne ment pas.** Les territoires `open` annoncent honnêtement *"invocable freestyle prose ou backlog skill explicite"*. Les territoires `partiels` annoncent *"skills shipped et NEW à venir"*. Pas de faux marketing, pas de territoire surévalué. La prose dit la vérité sur l'état canon.

**Awareness writes M1** · une fois la porte choisie · écrire `awareness.tour_entry_door = "A" | "B" | "C" | "D"` (slug Porte) + `awareness.tour_status = "in_progress"` + `awareness.sessions_count += 1`. Sert au routing downstream M2-M9 et aux analytics canon.

**Replay** · short acknowledgement + panorama narratif mis à jour selon état workspace actuel (cf. § Re-entrée /tour évolutive ci-dessous).

> Bienvenue back. Que veux-tu revisiter ?

Skip to Milestone 4 directly in replay mode (close adapté).

### Milestone 2 · Arc substance guidé tour à tour (corps Porte A uniquement)

**Scope canon v2.81 · M2 ne s'exécute QUE si Porte A choisie en M1** (slug `arc:substance`). Porte B (`setup:brand`) saute directement à M4. Porte C (`import:archive`) saute à M4 (variante post-import). Porte D (`explore:free`) saute à M8 close reflectively generated. Si l'opérateur revient en M2 depuis une autre Porte (via free-text *"explique-moi d'abord"* ou équivalent), c'est un pivot explicit · l'agent confirme et entre l'arc.

Le cœur de la Porte A. Une boucle conversationnelle qui distille la substance de PhantomOS, un volet à la fois, pilotée par l'opérateur. Chaque tour · une question guidée `AskUserQuestion` → l'opérateur choisit un volet → expansion **courte** (prose, calibrée au registre détecté, **jamais un pavé**) → nouvelle question guidée qui propose les volets non encore vus plus l'option d'avancer. Pas d'attente de texte libre nu. C'est le retour exact du conversationnel guidé d'avant v2.79.4.

**Volets substance canon** (l'agent verbalise l'effet opérateur, jamais les noms de doctrine · canon operator-facing) ·

- **Pourquoi ça existe** · les 3 frictions DTC (contexte client réinventé chaque session, connaissance métier éclatée entre outils, apprentissages jamais capitalisés). 5-8 lignes.
- **Comment ça raisonne** · mémoire métier persistante, l'agent route ton intent vers la bonne capacité, raisonnement cadré (pas d'impro), il montre sa réflexion. L'effet, pas les noms canon. 5-8 lignes.
- **Ce qui le rend singulier** · les 4 propriétés tenues ensemble par conception · univers métier qui persiste, raisonnement cadré, exécution (pas que du texte), connaissance qui se capitalise. Posture premium · on affirme ce que fait PhantomOS, jamais un comparatif agressif ni de concurrent nommé/dénigré (canon ton Largo). 5-8 lignes.
- **Le cycle** · encode une fois, opère au quotidien, capitalise en continu. 4-6 lignes.
- **Les 7 territoires** · panorama bref des territoires DTC sur pied d'égalité (une demi-ligne chacun, équité HR-OHD-1), alimenté par la table de référence interne ci-dessus. C'est ici, pas en Milestone 1, que le panorama territoires est rendu.

**Mécanique de la boucle** (réutilise le moteur réflexif Milestone 8) ·

- `AskUserQuestion`, exactement 4 options substantives, free-text natif pour le reste. Plafond harness 4 options · l'agent compose, jamais de menu figé, jamais d'option filler.
- **Porte de sortie setup toujours visible (canon Vincent · runtime enforced · non négociable).** Une des 4 options est TOUJOURS l'exit rapide vers la configuration d'une marque (*"Configurer une marque maintenant"*), à chaque tour, pour sortir du tunnel de questions sans friction. **Slug runtime nommé** `exit:setup` dans l'option AskUserQuestion (pas juste règle doctrinale · routing déterministe via slug). Single action option (miroir contrainte Milestone 8).
- **Pivot cross-subject (canon Vincent · runtime enforced · sujets imbriqués).** Dès que l'opérateur creuse un volet en profondeur (sous-sujets imbriqués), une des options doit permettre de pivoter latéralement vers un autre volet et d'y revenir, pas seulement creuser ou avancer. **Slug runtime nommé** `pivot:{volet}` dans l'option AskUserQuestion (e.g. `pivot:cycle`, `pivot:territoires`, `pivot:singularite` · routing déterministe via slug). L'opérateur n'est jamais enfermé dans une seule branche.
- Les 2 options restantes = volets substance non encore vus, composés selon les signaux. Slugs runtime nommés `volet:{nom}` (e.g. `volet:pourquoi`, `volet:raisonnement`). Après chaque expansion · écrire le volet vu dans `awareness.paths_explored`, ne jamais le re-proposer.
- **Anti-stagnation** · après 3 expansions substance, glisser une ligne *"On peut continuer à creuser, pivoter sur autre chose, ou passer à une marque concrète, comme tu veux"*. Après 4-5, l'agent oriente la composition vers l'exit setup sans fermer brutalement (anti-collapse · toujours 4 options substantives).
- Registre calibré (grounded/standard/dense/technical) selon détection live. Jamais de pavé · si un volet déborde, l'agent coupe et propose *"je peux creuser ça plus, ou on avance"*.

**Sortie de l'arc · routing par slug runtime** (option AskUserQuestion sélectionnée OR free-text) ·

- **Slug `volet:{nom}`** · expansion volet substance · même tour suivant, on continue l'arc.
- **Slug `pivot:{volet}`** · pivot latéral vers autre volet et retour possible · l'agent compose le tour suivant en gardant les volets non encore vus.
- **Slug `drill:{territoire}`** · territoire nommé (creative / tracking / media buy / brand / ops / business / lifecycle) → Milestone 3.
- **Slug `exit:setup`** · single action option toujours visible → `setup-brand` orchestrator via M4 (disclosure pré-engagement `engagement-disclosure-discipline.md`).
- **Skill scan** · l'opérateur veut le catalogue → `/skills`.
- **Détail exhaustif** · l'opérateur veut tout d'un bloc → pointer `/about` (backup deep doc), puis revenir à l'arc ou avancer.
- **Free-text autre** · intent non-listé → l'agent interprète et route, jamais re-poser *"tu fais quoi"*.

**Pattern · URL e-com pasted déclenche bypass M1 vers Porte B.** Si l'opérateur paste une URL e-com à n'importe quel tour de l'arc (M2 ou plus tard) → bypass Porte B silencieux · lancer `snapshot-brand` en async (background), setup minimal en parallèle (langue · scope solo/équipe/agency · pas de question profil métier), synthèse Milestone 7. Anti-pattern · attendre la fin de l'arc avant de lancer le scrape.

**Mode fast-track opérateur expert** (post-N brands setup OR flag explicit) · proposer d'emblée l'option avancer en tête, arc substance disponible mais non imposé.

Write the active mode to `/operator/awareness.json` transient field `tour_mode: "substance" | "drill" | "setup" | "skills" | "freestyle"`.

### Milestone 3 · Drill territoire (conditional · Porte A post-M2 uniquement)

**Scope canon v2.81 · M3 ne s'exécute QUE depuis Porte A post-M2**, quand l'opérateur clique un slug `drill:{territoire}` dans une option AskUserQuestion de l'arc substance. Porte B saute M3 (l'opérateur a configuré une marque · le drill territoire vient via M5b first deliverable encadré). Porte C saute M3 (post-import direct M4). Porte D saute M3 (free-text mode · pas de drill territoire séquentiel imposé).

**Si l'opérateur a choisi de drill un territoire en Milestone 2** (slug `drill:{territoire}`), l'agent zoom sur ce territoire avec un sous-panorama en prose conversationnelle. Zéro box ASCII. Zéro tableau. Juste prose narrative qui décrit les capacités câblées et le démarrage possible.

**Creative & Copy Production drill** · rendu prose ·

```
Creative et copy production · drill.

Les capacités câblées aujourd'hui · cartographier audiences et angles paid (chain `build-atlas-complete`), décomposer une créa concurrente (`decompose-ad`), produire un brief copy avec variants visuels (`creative-brief-composer`), adapter une créa concurrente vers ta marque (`adapt-from-competitor`), sales letters DR (`produce-copy-brief` mode long-form).

Pour démarrer · paste l'URL d'une marque, je cartographie en 5 min. Ou paste l'URL d'une ad concurrente, je la décompose en 11 atoms.
```

**Tracking & GTM drill** · rendu prose ·

```
Tracking et GTM · drill.

Territoire ouvert aujourd'hui · NEW skills backlog v2.80.

Les capacités annoncées (invocables freestyle prose ou via skill backlog) · audit pixels Meta/Google sur un compte, validation server-side tracking (CAPI · Enhanced Conversions), diagnostic consent mode (CMP · GDPR · iOS 14.5+), coverage analytics (GA4 · Server GTM).

Pour démarrer · décris ton stack tracking actuel, je diagnostique freestyle. Ou attend la release skill v2.80 pour invocation structurée.
```

**Media Buy & Performance drill** · rendu prose ·

```
Media buy et performance · drill.

Les capacités câblées aujourd'hui · audit setup compte Meta (`audit-meta-account` dimensions canoniques), routine perf quotidienne (`routine-perf` flags binaires), analyse perf end-to-end (`analyze-perf` CPA/ROAS/COS cross-ref), score matrice angles × audiences top-3 (`produce-paid-matrix`), brief-day état brand actuel (`brief-day`).

Pour démarrer · connecte ton compte Meta, je lance un audit setup. Ou paste un export perf, je diagnostique cross-ref.
```

**Brand Strategy drill** · rendu prose ·

```
Brand strategy · drill.

Les capacités câblées aujourd'hui · positioning canvas Moore (purpose · audience · category · differentiator), voice 4D Nielsen Norman (formal/casual · serious/funny · respectful/irreverent · matter-of-fact/enthusiastic), archetypes 12/12 Mark+Pearson (caregiver · creator · explorer · hero · etc), voice consistency validator cross-outputs.

Pour démarrer · décris ta marque ou paste URL, je propose positioning et voice. Ou drill un sous-axe (positioning · voice · archetype).
```

**Ops & Workflow drill** · rendu prose ·

```
Ops et workflow · drill.

Territoire partiel · shipped et extensions à venir.

Les capacités câblées aujourd'hui · todos système (P0-P3 · energy levels · dependencies), onboarding nouveaux opérateurs (`onboard-operator`), setup nouvelle marque (`setup-brand` orchestrator), scaffold extension (nouveau type d'objet, domaine, source).

Pour démarrer · décris ton workflow actuel, je propose améliorations. Ou drill un sous-axe (todos · setup · onboarding · extension).
```

**Business Pilotage drill** · rendu prose ·

```
Business pilotage · drill.

Territoire partiel · NEW skills backlog v2.79.x.

Les capacités annoncées · unit economics (LTV/CAC · payback · contribution margin), WBR (Weekly Business Review · KPIs canon e-com), cohort retention analysis, roadmap trimestrielle (`produce-strategy`).

Pour démarrer · paste tes data financières, je freestyle diagnostic. Ou attend skills NEW v2.79.x pour invocation structurée.
```

**Lifecycle & CRO drill** · rendu prose ·

```
Lifecycle et CRO · drill.

Territoire partiel · NEW skills backlog v2.81+.

Les capacités annoncées · PDP optimization (Product Detail Page · conversion drivers), landing page composition (sections canon DR), email flows lifecycle (welcome · abandoned cart · post-purchase · winback), upsell architecture, LTV optimization.

Pour démarrer · décris ton stack lifecycle actuel, je freestyle diagnostic. Ou attend skills NEW v2.81+ pour invocation structurée.
```

Après le drill territoire, l'agent **ne s'arrête pas sur du texte libre nu** · il pose un `AskUserQuestion` (3 options substantives + action, free-text natif) pour garder le tour-à-tour guidé. Options composées selon le territoire drillé · ex pour Creative · *"Cartographier une marque depuis une URL"* / *"Décomposer une ad concurrente"* / *"Drill un sous-axe (angles · copy · créa)"* + l'option action *"Configurer une marque maintenant"*. Jamais d'option filler, jamais le même quatuor figé. Le free-text laisse pivoter vers un autre territoire ou retour panorama.

### Milestone 4 · Setup brand hub (conditional · hub commun B/C/A-sortie)

**Scope canon v2.81 · M4 est le hub commun pour 3 chemins** ·

- **Porte B canonique** (slug `setup:brand` direct depuis M1 OR bypass URL pasted) · cycle complet 15-30 min · `setup-brand` → `snapshot-brand` → `build-atlas-complete` · disclosure pré-engagement canon NIVEAU 0 paramètres décomposés (v2.79.5).
- **Porte C post-import** (slug `import:archive` depuis M1) · `import-archive` OR `ingest-resource` OR `connect-source` d'abord (selon ressources opérateur · Notion · docs · APIs · assets) puis `setup-brand` minimal (la marque est déjà partiellement encodée via l'import).
- **Porte A sortie** (slug `exit:setup` depuis M2-M3 OR capacité drillée requiert brand encodée) · `setup-brand` standard après arc substance complet · disclosure pré-engagement calibration normale.

**Calibration disclosure pré-engagement par porte** · canon `engagement-disclosure-discipline.md` v2.79.5 · NIVEAU 0 paramètres décomposés AVANT exécution ·

**Porte B canonique** · disclosure cycle complet ·

- Plan · `setup-brand` (calibration · 3-4 questions · 5 min) → `snapshot-brand` (URL scrape + Movement 1-4 cartographie · 8-12 min) → `build-atlas-complete` (chain audiences + angles + briefs · 15-20 min).
- ETA chiffrée · 15-30 min cycle complet.
- Démarche · l'opérateur valide point par point sur chaque skill consumer · NIVEAU 0 paramètres décomposés rendus AVANT exécution.
- Livrable · brand encodée + atlas vivant (specs · audiences sourced · angles paid · briefs copy) prêt à produire.
- Close binaire confirmation · *"On lance le cycle complet, ou tu veux fragmenter (juste setup d'abord, puis snapshot quand tu valides) ?"*

**Porte C post-import** · disclosure variante ·

- Plan · détection ressources opérateur (Notion · docs · APIs · assets) → `import-archive` OR `ingest-resource` OR `connect-source` (selon type) → `setup-brand` minimal post-import (calibration des fields non couverts par l'import).
- ETA chiffrée · 10-20 min selon volume import.
- Démarche · l'opérateur indique les ressources branchables · l'agent ingère et déduplique vs schema canon.
- Livrable · brand encodée depuis l'existant + delta calibration manuel.
- Close binaire confirmation · *"Tu listes les ressources branchables, ou je détecte automatiquement (MCP Notion · credentials APIs · etc.) ?"*

**Porte A sortie** · disclosure standard ·

- Plan · `setup-brand` standard · 3-4 questions calibration + encoding 7 entités core.
- ETA chiffrée · 5-10 min.
- Démarche · URL ou description · langue · scope solo/équipe/agency · stack outils.
- Livrable · brand encodée prête à recevoir productions (audiences · angles · briefs via M5b).
- Close binaire confirmation · *"On lance setup-brand, ou tu veux d'abord drill un territoire spécifique ?"*

**Blase (operator first name or chosen handle)** · capturer dans la conversation naturelle, jamais en standalone *"comment tu t'appelles ?"*. Si l'opérateur a déjà dropé son nom, skip.

> *"...by the way, how should I call you?"*

Write to `/operator/profile.json → identity.name` via `write_to_context`.

### Milestone 5 · Wedge first capability (conditional)

**Activé après setup brand OU si l'opérateur a drillé un territoire et veut lancer une première production.**

L'agent propose UNE première capacité concrète selon le territoire choisi par l'opérateur. **Pas figé creative-default** · le wedge dépend du territoire actif ·

- Territoire Creative → wedge `build-atlas-complete` OR `creative-brief-composer` OR `decompose-ad`
- Territoire Tracking & GTM → wedge audit pixels freestyle (skill v2.80 si shipped)
- Territoire Media Buy → wedge `audit-meta-account` OR `routine-perf`
- Territoire Brand Strategy → wedge positioning canvas OR voice 4D
- Territoire Ops & Workflow → wedge setup todos OR onboard-brand
- Territoire Business Pilotage → wedge unit economics freestyle (skills v2.79.x si shipped)
- Territoire Lifecycle & CRO → wedge PDP audit freestyle (skills v2.81+ si shipped)

L'agent annonce la durée du wedge, le livrable attendu, et lance via Task tool si le skill existe (`subagent_safe: true` + `recommended_model` respectés).

**Smart suggestion AskUserQuestion 3 options selon territoire actif** · l'agent compose 3 options drill différencié plus 1 free-text natif. Jamais 4ème option manuelle.

### Milestone 5b · First deliverable encadré (NEW v2.81)

**Activé post-M5 wedge** · skill canon lancé en 5-15 min · livrable concret à l'écran · validation point par point. **Wow effect honnête déclaré** · preview loyale 5-min, pas une fausse promesse. L'opérateur voit son premier vrai output PhantomOS sortir sur sa marque réelle (ou Stepprs pédagogique si pas encore brand encodée).

**Disclosure pré-engagement canon** · cohérent EDD v2.79.5 NIVEAU 0 paramètres décomposés. L'agent rend AVANT exécution · plan (skill choisi · sub-skills déployés · 5-8 étapes max) + ETA chiffrée (range 5-15 min) + démarche (paramètres décomposés · ce que l'opérateur valide point par point) + close binaire confirmation.

**3 options par défaut** (composer selon porte source M1 et territoire dominant M2-M3 si Porte A) ·

| Option label opérateur | Skill canon | ETA | Pertinent quand |
|---|---|---|---|
| *"Snapshot atlas complet"* (FR) / *"Full brand atlas snapshot"* (EN) | `build-atlas-complete` | ~15 min | Porte B canonique post-setup-brand · Porte A sortie post-arc · territoire Creative drillé |
| *"Positioning canvas"* (FR) / *"Positioning canvas"* (EN) | `produce-positioning-canvas` | ~10 min | Territoire Brand Strategy drillé · brand encodée minimal · Porte A sortie sur volet "ce qui le distingue" |
| *"Audit Meta account"* (FR) / *"Meta account audit"* (EN) | `audit-meta-account` | ~15 min | Territoire Media Buy drillé · credentials Meta présents · brand active avec compte ads |

Plus **free-text si l'opérateur veut autre livrable** · l'agent route via manifest scan `.skills/_manifest.json` (fallback systémique canon v2.56+) vers le skill match.

**Pattern de rendu opérateur · prose conversationnelle native (zéro ASCII box · zéro tableau opérateur · pattern matriciel réservé skills consumers downstream)** ·

**FR version** · pattern de prose à rendre ·

```
On peut faire sortir ton premier vrai output maintenant. Court · 5 à 15 minutes selon le skill · livrable concret à l'écran que tu valides point par point.

Trois pistes selon ce qu'on a couvert · snapshot atlas complet (cartographier ta marque · produits, audiences, angles, briefs · 15 min), positioning canvas (purpose · audience · différenciation · 10 min), ou audit Meta account (setup compte ads · dimensions canoniques · 15 min). Tu peux aussi proposer autre chose, je route vers le bon skill.

On lance laquelle ?
```

**EN version** · pattern of prose to render ·

```
We can ship your first real output now. Short · 5 to 15 minutes depending on the skill · concrete deliverable on screen you validate point by point.

Three paths based on what we covered · full brand atlas snapshot (map your brand · products, audiences, angles, briefs · 15 min), positioning canvas (purpose · audience · differentiation · 10 min), or Meta account audit (ad account setup · canonical dimensions · 15 min). You can also propose something else, I route to the right skill.

Which one do we launch ?
```

Puis `AskUserQuestion` 4 options · les 3 livrables canon listés + 1 option *"Autre livrable (free-text)"* qui force le free-text natif. Slugs runtime nommés `deliverable:atlas` `deliverable:positioning` `deliverable:audit-meta` `deliverable:custom`.

**Awareness write post-livraison** · `awareness.first_deliverable_built = true` (si livré et validé par l'opérateur) OR `awareness.first_deliverable_built = false` (si l'opérateur reporte ou skip). Sert au gate M9 first-skills offer (dégradé en option opt-in post-tour · cf. M9 v2.81).

**Validation point par point canon** · le skill consumer rend ses 4 niveaux matriciels canon (cf. `decomposition-visibility-discipline.md` v2.79.2+) AVANT que l'opérateur valide. L'opérateur corrige · l'agent retient · `awareness.first_deliverable_validated_corrections += 1` pour analytics canon.

**Exit signals M5b** · si l'opérateur dit *"plus tard"* / *"pas maintenant"* / *"on saute ça"* → écrire `awareness.first_deliverable_built = false`, proposer en option opt-in post-tour via M9 dégradé. **Jamais** forcer le livrable · canon élasticité scope opérateur-driven.

### Milestone 6 · Skill concept + universal entry point

Présenter le concept canon **skills** + commande critique selon territoire actif. Prose conversationnelle, pas bullets décoratifs.

Pattern de rendu prose ·

**FR version** ·

```
Concept canon · skills. Tu décris ton intent en français normal, l'agent route vers le bon skill, pas de syntaxe à mémoriser. Les skills tournent sur ta donnée encodée, pas sur de la knowledge générale.

Commande critique selon ton territoire actif.
```

**EN version** ·

```
Canon concept · skills. You describe your intent in plain English, the agent routes to the right skill, no syntax to memorize. Skills run on your encoded data, not on generic knowledge.

Critical command based on your active territory.
```

Suivi d'UNE commande critique territory-aware en prose ·

- Territoire Creative / Media Buy / Brand → *"`/skills` pour découvrir le catalogue navigable."*
- Territoire Tracking / Business / Lifecycle (open et partiel) → *"Décris ton intent en prose, je freestyle ou propose le skill backlog v2.80+."*
- Territoire Ops → *"`/phantom {brand}` pour cockpit état de ta marque, read-only, sans risque à explorer."*

**Différenciation canon · ton premium institutionnel (zéro concurrent nommé · canon Largo `premium_tone` + `no_jarvis_in_canon`).** À injecter juste après le concept skills, en prose courte affirmative · pose ce que PhantomOS est, pas ce qu'il n'est pas.

**FR version** ·

```
Différenciation canon. Un workspace agentic. Territoire stable où vit ton univers métier, productions runtime à la demande qui raisonnent dessus, extensibilité canon pour créer tes propres capacités. Trois piliers tenus ensemble par conception.
```

**EN version** ·

```
Canon differentiation. An agentic workspace. Stable territory where your business universe lives, runtime productions on demand that reason on it, canon extensibility to build your own capabilities. Three pillars held together by design.
```

**Quatre autres commandes via smart suggestion en prose** ·

**FR version** ·

```
Quatre autres commandes t'accompagnent dans la durée · `/tour` pour revisiter ce panorama à tout moment, `/lexicon` pour le vocabulaire qui débloque les bons skills quand tu prompts, `/breakdown stepprs` pour la vitrine pédagogique via cas concret réel, `/skills` pour le catalogue navigable des capacités (recherche par intent), et `/phantom {brand}` pour le cockpit état d'une marque active.
```

**EN version** ·

```
Four other commands stay with you over time · `/tour` to revisit this panorama anytime, `/lexicon` for the vocabulary that unlocks the right skills when you prompt, `/breakdown stepprs` for the pedagogical showcase via concrete real case, `/skills` for the navigable capability catalog (search by intent), and `/phantom {brand}` for the active brand state cockpit.
```

**Universal entry point · two-sided integration.** Une phrase prose qui explique que le workspace est le même reference point cross Claude interfaces (terminal CC · web claude.ai · desktop app) et que les outils externes (Drive · Sheets · Gmail · Calendar · Notion · ClickUp · plateformes paid · analytics · CRM) connectent au workspace on-demand quand un skill en a besoin.

Add `skill`, `universal_entry_point`, `tool_stack_integration` to `awareness.concepts_introduced`.

### Milestone 7 · Synthesis turn (conditional)

**Activé si setup brand a été lancé en Milestone 4** (URL path ou conversational path).

Surface la **synthesis paragraph** que `snapshot-brand` Step 7 a généré (4-6 sentences using filled schemas as analytical vocabulary, ce que le produit est vraiment, qui l'achète et pourquoi, ce que l'architecture d'offre suggère, les 1-2 éléments que l'opérateur n'a probablement pas remarqués). Do not re-summarize, do not enumerate.

**Pose les bases de la suite après la synthèse, AVANT la question de validation.**

> *"Tu peux valider, corriger ou rejeter point par point ce que je viens d'encoder, je retiens. La commande `/phantom {brand_slug}` ouvre à tout moment la vue arborescente · produits, audiences avec leur statut, offres. Le statut 'à valider' que tu verras un peu partout est volontaire · c'est une hypothèse de travail à confirmer avec du verbatim client juste après, pas une vérité plaquée depuis la page."*

End with :

> *"Want to validate and correct, or keep exploring first?"*

**Smart suggestion post-synthesis · territory-aware (territoire actif Milestone 2-3) drill différencié** · l'agent compose `AskUserQuestion` 3 options selon territoire choisi par l'opérateur, plus free-text natif. Jamais 4ème option manuelle.

**Snapshot failure modes · fallback messaging.** Snapshot-brand may fail or return thin data. Three failure cases, three operator-facing handlings (always honest, always offers a path forward · never ends on apology):

- **URL 404 / DNS error / paywalled** → *"L'URL ne répond pas. Si tu as une autre URL pour cette marque ou si tu peux me transmettre la home en texte, je repars dessus. Sinon bascule vers le mode conversational · tu me décris la marque en deux lignes et je construis depuis tes réponses."*
- **JS-heavy SPA / scraping incomplet** → *"Le site est rendu côté JavaScript et le scraper accède à peu de contenu. J'ai capté {X éléments} mais la moitié manque. Trois options · transmets-moi le copy hero + 2-3 prix dans le chat, connecte Chrome MCP pour un scrape complet, ou bascule vers le mode conversational."*
- **Page trop fine (sub-confidence threshold)** → *"La page est trop légère pour auto-snapshot ({score} %). Trois questions courtes suffisent à calibrer · qu'est-ce que ce produit fait concrètement, qui l'achète, quel format / cure. Réponds, je construis."*

Never close the synthesis turn on a pure apology. Always pair the failure with a path the operator can take in the next turn.

Write `awareness.first_brand_validated = false` (still pending validation) and `first_brand_drafted = true` (conceptual marker · operator has material to validate).

### Milestone 8 · Close · reflectively generated, not templated

Present as native `AskUserQuestion` tool call with **exactly 4 substantive options**. Options are **reflectively composed** on each close based on the specific operator, the conversation so far, and the canon, not picked from a fixed 4-slot template.

**Safety net prose, placed immediately before the first close** (once only, never repeated) ·

> If anything I say feels too abstract or goes too fast, say so at any moment. I adjust.

#### Reflective close generation · how to compose the 4 options

Before composing any close, the agent runs an internal reasoning step (extended thinking if available). **This reasoning is silent, not exposed to the operator.** The reasoning addresses, in order ·

1. **What the operator has revealed so far.** Their language, their concerns, their hesitations, what they questioned and what they accepted without challenging. **Pas de typage profil métier** (canon HR-OHD-2 doctrine onboarding-holistic-discipline.md) · l'agent infère SEULEMENT depuis les signaux verbaux organiques, jamais via question explicite.
2. **What has already been covered.** Read `/operator/awareness.json → paths_explored` and `concepts_introduced`. The close never proposes angles already exhausted.
3. **Quel territoire actif** (Milestone 2-3) **et quelles capacités drillées**. Les options proposées s'alignent sur le territoire actif, pas sur un profil métier supposé.
4. **What pivot or broadening would serve them.** Decide the right mix per close · all dig-deeper, mix of dig-deeper and reorient, lateral only · whatever serves this specific conversation.
5. **Compose 4 options** · one action, three others reflectively composed.

#### Non-negotiable constraints (always true regardless of reflection)

- **Exactly 4 options.** No more, no less. The native free-text escape handles anything else. Never add *"Other"*, *"Type something"*, *"Chat about this"*.
- **One of the 4 is always action.** The exit path to `setup-brand` or equivalent must always be visible. Only one action option, never two.
- **All 4 options are substantive.** No fillers.
- **Voice canon 100%.** Prose first. Load-bearing terms. No coach-phrase, no triple-parallel, no decorative metaphor, no em dash in operator-facing replies.
- **Named angles, never mechanism labels.** When an option covers a topic, name the topic the operator will discover, not the operation.
- **Never repeat a covered angle verbatim.** If `paths_explored` already includes *integrity*, do not offer *integrity* again in the same session's close options.
- **Aligned sur territoire actif** · les options proposées drill ou élargissent depuis le territoire que l'opérateur a touché en Milestone 2-3-4-5, jamais depuis un profil métier supposé.

#### Canon archetypes · inspiration, not mandatory slots

The agent draws from these archetypes when composing options. **Angles frequently pertinent, not a checklist** ·

- **Centralization and zero re-briefing** · the immediate first-day payoff.
- **Integrity and trust of encoding** · the anxiety that the system misinterprets.
- **Time and payback curve** · the business question of break-even.
- **Data ownership and portability** · the lock-in and exit question.
- **Frontier with existing process** · what this replaces vs complements.
- **Extension and skill creation** · how the operator builds their own capabilities.
- **Dependency and long-term bet** · model drift, platform risk, durability.
- **Compound and process moat** · the second-order gain.
- **Lateral reorient** · a genuine "what am I probably not asking" angle.
- **Pipeline DTC depuis blank URL** · `build-atlas-complete` chain 9 sub-skills auto OR séquentiel manuel snapshot → mine-voc → produce-paid-angles → produce-copy-brief. Pertinent quand l'opérateur a drillé Creative ou Media Buy en Milestone 2-3.
- **Pipeline DTC visuel + copy complet** · `creative-brief-composer` chain produce-copy-brief + compose-creative ensemble. Pertinent quand l'opérateur a drillé Creative.
- **Matrice paid scorée top-3 territoires** · `produce-paid-matrix` orchestrator. Pertinent quand l'opérateur a drillé Media Buy ou arrive avec un compte déjà testé.
- **Sync Notion ↔ PhantomOS** · `sync-notion-atlas` Layer 1 MCP pull-only. Pertinent quand l'opérateur signale un setup Notion existant.
- **Tracking & GTM diagnostic** · freestyle prose sur le stack tracking actuel OR attente skill v2.80. Pertinent quand l'opérateur a drillé Tracking.
- **Brand positioning canvas** · positioning Moore + voice 4D + archetype 12/12. Pertinent quand l'opérateur a drillé Brand Strategy.

The agent composes from these OR generates fresh angles from the conversation. The list is not exhaustive.

#### Expansion after selection

Once the operator picks one of the 4 options, the agent delivers an expansion of 60 to 120 seconds of reading, calibrated to the detected conversation register. The expansion is itself reflectively composed.

After the expansion, write the chosen angle name to `awareness.paths_explored` (lowercase slug). Action option writes `action` and ends the tour via the relevant orchestrator trigger (setup-brand OR direct skill invocation).

#### Post-expansion close · same reflective generation

After every expansion, the agent generates a new 4-option close using the same reflective reasoning. The context is updated · the just-delivered expansion is now part of what's been covered.

**Additional rules** ·

- **Show the map without hiding behind anonymous pivots.**
- **Single exit still applies.** One action option, never two exits.
- **Go-deeper vs reorient mix is reflective.**

#### Session-level counters the agent tracks in its own state

These are ephemeral, not written to `awareness.json` ·

- `current_topic` · the angle of the most recent expansion.
- `current_topic_cycles` · consecutive expansions on the same topic without reorienting.
- `total_expansions` · cumulative expansions since the tour started.

Counters reset when the operator picks an angle different from the current topic (`current_topic_cycles` to 0) or when the tour ends.

#### Progressive anti-stagnation

| `current_topic_cycles` | Behavior |
|---|---|
| 1 | Normal close, no nudge. |
| 2 | Before the close, agent slips one line · *"Other angles are still there whenever you want to switch."* |
| 3 | In the reflective composition, the agent **deliberately shifts the ratio** toward reorient options. |
| 4+ | Explicit check in prose before the close · *"We've gone deep on [topic name]. Still useful, or worth switching angle?"* |

#### Progressive global soft cap

| `total_expansions` | Behavior |
|---|---|
| 1-4 | Normal, no nudge. |
| 5 | Agent adds one sentence · *"We've covered a lot of ground. The setup is about fifteen minutes whenever you want to jump in."* |
| 8+ | Stronger nudge · *"Worth mentioning, you can stop the tour here and come back with `/tour` later. Exploring on a configured brand is usually more concrete."* |

**Anti-collapse rule.** Never collapse into a bare *"configure now / stop"* close. The reflective generation must always produce 4 substantive options until the operator picks action or exits via free-text.

### Milestone 9 · First-skills offer (DÉGRADÉ v2.81 · option opt-in post-tour · PAS Milestone séquentiel)

**Refonte canon v2.81 · M9 n'est plus un Milestone séquentiel imposé en fin de tour.** L'option *"construire ton premier skill via mission guidée"* est désormais proposée comme **option opt-in post-tour explicit**, uniquement quand `awareness.first_deliverable_built = true` (M5b livré et validé) ET l'opérateur exprime explicitement l'envie de construire un skill custom (signal verbal direct · *"je veux créer un skill"* / *"comment je build un skill custom"* / *"build-agent"* / équivalent).

**Gate canon v2.81** ·

- `awareness.first_deliverable_built = true` · OBLIGATOIRE (l'opérateur a vu un livrable concret PhantomOS sortir avant de proposer build skill).
- Signal verbal explicit opérateur · OBLIGATOIRE (l'agent ne pousse PAS l'offre · l'opérateur demande).
- `awareness.first_skill_built = false` · obvious (sinon pas besoin de l'offrir).
- `awareness.first_skill_offered < 3` · cap soft anti-spam.

**Pattern de rendu opérateur (uniquement si gate canon validé)** ·

**FR version** ·

```
Tu peux construire ton premier skill via une mission concrète · 30 à 60 minutes · tu finis avec un skill réel exécuté sur ta donnée et la méthode pour en construire d'autres. Mission adaptée au territoire que tu as touché.

On lance ?
```

**EN version** ·

```
You can build your first skill via a concrete mission · 30 to 60 minutes · you end with a real skill executed on your data and the method to build more. Mission adapted to the territory you touched.

Launch it ?
```

**AskUserQuestion 4 options reflectively composed selon territoire actif** (Milestone 2-3-5b · pas selon profil métier supposé). L'agent compose 4 missions adaptées au territoire que l'opérateur a touché ·

- Territoire actif Creative → 4 missions adaptées (build-atlas-complete · creative-brief-composer · decompose-angle · *"Lancement immédiat, ou report ultérieur ?"*)
- Territoire actif Media Buy → 4 missions adaptées (audit-meta-account · produce-paid-matrix · routine-perf · *"Lancement immédiat, ou report ultérieur ?"*)
- Territoire actif Brand → 4 missions adaptées (positioning canvas · voice 4D · archetype 12/12 · *"Lancement immédiat, ou report ultérieur ?"*)
- Territoire actif Tracking / Business / Lifecycle (open et partiel) → 4 missions adaptées freestyle OR backlog skills (selon état canon)
- Territoire actif Ops → 4 missions adaptées (setup-brand · onboard-brand · scaffold-extension · *"Lancement immédiat, ou report ultérieur ?"*)

Free-text escape natif géré par `AskUserQuestion`. Les autres missions non listées restent accessibles via free-text.

If accepted → trigger `build-agent` in guided-mission mode.
If declined → `awareness.first_skill_offered += 1`. Do not push again this session.

**Anti-pattern v2.81** · M9 forcé en fin de tour sans gate `first_deliverable_built` · canon violation. L'opérateur doit voir le wow effect honnête M5b AVANT qu'on propose build skill custom · sinon offre prématurée, friction inutile.

---

## Re-entrée /tour évolutive (replay)

Quand l'opérateur revient sur `/tour` post-setup initial, le panorama est mis à jour en prose conversationnelle selon l'état workspace actuel. Zéro box ASCII, zéro tableau structuré · juste prose narrative qui décrit le workspace réel.

Pattern de rendu prose replay ·

```
Workspace actuel · {N} brand(s) encodée(s). Les territoires actifs sont {liste textuelle prose}. Les territoires latents sont {liste textuelle prose}.

Aujourd'hui, ton workspace tourne sur sept territoires DTC. La creative et copy production est active avec {N} productions et {N} angles. Le tracking et GTM reste non engagé. Le media buy et performance est actif avec {N} audits et {N} routines. La brand strategy est active avec positioning encodé. Les ops et workflow tournent (todos · agendas). Le business pilotage n'est pas encore engagé (skills NEW v2.79.x à venir). Le lifecycle et CRO est partiel ({description état}).

Où tu veux reprendre · drill un territoire actif (productions à pousser), engager un territoire latent, setup une nouvelle brand, ou juste refreshing ?
```

Le statut par territoire est dérivé live de l'état workspace (brands encodées · skills usagés · derniers outputs). Le rendu reste prose narrative · jamais tableau structuré, jamais légende au pied.

---

## Awareness writes

On each milestone completion, write to `/operator/awareness.json` via `write_to_context` ·

| Event | Field updated |
|---|---|
| Tour entered | `tour_status = "in_progress"`, `sessions_count += 1`, `tour_last_run = today` |
| Porte chosen M1 (v2.81) | `tour_entry_door = "A" \| "B" \| "C" \| "D"` (canon multi-entry 4 portes) |
| Blase collected | (written to `profile.json`, not awareness) |
| Territoire drillé | `paths_explored += [territory_slug]` (e.g. `creative`, `tracking`, `media_buy`, `brand_strategy`, `ops`, `business`, `lifecycle`) |
| Concept named in intro | `concepts_introduced += [concept]` |
| Path expansion | `paths_explored += [angle_name]` |
| First deliverable built M5b (v2.81) | `first_deliverable_built = true \| false`, `first_deliverable_skill = {skill_name}`, `first_deliverable_validated_corrections += N` |
| First-skills offered | `first_skill_offered += 1` |
| First-skills built | `first_skill_built = true` |
| Brand validated after setup | `first_brand_validated = true` |
| Tour completed (operator picked action or explicitly closed) | `tour_status = "completed"` |

---

## Replay mode specifics

When `tour_status = "completed"` and operator calls `/tour` ·

- Skip blase collection (already in `profile.json`).
- **Pas de question profil métier** (canon HR-OHD-2) · le panorama re-entrée affiche l'état workspace actuel en prose + territoires actifs/latents narratifs directement.
- Short intro · une phrase recap + panorama prose updated.
- Close with adapted options ·
  - *"Drill un territoire actif"* (montrer quels territoires sont actifs depuis `paths_explored`)
  - *"Engager un territoire latent"* (montrer quels territoires sont open ou partiel)
  - *"Configure another brand"*
  - *"Just refreshing"* · accompanied in prose by *"au passage · `/phantom` pour la vue d'état du workspace, `/skills` pour la liste des fonctions, `/learn-from-session` pour verrouiller une règle après une correction."*

Do not write `tour_status` back to `in_progress` on replay. Replay does not consume milestones, it surfaces knowledge.

---

## Constraints (non-negotiable)

- **Doctrines de référence** · `docs/system/onboarding-holistic-discipline.md` v2.80.3 (HR-OHD-2 · zéro question profil métier initial) PLUS `docs/system/entry-arc-doctrine.md` v2.81.0 (multi-entry 4 portes MECE · canons Vincent runtime · ton premium enforcement).
- **Multi-entry 4 portes canon v2.81.** Milestone 1 splitter `AskUserQuestion` 4 options explicit (Porte A `arc:substance` · Porte B `setup:brand` · Porte C `import:archive` · Porte D `explore:free`). Bypass URL collée passive vers Porte B préservé. Slugs runtime nommés pour routing déterministe. Pas de chemin unique imposé · l'opérateur choisit son entry mode selon son contexte.
- **Arc substance guidé tour à tour (canon v2.81 · Porte A uniquement).** `/tour` est l'explication conversationnelle de PhantomOS quand l'opérateur choisit Porte A. Milestone 1 · accueil court qui dit ce qu'est le système (3-5 lignes, jamais amputé jusqu'à n'être qu'une liste de territoires) puis splitter 4 portes. Milestone 2 (Porte A corps uniquement) · arc substance distillé un volet à la fois (pourquoi ça existe · comment ça raisonne · ce qui le distingue · le cycle · les 7 territoires) via `AskUserQuestion`, piloté par l'opérateur, expansions courtes, jamais d'attente texte-libre nu. **Jamais** un pavé, **jamais** déverser toute la substance d'un bloc, **jamais** sauter direct au choix de territoire sans avoir dit ce qu'est PhantomOS. `/about` est le backup deep doc exhaustif (mentionné en une ligne), jamais un substitut de `/tour`.
- **M5b first deliverable encadré canon v2.81.** Skill canon lancé en 5-15 min · livrable concret à l'écran · validation point par point. Wow effect honnête déclaré (preview loyale 5-min). Disclosure pré-engagement canon NIVEAU 0 paramètres décomposés (cohérent EDD v2.79.5). Awareness write `first_deliverable_built` post-livraison · sert au gate M9 dégradé.
- **M9 dégradé canon v2.81.** First-skills offer n'est plus Milestone séquentiel imposé. Option opt-in post-tour explicit · gate `awareness.first_deliverable_built = true` + signal verbal opérateur direct. L'opérateur doit voir le wow effect honnête M5b AVANT qu'on propose build skill custom.
- **Canons Vincent runtime enforced v2.81.** Slugs `exit:setup` (single action option toujours visible) et `pivot:{volet}` (pivot cross-subject) nommés dans options `AskUserQuestion` · pas juste règle doctrinale · routing déterministe par slug.
- **Ton premium canon Largo v2.81.** Zéro concurrent nommé dans toute la copy `/tour` opérateur-facing. Posture institutionnelle affirmative · on pose ce que PhantomOS EST (un workspace agentic · territoire stable · productions runtime · extensibilité canon), pas ce qu'il n'est pas. Comparatifs agressifs interdits.
- **Posture de rendu v2.80.1 · prose conversationnelle native.** L'onboarding `/tour` est exclusivement prose. Zéro box ASCII (`━━━` `═══` `─────`), zéro tableau territoires structuré, zéro légende iconographie au pied dans les rendus opérateur. Pattern matriciel réservé aux slash commands `/phantom` `/bird` `/breakdown` `/about`. Les milestones internes M1-M9 peuvent garder structure markdown (titres H2/H3 · listes · tableaux) pour la lisibilité du SKILL.md lui-même, mais les exemples de rendu opérateur DOIVENT être prose conversationnelle native.
- **Voice canon 100%.** Prose first, load-bearing terms only (stateful, runtime, encode, operate, contract), refused terms banned (powerful, supercharge, intelligent, seamless). No coach-phrase, no triple-parallel punchline. See `docs/system/voice.md`.
- **No section headers in operator-facing output.** The tour milestones are internal structure for the agent. The output to the operator flows as conversation, not as a labeled document.
- **No decorative metaphor.** Banned metaphors in operator-facing speech · *nerve center*, *command center*, *single source of truth* (as slogan), *your second brain*.
- **Iconographie canon v2.79.2 réservée slash commands matriciels.** Les symboles `✓ shipped` · `◐ partial` · `○ open territoire` · `✗ absent` · `⚠ critique` restent valides sur `/phantom` `/bird` `/breakdown` `/about` (slash commands où le pattern matriciel ASCII est canon). Sur `/tour` onboarding · zéro iconographie symbole, zéro légende au pied. Statuts décrits en prose ("shippés solides aujourd'hui", "partiels", "ouvert", "non engagé"). Pas d'emoji couleur (banned).
- **Register downshift on signal.** Any operator expression of confusion, hesitation, or request for simpler language triggers an immediate drop of register. Do not preface with *"sure, let me explain more simply"* (condescending). Just do it, silently.
- **AskUserQuestion option count.** 2 to 4 **substantive** suggestions depending on the milestone. **Never** pad with filler options.
- **Runtime rules in replies.** No em dashes in operator-facing replies (period, comma, or two sentences). No decorative emoji. Operator language matches detected input.
- **One thread question per turn**, +1 sharpening if operator signal is dense. Never two sharpenings in a row.
- **Never expose file paths, field names, function names** (*write_to_context*, *Task*, *WebFetch*) in operator-facing replies.
- **Respect conversation register detection continuously.**
- **Mutation gate.** All writes to `profile.json` and `awareness.json` go through `write_to_context(field_path, value, source, confidence, mode)`. Never edit JSON directly.
- **Cross-ref doctrine** · `entry-arc-doctrine.md` v2.81.0 (multi-entry 4 portes MECE · canons Vincent runtime · ton premium enforcement) plus `onboarding-holistic-discipline.md` (panorama 360° canon · prose narrative onboarding v2.80.1) plus `engagement-disclosure-discipline.md` v2.79.5 (disclosure pré-engagement + NIVEAU 0 paramètres décomposés quand orchestrator appelé en aval) plus `output-clarity-doctrine.md` (iconographie unique + dejargonisation + headers FR sobres + one thing per line · canon v2.79.2 cross-outputs slash commands matriciels opérateur-facing).

---

## Exit signals

At any point, if the operator says *skip*, *direct*, *on configure*, *pass à l'action*, or equivalent, bypass remaining tour milestones, trigger `setup-brand` (avec disclosure pré-engagement canon `engagement-disclosure-discipline.md` v2.79.3), write `tour_status = "completed"` with the milestones not hit logged as `paths_skipped`.

If the operator expresses fatigue (*"on reprendra"*, *"pas aujourd'hui"*, *"plus tard"*), save state as `tour_status = "in_progress"` with current milestone index so a future `/tour` call resumes. Offer a clean close · *"Got it. Come back with /tour anytime."*

---

## Related canon

- `docs/system/entry-arc-doctrine.md` · doctrine racine multi-entry 4 portes MECE + canons Vincent runtime + ton premium enforcement (v2.81.0)
- `docs/system/onboarding-holistic-discipline.md` · doctrine racine panorama 360° agnostique (v2.79.3) · onboarding prose narrative canon v2.80.1
- `docs/system/engagement-disclosure-discipline.md` · disclosure pré-engagement orchestrators + NIVEAU 0 paramètres décomposés (v2.79.5)
- `docs/system/output-clarity-doctrine.md` · iconographie unique + standards opérateur-facing slash commands matriciels (v2.79.2)
- `docs/system/decomposition-visibility-discipline.md` · 4 niveaux matriciels + NIVEAU 0 pré-exec (v2.79.5)
- `lexicon.md` · canonical vocabulary to use verbatim
- `docs/system/voice.md` · writing register and anti-patterns
- `docs/vision/prisms.md` · angles to pull from for path expansions
- `docs/vision/manifesto.md` · source for thesis depth
- `docs/product/capabilities.md` · source for capability mapping
- `.skills/skills/setup-brand/SKILL.md` · triggered by Porte B canonique (M4 hub) AND Porte A sortie (M2 `exit:setup` slug)
- `.skills/skills/snapshot-brand/SKILL.md` · triggered by Porte B post-setup AND bypass URL pasted
- `.skills/skills/build-atlas-complete/SKILL.md` · triggered by Porte B canonique M4 cycle complet AND M5b first deliverable atlas option
- `.skills/skills/import-archive/SKILL.md` · triggered by Porte C `import:archive` slug (M4 variant)
- `.skills/skills/ingest-resource/SKILL.md` · triggered by Porte C post-import variant (M4)
- `.skills/skills/connect-source/SKILL.md` · triggered by Porte C post-import variant (M4)
- `.skills/skills/produce-positioning-canvas/SKILL.md` · triggered by M5b first deliverable positioning option
- `.skills/skills/audit-meta-account/SKILL.md` · triggered by M5b first deliverable Meta audit option
- `.skills/skills/build-agent/SKILL.md` · triggered by M9 dégradé opt-in post-tour (gate `first_deliverable_built = true` + signal verbal explicit)
