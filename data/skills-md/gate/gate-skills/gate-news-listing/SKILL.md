---
name: gate-news-listing
version: "2026.3.12-1"
updated: "2026-03-12"
description: "Exchange listing tracker. Use this skill whenever the user asks about exchange listing, delisting, or maintenance announcements. Trigger phrases include: any new coins listed recently, what did Binance list, new listings, delisted. MCP tools: news_feed_get_exchange_announcements, info_coin_get_coin_info, info_marketsnapshot_get_market_snapshot."
---

# gate-news-listing

> Listing radar Skill. The user queries exchange listing/delisting/maintenance announcements, the system first calls the exchange announcements Tool, then supplements high-interest coins with fundamentals and market data. The LLM aggregates everything into a structured exchange activity report.

**Trigger Scenarios**: User mentions an exchange name + listing/delisting keywords, or asks "any new coins listed recently" or "any new projects".

---

## Routing Rules

| User Intent | Keywords/Pattern | Action |
|-------------|-----------------|--------|
| Query exchange listings | "what did Binance list" "any new coins on Gate" "recent new listings" | Execute this Skill's full workflow |
| Query specific coin listing info | "where is SOL listed" "when was PEPE listed on Binance" | Execute this Skill (filter by coin) |
| Query delistings/maintenance | "any coins getting delisted" "exchange maintenance announcements" | Execute this Skill (filter by announcement type) |
| News briefing | "what happened recently" | Route to `gate-news-briefing` |
| Coin analysis | "how is this new coin doing" | Route to `gate-info-coinanalysis` |
| Contract security check | "is this new coin safe" | Route to `gate-info-riskcheck` |

---

## Execution Workflow

### Step 1: Intent Recognition & Parameter Extraction

Extract from user input:
- `exchange` (optional): Exchange name (e.g., Binance, Gate, OKX, Bybit, Coinbase)
- `coin` (optional): Specific coin symbol
- `announcement_type` (optional): Announcement type (listing / delisting / maintenance)
- `limit`: Number of results, default 10

**Default Logic**:
- If no exchange specified, query all exchanges
- If no announcement type specified, default to listing
- If user mentions "delisting" or "maintenance", set the corresponding `announcement_type`

### Step 2: Call Exchange Announcements Tool

| Step | MCP Tool | Parameters | Retrieved Data | Parallel |
|------|----------|------------|----------------|----------|
| 1 | `news_feed_get_exchange_announcements` | `exchange={exchange}, coin={coin}, announcement_type={type}, limit={limit}` | Announcement list: exchange, coin, type, time, details | — |

### Step 3: Supplement Key Coins with Data (Parallel)

From Step 2 results, extract the top 3-5 newly listed coins and supplement in parallel:

| Step | MCP Tool | Parameters | Retrieved Data | Parallel |
|------|----------|------------|----------------|----------|
| 2a | `info_coin_get_coin_info` | `query={coin_symbol}` | Project fundamentals: sector, funding, description | Yes |
| 2b | `info_marketsnapshot_get_market_snapshot` | `symbol={coin_symbol}, timeframe="1d", source="spot"` | Market data: price, change, market cap, volume | Yes |

> Only supplement data for listing-type announcements. Delisting/maintenance announcements do not need market data.

### Step 4: LLM Aggregation — Generate Report

Pass announcement data and supplementary info to the LLM to generate the exchange activity report using the template below.

---

## Report Template

```markdown
## Exchange Activity Report

> Data range: {start_time} — {end_time} | Exchange: {exchange / "All"} | Type: {type / "Listings"}

### 1. Latest Listing Announcements

| # | Exchange | Coin | Type | Listing Time | Trading Pairs |
|---|---------|------|------|-------------|---------------|
| 1 | {exchange_1} | {coin_1} | Listed | {time_1} | {pairs_1} |
| 2 | {exchange_2} | {coin_2} | Listed | {time_2} | {pairs_2} |
| ... | ... | ... | ... | ... | ... |

### 2. Featured New Coins

{Quick analysis of the top 3-5 newly listed coins}

#### {coin_1}

| Metric | Value |
|--------|-------|
| Project Description | {description} |
| Sector | {category} |
| Funding Background | {funding} |
| Current Price | ${price} |
| Post-Listing Change | {change}% |
| 24h Volume | ${volume} |
| Market Cap | ${market_cap} |

{LLM one-liner: highlights and risks to watch for this project}

#### {coin_2}
...

### 3. Delisting / Maintenance Notices (if any)

| # | Exchange | Coin | Type | Effective Date | Notes |
|---|---------|------|------|---------------|-------|
| 1 | ... | ... | Delisted | ... | ... |

### 4. Activity Summary

{LLM generates a 2-3 sentence summary based on all announcement data:}
- Most active exchange for new listings recently
- Trending listing sectors (Meme / AI / DePIN / L2, etc.)
- Notable projects and why they stand out
- Delisting/maintenance reminders (if any)

### ⚠️ Risk Warnings

- Newly listed coins experience extreme volatility — the price discovery phase carries very high risk
- Some newly listed tokens may have insufficient liquidity — watch for slippage on large trades
- It is recommended to use the "Risk Assessment" feature to check contract security before trading

> The above information is compiled from public announcements and on-chain data and does not constitute investment advice.
```

---

## Decision Logic

| Condition | Assessment |
|-----------|------------|
| New coin 24h change > +100% post-listing | Flag "Abnormal surge — chasing the pump carries extreme risk" |
| New coin 24h change < -50% post-listing | Flag "Listed at a loss — buying now requires caution" |
| 24h volume < $100K | Flag "Extremely low volume — severe liquidity shortage" |
| Multiple exchanges list the same coin simultaneously | Flag "Multi-exchange simultaneous listing — high market attention" |
| Announcement type is delisting | Flag "Upcoming delisting — please handle positions promptly" |
| Announcement type is maintenance | Flag "Deposit/withdrawal maintenance in progress — transfers temporarily unavailable" |
| Coin fundamentals show no funding info | Flag "No funding information found — additional due diligence required" |
| Announcements return empty | Inform "No relevant announcements for this time period" |
| A supplementary Tool returns empty/error | Skip detailed analysis for that coin; mark "Data unavailable" |

---

## Error Handling

| Error Type | Handling |
|------------|----------|
| Misspelled exchange name | Attempt fuzzy match, e.g., "Binance" → Binance, "OKX" → OKX |
| No matching announcements | Inform "No {type} announcements for this exchange/time period." Suggest broadening the time range or switching exchanges |
| news_feed_get_exchange_announcements timeout | Return error message; suggest trying again later |
| Coin supplementary info (coin_info / market_snapshot) fails | Skip detailed analysis for that coin; display announcement info only |
| User asks when a coin will be listed (future) | Inform "Currently only published announcements can be queried — future listing plans cannot be predicted" |
| Too many results | Default to showing the most recent 10; inform user they can specify an exchange or time range to narrow results |

---

## Cross-Skill Routing

| User Follow-up Intent | Route To |
|-----------------------|----------|
| "Analyze this new coin for me" | `gate-info-coinanalysis` |
| "Is this new coin's contract safe?" | `gate-info-riskcheck` |
| "Compare a few of these new listings" | `gate-info-coincompare` |
| "Why did this coin get listed on the exchange?" | `gate-news-eventexplain` |
| "How is the overall market right now?" | `gate-info-marketoverview` |
| "On-chain data for this new coin" | `gate-info-tokenonchain` |

---

## Available Tools & Degradation Notes

| PRD-Defined Tool | Actually Available Tool | Status | Degradation Strategy |
|-----------------|----------------------|--------|---------------------|
| `news_feed_get_exchange_announcements` | `news_feed_get_exchange_announcements` | ✅ Ready | — |
| `info_coin_get_coin_rankings` | — | ❌ Not ready | Cannot list recent listings by ranking — extract coins from announcements and query individually instead |
| `info_coin_get_coin_info` | `info_coin_get_coin_info` | ✅ Ready | — |
| `info_marketsnapshot_get_market_snapshot` | `info_marketsnapshot_get_market_snapshot` | ✅ Ready | — |

---

## Safety Rules

1. **No investment advice**: Announcement analysis is based on public information and must include a "not investment advice" disclaimer
2. **No listing predictions**: Do not predict whether a coin will be listed on a specific exchange
3. **New coin risk reminder**: All reports on newly listed coins must include the "extreme volatility during initial listing" risk warning
4. **Data transparency**: Label announcement source and update time
5. **Flag missing data**: When any dimension has no data, explicitly inform the user — never fabricate data
6. **Delisting urgency**: For delisting announcements, prominently remind users to manage their positions
