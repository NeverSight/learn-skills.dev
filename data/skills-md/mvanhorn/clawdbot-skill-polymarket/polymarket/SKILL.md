---
name: polymarket
version: "1.1.0"
description: Query and trade on Polymarket prediction markets — check odds, trending markets, search events, view order books, place trades, and manage positions. Now available to US developers.
author: mvanhorn
license: MIT
repository: https://github.com/mvanhorn/clawdbot-skill-polymarket
homepage: https://polymarket.com
metadata:
  openclaw:
    emoji: "📊"
    tags:
      - prediction-markets
      - polymarket
      - trading
      - odds
      - betting
---

# Polymarket

Query [Polymarket](https://polymarket.com) prediction markets and trade from the terminal.

## Setup

**Read-only commands work immediately** (no install needed).

For trading, order books, and price history, install the [Polymarket CLI](https://github.com/Polymarket/polymarket-cli):

```bash
curl -sSL https://raw.githubusercontent.com/Polymarket/polymarket-cli/main/install.sh | sh
```

For trading, set up a wallet:

```bash
python3 {baseDir}/scripts/polymarket.py wallet-setup
```

Or manually configure `~/.config/polymarket/config.json` with your private key. See the [CLI docs](https://github.com/Polymarket/polymarket-cli) for details.

## Commands

### Browse Markets (no CLI needed)

```bash
# Trending/active markets
python3 {baseDir}/scripts/polymarket.py trending

# Search markets
python3 {baseDir}/scripts/polymarket.py search "trump"

# Get specific event by slug
python3 {baseDir}/scripts/polymarket.py event "fed-decision-in-october"

# Get markets by category
python3 {baseDir}/scripts/polymarket.py category politics
python3 {baseDir}/scripts/polymarket.py category crypto
```

### Order Book & Prices (CLI required, no wallet)

```bash
# Order book for a token
python3 {baseDir}/scripts/polymarket.py book TOKEN_ID

# Price history
python3 {baseDir}/scripts/polymarket.py price-history TOKEN_ID --interval 1d
```

### Wallet (CLI required)

```bash
python3 {baseDir}/scripts/polymarket.py wallet-setup
python3 {baseDir}/scripts/polymarket.py wallet-show
python3 {baseDir}/scripts/polymarket.py wallet-balance
python3 {baseDir}/scripts/polymarket.py wallet-balance --token TOKEN_ID
```

### Trading (CLI + wallet required)

All trades require `--confirm` to execute. Without it, the order is previewed only.

```bash
# Buy limit order: 10 shares at $0.50
python3 {baseDir}/scripts/polymarket.py --confirm trade buy --token TOKEN_ID --price 0.50 --size 10

# Sell limit order
python3 {baseDir}/scripts/polymarket.py --confirm trade sell --token TOKEN_ID --price 0.70 --size 10

# Market order: buy $5 worth
python3 {baseDir}/scripts/polymarket.py --confirm trade buy --token TOKEN_ID --market-order --amount 5
```

### Orders & Positions (CLI + wallet required)

```bash
# List open orders
python3 {baseDir}/scripts/polymarket.py orders

# Cancel a specific order
python3 {baseDir}/scripts/polymarket.py --confirm orders --cancel ORDER_ID

# Cancel all orders
python3 {baseDir}/scripts/polymarket.py --confirm orders --cancel all

# View positions
python3 {baseDir}/scripts/polymarket.py positions
python3 {baseDir}/scripts/polymarket.py positions --address 0xYOUR_WALLET
```

## Example Chat Usage

- "What are the odds Trump wins 2028?"
- "Trending on Polymarket?"
- "Search Polymarket for Bitcoin"
- "Show me the order book for [token]"
- "Buy 10 shares of YES on [market] at $0.45"
- "What are my open positions?"
- "Cancel all my orders"

## ⚠️ Safety Notes

- **Real money.** Trades execute on Polygon with real USDC. Double-check everything.
- **All trades require `--confirm`.** Without it, you get a preview only.
- **The CLI is experimental.** The Polymarket team warns: "Use at your own risk and do not use with large amounts of funds."
- **Private key security.** Your key is stored in `~/.config/polymarket/config.json`. Keep it safe.
- **Gas fees.** On-chain operations (approvals, splits, redeems) require MATIC for gas.

## API

Read-only commands use the public Gamma API (no auth):
- Base URL: `https://gamma-api.polymarket.com`

Trading commands wrap the official [Polymarket CLI](https://github.com/Polymarket/polymarket-cli) (Rust binary).
