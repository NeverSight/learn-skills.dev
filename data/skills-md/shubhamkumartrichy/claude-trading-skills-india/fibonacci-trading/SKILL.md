---
name: fibonacci-trading
description: |
  Fibonacci retracement entry zones and extension targets for NSE/BSE stocks and indices, with
  automatic swing detection (ta.py fib), trend-based extensions from the pullback point, and
  confluence with moving averages, support/resistance, round numbers and option OI strikes.

  Use when the user asks: "fib levels for X", "Fibonacci retracement", "where to buy the pullback",
  "golden ratio / 61.8%", "Fib extension targets", "how far can NIFTY fall/rise from here", or gives
  a swing high and low to compute levels.
---

# Fibonacci Trading

Fibonacci levels mark zones where pullbacks often pause and where extended moves often stall. Use
them as zones that need confirmation, never as standalone signals.

## Compute

```bash
# Manual swing (e.g. NIFTY rallied 22,000 → 24,000)
python3 ../technical-analysis/scripts/ta.py fib --high 24000 --low 22000 --trend up
# Add the pullback low (point C) for trend-based extension targets
python3 ../technical-analysis/scripts/ta.py fib --high 24000 --low 22000 --trend up --pivot 23200
# Down-swing (rally retracements are sell zones)
python3 ../technical-analysis/scripts/ta.py fib --high 24000 --low 22000 --trend down
# Automatic: largest swing in the last 120 bars, with current price position
python3 ../technical-analysis/scripts/ta.py fib --symbol NIFTY          # or --csv / --candles
```

The user's phrasing "from 24,000 to 22,000" means a **down-swing** (high first). Draw retracements
upward from the low.

## Retracements (entry zones)

| Level | Character | Use |
|---|---|---|
| 23.6% | Shallow | Very strong trend; aggressive entries only |
| 38.2% | Normal | Standard pullback entry zone |
| 50.0% | Deep (not a true Fib ratio, widely watched) | Valid with confirmation |
| 61.8% | Golden ratio | Last good defence of the trend; best R:R if it holds |
| 78.6% | Very deep | Trend likely failing; tight stop or avoid |

The best zone in healthy trends is 38.2%–61.8% on falling volume, followed by a reversal candle.
A close beyond 78.6% invalidates the swing.

## Extensions (targets)

| Level | Use |
|---|---|
| 100% | Measured move (AB = CD) |
| 127.2% | Conservative target, partial profit |
| 161.8% | Standard swing target |
| 200% / 261.8% | Strong trends only |

With `--pivot` (point C, the end of the retracement) the script projects **trend-based extensions**:
C ± (B − A) × level. Without it, extensions are measured from A, which is the classic extension beyond B.

## Drawing rules
1. Use a **completed** swing of at least about 5% (stocks) or 3% (indices), not one still in progress.
2. Uptrend: anchor at the swing low and drag to the swing high. Downtrend: the reverse.
3. Use split-adjusted data. A bonus or split inside the swing ruins the levels.
4. Draw from more than one timeframe. Where weekly and daily Fib levels overlap is a strong zone.

## Confluence (strength ladder)

| Combination | Strength |
|---|---|
| Fib alone | Moderate |
| Fib + horizontal S/R or gap zone | Strong |
| Fib + SMA50/SMA200 | Strong |
| Fib + round number (₹1,000; NIFTY 24,500) or a big option-OI strike | Strong (India-specific magnet) |
| Fib + S/R + MA, or multi-timeframe Fib overlap | Very strong |

## Rules
1. Treat each level as a zone (±1% for stocks, ±0.5% for indices).
2. Wait for a reaction candle in the zone (hammer, engulfing, 75-min reversal).
3. Stop goes beyond the next Fib level or the swing extreme, with a buffer of at least 1 ATR.
4. Take partial profits at 127.2%, trail the rest (`trailing-stops`).
5. Check R:R after costs before entering (`risk-reward-ratio`).
