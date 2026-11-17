---
name: psx-budget
description: >-
  PSX Budget / Sizing. Reads psx/plan.json and psx/config.json (editable
  cost table in PKR) and sizes the position against four limits -
  max_loss_per_trade, max_position_pct, max_order, cash_available.
  Computes every PSX cost on both sides of the round trip (broker
  commission, PSX trading fee, PSX regulatory fee, SECP levy, NCCPL
  trade fee, CDC transaction fee, provincial sales tax on brokerage,
  CGT on the gain), then writes psx/order.json so psx-risk can
  pre-flight-check it and psx-ticket can print the paper ticket. Use
  when the user says "size this trade", "how many shares", "position
  size for HUBC", "what's it cost round-trip", "what's my net R/R
  after taxes", "budget the trade", or right after /psx-exit.
argument-hint: "[--risk 5000] [--position-pct 10] [--max-order 100000] [--cash 500000]"
---

# psx-budget

`${CLAUDE_SKILL_DIR}` is this skill's folder.

```bash
python3 "${CLAUDE_SKILL_DIR}/size.py"                                   # read defaults from psx/config.json
python3 "${CLAUDE_SKILL_DIR}/size.py" --risk 5000                       # cap this trade's gross risk at PKR 5,000
python3 "${CLAUDE_SKILL_DIR}/size.py" --position-pct 10                 # cap position at 10 % of cash
python3 "${CLAUDE_SKILL_DIR}/size.py" --max-order 100000                # cap order gross value at PKR 100k
python3 "${CLAUDE_SKILL_DIR}/size.py" --cash 500000                     # override cash on hand
python3 "${CLAUDE_SKILL_DIR}/size.py" --config FILE --plan FILE --out FILE --json
```

On first run, `size.py` writes a default `psx/config.json` you can edit.

## The four limits

The largest share count that passes **all four** wins:

- **max_loss_per_trade** — rupees you will accept losing if the stop hits.
  qty ≤ floor(max_loss / risk_per_share).
- **max_position_pct** — percent of cash allowed in one position.
  qty ≤ floor(cash * pct / 100 / entry).
- **max_order** — rupee cap on the order's gross value.
  qty ≤ floor(max_order / entry).
- **cash_available** — you must be able to pay for it.
  qty ≤ floor(cash / entry).

Lot size on PSX's Regular Market is **1 share**, so there is no
rounding-to-lot step. Tick is flat PKR 0.01.

## The cost model (editable)

Every value in `psx/config.json` can be edited. Defaults are the
public PSX / NCCPL / SECP / CDC tariffs as of 2026-06; the user is
responsible for keeping them current (see `README.md` for sources).

```json
{
  "cash_available": 500000,
  "max_loss_per_trade": 5000,
  "max_position_pct": 10,
  "max_order": 100000,
  "broker": {"rate_bps": 15, "min_pkr": 50, "max_pkr": 10000},
  "fees_per_100k": {
    "psx_trading": 3.50, "psx_regulatory": 0.62,
    "nccpl_trade": 0.81, "nccpl_secp": 0.30
  },
  "secp_levy_bps": 0.065,
  "cdc": {"rate_bps": 0.36, "min_pkr": 5, "max_pkr": 25000},
  "sales_tax_pct_on_brokerage": 13,
  "cgt_pct_short_term": 15
}
```

`rate_bps` = basis points of order value (100 bps = 1 %).

## order.json shape

```json
{
  "symbol": "HUBC", "side": "long", "qty": 1351,
  "entry": 208.00, "stop": 204.30, "target": 215.40,
  "gross_cost": 280_808.00, "gross_proceeds_at_target": 291_105.40,
  "costs": {
    "buy_brokerage": 421.21, "buy_psx_fees": 14.49,
    "buy_sales_tax": 56.64, "buy_secp_levy": 1.82, "buy_cdc": 10.11,
    "sell_brokerage": 436.66, "sell_psx_fees": 15.03,
    "sell_sales_tax": 58.72, "sell_secp_levy": 1.89, "sell_cdc": 10.48,
    "round_trip_fixed": 1026.05,
    "cgt_on_gain": 1544.61
  },
  "net_risk_pkr": 6020.62, "net_reward_pkr": 8726.36,
  "net_rr": 1.45,
  "limit_hit": "max_loss_per_trade"
}
```

Fees are shown on both legs so you can tell what the exchange charges
versus what the broker charges, and `limit_hit` tells you which of the
four limits set your size.

## What it does NOT do

- Does not place the order. See `psx-ticket` for the paper ticket you
  enter in the broker platform by hand.
- Does not model slippage. Entry and target are exact prices; your
  real fill may differ.
- Short selling on PSX is only available through NCCPL's Securities
  Lending & Borrowing (SLB) scheme and is not covered here - the skill
  writes a `--short` order and `psx-risk` warns you.
