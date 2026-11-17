---
name: psx-ticket
description: >-
  PSX Ticket. Prints a plain-text paper ticket for the current
  psx/order.json so you can enter the order by hand in your PSX broker's
  platform (AKD Trade, JS Global TradeCast, Alfalah Trade, Arif Habib
  CTS, MIT, etc. - PSX has no public retail-broker API), records it in
  psx/state/broker.json, lets you log the actual fill price and quantity
  after the trade with `fill`, and can list open orders or cancel one.
  Paper-trading-first so you see how the plan survives real slippage
  before risking money. Use when the user says "print the ticket",
  "write the ticket for HUBC", "log the fill", "mark that filled at X",
  "list my open orders", "cancel order", or right after /psx-risk passes.
argument-hint: "write | fill ID @ PRICE qty QTY | list | cancel ID"
---

# psx-ticket

`${CLAUDE_SKILL_DIR}` is this skill's folder.

```bash
python3 "${CLAUDE_SKILL_DIR}/ticket.py" write                          # paper ticket for the current order
python3 "${CLAUDE_SKILL_DIR}/ticket.py" write --approve yes            # you MUST type "yes" exactly
python3 "${CLAUDE_SKILL_DIR}/ticket.py" list                           # show all orders
python3 "${CLAUDE_SKILL_DIR}/ticket.py" fill 7c8d3f1a9e4b2d5c --price 208.25 --qty 1351
python3 "${CLAUDE_SKILL_DIR}/ticket.py" cancel 7c8d3f1a9e4b2d5c
```

## Why there is no broker auto-submit

PSX retail brokers run proprietary trading platforms (AKD Trade / JS
TradeCast / Alfalah Trade / Arif Habib CTS / MIT / Foundation TradeX
and others). None publishes an authenticated retail API in the way
Alpaca, IBKR or Robinhood do. So `psx-ticket` prints a clean
plain-text order you type into the broker's own screen, and after
the trade you come back here and record what actually happened.

**This is a feature, not a limit.** The hand step forces you to
re-read every number - entry, stop, size, R/R - before you click
"Place Order" in your broker. If a trader can't bring themselves to
type the order by hand, they probably should not place it.

## The ticket

```
================= PSX PAPER TICKET =================
Fingerprint: 7c8d3f1a9e4b2d5c
Symbol:      HUBC                Side: LONG
Order type:  LIMIT               TIF:  DAY
Entry:       PKR 208.00          Qty:  1351
Stop:        PKR 204.30 (or-low)
Target:      PKR 215.40 (R/R 2.0)
----------------------------------------------------
Gross cost:  PKR 280,808.00      Net R/R: 1.45 (after costs + CGT)
Risk gross:  PKR 5,000.00        Risk net: PKR 6,020.62
----------------------------------------------------
Risk verdict: WARN   Checks that need a look: shariah (HUBC not in KMI-ALL)
----------------------------------------------------
Type EXACTLY "yes" to record this order:
====================================================
```

The approval parser only accepts the word **"yes"** on its own - not
"y", not "ok", not "all", not any phrase that mentions "yes" like
"yes but 1000 shares". The reference day-trader skill learned this
the hard way; we inherit the rule.

## state/broker.json

```json
{
  "orders": [{
    "fingerprint": "7c8d3f1a9e4b2d5c",
    "written_at": "2026-11-17T09:55:30+05:00",
    "symbol": "HUBC", "side": "long", "qty": 1351,
    "entry": 208.00, "stop": 204.30, "target": 215.40,
    "status": "pending"       // pending | filled | cancelled
  }],
  "fills": [{
    "fingerprint": "7c8d3f1a9e4b2d5c",
    "filled_at": "2026-11-17T09:56:12+05:00",
    "price": 208.25, "qty": 1351, "date": "2026-11-17"
  }],
  "lots": [...]                // FIFO lots per symbol
}
```

## Refuses to write a ticket when

- `psx/state/risk.json` doesn't exist (run `psx-risk` first).
- Risk verdict is `FAIL`.
- Order fingerprint doesn't match the risk file's fingerprint
  (something changed after the risk check - re-run `psx-risk`).
- `--approve yes` was not passed on the same command line.
