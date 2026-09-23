---
name: subscription-audit
description: Finds the recurring charges (subscriptions) hiding in a bank or credit-card CSV, tells you the true monthly and yearly cost, and flags the ones that look forgotten — a free trial that started charging, or a service that quietly kept billing after you stopped using it. Reads a statement you exported yourself; no bank login, no third-party service, fully offline and deterministic.
when_to_use: You (or the person you're helping) want to know where the small monthly charges are going — "why is my card $95 lighter every month?" Point it at an exported bank/card CSV and it clusters repeat payments by merchant and cadence, surfaces the real monthly total, and names the stale subscriptions worth cancelling. Also runs as a monthly cron/CI check that pings you when recurring spend creeps past a budget. NOT a full budgeting app, NOT a categorizer of one-off spending — it only tracks what recurs.
version: 1.0.0
license: MIT
metadata:
  agentskills:
    tags: [personal-finance, subscriptions, budget, csv, everyday]
---

# Subscription Audit

Re-read a year of statements the way no human bothers to.

## Overview

Subscriptions are engineered to be invisible. Each charge is small, they land on
different days, the merchant name is `ADOBE *CREATIVE CLOUD 800-833` instead of
"Adobe", and nobody sits down to re-read twelve months of a bank statement by
hand. So the free trial that started charging, the gym you stopped going to, the
app you used once — they just keep billing.

`subscription_audit.py` is the re-reader. Feed it a CSV you exported from your
bank or card and it:

- **finds the recurring charges** by clustering repeat payments to the same
  merchant at a regular cadence (weekly / monthly / quarterly / yearly), while
  ignoring one-off spending like groceries, gas, or a flight;
- **normalizes messy merchant names** (`AMZN Mktp US*RT4G9` → `amazon`, store
  numbers and auth codes stripped) so the same service groups together;
- **reports the true cost** — monthly and annualized — across everything it found;
- **flags review candidates**: a subscription whose expected next charge is well
  overdue (`STALE`), or one whose first non-zero charge was substantially smaller
  than later charges (`trial→paid`).

No bank login, no Plaid, no cloud. It reads a file you already have, is pure
standard library, and is deterministic — the same statement always gives the same
answer. A ruler for your recurring spend, not a budgeting app.

## When to use

- **The monthly "where does it go?" question.** Export a statement, run the tool,
  see the whole subscription stack ranked by cost in one screen.
- **A cancellation sweep.** The `STALE` and `trial→paid` flags are your cut list —
  the tool even totals what cancelling the stale ones saves per year.
- **A budget guardrail on a schedule.** Run it monthly with `--budget N`; it exits
  non-zero when detected recurring spend creeps past your line, so a cron job or CI
  step can ping you when subscription creep sets in.

Not for: categorizing one-off spending, forecasting, or replacing a real budgeting
app. It answers exactly one question — *what am I paying for on repeat?*

## The method

1. **Export a statement.** From your bank or card, download transactions as CSV
   (any date range; the more months, the better the cadence detection). Most
   exports have a date, a description/merchant, and an amount column — the tool
   sniffs these by header name or by content, so you usually need no flags.
2. **Run it.**
   ```bash
   python scripts/subscription_audit.py statement.csv
   # or pipe it:  cat card.csv | python scripts/subscription_audit.py -
   ```
3. **Read the stack.** Subscriptions are listed heaviest-first with their monthly
   cost, per-charge amount, cadence, and last-seen date. The footer gives the total
   monthly and yearly burn.
4. **Review the flags.** `⚠ STALE` means no charge appears within the configured
   interval; `trial→paid` means the first non-zero charge was smaller than later
   charges. The summary estimates the yearly cost of the stale entries. Confirm
   each charge with the provider before cancelling it.
5. **Put it on a leash.** Add `--budget 80` to fail (exit 1) when recurring spend
   passes $80/mo, and drop that into a monthly cron so creep gets caught early.

Useful flags: `--json` (machine-readable, for a cron/agent to consume),
`--min-charges N` (how many hits before a merchant counts as recurring; default 3),
`--stale-days N` (grace period past the expected next charge before flagging),
`--currency €` (display symbol).

## Anti-patterns

- **Feeding it two months and expecting miracles.** Cadence detection needs at
  least three hits of a merchant. A short statement will under-report — export a
  longer range.
- **Trusting `STALE` as "already cancelled".** Stale means *no recent charge in
  this file* — it might be an annual plan that just isn't due, or a charge outside
  your export window. It's a prompt to check, not proof it's dead.
- **Treating the monthly total as your whole budget.** This is recurring spend
  only; it deliberately ignores groceries, gas, and one-offs. It's not a full
  budget.
- **Cancelling on the merchant string alone.** `github` and `github sponsors` may
  be two different things collapsed by name normalization — glance at the example
  description before you cancel.

## Example

```
$ python scripts/subscription_audit.py statement.csv --budget 100 --stale-days 20
Subscription audit
======================================================================
  monthly      each  cadence    last          merchant
----------------------------------------------------------------------
$  54.99  $ 54.99  monthly    2026-06-15    adobe creative cloud
$  15.49  $ 15.49  monthly    2026-06-03    netflix
$  10.99  $ 10.99  monthly    2026-07-05    spotify usa ny
$  10.00  $ 10.00  monthly    2026-03-28    planet fitness  ⚠ STALE
$   4.00  $  4.00  monthly    2026-04-18    github  ⚠ STALE
----------------------------------------------------------------------
$  95.47  monthly across 5 subscriptions  (≈ $1,146/yr)

⚠ 2 look forgotten (no charge in a while): cutting them saves $14.00/mo (≈ $168/yr).
    · planet fitness — last seen 2026-03-28 (99d ago), $10.00/mo
    · github — last seen 2026-04-18 (78d ago), $4.00/mo

budget $100.00/mo  →  OK ($95.47 detected)
```

Groceries, gas, a flight, and an Amazon order in the same statement were correctly
ignored — only the things that recur on a rhythm were surfaced.
