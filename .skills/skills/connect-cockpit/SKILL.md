---
name: connect-cockpit
type: orchestrator
version: "1.1.0"
recommended_model: sonnet
reasoning_pattern: null
description: >
  Connect a brand workspace to the Abyss cockpit dashboard at app.abyss-initiative.com.
  Provisions Airbyte sources + Supabase rows server-side via POST /api/operator/onboard-brand
  so KPIs flow into the cockpit within 24h. Reads `connectors.json` registry to drive
  per-platform credential collection (Shopify, Meta, TikTok, Snap, Google Ads, GA4).
  Adding a new platform = 1 entry in connectors.json, no code change.
  Runs AFTER setup-brand (the workspace must already exist locally).
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
    - Operator has admin access on each platform at the moment of setup (token generation requires admin).
  postconditions: |
    - Brand row exists in Supabase clients table.
    - Per-platform Airbyte sources + connections provisioned.
    - First data lands in cockpit within 24h (sync schedule daily).
    - Operator gets the cockpit link to verify.
disambiguates_against:
  setup-brand: "route to setup-brand for the workspace folder structure (brand.json, products, audience). connect-cockpit assumes that's already done."
  onboard-brand: "route to onboard-brand for the full 4-step pipeline (setup + URL scan + ingest + validate). connect-cockpit only handles the cockpit data plumbing."
  connect-source: "route to connect-source to register a new platform convention in PhantomOS itself (resources/conventions/). connect-cockpit consumes existing conventions to feed the Abyss cockpit."
---

# Skill: connect-cockpit

Wire a brand to the Abyss cockpit dashboard. The operator pastes platform tokens, the skill provisions Airbyte sources and Supabase rows server-side. First data lands in the cockpit within 24h.

This skill is the **data plumbing** layer · presupposes the brand workspace already exists. Run `setup-brand` first if needed.

**Architecture · registry-driven.** All platform-specific knowledge (required fields, where-to-find instructions, server-side fallbacks) lives in `connectors.json`. The skill reads that file at runtime and loops over the chosen platforms. No platform-specific logic in this SKILL.md. Adding a new source (Klaviyo, Pinterest, X Ads, etc.) = 1 entry in `connectors.json`.

---

## Hard prerequisite · admin access on each platform

To generate the OAuth tokens / System User tokens / refresh_tokens that this skill consumes, the operator MUST have **admin-level access on each platform's account at the moment of setup**. Each platform's `admin_required` field in `connectors.json` spells out the minimum role.

After the token is generated, the access on the original account can be downgraded · the token keeps working.

If the operator only has analyst / viewer · ask the client to elevate temporarily, OR fallback to Largo (DM the credentials, he POSTs the API).

---

## Tone

Colleague helping with setup. The operator never sees JSON payloads, source IDs, namespaces, or Airbyte internals. They see clear questions about credentials and plain-language confirmations.

**Never expose** : `client_id` (cockpit DB), `connection_id`, `source_id`, raw error stack traces, payload schemas, the registry JSON itself. Reword in domain language: "brand created", "Shopify connected", "Meta source configured", "we'll see data in 24h".

---

## Question rule · 1 per turn, never 2

Same hard rule as setup-brand: ask **ONE** question per agent message. If multiple infos needed, pick the most structuring · the rest comes naturally next turn.

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

## Step 2 · Choose platforms

Read `.skills/skills/connect-cockpit/connectors.json`. For each entry, show `label` + `tagline` in a checklist format. Mark `admin_required` next to each.

Ask *"Quels canaux veux-tu brancher pour cette marque ?"*

Operator answers free-form ("Shopify et Meta", "tout sauf Google", "juste Shopify"). Parse into a list, confirm in one line.

---

## Step 3 · Per-platform credential collection

For each chosen platform, run the **registry-driven subflow** :

1. **Lookup spec** in `connectors.json#platforms[platform_key]`.
2. **Show admin reminder** if first turn on this platform : *"{platform.label} · {platform.admin_required} requis. Tu as le bon niveau d'accès ?"*. Skip if admin already confirmed.
3. **Show where-to-find** instructions verbatim from `platform.where_to_find` (one block, then ask the first field).
4. **Loop fields** in `platform.fields` array : ask one at a time, validate with `validate` rule if present (e.g. `endswith:.myshopify.com`), accept the value, move to next field.
5. **Optional fields** in `platform.fields_optional` : prompt with *"Optional : {prompt}. Press skip if not applicable."*.
6. **Server fallback** : do not ask for fields listed in `platform.server_fallback` · just acknowledge briefly *"Les champs {list} sont gérés côté serveur Abyss, tu n'as pas à les fournir."*.
7. **Special handling** : if `platform.ingest_method == "manual_cron"`, mention `platform.ingest_note` in operator-facing summary so they know it's not Airbyte but works the same.
8. **Fallback path** : if operator stuck, surface `platform.fallback_path` (e.g. Snap → DM Largo).

Never collect two platforms in parallel. One at a time, finish one before moving to the next.

---

## Step 4 · Provision via API

Once ALL credentials collected for the chosen platforms, build the payload :

```json
{
  "slug": "{slug}",
  "brand_name": "{brand_name}",
  "platforms": {
    "{platform_key}": { "{KEY}": "{value}", ... }
  }
}
```

POST to `${ABYSS_API_BASE}/api/operator/onboard-brand` with header `Authorization: Bearer ${ABYSS_OPERATOR_TOKEN}`.

Both env vars live in `credentials_shared.env` (workspace level), provisioned by Largo via `onboard-operator`.

**Annonce avant le POST** : *"Je provisionne tout côté serveur · ça prend 1-2 minutes (création sources Airbyte, encrypt credentials, INSERT Supabase rows)."*

**Don't expose** : the actual JSON payload, source IDs returned, namespace strings.

---

## Step 5 · Handle response

### Success (200, `ok: true`)

Affiche :
```
Marque {brand_name} branchée au cockpit ✓

Sources connectées :
✓ {platform_label_1}
✓ {platform_label_2}
...

Première sync prévue dans la nuit (cron Airbyte ~04:00 UTC).
Les KPIs apparaitront dans le cockpit demain matin :
→ https://app.abyss-initiative.com/?brand={slug}
```

Si certains platforms ont échoué partiellement (`status: "failed"` dans la réponse), liste-les distinctement :
```
⚠ {platform_label} a échoué : {plain-language reason}.
```

### Failure (non-200, network error, auth invalid)

Trois causes principales :
1. **401** : `ABYSS_OPERATOR_TOKEN` expiré ou manquant → demande à Largo de regenerate via `onboard-operator`.
2. **400** : platform credentials malformés → re-demande le platform en question.
3. **500** : serveur cockpit down ou Airbyte VPS unreachable → attendre 5 min et réessayer.

Ne JAMAIS retry automatiquement plus de 1 fois.

---

## Step 6 · Close

Une fois success, propose 1-2 actions max (suggestion regime guide-rail) :
- *"Tu veux brancher une autre marque ?"*
- Ou si setup-brand a juste tourné : *"On peut maintenant ingest les docs que tu as collectés pendant le setup."*

---

## Output Format

```
Cockpit branché · {brand_name}

Sources actives :
{liste des platforms onboardés}

Première data : {tomorrow_date} (sync nocturne Airbyte)
Cockpit       : https://app.abyss-initiative.com/?brand={slug}

{1-2 suggestion actions max}
```

---

## Hard Rules

- **NEVER expose** payload JSON, IDs, Airbyte namespaces, or Supabase columns to the operator.
- **NEVER ask 2 questions in one message.** Sequence fields one by one.
- **NEVER retry a failed POST silently more than 1 time.** Risk of orphan Airbyte sources.
- **NEVER persist credentials in the workspace.** Only pass them through the POST.
- **NEVER ask for fields listed in `platform.server_fallback`** · server provides them.
- **ALWAYS confirm brand identity in Step 1.**
- **ALWAYS show a concrete next-day ETA** in the success message.
- **ALWAYS handle partial-success gracefully** · list which platforms succeeded vs failed, never roll back the successes.
- **ALWAYS read connectors.json fresh on invocation** · the registry is the source of truth for platform specs, never hardcode platform fields in this SKILL.md.

---

## Limits known v1

| Limit | Workaround |
|---|---|
| Snap OAuth flow chiant | If operator can't get refresh_token, DM the 5 fields to Largo who POSTs the API for them |
| Connector drift (Meta API breaking changes weekly) | Server-side `setupShopifyPipeline` / equivalents updated when breakage observed. Operator surfaces the error to Largo, doesn't troubleshoot Airbyte. |
| First sync 24h delay | Airbyte cron schedule daily · cannot trigger on-demand from this skill v1 |
| No idempotency on re-run | If brand already exists, API returns 409 · operator must use a separate `/refresh-platform` flow |
| Admin access required at setup | Hard prereq, no workaround. See Hard prerequisite section above. |
