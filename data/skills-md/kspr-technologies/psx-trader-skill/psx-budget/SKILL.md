---
name: psx-budget
description: >-
  Budget Manager for the Pakistan Stock Exchange (PSX). Sizes a day trade or a
  swing trade to your budget and your max loss per trade in rupees, with the
  broker's costs included (commission, sales tax and fees). Reads the plan from
  psx-exit (entry, stop, target), finds the whole shares that fit four limits
  (max loss per trade, position cap, max order, cash after your buffer; a swing
  trade adds a fifth, the gap limit), says which limit decided it, and writes
  ONE order to psx/orders.json: a limit order at the plan's entry, with the stop
  and the target in it. A stop too far away is a plain refusal, not a smaller
  order. Nothing is placed. Use when the user says "how many shares", "size this
  trade", "how much should I buy", "I have Rs 500,000", "I only want to risk Rs
  5,000 a trade", "set my rules", "keep 10% in cash", "size my swing trade", or
  after /psx-exit writes a plan.
argument-hint: "[budget in rupees]"
---

# psx-budget

The Budget Manager turns a plan ("buy DEMO at 100.65, stop 99.55") into an
exact order ("buy 3,428 shares"). It works inside rules the user sets once.

- The stop decides the size. The further away the stop, the fewer shares.
- Costs count. Each buy and each sell costs money, and the max loss includes it.
- It writes a proposal only. psx-risk checks it. psx-broker asks the user yes or no.
- Day trading loses most people money. Swing trading loses money for many people too.
  Sizing to a max loss keeps each loss small. It does not make a trade win.
- A swing trade (`"style": "swing"`) is held for days. See "Swing style" below.

`${CLAUDE_SKILL_DIR}` below is this skill's folder (where this SKILL.md lives).

```bash
python3 "${CLAUDE_SKILL_DIR}/size.py"                         # psx/plan.json + psx/config.json
python3 "${CLAUDE_SKILL_DIR}/size.py" --write                 # write psx/orders.json
python3 "${CLAUDE_SKILL_DIR}/size.py" --limit 100.60 --json   # a limit order at 100.60
python3 "${CLAUDE_SKILL_DIR}/size.py" --market --write        # a market order (see Step 2)
python3 "${CLAUDE_SKILL_DIR}/size.py" --weights OGDC=60,HBL=40 --config split.json   # weights mode, below
```

- `--now "2026-10-29 10:15"` pins the clock. A time with no offset is Karachi time.
- A plan for another day is refused: make a new one with psx-exit.
- `--data DIR` is the PSX data folder (default `psx/data`). This tool only reads files.
  It never fetches, so `--offline` changes nothing here.
- `--config FILE` reads other rules. If that file is not there, it stops and says so.

## What it reads and writes

| file | what |
| --- | --- |
| `psx/config.json` | the rules (start from `config.example.json` in this folder) |
| `psx/plan.json` | the trade: entry, stop, target, setup, flat-by time, today's price limits (psx-exit writes it) |
| `psx/prices.json` | optional: a fresh price for a market order (psx-alerts writes it) |
| `psx/data/` | optional: today's tape, saved company pages, the saved screener page |
| `psx/portfolio.json` | optional: your account, cash plus holdings (psx-broker keeps it). Swing style needs it once a buy is placed |
| `psx/state/broker.json` | swing style: today's buys with no fill yet come off the cash (psx-broker keeps it; `--state FILE`) |
| `psx/orders.json` | the one proposed order it writes with `--write` |

## Step 1: set the rules once

If `psx/config.json` does not exist, copy `config.example.json` into
`psx/config.json`. Ask the user for each value in plain words:

- **budget**: how much money this is for, in rupees. Only money they can afford to lose.
- **cash_buffer_pct**: how much always stays in cash (default 10).
- **max_loss_per_trade_pkr**: the most one trade may lose if the stop fills at the stop,
  costs included (default Rs 5,000).
- **max_position_pct**, **max_order_pkr**, **min_order_pkr**: the biggest position (75% of the
  account), the biggest order (Rs 400,000) and the smallest order (Rs 5,000).
- **costs**: the broker's rates. The defaults: commission 0.15% of the value or Rs 0.03 a
  share, whichever is more, on each side. 15% sales tax on the commission. Other charges
  0.0066% of the value. Some brokers charge a same-day trade on one side only: then set
  `"day_trade_one_side": true`.
- The day limits psx-risk enforces: **max_daily_loss_pkr** (Rs 15,000), **max_trades_per_day** (3),
  **min_reward_risk** (1.0), **require_stop** (true), **no_entries_before** / **no_entries_after**
  ("09:45" / "15:00") and **flat_by** ("15:20"). These are Karachi times for Monday to Thursday.
  On a Friday or in Ramadan the tools move them to that day's hours (15:20 is 16:20 on a Friday).
- **blocked**: tickers they never want to trade, as a list: `["ABC", "XYZ"]`.
- **style**: `"day"` (the default) or `"swing"`. It is set here only, never by a flag.
  One style per folder. Switch only when no order is waiting and you hold no share without a
  swing plan. A day trade has no plan. A share you bought before the switch has none either.
  Such a share is watched only by its own rules in `psx/alerts.json`, and only with today's
  prices, never a closing file (README "If you already hold shares").
- **swing**: the swing rules. Write only the keys you change; the rest keep their defaults.
  For this tool: **max_gap_loss_pkr** (null means 3 x `max_loss_per_trade_pkr`; 0 is a
  limit of Rs 0, see "Swing style" below).
- Keep **paper** true until they have watched it work on paper. Try swing trades on paper first.
- Never turn paper on in a folder that already holds real shares or real cash. A paper fill
  there can go into the real `psx/portfolio.json`, next to the real shares. Use a new paper
  folder: copy `psx/config.json` and `psx/data/` into its `psx/`, set `"paper": true` there,
  and do not copy `psx/portfolio.json`. Then the paper cash starts from `"budget"` (README
  "Paper and real shares"). To lock a folder of real shares, put `"real_holdings": true` at
  the top of its `psx/portfolio.json`: then psx-broker refuses a paper fill into it.

## Step 2: size the trade

```bash
python3 "${CLAUDE_SKILL_DIR}/size.py" --write
```

Whole shares only (a lot is 1 share on the regular board). The size is the smallest of four limits:

| limit | shares |
| --- | --- |
| max loss | the most shares whose loss at the stop fits `max_loss_per_trade_pkr`: shares x (entry minus stop), plus the costs of the buy and the sell |
| position cap | (account x `max_position_pct`, minus what you already hold of this stock) / entry |
| max order | `max_order_pkr` / entry |
| cash | (cash minus the cash buffer) / entry, after the buy's costs. The buffer is account x `cash_buffer_pct` |

- The account is the one psx-risk checks against. With `psx/portfolio.json`, it is the
  cash plus your holdings. A holding counts at a fresh price, else at its cost.
- With no portfolio, the account and the cash are the budget.
- Costs are not a straight line (a minimum per share, rounding to the paisa). So the
  max loss limit is a search, not one division.
- The order is a limit order at the plan's entry by default. Free PSX prices are about
  5 minutes late, so a market order can fill far from the plan.
- `--limit PRICE` sets another limit price. It sizes at that price.
- `--market` gives a market order. It needs a fresh price: fresh means at most 15
  minutes old by its own time. It looks in `psx/prices.json`, then in the data folder:
  today's tape, then a saved company page. The first fresh one wins. psx-risk looks the
  same way.
- It sizes at the plan's entry, or at the fresh price if that is higher. With no fresh
  price there is no market order: the plan's entry can be hours old. Use a limit order
  then (the default).
- A price that ran up since the plan means a bigger loss at the same stop. A lower price
  never shrinks the risk. PSX takes no market orders in the pre-open.

It refuses, and writes no order, when:

- the size is zero shares, or the order is under the minimum order;
- reward:risk is under `min_reward_risk`;
- the stop is not below the entry, or the target is not above it (the move already happened);
- the target is above today's upper price limit, or the entry is outside the limits
  (from the plan's `"limits"`; if the plan has none, from a quote of today);
- the plan is for another day, the ticker is blocked, or the plan is a short.

Say the reason to the user in one line. Swing style changes a few of these: see "Swing style" below.

## Step 3: show the user

- Show the four limits, which one decided the size, the shares and the rupees.
- Show the max loss at the stop in two parts: the price risk and the costs. Say "costs included".
- When the costs are over 25% of the price risk, the tool says so. Pass it on: you pay
  the costs win or lose.
- Say plainly that a stop is a plan, not a promise. PSX has no stop orders. The user (or the
  broker's app) sells when the price gets there. In a fast market, or at the lower price
  limit, the sell can fill below the stop.
- Swing style: also show the gap loss, in rupees, and the gap limit. Say that more days
  down can lose more. The evening before, say it is a preview: size it again in the
  pre-open of the buy day, with `--write`.
- Then hand over to `/psx-risk`.

## Example: DEMO on Thursday 2026-10-29

The sample market in the tests is made up. DEMO ("Demo Industries Limited") is a made-up company.

- Opening-range breakout: entry 100.65 at 10:15 AM, stop 99.55 (the opening-range
  midpoint), target 101.75 (1R). Risk 1.10 a share.
- Today's price limits: 88.56 to 108.24 (10% from the last close, 98.40).
- The example config: Rs 500,000 budget, 10% cash buffer, Rs 5,000 max loss, costs included.

`size.py --now "2026-10-29 10:15"` prints:

```
DEMO buy, opening-range breakout, entry 100.65 at 10:15 AM
Stop 99.55: opening-range midpoint. Target 101.75: 1R (one times the risk).
Sized at 100.65 (the plan's entry). Risk 1.10 a share (entry 100.65 minus stop 99.55). Reward:risk 1.00.
Today's price limits: 88.56 to 108.24 (from the company page).

Limits (whole shares; the smallest one wins):
  max loss      Rs 5,000 at the stop, costs included                            3,428 shares  <- binds
  position cap  75% of Rs 500,000 = Rs 375,000 / 100.65                         3,725 shares
  max order     Rs 400,000 / 100.65                                             3,974 shares
  cash          Rs 450,000 (budget minus the buffer) / 100.65, with buy costs   4,462 shares
  Costs count: without them the max loss limit would be 4,545 shares (Rs 5,000 / 1.10).

Size: 3,428 shares of DEMO = Rs 345,028.20 at 100.65.
Max loss at the stop: Rs 4,999.94, costs included.
  price risk  3,428 x 1.10 = Rs 3,770.80
  costs       buy Rs 617.95 + sell at the stop Rs 611.19 = Rs 1,229.14
  one more share (3,429) would lose Rs 5,001.40: over your Rs 5,000
Costs are about 33% of the price risk (over 25%). You pay them win or lose.
A stop is a plan, not a promise. PSX has no stop orders: you, or your broker's app, sell
when the price gets there. In a fast market, or at the lower price limit, the sell can
fill below 99.55.

Proposed order (nothing has been placed):
  buy 3,428 DEMO, limit 100.65, day, REG board. Stop 99.55 and target 101.75 go with it.
A limit order never pays more than 100.65. Free PSX prices are about 5 minutes late.
Flat by 15:20 Karachi time: anything still open then gets closed (psx-alerts rings, psx-broker flatten).

Next: psx-risk checks it, then psx-broker shows you the ticket and asks yes or no.
Education and tooling, not financial advice.
```

- Without costs it would be 4,545 shares (Rs 5,000 / 1.10). Costs cut it to 3,428.
- The cash row counts the buy's costs too: Rs 450,000 buys 4,462 shares, not 4,470.
- The costs (Rs 1,229.14) are 33% of the price risk (Rs 3,770.80).

With `--write` it writes this order to `psx/orders.json`:

```json
{"symbol": "DEMO", "side": "buy", "qty": 3428, "type": "limit", "limit_price": 100.65,
 "time_in_force": "day", "board": "REG", "stop_loss": 99.55, "take_profit": 101.75,
 "why": "opening-range breakout on DEMO: 3428 shares, bound by your Rs 5,000 max loss per trade (3428 x 1.10 = Rs 3,770.80 at the stop + Rs 1,229.14 costs = Rs 4,999.94, costs included)",
 "plan": {"entry": 100.65, "stop": 99.55, "target": 101.75, "risk_per_share": 1.1,
          "max_loss": 4999.94, "costs": 1229.14, "setup": "orb", "entry_time": "10:15 AM",
          "flat_by": "15:20"}}
```

- `why` and `plan` are notes for psx-risk and psx-broker. The user places only the order part.
- `--market` gives `"type": "market"` and no `limit_price`.

At 10:52 the company page shows 101.30 (as of 10:52, so it is fresh). A limit at 101.30
(`--limit 101.30`), or a market order (`--market` reads it from `psx/prices.json` or the
tape), sizes at 101.30. Risk is 1.75 a share, so the max loss limit is 2,369 shares. But
the target is only 0.45 away:

```
No order: reward:risk 0.26 (target 101.75, entry 101.30, stop 99.55) is under your minimum 1, so psx-risk would block it. Skip it, or make a new plan with psx-exit.
```

The move it was waiting for has mostly happened.

## Swing style

Set `"style": "swing"` in `psx/config.json` to buy shares and hold them for days.
psx-exit then makes a swing plan from the closing files. This tool sizes it.
Try swing trades on paper first, in a new paper folder (see Step 1). Never turn paper on
in a folder that holds real shares or real cash.

What changes (day style stays as it was):

- **Styles do not mix.** A day plan in a swing folder, or a swing plan in a day folder, is
  refused with one plain line. Make a new plan with psx-exit. If you already hold the plan's
  stock, the line says so. Swing blocks a second buy of it, so do not plan it again.
- **Costs on both sides.** The sell comes on a later day, so it pays commission too,
  whatever `"day_trade_one_side"` says.
- **A fifth limit: the gap limit.** A share held overnight can open the next day at its
  lower price limit (10% under the entry). The loss then, costs included, is the gap loss.
  It must fit `swing.max_gap_loss_pkr`. Null means 3 x `max_loss_per_trade_pkr`
  (Rs 15,000 with Rs 5,000). When it decides the size, the report says "bound by your
  gap limit".
  `swing.max_gap_loss_pkr` set to 0 is a limit of Rs 0, so every swing buy is refused (the
  gap loss must have a cap). psx-risk reads 0 the same way. With null and no
  `max_loss_per_trade_pkr`, there is no gap limit, in psx-risk too.
- **The cash comes from your ledger.** It is the cash in `psx/portfolio.json`, less today's
  buys that have a yes (approved or placed) but no fill yet (`psx/state/broker.json`).
  psx-risk counts the same number. Those waiting buys count as held until they fill or end.
  A buy filled in part counts only the rest: the shares not filled yet may still fill today.
- **No ledger yet.** No `psx/portfolio.json` and no buy placed or filled: it sizes from the
  budget and says so. No `psx/portfolio.json` but a buy placed or filled: it refuses.
  Record your fills with psx-broker first (`ticket.py fill`), so open positions are not
  counted as cash.
- **The evening before is a preview.** A plan for the next session is sized, and it says
  "Preview for Thu 2026-10-29: size it again on that day, before you buy." `--write` is
  refused then: `psx/orders.json` must be made on the buy day (psx-risk checks its date).
- **The buy day's price limits.** A target over the upper limit is a note, not a refusal:
  it can fill on a later day. An entry outside the limits is still refused. A stop under the
  lower limit gets a note: it cannot be hit that day. A stop at the lower limit gets a note
  too: it can be hit that day, but at the limit there may be no buyers.
- **No flat-by time.** The order's plan has `"flat_by": null`, the exit-by day and time,
  the trend rule and the gap loss. psx-broker copies them into the ledger for psx-alerts.
- A share you already hold, or a buy of it still waiting today, gets a note: in swing,
  psx-risk blocks a second buy of it.

The example: the swing plan for DEMO from psx-exit. Buy day Thu 2026-10-29. Entry 99.38
(the last close 98.40 plus 1%). Stop 96.25 (2 x the daily ATR under the entry). Target
105.64 (2R). The example config with `"style": "swing"`, and no `psx/portfolio.json` yet.

`size.py --now "2026-10-29 09:20"` (the pre-open of the buy day) prints:

```
DEMO swing buy on Thu 2026-10-29, 20-day closing-high breakout, entry 99.38 (last close + 1%)
Stop 96.25: 2 x ATR(14) under the entry. Target 105.64: 2R (two times the risk).
No psx/portfolio.json yet: sized as if nothing is open. Record each fill with psx-broker.
Sized at 99.38 (the plan's entry). Risk 3.13 a share (entry 99.38 minus stop 96.25). Reward:risk 2.00.
Price limits for Thu 2026-10-29: 88.56 to 108.24 (computed from the last close).

Limits (whole shares; the smallest one wins):
  max loss      Rs 5,000 at the stop, costs included                             1,436 shares  <- binds
  gap limit     Rs 15,000 if it opens at the lower limit 89.44, costs included   1,459 shares
  position cap  75% of Rs 500,000 = Rs 375,000 / 99.38                           3,773 shares
  max order     Rs 400,000 / 99.38                                               4,024 shares
  cash          Rs 450,000 (budget minus the buffer) / 99.38, with buy costs     4,519 shares
  Costs count: without them the max loss limit would be 1,597 shares (Rs 5,000 / 3.13).

Size: 1,436 shares of DEMO = Rs 142,709.68 at 99.38.
Max loss at the stop: Rs 4,997.81, costs included.
  price risk  1,436 x 3.13 = Rs 4,494.68
  costs       buy Rs 255.59 + sell at the stop Rs 247.54 = Rs 503.13
  one more share (1,437) would lose Rs 5,001.30: over your Rs 5,000
Loss if it opens at the lower limit the next day: about Rs 14,759.46, costs included (your gap limit Rs 15,000). More days down can lose more.
A stop is a plan, not a promise. PSX has no stop orders: you, or your broker's app, sell
when the price gets there. In a fast market, or at the lower price limit, the sell can
fill below 96.25.

Proposed order (nothing has been placed):
  buy 1,436 DEMO, limit 99.38, day, REG board. Stop 96.25 and target 105.64 go with it.
A limit order never pays more than 99.38. Free PSX prices are about 5 minutes late.
PSX orders last one day: a limit buy that does not fill today ends at the close. Do not chase it.
Hold up to Fri 2026-11-27 (20 sessions). Out earlier at the stop, the target or a trend break.

Next: psx-risk checks it, then psx-broker shows you the ticket and asks yes or no.
Education and tooling, not financial advice.
```

- The max loss binds: 1,436 shares lose Rs 4,997.81 at the stop, costs included.
- The gap loss is about 3 times that: Rs 14,759.46 if the next day opens at 89.44. It is
  under the Rs 15,000 gap limit, so the order stays at 1,436 shares.
- More days down can lose more. A day at the lower limit may have no buyers at all.

With `"max_loss_per_trade_pkr": 500` it is 143 shares = Rs 14,211.34, max loss Rs 497.69, and:

```
Loss if it opens at the lower limit the next day: about Rs 1,469.78, costs included (your gap limit Rs 1,500). More days down can lose more.
```

A closer stop means more shares, so the gap limit can bind. With a stop of 98.38 (risk 1.00
a share) the max loss would allow 3,692 shares, but the gap limit allows 1,459:

```
  bound by your gap limit: one more share (1,460) would lose Rs 15,006.13 on such an open: over your Rs 15,000
```

The evening before (`--now "2026-10-28 17:00"`) it prints the same sizing, and ends with:

```
Preview for Thu 2026-10-29: size it again on that day, before you buy.
```

With `--write` in the pre-open it writes this order to `psx/orders.json`:

```json
{"symbol": "DEMO", "side": "buy", "qty": 1436, "type": "limit", "limit_price": 99.38,
 "time_in_force": "day", "board": "REG", "stop_loss": 96.25, "take_profit": 105.64,
 "why": "20-day closing-high breakout on DEMO: 1436 shares, bound by your Rs 5,000 max loss per trade (1436 x 3.13 = Rs 4,494.68 at the stop + Rs 503.13 costs = Rs 4,997.81, costs included)",
 "plan": {"style": "swing", "entry": 99.38, "stop": 96.25, "target": 105.64, "risk_per_share": 3.13,
          "max_loss": 4997.81, "costs": 503.13, "setup": "breakout_20d", "entry_time": null,
          "flat_by": null, "exit_by": "2026-11-27", "exit_by_time": "16:20", "trend_sessions": 10,
          "gap_loss": 14759.46}}
```

- PSX orders last one day. A limit buy that does not fill ends at the close. Do not chase it
  the next day. Record it expired with psx-broker, by its fingerprint, on the buy day or later:
  `ticket.py result --fingerprint FP --status expired`. FP is the fingerprint psx-broker
  prints after your yes. psx-risk prints this whole line while the buy waits.
  Do not use an order number here. `psx/orders.json` holds only the newest order you sized,
  so its number 1 can be another order.
- Hold up to the exit-by day. psx-alerts watches the stop, the target, the trend rule and the
  time stop once the fill is recorded.

## Weights mode (kept from v1)

`--weights OGDC=30,HBL=25` or `--targets FILE` splits a budget across a list by weight.

- The cash buffer comes off the top. The weights are scaled so they add up to 100.
- A stock over `max_position_pct` is pinned at the cap. Its extra is shared out.
- Each slice buys whole shares at its price, the buy's costs included.
- A slice under the minimum order is dropped, and its weight shared out.
- Money that cannot be invested is shown as "left idle", never hidden.

Prices come from `--prices` (or `psx/prices.json`), then the saved screener page
(`psx/data/screener.html`), then saved company pages. With no price, it says what to save.

`targets.example.json` here is a made-up split of five large PSX shares. It is not advice.
With `"max_position_pct": 25` and the sample screener's prices it buys 446 OGDC (capped at
Rs 125,000), 424 HBL, 199 LUCK, 135 FFC and 378 SYS.

- Each order is a limit order at the price it sized at (or a market order with `--market`).
- These are plain buys with no stop. psx-risk blocks them while `require_stop` is true and
  counts each one against `max_trades_per_day`.
- For a long-term split, use a separate config. Copy `config.example.json` to `split.json`.
  Set `max_position_pct` and `"require_stop": false` in it. Then pass `--config split.json`
  to this tool and to psx-risk.
- ETFs trade in lots of 500 units. This tool does not size them.

## Rules

- Proposals only. This skill never places an order and never calls a broker.
- Never size money the user has not said is for this. Ask for the budget and the max loss.
  The budget has no default. Once `psx/portfolio.json` exists, its account is that money.
- Every number comes from the config, the plan or the prices. Nothing is guessed.
- No projections: never say what a trade will make. A target is a plan, not a forecast.
- Free PSX prices are about 5 minutes late. The broker's screen shows the price that fills.
- Costs are estimates from the `costs` block. The broker's contract note has the real number.
  Tax on gains is not in these costs.
- Styles do not mix: never size a swing plan in a day folder, or a day plan in a swing folder.
  Never change `"style"` for the user.

## What it never does

It never places, approves or schedules an order. It never raises a limit on its own. It
never shrinks a stop to fit more shares. It never sizes options, margin or short positions.
It never fetches from the PSX site.

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
