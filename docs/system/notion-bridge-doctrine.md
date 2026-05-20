# Notion Bridge Doctrine

> Doctrine canonique v2.57+. Mode d'emploi du bridge bidirectionnel Notion ↔ PhantomOS. Définit le principe canon "PhantomOS = source of truth · Notion = UI optionnelle", les mappings cross-platform, les edge cases, et le workflow opérateur. Sœur de `connectivity-layering.md` (Layer 1 MCP) et de `compositional-cartography.md` (instance Notion stride-up = implémentation opérationnelle canonique de référence).

---

## Status

Canonique v2.57+. Codifie le bridge implémenté par `sync-notion-atlas` skill (orchestrator Layer 1). Le système Notion stride-up workspace (canvas Onday avec 11 collections inter-reliées) est l'**instance de référence canonique** · 4 arbres compositionnels reliés (Spec → Mécanisme → Bénéfice, Audience → Pain Points, Angle Obs+Tension+Reframe+Bridge, Roadmap timeline) + matrice Profil × Source d'angle + tags universels source / confidence / validation_status sur toutes les DB. Cette structure est exactement celle codifiée dans `compositional-cartography.md` doctrine canon. Notion est un client UI · PhantomOS est le moteur.

---

## Le principe canon

**PhantomOS = source of truth canonique. Notion = UI optionnelle pour opérateurs qui préfèrent une interface tabulaire navigable.**

Ce n'est pas une intégration symétrique. C'est un client/serveur asymétrique ·

- L'opérateur peut bosser dans **Notion** (UI navigable, vues board / timeline / table, drill-down par filtre persona × angle) OU dans **PhantomOS** (Claude Code skills, agents, primitives runtime).
- La **source de vérité** est toujours PhantomOS (`brands/{slug}/*.json` + canon resources). Notion est un mirror.
- Sync **bidirectionnel** · pull (Notion → PhantomOS) pour ingérer le travail opérateur fait en UI · push (PhantomOS → Notion) pour exposer le state encodé en UI navigable.

**Pourquoi cette asymétrie ?**

1. **Versioning** · git tracks PhantomOS, pas Notion. Audit trail, rollback, diff cross-time = PhantomOS.
2. **Schemas validés** · `validate-resources` haïku check intégrité cross-skill côté PhantomOS. Notion permet anything-goes.
3. **Skills consume** · les 56 skills PhantomOS consument JSON brand entities. Si la source vit en Notion, chaque skill devrait re-call l'API Notion à chaque turn · latence + coût.
4. **Multi-clients agency** · Abyss collectif 5-10 brands · PhantomOS isolation `brand_only` par filesystem · Notion isolation par workspace. PhantomOS scale plus facilement.

L'opérateur qui n'a pas besoin d'UI Notion peut ignorer cette doctrine. Notion bridge est **opt-in** · zéro impact si MCP Notion absent.

---

## Mappings cross-platform · 11 collections Notion ↔ schemas PhantomOS

Validé par audit Phase 1 (v2.56 alignement schemas). Chaque collection Notion mappe sur 1+ schemas PhantomOS + 1 storage path canonique.

| Collection Notion | Schema PhantomOS | Storage Path |
|---|---|---|
| Produits | `spec.schema` + `offer.schema` | `brands/{slug}/products/{p}/spec.json` + `offers.json` |
| Specs | `spec.composition` + `spec.specs` | subfields spec.json |
| Mécanismes | `spec.mechanisms[]` (+ xref `creative-mechanics-registry.md`) | subfield spec.json |
| Bénéfices | `spec.benefits[]` enrichis v2.56 (emotional_signal + latency_min/max + evidence_verbatim) | subfield spec.json |
| Personae / Audiences | `profile.schema` | `brands/{slug}/audiences/{a}/profile.json` |
| Pain Points | `profile.pain_benefit_chain[]` + `pain_category` v2.56 | subfield profile.json |
| Angles produits | `angle.schema` | `brands/{slug}/angles/{ANG-NN}.json` |
| Objections | `profile.objections[]` enrichi v2.56 (severity_score + response_counter + derived_angle_refs) | subfield profile.json |
| Frictions usage | `friction.schema` NEW v2.56 | `brands/{slug}/frictions/{FRC-NN}.json` |
| Roadmap [angles/audiences] | `roadmap.schema` NEW v2.56 | `brands/{slug}/roadmap.json` |
| Full funnel Meta | `creative.schema` + `funnel.schema` | `brands/{slug}/creatives/{CRT-NN}.json` + `funnel.json` |

**Cohérence cross-collections** · les relations Notion (ex Angle ↔ Persona ↔ Pain Points ↔ Mécanique dans Full funnel Meta) deviennent des refs cross-fichiers PhantomOS (`angle.cross_refs.audience_slugs[]`, `friction.cross_refs.objection_ids[]`, etc.). Le bridge maintient l'intégrité référentielle.

---

## Tags universels · mapping épistemic

Notion stride-up utilise 3 tags universels sur toutes les DB ·

- **Source** · `observed` (verbatim sourcé) / `inferred` (déduit) / `declared` (annoncé par le client)
- **Confidence** · 0 à 1
- **Validation status** · `hypothesis` / `tested` / `validated` / `scaled` / `fatigued`

PhantomOS encode cette discipline épistemic différemment mais équivalemment ·

| Tag Notion | Équivalent PhantomOS |
|---|---|
| Source | `_field_types` per-field · enum [`observed`, `stated`, `derived`, `structured`] |
| Confidence | `meta.confidence` (0-1) · présent profile / brief / canon-tool · ajouté v2.56 sur spec / offer / brand via `meta.validation_status` (composite) |
| Validation status | `meta.validation_status` $ref `_shared/validation-status.json` · enum cohérent atlas vivant canon-tool |

**Règle absolue de cohérence** · le bridge `sync-notion-atlas` doit traduire ces tags dans les 2 sens sans perte. Un row Notion sans tag = `meta.validation_status: "hypothesis"` + `_field_types: "stated"` par défaut côté PhantomOS (posture investigation-posture · "TRÈS faible confidence" jusqu'à validation).

---

## Workflow opérateur

3 modes de sync exposés par le skill `sync-notion-atlas` ·

### `--mode=pull` (Notion → PhantomOS)

Cas d'usage · l'opérateur a peuplé Notion (manuellement ou via collab agency), veut ingérer dans PhantomOS pour exécuter skills downstream (produce-paid-angles, score-matrix, compose-creative, etc.).

Commande · `/sync-notion-atlas {brand_slug} --mode=pull {notion_workspace_url}`

Steps internes ·
1. Verify MCP Notion connecté (`claude mcp list`)
2. `notion-search` + `notion-fetch` les 11 collections sous canvas brand
3. `notion-query-database-view` rows par collection
4. Apply mappings (table ci-dessus) · pour chaque row Notion, mutation correspondante PhantomOS
5. Stage chaque mutation via `stage-proposal.py` (mode proposed)
6. Trigger `validate-resources` silently
7. Surface synthesis 5 sections investigation-posture (Observé Notion · Déduit gaps · Inconnu fields manquants · Leviers actions opérateur · Close ouvert)

### `--mode=push` (PhantomOS → Notion)

Cas d'usage · l'opérateur a peuplé PhantomOS (via skills `build-atlas-complete`, `produce-paid-matrix`, etc.), veut exposer le state en Notion UI pour client review ou collab agency externe.

Commande · `/sync-notion-atlas {brand_slug} --mode=push {notion_parent_url}`

Steps internes ·
1. Verify MCP Notion connecté
2. Read PhantomOS state via `phantom-canon.py` + JSON entity files brand
3. Pour chaque entité, `notion-create-database` (si pas existe sous parent) puis `notion-create-pages` row par instance
4. Set relations via `notion-update-data-source` (cross-refs angles ↔ personae ↔ pain points)
5. Output URL workspace Notion créé + diff (combien rows créées / mises à jour)

### `--mode=diff` (compare sans muter · deferred P2)

Cas d'usage · audit pré-sync · compare state Notion vs PhantomOS, list divergences, l'opérateur décide quoi sync.

---

## Edge cases canonisés

### Property type mismatch

Cas · une property Notion est `select` alors que le mapping attend `multi_select` (ou inverse).

Règle · le bridge **flag explicitement** dans la synthesis pull, ne mute pas silencieusement. Opérateur arbitre · soit accept la traduction (transform `select` value → `multi_select` array singleton), soit corrige Notion d'abord.

### Deleted rows (Notion side)

Cas · l'opérateur a supprimé un row Notion qui était précédemment sync.

Règle pull · le bridge détecte le delta absent · stage une **proposition de suppression** côté PhantomOS via `stage-proposal.py --action=delete`. JAMAIS de suppression silencieuse. Opérateur valide avant.

### Dual-writes (concurrent edits)

Cas · l'opérateur édite Notion ET PhantomOS entre 2 syncs.

Règle · le bridge détecte les 2 mutations par timestamp. Si conflit · flag dans synthesis pull/push · opérateur arbitre quelle source gagne (Notion ou PhantomOS).

**Reco anti-pattern** · NE PAS éditer simultanément les 2 systèmes. Cycle propre · l'opérateur choisit son mode (Notion UI ou PhantomOS) pour une session, sync en début et fin de session.

### Notion workspace structure non-canonique

Cas · l'opérateur a un Notion existant avec structure différente des 11 collections canon stride-up.

Règle pull · le bridge utilise un **schema map override** optionnel · `~/notion-mappings/{brand_slug}.json` qui override le mapping par défaut. Si absent, fallback détection heuristique des noms de DB (cherche "Audiences" / "Personae" / "Angles" / etc.).

### Brand isolation cross-Notion-workspaces

Cas · Largo gère Abyss collectif 5-10 brands · chaque brand a son propre Notion workspace.

Règle · `isolation_scope: brand_only` strict respecté. Un sync = un brand. Le bridge ne pull JAMAIS de data depuis un Notion d'une autre brand vers le brand cible. L'opérateur passe explicitement l'URL Notion par brand.

---

## Positioning · Layer 1 cross-ref

Le bridge Notion est un **Layer 1** au sens `connectivity-layering.md` ·

- **Layer 1 MCP servers** · Notion MCP enregistré côté Claude Code opérateur (`~/.claude/mcp/`). Le template ship `.mcp.json.example` qui documente notion server (entry `notion` avec `_credentials_ref: NOTION_API_KEY`). Aucune connexion live shippée d'office.
- **Verify** · `claude mcp list` côté opérateur. Si absent · sync-notion-atlas refuse de tourner et propose installation.

Cross-refs Layer 1 ·
- `connect-mcp-server` skill (orchestrator Layer 1 setup) · peut installer Notion MCP pour l'opérateur
- `.mcp.json.example` · entry notion server documenté

---

## Anti-patterns

### AP-1 · Considérer Notion comme source of truth

Faux. PhantomOS est canon. Notion est mirror. Si l'opérateur édite Notion mais ne sync pas, les skills PhantomOS continuent de tourner sur l'ancien state. Pas de magic auto-sync.

### AP-2 · Push vers Notion avant validate-resources OK

Anti-pattern. Si l'état PhantomOS contient des MAJOR/CRITICAL findings non résolus, le push expose des inconsistencies en UI. Toujours · `validate-resources` zero blocking error AVANT push.

### AP-3 · Pull silencieux sans operator gate

Le pull stage les mutations en mode `proposed`. L'opérateur valide via `pending-validations.md`. JAMAIS d'auto-accept sans gate explicite.

### AP-4 · Bridge mutation cross-brand

Un sync = un brand. JAMAIS de bridge cross-brand · si Largo veut sync Brand A puis Brand B, 2 invocations distinctes du skill. Respecte `brand-isolation-doctrine.md`.

### AP-5 · Mapper sans canon validation

Si un row Notion contient un field qui n'existe pas dans le schema PhantomOS canon, ne pas l'inventer. Le bridge flag dans synthesis pull · opérateur décide soit `scaffold-extension` pour custom field, soit drop le field.

---

## Cross-refs

- `connectivity-layering.md` · Layer 1 MCP servers (cette doctrine étend la Layer 1)
- `compositional-cartography.md` · doctrine compositionnelle parente · le système Notion stride-up implémente exactement les 4 arbres + matrice + modulateurs canon
- `brand-isolation-doctrine.md` · règle isolation cross-brand respectée par le bridge
- `schema-encoding-discipline.md` · mutation gate + `_field_types` + validation_status canon
- `investigation-posture.md` · synthesis pull/push respecte les 5 sections (Observé / Déduit / Inconnu / Leviers / Close ouvert)
- `.skills/skills/sync-notion-atlas/SKILL.md` · implémentation du bridge
- `.mcp.json.example` · entry notion server Layer 1
- `docs/product/capabilities.md § Scénarios Notion ↔ PhantomOS` · 8 scénarios opérateur de bout-en-bout

---

## Évolutions futures

- **v2.57+** · Phase A pull-only MVP (skill `sync-notion-atlas --mode=pull`)
- **v2.58+** · Phase B push-only (skill `sync-notion-atlas --mode=push`)
- **v2.59+** · Phase C diff-mode (compare sans muter, audit pré-sync)
- **v2.60+** · Schema map override custom (`~/notion-mappings/{brand_slug}.json`) pour Notion non-canonique
- **v2.61+** · Auto-sync scheduled (Layer 2 cron-style) · opt-in opérateur
