---
name: crypto-research
description: |
  Performs comprehensive due diligence on a cryptocurrency using CoinMarketCap MCP data.
  Use when users ask about a specific coin beyond just its price. This includes questions like "what is [coin]", "is [coin] legit", "analyze [coin]", tokenomics questions, holder distribution, or any request for deep information about a single cryptocurrency.
  Trigger: "research [coin]", "tell me about [coin]", "should I invest in [coin]", "DYOR [coin]", "is [coin] safe", "/crypto-research"
license: MIT
compatibility: ">=1.0.0"
user-invocable: true
allowed-tools:
  - mcp__cmc-mcp__search_cryptos
  - mcp__cmc-mcp__get_crypto_quotes_latest
  - mcp__cmc-mcp__get_crypto_info
  - mcp__cmc-mcp__get_crypto_metrics
  - mcp__cmc-mcp__get_crypto_technical_analysis
  - mcp__cmc-mcp__get_crypto_latest_news
  - mcp__cmc-mcp__search_crypto_info
---

# Crypto Research Skill

Perform comprehensive due diligence on any cryptocurrency by systematically gathering and analyzing data from multiple CMC MCP tools.

## Prerequisites

Before starting research, verify the CMC MCP tools are available. If tools fail or return connection errors, ask the user to set up the MCP connection:

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

Thorough research requires looking at a token from multiple angles. Fetch all relevant data before forming conclusions. Surface both green flags and red flags.

## Research Workflow

### Step 1: Identify the Token

Call `search_cryptos` with the token name/symbol to get the CMC ID. If multiple results, clarify with the user which one they mean.

### Step 2: Basic Information

Call `get_crypto_info` to get:
- Project description and category
- Launch date
- Website, social links, documentation
- Tags (DeFi, Layer 1, Meme coin, etc.)

### Step 3: Market Data

Call `get_crypto_quotes_latest` to get:
- Current price and market cap
- 24h, 7d, 30d, 90d, 1y price changes
- Trading volume and volume change
- Circulating supply vs max supply
- Market cap rank

### Step 4: Holder Analysis

Call `get_crypto_metrics` to get:
- Address distribution by holding value ($0-1k, $1k-100k, $100k+)
- Whale concentration (% held by top holders)
- Holder behavior (traders vs cruisers vs long-term holders)

### Step 5: Technical Analysis

Call `get_crypto_technical_analysis` to get:
- Moving averages (7d, 30d, 200d SMA/EMA)
- RSI (oversold < 30, overbought > 70)
- MACD signal
- Fibonacci levels and pivot points

### Step 6: Recent News

Call `get_crypto_latest_news` with limit 5-10 to get recent headlines and sentiment.

### Step 7: Deep Dive (if needed)

Call `search_crypto_info` to answer specific questions about the token's technology, use case, or mechanics.

## Analysis Framework

After gathering data, evaluate across these dimensions:

### Fundamentals
- What problem does it solve?
- Is there a working product?
- How does it compare to competitors?
- Is the use case sustainable?

### Tokenomics
- What % of max supply is circulating?
- Is there inflation or deflation?
- Are there large unlocks coming?
- How concentrated is ownership?

### Market Position
- Market cap rank and trajectory
- Volume relative to market cap (healthy turnover?)
- Price trend (accumulation or distribution?)

### Risk Factors

**Red flags and why they matter:**
- Extreme whale concentration (>10% held by few addresses): Large holders can dump and crash price instantly
- Low holder count relative to market cap: Thin holder base means price is easily manipulated
- Declining holder numbers: Smart money may be exiting while retail holds bags
- Negative news sentiment: Ongoing negative coverage often precedes further declines
- Price down >80% from ATH with no recovery: May indicate fundamental problems, not just market cycles
- Very low trading volume: Hard to exit positions without significant slippage

**Green flags and why they matter:**
- Growing holder base: Organic adoption suggests real demand, not manufactured hype
- High % of long-term holders: Conviction from holders who have done research, less sell pressure
- Healthy distribution across address sizes: Resilient to any single actor manipulating price
- Active development and news flow: Team is shipping, project is alive and evolving
- Strong community engagement: Network effects build value and create sustainable demand

## Report Structure

Present findings in this format:

```
## [Token Name] Research Report

### Overview
- Category: [DeFi/Layer 1/Meme/etc.]
- Launched: [Date]
- Rank: #XX by market cap

### Market Data
- Price: $X.XX
- Market Cap: $X.XX B
- 24h Volume: $X.XX M
- Performance: 24h X.X% | 7d X.X% | 30d X.X% | 1y X.X%

### Supply
- Circulating: X.XX M (XX% of max)
- Max Supply: X.XX M

### Holder Analysis
- Total Addresses: X.XX M
- Whale Concentration: X.X%
- Long-term Holders: XX%
- Holder Trend: Growing/Stable/Declining

### Technical Outlook
- RSI: XX (oversold/neutral/overbought)
- Trend: Above/Below 200d MA
- Key Support: $X.XX
- Key Resistance: $X.XX

### Recent News
- [Headline 1]
- [Headline 2]
- ...

### Green Flags
- [List positive indicators]

### Red Flags
- [List concerns]

### Summary
[2-3 sentence synthesis of the research findings]
```

## Important Notes

- This is research, not financial advice
- Always present both positive and negative findings
- If data is missing or unavailable, note it explicitly
- For very new tokens, some metrics may be limited

## Handling Tool Failures

If individual tools fail during research:

1. **search_cryptos fails**: Cannot proceed without token ID. Ask user to verify spelling or try the contract address.
2. **get_crypto_info fails**: Skip Overview section, note "Project details unavailable" in report.
3. **get_crypto_quotes_latest fails**: Report is incomplete without price data. Retry once, then note "Market data unavailable."
4. **get_crypto_metrics fails**: Skip Holder Analysis section, note "Distribution data unavailable."
5. **get_crypto_technical_analysis fails**: Skip Technical Outlook section, note "Technical analysis unavailable."
6. **get_crypto_latest_news fails**: Skip Recent News section, proceed with other data.

Always complete the report with available data rather than abandoning the research entirely.
