---
name: ic-dashboard
description: "Query the public REST APIs that power dashboard.internetcomputer.org. Covers canister metadata, ICRC ledger data, SNS data, ICP ledger, and network metrics with cursor-based pagination. Use when fetching canister info, token data, SNS proposals, or network stats via HTTP from off-chain code. No canister deployment or cycles needed."
license: Apache-2.0
metadata:
  title: IC Dashboard APIs
  category: Integration
---

# IC Dashboard APIs

## What This Is

These public REST APIs power **dashboard.internetcomputer.org**. They expose read-only access to canister metadata, ICRC ledgers, SNS data, the ICP ledger, and network metrics via OpenAPI specs and Swagger UI. Agents and scripts can call them over HTTPS from off-chain (no canister deployment or cycles required). **Prefer v2 or higher API versions** where available; they provide cursor-based pagination (`after`, `before`, `limit`) and are the same surface the dashboard uses.

## Prerequisites

- Any HTTP client: `curl`, `fetch`, `axios`, or the language’s native HTTP library.
- No `icp-cli` or canister deployment needed for read-only API access.
- For OpenAPI-based codegen: optional use of the `openapi.json` URLs with your preferred OpenAPI tooling.

## API Base URLs and Docs

| API | Base URL | OpenAPI spec | Swagger / Docs | Prefer |
|-----|----------|--------------|----------------|--------|
| IC API | `https://ic-api.internetcomputer.org` | `/api/v3/openapi.json` | `/api/v3/swagger` | v4 for canisters, subnets (cursor pagination) |
| ICRC API | `https://icrc-api.internetcomputer.org` | `/openapi.json` | `/docs` | v2 for ledgers (TestICP and other ICRC tokens; **not** mainnet ICP) |
| SNS API | `https://sns-api.internetcomputer.org` | `/openapi.json` | `/docs` | v2 for snses, proposals, neurons |
| Ledger API (mainnet ICP) | `https://ledger-api.internetcomputer.org` | `/openapi.json` | `/swagger-ui/` | Use for **ICP token**; v2 for cursor pagination |
| Metrics API | `https://metrics-api.internetcomputer.org` | `/api/v1/openapi.json` | `/api/v1/docs` | v1 (no newer version) |

Full URLs for specs and UI:

- IC API: https://ic-api.internetcomputer.org/api/v3/openapi.json — https://ic-api.internetcomputer.org/api/v3/swagger
- ICRC API: https://icrc-api.internetcomputer.org/openapi.json — https://icrc-api.internetcomputer.org/docs
- SNS API: https://sns-api.internetcomputer.org/openapi.json — https://sns-api.internetcomputer.org/docs
- Ledger API: https://ledger-api.internetcomputer.org/openapi.json — https://ledger-api.internetcomputer.org/swagger-ui/
- Metrics API: https://metrics-api.internetcomputer.org/api/v1/openapi.json — https://metrics-api.internetcomputer.org/api/v1/docs

## How It Works

1. **Prefer v2+ APIs with cursor pagination.** IC API v4 (`/api/v4/canisters`, `/api/v4/subnets`), ICRC API v2 (`/api/v2/ledgers`, `/api/v2/ledgers/{id}/transactions`, etc.), and SNS API v2 (`/api/v2/snses`, `/api/v2/snses/{id}/proposals`, `/api/v2/snses/{id}/neurons`) use `after`, `before`, and `limit` for stable, efficient paging. Avoid v1/offset-based endpoints when a v2+ alternative exists.
2. **Choose the right API** for the data you need: IC API (canisters, subnets, NNS neurons/proposals), **Ledger API for mainnet ICP** (accounts, transactions, supply), ICRC API for **other** ICRC ledgers only (ckBTC, SNS tokens, testicp — ICRC API does not expose mainnet ICP), SNS API (SNS list, neurons, proposals), Metrics API (governance, cycles, Bitcoin, etc.).
3. **Use the OpenAPI spec** to get exact path, query, and body schemas and response shapes; prefer the spec over hand-written docs to avoid drift.
4. **Call over HTTPS** with `GET` (or documented method). Use the `next_cursor` / `previous_cursor` from v2+ responses to request the next or previous page.

## Mistakes That Break Your Build

1. **Wrong base URL or API version.** IC API uses `/api/v3/` (and v4 for canisters/subnets); ICRC has `/api/v1/` and `/api/v2/` (ICRC API does not serve mainnet ICP — use Ledger API). Ledger API uses unversioned paths for some endpoints (e.g. `/accounts`, `/supply/total/latest`) and `/v2/` for cursor-paginated lists. Metrics API uses `/api/v1/`. Using the wrong prefix returns 404 or wrong schema.

2. **Canister ID format.** Canister IDs in paths and queries must match the principal-like pattern: 27 characters, five groups of five plus a final three (e.g. `ryjl3-tyaaa-aaaaa-aaaba-cai`). Subnet IDs use the longer pattern (e.g. 63 chars). Sending a raw principal string in the wrong encoding or length causes 422 or 400.

3. **Using ICRC API for mainnet ICP.** ICRC API exposes **test ICP (TestICP) only**, not mainnet ICP. For mainnet ICP token data (accounts, transactions, supply) use **Ledger API** (`ledger-api.internetcomputer.org`). Use ICRC API for other ICRC ledgers (e.g. ckBTC, SNS tokens) and for TestICP.

4. **ICRC API: ledger_canister_id in path.** ICRC endpoints require `ledger_canister_id` in the path (e.g. `/api/v2/ledgers/{ledger_canister_id}/transactions`). Use the canister ID of the ledger you want (e.g. ckBTC `mxzaz-hqaaa-aaaar-qaada-cai`). Do not use ICRC API for mainnet ICP — use Ledger API instead.

5. **Using v1 or offset-based pagination when v2+ exists.** Always prefer v2 or higher endpoints that support cursor pagination (`after`, `before`, `limit`). IC API v4 (canisters, subnets), ICRC API v2 (ledgers, accounts, transactions), and SNS API v2 (snses, proposals, neurons) return `next_cursor`/`previous_cursor` and accept cursor query params. Older v1/offset/`max_*_index` endpoints are legacy; using the wrong pagination model returns empty or incorrect pages.

6. **Timestamps.** Most time-range query params (`start`, `end`) expect Unix seconds (integer). Sending milliseconds or ISO strings causes validation errors (422).

7. **Account identifier format.** Ledger API and ICRC/ICP endpoints use **account identifiers** (hex hashes), not raw principals, for account-specific paths. Use the same encoding the API documents (e.g. 64-char hex for account_identifier where required).

8. **Assuming authentication.** These public dashboard APIs do not require API keys or auth for the documented read endpoints. If you get 401/403, confirm you are not hitting a different environment or a write endpoint that requires auth.

## Implementation

### IC API — Canisters and subnets (prefer v4 with cursor pagination)

```bash
# List canisters (v4: cursor pagination, next_cursor/previous_cursor in response)
curl -s "https://ic-api.internetcomputer.org/api/v4/canisters?limit=5"

# Next page: use after= from previous response's next_cursor (see OpenAPI for cursor format)
# curl -s "https://ic-api.internetcomputer.org/api/v4/canisters?limit=5&after=..."

# Get one canister by ID (v3; no v4 single-canister endpoint)
curl -s "https://ic-api.internetcomputer.org/api/v3/canisters/ryjl3-tyaaa-aaaaa-aaaba-cai"

# List subnets (v4: cursor pagination)
curl -s "https://ic-api.internetcomputer.org/api/v4/subnets?limit=10"

# List NNS proposals (v3; use limit)
curl -s "https://ic-api.internetcomputer.org/api/v3/proposals?limit=5"
```

### ICRC API — Other ICRC ledgers only (v2 with cursor pagination)

ICRC API exposes **TestICP and other ICRC ledgers (e.g. ckBTC, SNS tokens), not mainnet ICP.** For mainnet ICP use Ledger API.

```bash
# List ledgers (v2: after/before/limit, next_cursor/previous_cursor in response)
curl -s "https://icrc-api.internetcomputer.org/api/v2/ledgers?limit=10"

# Get one ledger (e.g. ckBTC — mainnet ICP is not on ICRC API)
curl -s "https://icrc-api.internetcomputer.org/api/v2/ledgers/mxzaz-hqaaa-aaaar-qaada-cai"

# List transactions for a ledger (v2: cursor pagination)
curl -s "https://icrc-api.internetcomputer.org/api/v2/ledgers/mxzaz-hqaaa-aaaar-qaada-cai/transactions?limit=5"

# List accounts for a ledger (v2: after/before/limit)
curl -s "https://icrc-api.internetcomputer.org/api/v2/ledgers/mxzaz-hqaaa-aaaar-qaada-cai/accounts?limit=10"
```

### SNS API — SNS list and proposals (prefer v2 with cursor pagination)

```bash
# List SNSes (v2: after/before/limit, next_cursor/previous_cursor)
curl -s "https://sns-api.internetcomputer.org/api/v2/snses?limit=10"

# List proposals for an SNS root canister (v2: cursor pagination)
# Replace ROOT_CANISTER_ID with a real SNS root canister ID
curl -s "https://sns-api.internetcomputer.org/api/v2/snses/ROOT_CANISTER_ID/proposals?limit=5"

# List neurons for an SNS (v2: after/before/limit)
curl -s "https://sns-api.internetcomputer.org/api/v2/snses/ROOT_CANISTER_ID/neurons?limit=10"
```

### Ledger API — Mainnet ICP token (prefer v2 for cursor pagination)

```bash
# List accounts (v2: after/before/limit, next_cursor/prev_cursor)
curl -s "https://ledger-api.internetcomputer.org/v2/accounts?limit=10"

# Get account by account_identifier (64-char hex)
curl -s "https://ledger-api.internetcomputer.org/accounts/ACCOUNT_IDENTIFIER"

# List transactions (v2: cursor pagination)
curl -s "https://ledger-api.internetcomputer.org/v2/transactions?limit=10"

# Total supply (latest)
curl -s "https://ledger-api.internetcomputer.org/supply/total/latest"
```

### Metrics API

```bash
# Average cycle burn rate
curl -s "https://metrics-api.internetcomputer.org/api/v1/average-cycle-burn-rate"

# Governance metrics
curl -s "https://metrics-api.internetcomputer.org/api/v1/governance-metrics"

# ICP/XDR conversion rates (with optional start/end/step)
curl -s "https://metrics-api.internetcomputer.org/api/v1/icp-xdr-conversion-rates?start=1700000000&end=1700086400&step=86400"
```

### Fetching OpenAPI spec (for codegen or validation)

```bash
# IC API v3
curl -s "https://ic-api.internetcomputer.org/api/v3/openapi.json" -o ic-api-v3.json

# ICRC API
curl -s "https://icrc-api.internetcomputer.org/openapi.json" -o icrc-api.json

# SNS API
curl -s "https://sns-api.internetcomputer.org/openapi.json" -o sns-api.json

# Ledger API
curl -s "https://ledger-api.internetcomputer.org/openapi.json" -o ledger-api.json

# Metrics API v1
curl -s "https://metrics-api.internetcomputer.org/api/v1/openapi.json" -o metrics-api-v1.json
```

## Deploy & Test

No canister deployment is required. These are external HTTP APIs. Test from the shell or your app:

```bash
# Smoke test: IC API root
curl -s -o /dev/null -w "%{http_code}" "https://ic-api.internetcomputer.org/api/v3/"
# Expected: 200

# Smoke test: ICRC ledgers list
curl -s -o /dev/null -w "%{http_code}" "https://icrc-api.internetcomputer.org/api/v2/ledgers?limit=1"
# Expected: 200
```

## Verify It Works

```bash
# 1. IC API returns canister list with data array
curl -s "https://ic-api.internetcomputer.org/api/v3/canisters?limit=1" | head -c 200
# Expected: JSON with "data" or similar key and at least one canister

# 2. ICRC API returns ledger list
curl -s "https://icrc-api.internetcomputer.org/api/v2/ledgers?limit=1" | head -c 200
# Expected: JSON with "data" and ledger entries

# 3. Ledger API returns supply (array of [timestamp, value])
curl -s "https://ledger-api.internetcomputer.org/supply/total/latest"
# Expected: JSON array with two elements (timestamp and supply string)

# 4. OpenAPI specs are valid JSON
curl -s "https://ic-api.internetcomputer.org/api/v3/openapi.json" | python3 -c "import sys,json; json.load(sys.stdin); print('OK')"
# Expected: OK
```
