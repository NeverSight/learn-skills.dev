---
name: signals
description: Listen to live trading signals from SignalNGN using `sn signals`. Use this skill when acting as a trading bot to subscribe to the signal stream, parse signal payloads, filter by confidence or action, and decide when to trade.
allowed-tools: Bash
---

# Listening to Trading Signals with `sn signals`

`sn signals` subscribes to the live NATS signal stream and prints one JSON object per signal to stdout. This is the primary input loop for a trading bot agent.

## Prerequisites

`sn` must be installed and configured:

```bash
# Install
brew tap spot-canvas/sn https://github.com/Spot-Canvas/sn
brew install spot-canvas/sn/sn

# Configure (only needed if pointing at a non-default server)
sn config set api_url https://signalngn-api-potbdcvufa-ew.a.run.app
```

No NATS credentials setup is needed — `sn signals` uses embedded read-only credentials by default.

---

## Basic Usage

```bash
# All signals, all products, all strategies
sn signals --json

# Filter to one product
sn signals --json --exchange coinbase --product BTC-USD

# Filter to one granularity
sn signals --json --exchange coinbase --product BTC-USD --granularity ONE_HOUR

# Filter to one strategy
sn signals --json --exchange coinbase --product BTC-USD --strategy macd_momentum

# Combine filters
sn signals --json --exchange coinbase --product BTC-USD --granularity ONE_HOUR --strategy macd_momentum
```

**Granularity values:** `ONE_MINUTE`, `FIVE_MINUTES`, `FIFTEEN_MINUTES`, `THIRTY_MINUTES`, `ONE_HOUR`, `TWO_HOURS`, `SIX_HOURS`, `ONE_DAY`

Press **Ctrl-C** to stop.

---

## Signal Payload (JSON)

Each line of `sn signals --json` output is a JSON object with this shape:

```json
{
  "exchange":       "coinbase",
  "product":        "BTC-USD",
  "granularity":    "ONE_HOUR",
  "strategy":       "macd_momentum",
  "action":         "BUY",
  "confidence":     0.82,
  "price":          98500.50,
  "stop_loss":      97200.00,
  "take_profit":    100800.00,
  "risk_reasoning": "ATR-based stop 1.3% below entry",
  "reason":         "MACD crossed above signal line with bullish momentum",
  "position_pct":   0.25,
  "market":         "spot",
  "leverage":       1,
  "indicators": {
    "rsi":       58.3,
    "macd_hist": 0.0042,
    "sma50":     96800.0,
    "sma200":    91200.0
  },
  "timestamp":  1740218400
}
```

### Field Reference

| Field | Type | Description |
|-------|------|-------------|
| `exchange` | string | Always `"coinbase"` currently |
| `product` | string | e.g. `"BTC-USD"`, `"ETH-USD"` |
| `granularity` | string | Candle timeframe the strategy evaluated |
| `strategy` | string | Strategy that produced the signal |
| `action` | string | `"BUY"`, `"SELL"`, `"SHORT"`, or `"COVER"` |
| `confidence` | float | 0.0–1.0. Higher = stronger conviction |
| `price` | float | Candle close price at signal time |
| `stop_loss` | float | Suggested stop-loss price (0 if not set) |
| `take_profit` | float | Suggested take-profit price (0 if not set) |
| `risk_reasoning` | string | Why those SL/TP levels were chosen |
| `reason` | string | Human-readable explanation of the signal |
| `position_pct` | float | Fraction of capital suggested (0 = no recommendation) |
| `market` | string | `"spot"` or `"futures"` |
| `leverage` | int | 1 for spot; >1 for futures |
| `indicators` | object | `rsi`, `macd_hist`, `sma50`, `sma200` at signal time |
| `timestamp` | int | Unix seconds of the candle that triggered this signal |

### Action Semantics

| Action | Meaning |
|--------|---------|
| `BUY` | Open a long position (spot or futures-long) |
| `SELL` | Close a long position |
| `SHORT` | Open a short position (futures only) |
| `COVER` | Close a short position (futures only) |

**Important:** never infer direction from the strategy name alone. `ml_xgboost_short`
is the short-engine instance of `ml_xgboost` and will only ever emit `SHORT` (or
`COVER`). It will **never** emit `BUY`. Always use the `action` field to determine
what to do.

---

## Trading Bot Patterns

### Filter by confidence threshold

```bash
# Only act on signals with confidence >= 0.7
sn signals --json --exchange coinbase --product BTC-USD | \
  jq 'select(.confidence >= 0.7)'
```

### Filter to actionable signals only

```bash
# Ignore any signal that has no stop_loss set
sn signals --json | \
  jq 'select(.action != "" and .stop_loss > 0)'
```

### Watch a specific product for BUY signals

```bash
sn signals --json --product BTC-USD | \
  jq 'select(.action == "BUY") | {strategy, confidence, price, stop_loss, take_profit}'
```

### Multi-strategy consensus (count BUYs in last batch)

```bash
# Print each signal, accumulate in a loop and count
sn signals --json --product BTC-USD --granularity ONE_HOUR | \
  jq -r 'select(.action == "BUY") | [.strategy, .confidence] | @tsv'
```

### Forward signals to a webhook

```bash
sn signals --json | \
  jq -c 'select(.confidence >= 0.6)' | \
  while read -r sig; do
    curl -s -X POST https://my-bot/signal \
      -H "Content-Type: application/json" \
      -d "$sig"
  done
```

---

## NATS Subject Pattern

The underlying subject for every signal is:

```
signals.<exchange>.<product_id>.<granularity>.<strategy>
```

Examples:
```
signals.coinbase.BTC-USD.ONE_HOUR.macd_momentum
signals.coinbase.ETH-USD.FIVE_MINUTES.rsi_mean_reversion
signals.coinbase.BTC-USD.ONE_HOUR.ml_xgboost          ← long instance (BUY only)
signals.coinbase.BTC-USD.ONE_HOUR.ml_xgboost_short    ← short instance (SHORT only)
signals.coinbase.BTC-USD.ONE_HOUR.user.my-strategy
```

`sn signals` handles the subscription and wildcard expansion automatically based on your `--exchange`, `--product`, `--granularity`, `--strategy` flags.

---

## Available Strategies

### Built-in (always running)
| Strategy | Description |
|----------|-------------|
| `rsi_mean_reversion` | RSI oversold/overbought |
| `macd_momentum` | MACD crossover |
| `sma_trend` | SMA 50/200 trend follow |
| `combined_rsi_macd` | RSI + MACD together |
| `bollinger_breakout` | Bollinger band breakout |
| `bollinger_rsi` | Bollinger + RSI |
| `sma_macd` | SMA + MACD |
| `volume_momentum` | Volume-weighted momentum |
| `zscore_mean_reversion` | Z-score reversion |
| `alpha_beast` | Multi-indicator composite |
| `breakout` | Price channel breakout |

### ML (paid tier)
| Strategy | Description |
|----------|-------------|
| `ml_xgboost` | XGBoost model, 39-feature vector. Long-engine instance — emits `BUY` only |
| `ml_xgboost_short` | Same model, short-engine instance — emits `SHORT` only |

### User Starlark strategies (paid tier)
Published as `user.<strategy-name>`. Managed via `sn strategy` commands.

---

## ml_xgboost Signal Semantics

The XGBoost model outputs three probabilities on every candle: `P(hold)`, `P(long)`,
`P(short)`. The engine creates **two separate instances** from the same model —
one constrained to the long side, one to the short side — and publishes them on
separate NATS subjects.

### Long instance — strategy name `ml_xgboost`

```
Subject: signals.<exchange>.<product>.<granularity>.ml_xgboost
```

- `P(short)` is zeroed before threshold comparison — the instance can **only** produce `BUY`.
- If `P(long) > confidence` → publishes `action: "BUY"`.
- `stop_loss` is set below entry price; `take_profit` above.

### Short instance — strategy name `ml_xgboost_short`

```
Subject: signals.<exchange>.<product>.<granularity>.ml_xgboost_short
```

- `P(long)` is zeroed before threshold comparison — the instance can **only** produce `SHORT`.
- If `P(short) > confidence` → publishes `action: "SHORT"`.
- `stop_loss` is set above entry price; `take_profit` below.

### Why two instances?

Without direction constraints the model scores both sides on every candle. In a
futures short engine a strong `P(long)` could leak a `BUY` signal which a bot
might wrongly interpret as "open long". The constraint ensures:

- `ml_xgboost` → only ever `BUY`
- `ml_xgboost_short` → only ever `SHORT`

Both instances share the same confidence threshold and ATR-based SL/TP parameters
configured in trading config (`atr_stop_mult`, `rr_ratio`, `confidence`).

### Subscribing to both directions

```bash
# Long signals only
sn signals --json --strategy ml_xgboost

# Short signals only
sn signals --json --strategy ml_xgboost_short

# Both (use two subscriptions or no --strategy filter)
sn signals --json --product ADA-USD | jq 'select(.strategy | startswith("ml_xgboost"))'
```

---

## Message TTL

Signals have a 2-minute TTL set in the NATS message header (`Nats-Msg-Ttl: 2m`). Stale signals older than 2 minutes are automatically discarded and will never arrive at your subscriber. You will only ever receive fresh signals.

---

## Credentials

By default `sn signals` uses embedded read-only credentials that can only subscribe to `signals.>` (publish is denied on all subjects). No additional setup is needed.

To use custom credentials (e.g. for a private NATS deployment):

```bash
sn config set nats_creds_file ~/.config/sn/my.creds
# or per-run:
SN_NATS_CREDS_FILE=~/.config/sn/my.creds sn signals --json
```
