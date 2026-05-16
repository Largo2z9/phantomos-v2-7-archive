# brands/

Your brands. One per subfolder, slug in kebab-case.

## Organization

- **`{slug}/`**. An active brand. Contains its identity, products, customers, offers, learnings, strategy.
- **`_TEMPLATE/`**. Template copied by `setup-brand` to create a new brand. Do not edit.
- **`_EXAMPLE/`**. Brand pédagogique Stepprs (cas canonique PhantomOS · marque réelle foot care DTC · vitrine canon doctrine + skills). Pour découvrir comment PhantomOS structure le savoir métier, lance `/breakdown stepprs principe` (parcours 13 chapitres · ~30 min lecture · drill direct possible). Cf `_EXAMPLE/README.md` pour ordre de lecture suggéré + mapping doctrine.
- **`_ARCHIVE/`**. Archived brands, out of active scope.

Folders prefixed with `_` are ignored by the agent when auto-detecting brands.

## Brand structure

```
{slug}/
├── CLAUDE.md              ← brand-specific rules (tone, audience, constraints)
├── brand.json             ← identity, positioning, financials, contacts
├── products/{slug}/       ← specs + offers per product
├── audiences/{slug}/      ← detailed audiences (segments, pains, objections)
├── learnings.json         ← learned rules (append-only)
├── strategy.json          ← goals, current month focus
├── pending-validations.md ← ambient buffer (inferred gates, access, learnings to surface)
├── todos.md               ← tasks related to this brand
├── config.json            ← operator preferences for this brand
├── credentials.env        ← platform tokens (gitignored)
├── status.json            ← setup progress state
├── session-state.md       ← inter-session relay (auto-maintained)
└── sources/               ← raw docs ingested
```

## Rule

The operator never touches these files. They talk to the agent, which writes.
