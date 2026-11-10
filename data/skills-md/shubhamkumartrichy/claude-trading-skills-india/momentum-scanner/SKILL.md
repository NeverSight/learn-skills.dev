---
name: momentum-scanner
description: |
  Short-term momentum on NSE/BSE stocks across a whole universe: momentum-burst days (a 4%+ up-close
  out of a quiet base on rising volume, near the high, above a rising 50 DMA, not already extended),
  episodic pivots (a 5%+ opening gap on 3x+ volume that holds the gap-day low, with a day-1/day-2
  read and a catalyst checklist), and a 1-99 relative-strength rating with the RS line vs NIFTY.
  Flags upper-circuit closes, 2%/5% band stocks and low delivery, applies a ₹-crore liquidity floor,
  then ranks a short watchlist and hands the best names to breakout-planner. momentum.py works
  offline from CSVs.

  Use when the user asks: "which stocks broke out today", "find momentum bursts", "4% breakout
  scan", "stocks gapping up on results", "episodic pivot", "gap-up on volume after results",
  "which stocks have the best relative strength", "RS rating for my watchlist", "RS line new high",
  "momentum watchlist for this week", or "what's leading the market".
---

# Momentum Scanner (NSE/BSE)

Find what is moving now: a burst out of a quiet base, a news gap the market re-prices, or a leader
whose RS line makes a new high before its price. This skill finds candidates; `breakout-planner`
reads the base and builds the order.

## Commands

```bash
python3 scripts/momentum.py burst --csv-dir data/ --days 5 --show-rejects
python3 scripts/momentum.py pivot --csv-dir data/ --catalyst DIXON=results --catalyst KAYNES=order-win
python3 scripts/momentum.py rs --csv-dir data/ --benchmark-csv data/nifty.csv --top 20
python3 scripts/momentum.py scan --csv-dir data/ --benchmark-csv nifty.csv --bands bands.csv --regime confirmed
python3 scripts/momentum.py scan --symbols DIXON,KAYNES,TRENT,POLYCAB --benchmark NIFTY   # yfinance
```
The universe flags match `breakout.py scan`: `--csv-dir` + `--pattern` (file name = symbol),
`--csv FILE` (repeatable) or `--symbols`. Also `--as-of YYYY-MM-DD` (replay a date),
`--min-turnover-cr` (5), `--bands FILE` (`SYMBOL,band` with 2/5/10/20, or 0 for F&O names with
no fixed band) and `--json`. Use 260+ daily bars (64 is the minimum for RS). Blank or zero candles
are skipped. Bad input exits 2 with a one-line `error:`.

## Reading `burst` (last 5 sessions, `--days`)

| Test | Default (flag) |
|---|---|
| Move | Close ≥ +4% vs the previous close (`--min-move-pct`) |
| Volume | Above the previous session **and** above the 50-day average (the 50 sessions before) |
| Close | In the top 70% of the day's range (`--min-close-pos`) |
| Quiet base | 3+ sessions right before it inside an 8% high-low band (`--min-base-days`, `--max-base-pct`), with daily ranges no wider than the 20 sessions before (`--max-range-ratio 1.0`) |
| Not extended | Up no more than 6% in the 3 sessions before (`--max-run-pct`) |
| Trend | Close above a 50 DMA that is higher than 10 sessions ago |
| Liquidity | ≥ ₹5 crore average traded value over the 20 sessions **before** the burst, so a one-day spike can't pass an illiquid stock |

Score /100: move 25, volume 20, close 15, base length 10, range contraction 15, 50 DMA above 200
DMA 10, delivery at or above average 5, minus flag penalties. Plan reference: buy above the
burst-day high, stop at its low. A burst is a 3-5 day trade: book partials fast, exit if the low
breaks. `--show-rejects` lists near-misses and why (extended, illiquid, no base).

## Reading `pivot` (last 10 sessions)

Open ≥ 5% above the previous close (`--min-gap-pct`) on ≥ 3× the 50-day volume (`--min-vol-mult`),
with no close below the gap-day low since. **Day 1**: strong if it closed above the open near the
high, weak if sellers took it back to the low. **Day 2**: follow-through, holding, tested the low,
or failed. A gap that gets filled, or a stock already up 40%+ in the 60 sessions before, scores
lower. The open comes from NSE's **pre-open** call auction (orders 09:00-09:08, trading from 09:15),
so don't chase the first minutes. Buy above the gap-day high or the opening-range high, stop under
the gap-day low.

**Catalyst checklist.** Pass what you have verified: `--catalyst SYM=results|order-win|block-deal|approval|rating-upgrade|other`
(a bare `--catalyst results` applies to every name). Results beats with margin expansion and order
wins large against revenue carry the most weight. For a block deal, check who sold. A gap with no
catalyst is a burst, not a pivot, and in small caps it can be operator-driven.

## Reading `rs`

Weighted return = 0.4 × 3-month + 0.2 × 6-month + 0.2 × 9-month + 0.2 × 12-month (63/126/189/252
sessions, cumulative). The latest quarter sits inside all four, so recent strength counts most. The
rating is the percentile rank inside **your universe**, from 1 to 99. Rank NIFTY 500 or a full
watchlist, because ten names give coarse ratings. Stocks with less history are re-weighted over the
horizons they have and marked partial. With a benchmark, the RS line (stock ÷ NIFTY) is checked for
a new 52-week high in the last 5 sessions (`--rs-high-days`). **New high ahead of price** is the
leader's tell. A price high without an RS-line high is a laggard riding the index. The output also
shows where the benchmark itself would rate (use NIFTY Midcap 150 for midcaps).

## `scan`: the watchlist

Bursts, pivots and liquid RS leaders (RS ≥ 85 `--leader-rs`, within 10% of the high, above the 50
DMA, RS line at a high) go into one list ranked by signal strength (60%), RS rating (30%) and RS-line and high bonuses, minus
circuit and band penalties. Each name gets a one-line reason. The top tradable names (no circuit or
band flag) get a ready `breakout.py check` command (see `../breakout-planner/scripts/breakout.py`)
to find the base, pivot, stop and order. `--regime` takes the `market-regime` label and prints the
gate: Correction means no new momentum trades.

## India specifics

- **Results season** (mid-Jan, Apr-May, Jul-Aug, Oct-Nov) is when most real pivots happen. Gaps
  around the result date are the signal. A burst just *before* results is a coin toss.
- **Upper circuit.** A close at the high on a band-sized move (2/5/10/20%) is flagged `UC?`
  (inferred) or `UC` (band from `--bands`). Buyers queued unfilled, so the close isn't a price you
  could pay, and the next open usually gaps. `--exclude-locked` drops these closes.
- **2%/5% bands** (flag `band2`/`band5`, inferred when the tape keeps closing exactly ±2/5%) mean
  surveillance (ASM/GSM), trade-for-trade (BE/T2T) or SME. These names have no intraday or BTST,
  need 100% upfront margin and often have no MTF, and their exits can lock at the lower circuit.
  Operator and SME pumps live here: vertical moves, circuit after circuit, low delivery, no news.
  Skip them.
- **Delivery %.** If the CSV has an NSE delivery column (`DELIV_PER`, `% Dly Qt to Traded Qty`,
  or delivery quantity), a burst on below-average delivery is flagged as intraday churn.
  `--min-delivery-pct` makes it a filter.
- **Expiry-week noise.** Bursts in the week of the last-Tuesday F&O monthly expiry are tagged
  `expiry-wk`. Rollover and short covering in F&O names, and NIFTY's weekly Tuesday expiry, can fake
  one-day strength. Wait for a second day.

## Workflow

1. Run `../market-regime/scripts/regime.py status` (`market-regime`). Trade bursts only when the
   regime allows new longs, and stay inside its position count.
2. Run `scan` on the universe, read the reasons, and drop flagged names.
3. Hand the top names to `breakout-planner` (`check`, then `plan`) for the stop, trigger and GTT.
4. Size with `position-sizing` (`../position-sizing/scripts/risk.py`). Bursts are short trades, so
   check the round trip with `trading-costs`.
5. Run the `trading-discipline` gate (`../trading-discipline/scripts/discipline.py`) before any
   order. After entry, `trailing-stops` takes over.

## Output

```
 # Symbol  Close  RS  vs 52wH  Score  Signals [flags]   +  "Why:" one reason per name
Next: python3 .../breakout.py check --csv SYMBOL.csv --benchmark-csv nifty.csv
```
Limits: daily bars only, so there's no intraday pre-open data or live circuit status. Bands are
inferred unless you pass `--bands`, and an F&O stock up exactly 10% at its high can be a false
`UC?`. Catalysts are whatever you supply. RS ranks only the universe you give it.

_Educational analysis, not investment advice._
