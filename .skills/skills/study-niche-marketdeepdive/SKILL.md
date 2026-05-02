---
name: study-niche-marketdeepdive
type: orchestrator
version: "1.0.1"
recommended_model: sonnet
reasoning_pattern: matrix-driven
matrix_mode: generating
consumes:
  - path: resources/frameworks/market-deepdive.md
    min_version: 1.0.0
  - path: resources/frameworks/vom-mining.md
    min_version: 1.0.0
description: >
  Niche / market strategic deep-dive. Long-running (~30-60 min). Studies
  market sizing, player landscape, structural trends, regulatory environment,
  capital flow, sophistication evolution, disruption signals. Produces a
  4-6 page strategic memo + structured mutations to brand.json#market.* and
  strategy.json constraints / annual_goals. Cited claims linked to corpus
  archive. Mandatory ticket for runtime > 10 min.
  FR: "deep dive le marché {niche}", "étude marché secteur", "audit stratégique de la niche", "memo stratégique {niche}".
  EN: "market deep dive {niche}", "strategic study {niche}", "what's happening in {niche}".
permissions:
  reads: [brand, product, profile, strategy, learning]
  writes: [brand, strategy, learning]
  emits_events: [coherence_check]
  mode: proposed
  subagent_safe: true
pipeline:
  preconditions: brand exists with at least brand.json filled. Ticket opened at start.
  postconditions: strategic memo archived in custom/market-memo/{date}.md, Layer A corpus archived in sources/marketdeepdive/, Layer B mutations to brand.json#market.* and strategy.json proposed, ticket closed, finalize-mutation-batch event emitted
disambiguates_against:
  mine-vom: "route to mine-vom when operator wants market customer voice (vernacular, white-spaces from forum/review verbatim) — that's qualitative; deep-dive is structural/strategic"
  watch-competitors: "route to watch-competitors when operator wants recurring creative monitoring of named competitors — different cadence, different output"
  mine-voc: "route to mine-voc when operator wants brand-bound customer voice"
---

## Tone

Strategic register, chairman-to-CEO. Synthesis-first. Prose-first per `docs/system/voice.md` and `snapshot-brand` Step 7 canon. The operator-facing surface is short, the memo carries the depth, the corpus carries the audit trail. Frameworks are vocabulary, never section headers.

The memo reads like a senior strategy consultant who has read twenty years of similar reports and knows that the implications-for-the-brand section is the only section the operator reads twice. Everything before exists to make that section non-trivial.

Anti-patterns banned:

- Porter as section template. *"## Porter's 5 Forces. 1. Rivalry: medium. 2. New entrants: high…"* is form-fill, not analysis. The memo never carries a heading named after a framework.
- PESTEL as six-paragraph form-fill. Six forces in a row is a checklist, not a strategic read. Two or three are load-bearing in any given niche; the rest get one line or are skipped.
- TAM numbers without source. Every number ships with a `[MKT-NNN]` corpus pointer or stays null. Fabricated precision is refused.
- Twenty-page memo. Cap is 3000 words. Long memos are rewritten tighter, not shipped long.
- Tactical drift. The skill reads the niche. Campaign angles, copy hooks, channel tests are out of scope and route to `analyze-perf`, `watch-competitors`, `routine-perf`.

---

## Expert methodology

The agent reasons as a senior strategy consultant with twenty years of pattern recognition across consumer categories. The frameworks below are applied selectively. The memo names the load-bearing forces and skips the rest explicitly.

Canon for the analytical vocabulary lives in `resources/frameworks/market-deepdive.md`. The skill consumes that framework, never duplicates it. Read it before drafting any layer.

Selectivity rules apply per layer:

- Porter — name the 1-2 active forces. Document which force was tested and rejected, in one line.
- PESTEL — name the 2-3 active forces. Document which were peripheral.
- Schwartz — read longitudinally (3 years ago, today, 3 years out), not as a snapshot.
- Crossing the Chasm — apply only when the niche is under 5 years old and category leader is unclear. Skip otherwise.
- Capital flow — always active. Strategic memos that ignore capital are tactical memos.
- Disruption — always active. Tech, demographic, regulatory shifts that reframe the niche in 12-24 months.

The synthesis layer is the only mandatory output. Frameworks supply vocabulary; synthesis supplies the verdict.

---

## Step 0 — Ticket open + first-party data ask

Runtime exceeds 10 minutes by design. Open a ticket immediately, before any research. Ticket discipline is non-negotiable per `brands/_TEMPLATE/tickets/README.md`.

Ticket creation:

```
Path: brands/{slug}/tickets/marketdeepdive-{YYYY-MM-DD}-{HHMM}.md
Owner skill: study-niche-marketdeepdive
Status: in-progress
Cost estimate: ~45 min wall-clock, ~100-200k tokens, ~30 web fetches
```

The ticket is the authoritative state. Operator interaction:

- *"où est le ticket marketdeepdive"* / *"where is ticket X"* → read the ticket, surface current state + log tail
- *"pause"* → status=paused, log timestamp, halt
- *"resume"* → status=in-progress, continue from last logged step
- *"close"* → status=closed (only after finalize-mutation-batch passes)

Then ask first-party data, plain prose:

> *"Avant que je lance une étude marché complète (45 min), est-ce que tu as :*
>
> *— des reports payants (Statista, Mintel, Euromonitor, NPD) à digérer ?*
> *— des notes prises en conférence sectorielle ?*
> *— des analyses internes ou strategy decks récents ?*
> *— des notes de calls investisseurs / strategy si pertinent ?*
>
> *Drop ici si oui — ça précise mon analyse de 30-50% et je peux gagner 10-15 min sur le scrape public."*

Branching:

- Operator drops first-party material → route to `ingest-resource` first, then resume here with the corpus enriched. Tag corpus entries `source_type=primary_data` for those sources.
- Operator says no / silence → public sources only, flag in memo header (*"sourcing limited to public corpus, no operator-supplied primary data"*).

Heavy-skill gate per `voice.md § Heavy skill posture`. The first-party ask doubles as the gate confirmation. Operator must say go before scraping starts.

---

## Step 1 — Niche definition lock

Read `brand.json#/meta/vertical`, `brand.json#/market/market_overview/category`, top product `spec.json#/identity/category`. Compose the precise niche tuple:

```
sector × sub-vertical × geography × (optional) price-tier
```

Worked examples:

- Skincare clean / FR / mid-premium 30-80€
- Supplement sleep / FR-EU / premium 25-50€
- Anti-age facial skincare cosmetics-grade / France-EU primary, US secondary

If any axis is ambiguous, ask one targeted question and stop. No deep-dive on a vague niche — the memo would be unreadable.

```
"Avant de lancer : tu vois le marché comme {niche tuple proposed}, ou tu coupes plus serré ({alternative axis})?"
```

Lock the tuple in the ticket log before continuing.

---

## Step 2 — Selective Porter analysis

Per `market-deepdive.md` framework, identify the 1-2 forces that are *actually active* in this niche. Document the binary tests that activated them.

For each active force, write a paragraph naming what the force implies for the operator's window. Skip the rest explicitly with one-line dismissals (e.g. *"Buyer power non-load-bearing — DTC commerce keeps power on the brand side; review density on price terms is low"*).

The substitute force is the one most often missed and most often load-bearing. GLP-1 took share from weight-loss supplements in 24 months. AI tutoring is taking share from Khan-style apps. Med-spa procedures are taking share from anti-age skincare in the >35 segment. Always test the substitute force explicitly.

Output of this step is internal reasoning material for Step 9, not a section in the memo.

---

## Step 3 — Player landscape mapping

Triangulated crawl, three paths:

- Crunchbase scrape on the top 10-15 players in the niche (funding history, employee count, revenue estimate, recent rounds)
- Listicle aggregation on industry press (*"best {category} 2026"*, *"top {niche} brands"*) — Modern Retail, Glossy, Business of Fashion, sector-specific trade outlets
- Marketplace top-sellers where applicable (Amazon, Sephora, iHerb)

Layer in:

- Press coverage on strategic moves last 18 months — Forbes, TechCrunch, Vogue Business
- Strategic acquirer activity (CPG conglomerates buying DTC, roll-up funds active in the segment)
- Public market signals (IPOs, public-private comparable acquisitions, trading multiples)

For each player on the final list of 12-15:

- Positioning summary in one sentence
- Channel mix estimate (DTC % / retail % / marketplace %)
- Two recent moves (last 18 months)
- Funding / M&A status

Aim 12-15 players. The hero map matters; the long tail does not. A list of 50 is research, not analysis.

Cache aggressively. Player landscape fundamentals don't shift weekly. TTL 30 days for funding/M&A, 90 days for industry reports, 7 days for breaking news. Cache path: `brands/{slug}/sources/marketdeepdive/_cache/`.

---

## Step 4 — Selective PESTEL

Per framework, identify the 2-3 forces actually reshaping the niche right now. Document binary tests.

Worked example for skincare clean FR 2026: Social (anti-age stigma vs aging-positive movement) + Technological (peptide synthesis at scale, GLP-1 spillover on skin) + Legal (EU 1223/2009 evolution, peptides ANSM consultation, PFAS) are dominant. Economic and Environmental get one line. Political is peripheral.

That selection *is* the analysis. Form-filling all six dilutes signal.

For each active force, write a paragraph naming the policy / trend / regulation, the detection signal, the 12-24 month outlook, the implication for the operator's brand specifically.

---

## Step 5 — Schwartz longitudinal sophistication

The most load-bearing layer for messaging strategy. Place the niche on the 1-5 stage axis at three anchors:

- Where it was 3 years ago
- Where it sits today
- Where it likely heads in 3 years

Cite a source for each anchor. The trajectory is what makes the analysis operational.

Worked example, skincare clean FR:

- 2020 — stage 3 (mechanism: *"what's not in it"*)
- 2023 — stage 4 (mechanism + dermo proof: *"clean and it works"*)
- 2026 — stage 5 (identity + lifestyle: *"clean is who I am, performance is assumed"*)

Audience awareness distribution feeds this layer mechanically and routes to `brand.json#/market/awareness_distribution/*`. In a stage-4 niche, the audience is mostly product-aware; in a stage-2 niche, mostly problem-aware.

The analytical question is not *"what stage is the niche"*, it is *"when does the next stage begin, and is the operator's current positioning ready"*. Saying *"performance prouvée"* in a niche that just crossed into stage 5 is two years late. Saying it in a niche still consolidating stage 3 is two years early. Timing is the strategic decision.

Worked example, nootropics: stage 2 in 2018, stage 3 in 2022, stage 4 in 2025. Stage 5 hasn't arrived; stack-rationale messaging still wins.

---

## Step 6 — Capital flow + exit comparables

Strategic memos that ignore capital are tactical memos.

Four signal types, captured with sources:

- Recent deals last 18 months — name, acquirer, target, disclosed multiple (revenue × N or EBITDA × N), strategic rationale where stated
- Funding rounds — Series A/B/C amounts, disclosed valuations, geography (FR/EU/US), investor pattern (sector specialists vs generalists)
- Public market signals — IPOs, secondary acquisitions, comparable trading multiples for category leaders
- Strategic acquirer activity — which CPG conglomerates, which roll-up funds, on what cadence

For each, surface multiples where disclosed. Three deals at 4-6× revenue in the same niche signals an active exit window for similarly-sized targets. One deal at 12× revenue with strategic synergy is a one-off, not a market multiple.

Implication for the operator is one of three reads:

- Window favorable for exit — preserve optionality, build clean financials, avoid debt that complicates a deal
- Window favorable for raise — sharpen the deck, name the comparables, target sector specialists
- Window favorable for scale-and-hold — operate for cash flow, take the long route, IPO threshold higher

The memo names which read applies and why, sized to the operator's revenue band. Exit comparables ship in the memo only — never written to the core schema.

---

## Step 7 — Disruption signals

Three buckets, each detected by signal density.

Tech disruption arrives 12-24 months ahead of consumer impact from labs and venture rounds. AI in skincare diagnostics. Biotech ingredient platforms. Detection signal is VC investment pattern, patent filing trends, conference keynote density. Binary test: is the signal already affecting top-three players' product roadmaps? If yes, it's no longer disruption — it's table stakes the operator needs yesterday.

Demographic disruption is slower but harder to escape. Aging Western populations. Gen-Z purchasing power shift. GLP-1 adoption reshaping nutrition adjacencies. Single-person households reshaping SKU sizes. Detection signal is multi-year cohort data, not press cycles.

Regulatory disruption is binary. Claim restrictions remove positioning angles overnight (FTC enforcement, EU 1223/2009 cosmetic claim tightening, Nutri-Score 2025 mandates, peptides ANSM consultation, PFAS bans). Advertising platform policy redefines acquisition economics. Detection signal is regulator consultation pages, enforcement action density, platform policy update frequency.

For each signal flagged, the memo answers two questions: what is the brand's current exposure, and what protects it (IP, supply chain, customer lock-in, brand equity that survives the disruption). A signal without an exposure read is observation, not analysis.

---

## Step 8 — Strategic implications synthesis

The only mandatory output. Three questions answered:

1. **What positioning is durable for 24 months, what is commoditized in 12?** Anchor in Schwartz trajectory + selective Porter (substitute threat especially) + capital flow. Name the angles to defend, the angles to exit, the angles the operator could newly own.
2. **What capital window matters — exit, raise, or scale?** Name which read applies, sized to the operator's revenue band, with comparable precedents from Step 6. If no window is open, say so plainly.
3. **What disruption is the brand exposed to, what protects it?** Name the two or three disruption signals from Step 7 that hit this brand specifically, the exposure path, the structural protection or its absence.

End with one primary strategic bet, two-to-three secondary bets, recommended cadence to revisit. This section reads as prose, not as a bullet recap of framework layers.

---

## Step 9 — Memo writing

Write the memo to `brands/{slug}/custom/market-memo/{YYYY-MM-DD}-{niche-slug}.md`. Hard cap: 3000 words / ~6 pages.

The memo is NOT a Porter / PESTEL / Schwartz section template. Each paragraph is named by what it carries, not by which framework supplied the vocabulary. Worked structure follows the deepening-skills research brief 03 example:

- **Opening paragraph — market structural shift.** Names the dominant structural read in 2-3 sentences. Cites sources. *"Le marché skincare clean FR a basculé en 2024-2025 d'un marché positionnement-driven vers un marché performance-driven [MKT-003, MKT-007, MKT-012]…"*
- **Player landscape paragraph.** Top 3-5 named players, recent moves, consolidation read. *"Caudalie acquise à 65% par L'Oréal (deal 280M€) [MKT-018], Typology Series C 60M€ chez Eurazeo [MKT-021], Endro acquise 80% [MKT-023]. La cohorte indépendante restante FR — Respire, Aime, Oden, Sabé Masson — se réduit chaque trimestre."*
- **Forces shaping next 18 months paragraph.** 1-2 Porter + 2-3 PESTEL applied selectively, prose-form, named not numbered.
- **Capital window paragraph.** Multiples cited, exit/raise/scale read named, sized to operator band.
- **Disruption signals paragraph.** Tech + demographic + regulatory signals flagged, exposure named, protection named.
- **Strategic implications paragraph for THIS brand.** 3 bets prioritized — one primary, two secondary. The section the operator reads twice.

Every claim cites a `[MKT-NNN]` corpus pointer. The `finalize-mutation-batch` gate enforces this — any numeric or factual claim without a pointer blocks ship.

If the draft runs longer than 3000 words, rewrite tighter. Operators do not read consultant decks.

Memo header carries a privacy flag:

```yaml
---
_private: true
_skill: study-niche-marketdeepdive
_run_date: {YYYY-MM-DD}
_niche: {niche tuple}
_sources_count: {N}
---
```

`_private: true` flags the memo for non-sharing. The memo lives under `custom/market-memo/` and is regenerable. It is logged in `{entity}.extensions.json` per `docs/system/extending.md`.

---

## Step 10 — Surface synthesis

Per `snapshot-brand` Step 7 canon, the operator-facing surface is a 4-line synthesis pointing to the memo. Pure prose. No bullet list. No bold section labels. No technical fields.

```
Mémo stratégique livré pour {niche}. {1-2 sentences naming the dominant structural read with the strongest single insight}. Ton créneau {brand} est {durable / exposé} sur {N} mois si tu pivotes {direction maintenant} ; après, {what closes the window}. Memo complet dans brands/{slug}/custom/market-memo/{date}.md — N pages, M sources citées.

Want to read the full memo, or drill into a specific layer (player landscape / regulatory / disruption / strategic implications)?
```

Worked example, Respire on skincare clean FR:

> *Mémo stratégique livré pour clean beauty FR. Le marché est en consolidation accélérée — 3 deals M&A >50M€ en 2025, exit multiples 4-6× revenue, sophistication stage 5 atteint, le clean comme positionnement seul ne tient plus 18 mois. Ton créneau Respire (clean + performance dermo + pregnancy-safe) est défendable sur 12-24 mois si tu pivotes la communication maintenant ; après, fenêtre fermée par Caudalie qui a déposé 4 brevets bakuchiol-like en 2025. Memo complet dans brands/respire/custom/market-memo/2026-04-25.md — 6 pages, 23 sources citées.*
>
> *Want to read the full memo, or drill into a specific layer (player landscape / regulatory / disruption / strategic implications)?*

Hard rules for the surface (inherited from `snapshot-brand` Step 7):

- Pure prose, no bullets, no bold section anchors, no field enumeration
- Never name a path other than the memo destination
- Never expose `source`, `confidence`, `mode`, or any internal field path
- 4 lines plus the drill-down question. If the synthesis runs longer, rewrite.

---

## Step 11 — Routing to entity files (Layer B)

Field updates routed via `python3 .skills/write-to-context.py` with `mode=proposed` for every numeric or structured claim. Plumbing destinations:

- `brand.json#/market/market_overview/sophistication` — proposed update with trajectory note
- `brand.json#/market/market_overview/awareness_distribution` — % per stage if computable
- `brand.json#/market/market_overview/size_estimate` — TAM/SAM/SOM with confidence_signal, only if sourced
- `brand.json#/market/market_overview/growth_rate` — historical CAGR + projected, sourced
- `brand.json#/market/regulatory/upcoming_changes[]` — append entries for forthcoming regulations
- `brand.json#/market/regulatory/active_regulations[]` — append entries currently enforced
- `brand.json#/market/competitors[]` — enrich existing entries (positioning, recent moves, channel_mix), add missing players up to 12-15 total
- `brand.json#/market/external_intelligence[]` — append-only sourced signals (type=trend, type=competitor_move, type=demand_signal, type=category_shift, type=m_a)
- `strategy.json#/constraints[]` — consolidation_risk verdict (acquirer / target / neutral / roadkill), positioning_durability verdict (durable / eroding / dead), regulatory or capital flow constraints
- `strategy.json#/annual_goals[]` — propose 1 primary + 2 secondary bets (operator confirms before merge)
- `learnings.json` append — 3 strategic takeaways flagged by `learn-from-session`

Layer A corpus archive at `brands/{slug}/sources/marketdeepdive/{YYYY-MM-DD}-{run_id}/corpus.jsonl`. Every entry:

```json
{
  "id": "MKT-001",
  "source_type": "industry_report|press_article|crunchbase_player|analyst_post|forum_thread|conference_transcript|regulator_bulletin",
  "source_url": "https://…",
  "captured_at": "2026-04-24T14:32:00Z",
  "claim": "Anti-age skincare TAM EU = €18.4B in 2024, CAGR 4.2% projected through 2028.",
  "confidence_signal": "primary_data|secondary_estimate|opinion",
  "topic": "market_size|player_landscape|regulation|tech_disruption|m_a|demographic_shift|capital_flow",
  "layer": "0|1|2|3|4|5|6"
}
```

Plus cached HTML/PDF in `_cache/` if license-permitted. The corpus is private to the brand; never surfaces in the operator-facing memo as a list.

Memo destination: `brands/{slug}/custom/market-memo/{YYYY-MM-DD}-{niche-slug}.md`. Regenerable, archived, logged in `{entity}.extensions.json`.

Mutation discipline per root `CLAUDE.md`:

- Never call `write_to_context` on a whole file path with `mode=proposed`. Scaffold in `mode=direct` first, stamp inferred fields one by one with JSONPointer fragments.
- Never `Edit` / `Write` directly on `brands/*.json`. Mutation gate is non-optional.
- After any write under `brands/{slug}/custom/` or `{entity}.extensions.json`: trigger `validate-resources` silently. Flag MAJOR/CRITICAL.
- After any write to core files: rebuild snapshot via `python3 .skills/build-brand-snapshot.py {slug}`.

---

## Step 12 — Finalize + close ticket

Before any operator-facing summary, run the mutation gate. Mechanical, non-skippable:

```bash
python3 .skills/finalize-mutation-batch.py --brand-slug {slug}
```

The gate inspects every mutation written in this run, checks `_field_types`, flags unmapped paths, manual derived writes, tone misclassification, and most importantly here: any numeric or factual claim in field updates that does not trace to a `[MKT-NNN]` corpus pointer. Exit code 2 = blocking issue. Revise before shipping.

The soft-prescribed `validate-output-coherence` LLM call is not used here — it was skipped 100% of the time under load on the v2.7.1 stress test. `finalize-mutation-batch` is the replacement, mechanical, no negotiation, no skip path.

Once the gate passes:

- Close the ticket. Status = closed. Output paths cited. Last-update timestamp.
- Trigger `learn-from-session` with 3 strategic takeaways flagged for `learnings.json` (typically: a market structural read, a capital window read, a disruption exposure read).
- If the operator opted into auto-prompt cadence, append a re-run reminder to `pending-validations.md` at 9 months out.

Ship the operator-facing surface from Step 10 only after the gate has passed and the ticket is closed.

---

## --focus parameter modes

The skill accepts a `--focus` flag for narrower runs. Each mode is shorter (1-2 pages), faster (15-25 min), still archived as a memo under `custom/market-memo/`, still gated by `finalize-mutation-batch`.

| Mode | Scope | Layers active | Skip |
|---|---|---|---|
| **default** | Full strategic memo | 1-8 | none |
| `--focus=player-landscape` | Top 12-15 players + recent moves + consolidation read | 3 | macro forces, regulatory, disruption |
| `--focus=regulatory` | Active + forthcoming regulations + claim survival analysis | 4 (Legal subset) + Step 7 regulatory bucket | player landscape, capital, demographic |
| `--focus=exit-comparables` | M&A multiples + funding rounds + public comps + window read | 6 | Porter, PESTEL, Schwartz, disruption |
| `--focus=disruption` | Tech + demographic + regulatory shifts + 12-24 month outlook + brand exposure | 7 | player landscape, capital flow, sophistication |

Operator triggers focus mode with phrasing like *"étude marché — focus régulation seulement"* or *"deep dive {niche} mais juste les exit comparables"*.

The synthesis surface (Step 10) adapts: the drill-down question lists only the layers covered, the memo header notes the focus mode.

---

## Hard Rules

- **Mandatory ticket lifecycle.** Runtime > 10 min. Ticket opened at Step 0, closed at Step 12. Operator interaction surfaced via `pause / resume / close / where is ticket X`. Never run without a ticket.
- **First-party data ask non-negotiable** at Step 0. Operator branches the run; agent does not silently default to public sources without surfacing the ask.
- **Frameworks consumed from `resources/frameworks/market-deepdive.md`**, never duplicated, never applied as section headers in the memo. Porter / PESTEL / Schwartz / Crossing-the-Chasm names appear as analytical vocabulary in prose, never as `## H2` markdown headings.
- **Selective Porter — 1-2 forces.** Selective PESTEL — 2-3 forces. Document the rejected forces in one line each. Form-filling all six is a doctrine violation.
- **Every claim sourced.** Numeric or factual claim in the memo carries a `[MKT-NNN]` corpus pointer. `finalize-mutation-batch` blocks any unsourced number in field updates. Null > invention.
- **Memo cap 3000 words / 6 pages.** Drafts running long are rewritten tighter, not shipped long.
- **Synthesis surface 4 lines max** + memo pointer + drill-down question. Pure prose. No bullets, no bold section labels, no technical fields exposed.
- **Cache aggressive.** TTL 30 days for funding/M&A trackers and player landscape, 90 days for industry reports, 7 days for breaking news. Niche fundamentals don't shift weekly.
- **`finalize-mutation-batch` mandatory before ticket close.** Mechanical Python primitive. Exit code 2 blocks ship. Non-skippable.
- **Re-run cadence — every 6-9 months max.** If the skill detects a prior run on the same niche < 6 months old, surface: *"Marché ne bouge pas si vite — le mémo {date} couvre déjà cette niche, confirme rerun ou skip"*. Auto-prompt at 9 months in `pending-validations.md`. Hard nudge at 12 months.
- **Privacy.** Memo carries `_private: true` in its header. May contain sensitive competitive intel (deal multiples, exposure reads, internal positioning verdicts). Never auto-shared, never exported to `sources/` (which is auto-loaded under some triggers).
- **Mutation gate non-optional** per root `CLAUDE.md`. No `Edit` / `Write` on `brands/*.json`. All mutations through `write_to_context` with `mode=proposed`. `validate-resources` silent post-write. `build-brand-snapshot.py` after any core file write.
- **Scope discipline.** This skill reads the niche. Customer voice routes to `mine-voc` (own customers) or `mine-vom` (category customers). Tactical execution — channel tests, creative angles, copy hooks — routes to `analyze-perf`, `watch-competitors`, `routine-perf`. When the memo starts critiquing the operator's product copy or proposing campaign angles, scope has drifted.
- **Plumbing leak ban.** Operator-facing surface never exposes `source`, `confidence`, `mode`, field paths, JSONPointer syntax, or skill names. Operator verbs: accept / reject / correct / flag. Per `voice.md § Plumbing leak to operator`.
- **Heavy-skill gate** per `voice.md § Heavy skill posture`. Surface plan + cost estimate + scenario before launching the cascade. The Step 0 first-party ask doubles as the gate.

---

## Cross-references

- `resources/frameworks/market-deepdive.md` — analytical canon (Porter, PESTEL, Schwartz, Crossing-the-Chasm, capital flow, disruption signals). The skill consumes this framework, never duplicates it.
- `.skills/skills/snapshot-brand/SKILL.md` — voice canon for the surface synthesis (Step 7 Movement structure, prose-first, anti-form-fill rules).
- `.skills/skills/mine-vom/SKILL.md` — sister skill on category-level customer voice. Complementary, not substitutable. mine-vom = qualitative voice; study-niche-marketdeepdive = structural / strategic.
- `.skills/skills/mine-voc/SKILL.md` — brand-bound customer voice. Out of scope here.
- `.skills/skills/watch-competitors/SKILL.md` — recurring creative monitoring on already-known competitors. Different cadence, different output.
- `brands/_TEMPLATE/tickets/README.md` — ticket lifecycle pattern (mandatory for skills > 10 min runtime).
- `.skills/finalize-mutation-batch.py` — Step 12 mutation gate primitive. Mechanical, non-skippable.
- `.skills/write-to-context.py` — canonical mutation channel. `mode=proposed` for every claim, JSONPointer fragments only.
- `.skills/build-brand-snapshot.py` — post-write digest refresh on core files.
- `docs/system/contextual-intelligence.md` — master doctrine. Two-tier rule (mechanical strict, semantic trust). The skill operates at the semantic layer: trust the model's reasoning across Schwartz / Porter / PESTEL / sophistication calls; enforce strict at the mechanical layer (mutations, paths, ticket lifecycle, gate).
- `docs/system/voice.md` — register, anti-patterns, heavy-skill gate, plumbing leak ban.
- `docs/system/extending.md` — custom entity logging in `{entity}.extensions.json`.
- `docs/system/field-types.md` — `observed | stated | derived | structured`. Sourced corpus claims = observed. Synthesized verdicts (consolidation_risk, positioning_durability) = structured. Never derived (this skill never computes).
- `docs/system/skill-creation-protocol.md` — heavy-skill gate, graduation matrix.
