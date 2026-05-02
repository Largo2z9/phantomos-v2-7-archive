# Getting Started

From an empty clone to a first skill run on your brand: about fifteen minutes of active attention. Add five to ten minutes if Claude Code is not yet installed.

## Prerequisites

- **Claude Code** installed and signed in: [claude.ai/code](https://claude.ai/code). A Claude Pro, Team, or Max subscription is required. Files stay on your machine; the agent calls the Anthropic API for inference.
- **This workspace** cloned or downloaded to your machine. Open the root folder in Claude Code, not a subfolder. The agent loads its contracts from the whole tree.
- **Your brand in mind**: the name, a one-line positioning, at least one product. If you have a public URL, drop it in the first message and the agent pre-fills from it.

No package to install. No JSON to touch.

## Context levels

PhantomOS reports workspace readiness on three levels. Each level unlocks a set of deliverables. Start at Level 1; enrich over time.

| Level | What the agent can produce at this level | What fills this level |
|---|---|---|
| **Level 1 · Base** | Generic copy, audit outlines, first-pass briefs calibrated on brand tone | Brand identity, hero product, primary audience |
| **Level 2 · Targeted** | Calibrated creative, differentiated positioning, offer-aware copy | Competitor set, detailed benefits, active offers, audience pain and psychology |
| **Level 3 · Operational** | Pacing decisions, scenario planning, P&L-aware recommendations | Financials, annual goals, seasonality, operational learnings |

When you run `validate`, the agent reports your current level and lists what blocks the next one. You can operate productively at Level 1 from day one.

## The five steps

### 1. Configure your first brand

> "Configure the brand [your brand name]"

The agent asks for a handful of fields (name, language, sector), creates the folder structure, and hands back control.

### 2. Fill in your brand info

> "Ingest this info on [your brand name]"

Paste whatever you have (a brief, a positioning doc, a product sheet, or raw text describing your brand). The agent classifies, structures, and files.

Recommended order: brand first, then products, then customers. Customers reference products.

### 3. Add products, customers, offers

> "Ingest this product for [your brand name]"
> "Ingest this customer profile for [your brand name]"
> "Ingest this offer for [product name]"

Paste raw. The agent does the rest. Add as many as you want, any time. No setup to redo.

### 4. Validate

> "Validate the workspace"

The agent checks integrity and reports your current context level (see table above). Level 1 complete means you are operational; Level 2 and 3 are enrichments.

### 5. Use your brand

After validation, the agent operates with your brand context on every request. Try:

> "Write a product description for [product]"
> "Generate 5 ad hooks for [audience]"
> "Draft a launch email for [brand]"

No re-briefing. The agent pulls context automatically from the entities you filled.

## What you can do next

- **At any moment**: type `?` or `skills` and the agent shows what's available in your current context.
- **Explore capabilities**: `capabilities.md` lists every skill with trigger phrases.
- **Go deeper**: `../vision/prisms.md` for what PhantomOS is; `../system/architecture.md` for architecture.

## When you need more than the default entities

The workspace ships with the default DTC paid entities per brand (brand, product, offer, audience, angle, learnings, strategy). If your work needs to capture something that does not fit (competitor ads over time, margin by channel, supplier lead times, customer cohorts, a quarterly report), just say so:

> *"Monitor my competitors' Meta ads over time"*
> *"Track my margin by channel"*
> *"Store this Q1 contribution report properly"*
> *"Segment my customers by acquisition cohort"*

The agent either routes you to an existing structure that already covers it, or builds a new data area in your brand. In both cases, zero schema work for you. Describe the intent or paste the data, the agent handles the rest.

## Receiving updates

When the template is updated, you pull the new version in your workspace folder, then say:

> *"Update workspace"*

The agent reads what changed, applies it, and reports. Your brand data, your captured learnings, your custom trackers, your connected credentials: all untouched. Only the template files and skills are refreshed. If a schema change requires a data migration, the agent walks you through it explicitly before touching anything.

## Common questions

**Do I ever open a JSON file?** No. The agent writes, you talk.

**How do I know my workspace is ready?** Run `validate`. Level 1 complete = operational.

**Can I add products or customers later?** Yes. `"Ingest this product [name] for [brand]"` works at any point.

**Why is there a `_TEMPLATE/` folder in brands?** It's the blank copied when a new brand is created. Do not modify.

**Where does the shared library come from?** You ingest it (proven methods, angles, templates) via `"Ingest this resource"`. Pre-filled knowledge packs by sector are planned.

## Limits to know

- **Single-operator.** One operator at a time per workspace. Multi-operator planned for a future iteration.
- **Local only.** Files live on your machine. To switch machines, clone and re-auth credentials.
