# Lexicon

Canonical vocabulary of PhantomOS. Every term here passes three tests: it recurs three or more times across the project, it is shorter and more precise than its paraphrase, and it remains valid six months out. Once in the canon, a term is used across the project without redefinition.

Non-canonical terms still appear in prose when they clarify something in context. They just do not live here.

## Macro — the agentic economy

- **Agent economy** — the emerging economic layer where agents operate work previously done by humans. Macro frame of the shift PhantomOS addresses.
- **Agent-as-a-Service (AaaS)** — economic category where the agent replaces the human as the operator. Opposite of SaaS. Full context in `docs/vision/manifesto.md § 1`.
- **Services-as-a-Software** — the measured shift from human-delivered services to software-delivered work (HFS: $1.5T by 2035).
- **Allocation Economy** — Dan Shipper's reframe: knowledge workers become managers who allocate work to systems. Taste, decomposition, and validation gain value.

## Method — the encoding discipline

- **Encoding** — structuring knowledge into atomic, interconnected, addressable nodes an agent can operate on. Opposite of logging.
- **Logging** — write-only documentation, read once then forgotten. Produces documentation debt. What most AI transformation projects do while calling it encoding.
- **Context Layering** — the operational discipline of building, layer by layer, the environment in which an agent reasons. PhantomOS is Context Layering turned into a running workspace. Full context in `docs/vision/manifesto.md § 5`.
- **Decision Trace** — a structured entry capturing the reasoning behind a correction (context, rule, justification, conditions of application). Not a note.
- **Skill Graph** — a network of atomic, interconnected Decision Traces an agent navigates by index and description, not by full reading. Deterministic retrieval, not probabilistic.
- **Feedback Loop** — the cycle where the agent proposes, the operator corrects, the Decision Trace logs, and the graph densifies. Runs until corrections grow rare.
- **Process moat** — the defensible advantage is the continuous capture discipline, not the graph itself. An exfiltrated graph is a snapshot; the process keeps compounding.
- **Capture discipline** — the installed habit of logging Decision Traces continuously, treated as a reflex rather than an occasional task. What compounds into the process moat.
- **Parametric composition** — the core generation pattern: a proven method is decomposed into atomic variables (mechanics, angles, audiences, proof types, tones, formats), stored as curated banks in `resources/registries/` and cross-referenced through matrices in `resources/routing/`, then traversed by a workflow that composes output by picking coordinates. Produces high-variety, high-coherence output at volume because each atom is already curated and each combination is grounded rather than improvised. Concrete example: a creative generation workflow pulls `creative-mechanics-registry × angle-registry × audience profile × proof-registry` to produce a hundred coherent ad variants in minutes, each variant legitimately different from the others because the coordinates differ.
- **Extension** — any operator-built addition on top of the core workspace — custom entities, sidecar schemas, custom skills, external pipelines. Follows conventions (declared schema, index registration, README) to stay interoperable. Full pattern in `docs/system/extending.md`.
- **Custom entity** — a new data type scoped per brand, living under `brands/{slug}/custom/{entity_type}/`. Discovered via convention by `query-context`. Must declare a schema following canon.
- **Sidecar schema** — append-only extension fields on a core entity without modifying the core schema. File sits next to its target (`brand.extensions.json` next to `brand.json`). Declares `_extends: "brand"` pointing to the core entity it augments. Strictly **append-only** with respect to the core fields: adds new fields, never overrides or removes. The core stays stable; the operator layers on top. Agent reads core + sidecar as one merged view at runtime.
- **Core namespace vs custom namespace** — shipped skills live at `.skills/skills/{name}/` (flat, maintained by template releases). Operator-built skills live at `.skills/skills/custom/{name}/` (local to the workspace, untouched by template upgrades). Same convention applies to resources: shipped registries under `resources/registries/` vs operator-built custom entities under `brands/{slug}/custom/{type}/`.
- **Promotion threshold** — heuristic (not hard law) for when a custom extension should be considered for promotion to a vertical pack or to the core: the same pattern appearing in three or more brands, with schemas convergent enough to unify. Final decision is manual — the heuristic flags the candidate, the operator or maintainer judges.

## Workspace — the product

- **PhantomOS** — the product: an agentic workspace OS where an agent operates on brands under a structured contract.
- **Workspace** — the root folder that holds everything an operator needs for their brands. One workspace per operator.
- **Brand** — a subject the operator works on within a workspace. One brand folder per brand.
- **Template** — the blank workspace shipped in this repository, cloned or downloaded by a new operator.
- **Instance** — a deployed workspace running for a specific operator. Diverges from the template over time.
- **Context DB** — the six versioned entities per brand: `brand`, `product spec`, `offers`, `audience profile`, `learnings`, `strategy`. Mutated only through `write_to_context()`.
- **Brand state** — the live state of a brand across its Context DB and OS files. Distinct from any single `brand.json` snapshot.

## Contracts — the governance

- **Agent Contract** — files named `CLAUDE.md`, auto-injected into the system prompt at session start. Not memory, not documentation — rules the agent executes on. Full spec in `docs/system/agent-contracts.md`.
- **Operator** — the human running a PhantomOS workspace. Canonical label across all system docs.
- **Operator-grade** — the quality level the operator would hold themselves to. Used as a bar in skill outputs and deliverables.
- **Write contract** / **mutation gate** — the rule that every mutation to the Context DB passes through `write_to_context()` with source, confidence, and mode. No silent JSON editing.
- **Append-only discipline** — the rule that certain artifacts (session logs, learnings, Decision Traces) only grow through addition. Past entries are never modified or deleted.
- **Session continuity** — the property that a session resumes cleanly after interruption. Backed by `session-state.md` and the resume-session skill.

## Agents, skills, workflows

- **Agent** — the Claude instance operating on the workspace. Reads the Agent Contract at session start, triggers skills on operator signal, writes back through the mutation gate. A session has one main agent; sub-agents can be spawned for parallel work or model-specific tasks.
- **Sub-agent** — a secondary Claude instance launched by the main agent via the Task tool. Used for asynchronous execution (background scrape), long-running operations, or running a skill on a different model than the session. Declared via `subagent_safe: true` in the skill frontmatter.
- **Skill** — a pre-written executable capability living in `.skills/skills/{name}/SKILL.md`. Single-purpose, triggered by the agent when the operator's request matches the skill's declared triggers.
- **Skill taxonomy** — the six typologies every skill declares in its frontmatter: `producer`, `curator`, `capturer`, `orchestrator`, `navigator`, `builder`. Full spec in `docs/system/patterns.md § Skill Taxonomy`.
- **Orchestrator** — a skill that chains multiple other skills to accomplish a multi-step outcome. Example: `onboard-brand` chains `setup-brand`, `snapshot-brand`, `ingest-resource`, `validate-resources`.
- **Workflow** — a pattern of skills, orchestrators, agents, and sub-agents composed to deliver a specific operator outcome at scale (mass creative generation, portfolio-wide reporting, multi-brand Klaviyo flow design). Codified as an orchestrator skill when the pattern stabilizes, assembled ad-hoc by the operator when still exploratory. Workflows are how PhantomOS extends from single-skill capabilities into a platform.
- **Model routing** — the rule that `subagent_safe: true` skills with a `recommended_model` different from the session model launch via Task tool with that model. Full matrix in `docs/system/patterns.md § Model Routing`.

## Governance — the thesis discipline

- **Extractibility test** — the binary rule that a core feature must survive replacing *brand* with *matter*, *creator*, *account*, or *venue*. If it breaks, the feature goes into a vertical pack, not the core. Keeps the thesis of universality falsifiable.
- **Agnostic by test** — the position that PhantomOS's universality claim is verified continuously through the extractibility test, not asserted as marketing.

---

> **Why this doc exists:** a written canon compresses every future communication. Without it, each editor re-argues the same vocabulary battles and the surface drifts. With it, terms are identifiers — used anywhere, defined once. Add a term here only after it passes the three tests; remove a term here only when evidence shows it no longer earns its place.
