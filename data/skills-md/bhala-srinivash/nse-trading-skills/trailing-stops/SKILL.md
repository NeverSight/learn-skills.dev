---
name: trailing-stops
description: |
  Trailing stop strategies to lock in profits on NSE/BSE equity positions. Covers ATR trail,
  structure trail, MA trail, chandelier exit, and the recommended hybrid approach.

  Use when the user asks: "how to trail my stop", "trailing stop for [stock]", "lock in profits",
  "when to move stop to breakeven", "chandelier exit", "protect my gains", or any question about
  dynamically adjusting stop-losses as a trade moves in favor.
---

# Trailing Stops

Once a trade is profitable, trailing stops protect your gains while letting winners run.

## Prerequisites

No dependencies required. Provide entry, current price, and ATR manually. Enhanced with Groww MCP (live ATR, candles, MAs) or yfinance.

## Data Needed

1. **Entry price and current price**: Known or from `get_quotes_and_depth`
2. **ATR(14)**: `get_historical_technical_indicators` from Groww, or user-provided
3. **Recent swing lows/highs**: `fetch_historical_candle_data` (daily)
4. **Moving averages**: SMA20, EMA50 from indicators
5. **Initial risk (1R)**: Entry - original stop-loss

## The Hybrid Approach (Recommended)

This progressive system adapts as the trade matures:

| Trade Stage | Profit Level | Trailing Method |
|------------|-------------|-----------------|
| Just entered | 0 to 1R | **Fixed stop** — don't trail yet, use initial stop-loss |
| Early profit | 1R gained | **Move to breakeven** — stop at entry price (eliminates risk) |
| Building profit | 2R gained | **ATR trail** — highest close minus ATR(14) × 1.5 |
| Strong runner | 3R+ gained | **Structure trail** — below most recent swing low |

This works because:
- Below 1R: Moving stop too early gets you shaken out on noise
- At 1R: Breakeven means you can't lose money — psychological freedom to hold
- At 2R: ATR trail gives the stock room to breathe while protecting most profit
- At 3R+: Structure trail is tighter, appropriate when you have a large cushion

## Individual Methods

### ATR Trail
```
Trailing stop = Highest close since entry - ATR(14) × multiplier
Multiplier: 1.5 (tight), 2.0 (standard), 3.0 (loose)
```
Recalculate daily at market close. Only move stop up, never down.

### Structure Trail
```
Trailing stop = Below the most recent higher low
```
Identify swing lows on the daily chart. Each new higher low becomes the new stop reference. Best for stocks making clear stair-step patterns.

### Moving Average Trail
```
Aggressive: Trail below SMA20 (for fast trends)
Moderate: Trail below EMA50 (for steady trends)
Conservative: Trail below SMA200 (for long-term holds)
```
Use closing price vs MA — if daily close is below the MA, exit next day.

### Chandelier Exit
```
Trailing stop = Highest high since entry - ATR(14) × 3.0
```
More aggressive than standard ATR trail. Good for volatile runners where you want to ride big swings.

## Trailing Stop Rules

1. **Only move up**, never down — a trailing stop is a ratchet
2. **Check daily at market close** — don't adjust intraday (noise)
3. **Use closing prices** for triggers — ignore intraday wicks
4. **When stop is hit**: exit at next day's open, no exceptions
5. **Don't overtighten**: If you're trailing too tight, you'll get stopped out on normal pullbacks. Give the stock room proportional to its ATR.

## Choosing Your Method

| Stock Behavior | Best Trail Method |
|---------------|------------------|
| Strong uptrend, clear swing lows | Structure trail |
| Trending but volatile | ATR trail (2.0×) or Chandelier |
| Steady grinder, low volatility | MA trail (EMA50) |
| Explosive mover, unsure of top | Chandelier exit (3.0× ATR) |
| Long-term investment | MA trail (SMA200) |
