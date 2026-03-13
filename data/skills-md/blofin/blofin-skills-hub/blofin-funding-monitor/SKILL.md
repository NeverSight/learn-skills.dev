---
name: blofin-funding-monitor
description: "Monitor BloFin perpetual swap funding rates, analyze market sentiment through funding data, and track funding rate trends across instruments."
version: 1.0.0
license: Apache-2.0
metadata:
  openclaw:
    emoji: "📡"
    requires:
      bins:
        - node
auto_activate:
  - "funding rate"
  - "funding monitor"
  - "market sentiment"
  - "funding payment"
  - "funding history"
---

# BloFin Funding Rate Monitor

Monitor perpetual swap funding rates, analyze market sentiment, and track funding trends across BloFin instruments.

## Background

### What Are Funding Rates?

Perpetual swap contracts use **funding rates** to keep the contract price aligned with the spot price:
- **Positive funding rate**: Longs pay shorts — indicates bullish sentiment / overleveraged longs
- **Negative funding rate**: Shorts pay longs — indicates bearish sentiment / overleveraged shorts
- Funding is exchanged between traders every 8 hours (00:00, 08:00, 16:00 UTC)
- The rate reflects current market positioning and sentiment

### Why Monitor Funding Rates?

- **Market sentiment indicator**: Funding rates reveal whether the market is leaning long or short
- **Cost awareness**: Holding positions costs or earns funding — understanding rates helps plan trades
- **Volatility signal**: Extreme funding rates often precede significant price moves
- **Position management**: Knowing funding direction helps decide when to enter, exit, or hold

---

## Workflows

### 1. Funding Rate Overview

Scan all instruments for current funding rates:

1. **Get all tickers** via `get_tickers` (no instId filter)
2. **Get funding rates** via `get_funding_rate` (no instId filter) for all instruments
3. **Sort by absolute funding rate** to highlight notable rates
4. **Present a ranked table:**

```
Funding Rate Overview (sorted by |rate|)
=========================================
| Instrument | Funding Rate | Annualized | Direction    | Volume 24h |
|------------|-------------|------------|--------------|------------|
| XXX-USDT   | +0.0321%    | ~117%      | Longs pay    | $XXM       |
| YYY-USDT   | -0.0156%    | ~57%       | Shorts pay   | $XXM       |
| BTC-USDT   | +0.0100%    | ~37%       | Longs pay    | $XXM       |
| ...        | ...         | ...        | ...          | ...        |

Summary: XX/XX instruments have positive rates (bullish bias)
⚠️ Instruments with |rate| > 0.03% may indicate overleveraged positioning.
```

**Annualized rate formula:** `fundingRate * 3 * 365 * 100` (3 payments per day)

**Example prompts:**
- "Show me current funding rates across all instruments"
- "Which coins have the highest funding rates?"
- "What's the overall market sentiment based on funding?"

---

### 2. Single Instrument Funding Analysis

Deep-dive into one instrument's funding dynamics:

1. **Get current funding rate** via `get_funding_rate`
2. **Get funding rate history** via `get_funding_rate_history` (last 100 data points)
3. **Get current price and volume** via `get_tickers`
4. **Analyze:**
   - Current rate and direction
   - Average rate over recent history
   - Rate trend (increasing / decreasing / stable)
   - Consistency (how often positive vs negative)
   - Market sentiment interpretation

**Present:**

```
BTC-USDT Funding Rate Analysis
================================
Current Rate: +0.0100% (longs pay shorts)
Next Payment: ~[estimate based on 8h intervals]

Historical (last 7 days):
- Average: +0.0085%
- Max: +0.0321%
- Min: -0.0012%
- Positive: 95% of periods

Sentiment: Persistently positive — market is net long / bullish
Trend: Stable — no significant shifts in positioning
Note: Elevated rates may indicate crowded long positioning.
```

**Example prompts:**
- "Analyze BTC funding rate history"
- "Is ETH funding rate trending up or down?"
- "What does the BTC funding rate tell us about market sentiment?"

---

### 3. Funding Cost Calculator

Help traders understand the cost of holding positions:

1. **Get funding rate** for the target instrument
2. **Get current price** via `get_tickers`
3. **Get instrument specs** via `get_instruments` (contract value, min size)
4. **Calculate holding costs:**

```
Funding Cost Estimate
======================
Instrument: BTC-USDT
Your Position: Long, 100 contracts
Notional Value: $X,XXX
Current Funding Rate: +0.01%

Cost per funding period: $X.XX (you pay, since rate is positive and you're long)
Daily cost (3 periods): $X.XX
Weekly cost: $XX.XX
Monthly cost (est.): $XXX.XX

💡 Tip: Factor funding costs into your trade plan, especially for longer holds.
```

**Example prompts:**
- "How much will it cost me to hold my BTC long?"
- "Calculate funding costs for 50 ETH-USDT contracts"
- "What's the funding cost of my current position?"

---

### 4. Funding Rate Alerts

Monitor funding rates and flag significant changes:

When asked to monitor, periodically check:

1. **Extreme rates**: |rate| > 0.03% (annualized > ~110%) — may signal overleveraged market
2. **Rate flip**: Rate changes from positive to negative or vice versa — market sentiment shift
3. **Sustained high rates**: Consistently elevated rates over multiple periods — crowded positioning

**Example prompts:**
- "Alert me if any funding rate exceeds 0.05%"
- "Monitor BTC funding rate changes"
- "Watch for funding rate flips"

---

### 5. Market Sentiment Dashboard

Aggregate funding data for a broad market view:

1. **Get all funding rates** via `get_funding_rate`
2. **Classify instruments** by funding direction and magnitude
3. **Present sentiment summary:**

```
Market Sentiment (via Funding Rates)
=====================================
Total instruments: XX
Positive (bullish bias): XX (XX%)
Negative (bearish bias): XX (XX%)

Average rate: +0.00XX%
Median rate: +0.00XX%

Extreme bullish (>0.03%): [list]
Extreme bearish (<-0.03%): [list]

Overall: Market is leaning [bullish/bearish/neutral]
```

**Example prompts:**
- "What's the overall market sentiment?"
- "Are most funding rates positive or negative right now?"
- "Give me a market sentiment overview"

## Guidelines

1. **Funding rates reflect sentiment, not predictions** — they show current positioning, not future price direction
2. **Extreme rates signal caution** — very high/low rates often precede volatile moves or liquidation cascades
3. **Volume context matters** — low-volume instruments may have unreliable or exaggerated funding rates
4. **Annualized rates are estimates** — actual rates vary every 8 hours
5. **Always present rates with context** — show alongside price, volume, and trend for meaningful analysis
6. **Inform, don't prescribe** — present data and analysis; let the user make their own trading decisions
