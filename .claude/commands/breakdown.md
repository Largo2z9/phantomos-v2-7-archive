---
name: breakdown
description: Vitrine pédagogique PhantomOS via le cas Stepprs (brand pédagogique du cas canonique PhantomOS, marque réelle stepprs.com avec certains financials et verbatims mockés pour la pédagogie). 13 topics drillables structurés en 5 couches d'un système opérationnel plus 3 dimensions transverses · principe · atomicité · fractalité · composition · matrices · règles · templates · métriques · rituels · production · intelligence · apprentissage · extension. Ordre suggéré 1 à 10 (parcours couches) puis 11 à 13 (transverses qui scellent le parcours). Drill direct possible sur tout topic. Patch v2.79.2 · hygiène cohérente sprint slash commands (iconographie unique ✓ ◐ ○ ✗ ⚠ · légende canonique pied de fiche · headers FR sobres maintenus). Patch v2.79.1 · section transversale Decomposition Visibility canon (4 niveaux matriciels appliqués cas Stepprs encoded · doctrine racine cross-skills opérateur-facing).
version: 2.79.2
---

# `/breakdown stepprs {topic}` · vitrine pédagogique PhantomOS

**Disclaimer canon** · PhantomOS est le sujet de ce parcours. Stepprs est l'illustration pédagogique partagée (marque réelle stepprs.com avec certains financials et verbatims mockés pour la pédagogie). Agents et opérateurs peuvent référencer Stepprs comme cas concret pour clarifier ou illustrer un concept canon, JAMAIS l'utiliser comme runtime brand active. Si l'opérateur parle de "sa marque", l'agent regarde dans `brands/` (folders sans préfixe `_`), JAMAIS dans `_EXAMPLE/`.

Slash command qui démontre la grammaire opérationnelle PhantomOS via le cas concret Stepprs (brand pédagogique cas canonique · cf `_EXAMPLE/README.md`, foot care DTC encodée canon dans `brands/_EXAMPLE/`). L'agent source les fichiers Stepprs live à chaque invocation, pas dump statique.

**Cible audience** · opérateur novice complet (vibecoder, domain expert hors marketing, curieux). Pas un marketeur. Vocabulaire universel, ZERO jargon supposé connu. Premier contact avec un système opérationnel structuré. Ton institutionnel sérieux mais accessible, vulgarisé, jamais sales-bro.

**Promesse** · expliquer ce qui rend PhantomOS reproductible (cohérence 95% output cross-session) en 13 topics, avec Stepprs comme cas filé. Chaque topic = une couche ou une dimension transverse du système. Comprendre les 5 couches + 3 transverses = maîtriser n'importe quel domaine.

## Architecture pédagogique · 5 couches d'un système opérationnel

PhantomOS n'est pas une CRM enrichie. C'est un système opérationnel composé de 5 couches qui fonctionnent ensemble.

```
COUCHE        RÔLE                              CE QUE ÇA PRODUIT
─────────     ────────────────────────────      ─────────────────────────
1 MODÈLE      Comment encoder le savoir         Atomes connectés réutilisables
2 RÈGLES      Comment cadrer le raisonnement    Outputs reproductibles
3 TEMPLATES   Comment réutiliser ce qui marche  Production rapide qualité constante
4 MÉTRIQUES   Comment se corriger               Feedback chiffré + traçabilité
5 RITUELS     Comment durer dans le temps       Système qui ne se dégrade pas
```

**Plus 3 dimensions transverses qui scellent le parcours** ·

```
DIMENSION       RÔLE                                  CE QUE ÇA PRODUIT
─────────────   ────────────────────────────────      ─────────────────────────
11 INTELLIGENCE Comment les 5 couches ensemble        Raisonnement contextuel
                produisent du raisonnement adapté     adapté à chaque cas
12 APPRENTISSAGE Comment le système s'auto-améliore   Compound effect au fil
                via promotion entre couches            du temps
13 EXTENSION    Comment PhantomOS absorbe              Système extensible pas
                ce qui n'est pas shipped               rigide
                (4 chemins canon)
```

Les 13 topics du parcours couvrent ces 5 couches plus 3 dimensions transverses.

## Mode detection

| Argument | Mode |
|---|---|
| empty (`/breakdown stepprs`) | **index** · liste les 13 topics + parcours suggéré + diagramme 5 couches + 3 transverses |
| topic name (e.g. `/breakdown stepprs composition`) | **drill** · génère la fiche du topic sourçant Stepprs live |
| invalid topic | **redirect** · liste les 13 topics valides en 1 ligne, demande choix |

**Topics valides** · `principe` · `atomicite` · `fractalite` · `composition` · `matrices` · `regles` · `templates` · `metriques` · `rituels` · `production` · `intelligence` · `apprentissage` · `extension`

## Mode index, default

Si l'opérateur tape `/breakdown stepprs` sans arg, sortir exactement ceci (rendu fidèle, pas paraphrase) ·

```
══════════════════════════════════════════════════════════════════════
COMPRENDRE PHANTOMOS · expliqué via le cas pédagogique Stepprs
══════════════════════════════════════════════════════════════════════

  PhantomOS est le sujet. Stepprs est l'illustration. Marque réelle
  (stepprs.com) utilisée comme cas canonique partagé pour rendre
  tangibles les concepts back-end. Ce n'est PAS ta marque.
  Ta marque vit dans brands/{ton-slug}/, jamais dans _EXAMPLE/.

PRINCIPE    COUCHE 1 MODÈLE      COUCHE 2 RÈGLES    COUCHE 3       COUCHE 4       COUCHE 5    DÉMO
─────────   ────────────────     ────────────────   TEMPLATES      MÉTRIQUES      RITUELS     ────

1. principe → 2. atomicité    → 6. règles       →  7. templates → 8. métriques → 9. rituels → 10. production
              3. fractalité
              4. composition
              5. matrices

DIMENSIONS TRANSVERSES · scellent le parcours
─────────────────────────────────────────────

11. intelligence    (raisonnement contextuel grâce aux variables paramétrées)
12. apprentissage   (cycle de promotion entre couches · compound effect)
13. extension       (comment PhantomOS absorbe ce qui n'est pas shipped)

Ordre suggéré · 1 → 10 (parcours couches) puis 11 à 13 (transverses)
Drill direct · /breakdown stepprs {topic}
══════════════════════════════════════════════════════════════════════
```

## Mode drill · génération fiche topic

Pour chaque topic, appliquer le **format output canonique strict** ci-dessous, en sourçant les fichiers Stepprs spécifiques au topic (cf section "Topic guides").

### Format output canonique (sections, ordre strict)

```
══════════════════════════════════════════════════════════════════════
{TITRE TOPIC} · {sous-titre}
══════════════════════════════════════════════════════════════════════

  {Intro contextuelle 2-3 lignes. Pattern · "Avant d'attaquer ta propre
   marque, regarde Stepprs..." ou "Pour comprendre pourquoi PhantomOS
   tient dans le temps, regarde comment Stepprs..."}

{NOM SECTION CLÉ}
  {Contenu pédagogique en langage courant. Premier emploi d'un mot
   technique, expliquer inline. Exemple "audience (le groupe de
   personnes visé)".}

  ✦ {annotation inline qui décompresse · pas un emoji décoratif ·
     un repère visuel sobre pour signaler "ce qu'il faut retenir"}

{NOM SECTION 2}
  {Contenu. Diagramme cartographique ASCII obligatoire dans la section
   qui montre "ce qui rend ça possible" structurellement.}

CE QUE ÇA CHANGE POUR TOI
  {2-3 lignes. ROI implicite, jamais pitch. Comment l'opérateur applique
   ce principe sur sa propre activité.}

POUR ALLER PLUS LOIN
  → {action 1}                /breakdown stepprs {topic}
  → {action 2}                /breakdown stepprs {topic}
  → Continuer le parcours     /breakdown stepprs {topic+1}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Légende iconographie (canon sprint v2.79.2)
  ✓ complet OK    ◐ partiel    ○ vide    ✗ absent    ⚠ critique
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Règles strictes pour l'agent runtime** ·
- **ZERO file path exposé** operator-facing (jamais `audiences/workers-shifts/profile.json`)
- **ZERO field name JSON exposé** operator-facing (jamais `_meta.cross_narrative_notes`, `evidence_verbatim`)
- **ZERO acronyme doctrine non-traduit** · OTRB peut rester si expliqué inline première occurrence. SED, CMR, SAD, SED-X, IP, VOC JAMAIS exposés.
- **Vocabulaire universel** · première occurrence d'un terme métier, expliquer inline en langue courante. Exemple · "DTC (vente directe au consommateur, sans intermédiaire)". Exemple · "scale (passer du test au volume)". Exemple · "audience (le groupe de personnes visé)".
- **Verbatims sourcés** conservés littéralement, jamais paraphrasés
- **ZERO em-dash** (le caractère tiret-cadratin). Substituer par parenthèses, virgule, point, deux-points, ou middle dot (·)
- **Iconographie unique canon sprint v2.79.2** · ✓ complet OK · ◐ partiel · ○ vide · ✗ absent · ⚠ critique. Légende canonique placée en pied de fiche output (cf format canonique). JAMAIS emoji couleur (🔥 🟢 🟡 🔴 ✅ ❌) sur output.
- **Ton institutionnel mesuré**, jamais sales-bro ("L'erreur que la plupart font", "Faux.")
- **Livrable concret en tête** · valeur d'abord, mécanique après
- **Diagramme cartographique ASCII** obligatoire dans la section "ce qui le rend possible"
- **✦ markers sobres** pour annotations qui décompressent un point dense
- **Density modérée** · séparateurs ━━━━━━ entre sections majeures de la fiche (cohérent sprint v2.79.2)
- **Fiche ~30 lignes max**, drill en fin
- **Section transversale Decomposition Visibility canon v2.79+ obligatoire** sur les chapitres `principe` · `atomicite` · `composition` · `matrices` · `production`. L'agent ship en synthèse les 4 niveaux matriciels appliqués au cas Stepprs encoded (NIVEAU 1 décomposition produit · NIVEAU 2 many-to-many · NIVEAU 3 stage filter · NIVEAU 4 pédagogie verbale). Cross-ref doctrine `docs/system/decomposition-visibility-doctrine.md` v2.79+.
- **4 niveaux matriciels appliqués cas Stepprs réel encoded** (workers-shifts + chronic-pain-45+ audiences, massage-insoles product, atomes encodés `brands/_EXAMPLE/`). Jamais projection hypothétique sur ces chapitres · sourcing depuis le workspace canon.
- **Cross-ref doctrine canon racine** `decomposition-visibility-doctrine.md` cité explicit en clôture de synthèse pour les chapitres consumer.

## Topic guides · ce que l'agent doit produire par topic

---

### 1. principe · ce qui reste stable, ce qui se génère

**Couche** · principe transverse (préalable aux 5 couches)

**Concept à transmettre** · PhantomOS sépare deux choses qu'on a tendance à mélanger. Le **territoire** d'une marque (qui elle est, à qui elle parle, ce qu'elle vend) reste stable dans le temps. Les **productions** (une publicité, un email, un script de vidéo) changent chaque semaine. Encoder le territoire une fois, générer les productions à la demande.

**Image vulgarisation** · l'encyclopédie d'une marque (structure stable, mise à jour rare) vs les articles de magazine produits chaque mois à partir de cette encyclopédie. Sans encyclopédie, chaque article repart de zéro.

**Concept concret Stepprs** · brand pédagogique du cas canonique PhantomOS (marque réelle stepprs.com avec certains financials et verbatims mockés pour la pédagogie) qui vend des semelles anti-douleur (massage insoles) à deux types de personnes principales · les travailleurs qui restent debout 8h+ par jour (infirmières, magasiniers, serveurs) et les personnes de 45 ans et + qui souffrent de douleurs chroniques (épine calcanéenne, talalgie). Semelle avec mousse à mémoire de forme, redistribution de pression et soutien de la voûte plantaire. Vendue en ligne directement (DTC, vente directe au consommateur, pas de pharmacie ni distributeur).

**Investissement vs ROI** · setup initial 1-2h en semaine 1 pour encoder le territoire. ROI immédiat dès semaine 2 · chaque nouvelle production (publicité, email, page produit) prend 5-15 min au lieu de 1-2h.

**Setup canon · phasing progressif par profondeur**

Le territoire ne se construit pas en bloc en semaine 1. PhantomOS canon impose un phasing en 4 phases avec gates light entre chaque · Phase 1 macro (scrape automatique + confirmation light) · Phase 2 drilling (drill pages produits + reviews) · Phase 3 audiences hiérarchique (cartographie parent/enfants) · Phase 4 enrichissement continu (non-bloquant, l'opérateur drop des insights à tout moment). Setup initial 1-2h en semaine 1 couvre Phase 1+2. Phase 3 atteinte sem 1-2. Phase 4 ouverte ad vitam. Tu n'es jamais "obligé d'avoir tout encodé pour commencer à produire".

**Files Stepprs à sourcer**
- `brands/_EXAMPLE/brand.json` (identité, positionnement, audiences principales)
- `brands/_EXAMPLE/status.json` (état du workspace, validation)
- `brands/_EXAMPLE/README.md` (note canon vs réel)

**Livrable concret en tête** · "Pour produire 1 nouvelle créa Stepprs, l'opérateur n'a pas besoin de re-explorer la composition produit, les audiences, les angles, les preuves. Tout est encodé. Il pioche dans le territoire, génère, valide. Temps de production divisé par 10."

**Diagramme à produire** · vue 2 couches orthogonales TERRITOIRE / PRODUCTION ·

```
TERRITOIRE (stable, encodé 1 fois)
─────────────────────────────────────────
Identité · positionnement · audiences ·
produit · mécanismes · douleurs · preuves
─────────────────────────────────────────
                ↓
        consommé par
                ↓
─────────────────────────────────────────
PRODUCTION (runtime, multiple)
publicité 1 · publicité 2 · email · page
produit · script vidéo · post X · brief
```

**Sections fiche** · LIVRABLE OBTENU · CE QUI LE REND POSSIBLE (diagramme) · CE QUE ÇA CHANGE POUR TOI · POUR ALLER PLUS LOIN.

**Pour aller plus loin** ·
- → Comprendre comment le savoir est encodé en atomes connectés    `/breakdown stepprs atomicite`
- → Voir une production concrète de bout en bout    `/breakdown stepprs production`
- → Continuer le parcours    `/breakdown stepprs atomicite`

---

### 2. atomicité · le savoir comme graphe d'atomes connectés (couche 1 modèle)

**Couche** · 1 modèle

**Concept à transmettre** · le savoir d'une marque n'est pas une grosse note prose. C'est un ensemble d'**atomes** (petites unités identifiables, chacune avec un identifiant unique). Une douleur identifiée chez un client = 1 atome. Une objection fréquente = 1 atome. Un angle de publicité = 1 atome. Tous reliés par références croisées (un atome cite les autres atomes qu'il utilise).

**Avantage clé** · quand tu corriges 1 atome, tous les atomes qui le citent en bénéficient automatiquement. Une CRM stocke du texte. PhantomOS encode du raisonnement connecté.

**Concept concret Stepprs** · ~50 atomes identifiés au total ·
- 13 douleurs documentées (pain points)
- 11 objections d'achat (objections)
- 6 frictions produit (frictions d'usage)
- 7 angles de publicité (angles)
- 4 mécanismes produit (mechanisms)
- 5 bénéfices (benefits)
- 7 sous-audiences (audience pockets)

**Exemple connecté** · la douleur identifiée "douleur talalgie au réveil" (1 atome) est citée par 3 autres atomes · 1 angle de pub hero, 1 objection sceptique ("est-ce que ça marche vraiment au réveil ?"), 1 mécanisme produit (redistribution de pression). Si tu corriges la formulation de la douleur, les 3 dépendants se mettent à jour automatiquement.

**Files Stepprs à sourcer**
- `brands/_EXAMPLE/audiences/{audience}/pain_points/PNT-*.json` (douleurs identifiées)
- `brands/_EXAMPLE/audiences/{audience}/objections/OBJ-*.json` (objections d'achat)
- `brands/_EXAMPLE/products/massage-insoles/frictions/FRC-*.json` (frictions produit)
- `brands/_EXAMPLE/angles/ANG-*.json` (angles de publicité)

**Livrable concret en tête** · cartographie du graphe Stepprs · 50 atomes, ~120 connexions identifiées. Tu modifies 1 atome (verbatim corrigé), 3 atomes en aval se mettent à jour sans intervention manuelle.

**Diagramme à produire** · graphe atomique simplifié ·

```
ATOMES STEPPRS · graphe partiel

[douleur talalgie réveil]
        │
        ├──→ [angle hero "premier pas matin"]
        │
        ├──→ [objection "ça marche au réveil ?"]
        │
        └──→ [mécanisme redistribution pression]
                        │
                        ├──→ [bénéfice "confort dès le premier pas"]
                        │
                        └──→ [angle hero] (boucle)

1 atome corrigé = 3+ atomes dépendants mis à jour
```

**Pour aller plus loin** ·
- → Voir comment ce graphe se répète à toutes les échelles    `/breakdown stepprs fractalite`
- → Comprendre comment combiner les atomes en livrable    `/breakdown stepprs composition`
- → Continuer le parcours    `/breakdown stepprs fractalite`

---

### 3. fractalité · le même pattern à toutes les échelles (couche 1 modèle)

**Couche** · 1 modèle

**Concept à transmettre** · une fois qu'on a compris UN pattern de raisonnement, on l'applique à tous les niveaux. C'est ça la fractalité (le même motif visible à différentes échelles, comme un flocon de neige ou un chou romanesco). Un seul mode de pensée à apprendre, applicable partout.

**Le pattern unique** · observer une tension, formuler une réponse, terminer par un appel. Quatre temps. Toujours les mêmes.

**Concept concret Stepprs** · ce pattern se retrouve à 4 échelles distinctes ·

1. **Échelle brand entière** · positionnement entre 2 forces opposées (Stepprs se positionne entre le médical sérieux et le confort grand public)
2. **Échelle audience** · une douleur partagée par un groupe (workers-shifts partagent la fatigue podale fin de journée)
3. **Échelle douleur identifiée** · chaîne surface → conséquence → racine profonde (douleur talalgie → impact sommeil → tension lombaire chronique)
4. **Échelle angle de publicité** · formule OTRB · Observation (verbatim client) + Tension (insight douleur) + Reframe (mécanisme produit positionné) + Bridge (appel à l'action + garantie)

**OTRB expliqué inline** · acronyme interne PhantomOS pour la structure canonique d'un angle paid (Observation, Tension, Reframe, Bridge). C'est l'équivalent d'un plan en 4 cases pour une publicité.

**Files Stepprs à sourcer**
- `brands/_EXAMPLE/brand.json` (positionnement entre 2 forces)
- `brands/_EXAMPLE/audiences/workers-shifts/profile.json` (douleur partagée par audience)
- `brands/_EXAMPLE/audiences/workers-shifts/pain_points/PNT-01.json` (chaîne douleur)
- `brands/_EXAMPLE/angles/ANG-01.json` (angle structure OTRB)

**Livrable concret en tête** · même grille mentale à 4 niveaux. L'opérateur apprend UNE fois à structurer un raisonnement en observation/tension/réponse/appel, il l'applique partout.

**Diagramme à produire** · 4 échelles, même structure ·

```
ÉCHELLE              OBSERVATION         TENSION              RÉPONSE                APPEL
─────────────        ─────────────       ─────────────        ─────────────          ────────────

brand               le marché propose   ni l'un ni l'autre   nous tenons             rejoindre la
                    soit médical soit   ne convient à        la place du milieu      voie médiane
                    confort             la majorité          rigoureux + accessible

audience            travailleurs 8h+    fatigue podale       audience partage la     ils achètent
                    debout              affecte sommeil      même douleur racine     une solution
                                        et lombaires                                  unique

douleur PNT-01      "talalgie au        dégrade qualité      cause profonde =        produit traite
                    réveil"             de vie globale       inflammation aponévrose la cause

angle ANG-01        verbatim Trustpilot insight douleur      mécanisme produit       CTA + garantie
                    sourcé              articulé             positionné              60 jours
```

**Pour aller plus loin** ·
- → Comprendre l'équation qui assemble les atomes en livrable    `/breakdown stepprs composition`
- → Voir comment cartographier 3 façons différentes    `/breakdown stepprs matrices`
- → Continuer le parcours    `/breakdown stepprs composition`

---

### 4. composition · l'équation qui assemble les atomes en livrables (couche 1 modèle)

**Couche** · 1 modèle

**Concept à transmettre** · un livrable (une publicité, un email, une page produit) n'est pas inventé à partir de zéro. Il est **calculé** par une équation simple ·

```
LIVRABLE = NOYAU × CONTEXTE × MODIFICATEURS
```

  ✦ Tu ne calcules pas l'équation à la main. Le système combine les
    ingrédients à chaque invocation. Tu choisis le contexte, le système
    compose.

**NOYAU** · ce qui ne change pas (matériau du produit, effet physique principal)
**CONTEXTE** · ce qui dépend du moment (audience visée, verbatim client précis)
**MODIFICATEURS** · ce qui varie selon le canal (saisonnalité, registre de ton, format publicité, canal media)

**Concept concret Stepprs** · pour produire un hook (la première ligne d'une publicité qui doit accrocher) ·

- **NOYAU** · semelle massage avec mousse à mémoire (matière) + redistribution de pression (effet physique)
- **CONTEXTE** · audience workers-shifts (visée) + verbatim Trustpilot "mes pieds ne me lâchent plus en fin de service" (preuve concrète)
- **MODIFICATEURS** · hiver (saisonnalité, gel = douleur amplifiée), ton vulnérable empathique (registre), format vidéo verticale 9:16 (canal Instagram Reels)

Le hook qui en sort n'est pas inventé. Il est composé. Reproducible. Si tu changes 1 modificateur (saison ou registre), tu obtiens une variante cohérente sans repenser le noyau.

**Files Stepprs à sourcer**
- `brands/_EXAMPLE/products/massage-insoles/spec.json` (composition + mécanismes + bénéfices = NOYAU)
- `brands/_EXAMPLE/audiences/workers-shifts/profile.json` (audience = CONTEXTE)
- `brands/_EXAMPLE/angles/ANG-01.json` (hook composé en sortie)

**Livrable concret en tête** · 1 noyau × 7 audiences possibles × 4 saisons × 3 registres = 84 variations cohérentes. Tu ne réinventes jamais. Tu paramètres.

**Diagramme à produire** · cartographique de la composition ·

```
COMPOSITION D'UN LIVRABLE STEPPRS

NOYAU (stable)         CONTEXTE (situation)     MODIFICATEURS (variation)
─────────────          ────────────────         ─────────────────────────

matière                audience                 saisonnalité
  mousse mémoire         workers-shifts           hiver / été / rentrée
                                                  
effet physique         verbatim sourcé          registre ton
  redistribution         "mes pieds ne me        vulnérable / fier /
  pression               lâchent plus..."        chirurgical
                                                  
bénéfice racine        douleur ciblée           format livrable
  confort dès            talalgie réveil          vidéo verticale /
  premier pas                                    statique / carousel
                                                  
                                                 canal média
                                                   Meta / TikTok / mail

         ↓                  ↓                            ↓
         └──────────────────┴────────────────────────────┘
                              │
                              ▼
                      LIVRABLE COMPOSÉ
                      (hook + body + CTA)
```

**Pour aller plus loin** ·
- → Voir comment cartographier les atomes en matrices    `/breakdown stepprs matrices`
- → Comprendre les règles qui cadrent le raisonnement    `/breakdown stepprs regles`
- → Continuer le parcours    `/breakdown stepprs matrices`

---

### 5. matrices · cartographier · prioriser · produire des variations (couche 1 modèle)

**Couche** · 1 modèle

**Concept à transmettre** · une **matrice** (un tableau à 2 dimensions) sert à trois usages différents dans PhantomOS. Pas un seul. Trois usages distincts à reconnaître pour savoir lequel utiliser.

**Les 3 usages canon de matrice** ·

1. **Matrice cartographie** · douleurs en lignes × audiences en colonnes. Sert à voir qui souffre de quoi. Révèle les **asymétries** (1 douleur frappe 5 audiences) et les **zones blanches** (audiences peu adressées). Diagnostic, pas action.

2. **Matrice scoring** · angles × audiences avec un score d'intérêt par case. Sert à **prioriser** les top-3 territoires à tester. Aide à décider où mettre le budget en premier.

3. **Matrice production** · 1 angle × 4 audiences × 3 formats × 2 saisons = 24 variations possibles. On en priorise top-5 à produire selon couverture maximale. Sert à **multiplier** les variations sans repartir de zéro.

  ✦ Tu ne remplis pas les cellules manuellement. Le système calcule
    les scores à partir des atomes encodés.

**Concept concret Stepprs** ·

- **Cartographie** · 13 douleurs × 7 audiences = 91 cases. Révèle que la douleur "talalgie réveil" frappe 4 audiences sur 7 (forte horizontalité, candidate hero). À l'inverse, "douleur métatarsienne sport" frappe 1 seule audience (vertical, candidat niche).
- **Scoring** · 7 angles × 7 audiences, chaque case scorée /10 sur frottement et conversion estimée. Top-3 territoires révélés · angle hero Michelle × workers-shifts (8.5/10), angle reassurance × chronic-pain-45 (7.8/10), angle confession × plantar-fasciitis (7.5/10).
- **Production** · pour l'angle hero Michelle, 4 audiences × 3 formats vidéo × 2 saisons = 24 variations possibles. Top-5 priorisées sur couverture EU et budget.

**Files Stepprs à sourcer**
- `brands/_EXAMPLE/learnings.json` (LRN-0002 pattern observé, exemple cartographie)
- score-matrix output si disponible (sinon produire un exemple inline)

**Livrable concret en tête** · trois cartes mentales différentes. L'opérateur sait toujours quelle matrice utiliser pour quel besoin (diagnostiquer, prioriser, multiplier).

**Diagramme à produire** · 3 matrices distinctes, même format, usages différents ·

```
3 USAGES DE MATRICE PHANTOMOS

CARTOGRAPHIE (diagnostic)        SCORING (priorisation)      PRODUCTION (variations)

       workers  chronic           workers  chronic              fmt1  fmt2  fmt3
talalgie  ✓      ✓                ANG-01    8.5     7.2         saison
métat     ✗      ✓                ANG-02    6.1     7.8           hiver  ✓    ✓    ·
arch      ✓      ✗                ANG-03    7.0     6.5           été    ✓    ·    ✓
sciat     ✗      ✓                ANG-04    5.5     6.0         

révèle asymétries                identifie top-3              multiplie en top-5
+ zones blanches                  territoires test             cohérents
```

**Pour aller plus loin** ·
- → Comprendre les règles qui cadrent le raisonnement    `/breakdown stepprs regles`
- → Voir comment les templates accélèrent la production    `/breakdown stepprs templates`
- → Continuer le parcours    `/breakdown stepprs regles`

---

### 6. règles · vocabulaires fermés + posture investigation (couche 2 règles)

**Couche** · 2 règles

**Concept à transmettre** · PhantomOS impose des **règles de raisonnement** qui ressemblent à des contraintes mais qui sont en fait des accélérateurs. Deux règles centrales à connaître.

**Règle 1 · vocabulaires fermés** · au lieu d'inventer un terme à chaque fois pour décrire la même chose, on choisit dans une liste prédéfinie (un registre). Exemple sur Stepprs · pour décrire le mécanisme produit, on ne dit pas "soutien dynamique adaptatif" (texte libre, ininterprétable pour l'agent suivant). On dit "arch support" + "pressure redistribution" (deux entrées du registre canon des mécanismes). N'importe quel autre skill PhantomOS peut alors raisonner sur ces mêmes mécanismes sans interprétation. La contrainte produit la reproducibilité.

**Règle 2 · posture investigation (5 sections)** · toute synthèse stratégique sort structurée en 5 sections explicites ·
- **Observé** · faits sourcés (verbatim Trustpilot, scrape PDP, review Amazon)
- **Déduit** · hypothèses avec niveau de confiance (forte / moyenne / faible / très faible)
- **Inconnu** · variables non observables, à creuser
- **Leviers** · skills ou actions pour lever les inconnues
- **Close ouvert** · UNE question macro pour que l'opérateur arbitre où creuser

Pas de prose libre. Pas d'affirmation sans étiquette d'origine.

  ✦ Tu n'as pas à mémoriser les vocabulaires fermés. Le système te
    propose ce qui s'applique selon le contexte, tu valides.

**Concept concret Stepprs** ·

- **Texte libre interdit** · "Stepprs a une semelle qui s'adapte dynamiquement" → un autre skill ne peut pas raisonner sur "s'adapte dynamiquement"
- **Vocabulaire canon** · "Stepprs combine arch-support + pressure-redistribution + shock-absorption" → 3 entrées du registre, manipulables par tous les skills

- **Synthèse libre interdite** · "L'audience workers-shifts est probablement sensible au prix car..."
- **Synthèse en 5 sections** · Observé (3 verbatims sourcés), Déduit (sensibilité prix, confiance moyenne, basée sur 3 verbatims), Inconnu (élasticité réelle prix), Leviers (test A/B prix sur audience contrôle), Close ouvert ("on creuse l'élasticité prix ou on teste d'abord l'angle hero ?")

**Files Stepprs à sourcer**
- `brands/_EXAMPLE/products/massage-insoles/spec.json` (mécanismes typés canon)
- `brands/_EXAMPLE/learnings.json` (synthèse en 5 sections, exemple)
- registres canon `resources/registries/*` (citer 2-3 noms en clair sans path)

**Livrable concret en tête** · 2 sorties comparées · une en mode "texte libre" (irréutilisable) vs une en mode "règles PhantomOS" (manipulable par tous les skills, reproducible cross-session).

**Diagramme à produire** · comparaison freestyle vs règles ·

```
RÈGLE 1 · vocabulaire fermé

FREESTYLE (interdit)              CANON (imposé)
────────────────────              ──────────────────────────────
"soutien dynamique adaptatif"     arch-support
                                  + pressure-redistribution
                                  + shock-absorption

→ ininterprétable                 → 3 entrées registre canon
→ chaque skill réinvente          → manipulable par tous skills

RÈGLE 2 · synthèse 5 sections

PROSE LIBRE (interdite)           STRUCTURE INVESTIGATION
─────────────────                 ─────────────────────────────
"L'audience est sensible          Observé · 3 verbatims sourcés
au prix car probablement..."       Déduit · sensibilité prix (moyenne)
                                   Inconnu · élasticité réelle
→ affirmation non sourcée          Leviers · test A/B prix
→ pas auditable                    Close · "où on creuse ?"
```

**Pour aller plus loin** ·
- → Voir comment les templates encodent ce qui marche    `/breakdown stepprs templates`
- → Comprendre comment les métriques tracent l'origine    `/breakdown stepprs metriques`
- → Continuer le parcours    `/breakdown stepprs templates`

---

### 7. templates · raccourcis combinaisons gagnantes (couche 3 templates)

**Couche** · 3 templates

**Concept à transmettre** · un **template** encode une combinaison qui marche, sous forme réutilisable. Au lieu de re-décider à chaque création de tous les paramètres (audience, angle, mécanique, format, ton), tu pars d'un template prouvé et tu adaptes 20% au contexte. Passe de 1 livrable/jour à 10 livrables/jour avec qualité constante.

**Image vulgarisation** · un template, c'est une recette. La recette du pain dit "farine + eau + sel + levure, repos 2h, cuisson 250°C". Tu adaptes la farine selon ce que tu as sous la main, mais tu ne réinventes pas la recette à chaque fournée.

**Concept concret Stepprs** · template "POV confession" (point de vue, confession personnelle face caméra) ·

- **Composition figée** ·
  - audience early-stage (personnes qui découvrent le problème)
  - angle reassurance (rassurer sur la légitimité de la douleur)
  - mécanique confession (un témoignage personnel, vulnérable)
  - format statique ou vidéo ASMR 9:16
  - ton vulnérable empathique

- **Ce qu'on adapte (20%)** · le verbatim utilisé, l'identité du témoin (workers-shifts vs chronic-pain-45), l'angle de prise vidéo, la saisonnalité dans le hook.

Au lieu de re-décider chaque case à chaque création, tu pars du template et tu adaptes ces 4 paramètres. 5 minutes de travail au lieu de 1 heure.

**Files Stepprs à sourcer**
- `brands/_EXAMPLE/angles/ANG-*.json` (pattern réutilisable identifié)
- templates canon dans `resources/templates/*` (citer 2-3 noms sans path)

**Livrable concret en tête** · 10 variantes du template POV confession produites en 1h, qualité constante, sourcées du même territoire. Sans template · 10h de travail créatif et qualité variable.

**Diagramme à produire** · anatomie d'un template ·

```
TEMPLATE STEPPRS · "POV confession"

PARAMÈTRES FIGÉS (80%)            PARAMÈTRES ADAPTÉS (20%)
──────────────────────            ──────────────────────────

audience type    early-stage      verbatim cité     "mes pieds..."
                                                    "je n'osais plus..."
                                                    "ma femme m'a dit..."

angle structure  reassurance      identité témoin   workers nurse
                                                    workers warehouse
                                                    chronic-pain plantar

mécanique        confession       angle prise vidéo face camera
                                                    over shoulder
                                                    POV pieds

format           statique 1:1     saisonnalité     hiver gel
                 ou ASMR 9:16     dans hook         rentrée scolaire
                                                    été chaleur

ton              vulnérable

→ on instancie le template avec 4 paramètres adaptés
→ 5 min par variante · qualité constante
→ 10 variantes/heure au lieu de 1
```

**Pour aller plus loin** ·
- → Comprendre comment les métriques tracent l'origine    `/breakdown stepprs metriques`
- → Voir les rituels qui font durer le système    `/breakdown stepprs rituels`
- → Continuer le parcours    `/breakdown stepprs metriques`

---

### 8. métriques · feedback par niveau + traçabilité source (couche 4 métriques)

**Couche** · 4 métriques

**Concept à transmettre** · chaque information dans PhantomOS porte son **étiquette d'origine**. Tu sais toujours d'où vient une affirmation. Cinq étiquettes possibles ·

- **Observé** · capté directement (Trustpilot, Facebook followers, year_founded, marchés EU sourced live)
- **Déclaré** · saisi par l'opérateur (revenu mensuel mock, LTV, marge brute)
- **Déduit** · raisonné par l'agent (driver primaire, positionnement)
- **Structuré** · règle métier (les 4 mécanismes typés canon, formula OTRB)
- **Importé** · enrichi depuis source externe spy tool (TrendTrack ads winners, Trustpilot bulk, Foreplay creative library, etc.)

  ✦ Tu ne taggues pas chaque info manuellement. Le système l'auto-tag
    depuis les signaux sémantiques. Tu vois `observé/déduit/déclaré`,
    jamais les nombres.

**Enrichissement multi-source · Market Intelligence Layer**

Le territoire ne grandit pas seulement via scrape du site web propre. PhantomOS canonise un pattern de NEW skills `{source}-enrich-brand` qui enrichissent le territoire depuis sources externes spy tools (TrendTrack pour ads competitive, Foreplay pour creative library, Atria, Meta Ad Library, BigSpy, etc.). Chaque info importée porte l'étiquette `Importé` + meta tag de la source d'origine (e.g. `trendtrack`). Sur Stepprs · 8 patterns capturés via TrendTrack live (narrative diversity, geo distribution, spend concentration, etc.) enrichissent le territoire au-delà du scrape PDP.

Chaque atome porte aussi son **état de validation** · proposée, validée par opérateur, testée en réel, scalée en volume, fatiguée (n'est plus performante).

**Concept concret Stepprs** ·

- **Trustpilot 3.4/5 · 1247 reviews** · note observée (scrape direct site Trustpilot, date d'observation enregistrée)
- **Revenu mensuel 47k€** · valeur déclarée par l'opérateur (jamais déduit)
- **Driver d'achat primaire = soulagement immédiat** · déduit (niveau confiance moyen, basé sur 3 verbatims qui le mentionnent explicitement)
- **Score d'opportunité angle hero × workers-shifts = 8.5/10** · structuré (calculé à partir du score frottement × score conversion estimée)

Au niveau output, une matrice de scoring quantifie. Pas d'intuition seule. La traçabilité est garantie cross-session.

**Files Stepprs à sourcer**
- `brands/_EXAMPLE/brand.json` (étiquettes d'origine sur chaque champ)
- `brands/_EXAMPLE/learnings.json` (état de validation sur chaque atome)
- score-matrix output si disponible

**Livrable concret en tête** · tu reprends Stepprs 6 mois plus tard. Chaque atome te dit comment il est arrivé là (observé, déclaré, déduit). Tu sais ce qui a été testé en réel vs ce qui reste hypothèse. Zéro perte d'information.

**Diagramme à produire** · arbre de traçabilité ·

```
ÉTIQUETTES D'ORIGINE STEPPRS

observée                  déclarée                déduite                structurée
─────────                 ─────────               ─────────              ─────────────
Trustpilot 3.4/5          revenu 47k€/mois        driver primaire =      score opportunité
1247 reviews              objectif EU expansion   "soulagement"          angle × audience
scrape PDP                contraintes budget      (confiance moyenne)    8.5/10

  ↓                         ↓                       ↓                       ↓

source liée               opérateur statement     confidence chain        algorithme
+ date observation        + date déclaration      + 3 verbatims source    + inputs sourcés

ÉTAT DE VALIDATION (par atome)

proposée  →  validée  →  testée  →  scalée  →  fatiguée
(agent)    (opérateur)   (réel)     (volume)    (n'est plus performante)
```

**Pour aller plus loin** ·
- → Voir les rituels qui font durer le système    `/breakdown stepprs rituels`
- → Voir une production concrète bout en bout    `/breakdown stepprs production`
- → Continuer le parcours    `/breakdown stepprs rituels`

---

### 9. rituels · cadence opérationnelle + auto-correction (couche 5 rituels)

**Couche** · 5 rituels

**Concept à transmettre** · un système ne tient que s'il est **exécuté à fréquence**. Sans rituels (moments réguliers où on revisite le système), les règles se relâchent, les templates deviennent obsolètes, les métriques ne sont plus lues. Le système se dégrade silencieusement.

**4 rituels canon PhantomOS** ·

1. **Brief journalier** · en début de session, l'agent fait l'état de la brand active et propose les prochaines actions. 30 secondes. Empêche les sessions sans direction.

2. **Fin de session** · capture des décisions prises, des frictions observées, des corrections appliquées. Persiste dans le système. Empêche la perte d'information cross-session.

3. **Pré-ship** · audit de cohérence avant production réelle (avant de lancer une publicité payée, avant d'envoyer un email à la base). Vérifie que les atomes utilisés sont validés, que les verbatims sont sourcés, que les angles sont scorés. Empêche les ratés évitables.

4. **Audit hebdo** · scan complet du workspace · stale (atomes non touchés depuis 30+ jours), parasites (atomes non référencés), drift (atomes qui contredisent les nouveaux), duplicates (atomes presque identiques). Maintient l'hygiène long terme.

**Concept concret Stepprs** ·

- Lundi matin · brief journalier. État Stepprs (3 angles validés, 2 en test, 1 fatigué). Proposition · rotation de l'angle fatigué avec une variante template POV confession.
- Vendredi soir · fin de session. Capture · "l'angle hero Michelle performe mieux sur workers que sur chronic-pain. Verbatim x à corriger."
- Avant un test live · pré-ship. Verbatim sourcé ? Score territoire ≥ 7/10 ? Audience cartographiée ?
- Dimanche soir · audit hebdo. 3 atomes stale (>30j), 1 duplicate à fusionner, 0 drift.

**Files Stepprs à sourcer** (à invoquer dans la fiche live)
- rituel brief-day (skill existant)
- rituel learn-from-session (skill existant)
- rituel validate-resources (skill existant)
- rituel hygiene-audit (skill existant)

**Livrable concret en tête** · 4 rituels, total ~30 min/semaine. ROI · le système reste à jour, prêt à produire, sans dérive silencieuse. Sans rituels · 3 mois plus tard, ton workspace est devenu une CRM obsolète.

**Diagramme à produire** · 4 rituels, cadence, output ·

```
CADENCE OPÉRATIONNELLE PHANTOMOS

RITUEL             FRÉQUENCE        DURÉE       OUTPUT
─────────────      ─────────────    ─────       ─────────────────────────

brief journalier   début session    30 sec      état brand · prochaines
                                                 actions proposées

fin de session     fin session      2 min       capture décisions ·
                                                 frictions · corrections
                                                 persistées

pré-ship           avant production 5 min       audit cohérence ·
                                                 verbatim sourcé ·
                                                 angle scoré ≥ 7/10

audit hebdo        1×/semaine       10 min      scan stale · parasites
                                                 · drift · duplicates

TOTAL              hebdomadaire    ~30 min/sem  système maintenu propre

SANS RITUELS                       AVEC RITUELS
─────────────                       ─────────────
règles relâchées                    règles respectées
templates obsolètes                 templates rafraîchis
métriques non lues                  métriques activées
drift silencieux                    drift détecté + corrigé
```

**Pour aller plus loin** ·
- → Voir la démo complète d'une production en 5 min    `/breakdown stepprs production`
- → Revoir l'atomicité depuis l'angle système    `/breakdown stepprs atomicite`
- → Continuer le parcours    `/breakdown stepprs production`

---

### 10. production · brief copy en 5 minutes appliquant les 5 couches (démo)

**Couche** · démo complète (combine les 5 couches)

**Concept à transmettre** · démonstration concrète. Un brief copy hero pour Stepprs sur la douleur talalgie (plantar fasciitis) produit en 5 minutes en activant simultanément les 5 couches du système. Chaque ligne du brief vient d'une couche identifiable. Arbre de provenance visible.

**Concept concret Stepprs** · brief copy hero workers-shifts × angle Michelle × douleur talalgie ·

```
BRIEF COPY HERO · STEPPRS x WORKERS-SHIFTS x ANG-01 MICHELLE

HOOK
"Premier pas du matin · ces 30 premières secondes
qui décident de ta journée."

ARGUMENT
"Mousse à mémoire + redistribution de pression sur l'arche.
Pour que tes pieds ne te lâchent plus dès le réveil."

PREUVE
"Michelle, infirmière 12h shifts · 'Avant, je me levais
en m'agrippant au mur. Maintenant je marche normal.'
(Trustpilot · 4.5/5 · vérifié)"

CTA
"Essaie 60 jours. Si tes pieds ne changent pas, on rembourse.
Stepprs.com/start"
```

**Décomposition par couche** ·

- **HOOK** vient de **couche 1 (modèle composition)** + **couche 2 (règle audience cartographiée)**. Le NOYAU "premier pas du matin" est composé de la douleur talalgie réveil (atome PNT-01) × audience workers-shifts (audience cartographiée). La règle "vocabulaire de l'audience" impose "30 premières secondes" et "ta journée" (registre opérationnel travailleur, pas registre clinique).

- **ARGUMENT** vient de **couche 1 (modèle atomicité)**. Les 2 mécanismes cités ("mousse à mémoire" + "redistribution de pression sur l'arche") sont 2 atomes du graphe spec produit. Pas inventés, sourcés.

- **PREUVE** vient de **couche 4 (métrique traçabilité)**. Le verbatim Michelle est observé (scrape Trustpilot, vérifié). La note 4.5/5 est observée. Étiquette d'origine garantie.

- **CTA** vient de **couche 3 (template offer canon)**. "60 jours essai + remboursement" est un template canon Stepprs réutilisable sur tous les angles. Pas re-décidé à chaque fois.

**Files Stepprs à sourcer**
- `brands/_EXAMPLE/products/massage-insoles/spec.json` (mécanismes)
- `brands/_EXAMPLE/audiences/workers-shifts/profile.json` (audience)
- `brands/_EXAMPLE/angles/ANG-01.json` (angle structure)
- `brands/_EXAMPLE/products/massage-insoles/offers.json` (template offer)
- verbatim Michelle sourcé Trustpilot (sourcing observé)

**Livrable concret en tête** · 4 lignes de brief, 5 couches activées, arbre de provenance complet. Reproducible. Si tu remplaces workers-shifts par chronic-pain-45 dans le contexte, tu obtiens une variante cohérente automatiquement.

**Diagramme à produire** · arbre de provenance du brief ·

```
BRIEF COPY · ARBRE DE PROVENANCE

HOOK
├── NOYAU       ← couche 1 (atome PNT-01 talalgie)
├── CONTEXTE    ← couche 1 (audience workers-shifts)
└── REGISTRE    ← couche 2 (règle vocabulaire opérationnel)

ARGUMENT
├── mécanisme 1 ← couche 1 (atome mousse à mémoire)
└── mécanisme 2 ← couche 1 (atome redistribution pression)

PREUVE
├── verbatim    ← couche 4 (observé Trustpilot)
└── note        ← couche 4 (observé Trustpilot 4.5/5)

CTA
└── garantie    ← couche 3 (template offer canon 60j)

PRODUCTION COMPLÈTE = 5 min · 5 couches activées
arbre de provenance visible · reproducible
```

**Sans le système** · 1 brief = 1-2h de travail créatif, qualité variable, sourcing absent, non-reproducible.
**Avec le système** · 1 brief = 5 min, qualité constante, sourcing garanti, reproducible cross-session.

**Pour aller plus loin** ·
- → Comprendre comment l'intelligence contextuelle utilise les 5 couches    `/breakdown stepprs intelligence`
- → Comprendre comment le système s'auto-améliore    `/breakdown stepprs apprentissage`
- → Refaire le parcours complet    `/breakdown stepprs`

---

### 11. intelligence · raisonnement contextuel grâce aux variables paramétrées

**Dimension** · transverse · scelle le parcours (la promesse fondatrice que les 5 couches servent)

**Concept à transmettre** · Les 5 couches qu'on vient de voir ne sont pas leur propre fin. Elles existent pour rendre une seule chose possible · un système qui raisonne contextuellement, plutôt qu'un système qui applique des règles mécaniques aveugles. C'est la promesse fondatrice de PhantomOS (doctrine master · Contextual Intelligence).

**Différence concrète à montrer** ·

Système rigide (CRM enrichi, automation Zapier, scripts Make)
- Reçoit · "audience workers-shifts, saison hiver"
- Produit · le brief T-001 stocké en mémoire pour ce cas exact
- Adapte · zéro. Si le cas est nouveau, retombe sur défaut générique.

Système intelligent (PhantomOS)
- Reçoit · "audience workers-shifts, saison hiver"
- Raisonne · workers-shifts → douleur 10h+ shifts (couche 1) + saison hiver → urgence ressentie (couche 1) + modifieur saison → ton plus empathique (couche 2) + verbatim Trustpilot infirmière hiver (couche 4)
- Produit · un brief unique adapté à CE moment, CETTE audience, CETTE saison.

**L'équation revue sous l'angle intelligence**
- LIVRABLE = NOYAU × CONTEXTE × MODIFIEURS
- NOYAU stable (savoir territoire). CONTEXTE et MODIFIEURS paramétrés varient à chaque invocation. C'est cette variabilité paramétrée qui produit l'intelligence · le système adapte sans qu'on le reprogramme.

**Diagramme à proposer · les 5 couches ensemble servent l'intelligence**
- Couche 1 modèle    · fournit les atomes et leurs relations
- Couche 2 règles    · cadre le raisonnement (vocabulaires, posture investigation)
- Couche 3 templates · propose des combinaisons éprouvées
- Couche 4 métriques · fournit la traçabilité de chaque variable
- Couche 5 rituels   · maintient le système à jour pour rester pertinent

**Lecture opérateur** · Tu ne configures pas N templates pour N cas (qui te demanderait d'anticiper toutes les combinaisons, impossible). Tu encodes le territoire une fois, et le système raisonne à chaque invocation. Nouvelle audience ? Le système l'absorbe et produit. Nouvelle saison ? Pareil. Tu fournis les variables, le système raisonne.

**Files Stepprs à sourcer**
- `brands/_EXAMPLE/brand.json` (audiences cartographiées, modifieurs structurels)
- `brands/_EXAMPLE/products/massage-insoles/spec.json` (noyau composition)
- `brands/_EXAMPLE/angles/ANG-01.json` (exemple application équation)

**Drill-down suggéré**
- /breakdown stepprs apprentissage (comment le système s'auto-améliore)
- /breakdown stepprs principe (revenir au principe fondateur)
- /breakdown stepprs (refaire le parcours complet)

---

### 12. apprentissage · cycle de promotion entre couches · compound effect

**Dimension** · transverse · scelle le parcours (comment le système devient meilleur au fil du temps)

**Concept à transmettre** · Un système opérationnel statique se dégrade. Un système qui apprend s'enrichit. PhantomOS encode un cycle de promotion entre les 5 couches qui fait grandir le territoire à chaque cycle de production. C'est le compound effect canon.

**Cycle canon à 4 étapes (produce → test → learn → promote)**

1. PRODUCE · l'agent produit un livrable en combinant les 5 couches. Exemple Stepprs · 5 publicités avec variations de hook.
2. TEST · le livrable est lancé en réel. Exemple Stepprs · 5 publicités testées sur Meta pendant 7 jours.
3. LEARN · les métriques (couche 4) capturent ce qui marche. Exemple Stepprs · publicité #3 (hook "5h du matin") explose à 8x le CTR moyen.
4. PROMOTE · ce qui marche remonte vers une couche supérieure. Exemple Stepprs · le hook "5h du matin" est promu de production éphémère vers template canon (couche 3).

**Les 4 chemins de promotion canon**

- Production → Templates (couche 3) · un angle qui scale 3 fois devient template canonique. Exemple Stepprs · ANG-01 hero Michelle promu après 27 marchés EU.
- Règle → Template (couche 2 → 3) · une heuristique appliquée systématiquement avec succès devient template. Exemple · "verbatim Trustpilot toujours en proof" devient template hook canon.
- Métrique → Rituel (couche 4 → 5) · une métrique qui converge vers un seuil stable mérite son rituel de suivi. Exemple · "CTR cible 1.8% sur ad statique" devient rituel hebdomadaire.
- Rituel → Règle (couche 5 → 2) · un rituel exécuté assez de fois pour devenir automatique se cristallise en règle canon. Exemple · "auditer la cohérence territoire avant ship" devient règle hard.

**Diagramme à proposer** ·

```
           PRODUCTION éphémère
                  │
                  │ promote si scale ≥3 fois
                  ▼
              TEMPLATES (couche 3)
                  │
                  │ promote si appliqué systématique
                  ▼
              RÈGLES (couche 2)

           MÉTRIQUE convergente
                  │
                  │ promote si seuil stable
                  ▼
              RITUEL (couche 5)
                  │
                  │ promote si automatique
                  ▼
              RÈGLE (couche 2)
```

**Lecture opérateur** · Plus la marque vit dans PhantomOS, plus elle s'affine. Au bout d'un an, ton territoire contient les angles qui ont prouvé leur ROI, les objections qui reviennent vraiment, le vocabulaire qui résonne sur ta cible spécifique. Chaque nouvelle production démarre depuis un substrat plus riche. Le compound effect s'accumule.

**Files Stepprs à sourcer**
- `brands/_EXAMPLE/learnings.json` (8 patterns LRN-0001 à LRN-0008 capturés via TrendTrack live)
- `brands/_EXAMPLE/angles/ANG-01.json` (hero promu après scaling)
- `brands/_EXAMPLE/status.json` (validation_status sur entités · validated → tested → scaled)

**Drill-down suggéré**
- /breakdown stepprs intelligence (comment le système raisonne contextuellement)
- /breakdown stepprs principe (revenir au principe fondateur)
- /breakdown stepprs (refaire le parcours complet)

---

### 13. extension · comment PhantomOS absorbe ce qui n'est pas shipped

**Dimension** · transverse · scelle la promesse extensibilité (PhantomOS grandit avec ton besoin, pas l'inverse)

**Concept à transmettre** · PhantomOS arrive avec des concepts canon (audiences, produits, angles, etc.) qui couvrent les marques DTC standard. Mais ton besoin sortira parfois du cadre shipped. Le système est conçu pour absorber l'inconnu via une méthode canonique (doctrine `scope-extension-doctrine.md` v2.65 + orchestrateur `scaffold-extension` v1.1.0+ 9 phases).

**Les 4 chemins d'extension canon · cas concrets Stepprs**

Nouveau type d'objet (NEW entity)
  Stepprs lance une gamme chaussures. Ce n'est pas une semelle, c'est un nouveau type de produit. Le système te propose le scaffold avec les mêmes 4 arbres (composition, mécanismes, bénéfices, angles). Tu n'as pas à inventer la structure.

Nouveau domaine (NEW domain)
  Stepprs lance un service de podologie en cabinet. Sortie du cadre DTC ecom pur. Le système identifie · "ce n'est pas un produit physique, c'est un service." Propose la structure adaptée. Tu valides ou ajustes.

Nouvelle source de données (NEW source)
  Stepprs veut tracker les avis Reddit r/nursing. Le système propose un nouveau skill `mine-voc-reddit` basé sur le pattern canon mining VoC existant. Réutilisable, pas freelance.

Nouvelle capacité (NEW skill)
  Stepprs veut comparer la performance Meta Ads entre Allemagne et Roumanie. Le système identifie · "c'est un audit perf scopé par géo." Propose extension du skill existing audit-meta-account avec un mode --compare-geo. Pas de nouveau skill freelance qui duplique.

**Ce que l'opérateur fait, ce qu'il ne fait pas**

Tu décris ton besoin en langage naturel · "j'aimerais ajouter une gamme chaussures", "je veux suivre les avis Reddit", "j'ai besoin de comparer les pays". Le système décompose, propose la structure, te montre les implications, tu valides ou ajustes.

Tu ne conçois pas la structure technique. Tu ne choisis pas dans des listes fermées. Tu ne nommes pas les champs. Le système le fait pour toi à partir de la méthode canonique d'extension.

  ✦ Le canon protège ton territoire de la dérive. Tu ne peux pas créer une entité ou un skill qui dupliquerait un existing sans que le système te le flague. La cohérence est garantie par construction.

**Ce que ça change pour toi**

Tu n'es jamais coincé. Le système n'est pas un cadre rigide où tout ce qui n'est pas shipped est exclu. C'est un cadre extensible où le nouveau passe par le même filtre canonique que l'existing. PhantomOS grandit avec ton besoin, pas l'inverse.

**Files Stepprs à sourcer (pour exemples vivants si extensions encodées)**
- Aucune extension Stepprs encodée actuellement (Stepprs vit dans le canon shipped). Les exemples sont des PROJECTIONS hypothétiques pour illustrer les 4 chemins.

**Drill-down suggéré**
- /breakdown stepprs intelligence (comment le système raisonne sur les extensions)
- /breakdown stepprs apprentissage (comment le système apprend des extensions)
- /breakdown stepprs principe (revenir au principe fondateur)

---

## Section transversale · Decomposition Visibility canon v2.79+

Le cas Stepprs encodé dans le workspace `brands/_EXAMPLE/` illustre les 4 niveaux matriciels canon `decomposition-visibility-discipline` qui s'appliquent à tout brand opérateur-facing. Cette section synthétise comment les chapitres précédents (principe · atomicité · composition · matrices · production) montent ensemble en 1 pattern reproductible. À garder en filigrane pendant le drill par topic, et à reverbaliser quand l'opérateur passe de Stepprs au scaffold de sa propre marque.

### NIVEAU 1 · Décomposition produit Stepprs (massage insoles)

3 strates orthogonales · ce que le produit EST · ce qu'il FAIT · ce que ça CHANGE.

```
┌──────────────────────────────────────────────────────────────────────┐
│ NIVEAU 1 · Décomposition produit (canon strata) · Stepprs            │
├──────────────────────────────────────────────────────────────────────┤
│ SPECS · ce que le produit EST                                        │
│   semelle massage 3 couches · mousse à mémoire de forme ·            │
│   soutien voûte plantaire · épaisseur 5mm · format universel         │
├──────────────────────────────────────────────────────────────────────┤
│ MÉCANISMES · ce que le produit FAIT                                  │
│   mousse mémoire épouse la voûte · redistribution de pression        │
│   sur les 3 zones d'appui · absorption de choc talon · soutien       │
│   dynamique sur cycle de marche                                      │
├──────────────────────────────────────────────────────────────────────┤
│ BÉNÉFICES 3 couches · ce que ça CHANGE                               │
│   functional · fin de douleur talon réveil · pieds tiennent 8h+      │
│   emotional · sérénité fin de shift · plus de peur du lendemain      │
│   identity · pro qui prend soin de son corps · parent prévoyant      │
└──────────────────────────────────────────────────────────────────────┘
```

Le stack functional · emotional · identity vit dans la doctrine `pain-benefit-chain` canon. Skip 1 couche (functional seule) · différenciation premium impossible · positionnement single-layer.

### NIVEAU 2 · Many-to-many Stepprs (pain × audience)

1 produit · N pains · M audiences. Matrice force pensée systémique correcte. Évite la trap 1:1 (1 produit · 1 pain · 1 audience) qui plafonne le scaling.

```
┌────────────────────────────┬─────────────────┬───────────────────┐
│                            │ workers-shifts  │ chronic-pain-45+  │
├────────────────────────────┼─────────────────┼───────────────────┤
│ talalgie réveil            │     ✓✓ P        │      ✓✓ P         │
│ fatigue podale fin de jour │     ✓✓ P        │       ✓ S         │
│ douleur métatarsienne      │      ✓ S        │      ✓✓ P         │
│ tension lombaire chronique │      ✓ S        │       ✓ S         │
│ inflammation aponévrose    │       ·         │      ✓✓ P         │
├────────────────────────────┼─────────────────┼───────────────────┤
│ Espace blanc paid          │   emerging      │    weak           │
└────────────────────────────┴─────────────────┴───────────────────┘

Légende · ✓✓ P = PRIMARY (pain dominant) · ✓ S = SECONDARY · · = NONE
```

Lecture · talalgie réveil est PRIMARY sur les 2 audiences encodées (candidate hero horizontal). Inflammation aponévrose est PRIMARY seulement sur chronic-pain-45+ (candidate niche vertical). La même semelle sert 2 contextes business via 2 hooks calibrés.

### NIVEAU 3 · Positionnement filtre par stage business Stepprs

Audience produit-fit (qui le produit peut servir) ≠ audience ciblage créa (qui la communication mène en priorité au stage business courant). Distinction stratégique explicit.

```
┌──────────┬───────────────┬──────────────────┬──────────────────────────┐
│ Stage    │ ARR target    │ Audience focus   │ Angle dominant Stepprs   │
├──────────┼───────────────┼──────────────────┼──────────────────────────┤
│ early    │ 0 → 500k      │ 1 audience       │ angle hero "premier pas  │
│          │               │ workers-shifts   │ matin" × pain talalgie   │
├──────────┼───────────────┼──────────────────┼──────────────────────────┤
│ growth   │ 500k → 3M     │ 2 audiences      │ hero workers + variante  │
│          │               │ workers + chronic│ reassurance chronic-pain │
├──────────┼───────────────┼──────────────────┼──────────────────────────┤
│ scale    │ 3M+           │ 3-4 audiences    │ matrice complète angles  │
│          │               │ + sous-pockets   │ × audiences × saisons    │
└──────────┴───────────────┴──────────────────┴──────────────────────────┘
```

Audience produit-fit Stepprs · large (workers-shifts + chronic-pain-45+ + 5 sous-pockets cartographiées). Audience ciblage créa au stade early · étroite (workers-shifts seule, learning efficient). Confondre les deux · single-audience permanente même à 3M+ ARR · saturation auction garantie.

### NIVEAU 4 · Méthode pédagogique verbale

Verbaliser le HOW à l'opérateur AVANT et APRÈS la décomposition. Verbatim canon ·

- *"J'ai décomposé le produit Stepprs en 4 niveaux logiques · ce qu'il EST (semelle 3 couches mousse mémoire), ce qu'il FAIT (redistribution pression + absorption choc), ce que ça CHANGE (functional fin de douleur · emotional sérénité · identity pro qui prend soin), à QUI ça répond (matrice many-to-many pain × audience)."*
- *"Puis filtre POSITIONNEMENT par stage business · early stage Stepprs focus workers-shifts, growth ajoute chronic-pain-45+, scale ouvre la matrice complète angles × audiences × saisons."*
- *"L'audience produit-fit Stepprs (qui la semelle peut servir, surface large) n'est PAS l'audience ciblage créa (qui la communication mène en priorité au stade business courant, surface étroite stage-aware)."*

Pattern reproductible · l'opérateur encode SA marque en réappliquant les 4 niveaux. Même grammaire, brand différente, output canon. C'est la promesse PhantomOS · grammaire transférable, pas template figé.

Cross-ref doctrine `docs/system/decomposition-visibility-doctrine.md` v2.79+ canon racine cross-skills opérateur-facing.

## Anti-patterns à éviter dans toute fiche

- Dump prose continue sans diagramme
- Acronymes doctrine non-traduits exposés (SED, CMR, SAD, SED-X, IP, VOC, etc.)
- Field paths JSON exposés (`audiences/workers-shifts/profile.json#field`)
- Ton sales-bro ou tabloid ("L'erreur que la plupart font", "Faux.", "L'astuce que personne ne te dit")
- Em-dash (le caractère tiret-cadratin) anywhere
- Fiche au-delà de 35 lignes
- Vocabulaire technique sans explication inline première occurrence
- Présupposé de connaissance marketing (audience, DTC, scale, angle) sans expliquer en langue courante
- Vitrine pédagogique prose-only sans matrices appliquées au cas Stepprs (canon DVD v2.79+ trahi)
- Chapitre composition ou matrices sans rendu matrice canon (NIVEAU 1, 2, 3 ASCII obligatoires sur synthesis)
- Skip pédagogie verbale méthode (verbatim *"j'ai décomposé en 4 niveaux logiques"* obligatoire sur synthesis)

## Cross-refs canon

**Doctrine mère** ·
- `docs/system/operational-system-doctrine.md` (NEW v2.71.0 · les 5 couches d'un système opérationnel comme grammaire pédagogique mère)
- `docs/system/decomposition-visibility-doctrine.md` (v2.79+ canon racine cross-skills opérateur-facing · 4 niveaux matriciels obligatoires sur synthèse stratégique · doctrine sœur Investigation Posture + Canonical Matrix Reasoning + Skill Routing Discipline)

**Doctrines couche 1 (modèle)** ·
- `docs/system/compositional-cartography.md` (équation NOYAU × CONTEXTE × MODIFICATEURS)
- `docs/doctrine/audiences-cartography-doctrine.md` (cartographie hiérarchique)
- `docs/doctrine/pain-benefit-chain-doctrine.md` (chaîne douleur surface → racine)
- `docs/system/territory-doctrine.md` (territoire stable vs production volatile)

**Doctrines couche 2 (règles)** ·
- `docs/system/investigation-posture.md` (5 sections obligatoires + vocabulaires fermés)
- `docs/system/schema-encoding-doctrine.md` (encoding rigoureux + sourcing tags)

**Doctrines couche 4 (métriques)** ·
- `docs/system/confidence-propagation.md` (cascade confidence cross-skill)
- `docs/system/provenance-trust-discipline-scope.md` (provenance des assertions)

**Doctrines couche 5 (rituels)** ·
- `docs/system/progressive-cartography-doctrine.md` (cadence de mise à jour)
- `docs/system/contract-daily.md` (rituels post-setup daily-use)

**Brand pédagogique source** ·
- `brands/_EXAMPLE/` (foot care DTC Stepprs · brand pédagogique cas canonique · cf `_EXAMPLE/README.md` pour contexte complet · canon vs réel documenté dans README)

**Slash commands frères** ·
- `/tour` (onboarding complet PhantomOS)
- `/skills` (menu navigable des skills)
- `/phantom` (state cockpit brand active · canon v2.77 + v2.79.1 · 4 niveaux matriciels brand opérateur-facing)
- `/bird` (vue d'oiseau projet · canon v2.79.1 · pattern matriciel synthèse)
- `/scope` (cartographie paramètres décidables · canon v2.79.1 · pattern matriciel scoping)

**Sister skills v2.78.2+/v2.79+ consumers Decomposition Visibility canon** ·
- `snapshot-brand` (Phase output Movement 3-4 · matrices 4 niveaux brand encoded)
- `build-atlas-complete` (Phase output pipeline canonical · atlas matriciel multi-niveau)
- `profile-audience` (output enrichi matrice audience × pain × angle × stage)
- `define-specs` (output 3 niveaux specs · mécanismes · bénéfices matrice obligatoire)

**Discovery cross-link** ·
- `_EXAMPLE/stepprs/README.md` pointe vers `/breakdown stepprs`
- `tour.md` Milestone 6 mentionne `/breakdown stepprs` dans le trio commands
