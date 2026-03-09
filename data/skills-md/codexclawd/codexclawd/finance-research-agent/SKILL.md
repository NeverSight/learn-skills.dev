---
name: finance-research-agent
description: "Comprehensive financial research agent for market data, news analysis, technical indicators, and report generation. Use when Codex needs to: research stocks/crypto/macro data, analyze market trends, scan financial news, generate investment theses, or produce structured research reports. Integrates with Polymarket for price tracking and supports multiple data sources (Yahoo Finance, CoinGecko, etc.)."
---

# Finance Research Agent

## Overview

This skill provides a complete framework for autonomous financial research. It handles data gathering, analysis, and report generation across multiple asset classes (stocks, crypto, commodities, macro indicators). The agent can operate in different modes: quick snapshots, deep dives, or continuous monitoring.

**Key features:**
- Multi-source market data (real-time + historical)
- News sentiment analysis
- Technical indicator calculations
- Polymarket position tracking
- Automated report generation (markdown/PDF)
- Alert/watchlist management

## Core Capabilities

### 1. Market Data Research

Fetch current and historical price data for any ticker/symbol.

**Example requests:**
- "Get me the last 30 days of BTC price data"
- "What's the current P/E ratio for AAPL?"
- "Show me the 1-hour chart for ETH"

**Usage:**
```python
from .scripts.data_fetcher import fetch_historical, fetch_current
data = fetch_historical("AAPL", period="1mo", interval="1d")
```

**Supported sources:**
- Yahoo Finance (stocks, ETFs, indices)
- CoinGecko (crypto)
- FRED API (macro indicators)
- Polymarket (prediction markets)

### 2. News & Sentiment Analysis

Scan financial news and extract sentiment/insights.

**Example requests:**
- "What's the latest news on Nvidia?"
- "Scan for Fed policy news in the last 24 hours"
- "Summarize sentiment around Tesla"

**Process:**
1. Query news APIs (Google News, RSS feeds)
2. Filter by relevance (ticker, keywords, date range)
3. Extract sentiment (positive/negative/neutral)
4. Identify key entities and events
5. Summarize findings

**Output:** JSON with articles, sentiment scores, and summary.

### 3. Technical Analysis

Calculate indicators and identify patterns.

**Indicators included:**
- Moving averages (SMA, EMA, WMA)
- RSI, MACD, Bollinger Bands
- Volume profiles
- Support/resistance levels
- Candlestick patterns

**Example:**
```
Analyze NVDA technicals:
- RSI(14) = 67.3 (neutral)
- Price above 50-day SMA
- MACD bullish crossover
```

### 4. Polymarket Integration

Track your active positions and market probabilities.

**Features:**
- List all active positions
- Check market prices vs. your entry
- Get pending market updates (US-Iran strike dates, etc.)
- Alert on significant probability shifts

**Example:**
"Show my Polymarket positions on Feb 28 Iran strike market"

### 5. Report Generation

Create professional research reports in markdown or PDF.

**Report types:**
- **Snapshot** (1-2 pages): quick overview of a ticker
- **Deep Dive** (5-10 pages): comprehensive analysis with charts
- **Daily Briefing**: top movers, news summary, watchlist updates
- **Portfolio Summary**: aggregate view of all holdings + Polymarket

**Templates available:**
- `assets/templates/report_snapshot.md`
- `assets/templates/report_deep_dive.md`
- `assets/templates/daily_briefing.md`

**Customization:**
Reports use Jinja2 templates. Edit templates in `assets/templates/` to change format, add sections, or modify branding.

### 6. Watchlist & Alerts

Maintain a watchlist of symbols and receive alerts when conditions are met.

**Alert triggers:**
- Price thresholds (above/below)
- Volume spikes (>2x average)
- News sentiment shifts
- RSI overbought/oversold
- Polymarket probability changes

**Example setup:**
```yaml
watchlist:
  - symbol: BTC-USD
    alerts:
      - price_above: 100000
      - rsi_below: 30
```

## Workflow Examples

### Quick Snapshot (10 minutes)

User: "Give me a quick read on AMD"

Agent:
1. Fetch current price and key metrics (P/E, market cap, 52w range)
2. Get last 5 news articles with sentiment
3. Calculate RSI(14)
4. Generate `snapshot_report.md` using template
5. Output report + key takeaways

### Deep Dive (30-60 minutes)

User: "Do a full analysis on Tesla including competitive landscape"

Agent:
1. Historical price data (1y) with technical charts (MA, RSI, volume)
2. Fundamental data (revenue growth, margins, EPS trends)
3. News scan (last 30 days) with sentiment aggregation
4. Competitor comparison (NIO, RIVN, traditional automakers)
5. Options flow / institutional ownership (if available)
6. Generate full report with charts (matplotlib plots saved to `assets/charts/`)
7. Provide buy/sell/hold recommendation with confidence level

### Continuous Monitoring (Scheduled)

User: "Run a daily briefing at 8am CET"

Agent:
1. Scan watchlist symbols for overnight changes
2. Pull top financial news (Bloomberg, Reuters, CNBC)
3. Check Polymarket positions for probability updates
4. Summarize significant moves
5. Send Telegram message with briefing
6. Save full report to `memory/daily_briefings/YYYY-MM-DD.md`

## Configuration

Create a `config.yaml` in your workspace to set defaults:

```yaml
data_sources:
  stocks: yahoo
  crypto: coingecko
  news: google_rss
  macro: fred

polymarket:
  enabled: true
  positions_file: memory/polymarket_positions.md

reports:
  output_dir: memory/reports/
  default_format: markdown
  include_charts: true

alerts:
  telegram_enabled: true
  check_interval_minutes: 60
```

## Scripts Reference

| Script | Purpose | Usage |
|--------|---------|-------|
| `scripts/finance_api.py` | Core API module | `from finance_api import fetch_historical, calculate_rsi, generate_snapshot_report` |
| `scripts/demo.py` | Command-line demo | `python scripts/demo.py snapshot AAPL` |

See `references/data_sources.md` and `references/technical_indicators.md` for detailed documentation.

## References

- **Data Sources:** `references/data_sources.md` — API endpoints, rate limits, setup
- **Indicators:** `references/technical_indicators.md` — formulas and interpretation
- **Report Templates:** `assets/templates/` — Jinja2 templates and examples
- **Polymarket Schema:** `references/polymarket_schema.md` — market data structure

## Integration with OpenClaw

This skill integrates with:
- **NewsClawd:** Shared news sources (avoid duplication)
- **Clawd:Mail:** Email reports automatically
- **Telegram:** Send alerts and briefings via message tool
- **Cron:** Schedule daily/weekly runs

## Examples

### Example 1: Generate a Crypto Report

```
Create a research report on Ethereum including:
- Last 90 days price action
- Dominance vs Bitcoin
- Recent ecosystem news (L2s, DeFi)
- Technical outlook (RSI, MACD, volume)
```

### Example 2: Monitor Watchlist

```
Check my watchlist (AAPL, NVDA, BTC) and alert if:
- Any price moved >5% in 24h
- RSI goes below 30 or above 70
- Major news breaks
```

### Example 3: Polymarket Position Review

```
List all my Polymarket positions on US-Iran markets
Calculate current profit/loss
Alert if any market probability shifted >20% overnight
```

## Not Included (Out of Scope)

- Automated trading / order execution (only research)
- Financial advice (disclaimer required)
- Portfolio optimization (separate skill)
- Tax reporting
- ESG/sustainability metrics

## Changelog

**v0.1.0** (2026-02-15)
- Initial release
- Core data fetching, news scanning, technical analysis
- Polymarket integration
- Report generation with templates
