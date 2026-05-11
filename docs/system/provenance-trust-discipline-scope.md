# Provenance & Trust Discipline (PTD) — Scope Cadrage

> Working scope draft — R&D zone, Build mode. **Scope-only document, NOT a full doctrine.** Full PTD is to be authored when trigger conditions hit (see §5). Today this file reserves the conceptual space and bounds the scope so future work is constrained.

---

## 1. Why PTD must exist

Three converging trajectories make PTD indispensable within 6-12 months of authoring this scope:

**1.1 — Multi-operator workspaces.** PhantomOS today assumes a single operator per workspace (file locking V1.x, single semantic-trust arbiter per CI). When Mattéo + Largo + future operators share a brand workspace (Abyss agency model), the question becomes: who wrote this fact, who owns the canon, who has read access, who can mutate. SED carries `actor_id` events ; PTD carries the trust layer above that.

**1.2 — Canon as product (knowledge packs).** Roadmap V2 envisions canon (copywriting-canon, future skincare-FR-pack, gambling-FR-pack) as a vendable asset. Versioning, licensing, watermarking, IP attribution, deprecation forced by vendor — none of these fit in SED (substrate) or CMR (production mechanism). They need a discipline of *who owns and who is allowed to consume*.

**1.3 — Marketplace skills.** When third-party authors contribute skills (community contributions per SAD §11.3), trust becomes the dominant question. A skill that consumes canon partially correctly can pollute the workspace. A skill written by an unknown author needs sandbox + signature + provenance trail. SAD covers authoring quality ; PTD covers authoring identity and authorization.

These three are the same primitive at different scales: **who is the actor, what is their authority, with what visibility, signed by whom, expiring when.**

---

## 2. Scope — what PTD will cover

**2.1 — `_provenance` block per asset.** Every asset (canon file, skill, registry, brand JSON section) carries a `_provenance` block:
```
_provenance:
  actor_id: <operator_id | "system" | "third-party:<id>">
  written_at: ISO8601
  pack_id: <if from a knowledge pack, else null>
  pack_version: <semver>
  license: <license_id>
  signature: <hash | null for first-party>
```
Block is mutated through the SED gate, surfaced never to operator (visible to audit and admin only).

**2.2 — `actor_id` in event log.** SED's `events.jsonl` already supports `actor_id`. PTD enforces that *every* mutation event carries actor_id. Anonymous events refused. Surface the trail in audit reports.

**2.3 — Visibility scope per asset.** `visibility_scope: workspace | operator | public | client-readonly`. Determines who can read. Default: `workspace` (any operator with workspace access reads). Per-asset overrides: an operator's `awareness.json` is `operator`-scope only ; a client dashboard view is `client-readonly`.

**2.4 — Pack composition rules.** When multiple knowledge packs are loaded simultaneously (DTC-pack + FR-compliance-pack + premium-positioning-pack), conflicts on canon enums are resolved via:
- *Disjoint namespaces* — packs declare prefix (e.g. `BA-` for Schwartz, `FRC-` for FR-compliance), no cross-pack collision.
- *Alias bridges* — when packs reuse the same concept under different IDs, an explicit alias-bridge file declared by the consumer skill or workspace.
- *Refusal* — if neither, the loader refuses both packs simultaneous.

**2.5 — Skill signing.** Third-party skills sign the SKILL.md with operator's GPG or platform-issued key. Manifest tracks signatures. Unsigned skills run in sandbox (canon namespace `custom/` only, refused access to core canon).

**2.6 — License tracking per consumer.** A skill consuming a licensed canon declares which license it operates under. License conflicts (e.g. proprietary canon consumed by a community skill that re-distributes derivations) are surfaced as warnings.

**2.7 — Security-scan extension.** SED's mutation-guard already scans for 5 malicious patterns. PTD extends to scan installed skills (not just writes) — third-party skill installation triggers full scan.

---

## 3. What PTD will NOT cover (boundary)

To prevent scope creep, PTD explicitly does NOT cover:

- **Full RBAC** (role-based access control with permissions matrix). Workspace + role + permissions = infrastructure layer, lives in SAD lifecycle sub-corpus when ships.
- **Marketplace UI / discovery / rating**. Surface product, not doctrine.
- **Watermarking implementation**. Mechanism, not doctrine. PTD says "watermark is required for licensed pack"; the *how* is implementation detail.
- **Encryption of brand data**. Infra layer.
- **Audit dashboard implementation**. Surface tooling, not doctrine.
- **Operator authentication / SSO**. Auth layer.

PTD is about *the rules of trust and provenance*. The mechanisms that enforce them live elsewhere.

---

## 4. Relationship to other doctrines

**PTD ⊂ CI** — sister discipline to SED, CMR, SAD. Master = CI. PTD operationalizes CI's trust dimension (the agent reasons over a *known-provenance* universe, not an ambient one) for multi-tenant scale.

**PTD extends SED.** SED carries `actor_id` and `_field_types` ; PTD adds `_provenance`, `visibility_scope`, `license`, `signature`. PTD does not duplicate SED — it stacks on top.

**PTD constrains CMR.** A canon variable consumed by CMR must carry `_provenance`. Skills that consume unsigned third-party canon are flagged. CMR's compound effect (canon shared across skills) becomes traceable per-source.

**PTD constrains SAD.** Third-party authoring section in SAD references PTD for signature + provenance + sandbox rules.

**PTD touches D#307 Extractibility.** The test "if I replace `brand` with `creator` does it hold" must include "if I replace this knowledge pack with another, does the trust framework hold" once PTD ships.

---

## 5. Trigger conditions for graduation to full doctrine

PTD remains in scope-only state until **at least one** of the following hits:

**5.1 — 2nd operator connected.** A second human operator joins a brand workspace with write access. Multi-operator semantic-trust is no longer hypothetical.

**5.2 — 1st knowledge pack vendor-shipped.** A canon pack is sold (or licensed) to an external party. Versioning, watermarking, license tracking become operational concerns.

**5.3 — 1st third-party skill contributed.** An author outside Largo's direct authoring contributes a skill installed in any workspace. Signing, provenance, sandbox become operational concerns.

When any of these triggers, PTD scope is upgraded to full doctrine drafted in `research/provenance-trust-discipline-2026-XX-XX.md`, then promoted Release once invariants stabilize.

Until trigger, PTD scope serves as:
- Reservation of the conceptual space (no other doctrine should encroach)
- Constraint on near-term decisions (don't ship anything that would conflict with future PTD)
- Anchor for cross-references in CMR / SED / SAD that already mention provenance/trust without ambiguity

---

## 6. Anticipatory anti-patterns

Even before PTD ships full, three anti-patterns are flagged by the scope:

| Name | Symptom | Pre-emptive fix |
|---|---|---|
| **Anonymous mutations** | Event log entries without `actor_id`. | SED already requires `actor_id` ; enforce now. |
| **Canon namespace collision** | Two pack-candidate canons reuse the same ID prefix. | When ingesting a future pack, validate namespace uniqueness. |
| **Implicit ownership** | A workspace JSON section assumed to belong to "the operator" without explicit attribution. | When introducing the second operator, retroactively attribute existing content via `_provenance` migration. |

---

## 7. Open questions (to be resolved at graduation)

1. **Linux Foundation steward model vs Palantir vendor-controlled** for canon governance. Steward = elected maintainers, transparent process, slower iteration. Vendor-controlled = Largo as canon authority, fast iteration, single point of failure. PTD must arbitrate before marketplace ships.

2. **Bayesian prior updates from cross-brand learning.** When `mine-vom` runs on 50 DTC brands, the dataset of "Porter forces actually activated" forms a Bayesian prior. Should this *replace* the per-brand activation test (faster, may kill specificity) or *update* the prior while preserving per-brand override (slower, more correct) ? PTD's view: trust requires the operator to retain override, prior is a *suggestion*, never a *replacement*.

3. **Pack-of-packs composition.** Composing 3+ packs simultaneously is a meta-composition problem (DTC × FR-compliance × premium-positioning). Refusal-by-default is safe but limits market value. Alias-bridges are flexible but add complexity. To resolve at graduation.

4. **Migration of pre-PTD brands.** Existing brands lack `_provenance`. At PTD ship, retroactive attribution is required. Migration script + heuristics (last commit author = actor_id default, etc.).

5. **Failure mode for signature verification.** A signature that fails to verify — refuse install (safe but blocks legitimate operator if key is mis-managed) or warn-and-allow (permissive, can be exploited). Default: refuse, with explicit override for emergency cases logged.

---

## 8. Status

- **Scope draft v0.1** — R&D zone, Build mode, S44 (2026-04-26).
- **Reservation of conceptual space** — PTD is named as 4th sub-doctrine of CI in D#362.
- **No implementation today** — scope only. Triggers (§5) determine when full doctrine is authored.
- **Cross-referenced in** : SED §11.6 (overlap mention), SAD §11.3 (third-party authoring extension), CMR §11.x (open tensions on canon-as-product).

---

*Scope cadrage S44 — 2026-04-26 — reservation of the conceptual space for Provenance & Trust Discipline. Full doctrine deferred to trigger conditions (multi-operator / knowledge pack / third-party skill).*
