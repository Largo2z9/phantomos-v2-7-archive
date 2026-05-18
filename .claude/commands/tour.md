---
name: tour
version: v2.80.3
description: Onboarding PhantomOS · explication conversationnelle de PhantomOS déroulée tour à tour · prose native, zéro interface ASCII (réservée aux slash commands `/phantom` `/bird` `/breakdown` `/about`). Refonte v2.80.3 · accueil court qui dit ce qu'est PhantomOS, puis arc substance guidé (pourquoi ça existe · comment ça raisonne · ce qui le distingue · le cycle · les 7 territoires) distillé un volet à la fois via `AskUserQuestion`, piloté par l'opérateur, jamais un pavé, jamais une amorce amputée. `/about` reste le backup deep doc exhaustif, jamais un substitut de `/tour`. Conserve v2.80.1 prose native + v2.79.3 panorama agnostique + zéro typage profil métier initial (HR-OHD-2). Mémoire canon Largo · `feedback_no_em_dash`, `feedback_no_jargon_to_operator`, `feedback_no_overengineer`, `feedback_response_length`, `feedback_onboarding_native_prose`, `largo_cognitive_profile` (matriciel = SLASH COMMANDS, pas onboarding).
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

### Milestone 1 · Bienvenue + amorce substance

**First-run** · ouvrir par un accueil court qui dit **ce qu'est PhantomOS** de façon dense mais brève (3-5 lignes max), puis enchaîner sur la **première question guidée de l'arc substance** (Milestone 2). L'onboarding `/tour` est l'explication conversationnelle de PhantomOS · vision, fonctionnement, différenciation, territoires, distillés tour à tour et pilotés par l'opérateur. **Jamais** un pavé, **jamais** une amorce amputée qui saute direct au choix de territoire sans avoir dit ce qu'est le système. **Jamais** demander *"tu fais quoi"* / *"ton métier"* / *"ton rôle"* / *"ton profil"* (canon HR-OHD-2). `/about` reste le backup pour qui veut le détail exhaustif d'un coup · le mentionner en une ligne, jamais le substituer à `/tour`.

**Rendu opérateur · prose conversationnelle native (language opérateur FR/EN détecté, jamais codé en dur). Zéro box ASCII. Zéro tableau structuré. Zéro légende au pied. Chaque tour court, jamais un pavé.**

**FR version** · pattern de prose à rendre (accueil + amorce) ·

```
Bienvenue dans PhantomOS. C'est un workspace où vit ton opération DTC. Tu encodes ta marque une fois (produits, audiences, stratégie, learnings), et le système raisonne, exécute et apprend dessus avec toi à travers les sessions.

Concrètement · tu ne re-décris pas ton contexte client à chaque conversation, il est encodé une fois et l'agent raisonne dessus. Tu décris ton intent en langage normal, il route vers la bonne capacité, sans syntaxe à mémoriser. Sur tout ce qui est stratégique il montre sa réflexion (ce qu'il observe, ce qu'il déduit, ce qu'il ignore) et tu corriges point par point, il retient. Chaque sortie validée enrichit ta connaissance pour la suite.

Je peux te dérouler ça en quelques étapes courtes · pourquoi ça existe, comment ça raisonne, ce qui le rend singulier, le cycle de travail, et les territoires que ça couvre. Tu choisis ce qu'on creuse, et tu peux passer à la configuration d'une marque à tout moment. Si tu préfères le détail complet d'un bloc, `/about` l'a en entier.
```

**EN version** · pattern of prose to render (welcome + lead-in) ·

```
Welcome to PhantomOS. It's a workspace where your DTC operation lives. You encode your brand once (products, audiences, strategy, learnings), and the system reasons, executes and learns on it with you across sessions.

Concretely · you don't re-describe your customer context every conversation, it's encoded once and the agent reasons on it. You describe your intent in plain language, it routes to the right capability, no syntax to memorize. On anything strategic it shows its reasoning (what it observes, infers, still doesn't know) and you correct point by point, it remembers. Every validated output enriches your knowledge for what's next.

I can walk you through it in a few short steps · why it exists, how it reasons, what makes it singular, the work cycle, and the territories it covers. You pick what we dig into, and you can jump to configuring a brand at any time. If you'd rather get the full detail in one block, `/about` has it all.
```

Puis poser **immédiatement** la première question guidée de l'arc substance (Milestone 2). Pas d'attente de texte libre nu.

**Statut canon par territoire (référence interne · ne pas surfacer comme jargon · ne pas rendre en tableau opérateur · sert à alimenter le volet territoires de l'arc)** ·

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

**Replay** · short acknowledgement + panorama narratif mis à jour selon état workspace actuel (cf. § Re-entrée /tour évolutive ci-dessous).

> Bienvenue back. Que veux-tu revisiter ?

Skip to Milestone 4 directly in replay mode (close adapté).

### Milestone 2 · Arc substance guidé tour à tour

Le cœur de l'onboarding. Une boucle conversationnelle qui distille la substance de PhantomOS, un volet à la fois, pilotée par l'opérateur. Chaque tour · une question guidée `AskUserQuestion` → l'opérateur choisit un volet → expansion **courte** (prose, calibrée au registre détecté, **jamais un pavé**) → nouvelle question guidée qui propose les volets non encore vus plus l'option d'avancer. Pas d'attente de texte libre nu. C'est le retour exact du conversationnel guidé d'avant v2.79.4.

**Volets substance canon** (l'agent verbalise l'effet opérateur, jamais les noms de doctrine · canon operator-facing) ·

- **Pourquoi ça existe** · les 3 frictions DTC (contexte client réinventé chaque session, connaissance métier éclatée entre outils, apprentissages jamais capitalisés). 5-8 lignes.
- **Comment ça raisonne** · mémoire métier persistante, l'agent route ton intent vers la bonne capacité, raisonnement cadré (pas d'impro), il montre sa réflexion. L'effet, pas les noms canon. 5-8 lignes.
- **Ce qui le rend singulier** · les 4 propriétés tenues ensemble par conception · univers métier qui persiste, raisonnement cadré, exécution (pas que du texte), connaissance qui se capitalise. Posture premium · on affirme ce que fait PhantomOS, jamais un comparatif agressif ni de concurrent nommé/dénigré (canon ton Largo). 5-8 lignes.
- **Le cycle** · encode une fois, opère au quotidien, capitalise en continu. 4-6 lignes.
- **Les 7 territoires** · panorama bref des territoires DTC sur pied d'égalité (une demi-ligne chacun, équité HR-OHD-1), alimenté par la table de référence interne ci-dessus. C'est ici, pas en Milestone 1, que le panorama territoires est rendu.

**Mécanique de la boucle** (réutilise le moteur réflexif Milestone 8) ·

- `AskUserQuestion`, exactement 4 options substantives, free-text natif pour le reste. Plafond harness 4 options · l'agent compose, jamais de menu figé, jamais d'option filler.
- **Porte de sortie setup toujours visible (canon Vincent · non négociable).** Une des 4 options est TOUJOURS l'exit rapide vers la configuration d'une marque (*"Configurer une marque maintenant"*), à chaque tour, pour sortir du tunnel de questions sans friction. Single action option (miroir contrainte Milestone 8).
- **Pivot cross-subject (canon Vincent · sujets imbriqués).** Dès que l'opérateur creuse un volet en profondeur (sous-sujets imbriqués), une des options doit permettre de pivoter latéralement vers un autre volet et d'y revenir, pas seulement creuser ou avancer. L'opérateur n'est jamais enfermé dans une seule branche.
- Les 2 options restantes = volets substance non encore vus, composés selon les signaux. Après chaque expansion · écrire le volet vu dans `awareness.paths_explored`, ne jamais le re-proposer.
- **Anti-stagnation** · après 3 expansions substance, glisser une ligne *"On peut continuer à creuser, pivoter sur autre chose, ou passer à une marque concrète, comme tu veux"*. Après 4-5, l'agent oriente la composition vers l'exit setup sans fermer brutalement (anti-collapse · toujours 4 options substantives).
- Registre calibré (grounded/standard/dense/technical) selon détection live. Jamais de pavé · si un volet déborde, l'agent coupe et propose *"je peux creuser ça plus, ou on avance"*.

**Sortie de l'arc · routing** (option avancer cliquée, territoire nommé, ou free-text) ·

- **Drill territoire** · territoire nommé (creative / tracking / media buy / brand / ops / business / lifecycle) → Milestone 3.
- **Setup direct** · *"configurer"* / URL collée / *"on configure"* → `setup-brand` orchestrator (disclosure pré-engagement `engagement-disclosure-discipline.md`).
- **Skill scan** · l'opérateur veut le catalogue → `/skills`.
- **Détail exhaustif** · l'opérateur veut tout d'un bloc → pointer `/about` (backup deep doc), puis revenir à l'arc ou avancer.
- **Free-text autre** · intent non-listé → l'agent interprète et route, jamais re-poser *"tu fais quoi"*.

**Pattern · URL e-com pasted déclenche proactive chain.** Si l'opérateur paste une URL e-com à n'importe quel tour de l'arc → lancer `snapshot-brand` en async (background), setup minimal en parallèle (langue · scope solo/équipe/agency · pas de question profil métier), synthèse Milestone 7. Anti-pattern · attendre la fin de l'arc avant de lancer le scrape.

**Mode fast-track opérateur expert** (post-N brands setup OR flag explicit) · proposer d'emblée l'option avancer en tête, arc substance disponible mais non imposé.

Write the active mode to `/operator/awareness.json` transient field `tour_mode: "substance" | "drill" | "setup" | "skills" | "freestyle"`.

### Milestone 3 · Drill territoire (conditional)

**Si l'opérateur a choisi de drill un territoire en Milestone 2**, l'agent zoom sur ce territoire avec un sous-panorama en prose conversationnelle. Zéro box ASCII. Zéro tableau. Juste prose narrative qui décrit les capacités câblées et le démarrage possible.

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

### Milestone 4 · Setup brand minimum (conditional)

**Activé si l'opérateur choisit Setup direct en Milestone 2** OR si une capacité drillée en Milestone 3 requiert une brand encodée (cartographier audiences · audit compte Meta · etc.).

**Setup brand minimum** · trigger `setup-brand` orchestrator. Disclosure pré-engagement canon `engagement-disclosure-discipline.md` v2.79.3 ·

- Annonce ce que setup-brand fait (snapshot URL + 3-4 questions calibration + encoding 7 entités core)
- Annonce la durée (5-10 min)
- Annonce ce qui sera demandé (URL ou description · langue · scope solo/équipe/agency · stack outils)
- Annonce le livrable (brand encodée prête à recevoir productions)

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

### Milestone 6 · Skill concept + universal entry point

Présenter le concept canon **skills** + commande critique selon territoire actif. Prose conversationnelle, pas bullets décoratifs.

Pattern de rendu prose ·

```
Concept canon · skills. Tu décris ton intent en français normal, l'agent route vers le bon skill, pas de syntaxe à mémoriser. Les skills tournent sur ta donnée encodée, pas sur de la knowledge générale.

Commande critique selon ton territoire actif.
```

Suivi d'UNE commande critique territory-aware en prose ·

- Territoire Creative / Media Buy / Brand → *"`/skills` pour découvrir le catalogue navigable."*
- Territoire Tracking / Business / Lifecycle (open et partiel) → *"Décris ton intent en prose, je freestyle ou propose le skill backlog v2.80+."*
- Territoire Ops → *"`/phantom {brand}` pour cockpit état de ta marque, read-only, sans risque à explorer."*

**Différenciation canon · à injecter juste après le concept skills, en prose courte ·**

```
Différenciation canon. Notion stocke du texte indexable. Airtable structure des données interrogeables. Les SOPs documentent des process humains. PhantomOS opère sur ton univers business via un agent. Trois piliers · territoire stable, productions runtime à la demande, extensibilité canon.
```

**Quatre autres commandes via smart suggestion en prose** ·

```
Quatre autres commandes t'accompagnent dans la durée · `/tour` pour revisiter ce panorama à tout moment, `/lexicon` pour le vocabulaire qui débloque les bons skills quand tu prompts, `/breakdown stepprs` pour la vitrine pédagogique via cas concret réel, `/skills` pour le catalogue navigable des capacités (recherche par intent), et `/phantom {brand}` pour le cockpit état d'une marque active.
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

### Milestone 9 · First-skills offer (conditional, end of tour only)

If operator reached the end of the tour AND first-skill has not been built (`awareness.first_skill_built = false`) AND first_skill_offered count < 3 :

**Prose hook** ·

> One last thing. Tu peux construire ton premier skill via une mission concrète · 30 à 60 minutes · tu finis avec un skill réel exécuté sur ta donnée et la méthode pour en construire d'autres.

**AskUserQuestion 4 options reflectively composed selon territoire actif** (Milestone 2-3 · pas selon profil métier supposé). L'agent compose 4 missions adaptées au territoire que l'opérateur a touché ·

- Territoire actif Creative → 4 missions adaptées (build-atlas-complete · creative-brief-composer · decompose-angle · *"Lancement immédiat, ou report ultérieur ?"*)
- Territoire actif Media Buy → 4 missions adaptées (audit-meta-account · produce-paid-matrix · routine-perf · *"Lancement immédiat, ou report ultérieur ?"*)
- Territoire actif Brand → 4 missions adaptées (positioning canvas · voice 4D · archetype 12/12 · *"Lancement immédiat, ou report ultérieur ?"*)
- Territoire actif Tracking / Business / Lifecycle (open et partiel) → 4 missions adaptées freestyle OR backlog skills (selon état canon)
- Territoire actif Ops → 4 missions adaptées (setup-brand · onboard-brand · scaffold-extension · *"Lancement immédiat, ou report ultérieur ?"*)

Free-text escape natif géré par `AskUserQuestion`. Les autres missions non listées restent accessibles via free-text.

If accepted → trigger `build-agent` in guided-mission mode.
If declined → `awareness.first_skill_offered += 1`. Do not push again this session.

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
| Blase collected | (written to `profile.json`, not awareness) |
| Territoire drillé | `paths_explored += [territory_slug]` (e.g. `creative`, `tracking`, `media_buy`, `brand_strategy`, `ops`, `business`, `lifecycle`) |
| Concept named in intro | `concepts_introduced += [concept]` |
| Path expansion | `paths_explored += [angle_name]` |
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

- **Doctrine de référence** · `docs/system/onboarding-holistic-discipline.md` v2.80.3. HR-OHD-2 · zéro question profil métier initial.
- **Arc substance guidé tour à tour (canon v2.80.3).** `/tour` est l'explication conversationnelle de PhantomOS. Milestone 1 · accueil court qui dit ce qu'est le système (3-5 lignes, jamais amputé jusqu'à n'être qu'une liste de territoires). Milestone 2 · arc substance distillé un volet à la fois (pourquoi ça existe · comment ça raisonne · ce qui le distingue · le cycle · les 7 territoires) via `AskUserQuestion`, piloté par l'opérateur, expansions courtes, jamais d'attente texte-libre nu. **Jamais** un pavé, **jamais** déverser toute la substance d'un bloc, **jamais** sauter direct au choix de territoire sans avoir dit ce qu'est PhantomOS. `/about` est le backup deep doc exhaustif (mentionné en une ligne), jamais un substitut de `/tour`.
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
- **Cross-ref doctrine** · `onboarding-holistic-discipline.md` (panorama 360° canon · prose narrative onboarding v2.80.1) plus `engagement-disclosure-discipline.md` (disclosure pré-engagement quand orchestrator appelé en aval) plus `output-clarity-discipline.md` (iconographie unique + dejargonisation + headers FR sobres + one thing per line · canon v2.79.2 cross-outputs slash commands matriciels opérateur-facing).

---

## Exit signals

At any point, if the operator says *skip*, *direct*, *on configure*, *pass à l'action*, or equivalent, bypass remaining tour milestones, trigger `setup-brand` (avec disclosure pré-engagement canon `engagement-disclosure-discipline.md` v2.79.3), write `tour_status = "completed"` with the milestones not hit logged as `paths_skipped`.

If the operator expresses fatigue (*"on reprendra"*, *"pas aujourd'hui"*, *"plus tard"*), save state as `tour_status = "in_progress"` with current milestone index so a future `/tour` call resumes. Offer a clean close · *"Got it. Come back with /tour anytime."*

---

## Related canon

- `docs/system/onboarding-holistic-discipline.md` · doctrine racine panorama 360° agnostique (v2.79.3) · onboarding prose narrative canon v2.80.1
- `docs/system/engagement-disclosure-discipline.md` · disclosure pré-engagement orchestrators (v2.79.3)
- `docs/system/output-clarity-discipline.md` · iconographie unique + standards opérateur-facing slash commands matriciels (v2.79.2)
- `lexicon.md` · canonical vocabulary to use verbatim
- `docs/system/voice.md` · writing register and anti-patterns
- `docs/vision/prisms.md` · angles to pull from for path expansions
- `docs/vision/manifesto.md` · source for thesis depth
- `docs/product/capabilities.md` · source for capability mapping
- `.skills/skills/setup-brand/SKILL.md` · triggered by action path
- `.skills/skills/build-agent/SKILL.md` · triggered by first-skills offer
