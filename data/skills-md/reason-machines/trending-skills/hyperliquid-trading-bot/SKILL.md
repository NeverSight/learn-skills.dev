---
name: hyperliquid-trading-bot
description: Configurable grid trading bot for Hyperliquid DEX with TypeScript/Node.js primary implementation, supporting perpetuals and spot markets with risk management features.
triggers:
  - set up hyperliquid trading bot
  - configure grid trading on hyperliquid
  - run hyperliquid bot with custom config
  - add stop loss or take profit to hyperliquid grid
  - hyperliquid trading bot typescript
  - place grid orders on hyperliquid dex
  - hyperliquid bot risk management settings
  - automate trading on hyperliquid perpetuals
---

# Hyperliquid Trading Bot

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

A configurable grid strategy runner for [Hyperliquid](https://hyperliquid.xyz) DEX. Places layered buy/sell orders around a price range and enforces risk rules (stop loss, take profit, drawdown limits, rebalancing). Primary stack is **TypeScript on Node.js 20.19+**; a legacy Python tree exists for reference and learning examples.

---

## Installation

```bash
git clone https://github.com/PolyPulse-Analytics/hyperliquid-trading-bot.git
cd hyperliquid-trading-bot
npm install
```

### Requirements

- Node.js **20.19+**
- A Hyperliquid wallet private key (use a dedicated testnet key to start)
- `git`

Optional for Python examples: [uv](https://github.com/astral-sh/uv)

---

## Environment Setup

```bash
cp .env.example .env
```

Edit `.env` — minimum required keys:

```env
# Testnet (recommended to start)
HYPERLIQUID_TESTNET_PRIVATE_KEY=0xYOUR_TESTNET_PRIVATE_KEY_HERE
HYPERLIQUID_TESTNET=true

# Mainnet (real funds — set carefully)
# HYPERLIQUID_MAINNET_PRIVATE_KEY=0xYOUR_MAINNET_PRIVATE_KEY_HERE
# HYPERLIQUID_TESTNET=false
```

**Never commit `.env` or share your private key.**

---

## Key Commands

| Command | Purpose |
|---|---|
| `npm start` | Run bot using first `active: true` config in `bots/` |
| `npm run validate` | Validate YAML config structure (no private key needed) |
| `npm test` | Run automated tests (grid math, etc.) |
| `npx tsc --noEmit` | TypeScript type check |
| `npx tsx ts/src/runBot.ts path/to/config.yaml` | Run with explicit config file |

### Explicit config path (recommended for multi-bot setups)

```bash
npx tsx ts/src/runBot.ts bots/btc_conservative.yaml
```

### Graceful shutdown

Press **Ctrl+C** — the engine attempts to cancel all open orders before exiting. Always review logs to confirm cancellation.

---

## Bot Configuration (YAML)

Config files live in `bots/*.yaml`. Only one file should have `active: true` when using auto-discovery via `npm start`.

### Full annotated example

```yaml
name: "btc_grid_testnet"
active: true

exchange:
  type: "hyperliquid"
  testnet: true          # Set false for mainnet — also set HYPERLIQUID_TESTNET=false in .env

account:
  max_allocation_pct: 10.0   # Max % of account balance to allocate to this grid

grid:
  symbol: "BTC"              # Hyperliquid market symbol
  levels: 10                 # Number of buy/sell levels on each side
  price_range:
    mode: "auto"             # "auto" or "manual"
    auto:
      range_pct: 5.0         # Spread ±5% from current price
    # manual:
    #   lower: 90000
    #   upper: 100000

risk_management:
  stop_loss_enabled: false
  stop_loss_pct: 8.0         # Trigger if price drops X% from entry

  take_profit_enabled: false
  take_profit_pct: 15.0      # Trigger if price rises X% from entry

  max_drawdown_pct: 15.0     # Max allowed drawdown before halting
  max_position_size_pct: 40.0 # Max position as % of allocated capital

  rebalance:
    price_move_threshold_pct: 12.0  # Rebalance grid if price moves outside this %

monitoring:
  log_level: "INFO"          # DEBUG, INFO, WARN, ERROR
```

### Manual price range example

```yaml
grid:
  symbol: "ETH"
  levels: 8
  price_range:
    mode: "manual"
    manual:
      lower: 3000
      upper: 3600
```

---

## Common Patterns

### Running multiple bots with different configs

Do not use `active: true` — call each explicitly:

```bash
# Terminal 1
npx tsx ts/src/runBot.ts bots/btc_conservative.yaml

# Terminal 2
npx tsx ts/src/runBot.ts bots/eth_aggressive.yaml
```

### Validate before running (CI/pre-flight)

```bash
npm run validate && npm start
```

### Testnet workflow before going live

1. Set `HYPERLIQUID_TESTNET=true` in `.env`
2. Set `exchange.testnet: true` in your YAML
3. Fund via [Hyperliquid testnet faucet](https://faucet.chainstack.com/hyperliquid-testnet-faucet)
4. Run `npm run validate` then `npm start`
5. Watch logs — verify orders appear in testnet UI
6. Only then flip both flags to `false` for mainnet

---

## Python Learning Examples

```bash
# Install Python deps
uv sync

# Validate Python bot config
uv run src/run_bot.py --validate

# Run Python bot (legacy)
uv run src/run_bot.py

# Educational scripts
uv run learning_examples/01_websockets/realtime_prices.py
uv run learning_examples/02_market_data/get_all_prices.py
uv run learning_examples/04_trading/place_limit_order.py
```

### Python: Fetch real-time prices via WebSocket

```python
# learning_examples/01_websockets/realtime_prices.py pattern
import asyncio
from hyperliquid.websocket_manager import WebsocketManager

async def on_message(msg):
    print(msg)

async def main():
    ws = WebsocketManager(base_url="https://api.hyperliquid-testnet.xyz")
    await ws.subscribe({"type": "allMids"}, on_message)
    await asyncio.sleep(30)

asyncio.run(main())
```

### Python: Place a limit order (testnet)

```python
# learning_examples/04_trading/place_limit_order.py pattern
import os
from hyperliquid.exchange import Exchange
from hyperliquid.utils import constants
import eth_account

private_key = os.environ["HYPERLIQUID_TESTNET_PRIVATE_KEY"]
account = eth_account.Account.from_key(private_key)

exchange = Exchange(account, constants.TESTNET_API_URL)

# Place a limit buy for 0.001 BTC at $90,000
result = exchange.order(
    "BTC",
    is_buy=True,
    sz=0.001,
    limit_px=90000,
    order_type={"limit": {"tif": "Gtc"}},
)
print(result)
```

---

## Troubleshooting

### Bot exits immediately without placing orders

- Run `npm run validate` first — check for YAML syntax errors
- Confirm `active: true` is set (or pass config path explicitly)
- Verify `HYPERLIQUID_TESTNET` in `.env` matches `exchange.testnet` in YAML

### Orders placed but immediately cancelled

- Testnet account may have insufficient balance — refund via faucet
- `max_allocation_pct` may be too low for minimum order sizes on the symbol

### TypeScript compilation errors

```bash
npx tsc --noEmit
```

Check Node.js version — must be **20.19+**:

```bash
node --version
```

### Python `uv` not found

```bash
pip install uv
# or
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Private key errors / authentication failures

- Confirm the key in `.env` matches the funded testnet wallet
- Key must include `0x` prefix
- Never use a mainnet key on testnet configs — keep separate keys

### Grid not rebalancing when price moves

Check `risk_management.rebalance.price_move_threshold_pct` — default is `12.0`. Lower it if you want more frequent rebalancing (increases gas/fees).

---

## Project Structure

```
hyperliquid-trading-bot/
├── bots/                    # YAML strategy configs
│   └── btc_conservative.yaml
├── ts/src/
│   └── runBot.ts            # Main TypeScript entrypoint
├── src/
│   └── run_bot.py           # Legacy Python entrypoint
├── learning_examples/       # Educational Python scripts
│   ├── 01_websockets/
│   ├── 02_market_data/
│   └── 04_trading/
├── .env.example             # Environment variable template
├── package.json
└── pyproject.toml
```

---

## Risk Reminder

- Always start on **testnet** with a dedicated key
- Use `max_allocation_pct` to limit exposure
- Enable `max_drawdown_pct` as a safety net before enabling stop loss/take profit
- Review open orders in the Hyperliquid UI after every bot restart
- This software is provided "as is" — you are responsible for your capital
