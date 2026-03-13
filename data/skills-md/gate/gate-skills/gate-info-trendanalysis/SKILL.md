---
name: gate-info-trendanalysis
version: "2026.3.12-1"
updated: "2026-03-12"
description: "Trend and technical analysis. Use this skill whenever the user asks for technical or trend analysis of one coin. Trigger phrases include: technical analysis, K-line, RSI, MACD, trend, support, resistance. MCP tools: info_markettrend_get_kline, info_markettrend_get_indicator_history, info_markettrend_get_technical_analysis, info_marketsnapshot_get_market_snapshot."
---

# gate-info-trendanalysis

> A technicals-focused Skill. The user inputs a coin name + technical analysis intent; the system calls 4 Tools (K-line data, indicator history, multi-timeframe signals, real-time market snapshot) in parallel, then the LLM aggregates into a multi-dimensional technical analysis report.

**Trigger Scenarios**: User explicitly mentions technical analysis, K-line, indicators, trend, support/resistance, or similar keywords.

---

## Routing Rules

| User Intent | Keywords | Action |
|-------------|----------|--------|
| Technical analysis | "technical analysis" "K-line" "RSI" "MACD" "Bollinger" "moving average" "support" "resistance" "trend" | Execute this Skill's full workflow |
| Comprehensive analysis (incl. fundamentals) | "analyze BTC for me" | Route to `gate-info-coinanalysis` |
| Price only | "what's BTC price" | Call `info_marketsnapshot_get_market_snapshot` directly |
| Raw K-line data only | "BTC 30-day K-line" | Call `info_markettrend_get_kline` directly — no need for full Skill |

---

## Execution Workflow

### Step 1: Intent Recognition & Parameter Extraction

Extract from user input:
- `symbol`: Coin ticker (BTC, ETH, SOL, etc.)
- `timeframe`: Analysis timeframe (e.g., "daily" → 1d, "4-hour" → 4h; default: 1d)
- `indicators`: Specific indicators the user cares about (e.g., "RSI", "MACD"; default: all)
- `period`: K-line lookback days (default: 90)

### Step 2: Call 4 MCP Tools in Parallel

| Step | MCP Tool | Parameters | Retrieved Data | Parallel |
|------|----------|------------|----------------|----------|
| 1a | `info_markettrend_get_kline` | `symbol={symbol}, timeframe={timeframe}, limit=90` | K-line OHLCV data (default 90 bars) | Yes |
| 1b | `info_markettrend_get_indicator_history` | `symbol={symbol}, indicators=["rsi","macd","bollinger","ma"], timeframe={timeframe}` | Technical indicator history | Yes |
| 1c | `info_markettrend_get_technical_analysis` | `symbol={symbol}` | Multi-timeframe composite signals (1h/4h/1d/1w) | Yes |
| 1d | `info_marketsnapshot_get_market_snapshot` | `symbol={symbol}, timeframe="1d", source="spot"` | Real-time market snapshot (price, volume, OI, funding rate) | Yes |

> All 4 Tools are called in parallel.

### Step 3: LLM Analysis

The LLM performs technical analysis on the raw data, completing the following reasoning:
1. Identify trend from candlestick patterns (uptrend / downtrend / sideways channel)
2. Combine indicator history to assess current position (overbought / oversold / neutral)
3. Evaluate multi-timeframe signal alignment or divergence
4. Identify key support and resistance levels

### Step 4: Output Structured Report

---

## Report Template

```markdown
## {symbol} Technical Analysis Report

> Analysis time: {timestamp} | Primary timeframe: {timeframe}

### 1. Current Market Snapshot

| Metric | Value |
|--------|-------|
| Price | ${price} |
| 24h Change | {change_24h}% |
| 24h Volume | ${volume_24h} |
| 24h High | ${high_24h} |
| 24h Low | ${low_24h} |
| Open Interest | ${oi} (if available) |
| Funding Rate | {funding_rate}% (if available) |

### 2. Trend Assessment

**Overall Trend**: {Uptrend / Downtrend / Sideways / Trend Reversal}

{Trend analysis based on candlestick patterns and MA alignment:}
- MA7 / MA25 / MA99 alignment: {Bullish / Bearish / Tangled}
- Recent candlestick patterns: {Bullish Engulfing / Doji / Hammer / etc.} (if notable)
- Volume confirmation: {Rising volume + price up (healthy) / Declining volume + price up (weak momentum) / Rising volume + price down (accelerated selling)}

### 3. Technical Indicator Details

#### RSI (14)
| Timeframe | Value | Status |
|-----------|-------|--------|
| 1h | {rsi_1h} | {Overbought/Oversold/Neutral} |
| 4h | {rsi_4h} | {Overbought/Oversold/Neutral} |
| 1d | {rsi_1d} | {Overbought/Oversold/Neutral} |

{RSI divergence analysis: any bullish/bearish divergence present?}

#### MACD
| Timeframe | DIF | DEA | Histogram | Status |
|-----------|-----|-----|-----------|--------|
| 1h | {dif} | {dea} | {histogram} | {Golden Cross/Death Cross/Above Zero/Below Zero} |
| 4h | ... | ... | ... | ... |
| 1d | ... | ... | ... | ... |

#### Bollinger Bands (20, 2)
| Metric | Value |
|--------|-------|
| Upper Band | ${upper} |
| Middle Band | ${middle} |
| Lower Band | ${lower} |
| Bandwidth | {bandwidth}% |
| Current Position | {price relative to bands + percentile} |

{Narrowing bands → breakout imminent; price touching upper band → potential pullback to middle; touching lower band → potential bounce}

### 4. Key Price Levels

| Type | Price | Basis |
|------|-------|-------|
| Strong Resistance | ${resistance_1} | {Previous high / MA99 / Upper Bollinger / Round number} |
| Weak Resistance | ${resistance_2} | ... |
| Weak Support | ${support_1} | ... |
| Strong Support | ${support_2} | {Previous low / MA99 / Lower Bollinger / Volume profile cluster} |

### 5. Multi-Timeframe Signal Summary

| Timeframe | Composite Signal | Bullish Indicators | Bearish Indicators |
|-----------|-----------------|--------------------|--------------------|
| 1h | {Strong Buy/Buy/Neutral/Sell/Strong Sell} | {count} | {count} |
| 4h | ... | ... | ... |
| 1d | ... | ... | ... |
| 1w | ... | ... | ... |

**Signal Consistency**: {Are multi-timeframe signals aligned? e.g., "Short-term bearish but medium/long-term bullish — divergence present"}

### 6. Overall Technical Assessment

{LLM generates a comprehensive assessment:}
- Current trend strength evaluation
- Short-term (1-3 day) likely direction
- Medium-term (1-2 week) likely direction
- Key observation: a break above ${resistance_1} opens upside; a break below ${support_2} signals trend weakening

### Risk Warnings

{Data-driven risk alerts}

> Technical analysis is based on historical data and cannot predict future price movements. This does not constitute investment advice.
```

---

## Decision Logic

| Condition | Assessment |
|-----------|------------|
| RSI > 70 (multi-timeframe consistent) | "Multi-timeframe RSI overbought — high pullback probability" |
| RSI < 30 (multi-timeframe consistent) | "Multi-timeframe RSI oversold — high bounce probability" |
| MACD daily golden cross + 4h golden cross | "MACD multi-timeframe golden cross confirmed — bullish signal" |
| MACD daily death cross + 4h death cross | "MACD multi-timeframe death cross confirmed — bearish signal" |
| Bollinger bandwidth < 5% | "Extreme Bollinger squeeze — breakout imminent" |
| Price breaks above upper Bollinger | "Short-term overextended — potential pullback to middle band" |
| MA7 > MA25 > MA99 | "Bullish MA alignment" |
| MA7 < MA25 < MA99 | "Bearish MA alignment" |
| 3 consecutive days of rising volume + price up | "Rising volume rally — healthy trend" |
| Declining volume + price up | "Low-volume rally — watch for weakening momentum" |
| Short-term vs medium/long-term signals diverge | Flag "Bull/bear divergence — awaiting directional resolution" |
| funding_rate > 0.1% | "Extreme long crowding in futures — risk of long squeeze" |
| Any Tool returns empty/error | Skip that indicator analysis; note "Data unavailable" |

---

## Error Handling

| Error Type | Handling |
|------------|----------|
| Coin does not exist | Prompt user to verify the coin name |
| info_markettrend_get_kline insufficient data | Reduce lookback period or switch to larger timeframe; note limited data |
| info_markettrend_get_technical_analysis fails | Derive signals from K-line and indicator history manually; label "Composite signal manually derived" |
| info_markettrend_get_indicator_history partial indicators missing | Display available indicators; note missing ones as "temporarily unavailable" |
| All Tools fail | Return error message; suggest the user try again later |

---

## Cross-Skill Routing

| User Follow-up Intent | Route To |
|-----------------------|----------|
| "What about fundamentals?" / "Full analysis" | `gate-info-coinanalysis` |
| "Why is it pumping/dumping?" | `gate-news-eventexplain` |
| "On-chain chip analysis" | `gate-info-tokenonchain` |
| "Compare XX and YY" | `gate-info-coincompare` |
| "Recent news?" | `gate-news-briefing` |

---

## Safety Rules

1. **No trading advice**: Do not output "recommend going long/short" or "buy at XX"
2. **No specific price predictions**: Do not output "will rise to XX tomorrow" or "target price XX"
3. **Acknowledge limitations**: Clearly state that technical analysis is based on historical data and may fail
4. **Data transparency**: Label K-line data range and indicator parameter settings
5. **Flag missing data**: When indicators are unavailable, explicitly state it — never fabricate values
