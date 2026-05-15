---
name: watch-competitors
type: producer
version: "1.0.0"
recommended_model: sonnet
layer: territoire
reasoning_pattern: null
description: >
  Analyse les publicités Meta des concurrents d'une brand et produit un rapport
  de veille créative avec les angles, mechanics, et signaux d'opportunité observés.
  FR: "surveille mes concurrents Meta", "qu'est-ce que font mes concurrents sur Meta",
  "veille concurrentielle", "analyse les pubs des concurrents", "competitive Intel Meta".
  EN: "watch competitors on Meta", "competitor ads analysis", "Meta competitive intelligence".
permissions:
  reads: [brand]
  writes: [brand]
  mode: proposed
  subagent_safe: true
pipeline:
  preconditions: brand.json existe avec market.competitors[] renseigné
  postconditions: validate-resources
---

## Tone

Rapport en langage business. L'opérateur lit des insights concurrentiels, pas des données brutes. Chiffres quand pertinents, conclusions actionables.

# Skill: Competitor Watcher

Analyse les publicités Meta des concurrents d'une brand.

À partir de `brand.json → market.competitors[]`, l'agent accède à la Meta Ads Library de chaque concurrent, extrait les créas actives, les catégorise selon l'angle-registry et creative-mechanics-registry du workspace, et produit un rapport de veille avec les signaux d'opportunité.

---

## Step 1 — Charger le contexte de la brand

Lire dans cet ordre :

1. **`brand.json`** → extraire :
   - `market.competitors[]` → liste des concurrents avec leur URL
   - `positioning.purchase_driver` → le driver de la brand (pain / desire / identity / etc.)
   - `positioning.brand_differentiation` → le positionnement actuel
   - `meta.vertical` + `meta.market`

2. **`shared-resources/registries/angle-registry.md`** → charger la taxonomie complète des angles. Ce sont les catégories d'analyse.

3. **`shared-resources/registries/creative-mechanics-registry.md`** → charger la taxonomie des mechanics. Ces deux fichiers sont la grille de lecture.

**Si `market.competitors[]` est vide ou absent :**
→ Stopper et signaler : "Je ne trouve pas de concurrents dans brand.json → `market.competitors[]`. Ajoute au moins un concurrent (nom + URL Meta Ads Library) avant de lancer cet agent."

---

## Step 2 — Collecter les publicités actives

Pour chaque concurrent dans `market.competitors[]` :

**Si MCP Meta Ads Library disponible :**
- Appeler l'outil MCP avec `advertiser_page_id` ou URL page Facebook du concurrent
- Paramètres : `active_status: ACTIVE`, `limit: 20`, `fields: [ad_creative_body, ad_creative_link_caption, ad_delivery_start_time, impressions]`
- Stocker les résultats dans une variable `$raw_ads_{competitor_slug}`

**Si MCP Meta Ads Library indisponible (fallback) :**
- Informer l'opérateur : "Je n'ai pas accès direct à Meta Ads Library. Pour chaque concurrent, ouvre `https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&q={nom_concurrent}` et colle les textes des 5-10 pubs actives dans le chat."
- Attendre les inputs manuels
- Stocker dans `$raw_ads_{competitor_slug}`

**Si aucun résultat pour un concurrent :**
→ Logger "0 pubs actives trouvées pour {concurrent}" et continuer. Ne pas bloquer.

---

## Step 3 — Analyser chaque publicité

Pour chaque pub collectée, extraire :

| Champ | Comment l'identifier |
|-------|---------------------|
| `angle` | Comparer le message avec `angle-registry.md` → identifier l'angle dominant (1 angle par pub) |
| `mechanic` | Comparer la structure créative avec `creative-mechanics-registry.md` → identifier la mécanique (1-2 mechanics par pub) |
| `hook_type` | Question / Statement / Before-After / Statistic / Confession / Callout / Revelation |
| `awareness_level` | Unaware / Problem-aware / Solution-aware / Product-aware / Most-aware |
| `lever` | Fear / Desire / Rational |

Agréger par concurrent :
```
{concurrent_slug}:
  total_ads_analyzed: N
  angles_observed: [{angle: "transformation", count: 4}, ...]
  mechanics_observed: [{mechanic: "ugc", count: 6}, ...]
  dominant_angle: "transformation"  # le plus fréquent
  dominant_mechanic: "ugc"
  awareness_distribution: {problem_aware: 0.6, solution_aware: 0.3, ...}
```

---

## Step 4 — Identifier les signaux d'opportunité

Croiser les patterns concurrents avec la brand analysée :

**Angles over-indexés chez les concurrents** (> 60% des pubs sur un angle) :
→ Signal de saturation : éviter cet angle ou le contrarianer

**Angles absents chez les concurrents** :
→ Signal d'opportunité : whitespace potentiel

**Mechanics dominant la catégorie** :
→ Si même mechanic chez tous → hygiene. Si unique à un concurrent → propriété potentielle.

**Awareness gap** :
→ Si concurrents ciblent tous solution_aware → opportunité en problem_aware (top of funnel)

Format des signaux :
```
SIGNAL_1:
  type: "whitespace" | "saturation" | "mechanic_ownership" | "awareness_gap"
  observation: "[description factuelle]"
  implication: "[ce que ça signifie pour la brand]"
  suggested_action: "[angle ou mechanic à tester]"
  confidence: 0.7
```

---

## Step 5 — Produire le rapport

Générer `competitive-intel-{brand-slug}-{YYYY-MM-DD}.md` dans `brands/{brand}/strategy/` :

```markdown
# Competitive Intelligence — {brand.meta.name}
> Généré le : {date}
> Concurrents analysés : {liste}
> Pubs analysées : {total}
> Méthode : {MCP direct | input manuel}

---

## Vue par concurrent

### {concurrent_name}
- Angle dominant : {angle} ({count} pubs / {pct}%)
- Mechanics observées : {liste}
- Ton général : {lever} ({pct}%)
- Awareness ciblé : {distribution}
- Observations notables : [liste]

---

## Signaux d'opportunité

{liste des SIGNAL_X avec observation + implication + action suggérée}

---

## Recommandations pour la prochaine batch créative

1. **Angle à tester** : {angle whitespace identifié} — absent chez {N} concurrents sur {total}
2. **Mécanique à éviter** : {mechanic saturée} — utilisée par {N} concurrents
3. **Awareness à cibler** : {niveau sous-exploité} — {ratio concurrents qui l'utilisent}

---

## Sources

{liste des URLs Meta Ads Library consultées ou inputs manuels avec date}
```

---

## Step 6 — Proposer les insights au Context Engine

Pour les signaux à confidence ≥ 0.7, appeler `.skills/write-to-context.py` pour chaque insight :

```bash
python3 .skills/write-to-context.py \
  --path "brands/{slug}/brand.json#/market/external_intelligence/-" \
  --value '{"source":"Meta Ads Library","signal":"{1-line observation}","tags":["competitor","creative-intel","{ANGLE_TAG}"]}' \
  --source inference \
  --confidence {0.7-0.9} \
  --mode proposed \
  --reason "watch-competitors run {RUN_ID}"
```

Un appel par signal. `--mode proposed` n'accepte que des dict values (stamps `_proposed/_source/_confidence` en place).

Un appel par signal. Maximum 5 signaux par run.

---

## Output Format

- **Fichier markdown** : `brands/{brand}/strategy/competitive-intel-{brand-slug}-{YYYY-MM-DD}.md`
- **Proposals write-to-context** : `brands/{brand}/brand.json#/market/external_intelligence/-`
- **Log de run** : dernière ligne du rapport indique `RUN_ID` et nombre de proposals créées

---

## Hard Rules

- **NEVER inventer des pubs.** Si une pub n'est pas collectée, elle n'existe pas. Pas d'hallucination sur les créas.
- **NEVER écrire directement dans brand.json.** Toujours ``.skills/write-to-context.py` (canonical channel — see capture-learning Step 4 for the exact Bash invocation)` en mode `proposed`.
- **ALWAYS indiquer la méthode de collecte** (MCP direct ou input manuel) dans le rapport.
- **ALWAYS utiliser l'angle-registry et le creative-mechanics-registry comme grille.** Ne pas inventer de nouvelles catégories dans le rapport.
- **Max 5 proposals** par run. Si plus de 5 signaux, prioriser par confidence décroissante.
- **Si 0 pub collectée** pour tous les concurrents → stopper et demander à l'opérateur de vérifier `market.competitors[]` dans brand.json.
