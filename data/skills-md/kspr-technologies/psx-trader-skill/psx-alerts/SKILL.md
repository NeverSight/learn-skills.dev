---
name: psx-alerts
description: >-
  Price Alerts on the Pakistan Stock Exchange (PSX) clock. Rings when a price, a
  stop, a target, a daily price limit, a KSE30 move or the opening bell hits,
  once each, so you are not spammed. Turns the trade plan into three alerts in
  one go: the stop, the target and "flat by close". Knows PSX hours (the Friday
  Juma break, Ramadan) and the 2026 and 2027 holidays, in Karachi time. Reads
  PSX quotes (about 5 minutes late) from your saved pages, the tape or the PSX
  site (only if you turn it on), and writes psx/prices.json for sizing and the
  risk check. For a swing trade it watches the position until it is sold: the
  stop, the target, a trend break and the time stop, on every closing file, even
  after the Mac slept. Use when the user says "alert me when", "tell me if HUBC
  hits 170", "watch my stop", "watch my trade", "watch my swing trade", "remind
  me to close by 3:20", "is PSX open", "when does the market open", "get me a
  price", or right after /psx-exit writes a plan.
argument-hint: "[symbol] [price]"
---

# psx-alerts

Price Alerts watches the numbers, so the user does not have to stare at a chart.
An alert is information, never an order. When a stop alert rings, this skill sells nothing.
PSX has no stop or bracket orders of its own. So a stop alert is the cue to sell in the broker app.

`${CLAUDE_SKILL_DIR}` below is this skill's folder (where this SKILL.md lives).

```bash
python3 "${CLAUDE_SKILL_DIR}/alerts.py" clock                          # PSX open or closed, next open
python3 "${CLAUDE_SKILL_DIR}/alerts.py" add --from-plan                # stop, target, flat by close from psx/plan.json
python3 "${CLAUDE_SKILL_DIR}/alerts.py" add --opening-bell             # add --session 2 for the Friday 14:30 restart
python3 "${CLAUDE_SKILL_DIR}/alerts.py" add --symbol DEMO --stop 99.55
python3 "${CLAUDE_SKILL_DIR}/alerts.py" add --symbol DEMO --target 101.75
python3 "${CLAUDE_SKILL_DIR}/alerts.py" add --at 15:20 --label "flat by close" --before-close
python3 "${CLAUDE_SKILL_DIR}/alerts.py" add --symbol DEMO --pct 3
python3 "${CLAUDE_SKILL_DIR}/alerts.py" add --symbol DEMO --limit      # at the upper or lower price limit
python3 "${CLAUDE_SKILL_DIR}/alerts.py" add --index KSE30 --pct 4.5    # a warning before the 5% market halt
python3 "${CLAUDE_SKILL_DIR}/alerts.py" check                          # exit 0 rang, 1 nothing rang, 2 an error
python3 "${CLAUDE_SKILL_DIR}/alerts.py" quote DEMO --write             # -> psx/prices.json
python3 "${CLAUDE_SKILL_DIR}/alerts.py" quote --holdings --write       # portfolio + plan symbols
python3 "${CLAUDE_SKILL_DIR}/alerts.py" list
python3 "${CLAUDE_SKILL_DIR}/alerts.py" reset demo-plan-stop
```

- `--now "2026-10-29 10:53"` pins the clock (Karachi time). It is a replay: the tool then reads only the data folder.
- `--data DIR` is the data folder (default `psx/data`).
- `--offline` never touches the PSX site.
- `--source psx-screener` reads the screener instead of the company pages.
- `--portfolio FILE` (`check`, `list`): the ledger with your swing positions (default `psx/portfolio.json`).
- `--plan FILE` (`check`): a swing plan with no position gives an alert (default `psx/plan.json`).
- `--broker FILE` (`check`): psx-broker's log, read only (default: `broker.json` next to `--state`, so `psx/state/broker.json`).

## What it reads and writes

| file | what |
| --- | --- |
| `psx/plan.json` | the trade from psx-exit, for `add --from-plan`; `check` reads a swing plan to see if it has a position |
| `psx/config.json` | `psx_site`, `data_delay_minutes`, `flat_by`, `holidays`, `open_days`, `ramadan`, `paper`, `swing` |
| `psx/alerts.json` | the rules (`alerts.example.json` in this folder) |
| `psx/state/alerts.json` | which rules rang and when, so each rings once; for swing also the newest closing file checked, the rules met and the ex-dates seen |
| `psx/prices.json` | the latest quotes, merged in, for psx-budget and psx-risk |
| `psx/portfolio.json` | the symbols held, for `quote --holdings`; the swing positions and their plans, for `check` and `list` (read only) |
| `psx/state/broker.json` | psx-broker's log (read only): a swing check looks for today's stop-limit and for each `ticket.py stop --set` |
| `psx/data/tape/YYYY-MM-DD/` | snapshots the tools recorded: `<SYM>.jsonl` (company page), `market.jsonl` (screener) |
| `psx/data/company/<SYM>.html` | a company page you saved with your browser |
| `psx/data/screener.html`, `indices.html` | the screener and the indices pages you saved |
| `psx/data/mkt_summary/` | the daily closing files (the last close for the screener; a swing check reads each new one once) |

## Rule types

| type | rings when | rings again |
| --- | --- | --- |
| `above` / `target` | price at or above `price` | after `reset`, or on its own if `"rearm": true` and the price fell back |
| `below` / `stop` | price at or below `price` | same |
| `pct_move` | moved `pct` percent from the last close (LDCP), or from `ref`; `direction` up or down if you want | once per day at most |
| `limit` | price at the upper or lower daily price limit; `direction` up, down or any | once per day at most |
| `index_move` | an index (`index`, default KSE30) moved `pct` percent from its last close | once per day at most |
| `time` | the Karachi clock passed `at` ("15:20") on a trading day | once per trading day |
| `opening_bell` | PSX is open; `"session": 2` waits for the Friday restart at 14:30 | once per trading day |
| `trend` | swing only: an official close under the lowest close of the `sessions` (2 to 60) closes before it, from the closing files | once per day while held |

- `"rearm": "daily"` on an `above` or `below` rule: it rings at most once a day while it is hit. The swing stop and target use it.

- A rule with `"date"` is watched on that Karachi date only. `--from-plan` rules carry the plan's date. So yesterday's stop never rings today.
- A price rule uses a price from today only. An older price is not news.
- `"before_close": true` on a time rule with no date moves it with each day's close. Write the time for Monday to Thursday. So 15:20 rings at 16:20 on a Friday and at 13:20 on a Ramadan Monday.
- A rule with a date already holds that day's own time. psx-exit moved the plan's `flat_by` for its day, so the tool never moves it twice.
- The daily price limits are 10% below and 10% above the last close (LDCP). When 10% is under Rs 1, they are Rs 1 below and above.
- A price can reach a limit, never pass it. At the lower limit, a sell may not fill.
- The market halt: if KSE30 stays 5% from its last close for 5 minutes, PSX stops all trading for 60 minutes. It also cancels every open order. It does not apply in the last 75 minutes of the day.
- A KSE30 `index_move` at 4.5 is an early warning. The tool cannot see a halt itself: its data is about 5 minutes late.

## Quotes

- `psx-company` (the default): the company page of each symbol.
  - It gives the price, the page's As-of time, LDCP (the last close) and the day's price limits.
- `psx-screener`: one screener page for all symbols.
  - The screener has no As-of time. The data time is the fetch time minus `data_delay_minutes` (5).
  - A page from the site with an older clock in its top bar is old data: then that clock counts, not the fetch time.
  - Outside the session, the data time is the end of the last session. So a page saved at night is not fresh.
  - The last close comes from the daily closing file. The limits are worked out from it ("computed").
  - A page from the site with no share table (an error page, or a new layout) is one `error:` line. It never goes on the tape.
  - If the site does not give the closing file of the session before (a timeout, HTTP 500), that is one `error:` line.
    The prices are still checked, with no last close and no limits.
  - A stock with no trade today shows its last day's price on the screener. The company page shows the right date.
- Where the tool looks:
  - Site on (`"psx_site": true` in `psx/config.json`): the PSX site first, at every check.
    - If the site fails, your saved page. The check then prints an `error:` line.
    - A page from the site also goes on the tape.
  - Site off (the default), or with `--offline` or `--now`: only your saved pages. Never the site.
  - Today's tape is read too. The newest price at or before now wins.
- Turn the site on only if PSX has given you permission (marketdatarequest@psx.com.pk). PSX's website terms ban automated tools without it.
- Free PSX prices are about 5 minutes late. They are fine for alerts and for checking a size. They are not for timing an order. The broker's price is the one that fills.
- Each price in `psx/prices.json` keeps its data time. psx-risk uses only a price under 15 minutes old.
  - `limits_from` says where its price limits come from: "company page" or "computed" (from the last close).
  - A price you wrote by hand keeps your time (the file's `as_of`) when the tool adds new prices.
    A price with no time at all is dropped.
  - On the real clock (no `--now`), an older price never takes the place of a newer one, or of one you wrote by hand.
    A replay with `--now` writes what it read, as before.
- No page, and the site is off? Read the price in your broker app. Write it into `psx/prices.json` by hand, with the time the app showed:
  `{"as_of": "2026-10-29T10:52:00+05:00", "source": "manual", "prices": {"DEMO": 101.30}}`

## The PSX clock

Regular (REG) board hours, Karachi time (PKT, UTC+5, no daylight saving):

| day | hours |
| --- | --- |
| Monday to Thursday | 09:30 to 15:30 |
| Friday | 09:15 to 12:00, then 14:30 to 16:30 (the Juma break is in between) |
| Ramadan, Monday to Thursday | 09:15 to 13:30 |
| Ramadan, Friday | 09:15 to 12:30 |

- The pre-open runs for 15 minutes before each start: limit orders only, nothing trades.
- The first trades come 2 minutes after each start, after the opening match.
- After the close, the post-close session trades only at the closing price. The tool calls it closed.
- Holidays 2026: Feb 5, Mar 20, Mar 23, May 1, May 26 to 28, Jun 25 and 26, Aug 14, Aug 26, Nov 9 and Dec 25.
- Holidays 2027: Feb 5, Mar 23, May 28 and Nov 9 are fixed. The moon dates are expected only: Mar 5, Mar 10 to 12, May 17 to 19, Jun 15 and 16, and Aug 16. Check PSX notices.
- Ramadan 2027 is expected from 2027-02-09 to 2027-03-09.
- To fix a date, use `"holidays"`, `"open_days"` or `"ramadan"` in `psx/config.json`.
- For any other year, the clock says the holiday list is unknown.

## Steps

1. Right after psx-exit writes the plan, run `add --from-plan`. Confirm the three alerts back to the user: the stop, the target and the flat-by time.
   - A swing plan gives two alerts, for the buy day only: the stop and the target. There is no flat-by alert.
   - From the fill on, the swing alerts come from `psx/portfolio.json` (see "Swing style" below).
2. Run `check` while the trade is open, every few minutes.
   - Auto-run (psx-autorun) is the usual way. It checks every 5 minutes in the session, once after the close, and each morning.
   - A Claude scheduled task or `/loop` works too, but it needs an open Claude session.
   - Each run reads only the symbols in today's rules. Each alert rings once.
   - Swing: every closing file is checked once, even after the Mac slept. This is for a share with its swing plan
     in `psx/portfolio.json`. Your own rules in `psx/alerts.json` use only today's prices, never a closing file.
   - Swing: a met rule rings once a day until the share is sold.
   - Swing: the stop-limit reminder (live mode only), the ex-dates and the halt rule. See "Swing style".
   - Swing: an old price is a problem, not "nothing hit". In the session, a held swing share with no price newer
     than 15 minutes gives an `error:` line and exit 2.
   - Swing: a met rule is never "Nothing hit" either. When it rang earlier today, the check says "No new alert."
     and then one line for each met rule: which rule, on which day, and that you still hold the shares.
   - A check reads the latest delayed price. A price can pass a level between two checks.
   - With the site off (the default), no new price comes in by itself. Each check reads the same saved page.
     With the site off, save a fresh company page before each check, or watch your stop in your broker app.
   - Run only one tool that polls the PSX site at a time. Their requests are not spaced from each other.
   - Exit codes: 0 = something rang. 1 = nothing rang. 2 = a rule or a file could not be read.
     - 2 also means: a held swing share had no fresh price in the session, so its stop was not checked.
     - Each problem gets one `error:` line: a bad rule, a missing page, or a site that did not answer.
     - A bad rule never stops the others. Its line is `error: rule <id>: ...`. The other rules are still checked.
     - On 2, read all the output. An alert may have rung too.
3. Tell the user what rang, one line each.
   - A stop or target alert: PSX holds no stop order. The user sells in the broker app if they want out. If their broker app holds a stop for them, they check it there. Record any fill with psx-broker.
   - "Flat by close": close anything still open. psx-broker `flatten`, then psx-risk, then the user's yes. Never act for them.
   - A KSE30 move: a halt may be near, and a halt cancels all open orders.
   - A swing rule: say which rule is met and on which day. Then what the user could do. Then "You decide."

## Example

DEMO on Thursday 2026-10-29 (the made-up sample market in `tests/fixtures/psx-market`).
Entry 100.65 at 10:15 AM, stop 99.55, target 101.75, flat by 15:20.
`add --from-plan` writes `demo-plan-stop`, `demo-plan-target` and `demo-flat-by` for that day.

A `check --now "2026-10-29 10:53"` reads the 10:53 page: 101.23, between the stop and the target.

```
PSX OPEN (2026-10-29 10:53 PKT, regular session).
Nothing hit. 3 rule(s) watched today, DEMO 101.23 (as of 10:53 AM PKT).
```

At 11:41 the page shows 101.80:

```
PSX OPEN (2026-10-29 11:41 PKT, regular session).
ALERT DEMO is 101.80 at 11:41 AM PKT: at or above your target 101.75 (plan target: 1R (one times the risk)).
An alert is information, not an order. PSX prices here are about 5 minutes late, and PSX holds no stop order for you. To close a position: psx-broker flatten builds the sell ticket, then psx-risk and your yes. Record any fill with psx-broker.
```

At 15:20:

```
PSX OPEN (2026-10-29 15:20 PKT, regular session).
ALERT Flat by close: it is 15:20 PKT (set for 15:20), the market closes at 15:30. If DEMO is still open, close it: psx-broker flatten --symbol DEMO builds the sell ticket, then psx-risk and your yes.
An alert is information, not an order. PSX prices here are about 5 minutes late, and PSX holds no stop order for you. To close a position: psx-broker flatten builds the sell ticket, then psx-risk and your yes. Record any fill with psx-broker.
```

- Each alert rings once. The stop never rings that day: the lowest price after the entry is 100.55.
- The next day, the plan's three alerts are no longer watched.

## Swing style

A swing trade is held for days. Its alerts come from the ledger, `psx/portfolio.json`.

- psx-broker writes the position and its swing plan there at the fill.
- Each `check` builds the swing rules from it. They are never written to `psx/alerts.json`.
- When the position is sold, it leaves the ledger. Its alerts stop by themselves.
- On the buy day, the ledger rules take over from the `demo-plan-stop` and `demo-plan-target` alerts. So nothing rings twice.
- A share you hold with no swing plan in the ledger (a day buy, or one written by hand) gets none of the swing
  checks. In a swing folder (`"style": "swing"`), `check` and `list` give a note for it:
  `note: DEMO: you hold it with no swing plan in psx/portfolio.json, so the swing checks do not watch it. Only your own rules in psx/alerts.json watch it: 2 today.`
  Only your own rules watch it then: no closing-file walk, no daily ring, no old-price error, no reminder.
- So a share you bought before you set `"style": "swing"` has no plan, and the swing checks skip it.
  - Its rules in `psx/alerts.json` use only today's prices, never a closing file.
  - So they miss a dip under the stop between two checks. They also miss a day with no check (the Mac slept).
  - Give its stop `"rearm": "daily"`: then it rings once each day that it is hit. Watch its stop in your broker app too.
  - `ticket.py protect` and `ticket.py stop` refuse it. The README part "If you already hold shares" has more.

The swing rules (their ids end in the buy day, like `demo-swing-stop-2026-10-29`):

| rule | rings when |
| --- | --- |
| stop | a price at or under the stop, or a day's low in its closing file |
| target | a price at or over the target, or a day's high in its closing file |
| trend | an official close under the lowest close of the 10 sessions before it (payouts counted; the plan may say 2 to 60). It says: sell in the next session |
| time stop | the exit-by day, at the plan's exit-by time (for example 4:20 PM on a Friday) |
| stop-limit reminder | live mode only (`"paper": false`): the first check after the opening match (about 9:40 AM with auto-run; 9:25 AM on Fridays and in Ramadan), once a day, in the session only. Not while today's stop-limit sell is in `psx/state/broker.json`, while the price is at or under the stop, or while the stop rule is met |
| halt | while a swing share is held: KSE30 5% from its last close, in the session |

Every closing file is checked once:
- Oldest first, from the buy day on. The newest one checked is kept in `psx/state/alerts.json`.
- So a share with its swing plan in `psx/portfolio.json` loses no close when the Mac slept. The morning check reads the files it missed.
- The stop is checked on the day's low, the target on its high, the trend rule on its close.
- Each day's low is checked against the stop that was in force when that day began.
  A stop raised with `ticket.py stop --set` (it is in `psx/state/broker.json`) counts from the next session on.
  The price checks after the raise watch the rest of that day.
- A day that opened under the stop is a gap. A sell then fills near the open, not at the stop.
  An open at the stop is no gap: a sell there fills at about the stop.
- A file that is not there yet is skipped with a note. It is checked when it comes. After the close, today's file gets the note too.
  With the site off, the note says where to save it.
- The trend rule needs the closes of its sessions before the day. The tool reads enough files for up to 60 sessions.
  With too few files in the data folder, a note says the trend rule was not checked that day.
- Today's file is read after the close. With the site on, the tool asks for it from 30 minutes after the close, at most once every 15 minutes. Older missing files are left to `scan.py daily`.

A met rule rings once a day until the share is sold:
- It says which rule was met, on which day, and that you still hold the shares.
- The buy day's low or high may have come before your buy. Then the daily line says so.
  A later day that meets the rule rings again, as a new alert.
- After the exit-by day, while still held: an alert once a day.
- A swing plan with no position: an alert once a day, from the close of the buy day, on that day and the next session only. If you bought it, record the fill with psx-broker (`ticket.py fill`).

Ex-dates (payouts, bonus shares, rights and splits):
- The tool sees an ex-date on the company page (the flag after the name and the LDCP). It looks in the morning check, and at each check until the page shows today's data.
- With the site on: at most 4 page reads a share a day, at most 3 shares. At the latest, it sees the ex-date in that day's closing file.
- If the site gives no usable company page (an error page, a new layout, or only an old saved page), a note says so, once a day.
- XD (a cash payout): the stop and the target stay. A fall by the payout alone can meet the stop.
- XB, XR or a split: the stop and target are on the old price scale. An alert once a day until you choose: scale them (`ticket.py stop --symbol DEMO --scale F`) or keep them (`--scale 1`).
- A scale you typed before the tool saw the ex-date still counts. It waits until the ex-date is seen.
- A price that rose to a new scale (a factor over 1): `--scale` takes 1 or less. The alert says what you can do instead.
  Check your share count in your broker app.
- An ex-date on your buy day: a buy on the ex-date gets no payout, no bonus shares and no right. The alert says so.
- A stop alert on an ex-date says so.

An old price is a problem, not "nothing hit":
- In the session, a held swing share with no price newer than 15 minutes gives an `error:` line and exit 2. Its stop was not checked. Check the price in your broker app.
- With `"psx_site": false`, no new price comes in by itself. So each check in the session gives this error. Auto-run turns 3 in a row into a "PSX auto-run: problem" message, then at most one an hour.
- Right after the open (until about 7 minutes in), no price can be that new yet: the first trades come after the opening match, and prices are about 5 minutes late. A check then gives this error too. Auto-run's first check comes later.

Live mode (`"paper": false`):
- The stop-limit reminder: put in your stop-limit after the opening match. `ticket.py protect --symbol DEMO` makes the ticket (psx-risk and your yes first).
  - The reminder gives no prices. The order's prices come from `ticket.py protect`, after psx-risk checks them.
  - It does not ring while `psx/state/broker.json` has today's stop-limit sell of the share (approved or placed, not cancelled).
  - It does not ring while a fresh price is at or under the stop: a stop-limit would fire at once. The stop alert says it.
  - It does not ring while the stop rule is met. That lasts from the stop alert until you sell, also on the next days,
    and also when the price is back over the stop. A met stop means the plan's next step is a sell
    (`ticket.py flatten`), not a new stop-limit. The stop alert says so once a day.
    - A low only in the buy day's file may have come before your buy. It does not stop the reminder.
    - A scale for a bonus, right or split can clear a stop that was met on the old price scale. Then the reminder comes back.
  - With an XB, XR or split not answered yet, it says: answer the ex-date alert first.
  - A stop-limit you cancel in your app: record it (`ticket.py result ... --status cancelled`).
    If the reminder has not rung yet that day, it then rings at the next check.
- A stop alert adds: if your stop-limit is in, it may have filled. Check your broker app.
- The halt alert adds: a halt cancels all open orders at PSX, and may cancel your stop-limit. After the restart, check it.
  If PSX cancelled it, record that first: `ticket.py result --symbol DEMO --date <today> --status cancelled`.
  Then `ticket.py protect --symbol DEMO` makes a new one.

More:
- A stop in `psx/portfolio.json` under its stop at the buy gets a note: it was lowered by hand.
  The stop at the buy is scaled one `--scale` at a time, rounded down each time, as `ticket.py stop` does.
  - A `--scale` counts only for a bonus, rights or split ex-date the tool has seen, on or before the day of the scale.
  - It never counts for less than that ex-date's factor. `ticket.py stop` refuses less.
  - A scale written by hand with no such ex-date counts for nothing. So the note still comes.
- A limit of this tool: in the session, `pct_move` and `below` alerts compare with the raw last close in the files. On an ex-date a payout can look like a fall. The after-close check uses the LDCP and has no such problem.

Example: DEMO bought on Thu 2026-10-29, stop 96.25, target 105.64, exit by Fri 2026-11-27 (the made-up `gap` path in `tests/fixtures/psx-v2/paths/`). The first check after the close of Mon 2026-11-02:

```
PSX closed (2026-11-02 16:10 PKT, after the close).
ALERT DEMO traded at or under your stop 96.25 on Mon 2026-11-02: the low in that day's closing file was 94.80 (official close 95.60). DEMO opened at 95.40 on Mon 2026-11-02, under your stop 96.25 (a gap): a sell fills near the open, not at the stop. Your plan's stop rule is met. You could sell: psx-broker flatten --symbol DEMO, then psx-risk and your yes. You decide.
note: DEMO: the newest data is from Thu 2026-10-29 3:49 PM PKT, not today, so no alert used it.
note: DEMO: checked the closing files of Thu 2026-10-29, Fri 2026-10-30 and Mon 2026-11-02.
An alert is information, not an order. PSX prices here are about 5 minutes late, and PSX holds no stop order for you. To close a position: psx-broker flatten builds the sell ticket, then psx-risk and your yes. Record any fill with psx-broker.
```

A Mac that slept: the `trend` path, with the target at 112.00. The last check was after the close of Tue 11-24. The morning check of Fri 11-27 reads the two files it missed:

```
PSX closed (2026-11-27 08:15 PKT, before the open, pre-open from 9:00 AM PKT).
ALERT DEMO closed at 100.50 on Wed 2026-11-25 (the official close), under 101.20, the lowest close of the 10 sessions before. Your plan's trend rule was met on Wed 2026-11-25. It says: sell in the next session. You still hold 1,436 shares in psx/portfolio.json. You could sell: psx-broker flatten --symbol DEMO (--limit P in the pre-open), then psx-risk and your yes. You decide.
note: DEMO: the newest data is from Thu 2026-10-29 3:49 PM PKT, not today, so no alert used it.
note: DEMO: checked the closing files of Wed 2026-11-25 and Thu 2026-11-26.
An alert is information, not an order. PSX prices here are about 5 minutes late, and PSX holds no stop order for you. To close a position: psx-broker flatten builds the sell ticket, then psx-risk and your yes. Record any fill with psx-broker.
```

- "the newest data is from Thu 2026-10-29": the sample market has no company page or tape after that day.
- `list` shows the swing rules too, each with "(from psx/portfolio.json)".

## Rules

- An alert is a fact about a price or the clock. Say it as a fact.
- Free PSX prices are about 5 minutes late. Say so when a minute matters.
- Never present a quote as up to the second.
- Confirm every new rule back to the user: symbol, type, level and day.
- A swing alert says a rule is met. It is not advice. Say what the user could do, then "You decide."
- Two writers, one file: auto-run's checks and `alerts.py add` or `reset` all write `psx/state/alerts.json`. The last writer wins.
  - So, in a folder auto-run watches: first run `autorun.py pause all --minutes 10`.
  - Then run `alerts.py add` or `reset`. Then run `autorun.py resume`.
  - If the resume is forgotten, auto-run starts again by itself after 10 minutes.
- Never change a swing stop in `psx/alerts.json` or by hand. `ticket.py stop` is the one command that changes it.

## What it never does

It never places, cancels or changes an order. It never says a price is up to the second, and it never
says where a price is going. It never reads the PSX site unless the user turned it on in their own config.
It never writes `psx/portfolio.json` or `psx/state/broker.json`: it only reads them.

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
