---
name: find-arbitrage-opps
description: Find arbitrage opportunities across exchanges by comparing prices for fungible token pairs like BTC/WBTC and USDT/USDC.
metadata:
  author: hummingbot
---

# find-arbitrage-opps

Find arbitrage opportunities across all Hummingbot-connected exchanges by comparing prices for a trading pair, accounting for fungible tokens (e.g., BTC = WBTC, USDT = USDC).

## Prerequisites

Hummingbot API must be running with exchange connectors configured:

```bash
bash <(curl -s https://raw.githubusercontent.com/hummingbot/skills/main/skills/lp-agent/scripts/check_prerequisites.sh)
```

## Workflow

### Step 1: Define Token Mappings

User specifies the base and quote tokens, including fungible equivalents:

- **Base tokens**: BTC, WBTC, cbBTC (all represent Bitcoin)
- **Quote tokens**: USDT, USDC, USD (all represent USD)

### Step 2: Find Arbitrage Opportunities

```bash
# Basic usage - find BTC/USDT arb opportunities
python scripts/find_arb_opps.py --base BTC --quote USDT

# Include fungible tokens
python scripts/find_arb_opps.py --base BTC,WBTC --quote USDT,USDC

# More examples
python scripts/find_arb_opps.py --base ETH,WETH --quote USDT,USDC,USD
python scripts/find_arb_opps.py --base SOL --quote USDT,USDC --min-spread 0.1

# Filter by specific connectors
python scripts/find_arb_opps.py --base BTC --quote USDT --connectors binance,kraken,coinbase
```

### Step 3: Analyze Results

The script outputs:
- Prices from each exchange
- Best bid/ask across all exchanges
- Arbitrage spread (buy low, sell high)
- Recommended pairs for arbitrage

## Script Options

```bash
python scripts/find_arb_opps.py --help
```

| Option | Description |
|--------|-------------|
| `--base` | Base token(s), comma-separated (e.g., BTC,WBTC) |
| `--quote` | Quote token(s), comma-separated (e.g., USDT,USDC) |
| `--connectors` | Filter to specific connectors (optional) |
| `--min-spread` | Minimum spread % to show (default: 0.0) |
| `--json` | Output as JSON |

## Output Example

```
Arbitrage Opportunities: BTC vs USDT
=====================================

Prices Found:
  binance          BTC-USDT     $67,234.50
  kraken           BTC-USD      $67,289.00
  coinbase         BTC-USD      $67,312.25
  okx              BTC-USDT     $67,198.00
  hyperliquid      BTC-USD      $67,245.00

Best Opportunities:
  Buy  okx BTC-USDT @ $67,198.00
  Sell coinbase BTC-USD @ $67,312.25
  Spread: 0.17% ($114.25)
```

## Environment Variables

```bash
export API_URL=http://localhost:8000
export API_USER=admin
export API_PASS=admin
```

## Requirements

- Hummingbot API running
- Exchange connectors configured with API keys
