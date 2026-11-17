---
name: psx-broker
description: >-
  Order tickets for the Pakistan Stock Exchange (PSX). Paper trading by default,
  never without your yes. No PSX broker has an order API for retail clients, so
  it never places an order. Each order is a plain ticket: the order, stop and
  target, the max loss at the stop (costs included), why, and the one line to
  type into your broker app. It records your yes word for word, keeps a paper
  ledger with costs, builds the market sell that gets you flat by your flat-by
  time, and logs each trade's max loss for psx-risk. In swing style it keeps
  each plan, makes the stop-limit sell ticket (protect), moves a stop, and
  records a buy that did not fill, bonus shares and a cash fix. A paper fill
  never goes into a ledger of real shares. Use when the user says "place the
  order", "buy it", "execute", "send it to my broker", "close my position",
  "flatten", "get me out", "set up paper trading", "protect my position", "it
  did not fill", "record my bonus shares", "move my stop up", or after /psx-risk
  passes.
argument-hint: "[order number]"
---

# psx-broker

This is the last step before an order, so it is the strictest skill.
No PSX broker gives retail clients an order API. So nothing here places an order.

An order reaches the market only after three gates, every time, for every order:

1. **psx-risk passed this exact order today** (matched by fingerprint).
2. **The user typed an explicit yes for this one order** in the chat.
3. **The user places it in their own broker app**, with their own passwords and PIN.

One PASS from the rules. One yes from the user. Then the user's own hands in the app.
No yes, no order. In paper mode (the default) there is no app step. The yes plus
`result --status placed` fills the paper ledger.

`${CLAUDE_SKILL_DIR}` below is this skill's folder (where this SKILL.md lives).

```bash
python3 "${CLAUDE_SKILL_DIR}/ticket.py" show                     # every ticket, READY or not
python3 "${CLAUDE_SKILL_DIR}/ticket.py" approve --index 1 --reply "yes"
python3 "${CLAUDE_SKILL_DIR}/ticket.py" result --index 1 --status placed     # paper: fills at the limit price
python3 "${CLAUDE_SKILL_DIR}/ticket.py" result --index 1 --status placed --broker-id 12345 --filled-price 100.65
python3 "${CLAUDE_SKILL_DIR}/ticket.py" fill --symbol DEMO --side sell --qty 3428 --price 101.75
python3 "${CLAUDE_SKILL_DIR}/ticket.py" flatten --symbol DEMO
python3 "${CLAUDE_SKILL_DIR}/ticket.py" log
```

New in v2 (most are for swing style, see "Swing style" below):

```bash
python3 "${CLAUDE_SKILL_DIR}/ticket.py" result --index 1 --status expired         # it ended at the close, no fill
python3 "${CLAUDE_SKILL_DIR}/ticket.py" result --fingerprint FP --status expired  # an order of an earlier day
python3 "${CLAUDE_SKILL_DIR}/ticket.py" result --fingerprint FP --date 2026-10-30 --status cancelled   # that day's order
python3 "${CLAUDE_SKILL_DIR}/ticket.py" result --index 1 --status cancelled       # you cancelled it in your app
python3 "${CLAUDE_SKILL_DIR}/ticket.py" flatten --symbol DEMO --limit 97.00       # a limit sell (the pre-open)
python3 "${CLAUDE_SKILL_DIR}/ticket.py" protect --symbol DEMO                     # the stop-limit sell ticket
python3 "${CLAUDE_SKILL_DIR}/ticket.py" stop --symbol DEMO --set 97.00            # move the stop up
python3 "${CLAUDE_SKILL_DIR}/ticket.py" stop --symbol DEMO --scale 0.8333 --why "XB 20%"   # a bonus or a split
python3 "${CLAUDE_SKILL_DIR}/ticket.py" fill --symbol DEMO --bonus 28             # bonus shares at cost 0
python3 "${CLAUDE_SKILL_DIR}/ticket.py" fill --symbol DEMO --side buy --qty 143 --price 99.38 --real
python3 "${CLAUDE_SKILL_DIR}/ticket.py" cash --set 46000                          # fix the ledger's cash
```

`ticket.py` never talks to a broker and never uses the network. It shows tickets,
checks that a reply is a real yes for that order, builds the flatten ticket, keeps
the paper ledger, and keeps the log in `psx/state/broker.json`.
`--now "2026-10-29 10:15"` pins the clock (Karachi time, PKT).

- `--now` and `--today` are for replays, tests and paper only.
- Never pass them to `approve` for real money. With paper off in swing style,
  `approve` of a buy refuses a clock that is not the real one. `approve` of a
  sell prints a note. In day style it says nothing, as before.

## What it reads and writes

| file | what |
| --- | --- |
| `psx/orders.json` | the proposed orders (psx-budget writes it; `flatten` and `protect` replace it) |
| `psx/state/risk.json` | psx-risk's verdicts; only a PASS from today, 5 minutes old or less, is READY |
| `psx/state/broker.json` | every yes, no, placed, skipped, failed, expired, cancelled and filled, with each entry's max loss; also each `stop`, `bonus` and `cash` change |
| `psx/portfolio.json` | cash and shares, updated by `fill` and by `result`; each fill's costs come off the cash. In swing style each position also holds its plan. `"real_holdings": true` marks real shares |
| `psx/plan.json` | today's flat-by time for `flatten`; in swing style, the plan of today's buy for `fill` |
| `psx/config.json` | `paper`, `costs`, `flat_by`, `style`, `swing` and the calendar keys (`holidays`, `open_days`, `ramadan`) |
| `psx/universe.txt` | known symbols: a yes that names another one is refused |

## Your broker

- You trade through a PSX broker's app or website. Examples: KTrade, AKD,
  JS Global, Arif Habib and others. These are examples only, not advice.
- No PSX broker offers retail clients an order API or a Claude connector
  (checked 2026-10-30). So you place each order yourself, in your own app.
- An online order needs two passwords and a PIN (PSX rule 9.7(e)). They
  never go in the chat. Never ask for them. If the user pastes one, tell
  them to delete that message and change it in the app.
- PSX order types: limit, market and market-to-limit. A market order does
  not work in the pre-open. Every order is a day order.
- Stop-loss, bracket and OCO orders are not PSX orders. Some apps have a
  stop-loss feature of their own. The plan stop is yours to put in.
- A market halt cancels all open orders. It comes when the KSE-30 index stays
  5% up or down from its last close for 5 minutes (PSX rule 19.4). Trading
  stops for an hour. The tools cannot see a halt in delayed data. After a
  halt, check your app and put your stop in again.
- Settlement is T+1 (since 2026-02-09). A buy and a sell on the same day net
  out. The paper ledger moves the cash at once.
- Free PSX prices are about 5 minutes late. Check the price in your app
  before you place an order.
- If a broker tool that can place orders ever appears, set it to "Needs
  approval" (Customize > Connectors > tool permissions), never "Always allow".
- `"paper": true` in `psx/config.json` (the default) means practice. Only the
  user switches it off, in their own config.

## How a ticket works

- **READY** means all of this:
  - `psx/state/risk.json` is from today (the Karachi date).
  - It has a PASS for this exact order.
  - The check is 5 minutes old or less. After that, run `/psx-risk` again.
  - An entry (a buy) is inside the entry window (`no_entries_before` to
    `no_entries_after`, moved to the day's hours), and PSX is open.
    In swing style there are no times: PSX is open and past the 2-minute
    opening match, or it is the pre-open and the buy is a limit order.
  - Nobody decided on it today. A failed, skipped, expired or cancelled
    order is READY again after a new check. It still needs a new yes.
- "This exact order" is a fingerprint of these fields: symbol, side, qty,
  type, limit_price, time_in_force, board, stop_loss, take_profit, and
  trigger_price (a stop-limit only). Any change needs a new check. `why` and
  `plan` are not part of it. "BUY" and "buy" are the same side.
- **The ticket** shows the order in plain words, the plan stop and target,
  the max loss, why and the status. It has no line for your app.
  `approve` prints that line, after the yes.
- **Max loss** = qty x (entry - stop) + the costs of both legs (commission,
  sales tax and other charges from `costs`). It always says "costs included".
  The ticket and the log use psx-risk's number. For a market order, the
  ticket also says the entry psx-risk used.
- **A yes counts only if** it starts with "yes" (or "y") and:
  - it has no "?";
  - it has no batch word (all, both, rest, them, sab, dono ...);
  - it has no doubt word after the first word (no, wait, but, if, stop,
    when, lekin, magar, agar, mat ...);
  - it does not say the other side (sell for a buy, buy for a sell,
    becho, khareedo ...);
  - it does not say short, margin, futures or options;
  - it does not say the other order type (market for a limit order, limit
    for a market order);
  - it asks for no change (double, half, more, less, x2, tomorrow,
    next week, Monday, kal, zyada ...);
  - it names no other stock: none from the batch or `psx/universe.txt`,
    and no other word in capitals (like HBL);
  - every number in it is this order's qty, limit, stop, target, trigger or
    max loss.
- "haan", "ok", "sure" and "yes to all" do not count. Symbols with digits
  (BAPLR1, SPAC2, 786) are symbols, not amounts.
- **A paper fill** of a limit order is at its limit price, unless you give
  `--filled-price`. A market order needs `--filled-price`. The leg's costs
  come off the cash and go in the lot as `costs`. PSX trades whole shares.

## Steps: the entry

1. `ticket.py show`. Only READY tickets go to the user. A ticket that is NOT
   READY or BLOCKED goes back to `/psx-risk`.
2. Show ONE ticket and ask: "Place this order? Reply yes or no." One order
   per question. Never offer "yes to all".
3. Run `ticket.py approve --index N --reply "<the user's reply, word for word>"`.
   If it prints "Not recorded", the reply was not an explicit yes for this
   order (for example "sure", "yes to all", or a yes that names another
   stock, amount or side). Ask again. Never turn a reply into a yes yourself.
   If it says "not ready" (for example, the check is more than 5 minutes
   old), run `/psx-risk` again, show the ticket again and ask again.
4. After "Recorded your yes":
   - Paper: `ticket.py result --index N --status placed`. That is the paper fill.
   - Real money: the user places the order in their own app, with the line
     that `approve` printed. Claude never places it.
5. Record what happened:
   - Placed: `ticket.py result --index N --status placed --broker-id ID`.
   - When it fills: add `--filled-price P`. For a part fill, also add
     `--filled-qty Q`.
   - Not placed after all: `--status skipped`.
   - The app refused it: `--status failed --note "why"`.
   - A failed or skipped order needs a new check and a new yes.
   - The log keeps the entry's max loss for psx-risk's daily limit.

## Steps: while it is open, and out by the close

- PSX has no bracket order. After the buy fills, the user may put the plan
  stop in their app as a stop-loss order, if the app has one.
- psx-alerts watches the stop, the target and the flat-by time
  (`alerts.py add --from-plan`).
- When a sell fills (the stop, the target, or by hand), record it:
  `ticket.py fill --symbol DEMO --side sell --qty 3428 --price P`.
- By `flat_by`, anything still open gets closed. The config time (15:20) is
  for Monday to Thursday. `flatten` moves it to the day's hours: 16:20 on a
  Friday, 13:20 on a Ramadan Monday. Today's plan from psx-exit wins when it
  is for the same stock.
  1. Check in your app how many shares you hold.
  2. `ticket.py flatten --symbol DEMO` writes a market sell for the shares in
     `psx/portfolio.json` (or `--qty N` from your app) to `psx/orders.json`.
  3. `/psx-risk`. A sell of shares you hold is an exit. The daily limits and
     the entry window never block it.
  4. `ticket.py show`, then the user's yes for that one order, as above.
  5. Real money: if you put a stop-loss order in your app, cancel it first,
     so it cannot sell the same shares again. Then sell in your app, then
     `result`. Paper: `result --status placed --filled-price P`.
- A stock stuck at its lower price limit may find no buyer. Watch the fill.
- A market order does not work in the pre-open, in the Friday Juma break or
  after the close. The ticket says so when that is the case.

## Example: DEMO on Thu 2026-10-29

DEMO is a made-up company in the sample market. The order is psx-budget's
(3,428 shares, limit 100.65, stop 99.55, target 101.75), and psx-risk passed it.
Paper mode. At 10:15 Karachi time, `ticket.py show` prints:

```
ORDER 1 of 1, PAPER trade: practice, nothing goes to a broker
  BUY 3,428 DEMO, limit 100.65, good for today, REG board
  plan stop 99.55: after the buy fills, put it in your app as a stop-loss order, if your app has one
  plan target 101.75: PSX apps have no bracket order, so psx-alerts watches the stop and the target
  max loss about Rs 4,999.94 if the stop fills at 99.55, costs included (a fast market can fill it worse)
  why: opening-range breakout on DEMO: 3428 shares, bound by your Rs 5,000 max loss per trade (3428 x 1.10 = Rs 3,770.80 at the stop + Rs 1,229.14 costs = Rs 4,999.94, costs included)
  READY: psx-risk PASS, waiting for your yes
  Paper: do not place it in your app. After the yes, ticket.py result --index 1 --status placed records the paper fill.
  Reply "yes" to approve this one order, or "no" to skip it.

One order at a time: a yes covers one ticket, never the batch. Nothing here places an order. Education and tooling, not financial advice.
```

The ticket has no line for the app yet. That line comes after the yes.
The user replies "yes". `ticket.py approve --index 1 --reply "yes"` prints:

```
Recorded your yes for order 1: BUY 3,428 DEMO, limit 100.65, good for today, REG board / plan stop 99.55 / plan target 101.75 / max loss about Rs 4,999.94 if the stop fills at 99.55, costs included.
  In your broker app: BUY DEMO, REG board, quantity 3428, LIMIT price 100.65, valid for the day
Paper trade: nothing goes to a broker, so do not place it in your app. Record the paper fill:
  ticket.py result --index 1 --status placed
```

`ticket.py result --index 1 --status placed` fills it on paper at 100.65.
Cash: Rs 500,000 - Rs 345,028.20 - Rs 617.95 costs = Rs 154,353.85.

```
Recorded order 1 as placed.
Paper fill: BUY 3,428 DEMO at 100.65, costs about Rs 617.95. Cash now Rs 154,353.85 in psx/portfolio.json.
psx-alerts watches the plan (alerts.py add --from-plan): stop 99.55, target 101.75.
Be flat by 15:20 Karachi time: ticket.py flatten --symbol DEMO.
```

At 15:20, `ticket.py flatten --symbol DEMO` prints:

```
Flatten DEMO: SELL 3,428 DEMO, market, good for today, REG board (flat by 15:20 Karachi time).
Wrote it to psx/orders.json (it replaced 1 earlier proposal).
The qty comes from psx/portfolio.json. Check it in your broker app before you say yes.
Next:
  1. psx-risk: check.py. A sell of shares you hold is an exit: the entry window and the daily
     limits never block it.
  2. ticket.py show, then the user's yes for this one order.
  3. Paper: ticket.py result --index 1 --status placed --filled-price P (the price you see then).
```

The sell goes to psx-risk (PASS: an exit) and needs its own yes. With real
money, the user types "SELL DEMO, REG board, quantity 3428, MARKET order,
valid for the day" into their app.

## Swing style

`"style": "swing"` in `psx/config.json` turns it on. A swing trade is held
for days, up to its exit-by day. Try swing trades on paper first, in a folder
of their own (never turn paper on in a folder that holds real shares). Swing
trading loses money for many people too. Every order still needs a psx-risk
PASS of that exact order and your yes.

### The plan lives in the ledger

- When a swing buy fills, `result` (or `fill`) writes its plan into
  `psx/portfolio.json`, on the position: `stop`, `stop_at_buy` (the stop at
  the buy, it never changes), `target`, `exit_by`, `exit_by_time`, the trend
  rule, `max_loss` and `scaled`.
- psx-alerts and psx-risk read the plan from there. When the shares are sold,
  the position goes, and its plan and alerts go with it.
- `fill` takes the plan of today's swing buy in `psx/orders.json`, else
  today's `psx/plan.json`. A plan of another day does not count. Then give it
  by hand: `--stop`, `--target` and `--exit-by`. With no plan, `fill` writes
  nothing and says so.
- A day buy gets no plan in the ledger.

### A share you held before the switch

- A share with no plan in the ledger is not a swing position: a day trade, or
  a share you bought before you set `"style": "swing"`.
- No command gives it a plan. `--stop`, `--target` and `--exit-by` are for a
  new position only. `protect` and `stop` refuse it, and say so.
- Only your own rules in `psx/alerts.json` watch it. psx-risk counts its risk
  as your max loss per trade.
- So switch to swing only after such a share is sold. If you switch while you
  hold it, also watch its stop in your broker app. See the README, "If you
  already hold shares".

### The buy, and a buy that did not fill

- A swing buy is a limit buy. You may place it in the pre-open: the ticket
  is READY then. A market buy in the pre-open is not.
- A PSX order lasts one day. If it does not fill, it ends at the close. Do
  not chase it.
- Record that: `ticket.py result --index 1 --status expired`. On a later day,
  name the order by its fingerprint: `ticket.py result --fingerprint FP
  --status expired`, or by `--symbol DEMO --date 2026-10-29`. `approve` prints
  the fingerprint, and psx-risk's block line shows it.
- That way only `expired`, `skipped` or `cancelled` can be recorded. It needs
  no `psx/orders.json` and writes that one record only. A fill is recorded
  with `ticket.py fill`.
- The log keeps each order by its day. The same order put in again on another
  day (a protect sell, each day) has the same fingerprint, but it is another
  order. `--fingerprint FP` alone closes the newest open one and says its day.
  If an older one is open too, it says so, with the `--date` to use.
  `--fingerprint FP --date D` closes the order of day D. `--symbol X --date D`
  looks only at day D, and an order that filled does not count there.
- psx-risk blocks a new swing buy while an older buy has no fill and no
  expired, skipped or cancelled record.
- Only part of a buy filled? Then `result` (with `--filled-qty Q`) and
  `fill` say how many shares may still fill today. Record each fill with
  `ticket.py fill`. psx-risk counts the rest as a buy with no fill yet, until
  the close. To close the rest in the log, record it expired or cancelled.
  The fill stays.

### The stop-limit ticket (protect)

- After the buy fills: `ticket.py protect --symbol DEMO`. It writes one
  stop-limit sell of the shares in `psx/portfolio.json` (or `--qty N`) to
  `psx/orders.json`.
- The trigger is the plan stop. The limit is 1% under it
  (`swing.stop_limit_gap_pct`), rounded down: 96.25 gives 95.28. It has no
  `--stop` flag: `ticket.py stop` changes a stop.
- Then psx-risk, `show` and your yes, as for every order. The ticket asks for
  "yes 96.25". "yes, put the stop" is not a yes. `approve` prints the line.
- In your app it is a stop-limit (stop-loss) order. In FS EDGE, for example,
  the trigger goes in the "Trigger Price" field. Check the words in your own
  app.
- Treat it as a day order. Put it in again each day after the opening match,
  while you hold the shares. psx-alerts reminds you at the first check (paper
  off only).
- No order guards the opening price. A gap at the open can go past your stop.
- It sells only at its limit or better. If the price opens or falls under the
  limit, it may not fill. Then sell by hand (`ticket.py flatten`).
- A market halt cancels every open order at PSX. After the restart, check it
  in your app. If it is gone, record it cancelled first: `ticket.py result
  --fingerprint FP --status cancelled`. Then `protect` again, psx-risk and a
  new yes. Until then `show` says "DONE: placed" and names that step, and
  `protect` says a stop-limit of these shares is open today.
- While it rests, psx-risk refuses a second sell of the same shares. Cancel
  it in your app first, then record it: `ticket.py result --fingerprint FP
  --status cancelled` (or `--index 1` on the same day). `approve` prints this
  line with `--date` and the day, so it still names that order on a later day.
- `result --status placed` of it fills nothing. When it fills, record that
  with `ticket.py fill`.
- If only part of it filled, the rest still rests in your app. Cancel the rest
  there, then record it cancelled: that closes the rest, and the fill stays in
  the log. `flatten` says "Part of it filled" then.
- Paper mode writes no order. A paper stop rests nowhere: psx-alerts rings at
  the stop, then you flatten.

DEMO, 143 shares bought at 99.38 on Thu 2026-10-29 (a Rs 500 max loss), plan
stop 96.25. Paper off. On Fri 2026-10-30 at 9:35 AM, `ticket.py protect
--symbol DEMO` prints:

```
Protect DEMO: SELL 143 DEMO, stop-limit, trigger 96.25, limit 95.28, good for today, REG board.
The trigger is the plan stop in psx/portfolio.json. The limit is 1% under it (swing.stop_limit_gap_pct in psx/config.json).
Wrote it to psx/orders.json (it replaced 1 earlier proposal).
The qty comes from psx/portfolio.json. Check it in your broker app before you say yes.
Next:
  1. psx-risk: check.py. A sell of shares you hold is an exit: the entry window and the daily
     limits never block it.
  2. ticket.py show, then the user's yes for this one order: "yes 96.25".
  3. ticket.py approve prints the line to type into your broker app. Then record it: ticket.py result
     --index 1 --status placed --broker-id ID. When it fills: ticket.py fill.
```

psx-risk passes it. `ticket.py show` prints:

```
ORDER 1 of 1, REAL MONEY: you place it yourself in your broker app
  SELL 143 DEMO, stop-limit, trigger 96.25, limit 95.28, good for today, REG board
  why: protect DEMO: the plan stop 96.25 as a stop-limit sell in your broker app
  READY: psx-risk PASS, waiting for your yes
  note: PSX orders last one day. If your broker app ends this order at the close, put it in again each day after the opening match, while you hold DEMO (ticket.py protect --symbol DEMO). psx-alerts reminds you at the first check. Check its validity in your app.
  note: No order guards the opening price. A gap at the open can go past your stop.
  note: A stop-limit sells only at 95.28 or better. If the price opens or falls under 95.28, it may not fill: then sell by hand (ticket.py flatten).
  note: A market halt cancels every open order at PSX, and may cancel this one too.
  note: While this order rests, a second sell of the same shares is refused by psx-risk. Cancel it in your app first, and record it: ticket.py result --fingerprint 4f1f7cf1107d6b31 --status cancelled.
  Real money: the line to type into your broker app comes after your yes.
  Reply "yes 96.25" to approve this one order, or "no" to skip it.

One order at a time: a yes covers one ticket, never the batch. Nothing here places an order. Education and tooling, not financial advice.
```

The user replies "yes 96.25". `ticket.py approve --index 1 --reply "yes 96.25"` prints:

```
Recorded your yes for order 1: SELL 143 DEMO, stop-limit, trigger 96.25, limit 95.28, good for today, REG board.
Now place it yourself in your broker app:
  SELL DEMO, REG board, quantity 143, STOP LIMIT trigger price 96.25, limit price 95.28, valid for the day
Free PSX prices are about 5 minutes late: check the price in your app before you place it.
Your app asks for your passwords and PIN. Type them in the app only, never in this chat.
Then record what happened: ticket.py result --index 1 --status placed --broker-id <the app's order number>, or --status skipped, or --status failed --note "why".
If you cancel it later in your app, record it: ticket.py result --fingerprint 4f1f7cf1107d6b31 --date 2026-10-30 --status cancelled.
```

### Out of a swing trade (flatten)

- `ticket.py flatten --symbol DEMO` writes a market sell of the shares you
  hold. Its why is "close the DEMO swing position". There is no flat-by time:
  the plan's exit-by day is the time stop.
- PSX takes no market order in the pre-open. Then use a limit sell:
  `ticket.py flatten --symbol DEMO --limit 97.00`.
- If a stop-limit sell of these shares is open today, `flatten` says so.
  Cancel it in your app first, then record it:
  `ticket.py result --fingerprint FP --status cancelled`.

### Move the stop (stop)

- `ticket.py stop --symbol DEMO --set 97.00` moves the plan stop up. It is
  rounded down to the tick. A lower stop is refused: "move a stop up only".
- On an ex-date with a bonus, a right or a split, psx-alerts asks you to
  choose. `ticket.py stop --symbol DEMO --scale 0.8333 --why "XB 20%"` scales
  the stop (rounded down) and the target (half up). `--scale 1` keeps them.
- A scale under 1 lowers the stop, so it needs that ex-date. It must be from
  the buy day to today: a new XB or XR flag, or a split (an LDCP change of 10%
  or more with no flag), in the closing files in `psx/data` (`--data`). Or
  one psx-alerts saw, also on the company page in the morning
  (`psx/state/alerts.json`, `--alerts`). An XD (a cash payout) does not count.
- A scale is never under the ex-date's factor, and one ex-date takes one
  scale. Else nothing changes. A fall in the price is not an ex-date: then
  the stop moves up only.
- The choice goes into the plan's `scaled` list and the log:

```
DEMO stop 96.25 to 80.20, target 105.64 to 88.03 (scale 0.8333: XB 20% on Thu 2026-11-12). Your stop-limit in the broker app is not changed. Make a new one: ticket.py protect --symbol DEMO.
```

- `stop_at_buy` never changes. A stop lowered by hand in the file gets a
  warning from psx-risk and psx-alerts.
- The tools never move a stop by themselves. `stop` is the one command that
  does, and only at your word.

### Bonus shares (fill --bonus)

- When the bonus shares come, `ticket.py fill --symbol DEMO --bonus 28` adds
  them at cost 0. The cash does not change. The old cost is spread over all
  the shares (FBR rule 13N). It is a "bonus" record, not a fill, so psx-risk
  does not count it as a trade:

```
Recorded 28 bonus shares of DEMO at cost 0: 171 shares now, the same total cost. Record the bonus shares your broker app shows. The company may keep back 10% of them until a tax is paid (section 236Z).
```

### Real shares (real_holdings)

- `"real_holdings": true` at the top of `psx/portfolio.json` marks a file of
  real shares. Both styles.
- Paper mode: `result` and `fill` refuse a fill into it, and write nothing.
- `fill --real` ("this is a real fill from my broker app") records a real
  fill there while paper is on, for example in the long-term folder. The
  same goes for `fill --bonus`.
- A fill with paper off sets the flag, and so does `fill --real`. Paper mode
  never sets it.
- A ledger from before v2, or one made by hand, has no flag, even when its
  shares are real. So paper mode also refuses a fill into a file with no flag
  that shows a sign of real shares:
  - a top key the tools never write, like a `"note"` or `"as_of"`;
  - a yes in `psx/state/broker.json` made with paper off;
  - in swing style, a held share with no swing plan (no swing fill made it).
- Then it writes nothing. Ask the user which it is. Real shares: put
  `"real_holdings": true` at the top. A paper file: put `"real_holdings":
  false` at the top.
- Does a trading folder hold real shares or real cash? Then do not turn paper
  on there. On paper, every ticket says "do not place it in your app". But a
  real share needs a real sell, for example when its stop is hit.
- To practise, make a new folder. Copy `psx/config.json` and `psx/data/` into
  its `psx/`, and set `"paper": true` there. Do not copy `psx/portfolio.json`:
  the paper cash then starts from its `"budget"`.
- To lock a folder of real shares, put `"real_holdings": true` at the top of
  its `psx/portfolio.json`. Then a paper fill into it is refused, and nothing
  is written. Still keep paper off in a trading folder like that.
- When you go from paper to real money, start a fresh `psx/portfolio.json`,
  so paper and real positions never mix.
- The long-term folder is the one with paper on and `"real_holdings": true`.
  There psx-invest writes no `psx/orders.json`, so there is no ticket and
  nothing for `result`. Record each real fill with `ticket.py fill ... --real`.

### Blocked shares (both styles)

- The config's `"blocked"` list holds your long-term shares, so the trading
  tools leave them alone.
- `fill` refuses a buy of a share on that list, and writes nothing. It may
  belong in the long-term folder. If it really is a trade of this folder, add
  `--blocked-ok`. A sell and `fill --bonus` are never refused for this.
- `flatten` and `protect` of a blocked share print one line: these may be
  long-term shares, so check the folder before you say yes.

### Cash

- `ticket.py cash --set 46000` sets the cash in `psx/portfolio.json`. It
  prints the old and the new number, and logs it. Nothing else changes.
- One broker account holds the cash of both folders (trading and long-term).
  Never count the same money twice.
- PSX settles T+1. A buy and a sell on the same day net out. The paper ledger
  moves the cash at once.
- In swing style, commission counts on both sides, also on a same-day sell.

### Paper fills that match PSX

- A paper buy should record the price PSX really traded: `--filled-price P`.
  If PSX opened under your limit, that is the open.
- If PSX never traded at your limit, the paper buy did not fill. Record it
  expired.

## What it never does

- Never places an order. It has no broker link and no network.
- Never takes two orders on one yes, and never turns a reply into a yes.
- Never runs from a scheduled or background task: nobody is there to say yes.
- Never asks for, reads, stores or repeats passwords, PINs or login details.
- Never switches `"paper"` off. The user does that in their own config.
- Never promises a fill price. A market order and a stop fill at whatever the
  market gives, and a halt cancels open orders.
- Never records a sale of shares you do not hold (PSX bans blank sales).
- Never prints a profit, a P&L or a return.
- Never moves a stop by itself. Only `ticket.py stop`, at your word. It never
  lowers a stop, except to match a bonus, rights or split ex-date.
- Never writes a paper fill into a file of real shares (marked, or with signs
  of real shares).

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
