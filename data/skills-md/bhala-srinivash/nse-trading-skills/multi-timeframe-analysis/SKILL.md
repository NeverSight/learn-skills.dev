---
name: multi-timeframe-analysis
description: |
  Multi-timeframe analysis using the 3-screen method for NSE/BSE equities. Higher timeframe
  sets bias, primary timeframe identifies setup, lower timeframe times the entry.
  Includes confluence scoring system.

  Use when the user asks: "what's the weekly trend", "daily vs weekly", "multi-timeframe check",
  "higher timeframe analysis", "3-screen analysis", "trend on different timeframes", "weekly bias
  for [stock]", or any question about analyzing a stock across multiple timeframes.
---

# Multi-Timeframe Analysis

Higher timeframes set the direction. Lower timeframes refine the entry. Never trade against the higher timeframe trend unless you have very strong reasons.

## The 3-Screen Method

| Screen | Timeframe | Purpose | What to Look For |
|--------|-----------|---------|-----------------|
| Screen 1 | **Weekly** | Trend bias | Primary trend, major S/R, 200-week MA |
| Screen 2 | **Daily** | Setup | Pattern formation, indicator signals, entry zone |
| Screen 3 | **4H / 1H** | Entry timing | Precise entry price, tight stop placement |

### How to use it:
1. **Weekly decides direction** — only take trades in the weekly trend's direction
2. **Daily identifies the setup** — pullback to support in uptrend, rally to resistance in downtrend
3. **Hourly/4H times the entry** — wait for the lower TF to confirm reversal in your direction

## Prerequisites

No dependencies required. Framework applies to any timeframe data. Enhanced with Groww MCP (multi-interval candles) or yfinance (`pip install yfinance`) for weekly/monthly history.

## Fetching Multi-TF Data

When data tools are available:
```
Weekly:  fetch_historical_candle_data with interval=1w
Daily:   fetch_historical_candle_data with interval=1d
Hourly:  fetch_historical_candle_data with interval=1h (limited to ~30 days)
```

For weekly indicators via yfinance: `yf.download("SYMBOL.NS", period="2y", interval="1wk")`

## Screen 1: Weekly Analysis

Check these on the weekly chart:
- **Trend**: Series of higher highs/lows (up) or lower highs/lows (down)?
- **Position vs MAs**: Price relative to 20W and 50W SMA
- **RSI(14) weekly**: Above 50 = bullish bias, below 50 = bearish bias
- **Major S/R**: Horizontal levels with multiple weekly touches
- **Volume trend**: Rising into the trend direction = healthy

**Weekly verdict:** Bullish / Bearish / Neutral — this sets your trading bias.

## Screen 2: Daily Analysis

With the weekly bias established:
- **Look for setups that align**: Pullbacks to buy in uptrend, rallies to sell in downtrend
- **Pattern identification**: Flags, wedges, double bottoms/tops, breakouts
- **Indicator signals**: RSI, MACD, Bollinger on daily
- **Volume**: Confirmation of the setup (declining volume on pullback = healthy)

**Daily verdict:** Setup present / No setup / Counter-trend setup (risky)

## Screen 3: Entry Timeframe (4H / 1H)

Once weekly bias + daily setup align:
- **Wait for lower TF confirmation**: A candlestick reversal pattern, RSI bounce, or MACD cross
- **Place entry**: At the confirmation signal
- **Set stop**: Based on lower TF structure (tighter = better R:R)
- **Target**: From daily/weekly levels

## Confluence Scoring

Award 1 point for each alignment. This keeps you honest about setup quality.

| Factor | Point |
|--------|-------|
| Weekly trend agrees with trade direction | +1 |
| Daily shows valid setup pattern | +1 |
| RSI supports on daily timeframe | +1 |
| MACD supports on daily timeframe | +1 |
| Key S/R level provides clear stop or target | +1 |
| Volume confirms the move | +1 |

| Score | Action |
|-------|--------|
| 5-6 | Strong setup — full position size |
| 4 | Good setup — full position size |
| 3 | Marginal — half position size |
| 2 | Weak — skip or paper trade only |
| 0-1 | No setup — do not trade |

## Common Mistakes

- **Trading against the weekly trend** hoping for a reversal — the weekly trend wins most of the time
- **Using only one timeframe** — you miss context and enter with poor timing
- **Forcing alignment** — if timeframes disagree, the answer is "no trade" not "trade anyway"
