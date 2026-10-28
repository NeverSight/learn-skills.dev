---
name: hyperliquid-grid-trading-bot
description: Configure and run an automated grid trading bot on Hyperliquid DEX with TypeScript/Node.js, supporting perpetuals and spot markets with risk management.
triggers:
  - set up hyperliquid trading bot
  - configure grid trading on hyperliquid
  - run automated trading bot hyperliquid
  - hyperliquid grid strategy configuration
  - place layered orders hyperliquid bot
  - hyperliquid trading bot stop loss take profit
  - deploy crypto grid bot hyperliquid dex
  - hyperliquid perpetuals automated trading
---

# Hyperliquid Grid Trading Bot

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

A configurable grid strategy runner for [Hyperliquid DEX](https://hyperliquid.xyz). Places layered buy/sell orders around a price range with risk controls (stop loss, take profit, drawdown limits, rebalancing). Primary implementation is **TypeScript/Node.js**; a legacy Python tree exists for reference and learning examples.

---

## Install

```bash
git clone https://github.com/PolyPulse-Analytics/hyperliquid-trading-bot.git
cd hyperliquid-trading-bot
npm install
```

**Requirements:** Node.js 20.19+, a Hyperliquid wallet private key, `git`.

Optional Python support: install [uv](https://github.com/astral-sh/uv) for legacy `src/` tree and `learning_examples/`.

---

## Environment Setup

```bash
cp .env.example .env
```

Edit `.env` — minimum required fields:

```env
# Testnet (recommended for development)
HYPERLIQUID_TESTNET_PRIVATE_KEY=0xyour_testnet_private_key_here
HYPERLIQUID_TESTNET=true

# Mainnet (real funds — use with caution)
# HYPERLIQUID_MAINNET_PRIVATE_KEY=0xyour_mainnet_private_key_here
# HYPERLIQUID_TESTNET=false
```

> **Never commit `.env` or share your private key.** Use a dedicated testnet wallet when experimenting.

---

## Key CLI Commands

| Command | Purpose |
|---------|---------|
| `npm start` | Run bot using first `active: true` config in `bots/` |
| `npm run validate` | Validate selected YAML config (no key required) |
| `npm test` | Run automated tests (grid math, etc.) |
| `npx tsc --noEmit` | TypeScript type check |
| `npx tsx ts/src/runBot.ts path/to/config.yaml` | Run with explicit config file |

```bash
# Validate before running live
npm run validate

# Start with auto-discovered active config
npm start

# Start with explicit config
npx tsx ts/src/runBot.ts bots/btc_conservative.yaml
```

---

## Bot Configuration (YAML)

Configs live in `bots/*.yaml`. Set `active: true` on exactly one file for auto-discovery.

### Full configuration reference

```yaml
# bots/my_strategy.yaml
name: "btc_grid_v1"
active: true

exchange:
  type: "hyperliquid"
  testnet: true            # Override with HYPERLIQUID_TESTNET env var

account:
  max_allocation_pct: 10.0  # Use at most 10% of account balance

grid:
  symbol: "BTC"            # Perpetual symbol on Hyperliquid
  levels: 10               # Number of grid levels (buy + sell orders)
  price_range:
    mode: "auto"           # "auto" or "manual"
    auto:
      range_pct: 5.0       # ±5% around current price
    # manual:
    #   lower: 90000
    #   upper: 100000
  order_size_usd: 50.0     # Size per grid level in USD

risk_management:
  stop_loss_enabled: false
  stop_loss_pct: 10.0       # Trigger if price drops X% below entry

  take_profit_enabled: false
  take_profit_pct: 20.0     # Trigger if profit exceeds X%

  max_drawdown_pct: 15.0    # Cancel/pause if drawdown exceeds this
  max_position_size_pct: 40.0  # Max % of allocation in open position

  rebalance:
    enabled: true
    price_move_threshold_pct: 12.0  # Rebalance grid if price moves this far

monitoring:
  log_level: "INFO"         # DEBUG | INFO | WARN | ERROR
```

### Conservative BTC example (testnet)

```yaml
# bots/btc_conservative.yaml
name: "btc_conservative"
active: true

exchange:
  type: "hyperliquid"
  testnet: true

account:
  max_allocation_pct: 5.0

grid:
  symbol: "BTC"
  levels: 8
  price_range:
    mode: "auto"
    auto:
      range_pct: 3.0
  order_size_usd: 25.0

risk_management:
  stop_loss_enabled: true
  stop_loss_pct: 8.0
  take_profit_enabled: false
  max_drawdown_pct: 10.0
  max_position_size_pct: 30.0
  rebalance:
    enabled: true
    price_move_threshold_pct: 10.0

monitoring:
  log_level: "INFO"
```

---

## Python Legacy & Learning Examples

```bash
# Sync Python dependencies
uv sync

# Validate Python bot config
uv run src/run_bot.py --validate

# Run Python bot
uv run src/run_bot.py
```

### Learning examples (educational, testnet only)

```bash
# Real-time price feed via WebSocket
uv run learning_examples/01_websockets/realtime_prices.py

# Fetch all market prices
uv run learning_examples/02_market_data/get_all_prices.py

# Place a limit order
uv run learning_examples/04_trading/place_limit_order.py
```

---

## Common Patterns

### Running multiple strategies

Only one config should have `active: true` for auto-discovery. Use explicit path to run a specific config:

```bash
# Run ETH strategy explicitly
npx tsx ts/src/runBot.ts bots/eth_aggressive.yaml

# In a separate terminal, run BTC strategy
npx tsx ts/src/runBot.ts bots/btc_conservative.yaml
```

### Switching between testnet and mainnet

```bash
# Force testnet via env (overrides YAML)
HYPERLIQUID_TESTNET=true npm start

# Mainnet — verify YAML also has testnet: false
HYPERLIQUID_TESTNET=false npx tsx ts/src/runBot.ts bots/btc_live.yaml
```

### Graceful shutdown

Press **Ctrl+C** — the engine attempts to cancel all open orders before exiting. Always check logs to confirm cancellation completed:

```bash
npm start 2>&1 | tee bot.log
# After Ctrl+C:
grep -i "cancel" bot.log
```

### Validate config without credentials

```bash
npm run validate
# or explicitly:
npx tsx ts/src/validateConfig.ts bots/my_strategy.yaml
```

---

## Grid Math Concepts

The bot divides a price range into `levels` equally spaced steps:

```
price_upper = current_price * (1 + range_pct / 100)
price_lower = current_price * (1 - range_pct / 100)
step = (price_upper - price_lower) / levels

# Buy orders placed at: price_lower, price_lower + step, ..., current_price
# Sell orders placed at: current_price, current_price + step, ..., price_upper
```

Each fill triggers the opposite order at the adjacent level, capturing the spread repeatedly.

---

## Troubleshooting

### Bot exits immediately / no orders placed
- Run `npm run validate` first — check YAML syntax errors
- Confirm `.env` has the correct private key variable for testnet vs mainnet
- Verify `HYPERLIQUID_TESTNET` matches `exchange.testnet` in YAML

### "No active config found"
- Ensure exactly one `bots/*.yaml` has `active: true`
- Or pass explicit path: `npx tsx ts/src/runBot.ts bots/myconfig.yaml`

### Orders not cancelling on shutdown
- Check logs: `grep -i "cancel\|error" bot.log`
- Manually cancel via Hyperliquid UI or API if needed
- Re-run bot briefly then Ctrl+C again

### Insufficient balance errors
- Lower `max_allocation_pct` or `order_size_usd` in YAML
- Fund testnet wallet via [testnet faucet](https://faucet.chainstack.com/hyperliquid-testnet-faucet)

### TypeScript errors
```bash
npx tsc --noEmit   # Shows all type errors without compiling
npm test           # Runs unit tests to catch logic issues
```

### Python `uv` not found
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
# or
pip install uv
```

---

## Project Structure

```
hyperliquid-trading-bot/
├── bots/                    # YAML strategy configs
│   └── btc_conservative.yaml
├── ts/src/                  # TypeScript source (primary)
│   ├── runBot.ts            # Main entrypoint
│   └── validateConfig.ts    # Config validator
├── src/                     # Python legacy bot
│   └── run_bot.py
├── learning_examples/       # Educational Python scripts
│   ├── 01_websockets/
│   ├── 02_market_data/
│   └── 04_trading/
├── .env.example             # Environment variable template
├── package.json
└── pyproject.toml           # Python deps (uv)
```

---

## Safety Checklist

- [ ] Always start on **testnet** (`HYPERLIQUID_TESTNET=true`)
- [ ] Use a **dedicated wallet** — never your main holdings wallet
- [ ] Start with **small `order_size_usd`** (e.g. $10–25)
- [ ] Enable **`max_drawdown_pct`** as a safety net
- [ ] Run `npm run validate` before every config change
- [ ] Monitor logs actively during first live run
- [ ] Keep private keys only in `.env`, never in YAML or code
