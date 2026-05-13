# Compositional Cartography Discipline

> Doctrine canonique v2.42+. Méthode systémique de cartographier puis composer outputs créatifs et stratégiques via équation v3.1 NOYAU × CONTEXTE × MODIFIEURS. Sœur de Schema Encoding Discipline (SED) et Canonical Matrix Reasoning (CMR), opère comme implémentation domaine-spécifique de CMR appliquée au créatif.

---

## Status

Canonique v2.42+. Distille `resources/templates/creative-formula.md` (registry vivant, 522 créas analysées, 10 patches S55) en doctrine system-side rigoureuse, skill-author-facing. Toute évolution future passe par doctrine governance (`docs/system/doctrine-governance.md`) : amendment via D# verrouillé append-only, retraction interdite par défaut, supersession formalisée.

La distinction registry vs doctrine est préservée. `creative-formula.md` reste le registre vivant exhaustif (mécaniques, hooks, proof, angles, sous-types UGC, curseur texte/visual, classificateur production). Cette doctrine codifie les invariants conceptuels que tout skill producer / curator / orchestrator créatif doit honorer.

---

## Le problème

PhantomOS produit outputs créatifs et stratégiques via skills production (`produce-paid-angles`, `produce-copy-brief`, `compose-creative`, `recompose-creative`, `score-matrix`). Sans doctrine compositionnelle canon, chaque skill réinvente sa logique d'assemblage. Conséquences :

1. Drift cross-skill. `produce-paid-angles` compose audience × angle × proof, `compose-creative` compose mécanique × hook × format, sans grammaire partagée le même creative reproduit deux fois donne deux décompositions incompatibles.
2. Output qualité inégale. Composition implicite produit local optimum autoregressif (premier composant ancre le reste), pas l'espace Pareto des choix compatibles.
3. Pas de cycle validation cohérent. Sans canon compositionnel, impossible d'attribuer un résultat test à un composant identifié, donc pas de compound learning ciblé.

Compositional Cartography canonise quatre opérations :

- **Décomposer** un output créatif en composants typés (NOYAU · CONTEXTE · MODIFIEURS).
- **Composer** un output créatif depuis ces composants (équation v3.1).
- **Cartographier** audiences, produits, angles, creatives en arbres + matrices priorisation.
- **Alimenter** atlas vivant via cycle validation produce → test → learn → promote.

---

## Équation v3.1 canon

L'output créatif unitaire (`creative.schema/1.2`) suit l'équation suivante :

```
creative_statique = NOYAU(mécanique × format × stop_scroller × ton)
                  × CONTEXTE(angle × pain_point × persona × proof)
                  × MODIFIEURS(occasion · offer · destination · intent_mix · overlay_density · brand_mark_present)
```

Trois couches orthogonales par construction :

- **NOYAU** · transferable cross-context, indépendant de l'audience et du produit. Mécanique persuasive + format (ratio, durée, canal), élément stop-scroller (visual ou hook), ton. Un creative qui change uniquement de NOYAU change de structure persuasive.
- **CONTEXTE** · audience-spécifique et produit-spécifique. Angle stratégique, pain point traité, persona ciblée, proof activée. Un creative qui change uniquement de CONTEXTE change de cible.
- **MODIFIEURS** · ajustement runtime sans modifier structure ni cible. Occasion (saisonnalité, trigger événementiel), offer (variante prix, bundle), destination (LP, PDP, collection), intent_mix (DR · Brand · Hybrid · B2B_lead_gen), overlay_density, brand_mark_present.

Détails registre exhaustif (mécaniques, hooks, formules proof, angles, sous-types UGC, curseur texte/visual, classificateur production · CONCEPT · TEMPLATE · ASSET) : `resources/templates/creative-formula.md`.

---

## 4 arbres + 1 matrice + 4 modulateurs

Cartographier une brand au sens compositionnel se traduit par la construction de quatre arbres orientés, une matrice de priorisation et quatre modulateurs contextuels.

**4 arbres** ·

1. **Audiences** · broad → segment → micro. Hiérarchie 3 niveaux maximum (invariant `audience-cartography-doctrine.md`). Framework 4 questions canon v2.39 (audience-cartography-framework operator-facing).
2. **Products** · specs → mechanisms → benefits. Chain functional / emotional / identity. Ancrage `products/{slug}/spec.json`.
3. **Angles** · compositional · Observation + Tension + Reframe + Bridge. Lineage canon angle-registry. Chaque angle référence sa source canon Schwartz / Sugarman / Halbert.
4. **Creatives produced** · NOYAU × CONTEXTE × MODIFIEURS. Lineage angles (chaque creative pointe l'angle parent), lineage atlas canon (hook_canon_id, framework_canon_id, archetype_canon_id, etc.).

**1 matrice** · `score-matrix` · Sub-cluster × Source d'angle. Cellules compatibles scorées Impact × 3 + Vitesse × 2 + Signal × 1. Score interne uniquement, jamais exposé operator (anti-pattern BCG documenté CMR §7).

**4 modulateurs brand** ·

- Stade brand · pre-PMF · early-growth · scale · mature.
- Moment stratégique · launch · sustain · pivot · revival.
- Contexte marché · maturity stage du sub-vertical, intensité concurrentielle.
- État atlas · couverture verbatims, densité validations, fraîcheur learnings.

Coefficients cumulés appliqués au scoring matrice, plage 0.5 à 2.0 capped. Modulateurs s'appliquent en second pass (pattern modulator-vs-cell CMR invariant #5), ne multiplient pas la cardinalité.

---

## Cycle validation, atlas vivant feed

Compound learning end-to-end, quatre temps :

1. **Produce** · `compose-creative` (ou skill production équivalent) génère output ancré canon refs · `hook_canon_id`, `framework_canon_id`, `archetype_canon_id`, `angle_id`. Output taggé lineage explicite.
2. **Test** · output testé live (Meta Ads, Google Ads, organique, email). Résultat capturé (CTR, conversion, longevity_signal, qualitative).
3. **Learn** · `learn-from-session` capture résultat. Alimente `validations[]` append-only sur le canon-tool utilisé. Schema `canon-tool/1.1` v2.27.0 attribution + decay v2.37.
4. **Promote** · si N≥3 brands distinctes valident même pattern · promotion vers canon copy générique cross-brand. Bridge atlas brand-spécifique (sense 4) vers atlas canon (sense 1).

Pattern compound learning canonisé v2.27.0 (atlas vivant) · canon-tool schema v1.1 attribution · decay v2.37 (fatigue creative et fatigue framework).

---

## 7 disciplines, décompte résolu

Compositional Cartography est la sixième discipline. Sœur de :

1. **Contextual Intelligence (CI)** · master doctrine. L'agent raisonne sur l'univers business, ne form-fill jamais.
2. **Schema Encoding Discipline (SED)** · substrat, encodage rigoureux des entités, fields, sources, vocabulaire.
3. **Canonical Matrix Reasoning (CMR)** · production qualité 95% via schema + canon matrice. Théorie générale.
4. **Skill Authoring Discipline (SAD)** · création et extension de skills. Type taxonomy, frontmatter triad, composition contracts, lifecycle.
5. **Provenance & Trust Discipline (PTD)** · scope provenance, multi-operator, marketplace skills.
6. **Compositional Cartography (CC)** · cartographier + composer outputs créatifs via équation v3.1. Cette doctrine.
7. **Doctrine Governance** · meta-process évolution doctrines (promotion, amendment, retraction, conflict resolution).

Plus **Extractibility test** · frame de validation transverse appliqué aux disciplines 1-6, pas une doctrine en soi. Test : "si je remplace brand par matter / creator / venue / account, les invariants tiennent-ils ?"

**Distinction CC vs CMR.** CMR énonce la théorie générale de production qualité via matrices canon (13 invariants, 4 modes, anti-patterns, decision-aid). CC est l'application spécifique de CMR au domaine créatif · équation v3.1 + 4 arbres + matrice priorisation + cycle validation atlas vivant. CC opère sous CMR comme implémentation domaine-spécifique. Un skill créatif est CMR-compliant et CC-compliant. Un skill consulting (`study-niche-marketdeepdive`) est CMR-compliant sans être CC-compliant (pas de domaine créatif).

---

## Cross-refs

- `resources/templates/creative-formula.md` · registry vivant exhaustif (mécaniques, hooks, proof, angles, sous-types UGC, curseur texte/visual, classificateur production, 522 créas analysées, 10 patches S55).
- `docs/system/canonical-matrix-reasoning.md` · théorie matrice parente (13 invariants, 4 modes, anti-patterns).
- `docs/system/schema-encoding-discipline.md` · substrat encodage requis (entités, fields, sourcing tags, vocabulaire fermé).
- `docs/system/atlas-canon-copy.md` · sense 1 cross-brand, référentiel typé partagé outils canon copy.
- `docs/system/atlas-brand.md` · sense 4 brand-spécifique, cartographie holistique data d'une brand.
- `docs/system/audience-cartography-doctrine.md` · cartographie audiences spécifique (3 niveaux, invariants validate-resources).
- `docs/doctrine/audience-cartography-framework.md` · operator-facing 4 questions canon.
- `docs/system/doctrine-governance.md` · processus évolution doctrines.
- `docs/system/notion-bridge-doctrine.md` · implémentation Notion canonique de référence · sync bidirectionnel via `sync-notion-atlas` skill · le système Notion stride-up workspace implémente opérationnellement les 4 arbres + matrice + modulateurs codifiés ici.

---

## Évolutions futures

- **v2.43+** · Cartographie produits parallèle. Mêmes patterns appliqués à products (mechanisms → benefits → identity chain) avec invariants propres.
- **v2.43+** · Cartographie angles autonome. Le 4e arbre formalisé doctrine séparée, lineage canon + lineage tests + decay.
- **v2.44+** · Compositionnel temporel. Séries de creatives liés narrativement (saga, sequencing), scoring contextualisé par position dans la série.
- **v2.45+** · Extractibility test formalisé en doctrine séparée. Aujourd'hui transverse, peut graduer en doctrine 7 si cardinalité d'usage atteinte (≥3 disciplines testées explicitement).

---

*Doctrine canonique, skill-author-facing. Cross-référence avec CMR (théorie parente), SED (substrat requis), atlas-canon-copy (référentiel partagé), atlas-brand (cartographie data). Operator-facing 4 questions : `docs/doctrine/audience-cartography-framework.md`.*
