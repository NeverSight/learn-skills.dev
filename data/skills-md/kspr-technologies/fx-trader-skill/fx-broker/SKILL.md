---
name: fx-broker
description: >-
  MetaTrader order tickets for forex, gold, silver, oil and gas. Paper trading by default. Never
  places an order: it shows each order as a plain ticket (Buy or Sell, lots, stop loss, take
  profit, max loss with costs, how old the price is), waits for your explicit yes, then gives the
  one line to type into your own MetaTrader. Keeps a paper ledger, builds close orders and moves
  stops. Use when the user says "place the order", "buy it", "sell it", "execute", "send it to
  MetaTrader", "close my trade", "flatten", "get me out", "move my stop", "set up paper trading",
  or after /fx-risk passes.
argument-hint: "[order number]"
---

# fx-broker

This is the last step before an order, so it is the strictest skill.
It has no broker link and no network code. Nothing here places an order.

An order reaches MetaTrader only after three gates, every time, for every order:

1. **A fresh fx-risk PASS for this exact order.** It is matched by the order's
   fingerprint, and it counts for 5 minutes.
2. **The user's explicit yes in the chat**, for this one order.
3. **The user's own hands in MetaTrader.** The user types the order in, with their own login.

One PASS from the rules. One yes from the user. Then the user's own hands.
No yes, no order. In paper mode (the default) there is no MetaTrader step:
the yes plus `result --status filled` fills the paper account.

`${CLAUDE_SKILL_DIR}` below is this skill's folder (where this SKILL.md lives).

```bash
python3 "${CLAUDE_SKILL_DIR}/ticket.py" show                     # every ticket, READY or not
python3 "${CLAUDE_SKILL_DIR}/ticket.py" show --index 1 --broker-price 2429.15
python3 "${CLAUDE_SKILL_DIR}/ticket.py" approve --index 1 --reply "yes" --broker-price 2429.15
python3 "${CLAUDE_SKILL_DIR}/ticket.py" decline --index 1 --reply "no"
python3 "${CLAUDE_SKILL_DIR}/ticket.py" result --index 1 --status filled
python3 "${CLAUDE_SKILL_DIR}/ticket.py" close --position EURUSD-1
python3 "${CLAUDE_SKILL_DIR}/ticket.py" close --position XAUUSD-1 --already --fill 2512.41
python3 "${CLAUDE_SKILL_DIR}/ticket.py" flatten                  # close orders for the day trades
python3 "${CLAUDE_SKILL_DIR}/ticket.py" stop --position XAUUSD-1 --to 2421.59
python3 "${CLAUDE_SKILL_DIR}/ticket.py" log                      # the last 30 days
```

Every command also takes `--config FILE`, `--data DIR`, `--offline`, `--json`, `--quiet`
and `--now "2026-07-17 09:09"` (Karachi time, PKT; `...Z` for UTC).
`--now` pins the clock for a replay. `--offline` changes nothing here: there is no network.

Exit codes: 0 done (a READY ticket, a yes, a result, close orders written, a stop moved,
the log). 1 a plain no (not READY, not a yes, already answered, nothing to close, stop
refused). 2 an error (a missing or broken file, a bad flag, a broker price too far away).

## What it reads and writes

| file | what |
| --- | --- |
| `fx/orders.json` | the orders (fx-budget writes them; `close` and `flatten` replace them) |
| `fx/state/risk.json` | fx-risk's verdicts; only a PASS for this exact order, 5 minutes old or less, is READY |
| `fx/state/broker.json` | the ledger: every yes, no, placed, filled, closed, rebase and stop move |
| `fx/portfolio.json` | the account and the open trades (paper or live) |
| `fx/prices.json` | the broker price you typed (`--broker-price`), good for 60 minutes |
| `fx/plan.json`, `fx/config.json` | the plan's words; `paper`, `account`, `day.flat_by` |
| `fx/data/` | read only, never downloaded: Yahoo prices and their age, rolls, the calendar |

- The ledger only grows. A record is never changed or removed.
- A damaged ledger is an error, never "no trades": fix it by hand or restore a backup.
- It never asks for, stores or repeats MetaTrader logins, passwords or PINs.

## Your broker and MetaTrader

- **Server time.** MetaTrader shows the broker's server clock. Set `account.server_time`
  (`"ny+7"` for most brokers: GMT+2 in winter, GMT+3 in summer; or like `"utc+0"`).
  The ticket shows a pending order's expiry in that clock.
- **Platform.** `account.platform` is `"mt5"` or `"mt4"`. The MetaTrader line uses that
  platform's words (Toolbox or Terminal, Expiration or Expiry).
- **The Close button.** To close a trade, use the position's Close button in MetaTrader.
  On a hedging account (`account.hedging: true`) a new opposite order opens a second
  trade. It does not close the first one.
- **Broker symbols.** Your broker may call gold `XAUUSD`, `GOLD` or `XAUUSD.m`. Put that
  name in the instrument's `broker_symbol`. The ticket and the MetaTrader line use it.
- **Yahoo prices are not your broker's prices.** Spot FX on Yahoo is close to your
  broker's price. Gold, silver, oil and gas on Yahoo are futures prices, a few dollars
  away from your broker's CFD price.
- **`--broker-price P`.** Type your broker's BID now (from MetaTrader) for the order's
  symbol. The ticket then works out exact SL and TP levels on your broker's scale. It
  keeps the same distances as the plan. The price counts for 60 minutes, on the same FX
  day, and not after a futures roll.
- A gold, silver, oil or gas order needs that broker price before a yes is recorded.
  Spot FX does not.

## How a ticket works

- **READY** means all of these hold. The first that fails is shown as the reason:
  - fx-risk said PASS for this exact order (same fingerprint);
  - that check is 5 minutes old or less (and not from a later time);
  - the order has no yes or no yet today;
  - no futures roll is missing from the order (else "Gold rolled. Run fx-budget again.");
  - an open order: the broker's market is open now;
  - a close order: the position is still open.
- **The fingerprint** is a short hash of the order's main fields (symbol, side, intent,
  lots, type, entry, stop loss, take profit, expiry, style). Change one, and it is a new
  order: it needs a new fx-risk check and a new yes.
- **Max loss** is fx-risk's number: the loss if the stop fills at its price, with the
  spread, commission, swap and any swap-free fee included.
- **The yes rule.** A reply counts only when all of this is true:
  - it starts with `yes` or `y`, and has no `?`;
  - it is for one order (no "all", "both", "every");
  - it has no doubt or condition ("but", "wait", "if", "maybe", "as soon as");
  - it does not say the other side, another order type, or a change ("double", "x2", "Monday");
  - it names no other symbol, and each number in it is this order's lots, price, SL, TP or max loss;
  - for a close order: only `yes` or `yes, close` (a buy or sell word is refused).
- A reply that is not a yes is not recorded. The ticket is simply asked again.

## Steps: the entry

1. Run `ticket.py show`. Show the user the ticket as it is printed.
2. For gold, silver, oil or gas: ask for the broker's BID in MetaTrader, then run
   `show --index N --broker-price P` to get exact levels.
3. Ask: "Place this order? Reply yes or no."
4. Pass the user's reply word for word:
   `ticket.py approve --index N --reply "<the exact words>"` (add `--broker-price P` if needed).
   Never turn a reply into a yes. Never type the yes yourself.
5. Only after a recorded yes, show the `In MetaTrader:` line. In paper mode, tell the
   user not to place it.
6. Record what happened: `ticket.py result --index N --status filled` (paper fills at the
   order price; give `--fill P` for another price). Live: `--fill P` is the price
   MetaTrader shows. Other results: `placed`, `skipped`, `failed`, `cancelled`, `expired`.
7. If the user says no: `ticket.py decline --index N --reply "<their words>"`.

## Steps: while it is open, and the close

- **Watch it.** Next: `python3 fx-alerts/alerts.py add --from-plan`.
- **Move the stop.** `ticket.py stop --position ID --to PRICE`. It moves only toward the
  profit side. A wider stop needs `--wider`, and the ticket says how much the max loss grows.
  It prints the MetaTrader step to change the stop there too.
- **Close it.** `ticket.py close --position ID` writes one close order to `fx/orders.json`.
  Then run fx-risk, `ticket.py show`, and the user's yes, as for an entry. The yes gives
  the Close button step. Then `result --index 1 --status filled`.
- **Day trades.** `ticket.py flatten` writes close orders for every open day trade
  (`--all`: every position). Be flat by your `day.flat_by` time.
- **MetaTrader closed it already** (its SL or TP fired):
  `ticket.py close --position ID --already --fill P`. This records the close at once,
  with no order and no yes.
- **A futures roll.** When Yahoo moves to the next gold or oil contract, the plan levels
  of an open trade move by the same ratio. The broker's levels do not change: keep the SL
  and TP you set in MetaTrader.
- **The ledger.** `ticket.py log` (the last 30 days) or `log --today`.

## Example

The made-up sample market: a swing BUY of gold on Fri 17 Jul, at 9:09 AM PKT, with the
user's broker bid 2,429.15
(`show --index 1 --broker-price 2429.15 --now "2026-07-17 09:09"`):

```
READY: fx-risk PASS for this exact order (checked 9:08 AM PKT). Waiting for your yes.

Order 1 of 1 (paper)
  BUY XAUUSD, market, 0.02 lots
  Stop loss (SL)    2,395.75   33.49 below the price (3,349 points)
  Take profit (TP)  2,485.75   56.51 above the price (5,651 points)
  Price now         2,433.40   Yahoo price (gold futures), not your broker's price, 4 min old
  Your price        2,429.15   your broker's price (you typed it), live
  Broker levels     entry 2,429.24 (Yahoo plan: entry 2,433.49, SL 2,400.00, TP 2,490.00)
  Expiry            good till cancelled (swing: up to 20 FX days, to Fri 14 Aug 2:00 AM PKT)
  Max loss at the stop: $97.81, costs included ($66.98 price and spread,
  $0.12 commission, $30.71 swap for 28 nights).
  Margin used: about $48.67.

Yahoo's price was 4 min old, so these levels may be off by about $1.68. Check them
against your MetaTrader chart.
Note: a buy opens at the ask and its stop fires on the bid.
Note: this is a swing trade. Swap is booked each night at 5:00 PM New York
(2:00 AM PKT).
Note: The market closes for the weekend. On Monday the price can open past
your stop.
Note: A stop is not a promise. If the price jumps, it fills at the next price.

Type yes to approve this exact order. Anything else is a no.
```

The user replies "yes" (`approve --index 1 --reply "yes" --broker-price 2429.15`):

```
Recorded your yes for order 1: BUY XAUUSD, market, 0.02 lots.
  Broker levels: entry 2,429.24, SL 2,395.75, TP 2,485.75 (from your broker's price (you typed it), 2,429.15).
In MetaTrader: New order > Symbol XAUUSD > Market Execution > Volume 0.02 > Stop Loss 2395.75 > Take Profit 2485.75 > Buy by Market.
Paper trade: do not place it in MetaTrader. Record the paper fill:
  python3 fx-broker/ticket.py result --index 1 --status filled
```

## What it never does

- It never places, changes or cancels an order. It has no broker link and no network.
- It never counts two orders on one yes, and never turns a reply into a yes.
- It never runs from a scheduled or background task: nobody is there to say yes.
- It never asks for, stores or repeats MetaTrader logins, passwords or PINs.
- It never switches `"paper"` off. Going live is the user's own change in the config.
- It never writes a rebased order to `fx/orders.json`. A rolled order needs fx-budget again.
- It never promises a fill price.
- It gives no advice. A READY ticket is a rules check, not a recommendation.

## Safety

- Education and tooling, not financial advice. A PASS is a rules check, not a recommendation.
- Paper trading by default (`"paper": true`). Going live is the user's own decision, in their own config.
- Nothing in this pack places an order. fx-broker shows the order and waits. It prints the line to
  type into MetaTrader only after fx-risk passed that exact order in the last 5 minutes and the user
  typed an explicit yes for that one order in the chat. The user then places it in their own
  MetaTrader. If the user ever adds a broker tool that can place orders, set it to "Needs approval"
  (Customize > Connectors > tool permissions), never "Always allow".
- Both sides. A buy opens at the ask, a sell opens at the bid. A sell's stop is above the price.
  Sells are on by default; `"allow_short": false` turns them off.
- Leverage makes losses bigger, as fast as gains. Every order carries a stop loss (SL) and a take
  profit (TP).
- A stop is not a promise. Over a weekend, at big news or at a futures roll the price can jump past
  the stop, and the fill is worse than the stop.
- Most retail CFD accounts lose money: 74% to 89% of them in EU regulators' studies (ESMA, 2018).
- MetaTrader logins, passwords and PINs never go in the chat.
