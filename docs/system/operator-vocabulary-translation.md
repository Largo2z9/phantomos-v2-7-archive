# Operator vocabulary translation

> Mapping canonique vocabulaire interne -> vocabulaire opérateur. Application stricte sur tout output operator-facing v2.37+. Violation = bug.

## Règle absolue

CLAUDE.md root déclare : "Translate PhantomOS vocabulary into operator value when mapping architecture, prerequisites, or expert methodology. NEVER expose internal names (`convention`, `framework`, `SOP`, `quality-spec`, `catalogue`, `entity`, `field`, `schema`) in architectural cartography."

Cette règle s'étend aux concepts canon : atlas, canon, validations, fiches, couches, archetype, etc. Aucun jargon interne ne doit apparaître dans une vue, un message, ou un output destiné à l'opérateur.

## Mapping canonique

| Interne (jargon) | Operator-facing (FR) | Operator-facing (EN) |
|---|---|---|
| atlas brand | matière brand · cartographie | brand cartography · brand data |
| atlas canon copy | bibliothèque copywriting partagée | shared copy library |
| atlas vivant | historique de ce qui a marché | track record · what worked |
| validations[] | tests passés · résultats observés | past tests · observed results |
| canon-tool | outil de référence | reference template |
| fiches (canon) | entrées · références | entries · references |
| couches (11) | catégories · familles | categories · families |
| archetype voix | style de parole | speaking style |
| hook (canon) | accroche · début | hook · opener |
| framework (canon) | structure · gabarit | structure · template |
| _field_types | source · provenance | source · origin |
| schema | structure · format | structure · format |
| entity | élément · bloc | item · block |
| confidence_chain | parcours certitude | confidence trail |
| isolation_scope brand_only | privé à cette brand | this brand only |
| validation_status hypothesis | non testé · à valider | not tested · to validate |
| L1/L2/L3 fallback | automatique · à toi · partiel | auto · your call · partial |
| prerequisites | pré-requis · dépendances | prerequisites · dependencies |

## Output policy

Tout texte opérateur-facing :
1. Pre-render filter · scan output pour tokens jargon de la table mapping
2. Substitute par equivalent operator-facing
3. Si pas d'equivalent disponible -> reformuler ou virer la mention
4. Si jargon **doit** apparaître (ex référence path absolu code) -> encadrer en backtick code · signal explicite "tech detail"

## Examples

**Avant (v2.36 actuel `/phantom kara atlas`)** :
```
ATLAS VIVANT (validations[] cumulées)
  hooks canon          0
  frameworks canon     0
  archetypes canon     0
```

**Après (v2.37 conforme translation)** :
```
HISTORIQUE BRAND
  Accroches qui ont marché          0
  Structures testées                0
  Styles de parole validés          0
```

Substance préservée. Jargon retiré. Operator junior comprend sans doc.

## Enforcement

- `validate-resources` v2.37+ scan SKILL.md outputs prose pour jargon leak (lint rule)
- Scripts comme `phantom.md` modes templates passent filter pre-output
- learn-from-session Trigger 8 daemon flag jargon detected post-skill completion

## Cross-refs

- CLAUDE.md root § Operator contract (règle no_jargon_to_operator)
- `lexicon.md` (vocabulaire interne canon · NE doit PAS leak operator)
- Mémoire user `feedback_no_jargon_to_operator.md`
