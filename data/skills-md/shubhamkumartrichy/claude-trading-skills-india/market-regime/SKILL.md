---
name: market-regime
description: |
  Reads the market regime of NIFTY, BANKNIFTY, SENSEX (or any index/ETF CSV) from the index's own
  tape: distribution-day clusters with 25-session/5%-rally expiry, the correction → rally attempt →
  follow-through cycle, 50/200 DMA and 52-week drawdown context, and optional India VIX. Outputs a
  0–100 risk score, a regime label, an exposure ceiling (% of capital, max new positions) and the
  levels that would change the label. Handles Yahoo's missing index volume via ETF/futures proxy or a
  clearly flagged price-only mode. regime.py works offline from CSV.

  Use when the user asks: "is the market in an uptrend", "should I be buying now", "how much should
  I be invested", "is NIFTY topping", "distribution days on NIFTY", "follow-through day", "is this
  bounce real", "market regime", "should I go to cash", or before any new swing/positional entries.
---

# Market Regime

Decide how much risk the market allows before picking stocks. Most swing breakouts fail when the
index is distributing or correcting, so the regime sets the exposure ceiling for every other skill.

## Commands

```bash
python3 scripts/regime.py status --csv nifty.csv --volume-csv niftybees.csv --vix 14.2
python3 scripts/regime.py status --symbol NIFTY --vix 14.2          # yfinance; ETF volume auto-fetched
python3 scripts/regime.py distribution --csv nifty.csv --volume-csv niftybees.csv --all --stalling
python3 scripts/regime.py ftd --csv banknifty.csv --volume-csv bankbees.csv --events 15
python3 scripts/regime.py trend --symbol SENSEX
python3 scripts/regime.py status --csv nifty.csv --as-of 2026-06-05 --json   # replay a past date
```
Inputs match `../technical-analysis/scripts/ta.py` (`--csv`, `--candles`, `--symbol`). Useful flags:
`--ftd-pct`, `--dd-pct` (0.2), `--dd-window` (25), `--correction-pct` (5), `--ignore DATE,DATE`,
`--expiry-day tue|thu`, `--price-only`, `--no-proxy`, `--json`. Run after 15:30 IST on daily bars.

## Volume: the India data problem

Yahoo's `^NSEI` and `^NSEBANK` usually carry zero or patchy volume. The script checks this (≥80% of
recent sessions must have non-constant volume) and then:
1. `--volume-csv` / `--volume-symbol`: volume from another series matched by date. Use NIFTYBEES or
   BANKBEES (ETF), or continuous NIFTY futures exported from your broker or TradingView. Futures
   volume jumps in the monthly rollover week (last Tuesday), so treat DDs there with suspicion.
2. With `--symbol NIFTY` or `BANKNIFTY` it fetches NIFTYBEES/BANKBEES volume automatically.
3. Otherwise it runs **price-only** and says so. In this mode a heavy-selling day is a fall of at
   least 0.75% closing in the lower half of its range, and a follow-through needs only the gain and an
   upper-half close. Report the result as lower-confidence. Never call it "distribution" without volume.

Sessions after an abnormally thin one (Muhurat trading, special Saturday sessions) are not judged,
because beating a thin session's volume proves nothing.

## Signals and how to read them in India

| Signal | Rule in regime.py | Indian reading |
|---|---|---|
| Distribution day | Close −0.2% or worse on higher volume than the prior session. Counts for 25 sessions incl. the day, or until a close 5% above it | 4–5 inside 25 sessions = institutions selling into strength. Carries more weight when NSE provisional data shows a multi-day FII cash-selling streak. Heavy DII/SIP buying often turns FII selling into flat or small-down days |
| Stalling day (`--stalling`, half weight) | Gain of 0–0.4% on higher volume near the 25-session high, closing in the lower half of the range | Churning at the top. Common before results-season disappointments |
| Correction | Close 5% below the cycle peak | Starts the bottoming watch |
| Rally attempt | First up close after the correction low. Fails if that low is undercut | Days 1–3 prove nothing. Short-covering into weekly expiry often creates them |
| Follow-through (FTD) | Day 4 or later of the attempt, gain ≥ threshold on higher volume | Confirms a new uptrend. It fails if price later closes below the rally low; many do |
| Trend/duration | Close vs 50/200 DMA, 50 DMA slope, drawdown from 52-week high, sessions since high/low | Depth: <3% near highs, 3–5% pullback, 5–10% correction, 10–20% deep, 20%+ bear |
| India VIX (`--vix`) | <13 calm, 13–17 normal, 17–22 elevated, 22–30 stressed, 30+ panic | VIX ≥ 22 caps exposure at 50% |

**FTD threshold default.** The script uses 1.5 × the 250-session standard deviation of daily returns,
clamped to 1.0–2.0%. NIFTY's daily σ is usually 0.7–0.9%, so this lands near **1.1–1.3%**, and
higher for BANKNIFTY. A fixed US-style 1.5–1.7% hurdle would almost never fire on NIFTY. Pass
`--ftd-pct` to fix it (for example 1.2 for NIFTY or 1.5 for BANKNIFTY).

**Event days.** Pass Budget day, RBI policy days, election-result days, MSCI/FTSE rebalance days
(huge closing-auction volume) and Muhurat sessions to `--ignore` if they distort volume. DDs that
land on the weekly-expiry weekday are tagged (`--expiry-day`: tue for NIFTY, the default; thu for
SENSEX). Weigh them lighter if your volume source is futures or the ETF. A market-wide
circuit-breaker day (±10/15/20% on NIFTY or SENSEX, see `indian-market-structure`) is tagged. It
means the regime has already broken, so don't wait for a DD count.

## Regime → exposure

| Label | When | Exposure ceiling | New positions |
|---|---|---|---|
| Confirmed uptrend | No correction, < 5 DDs, above 50 DMA, score < 50 | 100% (score < 25) / 80% | 5 / 4 |
| Confirmed uptrend (fresh FTD) | FTD in the last 10 sessions and score < 60 | 50% | 3 starter-size |
| Uptrend under pressure | ≥ 5 DDs in 25 sessions, ≥ 4 in 15, below 50 DMA, or score ≥ 50 | 60% / 40% if score ≥ 50 | 2 / 1 |
| Uptrend under pressure (fresh FTD) | FTD in the last 10 sessions but score ≥ 60 | 30% | 2 pilots |
| Rally attempt | Bouncing from the correction low, no FTD yet | 25% | 1 pilot, half size |
| Correction | ≥ 5% below the cycle peak, no rally attempt | 20% (10% if 10%+ deep) | 0 |

The risk score combines distribution (35 points), trend (30), drawdown (20) and VIX (15 if given),
scaled to 100, minus 10 during a live follow-through. It is a heuristic, not a probability.
"What would change the label" lists the exact closes to watch: DD expiry and clearing levels, the
50 DMA, the correction trigger, the FTD close needed, and the rally low.

## How other skills use the regime

- `india-market-analyst`: put the label, score and ceiling in the first line of any trade view.
  Don't recommend fresh breakouts in Correction.
- `position-sizing`: scale risk per trade with the regime. Confirmed: 1%. Under pressure: 0.5–0.75%.
  Rally attempt or fresh FTD: 0.25–0.5% pilots. Correction: no new risk. Total deployed capital stays
  below the ceiling.
- `trailing-stops` / `stop-loss-strategies`: under pressure, tighten trails to 1.5 × ATR and book
  partial profits. In Correction, honour every stop.
- `technical-analysis`: a stock setup with a weak regime needs strong relative strength vs NIFTY.
- `fno-options-analysis`: a correction with high VIX favours defined-risk spreads over naked selling.

## Caveats

- The index is not your portfolio. Midcaps and smallcaps can diverge for months. Run it on NIFTY
  MIDCAP 100 or SMALLCAP data too if that is where you trade.
- It uses daily closes only. Intraday reversals and gap risk (global cues, GIFT Nifty) are not seen.
- ETF volume includes market-maker and arbitrage flow. It is a participation proxy, not institutional
  flow. Cross-check with FII/DII figures via `market-pulse`.
- Thresholds are conventions, tuned for NIFTY's lower volatility. Check `--as-of` replays on past
  corrections (Mar 2020, Oct 2024–Mar 2025) before you trust the defaults.

## Output

```
Regime: [label] | risk score s/100 | data as of [date] IST close, volume: [source / price-only]
Exposure ceiling: x% | max new positions: n | stance: ..
DDs: d5 a | d15 b | d25 c (oldest drops out in k sessions; clears ≥ ..) | FTD state: ..
Trend: vs 50 DMA ..% | vs 200 DMA ..% | drawdown ..% (depth class), .. sessions since high
Watch: [levels that change the label]
```
_Educational analysis, not investment advice._
