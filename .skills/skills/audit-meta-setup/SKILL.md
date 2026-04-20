---
name: audit-meta-setup
type: producer
version: "1.1.0"
recommended_model: sonnet
description: >
  Structured audit of a Meta Ads account setup. Two modes: API-driven (default when
  token available, factual data-backed audit) or declarative interview (fallback,
  operator answers questions or sends screenshots).
  FR: "audit meta", "vérifie mon setup meta", "check ma config meta", "audit setup meta".
  EN: "audit meta setup", "check my meta config", "meta ads audit".
permissions:
  reads: [brand]
  writes: [learning]
  mode: proposed
  subagent_safe: true
pipeline:
  preconditions: brands/{slug}/brand.json must exist
  postconditions: optional capture-learning for key findings with confidence ≥ 8
disambiguates_against:
  validate-resources: "route to validate-resources when operator says 'audit' or 'check' without a platform context — that's a workspace integrity check, not a Meta platform audit"
---

# Skill: audit-meta-setup

Senior media buyer account health check. Two modes based on API access. Observational findings, not blame. Zero questionnaire format when API is available.

## Expert methodology

**Canonical expert persona**: senior media buyer / account strategist with 10+ years on Meta Ads.

**Framework**: 5-block diagnostic covering pixel reliability, account structure, campaign architecture, catalog health, rules and safety.

**Matrix** (applied to each block): *finding status (OK / Warning / Issue) × operational impact × recommended action*.

**Key variables**: CAPI event received last 7d, event_id dedup rate, domain verification status, 8-event priority order, campaign-to-adset ratio, catalog sync freshness, policy flags count.

**Codified reference**: if `resources/conventions/meta-ads.json` missing or incomplete, Gate doc blocks execution until it is filled (rate limits, OAuth scopes, endpoint patterns, pitfalls).

---

## Step 0 — Gate access check (MANDATORY, before anything else)

**CRITICAL:** **YOU MUST** check Meta API access BEFORE starting the audit. **NEVER** fall back to a questionnaire silently.

1. Read `brands/{slug}/credentials.env` and `credentials_shared.env` (workspace root). Look for `META_ACCESS_TOKEN` (or equivalent per convention).
2. Read `resources/conventions/meta-ads.json`. Check scopes, endpoint patterns, rate limits. If incomplete or missing → Gate doc first (read official Meta doc via WebFetch, fill the convention) before any API call.

**Branching** (use AskUserQuestion for option presentation when token absent):

- **Token present + convention complete** → announce API mode, proceed to Step 1A:
  > *"API access OK for {brand}. I pull the data directly from Meta. 2-3 min, back with the audit."*

- **Token absent** → present the choice:
  > *"To audit your Meta setup I need API access. Two options:*
  > *(a) Walk you through generating a Meta System User token. ~5 min, one-time, audit becomes factual and future audits are instant.*
  > *(b) Declarative mode: I ask questions, you answer or send screenshots. Slower, depends on your memory."*

(a) → run setup flow, then Step 1A. (b) → Step 1B.

---

## Step 1A — API mode (default when token available)

Read `brands/{slug}/brand.json` for name, language, stage.

Pull from Meta Marketing API (respect rate limits in convention):

1. **Ad Accounts** — list, IDs, currency, owner
2. **Pixels + CAPI** — installed, CAPI events last 7 days, event_id dedup rate
3. **Domain verification** — verified domains at business level
4. **Standard events** — received last 28 days per pixel, volume per event
5. **Campaign structure** — campaigns by objective, ad sets, ads
6. **Catalog** — connected catalogs, product count, last sync, feed errors
7. **Attribution + iOS14 AEM** — 8-event priority, attribution window per campaign
8. **Account warnings** — policy flags, spending limits, identity confirmation

Deliver a factual audit: 5 blocks with **data-backed findings**. Each finding = status (OK / Warning / Issue) + what the data says + one-line operational impact. **NEVER** ask the operator questions the API already answered.

---

## Step 1B — Declarative mode (fallback only)

Announce the mode explicitly:
> *"Declarative mode. Structured questions on 5 areas. Answer what you know, skip what you don't, screenshots OK. The audit will be as reliable as your memory of the setup."*

Then proceed area by area, conversationally. **NEVER** a form, **NEVER** decorative ✓ bullets, **NEVER** dump all questions at once. One question per turn.

---

## Step 1 — Initialisation (applies to both modes)

Read `brands/{slug}/brand.json`. Extract:
- Brand name and positioning
- Language preference (FR/EN) — default FR
- Existing `platforms.meta` config (if any)
- Brand stage (new, piloting, scaling)

If brand.json is missing → gracefully stop and ask operator to create it first (`setup-brand`).

If `platforms.meta` exists, read current setup notes to avoid re-auditing known data.

---

## The 5 audit blocks

### Block 1 — Pixel and tracking

Verify:
- Meta pixel installed on all pages (Events Manager diagnostics)
- Conversions API (CAPI) active and receiving events server-side
- Standard events configured (ViewContent, AddToCart, InitiateCheckout, Purchase)
- Domain verified at Business Manager level
- Pixel + CAPI deduplication active (shared event_id)

### Block 2 — Account structure

Verify:
- Business Manager hygiene (users, assets, access levels)
- Ad account naming convention
- Custom audience creation and retention
- Lookalike sources (source quality signal)
- Catalog connected if ecommerce

### Block 3 — Campaign structure

Verify:
- Campaign count per objective (not too fragmented)
- Ad set per campaign (CBO vs ABO usage)
- Ads per ad set (too few → no learning phase exit, too many → budget fragmentation)
- Active vs paused ratio
- Campaign naming convention

### Block 4 — Catalog and dynamic ads

Verify (if catalog connected):
- Product count and last sync timestamp
- Feed errors or warnings
- Dynamic ads set up with audience signals
- Product sets and use cases

### Block 5 — Rules and safety

Verify:
- Account warnings or policy flags
- Spending limits configured
- Identity confirmation status
- Automated rules (budget, performance)

---

## Output format

Deliver findings per block. For each:

```
Block N — {name}

- {finding 1}: OK | Warning | Issue
  {what the data or answer says}
  Impact: {one-line operational consequence}
  Recommended action: {specific next step}

- {finding 2}: ...
```

Close with **priority action list** (top 5 by severity) and **archive** the audit at `brands/{slug}/audits/YYYY-MM-DD-audit-meta.md`.

## Optional post-audit

- If findings confidence ≥ 8 → trigger `capture-learning` automatically
- Critical findings (Issue severity) → append to `brands/{slug}/pending-validations.md`
