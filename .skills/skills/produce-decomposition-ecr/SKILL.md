---
name: produce-decomposition-ecr
type: producer
version: "1.0.0"
recommended_model: sonnet
subagent_safe: true
layer: meta
reasoning_pattern: compositional_recursive_equation
description: >
  Sub-skill of scaffold-extension Phase 3bis. Consume ECR decomposition object from
  analyze-extension-intent v2.0.0 + schema draft from Phase 3. Produit décomposition
  canon opérateur-facing · équation OUTPUT = NOYAU × CONTEXTE × MODIFIEURS instanciée
  pour le sujet + matrice cartographique proposée (axes × valeurs) + atomes mesurables
  identifiés + templates pré-pensés depuis registry pattern existing (creative-mechanics-registry,
  angle-registry, proof-registry, frameworks). Surface à l'opérateur via AskUserQuestion
  pour validation OR ajustement. Halt si refus opérateur · re-prompt analyze-extension-intent
  avec corrections.
  FR · "produit la décomposition", "génère équation et matrice", "produit ECR".
  EN · "produce decomposition", "generate equation and matrix", "produce ecr".
permissions:
  reads: [resource, brand]
  writes: []
  mode: none
  subagent_safe: true
allowed-tools: Read, Glob, Grep, AskUserQuestion
disambiguates_against:
  propose-schema-draft: "propose-schema-draft génère le schema JSON technique. produce-decomposition-ecr génère la décomposition opérateur-facing (équation + matrice + atomes + templates suggérés) consommée AVANT le schema."
  analyze-extension-intent: "analyze-extension-intent capture l'intent + applique ECR méthodologie 5 étapes. produce-decomposition-ecr consomme cet output ECR pour produire l'artefact opérateur-facing."
---

# Skill · Produce ECR Decomposition

Produces an operator-facing ECR decomposition artifact from the structured intent + ECR decomposition produced by `analyze-extension-intent v2.0.0`. Output is the canonical decomposition the operator validates before scaffold proceeds.

## Pipeline

### Step 1 · Consume ECR decomposition object

Read the `ecr_decomposition` object from `analyze-extension-intent v2.0.0` output (passed via Task tool context OR stage file).

If `eligibility.applicable = false` → halt. The subject is not ECR-eligible. Skip this skill (scaffold-extension proceeds directly to Phase 4).

### Step 2 · Instantiate master equation for the subject

Render the master equation in canonical form ·

```
[SUJET] = X × Y × Z
```

Where X, Y, Z are the triptych dimensions identified in Étape ECR-3 (Stratégie × Composition × Exécution OU pattern adapté · Funnel · Système · Performance).

Example for "script IA vidéo ads" ·

```
SCRIPT VIDÉO ADS = STRATÉGIE × COMPOSITION × EXÉCUTION
                   ^^^^^^^^^   ^^^^^^^^^^^   ^^^^^^^^^^
                   audience    structure     atomes
                   angle       narrative     visuels/copy
                   format      hooks         seconde-par-seconde
                   canal       proofs        CTA timing
                   duration    body          screen overlay
                   tone        outro
```

### Step 3 · Produce cartographic matrix

Build a 2D matrix proposal that captures the main axes of the subject.

For script IA vidéo ads ·

```
                  AUDIENCE 1     AUDIENCE 2     AUDIENCE 3
              ─────────────────────────────────────────────
ANGLE 1 ·       cellule         cellule         cellule
ANGLE 2 ·       cellule         cellule         cellule
ANGLE 3 ·       cellule         cellule         cellule
```

Each cell = un script unique paramétré par (audience, angle, format, duration, tone).

Combinaisons théoriques · audience × angle × format × duration = N × M × P × Q variations.
Top-K piochées selon scoring composé (pertinence audience × force angle × cohérence visuel).

### Step 4 · List atomes mesurables identified

Read `atoms_identified` from ECR decomposition. Pour chaque atome, expliquer ·
- Nom de l'atome
- Test d'atomicité (modifier l'atome → quel delta observable sur output final ?)
- Métriques associées (niveau couche 4)

### Step 5 · Suggest templates depuis registry pattern existing

Read `resources/registries/` (creative-mechanics-registry.md, angle-registry.md, proof-registry.md) + `resources/frameworks/` pour identifier patterns réutilisables applicables au sujet.

Exemple script IA vidéo ads ·
- "POV-confession-15s" depuis creative-mechanics-registry (vulnérabilité narrative)
- "Before-After-dramatic-30s" depuis angle-registry (transformation)
- "Native-review-screenshot-15s" depuis proof-registry (social proof natif)

Propose top-3 templates pré-pensés.

### Step 6 · Surface to operator via AskUserQuestion

Format output canon ·

```
══════════════════════════════════════════════════════════════════════
DÉCOMPOSITION ECR · {sujet}
══════════════════════════════════════════════════════════════════════

ÉLIGIBILITÉ
  Hiérarchique ✓ · Auto-similaire ✓ · Multiplicatif ✓
  → ECR applicable

ATOME DE SORTIE
  {description atome final mesurable}

ÉQUATION MAÎTRE
  {SUJET} = X × Y × Z

  X · {variable 1} · sous-variables a, b, c
  Y · {variable 2} · sous-variables d, e, f
  Z · {variable 3} · sous-variables g, h, i

MATRICE CARTOGRAPHIQUE PROPOSÉE
  {grille ASCII 2D · axes × valeurs}

ATOMES MESURABLES IDENTIFIÉS
  {liste atomes avec métriques associées}

TEMPLATES SUGGÉRÉS DEPUIS REGISTRY EXISTING
  {top-3 templates pré-pensés réutilisables}

══════════════════════════════════════════════════════════════════════
```

AskUserQuestion ·
- Option A · valide la décomposition, continue Phase 4 scaffold
- Option B · ajuste 1-2 dimensions (re-prompt analyze-extension-intent avec corrections)
- Option C · halt · sujet pas adapté à ECR finalement

## Halt conditions

- ECR eligibility fail (test 3 critères) → skip skill, scaffold proceed direct Phase 4
- Operator refuse décomposition → halt scaffold, re-prompt analyze-extension-intent
- Registry resources absent → fallback "capture-then-matricize" (canon doctrine v2.71)

## Hard rules

- HR-1 · Respecter MECE strict (test triple appliqué aux sous-variables)
- HR-2 · Maximum 5 sous-variables par niveau (sinon fusionner)
- HR-3 · Atomes mesurables required (test d'atomicité appliqué)
- HR-4 · Templates suggérés depuis registry existing UNIQUEMENT (pas freelance)
- HR-5 · Output operator-facing en langage courant (zero jargon doctrine, zero acronyme non-traduit)

## Cross-refs

- `docs/system/operational-system-discipline.md` (doctrine mère ECR canonisée)
- `docs/system/scope-extension-discipline.md` (SED-X · ECR amont)
- `docs/system/compositional-cartography.md` (équation NOYAU × CONTEXTE × MODIFIEURS)
- Sub-skill of `scaffold-extension` v1.2.0+ (Phase 3bis)
- Upstream sibling · `analyze-extension-intent` v2.0.0 (produces ECR decomposition object)
