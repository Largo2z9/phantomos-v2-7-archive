# Skills index by operator intent

Operator-facing index of skills, grouped by what the operator wants to *do*, not by skill type or alphabetical order. Use this when an operator describes a goal in natural language without naming a skill.

The agent reads `_manifest.json` for routing details (frontmatter, triggers, model, subagent). This file is the human bridge from intent to skill name.

Last update : 2026-05-04 (v2.33 enrichment : domain map + phase workflows + per-skill cards).

---

## Navigation par domaine

| Domain | Skills | Phase doctrine |
|---|---|---|
| **onboarding** | setup-brand · onboard-brand · snapshot-brand · connect-source | P0 |
| **cartography** | cartograph · query-context · brief-day · session-search · resume-session | P1-P2 (read-only) |
| **product** | define-specs · weight-dimensions | P1 + P3 modulator |
| **audience** | mine-voc · mine-vom · mine-audience · profile-audience | P2a |
| **production** | produce-paid-angles · produce-copy-brief · decompose-ad | P2b-P5 |
| **audit** | validate-resources · audit-meta-account · validate-output-coherence · validate-schema-canon · check-cross-refs · check-existing-coverage | ongoing |
| **capture** | capture-learning · learn-from-session · export-session | ongoing |
| **extensibility** | build-agent · scaffold-extension · scaffold-skill-stub · scaffold-entity-files | builder |
| **support** | propose-schema-draft · ingest-resource · cross-deepening-signals · deepen-brand-context · encode-batch · finalize-mutation-batch · write-to-context · promote-learning | utility |

> Note : navigation skills par domaine. Pour la doctrine cartographie compositionnelle complète (P0 vers P5), voir `docs/system/atlas-canon-copy.md` + `lexicon.md § Atlas` + `resources/templates/creative-formula.md`.

---

## Workflow type par phase

**P0 · Onboarding brand**
  setup-brand OU snapshot-brand vers cartograph (synthèse) vers mine-voc/mine-vom (audiences signals)

**P1 · Product cartography**
  define-specs (mode hybride : auto-pull URL + Q&A + sources) vers cartograph (synthèse)

**P2a · Audience cartography**
  mine-voc + mine-vom + mine-audience (mining raw) vers profile-audience (synthèse 8 dim)

**P2b · Angle cartography**
  produce-paid-angles (forward) OU decompose-ad (reverse benchmark) vers cartograph

**P3 · Matrix + scoring**
  weight-dimensions (compute coefficients) vers score-matrix (futur v2.34)

**P4 · Brief structured**
  produce-copy-brief (depuis angle.json + creative.json optional)

**P5 · Creative production (visual)**
  decompose-ad (reverse benchmark) vers compose-creative (futur v2.34) vers recompose-creative (futur v2.34)

---

## I want to set up a new brand or workspace

| Operator says | Skill to invoke |
|---|---|
| *"on commence sur une nouvelle marque"*, *"new brand"*, *"setup une marque"* | `setup-brand` (orchestrator that walks the 4-step pipeline) |
| *"juste fais le setup vite fait"*, *"onboard cette marque"* | `onboard-brand` (full pipeline shortcut) |
| *"je te donne l'URL, fais-moi un premier scan"* | `snapshot-brand` (URL → brief fiche défendable) |
| *"je veux comprendre ce que je tourne"*, *"quelle version j'ai ?"* | Read `_version.json` + `docs/product/variant-map.md` |

---

## I want to understand the audience or the market

| Operator says | Skill to invoke |
|---|---|
| *"qu'est-ce que disent les clients de cette marque"*, *"voice of customer"*, *"VoC"* | `mine-voc` |
| *"qu'est-ce qui se passe sur le marché", *"voice of market"*, *"VoM"* | `mine-vom` |
| *"identifie les audiences candidates"*, *"qui sont les acheteurs"* | `mine-audience` |
| *"approfondis le contexte de cette marque"*, *"deepen brand"* | `deepen-brand-context` (orchestrates VoC + VoM in parallel) |
| *"le produit fit avec cette audience ?"* | `score-product-fit` |
| *"étude de niche complète"*, *"market deep dive"* | `study-niche-marketdeepdive` |

---

## I want to produce a paid creative or copy

| Operator says | Skill to invoke |
|---|---|
| *"sors-moi des angles paid"*, *"angles for Meta ads"*, *"5 angles ranked"* | `produce-paid-angles` |
| *"écris-moi un brief copywriter"*, *"copy brief on this audience"* | `produce-copy-brief` |
| *"score cette offre", *"audit cette offre"*, *"l'offre tient ou pas ?"* | `score-product-fit` |

---

## I want to audit something

| Operator says | Skill to invoke |
|---|---|
| *"audit le setup Meta"*, *"check les comptes pubs"* | `audit-meta-account` |
| *"valide le workspace"*, *"check les ressources"*, *"y a quoi qui cloche"* | `validate-resources` |
| *"audit la cohérence cross-docs"* | (sub-agent Explore on demand, no shipped skill) |

---

## I want to capture or persist something

| Operator says | Skill to invoke |
|---|---|
| *"note ça"*, *"retiens que"*, *"capture ce learning"*, *"on a découvert que"* | `capture-learning` (single fact) |
| *"learn from session"*, *"persiste la session"*, *"end of day"* | `learn-from-session` (batch session capture) |
| *"exporte cette conversation"*, *"archive cette session"* | `export-session` |
| *"range ce document"*, *"range cette URL"*, *"ingest ça"* | `ingest-resource` |

---

## I want to extend or build something new

| Operator says | Skill to invoke |
|---|---|
| *"j'aimerais créer une automatisation"*, *"on va segmenter les étapes"*, *"je veux faire un workflow X"* | `scaffold-extension` (then a sub-skill for the specific output) |
| *"crée une extension"*, *"nouveau type de donnée"*, *"où je range cette donnée"* | `scaffold-extension` |
| *"tracker X au fil du temps"*, *"j'ai une donnée nouvelle à ranger"*, *"ajoute un sidecar"* | `scaffold-extension` |
| *"build un agent pour X"*, *"crée un skill custom"* | `build-agent` |

---

## I want to navigate or resume

| Operator says | Skill to invoke |
|---|---|
| *"où j'en suis ?"*, *"brief-moi sur où j'en étais"*, *"recap"* | `brief-day` |
| *"reprends"*, *"continue où on s'est arrêté"* | `resume-session` |
| *"qu'a-t-on dit sur X"*, *"cherche dans les sessions passées"* | `session-search` |

---

## I want to migrate or upgrade

| Operator says | Skill to invoke |
|---|---|
| *"upgrade le workspace"*, *"migre vers la nouvelle version"* | `migrate-workspace` |

---

## I want to connect an external tool

| Operator says | Skill to invoke |
|---|---|
| *"connect meta ads"*, *"ajoute shopify"*, *"branch klaviyo"* | `connect-source` (uses convention if shipped, scopes new platforms via `scope` skill) |
| *"connect un nouvel outil"*, *"add external source"* | `connect-source` (asks platform name, then routes) |
| *"qu'est-ce que j'ai connecté ?"*, *"liste mes sources"* | Read `operator/connected-sources.json` + `brands/{slug}/connected-sources.json` |

---

## When the intent is ambiguous

If the operator's phrasing matches multiple intents (e.g. *"audit le contexte de cette marque"* could be `validate-resources` or `deepen-brand-context`), read the `disambiguates_against` block in the manifest entry of each candidate. If still ambiguous after that, ask one `AskUserQuestion` with 2 to 3 candidates.

If no skill matches, do not invent one. Surface honestly that the requested operation does not have a shipped skill, and offer to scaffold one via `scaffold-extension` if it is structural enough to deserve persistence.

---

## Skill cards (mini-tables d'orientation)

Chaque card situe un skill sur 4 axes : domain · phase · prerequisites · next steps. 46 skills (43 existants + 3 nouveaux v2.33).

### onboarding

**setup-brand**
| Domain | Phase | Prerequisites | Next steps |
|---|---|---|---|
| onboarding | P0 | aucun | snapshot-brand (auto-pull URL) ou define-specs (Q&A guidé) |

**onboard-brand**
| Domain | Phase | Prerequisites | Next steps |
|---|---|---|---|
| onboarding | P0 | URL produit fournie | cartograph (synthèse) |

**snapshot-brand**
| Domain | Phase | Prerequisites | Next steps |
|---|---|---|---|
| onboarding | P0 | URL produit fournie | define-specs (gaps non-scrapés) puis cartograph |

**connect-source**
| Domain | Phase | Prerequisites | Next steps |
|---|---|---|---|
| onboarding | P0 | brand existante · credentials platform | ingest-resource (route flux) |

### cartography

**cartograph**
| Domain | Phase | Prerequisites | Next steps |
|---|---|---|---|
| cartography | P1-P2 (read-only) | brand.json + spec.json minimum | mine-voc OR produce-paid-angles |

**query-context**
| Domain | Phase | Prerequisites | Next steps |
|---|---|---|---|
| cartography | ongoing (read-only) | brand encodée | n'importe quel producer skill |

**brief-day**
| Domain | Phase | Prerequisites | Next steps |
|---|---|---|---|
| cartography | ongoing | session-state.md present | resume-session OU producer prochain |

**session-search**
| Domain | Phase | Prerequisites | Next steps |
|---|---|---|---|
| cartography | ongoing | sessions archivées | resume-session si match |

**resume-session**
| Domain | Phase | Prerequisites | Next steps |
|---|---|---|---|
| cartography | ongoing | session-state.md OR session export | enchaîner producer interrompu |

### product

**define-specs** (NEW v2.33)
| Domain | Phase | Prerequisites | Next steps |
|---|---|---|---|
| product | P1 | brand.json existe | cartograph (synthèse) ou mine-voc (audience) |

**weight-dimensions** (NEW v2.33)
| Domain | Phase | Prerequisites | Next steps |
|---|---|---|---|
| product | P3 (modulator) | profile-audience populated · angles disponibles | score-matrix (futur v2.34) |

### audience

**mine-voc**
| Domain | Phase | Prerequisites | Next steps |
|---|---|---|---|
| audience | P2a | brand.json + spec.json | profile-audience (synthèse) |

**mine-vom**
| Domain | Phase | Prerequisites | Next steps |
|---|---|---|---|
| audience | P2a | brand.json + spec.json | profile-audience (synthèse) |

**mine-audience**
| Domain | Phase | Prerequisites | Next steps |
|---|---|---|---|
| audience | P2a | brand.json + spec.json | profile-audience (synthèse) |

**profile-audience** (NEW v2.33)
| Domain | Phase | Prerequisites | Next steps |
|---|---|---|---|
| audience | P2a | mine-voc OR mine-vom OR mine-audience tourné | produce-paid-angles (P2b) |

### production

**produce-paid-angles**
| Domain | Phase | Prerequisites | Next steps |
|---|---|---|---|
| production | P2b vers P4 | profile-audience + spec.json | produce-copy-brief OR decompose-ad |

**produce-copy-brief**
| Domain | Phase | Prerequisites | Next steps |
|---|---|---|---|
| production | P4 | angle.json (depuis produce-paid-angles) · creative.json optional | livrable copywriter |

**decompose-ad**
| Domain | Phase | Prerequisites | Next steps |
|---|---|---|---|
| production | P5 (reverse) | ad source (TrendTrack/URL/drop) + visual_identity (optional) | produce-paid-angles (forward) |

### audit

**validate-resources**
| Domain | Phase | Prerequisites | Next steps |
|---|---|---|---|
| audit | ongoing | brand encodée | corriger issues flagged |

**audit-meta-account**
| Domain | Phase | Prerequisites | Next steps |
|---|---|---|---|
| audit | ongoing | credentials Meta + ad account ID | analyze-perf (Abyss side) |

**validate-output-coherence**
| Domain | Phase | Prerequisites | Next steps |
|---|---|---|---|
| audit | ongoing (post-produce) | output producer disponible | re-run producer si invalide |

**validate-schema-canon**
| Domain | Phase | Prerequisites | Next steps |
|---|---|---|---|
| audit | ongoing | schemas/ touchés récemment | promote schema OR fix drift |

**check-cross-refs**
| Domain | Phase | Prerequisites | Next steps |
|---|---|---|---|
| audit | ongoing | docs cross-référencés | corriger broken refs |

**check-existing-coverage**
| Domain | Phase | Prerequisites | Next steps |
|---|---|---|---|
| audit | ongoing (pré-create) | intention nouveau doc/skill | extend > create OU procéder |

### capture

**capture-learning**
| Domain | Phase | Prerequisites | Next steps |
|---|---|---|---|
| capture | ongoing | fait isolé à persister | learn-from-session en fin de jour |

**learn-from-session**
| Domain | Phase | Prerequisites | Next steps |
|---|---|---|---|
| capture | ongoing (end-of-session) | session active avec signaux | export-session si archivage formel |

**export-session**
| Domain | Phase | Prerequisites | Next steps |
|---|---|---|---|
| capture | ongoing | session significative à archiver | session-search future |

### extensibility

**build-agent**
| Domain | Phase | Prerequisites | Next steps |
|---|---|---|---|
| extensibility | builder | spec agent claire (manifest brief) | scaffold-skill-stub si skill custom |

**scaffold-extension**
| Domain | Phase | Prerequisites | Next steps |
|---|---|---|---|
| extensibility | builder | besoin entité/sidecar nouveau | scaffold-entity-files OR scaffold-skill-stub |

**scaffold-skill-stub**
| Domain | Phase | Prerequisites | Next steps |
|---|---|---|---|
| extensibility | builder | name + type + frontmatter triad décidés | rédiger SKILL.md complet |

**scaffold-entity-files**
| Domain | Phase | Prerequisites | Next steps |
|---|---|---|---|
| extensibility | builder | extension scaffoldée (custom entity) | encode-batch first records |

### support

**propose-schema-draft**
| Domain | Phase | Prerequisites | Next steps |
|---|---|---|---|
| support | utility | besoin schéma nouveau | validate-schema-canon puis promote |

**ingest-resource**
| Domain | Phase | Prerequisites | Next steps |
|---|---|---|---|
| support | utility | URL/doc/asset à ranger | validate-resources |

**cross-deepening-signals**
| Domain | Phase | Prerequisites | Next steps |
|---|---|---|---|
| support | utility | mining VoC + VoM tournés | profile-audience |

**deepen-brand-context**
| Domain | Phase | Prerequisites | Next steps |
|---|---|---|---|
| support | utility (orchestrator) | brand.json minimum | profile-audience |

**encode-batch**
| Domain | Phase | Prerequisites | Next steps |
|---|---|---|---|
| support | utility | batch raw à encoder (mining/scrape) | finalize-mutation-batch |

**finalize-mutation-batch**
| Domain | Phase | Prerequisites | Next steps |
|---|---|---|---|
| support | utility | encode-batch produced proposed mutations | accept/reject par opérateur |

**write-to-context**
| Domain | Phase | Prerequisites | Next steps |
|---|---|---|---|
| support | utility (gate) | mutation prête | validate-resources auto |

**promote-learning**
| Domain | Phase | Prerequisites | Next steps |
|---|---|---|---|
| support | utility | learning isolé récurrent | encode dans canon (schema/skill/doc) |

---

## Maintenance

This index is human-edited. Add an entry when :
- A new skill ships (add row in the matching section).
- An operator phrasing repeatedly fails to match an existing skill (add the phrasing to the trigger column).
- A skill is renamed, removed, or merged (update or delete the row).

The index does not replace the manifest. It complements it for the moment when the operator describes a goal without naming a skill.
