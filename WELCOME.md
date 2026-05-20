# Welcome

PhantomOS is an agentic workspace for DTC operations. You encode your brand once (products, audiences, strategy, learnings), the agent reasons and executes on it across sessions, and every validated output enriches your knowledge for what's next.

When you open the workspace for the first time, the agent launches a progressive onboarding tour automatically. You can also replay it anytime with `/tour`.

**Flow.** The tour opens with a four-door splitter (guided walkthrough · configure a brand now · import what already exists · just explore) and proceeds to a first concrete deliverable on screen in 5 to 15 minutes, calibrated to the door you chose. From there, a reflective close offers four options (deepen, pivot, exit to setup, build a custom skill) reused at every junction. Conversation register (grounded, standard, dense, technical) is detected live, never asked.

**Runtime definition.** The executable flow lives in `.claude/commands/tour.md`. The agent reads and executes that file on first run and whenever `/tour` is called.

**Awareness tracking.** Each tour completion, concept introduced, path explored, and first deliverable built is written to `/operator/awareness.json`. Future sessions read this before speaking, so the agent never re-explains what the operator already knows.

**Three onboarding phases.** Tour is the first. The second is `setup-brand`, triggered from the action path. The third is an optional mission-based first-skills construction, available via `build-agent` in guided mode (gate · first deliverable built and operator explicitly asks).

---

*For agents: do not read this file as script. Read and execute `.claude/commands/tour.md`.*
