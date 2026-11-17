---
name: psx-exit
description: >-
  Exit Planner for the Pakistan Stock Exchange (PSX). Sets your stop and target
  before you buy, so you know when to get out. Reads the entry from psx-entry
  (or a price you give). The stop goes at the opening-range midpoint by default
  (or the range low, a price, a percent or an ATR multiple), rounded down to the
  Rs 0.01 tick. The target is 2R (or 1R, or a price). Checks the day's price
  limits and costs. Refuses a stop at or above the entry, a target at or below
  it or over the upper price limit, or a stop too tight to survive the spread,
  and says why. In swing style it plans a limit buy for the next session: a stop
  from the daily ATR, a target, an exit-by day, a trend rule and the gap risk.
  Writes psx/plan.json. Long side only. Use when the user says "where's my
  stop", "set my stop and target", "plan the exit", "when do I get out", "stop
  loss", "what's my R", "risk reward", "plan a swing trade", or after /psx-entry
  (day style) or /psx-scanner (swing style), before /psx-timemachine.
argument-hint: "[--stop or-mid|or-low|price:X|pct:X|atr:K|low:N|level:K] [--target 2R|1R|price:X]"
---

# psx-exit

The Exit Planner decides how a trade ends before it starts.

- The stop is where the setup has failed.
- The target is where you take what you came for.
- Both are set BEFORE the entry and written down. So nobody has to decide
  anything in the middle of a fast move.

A stop is a plan, not a guarantee: a gap or a fast market can fill past it.
PSX has no stop order at the exchange. You sell at the stop yourself, or you
use your broker app's stop feature. Day trading loses most people money, and
a neat plan does not change that.

`${CLAUDE_SKILL_DIR}` below is this skill's folder (where this SKILL.md lives).

```bash
python3 "${CLAUDE_SKILL_DIR}/exit.py" plan                          # psx/entry.json: midpoint stop, 2R target
python3 "${CLAUDE_SKILL_DIR}/exit.py" plan --stop or-mid --target 1R --write
python3 "${CLAUDE_SKILL_DIR}/exit.py" plan --stop atr:1.5           # needs today's bars (a bars file or a tape)
python3 "${CLAUDE_SKILL_DIR}/exit.py" plan --symbol DEMO --entry 100.65 --or-high 100.20 --or-low 98.90
python3 "${CLAUDE_SKILL_DIR}/exit.py" show                          # the current psx/plan.json
```

Other flags:

- `--flat-by 15:00`: a time on the plan's day itself (Karachi time).
- `--json`: the plan and its notes as JSON.
- `--now "2026-10-29 10:15"`: pretend it is this Karachi time.
- `--entry PRICE` with a waiting entry.json: plan ahead.
- `--setup level`, `--time 10:15`, `--entry-bar 8`, `--date YYYY-MM-DD`.
- `--data DIR` (default `psx/data`), `--bars FILE`, `--offline`.

## What it reads and writes

| file | what |
| --- | --- |
| `psx/entry.json` | the trigger from psx-entry: symbol, entry price, time, bar, opening range |
| `psx/config.json` | `flat_by` (15:20), `min_reward_risk` (1.0: a note here, psx-risk enforces it), `costs`, `psx_site`, `holidays`, `open_days`, `ramadan`, `style` and the `swing` block |
| `psx/watchlist.json` | swing style: the scan's setup and level of the share (psx-scanner), for the title and a `level:K` stop |
| `psx/metrics.json` | swing style: the next board meeting (psx-analyst), for a note |
| `psx/data/company/<SYM>.html` | a saved PSX company page: its CIRCUIT BREAKER is the day's price limits |
| `psx/data/tape/<date>/<SYM>.jsonl` | the company page tape: the same limits, and bars for an ATR stop |
| `psx/data/tape/<date>/market.jsonl` | the market tape (screener prices): rough bars for an ATR stop, the last choice |
| `psx/data/mkt_summary/` | PSX closing files: the day's LDCP or the last close, when there is no page for the day. In swing style also the daily bars: the stop, the trend rule and the ATR |
| `psx/data/bars/<SYM>.csv` | bars from your broker, for an `atr:K` stop (or `--bars FILE`) |
| `psx/plan.json` | with `--write`: entry, stop, target, risk a share, flat by, the session, the limits and the costs a share. A swing plan has the exit-by day, the trend rule and the gap risk in place of flat by. psx-timemachine, psx-budget and psx-alerts read it |

It reads only the data folder, unless `"psx_site": true` is in your config.
Then it asks the PSX site first for today's company page. If the site fails,
it uses the saved page. A plan for another day uses only the saved page (the
site only has today's). It never asks the site with `--offline` or `--now`.

## Stops and targets

| stop | where it goes |
| --- | --- |
| `or-mid` | the opening-range midpoint (the default for an opening-range breakout) |
| `or-low` | the opening-range low: wider, so fewer shares for the same max loss |
| `price:X` | your price |
| `pct:X` | X percent under the entry |
| `atr:K` | K times the 14-bar ATR under the entry, on today's bars up to the entry bar. With fewer than 14 bars by then, it averages all of them and says so |

A level setup has no opening range to lean on, so it needs a stop you name.
The ATR bars come from the first of these that has any: `--bars FILE`,
`psx/data/bars/<SYM>.csv`, the company page tape, the market tape.

- **Rounding.** The stop rounds AWAY from the entry to the Rs 0.01 tick (down,
  for a long). Risk = entry minus stop. Target = entry + R x risk, rounded
  half up. `2R` by default; `1R`, `1.5R` or `price:X` also work.
- **Price limits.** PSX stops a share at 10% from its last close (LDCP), or
  Rs 1 when 10% is under Rs 1. Trading can reach a limit, not pass it. The
  tool uses the first of these:
  - the company page's CIRCUIT BREAKER for the plan's day (the site or the
    saved page, then the tape);
  - computed from the LDCP in the day's closing file, when it is saved (on an
    ex-date, PSX has already lowered it there);
  - computed from the last close; an ex-date lowers it;
  - none of these: the limits are unknown, and the tool says what to save.
- **Costs.** It estimates the costs a share of a buy at the entry and a sell
  at the stop: commission, sales tax and fees, from your `costs` settings.
- **Refused.** It refuses these, and says why:
  - a stop at or above the entry;
  - a target at or below the entry;
  - an entry or a target over the upper price limit, or an entry under the
    lower limit (it cannot fill that day);
  - an entry at 12:00 PM on a Friday, or at the close (nothing trades after
    it, so it cannot fill);
  - a stop under 0.05% of the price, or under Rs 0.02, from the entry: too
    tight to survive the spread (small moves would stop you out);
  - an `or-mid` or `or-low` stop when psx-entry saw only part of the opening
    range (its tape started late);
  - an entry.json that has not triggered (unless you give `--entry`);
  - a short: this pack plans longs only;
  - an entry at or after the flat-by time;
  - a day PSX is closed.
- **Warned.** A stop at or under the lower price limit: at the limit there
  may be no buyers, so you may not get out. Costs over 25% of the price risk:
  you pay them win or lose. The price risk is the shares x the risk a share.
  The size is not known yet, so it uses 1,000 shares. psx-budget and psx-risk
  use the same rule.
- **Flat by.** 15:20 by default (or `flat_by` in the config). Out by then,
  win or lose, no overnight hold. The config time is for Monday to Thursday.
  On other days it keeps its place: 16:20 on a Friday (10 minutes before the
  4:30 PM close), 13:20 on a Ramadan Monday.
- **Friday.** PSX stops for the Juma break, 12:00 PM to 2:30 PM. A morning
  trade is held through it, and the tool says so. For an entry before
  11:55 AM, `--flat-by 11:55` gets you out before the break. An entry at
  12:00 PM cannot fill. The next chance is the 2:30 PM session, at a new
  price.
- **Bar numbers.** Bar 0 is the first 5-minute bar of the day (9:30 AM Monday
  to Thursday, 9:15 AM on Friday and in Ramadan). The count runs across the
  Friday break: the 2:30 PM bar is bar 33.

## Steps

1. Run it right after `/psx-entry` triggers. Before that, `--entry PRICE`
   plans ahead at the level you expect.
2. Use the default stop for an opening-range breakout unless the user names
   another. A level setup needs one: ask.
3. Run `exit.py plan --write`. Read back the entry, the stop and its rule,
   the target and its rule, the risk a share, reward:risk, the costs, the
   price limits and flat by. Read every note too.
4. If it refuses, say the reason and the fix (a wider stop, another
   target). Never loosen anything on your own.
5. Say once that the stop is a plan, not a guarantee. Free PSX prices are
   about 5 minutes late, so the user should watch the stop on the broker's
   screen.
6. Hand off to `/psx-timemachine` to replay the plan, then `/psx-budget` to
   size it to the max loss per trade, costs included. Offer `/psx-alerts` for
   the stop, the target and the flat-by time.

## Example: DEMO on Thu 2026-10-29

This is the made-up sample market of the tests. DEMO is not a real share.
The entry is 100.65 at 10:15 AM (the 10:10 bar, bar 8). The opening range is
98.90 to 100.20. `exit.py plan --stop or-mid --target 1R --write`:

```
Exit plan: DEMO long, Thu 2026-10-29, opening-range breakout on 5-minute bars
  Entry         100.65 at 10:15 AM (bar 8)
  Stop          99.55  opening-range midpoint: (100.20 + 98.90) / 2 = 99.55
  Target        101.75  1R (one times the risk)
  Risk a share  1.10 (1.09% of the entry)
  Reward:risk   1.00
  Costs         about 0.3586 a share, buy and sell at the stop (estimated)
  Price limits  88.56 to 108.24, from the company page (LDCP 98.40)
  Flat by       15:20 PKT, win or lose: no overnight hold
Set before the entry. If price hits the stop, you are out; never move it further away.
A stop is a plan, not a guarantee: a gap or a fast market can fill past it.
PSX has no stop order: sell at the stop yourself, or use your broker app's stop feature.
Free PSX prices are about 5 minutes late: watch the stop on your broker's screen.
Note: Costs are about 33% of the price risk (over 25%). You pay them win or lose.
Wrote psx/plan.json.
Next: /psx-timemachine replays it, then /psx-budget sizes it to your max loss, costs included. Nothing was placed.
```

- The default 2R target would be 100.65 + 2 x 1.10 = 102.85.
- Costs: 1,000 shares cost Rs 358.55 for the round trip, so about 0.3586 a share.
  The price risk of 1,000 shares is Rs 1,100.00. 358.55 / 1,100.00 is 32.6%, so about 33%.
- Both levels can fill: 88.56 is under the stop, 108.24 is over the target.
- On Friday 10-30 the page is old, so the limits are 91.44 to 111.76:
  computed from the last close; an ex-date lowers it.

## Swing style

Swing style holds a share for days or weeks, not minutes. Set
`"style": "swing"` in `psx/config.json`. The `"swing"` block holds the
numbers. Swing trading loses money for many people too. Try it on paper
first (`"paper": true`). `/psx-entry` is not used: the setup comes from the
daily scan.

```bash
python3 "${CLAUDE_SKILL_DIR}/exit.py" plan --symbol DEMO --write          # the evening before the buy day
python3 "${CLAUDE_SKILL_DIR}/exit.py" plan --symbol DEMO --stop low:10    # one tick under the 10-session low
python3 "${CLAUDE_SKILL_DIR}/exit.py" plan --symbol DEMO --stop level:0.5 --entry 99.50
```

- **Buy day.** `--date`, else today until PSX closes, else the next PSX
  session. A plan made on Fri 2026-11-06 at 5:00 PM is for Tue 2026-11-10:
  Mon 2026-11-09 is Iqbal Day.
- **Entry.** A limit buy at the last close plus 1% (`swing.entry_buffer_pct`),
  or `--entry PRICE`. PSX takes a limit buy in the pre-open. It is a day
  order: if it does not fill, it ends at the close. Do not chase it.
- **Data.** The newest 60 closing files before the buy day, in
  `psx/data/mkt_summary/`. It needs 20 daily bars of the share. The newest
  file must be from the session before the buy day. Else it refuses and says
  which file to save.
- **Stop.** `--stop`, else `swing.stop` (`atr:2`). It rounds down to the tick.
- **ATR.** ATR(14) is how far the share moves in a normal day. It is the
  average of the last 14 sessions, each from its low to its high. A jump from
  the last close counts too.

| stop | where it goes |
| --- | --- |
| `atr:K` | K times the daily ATR(14) under the entry. The ATR comes from the closing files, with payouts and bonus shares taken out, so an ex-date is not a big range |
| `low:N` | one tick under the lowest low of the last N sessions |
| `level:K` | K times the daily ATR under the scan's level in `psx/watchlist.json` (from the same close). A setup with no level is refused |
| `price:X`, `pct:X` | as in a day trade |

- **Refused in swing.** `or-mid` and `or-low`: they are opening-range stops,
  for a day trade. Also the day flags `--or-high`, `--or-low`, `--time`,
  `--entry-bar`, `--interval`, `--flat-by` and `--bars`.
- **Target.** `--target`, else `swing.target` (2R). A target over the buy
  day's upper price limit is a note, not a refusal: it can fill on a later
  day. An entry outside the limits is still refused.
- **Stop and the lower limit.** The price can trade at a limit, never past
  it. A stop under the buy day's lower price limit cannot be hit that day: it
  counts from the next session. A stop at the limit can be hit that day. At
  the limit there may be no buyers, so you may not get out. Both are notes.
- **Stop and the LDCP.** A limit buy fills at its price or lower. The stop
  may be at or over the buy day's LDCP. Then a fill at the LDCP or under is
  at or under the stop at once. The plan says so in a note.
- **Ex-date on the buy day.** PSX moves the LDCP on an ex-date (a payout, a
  bonus or a right) or a split. It can also move after days with no trade.
  The buy day's own company page or closing file may show an LDCP that is
  not the last close. Then the closing files before that day do not fit its
  prices. On an ex-date they are on the old prices. In that case:
  - with no `--entry`, the plan is refused. The line shows the new LDCP + 1%
    for `--entry`. Or plan for the next session, once that day's closing
    file is saved. Then the old prices are put on the new scale;
  - `low:N` and `level:K` stops are refused that day;
  - with your own entry, it plans and adds a note: the ATR and the trend
    level may be on the old prices.
  A plan made the evening before cannot see an ex-date yet. Plan again on
  the buy day, before you buy, with that day's company page.
- **Exit by.** The time stop: 20 PSX sessions after the buy day
  (`swing.max_hold_sessions`), by your `flat_by` time that day. On a Friday
  that is 4:20 PM.
- **Trend rule.** Out after a close under the lowest close of the 10 sessions
  before it (`swing.trend_exit_sessions`). The plan shows that level now.
  psx-alerts checks it on each closing file.
- **Costs.** Commission counts on both sides: a sell on a later day always
  pays it, whatever `day_trade_one_side` says. Tax on gains is not in these
  costs.
- **Gap risk.** A share you hold overnight can open the next day at its lower
  price limit (10% under the entry). The "Gap risk" line shows what that
  loses a share, costs included. It also shows how many times the loss at the
  stop that is. A gap goes past the stop: the sell fills at the open, not at
  the stop. More days down can lose more. psx-budget and psx-risk show it in
  rupees and cap it (`swing.max_gap_loss_pkr`).
- **Results.** A board meeting of the share in `psx/metrics.json`
  (psx-analyst) from the buy day to the exit-by day gives a note. Results can
  gap the price.

**Swing example: DEMO on the evening of Wed 2026-10-28.** No company page and
no closing file of Thu 2026-10-29 are saved yet. `psx/watchlist.json` holds
the scan of the 10-28 close. `exit.py plan --symbol DEMO --write`:

```
Swing plan: DEMO long, buy on Thu 2026-10-29, 20-day closing-high breakout (level 96.56)
  Entry         99.38  limit buy: the last close 98.40 (Wed 2026-10-28) + 1%
  Stop          96.25  2 x ATR(14) under the entry: daily ATR 1.5650 over the 14 sessions to Wed 2026-10-28
  Target        105.64  2R (two times the risk)
  Risk a share  3.13 (3.15% of the entry)
  Reward:risk   2.00
  Costs         about 0.3504 a share, buy and sell at the stop (estimated, commission both sides)
  Price limits  88.56 to 108.24 (LDCP 98.40): computed from the last close; an ex-date lowers it
  Exit by       Fri 2026-11-27 at 16:20 PKT: 20 sessions after the buy day (the time stop)
  Trend rule    out after a close under the lowest close of the 10 sessions before it (now 92.36)
  Gap risk      a next-day open at the lower limit 89.44 loses about 10.28 a share, costs included: 2.95 times the loss at the stop
Set before the entry. If price hits the stop, you are out; never move it further away.
A stop is a plan, not a guarantee: a gap or a fast market can fill past it.
PSX has no stop order: sell at the stop yourself, or use your broker app's stop feature.
Free PSX prices are about 5 minutes late: watch the stop on your broker's screen.
Held overnight: a gap can open past the stop. Then a sell fills at the open, not at the stop.
Note: This plan is for 2026-10-29, not today (2026-10-28).
Wrote psx/plan.json.
Next: /psx-timemachine replays the next 20 sessions, then /psx-budget sizes it on the buy day. Nothing was placed.
```

- Entry: 98.40 x 1.01 = 99.384, so 99.38.
- Stop: 99.38 - 2 x 1.5650 = 96.25. The risk is 3.13 a share. Target:
  99.38 + 2 x 3.13 = 105.64.
- Gap risk: 99.38 - 89.44 = 9.94 of price, plus about 0.3382 of costs, is
  10.2782 a share. The loss at the stop is 3.13 + 0.3504 = 3.4804 a share.
  10.2782 / 3.4804 is 2.95.
- With `--stop low:10` the stop is 92.06 (the low 92.07, less one tick). With
  `--stop level:0.5` it is 95.77 (96.56 - 0.5 x 1.5650 = 95.7775, rounded
  down).

Steps in swing style:

1. After the close, run `/psx-scanner` (`scan.py daily`). Pick one setup.
2. Run `exit.py plan --symbol X --write`. Read back the entry, the stop and
   its rule, the target, the exit-by day, the trend rule and the gap risk.
   Read every note too. Say what the ATR is in plain words: how far the share
   moves in a normal day.
3. Say what the gap line means, with its numbers. A gap can open past the
   stop. So one bad open can lose more than the planned loss.
4. Hand off to `/psx-timemachine`. Then `/psx-budget` sizes it on the buy day.

## Rules

- The stop and the target are set before the entry, never after.
- Never move a stop further from the entry once the trade is on.
- Plain numbers only: entry, stop, target, risk a share, reward:risk, costs.
  It never prints a P&L or a return.
- Nothing here promises winning trades or money. A 1R target is not a
  prediction that the price gets there.
- Long side only. This pack plans longs only: PSX bans blank sales.

## What it never does

It never places an order, never sizes a position, never widens a stop to
make a plan pass, and never calls a stop a guarantee.

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
