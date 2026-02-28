---
name: sn
description: Use the sn CLI to manage the SignalNGN platform. Covers products, backfill, backtests, trading config, user strategies, strategies, ML model reloads, metrics, engine status, tenants, live signal streaming, and live price lookup. Use sn instead of curl for all API operations.
---

# sn — SignalNGN CLI

`sn` is the unified CLI for the [SignalNGN](https://signalngn.com) cryptocurrency trading platform.
It wraps every API endpoint with a consistent interface: human table output by
default, `--json` for scripting.

## Setup

### Install

```bash
# Homebrew (macOS / Linux)
brew tap spot-canvas/sn https://github.com/Spot-Canvas/sn
brew install spot-canvas/sn/sn

# Go toolchain
go install github.com/Spot-Canvas/sn/cmd/sn@latest
```

### Configure

Config file: `~/.config/sn/config.yaml` (created on first `sn config set`).

```bash
# Point at staging (ingestion server)
sn config set ingestion_url https://ingest.signalngn.com

# Point at staging (API server)
sn config set api_url https://api.signalngn.com

# Set tenant ID (for trading config operations)
sn config set tenant_id 00000000-0000-0000-0000-000000000001

# Show all resolved config and sources
sn config show
```

**Priority** (highest first): `--flag` > `SN_*` env var > `~/.config/sn/config.yaml` > built-in default (`http://localhost:8081` / `http://localhost:8082`).

**Valid config keys**: `tenant_id`, `api_url`, `ingestion_url`, `nats_url`, `nats_creds_file`

---

## Products

Manage which coins the ingestion pipeline tracks.

| Command | Description |
|---------|-------------|
| `sn products list` | List all products |
| `sn products list --enabled` | Only enabled products |
| `sn products list --exchange coinbase` | Filter by exchange |
| `sn products get coinbase BTC-USD` | Get a single product |
| `sn products add coinbase SOL-USD` | Add a product |
| `sn products enable coinbase SOL-USD` | Enable ingestion |
| `sn products disable coinbase SOL-USD` | Pause ingestion |
| `sn products delete coinbase SOL-USD` | Remove from pipeline |

```bash
# Add and enable a new coin
sn products add coinbase NEAR-USD
sn products enable coinbase NEAR-USD

# List enabled coinbase products as JSON (pipe to jq)
sn products list --exchange coinbase --enabled --json | jq '.[].product_id'
```

---

## Backfill

Trigger historical candle backfill jobs.

| Command | Description |
|---------|-------------|
| `sn backfill start <exchange> <product>` | Start a backfill job |
| `sn backfill start ... --days 60` | Backfill 60 days (default: 30) |
| `sn backfill list <exchange> <product>` | List jobs for a product |
| `sn backfill get <exchange> <product> <job-id>` | Get job status |
| `sn backfill cancel <exchange> <product> <job-id>` | Cancel a pending or running job |

Jobs are executed **one at a time** per tenant server — concurrent backfills are queued and run serially to avoid OOM. Use `cancel` to drain the queue if needed.

```bash
# Backfill 90 days of SOL-USD
sn backfill start coinbase SOL-USD --days 90

# Monitor progress
sn backfill list coinbase SOL-USD
sn backfill get coinbase SOL-USD <job-id>

# Cancel a specific job (pending or running)
sn backfill cancel binance BTC-USD <job-id>

# Cancel all pending/running backfill jobs for a product
sn backfill list binance BTC-USD --json \
  | jq -r '.[] | select(.status == "pending" or .status == "running") | .id' \
  | xargs -I{} sn backfill cancel binance BTC-USD {}
```

---

## Backtest

Run and query backtests against historical data.

| Command | Description |
|---------|-------------|
| `sn backtest run` | Submit a backtest and **wait for results** (default) |
| `sn backtest run --no-wait` | Submit and return immediately; prints poll command |
| `sn backtest job <job-id>` | Poll a job; prints result when completed |
| `sn backtest list` | List results |
| `sn backtest get <id>` | Get a result by ID |

Backtests run asynchronously on the tenant server. `sn backtest run` submits the
job and then polls `GET /jobs/{id}` every 2 seconds (printing dots) until the job
completes or fails, then prints the full result. Use `--no-wait` to get back a
job ID immediately instead.

**`sn backtest run` flags:**

| Flag | Description | Default |
|------|-------------|---------|
| `--exchange` | Exchange (required) | — |
| `--product` | Product ID (required) | — |
| `--strategy` | Strategy name (required) | — |
| `--granularity` | Granularity e.g. ONE_HOUR (required) | — |
| `--mode` | `spot`, `futures-long`, `futures-short` | `spot` |
| `--start` | Start date YYYY-MM-DD | 1 year ago |
| `--end` | End date YYYY-MM-DD | today |
| `--leverage` | Leverage (futures modes) | — |
| `--trend-filter` | Enable trend filter | false |
| `--no-wait` | Return immediately after submitting | false |

```bash
# Spot backtest — waits and prints result when done
sn backtest run --exchange coinbase --product BTC-USD \
  --strategy macd_momentum --granularity ONE_HOUR

# Submit without waiting; prints job ID and poll command
sn backtest run --exchange coinbase --product BTC-USD \
  --strategy ml_xgboost --granularity ONE_HOUR --no-wait
# → Job ID: abc123  Status: pending
# → Poll:   sn backtest job abc123

# Poll an existing job (prints result table when done, dots while running)
sn backtest job abc123

# Futures with leverage
sn backtest run --exchange coinbase --product ETH-USD \
  --strategy rsi_mean_reversion --granularity THIRTY_MINUTES \
  --mode futures-long --leverage 2

# List all BTC-USD backtests
sn backtest list --product BTC-USD

# Get result and pipe to jq
sn backtest get 42 --json | jq '.metrics'
```

---

## Trading Config

Manage server-side trading configuration (which strategies run on which products).

| Command | Description |
|---------|-------------|
| `sn trading list` | List all configs |
| `sn trading list --enabled` | Only enabled configs |
| `sn trading get <exchange> <product>` | Get config |
| `sn trading set <exchange> <product> [flags]` | Create or update |
| `sn trading delete <exchange> <product>` | Remove config |
| `sn trading reload` | Hot-reload config into running engine |

**`sn trading set` flags** (unset flags preserve existing values):

| Flag | Description |
|------|-------------|
| `--granularity <g>` | Candle granularity |
| `--long <strategies,...>` | Comma-separated long strategies |
| `--short <strategies,...>` | Comma-separated short strategies |
| `--spot <strategies,...>` | Comma-separated spot strategies |
| `--long-leverage <n>` | Long leverage |
| `--short-leverage <n>` | Short leverage |
| `--trend-filter` | Enable trend filter |
| `--no-trend-filter` | Disable trend filter |
| `--enable` | Enable this config |
| `--disable` | Disable this config |
| `--params <strategy>:<key>=<value>` | Set a per-strategy parameter override (repeatable). Use `<strategy>:clear` to remove all overrides for a strategy. |

`--params` merges into the existing `strategy_params` — other strategies and keys are preserved. Valid keys per strategy:

| Strategy | Valid keys |
|----------|-----------|
| `ml_xgboost` | `atr_stop_mult`, `rr_ratio`, `confidence`, `exit_confidence` |
| `alpha_beast` | `atr_stop_mult`, `rr_ratio`, `rsi_buy_max`, `rsi_sell_min`, `vol_multiplier` |
| `zscore_mean_reversion` | `entry`, `exit`, `max_pos`, `dampening` |
| `rsi_mean_reversion` | `oversold`, `overbought` |
| `macd_momentum` | `threshold` |
| `volume_momentum` | `multiplier` |
| `combined_rsi_macd` | `oversold`, `overbought` |
| `bollinger_rsi` | `rsi_oversold`, `rsi_overbought` |

`exit_confidence` (ml_xgboost only, default `0.72` = same as `confidence`): lower probability bound for exit signals. When the model's conviction for the open side drops below this threshold after a prior entry, a SELL exit (or COVER for futures-short) is emitted. Default equals `confidence` so an exit fires as soon as the entry condition is no longer met. Lower values widen the hysteresis band (exit only on strong conviction loss); must be > 0 and ≤ `confidence`.

```bash
# Create a new trading config
sn trading set coinbase XRP-USD \
  --granularity ONE_HOUR \
  --long macd_momentum \
  --short macd_momentum,rsi_mean_reversion \
  --short-leverage 2 \
  --enable

# Disable a config without changing anything else
sn trading set coinbase XRP-USD --disable

# Widen SL/TP for ml_xgboost on ATOM-USD (strong trend market)
sn trading set coinbase ATOM-USD \
  --params ml_xgboost:atr_stop_mult=2.5 \
  --params ml_xgboost:rr_ratio=3.0

# Tighten ml_xgboost exit threshold on BTC-USD (exit sooner on conviction loss)
sn trading set binance BTC-USD \
  --params ml_xgboost:exit_confidence=0.50

# Set alpha_beast ATR multiplier and clear ml_xgboost overrides
sn trading set coinbase BTC-USD \
  --params alpha_beast:atr_stop_mult=3.0 \
  --params ml_xgboost:clear

# Reload engine after changes
sn trading reload

# List all enabled configs as table (includes PARAMS column)
sn trading list --enabled
```

---

## User Strategies

Author, validate, and manage custom Starlark strategies.

| Command | Description |
|---------|-------------|
| `sn strategy list` | List all user strategies |
| `sn strategy list --active` | Only active strategies |
| `sn strategy get <id>` | Get strategy with source |
| `sn strategy validate --name <n> --file <path>` | Validate source |
| `sn strategy create --name <n> --file <path>` | Create strategy |
| `sn strategy update <id> --file <path>` | Update source |
| `sn strategy activate <id>` | Activate strategy |
| `sn strategy deactivate <id>` | Deactivate strategy |
| `sn strategy delete <id>` | Delete strategy |
| `sn strategy backtest <id>` | Backtest a user strategy |

**`sn strategy create` flags:**

| Flag | Description |
|------|-------------|
| `--name <n>` | Strategy name (required) |
| `--file <path>` | Path to .star source file (required) |
| `--description <d>` | Optional description |
| `--params <json>` | Parameters JSON, e.g. `'{"THRESHOLD": 2.0}'` |

```bash
# Validate before creating
sn strategy validate --name my_strat --file ./my_strat.star

# Create and activate
sn strategy create --name my_strat --file ./my_strat.star \
  --description "RSI bounce with volume filter"
sn strategy activate 5

# Backtest a user strategy
sn strategy backtest 5 \
  --exchange coinbase --product BTC-USD \
  --granularity ONE_HOUR --mode spot \
  --start 2024-01-01 --end 2025-01-01
```

---

## Strategies (built-in + user)

List all available strategies (both built-in and user-defined):

```bash
sn strategies list

# JSON output for scripting
sn strategies list --json | jq '.builtin[].name'
```

---

## ML Model

Hot-reload an ML model from a GCS URI:

```bash
sn ml reload --uri gs://spot-canvas-models/ml_xgboost/latest/model.onnx
```

---

## Metrics

Display a live metrics dashboard from the ingestion server:

```bash
sn metrics

# Raw JSON metric map (pipe to jq)
sn metrics --json | jq '.spot_canvas_candles_processed_total'
```

**Dashboard sections:**
- Uptime, goroutines, heap memory
- Pipeline: candles received/processed, throughput
- Batch writer: batch count, avg size, DB write latency
- WebSocket: connections, reconnects, errors
- Channel utilization bar chart (WARN above 80%)
- Top 10 products by candles processed
- Strategy evaluations, signals, signal rate
- Indicator alert breakdown

---

## Engine Status

Show indicator engine state (products, granularities, warming count):

```bash
sn engine status

sn engine status --json
```

---

## Tenants

Manage tenants on the API server.

| Command | Description |
|---------|-------------|
| `sn tenants list` | List all tenants |
| `sn tenants get <id>` | Get a tenant |
| `sn tenants create --name <n>` | Create a tenant |
| `sn tenants update <id> [flags]` | Update a tenant |

```bash
# Create a paid tenant
sn tenants create --name acme --tier paid

# Update tier
sn tenants update <id> --tier paid

# Set always-on
sn tenants update <id> --always-on

# List all tenants
sn tenants list --json | jq '.[].name'
```

---

## Price

Query the current live price for a product (or all enabled products).

| Command | Description |
|---------|-------------|
| `sn price <product>` | Show live price for a product |
| `sn price <product> --exchange <e>` | Specify exchange (default: `coinbase`) |
| `sn price <product> --granularity <g>` | Specify granularity (default: `ONE_MINUTE`) |
| `sn price --all` | Show live prices for all enabled products |
| `sn price --all --granularity ONE_HOUR` | All products at a coarser granularity |

**Output columns:** `EXCHANGE`, `PRODUCT`, `PRICE`, `OPEN`, `HIGH`, `LOW`, `VOLUME`, `AGE`

`AGE` is the time since the last candle update (`< 1s`, `4s`, `2m 30s`, `!1h 5m`).
Ages over 1 hour are prefixed with `!` to signal potential staleness.

```bash
# Current BTC-USD price
sn price BTC-USD

# ETH-USD on the ONE_HOUR candle
sn price ETH-USD --granularity ONE_HOUR

# All enabled products, sorted by exchange then product
sn price --all

# All prices as JSON (only products with data)
sn price --all --json

# Single product as raw JSON
sn price BTC-USD --json | jq '.close'
```

**Notes:**
- Backed by `GET /prices/{exchange}/{product}?granularity=` on the API server.
- Returns the latest candle written by the ingestion server (updated ~every 50ms).
- Products with no candle data yet show `—` / `no data` in `--all` mode.

---

## Signals

Stream live strategy signals from NATS in real time.

```bash
# All signals
sn signals

# Filter by product and exchange
sn signals --exchange coinbase --product BTC-USD

# Filter by strategy
sn signals --strategy macd_momentum

# Filter by granularity
sn signals --granularity ONE_HOUR

# NDJSON output (pipe to jq)
sn signals --json | jq 'select(.action == "BUY")'
```

**Output format** (one line per signal):
```
14:32:05  coinbase  BTC-USD  ONE_HOUR  macd_momentum  BUY   conf=0.82  sl=91200.00  tp=96800.00
```

**Credentials**: By default, uses embedded read-only NATS credentials scoped
to `signals.>`. Override with:
```bash
sn config set nats_creds_file ~/.config/sn/custom.creds
# or
SN_NATS_CREDS_FILE=~/.config/sn/custom.creds sn signals
```

**Exit**: Press Ctrl-C to unsubscribe and exit cleanly.

---

## Tips & Scripting

### Global flags (available on all commands)
```
--ingestion-url <url>   Override ingestion server URL
--api-url <url>         Override API server URL
--json                  Output as JSON
```

### Common scripting patterns

```bash
# Get all enabled product IDs for coinbase
sn products list --exchange coinbase --enabled --json | jq -r '.[].product_id'

# Run backtest for all products in trading config (waits for each result)
sn trading list --enabled --json | jq -r '.[] | .exchange + " " + .product_id' | while read e p; do
  sn backtest run --exchange $e --product $p --strategy macd_momentum --granularity ONE_HOUR --json
done

# Submit all at once without waiting, then poll each job
sn trading list --enabled --json | jq -r '.[] | .exchange + " " + .product_id' | while read e p; do
  sn backtest run --exchange $e --product $p --strategy macd_momentum --granularity ONE_HOUR --no-wait
done

# Check live price quickly
sn price BTC-USD

# Check all prices and highlight stale ones (AGE starts with !)
sn price --all | grep '!'

# Get close price as a number
sn price BTC-USD --json | jq '.close'

# Watch metrics (refresh every 30s)
watch -n 30 sn metrics

# Monitor signals and alert on low confidence
sn signals --json | jq 'select(.confidence < 0.5) | "LOW CONF: " + .product + " " + .action'

# Pipe backtest results to jq for analysis
sn backtest list --strategy macd_momentum --json | jq '[.results[] | {product: .product_id, return: .metrics.total_return}] | sort_by(-.return)'
```

### Point at local development servers

```bash
SN_INGESTION_URL=http://localhost:8081 SN_API_URL=http://localhost:8082 sn products list
```

Or set permanently:
```bash
sn config set ingestion_url http://localhost:8081
sn config set api_url http://localhost:8082
```
