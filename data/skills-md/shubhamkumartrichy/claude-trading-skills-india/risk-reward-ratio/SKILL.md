---
name: risk-reward-ratio
description: |
  Risk-reward evaluation for Indian trades after real costs: R multiples per target, weighted R for
  scale-outs, breakeven win rate, expectancy, trade-filter thresholds, and option-specific R:R
  (theta, IV, premium). risk.py rr computes everything including Indian round-trip charges.

  Use when the user asks: "is this trade worth it", "risk reward for entry X stop Y target Z", "R:R",
  "expected value", "what win rate do I need", "should I take this setup", or compares multiple
  trade ideas.
---

# Risk-Reward Ratio

If the maths doesn't work after costs, skip the trade. R:R is the cheapest filter there is.

## Calculator

```bash
python3 ../position-sizing/scripts/risk.py rr --entry 1800 --stop 1700 --target 2100
python3 ../position-sizing/scripts/risk.py rr --entry 1800 --stop 1700 \
    --target 1900:50 --target 2000:30 --target 2200:20 --win-rate 45 --cost-pct 0.25
python3 ../position-sizing/scripts/risk.py rr --entry 450 --stop 470 --target 410 --cost-pct 0.05   # short
```
Weights after `:` are the % of the position exited at each target. `--cost-pct` is the round-trip
cost (delivery ≈0.25, intraday ≈0.05, futures ≈0.06, or exact from `trading-costs`).

## Core maths

```
R per target   = (Target − Entry) ÷ (Entry − Stop)              long; mirror for shorts
R after costs  = (Reward − cost) ÷ (Risk + cost)
Weighted R     = Σ weight × R
Breakeven win% = 1 ÷ (1 + R_after_costs)
Expectancy (R) = W × R_after_costs − (1 − W)
```

Example: entry ₹1,800, stop ₹1,700, scale out 50/30/20 at ₹1,900/₹2,000/₹2,200 gives a weighted
1.90R. With 0.25% delivery costs it is 1.78R, so the breakeven win rate is 36%. At a 45% win rate,
expectancy is +0.25R per trade.

## Minimum R by win rate

| Win rate | Breakeven R | Recommended min R (after costs) |
|---|---|---|
| 30% | 2.33 | 3.0 |
| 40% | 1.50 | 2.0 |
| 50% | 1.00 | 1.5 |
| 60% | 0.67 | 1.0 |

If the user doesn't know their win rate, assume 40–45% and require at least 2R after costs.
`risk.py journal` measures the real win rate from their trades.

## Filter

| R after costs | Decision |
|---|---|
| < 1 | Skip |
| 1 – 1.5 | Only with a proven >55% win rate |
| 1.5 – 2 | Acceptable |
| 2 – 3 | Good (standard swing) |
| > 3 | Excellent, but check the target is realistic (below the next major resistance) |

## Making R honest
- **Target realism:** the target must sit at or before the next real resistance (`ta.py levels`), the
  Fib extension, or the expected move. A target above three resistance levels is fantasy R.
- **Stop realism:** if the stop is inside daily noise (under 1 ATR), the "great R:R" is an illusion of
  a tight stop.
- **Costs and slippage:** small targets in small caps lose a lot to spread and impact.

## Options
- **Long options:** R:R depends on the move **and its timing**. Price the target premium with
  `options.py greeks` at the target date and IV (IV often falls after events: IV crush). A ₹100 → ₹200
  target needs the underlying move before theta eats the premium.
- **Short options:** typical credit trades risk 2–4 units to make 1 (R ≈ 0.25–0.5) with a high win
  rate. Judge them on expectancy and tail loss, not R. `options.py payoff` gives max profit, max loss,
  breakevens and probability of profit.

## Checklist
- [ ] Specific target(s) at real levels
- [ ] Stop at a technical invalidation point, ≥1 ATR away
- [ ] R ≥ 1.5–2 **after costs**
- [ ] Position risk ≤ 1–2% of capital
- [ ] Positive expectancy at a realistic win rate
