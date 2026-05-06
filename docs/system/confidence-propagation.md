# Confidence propagation discipline

> Doctrine canonique v2.37+. Comment la confidence se propage à travers les chains de skills PhantomOS. Empêche le data loss silencieux du signal d'incertitude.

## Le problème

PhantomOS skills produisent des outputs avec un score `confidence: 0.0-1.0`. Quand un skill consume l'output d'un skill précédent, sa propre output a une confidence. Sans règle canonique, chaque skill interprète différemment :
- Skill A : `output.confidence = input.confidence` (passthrough)
- Skill B : `output.confidence = min(input.confidence, my_local_confidence)` (defensive)
- Skill C : `output.confidence = input.confidence * my_local_confidence` (multiplicative)
- Skill D : ignore et écrit sa propre confidence locale (lossy)

Sur chain 4 skills à 0.6 chacun, output final affiché 0.6 mais réalité multiplicative 0.13. Opérateur trompé, atlas vivant pollué.

## Doctrine canonique

**Default obligatoire : `confidence_propagation: min`** (defensive, conservative).

`output.confidence = min(all_input_confidences, my_local_confidence)`

**Override autorisé** par skill via frontmatter `confidence_propagation:` enum :

| Mode | Formula | Quand |
|---|---|---|
| `min` (default) | `min(inputs ∪ {local})` | Defensive · default safe partout |
| `multiplicative` | `prod(inputs) * local` | Quand chaque step ajoute incertitude réelle independante |
| `weighted_avg` | `sum(w_i * c_i) / sum(w_i)` | Quand inputs ont importance variable (poids declared) |
| `passthrough` | `input.confidence` | Skill purement transformatif (pas d'inférence ajoutée) |
| `local_only` | `my_local_confidence` | Skill qui regenere from scratch (rare, doit justifier) |

## Audit trail · `confidence_chain[]`

Tout output skill v2.37+ doit porter un field `confidence_chain[]` :

```json
{
  "confidence": 0.42,
  "confidence_chain": [
    {"skill": "mine-voc", "level": "L3", "value": 0.6, "source": "verbatim_density_thin"},
    {"skill": "produce-paid-angles", "level": "L1", "value": 0.85, "source": "canon_lookup_ok"},
    {"skill": "analyze-copy", "level": "L3", "value": 0.7, "source": "no_test_data"},
    {"skill": "create-campaign", "level": "L1", "value": 0.9, "source": "config_complete"}
  ],
  "confidence_propagation": "min"
}
```

Audit trail visible. Opérateur peut tracer pourquoi confidence 0.42 (= min de la chain). Atlas vivant validations[] consume ce trail pour learning post-test.

## Frontmatter SKILL.md

Tout skill producer/orchestrator/curator (v2.37+) doit déclarer son mode :

```yaml
---
name: produce-paid-angles
type: producer
confidence_propagation: min
...
---
```

Si absent → default `min` appliqué automatiquement par runtime + warning logged.

## Operator surface

Opérateur ne voit JAMAIS `confidence_chain[]` brut. Surface traduite :

- confidence ≥ 0.8 → label `high confidence` (no flag visible)
- 0.5-0.8 → label `medium · 1 input thin` (1 ligne flag)
- < 0.5 → label `low · {weakest_input_skill} a flag {source}` (visible warning)

Mapping géré par skill `validate-output-coherence` ou orchestrator final de chain.

## Atlas vivant feed

Quand `learn-from-session` promote validations[] vers atlas canon copy, il consume `confidence_chain[]` pour pondérer la promotion :

- Si `min(chain) < 0.5` → promotion bloquée (signal trop faible, attendre confirmation tests)
- Si `min(chain) >= 0.7` + outcome `success` → promotion candidate
- Si chain courte (1-2 skills) + outcome `success` → promotion immediate
- Si chain longue (4+ skills) avec multiplicative mode → require ≥0.6 cumul pour eligibility

Empêche la pollution canon par signaux faibles cumulés.

## Cross-refs

- `docs/system/dependency-resolution-protocol.md` (DRGFP v2.38, où confidence est attribuée par level)
- `docs/system/atlas-canon-copy.md` (consume chain pour promotion gate)
- `resources/schemas/_shared/validation-state.json` v2.32 (composite status + confidence + confidence_source)
