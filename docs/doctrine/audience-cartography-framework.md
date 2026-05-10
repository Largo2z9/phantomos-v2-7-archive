# Audience Cartography Framework

> Comment cartographier les audiences d'une brand · model mental simple, applicable à n'importe quel marché. Pas une spec technique, un cours.

## Pourquoi cartographier ?

Une brand qui parle à "toutes les femmes" parle à personne. La cartographie d'audience te dit · qui parle quoi, où concentrer ton effort, et où sont les angles porteurs cachés.

Cartographier = répondre à 4 questions simples par audience.

## Le framework · 4 questions

### Q1 · Quelle est sa PORTE D'ENTRÉE ?

Une audience entre dans ta catégorie produit par une de 3 portes :

| Porte | Définition | Exemple hair care |
|---|---|---|
| **Pain-driven** | Entre par un problème ressenti | "Mes cheveux tombent" |
| **Goal-driven** | Entre par une ambition projet | "Je veux des cheveux longs pour mon mariage" |
| **Identity-driven** | Entre par qui elle est ou veut être | "Je porte des tresses serrées et je veux préserver mes edges" |

Une vraie audience a 1 porte dominante. Si elle a 3 portes égales, c'est un mix mal séparé · à re-découper.

### Q2 · Quel est son NIVEAU de granularité ?

Comme une matriochka, audiences emboîtées sur 3 niveaux maximum :

```
BROAD              "femme qui perd ses cheveux"
  └── SEGMENT          "post-grossesse"
        └── MICRO          "post-grossesse allaitante 1ère fois"
```

| Niveau | Volume | Cardinalité par brand |
|---|---|---|
| Broad | Grand · 500k+ | 1-3 maximum |
| Segment | Moyen · 100-500k | 5-15 par broad |
| Micro | Niche · 20-100k | 0-3 par segment, optionnel |

**Règle pour descendre d'un niveau · faut 3/3** :

1. Volume restant suffisant pour activation
2. Pitch vraiment divergent (hook · registre · visuels)
3. Offer/produit divergent (composition · format · prix)

Si seulement 2/3 → variation copy, pas sous-audience.
Si 1/3 → simple nuance, pas découpage.

### Q3 · Quel est son STADE ?

Schwartz 1957 toujours valide. Deux axes modulent comment lui parler :

**Axe product-awareness · où dans le funnel produit ?**

```
Unaware → Problem-aware → Solution-aware → Product-aware → Most-aware
```

**Axe emotional-maturity · rapport psychologique au problème ?**

```
Niant → Résigné → En recherche → Combatif → Acceptant
```

Une même "femme post-grossesse" peut être à 5 stades différents. Ce ne sont pas 5 audiences · ce sont 5 hooks différents pour la même audience.

### Q4 · Avec qui elle CHEVAUCHE ?

Aucune audience ne vit en isolation. Exemples hair care :

```
chute-post-grossesse  ↔  chute-stress-hormonal     (post-partum = stress hormonal)
chute-stress-hormonal ↔  chute-active              (stress chronique = chute manifeste)
pousse-jeune-adulte   ↔  croissance-projet         (objectif "summer hair")
```

Reconnaître les chevauchements · c'est éviter de créer des angles contradictoires et permettre cross-pollinisation copy entre audiences cousines.

## Le model mental visuel · arbre généalogique avec cousins

- **Branches verticales** = hiérarchie (parent → enfant → petit-enfant)
- **Liens horizontaux** = chevauchements (cousins)
- **Feuilles** = personas individuels qui peuvent vivre dans plusieurs branches

L'audience est un **niveau d'agrégation comportementale**, pas une personne. Tu cartographies des comportements partagés, pas des individus.

## Les 3 pièges classiques

### Piège 1 · Audience-fantôme

Sub-division créée sans pitch ni offer divergent. Tu créés du travail mort. Détecte-la · le test 3/3 (Q2) échoue.

### Piège 2 · Audience-redondante

2 segments différents qui parlent au même persona avec des labels différents. Tu te dis "j'ai 2 audiences" alors qu'elles sont 90% les mêmes. Détecte-la · si tu écris des personas tests A et B et qu'ils sont quasi identiques, fusionne.

### Piège 3 · Audience-orpheline

Segment sans broad parent. Signe que tu as raté une étape de cartographie ascendante. Détecte-la · pas de réponse à la question "elle vient d'où dans le marché ?".

## Loi de Pareto · l'audience-king

80% du revenue brand vient de **2-3 audiences activées**, jamais 7.

La cartographie ne sert PAS à activer toutes les audiences. Elle sert à :

1. **Prioriser** quelles 2-3 valent l'investissement maintenant
2. **Préparer** les autres pour activation future quand bandwidth dispo
3. **Détecter** les chevauchements pour bonifier les angles top-priorité

## Le résumé en 1 phrase à retenir

> Une audience c'est une **porte d'entrée** + un **niveau de granularité** + un **stade dans le funnel**. Ses chevauchements avec d'autres révèlent les angles porteurs. Tu en cartographies 7 mais tu en actives 2-3.

C'est le framework complet. Tu l'appliques systématiquement à n'importe quelle brand.

## Comment l'utiliser dans PhantomOS

- `/phantom {brand} audiences` rend l'arbre + chevauchements visuellement de tes audiences cartographiées
- `/phantom doctrine audiences` rend ce framework consultable à tout moment
- Skill `profile-audience` t'accompagne en posant les 4 questions au bon moment quand tu cartographies une nouvelle audience
- Schema profile.json supporte `meta.scope` (broad/segment/micro), `meta.parent_slug` (hiérarchie), `meta.overlap_with` (chevauchements)

## Cross-refs

- `docs/system/audience-cartography-doctrine.md` (spec rigoureuse système-side)
- `resources/schemas/profile.schema.json` (champs hiérarchie cartographie)
- `.claude/commands/phantom.md` (modes audiences + doctrine)
