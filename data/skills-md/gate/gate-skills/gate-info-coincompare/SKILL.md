---
name: gate-info-coincompare
version: "2026.3.12-1"
updated: "2026-03-12"
description: "Coin comparison. Use this skill whenever the user asks to compare two or more coins. Trigger phrases include: compare, versus, vs, which is better, difference. MCP tools: info_marketsnapshot_get_market_snapshot, info_coin_get_coin_info per coin (or batch/search when available)."
---

# gate-info-coincompare

> Side-by-side comparison Skill. The user inputs 2-5 coins, the system calls market snapshot + fundamentals tools for each coin in parallel, and the LLM aggregates multi-dimensional data into a comparison table with overall analysis.

**Trigger Scenarios**: User mentions two or more coins + keywords like compare, versus, vs, which is better, difference, head-to-head.

---

## Routing Rules

| User Intent | Keywords/Pattern | Action |
|-------------|-----------------|--------|
| Multi-coin comparison | "compare BTC and ETH" "SOL vs AVAX" "Layer2 coin comparison" | Execute this Skill's full workflow |
| Single coin analysis | "analyze SOL for me" | Route to `gate-info-coinanalysis` |
| Price only | "what's BTC price" | Call `info_marketsnapshot_get_market_snapshot` directly |
| Sector overview | "how is the DeFi sector doing" | Route to `gate-info-marketoverview` |
| Ranking list | "top 10 coins by market cap" | `info_coin_get_coin_rankings` not yet available — prompt user to list specific coins to compare |

---

## Execution Workflow

### Step 1: Intent Recognition & Parameter Extraction

Extract from user input:
- `symbols[]`: List of coins (2-5), e.g., [BTC, ETH, SOL]
- If the user mentions project names (e.g., Solana, Avalanche), map to ticker symbols
- If the user mentions a sector without specific coins (e.g., "which Layer2 coins are good"), prompt them to list 2-5 specific coins

**Limits**: Minimum 2, maximum 5. If more than 5, prompt user to narrow the scope. If only 1 coin, ask for at least one more or route to `gate-info-coinanalysis`.

### Step 2: Call 2 MCP Tools per Coin in Parallel

For each `symbol` in the list, execute in parallel:

| Step | MCP Tool | Parameters | Retrieved Data | Parallel |
|------|----------|------------|----------------|----------|
| 1a | `info_marketsnapshot_get_market_snapshot` | `symbol={symbol}, timeframe="1d", source="spot"` | Market data: real-time price, K-line summary, market cap, FDV, Fear & Greed Index | Yes |
| 1b | `info_coin_get_coin_info` | `query={symbol}` | Fundamentals: project info, sector, funding, tokenomics | Yes |

> For 3 coins, this results in 6 parallel Tool calls with no dependencies. When `info_marketsnapshot_batch_market_snapshot` and `info_coin_search_coins` are available, prefer them; otherwise use per-coin calls above.

### Step 3 (Optional): Technical Comparison

If the user explicitly requests technical comparison, or the number of coins is 3 or fewer, optionally call in parallel:

| Step | MCP Tool | Parameters | Retrieved Data | Parallel |
|------|----------|------------|----------------|----------|
| 2 | `info_markettrend_get_technical_analysis` | `symbol={symbol}` | Technical signals: RSI, MACD, MA alignment, support/resistance | Yes |

### Step 4: LLM Cross-Comparison Report Generation

Group all Tool responses by coin, and the LLM generates a side-by-side comparison report using the template below.

---

## Report Template

```markdown
## Coin Comparison: {symbol_1} vs {symbol_2} [vs {symbol_3} ...]

### 1. Key Metrics Comparison

| Metric | {symbol_1} | {symbol_2} | {symbol_3} |
|--------|-----------|-----------|-----------|
| Price | ${price_1} | ${price_2} | ${price_3} |
| 24h Change | {change_24h_1}% | {change_24h_2}% | {change_24h_3}% |
| 7d Change | {change_7d_1}% | {change_7d_2}% | {change_7d_3}% |
| Market Cap | ${mcap_1} | ${mcap_2} | ${mcap_3} |
| Market Cap Rank | #{rank_1} | #{rank_2} | #{rank_3} |
| FDV | ${fdv_1} | ${fdv_2} | ${fdv_3} |
| 24h Volume | ${vol_1} | ${vol_2} | ${vol_3} |
| Fear & Greed Index | {fg_1} | {fg_2} | {fg_3} |

### 2. Fundamentals Comparison

| Dimension | {symbol_1} | {symbol_2} | {symbol_3} |
|-----------|-----------|-----------|-----------|
| Sector | {category_1} | {category_2} | {category_3} |
| Total Funding | ${funding_1} | ${funding_2} | ${funding_3} |
| Key Investors | {investors_1} | {investors_2} | {investors_3} |
| Circulating Ratio | {circ_ratio_1}% | {circ_ratio_2}% | {circ_ratio_3}% |
| Upcoming Unlocks | {unlock_1} | {unlock_2} | {unlock_3} |

### 3. Technical Comparison (if available)

| Dimension | {symbol_1} | {symbol_2} | {symbol_3} |
|-----------|-----------|-----------|-----------|
| Overall Signal | {signal_1} | {signal_2} | {signal_3} |
| RSI(14) | {rsi_1} | {rsi_2} | {rsi_3} |
| MACD | {macd_1} | {macd_2} | {macd_3} |
| MA Alignment | {ma_1} | {ma_2} | {ma_3} |

### 4. Comparative Summary

{LLM generates a 3-5 sentence cross-comparison analysis covering:}
- Strengths and weaknesses of each coin across dimensions
- Which coin has stronger recent performance and which is weakening
- Whether fundamentals and market data align
- Differentiated risks to watch

### 5. Dimension-by-Dimension Winners

| Dimension | Best Performer | Weakest Performer | Notes |
|-----------|---------------|-------------------|-------|
| Short-term Gains | {best_1} | {worst_1} | ... |
| Market Cap / FDV Ratio | {best_2} | {worst_2} | ... |
| Funding Background | {best_3} | {worst_3} | ... |
| Technical Signals | {best_4} | {worst_4} | ... |

### ⚠️ Risk Warnings

{Risk differentials identified in the comparison, e.g.:}
- {symbol_x} has only {x}% circulating supply — significantly higher unlock pressure than peers
- {symbol_y} RSI is in overbought territory — higher short-term pullback risk than {symbol_z}
- {symbol_w} 24h volume is disproportionately low relative to market cap — liquidity disadvantage

> The above analysis is a data-driven side-by-side comparison and does not constitute investment advice. Please make decisions based on your own risk tolerance.
```

---

## Decision Logic

| Condition | Assessment |
|-----------|------------|
| 24h change difference > 10% between coins | Flag "Significant short-term performance divergence" |
| FDV/Market Cap ratio for one coin > 2x others | Flag "Relatively elevated FDV — higher unlock risk" |
| Circulating ratio < 30% | Flag "Low circulating ratio — future sell pressure risk" |
| 24h volume / market cap < 1% | Flag "Low liquidity — slippage risk for large trades" |
| RSI difference > 30 (one overbought, another oversold) | Flag "Technicals in opposite states — evaluate separately" |
| Any Tool returns empty/error | Mark corresponding column as "Data unavailable"; display remaining coins normally |
| Two coins are from entirely different sectors | Remind user: "Cross-sector comparison is for reference only — core value drivers differ significantly" |

---

## Error Handling

| Error Type | Handling |
|------------|----------|
| A coin does not exist | Note the name may be incorrect; exclude it and continue comparing the rest |
| Only 1 coin provided | Route to `gate-info-coinanalysis` (single coin analysis) |
| More than 5 coins provided | Prompt user to narrow down to 5 or fewer, or suggest comparing in batches |
| A coin's Tool times out | Skip that coin's dimension; mark as "Temporarily unavailable" in the table |
| All Tools fail | Return error message; suggest the user try again later |
| User inputs an address | Route to `gate-info-addresstracker` |

---

## Cross-Skill Routing

| User Follow-up Intent | Route To |
|-----------------------|----------|
| "Give me a deep dive on SOL" | `gate-info-coinanalysis` |
| "Show me SOL technicals in detail" | `gate-info-trendanalysis` |
| "Any recent news for these coins?" | `gate-news-briefing` |
| "Is SOL's contract safe?" | `gate-info-riskcheck` |
| "Why did ETH pump but SOL didn't?" | `gate-news-eventexplain` |
| "How about on-chain data comparison?" | `gate-info-tokenonchain` |

---

## Available Tools & Degradation Notes

| PRD-Defined Tool | Actually Available Tool | Status | Degradation Strategy |
|-----------------|-------------------------|--------|----------------------|
| `info_marketsnapshot_batch_market_snapshot` | `info_marketsnapshot_get_market_snapshot` | Degraded | Call `get_market_snapshot` per coin in parallel — no speed impact |
| `info_coin_search_coins` | `info_coin_get_coin_info` | Degraded | Use `get_coin_info` with symbol query as substitute |
| `info_markettrend_get_technical_analysis` | `info_markettrend_get_technical_analysis` | ✅ Ready | — |

---

## Safety Rules

1. **No investment advice**: Comparative analysis is data-driven and must include a "not investment advice" disclaimer
2. **No ranking recommendations**: Do not output conclusions like "buy A instead of B" — only present data differences
3. **No price predictions**: Do not output specific target prices or up/down predictions
4. **Data transparency**: Label data source and update time for each dimension
5. **Flag missing data**: When any dimension has no data, explicitly mark "Data unavailable" — never fabricate data
6. **Cross-sector reminder**: When compared coins belong to different sectors, remind the user of fundamental logic differences
