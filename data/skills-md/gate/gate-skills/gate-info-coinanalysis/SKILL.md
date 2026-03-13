---
name: gate-info-coinanalysis
version: "2026.3.12-2"
updated: "2026-03-11"
description: "Coin comprehensive analysis. Use this skill whenever the user asks to analyze a single coin. Trigger phrases include: analyze, how is, worth buying, look at. MCP tools: info_coin_get_coin_info, info_marketsnapshot_get_market_snapshot, info_markettrend_get_technical_analysis, news_feed_search_news, news_feed_get_social_sentiment."
---

# gate-info-coinanalysis

> The most frequently used Skill. The user inputs a coin name, the system calls 5 MCP Tools in parallel to fetch fundamentals + market data + technicals + news + social sentiment, then the LLM aggregates the results into a structured analysis report.

**Trigger Scenarios**: User mentions a specific coin + keywords like analyze, how is, worth, look at, fundamentals, market analysis.

---

## Routing Rules

| User Intent | Keywords | Action |
|-------------|----------|--------|
| Single coin comprehensive analysis | "analyze SOL" "how is BTC" "is ETH worth buying" | Execute this Skill's full workflow |
| Price only | "what's BTC price" "ETH current price" | Do NOT use this Skill — call `info_marketsnapshot_get_market_snapshot` directly |
| Multi-coin comparison | "compare BTC and ETH" | Route to `gate-info-coincompare` |
| News only | "any SOL news lately" | Route to `gate-news-briefing` |
| Technicals only | "BTC technical analysis" "what's the RSI" | Route to `gate-info-trendanalysis` |

---

## Execution Workflow

### Step 1: Intent Recognition & Parameter Extraction

Extract from user input:
- `symbol`: Coin ticker (e.g., BTC, SOL, ETH)
- If the user mentions a project name (e.g., Solana, Uniswap), map it to the ticker symbol

If the coin cannot be identified, **ask the user to clarify the coin name** — do not guess.

### Step 2: Call 5 MCP Tools in Parallel

| Step | MCP Tool | Parameters | Retrieved Data | Parallel |
|------|----------|------------|----------------|----------|
| 1a | `info_coin_get_coin_info` | `query={symbol}, scope="full"` | Fundamentals: project info, team, funding, sector, tokenomics, unlock schedule | Yes |
| 1b | `info_marketsnapshot_get_market_snapshot` | `symbol={symbol}, timeframe="1d", source="spot"` | Market data: price, 24h/7d change, market cap, OI, funding rate, Fear & Greed Index | Yes |
| 1c | `info_markettrend_get_technical_analysis` | `symbol={symbol}` | Technicals: multi-timeframe signals (RSI zones, MACD cross, MA alignment, support/resistance) | Yes |
| 1d | `news_feed_search_news` | `coin={symbol}, limit=5, sort_by="importance"` | News: top 5 most important recent articles | Yes |
| 1e | `news_feed_get_social_sentiment` | `coin={symbol}` | Social sentiment: Twitter KOL discussion volume, sentiment bias | Yes |

> All 5 Tools are called in parallel with no dependencies. If no news MCP is configured, call only the first 3 Gate-info tools; mark sentiment sections as "No data".

### Step 3: LLM Aggregation

Pass all 5 Tool responses to the LLM to generate a structured analysis report.

### Step 4: Output Structured Report

---

## Report Template

```markdown
## {symbol} Comprehensive Analysis

### 1. Fundamentals Overview

| Metric | Value |
|--------|-------|
| Project Name | {project_name} |
| Sector | {category} |
| Market Cap Rank | #{market_cap_rank} |
| Circulating Market Cap | ${market_cap} |
| Fully Diluted Valuation | ${fdv} |
| Total Funding Raised | ${total_funding} |
| Key Investors | {investors} |

{Brief analysis of tokenomics and unlock schedule; flag any upcoming large unlocks}

### 2. Market Data & Technical Analysis

**Current Market Data**

| Metric | Value | Status |
|--------|-------|--------|
| Price | ${price} | — |
| 24h Change | {change_24h}% | {Up/Down/Sideways} |
| 7d Change | {change_7d}% | {Up/Down/Sideways} |
| 24h Volume | ${volume_24h} | {High/Low/Normal} |
| RSI(14) | {rsi} | {Overbought/Oversold/Neutral} |
| Fear & Greed Index | {fear_greed} | {Extreme Fear/Fear/Neutral/Greed/Extreme Greed} |

**Technical Signals**

{Based on info_markettrend_get_technical_analysis multi-timeframe signals, give a Bullish/Bearish/Neutral overall assessment}

- Short-term (1h/4h): {signal}
- Medium-term (1d): {signal}
- Support: ${support}
- Resistance: ${resistance}

### 3. News & Market Sentiment

**Recent Key News**

1. [{title}]({source}) — {summary} ({time})
2. ...

**Social Sentiment**

- Twitter Discussion Volume: {level}
- KOL Sentiment Bias: {Bullish/Bearish/Neutral}
- Sentiment Score: {sentiment_score}

### 4. Overall Assessment

{LLM generates a 3-5 sentence assessment covering:}
- Current market phase for this asset
- Primary drivers (fundamentals / technicals / sentiment)
- Key risks to monitor

### ⚠️ Risk Warnings

{Data-driven risk alerts, e.g.:}
- RSI overbought — elevated short-term pullback risk
- Upcoming large token unlock
- High funding rate — leveraged long crowding
- Low liquidity (if applicable)

> The above analysis is data-driven and does not constitute investment advice. Please make decisions based on your own risk tolerance.
```

---

## Decision Logic

| Condition | Assessment |
|-----------|------------|
| RSI > 70 | Flag "Overbought — elevated short-term pullback risk" |
| RSI < 30 | Flag "Oversold — potential bounce" |
| 24h volume > 7d avg volume x 2 | Flag "Significant volume surge" |
| 24h volume < 7d avg volume x 0.5 | Flag "Notable volume decline" |
| funding_rate > 0.05% | Flag "High funding rate — long crowding" |
| funding_rate < -0.05% | Flag "Negative funding rate — short crowding" |
| fear_greed > 75 | Flag "Extreme Greed — exercise caution" |
| fear_greed < 25 | Flag "Extreme Fear — potential opportunity" |
| Token unlock in next 30 days > 5% of circulating supply | Flag "Large upcoming token unlock — potential sell pressure" |
| Any Tool returns empty/error | Skip that section; note "Data unavailable" in the report |

---

## Error Handling

| Error Type | Handling |
|------------|----------|
| Coin does not exist | Prompt user to verify the coin name; suggest using `info_coin_search_coins` |
| A single Tool times out | Skip that dimension; note "This dimension is temporarily unavailable" |
| All Tools fail | Return error message; suggest the user try again later |
| User inputs multiple coins | Route to `gate-info-coincompare` |
| User inputs an address instead of a coin | Route to `gate-info-addresstracker` |

---

## Cross-Skill Routing

| User Follow-up Intent | Route To |
|-----------------------|----------|
| "Give me a technical analysis" | `gate-info-trendanalysis` |
| "Any recent news?" | `gate-news-briefing` |
| "What about on-chain data?" | `gate-info-tokenonchain` |
| "Is this coin safe?" | `gate-info-riskcheck` |
| "Compare XX and YY" | `gate-info-coincompare` |
| "Why is it pumping/dumping?" | `gate-news-eventexplain` |

---

## Safety Rules

1. **No investment advice**: The overall assessment is data-driven analysis and must include a "not investment advice" disclaimer
2. **No price predictions**: Do not output specific target prices or up/down predictions
3. **Data transparency**: Label data source and update time for each dimension
4. **Flag missing data**: When any dimension has no data, explicitly inform the user — never fabricate data
