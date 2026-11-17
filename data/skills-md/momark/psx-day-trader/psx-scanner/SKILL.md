---
name: psx-scanner
description: >-
  PSX Chart Scanner. Reads the Pakistan Stock Exchange symbol universe from
  dps.psx.com.pk, filters to the Regular Market common stocks (optionally to
  KSE-100, KMI-30 or the Shariah-screened KMI-ALL list), runs a pre-open
  scan of daily closes (20-day closing-high breakout, bull flag, reclaim
  20-day MA, oversold, oversold bounce) and an intraday opening-range
  breakout scan on 5-minute bars bucketed from PSX intraday ticks, then
  writes psx/watchlist.json for psx-news and psx-entry. Free PSX Data
  Portal data, bar by bar, Asia/Karachi time. Use when the user says
  "scan the PSX", "find me PSX setups", "KSE-100 breakouts", "KMI-30
  Shariah setups", "scan for bull flags on PSX", "oversold PSX stocks",
  "pre-open PSX scan", "build my PSX watchlist", "what should I look at
  today on the exchange", or at the start of a PSX trading day before
  /psx-news.
argument-hint: "[universe | daily | orb] [--index KSE100|KMI30|KMIALL] [--shariah] [--at HH:MM]"
---

# psx-scanner

The PSX Chart Scanner is the first step of a day trade on the Pakistan Stock
Exchange. It reads the free charts the PSX Data Portal publishes and lists
the ones that match a rule. That is all it does. A scan is a list of charts
that match a rule, not a list of stocks to buy, and a setup on a chart is
not a prediction. **Most people who day trade lose money; the scanner does
not change that.** It only saves you from flipping through 500+ charts by
hand.

`${CLAUDE_SKILL_DIR}` below is this skill's folder (where this SKILL.md lives).

```bash
python3 "${CLAUDE_SKILL_DIR}/scan.py" universe                       # -> psx/universe.txt
python3 "${CLAUDE_SKILL_DIR}/scan.py" universe --index KSE100        # only KSE-100 constituents
python3 "${CLAUDE_SKILL_DIR}/scan.py" universe --index KMI30         # Shariah-screened KMI-30
python3 "${CLAUDE_SKILL_DIR}/scan.py" universe --shariah             # all Shariah-compliant (KMI-ALL)
python3 "${CLAUDE_SKILL_DIR}/scan.py" daily                          # before the open -> psx/watchlist.json
python3 "${CLAUDE_SKILL_DIR}/scan.py" daily --symbols OGDC,HUBC,LUCK  # or --watchlist FILE, --limit 200
python3 "${CLAUDE_SKILL_DIR}/scan.py" orb                            # after 09:47 PKT -> psx/watchlist.json
python3 "${CLAUDE_SKILL_DIR}/scan.py" orb --at 10:15                 # cut the clock at 10:15 PKT
python3 "${CLAUDE_SKILL_DIR}/scan.py" orb --watchlist psx/watchlist.json --json
```

Flags: `--min-price 5` (PKR), `--min-volume` (daily 100,000; orb 0),
`--or-minutes 15`, `--max-confirm 200` (orb stage 2),
`--now "2026-11-17 10:15"` (Asia/Karachi time) to pin the clock,
`--offline PATH` to point PSX_FIXTURES_DIR to a captured-fixtures folder.

## What each sub-command does

**universe.** Pulls `/symbols` from dps.psx.com.pk, keeps Regular-Market
common stocks (`isETF==false` and `isDebt==false`), and, if asked, filters
to a single index's constituents. Writes one symbol per line to
`psx/universe.txt`. This file is the list of charts the daily and ORB
scans look at. Re-run it once a week.

**daily.** For each symbol in the universe (or the list you pass with
`--symbols` or `--watchlist`), pulls `/timeseries/eod/{SYM}` and applies
five rules to the closes:

- **breakout_20d** — today's close is above the 20-day closing high.
- **bull_flag** — the stock rose >= 10 % in 2-10 days, then pulled back
  3-8 % over the last 3-7 days on lower volume.
- **reclaim_ma20** — today closed above the 20-day moving average for
  the first time in 5+ days.
- **oversold** — today's 14-day RSI closed below 30.
- **oversold_bounce** — yesterday's RSI was below 30, today's close is
  up on volume.

Writes `psx/watchlist.json`:
```json
{
  "scope": "daily", "date": "2026-11-17",
  "setups": [
    {"symbol": "OGDC", "rule": "breakout_20d", "close": 316.20,
     "prev_close": 313.39, "volume_m": 3.04, "idx": ["KSE100"]}
  ]
}
```

**orb.** For each symbol in the watchlist, pulls `/timeseries/int/{SYM}`,
buckets the ticks into 5-minute bars using Asia/Karachi time, finds the
opening range (first 15 minutes from 09:32), and lists symbols whose
later bars broke above the range high or below the range low with volume
confirmation. Writes `psx/watchlist.json` with `"scope": "orb"`.

## Universe rules and Shariah filter

By default the universe keeps every PSX common stock in the Regular
Market. `--index KSE100`, `--index KMI30` or `--index KMIALL` narrow
it to that index's constituents (freshly scraped from
`/indices/{index}`). `--shariah` is an alias for `--index KMIALL`.

The author trades only Shariah-compliant stocks (KMI-30 or KMI-ALL),
but the default is open so public forkers see every setup. You decide
what you trust.

## Session and clock

PSX trades Mon-Thu 09:32-15:30 Asia/Karachi, and Friday as a split
session (09:17-12:00 / 14:32-16:30). Ramadan compresses this (see
`psx-alerts` for the full calendar). The scanner refuses to run `orb`
before 09:47 PKT (15 minutes after the open) unless `--at` or `--now`
is passed. Weekends and PSX holidays short-circuit with a no-op.

## Costs are on every plan

The scanner does not size positions or compute net return. It only
surfaces setups. Costs (broker commission, PSX / NCCPL / SECP / CDC
fees, provincial sales tax, CGT) are applied by `psx-budget` and
`psx-exit` later; see `psx/config.json` for the editable cost table.

## Offline mode

`--offline PATH` points `PSX_FIXTURES_DIR` to a folder written by
`tests/scripts/capture_fixtures.py`. The scanner then reads from disk
and never touches the network - useful for tests, backtests, and
re-running a scan as of a past date.
