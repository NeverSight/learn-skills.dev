---
name: psx-scanner
description: >-
  Chart Scanner for the Pakistan Stock Exchange (PSX). Builds the list of
  ordinary shares from the PSX closing file, scans daily closes before the
  open (20-day closing-high breakout, bull flag, back over the 20-day
  average, oversold, oversold bounce), records the market tape from the PSX
  screener in the session (only with "psx_site": true), and scans that tape
  for opening-range breakouts on 5-minute bars. Leaves out the shares on
  your blocked list, and says which. In swing style, run the daily scan
  after the close; orb and tape are day tools. Writes psx/watchlist.json
  for psx-news, psx-entry and psx-exit. Use when the user says "scan the
  market", "scan PSX", "find me setups", "find swing setups", "what is
  breaking out", "opening range breakouts", "oversold stocks", "pre-market
  scan", "build my watchlist", "what should I look at today", or at the
  start of a trading day before /psx-news.
argument-hint: "[universe | daily | tape | orb] [--at HH:MM]"
---

# psx-scanner

The Chart Scanner is the first step of a trade on PSX: a day trade or a
swing trade. It reads the charts and lists the ones that match a rule.
That is all it does.

- A scan is a list of charts that match a rule, not a list of stocks to buy.
- A setup on a chart is not a prediction.
- Most people who day trade lose money. The scanner does not change that.
- Swing trading loses money for many people too. Try it on paper first, in a
  folder of its own. Never turn paper on in a folder that holds real shares or
  real cash. See "Swing style" below.
- It only saves you from flipping through 450 charts by hand.

`${CLAUDE_SKILL_DIR}` below is this skill's folder (where this SKILL.md lives).

```bash
python3 "${CLAUDE_SKILL_DIR}/scan.py" universe                    # -> psx/universe.txt
python3 "${CLAUDE_SKILL_DIR}/scan.py" daily                       # before the open -> psx/watchlist.json
python3 "${CLAUDE_SKILL_DIR}/scan.py" daily --symbols OGDC,HUBC   # or --watchlist FILE, --limit 50
python3 "${CLAUDE_SKILL_DIR}/scan.py" tape                        # in the session: record the tape (site on)
python3 "${CLAUDE_SKILL_DIR}/scan.py" orb                         # after 9:50 AM PKT -> psx/watchlist.json
python3 "${CLAUDE_SKILL_DIR}/scan.py" orb --at 10:15              # cut the clock at 10:15 AM PKT
python3 "${CLAUDE_SKILL_DIR}/scan.py" orb --watchlist psx/watchlist.json --json
```

Flags:

- `--data DIR` (default `psx/data`), `--config FILE` (default `psx/config.json`),
  `--offline` (never use the network).
- `--min-price 10` (rupees) and `--min-volume` (daily 500,000 shares, orb 0).
- daily: `--sessions 60`. orb: `--or-minutes 15`, `--at HH:MM`, `--until HH:MM`,
  `--tape FILE`. tape: `--every 120`, `--until HH:MM`.
- `--now "2026-10-29 10:15"` (Karachi time) pins the clock. Also `--universe FILE`,
  `--out FILE`, `--no-write`, `--show N`, `--quiet`, `--json`.
- Exit code 0 when the scan found something. 1 when it found nothing or could
  not run. The reason is one plain line.

## What it reads and writes

| file | what |
| --- | --- |
| `psx/data/mkt_summary/YYYY-MM-DD.Z` | read: the PSX closing files, one a session |
| `psx/data/symbol_name/YYYY-MM-DD.zip` | read when it is there: full names, to tell share kinds apart. With the site on, `universe` saves it once for the newest closing day |
| `psx/data/tape/YYYY-MM-DD/market.jsonl` | written by `tape`, read by `orb`: one screener snapshot a line |
| `psx/universe.txt` | written by `universe`: one `SYMBOL\|Name\|Sector code` a line, read by `daily` and `orb` |
| `psx/watchlist.json` | written by `daily` and `orb`: `mode`, `as_of`, `universe`, `scanned`, `failed`, `hits[]`. Each hit has `symbol`, `name` and `sector`. psx-news reads `symbol` and `name`, psx-entry reads `symbol` and `level`. In swing style, psx-exit reads the hit's setup and `level`. `blocked_left_out` is there only when a share on your blocked list matched |
| `psx/config.json` | read: `psx_site`, `blocked` (daily and orb), `style` (`"day"` or `"swing"`; in swing, orb and tape print a note), `no_entries_after` (orb), `data_delay_minutes` (tape), `holidays`, `open_days`, `ramadan` |

## The universe

`universe` reads the newest 20 closing files in the data folder (about a month).

- A share is kept when it traded on any of those 20 days. So a share that did
  not trade on the newest day is still kept. psx-risk reads this list.
- A share's kind and sector come from its newest row.
- It adds full names from the symbol name file, when that file is there.
  Without it, the short names of the closing file are used.
- It keeps the ordinary shares only. A class B share (like PIAHCLB) counts as ordinary.
- It leaves out GEM board shares, non-voting and preference shares, rights,
  ETFs, modarabas, REITs, closed-end funds, debt, stock futures and index futures.
- It tells them apart by the sector code (36 debt, 40 stock futures, 41 index
  futures, 0806, 0819, 0836, 0837 funds) and by the name ("(R)", "(Pref)",
  "Non-Voting", a GEM symbol).
- A share with no trade on any of the 20 days is not kept.
- Today's file counts only after today's close.
- It prints how many it kept, and how many of each other kind it left out.
  When it kept a share with no trade on the newest day, it says how many.

On the real files up to 2026-10-29, the newest file has 1,049 rows. The tool
keeps 455 ordinary shares: 446 traded on 10-29, and 9 only in the 19 sessions before.

## The daily scan (before the open)

- It reads the newest 60 closing files (`--sessions`), about 3 months.
- Today's file counts only after the close. So a scan before the open uses
  closes up to the last session.
- A chart needs 30 closes or more. A day with no regular-board trade is skipped.
- Floors on the last session:
  - a close of Rs 10 or more (`--min-price`). Under Rs 10 the Rs 0.03 a share
    minimum commission makes a round trip cost 0.7% or more.
  - 500,000 shares or more traded (`--min-volume`).
- PSX closing files are not adjusted for payouts. On an ex-date (XD, XB, XR)
  or a split, the file's LDCP is the last close after the payout. The scan
  scales the older closes by LDCP / the close before. So a dividend does not
  look like a fall.
- A PSX session with no closing file in the window gets a "Note:" line.
  Closes are never scaled across it, because its close is not known. Save
  the file, or, if PSX was closed that day, add it to `holidays` in psx/config.json.
- The CLOSE in the file is the official close: about a 30-minute average, not the last trade.

| setup | the rule on closes |
| --- | --- |
| `breakout_20d` | the last close is above every close of the 20 sessions before it |
| `bull_flag` | up more than 10% over the 10 sessions before the last 5, then the last 5 closes inside a 5% range |
| `reclaim_ma20` | the close before was under its 20-day average, the last close is above it |
| `oversold` | RSI 14 (Wilder) under 30 |
| `oversold_bounce` | RSI 14 was under 30 the session before, and the last close is up |

- Hits are listed most traded first (close x volume).
- Each hit has `close`, `close_date`, `rsi`, `volume` and `level`, the price the setup broke:
  - `breakout_20d`: the top close of the 20 sessions before.
  - `reclaim_ma20`: the 20-day average (with the last close), half up to 0.01.
  - the others: `null`.

## Your blocked list

`"blocked"` in psx/config.json lists the shares you never want to trade here.
For example, the shares you hold for the long term.

- `daily` and `orb` leave them out of the hits, in both styles.
- They are still read, so the counts (symbols, scanned) stay the same.
- When a blocked share matched a setup, one line says so. It names only the
  blocked shares that matched, most traded first:
  `Left out 3 on your blocked list: HUBC, UBL, PPL.`
- psx/watchlist.json then has `"blocked_left_out"` with the same names.
  When no blocked share matched, there is no line and no key.
- With `"blocked": []` (the default) the scan is the same as before.
- `universe` keeps every ordinary share: psx-risk reads that list. psx-budget
  and psx-risk refuse a buy of a blocked share by themselves.
- `tape` keeps every price on the screener: psx-alerts reads the tape for the
  shares you hold.
- Write the list like this: `["HUBC", "UBL"]`. One string, `"HUBC, UBL"`, works
  too. Anything else stops the scan with one plain line.

The sample market, with `"blocked": ["LUCK", "DEMO"]` in psx/config.json,
after `scan.py universe`:

```
python3 scan.py daily --data tests/fixtures/psx-market --now "2026-10-29 09:00"
Daily scan, Thu 2026-10-29 9:00 AM PKT. Closes through Wed 2026-10-28: 60 PSX closing files from 2026-08-04.
31 symbols. 28 passed the floors (close Rs 10 or more, 500,000 shares or more on 2026-10-28). 28 scanned.
5 charts matched a setup. By setup: bull flag 1, back over the 20-day average 1, oversold (RSI under 30) 2, oversold bounce 1.
Left out 2 on your blocked list: LUCK, DEMO.
Most traded first (close x volume):
  PSO      418.00  RSI  33.8  oversold bounce
  PPL      188.00  RSI  74.8  bull flag
  UBL      392.00  RSI  53.6  back over the 20-day average (level 388.05)
  TRG       74.80  RSI  12.4  oversold (RSI under 30)
  SEARL    104.50  RSI  12.3  oversold (RSI under 30)
Wrote psx/watchlist.json (mode daily, 5 hits).
A scan is a list of charts that match a rule, not a list of stocks to buy. Next: pick one chart, then /psx-news SYMBOL.
```

- LUCK and DEMO matched a 20-day closing-high breakout. They are on the
  blocked list, so they are not hits.
- psx/watchlist.json has `"blocked_left_out": ["LUCK", "DEMO"]`.

## The tape (during the session)

- `tape` reads the PSX screener every 120 seconds (`--every`, 60 to 300).
- Each read is one line in `psx/data/tape/YYYY-MM-DD/market.jsonl`, with the
  price of every listed share.
- The screener has no time of its own, and it is about 5 minutes late. So a
  line's `asof` is the fetch time minus 5 minutes (`data_delay_minutes`).
- Start it in the pre-open or in the session. It stops at `--until`, or once
  the tape has seen the close (about 5 minutes after it).
- It does not read the screener while no bar can change:
  - before the first bar shows on the late screener: 9:35 AM Mon to Thu,
    9:20 AM on a Friday and in Ramadan,
  - in the Friday Juma break, once the tape has seen 12:00. It reads again at 2:35 PM.
- It needs `"psx_site": true`. Without it, it prints one line and stops.
  A saved screener page cannot make a tape. Without the site, use a bars
  file from your broker with psx-entry.
- Run only one tool that polls the PSX site at a time (this one, `entry.py
  watch`, or alerts on a loop). Each tool keeps its own 1.5 s gap only.
- Ctrl+C stops it. Every line written so far stays.

## The opening-range breakout scan (during the session)

- The opening range is the first `--or-minutes` (15) of the first segment:
  - Mon to Thu: the 9:30, 9:35 and 9:40 bars.
  - Friday and Ramadan: the 9:15, 9:20 and 9:25 bars.
- The 5-minute bars come from the day's tape. A snapshot goes into the bar
  that holds its `asof`.
- The screener shows prices only. So a bar's high and low are only the prices
  the tape saw, about 5 minutes late. A peak between two snapshots is missed.
- Only snapshots as of the cutoff (now, `--now` or `--at`) or before are
  used. So a replay sees only what the tape held then, like psx-entry.
- A bar counts only once it is complete:
  1. it ended by the cutoff, and
  2. the tape has a snapshot at or after its end.
- A chart is usable when every bar from the open to the last complete bar is
  there. A missing bar means the screener lost the share for a while.
- A hit is the first complete bar after the range that CLOSES above the range
  high, at that bar's close time.
- Floors: `--min-price 10` on the last complete bar's close, `--min-volume 0`
  on the last closing file.
- Bar numbers count across the day's segments. Bar 0 is 9:30 (Mon to Thu) or
  9:15 (Friday, Ramadan). On a Friday the 14:30 bar is bar 33.
- A share that did not trade today still shows on the screener at its last
  price. It looks flat all day.
- It prints one plain line and writes nothing:
  - on a weekend or a PSX holiday,
  - before the range plus one bar is done (9:50 AM Mon to Thu, 9:35 AM on
    Friday and in Ramadan),
  - after the close,
  - after `no_entries_after` (an expired setup). The config time is for Mon
    to Thu: 15:00 is 16:00 on a Friday and 13:00 in Ramadan.

## Swing style

In swing style (`"style": "swing"` in psx/config.json) you hold a share for
days, not minutes. The scanner works the same way. Only the time to run it changes.

- Run `scan.py daily` after the close, once the day's closing file is out.
  The file shows about 30 to 40 minutes after the close (3:30 PM Mon to Thu,
  4:30 PM on a Friday, earlier in Ramadan). Then the scan has that day's close.
- Before the close, it uses the closes up to the day before. After the close,
  until the file is out, a "Note:" line says the newest file is old.
- The hits are setups for the next session. psx-exit plans the buy from the
  closing files: the limit price, the stop, the target and the exit-by day.
  The scanner adds no swing fields.
- `orb` and `tape` are day tools: they work on the 5-minute bars of one
  session. In swing style they still run, but first they print one note:
  `orb and tape are for day trades; your style is swing.`
- When auto-run (psx-autorun) is installed, `scan.py daily` runs by itself
  after the close and each morning.
- Swing trading loses money for many people too. Try it on paper first, in a
  folder of its own. Never turn paper on in a folder that holds real shares or
  real cash. A paper fill can go into that folder's `psx/portfolio.json`, next
  to your real shares. Then its cash and shares no longer match your broker app.
- To make the paper folder, copy `psx/config.json` and `psx/data/` into the new
  folder's `psx/`. Set `"paper": true` and `"style": "swing"` there. Do not
  copy `psx/portfolio.json`: it holds the real shares and cash.
- Auto-run does not scan the paper folder. It scans only the trading folder
  you gave it at install. In the paper folder, run the scans yourself:
  `scan.py universe` first and once a week, `scan.py daily` after each close.

## Data and limits

- Default: the data folder only (`psx/data`, or `--data`). Save files there with your browser:
  - closing files from `https://dps.psx.com.pk/download/mkt_summary/YYYY-MM-DD.Z`
    as `mkt_summary/YYYY-MM-DD.Z`,
  - the symbol name file from `https://dps.psx.com.pk/download/symbol_name/YYYY-MM-DD.zip`
    as `symbol_name/YYYY-MM-DD.zip`.
- A day's closing file shows about 30 to 40 minutes after the close.
- PSX's terms ban automated tools without its written permission. So the PSX
  site is used only with `"psx_site": true` in psx/config.json, never with
  `--offline` or `--now` (a replay never fetches). Turn it on only if PSX has given you permission
  (marketdatarequest@psx.com.pk). Plain GETs, at least 1.5 s apart.
- With the site on, a missing closing file is fetched once and saved. A 404
  means no session that day, or the file is not out yet.
- PSX has no free intraday bars. Without the site there is no tape, so `orb`
  has nothing to read. psx-entry can use a bars file from your broker instead.
- Free PSX data is about 5 minutes late. The tool never calls it real time.
- Partial results are said as partial: "2 symbols, 1 with closes (1 had none)".
- When the newest closing file is older than the last session, the scan says so
  in a "Note:" line. Old closes are never passed off as new.
- The PSX calendar (holidays, Friday hours, Ramadan hours) is built in for 2026
  and 2027. The 2027 moon dates are expected only: fix them in psx/config.json
  (`holidays`, `open_days`, `ramadan`) when PSX announces them.

## Steps

1. Once a week or so, after a close: `scan.py universe`.
2. Before the open: `scan.py daily`. Tell the user the counts (symbols, passed
   the floors, scanned, hits) and the top few by setup. If it left out shares
   on the blocked list, say which ones.
   In swing style, run it after the close instead, once the closing file is out.
3. Day style, in the session, only if the site is on: `scan.py tape`. It runs to
   the close. Do not run another tool that polls the PSX site at the same time.
4. Day style, after 9:50 AM PKT (9:35 AM on a Friday or in Ramadan):
   `scan.py orb`. Tell the user how many usable charts broke their range, and
   when. Say a later hit is closer to the price now, and the data is about
   5 minutes late.
5. The user picks one chart. Hand it on: `/psx-news SYMBOL` (what is moving
   it), then `/psx-entry SYMBOL` (the entry, bar by bar). Never pick for them.
   In swing style: `/psx-news SYMBOL`, then `/psx-exit` plans the buy for the
   next session. psx-entry is not used in swing.

## Example: Thursday 2026-10-29

This is the sample market in `tests/fixtures/psx-market/`. It is made up.
DEMO ("Demo Industries Limited") is a made-up company.

Before the open, closes up to Wed 10-28. The 10-29 file is in the folder, but
it is from after the close, so it is left out:

```
python3 scan.py universe --data tests/fixtures/psx-market --now "2026-10-29 09:00"
PSX closing file of Wed 2026-10-28: 43 rows; names from 2026-10-29.zip (41 symbols).
Kept 31 ordinary shares.
Left out 12: 3 stock futures, 1 debt, 1 ETF, 1 GEM board share, 1 index future, 1 modaraba, 1 non-voting share, 1 preference share, 1 REIT, 1 right.
Wrote psx/universe.txt (one SYMBOL|Name|Sector code a line).

python3 scan.py daily --data tests/fixtures/psx-market --now "2026-10-29 09:00"
Daily scan, Thu 2026-10-29 9:00 AM PKT. Closes through Wed 2026-10-28: 60 PSX closing files from 2026-08-04.
31 symbols. 28 passed the floors (close Rs 10 or more, 500,000 shares or more on 2026-10-28). 28 scanned.
7 charts matched a setup. By setup: 20-day closing-high breakout 2, bull flag 1, back over the 20-day average 1, oversold (RSI under 30) 2, oversold bounce 1.
Most traded first (close x volume):
  PSO      418.00  RSI  33.8  oversold bounce
  PPL      188.00  RSI  74.8  bull flag
  UBL      392.00  RSI  53.6  back over the 20-day average (level 388.05)
  LUCK     468.00  RSI  65.5  20-day closing-high breakout (level 461.80)
  TRG       74.80  RSI  12.4  oversold (RSI under 30)
  DEMO      98.40  RSI  75.7  20-day closing-high breakout (level 96.56)
  SEARL    104.50  RSI  12.3  oversold (RSI under 30)
Wrote psx/watchlist.json (mode daily, 7 hits).
A scan is a list of charts that match a rule, not a list of stocks to buy. Next: pick one chart, then /psx-news SYMBOL.
```

- Out on price: CNERGY 8.25 and KEL 6.12. Out on volume: NML, 319,100 shares.
- DEMO closed at 98.40, over 96.56, the top close of the 20 sessions before.

At 10:16, from the day's tape (one screener snapshot every 2 minutes). In a
replay, `--now` is the tape's own time, and later snapshots are not used:

```
python3 scan.py orb --data tests/fixtures/psx-market --now "2026-10-29 10:16" --min-price 0
Opening-range breakout scan, Thu 2026-10-29 10:16 AM PKT: 15-minute range (9:30 AM to 9:45 AM), 5-minute bars from the market tape.
Tape: 23 screener snapshots, as of 9:32 AM to 10:16 AM PKT. Bars that ended by 10:16 AM count.
The screener is about 5 minutes late, and a bar's high and low are only the prices the tape saw.
31 charts on the tape. 30 usable (PIOC has a missing bar). 30 scanned.
7 of 30 usable charts closed above their opening-range high by 10:16 AM:
   9:50 AM  HUBC     163.16  range 161.35 to 162.41  +0.46% over   (bar 3)
   9:55 AM  OGDC     283.29  range 280.98 to 281.90  +0.49% over   (bar 4)
  10:00 AM  FFC      525.38  range 523.30 to 523.77  +0.31% over   (bar 5)
  10:00 AM  KEL        6.14  range 6.10 to 6.12      +0.33% over   (bar 5)
  10:05 AM  MEBL     442.89  range 440.32 to 441.65  +0.28% over   (bar 6)
  10:10 AM  ENGROH   262.70  range 261.24 to 261.65  +0.40% over   (bar 7)
  10:15 AM  DEMO     100.65  range 98.90 to 100.20   +0.45% over   (bar 8)
Wrote psx/watchlist.json (mode orb, 7 hits).
A scan is a list of charts that match a rule, not a list of stocks to buy. Next: pick one chart, then /psx-news SYMBOL and /psx-entry SYMBOL.
```

- DEMO's range is the 9:30, 9:35 and 9:40 bars: high 100.20, low 98.90.
- The 10:10 bar (bar 8) closed at 100.65, 0.45% over the high, at 10:15 AM.
- With `--now "2026-10-29 10:15"` the tape reaches only 10:14. The 10:10 bar
  has ended, but no snapshot shows that yet. So DEMO is not a hit yet: 6 hits.
  The 10:16 snapshot shows it. psx-entry on this tape says the same.
- PIOC is not usable: the screener lost it in two snapshots, so its 9:55 bar is empty.
- With the default Rs 10 floor, KEL (6.14) and CNERGY (8.25) are left out:
  28 scanned, 6 hits.
- On the real clock the tape is about 5 minutes behind. The 10:16 snapshot is
  fetched at 10:21.
- The user picks DEMO. Claude hands it to `/psx-news DEMO`, then `/psx-entry DEMO`.

## Rules

- Say what was scanned: how many symbols, how many had closes or were on the
  tape, how many were usable, and the time of the data.
- Say the data is about 5 minutes late, and tape highs and lows are only the
  prices the tape saw.
- Say "matched a rule", never "a buy", "a winner" or "a good trade".
- Never print a P&L, a return or a profit figure.
- A hit is stale once the price has moved on. Run the scan again before acting on it.
- A share on the blocked list is never a setup here. Never suggest one. Say
  which ones the scan left out.

## What it never does

It never places, sizes or checks an order. It never says which stock to buy.
It never calls data real time, and never promises that a setup works. It never
uses the PSX site unless the user turned it on in their own config.

## Safety

- Education and tooling, not financial advice. A PASS is a rules check, not a recommendation.
- Paper trading by default (`"paper": true`). Going live is the user's own decision, in their own config.
- Nothing in this pack places an order. psx-broker shows the order and waits. It prints the line to
  type into the broker app only after psx-risk passed that exact order today and the user typed an
  explicit yes for that one order in the chat. The user then places it in their own broker's app.
  If the user ever adds a broker tool that can place orders, set it to "Needs approval"
  (Customize > Connectors > tool permissions), never "Always allow".
- Long only. No short selling (PSX bans blank sales), no margin, no futures and no options.
- Broker logins, passwords and PINs never go in the chat.
