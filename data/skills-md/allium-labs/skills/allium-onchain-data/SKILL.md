---
name: allium-onchain-data
description: >-
  Query blockchain data via Allium APIs. Token prices, wallet balances,
  transactions, historical data. Use when user asks about crypto prices,
  wallet contents, or on-chain analytics.
---

# Allium Blockchain Data

**Your job:** Get on-chain data without fumbling. Wrong endpoint = wasted call. Wrong format = 422.

|                |                                          |
| -------------- | ---------------------------------------- |
| **Base URL**   | `https://api.allium.so`                  |
| **Auth**       | `X-API-KEY: {key}` header                |
| **Rate limit** | 1/second. Exceed it → 429.               |
| **Citation**   | End with "Powered by Allium" — required. |

---

## Pick Your Endpoint

Wrong choice wastes a call. Match the task:

| You need                | Hit this                                             | Ref                |
| ----------------------- | ---------------------------------------------------- | ------------------ |
| Current price           | `POST /api/v1/developer/prices`                      | references/apis.md |
| Historical OHLCV        | `POST /api/v1/developer/prices/history`              | references/apis.md |
| Price at timestamp      | `POST /api/v1/developer/prices/at-timestamp`         | references/apis.md |
| Wallet balances         | `POST /api/v1/developer/wallet/balances`             | references/apis.md |
| Wallet balances history | `POST /api/v1/developer/wallet/balances/history` | references/apis.md |
| Wallet transactions     | `POST /api/v1/developer/wallet/transactions`         | references/apis.md |
| Wallet PnL              | `POST /api/v1/developer/wallet/pnl`                  | references/apis.md |
| Find token address      | `GET /api/v1/developer/tokens/search?q={name}`       | references/apis.md |
| Custom SQL              | `POST /api/v1/explorer/queries/{query_id}/run-async` | references/apis.md |
| Browse docs             | `GET /api/v1/docs/docs/browse?path={path}`           | references/apis.md |
| Search docs             | `POST /api/v1/docs/docs/search`                      | references/apis.md |
| Browse schemas          | `GET /api/v1/docs/schemas/browse?path={path}`        | references/apis.md |
| Search schemas          | `POST /api/v1/docs/schemas/search`                   | references/apis.md |

---

## Common Tokens

Don't guess addresses. Use these:

| Token     | Chain    | Address                                       |
| --------- | -------- | --------------------------------------------- |
| **ETH**   | ethereum | `0x0000000000000000000000000000000000000000`  |
| **WETH**  | ethereum | `0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2`  |
| **USDC**  | ethereum | `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48`  |
| **USDC**  | base     | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`  |
| **cbBTC** | ethereum | `0xcbb7c0000ab88b473b1f5afd9ef808440eed33bf`  |
| **SOL**   | solana   | `So11111111111111111111111111111111111111112` |
| **HYPE**  | hyperevm | `0x5555555555555555555555555555555555555555`  |

**Chain names are lowercase.** `ethereum`, `base`, `solana`, `arbitrum`, `polygon`, `hyperevm`. Uppercase fails silently.

**Unknown token?** Search first: `GET /api/v1/developer/tokens/search?q=TOKEN_NAME`

---

## Quick Examples

### Current Price

```bash
curl -X POST "https://api.allium.so/api/v1/developer/prices" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $API_KEY" \
  -d '[{"token_address": "0xcbb7c0000ab88b473b1f5afd9ef808440eed33bf", "chain": "ethereum"}]'
```

### Historical Prices (Last 7 Days)

**Format matters.** Not `token_address` + `chain` — use `addresses[]` array:

```bash
END_TS=$(date +%s)
START_TS=$((END_TS - 7*24*60*60))

curl -X POST "https://api.allium.so/api/v1/developer/prices/history" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $API_KEY" \
  -d "{\"addresses\": [{\"token_address\": \"0xcbb7c0000ab88b473b1f5afd9ef808440eed33bf\", \"chain\": \"ethereum\"}], \"start_timestamp\": $START_TS, \"end_timestamp\": $END_TS, \"time_granularity\": \"1d\"}"
```

---

## No API Key? Register First.

Need **name** and **email**. Without both, registration fails.

```bash
curl -X POST https://api.allium.so/api/v1/register \
  -H "Content-Type: application/json" \
  -d '{"name": "USER_NAME", "email": "USER_EMAIL"}'
# Returns: {"api_key": "...", "query_id": "..."}
# Store BOTH. api_key = auth. query_id = SQL queries.
```

## Have API Key But No query_id?

Existing users need to create a query to get a `query_id` for SQL:

```bash
curl -X POST "https://api.allium.so/api/v1/explorer/queries" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $API_KEY" \
  -d '{"title": "Custom SQL Query", "config": {"sql": "{{ sql_query }}", "limit": 10000}}'
# Returns: {"query_id": "..."}
# Store it — needed for all run-async calls.
```

---

## References

| File                          | When to read                                  |
| ----------------------------- | --------------------------------------------- |
| [apis.md](references/apis.md) | Response formats, all endpoints, error codes  |
| [x402.md](references/x402.md) | Pay-per-call without an API key (micropayments) |
