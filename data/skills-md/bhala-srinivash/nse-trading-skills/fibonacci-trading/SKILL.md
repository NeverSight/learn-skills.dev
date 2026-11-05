---
name: fibonacci-trading
description: |
  Fibonacci retracement and extension trading for NSE/BSE equities. Covers entry zones using
  retracement levels, profit targets using extension levels, and confluence zone identification.

  Use when the user asks: "fib levels for [stock]", "Fibonacci retracement", "fib extensions",
  "where to enter on pullback", "what are the retracement levels", "golden ratio level",
  "Fibonacci targets", or any question about Fibonacci-based trading levels for Indian equities.
---

# Fibonacci Trading

Fibonacci levels identify high-probability zones where price tends to react — for entries on pullbacks and targets on extensions.

## Prerequisites

No dependencies required. Just provide a swing high and swing low price — Claude calculates all Fib levels instantly. Enhanced with Groww MCP (auto-identifies swings from candles) or yfinance.

## Data Needed

1. **Swing high and swing low**: From `fetch_historical_candle_data` or user-provided prices
2. **Current price**: `get_quotes_and_depth` from Groww, or user-provided
3. For precise calculation, you can compute in Python:
   ```python
   diff = swing_high - swing_low
   levels = {
       "23.6%": swing_high - diff * 0.236,
       "38.2%": swing_high - diff * 0.382,
       "50.0%": swing_high - diff * 0.500,
       "61.8%": swing_high - diff * 0.618,
       "78.6%": swing_high - diff * 0.786,
   }
   ```

## Retracement Levels (Entry Zones)

After a significant move up, price often pulls back to these levels before continuing:

| Level | Character | Trading Implication |
|-------|-----------|-------------------|
| 23.6% | Shallow pullback | Strong trend — buyers eager, enter aggressively |
| 38.2% | Normal pullback | Healthy trend — standard entry zone |
| 50.0% | Deep pullback | Trend weakening but viable — enter with caution |
| 61.8% | Golden ratio | Last stand for the trend — high reward if it holds |
| 78.6% | Very deep | Trend likely failed — avoid or use tight stop |

### For downtrend retracements (price bouncing up):
Same levels but inverted — measure from swing high down to swing low.

## Extension Levels (Profit Targets)

After a retracement completes and price resumes the trend:

| Level | Use |
|-------|-----|
| 100% | Measured move — equal to the prior swing |
| 127.2% | Conservative target — good for partial profit |
| 161.8% | Standard target — most common for swing trades |
| 200.0% | Extended target — for strong trends |
| 261.8% | Full extension — rare, only in powerful moves |

### Calculating Extensions
```python
# For uptrend: price resumed from point C (retracement low)
ext_127 = C + (swing_high - swing_low) * 1.272
ext_161 = C + (swing_high - swing_low) * 1.618
ext_200 = C + (swing_high - swing_low) * 2.000
```

## How to Draw Fibs

1. **Identify the swing**: Find the most recent significant high and low (at least 5% move)
2. **Direction matters**:
   - Uptrend retracement: Anchor at swing low, drag to swing high
   - Downtrend retracement: Anchor at swing high, drag to swing low
3. **Use the right swing**: The most recent *completed* swing, not one still in progress
4. **Multiple swings**: You can draw Fibs from different timeframes. When levels from different swings overlap, that's a confluence zone (very strong).

## Confluence Zones

The most powerful Fibonacci levels are where they align with other technical factors. These zones have the highest probability of price reaction.

| Confluence Combination | Strength |
|-----------------------|----------|
| Fib level alone | Moderate |
| Fib + horizontal S/R | Strong |
| Fib + moving average (SMA50/200) | Strong |
| Fib + trendline | Strong |
| Fib + S/R + MA | Very strong |
| Fib from multiple timeframes overlapping | Very strong |

### Practical Examples
- Fib 38.2% from daily swing aligns with SMA50 → strong buy zone
- Fib 61.8% from weekly swing aligns with horizontal support from 3 months ago → high-probability entry
- Fib extension 161.8% aligns with a round number (Rs.2,000) → likely profit target

## Fibonacci Trading Rules

1. **Don't use Fibs in isolation** — they work best as confirmation alongside S/R, volume, and indicators
2. **Zone, not line** — treat each level as a zone (±1-2%), not a precise price
3. **Wait for reaction** — don't blindly buy at a Fib level. Wait for a reversal candle (hammer, engulfing, etc.)
4. **Strongest entries**: Fib 38.2% to 61.8% zone in a healthy trend with volume confirmation
5. **If 78.6% breaks**: The trend is likely over — exit or reverse
