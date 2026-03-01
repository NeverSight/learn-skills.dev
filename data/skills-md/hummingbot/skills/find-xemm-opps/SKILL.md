---
name: find-xemm-opps
description: Find Cross-Exchange Market Making (XEMM) opportunities by comparing order book depth and liquidity across exchanges. Identifies pairs where one exchange has thin liquidity (ideal for quoting) and another has deep liquidity (ideal for hedging).
metadata:
  author: hummingbot
---

# find-xemm-opps

Find Cross-Exchange Market Making (XEMM) opportunities by analyzing order book depth and liquidity across connected exchanges.

XEMM involves quoting on one exchange (the **maker** side) while hedging fills on another (the **taker/hedge** side). The best opportunities exist where:

- One exchange has a **wide spread** and **thin book** (maker side — room to quote profitably)
- Another has a **tight spread** and **deep book** (taker side — cheap to hedge)
- A **mid-price difference** exists between them

## Prerequisites

Hummingbot API must be running with exchange connectors configured:

```bash
bash <(curl -s https://raw.githubusercontent.com/hummingbot/skills/main/skills/lp-agent/scripts/check_prerequisites.sh)
```

## Workflow

### Step 1: Define Token Pair

```bash
# Scan for SOL/USDT XEMM opportunities
python scripts/find_xemm_opps.py --base SOL --quote USDT

# Include fungible equivalents
python scripts/find_xemm_opps.py --base ETH,WETH --quote USDT,USDC

# Filter to specific connectors
python scripts/find_xemm_opps.py --base BTC --quote USDT --connectors binance,kraken,coinbase,okx

# Minimum mid-price spread between exchanges (default: 0.0%)
python scripts/find_xemm_opps.py --base SOL --quote USDC --min-spread 0.05
```

### Step 2: Interpret Results

The script outputs a **market overview table** and ranked **XEMM opportunity pairs**:

```
====================================================================
  XEMM Opportunities — SOL / USDC
  Order book depth: 20 levels | Sources: 18
====================================================================

  Exchange               Pair            Mid     Spread    Bid Depth    Ask Depth    B/A
  ---------------------- -------------- ---------- -------- ------------ ------------ ------
  bitstamp               SOL-USDC         $87.45   0.120%       $23.4K       $18.9K   1.24
  binance                SOL-USDT         $87.51   0.015%      $412.0K      $389.0K   1.06
  okx                    SOL-USDT         $87.56   0.023%      $287.0K      $301.0K   0.95
  ...

  Top XEMM Opportunities (MAKER → hedge on TAKER):
  ----------------------------------------------------------------

  #1  Score: 8.42
      MAKER  bitstamp               $87.45  spread 0.120%  depth $42.3K
      TAKER  binance                $87.51  spread 0.015%  depth $801.0K
      Mid-price gap: 0.0686%  |  Spread ratio: 8.0x  |  Depth ratio: 18.9x
```

**Columns explained:**
| Column | Description |
|--------|-------------|
| Mid | Mid-price between best bid and ask |
| Spread | Bid-ask spread as % of mid |
| Bid/Ask Depth | Total quote value of top-N order book levels |
| B/A | Bid-to-ask depth ratio (>1 = more buy pressure) |
| Spread ratio | Maker spread ÷ taker spread — higher = better maker edge |
| Depth ratio | Taker depth ÷ maker depth — higher = better hedge liquidity |

## Script Options

| Option | Description |
|--------|-------------|
| `--base` | Base token(s), comma-separated (e.g., ETH,WETH) |
| `--quote` | Quote token(s), comma-separated (e.g., USDT,USDC) |
| `--connectors` | Filter to specific connectors (optional) |
| `--depth` | Order book depth per exchange (default: 20) |
| `--min-spread` | Minimum mid-price spread % between exchanges (default: 0.0) |
| `--include-btc-markets` | Include btc_markets (Australian residents only) |
| `--include-ndax` | Include ndax (Canadian residents only) |
| `--json` | Output as JSON |

## Environment Variables

```bash
export HUMMINGBOT_API_URL=http://localhost:8000
export API_USER=admin
export API_PASS=admin
```

Scripts check for `.env` in: `./hummingbot-api/.env` → `~/.hummingbot/.env` → `.env`

## Requirements

- Hummingbot API running
- At least 2 exchange connectors configured with API keys
