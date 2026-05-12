# Model Versioning Canon

> Doctrine canonique v2.44+. Tout skill qui appelle une API externe (image gen · LLM · etc.) doit vérifier la version la plus récente disponible avant de hardcoder un endpoint. Sœur de skill-authoring-discipline et compositional-cartography.

## Le problème

PhantomOS skills hardcodent les endpoints API externes dans frontmatter `permissions.bash` et HR. Exemple v2.43 · `compose-creative` et `craft-packshot` utilisaient `fal-ai/nano-banana-pro/edit` (Gemini 2.5 Flash Image · pre-novembre 2025). En novembre 2025, Google a release Gemini 3 Pro Image (fal endpoint `nano-banana-2/edit`) · meilleur · text fidelity supérieur · material preservation native. Skills PhantomOS continuaient à utiliser endpoint legacy · résultats sub-optimaux.

Cycle USAGE v2.44 stress test cellule-boost a livré 9 attempts échouées sur endpoint legacy (silhouette bouteille réinventée OR text gibberish) avant que swap vers `nano-banana-2/edit` résolve en 1 attempt avec prompt naturel français court. Apprentissage canon · le canon de novembre 2025 n'était plus le canon de mai 2026. Drift silencieux entre release modèle et adoption skill.

## Règle canon

### Verification pre-call

Avant tout call API externe, le skill DOIT ·

1. Check docs API officielle pour latest version dispo (URL fournie en frontmatter `permissions.external_apis[].version_check_url`)
2. Compare avec endpoint hardcoded dans skill · si version récente dispo · flag operator OR auto-switch selon `auto_upgrade` config
3. Log version utilisée dans output metadata pour audit trail

### Frontmatter SKILL.md required fields

Chaque skill qui call API externe DOIT declarer `permissions.external_apis[]` ·

```yaml
permissions:
  external_apis:
    - provider: "fal.ai"
      endpoint: "fal-ai/nano-banana-2/edit"
      model_family: "gemini_3_pro_image_novembre_2025"
      version_check_url: "https://fal.ai/models?keywords=banana"
      version_canon_date: "2025-11"
      replaced_legacy: "fal-ai/nano-banana-pro/edit (v2.43)"
      auto_upgrade: false
```

Champs ·
- `provider` · vendor de l'API (fal.ai, openai, anthropic, etc.)
- `endpoint` · path canonical actuel utilisé par skill
- `model_family` · famille modèle sous-jacent (gemini_3_pro_image, gpt_5, claude_5, etc.)
- `version_check_url` · URL docs vendor pour check latest version
- `version_canon_date` · date release version utilisée (YYYY-MM)
- `replaced_legacy` · endpoint précédent superseded (audit trail)
- `auto_upgrade` · `false` par défaut (operator gate pour upgrade) · `true` autorise auto-switch silent

### Naming convention versions

Endpoints fal.ai canon · noter version dans path ·
- `nano-banana` (v1.0 · Gemini 2.5 Flash Image)
- `nano-banana-pro` (v1.5 · Gemini 2.5 Pro Image)
- `nano-banana-2` (v2.0 · Gemini 3 Pro Image novembre 2025)
- Always check latest via `https://fal.ai/models` listing

Pattern equivalent autres vendors ·
- OpenAI · `gpt-image-1` (v1.0 mai 2025) · `gpt-image-2` (à venir 2026)
- Anthropic · `claude-opus-4-7` (canon mai 2026 · 1M context)

### Audit log

Chaque skill output doit logger ·
- Endpoint utilisé exact (path complet vendor/model/operation)
- Version date (YYYY-MM release model)
- Si auto-upgrade applied OR legacy used (flag explicite)
- Comparison metric vs legacy si test parallèle dispo (silhouette preservation, text fidelity, latency, cost/call)

## Application v2.44

Skills affectés ·
- `compose-creative` · TODO swap nano-banana-pro/edit → nano-banana-2/edit (v2.45+)
- `craft-packshot` v1.1 · swap fait v2.44 (cellule-boost canon validé · audit ref)
- `recompose-creative` · TODO check v2.45+
- `decompose-ad` · TODO check (trendtrack endpoint legacy)

## Cross-refs

- `docs/system/skill-authoring-discipline.md` (frontmatter permissions canon)
- `docs/system/compositional-cartography.md` (production loop canon)
- `docs/system/visual-identity-discipline.md` v2.43 (chantier 1 fidélité)
