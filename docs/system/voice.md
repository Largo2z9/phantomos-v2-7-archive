# Voice & Style Canon

This document defines how PhantomOS writes — across agent contracts, reference docs, skills, READMEs, and operator-facing surfaces. It is the source of truth every editor, human or agent, consults before modifying any written artifact in the workspace.

The canon is short on purpose. It locks the axes that matter and leaves the rest to judgment.

## Core principles

**Punch by insight, not by volume.** A sentence earns its place by telling the reader something they did not already know. Emotional register is minimal. Opinion is expressed through the structure of what we choose to say, not through exclamation, provocation, or marketing cadence. If a line could appear on a landing page, cut it.

**Prose first, structures in support.** Paragraphs carry the reasoning. Tables and bullets appear when enumeration genuinely helps — three or more mutually exclusive items, a matrix, a rule set. A two-item bullet list is a paragraph in disguise; write the paragraph.

**Specificity over generality.** Name the file. Name the line number. Name the function. Abstraction without a concrete anchor is noise. If a claim cannot be checked against a specific artifact in the workspace, it is either wrong or in the wrong doc.

**The reader is an operator.** Technical, competent, short on time. Assume they know what a brand is, what a skill is, what an agent contract is — and reach for `lexicon.md` when they don't. Never re-explain canonical concepts mid-document.

**Write for distribution.** PhantomOS ships to operators who are not Largo, not French, and not versed in the heist thematic. Every doc is authored as if a stranger will read it on first open. Context unfolds through naming and structure, not through a foreword.

**Durability over cleverness.** A punchline is only worth writing if it is still right in six months. Dated hype, seasonal references, and self-congratulatory framing rot fast. Declarative neutral sentences age well.

**Strong terms must be load-bearing.** A strong adjective or verb is earned when it names a mechanism the reader can verify in the product. *Stateful*, *durable*, *opinionated*, *runtime*, *executes*, *enforces*, *scoped*, *contract* — earned when the product actually does those things. *Powerful*, *supercharge*, *intelligent*, *seamless*, *AI-driven*, *robust*, *enterprise-grade* — never earned. They decorate without describing. Neutral is not the alternative to bullshit; specificity is. A sentence should carry weight through the nouns and verbs it chooses, not through softening or through hype.

**Name what recurs.** Formalize a concept with a canonical name once it appears three or more times and forces a re-explanation. *Agent Contract*, *Operator*, *Expert Relay*, *Executive Briefing Posture* — each replaces a paragraph with a term and compresses every future reference. Two conditions: the name must be shorter and more precise than the paraphrase it replaces, and it must survive a six-month test. Ephemeral concepts, one-session abstractions, and team-internal shorthand do not belong in the canon. When a named concept enters circulation, add it to the terminology canon below on the same patch. Naming is editorial infrastructure; treat it with the same care as renaming a public API.

## Register

The register is chairman punchy via expert insight: dense, technical, actionable, subtle. Punch comes from the specificity of the claim and the tightness of the sentence, not from emphasis or vibe.

Avoid exclamation marks, emojis, rhetorical questions, vibey marketing verbs (*unlock*, *supercharge*, *transform*, *empower*), and parenthetical asides that soften a claim. When tempted to soften, delete instead.

Short sentences land. Long sentences earn length through information density, not elaboration. A period is cheaper than a comma.

## Terminology canon

The workspace has a defined lexicon — a written set of canonical terms that pass three tests (recurrence, precision, durability) and are used across the project without redefinition. Full canon and definitions live in [`lexicon.md`](../../lexicon.md).

When writing a doc, use the canonical term from the lexicon. Link to its definition on first use only if ambiguity is likely for the target reader. Non-canonical terms still appear in prose when they clarify something in context — they just do not live in the lexicon.

When a new concept earns canonical status (three occurrences, shorter and more precise than its paraphrase, valid six months out), add it to `lexicon.md` in the appropriate cluster before using it in a shipped doc. Naming is editorial infrastructure — treat it with the same care as renaming a public API.

## Language policy

All system docs, READMEs, `CHANGELOG.md`, `SKILL.md` files, and YAML frontmatter are authored in English. Operator-facing surfaces (WELCOME, getting-started, capabilities) ship in English too. No bilingual files, no side-by-side translations, no French-first exceptions.

Runtime language adaptation is the agent's responsibility. The root Agent Contract instructs Phantom to respond to the operator in their detected language, regardless of source doc language. A French-speaking operator reads a French agent; every file on disk stays English. Distribution, consistency, and register all improve under a single authoring language.

## Formatting conventions

Paragraphs do the work. Reach for structures only when they carry meaning a paragraph cannot.

| Use case | Format |
|---|---|
| Three or more mutually exclusive items | Table |
| Ordered steps | Numbered list |
| Parallel unordered options | Bullet list |
| Meta commentary (why, warning, note) | Blockquote with bold lead (`> **Why:** …`) |
| File, command, or identifier reference | Inline code |
| Longer code or configuration | Fenced block with language tag |

Headings stop at H3 within a doc. H4 or deeper indicates the section needs splitting or the topic belongs in a pointer doc. Keep a blank line before and after every heading, table, list, and code block.

## Onboarding posture

WELCOME.md, getting-started, and first-run surfaces follow a **product-tour factual** register with **progressive vision reveal**. Describe what PhantomOS is by what it does, not by what it means. Lead with the first action the operator can take in under three minutes. Keep vision statements out of the opening; link to `vision-public.md` for operators who want the framing.

The product carries the narrative. The narrative does not carry the product.

## Anti-patterns

Three failure modes recur in first drafts. Each is caught by a binary test before the line ships.

**Claim without mechanism.** Phrases like *fills the gap*, *operates on something*, *each with a defined behavior*, *installs the discipline* sound confident and say nothing. If a sentence contains an action verb, the mechanism must follow in the same sentence or the next one. If the reader can ask *"and concretely ?"* without an answer in scope, cut the sentence.

**Crafted punchline that reads as growth coach.** *Capture the rent the ones who wait will lose*, *first-movers win*, *the moat compounds* in isolation. Chairman punchy comes from precision, not from rhetorical cadence. Test: if a sentence would fit in a Twitter growth thread, rewrite it flat.

**Unverifiable metric.** *Three minutes to boot*, *10x faster*, *zero setup*. Every quantitative claim in a doc must be reproducible by the reader. Either specify the condition (*three minutes from empty workspace to first skill run*) or cut.

**Triple-parallel punchline.** *"You talk, the agent writes. You correct, the agent learns. You stop, the agent persists."* Rhythmic triplets feel decisive but collapse into coach cadence when each member is a restatement of the others. The pattern recurs under many shapes (*"No X. No Y. No Z."*, *"X becomes rules. Y becomes patterns. Z becomes operable."*). Test: if the three members are paraphrases of one claim, keep the strongest and delete the rest. Keep the triplet only when each member adds distinct information.

## Cross-surface rules (runtime vs docs)

Two surfaces with different rules that editors should not mix up.

**Docs** (this canon applies): em dashes allowed for punctuation. Functional signals `✓` and `⚠` allowed inline for state. No decorative emojis (*📋 💡 🧠 📥 ✅*). EN everywhere.

**Runtime agent replies** (rules live in root `CLAUDE.md § Operator contract`, stricter): no em dashes in operator-facing replies (use period, comma, or two sentences). No decorative emojis at all. Operator language matches detected input (FR / EN).

The distinction matters when quoting agent template texts inside doc examples. A template text shown as an example in a doc follows runtime rules, not doc rules. When in doubt, strip the em dashes from quoted agent speech even if the surrounding doc prose allows them.

## References

Canon influences, in order of weight: Stripe engineering documentation (rigor, specificity, technical calm), Linear product documentation (opinionated minimalism, short sentences), Anthropic developer docs (authoritative clarity, prose-first technical explanation). Vercel and Notion were studied and not adopted as primary references — too dense and too warm respectively for the PhantomOS register.

## Examples

**Before — marketing decoration, no mechanism**

> PhantomOS is a powerful agentic workspace that lets you supercharge your brand operations with AI-driven workflows and intelligent context management.

**After — load-bearing terms, opinionated structure**

> PhantomOS is a stateful runtime for operator work. One brand, one workspace, one agent contract. The agent executes on that contract every session — it does not chat, it operates.

The difference: every strong term in the second version points to a real mechanism — *stateful* (context persists), *runtime* (actually runs skills), *contract* (binding rules), *executes* (not conversational). The first version's strong terms point nowhere.

**Before — bullet padding without content**

> - Fast
> - Reliable
> - Easy to use

**After — cut, or specify**

> Brand setup takes under three minutes. Agent contracts load in under 5KB per session.

**Before — vague rule**

> Keep CLAUDE.md files small.

**After — specific rule**

> Root Agent Contract ≤ 220 lines. Brand Agent Contract ≤ 100 lines. Over budget, `learn-from-session` flags for operator review.

---

> **Why this doc exists:** without a written canon, every editor re-arbitrates the same voice decisions and the doc surface drifts. The canon locks the decisions once. Open a PR against this file rather than patching downstream when the voice needs to evolve.
