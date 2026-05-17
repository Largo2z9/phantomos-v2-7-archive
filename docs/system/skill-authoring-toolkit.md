# Skill Authoring Toolkit · Prompt Engineering for SKILL.md

> **Audience.** Skill authors and contributors writing or extending SKILL.md files. Skip if you only use the kit shipped, this document has nothing for runtime operators.
>
> **Posture.** The patterns below are levers, not constraints. They name what the doctrines already apply implicitly, so authors can reach for the right one when relevant, without imposing a rigid template that would crush the agent's reasoning. The agent thinks freely ; the author provides the right anchors.

---

## Why this exists

A `SKILL.md` is a dense prompt. The agent reads it before invoking the skill, and the quality of the output depends partly on whether the prompt activates the right reasoning patterns. PhantomOS doctrines (CI, SED, CMR, SAD) already use a set of prompt engineering techniques, implicitly. This document names them so future skill authors can apply them deliberately when the situation calls for it.

The aim is **not** to enforce a fixed template. It is to give authors a vocabulary for the leverage points they already see working in the existing skills. The agent's intelligence remains the primary engine ; the techniques below are how authors set the conditions for that intelligence to operate well.

---

## Three principles of dense prompting

Density beats verbosity. *"Dissect methodically. Granular."* activates more reasoning depth than *"Please analyze carefully and thoroughly."*, because the dense terms appear in high-quality training corpora and pull their associated patterns with them.

Macro before micro. A SKILL.md reads top-down. Open with the decisive test or thesis, then the steps, then the examples. The reader (agent or author) loads the frame before the detail.

A magic keyword carries the weight of a paragraph. This is why our anti-patterns are *named* (Form-fill cascade, Score leakage, Acronym leak, Permutation-without-pivot, Sourcing-mort). The name itself activates refusal-by-default.

---

## Verbs worth reaching for

When the situation calls for them. Not a checklist.

| Context | Verbs that activate the right pattern |
|---|---|
| Audit / diagnostic | *dissect methodically*, *granular*, *ground in evidence*, *trace to canon* |
| Producer / synthesis | *synthesize*, *triangulate*, *cross-reference*, *converge* |
| Hard Rules / refusals | *decisive*, *binary*, *refuse by default*, *non-negotiable* |
| Operator surface | *surface*, *flag*, *anchor*, *recommend* |
| Reasoning posture | *reason step by step*, *macro then micro*, *load-bearing*, *first-principles* |

Curated subset of `operator-kb/02-ai/prompting/magic-keywords.md` (full 115+ keyword library). Use any verb that fits ; do not force one because it is on the list.

---

## Interaction patterns the doctrines already apply

Five techniques you will see across PhantomOS skills, named here so they are recognizable when authoring a new one.

**Validation gates.** Workflow-integrity hooks (mutation-guard, convention-guard, finalize-mutation-batch). The agent stages, the operator confirms or corrects, the gate enforces. Use when a downstream step depends on a prior commitment that should not be silently revised.

**Iterative loop with falsifiable hypothesis.** Our `--mode=breakthrough` opt-in (cell tagged `bet=true`, hypothesis declared, route to learnings post-test). Use when the safe path produces median output and a bet is justified.

**Role switching.** The agent shifts posture across a session · orchestrator when planning, senior practitioner when producing, auditor when reviewing. Each posture has its own register and rule set. Use when the skill spans multiple cognitive modes.

**Adversarial review.** The `red-team` skill ; multi-prism audits with explicit refusal-by-default. Use when a deliverable needs hostile pressure-testing before ship.

**Upstream questioning.** Before answering the operator's literal question, map one level above (intention, constraint, blind spot) and let that frame the answer. Already coded as Expert Relay in the project root and as intention detection in `contextual-intelligence.md`. Source : `operator-kb/02-ai/prompting/upstream-questioning.md`.

---

## Going deeper

This document covers the patterns visibly applied in PhantomOS V1. The full prompt engineering library, including dense prompting full process, P.A.R.O framework, the 75-technique interaction modifier catalog, structured context design, prompt transformation workshop, lives in `operator-kb/02-ai/prompting/` and `operator-kb/02-ai/context/`. External reference : the GHOSTY skill (origin).

Skill authors who want to push their craft further should read the sources directly. This toolkit is a curated entry point, not a substitute.

---

## What this is not

Not a template. Not a checklist. Not a mandatory pass before shipping a skill. Authors who write a clean, idiomatic `SKILL.md` without ever opening this document are doing the right thing. The patterns above are a vocabulary for the techniques that work, to be used when they fit, ignored when they don't.

The agent's intelligence is the primary engine. The skill author provides the conditions ; the doctrines guarantee the floor ; the toolkit names the levers. The output emerges from the combination.
