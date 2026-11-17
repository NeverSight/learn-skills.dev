---
name: psx-exit
description: >-
  PSX Exit. Takes psx/entry.json and the opening-range it was drawn
  against, and writes psx/plan.json with an explicit stop price, a
  reward/risk target, a stop-rule label (or-mid, or-low, or-high,
  price:X, pct:X) and the detail you need to defend it later. One
  clean exit plan per trade. Use when the user says "set my stop",
  "plan the exit on OGDC", "where do I cut this", "what's my target",
  "stop-and-target", "write the plan", or right after /psx-entry fires.
argument-hint: "[--stop or-mid|or-low|or-high|price:X|pct:X] [--rr 2]"
---

# psx-exit

`${CLAUDE_SKILL_DIR}` is this skill's folder.

```bash
python3 "${CLAUDE_SKILL_DIR}/exit.py"                                  # default: or-mid, R/R=2
python3 "${CLAUDE_SKILL_DIR}/exit.py" --stop or-low --rr 2             # ORB long usually
python3 "${CLAUDE_SKILL_DIR}/exit.py" --stop or-high --rr 2            # ORB short
python3 "${CLAUDE_SKILL_DIR}/exit.py" --stop price:310.50              # hard price
python3 "${CLAUDE_SKILL_DIR}/exit.py" --stop pct:1.5                   # 1.5 % away from entry
python3 "${CLAUDE_SKILL_DIR}/exit.py" --json
```

Flags: `--rr 2` (reward-to-risk multiple; 1, 1.5, 2, 3 are typical),
`--entry PATH` (default `psx/entry.json`), `--out PATH` (default
`psx/plan.json`).

## Stop rules

- **or-mid** - halfway between the opening range high and low. Tight.
- **or-low** - the OR low (for long trades) or OR high (for shorts).
  The "obvious" level the move was supposed to hold.
- **or-high** - the OR high; unusual for a long entry, standard for a
  short entry.
- **price:X** - a fixed price in rupees. You pick it; this skill records it.
- **pct:X** - X % from the entry price (long: below; short: above).

## plan.json shape

```json
{
  "symbol": "HUBC", "side": "long", "entry": 208.00,
  "stop": 204.30, "stop_label": "or-low",
  "stop_detail": "opening-range low (09:32-09:47 PKT)",
  "target": 215.40, "rr": 2.0,
  "risk_per_share": 3.70, "reward_per_share": 7.40
}
```

Prices are stored as two-decimal numbers. Lot size is 1 share in the
Regular Market, and the tick is a flat PKR 0.01.

## Costs

`psx-exit` writes the risk/reward **in share units**. Gross rupees,
commissions, PSX / NCCPL / SECP / CDC fees, Sindh sales tax (13 %) on
brokerage, and CGT (flat 15 %, TY 2026) are applied by `psx-budget`
and `psx-risk` once the share count is known.

## Scrip circuit breaker

PSX halts a scrip whose daily move hits 8 % or Re 1 (whichever is
higher) from the previous close. If your target or stop crosses the
day's circuit limit, `psx-risk` flags it before the order goes in -
see that skill.
