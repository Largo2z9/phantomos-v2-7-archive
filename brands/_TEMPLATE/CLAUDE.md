# Brand: {brand-name}

> Auto-loaded when working in this brand folder.
> Note. This file complements the parent CLAUDE.md (workspace root). Always open the workspace from the root folder, never open a brand folder directly. Opening just the brand folder loses the OS, skills, and all behavioral rules.
> Shared resources → `../../resources/` (reference by ID, never duplicate).
> Resource discovery → `../../index.json`.

## Ecosystem

Platforms this brand operates on. The agent uses these identifiers for on-demand API calls when the operator asks for data (campaigns, orders, emails, analytics).

| Platform | Account / Store | Status |
|----------|----------------|--------|
| Meta Ads | `act_XXXXXXXXX` | — |
| Shopify | `{slug}.myshopify.com` | — |
| Google Ads | `XXX-XXX-XXXX` | — |
| GA4 | `G-XXXXXXXXXX` | — |
| Klaviyo | — | — |

API tokens and secrets → `credentials.env` (gitignored, never in context).
Shared workspace tokens → `../../credentials_shared.env` (gitignored).

**Credential loading** — before any API call:
```python
from dotenv import load_dotenv; import os
load_dotenv(os.path.join(BRAND_PATH, 'credentials.env'))
# For workspace tools (Slack, ClickUp, Google Suite):
load_dotenv(os.path.join(WORKSPACE_ROOT, 'credentials_shared.env'))
```
Never display tokens in output. Install deps: `pip install requests python-dotenv --break-system-packages -q`

## Data Access

- **Sources** : `sources/` — raw files (briefs, PDFs, screenshots, exports). Never auto-loaded. No impact on context budget.

## Workspace State

- **Status**: `status.json` — completeness, freshness, flags (auto-maintained)
- **Todos**: `todos.md` — tasks, backlog, flags
- **Config**: `config.json` — brand-specific customization
- **Session relay**: `session-state.md` — rolling activity log, auto-maintained on every write (no manual rotation)
- **Learnings**: `learnings.json` — append-only operational facts (API workarounds, test results, compliance rules)

## Context DB — 6 Entities

| Entity | File | Status |
|--------|------|--------|
| Brand | `brand.json` | empty |
| Products | `products/{slug}/spec.json` | — |
| Offers | `products/{slug}/offers.json` | — |
| Audiences | `audiences/{slug}/profile.json` | — |
| Learnings | `learnings.json` | empty |
| Strategy | `strategy.json` | empty |

### Context Levels

**Level 1. MVP** (agents can work):
- [ ] `brand.json`. name, positioning, tone of voice
- [ ] `products/{product}/spec.json`. hero product (name, price, benefits, problems_solved)
- [ ] `audiences/{audience}/profile.json`. primary audience (who, pain points)

**Level 2. Enriched** (targeted content):
- [ ] Benefit/pain chains in products and audiences
- [ ] Competitors (>=1) in brand.json
- [ ] Offers (>=1) in products/{product}/offers.json
- [ ] Tone details (banned_words, frequent_words)

**Level 3. Operational** (after first sales):
- [ ] Financials (AOV, revenue, margins)
- [ ] Strategy (goals, targets, focus)
- [ ] Seasonality

## How to Reference Resources

- Catalogue entries: `{PREFIX}-{NN}` (e.g. `ANG-01`, `FMT-03`)
- Other resources: `id` field from `../../index.json`
- To find: read `../../index.json` → filter by `type` and `domain`
- Cross-refs in context files: use `ref` fields pointing to IDs in spec.json or index.json

## Field Types

All JSON files contain `_field_types`. See parent CLAUDE.md and docs/system/architecture.md for details. Agents must respect types: never fill derived fields manually, never inject decisions into any field.
