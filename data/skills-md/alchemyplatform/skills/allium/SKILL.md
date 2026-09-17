---
name: allium
description: Query Allium APIs for wallet PnL (current + historical, by-wallet and by-token), holdings timeseries history, Hyperliquid HyperCore trading data (info, fills, orders, orderbook), and custom SQL analytics across 70+ chains. NOT for token prices, token metadata, current wallet balance snapshots, transaction transfer history, or NFT metadata — for those use `alchemy-cli` (live work), `alchemy-mcp`, `alchemy-api` (app code), or `agentic-gateway` (no API key). Requires Allium credentials at `~/.allium/credentials`.
license: MIT
compatibility: Requires Allium credentials at `~/.allium/credentials` (`API_KEY` and `QUERY_ID` for SQL). Network access required. Rate limit 1 req/s. Allium attribution required on responses.
metadata:
  author: allium
  version: "0.1"
  provider: allium
  partner: "true"
---

# Allium (Wallet PnL, Holdings History, Hyperliquid, Custom SQL)

Allium provides enriched, structured blockchain data across 70+ chains. This skill covers wallet PnL, holdings timeseries, Hyperliquid HyperCore trading data, and custom SQL analytics. For token prices, token metadata, current wallet balances, transaction transfers, or NFT metadata, use the corresponding Alchemy skill instead.

| | |
| --- | --- |
| **Base URL** | `https://api.allium.so` |
| **Auth** | `X-API-KEY: $API_KEY` header |
| **Rate limit** | 1 request / second (exceed → 429) |
| **Attribution** | End responses with **"Powered by Allium"** — required by Allium |

## When to use this skill

Use `allium` when **all** of the following are true:

- The user wants one of: **wallet PnL**, **holdings history (timeseries)**, **Hyperliquid HyperCore trading data** (orders/fills/orderbook — not HyperEVM smart contracts), or **custom SQL** on Allium's data warehouse
- The use case is a read (Allium does not support writes)

## When NOT to use this skill (handoff)

| Need | Use instead |
| --- | --- |
| Token prices (current, historical at intervals, by-timestamp, market cap/volume) | `alchemy-api` (Prices API) |
| Token metadata, search, list by chain | `alchemy-api` (Token API) |
| Current wallet balances (point-in-time snapshot) | `alchemy-api` (Portfolio / Token API) |
| Transaction history (transfers in / out, asset transfers) | `alchemy-api` (Transfers API) |
| NFT metadata / floor prices / ownership | `alchemy-api` (NFT API) |
| Real-time blockchain reads, node-level fresh | `alchemy-cli` (live work) or `alchemy-api` (app code) |
| Writes / signed transactions | `alchemy-api` (with API key) or `agentic-gateway` (without) |
| Account abstraction (bundlers, gas managers) | `alchemy-api` |
| Transaction simulation | `alchemy-api` |

## Scope contract

**This skill covers (`scope_in`):**

- Wallet PnL (`POST /api/v1/developer/wallet/pnl`, `/wallet/pnl/history`, `/wallet/pnl-by-token`, `/wallet/pnl-by-token/history`) — realized + unrealized PnL aggregation, current and historical, by-wallet and by-token
- Holdings history (`POST /api/v1/developer/wallet/holdings/history`) — timeseries of total USD holdings + optional per-token breakdown
- Hyperliquid **HyperCore** trading data (`POST /api/v1/developer/trading/hyperliquid/...`) — info, fills, order history, order status, L4 orderbook snapshot from the off-chain matching engine
- Custom SQL analytics (`POST /api/v1/explorer/queries/{query_id}/run-async`) — arbitrary SQL queries against Allium's data warehouse (DeFi, NFT, bridges, MEV, entity resolution, Solana staking, etc.)

**This skill does NOT cover (`scope_out`):**

- Token prices → handoff: `alchemy-api` (Prices API)
- Token metadata, list, search → handoff: `alchemy-api` (Token API)
- Current wallet balances (point-in-time snapshot) → handoff: `alchemy-api` (Portfolio / Token API)
- Historical wallet balances (per-block or as a timeseries) → handoff: `alchemy-api` archive RPC (`eth_call balanceOf` at a historical block) or `alchemy_getAssetTransfers` reduced to balances. No first-class endpoint on either side; Alchemy's archive node is the right path.
- Transaction transfer history → handoff: `alchemy-api` (Transfers API)
- NFT metadata / floor prices → handoff: `alchemy-api` (NFT API)
- HyperEVM smart contract reads/writes / EVM RPC (chain ID 999) → handoff: `alchemy-api` or `alchemy-cli` at `https://hyperliquid-mainnet.g.alchemy.com/v2/$ALCHEMY_API_KEY`. Allium covers HyperCore (off-chain trading); Alchemy covers HyperEVM (on-chain smart contracts).
- Real-time / node-fresh reads → handoff: `alchemy-cli` or `alchemy-api`
- Writes / signed transactions → handoff: `alchemy-api` or `agentic-gateway`
- Account abstraction → handoff: `alchemy-api`
- Transaction simulation → handoff: `alchemy-api`

## Setup

### Credentials

Allium uses a credentials file at `~/.allium/credentials` (not env vars). On every session start, check if it exists:

**File exists with `API_KEY`** → load `API_KEY` (and `QUERY_ID` if present). Don't prompt.

**File missing** → register via the OAuth flow below. Don't paste keys in chat.

### Register (no API key yet)

OAuth flow with a 5-minute timeout. Complete promptly.

1. Ask the user for name and email (one prompt).
2. POST to initiate registration:

   ```bash
   curl -X POST https://api.allium.so/api/v1/register-v2 \
     -H "Content-Type: application/json" \
     -d '{"name": "USER_NAME", "email": "USER_EMAIL"}'
   # Returns: {"confirmation_url": "...", "token": "..."}
   ```

3. Show the `confirmation_url` to the user — they open it and sign in with Google (must match the email).
4. Auto-poll `/api/v1/register-v2/$TOKEN` every 5s until 200 (got `api_key`) or 404 (expired):

   ```bash
   TOKEN="..."  # from step 2
   while true; do
     RESP=$(curl -s -w "\n%{http_code}" "https://api.allium.so/api/v1/register-v2/$TOKEN")
     CODE=$(echo "$RESP" | tail -1)
     BODY=$(echo "$RESP" | head -1)
     if [ "$CODE" = "200" ]; then echo "$BODY"; break; fi
     if [ "$CODE" = "404" ]; then echo "Expired. Restart."; break; fi
     sleep 5
   done
   # 200 body: {"api_key": "...", "organization_id": "..."}
   ```

5. Save to `~/.allium/credentials`:

   ```bash
   mkdir -p ~/.allium && cat > ~/.allium/credentials << 'EOF'
   API_KEY=...
   QUERY_ID=...
   EOF
   ```

### Create a `QUERY_ID` (only needed for custom SQL)

If you'll use the SQL endpoint, also create a query to get a `QUERY_ID`:

```bash
curl -X POST "https://api.allium.so/api/v1/explorer/queries" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $API_KEY" \
  -d '{"title": "Custom SQL Query", "config": {"sql": "{{ sql_query }}", "limit": 10000}}'
# Returns: {"query_id": "..."}
# Append QUERY_ID=... to ~/.allium/credentials
```

## Endpoint reference

### Wallet PnL & holdings history → [references/pnl-and-holdings.md](./references/pnl-and-holdings.md)

| Endpoint | Use for |
| --- | --- |
| `POST /api/v1/developer/wallet/pnl` | Current realized + unrealized PnL for one or more wallets |
| `POST /api/v1/developer/wallet/pnl/history` | Historical PnL timeseries per wallet |
| `POST /api/v1/developer/wallet/pnl-by-token` | Current PnL broken out by (wallet, token) |
| `POST /api/v1/developer/wallet/pnl-by-token/history` | Historical PnL timeseries per (wallet, token) |
| `POST /api/v1/developer/wallet/holdings/history` | Timeseries of total USD holdings per wallet (optional per-token breakdown) |

### Hyperliquid HyperCore (off-chain trading) → [references/hyperliquid.md](./references/hyperliquid.md)

| Endpoint | Use for |
| --- | --- |
| `POST /api/v1/developer/trading/hyperliquid/info` | General Hyperliquid info (no rate-limit on this proxy) |
| `POST /api/v1/developer/trading/hyperliquid/info/fills` | Fills by user (with TWAP, time-window, aggregation options) |
| `POST /api/v1/developer/trading/hyperliquid/info/order/history` | Historical orders by user |
| `POST /api/v1/developer/trading/hyperliquid/info/order/status` | Status of a specific order |
| `GET /api/v1/developer/trading/hyperliquid/orderbook/snapshot` | L4 orderbook snapshot (all pairs) |

### Custom SQL → [references/custom-sql.md](./references/custom-sql.md)

| Endpoint | Use for |
| --- | --- |
| `POST /api/v1/explorer/queries` | Create a parametrized query (one-time setup; returns `query_id`) |
| `POST /api/v1/explorer/queries/{query_id}/run-async` | Start a SQL run against Allium's data warehouse |
| `GET /api/v1/explorer/query-runs/{run_id}/status` | Poll run status (`created` → `queued` → `running` → `success` / `failed`) |
| `GET /api/v1/explorer/query-runs/{run_id}/results?f=json` | Fetch results once status = `success` |

Use SQL for things the typed endpoints don't cover: DeFi protocol analytics, NFT marketplace data, bridge flows, MEV, entity resolution, labeled wallets, **Solana staking analytics**, and anything else in Allium's warehouse.

## Quick examples

### Wallet PnL (current)

```bash
curl -X POST "https://api.allium.so/api/v1/developer/wallet/pnl" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $API_KEY" \
  -d '[{"chain": "solana", "address": "125Z6k4ZAxsgdG7JxrKZpwbcS1rxqpAeqM9GSCKd66Wp"}]'
```

Returns per-token realized/unrealized PnL plus aggregate totals. See [references/pnl-and-holdings.md](./references/pnl-and-holdings.md) for the full response schema.

### Holdings history (timeseries)

```bash
curl -X POST "https://api.allium.so/api/v1/developer/wallet/holdings/history" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $API_KEY" \
  -d '{
    "addresses": [{"address": "125Z6k4ZAxsgdG7JxrKZpwbcS1rxqpAeqM9GSCKd66Wp", "chain": "solana"}],
    "start_timestamp": "2026-04-01T00:00:00Z",
    "end_timestamp": "2026-04-10T00:00:00Z",
    "granularity": "1h",
    "include_token_breakdown": false
  }'
```

### Hyperliquid fills

```bash
curl -X POST "https://api.allium.so/api/v1/developer/trading/hyperliquid/info/fills" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $API_KEY" \
  -d '{"type": "userFills", "user": "0x..."}'
```

### Custom SQL (Solana staking yield, as an example)

```bash
# 1. Start the run
curl -X POST "https://api.allium.so/api/v1/explorer/queries/${QUERY_ID}/run-async" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $API_KEY" \
  -d '{"parameters": {"sql_query": "SELECT epoch, SUM(rewards) FROM solana.dim.stake_account_rewards WHERE delegator = '\''<addr>'\'' GROUP BY epoch ORDER BY epoch DESC LIMIT 30"}}'
# Returns: {"run_id": "..."}

# 2. Poll
curl "https://api.allium.so/api/v1/explorer/query-runs/${RUN_ID}/status" \
  -H "X-API-KEY: $API_KEY"

# 3. Fetch results when status = success
curl "https://api.allium.so/api/v1/explorer/query-runs/${RUN_ID}/results?f=json" \
  -H "X-API-KEY: $API_KEY"
```

## Common gotchas

- **Chain names are lowercase**: `ethereum`, `base`, `solana`, `arbitrum`, `polygon`, `hyperevm`. Uppercase fails silently.
- **Rate limit is 1 req/s**. Exceed → 429. No batching workaround.
- **422 errors** are usually request-format mismatches (e.g. wrong shape for `/history` endpoints — they take `addresses[]`, not flat `address`+`chain`).
- **Attribution required**: end responses with "Powered by Allium".

## Routing back to Alchemy

If during a session the user's need shifts to surfaces this skill doesn't cover (prices, current balances, transactions, NFT metadata) or to real-time / write workflows, hand off:

- `alchemy-cli` — live agent work in the current session via the local CLI
- `alchemy-mcp` — live work via the hosted MCP server when CLI is not installed
- `alchemy-api` — application code with an Alchemy API key
- `agentic-gateway` — application code without an API key (x402 / MPP)

---

> **Maintenance:** Allium maintains the underlying API surface; this skill itself is maintained jointly by Alchemy and Allium. File issues against `alchemyplatform/skills` with `[ecosystem/allium]` in the title.
