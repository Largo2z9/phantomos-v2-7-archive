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

See `resources/schemas/angle.schema.json` (shipped v2.28.0). Two-pass enrichment:

- **Light pass** (auto, by `produce-paid-angles`): `angle_id`, `name`, `audience_slug`, `source`, `awareness_movement {in, out}`, `lineage {schwartz, hook, framework, archetype, pain, proof, cta}`, `formula {observation, tension, reframe, bridge}` summaries (one-line each), `meta.validation_status = hypothesis`.
- **Deep pass** (on demand, by `decompose-angle`): each `formula` component decomposed to atoms (`observation.phenomenon/source/sample_size`, `tension.state_actual/desired/blocked`, `reframe.perceptual_pivot/mechanism`, `bridge.spec_activated/benefit_served/promise`).

## Status

Skills `produce-paid-angles` writes light pass here. `decompose-angle` (to ship) enriches on demand. `learn-from-session` updates `meta.validation_status` when test outcomes are captured.
