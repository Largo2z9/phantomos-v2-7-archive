# Skill resource discovery — runtime pattern

> How skills find and consume knowledge from `resources/` at runtime without any tagging by the operator. Pattern : structured schemas (mandatory) → primary reasoning (LLM) → resource discovery (FTS5) → confrontation → coherence validation. Zero maintenance when adding or removing resources.

## The problem this solves

Previous approach considered tagging every resource with `applies_when: {vertical, brand_type, skill_names}` so skills could know which resources to consult. Rejected — maintenance hell. Every time an operator adds a doc, someone has to update the tags. Every time a skill is created, someone has to re-tag all resources that might apply. Drift is guaranteed.

**The new approach : discovery at runtime via FTS5.** Resources are indexed automatically on ingestion. Skills query the index with keywords derived from their current context. The match is content-driven, not tag-driven. A doc deposited 6 months ago can be rediscovered the moment its content matches a new context.

## The execution flow

Every skill that consumes knowledge follows this order :

```
1. Load structured brand schemas (mandatory)
 ↓
2. Primary reasoning (LLM thinks with brand facts)
 ↓
3. Derive context keywords (from brand + task)
 ↓
4. Call discover-resources (FTS5 query, top-K chunks)
 ↓
5. Confront primary reasoning with retrieved chunks
 ↓
6. Compose output
 ↓
7. Pass through validate-output-coherence
 ↓
8. Ship to operator (or revise if blocking)
```

**Priority rule** — brand facts always win. If a retrieved resource says one thing and `brand.json` says another, the brand wins. Resources enrich, they don't override.

## Each step in detail

### Step 1 — Load structured schemas

The skill's frontmatter declares `inputs_required`. For a creative audit :

```yaml
inputs_required:
 - brands/{slug}/brand.json#/positioning
 - brands/{slug}/brand.json#/tone_of_voice
 - brands/{slug}/brand.json#/meta/vertical
 - brands/{slug}/products/{product_slug}/spec.json
 - brands/{slug}/audiences/{audience_slug}/profile.json
```

All loaded before any reasoning. These are the source of truth.

### Step 2 — Primary reasoning

The skill + LLM reason on the loaded schemas. Produces preliminary conclusions or questions. At this stage, the skill does NOT hit external resources. It thinks with what the brand declared first.

Why first reasoning, then retrieval : the reasoning itself generates the KEYWORDS that the retrieval will use. If we retrieved first with blind keywords, we'd get low-signal chunks. Reasoning narrows the search space.

### Step 3 — Derive context keywords

From the primary reasoning + loaded schemas, the skill builds a keyword string for FTS5. Examples :

| Skill context | Derived keywords |
|---|---|
| Auditing Meta creatives for Northsense (supplements, femmes 30-50, FR) | `"audit creative supplements hair care femmes diversity FR angles"` |
| Checking compliance claims for a cosmetics brand | `"cosmetics compliance claims EU EFSA beauty regulation"` |
| Briefing an ad for a fashion brand targeting Gen-Z | `"brief ad fashion Gen-Z hook trends seasonal apparel"` |

The skill can also accept an explicit `resource_discovery.keywords_template` from an SOP. Example SOP frontmatter :

```yaml
checkpoint 5.4:
 tier: contextual
 resource_discovery:
 keywords_template: "angle diversity {vertical} {product_category} ecommerce"
 limit: 5
 source_types: [framework, guide]
```

Variables like `{vertical}` are filled at runtime from the loaded brand schemas.

### Step 4 — Call discover-resources

```bash
python3 .skills/discover-resources.py \
 --query "{keywords}" \
 --source-types framework,guide \
 --limit 5 \
 --boost-recency \
 --format json
```

Returns top-K chunks ranked by BM25 + optional recency boost. Each chunk comes with : `resource_type`, `ref`, `title`, `date`, `file_path`, `snippet`, `score`.

Skill consumes the JSON output. Typically injects the top 3-5 snippets into its reasoning context as retrieved evidence.

### Step 5 — Confront reasoning with resources

Three outcomes :

- **Resource confirms reasoning** → reasoning strengthened, cite the resource in the output as support
- **Resource enriches reasoning** → incorporate the new angle, credit the resource
- **Resource contradicts reasoning** → check against brand facts first (brand wins), then either discard the resource as not applicable, or revise reasoning if the resource is more authoritative (rare — only if resource is flagged `source_of_truth`)

**If resource contradicts brand fact** → resource is ignored, brand fact stands. Period.

### Step 6 — Compose output

The skill writes its deliverable (audit report, brief, analysis, whatever). Output cites : retrieved resources by `file_path` if their content shaped a conclusion, brand fields by path if a brand fact drove a finding, inferences explicitly tagged as such.

### Step 7 — Validate-output-coherence

Before shipping to operator, the skill calls `validate-output-coherence` sub-skill :

```bash
python3 -c "import subprocess; ..." # pseudo-invocation
```

The sub-skill checks : schema consistency (referenced fields exist), fact consistency (no brand contradiction), tone consistency (matches declared voice), no fabrication (numbers/claims sourced).

Returns `{ok: bool, warnings: [...], blocking_issues: [...]}`.

### Step 8 — Ship or revise

- `ok: true` + no warnings → ship to operator
- `ok: true` + warnings → ship to operator with warnings surfaced as footnote ("I noted some style drift — want me to revise ?")
- `ok: false` (blocking_issues present) → skill attempts one revision using the flagged issues as correction cues, re-validates, then ships. Two failed revisions = escalate to operator with explanation.

## How this interacts with existing primitives

- `.skills/memory-index.py` — indexes `resources/{frameworks,guides,catalogues,sops,conventions,quality-specs,templates,routing}/` automatically. No action from operator.
- `.skills/ensure-memory-fresh.py` — keeps the index up-to-date. Called by any skill that needs fresh state.
- `.skills/discover-resources.py` — the primitive skills call to query the index.
- `.skills/skills/validate-output-coherence/SKILL.md` — the final gate sub-skill.
- `resources/schemas/sop.schema.json` — SOPs declare `resource_discovery` blocks per contextual checkpoint.
- `resources/sops/audit-meta-global.md` — reference SOP showing the pattern in practice (contextual checkpoints have `tier: contextual` + `resource_discovery: {...}`).

## What NOT to do

- **Don't pre-tag resources with tags like `applies_when: [fashion, supplements]`.** Content-based retrieval handles niche matching automatically.
- **Don't hard-code resource paths in skills.** Discover at runtime.
- **Don't let retrieved resources override brand facts.** Brand wins, always.
- **Don't skip validate-output-coherence.** It's the final gate. Even when tempted by deadline or simplicity, run it.
- **Don't inject resources into prompt prefix.** It breaks prefix cache. Resources come back as tool output (from the Bash call to `discover-resources.py`), which is mid-turn content, not prefix.

## Cost budget per skill execution

Typical creative audit or brief :

- 1-3 `discover-resources` calls per skill execution (≈ 800 tokens each)
- 1 `validate-output-coherence` call (≈ 2k tokens including brand context load)
- Total overhead : 3-5k tokens per skill execution

For reference, the full LLM reasoning for a skill is typically 20-80k tokens. Overhead = 5-15%. Acceptable for the moat value (no tagging, automatic rediscovery, coherence gate).

## When to add semantic search (embeddings)

FTS5 lexical match works well when operator-deposited resources use vocabulary aligned with the brand's structured fields. Edge cases where it misses :

- Synonyms (`sans caféine` vs `caffeine-free`)
- Paraphrase (`alternative café` vs `substitut du café`)
- Cross-language (FR content, EN keywords)

If these become bottlenecks in practice, add a semantic layer : local embeddings (sentence-transformers) or lightweight API (OpenAI, Voyage) as a secondary retrieval step. Not V1. Wait for real usage signal before adding the dependency.

## Related docs

- `docs/system/sop-skill-conversion.md` — where the canonical skill/SOP/doc separation is defined
- `docs/system/skill-architecture-redteam.md` — the red team findings that motivated this design
- `docs/system/skill-builder-cartography.md` — when to scaffold a new custom entity vs add a resource doc
