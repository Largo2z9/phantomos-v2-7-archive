---
name: mine-voc
type: producer
version: "1.0.2"
isolation_scope: brand_only
layer: 2
recommended_model: sonnet
reasoning_pattern: matrix-driven
matrix_mode: coding
consumes:
  - path: resources/frameworks/voc-coding.md
    min_version: 1.0.0
description: >
  Voice of Customer mining. Captures what real customers say about THIS brand
  from native review widgets, Trustpilot, Reddit threads, app stores, forums.
  Codes verbatim through 4 lenses (JTBD, Schwartz awareness, theme typology,
  pain category). Produces a synthesis paragraph naming what the customers
  reveal that the brand likely does not see, plus structured mutations into
  spec.json verbatim_quotes[] and profile.json voice.key_expressions[].
  FR: "voc {brand}", "scrape les avis", "mine les reviews", "extrais ce que disent les clients", "voice of customer".
  EN: "voc {brand}", "mine reviews", "voice of customer", "scrape customer reviews".
permissions:
  reads: [brand, product, profile]
  writes: [brand, product, profile, learning]
  emits_events: [coherence_check]
  mode: proposed
  subagent_safe: true
pipeline:
  preconditions: brand exists with at least brand.json filled (run setup-brand + snapshot-brand first)
  postconditions: synthesis delivered, Layer A corpus archived in sources/voc/, Layer B mutations proposed, finalize-mutation-batch event emitted
disambiguates_against:
  mine-vom: "route to mine-vom when operator wants market-level voice (competitors, niche communities), not brand-bound customer voice"
  mine-audience: "route to mine-audience when operator wants product-level audience discovery from scraping, not review verbatim mining"
  ingest-resource: "route to ingest-resource when operator drops a single document/CSV — that's a one-off ingest, not a multi-source mining session"
  watch-competitors: "route to watch-competitors when operator wants recurring monitoring of competitors' paid creatives, not one-shot customer voice"
---

# mine-voc

Mine Voice of Customer for an existing brand. Read what the brand's actual customers say across the surfaces where they leave traces, code each verbatim through four established lenses, deliver a synthesis paragraph that names what the brand likely does not see, route the structured findings into existing entities. One brand per invocation. One snapshot in time. The corpus stays as audit substrate; the synthesis is what the operator uses.

---

## Tone

Strict synthesis-first. Prose-first. Voice canon strict — three movements of plain prose at Step 5, blank line between each, no titles, no bold-section anchors, no field enumeration, no numbers exposed unless load-bearing, no internal vocabulary leaked. The synthesis IS the analysis; it is not a recap of what was scraped.

The Step 5 output follows the snapshot-brand Step 7 canon exactly. Read `.skills/skills/snapshot-brand/SKILL.md § Step 7` and apply its decisive test verbatim before sending: if the output carries bold section labels, numbered headings, "X themes detected" enumerations, or `Field. content.` templated openers, the skill reverted to form-fill and must rewrite.

The corpus volume, the source split, the coding distribution — none of these are operator-facing. They live in Layer A. The operator sees the read, not the inventory.

Anti-pattern bans, non-negotiable.

- No form-fill recap of the form *"I scraped 247 verbatims, identified 12 themes, 5 pain points, 8 objections, 6 audience signals"*.
- No bold-section anchors marking movements.
- No exposed scores, confidence numbers, or coding distribution percentages.
- No internal field paths (`spec.json#problems_solved[].verbatim_quotes[]`) named in the operator surface.
- No platform names listed as a tally (*"Trustpilot: 89, Judge.me: 234, Reddit: 12"*) — provenance shows up only when an asymmetry is the finding.
- No marketing language. Banned vocabulary: supercharge, unlock, empower, leverage, optimize, transform, journey, deep-dive.

---

## Expert methodology

Persona for this skill: senior consumer insights consultant who has read every Trustpilot review on the brand, cross-referenced the Judge.me hero against the Reddit threads naming the brand by name, checked Sephora cross-listings if relevant, and is now sitting across from the operator with one read, two corrections to the brand's stated audience, and one channel opportunity the operator has not surfaced. Not a researcher dumping data. The synthesis is what the operator pays for; the corpus is the substrate that backs every line.

Framework: four lenses applied sequentially per verbatim. Theme typology first (filters the corpus and decides which other lenses run), JTBD second (frames what the customer hired the product for), Schwartz awareness third (depends on vocabulary surfaced in the previous two), pain category fourth and only conditionally on theme = pain. The coding canon is `resources/frameworks/voc-coding.md`. The skill consumes that file; it does not improvise the lenses, does not invent themes outside the closed typology, does not promote singletons to claims.

The triangulation rule from snapshot-brand carries through unchanged. A pattern earns Layer B status when at least three distinct verbatims across or within sources name a close variant of the same thing. Singletons stay in Layer A as evidence; they do not become claims. A four-source convergence on a single signal is a stronger finding than fifty verbatims on one platform — provenance is named when the asymmetry is the read.

Sample before exhausting. When the available corpus exceeds 200 verbatims, code 50 randomly sampled entries first, check whether the coding distribution matches the brand's stated profile, and only run the full pass if the sample shows divergence. This is the validation-cascade-avoidance rule from `docs/system/contextual-intelligence.md` applied to coding: do not run all four lenses on every verbatim before talking to the operator if a sample answers the synthesis question.

---

## Step 0 — First-party data ask (mandatory)

Before scraping anything public, ask the operator. Verbatim:

> *"Avant que je scrape les avis publics, est-ce que tu as :
> - Un export de tes reviews Shopify (CSV) ?
> - Un dump Klaviyo de tes campagnes feedback / NPS ?
> - Des transcripts de support client ?
> - Des résultats de sondage ou enquête client récente ?
> - N'importe quoi de first-party, format libre.
>
> Si oui, drop ici, je le digère en priorité.
> Si non, je pars sur les sources publiques (Trustpilot, Reddit, app stores)."*

Two branches.

**First-party material provided.** Route through `ingest-resource` first to digest the file. The first-party corpus becomes the primary evidence; the third-party scrape that follows runs as cross-validation, not as primary signal. First-party data is denser, less biased, and reflects the buyers the brand actually sells to — not the angry-Trustpilot-leaver minority.

**No first-party.** Proceed to Step 1 with public sources only. Flag the limitation in Step 5 prose, woven into the synthesis: *"Synthèse basée sur sources publiques uniquement. Si tu as des données first-party, on peut affiner."* — never as a separate disclaimer block.

This step is non-negotiable. A skill that scrapes Trustpilot before checking whether the operator has a Klaviyo export with 5000 NPS responses is incompetent. First-party data, when available, is the strongest signal the brand owns.

---

## Step 1 — Source detection and crawl plan

Read `brand.json`. Extract the brand domain, Shopify handle, social handles, marketplaces in `external_ids`, Google Business name. Build the surface inventory.

Available review surfaces, in order of typical density:

- Native review widgets on the brand site — Shopify Product Reviews, Judge.me, Loox, Okendo, Yotpo, Stamped. JS-rendered, requires Chrome MCP capture; static WebFetch returns empty review blocks. Highest density on most Shopify DTC brands.
- Trustpilot if the brand has a profile (`trustpilot.com/review/{domain}`).
- Sephora, Mecca, Marionnaud, Amazon, retail-marketplace cross-listings if the brand sells through them.
- Reddit threads naming the brand or a product by name (search via `site:reddit.com {brand}` plus the niche subreddits the brand's audience inhabits).
- App Store / Play Store reviews if a companion app exists.
- YouTube comments under brand-channel videos and under reviewer videos that name the brand.
- Brand support forum or Discord if accessible.

Output the crawl plan to the operator, one declarative sentence per source. Format: *"Je vais lire ton Judge.me, Trustpilot, et trois threads Reddit qui nomment la marque. Démarre dans 30 secondes."* — no menu, no enumeration of platforms operator has not heard of, no mention of file paths or field names. The plan is binary: surfaces named, run.

Triage probe before deep crawl. For each surface, run a cheap WebFetch or API call to count visible reviews. Three buckets. Dense (>50 verbatims accessible) — sample with quotas per theme. Thin (5-50) — exhaust. Absent (0 or paywalled) — note silently and move on. The triage prevents spending a 30-minute budget on a surface that returns 3 reviews.

---

## Step 2 — Crawl with rate-limit and provenance

Each verbatim captured with full provenance — non-negotiable. The corpus is audit material; an unsourced quote is unusable downstream.

Required fields per verbatim, captured at extraction time:

- Source platform (enum: trustpilot, judge_me, loox, okendo, yotpo, shopify_native, sephora, amazon, reddit, twitter, youtube_comments, tiktok, instagram, app_store, play_store, support_export).
- Source URL or platform-specific reference ID.
- Captured timestamp (ISO 8601).
- Rating if surfaced (1-5 scale; null if the platform does not expose rating).
- Verified-buyer flag if surfaced (true / false / null).
- Raw verbatim text — no paraphrase, no cleanup beyond whitespace normalization.
- Anchor product slug — which SKU the verbatim concerns (null if brand-level).
- Language detected.
- Username retained for first-party data (operator's own export); anonymized for third-party (replaced with `anon_{nano_id}`).

Rate-limit handling: exponential backoff per source, max 3 retries, then skip the surface and continue. 403 / captcha → log surface as `inaccessible` in the run report, do not block. Empty surface → note silently in the run report, do not fabricate. Imported-but-unverifiable widget content (Judge.me / Loox import features) → tag `verified_buyer: false` with `provenance_note: "displayed on-site, source unverifiable"` and downweight in frequency counts.

Caps. 200 verbatims per source maximum at default depth; 1000 verbatims total maximum across all surfaces. Larger corpora require operator-explicit `--depth=deep` flag. The cap exists because a 5000-verbatim corpus does not produce a 25× better synthesis than a 200-verbatim sample — diminishing returns hit hard around the third source.

Cache by `domain × week` to avoid re-scraping the same surface within seven days of a prior run. Documented per platform in `resources/conventions/{platform}.json`.

---

## Step 3 — 4-lens coding per verbatim (+ canon tagging v2.26.0+)

> **Atlas refs** dans cette skill = atlas canon copy (sense 1, référentiel cross-brand doctrine copywriting). Brand-side enrichment via `validations[]` (sense 2 atlas vivant). Distinct de l'atlas brand (sense 4, cartographie holistique data brand) qui désigne la matière brand structurée navigable via `/phantom`. Pour la distinction lexicale complète : `lexicon.md § Atlas, 4 senses MECE`.

<!-- v2.29.0 alignment verify : awareness_stage rename in angle.lineage. Canon tagging field names unchanged (point vers fiches canon copy). Layer A `awareness_stage` field already aligned with `_shared/awareness-stage.json` $ref (5 valeurs canoniques `unaware | problem_aware | solution_aware | product_aware | most_aware`). -->


Apply `resources/frameworks/voc-coding.md` strictly. The order is the order; do not reshuffle.

**Canon tagging additif.** Depuis v2.26.0, chaque verbatim qui passe le coding (i.e. propage à Layer B) est aussi tagué selon les outils canon copy pertinents. Cela enrichit la map et débloquera plus tard les vues `copy-matrix audience × stade-conscience`. Les tags canon ajoutés au verbatim Layer B :

- `canon_schwartz_conscience_id` : un parmi `unaware | problem_aware | solution_aware | product_aware | most_aware` (cohérent avec le coding lens 3 ci-dessous, nommé par référence à `canon copy niveaux-schwartz conscience`).
- `canon_emotion_id` : un terme issu du vocabulaire émotion canonique (espoir, peur, frustration, culpabilite, soulagement, fierte, envie, indignation, surprise, mefiance-eveillee, complicite, regret-anticipe, reconnaissance, appartenance, volonte). Si le verbatim ne porte pas d'émotion claire, laisser null.
- `canon_objection_pattern_id` (uniquement si theme=objection) : un parmi les 4 patterns canon `feel-felt-found | reframe-positif | pre-emption | comparaison-cout-inaction` selon ce que la résolution implicite du verbatim suggère. Souvent null en mining (l'objection est posée, pas encore résolue).

Ces tags sont écrits sur le verbatim dans le Layer A jsonl (`brands/{slug}/sources/voc/{run-date}/{platform}.jsonl`) et utilisés en Step 6 pour informer les routes Layer B.

1. **Theme typology first.** Assign one or many themes from the closed list of seven (pain, benefit, objection, comparison, surprise, vocabulary, social-proof-signal). A verbatim that matches none stays in Layer A as raw evidence and does not propagate to Layer B. Multi-theme is normal — *"le produit est top mais la livraison est catastrophique"* carries benefit (product) plus pain (operational).

2. **JTBD second.** If the verbatim names a job the customer hired the product for, code along three independent dimensions: functional (mechanical change in physical state, time, output, behavior), emotional (internal state the purchase resolves), social (position relative to others the purchase secures). Each dimension is coded only if the language supports it; absence of mention is absence of evidence. Stay in customer voice — if the verbatim only restates a brand claim, JTBD is null.

3. **Schwartz awareness third.** Single value from the five-stage ladder, picking the highest stage the verbatim demonstrates. Most-aware (names the brand or a specific SKU and discusses repurchase, format, or offer terms) → product-aware (names two or more competing branded products) → solution-aware (names the solution category without naming brands) → problem-aware (names the problem state without a solution category) → unaware (downstream symptom, problem unframed). Promotion of a verbatim above the stage its vocabulary supports is back-projection — refused.

4. **Pain category fourth, conditional.** Run only if a theme codes as pain. Tag each category the verbatim explicitly names; multi-category is normal. Functional (product does not deliver the mechanical outcome), emotional (internal state persists or worsens), social (perceived position vs others), financial (absolute cost or value-for-money), temporal (time-to-result, timing-of-purchase, duration-of-use), relational (frictions with another person triggered by purchase or use). The financial-versus-value-perception split is the most consequential miscode — *"c'est trop cher"* alone is financial, *"pour ce que c'est, c'est trop cher"* is value-perception. Code both when ambiguous; the synthesis flags the ambiguity rather than collapse it.

Coding model: Sonnet for v1.0 — JTBD and Schwartz coding quality is the load-bearing factor and Haiku has not been validated yet. A/B test Haiku 4.5 on a 50-verbatim corpus in v1.1 before downgrading.

Layer A entry shape, written to `brands/{slug}/sources/voc/{YYYY-MM-DD}/{platform}-{anchor}.jsonl`, one entry per line:

```json
{
  "id": "VOC-{platform}-{nano_id}",
  "captured_at": "2026-04-24T14:32:00Z",
  "source_platform": "trustpilot",
  "source_url": "https://www.trustpilot.com/review/example-brand.com/123456",
  "anchor_product_slug": "respire-sticks-deo",
  "rating": 2,
  "verified_buyer": true,
  "verbatim": "<exact text, no edits>",
  "language": "fr",
  "themes": ["pain.functional", "objection.efficacite"],
  "jtbd": {"functional": "regained morning routine", "emotional": null, "social": null},
  "awareness_stage": "product_aware",
  "pain_category": ["functional"],
  "audience_signals": {"demographic_clues": ["mention of 'mes enfants'"], "register": "casual"},
  "competitor_named": null,
  "brand_vs_product": "product"
}
```

Batch coding in groups of 30-80 verbatims per pass to keep token usage bounded. Sample first when corpus exceeds 200 (see § Expert methodology).

---

## Step 4 — Pattern detection and gap analysis

After coding, four reads run on the corpus.

**Recurring themes.** A theme reaches Layer B status when at least three distinct verbatims (across or within sources) carry close variants of it. Cluster on JTBD, pain category, and theme + sub-axis. Singletons stay in Layer A as audit material; they do not become claims.

**Brand-stated vs customer-said gaps.** Compare `brand.json#positioning`, `brand.json#tone_of_voice`, and `brand.json#identity` claims against the dominant verbatim themes. The brand says X — do customers actually mention X, or do they talk about Y? Compare each `audiences/{slug}/profile.json#identity` against the demographic clues and registers surfaced in coding. Every contradiction is a load-bearing finding — the operator paid for snapshot's hypothesis, the customers either ratified it or invalidated it. Synthesis surfaces the contradiction explicitly, never silently overwrites.

**Audience signals.** Demographic clues, life-stage references, professional context, language register. When a coherent cluster shows up that is distinct from the existing audience folders (a B2B sub-segment in a B2C brand's reviews, a 22-32 sub-cohort in a brand targeting 35-50, a male buyer pattern in a female-positioned brand), propose a new audience candidate with `validation_status: "hypothesis"` and `_source_meta.origin: "voc-mining"`.

**Vocabulary patterns.** Recurring expressions, vernacular phrasings, customer-voice anchors. These feed `profile.json#voice.key_expressions[]`. Two filters apply. First, distinguish vernacular from brand-jargon-echoed-back — *"actifs naturels"* repeated in customer reviews is the brand's positioning vocabulary returned, not customer voice. Tag it as benefit-claimed, not vocabulary. Second, frequency without sample_size is meaningless; the schema enforces the denominator (e.g. `frequency: 47, sample_size: 89, platform: trustpilot`).

**Channel signals.** Sources that surfaced the brand organically (Reddit threads, niche-forum mentions, YouTube reviewer pieces) are channel hypotheses. A 47-upvote thread on r/Skincareaddiction naming the brand as *"ce que j'aurais voulu trouver plus tôt"* is an untapped acquisition signal — the brand has organic resonance in a community it has not activated in paid. These route to `learnings.json` as channel-opportunity entries when the operator validates them at Step 5 close.

---

## Step 5 — Operator-facing synthesis (mandatory format)

Apply the snapshot-brand Step 7 canon strictly. Pure prose, three movements, blank line between each, no titles, no bold-section anchors, no enumeration, no scores, no "X themes detected", no platform tally.

**Movement 1.** What the customers reveal about who they are and why they buy. Often diverges from the brand-stated audience. Name the divergence in the first or second sentence — that is the headline. Use the JTBD and Schwartz coding as raw material; do not name the framework. A reader should leave Movement 1 knowing who actually buys and what they hired the product for, in customer voice, not in brand voice. 1-3 sentences.

**Movement 2.** What customers say about the product and the offer that the brand does not claim, or claims differently. The brand-stated-vs-customer-said gap from Step 4 lands here. If the brand communicates performance and customers buy softness, this is where it surfaces. If the offer architecture suggests one thing and the verbatims reveal another, this is where it surfaces. Use comparison-vs-competitor and benefit-perceived-vs-claimed coding as raw material. 1-3 sentences.

**Movement 3.** The one or two things the operator likely did not see. Channel opportunity (organic resonance in an unactivated community), dissonant signal (a pattern that contradicts brand identity in a way the brand can lean into), ops gap (a recurring delivery / packaging / support flag distinct from the product itself), regulatory or trust signal (a third-party-named concern the brand should know about). The skill is paid for these. 1-3 sentences.

End with a closing line, prose-form, conditional on what was surfaced:

> *"Want to validate and route these signals into the brand context, or keep digging?"*

Hard rule, restated: never list "themes detected", "verbatims captured", "platforms scraped", "patterns identified", "audiences found" as numbers. The synthesis IS the analysis. The corpus volume lives in Layer A — the operator can audit it on demand, never as default surface.

If sources were thin or inaccessible, weave the limitation into the synthesis prose: *"Trustpilot returned 0 reviews — ta marque n'est pas encore indexée là-bas, ce qui colore le read"*. Never as a separate "data quality" block.

Decisive test before sending. Read the synthesis as a stranger. If it carries bold section labels, numbered headings, *Field. content. Field. content.* templated openers, or any enumeration of internal structure (`coded 247 verbatims`, `12 themes detected`, `4 audience signals`), the skill reverted to form-fill. Rewrite as flowing prose where each paragraph names what it carries via its first sentence, not via a label above it.

---

## Step 6 — Routing into entity files (Layer B)

Based on patterns confirmed at Step 4, propose mutations through the canonical channel. All writes are `mode=proposed`; nothing direct.

`python3 .skills/write-to-context.py --mode proposed --field-path {path} --value {value} --source {voc} --confidence {0.55-0.85}` for each routed signal.

Route map.

- `products/{slug}/spec.json#problems_solved[].verbatim_quotes[]` — top 3-5 representative quotes per problem, each carrying `_source_meta.origin: "voc"` and pointing by `verbatim_ids` into Layer A. Frequency and urgency derived from corpus counts (1-10 scale per schema).
- `products/{slug}/spec.json#benefits[].verbatim_quotes[]` — same shape, surfacing perceived-benefit angles the brand under-exploits.
- `audiences/{slug}/profile.json#voice.key_expressions[]` — 5-10 highest-frequency real-customer phrases. Mandatory triplet: `frequency`, `sample_size`, `platform`. Frequency without denominator is refused at the schema level.
- `audiences/{slug}/profile.json#pain_points[]` — refined or new entries with formulation in customer voice, awareness_stage per Schwartz, `_source_meta.origin: "voc"`, sample_size attached.
- `audiences/{slug}/profile.json#objections[]` — typed objections (price / trust / fit / use case / regulatory) with frequency, severity, lifecycle stage. Post-purchase objections (refund issues, expectation gap) are unique to VoC mining; snapshot cannot see them.
- `audiences/{slug}/profile.json#psychology.beliefs_limiting` — only if a belief recurs in three or more verbatims and contradicts a brand claim.
- New `audiences/{new-slug}/profile.json` scaffolded if a coherent sub-segment surfaces that is distinct from existing audience folders. Status `hypothesis`, source `voc-mining`. Operator can reject in next turn; the proposal lives until accepted.
- `brand.json#tone_of_voice` flags — if customers describe the brand in language wildly different from the brand's stated tone, flag for operator review. Never auto-overwrite operator-validated tone.
- `learnings.json` append — only when a cross-session-stable pattern earns it (a recurring ops flag the operator confirmed actionable, a regulatory signal that warrants compliance review, a channel opportunity the operator wants tracked across sessions). Routine theme detection does not append learnings.

Layer A corpus written to `brands/{slug}/sources/voc/{YYYY-MM-DD}/{platform}-{anchor}.jsonl`. Never auto-loaded into context. Audit substrate, queryable on demand, copy-gold reservoir for downstream skills (`generate-hook-brief`, ad copy generation, email sequencing) — those skills pull verbatims from here, never invent.

Every Layer B field carrying VoC content must reference at least one Layer A `id` via `_source_meta.verbatim_ids`. The link is mechanical — operator clicks a synthesized claim, lands on the raw verbatim that justifies it. No claim without backing evidence.

Never overwrite operator-validated data. If a `profile.json` field carries `_source: operator`, propose update via `mode=proposed`; the operator accepts or rejects in the next turn. Direct overwrite of operator-stated fields is refused at the mutation gate.

---

## Step 7 — Finalize (mandatory)

Run, after all Step 6 mutations complete:

```bash
python3 .skills/finalize-mutation-batch.py --brand-slug {slug}
```

Mechanical Python primitive. No LLM negotiation. No skip path.

Exit code 0 → ship; the synthesis from Step 5 is delivered to the operator. Exit code 2 → blocking issue (schema violation, broken Layer A reference, missing denominator on a key_expressions entry, validate-resources MAJOR/CRITICAL). Revise the offending mutation, re-run finalize, do not deliver Step 5 until exit 0.

Skipping Step 7 is the kind of failure that produces a coherence_check warning at turn-end-audit. The hook reads finalize events; if the skill claims "VoC mining done" without a finalize event for the run window, the hook flags an unchecked-entity-claim warning to the operator. Non-negotiable.

After finalize exit 0, trigger the brand snapshot rebuild silently:

```bash
python3 .skills/build-brand-snapshot.py {slug}
```

Per the master mutation rule, any write to a brand's core files refreshes `_snapshot.md`. ~50ms per brand.

---

## --focus parameter modes

The skill ships four narrow modes that adjust Step 5 synthesis emphasis without changing the Step 1-4 mining. Layer A is always full; only the operator-facing surface narrows.

- **default** (no flag) — full three-movement synthesis as specified at Step 5.
- **--focus=objections** — Movement 1 names the audience-as-revealed; Movements 2 and 3 surface only objections, blockers, post-purchase regret. Benefits and vocabulary skipped from the prose. Useful when the operator is briefing a sales-page rebuild and needs the friction inventory in customer voice.
- **--focus=vocabulary** — Movement 1 names the audience; Movements 2 and 3 surface only customer-vocabulary patterns (vernacular expressions, recurring terms, register markers). Theme synthesis skipped. Useful when the operator is writing copy and needs the words their customers actually use.
- **--focus=audience-refinement** — All three movements reorient around audience: who the customers are vs who the brand thought they were, what sub-segments surfaced, where the demographic clues land. Useful after snapshot when the operator suspects the inferred audience is off.
- **--focus=channel-signals** — All three movements reorient around acquisition: where the brand has organic resonance it has not activated, what communities surface the brand by name, what third-party validations show up unprompted. Useful when the operator is planning paid channels and wants the unactivated-organic read first.

Layer A corpus is full regardless of focus mode; the focus only narrows what the operator sees in the synthesis. A subsequent invocation with a different focus reads the same Layer A and re-renders Movement-prose without re-scraping.

---

## Triggers and chaining contexts

Three contexts surface this skill.

**Standalone invocation.** Operator pastes *"voc on respire"*, *"voc {brand}"*, *"scrape les avis pour {brand}"*, *"extrais ce que disent les clients de {brand}"*, *"mine reviews for {brand}"*. Direct trigger. Skill checks brand exists with `brand.json` filled, runs Step 0 ask, proceeds.

**Post-snapshot escape hatch.** At Step 7 close of `snapshot-brand`, the synthesis paragraph proposes (in prose, not menu): *"Want me to go pull what your actual customers say (Trustpilot, native reviews, Reddit) and validate the audience I just inferred? ~10 min."* Operator says yes → mine-voc launches in subagent (Sonnet, `subagent_safe: true`). Snapshot's inferred audience and tone become the testable hypothesis; mine-voc validates or contradicts.

**Orchestrator chaining.** `deepen-brand-context` orchestrator chains mine-voc → mine-vom → final synthesis. mine-voc first (this brand's customers), mine-vom second (the market and competitors), final synthesis cross-references the two. The orchestrator passes `--depth=standard` by default; operator can override at trigger.

---

## Hard Rules

- **Step 0 first-party ask is non-negotiable.** Never start scraping without asking. A skill that misses a 5000-row Klaviyo NPS export because it skipped to Trustpilot is incompetent.
- **Triangulation mandatory.** Minimum three sources before naming a pattern. Singletons stay in Layer A; they do not become Layer B claims.
- **Source provenance always tagged.** Trustpilot ≠ Judge.me ≠ Reddit ≠ Sephora ≠ Amazon. Never aggregate cross-platform without naming the split when the asymmetry matters. A 4.7 average on Loox plus a 2.1 on Trustpilot is not a 3.4; it is a story about who shows up where.
- **Synthesis follows snapshot Step 7 canon strictly.** Three movements of prose, blank line between, no titles, no bold-section anchors, no exposed numbers, no field paths leaked. The decisive stranger-test runs before send.
- **Schema field semantics as analytical vocabulary, never as JSON path mentions.** The skill reasons over `voice.key_expressions` and `pain_points`; it never says those words to the operator.
- **Inferred attributes flagged inline** with *"(à valider)"* / *"(I deduced this)"* — never as a separate "missing fields" or "low confidence" block.
- **finalize-mutation-batch mandatory at Step 7.** Skipping = unchecked-entity-claim warning at turn-end-audit. No skip path. Exit code 2 blocks Step 5 delivery until revised.
- **Verbatim citation policy.** Third-party reviews retain URL and timestamp, anonymize username (replace with `anon_{nano_id}`). First-party data retains author identifier when the operator's export carries one. GDPR consideration: redact email fragments and full names at extraction time.
- **Never overwrite operator-validated data.** Fields carrying `_source: operator` route through `mode=proposed`; the operator accepts or rejects in the next turn. Direct overwrite is refused at the mutation gate.
- **Cap per session.** 200 verbatims per source maximum at default depth, 1000 verbatims total maximum across all surfaces. Larger corpora require operator-explicit `--depth=deep`. Diminishing returns hit hard around the third source.
- **Coding canon non-negotiable.** Read `resources/frameworks/voc-coding.md` at first invocation per session. The four lenses, their order, their binary tests, and their anti-patterns are consumed verbatim. The skill does not improvise the coding.
- **Imported-but-unverifiable widget content downweighted.** Judge.me / Loox / Yotpo allow brands to import or fabricate reviews. Tag `verified_buyer: false` with `provenance_note` when the platform does not expose verification, and downweight in frequency counts.
- **Public-only by default.** Private support tickets require explicit operator authorization before ingestion.
- **Recency weighting.** Reviews older than 12 months carry less weight in synthesis unless the operator asks otherwise. A 2019 review of a discontinued formulation is noise.
- **No fabrication.** Never invent verbatims, never composite quotes from multiple reviewers, never paraphrase into the corpus. The corpus is audit substrate; the synthesis can paraphrase, the corpus never does.

---

## Cross-references

- `resources/frameworks/voc-coding.md` — analytical canon for the four lenses. Mandatory read at first invocation per session. The skill consumes; it does not improvise.
- `.skills/skills/snapshot-brand/SKILL.md § Step 7` — voice canon source for Step 5 synthesis. Three-movement prose, blank-line separation, no-title rule, decisive stranger-test.
- `.skills/skills/ingest-resource/SKILL.md` — first-party data digestion path. Routed at Step 0 when operator drops a CSV / Klaviyo export / support transcript.
- `.skills/skills/mine-vom/SKILL.md` — sister skill for market-level voice (competitors, niche communities). Disambiguation: mine-voc reads this brand's customers; mine-vom reads the market.
- `.skills/skills/mine-audience/SKILL.md` — sister skill for product-level audience discovery. Disambiguation: mine-audience clusters audiences from market scraping; mine-voc mines verbatim from existing customers.
- `.skills/finalize-mutation-batch.py` — mandatory Step 7 primitive. Mechanical, exit 2 = block.
- `.skills/write-to-context.py` — canonical mutation channel. All Layer B writes route through this; never `Edit` on JSON.
- `.skills/build-brand-snapshot.py` — silent rebuild after Step 7 finalize. Per master mutation rule.
- `.claude/hooks/turn-end-audit.py` — reads coherence_check events. Flags unchecked-entity-claim if Step 7 finalize did not run.
- `docs/system/contextual-intelligence.md` — master doctrine. Validation-cascade-avoidance and trust-the-model rules govern the workflow.
- `docs/system/voice.md` — voice canon. Operator-facing synthesis follows it strictly.
- `resources/schemas/spec.schema.json`, `resources/schemas/profile.schema.json` — exit points for Layer B mutations. Field definitions live there.

---

## Changelog

- **1.0.0** (2026-04-24) — Initial spec. Four-lens coding consumes `voc-coding.md`. Layer A corpus + Layer B routed mutations. Step 0 first-party ask non-negotiable. Step 5 synthesis follows snapshot Step 7 canon strictly. Step 7 finalize-mutation-batch mandatory. Four `--focus` modes ship at v1. Sonnet for coding; Haiku A/B in v1.1.
- **1.0.1** — Canon tagging additif (`canon_schwartz_conscience_id`, `canon_emotion_id`, `canon_objection_pattern_id`) on Layer B verbatims. Feeds copy-matrix audience x stade-conscience views.
- **1.0.2** (v2.29.0 alignment verify) — `awareness_stage` rename confirmed in Layer A entry shape and profile routing (`pain_points[].awareness_stage` consumes `_shared/awareness-stage.json` $ref, 5 canoniques). Canon tagging field names unchanged: `canon_schwartz_conscience_id` reste tel quel car pointe vers la fiche canon copy `niveaux-schwartz/conscience.json`, pas vers l'enum `awareness_stage` d'`angle.lineage`. No structural patches needed beyond verify.
