---
name: rsi-divergence
description: |
  RSI divergence identification and trading for NSE/BSE equities. Covers regular divergence
  (reversal signals) and hidden divergence (continuation signals) with confirmation rules.

  Use when the user asks: "RSI divergence on [stock]", "is there divergence", "bearish/bullish
  divergence", "momentum divergence", "RSI showing weakness", "hidden divergence", or any
  question about price vs RSI momentum divergences on Indian equities.
---

# RSI Divergence

Divergences signal that momentum is fading — price is moving one way but the engine (RSI) is losing steam. They're early warnings, not guarantees.

## Prerequisites

No dependencies required. Describe price and RSI patterns verbally and Claude identifies divergences. Enhanced with Groww MCP (RSI values, candles) or yfinance (`pip install yfinance`).

## Data Needed

1. **Daily candles**: `fetch_historical_candle_data` (last 90-120 days) or user-provided
2. **RSI(14) values**: `get_historical_technical_indicators` from Groww
3. For manual calculation via yfinance if needed:
   ```python
   import yfinance as yf
   data = yf.download("SYMBOL.NS", period="6mo")
   # Calculate RSI from close prices
   ```

## Regular Divergence (Reversal Signal)

Regular divergence suggests the current trend may be exhausting.

| Type | Price Makes | RSI Makes | Meaning |
|------|-----------|-----------|---------|
| **Bullish** | Lower low | Higher low | Selling pressure fading — potential bottom |
| **Bearish** | Higher high | Lower high | Buying pressure fading — potential top |

### How to Identify
1. Find the last 2-3 swing lows (for bullish) or swing highs (for bearish) on the price chart
2. Mark the corresponding RSI values at those same candles
3. If price makes a new extreme but RSI doesn't — that's divergence

### Strength Grading
| Signal | Strength |
|--------|----------|
| 2-point divergence (2 swings) | Standard |
| 3-point divergence (3 swings) | Strong |
| Divergence + oversold/overbought RSI | Stronger |
| Divergence + volume decline | Strongest |

## Hidden Divergence (Continuation Signal)

Hidden divergence suggests the existing trend will continue after a pullback.

| Type | Price Makes | RSI Makes | Meaning |
|------|-----------|-----------|---------|
| **Bullish** | Higher low | Lower low | Uptrend healthy — pullback is a buying opportunity |
| **Bearish** | Lower high | Higher high | Downtrend healthy — rally is a selling opportunity |

Hidden divergence is often overlooked but very powerful in trending markets.

## Trading Divergences

### Entry Strategy
1. **Identify the divergence** on daily chart
2. **Wait for confirmation** — do NOT enter on divergence alone
   - Price breaks above the minor trendline connecting the swing points
   - RSI crosses above 30 (bullish) or below 70 (bearish)
   - A bullish/bearish engulfing candle at the divergence point
3. **Enter** on the close of the confirmation candle
4. **Stop-loss**: Below the divergence low (bullish) or above the divergence high (bearish)
5. **Target**: Previous swing high/low, or use Fibonacci levels (→ fibonacci-trading skill)

### Risk Management
```
Entry: Confirmation candle close
Stop: Below divergence swing low + 1% buffer
Target 1: Previous swing high (conservative)
Target 2: Fibonacci extension 127.2% (moderate)
Target 3: Fibonacci extension 161.8% (aggressive)
```

## Important Caveats

- **Divergence can persist**: In strong trends, you can see multiple divergences before price actually reverses. This is why confirmation is mandatory.
- **Timeframe matters**: Daily divergences are more reliable than hourly. Weekly divergences are the most significant.
- **Not standalone**: Always combine with other evidence (S/R levels, volume, trend analysis). Divergence is one input, not the whole thesis.
- **False divergences**: If the RSI is in the 40-60 neutral zone, divergence signals are less meaningful. Best signals come from oversold (<30) or overbought (>70) zones.

## Quick Reference

```
Bullish regular:  Price ↓↓  RSI ↗  → Potential reversal UP
Bearish regular:  Price ↑↑  RSI ↘  → Potential reversal DOWN
Bullish hidden:   Price ↗   RSI ↓↓ → Trend continues UP
Bearish hidden:   Price ↘   RSI ↑↑ → Trend continues DOWN
```
