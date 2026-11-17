---
name: psx-risk
description: >-
  Risk Manager for the Pakistan Stock Exchange (PSX). Checks every order against
  your limits and the PSX rules, before psx-broker shows it. Day trades: a stop
  is needed, and it checks the loss at the stop (costs included), reward:risk,
  the day's total risk, trades per day and entry times (Karachi time). Swing
  trades add your open positions, the open risk across days and the loss if the
  next day opens at the lower price limit. PSX rules: the REG board, the Rs 0.01
  tick, today's price limits, ordinary shares only and no blank sales. It also
  checks order size, position cap, cash buffer, no margin and duplicates.
  Getting out is never blocked by a day or swing limit. Prints PASS or BLOCK
  with the reason and records it, so psx-broker shows only an order that passed.
  Use when the user says "check my order", "is this safe", "risk check", "does
  this break my rules", "can I take this trade", "how much have I risked today",
  "can I add another swing trade", or before /psx-broker, always.
argument-hint: "[path to orders.json]"
---

# psx-risk

The Risk Manager is the gate between a proposal and the ticket. Every order
from psx-budget, or from psx-broker's flatten, goes through it.

A BLOCK is final for that order. It does not go to the user for a yes, and
psx-broker prints no ticket for it.

Most people who day trade lose money. These limits keep each loss and each
day's losses small. They do not make a trade win.

`${CLAUDE_SKILL_DIR}` below is this skill's folder (where this SKILL.md lives).

```bash
python3 "${CLAUDE_SKILL_DIR}/check.py"                           # psx/ files; writes psx/state/risk.json
python3 "${CLAUDE_SKILL_DIR}/check.py" --json
python3 "${CLAUDE_SKILL_DIR}/check.py" --no-write                # look without recording
python3 "${CLAUDE_SKILL_DIR}/check.py" --now "2026-10-29 10:15"  # pin the clock (Karachi time)
python3 "${CLAUDE_SKILL_DIR}/check.py" --offline --data DIR      # PSX files from DIR, no network
```

## What it reads and writes

| file | what |
| --- | --- |
| `psx/orders.json` | the proposed orders (psx-budget, or psx-broker's flatten) |
| `psx/config.json` | the limits (psx-budget ships `config.example.json`); `"style"` is `"day"` or `"swing"` |
| `psx/portfolio.json` | cash and holdings; if missing, a fresh account funded with the budget. In swing also each position's plan stop (open risk) |
| `psx/prices.json` | a fresh price raises the entry it measures risk from; today's price limits |
| `psx/state/broker.json` | what was placed today: duplicates, trades per day, daily loss. In swing also the buys and sells with no fill yet, and older buys with no fill |
| `psx/universe.txt` | your ordinary PSX shares (psx-scanner); a buy must be on it |
| `psx/data/tape/<date>/<SYM>.jsonl` | today's company tape: a fresh price when `psx/prices.json` has none |
| `psx/data/company/<SYM>.html` | a saved company page: today's price limits (the circuit breaker), and a fresh price |
| `psx/data/mkt_summary/` | PSX closing files: the last close, the kind of share, computed limits. In swing also the ex-dates behind a `ticket.py stop --scale` |
| `psx/plan.json` | swing, read only (`--plan`): the LDCP the plan was made on, when it is the plan of the order |
| `psx/state/alerts.json` | swing, read only (`--alerts`): psx-alerts' record of ex-dates, behind a `ticket.py stop --scale` |
| `psx/state/risk.json` | the verdicts it writes, with a fingerprint of each exact order and the check time (`checked_at`, the `--now` time) |

Network: none by default.

- Only with `"psx_site": true` in `psx/config.json` it may fetch a company page
  from the PSX site, for today's price limits. Then it asks the site first. If
  the site fails, it uses the saved page.
- Never with `--offline`, and never with `--now` (the site only has today).
- Turn the site on only if PSX has given you permission.

## Entries and exits

An **entry** opens or adds to a position: a buy. A sell of more than you hold
is an entry too, and it is always blocked.

An **exit** only cuts what you already hold. Getting out must always be
possible. So an exit is checked for format and blank sales only.

Every other rule turns into a warning for an exit, never a BLOCK: day limits,
the entry window, loss, price limits, the blocked list, size, duplicates, an
old orders file. Selling a held ETF, right, REIT or fund only warns too.

One exception: a future, an index, a GEM board share or debt is blocked even
for a sell. They do not trade on the REG board.

In swing style no swing check ever blocks an exit. One blank-sale check is
added: a sell placed today with no fill yet already uses its shares, so a
second sell of the same shares is blocked (see "Swing style").

## The checks

Orders are checked in file order, as if each passed order had filled. So a
batch that is fine order by order, but breaks a limit together, is caught.

| check | blocks when |
| --- | --- |
| format | no symbol; side not buy or sell; qty not a whole number above 0; type not `limit` or `market`; a limit order with no `limit_price`; a price off the Rs 0.01 tick; `time_in_force` not `day`; `board` not `REG`; a market order in the pre-open; a field PSX does not have (`notional`, `order_class`, `stop_price`, `extended_hours`) |
| asset | not an ordinary PSX share: a future (OGDC-NOV), an ETF, debt, an index, a fund, a REIT, a right or a preference share. For a buy, also: not in `psx/universe.txt` (when that file is there), or SUSPENDED on its company page |
| short | a sell of more than you hold. PSX bans blank sales, so this blocks whatever `allow_short` says |
| blocked | (entries) the symbol is on the `blocked` list |
| size | (entries) under `min_order_pkr` or over `max_order_pkr` |
| position | (entries) the stock would be over `max_position_pct` of the account |
| cash | (entries) the buy and its costs would leave less than the cash buffer, or need margin (never allowed) |
| stop | (entries) no stop while `require_stop` is true (the order's `stop_loss`, or the plan's stop); a stop at or above the entry |
| loss | (entries) the max loss at the stop, costs included, over `max_loss_per_trade_pkr` |
| reward:risk | (entries) (target minus entry) / (entry minus stop) under `min_reward_risk` |
| limits | (entries) a limit price or entry outside today's price limits; a target above the upper limit (it cannot fill today) |
| daily loss | (entries) the max losses of today's entries, plus this one, over `max_daily_loss_pkr` |
| trades | (entries) `max_trades_per_day` entries already placed today |
| window | (entries) before `no_entries_before` or after `no_entries_after`; or the market is not open: closed, pre-open, the 2-minute opening match, the Friday break, post-close. The market check holds even when your times are off |
| price | (entries) a market order with no fresh price and no plan entry to measure the risk from |
| date | (entries) `psx/orders.json` was made on another day (its `created_at`, as a Karachi date) |
| duplicate | (entries) the same symbol and side twice in one batch, or already placed today |
| daily limit | (entries) `max_orders_per_day` orders already placed today |
| style | (buys, both styles) a swing plan in a day folder; in a swing folder a day plan or a buy with no plan. A psx-invest plan passes in both |
| window (swing) | (buys) PSX is not open, or the 2-minute opening match runs, or a market buy in the pre-open. Your `no_entries_*` times are not used |
| limits (swing) | (buys) an entry outside today's price limits. A target over the upper limit is only a note |
| open (swing) | (buys) you already hold the stock: one swing plan a stock |
| fill (swing) | (buys) a buy approved or placed on an earlier day has no fill, and no "expired", "skipped" or "cancelled" record |
| positions (swing) | (buys) what you hold, today's buys with no fill yet, earlier passes in this batch and this one, over `swing.max_open_positions` |
| open risk (swing) | (buys) the max loss at the stop of all of those, costs included, over `swing.max_open_risk_pkr` (null: `max_daily_loss_pkr`) |
| gap (swing) | (buys) the loss if the next session opens at its lower price limit, costs included, over `swing.max_gap_loss_pkr` (null: 3 x `max_loss_per_trade_pkr`) |
| ex-date (swing) | (buys) today's LDCP (the company page, or `psx/prices.json`) is not the LDCP the plan was made on: an ex-date, a split or days with no trade moved it |
| cash (swing, psx-invest) | (buys) the cash is checked after today's buys with no fill yet; a buy in the log with no price |
| format (swing) | a stop-limit order that is not a sell of shares you hold; no `trigger_price` or `limit_price`; a limit over the trigger; a trigger at or over the price now (the block says why, see "Sells in swing") |
| short (swing) | a sell of shares that a sell placed today, with no fill yet, already covers (a part fill keeps the rest open) |

How the numbers work:

- **The entry it measures from.** A limit order: its limit price. A market
  order: the HIGHER of the plan's entry and a fresh price. Fresh means 15
  minutes old or less, by its data time. Free PSX data is about 5 minutes late.
- **Where a fresh price comes from**, in this order (psx-budget uses the same):
  - `psx/prices.json`;
  - today's company tape, `psx/data/tape/<date>/<SYM>.jsonl`;
  - the saved company page, by its "As of" time.
- **An older price is never used for an entry.** It says so.
  - A market order needs a fresh price. Without one it is blocked, even when
    the plan has an entry: that entry can be hours old.
  - So with no fresh price, use a limit order. Its limit price is what the
    risk is measured from.
  - An exit can still show its value at an old price.
- **Max loss, costs included.** Shares x (entry minus stop), plus the round
  trip costs: commission, sales tax and fees on the buy, and on the sell at
  the stop. psx-budget sizes with the same number.
- **Reward:risk** is compared exactly, in paisa, with no rounding first. The
  report shows it rounded to 2 decimals. psx-exit and psx-budget use the same
  rule.
- **Costs warning.** It warns when the costs are over 25% of the price risk,
  shares x (entry minus stop). You pay the costs win or lose.
- **Daily loss** counts the full max loss of every entry today, win or lose,
  as psx-broker logged it. Three full-size trades use up a Rs 15,000 day.
- **What counts as placed today** (for trades, daily loss and duplicates):
  - an order you said yes to, until it is recorded as skipped or failed;
  - a placed order;
  - a fill you recorded by hand (`ticket.py fill`). It has no max loss, so it
    is not in the daily loss: it warns.
- **Cash after** takes off the value and the buy costs of each passed buy,
  like a paper fill. A yes with no fill recorded yet is not taken off: it
  warns.
- **Today's price limits**, in this order (the tool says which one it used):
  - `psx/prices.json`, only when its lower and upper are from the company
    page (`"limits_from": "company page"`, psx-alerts writes it);
  - the company page as of today: the PSX site first when it is on, else the
    saved page;
  - else computed from the last close. On an ex-date PSX lowers the base, so
    computed limits can be too high: it warns.
- **The window** is Karachi time (UTC+5, no daylight saving), never the
  computer's clock zone. The config times are for Monday to Thursday. On
  other days they move:
  - Friday: 09:30 and 16:00.
  - Ramadan, Monday to Thursday: 09:30 and 13:00.
  - Ramadan Friday: 09:30 and 12:00.
- **The market must be open** for an entry. Weekends, PSX holidays, the
  pre-open, the opening match and the Friday break always block. Set a
  `no_entries_*` time to null to switch off only that time.
- **An old orders file.** An entry is blocked when `psx/orders.json` was made
  on another day. Make a new plan.

Warnings do not block, but say them to the user:

- a LIVE account (`"paper": false`). Only `false` is live: anything else is
  paper, as in psx-broker;
- the stop and the target live only in the plan. PSX has no stop or bracket
  order. Set a stop in your broker app if it has one; psx-alerts watches both;
- a price too old to use;
- a yes with no fill recorded yet (its cash is not taken off);
- a fill recorded by hand (it has no max loss);
- an entry 30 minutes or less before the Friday break;
- costs over 25% of the price risk;
- a stop at or below today's lower limit;
- price limits that are computed, or not known;
- a tag like NON-COMPLIANT or WINDING-UP on the company page;
- no `psx/universe.txt` yet;
- a holiday or Ramadan date that is only expected (check PSX notices).

When an order passes, the report ends with a note: a market halt at PSX
cancels every open order, and delayed data cannot show a halt.

## Steps

1. If the price may have moved since the plan, refresh it first
   (psx-alerts: `alerts.py quote DEMO --write`). That also writes today's
   price limits.
2. Run `check.py`. Exit code 0 means every order passed. 1 means at least one
   was blocked.
3. Tell the user the result in plain words, order by order: the max loss at
   the stop (costs included), reward:risk, today's price limits, and how much
   of today's limits it uses.
4. For a BLOCK, give the reason and the fix: fewer shares, a closer stop from
   psx-exit, wait for the window, or skip the trade. Never change a limit
   yourself.
5. If the order changes in any way, run the check again. psx-broker matches
   each order to its verdict by fingerprint. So an edited order is not ready
   until it passes again, and a verdict from yesterday does not count today.
6. Run the check again right before the yes. psx-broker does not take a yes
   for a verdict more than 5 minutes old.

## Example

The DEMO order from psx-budget at 10:15 AM on Thursday 2026-10-29. A fresh
Rs 500,000 paper account, the example config. (DEMO is a made-up company in
the test data.)

```
PASS  #1 buy DEMO 3428 shares, entry
          entry 100.65 (the limit price), stop 99.55, target 101.75: risk 1.10 a share
          max loss Rs 4,999.94 (limit Rs 5,000), costs included, reward:risk 1.00 (min 1)
          today before this: 0 of 3 trades, Rs 0 of Rs 15,000 daily loss
          today's price limits 88.56 to 108.24 (company page)
        ~ Costs are about 33% of the price risk (over 25%). You pay them win or lose.
        ~ the stop 99.55 and the target 101.75 live only in the plan (PSX has no stop or bracket
          order): set a stop in your broker app if it has one; psx-alerts watches both

1 passed, 0 blocked at 2026-10-29 10:15 Karachi time. Cash after the passed orders: Rs 154,353.85 (paper account).
Every order passed. psx-broker still asks you yes or no for each one.
A market halt at PSX (the KSE-30 index 5% up or down for 5 minutes) cancels every open order.
Delayed data cannot show a halt: after one, check your orders in your broker app.
Education and tooling, not financial advice.
```

- The max loss is Rs 3,770.80 from the price and Rs 1,229.14 in costs.
- Costs are 32.6% of the price risk (1,229.14 / 3,770.80), over 25%, so it
  warns.
- Cash after: Rs 500,000 - Rs 345,028.20 - Rs 617.95 buy costs = Rs 154,353.85.

One more share and it is blocked:

```
BLOCK #1 buy DEMO 3429 shares, entry
          entry 100.65 (the limit price), stop 99.55, target 101.75: risk 1.10 a share
          max loss Rs 5,001.40 (limit Rs 5,000), costs included, reward:risk 1.00 (min 1)
          today before this: 0 of 3 trades, Rs 0 of Rs 15,000 daily loss
          today's price limits 88.56 to 108.24 (company page)
        - loss: 3429 shares x 1.10 = Rs 3,771.90 at the stop + Rs 1,229.50 costs = Rs 5,001.40,
          over your Rs 5,000 max loss per trade (costs included)
```

The same 3,428 shares at 9:40 are blocked by the window:

```
        - window: no new entries before 09:45 Karachi time (it is 09:40)
```

The 3:20 PM sell that closes the position passes. It is an exit, so the
window and the day limits never block it:

```
PASS  #1 sell DEMO 3428 shares, exit
          value Rs 348,216.24 at 101.58 (the latest price), sell costs about Rs 623.66
```

## Swing style

Set `"style": "swing"` in `psx/config.json` to hold a trade for days. `"day"`
is the default. The style is set in the config only, never by a flag. Any
other word is one plain error.

Swing trading loses money for many people too. Try it on paper first, in a
folder of its own. Never turn paper on in a folder that holds real shares or
real cash. See "Paper and real shares" in the README.

- With paper on, the report warns when `psx/portfolio.json` holds real shares
  (`"real_holdings": true`). It also warns at a sign of them: a top key the
  tools never write (like a `"note"`), a yes made with paper off, or a held
  share with no swing plan. psx-broker records no paper fill in such a file.
- Then the last line says so, in place of "(paper account)".

Every check above still holds. Swing adds these, for a buy only:

- **Styles do not mix.** A day plan, or a buy with no plan, is blocked in a
  swing folder. A swing plan is blocked in a day folder. A psx-invest plan
  (`"style": "invest"`) passes in both. It is checked as a buy with no stop.
- **The window.** PSX must be open, past the 2-minute opening match. In the
  pre-open a limit buy is fine: it waits for the opening match. A market buy
  is not. `no_entries_before` and `no_entries_after` are day rules, so swing
  does not use them.
- **The target.** A target over today's upper limit is a note, not a block.
  It cannot fill today, but it can on a later day.
- **A stop at the lower limit.** Both cases only warn.
  - A stop under today's lower limit cannot be met today. It counts from the
    next session.
  - A stop exactly at the limit can be met today: a trade at the limit meets
    it. At the limit there may be no buyers.
- **An ex-date on the buy day.** A plan made the evening before works from
  the last close. On the buy day the company page (or `psx/prices.json`)
  shows today's LDCP. If it is not the LDCP the plan was made on, the buy is
  blocked. An ex-date, a split or days with no trade moved it. So the plan's
  entry and stop are on old prices. Make a new plan with psx-exit, then size
  it again.
  - The plan's LDCP comes from `psx/plan.json` (`--plan`), when it is the
    plan of this order. Else it is the last close in the closing files.
  - With computed limits (no company page of today), this is not checked.
  - A stop at or over today's LDCP warns: a limit buy can fill lower, at or
    under the stop.
- **One plan a stock.** A buy of a stock you already hold is blocked.
- **An earlier buy with no fill.** A buy approved or placed on an earlier day,
  with no fill and no "expired", "skipped" or "cancelled" record, blocks new
  buys. The block line has the exact line to clear it, like
  `ticket.py result --fingerprint FP --status expired`.
- **Open positions.** What you hold (every position in `psx/portfolio.json`),
  plus today's buys with no fill yet, plus earlier passes in this batch, plus
  this one. Over `swing.max_open_positions` (3) is blocked.
- **Open risk.** The max loss at the stop of each of those, costs included.
  Over `swing.max_open_risk_pkr` is blocked. Null means `max_daily_loss_pkr`.
  - A held position counts from its cost a share and the stop in its plan in
    `psx/portfolio.json`. A stop at or over the cost counts 0.
  - A position with no plan stop counts as your max loss per trade. It warns.
  - A stop lowered by hand (under its `"stop_at_buy"`) warns. The lower stop
    is the one that counts.
  - A `ticket.py stop --scale` record counts only when the data shows a
    bonus, rights or split ex-date for it. The data: the closing files
    (`--data`), or psx-alerts' record in `psx/state/alerts.json`
    (`--alerts`). A record with no such ex-date does not count. So a stop
    under its `"stop_at_buy"` warns, and the warning names the record.
  - A record under its ex-date's factor counts as that factor, the most
    `ticket.py stop --scale` takes.
  - After `ticket.py stop --scale F` the stop is on the new price scale at
    once. The cost a share and the shares move to it only when you record
    the new shares (`ticket.py fill --bonus N`). Until then the open risk
    uses the stop before the scale, so all three are on the old scale. It
    warns until the bonus or split shares are recorded.
- **The gap loss.** The loss if the next session opens at its lower price
  limit (10% under the entry), costs included. The report shows it for every
  swing buy. Over `swing.max_gap_loss_pkr` is blocked. Null means 3 x your
  max loss per trade.
- **Waiting buys and the cash.** Today's buys with no fill yet (a yes, or
  placed) come off the cash first. So two buys can never spend the same
  rupees. A psx-invest order gets this rule in both styles. A buy in the log
  with no price blocks: record its fill, or record it expired.
  - They count as held at their price, as if filled. So the account total,
    the cash buffer and the position cap are the ones psx-budget uses.
  - The warning gives the exact line to record each one expired, like
    `ticket.py result --fingerprint FP --status expired`.
  - A buy filled in part: the other shares may still fill today. Their cash
    and their risk still count, until the close. A PSX order ends at the
    close, so the rest stops counting after that day.

What 0 means in the swing block:

- `swing.max_open_positions` or `swing.max_open_risk_pkr` set to 0 is off, as
  0 is for the day limits.
- `swing.max_gap_loss_pkr` set to 0 is a limit of Rs 0, so every swing buy is
  blocked. The gap loss must have a cap. psx-budget reads 0 the same way.
- Null keeps the default rule above. With null and no
  `max_loss_per_trade_pkr`, there is no gap limit, in psx-budget too.
- Anything else that is not a number is one plain error.

**The daily loss** keeps its day meaning: the max loss of the buys you
placed today, the new risk added today. **The open risk** is the risk of
everything you hold, bought on any day. A gap at the open is in neither: it
can lose more than the max loss.

Costs: in swing every sell pays commission, whatever `"day_trade_one_side"`
says. A sell on a later day always pays it.

The report says once: "A gap can open past a stop: a loss can be bigger than
its max loss."

Check a swing buy on its buy day: in the pre-open, or after the opening
match. `psx/orders.json` must be made that day (the date check).

### Swing example

The DEMO swing buy from psx-budget, in the pre-open at 9:20 AM on Thursday
2026-10-29 (`tests/fixtures/psx-v2/contract/orders-swing.json`). A fresh
Rs 500,000 paper account, the example config with `"style": "swing"`.

```
PASS  #1 buy DEMO 1436 shares, entry
          entry 99.38 (the limit price), stop 96.25, target 105.64: risk 3.13 a share
          max loss Rs 4,997.81 (limit Rs 5,000), costs included, reward:risk 2.00 (min 1)
          gap loss Rs 14,759.46 if it opens at the lower limit 89.44 (limit Rs 15,000)
          today before this: 0 of 3 trades, Rs 0 of Rs 15,000 daily loss
          open before this: 0 of 3 positions, Rs 0 of Rs 15,000 open risk (costs included)
          today's price limits 88.56 to 108.24 (company page)
        ~ the stop 96.25 and the target 105.64 live only in the plan (PSX has no stop or bracket
          order): after the buy fills, ticket.py protect makes a stop-limit ticket for your broker
          app; psx-alerts watches both

1 passed, 0 blocked at 2026-10-29 09:20 Karachi time. Cash after the passed orders: Rs 357,034.73 (paper account).
Every order passed. psx-broker still asks you yes or no for each one.
A gap can open past a stop: a loss can be bigger than its max loss.
A market halt at PSX (the KSE-30 index 5% up or down for 5 minutes) cancels every open order.
Delayed data cannot show a halt: after one, check your orders in your broker app.
Education and tooling, not financial advice.
```

- The gap line: if Friday opens at the lower limit 89.44, the 1,436 shares
  lose about Rs 14,759.46, costs included. That is about 3 times the max
  loss at the stop.
- The gap limit is Rs 15,000: 3 x the Rs 5,000 max loss per trade. With
  Rs 500 a trade, 143 shares lose about Rs 1,469.78 in a gap (limit Rs 1,500).
- At 9:31 AM the same buy is blocked: the opening match runs until 9:32 AM.

### Sells in swing

- A sell of shares you hold is an exit. No swing check blocks it.
- **A stop-limit sell** (`"type": "stop_limit"`, from `ticket.py protect`)
  passes as an exit when:
  - it has a `trigger_price` and a `limit_price`, both on the Rs 0.01 tick;
  - the limit is at or under the trigger;
  - it sells shares you hold;
  - the trigger is under the price now (a fresh price, else the last close).
    A trigger at or over it would fire at once.
- When the trigger is at or over the price, the block says why:
  - A bonus, right or split shows in the data (an XB or XR tag, or a big
    LDCP change with no tag), and your plan is not scaled for it yet. You
    choose: `ticket.py stop --scale F` (psx-alerts gives F) or `--scale 1`.
  - A cash payout (XD) does not change the stop. It stays as it is.
  - The price is at or under your plan's stop: the stop rule is met. To sell:
    `ticket.py flatten --symbol X` (`--limit P` in the pre-open).
  - Your plan's stop is under the price, but the ticket is old: make a new
    one with `ticket.py protect`.
- A stop-limit buy is blocked. Day style does not take stop-limit orders.
- **No second sell of the same shares.** Today's sells with no fill yet count
  against the shares you hold. A sell of more than is left is a blank sale,
  so it is blocked. Cancel the first sell in your broker app, then record it:
  `ticket.py result --fingerprint FP --status cancelled`. A "cancelled" or
  "expired" record frees it, the way "skipped" does. Day style keeps the v1
  warning ("duplicate").
- **A sell filled in part.** The other shares may still sell at the broker
  today. So they still count against the shares you hold. The block line
  says how many filled, like "(stop-limit, 09:52; 100 of 253 filled)".

Example: a stop-limit sell of 143 DEMO was placed at 9:36 AM on Friday
2026-10-30. A flatten sell of the same 143 shares is then blocked:

```
BLOCK #1 sell DEMO 143 shares, exit
        - short: 143 DEMO shares are already in a sell placed today (stop-limit, 09:36). Cancel it
          in your broker app, then record it: ticket.py result --fingerprint 4f1f7cf1107d6b31
          --status cancelled
```

Once that sell is recorded cancelled, the flatten sell passes.

## Rules

- A PASS only means the order may be shown to the user. It is not a yes.
- Every number comes from the config, the order, the portfolio, the prices,
  the PSX files or the broker log.
- Free PSX data is about 5 minutes late. Your broker's price is the one that
  fills.
- A stop can fill worse than its price. At the lower limit a sell may not
  fill at all: there may be no buyers.
- The tool cannot see a market halt. A halt cancels every open order at PSX.
- In swing a gap at the open can sell far under the stop. The gap loss shows
  what one bad open can cost. Several bad days can cost more.
- The tool never moves a stop. Only `ticket.py stop` does, and only up (or
  scaled for a bonus or a split).

## What it never does

- It never places an order.
- It never edits an order to make it pass.
- It never loosens a limit.
- It never blocks a sell that only gets the user out. Two exceptions:
  - A future, an index, a GEM board share or debt is blocked, even for a
    sell. It is not on the REG board.
  - In swing, a second sell of the same shares is blocked. A sell placed
    today already uses them. That is a blank sale.
- It never treats a PASS as the user's yes.

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
