# Doctrine Governance — Meta-Process

> Working draft — R&D zone, Build mode. To be reviewed, then promoted to `workspace-template/docs/system/doctrine-governance.md` in Release mode. **This is a meta-process, not a doctrine.** It governs how the doctrines themselves (CI, SED, CMR, SAD, PTD, future) are promoted, amended, retracted, and reconciled when they conflict.

---

## 1. Why governance is needed

PhantomOS doctrines are not finished documents. They are living rules. Without explicit governance:

- Amendments happen silently (someone edits `contextual-intelligence.md` directly, the change is lost in git history without a decision trace).
- New doctrines proliferate without criteria (every author who senses a gap drafts a new doctrine, the architecture diluteates into jargon-stack).
- Retractions are unsafe (a doctrine someone depended on disappears, downstream skills break).
- Conflicts between doctrines are arbitrated mentally by the maintainer (CI says trust, SED says enforce — which wins?).

This meta-process names the rules. It is short. It is append-only. It mirrors the discipline imposed on `decisions.md` (D# verrouillé, [SUPERSEDED Sxx], no deletion) applied to the doctrines themselves.

---

## 2. Promotion criterion — when a draft becomes a binding doctrine

A doctrine candidate (today : SED, CMR, SAD drafts in `research/`) becomes binding (promoted to `workspace-template/docs/system/`) only when **all four** of the following hold:

1. **≥3 instances of application in active skills.** The doctrine has been applied at least three times to real skills, not just theorized. CMR satisfies this via paid-angles, copy-brief, analyze-copy.
2. **Extractibility test passed.** Per — *"if I replace 'brand' with 'matter' / 'creator' / 'venue' / 'account', do the doctrine's invariants still hold?"* Pure marketing-anchored invariants are isolated as marketing-canon sub-corpus, not the doctrine's core.
3. **Cross-reference consistency verified.** The candidate doctrine cross-references with all sister doctrines (CI master, SED substrate, CMR mechanism, SAD authoring, PTD provenance) in both directions. Boundary cases identified and either resolved or flagged as open tensions.
4. **D# verrouillé in `decisions.md`.** A formal decision entry, append-only, marks the promotion. The D# is the immutable reference for any future amendment.

Drafts that fail any of these stay in R&D. No promotion under pressure.

---

## 3. Amendment — append-only via D# new

Amending a binding doctrine **never** edits the original silently. It follows:

1. **Draft amendment** — propose change in a new `research/{doctrine}-amendment-{date}.md` file describing what changes and why.
2. **Decision entry** — when validated, add new D# in `decisions.md` with explicit `[SUPERSEDES Dxxx]` annotation pointing to the prior decision.
3. **Doctrine in-place patch** — update the doctrine file in `workspace-template/docs/system/` with a changelog header noting the supersession.
4. **Consumer re-test** — surface a re-test list of skills consuming the amended doctrine. Test fixtures must pass post-amendment.
5. **Sync derived workspaces** — if breaking change, follow Build vs Release governance for the propagation.

The amendment doctrine is itself amendable by amendment. The recursion stops at the first amendment by convention — amendments to the amendment doctrine require the maintainer + 2 senior reviewers.

---

## 4. Retraction — interdiction par défaut

A binding doctrine cannot be retracted silently. Three options:

**4.1 — `[DEPRECATED Sxx]` window.** Doctrine marked deprecated in its file header, paired with a migration path for consumers. Window of ≥30 days during which consumers must migrate. After window, the doctrine file moves to `_archive/doctrines/{name}-{deprecation_date}/`, stays read-only.

**4.2 — Supersession by stronger doctrine.** If a new doctrine fully subsumes an old one (e.g. PTD partially subsumes SED's `actor_id` discipline), the new doctrine inherits the responsibilities and the old doctrine is `[SUPERSEDED]`. Old doctrine's invariants are absorbed, not lost.

**4.3 — Refused.** Most retractions are refused by default. Doctrines codify hard-won discipline. Removing one because it's "inconvenient" is the same anti-pattern as removing a Hard Rule because a skill is failing — the symptom, not the cause.

---

## 5. Conflict resolution

When two doctrines appear to conflict, the resolution follows this priority:

| Layer | Discipline | Wins on |
|---|---|---|
| 0 (Frame) | Extractibility (Extractibility test) | Architectural agnosticity — a feature that breaks the test loses |
| 1 (Master) | CI | Substantive judgment, surface contract, two-tier rule |
| 2 (Sub) | SED | Substrate integrity (mutation gate, sourcing, layer separation) |
| 2 (Sub) | CMR | Production discipline when output is intersectional |
| 2 (Sub) | SAD | Authoring rules, composition contracts, lifecycle |
| 2 (Sub) | PTD | Trust and provenance |

**General rule:** when two layers conflict, **higher layer wins on its territory** (CI wins on judgment, SED wins on substrate). When two same-layer disciplines conflict, the resolution depends on the territorial nature of the conflict :

- *SED vs CMR* — SED wins on substrate questions (does this field have right `_field_types`?), CMR wins on production questions (does this output respect cardinality cap?). In practice the disciplines do not really conflict because they cover different territories ; apparent conflicts are usually mis-identification.
- *SED vs SAD* — SED wins on data write rules (mutation gate non-optional), SAD wins on skill design rules (frontmatter triad, composition).
- *CMR vs SAD* — CMR wins on output quality (matrix invariants), SAD wins on authoring procedure (extend before create, type taxonomy).
- *PTD vs others* — PTD acts as constraint stacked on top once shipped. PTD does not override but adds requirements.

When conflict is genuinely irreducible : route to the maintainer. Decision logged in `decisions.md`, doctrine cross-references updated to clarify the boundary.

---

## 6. Adding a new doctrine

A new doctrine candidate (e.g. tomorrow : Model-Adaptive Discipline, or Provider-Agnostic Discipline) requires:

1. **Gap demonstration** — clearly named gap that no existing doctrine covers, validated on ≥2 concrete cases.
2. **Sub-corpus check** — could the gap be covered by a sub-corpus of an existing doctrine? Default *yes* until proven otherwise (per — sub-corpus stratégie).
3. **Draft in R&D** — `research/{name}-{date}.md` with structure mirroring existing doctrines (thesis, problem, anatomy, anti-patterns, decision-aid, ops requirements, cross-references, open tensions).
4. **Promotion criterion** — same as §2.

Default posture: **most gaps are sub-corpus-able.** A new doctrine is justified only when the gap is genuinely orthogonal to existing disciplines (PTD is orthogonal to SED+CMR+SAD because trust is a different axis from substrate / production / authoring). New doctrines that overlap > 30% with existing are refused.

---

## 7. Doctrine versioning

Each binding doctrine carries `_doctrine_version` (semver) :
- **Major** — breaking change to invariants. Consumer skills may need patches. Migration path mandatory.
- **Minor** — additive (new invariant, new sub-corpus, new anti-pattern named). Backwards compatible.
- **Patch** — clarification, typo fix, example added. No semantic change.

Promotion to Release zone requires `_doctrine_version: 1.0.0`. Pre-release in R&D zone uses `0.x` versioning.

Versions are tracked in the doctrine file header :
```
---
title: Canonical Matrix Reasoning (CMR) — Operating Doctrine
_doctrine_version: 1.0.0
status: binding | draft | deprecated
last_amendment: D#xxx
---
```

---

## 8. Boundaries with skill governance

Doctrine governance is distinct from skill governance:
- **Doctrine governance** (this document) — meta-process for the rules themselves.
- **Skill governance** (SAD `extend_before_create`, manifest, deprecation) — process for skills consuming the doctrines.

A doctrine can change without skills changing. A skill can change without doctrine changing. They evolve at different speeds. Doctrines are slower (months / years), skills faster (weeks / months).

---

## 9. Anti-patterns

| Name | Symptom | Fix |
|---|---|---|
| **Silent edit of binding doctrine** | Author updates `contextual-intelligence.md` directly without D#. | Pre-commit hook refuses changes to bound doctrine without paired D# entry. |
| **Doctrine proliferation** | Every gap → new doctrine, jargon-stack accumulates. | Sub-corpus default rule. Doctrine-add gate (§6). |
| **Retraction by deletion** | Author deletes a doctrine instead of `[DEPRECATED]` window. | Refused by hook. Append-only enforcement. |
| **Conflict resolution by tribal knowledge** | "the maintainer would say SED wins here" — mental arbitration. | §5 conflict table explicit. New conflict types add a row to the table. |
| **Promotion under pressure** | Draft promoted to Release before ≥3 instances + extractibility test. | §2 criterion enforced — no promotion under deadline. |
| **Versioning skipped** | Doctrine file in Release without `_doctrine_version`. | Schema validation refuses. |

---

## 10. Status

- **Meta-process draft v0.1** — .
- **Promotion criterion** — same as the doctrines it governs. Once 3 doctrines have been promoted under this process, this meta-process graduates to Release.
- **First applications** — CMR / SED / SAD / PTD scope all routed through this process.
- **Cross-references** — referenced by CMR §3.5, SED §11.6, SAD §11.6, PTD scope §5.

---

*Meta-process — codifies how doctrines are promoted (≥3 instances + extractibility + cross-ref + D#), amended (append-only via new D#), retracted ([DEPRECATED Sxx] window), and reconciled (layer hierarchy + same-layer territorial). Append-only mirror of `decisions.md` discipline applied to the doctrines themselves.*
