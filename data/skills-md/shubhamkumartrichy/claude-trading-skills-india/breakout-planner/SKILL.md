---
name: breakout-planner
description: |
  Stage-2 breakout setups on NSE/BSE stocks: a trend-template check (rising 200 DMA, 50>150>200
  stack, distance from 52-week high/low, relative strength vs NIFTY), base detection (volatility
  contraction with successively tighter pullbacks, or a flat base) with pivot, depth, duration,
  volume dry-up and a grade, then an order-ready plan: trigger, chase limit, capped stop, size,
  Indian charges, R targets, GTT/SL templates, circuit-band and NSE tick-size checks. breakout.py
  scans a folder of CSVs or yfinance symbols and ranks them, offline-capable.

  Use when the user asks: "is X in a Stage 2 uptrend", "find VCP setups", "where is the pivot on X",
  "plan a breakout trade in X", "breakout buy point and stop", "scan these stocks for breakouts",
  "Minervini trend template for NSE stocks", "how do I place a GTT for a breakout", or any question
  about buying stocks as they clear a base.
---

# Breakout Planner (NSE/BSE)

Buy strength only where three things line up: a stock already in a Stage-2 uptrend, a tight base
whose pullbacks shrink as supply dries up, and a pivot you can define to the tick. The script does
the detection and arithmetic. You add regime, news and judgement.

## Commands

```bash
# One stock: trend template + liquidity + base + pivot (add a NIFTY CSV for relative strength)
python3 scripts/breakout.py check --csv polycab.csv --benchmark-csv nifty.csv
python3 scripts/breakout.py check --symbol POLYCAB --benchmark NIFTY          # yfinance
# Plan from the chart (pivot, last low and ATR are read from the data)
python3 scripts/breakout.py plan --csv polycab.csv --capital 1000000 --risk-pct 1 --band 0
# Plan from numbers you already have (no data needed)
python3 scripts/breakout.py plan --pivot 1520 --contraction-low 1462 --prev-close 1498 \
    --capital 500000 --band 10 --segment mtf --leverage 2 --broker zerodha
# Rank many: one CSV per symbol (file name = symbol), or a yfinance list
python3 scripts/breakout.py scan --csv-dir data/ --benchmark-csv data/nifty.csv --top 15
python3 scripts/breakout.py scan --symbols DIXON,KAYNES,TRENT,POLYCAB --benchmark NIFTY
```
Inputs follow `technical-analysis`: `--csv`, `--candles` (broker-MCP JSON) or `--symbol`. Use 260+
daily bars. Every command takes `--json`. Bad input exits 2 with a one-line error.

## Reading `check`

**Trend template** (all must pass for "Stage 2"): close above SMA50/150/200; SMA50 > SMA150 > SMA200;
SMA200 higher than 22 sessions ago; within 25% of the 52-week high; at least 30% above the 52-week
low; with a benchmark, beating it over both 3 and 6 months. Use NIFTY for large caps and NIFTY
Midcap/Smallcap or the sector index for the rest. Five of six is "watch", not "buy".

**Base.** The base starts at the highest high of the last 150 bars. Swings are traced with a
threshold of max(3%, 1.25 × ATR%). A bounce that fails into a lower low stays part of the same
pullback; a small dip on the way to a higher high is ignored.
- **VCP**: 2+ pullbacks, each shallower than the previous (≤0.85x), last one ≤15% (ideally ≤6%),
  first ≤50%. Pivot = high of the last pullback.
- **Flat base**: whole base ≤15% deep and 5+ weeks long when the pullbacks don't tighten. Pivot =
  base high.
- **Loose/unclassified**: neither. Grade D. Wait for a proper base.
- **Volume dry-up** = volume in the last pullback ÷ the 50 bars before it. Below 0.6 is strong; above
  1.0 means supply.
- **Grade** A ≥80, B ≥60, C ≥40, D below. **State**: pre-breakout, breakout zone (≤ chase above
  pivot), extended, deep below pivot, or failed (closed under the last low).
- Cup-with-handle is not detected separately. Most read as a VCP or loose base, so confirm on the chart.

## Reading `plan`

| Item | Rule (defaults) |
|---|---|
| Trigger | pivot + 0.2%, rounded **up** to the tick |
| Chase limit | pivot + 3% (`--max-chase-pct`; warns above 5%). Size is computed at this worst fill |
| Stop | last contraction low − 1% (`--stop-method atr` = trigger − 2×ATR), **capped at 8%** below the limit |
| Size | `position-sizing` logic (risk.py): risk % of capital incl. costs, 20% single-stock cap; MTF divides the risk budget by the leverage |
| Charges | trading-costs (charges.py) round trip at the stop and at each target, delivery or MTF with interest |
| Targets | 2R and 3R from the worst fill (`--targets 2,3,5`) |

A capped stop sits inside the base, so the base is too loose for your chase. Prefer to skip it or
buy closer to the pivot.

## India specifics

- **Order types.** Exchange stop orders (SL / SL-M) are **DAY-only** and lapse at 15:30, and the
  pre-open session takes no stop orders. For a multi-day wait use a broker **GTT** (trigger = entry
  trigger, limit = chase limit). After the fill, protect it with a **GTT OCO** (stop + target).
  Shares settle **T+1**, so on the buy day some brokers need a DAY SL-sell until the shares show
  in holdings.
- **Tick size** follows NSE slabs effective 15-Apr-2025: below ₹250 ₹0.01; ₹250–1,000 ₹0.05;
  ₹1,000–5,000 ₹0.10; ₹5,000–10,000 ₹0.50; ₹10,000–20,000 ₹1; above ₹20,000 ₹5. NSE reassigns
  slabs monthly from a reference close, and BSE can differ, so pass `--tick` if the broker rejects
  a price.
- **Circuit bands.** `--band 2|5|10|20` with `--prev-close` (taken from the data's last close)
  warns when the trigger or chase limit is beyond today's upper circuit. 2%/5% bands mark
  surveillance, SME or illiquid names, where breakouts lock at the upper circuit and exits lock at
  the lower one. F&O stocks have no fixed circuit (`--band 0`): the exchange widens their dynamic
  band in steps.
- **Surveillance.** ASM/GSM stocks and trade-for-trade (BE/T2T) stocks have no intraday or BTST,
  need 100% upfront payment and usually can't be funded with MTF. Check NSE's lists or pass
  `--surveillance asm|gsm|t2t`.
- **Liquidity.** The default floor is ₹5 crore average daily traded value (`--min-turnover-cr`).
  Scans push illiquid names to the bottom. Skip SME and operator-style stocks: a vertical base on
  rising volume with no news or delivery is a red flag.
- **Delivery %** on the breakout day should match or beat its recent average (NSE security-wise
  delivery data). A high-volume breakout on low delivery is mostly intraday churn.
- **Results season.** A pivot within ~5 sessions of quarterly results is a coin toss with a 5–15%
  gap. Wait for the number or size down. The plan reports the worst 60-bar gap-down and sizes the
  gap-through loss for it.

## Workflow

1. Run `../market-regime/scripts/regime.py status` first (see `market-regime`). Take new
   breakouts only when the regime allows long exposure, and respect its position cap.
2. Run `scan` on the watchlist, then `check` the top names and confirm the base on the chart
   (`technical-analysis`, `multi-timeframe-analysis`).
3. Run `plan` for actionable names. Cross-check the stop with `stop-loss-strategies` and the size
   with `position-sizing`.
4. After entry, hand trade management to `trailing-stops`: breakeven at 1R, trail from 2R.
   Exit fast if price closes back under the pivot on heavy volume within a few sessions.

## Output

```
SYMBOL — date, close | trend 6/6 | base VCP A | pre-breakout (−2.1% vs pivot)
T1 20% → T2 10% → T3 5% | dry-up 0.40x | pivot ₹P | last low ₹L
Trigger ₹T | chase ≤ ₹C | stop ₹S (x% , capped?) | qty N (₹value, y% of capital) | risk ₹R
Targets 2R ₹.. / 3R ₹.. (net of charges) | band check | tick
Orders: GTT buy (trigger/limit) → GTT OCO (stop/target); DAY SL alternative
Checklist: regime, surveillance, results date, delivery %, liquidity
```

_Educational analysis, not investment advice._
