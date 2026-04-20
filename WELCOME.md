# Welcome

PhantomOS uses a progressive onboarding tour. When the agent detects no brand is configured, it launches the tour automatically. You can also replay it at any time with the `/tour` command.

**Flow.** Absence of brand detected. The agent asks for a URL or a short description of the brand you want to configure. A scan runs in the background, or a short conversation builds the profile manually. During that time, the agent collects your first name, introduces PhantomOS in three short paragraphs calibrated to your AI experience level (detected live, never asked), and plants the concept of what a skill is. When the scan returns or the profile is built, the agent delivers the first tangible result. You then choose between three discovery paths (workspace concrete, learning mechanics, positioning) or move directly to configuring your brand. An implicit skip is available at any moment by saying *skip* or *direct*.

**Runtime definition.** The executable flow lives in `.claude/commands/tour.md`. The agent reads and executes that file on first run and whenever `/tour` is called.

**Awareness tracking.** Each tour completion, concept introduced, and path explored is written to `/operator/awareness.json`. Future sessions read this before speaking, so the agent never re-explains what the operator already knows.

**Three onboarding phases.** Tour is the first. The second is `setup-brand`, triggered from the tour's action path. The third is an optional mission-based first-skills construction, available via `build-agent` in guided mode.

---

*For agents: do not read this file as script. Read and execute `.claude/commands/tour.md`.*
