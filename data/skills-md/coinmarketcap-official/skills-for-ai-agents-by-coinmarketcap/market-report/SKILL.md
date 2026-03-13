---
name: market-report
description: |
  Generates a comprehensive crypto market report using CoinMarketCap MCP data.
  Use when users ask about overall market conditions, sentiment, or want a summary. Also use for questions about fear/greed, BTC dominance, altcoin season, trending narratives, or general "how's the market" queries.
  Trigger: "market report", "market overview", "what's happening in crypto", "market sentiment", "fear and greed", "is it altcoin season", "/market-report"
license: MIT
compatibility: ">=1.0.0"
user-invocable: true
allowed-tools:
  - mcp__cmc-mcp__get_global_metrics_latest
  - mcp__cmc-mcp__get_global_crypto_derivatives_metrics
  - mcp__cmc-mcp__trending_crypto_narratives
  - mcp__cmc-mcp__get_upcoming_macro_events
  - mcp__cmc-mcp__get_crypto_marketcap_technical_analysis
  - mcp__cmc-mcp__get_crypto_quotes_latest
  - mcp__cmc-mcp__search_cryptos
---

# Market Report Skill

Generate a comprehensive crypto market report by systematically pulling data from multiple CMC MCP tools.

## Prerequisites

Before generating a report, verify the CMC MCP tools are available. If tools fail or return connection errors, ask the user to set up the MCP connection:

```json
{
  "mcpServers": {
    "cmc-mcp": {
      "url": "https://mcp.coinmarketcap.com/mcp",
      "headers": {
        "X-CMC-MCP-API-KEY": "your-api-key"
      }
    }
  }
}
```

Get your API key from https://pro.coinmarketcap.com/login

## Core Principle

Fetch data from all relevant tools to provide a complete market picture. Users want a one-stop summary they can rely on daily.

## Report Workflow

### Step 1: Global Market Health

Call `get_global_metrics_latest` to get:
- Total crypto market cap and 24h/7d/30d changes
- Fear & Greed Index (current value and trend)
- Altcoin Season Index
- BTC and ETH dominance
- Total volume
- ETF flows (BTC and ETH)

### Step 2: Market Technical Analysis

Call `get_crypto_marketcap_technical_analysis` to get:
- Total market cap RSI
- MACD signals
- Key support/resistance levels (Fibonacci, pivot points)

### Step 3: Leverage and Derivatives

Call `get_global_crypto_derivatives_metrics` to get:
- Total open interest and changes
- Funding rates (positive = longs paying shorts)
- BTC liquidations (long vs short bias)
- Futures vs perpetuals breakdown

### Step 4: Trending Narratives

Call `trending_crypto_narratives` to get:
- Top trending themes/sectors
- Market cap and performance of each narrative
- Top coins within each narrative

### Step 5: Upcoming Catalysts

Call `get_upcoming_macro_events` to get:
- Fed meetings and rate decisions
- Regulatory deadlines
- Major protocol upgrades
- Other market-moving events

### Step 6: BTC and ETH Quick Check

Call `get_crypto_quotes_latest` with id="1,1027" to get current BTC and ETH prices and changes as anchors for the report.

## Report Structure

Present the data in this order:

```
## Market Snapshot
- Total market cap: $X.XX T (24h: +X.X%)
- Fear & Greed: XX (Extreme Fear/Fear/Neutral/Greed/Extreme Greed)
- BTC Dominance: XX% | ETH Dominance: XX%
- Altcoin Season Index: XX

## BTC & ETH
- BTC: $XX,XXX (24h: X.X%, 7d: X.X%)
- ETH: $X,XXX (24h: X.X%, 7d: X.X%)

## Market Technicals
- RSI: XX (oversold/neutral/overbought)
- MACD: bullish/bearish
- Key levels: support at $X.XX T, resistance at $X.XX T

## Leverage & Sentiment
- Open Interest: $XXX B (24h: X.X%)
- Funding Rate: X.XXX% (longs/shorts paying)
- 24h Liquidations: $XXX M (XX% longs, XX% shorts)

## Trending Narratives
1. Narrative Name - $XX B market cap, +XX% (7d)
2. ...

## Upcoming Catalysts
- Date: Event description
- ...
```

## Adapting the Report

- **Quick summary**: If user asks for brief overview, focus on Market Snapshot and BTC/ETH sections only
- **Full report**: Include all sections
- **Specific focus**: If user asks about derivatives or narratives specifically, expand that section with more detail

## Handling Tool Failures

If individual tools fail during report generation:

1. **get_global_metrics_latest fails**: Critical for Market Snapshot. Retry once, then note "Global metrics unavailable" and skip that section.
2. **get_crypto_marketcap_technical_analysis fails**: Skip Market Technicals section, proceed with other data.
3. **get_global_crypto_derivatives_metrics fails**: Skip Leverage & Sentiment section, note "Derivatives data unavailable."
4. **trending_crypto_narratives fails**: Skip Trending Narratives section, proceed with core metrics.
5. **get_upcoming_macro_events fails**: Skip Upcoming Catalysts section, proceed with market data.
6. **get_crypto_quotes_latest fails**: Note "BTC/ETH price check unavailable" but continue with global metrics.

Always deliver a partial report with available data rather than no report at all. Clearly note which sections are missing and why.
