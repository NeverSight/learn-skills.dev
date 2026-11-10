---
name: trailing-stops
description: |
  Trailing-stop plans that lock in profit on NSE/BSE positions: the R-multiple ladder (hold → breakeven
  at 1R → ATR trail at 2R → structure trail at 3R+), plus ATR, structure, moving-average and
  chandelier trails, with GTT/SL execution realities for Indian brokers. risk.py trail computes
  the recommended ratcheted stop.

  Use when the user asks: "how should I trail my stop", "lock in profits on X", "when to move stop to
  breakeven", "chandelier exit", "protect my gains", "my stock is up 15%, what now", or anything about
  adjusting stops as a trade moves in their favour.
---

# Trailing Stops

Trail to protect open profit while giving the trend room. The stop only moves in the trade's favour.

## Calculator

```bash
python3 ../position-sizing/scripts/risk.py trail --entry 750 --stop 720 --highest-close 845 \
    --atr 14 --swing-low 805 --highest-high 850 --sma20 812 --current-stop 760
```
It reports R gained, the ladder stage, every candidate level, and the recommended stop (never below
`--current-stop`). Get ATR, SMA20/EMA50 and the latest swing low from `ta.py summary`.

## The R-multiple ladder (default)

1R = entry − initial stop.

| Stage | Open profit | Stop rule | Why |
|---|---|---|---|
| Fresh | 0 – 1R | Keep the initial stop | Trailing early gets shaken out by noise |
| Early | ≥ 1R | Move to breakeven (entry; add costs for true breakeven) | The trade can no longer lose money |
| Building | ≥ 2R | Highest close − 1.5 × ATR(14) | Gives room while banking most of the move |
| Runner | ≥ 3R | Below the latest higher low (structure) | Follows the trend's own rhythm |

Take the **highest** qualifying level (the tightest) and never lower it.

## Individual methods

| Method | Rule | Best for |
|---|---|---|
| ATR trail | Highest close − k × ATR (k 1.5 tight / 2 standard / 3 loose) | Trending but volatile stocks |
| Structure | Below each new higher low | Clean stair-step trends |
| MA trail | Daily close below SMA20 (fast) / EMA50 (steady) / SMA200 (positional) → exit | Smooth grinders |
| Chandelier | Highest high − 3 × ATR | Explosive runners, momentum names |
| Partial + trail | Book 30–50% at 2R or the 127.2% Fib, trail the rest | Results-season or event-heavy names |

## Execution in India

- **Update daily after the close** using the official close (30-min VWAP), not intraday wicks.
  Modify the **GTT** for delivery holdings, or re-place the SL each morning because SL orders expire daily.
- For F&O positions, trail on the underlying or futures chart and execute with SL-limit orders.
  Brokers' old bracket/cover orders with trailing are largely discontinued.
- Before **results, Budget or RBI policy days**, tighten to the 1.5 × ATR level or book partial
  profits. A gap can jump past any trail.
- **Tax-aware trailing:** if a delivery position is a few weeks from turning long-term (over 12
  months), a slightly looser trail may be worth it because the tax rate drops from 20% to 12.5%.
  Quantify it with `indian-tax-for-traders`.

## Rules
1. A ratchet: up only (longs), down only (shorts).
2. Evaluate on daily closes; exit in the closing session or at the next open when breached.
3. Don't overtighten: a trail closer than about 1 ATR gets hit by ordinary pullbacks.
4. Choose the method before the trade and stick to it.

## Output

```
Gained: x.xR → stage: [..]
Candidates: breakeven ₹.. | ATR(1.5x) ₹.. | structure ₹.. | chandelier ₹.. | SMA20 ₹..
New stop: ₹S (locks +y.yR) → update GTT trigger ₹S / limit ₹S−b
Next review: after today's close; event risk: [results on dd-mmm]
```
