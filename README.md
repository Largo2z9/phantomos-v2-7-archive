# PhantomOS

PhantomOS is a workspace where everything about your brand lives in one place and an agent operates on it every session. One workspace per brand, one Agent Contract per workspace. You tell the system something once and it keeps it, so you stop re-briefing the same brand, tone, audience, and offers every time you open a new chat.

Built for operators who run their own business. Not a chatbot with memory. Your brand context lives in this workspace, read by your agent before every response. Corrections you make along the way also become rules applied next time, which compounds over sessions. But the first-day value is simpler than that: you stop restarting from zero.

**Best fit.** Solo operators with a portfolio of 1 to 8 brands. Senior consultants and service businesses. DTC operators past month 6. Coaches and experts who productize knowledge. **Conditional fit.** Early-stage founders between month 3 and 12, and small teams of 2 to 4 operators. **Not fit today.** Enterprise agencies with 5+ people on shared client accounts, pre-traction founders in the first two months, and performance creators focused on volume and distribution. Full honest audit in [`docs/product/fit.md`](docs/product/fit.md).

## Requirements

PhantomOS runs inside [Claude Code](https://claude.ai/code), the Anthropic CLI (not the web chat). Not ChatGPT, not Cursor — the agent needs filesystem access to read and write the workspace without intermediaries, and CLAUDE.md auto-injection is what loads its contracts. A Claude Pro, Team, or Max subscription is required; files stay on your machine, the agent calls the Anthropic API for inference.

## First steps

From an empty clone to a first skill run: about fifteen minutes.

1. **Open the workspace in Claude Code.** Open the root folder, not a subfolder — the agent needs the whole tree to load its contracts.
2. **Say hi.** On first run, the agent detects no brand is configured and starts onboarding. It asks your comfort level with AI and calibrates from there.
3. **Drop a brand URL.** The agent scans for 3 to 5 minutes, pre-fills your brand at roughly 60% of Level 1 completeness, hands back for validation.

No package to install, no config to write. Everything ships in this repo.

Nothing here is one-shot. You can stop mid-setup and come back tomorrow — everything you've told the agent stays. The workspace grows at your pace, not in a single sitting.

## What lives here

- **`CLAUDE.md`** — root Agent Contract. Auto-loaded every session.
- **`WELCOME.md`** — first-run onboarding script. Agent-facing, read once before your first brand exists.
- **`brands/`** — one folder per brand. Six versioned entities each: brand, product, offer, audience, learnings, strategy.
- **`resources/`** — shared library across brands: frameworks, angles, platform conventions, templates.
- **`.skills/skills/`** — executable capabilities the agent triggers on context.
- **`docs/`** — product, vision, and system docs. Start at `docs/README.md`.
- **`CHANGELOG.md`** — version history.

External tools (Meta, Shopify, Klaviyo, Google Calendar, Notion, ClickUp) connect on demand when a skill needs them. No continuous sync.

## The one rule

You never touch a file. You talk, the agent writes. If something is wrong, say *"fix X on my brand"* — the agent records the change and keeps a trace.

## Going further

- **To use PhantomOS** → `docs/product/getting-started.md`
- **To understand what it is** → `docs/vision/prisms.md`
- **To extend it** → `docs/system/README.md`
- At any moment in a session, type `?` or `skills` — the agent pulls the right section from `docs/product/capabilities.md`.
