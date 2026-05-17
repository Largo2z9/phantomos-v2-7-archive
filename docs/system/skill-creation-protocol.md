# Skill creation protocol

> Decision and execution protocol for skill creation in PhantomOS. Written in response to red-team findings + operator framing : operator controls the lifecycle end-to-end, graduation of granularity is explicit, heavy skills gate before cascading, enrichment is continuous via learn-from-session.

## When a skill is proposed

A skill is proposed when the operator performs a task that matches at least one of these signals :

1. **Repetition**, same task executed ≥ 2 times on the same or different brands
2. **Genericity**, task applicable to other brands or to workspace-level, not a one-off
3. **High token cost**, task consumes > 10k tokens per execution (structured brief, multi-layer audit, complex analysis)
4. **Pattern identified by learn-from-session**, at session close, detection of a workflow the operator might want to automate

**Who proposes** : the agent, not the operator. The operator asks for an action ; the agent notes the pattern mentally ; at session close (or when the pattern repeats), it surfaces the creation proposal.

## Graduation of granularity

Before building anything, classify the request :

### Specific · one skill is enough

Criteria :
- Atomic action or a short linear procedure (< 5 steps)
- Scope is either single-brand-entity OR workspace-agnostic (no brand scope at all)
- No sub-task decomposition needed
- Runtime < 5 minutes

Examples :
- "Generate a hook variant for an existing ad"
- "Technical audit of a pixel"
- "Extract product mentions from a transcript"

**Build** : `scaffold-skill-stub` → one SKILL.md file + optional associated script. No SOP required.

### Heavy · SOP + orchestrator + mini-skills

Criteria :
- Multi-step procedure with conditional decisions
- Multiple sources of truth to consult (brand + products + audiences + resources)
- Token budget > 30k per execution
- Runtime > 10 minutes
- Established methodology (audit, roadmap, discovery, strategy)
- Broad business-expert vision (not just one action, a method)

Examples :
- "Full Meta Ads audit on a brand"
- "End-to-end creative strategy setup"
- "Quarterly brand roadmap"
- "Competitor intelligence across a vertical"

**Build** : three-step process :
1. **SOP first**, methodology written as a paid-consultant document : checkpoints with severity, reasoning layer, resource discovery, scenario variants
2. **Orchestrator skill**, thin executor that reads the SOP and calls mini-skills
3. **Mini-skills incremental**, atomic checks/actions, built progressively as checkpoints are implemented

### Macro · multiple orchestrators

Criteria :
- Very broad business vision covering multiple dimensions (e.g., "global audit" = Meta + Shopify + tracking + email + SEO)
- Each dimension has its own methodology and its own skills
- Operator might want to run one dimension alone OR the whole set

**Build** : multiple SOPs + multiple orchestrators (one per dimension), plus a parent orchestrator (`audit-global`) that fans out to the child orchestrators. Mini-skills are reusable across orchestrators.

Example pattern :
```
audit-global (macro orchestrator)
├── audit-meta-global (orchestrator + SOP)
│ ├── mini-skill: check-pixel-deployment
│ ├── mini-skill: check-audience-exclusions
│ └── ...
├── audit-shopify-global (orchestrator + SOP)
│ ├── mini-skill: check-funnel-integrity
│ └── ...
├── audit-tracking-global (orchestrator + SOP)
└── audit-email-global (orchestrator + SOP)
```

---

## Operator control · always

Three moments where the operator must validate :

### 1. Creation proposal

The agent never creates a skill or SOP silently. On pattern detection :

> "I noticed you did [pattern X] on Northsense and Cherico. Would formalizing that as a skill save you time ? I can propose (a) a simple skill, (b) a skill + SOP if it's broader, or (c) drop it for now."

Operator accepts → agent starts the scaffolding phase. Operator refuses or "later" → agent logs in pending-validations.md, re-proposes after 2-3 additional repetitions.

### 2. Gate before cascade of agents

**CRITICAL** : when a heavy skill is about to cascade multiple subagents or execute a long sequence, it MUST request confirmation before embarking.

Example, orchestrator `audit-meta-global` at start :

> "I'm about to run the full Meta audit on Northsense. Here's what's going to execute :
> - 40 checkpoints organized across 7 layers
> - Estimate : 15-30 min, ~50-80k tokens
> - Mini-skills called : check-pixel-deployment, check-capi-deployment, check-audience-exclusions, ... (full list below or on request)
> - Output : markdown report + appended actionable items in pending-validations
>
> Scenario (default : new-client-discovery), alternatives : pre-scaling-diagnostic, post-incident-diagnostic, quarterly-review, agency-switching.
>
> Run as-is, different scenario, or do you want to reframe ?"

Operator confirms → execution proceeds. Operator adjusts → skill reconfigures. Operator refuses → skill stops without consuming tokens.

**Hard rule** : no cascade > 3 subagents without an explicit gate. No execution > 20k estimated tokens without an explicit gate.

### 3. Final validation before output ships

Every skill producing an output (report, brief, plan) goes through `validate-output-coherence` before shipping to the operator. If blocking_issues → skill proposes a revision, operator sees the diff.

Every skill mutating data (via write-to-context) goes through workflow-integrity gates (stage-proposal + checkpoint-resolver) for gated fields.

---

## learn-from-session · continuous enrichment

`learn-from-session` is called at session close. Its mission is not limited to persisting decisions, it also **proposes system improvements** :

### Skill candidates at close

Scan the session for :
- **Repeated tasks** : same request type executed ≥ 2 times in the session → lightweight skill candidate
- **Multi-step workflows** : recurring sequence (e.g., "check X, then compare to Y, then generate Z") → heavy skill candidate with SOP
- **Cross-brand tasks** : same action on multiple brands in the session → workspace-level skill candidate

Surface to the operator at close :

> "During this session I observed :
> - You generated 3 ad briefs with the same structure (hook → body → CTA → proof). Simple skill candidate `brief-ad-quick` ?
> - You audited the offers of 2 brands with the same method. Heavy skill candidate `audit-offers` with SOP ?
>
> Scaffold one, the other, later, or never ?"

### SOP / doc enrichment candidates

Scan the conversation for :
- **Business patterns discussed** : operator explained a pattern, gave concrete examples, critiqued an approach → potential enrichment of an existing SOP (reasoning layer) or a framework/guide
- **Decisions to promote** : a local learning on a brand that has broader reach → candidate for workspace-level promotion

Example :

> "We discussed during the session that the GWP Spring Days pattern at Northsense only performs if the average AOV is above the threshold, that's a business insight. Want me to add it to the reasoning layer of checkpoint 4.x in audit-meta-global, or as a separate framework ?"

### Convention or rule promotion candidates

If a learning on a specific brand is generalizable :

> "Learning L-042 on Northsense ('Meta rejects efficacy claims without disclaimer in FR') is applicable to all supplement brands. Want me to promote it as a workspace-level convention ?"

---

## Sibling skills vs extension

Before creating a new skill, apply the **extend_before_create** rule (permanent memory feedback) :

If similar functionality already exists :
- Can we add a mode / phase / conditional input to the existing skill ? → extension
- Does the typology require a split (disjoint permissions, non-overlapping write scope) ? → sibling skill justified

Default = extension. New sibling skill = justified exception.

---

## Rollback / sunset of skills

A skill can become obsolete. Criteria :
- Not invoked for 6+ months
- Superseded by a more generic skill
- Schema migration renders it stale

**No immediate deletion.** Mark `deprecated: true` + `deprecated_since` + `replaced_by`. Operator sees the flag in the manifest, can decide to revive or let it sunset. Archive in `.skills/skills/_archive/` after 6 more months.

Preserves traceability for retrospective audits.

---

## Cross-references

- `docs/system/sop-skill-conversion.md` · the 5 SOP ↔ skill conversion scenarios
- `docs/system/skill-builder-cartography.md` · when to extend a schema before creating a skill
- `docs/system/skill-resource-discovery.md` · how skills find resources at runtime
- `.skills/skills/learn-from-session/SKILL.md` · updated with enrichment detection rules
- `.skills/skills/build-agent/SKILL.md` · scaffolding orchestrator
- `.skills/skills/scaffold-skill-stub/SKILL.md` · creation primitive
- Memory feedback `extend_before_create` · canonical rule
