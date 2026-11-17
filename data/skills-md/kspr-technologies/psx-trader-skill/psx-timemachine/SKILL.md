---
name: psx-timemachine
description: >-
  Time Machine for the Pakistan Stock Exchange (PSX). Replays a planned trade
  before you risk a rupee: 10,000 simulated runs, plus the same rule on past
  days. Takes the plan from psx-exit (entry, stop, target). A day plan replays
  the rest of the session. With 20 or more past sessions of the stock's own
  5-minute bars it replays those bars (bars mode). Without them it uses a
  simpler model from the last 60 daily bars (daily mode), and says so. A swing
  plan replays the next 20 sessions, one daily bar at a time, gaps at the open
  included (swing mode). Prints the odds of target first, stop first or neither,
  where the price may end, the average R with PSX costs counted, and one honest
  verdict. Use when the user says "run the time machine", "replay this trade",
  "what are the odds", "simulate this trade", "monte carlo", "backtest this
  setup", "how often does this hit the target", "is this a coin flip", or after
  /psx-exit writes a plan, before /psx-budget.
argument-hint: "[path to plan.json, or SYMBOL]"
---

# psx-timemachine

The Time Machine sits between the plan and the money. psx-exit has set the
entry, the stop and the target. Before anything is sized, this skill asks
one question.

If today plays out like the stock's own past days, how often does this plan
hit the target first, the stop first, or neither? It answers with 10,000
replays and with the real record of the same rule on past days.

It is a simulation, not a prediction. Day trading loses most people money,
and a good-looking replay does not change that.

A swing plan gets its own mode (see "Swing mode" below). Its replays walk the
next 20 sessions, one day at a time. Swing trading loses money for many
people too.

`${CLAUDE_SKILL_DIR}` below is this skill's folder (where this SKILL.md lives).

```bash
python3 "${CLAUDE_SKILL_DIR}/timemachine.py" run                # psx/plan.json to its flat_by, 10,000 replays, seed 19
python3 "${CLAUDE_SKILL_DIR}/timemachine.py" run --write        # also save psx/timemachine.json
python3 "${CLAUDE_SKILL_DIR}/timemachine.py" run --mode daily   # the daily model, even with bars
python3 "${CLAUDE_SKILL_DIR}/timemachine.py" run --json
python3 "${CLAUDE_SKILL_DIR}/timemachine.py" run --symbol DEMO --date 2026-10-29 \
    --entry 100.65 --stop 99.55 --target 101.75 --entry-time "10:15 AM"
python3 "${CLAUDE_SKILL_DIR}/timemachine.py" chart --from       # ASCII fan chart of the saved run
python3 "${CLAUDE_SKILL_DIR}/timemachine.py" run --sessions 10  # a swing plan: 10 sessions, not to its exit-by day
```

Other flags:

- `--mode auto|bars|daily` (default auto: it picks and says why). A swing
  plan always runs swing mode.
- `--sessions N`: a swing plan only. It replays the buy day and the N
  sessions after it. The default is the plan's `max_hold_sessions` (20), so
  the replays end on its exit-by day.
- `--replays N`, `--seed N` (default 19), `--window N` (bars mode, default 2 bars).
- `--until HH:MM`: a day plan only. End each replay then. The default is the plan's
  `flat_by` (psx-exit has moved it to the day's hours: 16:20 on a Friday).
  A plan with no `flat_by` runs to the close. The output says which one.
- `--data DIR` (default `psx/data`), `--config FILE` (default `psx/config.json`).
- `--offline`: never use the network, read only the data folder.
- `--now "2026-10-29 10:20"` (Karachi time) to pin the clock. It replays a
  past time, so it reads only the data folder too.

## What it reads and writes

| file | what |
| --- | --- |
| `psx/plan.json` | the plan from psx-exit: symbol, date, entry, entry_time / entry_bar, stop, stop_rule, target, target_r, opening range, the day's price limits, flat_by (where the replays end), and a `costs` block if it has one. A swing plan (`"style": "swing"`) has the buy day, the limit entry, stop, target, `max_hold_sessions`, `exit_by`, `trend_sessions`, the last close and the buy day's price limits |
| `psx/data/bars/<SYM>.csv` | bars mode: 5-minute or 1-minute bars you export from your broker (Karachi times) |
| `psx/data/tape/YYYY-MM-DD/<SYM>.jsonl` | bars mode: company page snapshots the pack's tools recorded, for days the bars file does not have |
| `psx/data/mkt_summary/YYYY-MM-DD.Z` | daily mode and swing mode: the PSX daily closing files, the last 60 before the plan's day |
| `psx/config.json` | `costs` sets the PSX costs (else the pack's defaults); `holidays`, `open_days` and `ramadan` fix the calendar; `"psx_site": true` lets it fetch a missing closing file; the `swing` block gives `max_hold_sessions` and `trend_exit_sessions` when a swing plan has none |
| `psx/timemachine.json` | with `--write`: `{mode, plan, mc, history}` plus the verdict. `mc` holds the odds, percentiles, the fan-chart bands, 160 sample paths and a 24-bin histogram. In swing mode `mc` holds the outcome counts and shares, the average R, the session each replay ended in, the bands of each session's close, 160 sample paths and the price the buy day starts from (`base`: the last close, or the buy day's LDCP) |

- The PSX site is off by default. Turn it on only if PSX has given you
  permission (marketdatarequest@psx.com.pk).
- When it is on, a missing closing file is fetched once, with a plain
  request, and saved in `mkt_summary/`. A saved file is never fetched again.
- Bars mode never fetches anything. A run with `--offline` or `--now` never
  fetches either.
- The market tape (`market.jsonl`) is not used: it samples each stock too
  seldom to show a bar's real high and low.

## How it works

1. **The mode.** `--mode auto` (the default) picks one and says why.
   - **Bars mode** when there are 20 or more FULL past sessions of the
     stock's own 5-minute bars with the same hours as the plan's day.
   - A Thursday plan uses Mon to Thu sessions. A Friday plan uses Friday
     sessions. A Ramadan plan uses Ramadan sessions.
   - **Daily mode** otherwise. It is a simpler model.
2. **Bars mode: the pool.** Every past bar becomes four ratios to the close
   of the bar before it: open, high, low and close.
   - Bar numbers follow the PSX grid. Bar 0 is the 9:30 bar Mon to Thu, and
     the 9:15 bar on a Friday and in Ramadan.
   - The Friday break has no bars, so the 2:30 PM Friday bar is bar 33.
   - A session with a missing bar is left out. So is a session with other hours.
3. **Bars mode: one replay.** Start at the entry price. For each bar left,
   pick a past bar from the same time of day (plus or minus 2 bars) at
   random, and scale it to the price.
   - A Friday morning bar is never drawn for the afternoon, or the other way.
   - The 2:30 PM Friday bar holds the move over the Juma break. So it is
     drawn only from past 2:30 PM bars, and no other bar uses them.
   - Near the start or the end of a segment there are fewer bars to pick
     from. Each one is still just as likely.
4. **Daily mode: one replay.** It reads the last 60 daily bars before the
   plan's day. A day with no regular-board trade (zero prices) is skipped.
   - It measures how far the stock moves in a day, from its daily highs and lows.
     That is `sigma_day`. (The formula is called the Parkinson method. The
     code has it.)
   - Each 5-minute step is a small random move of that size. Up and down are
     just as likely.
   - The step size is `sigma_day` split over the bars of a full day: 72 Mon
     to Thu, 57 on a Friday, 51 in Ramadan, 39 on a Ramadan Friday.
   - A formula (the Brownian bridge) gives each step's high and low.
5. **Both modes.** Bar by bar (or step by step), it checks the stop first,
   then the target. A bar that touches both counts as the stop.
   - No price goes past the day's price limits: PSX does not allow it.
   - The limits come from the plan (the company page). Without them they are
     computed from the last close (an ex-date would lower them).
6. **10,000 replays** give four odds.
   - Target first. Stop first.
   - Neither: the trade was still open at `--until`. That is the plan's
     `flat_by`. With no `flat_by` it is the close: 3:30 PM Mon to Thu, 4:30
     PM on a Friday, 1:30 PM in Ramadan, 12:30 PM on a Ramadan Friday.
   - Green: target first, or above the entry at `--until`. Green is by price
     alone, before costs.
7. **R counts the PSX costs.** R is the risk a share (entry minus stop).
   - Before costs, a trade is +1R at a 1R target and -1R at the stop.
     Otherwise it is the move from the entry at `--until`, divided by the risk.
   - Then the costs come off: broker commission, sales tax and fees, to buy
     at the entry and sell at the exit. The tool works them out for 1,000
     shares, then turns them into R.
   - The costs settings come from the plan's `costs` block, else from
     `psx/config.json`, else the pack's defaults. One line says how much.
   - A close stop makes the same costs more R. In the example, costs are
     about 0.33R a trade: +0.67R at the target, -1.33R at the stop.
   - A gap through the stop still counts at the stop. A real fill can be
     worse. At a price limit there may be no buyer at all.
8. **The history.** This is what really happened, not a simulation.
   - Bars mode: the plan's own rule (the same opening range, stop rule and
     target R) runs again on every past session in the pool. Each day's R
     counts that day's own costs.
   - Daily mode: the plan's stop and target, as percents of the entry, go on
     each past day from its open. It counts the days that reached the target
     only, the stop only, both, and neither. With both, the order inside the
     day is not known.
9. **The verdict** is one line from the replays. It looks only at the
   replays that hit one side, and asks how often the target came first.
   - A bigger target needs to come first less often to break even. With
     costs, it must come first more often.
   - The break-even share is (1 + c) / (1 + R). c is the costs in R of a trade
     that ends at the stop.
   - With no costs that is 50 % at 1R and 33 % at 2R. With costs of 0.33R it
     is 66 % at 1R and 44 % at 2R.
   - Less than 5 points from break-even: "Close to break-even". (At 1R with
     no costs at all, it says "Close to a coin flip".)
   - 5 to 15 points: "Leans toward the target" or "Leans toward the stop".
   - 15 points or more: "Strongly toward" one of them.
   - When the costs are as big as the target, it says "Costs eat the target".
10. **Below the verdict**, when it applies: a line when more than 40 % of the
    replays hit neither (the price at `--until` decides those), and the
    average R when its sign goes against the lean.

**The seed.** The draws come from Python's `random.Random(seed)`, seed 19 by
default, in a fixed order. Same plan, same data, same seed: the same numbers.
Say the seed with every result, so the user can repeat it.

**What it refuses**, in one plain line:

- A plan that does not make sense: a stop above the entry, an entry off the
  5-minute grid, a sell (PSX bans blank sales), a day PSX is closed.
- An entry bar that has not closed yet by the clock.
- A `flat_by` or `--until` that leaves no bar to replay after the entry.
- A `costs` setting that is not a number of 0 or more.
- Too few sessions: 20 full ones for bars mode, 20 daily bars for daily mode
  and for swing mode.
- A missing closing file when the site is off: it says which file to save where.
- A swing plan with `--mode bars`, `--mode daily` or `--until`. A day plan
  with `--sessions`.

## Swing mode

A swing plan from psx-exit (`"style": "swing"`) runs swing mode by itself,
and the output says why. A swing trade is held for days, so each replay
walks whole days, not 5-minute bars.

1. **The pool.** The stock's last 60 daily bars before the buy day, from the
   closing files.
   - Each bar becomes four ratios to its own LDCP (the reference price PSX
     sets for that day): open, high, low and close.
   - PSX lowers the LDCP on an ex-date. So a payout is not a fall here.
   - A bar with no LDCP is left out.
2. **One replay.** Session 1 is the buy day. Then come the sessions after it,
   up to the exit-by day (20 sessions after the buy day).
   - Each session is one past bar, drawn whole at random and scaled from the
     close before. So a gap from one day to the next is in it.
   - No price goes past that day's price limits.
   - The buy day starts from its own LDCP when the plan's price limits give
     it (from the company page, or from the buy day's closing file). On an
     ex-date that LDCP is under the last close. Then the closes before it
     are scaled the same way, and a note says so.
3. **The buy day.** The plan's buy is a limit buy (by default the last close
   plus 1 %).
   - It opens at or under the limit: it fills at the open. The rules of step
     4 count that day too. An open already under the stop is out at once, at
     that open.
   - Else its low comes down to the limit: it fills at the limit. Then only
     the stop counts that day, because the high may have come first.
   - Else there is no fill. A PSX order lasts one day, so that replay ends.
4. **Each day it is held**, in this order:
   - It opens at or under the stop: out at the open. That is a gap. The loss
     is bigger than at the stop.
   - It opens at or over the target: out at the open.
   - Its low reaches the stop: out at the stop.
   - Its high reaches the target: out at the target.
   - It closes under the lowest close of the 10 sessions before it (the trend
     rule): out at the next open.
   - The exit-by day: out at its close (the time stop).
5. **R** is the move from the fill to the exit, divided by the plan's risk
   (entry minus stop). Then the costs come off.
   - In swing the commission counts on both sides. A sale on a later day
     always pays it, whatever `"day_trade_one_side"` says.
   - A fill at the open under the limit counts from that price.
   - The average R counts only the replays that filled.
6. **The outcomes**: target, stop (and how many were gaps), trend, time and
   no fill.
   - The verdict works as in the other modes: the target against the stop,
     with the costs.
   - A note comes when over 40 % end by the trend rule or the time stop.
7. **The history.** The plan's stop and target, as percents of the entry, go
   on each of those 60 past days from its open. Each one walks forward up to
   20 real sessions, with the same rules.
   - It counts target, stop (and gaps), trend, time and "the data ran out".
   - "The data ran out": the newest closing file came before any rule. That
     can only happen for the last days.
   - The prices are adjusted for payouts, so a payout is not a fall here
     either.
8. **The fan chart** (`chart`): one column a session, the dates as labels
   ("10-29").

The flags: `--sessions N` replays N sessions after the buy day instead of 20.
`--mode bars`, `--mode daily` and `--until` are for day plans: a swing plan
refuses them.

## Steps

1. Make sure `psx/plan.json` is today's plan from `/psx-exit`. If there is
   none, run that first, or pass the plan as flags.
2. Run `timemachine.py run --write`.
   - Each replay ends at the plan's `flat_by` (16:20 on a Friday). So
     "neither" means still open at the time you would get out.
3. Tell the user, in this order:
   1. The mode, and why.
   2. The four odds.
   3. The middle price, and the 5 to 95 range at `--until`.
   4. The costs line and the average R. Say that the R counts the costs.
   5. The history.
   6. The verdict line and the lines under it, word for word.
   7. The seed.
4. In daily mode, say once that it is a simpler model. Say that a bars file
   or a tape with 20 or more sessions gives the stock's own 5-minute bars.
5. If the verdict is a coin flip or close to break-even, say so plainly. Do
   not dress it up. If the history and the replays disagree, say that too.
6. Say once that this is built from past days and is not a prediction.
   Results, news and halts can do things those days never did. Check
   `/psx-news` for the stock before going on.
7. If the user still wants the trade, hand off to `/psx-budget` to size it.
8. A swing plan: run it the same evening, after `/psx-exit`. Tell the user
   the outcomes in their order (target, stop and its gaps, trend, time, no
   fill), the average R, the history and the verdict. Say once that a gap
   through the stop sells at the open, so a loss can be bigger than the
   plan's max loss. `/psx-budget` sizes it on the buy day.

## Example

The sample market of the tests. It is made up, and so is DEMO.

- Thursday 2026-10-29. DEMO's 15-minute opening range is 98.90 to 100.20.
- The 10:10 bar closes above it: entry 100.65 at 10:15 AM (bar 8).
- Stop 99.55 (the range middle). Target 101.75 (1R, risk 1.10 a share).
- Flat by 15:20. Today's price limits: 88.56 to 108.24.

**Bars mode.** `bars/DEMO.csv` has 30 past sessions. The 24 Mon to Thu
sessions make the pool. The 6 Fridays have other hours, so they stay out.
The command is `timemachine.py run`. It prints:

```
DEMO buy, Thu 2026-10-29: entry 100.65 at 10:15 AM (bar 8), stop 99.55, target 101.75 (1R, risk 1.10 a share).
Mode: bars. There are 24 full Mon to Thu sessions of DEMO's 5-minute bars in bars/DEMO.csv before this day (20 needed).
10,000 replays of the rest of the session, 10:15 AM to 3:20 PM, the plan's flat-by time (61 five-minute bars), seed 19.
Each bar is drawn whole from DEMO's own 5-minute bars at the same time of day (+-2 bars).
The pool: its last 24 full Mon to Thu sessions, 2026-09-17 to 2026-10-28.
Price limits for the day: 88.56 to 108.24 (from the company page). No replay goes past them.
Costs: about 0.33R a trade (your costs settings), counted in the R and the verdict.

  target first   31.3 %
  stop first     23.6 %
  neither        45.1 %   still open at 3:20 PM
  green          56.1 %   target first, or above the entry at 3:20 PM

  Price at 3:20 PM: median 100.85, 90 % of replays between 99.16 and 102.67.
  Average R: -0.226, costs included (R = the 1.10 risk: +0.67R at the target, -1.33R at the stop).

History: the same rule (15-min opening range, stop at the opening-range midpoint, 1R target)
  on each of those 24 real sessions fired 23 times: 19 target, 4 stop, 0 neither. Average R -1.670, costs included.
  Costs: 0.61R to 8.16R a trade on those days (the closer the stop, the more R the costs are).

Leans toward the stop: at 1R after costs the target has to come first in 66 % of the replays that hit one side; it did in 57 % (target first 31.3 % vs stop first 23.6 %).
45.1 % of the replays hit neither by 3:20 PM; the price at 3:20 PM decides those.

Left out 6 sessions with other hours (Friday).
A simulation built from DEMO's own last 24 full Mon to Thu sessions.
It is not a prediction: results, news and halts can do things those days never did.
Same seed, same numbers: repeat this run with --seed 19.
Next: /psx-budget sizes it to your budget and your max loss per trade, costs included.
```

**Daily mode.** The same plan, from DEMO's last 60 daily bars. The command
is `timemachine.py run --mode daily`. It prints:

```
DEMO buy, Thu 2026-10-29: entry 100.65 at 10:15 AM (bar 8), stop 99.55, target 101.75 (1R, risk 1.10 a share).
Mode: daily. You asked for it (--mode daily). There are 24 full Mon to Thu sessions of DEMO's 5-minute bars in bars/DEMO.csv before this day.
10,000 replays of the rest of the session, 10:15 AM to 3:20 PM, the plan's flat-by time (61 five-minute steps), seed 19.
Daily mode is a simpler model: each step is a random move, not a real bar.
The moves are sized from DEMO's last 60 daily bars, 2026-08-04 to 2026-10-28.
sigma_day 1.16 % (from the daily highs and lows), so 0.136 % a step.
A tape or a bars file with 20 or more Mon to Thu sessions gives DEMO's own 5-minute bars instead (bars mode).
Price limits for the day: 88.56 to 108.24 (from the company page). No replay goes past them.
Costs: about 0.33R a trade (your costs settings), counted in the R and the verdict.

  target first   29.4 %
  stop first     31.0 %
  neither        39.6 %   still open at 3:20 PM
  green          49.4 %   target first, or above the entry at 3:20 PM

  Price at 3:20 PM: median 100.63, 90 % of replays between 98.89 and 102.43.
  Average R: -0.344, costs included (R = the 1.10 risk: +0.67R at the target, -1.33R at the stop).

History: on each of those 60 days, the stop 1.09 % under the open and the target 1.09 % over it:
  target only 21, stop only 13, both 1, neither 25.
  On a day with both, the order inside the day is not known.

Strongly toward the stop: at 1R after costs the target has to come first in 66 % of the replays that hit one side; it did in 49 % (target first 29.4 % vs stop first 31.0 %).

A simulation built from DEMO's last 60 daily bars.
It is not a prediction: results, news and halts can do things those days never did.
Same seed, same numbers: repeat this run with --seed 19.
Next: /psx-budget sizes it to your budget and your max loss per trade, costs included.
```

(On the sample market, add `--data tests/fixtures/psx-market --config
psx-budget/config.example.json --offline --now "2026-10-29 10:20"` to get
these exact lines.)

How to read it:

- The costs are about 0.33R a trade. So a 1R target is worth +0.67R, and the
  stop costs -1.33R.
- Bars mode: the target came first in 57 % of the replays that hit one side.
  That beats 50 %, but after costs 1R needs 66 %. So it leans toward the
  stop, and the average R is -0.226.
- Daily mode: target first and stop first are close to even. After costs,
  that is strongly toward the stop.
- The history hit the target 19 times in 23. But those days had closer stops,
  so the costs were 0.61R to 8.16R a trade, and the average R is -1.670.
- Both modes come out toward the stop once the costs count. Say that plainly.
- The sample market is made up, so do not read anything into it.

**Swing mode.** psx-exit's swing plan for DEMO, made the evening before the
buy day. It is a limit buy at 99.38 on Thu 2026-10-29 (the last close 98.40
plus 1 %), stop 96.25 (2 x the daily ATR under the entry), target 105.64
(2R), exit by Fri 2026-11-27. The command is `timemachine.py run`. It prints:

```
DEMO swing buy, Thu 2026-10-29: a limit buy at 99.38 (last close + 1%), stop 96.25, target 105.64 (2R, risk 3.13 a share).
Mode: swing. A swing plan: the replays walk the next 20 sessions, one daily bar at a time.
10,000 replays of the next 20 sessions, Thu 2026-10-29 to the exit-by day Fri 2026-11-27, seed 19.
Each session is one of DEMO's own last 60 daily bars, drawn whole, so gaps between sessions are in it.
The pool: 2026-08-04 to 2026-10-28, each bar as ratios to its own LDCP, so a payout is not a fall.
A gap through the stop sells at the open, not at the stop.
The trend rule: a close under the lowest close of the 10 sessions before it (now 92.36) sells at the next open.
Price limits: 88.56 to 108.24 on the buy day (computed from the last close 98.40), then from each replayed close. No replay goes past them.
Costs: about 0.11R a trade (your costs settings, commission on both sides), counted in the R and the verdict.

  target         34.5 %   out at 105.64, or at the open when it opens over it
  stop           34.0 %   out at 96.25, or at the open when it opens under it (a gap: 2.8 %)
  trend          19.8 %   out at the next open (the trend rule)
  time           11.7 %   out at the close of Fri 2026-11-27 (the time stop)
  no fill        0.0 %    the limit 99.38 did not fill on Thu 2026-10-29: the order ends at the close

  Average R: +0.584 over the replays that filled, costs included (R = the 3.13 risk: +1.88R at the target, -1.11R at the stop, for a fill at 99.38).

History: a buy at the open of each of those 60 days, with the stop 3.15 % under it and the target 6.30 % over it, walked forward up to 20 real sessions:
  target 10, stop 6 (0 gaps), trend 35, time 0, the data ran out 9.
  The data ran out: those walks met no rule before the newest closing file.

Leans toward the target: at 2R after costs the target has to come first in 37 % of the replays that hit one side; it did in 50 % (target first 34.5 % vs stop first 34.0 %).

A simulation built from DEMO's own last 60 daily bars.
It is not a prediction: results, news and halts can do things those days never did.
Same seed, same numbers: repeat this run with --seed 19.
Next: /psx-budget sizes it on the buy day, before you buy. Nothing was placed.
```

(On the sample market, add `--plan tests/fixtures/psx-v2/contract/plan-swing.json
--data tests/fixtures/psx-market --config psx-budget/config.example.json
--offline --now "2026-10-28 17:00"` to get these exact lines.)

How to read it:

- Every replay filled. In its last 60 days DEMO never opened 1 % over the
  close before, so every replay filled at the open.
- The target and the stop came first about as often. A 2R target needs to
  come first in only 37 % of those after costs. So it leans toward the target.
- 2.8 % of the replays opened under the stop. Those sold at the open, for a
  bigger loss than the plan's.
- The costs are smaller in R than in the day example (about 0.11R), because
  the stop is further away.
- The history is DEMO's own path: falls in September (the trend rule), rises
  in August and October (the target). 9 of the last 10 days ran out of data.
- DEMO rose about 12 % in those 60 days, and the replays carry that rise. A
  real share can turn. The sample market is made up, so do not read anything
  into it.

## Rules

- Every number comes from the run. Never round a coin flip up into an edge.
- The verdict line and the lines under it are printed by the tool. Repeat
  them, do not rewrite them.
- Never judge a plan by target first vs stop first alone: the verdict
  already weighs the target's R and the costs.
- The average R, the history's R and the verdict count PSX costs. Green does
  not: it is by price alone. Say so when you give the numbers.
- Simulated odds are not predictions and not promises. Say it once, plainly.
- Say the mode. Daily mode is a simpler model: say so once.
- Free PSX data is about 5 minutes late. Bars are 5-minute bars, checked bar
  by bar, never tick by tick.
- Always say the seed, so any run can be repeated.
- One plan per run. A changed entry, stop, target or date is a new run.
- Long only. A sell plan is refused (PSX bans blank sales).
- Swing mode: say the share of gaps. A gap through the stop sells at the
  open, so a loss can be bigger than the plan's max loss.
- Swing mode: the trend rule and the time stop sell at the price then. It
  can be under or over the fill. The average R counts both.
- Swing mode: a note that the buy day's LDCP is under the last close means
  the share is ex that day (a payout, bonus shares or a right). Say so.
  When the next note says the entry was set from the last close, say that
  the entry and the stop came from the old price.

## What it never does

- It never places an order, never sizes a position and never changes the plan.
- It never calls a result a sure thing. It never prints a P&L or a profit.
- It never uses a bar that has not closed yet, and never mixes today's bars
  into the pool.
- It never fetches from the PSX site unless `psx/config.json` says
  `"psx_site": true`, and never with `--offline` or `--now`.

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
