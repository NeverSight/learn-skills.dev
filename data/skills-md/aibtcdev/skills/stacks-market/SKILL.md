---
name: stacks-market
description: "Prediction market trading on stacksmarket.app — discover markets, quote LMSR prices, buy/sell YES/NO shares, and redeem winnings. Uses the market-factory-v18-bias contract on Stacks mainnet. Write operations require an unlocked wallet with STX."
metadata:
  author: "whoabuddy"
  author-agent: "Trustless Indra"
  user-invocable: "false"
  arguments: "list-markets | search-markets | get-market | quote-buy | quote-sell | buy-yes | buy-no | sell-yes | sell-no | redeem | get-position"
  entry: "stacks-market/stacks-market.ts"
  requires: "wallet"
  tags: "l2, defi, write, mainnet-only, requires-funds"
---

# Stacks Market Skill

Trade prediction markets on [stacksmarket.app](https://www.stacksmarket.app) via the on-chain contract `SP3N5CN0PE7YRRP29X7K9XG22BT861BRS5BN8HFFA.market-factory-v18-bias`.

- **Market Discovery** — List and search prediction markets via REST API with filters for status, category, and featured flag.
- **Price Quoting** — Get real-time LMSR prices for YES/NO shares via on-chain read-only calls before committing funds.
- **Trading** — Buy YES or NO shares with slippage protection (`buy-yes-auto`, `buy-no-auto`). Sell with minimum proceeds guard (`sell-yes-auto`, `sell-no-auto`).
- **Redemption** — Redeem winning shares after market resolution (1 share = 1 STX for winners).
- **Position Tracking** — Check your YES and NO share balances in any market.

All operations are **mainnet-only**. Write operations (buy-yes, buy-no, sell-yes, sell-no, redeem) require an unlocked wallet (use `bun run wallet/wallet.ts unlock` first).

## Usage

```
bun run stacks-market/stacks-market.ts <subcommand> [options]
```

## Subcommands

### list-markets

List prediction markets from stacksmarket.app. Returns markets sorted by most recent activity.

```
bun run stacks-market/stacks-market.ts list-markets [--limit <n>] [--status <status>] [--category <cat>] [--featured]
```

Options:
- `--limit` (optional) — Number of markets to return (default: 20)
- `--status` (optional) — Filter by status: `active` | `ended` | `resolved`
- `--category` (optional) — Filter by category (e.g., `Crypto`, `Politics`)
- `--featured` (optional) — Show only featured markets

Output:
```json
{
  "network": "mainnet",
  "marketCount": 5,
  "markets": [
    {
      "_id": "699c573ea7bb5ad25fee68a0",
      "marketId": "1771853629839",
      "title": "Will BTC close above $100k by end of Q1?",
      "category": "Crypto",
      "isActive": true,
      "isResolved": false,
      "endDate": "2026-03-31T23:59:00.000Z",
      "totalVolume": 5000000000,
      "totalTrades": 42
    }
  ]
}
```

### search-markets

Search prediction markets by keyword. Searches titles and descriptions.

```
bun run stacks-market/stacks-market.ts search-markets --query <keyword> [--limit <n>]
```

Options:
- `--query` (required) — Search keyword
- `--limit` (optional) — Maximum results (default: 10)

Output:
```json
{
  "network": "mainnet",
  "query": "bitcoin",
  "resultCount": 3,
  "markets": [
    {
      "_id": "699c573ea7bb5ad25fee68a0",
      "marketId": "1771853629839",
      "title": "Will BTC close above $100k by end of Q1?",
      "isActive": true,
      "isResolved": false
    }
  ]
}
```

### get-market

Get full details for a single prediction market including trade history and order book.

```
bun run stacks-market/stacks-market.ts get-market --market-id <mongoId>
```

Options:
- `--market-id` (required) — MongoDB `_id` of the market (e.g., `699c573ea7bb5ad25fee68a0`)

Output:
```json
{
  "network": "mainnet",
  "market": {
    "_id": "699c573ea7bb5ad25fee68a0",
    "marketId": "1771853629839",
    "title": "Will BTC close above $100k by end of Q1?",
    "description": "Resolution source: CoinGecko closing price...",
    "category": "Crypto",
    "options": [
      { "text": "Yes", "impliedProbability": 52, "totalVolume": 3000000000 },
      { "text": "No", "impliedProbability": 48, "totalVolume": 2000000000 }
    ],
    "isActive": true,
    "isResolved": false,
    "winningOption": null,
    "endDate": "2026-03-31T23:59:00.000Z",
    "totalVolume": 5000000000,
    "totalTrades": 42,
    "tradeHistory": []
  }
}
```

### quote-buy

Get a price quote for buying YES or NO shares. Always quote before buying to verify cost and slippage.

```
bun run stacks-market/stacks-market.ts quote-buy --market-id <id> --side <yes|no> --amount <shares>
```

Options:
- `--market-id` (required) — Market ID (epoch millisecond timestamp, e.g., `1771853629839`)
- `--side` (required) — `yes` or `no`
- `--amount` (required) — Number of shares to buy (integer, e.g., `5` for 5 shares)

Output:
```json
{
  "network": "mainnet",
  "quote": {
    "marketId": "1771853629839",
    "side": "yes",
    "shares": 5,
    "totalCostUstx": 5250000,
    "totalCostStx": "5.25",
    "fees": {
      "protocolUstx": 125000,
      "lpUstx": 75000
    }
  }
}
```

### quote-sell

Get a price quote for selling YES or NO shares. Always quote before selling to verify proceeds.

```
bun run stacks-market/stacks-market.ts quote-sell --market-id <id> --side <yes|no> --amount <shares>
```

Options:
- `--market-id` (required) — Market ID (epoch millisecond timestamp)
- `--side` (required) — `yes` or `no`
- `--amount` (required) — Number of shares to sell (integer)

Output:
```json
{
  "network": "mainnet",
  "quote": {
    "marketId": "1771853629839",
    "side": "yes",
    "shares": 5,
    "totalProceedsUstx": 4750000,
    "totalProceedsStx": "4.75",
    "fees": {
      "protocolUstx": 125000,
      "lpUstx": 75000
    }
  }
}
```

### buy-yes

Buy YES shares in a prediction market. Uses `buy-yes-auto` for slippage protection. Requires an unlocked wallet.

```
bun run stacks-market/stacks-market.ts buy-yes --market-id <id> --amount <shares> --max-cost <ustx>
```

Options:
- `--market-id` (required) — Market ID (epoch millisecond timestamp)
- `--amount` (required) — Number of YES shares to buy
- `--max-cost` (required) — Maximum total cost in uSTX (slippage protection). Get from `quote-buy` first.

Output:
```json
{
  "success": true,
  "txid": "abc123...",
  "network": "mainnet",
  "explorerUrl": "https://explorer.hiro.so/txid/abc123...?chain=mainnet",
  "trade": {
    "marketId": "1771853629839",
    "side": "yes",
    "shares": 5,
    "maxCostUstx": 5500000
  }
}
```

### buy-no

Buy NO shares in a prediction market. Uses `buy-no-auto` for slippage protection. Requires an unlocked wallet.

```
bun run stacks-market/stacks-market.ts buy-no --market-id <id> --amount <shares> --max-cost <ustx>
```

Options:
- `--market-id` (required) — Market ID (epoch millisecond timestamp)
- `--amount` (required) — Number of NO shares to buy
- `--max-cost` (required) — Maximum total cost in uSTX (slippage protection)

Output:
```json
{
  "success": true,
  "txid": "abc123...",
  "network": "mainnet",
  "explorerUrl": "https://explorer.hiro.so/txid/abc123...?chain=mainnet",
  "trade": {
    "marketId": "1771853629839",
    "side": "no",
    "shares": 5,
    "maxCostUstx": 5500000
  }
}
```

### sell-yes

Sell YES shares before market resolution. Uses `sell-yes-auto` with minimum proceeds guard. Requires an unlocked wallet.

```
bun run stacks-market/stacks-market.ts sell-yes --market-id <id> --amount <shares> --min-proceeds <ustx>
```

Options:
- `--market-id` (required) — Market ID (epoch millisecond timestamp)
- `--amount` (required) — Number of YES shares to sell
- `--min-proceeds` (required) — Minimum acceptable proceeds in uSTX (slippage protection). Get from `quote-sell` first.

Output:
```json
{
  "success": true,
  "txid": "abc123...",
  "network": "mainnet",
  "explorerUrl": "https://explorer.hiro.so/txid/abc123...?chain=mainnet",
  "trade": {
    "marketId": "1771853629839",
    "side": "yes",
    "shares": 5,
    "minProceedsUstx": 4500000
  }
}
```

### sell-no

Sell NO shares before market resolution. Uses `sell-no-auto` with minimum proceeds guard. Requires an unlocked wallet.

```
bun run stacks-market/stacks-market.ts sell-no --market-id <id> --amount <shares> --min-proceeds <ustx>
```

Options:
- `--market-id` (required) — Market ID (epoch millisecond timestamp)
- `--amount` (required) — Number of NO shares to sell
- `--min-proceeds` (required) — Minimum acceptable proceeds in uSTX

Output:
```json
{
  "success": true,
  "txid": "abc123...",
  "network": "mainnet",
  "explorerUrl": "https://explorer.hiro.so/txid/abc123...?chain=mainnet",
  "trade": {
    "marketId": "1771853629839",
    "side": "no",
    "shares": 5,
    "minProceedsUstx": 4500000
  }
}
```

### redeem

Redeem winning shares after market resolution. Winning shares pay 1 STX (1,000,000 uSTX) each. Requires an unlocked wallet.

```
bun run stacks-market/stacks-market.ts redeem --market-id <id>
```

Options:
- `--market-id` (required) — Market ID (epoch millisecond timestamp)

Output:
```json
{
  "success": true,
  "txid": "abc123...",
  "network": "mainnet",
  "explorerUrl": "https://explorer.hiro.so/txid/abc123...?chain=mainnet",
  "marketId": "1771853629839"
}
```

### get-position

Get your YES and NO share balances in a market. Optionally check any address.

```
bun run stacks-market/stacks-market.ts get-position --market-id <id> [--address <stacksAddress>]
```

Options:
- `--market-id` (required) — Market ID (epoch millisecond timestamp)
- `--address` (optional) — Stacks address to check (uses active wallet if omitted)

Output:
```json
{
  "network": "mainnet",
  "address": "SP2...",
  "marketId": "1771853629839",
  "position": {
    "yesShares": 5,
    "noShares": 0
  }
}
```

## Notes

- All operations are **mainnet-only**. Calls on testnet will return an error.
- Write operations require an unlocked wallet (use `bun run wallet/wallet.ts unlock` first).
- Always run `quote-buy` or `quote-sell` before trading to verify costs and set slippage bounds.
- Market IDs are epoch millisecond timestamps (e.g., `1771853629839`), not MongoDB `_id`.
- The `get-market` subcommand takes MongoDB `_id` (e.g., `699c573ea7bb5ad25fee68a0`), not `marketId`.
- Write operations MUST use `PostConditionMode.Allow` — the contract moves STX internally (sender → pool → fee wallets) and default post-conditions block this.
- `isActive` can be `true` even after `endDate` passes — the contract owner must manually resolve. Always check `isResolved` and compare time.
- Winning shares pay 1 STX each on redemption; losing shares pay nothing. Burns all shares.
- Gas fees are approximately 0.05–0.1 STX per transaction, in addition to the share cost.
- LMSR pricing: cost of shares follows a logarithmic curve — buying more shares in one direction increases price. Get a fresh quote immediately before submitting a buy.
