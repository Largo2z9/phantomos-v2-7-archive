# Audience cartography

> Doctrine for the audience-mapping phase of `snapshot-brand` (Step 5) and downstream consumers (`mine-voc`, `produce-paid-angles`, `produce-copy-brief`). Read this when authoring or extending any skill that touches `audiences/{slug}/profile.json`.

## The problem this solves

A product page does not tell the agent who buys the product. It tells the agent what the product is. Naively scraping a page and outputting "Audience: women, problem: hair loss" is form-fill, not cartography. The operator ends up tearing the classification apart and rebuilding it manually (S55 karacare test: operator had to re-do the entire audience hierarchy because the agent had collapsed seven audiences into one flat "femmes-cheveux-fragiles").

The fix is not better extraction. It is a different posture. The agent presents **observations**, then proposes **multiple cartographies**, then offers a **hierarchy by default**, then hands off to the next skill with **explicit pedagogy** about how the audience encoding will be exploited downstream.

## The four operator-facing movements

The agent must run these four movements in order during Step 5 of `snapshot-brand`. Each movement has a hard contract.

### Movement 1 — Raw observations

Before any classification, the agent names what the page literally said. No interpretation, no inference, just observations with their source. Format:

> *"Voici ce que la page m'a dit, mot pour mot : la marque s'adresse à des femmes (mention `for her` ligne 14), évoque la chute (mot apparaît 8 fois dans le body), évoque la pousse (4 fois), pas de mention d'âge explicite, pas de mention de profession ou de contexte de vie. Les tags produit pointent sur biotine, post-grossesse, cheveux abîmés."*

**Why this matters.** The operator immediately sees the raw material the agent is working with. If the page is thin, this exposes it without hiding behind a confident-looking classification. If the page is rich, the operator can spot signals the agent is about to under-weight. This movement is **never skipped**, even when observations are thin. *"La page n'a quasiment rien dit côté audience"* is a valid Movement 1 output and is more useful than a fabricated profile.

### Movement 2 — Cartography axes

The agent proposes 2 to 3 alternative **cartography axes** for slicing the audience. Each axis is a different way of cutting the same population. The operator picks the axis that matches what they see in performance data, not what the agent guesses.

The three canonical axes:

- **Pain-driven** — slice by what hurts (e.g. *"want to grow"* vs *"losing hair"*). Best when the product addresses two distinct emotional states with different urgency profiles. Drives different copy registers (aspirational vs urgent).
- **Situational** — slice by life moment or context (e.g. *"post-grossesse"* vs *"stress longue durée"* vs *"chute saisonnière"*). Best when the product hits the same pain in different trigger contexts. Drives different acquisition windows and different creative casting.
- **Demographic / cultural** — slice by who they are (e.g. *"jeunes femmes voilées"* vs *"jeunes femmes non voilées"*). Best when cultural codes shape both the visual world of the creative and the channel mix (e.g. influence-heavy on one segment, paid-cold-heavy on the other). Demographic axes are **rarely the dominant axis** for paid acquisition — they tend to be modulators within a pain axis or a situational axis. Surface them when the operator's channel mix or creative casting clearly diverges by demographic.

**Format the agent uses to present axes:**

> *"Trois manières de découper cette audience, je te donne les trois et tu me dis laquelle colle à ce que tu vois en perfs.*
>
> *Axe pain-driven : 'je veux pousser' (longueur, densité, projet beauté positif) vs 'je perds mes cheveux' (chute active, charge émotionnelle, urgence). Adapté quand les deux états émotionnels appellent des registres copy différents.*
>
> *Axe situationnel : 'post-grossesse' vs 'stress longue durée' vs 'chute saisonnière'. Adapté quand le même pain est déclenché dans des contextes très différents.*
>
> *Axe démographique-culturel : 'jeunes femmes voilées' vs 'jeunes femmes non voilées'. Adapté quand le casting créa et le canal d'acquisition divergent par segment.*
>
> *Mon hypothèse default à corriger franchement : axe pain-driven, parce que [raison appuyée sur un signal observé en Movement 1]. Mais si tu vois un autre axe en perfs, dis-le."*

**Hard rule.** The agent **always** proposes at least 2 axes, **always** marks one as the default hypothesis with a one-line rationale tied to a Movement 1 observation, **always** invites the operator to override. Single-axis proposals are a regression to form-fill.

### Movement 3 — Hierarchy mère / sous-audiences

Once the operator picks an axis, the agent proposes a hierarchy: 2 to 3 **mother audiences** with 1 to 3 **sub-audiences** under each. Mother audiences carry the strategic positioning. Sub-audiences carry the situational or demographic refinement that drives creative casting and channel choice.

A flat audience list with no hierarchy is the wrong default. Sub-audiences must be marked `validation_status: hypothesis` until verbatim evidence (mine-voc) or paid performance (audit-meta-account) validates them.

**Format:**

> *"Sur l'axe pain-driven que t'as choisi, voici la hiérarchie que je propose :*
>
> *Mère 'pousse-projet' : longueur ou densité jugées insuffisantes, démarche beauté positive, pas d'urgence. Sous-audiences : pousse-jeune-adulte (18-30, projet esthétique), pousse-recovery (post-coloration ou post-lissage, casse récente).*
>
> *Mère 'chute-active' : chute en cours, charge émotionnelle, urgence. Sous-audiences : chute-post-grossesse (25-35, hormonal aigu), chute-hormonale-stress (22-32, diffuse longue durée), chute-traction (zones d'appui voile / tissages / tresses).*
>
> *Toutes les sous-audiences sont en hypothesis. Elles seront enrichies par mine-voc à partir de verbatims réels (Trustpilot, reviews, Reddit). Tu valides la hiérarchie ou tu veux qu'on en garde moins en hypothèse pour démarrer plus serré ?"*

The agent never grinds the operator with 5 questions to fill 5 audiences. It proposes the full hierarchy in one move, defaulted with hypothesis status, and lets the operator trim or expand.

### Movement 4 — Hand-off pédagogique

Before closing Step 5, the agent explicitly tells the operator how the audience encoding will be **exploited downstream**. This is the pedagogy step. It anchors why we did the work and points to the next skill in the chain.

**Format:**

> *"Voilà comment ces audiences vont servir à partir de maintenant.*
>
> *L'encodage qu'on vient de poser est volontairement minimal : un slug, un axe, une hypothèse. Pour qu'il devienne opérationnel pour ton paid, deux skills l'enrichissent.*
>
> *mine-voc va lire les reviews Trustpilot, les widgets onsite, les threads Reddit pertinents et remplir pour chaque sous-audience les pain_points exacts (le vrai mot qu'elles utilisent), les objections récurrentes, les expressions clés. C'est ce qui transforme tes audiences hypothèse-grade en audiences validation-grade. ~30 min en background.*
>
> *produce-paid-angles consomme ensuite ces audiences enrichies pour te sortir un set d'angles ranked, prêts à brief créa. Sans mine-voc d'abord, les angles sortent au mot près de mon chapeau, pas de tes clientes.*
>
> *Mon avis : on lance mine-voc maintenant et on enchaîne sur les angles. Si t'as une raison de pousser direct sur les angles en hypothèse-grade (deadline créa cette semaine), dis-le, on ajuste."*

This movement reframes the audience as **infrastructure** that compounds across the next skills, not as a one-off form-fill. It also primes the operator on the cost asymmetry (hypothesis-grade angles ship faster but converge slower). The operator chooses the trade-off knowingly.

## What this replaces

The old Step 5 (1.x) ran:

1. Infer from page (Step 5A)
2. Stage + present 5 fields (Step 5B)
3. Single complementary question if missing data (Step 5C)
4. Existing data probe (Step 5D)

It produced a flat single audience with no axis declaration, no hierarchy, no hand-off pedagogy. It systematically forced the operator to rebuild the cartography by hand. The S55 karacare test exposed this in 6+ minutes of operator-driven re-classification ("femme magrébine voilée 18-30" → "deux audiences mères + 3 sous"), which is exactly the work the agent should have done autonomously by proposing 3 axes upfront.

## What stays unchanged

- Stage-then-ask pattern (`stage-proposal.py` → `checkpoint-resolver` hook). Audience writes still gated by `audience_q1q4_answered`.
- "If page is thin" branch (Step 5C single question) remains, but only fires when Movement 1 observations are genuinely empty.
- Existing data probe (Step 5D) becomes the closing question of Movement 4 instead of a separate step.

## Cross-references

- `.skills/skills/snapshot-brand/SKILL.md § Step 5` — implementation
- `.skills/skills/mine-voc/SKILL.md` — downstream consumer, reads audiences and enriches them with verbatim
- `.skills/skills/produce-paid-angles/SKILL.md` — downstream consumer, reads enriched audiences to produce angles
- `docs/system/contextual-intelligence.md` — master doctrine, "no form-fill, propose multiple framings"
- `resources/schemas/profile.schema.json` — `meta.scope` (broad / segment / micro), `meta.parent_slug`, `meta.validation_status` (hypothesis → tested → validated → scaled → fatigued)

## Anti-patterns

- **Single-axis classification.** Agent picks one axis silently and presents one slicing. Operator forced to challenge from scratch.
- **Flat audience list.** Agent proposes 5 audiences in parallel without mother/sub structure. Operator can't see the strategic levels.
- **No hand-off pedagogy.** Agent finishes Step 5 with *"audiences saved, what next?"*. Operator has no idea why it matters or what consumes the encoding.
- **Confident hallucination.** Agent fills `pain_points[]` and `psychology.beliefs_limiting[]` from the product page alone. These belong to mine-voc verbatim, not snapshot inference. snapshot-brand fills `meta`, `identity.gender`, `identity.age_range`, `pain.primary_problem`, `meta.tags[]`, `meta.scope`, `meta.parent_slug`, `meta.validation_status`. That is all.
- **Skipping Movement 1.** Agent jumps to classification without showing raw observations. Operator can't audit the agent's working memory.

## Field-level contract for snapshot-brand audience writes

Snapshot-brand fills these fields per audience and **only these** (everything else stays null until mine-voc or operator-driven enrichment):

```
meta.name              → human-readable label
meta.slug              → kebab-case slug
meta.scope             → broad | segment | micro
meta.parent_slug       → null for mother, slug-of-mother for sub
meta.validation_status → "hypothesis"
meta.audience_type     → "primary" | "secondary" | "discovered" | "assumed"
meta.applies_to_products → array of product slugs (multi-product binding, see § Audience binding par produit)
meta.tags              → namespace-prefixed tags from page (e.g. "problem:hair-loss", "context:post-pregnancy")
identity.gender        → male | female | all (only if explicit on page)
identity.age_range     → {min, max} (only if explicit on page)
pain.primary_problem   → one-line problem statement in operator's language (only if explicit)
```

Everything else null until mine-voc runs.

## Audience binding par produit (v2.24.0)

Une audience vit au niveau brand (`brands/{slug}/audiences/{audience_slug}/profile.json`) mais elle est **indexée multi-produit** via `meta.applies_to_products[]`. Storage flat, indexation multidimensionnelle.

**Sémantique du champ.**
- `[]` (vide) : audience **brand-wide**, pertinente pour tous les produits ou pour la marque sans produit spécifique.
- `["hair-boost"]` : audience **mono-produit**, achète uniquement Hair Boost.
- `["hair-boost", "cellule-boost"]` : audience **cross-product**, achète plusieurs produits de la même marque.

**Pourquoi pas un dossier `products/{p}/audiences/`** : multi-produit oblige à dupliquer ou symlink. Storage flat avec indexation = pas de duplication, et une audience cross-product reste une seule entité dans le système.

**Comment l'opérateur navigue le binding.**
- `/phantom {brand} audiences` : liste toutes les audiences du brand, chaque ligne affiche son `→ applies_to`.
- `/phantom {brand} products {p}` : item-mode produit, section AUDIENCES filtre celles dont `applies_to_products` contient `{p}`.
- `/phantom {brand} audiences {audience_slug}` : item-mode audience, section APPLIQUÉ AUX PRODUITS liste les bindings.
- `/phantom search {keyword}` : indexe `applies_to_products[]`, donc taper un slug produit retrouve les audiences taggées.

**Snapshot Step 5 Movement 3.** Lors de la cartographie hierarchy, demander pour chaque audience proposée *"cette audience achète quel(s) produit(s) ?"* (multi-coche). Default = le hero produit du run snapshot. Multiple = cross-product (acceptable). Vide acceptable = brand-wide générique.

**Backward compatibility.** `meta.product_id` (single, deprecated v2.24.0) reste lu en fallback si `applies_to_products` est vide. Migration via `python3 .skills/migrate-audience-applies-to.py` (idempotent, dry-run avec `--dry-run`).
