# Angles

Angle definitions for this brand. Each angle = one file `{slug}/angle.json`.

An angle is an attack axis (Observation, Tension, Reframe, Bridge) with a typed statement, optional intensity levers (Big Idea, Mechanism Reveal, Stake Raising), and links to compatible audiences and creative mechanics.

Angles are stored independently of audiences and crossed at production time. The same angle can serve multiple audiences with different mechanics.

## Structure

```
angles/
├── README.md
├── {angle-slug}/
│   └── angle.json
└── ...
```

## Schema

See `resources/schemas/angle.schema.json` for the full schema (when shipped).

## Status

Stubbed for V1. Skill `produce-paid-angles` writes here when generating new angles. Validation via `validate-resources`.
