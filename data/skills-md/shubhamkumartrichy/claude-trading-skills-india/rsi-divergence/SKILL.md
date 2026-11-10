---
name: rsi-divergence
description: |
  Detect and trade RSI(14) divergences on NSE/BSE stocks and indices: regular divergence (reversal
  warning) and hidden divergence (trend continuation), with strength grading, confirmation rules,
  entries, stops and Fibonacci targets. ta.py divergence finds them automatically from swing points.

  Use when the user asks: "RSI divergence on X", "is there bullish/bearish divergence", "momentum
  divergence", "RSI showing weakness", "hidden divergence", or wants to know if momentum confirms
  a new high/low.
---

# RSI Divergence

Divergence means price is making a new extreme but momentum is not following. It is an early
warning, not a trigger.

## Find them

```bash
python3 ../technical-analysis/scripts/ta.py divergence --symbol ICICIBANK     # or --csv / --candles
python3 ../technical-analysis/scripts/ta.py summary --csv data.csv            # includes the 3 most recent
```

The script uses Wilder RSI(14) and compares consecutive swing lows (bullish) or swing highs (bearish)
at least 5 bars apart within the last 90 bars. Each finding includes the dates, prices, RSI values,
strength, and a warning when RSI sits in the weak 40–60 zone.

## Types

| Type | Price | RSI | Meaning |
|---|---|---|---|
| Regular bullish | Lower low | Higher low | Selling pressure fading; possible bottom |
| Regular bearish | Higher high | Lower high | Buying pressure fading; possible top |
| Hidden bullish | Higher low | Lower low | Uptrend pullback; continuation likely |
| Hidden bearish | Lower high | Higher high | Downtrend rally; continuation likely |

**Strength grading:** a 2-swing divergence is standard; 3 swings is strong; from oversold (<30) or
overbought (>70) territory is stronger; combined with falling volume or falling delivery % into the
extreme is strongest. Weekly beats daily, and daily beats intraday.

## Trade it (only with confirmation)

1. Identify the divergence on the daily chart and check the weekly bias (`multi-timeframe-analysis`).
   Regular divergences against a strong weekly trend fail often. Hidden divergences *with* the weekly
   trend are the higher-probability use.
2. Wait for confirmation:
   - a close beyond the minor trendline or the last lower-high (bullish case);
   - RSI crossing back above 30 (bullish) or below 70 (bearish);
   - a reversal candle (bullish engulfing, hammer) at a support level or Fib zone.
3. Enter on the confirmation candle's close, or on the next day's open if it was a results or event day.
4. **Stop:** beyond the divergence extreme plus a buffer (0.5% large cap, 1% mid/small cap), and at
   least 1 ATR away.
5. **Targets:** previous swing high/low, then Fib extensions 127.2% and 161.8% (`ta.py fib`).
6. Size with `position-sizing` and check R:R after costs (`risk-reward-ratio`).

## Caveats
- **Divergence can persist.** Strong trends print several divergences before turning.
- **RSI in 40–60** makes signals weak, and the script flags it.
- **Event distortion:** results days, ex-dividend drops, and bonus/split adjustments create artificial
  swings. Exclude those bars or treat findings around them with caution.
- **Index vs constituents:** a divergence on NIFTY is more reliable when heavyweights (HDFCBANK,
  RELIANCE, ICICIBANK, INFY, TCS…) show the same pattern.

## Output
```
Divergence: [type] on [timeframe], [date1] → [date2]
Price ₹a → ₹b; RSI x → y ([strength]; RSI zone note)
Context: weekly bias …, level …, volume/delivery …
Plan: confirm on … | entry … | stop … | targets … | R:R after costs …
```
