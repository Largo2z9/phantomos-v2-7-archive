# Connectivity layering

> Canon des 3 couches de connectivité PhantomOS. Référencé par CLAUDE.md root (Operator contract → "Connected tools, three layers"), par le skill `connect-mcp-server` (Layer 1), par le skill `connect-source` (Layer 2), et par les audits scope.

PhantomOS interagit avec des outils externes via trois couches distinctes. Elles ne sont pas équivalentes, elles n'ont pas la même surface de configuration, elles ne s'activent pas via le même point d'entrée. Toujours nommer la couche concernée explicitement, jamais confondre.

---

## Layer 1 · MCP servers (Claude Code level)

**Quoi.** Serveurs MCP (Model Context Protocol) enregistrés au niveau Claude Code (CLI), pas au niveau du template PhantomOS. Une fois enregistrés, ils exposent des outils que le modèle peut appeler directement comme s'ils étaient natifs (Gmail, Slack, Notion, ClickUp, Excalidraw, Supabase, etc.).

**Où ça vit.** `~/.claude/mcp/` (config opérateur, hors workspace). Listé via `claude mcp list`. Ajouté via `claude mcp add` ou via un `.mcp.json` au workspace root.

**Surface template.** Le template ship `.mcp.json.example` (template MCP defaults documenté) + le skill `connect-mcp-server` (orchestrateur setup). Aucune connexion live n'est shippée d'office. Tout est opérationnalisé côté opérateur.

**4 defaults PhantomOS** :
- `facebook-graph` (Meta Graph API, requis par `audit-meta-account` / `list-accounts` / `routine-perf`)
- `youtube-transcript` (pas de token, requis par `mine-vom`)
- `supabase` (Postgres SQL + auth, requis par cockpit + analytics)
- `google-calendar` (read/write events, requis par `brief-daily`)

**Custom possibles** : gmail, slack, notion, clickup, excalidraw, gitlab, mcp custom hébergé par l'opérateur, etc. Catalogue Anthropic + tiers.

**Comment vérifier.** Avant de claim qu'un MCP est connecté : `claude mcp list`. Si absent → pas connecté côté Layer 1.

---

## Layer 2 · APIs callable via skills (template-shipped code + operator credentials)

**Quoi.** Des appels API externes faits depuis le code des skills shippés dans le template (`.skills/skills/{name}/SKILL.md` + scripts associés). Le code de l'appel est présent et versionné dans le template. La connexion est inactive tant que l'opérateur n'a pas droppé ses tokens dans `credentials_shared.env` (workspace) ou `brands/{slug}/credentials.env` (brand-specific).

**Où ça vit.** Skills consumer (audit-meta-account, audit-google-pmax, mine-voc, etc.) + tokens dans `credentials_shared.env` ou `brands/{slug}/credentials.env`.

**Surface template.** Le calling code est shippé. Les conventions sont shippées dans `resources/conventions/{platform}.json`. Le skill `connect-source` orchestre la liaison opérateur ↔ plateforme.

**Plateformes shippées d'office** : Meta Ads, Google Ads, TikTok Ads, GA4, Shopify, Klaviyo, TripleWhale (conventions présentes dans `resources/conventions/`).

**Comment vérifier.** Avant de claim qu'une API est joignable : check `credentials_shared.env` ou `brands/{slug}/credentials.env`. Si le token requis est vide ou absent → l'API ne répond pas, le skill consumer va échouer sur la première call.

---

## Layer 3 · Infrastructure scripts (shipped, runs out of the box)

**Quoi.** Scripts shippés dans `.skills/` qui s'exécutent localement, sans credentials externes : mining publique (Reddit, Trustpilot, YouTube, Google Trends), mutation gate (`write_to_context`), validation (`validate-resources`), build manifest, build brand snapshot, etc.

**Où ça vit.** `.skills/*.py`, `.skills/skills/*/SKILL.md`. Aucun setup requis.

**Surface template.** 100% shippé. Marche dès qu'un opérateur clone ou réimporte le template.

**Comment vérifier.** N'a pas besoin d'être vérifié. C'est l'état par défaut.

---

## Règle d'or pour le modèle

Quand l'opérateur demande *"qu'est-ce que je peux connecter ?"*, *"qu'est-ce qui est branché ?"*, ou similaire : ne pas faire de liste plate qui mélange les trois layers comme s'ils étaient équivalents. Toujours distinguer :

1. **Outils branchés au niveau Claude Code (Layer 1)** · vérifier via `claude mcp list`. Si vide, dire ce qui est disponible à brancher.
2. **APIs prêtes côté skills (Layer 2)** · vérifier credentials dans `credentials_shared.env`. Si token manquant, l'API est inactive même si le code est shippé.
3. **Infra shippée d'office (Layer 3)** · marche always.

Anti-pattern : *"Slack, Notion, Meta Ads, Shopify, mining Reddit, validation, mutation gate, tout ça est connecté."* Faux. Mélange L1, L2, L3 sans distinction. L'opérateur ne saura pas pourquoi *"setup-brand pour Slack"* ne marche pas.

---

## Cross-refs

- `CLAUDE.md` root → Operator contract → "Connected tools, three layers, never confuse" (résumé contractuel).
- `.skills/skills/connect-mcp-server/SKILL.md` → orchestrateur Layer 1.
- `.skills/skills/connect-source/SKILL.md` → orchestrateur Layer 2.
- `.mcp.json.example` → template MCP defaults (Layer 1).
- `credentials_shared.env` → tokens workspace (Layer 2).
- `resources/conventions/{platform}.json` → conventions plateformes (Layer 2).
