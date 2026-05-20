# La chaîne pain · benefit · fonctionnel → émotionnel → identitaire

> *"Les amateurs vendent ce que le produit FAIT. Les pros vendent ce que le client DEVIENT."* · principe canon Direct Response (Halbert, Sugarman, Kennedy)

---

## L'enjeu

Tu écris une fiche produit. Tu listes 10 features. Tu balances 3 bénéfices au pluriel · *"hydrate, nourrit, protège"*. La fiche convertit à 1.2%. Tu blâmes la photo, le prix, le delivery.

Le problème · ton copy s'arrête à ce que le produit **fait**. Il ne dit jamais qui le client **devient**.

Un client n'achète pas une crème hydratante. Il achète *"je suis quelqu'un qui prend soin de moi."* Il n'achète pas une montre de sport. Il achète *"je suis un athlète."* Il n'achète pas un tracker de sommeil. Il achète *"je suis quelqu'un qui contrôle sa santé."*

La chaîne canon · **fonctionnel → émotionnel → identitaire**. Trois layers de bénéfice, séquencés sans saut. Skip un layer = ton claim sonne magique et non-crédible. Vendre seulement le fonctionnel = ton copy reste plat et interchangeable avec un concurrent.

Gary Halbert dans *The Boron Letters* (1984) le résume sans détour · *"People do not buy products. They buy results. And not just any results · the emotional and identity-level outcomes those products promise."* 40 ans plus tard, c'est encore la frontière entre copywriter amateur et copywriter pro.

**Ontologie pure v2.64 · pain_points sont sub-folder OWNED dans audiences/{slug}/pain_points/.** Un pain_point est l'expression subjective d'une audience donnée · même pain canonique ("sommeil profond perturbé") peut diverger entre stress-pro et post-partum (severity, chain functional/emotional/identity, verbatim_quotes registre, trigger). Le storage OWNED sub-audience rend cette propriété sémantique explicite. Les pain_points ne sont PAS des sub-fields dans `audience.profile.json` ni des entités top-level brand-wide (v2.63 deprecated). Ils vivent comme entités OWNED dans le sub-folder · `brands/{brand}/audiences/{slug}/pain_points/PNT-NN.json`. Cross-refs canonical · pain_points shared entre plusieurs audiences sont stockés primary owner avec `also_affects_audiences[]` array (slugs autres audiences impactées). Évite duplication, expose visibility cross-audience explicite. Permet la chain pain → benefit canonical cross-skills · `mine-voc` capture verbatim sources, `profile-audience` structure sub-folder OWNED, `produce-paid-angles` consume PNT-NN pour générer angles dérivés (formula Observation + Tension + Reframe + Bridge), `compose-creative` reference PNT-NN comme substrate angle. Drill audience-drill expose pain_points inline 360° via `/phantom {brand} audiences {slug}` · drill item `/phantom {brand} audiences {slug}/pain_points/{PNT-NN}` (fiche complète avec chain functional/emotional/identity + verbatim_quotes + cross-refs).

## Les principes canon

### 1 · Le client achète l'identité, pas le mécanisme

Le mécanisme (formule, technologie, ingrédient) est ce qui rend la promesse crédible. Ce n'est pas ce qui déclenche l'achat. Le déclencheur est l'identité que le produit projette sur le client.

Exemple · AG1 contient 75 vitamines/minéraux/herbes (mécanisme). Le client achète *"je prends soin de mon corps comme un athlète olympique"* (identité). Si Athletic Greens vendait juste *"75 nutriments dans un sachet"*, le produit existerait à 5x moins cher chez Costco. Ce qui justifie le $99/mois · l'identité.

Règle · le mécanisme prouve, l'identité vend.

### 2 · La chaîne canon, jamais skip un layer

Trois layers, séquencés sans saut. Si tu sautes le functional, le claim emotional sonne magique. Si tu sautes l'emotional, l'identity sonne artificielle. Si tu ne va pas jusqu'à l'identity, ton copy reste interchangeable.

```
Functional      →     Emotional     →     Identity
(observable)         (ressenti)          (projection self-concept)

"je dors 8h"    →    "je me réveille    →    "je suis quelqu'un
                      reposé"                 qui dort bien"
```

Test rapide · prends n'importe quel bullet de ton copy. Demande-toi *"et alors ?"* trois fois. Si à la troisième tu n'arrives pas à un statement d'identité, tu n'as pas chainé.

### 3 · Latency observable · le timing fait partie de la promise

Un bénéfice sans timing est une promesse floue. *"Tu dormiras mieux"* convertit moins que *"tu dormiras mieux en 14 jours"*. Le timing transforme une promesse abstraite en attente concrète mesurable.

Latency typique selon catégorie ·
- Skincare · 4-8 semaines pour résultats visibles (concentration peptides, retinoïdes)
- Supplements · 2-12 semaines selon métabolisme et déficience initiale
- Software · résultats immédiats (productivité, automation, signup → résultat)
- Hardware fitness · 1-7 jours pour habituation, 4-12 semaines pour transformation
- Fashion · immédiat (porter = ressentir)

Le copywriter pro mentionne explicitement la latency. Le copywriter amateur la laisse implicite. Le client achète plus quand le timing est nommé.

### 4 · Evidence verbatim · ancrer dans la voix client, pas la voix brand

L'identité projetée doit sonner comme **les mots du client**, pas les mots du brand. Le brand qui dit *"tu deviendras la version reposée de toi"* sonne marketing. Le client qui dit *"depuis que je dors mieux, je me sens à nouveau moi-même"* sonne authentique.

Sourcing · interviews clients, reviews, DMs, Reddit threads, App Store reviews, comments YouTube. La phrase identitaire DOIT déjà avoir été prononcée par un client réel pour être insérée en copy. Inventer une identité = bullshit detector activé.

Joseph Sugarman dans *The Adweek Copywriting Handbook* (Chapter 5, "The Psychological Triggers") · *"The customer's exact words, used back to them, are 10x more persuasive than your most clever copy."*

### 5 · Identity layer · jamais verbalisé directement

Règle technique souvent ratée · l'identité ne se dit pas explicitement *"tu deviendras X"*. Elle se projette implicitement à travers les choix lexicaux, les visuels, les références culturelles, les témoignages choisis.

**Mauvais** · *"Avec Whoop, tu deviendras un athlète optimisé."* → sonne forcé, infantilisant.

**Bon** · ad Whoop qui montre LeBron James, NBA conditioning coaches, marathoner pro. Le viewer s'identifie. *"Je suis comme eux. Je suis sérieux. J'optimise."* L'identité est inférée, jamais déclarée.

Donald Miller dans *Building a StoryBrand* le formule · *"Position the customer as the hero, not the brand. The hero becomes who he is through the action, not because you tell him so."*

---

## La méthode · les 3 layers

### Layer 1 · Functional (observable, mesurable, factuel)

**Définition** · effet physique observable, mesurable par le client lui-même, sans interprétation subjective.

**Caractéristiques** ·
- Vérifiable (le client peut le constater seul)
- Mesurable (chiffres, durée, fréquence, quantité)
- Factuel (zéro interprétation émotionnelle requise)

**Exemples cross-catégories** ·
- Skincare · *"hydrate 24h"*, *"réduit les rides de 30% en 8 semaines"*, *"absorbe en 60 secondes"*
- Supplements · *"endormissement en 23 minutes"*, *"+18% d'énergie matinale"*, *"75 vitamines/minéraux"*
- Software · *"automatise 12 workflows"*, *"économise 5h/semaine"*, *"intègre 50 outils"*
- Hardware · *"autonomie 18h"*, *"poids 89g"*, *"étanche jusqu'à 50m"*
- Fashion · *"sèche en 4h"*, *"résiste à 200 lavages"*, *"-20°C confort"*

**Comment l'identifier en VoC (voice of customer)** · cherche les verbatims **descriptifs sans émotion**.
- *"J'ai dormi 8h"* → functional
- *"Mes cheveux poussent de 2cm/mois"* → functional
- *"L'app a importé mes 500 contacts en 30s"* → functional

**Pitfall fréquent** · s'arrêter au functional. Beaucoup de copy DTC ne dépasse jamais ce layer. Convertit à minima.

### Layer 2 · Emotional (ressenti subjectif, non-mesurable, interprétatif)

**Définition** · ressenti subjectif que le client vit en conséquence du functional. Non-mesurable directement, mais nommable verbalement.

**Caractéristiques** ·
- Subjectif (varie d'un client à l'autre)
- Verbalisable (*"je me sens X"*)
- Causalement lié au functional (sans le functional, l'emotional ne tient pas)

**Exemples cross-catégories chain functional → emotional** ·

| Functional | → Emotional |
|---|---|
| "je dors 8h" | "je me réveille reposé sans café" |
| "ma peau brille" | "je me sens belle sans maquillage" |
| "j'ai perdu 3 kg" | "je rentre dans mon jean préféré sans aspirer le ventre" |
| "l'app gère mes tâches" | "j'ai l'esprit libre le weekend" |
| "le casque coupe le bruit" | "je suis dans ma bulle même dans l'open space" |
| "la montre track mon sommeil" | "je comprends enfin pourquoi je suis crevé" |

**Comment l'identifier en VoC** · cherche les verbatims **"je me sens..."**, **"j'ai l'impression de..."**, **"depuis que..."**.

**Pitfall fréquent** · sauter directement du functional à l'identity (*"endormissement 30 min, deviens la version reposée de toi"*). Manque le pont causal. Le client n'achète pas.

### Layer 3 · Identity (projection self-concept, durable, identitaire)

**Définition** · projection de qui le client devient (ou se confirme être) par l'usage répété du produit. Self-concept stabilisé dans le temps.

**Caractéristiques** ·
- Durable (l'identité persiste, le produit l'alimente)
- Self-defining (*"je suis quelqu'un qui..."*)
- Sociale implicite (le client se positionne dans un groupe)

**Exemples cross-catégories chain emotional → identity** ·

| Emotional | → Identity |
|---|---|
| "je me réveille reposé" | "je suis quelqu'un qui dort bien" |
| "je me sens belle sans maquillage" | "je suis une femme qui n'a pas besoin d'artifice" |
| "je rentre dans mon jean préféré" | "je suis quelqu'un qui prend soin de son corps" |
| "j'ai l'esprit libre le weekend" | "je suis un pro qui sait s'organiser" |
| "je suis dans ma bulle" | "je suis quelqu'un qui maîtrise son focus" |
| "je comprends pourquoi je suis crevé" | "je suis un athlète qui pilote sa récup" |

**Comment l'identifier en VoC** · cherche les verbatims **"je suis...", "je suis devenu...", "depuis [produit], je..."**, en particulier dans les reviews long-form ou interviews.

**Pitfall fréquent** · inventer une identité non-ancrée dans la voix client. *"Tu deviendras Athena, déesse moderne de l'équilibre."* → personne n'a jamais dit ça. Le copy sonne corporate.

### Règle de chaînage · ordre obligatoire functional → emotional → identity

L'ordre n'est pas optionnel. C'est une cascade causale.

```
[Functional] cause → [Emotional] cause → [Identity]
```

Le functional **cause** l'emotional. L'emotional **renforce** l'identity. Sans causalité, la chaîne casse.

Erreur classique · partir de l'identity sans la fonder.

> *"Deviens la meilleure version de toi avec [produit]."*

Mais quel functional ? Quel emotional ? Le client lit, ne comprend pas comment cette transformation s'opère, n'achète pas.

Bon chaînage ·

> *"Endormissement en 23 minutes (functional). Tu te réveilles sans avoir besoin de café pour démarrer (emotional). Tu redeviens quelqu'un qui dort bien, comme avant les enfants (identity)."*

Chaque étape est causale, vérifiable, ancrée. Le client comprend mécaniquement comment il arrive à l'identité finale.

---

## Exemples · 5 brands publiques décomposées

### Exemple 1 · Hims (Sleep Gummies)

**Functional** · *"Fall asleep in less than 30 minutes. With melatonin, L-theanine and chamomile."*
→ Effet observable, latency nommée (30 min), mécanisme transparent (ingrédients).

**Emotional** · *"Wake up refreshed, not groggy."*
→ Ressenti subjectif au réveil. Causalement lié à un meilleur endormissement.

**Identity** · projetée visuellement et par les testimonials · *"I'm someone who's finally got my sleep figured out."* Hims évite de verbaliser directement *"deviens un dormeur optimisé"*. À la place, ils montrent des hommes 30-45 ans, vie pro intense, qui parlent en review de *"feeling like myself again"*, *"being a better dad because I'm rested"*.

**Chain analysis** · functional concret, emotional empathique, identity ancrée dans verbatims de pères/pros surchargés. Pas de saut. Pas d'identité magique.

### Exemple 2 · Athletic Greens (AG1)

**Functional** · *"75 vitamins, minerals, whole-food sourced ingredients, prebiotics, probiotics, adaptogens · all in one scoop."*
→ Quantifié, formulation explicite. Le client peut vérifier la liste.

**Emotional** · *"Sustained energy throughout the day, without the afternoon crash."*
→ Ressenti subjectif (énergie stable). Causalement lié au functional (couvre les déficiences nutritionnelles qui causent les crashes).

**Identity** · *"I'm the type of person who treats my body like an athlete treats theirs."* Confirmé par les endorsements (Tim Ferriss, Andrew Huberman, Joe Rogan · biohackers high-performers). Le client AG1 se positionne dans la culture "high performance / longevity" sans avoir à le dire.

**Chain analysis** · functional ultra-spécifique (75 ingrédients = breakthrough sur sophistication élevée), emotional axé sur stabilité (vs spike caféine), identity portée par culture social-proof high-performer. La latency est moins explicite (AG1 dit "feel a difference in 30 days") mais présente.

### Exemple 3 · Glossier (Boy Brow / Cloud Paint)

**Functional** · *"Brow gel that shapes, fills and grooms in one stroke. Smudge-proof. 6 shades."*
→ Effet observable et factuel. Mesurable (6 shades, smudge-proof).

**Emotional** · *"You feel pulled-together without looking like you tried."*
→ Ressenti subjectif (l'aisance, le naturel). Causalement lié au functional (un produit qui fait tout en une étape).

**Identity** · *"No-makeup makeup, c'est moi."* Glossier a construit toute une identité de marque autour de l'idée que la femme Glossier n'est pas une femme "maquillée" classique · elle est *"effortlessly cool"*. Confirmé par toute la communication visuelle (skin in close-up, freckles visible, peu de retouches).

**Chain analysis** · Glossier est un cas d'école du layer identity puissant. La marque a même façonné une catégorie ("skin-first makeup") pour rendre l'identité plus tangible. Le functional reste honnête (pas surclaim), l'emotional est universellement reconnaissable, l'identity est presque devenue un mouvement culturel.

### Exemple 4 · Apple AirPods Pro

**Functional** · *"Active noise cancellation. Adaptive Audio. Transparency mode. Up to 6 hours of listening time."*
→ Technologies nommées, métriques précises (6h autonomie).

**Emotional** · *"Your world becomes yours. Switch from full focus to full awareness, instantly."*
→ Ressenti subjectif de maîtrise. Causalement lié au functional (ANC + Transparency = contrôle).

**Identity** · *"I'm someone who controls my focus and my environment."* Apple ne verbalise jamais cette identité directement. Elle est portée par les visuels (gens dans des moments de concentration · running, designing, conversation intime), par les use cases mis en scène, et par l'écosystème Apple plus large (être un Apple user = certaine identité de "creator/maker/optimizer").

**Chain analysis** · Apple maîtrise le layer identity sans jamais l'écrire. Le copy s'arrête à l'emotional ("your world becomes yours"). L'identity est inférée par le viewer via les visuels, le cadre, le contexte. Pattern Apple classique · *"Show, don't tell."*

### Exemple 5 · Whoop

**Functional** · *"Tracks 24/7 your heart rate variability, strain, recovery, and sleep. Generates a daily recovery score 0-100."*
→ Métriques précises, technologie nommée (HRV).

**Emotional** · *"You know when to push and when to rest. No more guessing."*
→ Ressenti subjectif de clarté décisionnelle. Causalement lié au functional (recovery score → action).

**Identity** · *"I'm an athlete who optimizes."* Confirmé par les endorsements (LeBron James, Cristiano Ronaldo, Michael Phelps), par le langage Whoop (*"members"*, *"performance"*, *"WHOOP Coach"*), et par la communauté (groupes Reddit, Whoop forums où les users discutent leurs *"strain coach"* et *"sleep coach"*).

**Chain analysis** · Whoop a explicitement construit une identité ("the athlete who tracks"). Le functional est technique mais accessible. L'emotional traduit la complexité technique en action simple (push vs rest). L'identity est portée par le cercle social (athletes pro endorsés, communauté users). Le client devient un *"Whoop member"* · l'identité est marquée par le nom même de leur abonnement.

---

## Pitfalls classiques

### Pitfall 1 · Vendre seulement le functional

Erreur de débutant. Tu écris une fiche produit qui liste 10 features et 3 bénéfices fonctionnels. *"100% naturel, sans gluten, vegan, vegan, locally sourced."* Tu crois faire du copy. Tu fais une fiche technique.

Diagnostic · si ton copy peut être copié-collé sur le produit d'un concurrent en changeant juste le nom de la brand, tu es bloqué au functional.

Fix · pour chaque bénéfice fonctionnel, demande-toi *"et alors, qu'est-ce que ça change pour le client dans sa vie ?"* Tu trouves l'emotional. Demande-toi à nouveau *"et alors, qu'est-ce que ça dit de lui ?"* Tu trouves l'identity.

### Pitfall 2 · Sauter du functional à l'identity (saut magique)

Tu lis Schwartz, tu comprends qu'il faut viser l'identité. Tu sautes l'étape emotional. Résultat ·

> *"Endormissement en 30 minutes (functional). Deviens la version reposée de toi (identity)."*

Le client lit, sent qu'il y a un saut. Le claim sonne magique, non-crédible. Comment passe-t-on de *"je m'endors plus vite"* à *"je suis une nouvelle personne"* ? Sans l'emotional intermédiaire (*"je me réveille frais, je commence ma journée différemment"*), le pont manque.

Fix · toujours nommer le ressenti subjectif intermédiaire avant de projeter l'identité.

### Pitfall 3 · Identity sans evidence verbatim

Tu inventes une identité qui sonne bien à toi mais n'a jamais été prononcée par un vrai client.

> *"Deviens la déesse moderne de ton équilibre intérieur."*

Personne ne dit ça. Le client lit, sent l'artifice, bullshit detector activé. Le copy sonne corporate, comme une brand qui parle de son audience sans la connaître.

Fix · chaque statement identitaire en copy doit être traçable à un verbatim client (review, interview, DM). Si tu ne peux pas pointer vers le verbatim source, l'identité est inventée. Reformule ou drop.

Halbert dans *Boron Letter #11* · *"The best copy I've ever written, I've stolen from customer letters."*

### Pitfall 4 · Identity verbalisée explicitement (banni)

Erreur subtile. Tu as bien chainé, tu as bien sourcé, mais tu écris l'identité directement ·

> *"Tu seras la version reposée de toi."* / *"Tu deviendras un athlète optimisé."*

Le client lit, sent l'instruction. Sonne forcé, presque infantilisant. L'identité n'est pas un état à atteindre que tu prescris · c'est une projection que le client fait lui-même quand le copy crée les conditions.

Fix · ne jamais conjuguer l'identity au futur direct. Plutôt ·
- Témoignages clients qui décrivent leur transformation à eux
- Visuels qui montrent des gens dans cette identité (cf. Apple, Whoop)
- Langage du brand qui présuppose l'identité (*"for the athlete in you"* vs *"deviens un athlète"*)

### Pitfall 5 · Chaîne incohérente entre les 3 layers

Tu chaînes les 3 layers mais ils ne sont pas cohérents narrativement. Exemple ·

> *"Hydrate 24h (functional). Tu te sens fraîche (emotional). Tu es une femme d'affaires conquérante (identity)."*

Le saut emotional → identity est arbitraire. Rien dans *"fraîche"* ne mène à *"conquérante"*. Le copy sonne piloté par buzzwords, pas par une vraie story.

Fix · l'identité doit être la **conclusion logique** du functional + emotional, pas un statement greffé. Test · demande-toi *"si je ne montre que le functional + emotional, est-ce que l'identité ressort naturellement dans la tête du lecteur ?"* Si oui, tu as chaîné. Si non, tu as collé.

### Pitfall 6 · Ignorer la latency

Tu décris bien functional/emotional/identity, mais tu ne précises jamais en combien de temps. Le client lit, fantasme une transformation immédiate, achète, est déçu à J+7 (*"il ne s'est rien passé"*), churn.

Fix · ajoute la latency à chaque promise. *"En 14 jours."*, *"D'ici 8 semaines."*, *"Dès la première application."*. Sois honnête. Le client préfère une promesse vraie à 4 semaines qu'une promesse magique à J+1 qu'il vivra comme un mensonge.

---

## Checklist applicable

Pour chaque bénéfice majeur du produit, applique cette grille en 7 questions.

- [ ] **Quel functional observable** (mesurable, vérifiable par le client) ai-je formulé ?
- [ ] **Quel emotional ressenti subjectif** découle causalement de ce functional ?
- [ ] **Quelle identity projection** se construit naturellement à partir de cet emotional ?
- [ ] **La chain est-elle cohérente** sans saut (functional → emotional → identity = causalité, pas collage) ?
- [ ] **La latency observable** est-elle mentionnée (timing concret de la transformation) ?
- [ ] **L'identity est-elle implicite** (projetée par testimonials, visuels, langage) plutôt que verbalisée au futur direct ?
- [ ] **Chaque layer est-il ancré sur evidence verbatim** (reviews, interviews, DMs sourcés) ?

Si une seule case n'est pas cochée, retravaille avant ship.

### Quick test "Et alors ?" en 3 itérations

Prends n'importe quel bullet de ton copy.

1. *"100% magnésium bisglycinate haute absorption."* → **Et alors ?**
2. *"Tu absorbes 4x plus de magnésium que les supps classiques · tu sens vraiment l'effet."* → **Et alors ?**
3. *"Tu te réveilles reposé, calme · tu es enfin quelqu'un qui dort bien sans somnifère."*

Si tu n'arrives pas à l'identité au 3ème *"et alors"*, ta chaîne est incomplète. Tu vends encore le mécanisme, pas la transformation.

---

## Position dans le système opérationnel 5 couches

Pain-benefit chain est une instance canonique de la couche 1 (modèle ·
ECR pattern Funnel auto-similaire) du système opérationnel PhantomOS (cf
`operational-system-doctrine.md`). Le chaînage surface → consequence →
deep est fractal · le même schéma de décomposition (3 niveaux séquentiels
emboîtés) se retrouve sur chaque pain point, et à l'échelle de l'audience
mère vs sous-poches.

Severity discriminante + tier marker primary/secondary touchent aussi
la couche 4 (métriques · scoring entité-level).

---

## Cross-refs · canonical IDs explicit (v2.64)

L'ontologie pure v2.64 verrouille la chain pain → benefit via canonical IDs PNT-NN référencés explicitement dans les entités sœurs. Storage canonical · sub-folder OWNED audience-specific `brands/{brand}/audiences/{slug}/pain_points/{PNT-NN}.json`. Pain shared cross-audiences · stocké primary owner avec `also_affects_audiences[]` array.

| Entité référente | Field cross-ref | Description |
|---|---|---|
| `angle.lineage.pain_ref` | `PNT-NN` | Angle dérivé d'un pain canonical (e.g. ANG-04 reframe sur PNT-01 "sommeil profond perturbé") |
| `objection.derived_angle_refs[]` | `PNT-NN` array | Pains qui alimentent une objection (e.g. OBJ-01 "trop cher" reliée à PNT-01 + PNT-04 sources) |
| `friction.cross_refs.pain_point_ids[]` | `PNT-NN` array | Frictions usage product-specific qui touchent le même substrat pain (e.g. FRC-05 sub-product onboarding sur PNT-01 chain) |
| `audience.pain_point_refs[]` | `PNT-NN` array | Audience cartographiée référence ses pains OWNED sub-folder (legacy v2.60- inline pain_points deprecated) |
| `brief.derived_pain_refs[]` | `PNT-NN` array | Brief copy ancre sur pains canonical (traçabilité source) |
| `pain_point.also_affects_audiences[]` | slug array | Audiences additionnelles impactées par ce pain (shared cross-audience entry, primary owner stocke) |

**Pattern v2.64 sémantique pure · sub-folders OWNED + cross-refs shared.** Pain_points + objections = OWNED sub-folder audiences/{slug}/, frictions = OWNED sub-folder products/{slug}/. Cross-refs entre entities via `related_pain_point_refs[]`, `related_objection_refs[]`, `related_friction_refs[]` (bi-directionnel). Storage 1 fichier par entité primary owner · pain shared entre N audiences encodé 1 fois avec `also_affects_audiences[]` array. Drill audience-specific 360° via `/phantom {brand} audiences {slug}` expose pain_points + objections inline natif.

**Skill consumption pattern (v2.64)** ·
- `mine-voc` capture verbatim_quotes[] → propose nouveau PNT-NN candidat audience-specific
- `profile-audience` structure sub-folder OWNED pain_points/ + objections/ + cross-refs `also_affects_audiences[]`
- `produce-paid-angles` consume PNT-NN canon pour formula angle (Observation = pain surface · Tension = pain consequence · Reframe = benefit identity · Bridge = mécanisme)
- `compose-creative` reference PNT-NN comme substrate canonical, traçable depuis l'angle source

## Sources & lectures

### Canon direct-response

- **Gary Halbert, *The Boron Letters* (1984-1986, compilation 2013)** · letter #11 dédiée au principe *"people buy results, not features"*. Halbert insiste sur le sourcing des bénéfices via customer letters, jamais inventés.
- **Joseph Sugarman, *The Adweek Copywriting Handbook* (2007)** · Chapter 5 "Psychological Triggers" et Chapter 7 "The Link Between Problem and Solution" couvrent explicitement le pont functional → emotional → identity, avec exemples de sales letters Sugarman (Blu Blocker sunglasses, JS&A products).
- **Dan Kennedy, *The Ultimate Sales Letter* (1990, ed. 4 2011)** · chapter sur "Painting a picture" qui formalise comment chaîner observable + sensoriel + identitaire dans un long-form sales letter.
- **John Caples, *Tested Advertising Methods* (1932, ed. revue 1997)** · Chapter 1 ouvre sur le canon *"Don't sell the steak, sell the sizzle"* (attribué à Elmer Wheeler, popularisé par Caples). Le steak = functional. Le sizzle = emotional. L'identity vient en couche au-dessus chez Caples.

### Storytelling & transformation

- **Donald Miller, *Building a StoryBrand* (2017)** · framework SB7 (Character, Problem, Guide, Plan, Call to Action, Avoiding Failure, Success). Le layer "Success" est exactement la projection d'identité. Miller insiste sur le fait que le client est le hero, pas le brand · l'identité se projette sur lui, pas sur le produit.
- **Chip & Dan Heath, *Made to Stick* (2007)** · principe *"Emotional"* dans le framework SUCCESs. Heath insiste sur *"piggybacking"* · attacher l'émotionnel à quelque chose que le client ressent déjà fortement (groupe d'appartenance, valeur identitaire).
- **Russell Brunson, *Expert Secrets* (2017)** · *"the new opportunity vs the improvement"* · transformer ce que le client devient (new opportunity = identity) vs juste améliorer ce qu'il fait. Frontière exacte functional → identity.

### Neurosciences & décision

- **Donald Calne (neurologue, 1999)** · principe canon *"Reason leads to conclusions. Emotion leads to action."* La décision d'achat est émotionnelle, justifiée rationnellement après coup. Le functional sert à justifier · l'emotional + identity déclenche.
- **Antonio Damasio, *Descartes' Error* (1994)** · démonstration neurologique que les patients avec lésion du cortex préfrontal (zone émotionnelle) sont incapables de décider, malgré une logique intacte. Confirme empiriquement que vendre uniquement functional = vendre à un cerveau qui ne décide pas.
- **Daniel Kahneman, *Thinking Fast and Slow* (2011)** · Système 1 (rapide, émotionnel, intuitif) prend la décision · Système 2 (lent, analytique) rationalise. Le copy pro parle au Système 1 (emotional + identity) puis nourrit le Système 2 (functional + proof) pour la rationalisation post-décision.

### Marketing intelligence

- **Clayton Christensen, *Jobs to Be Done* (formalisé 2003-2016)** · le client *"hires"* un produit pour un *"job"*. Le job est rarement functional pur · c'est presque toujours emotional ou identity. *"I don't hire a milkshake because it's tasty. I hire it because it makes my boring commute feel meaningful."* Application directe du chain layer.
- **Bernadette Jiwa, *The Story of Telling* (blog + livres 2013+)** · principe *"Marketing is not about selling products. It's about helping people become the people they want to be."* Formulation contemporaine du canon Halbert / Miller.
- **Seth Godin, *This Is Marketing* (2018)** · *"People like us do things like this."* Statement identitaire ultime. Godin insiste sur la cohérence du *"people like us"* (tribu) comme moteur de décision plus puissant que feature/price.

### Pour pratiquer

- Prends 10 ads concurrentes de ta catégorie. Décompose chacune en functional / emotional / identity. Tu trouveras 60-70% bloquées au functional ou avec une chain cassée. Identifies-y ton edge.
- Sur les reviews 5-stars d'un produit, surligne en 3 couleurs · functional (bleu), emotional (jaune), identity (rouge). Tu verras visuellement où les meilleurs verbatims clients atterrissent. Ce sont tes copy hooks.
- Chez Glossier, Apple, Whoop, lis 10 pages produits chacune. Tu verras le pattern · la chain est explicite en functional + emotional, l'identity est implicite (visuels, testimonials, langage). Imite la structure, pas le ton.
