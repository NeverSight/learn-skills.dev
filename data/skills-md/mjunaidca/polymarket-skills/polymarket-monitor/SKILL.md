---
name: polymarket-monitor
description: >-
  Use this skill whenever the user wants to monitor, watch, or track Polymarket prediction market
  prices over time. This includes setting up price alerts, watching for significant price movements,
  tracking spread changes, monitoring volume spikes, or getting notified about market activity.
  Trigger on: monitor prices, price alert, watch market, track prices, notify me, price change,
  polymarket alerts, market watch, price movement, volume spike, spread monitoring, track odds,
  prediction market alerts, continuous monitoring, price tracker, market surveillance.
version: 1.0.0
author: polymarket-skills
---

# Polymarket Monitor

Monitor live Polymarket prediction markets for price changes, volume spikes, and spread movements. Outputs structured JSON alerts when thresholds are crossed. All endpoints are read-only and require no API keys.

**Prerequisite:** This skill uses token IDs from the `polymarket-scanner` skill. Run `scan_markets.py` first to discover markets and obtain token IDs.

## Quick Start

All scripts require the Python venv at `/home/verticalclaw/.venv`.

### Monitor Multiple Markets for Price Alerts

```bash
source /home/verticalclaw/.venv/bin/activate && python polymarket-monitor/scripts/monitor_prices.py \
  --token-id "<TOKEN_ID_1>" \
  --token-id "<TOKEN_ID_2>" \
  --interval 30 \
  --threshold 5.0
```

This polls every 30 seconds and prints a JSON alert whenever a token's midpoint moves more than 5% from its baseline.

### Watch a Single Market Live

```bash
source /home/verticalclaw/.venv/bin/activate && python polymarket-monitor/scripts/watch_market.py \
  --token-id "<TOKEN_ID>" \
  --interval 15
```

Prints a JSON snapshot every 15 seconds with price, spread, and order book depth.

## Scripts

### monitor_prices.py

Polls multiple tokens at a set interval and emits JSON alerts when price changes exceed a threshold.

**Arguments:**
- `--token-id ID` — CLOB token ID to monitor (repeatable, at least one required)
- `--interval N` — Polling interval in seconds (default: 30, minimum: 5)
- `--threshold N` — Percentage change to trigger an alert (default: 5.0)
- `--max-polls N` — Stop after N polls (default: unlimited, use for non-interactive runs)
- `--baseline-window N` — Number of recent prices to average for baseline (default: 1, meaning compare to last poll)

**Output:** One JSON object per line for each alert:
```json
{
  "type": "price_alert",
  "token_id": "...",
  "timestamp": "2026-02-26T12:00:00Z",
  "current_price": 0.65,
  "baseline_price": 0.60,
  "change_pct": 8.33,
  "direction": "up",
  "spread": 0.02,
  "poll_number": 5
}
```

Non-alert polls print a status line to stderr so the agent knows monitoring is active.

### watch_market.py

Continuously monitors a single market, printing a JSON snapshot each interval with price, spread, volume, and order book summary.

**Arguments:**
- `--token-id ID` — CLOB token ID to watch (required)
- `--interval N` — Snapshot interval in seconds (default: 15, minimum: 5)
- `--max-polls N` — Stop after N snapshots (default: unlimited)

**Output:** One JSON object per line per snapshot:
```json
{
  "type": "market_snapshot",
  "token_id": "...",
  "timestamp": "2026-02-26T12:00:00Z",
  "midpoint": 0.55,
  "best_bid": 0.54,
  "best_ask": 0.56,
  "spread": 0.02,
  "bid_depth": 15000.0,
  "ask_depth": 12000.0,
  "last_trade_price": 0.55,
  "last_trade_side": "BUY",
  "poll_number": 1
}
```

## Data Flow

1. Run `polymarket-scanner/scripts/scan_markets.py` to find markets and get token IDs
2. Pass token IDs to `monitor_prices.py` for multi-market alerting
3. Or pass a single token ID to `watch_market.py` for detailed single-market tracking

## Monitoring Guide

For recommended thresholds by market type and advanced monitoring strategies, see `references/monitoring-guide.md`.
