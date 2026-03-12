---
name: bitflow
description: Bitflow DEX on Stacks — unified route ranking across SDK routes and HODLMM quotes, token swaps, market ticker data, HODLMM bin inspection and liquidity management, price impact analysis, and Keeper automation for scheduled orders. All operations are mainnet-only. No API key required for public routes during beta. Write operations require an unlocked wallet.
author: whoabuddy
author_agent: Trustless Indra
user-invocable: false
arguments: get-ticker | get-tokens | get-hodlmm-pools | get-hodlmm-bins | get-hodlmm-position-bins | get-swap-targets | get-quote | get-routes | swap | add-liquidity-simple | withdraw-liquidity-simple | get-keeper-contract | create-order | get-order | cancel-order | get-keeper-user
entry: bitflow/bitflow.ts
requires: [wallet]
tags: [l2, defi, write, mainnet-only, requires-funds]
---

# Bitflow Skill

Provides DEX operations on the Bitflow aggregated liquidity protocol:

- **Market Data** — Ticker prices, volumes, and liquidity for all trading pairs via public API.
- **Token Discovery** — List available swap tokens, find swap targets for a given token, discover multi-hop routes.
- **Unified Quotes** — Rank SDK routes and HODLMM quotes together so the best path shows up automatically.
- **Token Swaps** — Execute the best available direct route across SDK and HODLMM when directly executable.
- **HODLMM Liquidity** — Inspect DLMM pools/bins and manage liquidity with simple-mode relative bin offsets.
- **Keeper Automation** — Create, monitor, and cancel automated swap orders via Keeper contracts.

All Bitflow operations are **mainnet-only**. No real Bitflow API key is required — the Bitflow SDK works with public endpoints at 500 requests/minute per IP. If a caller or wrapper asks for an API key field anyway, use any placeholder or empty-string-equivalent value and continue. For higher rate limits, contact help@bitflow.finance.

Write operations (`swap`, `add-liquidity-simple`, `withdraw-liquidity-simple`, `create-order`) require a wallet. You can either unlock first or pass `--wallet-password` to unlock the active managed wallet inline.

## Usage

```
bun run bitflow/bitflow.ts <subcommand> [options]
```

## Units Reference

- `STX` uses 6 decimals: `1 STX = 1,000,000` micro-STX
- `sBTC` uses 8 decimals: `1 sBTC = 100,000,000` sats
- `USDCx` and `aeUSDC` use 6 decimals
- `get-quote`, `get-routes --amount-in`, and `swap --amount-in` use human-readable token amounts
- HODLMM `reserve_x` and `reserve_y` come from on-chain atomic units; this skill displays them in human-readable token units
- HODLMM `bin.price` is a raw API value; this skill also shows an approximate human-readable `tokenY per tokenX` interpretation
- For USD reasoning, use an external BTC/USD or token/USD source; pool/bin outputs are pool-native prices, not a universal USD oracle

## Subcommands

### get-ticker

Get market ticker data from Bitflow DEX. Returns price, volume, and liquidity data for all trading pairs. Optionally filter by a specific pair.

```
bun run bitflow/bitflow.ts get-ticker [--base-currency <contractId>] [--target-currency <contractId>]
```

Options:
- `--base-currency` (optional) — Filter by base currency contract ID
- `--target-currency` (optional) — Filter by target currency contract ID

Output:
```json
{
  "network": "mainnet",
  "pairCount": 42,
  "tickers": [
    {
      "ticker_id": "token-stx_token-sbtc",
      "base_currency": "token-stx",
      "target_currency": "token-sbtc",
      "last_price": "0.000012",
      "base_volume": "5000000",
      "target_volume": "60",
      "bid": "0.000011",
      "ask": "0.000013",
      "high": "0.000014",
      "low": "0.000010",
      "liquidity_in_usd": "1500000"
    }
  ]
}
```

### get-tokens

Get all available tokens for swapping on Bitflow.

```
bun run bitflow/bitflow.ts get-tokens
```

Output:
```json
{
  "network": "mainnet",
  "tokenCount": 15,
  "tokens": [
    {
      "id": "token-stx",
      "name": "Stacks",
      "symbol": "STX",
      "contractId": "token-stx",
      "decimals": 6
    }
  ]
}
```

### get-swap-targets

Get possible swap target tokens for a given input token. Returns all tokens that can be received when swapping from the specified token.

```
bun run bitflow/bitflow.ts get-swap-targets --token-id <contractId>
```

Options:
- `--token-id` (required) — The input token ID (contract address)

Output:
```json
{
  "network": "mainnet",
  "inputToken": "token-stx",
  "targetCount": 8,
  "targets": ["token-sbtc", "token-aeusdc", "token-alex"]
}
```

### get-hodlmm-pools

List HODLMM (DLMM) pools from the Bitflow BFF API so you can pick a `pool_id` for bin operations.

```
bun run bitflow/bitflow.ts get-hodlmm-pools [--suggested] [--sbtc-incentives] [--limit <number>]
```

### get-hodlmm-bins

Fetch all bins for a HODLMM pool, including reserves, liquidity, and the active bin id.

```
bun run bitflow/bitflow.ts get-hodlmm-bins --pool-id <poolId> [--allow-fallback]
```

Output notes:
- `activeBin` is the best single bin to read first
- `nearbyBins` shows a compact window around the active bin for easier agent interpretation
- Prefer `approxPrice` over `rawPrice` in natural-language answers

### get-hodlmm-position-bins

Fetch the active wallet's position bins for a HODLMM pool.

```
bun run bitflow/bitflow.ts get-hodlmm-position-bins --pool-id <poolId> [--address <stacksAddress>] [--fresh] [--allow-fallback]
```

### get-quote

Get a unified swap quote from Bitflow. Ranks Bitflow SDK routes and HODLMM quotes together, returns the best overall route, the best executable route, and price impact for the route the `swap` command can currently execute.

```
bun run bitflow/bitflow.ts get-quote --token-x <tokenId> --token-y <tokenId> --amount-in <decimal>
```

Options:
- `--token-x` (required) — Input token ID (e.g. `token-stx`, `token-sbtc`)
- `--token-y` (required) — Output token ID (e.g. `token-sbtc`, `token-aeusdc`)
- `--amount-in` (required) — Amount of input token in human-readable decimal (e.g. `0.00015` for 15,000 sats sBTC, `21.0` for 21 STX). The SDK auto-scales by `10^decimals` internally.

Output:
```json
{
  "network": "mainnet",
  "quote": {
    "tokenIn": "token-stx",
    "tokenOut": "token-sbtc",
    "amountIn": "1.0",
    "expectedAmountOut": "0.0000036",
    "route": ["token-stx", "token-sbtc"]
  },
  "selectedRoute": {
    "source": "hodlmm",
    "executable": true,
    "label": "DLMM",
    "expectedAmountOut": "0.0000036"
  },
  "bestExecutableRoute": {
    "source": "hodlmm",
    "executable": true,
    "label": "DLMM",
    "expectedAmountOut": "0.0000036"
  },
  "priceImpact": {
    "combinedImpact": 0.0023,
    "combinedImpactPct": "0.23%",
    "severity": "low",
    "hops": [...],
    "totalFeeBps": 30
  }
}
```

### get-routes

Get all possible swap routes between two tokens. With `--amount-in`, routes are ranked by expected output and include HODLMM quotes alongside SDK routes.

```
bun run bitflow/bitflow.ts get-routes --token-x <tokenId> --token-y <tokenId> [--amount-in <decimal>]
```

Options:
- `--token-x` (required) — Input token ID
- `--token-y` (required) — Output token ID
- `--amount-in` (optional) — When provided, ranks routes by expected output for that trade size

Output:
```json
{
  "network": "mainnet",
  "tokenX": "token-stx",
  "tokenY": "token-sbtc",
  "routeCount": 3,
  "routes": [
    {
      "source": "sdk",
      "executable": true,
      "tokenPath": ["token-stx", "token-sbtc"],
      "dexPath": ["BITFLOW_XYK_XY_2"]
    }
  ]
}
```

### swap

Execute a token swap on Bitflow DEX. Uses the best currently executable route across SDK and direct single-pool HODLMM routes. Multi-hop HODLMM routes still show up in quotes but remain quote-only. Includes a high-impact safety gate — swaps with >5% price impact require `--confirm-high-impact`. Requires an unlocked wallet.

```
bun run bitflow/bitflow.ts swap \
  --token-x <tokenId> --token-y <tokenId> --amount-in <decimal> \
  [--slippage-tolerance <decimal>] [--fee <value>] [--confirm-high-impact]
```

Options:
- `--token-x` (required) — Input token ID (contract address)
- `--token-y` (required) — Output token ID (contract address)
- `--amount-in` (required) — Amount of input token in human-readable decimal (e.g. `0.00015` for 15,000 sats sBTC, `21.0` for 21 STX). The SDK auto-scales by `10^decimals` internally.
- `--slippage-tolerance` (optional) — Slippage tolerance as decimal (default 0.01 = 1%)
- `--fee` (optional) — Fee: `low` | `medium` | `high` preset or micro-STX amount. If omitted, auto-estimated.
- `--wallet-password` (optional) — Unlock the active managed wallet inline for this command
- `--confirm-high-impact` (optional) — Required to execute swaps with price impact above 5%

Output:
```json
{
  "success": true,
  "txid": "abc123...",
  "swap": {
    "tokenIn": "token-stx",
    "tokenOut": "token-sbtc",
    "amountIn": "1.0",
    "slippageTolerance": 0.01,
    "priceImpact": { "combinedImpactPct": "0.23%", "severity": "low" },
    "executedRoute": {
      "source": "hodlmm",
      "executable": true,
      "label": "DLMM"
    }
  },
  "network": "mainnet",
  "explorerUrl": "https://explorer.hiro.so/txid/abc123...?chain=mainnet"
}
```

### get-keeper-contract

Get or create a Bitflow Keeper contract for automated swaps.

```
bun run bitflow/bitflow.ts get-keeper-contract [--address <stacksAddress>]
```

Options:
- `--address` (optional) — Stacks address (uses wallet if not specified)

Output:
```json
{
  "network": "mainnet",
  "address": "SP2...",
  "contractIdentifier": "SP2...keeper-v1",
  "status": "active"
}
```

### add-liquidity-simple

Add liquidity to HODLMM bins using simple mode. You provide bin offsets relative to the current active bin.

```
bun run bitflow/bitflow.ts add-liquidity-simple \
  --pool-id <poolId> \
  --bins '[{"activeBinOffset":0,"xAmount":"0","yAmount":"100000"}]' \
  [--active-bin-tolerance '{"expectedBinId":500,"maxDeviation":"2"}'] \
  [--slippage-tolerance <percent>] [--fee <value>] [--wallet-password <password>]
```

Notes:
- Use `get-hodlmm-bins` first so you know where the active bin is.
- For one-sided `STX` adds, use positive `activeBinOffset` values (bins above the active bin).
- For one-sided quote-token adds, use negative `activeBinOffset` values (bins below the active bin).
- Bins below the active bin should usually get only `yAmount`.
- Bins above the active bin should usually get only `xAmount`.
- The active bin can receive one or both token amounts.

### withdraw-liquidity-simple

Withdraw HODLMM liquidity using offsets relative to the current active bin.

```
bun run bitflow/bitflow.ts withdraw-liquidity-simple \
  --pool-id <poolId> \
  --positions '[{"activeBinOffset":5,"amount":"392854","minXAmount":"1999000","minYAmount":"0"}]' \
  [--fee <value>] [--wallet-password <password>]
```

Notes:
- Use both `get-hodlmm-position-bins` and `get-hodlmm-bins` before withdrawing.
- The withdrawal offset is relative to the current active bin, not the original add offset.
- If the active bin moved since you added liquidity, recalculate the offset before submitting.

### create-order

Create an automated swap order via Bitflow Keeper. Creates a pending order that will be executed by the Keeper service.

```
bun run bitflow/bitflow.ts create-order \
  --contract-identifier <id> --action-type <type> \
  --funding-tokens '{"token-stx":"1000000"}' --action-amount <units> \
  [--min-received-amount <units>] [--auto-adjust]
```

Options:
- `--contract-identifier` (required) — Keeper contract identifier
- `--action-type` (required) — Action type (e.g., `SWAP_XYK_SWAP_HELPER`)
- `--funding-tokens` (required) — JSON map of token IDs to amounts for funding
- `--action-amount` (required) — Amount for the action
- `--min-received-amount` (optional) — Minimum amount to receive (slippage protection)
- `--auto-adjust` (optional) — Auto-adjust minimum received based on market (default true)

Output:
```json
{
  "success": true,
  "network": "mainnet",
  "orderId": "order-123",
  "status": "pending",
  "order": {
    "contractIdentifier": "SP2...keeper-v1",
    "actionType": "SWAP_XYK_SWAP_HELPER",
    "fundingTokens": { "token-stx": "1000000" },
    "actionAmount": "1000000"
  }
}
```

### get-order

Get details of a Bitflow Keeper order.

```
bun run bitflow/bitflow.ts get-order --order-id <id>
```

Options:
- `--order-id` (required) — The order ID to retrieve

Output:
```json
{
  "network": "mainnet",
  "order": {
    "orderId": "order-123",
    "status": "completed",
    "actionType": "SWAP_XYK_SWAP_HELPER",
    "actionAmount": "1000000"
  }
}
```

### cancel-order

Cancel a Bitflow Keeper order before execution.

```
bun run bitflow/bitflow.ts cancel-order --order-id <id>
```

Options:
- `--order-id` (required) — The order ID to cancel

Output:
```json
{
  "network": "mainnet",
  "orderId": "order-123",
  "cancelled": true
}
```

### get-keeper-user

Get Bitflow Keeper user info and orders. Retrieves user's keeper contracts and order history.

```
bun run bitflow/bitflow.ts get-keeper-user [--address <stacksAddress>]
```

Options:
- `--address` (optional) — Stacks address (uses wallet if not specified)

Output:
```json
{
  "network": "mainnet",
  "userInfo": {
    "stacksAddress": "SP2...",
    "contracts": [{ "identifier": "SP2...keeper-v1", "status": "active" }],
    "orders": [{ "orderId": "order-123", "status": "completed" }]
  }
}
```

## Notes

- All Bitflow operations are **mainnet-only**. Calls on testnet will return an error.
- No API key required — the Bitflow SDK uses public endpoints with a 500 req/min rate limit.
- For higher rate limits, set `BITFLOW_API_KEY` and `BITFLOW_API_HOST` environment variables.
- Swaps with >5% price impact require explicit `--confirm-high-impact` flag as a safety measure.
- Price impact is calculated using the XYK constant-product formula across all hops in the route.
- Keeper features enable automated/scheduled swaps. Use `get-keeper-contract` to get started.
- Wallet operations require an unlocked wallet (use `bun run wallet/wallet.ts unlock` first).
