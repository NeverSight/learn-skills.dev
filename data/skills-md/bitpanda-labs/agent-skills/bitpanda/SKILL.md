---
name: bitpanda
description: >
  Query a Bitpanda account via the Bitpanda API using a bundled bash CLI.
  Covers all read-only endpoints: balances, trades, transactions, asset info, and live prices.
  Use when the user wants to check their Bitpanda portfolio, balances, trade history,
  deposits, withdrawals, asset prices, or any account information from Bitpanda.
  Usable for mentions of Bitpanda, crypto portfolio on Bitpanda, price checks, or requests
  involving Bitpanda wallet/trade data.
  This skill is READ-ONLY — it does NOT support trading, placing orders, deposits,
  withdrawals, or any write operations.
compatibility: Requires curl, jq, and BITPANDA_API_KEY environment variable
metadata:
  homepage: https://github.com/bitpanda-labs/agent-skills
  requires-bins: curl jq
  requires-env: BITPANDA_API_KEY
---

# Bitpanda

Query a Bitpanda account through the API using the bundled `scripts/bitpanda.sh` CLI.

## Prerequisites

Set `BITPANDA_API_KEY` environment variable with a key from https://web.bitpanda.com/my-account/apikey

Verify access works:
```bash
bash <skill-path>/scripts/bitpanda.sh balances --page-size 5
```

## CLI Usage

All commands are invoked as `bash <skill-path>/scripts/bitpanda.sh <command> [options]`. Output is JSON.

### Start here: `portfolio`

For any request about the user's holdings, balances, or portfolio, **always use `portfolio` first**:
```bash
bash <skill-path>/scripts/bitpanda.sh portfolio
```
It handles pagination, zero-balance filtering, asset name resolution, EUR price enrichment, and **aggregation by asset** (combining regular, staking, and index wallets) automatically. Use `--sort value` to sort by EUR value descending (default: alphabetical by name). Returns:
```json
{
  "wallets": [
    {"asset_name": "Bitcoin", "asset_symbol": "BTC", "balance": "0.123", "eur_price": "95000", "eur_value": 11685.0, "asset_id": "...", "wallets": [{"wallet_id": "...", "wallet_type": null, "balance": "0.123"}]}
  ],
  "count": 25,
  "total_eur": 50000.0
}
```

Do NOT manually paginate `balances` + call `asset` per ID — `portfolio` does this for you.

#### Handling null prices

When `portfolio` returns wallets with `eur_price: null`, the exact symbol didn't match the ticker. Report these assets to the user.

### Price commands

| Command | Description |
|---|---|
| `price <SYMBOL>` | Get price, currency, and daily change for a single asset. |
| `prices` | List prices for held assets. |
| `prices --all` | List all available ticker prices. |

### Trades: `trades`

For any request about **buy/sell history**, recent purchases, or trade activity, **always use `trades` first** — NOT `all-transactions`:
```bash
bash <skill-path>/scripts/bitpanda.sh trades [options]
```
It auto-paginates transactions, filters for buys/sells, resolves asset names, and enriches with asset type and price. Returns:
```json
[
  {"date": "2025-12-22T16:20:48Z", "operation": "buy", "asset_name": "Bitcoin", "asset_symbol": "BTC", "asset_type": "cryptocoin", "amount": "0.5", "current_eur_price": "95000", "trade_id": "...", "asset_id": "..."}
]
```

Options:
- `--operation buy|sell` — filter by trade direction (default: both)
- `--asset-type <type>` — filter by asset type: `cryptocoin`, `metal`, `stock`, `commodity`, `etf`, etc.
- `--limit <n>` — number of trades to return (default 5)
- `--from <datetime>` / `--to <datetime>` — date range filter

Examples:
```bash
# Last 3 purchases
bash <skill-path>/scripts/bitpanda.sh trades --operation buy --limit 3

# Last 3 crypto purchases
bash <skill-path>/scripts/bitpanda.sh trades --operation buy --asset-type cryptocoin --limit 3

# All trades in January 2026
bash <skill-path>/scripts/bitpanda.sh trades --from 2026-01-01T00:00:00Z --to 2026-02-01T00:00:00Z --limit 20
```

Do NOT manually paginate `all-transactions` + resolve asset names — `trades` does this for you.

### Other commands

| Command | Description |
|---|---|
| `balances` | Raw wallet list (use `--non-zero` to filter zeros). Only use when you need pagination control or filtering by asset_id. |
| `all-transactions` | Raw transaction list across all asset types. Only use when you need full transaction details, non-trade operations (rewards, deposits, etc.), or direct cursor control. |
| `asset <asset_id>` | Get single asset info. Response: `{"data": {"id": "...", "name": "Bitcoin", "symbol": "BTC"}}` |

### Pagination

`balances` and `all-transactions` use cursor pagination:
- `--before <cursor>` / `--after <cursor>` / `--page-size <n>` (1-100, default 25)

### Filtering

```bash
# Balances: filter by asset
bash <skill-path>/scripts/bitpanda.sh balances --asset-id <uuid>

# Transactions: filter by direction and wallet
bash <skill-path>/scripts/bitpanda.sh all-transactions --flow incoming --wallet-id <uuid>

# Transactions: filter by asset
bash <skill-path>/scripts/bitpanda.sh all-transactions --asset-id <uuid>

# Transactions: filter by date range
bash <skill-path>/scripts/bitpanda.sh all-transactions --from 2024-01-01T00:00:00Z --to 2024-02-01T00:00:00Z
```

## Common Tasks

**Last purchases**:
```bash
bash <skill-path>/scripts/bitpanda.sh trades --operation buy --limit 3
```

**Recent trades**:
```bash
bash <skill-path>/scripts/bitpanda.sh trades --limit 10
```

**List recent transactions (all types including rewards, dividends)**:
```bash
bash <skill-path>/scripts/bitpanda.sh all-transactions --page-size 10
```

**Check current BTC price**:
```bash
bash <skill-path>/scripts/bitpanda.sh price BTC
```

## Transaction fields

- `operation_type`: The category of operation (e.g. `buy`, `sell`, `deposit`, `withdrawal`, `transfer`, `staking`).
- `flow`: `incoming` (credit) or `outgoing` (debit).
- `compensates`: Links to a reversed/corrected transaction ID (null for normal transactions).
- `trade_id`: Present when the transaction resulted from a trade; null for deposits/withdrawals/staking.

## API Reference

For full endpoint details, parameters, and response schemas, read [references/api_reference.md](references/api_reference.md).
