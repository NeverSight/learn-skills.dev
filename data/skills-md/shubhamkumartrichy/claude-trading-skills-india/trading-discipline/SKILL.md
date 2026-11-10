---
name: trading-discipline
description: |
  Rules that protect an Indian trader from themselves: an account-level circuit breaker (daily 2%,
  weekly 5%, monthly 10% loss limits plus losing-streak cooldowns) read from the trade journal, a
  pre-trade gate (stop, rupee risk, R:R, written plan, revenge window, regime, F&O ban, ASM/GSM/T2T,
  results, circuit lock, expiry day, MIS cut-off) that returns PASS / PASS-WITH-WARNINGS / BLOCK
  before any order ticket, a performance review by setup, weekday, hour, segment and mistake, a
  weekly digest, and an opt-in decision log. discipline.py, stdlib only, offline.

  Use when the user asks: "should I take this trade", "can I trade today", "I've lost 3 in a row",
  "am I revenge trading", "check my trade before I place it", "daily loss limit", "review my
  journal / trades", "what's my worst setup", "weekly trading report", "why do I keep losing in F&O",
  or before any order is drafted.
---

# Trading Discipline

Most retail losses come from behaviour, not analysis: the oversized trade, the revenge trade after
a loss, the fifth trade on a red day. This skill turns the rules into checks that run *before*
money moves, and turns the journal into feedback afterwards.

## Commands

```bash
# Can I trade today? (status GREEN / AMBER / RED + allowed risk for the next trade)
python3 scripts/discipline.py breaker trades.csv --capital 500000 [--as-of 2026-10-29]
# Pre-trade gate (writes nothing). Add --journal to fold in the breaker.
python3 scripts/discipline.py gate --capital 500000 --entry 1450 --stop 1410 --target 1550 --qty 120 \
    --plan-written yes --minutes-since-last-loss 90 --regime risk-on --fno-ban no --asm-gsm no \
    --event no --circuit-locked no --journal trades.csv
python3 scripts/discipline.py gate --segment options-buy --entry 140 --stop 85 --qty 75 --expiry-day yes ...
# Coaching review, and the latest ISO-week digest (or --week 2026-W43)
python3 scripts/discipline.py review trades.csv [--recent 10]
python3 scripts/discipline.py review trades.csv --week
# Only when the user asks to keep a record: run the gate and append one row to a CSV log
python3 scripts/discipline.py log --log decisions.csv --symbol INFY --action taken <gate flags>
```

Every command takes `--json`. Dates are IST; `--as-of` defaults to today in IST. Bad input prints
`error: ...` and exits 2.

**Journal:** the same CSV as `../position-sizing/scripts/risk.py journal`
(`date,symbol,side,entry,exit,stop,qty,charges`, or a `pnl` column), plus optional `exit_date`,
`time` (HH:MM entry time), `setup` (or `tag`), `mistake` (several separated by `;`), `segment`
(equity / fno / intraday) and `notes`. A row with a blank exit and blank pnl is an **open** trade:
it is left out of realised statistics and listed separately, and its stop risk counts against the
breaker's remaining room. A zero-P&L trade is a **breakeven**, not a loss.

## Circuit breaker: rules and why

| Rule (default, flag) | Trips | Releases | Why |
|---|---|---|---|
| Daily loss 2% (`--daily-pct`) | RED | Next weekday | Two full 1% losses; after that, decisions get worse |
| Weekly loss 5% (`--weekly-pct`, Mon–Sun) | RED | Next Monday | Stops a bad day turning into a bad month |
| Monthly loss 10% (`--monthly-pct`) | RED | 1st of next month | Recovering 10% needs 11%; recovering 30% needs 43% |
| 3 losses in a row, latest today (`--stop-streak`) | RED | Next weekday | Tilt: the next trade is usually the worst one |
| 3+ streak still open from an earlier day | AMBER | A win | First trade back should be your best setup |
| 5 losses in a row (`--reduce-streak`) | AMBER, size ×0.5 | After 5 more trades (`--reduce-trades`) | Shrink until the edge reappears |
| Any period ≥ 50% of its limit | AMBER | — | Early warning |

Limits use **net realised P&L** for the IST day, ISO week and calendar month. Breakevens neither
extend nor break a streak. **Allowed risk** for the next trade = normal risk (`--risk-pct`, 1%) × the
size multiplier, capped so that a stop-out (plus stop risk on open trades) cannot breach any limit.
Holidays are not modelled; "next weekday" may be an NSE holiday (see `indian-market-structure`).

## Pre-trade gate

Any BLOCK → **BLOCK**; otherwise any WARN → **PASS-WITH-WARNINGS**; else **PASS**. Unsupplied
yes/no flags are skipped, except where noted.

| Check | BLOCK when | WARN when |
|---|---|---|
| Stop-loss | Missing, or on the wrong side | Option buy with no premium stop (full premium = risk) |
| Rupee risk | Unknown (no qty/capital), or > `--risk-pct-limit` (1%) | — |
| Target | Wrong side, or R:R < 1 | Missing, or R:R < 1.5 |
| Written plan | `--plan-written no` | Not stated |
| Revenge window | < 30 min since last loss (`--revenge-minutes`) | Not stated but today's last journal trade was a loss |
| Regime (label from `market-regime`) | crash / panic / no-trade, for longs | Trading against risk-off or risk-on; sideways / volatile; unknown label |
| F&O ban | Fresh F&O position in a ban-period stock | Cash trade in a ban stock; F&O with ban status unknown |
| ASM / GSM / T2T (`--asm-gsm`) | Intraday (T2T/GSM can't be squared off) | Delivery |
| Results / board meeting in window (`--event`) | — | Gap risk; IV crush for options |
| Circuit-locked (`--circuit-locked`) | Always | — |
| Expiry day (Tue NIFTY, Thu SENSEX) | — | Option buy on expiry; option sell (extra ELM). Auto-flagged on Tue/Thu if not stated |
| MIS cut-off (`--segment intraday`, `--time`) | At or after 15:00 IST (auto square-off ~15:15–15:20) | Before 09:15 |
| Circuit breaker (`--journal`) | RED, or trade risk > breaker's allowed risk | AMBER |

`--segment` is equity, intraday, futures, options-buy or options-sell. `--qty` is the total quantity
(lots × lot size). Add `--charges` (₹) from `trading-costs` to include costs in the risk.

## How other skills use the gate

- **`india-market-analyst`**: when a trade idea reaches a concrete entry/stop/target, run the gate
  and show its verdict with the plan. Fetch ban list, ASM/GSM status and results dates first where
  a data source allows; otherwise ask the user rather than assuming "no".
- **`broker-integration`**: the gate runs *before* step 3 of the order protocol (the ticket).
  BLOCK → do not draft a ticket; explain the blocks. PASS-WITH-WARNINGS → list each warning on the
  ticket and still wait for an explicit "yes". PASS → the normal ticket and confirmation still apply.
  The gate never places, modifies or cancels orders.
- **Logging** is opt-in: use `log` only when the user asks to keep a decision record. It appends one
  row and refuses a file whose header is not a decision log.

## Not the same as position-sizing

`position-sizing` answers *how many shares* for a given risk. This skill answers *whether to trade
at all, and how much risk is allowed right now*, given today's losses, streaks and the checklist.
Use the breaker's allowed risk as the `--risk-pct` input to `risk.py size`, then gate the result.

## Review and weekly digest

`review` reports win rate, average win/loss, profit factor, expectancy (₹ and R), max drawdown and
longest losing streak, then breaks results down by setup, entry weekday, entry hour, segment, F&O
vs cash, mistakes ranked by ₹ lost, clean vs mistake trades, winner vs loser holding days (needs
`exit_date`), and the last N trades vs the N before. Coach notes name the best and worst setup, the
costliest mistake and any trend. `--week` summarises one ISO week: trades closed, best and worst,
mistakes, setup mix and the previous week's net.

**F&O context:** SEBI's FY25 study found about 91% of individual F&O traders lost money; the FY26
update (press release 50/2026) put it near 88%. If a user's own F&O rows are net negative while cash
trades are positive, say so plainly and suggest pausing F&O until the cash edge is proven.

## Output

```
Circuit breaker: AMBER (as of Tue 27 Oct 2026 IST, capital ₹5,00,000)
Allowed risk on next trade: ₹2,500 (0.50%) • After a 5+ loss streak, risk is cut to 50% for 3 more trades
Pre-trade gate: BLOCK  [BLOCK] revenge-window  Only 10 min since the last loss ...
```

Limits: every India flag is supplied by the user or a data tool, so the gate is only as good as
those answers. Regime labels are matched by keyword. Fewer than 30 trades make review numbers noisy.

_Educational discipline tool, not investment advice. The rules are defaults; the decision stays yours._
