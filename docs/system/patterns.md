# Patterns & Taxonomies

> Operational patterns and taxonomies the agent consults on demand: close variants, sharpening examples, context levels, model routing, skill taxonomy, skill philosophy.

---

## Close Variants

Post-scrape / post-setup close. The operator profile (inferred at setup-brand Step 1 or later) picks the variant. If mixed or ambiguous profile, propose the dominant variant with (d) "Other, tell me".

*Variant A — solo-brand-live* (one live brand with history, possible access, solo or small team):
> Context is about 60% set. Before we ship a deliverable, 3 chantiers to arbitrate:
> (a) Validate the inferred (audience, positioning) before we use it everywhere
> (b) Set up access to the platforms you use (2 min per platform, documented for reuse)
> (c) Surface your past operational learnings (campaigns run, rules learned)
> (d) Other, tell me

*Variant B — early-founder pre-launch* (no site, idea or MVP, no ads history):
> Context is set but your operational past is empty (normal, you're starting). 3 chantiers to arbitrate:
> (a) Structure your offer and value proposition before touching acquisition
> (b) Dig into your target audience beyond intuition (concrete pains, objections)
> (c) Test messaging on a sample before scaling
> (d) Other, tell me

*Variant C — creator-led* (monetized personal audience, mix organic plus paid, existing content archive):
> Context is set from the site. But your real signals are in your content archive. 3 chantiers to arbitrate:
> (a) File your top 10 posts and your DMs (your real audience study)
> (b) Map past collabs and what converted (if any)
> (c) Set up organic vs paid tracking so I reason on the right signals
> (d) Other, tell me

*Variant D — agency-portfolio* (3+ client brands, reproducibility scope, no personal access):
> You arrive with {N} brands. Before we dive into one, 3 chantiers to arbitrate:
> (a) Structure the multi-brand approach (prioritize which brand to start with, why)
> (b) Access request script for your clients (reusable, templatable cross-brand)
> (c) Identify the skill that will run on all 3 brands and formalize it fast
> (d) Other, tell me

**Profile detection**: first source = `operator.profile` field filled at setup-brand Step 1. Second source = conversational signals (mentions of "my clients" vs "my brand", number of brands, live site presence, business language). If ambiguous, ask ONE targeted sharpening question (thread + sharpening rule).

---

## Sharpening Examples

When the operator gives a **dense signal** in their answer, add ONE targeted sharpening question on top of the thread question. Never two. Sharpening personalizes the context without turning the conversation into a questionnaire.

Examples of dense signals that deserve sharpening:
- *"I manage 15 brands at an agency"*, sharpening: *"mostly scaling brands or one-off audits?"* (clarifies operating mode)
- *"I run DS, 8 stores/month"*, sharpening: *"how many days before you kill when it doesn't scale?"* (clarifies pace)
- *"I'm a creator, 85k IG mental health"*, sharpening: *"do you convert mostly organic direct or via collabs?"* (clarifies acquisition mode)
- *"Ex-marketer, launching my brand"*, sharpening: *"do you have an active ads budget or starting 100% organic?"* (clarifies stage)

**Never 2 sharpening questions in a row.** If the operator answered both (thread + sharpening), next turn = pure thread only. No questionnaire spiral.

---

## Context Levels

Progressive enrichment of the brand Context DB. Agents can operate at Level 1, deepen at Level 2, pilot at Level 3.

- **Level 1** — brand identity + hero product + primary audience → agents can work
- **Level 2** — benefit chains + competitors + offers + tone details → targeted content
- **Level 3** — financials + strategy + seasonality + learnings → operational piloting

---

## Model Routing

PhantomOS skills declare a `recommended_model` and `subagent_safe` flag in their frontmatter. The agent reads both at skill trigger and decides whether to launch via Task tool (subagent) or inline.

### Decision rule

- If `subagent_safe: true` AND `recommended_model` differs from session model → **launch via Task tool with `model: {recommended}`**. Fresh context, parallel execution, cost/latency gain.
- Otherwise → **run inline with session model**. Skill needs full conversational context or model override impractical.

### Full matrix

| Skill | Model | Subagent | Rationale |
|---|---|---|---|
| `validate-resources` | haiku | ✅ | Deterministic JSON integrity checks, zero business reasoning |
| `query-context` | haiku | ✅ | Read-only lookup in Context DB, deterministic |
| `capture-learning` | haiku | ✅ | Simple classification + routing |
| `snapshot-brand` | sonnet | ✅ | Brand inference from URL, parallelizable (setup-brand Step 0) |
| `ingest-resource` | sonnet | ✅ | Doc classification + routing to right entity |
| `audit-meta-setup` | sonnet | ✅ | Structured business audit on declared account |
| `promote-learning` | sonnet | ✅ | Cross-brand learning promotion, deterministic matching |
| `migrate-workspace` | sonnet | ✅ | Schema migration, documented transformations |
| `setup-brand` | sonnet | ❌ | Interactive guide, needs full conversational context |
| `learn-from-session` | sonnet | ❌ | Full session scan, needs main conversation buffer |
| `build-agent` | opus | ❌ | Custom skill design, needs operator dialogue + iteration |

### Rationale for flagging `subagent_safe: false`

Three skills stay inline on purpose:
- **`setup-brand`** conducts the onboarding dialogue itself. A subagent would break the conversational thread.
- **`learn-from-session`** scans the entire session buffer to extract learnings. A subagent has a fresh context, it would miss 90% of the captured signal.
- **`build-agent`** designs a new skill through back-and-forth with the operator (what it does, which fields it reads/writes, edge cases). Not parallelizable.

### Expected gain on a typical workflow

setup-brand (Sonnet, inline) → snapshot-brand (Sonnet, subagent) → validate (Haiku, subagent) → ingest (Sonnet, subagent) → query (Haiku, subagent).

- **Cost**: ~40% reduction vs all-Sonnet. Haiku 4.5 is ~4x cheaper on skills where it suffices.
- **Latency**: ~30% faster on Haiku skills (~3x faster inference + parallel subagent).
- **Quality**: zero degradation on deterministic skills. Haiku 4.5 handles validate/query/capture natively.

### Prerequisites to activate in production

- Verify Claude Code's Task tool accepts the `model:` parameter at spawn (tested case-by-case).
- Confirm subagent read/write permissions on the workspace are scoped correctly.
- Benchmark empirically on a real session (e.g. `validate-resources` in Haiku vs Sonnet) before locking in the config.

### How skills declare this

In each `.skills/skills/{name}/SKILL.md` frontmatter:

```yaml
name: {skill-name}
recommended_model: haiku | sonnet | opus
permissions:
  reads: [...]
  writes: [...]
  mode: direct | proposed | none
  subagent_safe: true | false
```

The `recommended_model` + `subagent_safe` pair is the contract. The agent **NEVER** overrides without explicit reason.

---

## Skill Taxonomy

**CRITICAL:** every skill in `.skills/skills/` **YOU MUST** declare a `type:` field in its frontmatter. Exactly one of six typologies below. Enforced by `validate-resources`.

### The 6 typologies

| Typology | Role | Binary test (if YES → this type) | Actual examples | Default model | Default `subagent_safe` | Default write mode |
|---|---|---|---|---|---|---|
| **Producer** | Builds a deliverable directly consumed by a human (operator, client, campaign output) | Is the output meant to be read/used by a human as-is, with no further skill in the pipeline? | `snapshot-brand`, `audit-meta-setup` | `sonnet` | `true` | `proposed` |
| **Curator** | Maintains or queries the workspace state, invoked **in pipeline by other skills** (backend) | Is the skill invoked primarily by other skills as part of a larger flow, not directly by the operator? | `query-context`, `validate-resources`, `ingest-resource`, `migrate-workspace`, `promote-learning` | `haiku` | `true` | `direct` or `none` |
| **Capturer** | Turns the current conversation/session into persistent memory | Does the skill scan the current conversation to extract persistable knowledge (learnings, decisions, preferences)? | `capture-learning`, `learn-from-session` | `sonnet` | `false` (needs full session context) | `proposed` |
| **Orchestrator** | Chains N ≥ 2 distinct named skills to reach one operator goal | Does the skill literally call 2+ other named skills as sub-steps (via Task tool or invocation)? | `setup-brand` | `sonnet` | `false` (it is the pilot) | indirect (via sub-skills) |
| **Navigator** | Reduces operator cognitive friction, invoked **directly by the operator** (frontend) | Is the skill invoked directly by the operator to orient / understand / get status, with no external deliverable? | (none yet, coming: `brief-day`, `resume-session`, `show-progress`, `portfolio-overview`, `explain-this`) | `haiku` | `true` | `none` (read-only) |
| **Builder** | Modifies PhantomOS itself (meta-OS) | Does the skill write into `.skills/` or modify OS rules? | `build-agent` | `opus` | `false` | `proposed` |

### Primary disambiguation rule

**Curator vs Navigator** — the sharpest frontier. Decide by **who invokes the skill**, not who consumes its output:
- Invoked by another skill in a pipeline (agent-to-agent) → **Curator**
- Invoked by the operator directly for orientation → **Navigator**

`query-context` is a Curator because `setup-brand` and `ingest-resource` invoke it internally; the operator rarely calls it by name. `brief-day` would be a Navigator because the operator triggers it explicitly ("où j'en suis ?" / "démarre ma session").

### Secondary disambiguation rule

**Orchestrator vs skill-with-steps** — having numbered internal Steps does **NOT** make a skill an Orchestrator. The test is: *does it literally call N ≥ 2 named skills as sub-steps?*

`audit-meta-setup` has Steps 1A/1B but calls no other skill → it is a Producer with internal structure. `setup-brand` calls `snapshot-brand` (Step 0) + chains Step 1-5 logic → Orchestrator.

### Override rule

Contract defaults (model, `subagent_safe`, write mode) are **defaults**, not law. A skill **MAY** override them in its frontmatter when its specifics require it, provided the override includes a one-line justification as a YAML comment. Example:

```yaml
type: curator
recommended_model: sonnet   # override: dense document classification requires reasoning, not just lookup
subagent_safe: true
```

`validate-resources` flags an override without justification comment as a warning.

### Enforcement

- **`validate-resources`** **YOU MUST** refuse any `SKILL.md` where `type` is missing, `null`, or not one of the 6 enum values. Blocking error.
- **`build-agent`** **YOU MUST** ask for the type during skill generation, apply the binary test, and refuse to generate a skill if the operator's chosen type fails the test.
- At every batch flush, `learn-from-session` scans `.skills/skills/` for skills missing `type` and flags in the recap.

### What this taxonomy drives

- **Model routing** (defaults in the table above, see also `§ Model Routing`)
- **Subagent spawn decision** (`subagent_safe` default per type)
- **Permissions baseline** (reads/writes/mode default per type)
- **Skill table in CLAUDE.md** displays type per skill
- **Operator shortcut** (`?` / `help`) surfaces Navigators in priority for "what can I do right now"

### What this taxonomy does NOT do

- It is **not exposed to the operator in daily use**. Internal routing concern. The operator never needs to know `brief-day` is a Navigator.
- It does **not replace** the `_proposals` / `_validated` lifecycle for write actions. Orthogonal concerns.

---

## Skill Philosophy

**CRITICAL:** every skill embodies **codified expertise**, not improvised action. This is the non-negotiable core of PhantomOS.

### The principle

A skill is not a wrapper around "ask the LLM to do X". A skill incarnates the **reasoning of a senior domain expert**: their framework, their key variables, their matrices, their thresholds, their formulas. The agent replicates the rigor of an artisan, it never improvises domain reasoning.

### Complexity gate — apply only when it matters

**CRITICAL:** this expert-methodology discipline applies to **complex tasks only**. Over-engineering a simple task is a failure mode as bad as under-engineering a complex one.

**Simple tasks** (bypass expert dissection, skill léger) :
- Deterministic lookup, filter, transformation (e.g. *"list active brands", "show pending validations", "rename a field"*)
- No qualitative arbitrage, no domain thresholds, output is obvious
- No matrix, formula, or named framework needed
- Typology usually Curator or Navigator

**Complex tasks** (full expert dissection mandatory) :
- Output informs business decisions (audit, brief, diagnostic, scoring)
- A senior practitioner would apply a named framework (AIDA, RFM, DMARC, JTBD, STPD, etc.)
- Results vary by variables / thresholds / context, not all equal
- Domain literature exists in the real world
- Typology usually Producer or Orchestrator

**Binary test before dissection** : *"Would a senior expert in this domain apply a specific framework or matrix to do this, or is it pure mechanical execution?"* Framework → complex, go expert. Mechanical → simple, skill léger.

Examples :
- **Simple** : `list-brands-by-stage`, `show-progress`, `rename-audience-slug` → 5-10 line skill, no framework reference needed
- **Complex** : `audit-klaviyo-deliverability`, `score-product-fit`, `generate-hook-brief` → full expert dissection, methodology codified in `resources/` first if missing

### What this means in practice (complex tasks)

Before generating any skill, **YOU MUST** identify:

- **Canonical expert persona** — who incarnates this task at senior level in the real world? (e.g. senior media buyer for Meta audit, email deliverability engineer for Klaviyo audit, direct response copywriter for creative brief)
- **Expert's reasoning framework** — which methodology they apply (AIDA, RFM, DMARC, JTBD, STPD, etc.)
- **Key variables they compute** — thresholds, metrics, signals the expert tracks
- **Structuring matrix** — 2D or 3D grid that encodes their decisions (e.g. audience awareness × pain intensity × angle type for hooks ; IP × domain × list freshness × warmup phase for deliverability)
- **Formulas / heuristics** — numeric or decisional, if applicable

### Where this expertise lives

- **`resources/frameworks/*.md`** — methodology artifacts (AIDA applied to DTC, RFM segmentation, email deliverability rules, creative hook framework, etc.)
- **`resources/catalogues/*.json`** — enumerated expert-curated lists (tested angles, proven mechanics, rejected patterns, etc.)
- **`resources/quality-specs/*.md`** — binary criteria grids an expert uses to validate an output (hook quality 5 criteria, email deliverability checklist, brief completeness, etc.)
- **`resources/conventions/*.json`** — platform-specific expert knowledge (API rate limits, scopes, pitfalls, anti-ban rules)
- **`resources/sops/*.md`** — step-by-step expert procedures when the order matters

### Gate expertise — NEVER generate without codified methodology

If the required expert methodology is **not yet codified** in any of the locations above, **STOP** generation (Gate doc extended). Build the methodology artifact first via `ingest-resource` + WebFetch on authoritative sources. Only then generate the skill that consumes it.

**YOU MUST NEVER** let the LLM improvise expert reasoning inside the skill SKILL.md itself. The skill loads and applies the codified methodology ; it does not re-invent it each run.

### The compound effect

Each framework codified once is reused by every future skill in that domain. One deliverability framework built for Klaviyo audit is reused by Mailchimp audit, Attentive audit, any future email platform. One RFM matrix codified once is reused by every segmentation skill. This is what makes PhantomOS scale : codified expertise compounds, improvised reasoning doesn't.

### Operator-facing cartography rule

When presenting the architecture of a skill to the operator, **YOU MUST** translate this expert methodology into operator value :

- ❌ *"Missing: convention Klaviyo, framework deliverability, framework RFM"*
- ✅ *"The expert way I'll reason : like an email deliverability engineer, applying identity rules (SPF/DKIM/DMARC), warm-up curves, bounce and complaint thresholds, a matrix IP × domain × list × phase. Missing in your workspace today — I'll build these references first (1h), then run the audit."*

The operator sees *how the expert thinks*, not the internal filename of the framework. See CLAUDE.md § Operator contract for the jargon translation rule.

## Capture & Build routing

The main agent routes operator intent to the right skill using three binary tests. Applied in order, they disambiguate the four build/capture skills that occupy adjacent registers.

### Decision matrix

| Operator intent | Skill | Output target | Example |
|---|---|---|---|
| A single fact, rule, or observation to remember | `capture-learning` | Append one entry to `brands/{slug}/learnings.json` | *"retiens que le pixel Meta nécessite delay=0 en iOS 17"* |
| Persist the full session's decisions and discoveries | `learn-from-session` | Batch update `session-log.md` + `project-state.md` of the active project | *"save session"* at the end of a 2h work block |
| A new concept that will recur, evolve, be traversed | `scaffold-extension` (custom entity mode) | New `brands/{slug}/custom/{type}/` with schema + README | *"je veux tracker les prix concurrents au fil du temps"* |
| New fields on an existing core entity | `scaffold-extension` (sidecar mode) | New `brands/{slug}/{entity}.extensions.json` | *"ajoute contribution margin par channel à ma brand"* |
| A new multi-step workflow to automate | `build-agent` | New `.skills/skills/{name}/SKILL.md` with pipeline | *"construis un agent reporting Klaviyo mensuel"* |
| A brand-level learning that generalizes cross-brand | `promote-learning` | Move entry from `brands/{slug}/learnings.json` to `resources/{type}/` | *"ce workaround Meta marche pour toutes mes brands"* |

### Three binary tests to disambiguate

Apply in order. Stop at the first definitive answer.

1. **Capture or construct?**
   - Capture an existing fact → `capture-learning` (single) or `learn-from-session` (batch).
   - Construct a new structure or behavior → `scaffold-extension` or `build-agent`.

2. **(If capture) Single fact or whole session?**
   - Single fact → `capture-learning`.
   - Full session → `learn-from-session`.

3. **(If construct) Data structure or skill behavior?**
   - Data that will be stored, queried, traversed → `scaffold-extension`.
   - Behavior that will be automated → `build-agent`.

### Overlap zones clarified

- `learn-from-session` writes to **project docs** (session-log, project-state). Never writes to brand entities or extensions.
- `capture-learning` writes to **one brand's learnings.json**. Stays within core. Never creates new schemas.
- `scaffold-extension` writes to **brand custom entities or sidecars** (optionally stub skill). Only when genuinely new — the five-dimension gate in Phase 2 routes to existing structures if coverage exists.
- `build-agent` writes to **`.skills/skills/`** (generates new skills). Delegates to `scaffold-extension` when the intent is a simple extension pattern.

### The orchestration gate

Every build decision (capture-learning excepted — it's always safe, append-only, trivial) passes through the main agent's orchestration gate first. Before invoking `scaffold-extension` or `build-agent`, the main agent applies the five-dimension check (core entities / active-brand sidecars / active-brand custom entities / sibling-brand custom entities / shared resources). If any matches, routes to existing. Build only when genuinely new.

Full orchestration rule → root `CLAUDE.md § Orchestration gate`.
