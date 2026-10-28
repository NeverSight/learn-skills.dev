---
name: nothing-ever-happens-polymarket-bot
description: Async Python bot for Polymarket that buys "No" on all standalone non-sports yes/no markets using the "nothing ever happens" strategy.
triggers:
  - set up the nothing ever happens polymarket bot
  - configure polymarket no bot
  - run polymarket trading bot
  - deploy nothing happens bot to heroku
  - enable live trading on polymarket bot
  - add nothing_happens strategy config
  - troubleshoot polymarket bot dry run
  - inspect polymarket bot positions and logs
---

# Nothing Ever Happens Polymarket Bot

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

An async Python bot that scans Polymarket standalone non-sports yes/no markets and buys the "No" outcome on any market where the NO price is below a configured cap. Designed for paper trading by default with explicit opt-in to live order transmission.

---

## What It Does

- Scans Polymarket for standalone (non-grouped) yes/no markets
- Filters out sports markets
- Buys NO positions when NO price is below `max_no_price` threshold
- Tracks open positions and persists recovery state to a database
- Exposes a live dashboard (HTTP) showing portfolio and activity
- Uses `PaperExchangeClient` unless all three live-mode env vars are set

---

## Installation

```bash
git clone https://github.com/sterlingcrispin/nothing-ever-happens.git
cd nothing-ever-happens
pip install -r requirements.txt
cp config.example.json config.json
cp .env.example .env
```

---

## Configuration

### `config.json` (non-secret runtime settings)

Edit the `strategies.nothing_happens` block:

```json
{
  "strategies": {
    "nothing_happens": {
      "max_no_price": 0.08,
      "order_size_usdc": 1.0,
      "max_open_positions": 50,
      "scan_interval_seconds": 60,
      "min_liquidity_usdc": 100,
      "exclude_keywords": ["sport", "nfl", "nba", "mlb", "nhl", "soccer", "tennis"]
    }
  }
}
```

Point to a different config file:

```bash
CONFIG_PATH=/path/to/other_config.json python -m bot.main
```

### `.env` (secrets and runtime flags)

```dotenv
# Safety flags — ALL three required for live order transmission
BOT_MODE=paper               # set to "live" for real orders
DRY_RUN=true                 # set to "false" for real orders
LIVE_TRADING_ENABLED=false   # set to "true" for real orders

# Required only in live mode
PRIVATE_KEY=$PRIVATE_KEY
FUNDER_ADDRESS=$FUNDER_ADDRESS
DATABASE_URL=$DATABASE_URL
POLYGON_RPC_URL=$POLYGON_RPC_URL

# Optional
PORT=8080
DASHBOARD_PORT=8080
```

> **Never hardcode secrets.** Always use environment variable references.

---

## Running Locally

```bash
# Paper trading (default — safe, no real orders)
python -m bot.main

# Enable live trading (requires all three flags)
BOT_MODE=live DRY_RUN=false LIVE_TRADING_ENABLED=true python -m bot.main
```

The dashboard will bind to `$PORT` or `$DASHBOARD_PORT` when set.

---

## Project Structure

```
bot/
  main.py               # Entry point — starts the runtime loop
  strategies/
    nothing_happens.py  # Core strategy: scan, filter, buy NO
  exchange/
    client.py           # Live exchange client (Polymarket CLOB API)
    paper_client.py     # PaperExchangeClient for safe simulation
  dashboard.py          # HTTP dashboard server
  recovery.py           # Persist and restore open positions

scripts/
  db_stats.py           # Inspect DB table counts and recent activity
  export_db.py          # Export live DB tables
  wallet_history.py     # Positions, trades, balances for configured wallet
  parse_logs.py         # Convert Heroku JSON logs to readable output

tests/                  # Unit and regression tests
```

---

## Key Commands

### Run Tests

```bash
python -m pytest -q
```

### Operational Scripts

```bash
# Inspect live database
python scripts/db_stats.py

# Export database tables (uses DATABASE_URL or Heroku app)
python scripts/export_db.py

# Pull wallet history
python scripts/wallet_history.py

# Parse Heroku JSON logs into readable output
python scripts/parse_logs.py
```

---

## Heroku Deployment

### One-time setup

```bash
export HEROKU_APP_NAME=my-polymarket-bot

# Set runtime flags
heroku config:set BOT_MODE=live DRY_RUN=false LIVE_TRADING_ENABLED=true \
  -a "$HEROKU_APP_NAME"

# Set secrets
heroku config:set \
  PRIVATE_KEY="$PRIVATE_KEY" \
  FUNDER_ADDRESS="$FUNDER_ADDRESS" \
  POLYGON_RPC_URL="$POLYGON_RPC_URL" \
  DATABASE_URL="$DATABASE_URL" \
  -a "$HEROKU_APP_NAME"

# Deploy
git push heroku main:main

# Scale — ONLY the web dyno
heroku ps:scale web=1 worker=0 -a "$HEROKU_APP_NAME"
```

> Do **not** run the `worker` dyno. It exists only to fail fast if started accidentally.

### Shell helpers

```bash
./alive.sh              # Check if the app is alive
./logs.sh               # Tail logs
./live_enabled.sh       # Enable live trading
./live_disabled.sh      # Disable live trading (back to paper)
./kill.sh               # Stop the bot
```

All helpers use `$HEROKU_APP_NAME` or accept an app name as an argument:

```bash
./logs.sh my-polymarket-bot
```

---

## Safety Model

The bot defaults to `PaperExchangeClient` (simulated orders, no real money) unless **all three** of these are set:

| Variable | Required value |
|---|---|
| `BOT_MODE` | `live` |
| `LIVE_TRADING_ENABLED` | `true` |
| `DRY_RUN` | `false` |

If any one is missing or wrong, paper mode is used. This is intentional — it makes accidental live trading very hard.

Additional live-mode requirements:
- `PRIVATE_KEY` — wallet private key
- `FUNDER_ADDRESS` — required for signature types `1` and `2`
- `DATABASE_URL` — for recovery state persistence
- `POLYGON_RPC_URL` — for proxy-wallet approvals and redemption

---

## Code Examples

### Check if bot will use live or paper mode

```python
import os

def is_live_mode() -> bool:
    return (
        os.getenv("BOT_MODE") == "live"
        and os.getenv("LIVE_TRADING_ENABLED", "").lower() == "true"
        and os.getenv("DRY_RUN", "true").lower() == "false"
    )

print("Live mode:", is_live_mode())
```

### Load strategy config

```python
import json, os

config_path = os.getenv("CONFIG_PATH", "config.json")
with open(config_path) as f:
    config = json.load(f)

strategy_cfg = config["strategies"]["nothing_happens"]
max_no_price = strategy_cfg["max_no_price"]       # e.g. 0.08
order_size   = strategy_cfg["order_size_usdc"]    # e.g. 1.0
print(f"Will buy NO when price <= {max_no_price} USDC, size={order_size} USDC")
```

### Run the bot programmatically

```python
import asyncio
from bot.main import main

asyncio.run(main())
```

### Inspect DB stats

```bash
DATABASE_URL=$DATABASE_URL python scripts/db_stats.py
```

### Parse Heroku logs to HTML

```bash
heroku logs --num=1500 -a "$HEROKU_APP_NAME" | python scripts/parse_logs.py --html > report.html
```

### Export DB from a Heroku app

```bash
python scripts/export_db.py --app "$HEROKU_APP_NAME"
```

---

## Common Patterns

### Disabling live trading quickly (kill switch)

```bash
heroku config:set LIVE_TRADING_ENABLED=false -a "$HEROKU_APP_NAME"
# or use the helper:
./live_disabled.sh
```

The bot will immediately fall back to paper mode on next cycle without a restart.

### Adjusting the NO price cap without redeploying

Edit `config.json`, commit, and push:

```bash
# Lower the cap to only buy very cheap NOs
jq '.strategies.nothing_happens.max_no_price = 0.05' config.json > tmp.json && mv tmp.json config.json
git add config.json && git commit -m "lower max_no_price to 0.05"
git push heroku main:main
```

### Adding more keyword exclusions

```json
{
  "strategies": {
    "nothing_happens": {
      "exclude_keywords": ["sport", "nfl", "nba", "mlb", "nhl", "soccer", "tennis", "golf", "ufc", "esport"]
    }
  }
}
```

---

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| Bot uses paper mode unexpectedly | One of the three live flags is missing/wrong | Check all three: `BOT_MODE`, `LIVE_TRADING_ENABLED`, `DRY_RUN` |
| `DATABASE_URL` errors in live mode | Postgres not provisioned | `heroku addons:create heroku-postgresql -a "$HEROKU_APP_NAME"` |
| Orders never transmit | `DRY_RUN` still `true` | `heroku config:set DRY_RUN=false` |
| Dashboard not accessible | `PORT` not set | `heroku config:set PORT=8080` |
| Worker dyno crashes immediately | Don't run worker dyno | `heroku ps:scale worker=0` |
| Bot buys sports markets | Keywords not in `exclude_keywords` | Add sport/league names to config |
| Logs unreadable (JSON) | Heroku structured logging | Pipe through `scripts/parse_logs.py` |

---

## Disclaimer

*FOR ENTERTAINMENT ONLY. PROVIDED AS IS, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED. USE AT YOUR OWN RISK. NOT FINANCIAL ADVICE.*
