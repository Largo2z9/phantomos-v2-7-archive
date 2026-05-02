---
name: connect-cockpit
type: builder
version: "1.0.0"
recommended_model: sonnet
description: >
  Connect a brand workspace to the Abyss cockpit dashboard at app.abyss-initiative.com.
  Provisions Airbyte sources + Supabase rows for the brand so KPIs flow into the cockpit
  within 24h. Runs AFTER setup-brand (the workspace must already exist locally).
  Guided collection of platform credentials (Shopify, Meta, TikTok, Snapchat, Google Ads, GA4),
  one platform at a time, with concrete instructions on where to fetch each token.
  FR: "branche le cockpit", "connecte le dashboard", "active les data sources", "setup cockpit",
      "onboard cockpit", "connecte cette marque au cockpit", "branche les sources data".
  EN: "connect cockpit", "wire dashboard", "activate data sources", "onboard cockpit",
      "hook brand to cockpit dashboard".
permissions:
  reads: [brand]
  writes: []
  mode: direct
  subagent_safe: false
pipeline:
  preconditions: |
    - Brand workspace exists (setup-brand was run prior, or operator confirms slug + name).
    - credentials_shared.env contains ABYSS_OPERATOR_TOKEN + ABYSS_API_BASE.
    - Operator has the platform tokens ready (or knows where to fetch them).
  postconditions: |
    - Brand row exists in Supabase clients table.
    - Per-platform Airbyte sources + connections provisioned.
    - First data lands in cockpit within 24h (sync schedule daily).
    - Operator gets the cockpit link to verify.
disambiguates_against:
  setup-brand: "route to setup-brand for the workspace folder structure (brand.json, products, audience). connect-cockpit assumes that's already done."
  onboard-brand: "route to onboard-brand for the full 4-step pipeline (setup + URL scan + ingest + validate). connect-cockpit only handles the cockpit data plumbing."
---

# Skill: connect-cockpit

Wire a brand to the Abyss cockpit dashboard. The operator pastes platform tokens, the skill provisions Airbyte sources and Supabase rows server-side via `POST /api/operator/onboard-brand`. First data lands in the cockpit within 24h.

This skill is the **data plumbing** layer · it presupposes the brand workspace already exists (folders, brand.json, etc.). Run `setup-brand` first if needed.

---

## Tone

Colleague helping with setup. The operator never sees JSON payloads, source IDs, namespaces, or Airbyte internals. They see clear questions about credentials and plain-language confirmations.

**Never expose** : `client_id`, `connection_id`, `source_id`, raw error stack traces, payload schemas. Reword in domain language: "brand created", "Shopify connected", "Meta source configured", "we'll see data in 24h".

---

## Question rule · 1 per turn, never 2

Same hard rule as setup-brand: ask **ONE** question per agent message. If multiple infos needed, pick the most structuring · the rest comes naturally next turn.

---

## Fast-path · skip what's already known

Before asking each question, scan previous operator messages and `brand.json` if present:
- **Brand name + slug** → if a brand workspace was just configured via setup-brand, read its `brand.json` to pre-fill. Confirm in one line, no question.
- **Platforms requested** → if operator mentioned "connect Meta and Shopify" upfront, pre-select those · skip the platform-list question.

Binary rule : info known = zero question on that info.

---

## Step 1 · Confirm brand identity

Read the active brand from workspace context (last `setup-brand` run, or current `brands/{slug}/brand.json`).

Show in one block:
```
Brand    : {brand_name}
Slug     : {slug}
Currency : {currency}    # default EUR if unspecified
```

Ask : *"Confirme la marque, ou dis-moi le bon nom."*

If no brand context exists in workspace → ask *"Quelle marque veut-on brancher au cockpit ?"* and require name + slug minimum before continuing.

---

## Step 2 · Choose platforms to connect

Show the menu of available platforms with current status:

| Platform | Status | Notes |
|---|---|---|
| **Shopify** | ✅ Self-serve | Admin API token, easy to generate |
| **Meta Ads** | ⚠️ Self-serve | Needs Marketing API access on the ad account |
| **TikTok Ads** | ✅ Self-serve | Business Center developer app required |
| **Snapchat Ads** | ✅ Self-serve | Business Manager OAuth app required |
| **Google Ads** | 🔴 Blocked | Awaiting Google dev token approval (Largo external action) |
| **GA4** | ✅ Self-serve | Same Google OAuth as Google Ads, but works without dev token |

Ask *"Quels canaux veux-tu brancher pour cette marque ?"*

Operator answers free-form ("Shopify et Meta", "tout sauf Google", "juste Shopify pour commencer"). Parse into a list, confirm in one line.

---

## Step 3 · Collect credentials per platform · one at a time

For each chosen platform, run the corresponding **subflow**. Never collect two platforms in parallel · one at a time, finish one before moving to the next.

### Shopify subflow

Need 2 things:
1. `SHOPIFY_STORE` · the shop domain (e.g. `{your-shop}.myshopify.com`)
2. `SHOPIFY_ADMIN_TOKEN` · Admin API access token

Where to find the token (paste this verbatim if operator asks):
> Dans le back-office Shopify : Settings → Apps and sales channels → Develop apps → Create an app → API credentials. Active les scopes `read_orders, read_products, read_customers, read_inventory`. Le token apparait après "Install app". Copie celui qui commence par `shpat_`.

Ask one question : *"Donne-moi le shop_domain et l'Admin API token (ou colle juste les deux dans un message)."*

Validate format quickly : domain ends with `.myshopify.com`, token starts with `shpat_`. If wrong, ask again with a hint.

### Meta Ads subflow

Need 2 things:
1. `META_AD_ACCOUNT_ID` · format `act_1234567890`
2. `META_ACCESS_TOKEN` · long-lived Marketing API token (System User token from Business Manager)

Where to find:
> Business Manager → Business Settings → System Users → Create or pick existing → Generate New Token → choisis l'app + scopes `ads_read, ads_management`. Le token expire jamais si System User. L'ad account ID est visible dans Ads Manager URL (`act_XXXXXXXX`).

**Important pour Matteo** · si la marque cliente n'a jamais partagé l'access, demander au client d'ajouter Abyss Business Manager comme partner sur leur ad account. Sinon l'access token ne donnera aucune visibilité.

Ask : *"Donne-moi l'ad account ID (format act_xxx) et le System User token."*

### TikTok Ads subflow

Need 4 things:
1. `TIKTOK_ADVERTISER_ID`
2. `TIKTOK_ACCESS_TOKEN`
3. `TIKTOK_APP_ID`
4. `TIKTOK_APP_SECRET`

Where to find:
> TikTok Business Center → Developer Portal → Create a Marketing API App → après approbation, l'app a app_id + app_secret. Pour générer un access_token, suivre le flow OAuth Long-term Authorization (24h max sans refresh, sinon system user). L'advertiser_id est l'ID du compte pub dans Business Center.

Ask one at a time : advertiser_id d'abord, puis access_token, puis app_id, puis app_secret.

### Snapchat Ads subflow

Need 5 things:
1. `SNAP_AD_ACCOUNT_ID`
2. `SNAP_ORGANIZATION_ID`
3. `SNAP_CLIENT_ID`
4. `SNAP_CLIENT_SECRET`
5. `SNAP_REFRESH_TOKEN`

Where to find:
> Snapchat Business Manager → Settings → Business Details : organization ID. Ad accounts : ad_account_id. Pour client_id/client_secret/refresh_token, créer une OAuth app via developers.snapchat.com → Marketing API → suivre le flow Authorization Code grant pour obtenir un refresh_token.

Snap est le plus chiant des 6 · si Matteo galère, propose-lui d'envoyer les creds à Largo en privé qui peut faire le setup OAuth pour lui.

### GA4 subflow (si choisi sans Google Ads)

Need 4 things (réutilise le même Google OAuth que Google Ads sauf pour le dev_token) :
1. `GA4_PROPERTY_ID`
2. `GOOGLE_CLIENT_ID`
3. `GOOGLE_CLIENT_SECRET`
4. `GOOGLE_REFRESH_TOKEN`

Where to find:
> Google Cloud Console → APIs & Services → Credentials → OAuth client ID (type Web). Le refresh_token s'obtient via OAuth Playground ou flow custom. Le property_id de GA4 est dans Admin → Property Settings.

### Google Ads subflow

🔴 **Bloqué actuellement.** Si l'operator choisit Google Ads, dis-lui :
> Le connecteur Google Ads attend la validation du developer token côté Google (action externe Largo, ~1-3 semaines de délai Google). Pour l'instant on skip Google Ads · tu peux brancher GA4 séparément si tu veux les sessions/funnel sans le ad data.

Skip ce platform et continue avec les autres.

---

## Step 4 · Provision via API

Une fois TOUS les credentials collectés pour les platforms choisis, build le payload :

```json
{
  "slug": "{slug}",
  "brand_name": "{brand_name}",
  "platforms": {
    "shopify": { "SHOPIFY_STORE": "...", "SHOPIFY_ADMIN_TOKEN": "..." },
    "meta": { "META_AD_ACCOUNT_ID": "...", "META_ACCESS_TOKEN": "..." }
  }
}
```

POST le à `${ABYSS_API_BASE}/api/operator/onboard-brand` avec header `Authorization: Bearer ${ABYSS_OPERATOR_TOKEN}`.

`ABYSS_API_BASE` et `ABYSS_OPERATOR_TOKEN` sont dans `credentials_shared.env` (workspace level).

**Annonce avant le POST** : *"Je provisionne tout côté serveur · ça prend 1-2 minutes (création sources Airbyte, encrypt credentials, INSERT Supabase rows)."*

**Don't expose** : the actual JSON payload, source IDs returned, namespace strings.

---

## Step 5 · Handle response

### Success (200, `ok: true`)

Affiche :
```
Marque {brand_name} branchée au cockpit ✅

Sources connectées :
✅ Shopify
✅ Meta Ads
✅ TikTok Ads

Première sync prévue dans la nuit (cron Airbyte ~04:00 UTC).
Les KPIs apparaitront dans le cockpit demain matin :
→ https://app.abyss-initiative.com/?brand={slug}
```

Si certains platforms ont échoué partiellement (`status: "failed"` dans la réponse), liste-les distinctement sans paniquer :
```
⚠️ Snap a échoué : refresh_token invalide. Tu peux réessayer ce platform isolément avec /connect-cockpit ou le faire ajouter manuellement par Largo.
```

### Failure (non-200, network error, auth invalid)

Trois causes principales :
1. **401** : `ABYSS_OPERATOR_TOKEN` expiré ou manquant. Demande à Largo de regenerate via `onboard-operator`.
2. **400** : platform credentials malformés. Re-demande le platform en question.
3. **500** : serveur cockpit down ou Airbyte VPS unreachable. Lui dire d'attendre 5 min et réessayer.

Ne JAMAIS retry automatiquement plus de 1 fois · les retries silencieux multiplient les sources orphelines côté Airbyte.

---

## Step 6 · Close

Une fois success, propose 1-2 actions max (suggestion regime guide-rail) :
- *"Tu veux brancher une autre marque ?"*
- Ou si setup-brand a juste tourné : *"On peut maintenant ingest les docs que tu as collectés pendant le setup."*

Ne propose pas de naviguer vers le cockpit · l'operator le fera de lui-même.

---

## Output Format

```
🔗 Cockpit branché · {brand_name}

Sources actives :
{liste des platforms onboardés}

Première data : {tomorrow_date} (sync nocturne Airbyte)
Cockpit       : https://app.abyss-initiative.com/?brand={slug}

{1-2 suggestion actions max}
```

---

## Hard Rules

- **NEVER expose** payload JSON, IDs (client_id, source_id, connection_id), Airbyte namespace strings, or Supabase columns to the operator.
- **NEVER ask 2 questions in one message.** Even if 2 fields belong to the same platform, sequence them.
- **NEVER retry a failed POST silently more than 1 time.** Risk of orphan Airbyte sources.
- **NEVER attempt Google Ads** until Largo confirms dev_token approved · skip with explanation.
- **NEVER persist credentials in the workspace** · only pass them through the POST. The server encrypts and stores them in Supabase `account_credentials` table.
- **ALWAYS confirm brand identity in Step 1** · pulling slug + name from `brand.json` if available, asking if not.
- **ALWAYS show a concrete next-day ETA** in the success message · "demain matin" not "soon".
- **ALWAYS handle partial-success gracefully** · list which platforms succeeded vs failed, never roll back the successes.

---

## Limits known v1

| Limit | Workaround |
|---|---|
| Google Ads dev token pending | Skip platform, brand still onboards on remaining platforms |
| Meta App Review (if operator uses Abyss-OAuth instead of System User) | Operator must use System User token from client's BM, not Abyss-managed OAuth |
| First sync 24h delay | Airbyte cron schedule daily · cannot trigger on-demand from this skill v1 |
| No idempotency on re-run | If brand already exists, API returns 409 · operator must use a separate `/refresh-platform` flow |
