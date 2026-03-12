---
name: etsy-api
description: >
  Manages Etsy shop operations (listings, inventory, receipts/orders, shop data, taxonomy, and webhooks)
  via Etsy Open API v3 with OAuth 2.0 + PKCE and rate-limit-aware request handling.
metadata:
  short-description: Etsy shop management and marketplace operations via Open API v3
allowed-tools: ["code_execution"]
---

# Etsy Open API v3 Skill

Use this skill when you need to **read or modify Etsy shop resources** using Etsy Open API v3, including:

- Listings: create drafts, update listing metadata, upload images/files, manage videos, update inventory/offerings
- Shop: retrieve/update shop settings, shop sections, shipping profiles, processing profiles, return policies
- Receipts/orders: retrieve receipts and transactions, post-purchase workflows
- Taxonomy: seller/buyer taxonomy nodes and properties
- Webhooks: create/rotate endpoints, subscribe to events, verify signatures

This skill package includes **reference docs** and **scripts** to make correct, rate-limit-aware requests.

## Authentication model (critical)

Etsy uses:

- **API key header** on **all** requests
- **OAuth 2.0 user tokens** (Authorization Code + PKCE) for scoped/private endpoints

### Required headers

All requests must include:

- `x-api-key: <ETSY_KEYSTRING>:<ETSY_SHARED_SECRET>`

Scoped endpoints additionally require:

- `Authorization: Bearer <ETSY_OAUTH_USER_ID>.<ETSY_OAUTH_ACCESS_TOKEN>`

> Note: Etsy’s Bearer token format includes the numeric user id, a dot (`.`), and then the access token.

See:
- `references/02_authentication.md`
- `references/03_request_standards.md`

## Rate limits (must follow)

Etsy enforces **per-application** rate limits:

- **QPS** (queries per second)
- **QPD** (queries per day) using a **rolling 24-hour sliding window**

When you receive HTTP `429`, honor the `retry-after` header and use exponential backoff.

See:
- `references/04_rate_limits.md`

## Scripts you can run (code_execution)

All scripts are under `skills/etsy-api/scripts/`.

### 1) Make requests safely

Use the CLI to perform an arbitrary request with proper headers:

```bash
python skills/etsy-api/scripts/etsy_cli.py request GET /v3/application/listings?state=active
```

You can pass a body for POST/PUT with `--data` (JSON) or `--form` (x-www-form-urlencoded).

### 2) OAuth helpers (PKCE + token exchange)

Generate a PKCE verifier/challenge and an authorization URL:

```bash
python skills/etsy-api/scripts/oauth_pkce.py auth-url --scopes "listings_r listings_w shops_r shops_w"
```

Exchange an authorization code for tokens:

```bash
python skills/etsy-api/scripts/oauth_pkce.py exchange-code --code "<AUTH_CODE>"
```

Refresh a token:

```bash
python skills/etsy-api/scripts/oauth_pkce.py refresh-token
```

### 3) Webhook verification

Verify a webhook signature locally:

```bash
python skills/etsy-api/scripts/webhook_verify.py verify --secret "$ETSY_WEBHOOK_SIGNING_SECRET" --headers-json headers.json --body-file body.json
```

## How to use this skill effectively

1. Prefer reading **references/** for policy, rate limits, and authentication details before coding.
2. Use `scripts/etsy_cli.py` for exploratory calls and to validate request shapes.
3. Cache responses where appropriate to reduce QPS/QPD usage.
4. Be careful when testing: follow Etsy’s API testing policy (draft listings, test prices, etc.). See `references/11_terms_and_policies.md`.

## Safety and compliance

- Never print or log secrets (shared secret, access token, refresh token).
- Avoid creating “real” listings/orders during testing; follow Etsy testing policy guidance.
- If uncertain about an endpoint’s parameters, consult the OpenAPI reference site or the OpenAPI spec.

