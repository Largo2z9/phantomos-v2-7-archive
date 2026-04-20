# Brand: Lumya

> EXEMPLE — Brand fictive pour démonstration du workspace.
> Auto-loaded when working in this brand folder.
> Shared resources → `../../Ressources/` (reference by ID, never duplicate).
> Resource discovery → `../../index.json`.

## Data Access

- **Sources** : `sources/` — archivage manuel des fichiers bruts (briefs, PDFs, screenshots, exports). Les agents ne chargent pas ce dossier automatiquement. Pas de nettoyage automatique — purge manuelle si le disque est plein. Aucun impact sur le budget contexte.
- **Credentials**: `credentials.env` (brand-level: Meta ad account, Shopify, Klaviyo, etc.)
- **Shared tokens**: `../../credentials_shared.env` (workspace-level: Meta system token, Google OAuth, etc.)
- **Meta Ads**: `act_1234567890` (pixel: `px_9876543210`)
- **Shopify**: `lumya.myshopify.com`
- **Klaviyo**: `KLV_lumya_main`

**Credentials manquants ?** Si `credentials.env` est absent ou vide, lire `config.json → integrations` pour savoir quelles plateformes ont été configurées. Pour chaque flag à `true` → guider la reconfiguration champ par champ. Dire à l'opérateur : "Tes accès {plateforme} manquent sur cette machine. Donne-moi {champ attendu}."

## Workspace State

- **Status**: `status.json` — Niveau 1: ok | brand: partial | produit: complete | audience: complete
- **Todos**: `todos.md` — 1 flag actif (offers manquantes)
- **Config**: `config.json`
- **Session relay**: `session-state.md` — rolling activity log, auto-maintained on every write (no manual rotation)
- **Learnings**: `learnings.json` — 4 entrées (meta_ads, shopify, compliance)

## Context DB — 6 Entities

| Entity | File | Status |
|--------|------|--------|
| Brand | `brand.json` | partial |
| Produit | `products/creme-eclat/spec.json` | complete |
| Offre | `products/creme-eclat/offers.json` | manquante |
| Audience | `audiences/femmes-40-55/profile.json` | complete |
| Learnings | `learnings.json` | 4 entries |
| Strategy | `strategy.json` | complete |

### Context Levels
**Niveau 1 — MVP** complet :
- [x] `brand.json` — identité, positionnement, tone
- [x] `products/creme-eclat/spec.json` — produit hero
- [x] `audiences/femmes-40-55/profile.json` — audience principale

**Niveau 2 — Enrichi** partiel :
- [x] Benefit chains + pain chains remplis
- [x] Concurrents déclarés
- [ ] `products/creme-eclat/offers.json` — **à créer**
- [x] Tone details

**Niveau 3 — Opérationnel** complet :
- [x] Financials renseignés
- [x] Strategy complète (3 objectifs + targets)
- [x] 4 learnings enregistrés

## Brand-Specific Rules

- Audience principale : femmes-40-55 (problem_aware)
- Angle dominant validé en perf : BEN-01 (rides réduites, chiffres cliniques)
- Objection prioritaire à traiter : scepticisme rétinol (fréquence 9/10)
- Ne jamais utiliser "rajeunir" ou "paraître plus jeune" — non-conforme DGCCRF
