---
name: fx-budget
description: >-
  Budget Manager for currency pairs, gold, silver, oil, gas and copper at a
  MetaTrader 4/5 broker. Sizes one trade in lots to your max loss per trade in
  US dollars (1% of your balance by default), with the spread, the commission
  and the swap counted. Reads the plan from fx-exit (entry, stop, target), works
  for buys and sells, swing and day trades, checks the margin, says which limit
  decided the size, and writes ONE order to fx/orders.json. If even the smallest
  lot loses too much, it says no and never moves the stop. Nothing is placed.
  Use when the user says "how many lots", "size this trade", "what lot size",
  "how much should I risk", "I have $1,000", "I only want to risk $20 a trade",
  "set my rules", "copy my broker's specs", or after /fx-exit writes a plan.
argument-hint: "[max loss in dollars]"
---

# fx-budget

The Budget Manager turns a plan ("buy gold at 2,433.49, stop 2,400.00") into an
exact order ("buy 0.02 lots"). It works inside rules the user sets once.

- The stop decides the size. The further away the stop, the fewer lots.
- Costs count. The spread, the commission and the swap are in the max loss.
- It writes a proposal only. fx-risk checks it. fx-broker asks the user yes or no.
- Sizing keeps each loss small. It does not make a trade win.

`${CLAUDE_SKILL_DIR}` below is this skill's folder (where this SKILL.md lives).

```bash
python3 "${CLAUDE_SKILL_DIR}/size.py"                          # show the size, write nothing
python3 "${CLAUDE_SKILL_DIR}/size.py" --write                  # write fx/orders.json
python3 "${CLAUDE_SKILL_DIR}/size.py" --risk-usd 50 --write    # at most $50 at the stop
python3 "${CLAUDE_SKILL_DIR}/size.py" --risk-pct 0.5 --json    # half a percent, JSON answer
python3 "${CLAUDE_SKILL_DIR}/size.py" --plan old-plan.json --offline   # another plan, saved prices only
```

- `--now "2026-07-17 09:07"` pins the clock. A time with no offset is Karachi time.
  `--now` also means `--offline`.
- `--risk-pct` and `--risk-usd` can only make the max loss smaller, never bigger.
- A plan from another FX day is refused: make a new one with fx-exit.
- Exit codes: 0 sized, 1 a plain no (nothing written), 2 an error (one line).

It reads Yahoo prices for this instrument and the FX rates it needs (a few small
requests, 2 seconds apart). --offline and --now read only the saved prices.

## What it reads and writes

| file | what |
| --- | --- |
| `fx/config.json` | your account and limits, and each instrument's MetaTrader values (start from `config.example.json` in this folder) |
| `fx/plan.json` | the trade: side, entry, stop, target, style, flat-by or exit-by time (fx-exit writes it) |
| `fx/timemachine.json` | optional: one line of replay odds when it matches the plan (fx-timemachine) |
| `fx/portfolio.json` | optional: your balance and open trades (fx-broker keeps it) |
| `fx/prices.json` | optional: a newer Yahoo quote (fx-alerts `quote`) |
| `fx/data/` | the Yahoo price cache, FX rates for the money math, futures rolls |
| `fx/orders.json` | the one order it writes with `--write` |

## Step 1: set the rules once

1. Copy `config.example.json` from this folder to `fx/config.json`.
2. Ask for the balance. Use only money the user can lose.
3. Ask for the max loss per trade: `risk.max_risk_per_trade_pct` (1.0 means 1% of
   the balance), or a dollar cap in `risk.max_risk_per_trade_usd`. The smaller wins.
4. Ask for the margin cap: `risk.max_margin_used_pct` (30 by default).
5. Copy each instrument's values from MetaTrader. Right click the symbol in Market
   Watch > Specification (MT4: Symbols > Properties). Copy: contract size, digits,
   min, max and step lots, calculation mode, swap type, swap long and short, and the
   3-day swap day.
6. Keep `"paper": true`.

The six traps when you copy (`size.py --help` lists them too):

- Oil lot size. One lot of oil is 1 barrel (Tickmill), 100 barrels (IC, HFM) or 1,000
  barrels (Exness, FxPro). The same 2-dollar move is 2, 200 or 2,000 USD a lot. Copy yours.
- Silver lot size. 5,000 oz at most brokers (Tickmill, Exness, FxPro, XM), but 1,000 oz
  at IC. Copy yours.
- Gold digits. Most brokers show 2 digits (4126.20), some 3 (4126.200). Then one point
  is 0.01 or 0.001, and a swap of -54.84 points is -54.84 or -5.484 USD a lot.
- Swap in points or money. Copy "Swap type" too. -6.23 in points on EURUSD is -6.23 USD
  a lot; -6.23 "in money" means the same here only by chance. Exness web pages give swaps
  in pips, MetaTrader in points (10 times more on 5-digit pairs).
- Triple-swap day. Tickmill: Wednesday for FX, gold and silver; Friday for the rest.
  Exness: none for energies, Thursday for USDCAD. Copy "3-day swap" (MT5 shows a rate per
  weekday; the day with 3 is the triple day).
- Min lot. 0.01 lot of gold is 1 oz; Tickmill oil is 1 barrel a lot but the min is 1
  lot; IC oil min is 0.5 lot (50 barrels). A small account may not fit even one min lot.

## Step 2: size the trade

Run `python3 "${CLAUDE_SKILL_DIR}/size.py" --write` after fx-exit wrote `fx/plan.json`.
The lots are the smallest of four limits, rounded DOWN to the lot step:

| limit | what it allows |
| --- | --- |
| max loss | the lots that lose at most your max loss at the stop, costs in |
| max lot | the broker's largest order (`max_lot`) |
| margin cap | `max_margin_used_pct` of the balance, minus the margin in use |
| free margin | your equity minus the margin in use |

- Below the min lot it says no (exit 1). It never rounds up. It never moves the stop.
- The sizing entry: for a market order, the worse of the plan's entry and a fresh
  price (a buy at the ask, a sell at the bid). A price that ran away means a bigger
  loss at the same stop. A stop or limit order uses the plan's entry.
- A swing trade counts the swap for the whole hold (every night to the exit-by day,
  Wednesday 3 times). A swap paid to you counts 0: a broker can change it.
- A swap-free account counts the swap-free fee after the free nights.
- The order is a market, stop or limit order, as the plan says. A day order ends at
  the flat-by time. A swing order is good till cancelled.

## Step 3: show the user

- The lots, and the max loss at the stop in its parts: price and spread,
  commission, swap. Say "costs included".
- The margin, and the value of one point (and one pip for FX).
- The gap note: a jump past the stop loses more than the max loss.
- A stop is a plan, not a promise. Over a weekend or at big news the fill can be worse.
- Then hand over to `/fx-risk`: `python3 fx-risk/check.py`.

## Example

The sample market made for the tests. All its prices are made up. Gold swing BUY,
`--now "2026-07-17 09:07" --write`, a $10,000 paper account, 1% a trade:

```
SIZED: 0.02 lots of XAUUSD (BUY, swing).
Setup: 20-day high breakout. Market order: you buy at the ask.
Entry 2,433.49 = Yahoo bid 2,433.40 + spread 0.09.
Stop 2,400.00: 33.49 (3,349 points) under the entry.
...
Max loss at the stop: $97.81, costs included.
  price and spread  0.02 lots x 33.49 x 100 = $66.98
  commission        $0.12 (both sides)
  swap              $30.71 if held all 28 nights (-54.84 points a night)
  one more step (0.03 lots) would lose $146.72: over your $100.00
...
Proposed order (nothing has been placed):
  BUY 0.02 lots XAUUSD at the market. SL 2,400.00. TP 2,490.00. Good till cancelled.
Wrote 1 order to fx/orders.json.
```

The same plan on the shipped $1,000 account:

```
NO ORDER for XAUUSD (BUY, swing).
0.01 lot is the smallest order for XAUUSD. At this stop it loses $48.91. Your
max loss is $10.00. So this trade is too big for your account. Do not move the
stop closer to make it fit. At 1.0% a trade you need about $4,890.52 for this
trade.
Nothing was written.
```

The EURUSD day SELL of Thu 2026-07-23: 0.86 lots lose $98.90 at the stop; 0.87 lots
would lose $100.05, over the $100.00 limit.

## Rules

- Proposals only. It writes one order to `fx/orders.json`. It never places it.
- Every number comes from the config, the plan or the prices. Nothing is guessed:
  not the contract size, not the swap.
- Yahoo prices are not your broker's prices. Futures-based ones (gold, silver,
  oil, gas, copper) differ more. fx-broker turns the levels into your broker's.
- It never says what a trade will make. A target is a plan, not a forecast.

## What it never does

- It never places, approves or sends an order. It never calls a broker.
- It never raises a limit on its own and never moves a stop or a target.
- It never writes plan.json (only fx-exit does). A roll moves the plan in memory only.
- It never writes more than one order. `--write` replaces orders.json whole.
- It never guesses a contract size. The numbers come from the config.
- It never says what a trade will make.

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
