---
name: psx-risk
description: >-
  PSX Risk. Pre-flight-checks psx/order.json against a dozen named rules
  (order shape, cash on hand, position-pct cap, PSX scrip circuit breaker,
  stop on the correct side, minimum net R/R after costs, daily loss
  budget, trading-window open, PSX holiday, short-selling flagged, duplicate
  order via fingerprint, Shariah tag mismatch) and prints a pass/warn/fail
  per check with the exact numbers. Writes psx/state/risk.json.  Use when
  the user says "check the risk", "is this trade safe", "pre-flight the
  order", "risk check on OGDC", "am I over my daily limit", "any red flags",
  or right after /psx-budget and before /psx-ticket.
argument-hint: "[--order FILE] [--prev-close P] [--daily-loss-cap L] [--shariah strict|warn|off]"
---

# psx-risk

`${CLAUDE_SKILL_DIR}` is this skill's folder.

```bash
python3 "${CLAUDE_SKILL_DIR}/check.py"                           # all defaults
python3 "${CLAUDE_SKILL_DIR}/check.py" --prev-close 207.33       # supply the scrip's previous close
python3 "${CLAUDE_SKILL_DIR}/check.py" --daily-loss-cap 15000    # override
python3 "${CLAUDE_SKILL_DIR}/check.py" --shariah strict          # block non-KMI-ALL symbols
python3 "${CLAUDE_SKILL_DIR}/check.py" --json
```

Flags: `--order PATH` (default `psx/order.json`), `--config PATH`
(default `psx/config.json`), `--now "YYYY-MM-DD HH:MM"` (PKT),
`--offline PATH`.

## The checks

Each check prints one line and ends with `PASS`, `WARN`, or `FAIL`:

1. **shape** — qty>0, prices > 0, stop on correct side of entry.
2. **cash** — gross_cost ≤ cash_available.
3. **position_pct** — gross_cost ≤ cash × max_position_pct / 100.
4. **circuit_breaker** — stop and target are inside the PSX scrip
   circuit (`max(8 % of prev_close, PKR 1)`), unless the user passes
   `--allow-circuit`.
5. **net_rr** — order.net_rr ≥ 0.5 (after all costs incl. CGT).
6. **daily_loss** — order.net_risk + today's realised loss ≤
   daily_loss_cap.
7. **trading_window** — `now` is inside the regular PSX session
   (Mon-Thu 09:32-15:30 / Friday 09:17-12:00 or 14:32-16:30 / Ramadan
   09:17-13:30|12:30). Uses the baked-in 2026 PSX holidays; 2027
   dates are flagged as "to confirm" and warn only.
8. **short_sell** — `side=="short"` warns: on PSX short selling is
   only available through NCCPL's SLB, and ordinary retail cash
   accounts can't do it.
9. **shariah** — with `--shariah strict`, fails if the symbol is not
   in the KMI-ALL universe; with `warn`, warns; with `off` (default
   when run from the public GitHub fork), silently passes.
10. **duplicate** — fingerprint (sha256 of symbol|side|qty|entry|stop
    |target)[:16] must not match any order in `psx/state/broker.json`
    with status != cancelled.
11. **fingerprint_stable** — prints the tag so `psx-ticket` can match
    it later. If the two don't match, something changed in between.
12. **cost_sanity** — round_trip_fixed should be at least PKR 50 (min
    brokerage both legs). A value below that usually means a mis-edited
    config.

## state/risk.json shape

```json
{
  "checked_at": "2026-11-17T09:55:12+05:00",
  "fingerprint": "7c8d3f1a9e4b2d5c",
  "checks": [
    {"name": "shape", "status": "PASS", "detail": "qty=1351, long"},
    {"name": "cash", "status": "PASS", "detail": "280808 <= 500000"},
    ...
  ],
  "verdict": "PASS"    // overall: PASS | WARN | FAIL
}
```

The overall `verdict` is FAIL if any check is FAIL, else WARN if any
is WARN, else PASS. `psx-ticket` refuses to print a paper ticket
unless the verdict is PASS or WARN (never FAIL).
