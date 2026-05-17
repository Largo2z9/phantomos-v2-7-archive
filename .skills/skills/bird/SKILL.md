---
name: bird
type: navigator
version: "0.2.1"
recommended_model: sonnet
subagent_safe: true
user_invocable: true
isolation_scope: workspace_global
layer: meta
description: >
  Vue d'oiseau sur un projet ou une brand active. Recale l'opérateur instantanément après reprise de session ou perte de fil, en rendant le territoire entier visible (zones acquises, zones bloquées, zones identifiées non engagées, zones non cartographiées). Lit la carte produite par /scope, ne la crée pas. Pair canon avec /scope (scope CRÉE la carte d'un sujet flou · bird LIT la carte).
  FR: "où on en est", "j'ai perdu le fil", "fais-moi un bird", "vue d'oiseau", "/bird", "/bird all", "/bird --zoom {zone}".
  EN: "where are we", "I lost the thread", "give me a bird's eye", "/bird", "/bird all", "/bird --zoom {zone}".
argument-hint: "[brand-slug or all] [--zoom zone]"
allowed-tools: Read, Glob, Grep, Bash
permissions:
  reads: ["brands/", "docs/"]
  writes: []
  mode: none
  subagent_safe: true
disambiguates_against:
  brief-day: "bird zoom sur 1 brand/projet (recadrage session) · brief-day scan workspace entier au start (todos, P0/P1, status portfolio cross-brands)."
  goodnight: "bird ouverture/recadrage milieu de session · goodnight clôture fin journée."
  generate-handoff: "bird = lecture rapide état (consommé immédiatement) · generate-handoff = artefact dense pour prochaine session."
  scope: "bird LIT la carte d'un projet existant · scope CRÉE la carte d'un sujet flou. Pair canon."
  resume-session: "bird = vue spatiale macro territoire · resume-session = reprise narrative du dernier thread actif."
pipeline:
  preconditions:
    - "brand ou projet identifiable (argument explicite OR pwd match OR portfolio actif)"
  postconditions:
    - "vue spatiale ASCII rendue (grille de zones ou anatomie zone)"
    - "≥2 zones en fog → hook 1-ligne vers extension-discovery / scope si pertinent"
    - "iconographie canon respectée (✓ ◐ ○ ✗ ⚠ ▓░ ► ──▶ · zéro emoji couleur · légende au pied)"
---

# Bird · Vue d'oiseau projet

Recaler l'opérateur en 5 secondes par une carte du territoire entier du projet ou de la brand, pas un status report.

## Doctrine

L'opérateur jongle plusieurs brands / projets profonds. Quand il revient sur un territoire après une absence ou une zone d'attention longue, il devient aveugle à son propre périmètre. `/bird` rend visible ·

1. **Anti-tunnel** · ce qu'il ne voit plus (zones oubliées, fog)
2. **Allocation d'énergie** · où il reste à pousser pour faire avancer
3. **Relations** · qui dépend de qui, qui débloque quoi

Les trois fonctions sont encodées dans **une seule vue macro composite**, pas trois commandes séparées.

## Hard Rules

### HR-1 · Output spatial obligatoire

La carte (grille de zones ASCII) est le cœur de l'output. Pas de version texte-only. Si tu ne sais pas spatialiser, c'est que tu n'as pas assez compris le projet, relis avant d'écrire.

### HR-2 · Le territoire d'abord, l'état après

Toutes les zones du projet existent visuellement, même celles à 0%. Une zone vierge prend autant de place qu'une zone à 95%. Sinon le fog ne se voit pas, le skill rate sa fonction.

### HR-3 · Stabilité visuelle inter-sessions

Les zones gardent leur position dans la grille d'une invocation à l'autre. L'opérateur reconnaît son terrain comme un joueur reconnaît sa carte. Pas besoin de recharger le mental model à zéro.

### HR-4 · Registre sobre institutionnel accessible

Le ton doit permettre à un externe non-familier du projet de comprendre la carte. Trois interdits ·

- Pas de métaphores ludiques (jamais "Tuyauterie", "Règles du jeu", "Terrain de chasse")
- Pas de jargon projet brut non expliqué (pas "DRGFP", "HR-20", "canon-tool" tels quels dans les labels)
- Pas de prose narrative ("Aujourd'hui tu as 3 audits qui...")

Le bon registre · termes consacrés sobres (Fondations, Infrastructure, Production, Assurance Qualité, Déploiement, Agents, Modèle de données) + descriptions factuelles courtes.

### HR-5 · Révélation > confirmation

Au moins une fois sur trois, l'output doit faire dire à l'opérateur "ah merde j'avais oublié X". Si le bird ne révèle jamais rien, il est inutile. C'est le test de viabilité du skill.

### HR-6 · Zéro em-dash

Substituer par parenthèses, virgule, point, deux-points ou middle dot (·).

### HR-7 · Investigation posture (alignement canon)

Les zones du bird portent leur étiquette d'origine ·
- **Acquis** = observé (artefacts effectifs persistés workspace · skill executé · entité encodée · doc shipped)
- **En cours** = observé partiel + déduit (work-in-progress signalé par decisions.md ou commits récents)
- **Identifié non engagé** = déclaré (mentionné en todos.md ou decisions.md, jamais démarré)
- **Non cartographié** = inconnu (zone implicite jamais formalisée, fog detection)

Cross-ref `docs/system/investigation-posture.md`.

### HR-8 · Iconographie canon unifiée (cohérence cross-commands)

Symboles uniques cohérents cross-commands opérateur-facing (pair canon `/phantom`) ·

| Symbole | Sens |
|---|---|
| `✓` | acquis · observé |
| `◐` | en cours · partiel |
| `○` | identifié · non engagé |
| `✗` | absent · non cartographié |
| `⚠` | alerte · attention requise |
| `▓░` | barre de complétion (visuel territoire) |
| `►` | position courante |
| `──▶` | dépendance entre zones |

**Zéro emoji couleur** (🔥 🟢 🟡 🔴 etc) où que ce soit dans l'output. Légende rendue au pied de chaque output (jamais en tête).

**Lexique opérateur · substitutions canon pour rester accessible non-expert** ·

| Interne | Opérateur-facing |
|---|---|
| données manquantes | (zone vide cartographiée) |
| fiche incomplète | (zone observée partielle) |
| spec incomplète | (entité encodée atomes manquants) |
| voix client manquante | (pas de verbatims sourcés) |
| tâche de fond | (skill en exécution silencieuse) |
| changement | (mutation entité) |
| alertes | (zones à surveiller) |
| action verbalisée | (jamais le nom du skill brut · *"creuser la zone"* pas *"scope X"*) |

`fog` reste canon `/bird` signature. Définition au pied de chaque output · *"fog = zone identifiée non engagée ou non cartographiée, point aveugle du territoire"*.

## Modes

```
/bird                       vue macro composite, brand/projet actif
/bird {nom}                 vue macro brand/projet nommé
/bird all                   vue multi-brands (mini-territoires comparés)
/bird --zoom {zone}         vue micro d'une zone scopée du projet courant
```

## Workflow

### 1. Détecter le projet/brand actif

Cascade dans l'ordre, s'arrêter au premier hit ·

1. Argument explicite (`/bird stepprs`) → brand = stepprs
2. `pwd` matche `brands/{x}/` ou sous-dossier → brand = x
3. Dernier commit `git log -1 --name-only` touche `brands/{x}/` → brand = x
4. Sinon · lire la liste des brands actifs (exclude `_`-prefixed), prendre la brand avec `status.json` dernière activité la + récente

Si ambigu (2 candidats équivalents) · afficher les 2 noms et demander en 1 ligne.

### 2. Chercher la cartographie

Lire `brands/{brand}/scope-map.md` (artefact produit par `/scope`).

**Si présent** → utiliser comme source des zones du projet.

**Si absent** → afficher ce message une fois et continuer en mode dégradé ·

```
Aucune cartographie scope trouvée pour {brand}.
Recommandé · lance `/scope {brand}` une fois pour stabiliser le territoire.
Mode dégradé · zones déduites des decisions / todos / structure dossiers.
```

En mode dégradé · déduire les zones depuis `status.json`, `todos.md` (si présent), `pending-validations.md`, `session-state.md`, et la structure des dossiers de la brand. Annoter dans l'output que la carte est déduite (mention discrète en bas, pas dans la grille).

### 3. Composer la vue macro

Lire en parallèle ·

- `brands/{x}/status.json` (statut setup, validation, completion)
- `brands/{x}/_snapshot.md` si présent (digest brand 1-2KB)
- `brands/{x}/pending-validations.md` (validations en attente)
- `brands/{x}/session-state.md` (dernier thread actif)
- `brands/{x}/todos.md` si présent (premiers items P0/P1)
- `git log -10 --oneline -- brands/{x}/`

Pour chaque zone identifiée ·

- Niveau de complétion (déduit · entités encodées / total + densité commits récents)
- État · acquis ✓ · en cours ◐ · identifié non engagé ○ · non scopé ✗
- Énergie à déployer ⚠ si la zone est en aval d'un blocage actif
- Dépendances ──▶ vers les zones suivantes

### 4. Format output macro

Plafond · ~50 lignes total. Structure invariante ·

```
{Nom brand/projet} · {pitch 1 ligne sobre}                   {version / phase}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Vision · {1 à 2 lignes du positionnement, sobre, accessible}

[GRILLE DE ZONES · 6 à 9 zones · barres de complétion · flèches de dépendance · zones non engagées en pointillés · position ► visible]

──────────────────────────────────────────────────────────────────────

► POSITION ACTUELLE
  {Zone} · {Sous-zone si applicable}
  {2 à 4 lignes · ce qui se passe dans cette zone, l'enjeu courant.
   Factuel, accessible à un externe, pas de jargon brut.}

  Arbitrage en suspens · {2 options numérotées avec trade-off chacune}

  ZONES BLOQUÉES PAR CET ARBITRAGE
  {2 à 3 lignes · quelles zones attendent et pourquoi}

○ ZONES IDENTIFIÉES NON ENGAGÉES
  {zone} · {description courte + statut, pourquoi pas démarré}

✗ ZONES NON CARTOGRAPHIÉES
  {1 ligne signal · pour décider quoi prioriser, voir `/scope` pour creuser}

──────────────────────────────────────────────────────────────────────
Légende ·
  ✓ acquis · ◐ en cours · ○ identifié non engagé · ✗ non cartographié · ⚠ alerte
  ▓░ complétion · ► position courante · ──▶ dépendance
  fog · zone identifiée non engagée ou non cartographiée, point aveugle du territoire

[Si ≥2 zones en fog (○ ou ✗) OU couplages flous détectés, ajouter ·]

── ANGLE MORT FLAGUÉ ──
{1 phrase factuelle nommant le plus saillant}  →  `/scope {zone}` pour creuser
```

**Hook scope (léger)** · déclenché automatiquement par `/bird` quand le territoire présente ≥2 zones en fog (`○` ou `✗`) ou des couplages implicites entre zones actives non formalisés. Strictement 1 ligne, ne nommer que l'angle mort le plus critique. Ne jamais faire l'audit ici, juste signaler le pointeur vers `/scope`.

### 5. Format output micro (--zoom)

Quand `/bird --zoom {zone}` est invoqué · afficher l'anatomie d'une seule zone.

```
{Brand} · {Zone}                                        anatomie
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Parent      [ {Macro-zone parent} · {complétion} ]  ◀── revenir
Position    ► ICI

╔═══ ACQUIS (observé) ══════════════════════════════════════════╗
║  ✓ {élément 1 · source}                                       ║
║  ✓ {élément 2 · source}                                       ║
╚═══════════════════════════════════════════════════════════════╝

╔═══ EN COURS (observé partiel + déduit) ═══════════════════════╗
║  ◐ {décision/action courante}                                 ║
╚═══════════════════════════════════════════════════════════════╝

╔═══ OUVERT (déclaré, non engagé) ══════════════════════════════╗
║  ○ {item non tranché 1}                                       ║
║  ○ {item non tranché 2}                                       ║
╚═══════════════════════════════════════════════════════════════╝

╔═══ DÉPENDANCES SORTANTES ═════════════════════════════════════╗
║  Débloque ▶ {zone aval 1}                                     ║
║  Débloque ▶ {zone aval 2}                                     ║
╚═══════════════════════════════════════════════════════════════╝

──────────────────────────────────────────────────────────────────────
Légende · ✓ acquis · ◐ en cours · ○ identifié · ▶ débloque

Next · {1 ligne · action ou décision immédiate}
```

Si la zone demandée n'est pas dans la scope-map · afficher `Zone "{x}" non cartographiée. Lance /scope {x} pour ouvrir.` et stop.

### 6. Format output all

Pour `/bird all` · afficher un mini-territoire par brand active (lus depuis la liste brands actives, exclude `_`-prefixed).

```
{N} brands actives · {date}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌─────────────────────────────────────────────────────────────────┐
│ {Brand 1}                                  {STATUT setup}        │
│ ▓▓▓▓▓▓▒░░░  {version / phase courte}                            │
│ ► {position courante 1 ligne}              dernière act · {N}j   │
│ ⚠ {flag énergie ou risque si applicable}                        │
└─────────────────────────────────────────────────────────────────┘

[répéter par brand active, ordre · priorité/activité, puis dernière session]

──────────────────────────────────────────────────────────────────────
Légende · ✓ acquis · ◐ en cours · ○ identifié · ✗ non cartographié · ⚠ alerte

Focus session probable · {brand la + chaude}
Alerte stale · {brands >30j sans activité}
Drill · `/bird {nom}` pour entrer dans une brand
```

## Anti-patterns

- Liste de commits récents
- "Voici ce que j'ai compris du projet · ..."
- Sections H2/H3 multiples
- Tableau markdown standard (≠ représentation spatiale)
- Recommandations stratégiques longues (autre skill)
- Inventaire de fichiers touchés
- Em-dash
- Métaphores ludiques pour les noms de zones
- Jargon projet brut non expliqué dans les labels
- Prose narrative dans le bloc bas
- **AP-NEW · Emoji couleur dans output (v0.2.1)** · NEVER ship `/bird` avec 🔥 🟢 🟡 🔴 ou tout autre emoji couleur. Iconographie unique canon ✓ ◐ ○ ✗ ⚠ ▓░ ► ──▶. Cohérence cross-commands opérateur-facing (pair canon `/phantom`).
- **AP-NEW · Légende absente au pied (v0.2.1)** · NEVER ship output sans légende symboles + définition `fog` au pied. Opérateur externe ne décode pas l'iconographie sans légende.
- **AP-NEW · Jargon interne brut leak (v0.2.1)** · NEVER laisser `coquilles vides`, `passe légère`, `spec light`, `verbatims sparse`, `background actif`, `mutation`, `hot spots`, ou noms de skills bruts (`scope X`, `mine-voc Y`) dans l'output opérateur-facing. Lexique opérateur HR-8 obligatoire.

## Cross-référence

- **scope (pair canon)** · `/scope` produit la `brands/{slug}/scope-map.md` que `/bird` lit. Sans scope-map, `/bird` opère en mode dégradé sur status.json + structure dossiers. Pair canon `scope crée la carte · bird lit la carte`.
- **brief-day** · briefing macro cross-brands au start de session. `/bird` zoome sur 1 brand spécifique.
- **resume-session** · reprise narrative thread actif. `/bird` est spatial macro, `resume-session` est narratif local.
- **Investigation Posture** · `docs/system/investigation-posture.md` (étiquettes observé / déduit / inconnu utilisées pour catégoriser zones).
- **brands/{slug}/_snapshot.md** · digest 1-2KB lu en priorité pour vue brand state rapide (cf `docs/system/architecture.md`).

## Version

**v0.2.1** · hygiène output canon Vercel/GitHub clarté. Iconographie unifiée canon (✓ ◐ ○ ✗ ⚠ ▓░ ► ──▶ · zéro emoji couleur · légende obligatoire au pied de chaque output) cohérente cross-commands opérateur-facing (pair canon `/phantom`). Lexique opérateur HR-8 (substitutions internes → opérateur-facing · `fog` canon signature préservé avec définition au pied). Séparateurs `━━━━━━` macro-sections + `──────` sous-sections (whitespace généreux). RETIRÉ Section Decomposition Visibility territoire-level (la doctrine reste canon ailleurs · sur `/bird` la décomposition produit n'a pas sa place · territoire = zones projet, pas reverse engineering produit). NEW HR-8 iconographie canon unifiée · NEW AP-NEW 3 anti-patterns (emoji couleur · légende absente · jargon interne leak). Backward compat strict additif · Steps 1-4 (détection · cartographie · composition · format macro) preserved · Step 5 micro --zoom preserved · Step 6 all preserved · contrat fonctionnel `/bird` inchangé (cascade détection projet, modes --zoom, all).

v0.2.0 · ship Decomposition Visibility territoire-level canon v2.79+ (Section 4.5 post-grille macro · 4 niveaux matriciels). RETIRÉ en v0.2.1 (doctrine reste canon ailleurs · pas sa place sur territoire-level lecture).

v0.1.0 · port workspace-template depuis root largo-kb. Aligné canon · scope-map.md persisté dans `brands/{slug}/`, hook scope (pas unfog · skill non-shipped workspace-template v0.1), étiquettes investigation-posture (observé / déduit / déclaré / inconnu) intégrées dans les zones. Extensions prévues · v0.2 vue temporelle (timeline activité par zone), v0.3 diff inter-sessions (zones bougé depuis dernière invocation).
