---
name: finance
description: Track stocks, ETFs, indices, crypto (where available), and FX pairs with caching + provider fallbacks.
metadata: {"clawdbot":{"config":{"requiredEnv":["TWELVEDATA_API_KEY","ALPHAVANTAGE_API_KEY"],"stateDirs":[".cache/finance"],"example":"# Optional (only if you add a paid provider later)\n# export TWELVEDATA_API_KEY=\"...\"\n# export ALPHAVANTAGE_API_KEY=\"...\"\n"}}}
---

# Market Tracker Skill

This skill helps you fetch **latest quotes** and **historical series** for:
- Stocks / ETFs / Indices (e.g., AAPL, MSFT, ^GSPC, VOO)
- FX pairs (e.g., USD/ZAR, EURUSD, GBP-JPY)
- Crypto tickers supported by the chosen provider (best-effort)

It is optimized for:
- fast “what’s the price now?” queries
- lightweight tracking with a local watchlist
- caching to avoid rate-limits

## When to use
Use this skill when the user asks:
- “What’s the latest price of ___?”
- “Track ___ and ___ and show me daily changes.”
- “Give me a 30-day series for ___.”
- “Convert USD to ZAR (or track USD/ZAR).”
- “Maintain a watchlist and summarize performance.”

## Provider strategy (important)
- **Stocks/ETFs/indices** default: Yahoo Finance via `yfinance` (no key, broad coverage), but it is unofficial and can rate-limit.
- **FX** default: ExchangeRate-API Open Access endpoint (no key, daily update).
- If the user needs high-frequency or many symbols, recommend adding a paid provider later.

See `providers.md` for details and symbol formats.

---

# Quick start (how you run it)
These scripts are intended to be run from a terminal. The agent should:
1) ensure dependencies installed
2) run the scripts
3) summarize results cleanly

Install:
- `python -m venv .venv && source .venv/bin/activate` (or Windows equivalent)
- `pip install -r requirements.txt`

## Commands

### 1) Latest quote (stock/ETF/index)
Examples:
- `python scripts/market_quote.py AAPL`
- `python scripts/market_quote.py ^GSPC`
- `python scripts/market_quote.py VOO`

### 2) Latest FX rate
Examples:
- `python scripts/market_quote.py USD/ZAR`
- `python scripts/market_quote.py EURUSD`
- `python scripts/market_quote.py GBP-JPY`

### 3) Historical series (CSV to stdout)
Examples:
- `python scripts/market_series.py AAPL --days 30`
- `python scripts/market_series.py USD/ZAR --days 30`

### 4) Watchlist summary (local file)
- Add tickers: `python scripts/market_watchlist.py add AAPL MSFT USD/ZAR`
- Remove: `python scripts/market_watchlist.py remove MSFT`
- Show summary: `python scripts/market_watchlist.py summary`

---

# Output expectations (what you should return to the user)
- For quotes: price, change %, timestamp/source, and any caveats (like “FX updates daily”).
- For series: confirm date range, number of points, and show a small preview (first/last few rows).
- If rate-limited: explain what happened and retry with backoff OR advise to reduce frequency.

---

# Safety / correctness
- Never claim “real-time” unless the provider is truly real-time. FX open access updates daily.
- Always cache responses and throttle repeated calls.
- If Yahoo blocks requests, propose a paid provider or increase cache TTL.
