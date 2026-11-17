---
name: psx-alerts
description: >-
  PSX Alerts. Keeps a small list of price-and-time alerts on symbols
  (above PRICE, below PRICE, pct_move >= X %, bar at HH:MM, opening
  bell), checks them against the PSX Data Portal's latest intraday
  tick, and marks them triggered with the exact tick that fired.
  Reads/writes psx/state/alerts.json. Use when the user says "alert me
  on OGDC above 320", "ping me when HUBC breaks 210", "alert if LUCK
  drops 2 %", "wake me at opening bell", "check my alerts", or wants
  something to watch the market while /psx-entry is running.
argument-hint: "add SYM above|below|pct_move PRICE | check | list | clear"
---

# psx-alerts

`${CLAUDE_SKILL_DIR}` is this skill's folder.

```bash
python3 "${CLAUDE_SKILL_DIR}/alerts.py" add OGDC above 320
python3 "${CLAUDE_SKILL_DIR}/alerts.py" add HUBC below 204.30
python3 "${CLAUDE_SKILL_DIR}/alerts.py" add LUCK pct_move -2.0
python3 "${CLAUDE_SKILL_DIR}/alerts.py" add OGDC time 10:30
python3 "${CLAUDE_SKILL_DIR}/alerts.py" add * opening_bell
python3 "${CLAUDE_SKILL_DIR}/alerts.py" check                 # poll once
python3 "${CLAUDE_SKILL_DIR}/alerts.py" list
python3 "${CLAUDE_SKILL_DIR}/alerts.py" clear --triggered     # remove fired ones
python3 "${CLAUDE_SKILL_DIR}/alerts.py" clear --all
```

Flags: `--offline PATH`, `--now "YYYY-MM-DD HH:MM"`, `--json`.

## Rule types

- **above PRICE** — latest tick ≥ PRICE
- **below PRICE** — latest tick ≤ PRICE
- **pct_move N** — abs((latest - prev_close) / prev_close × 100) ≥ |N|;
  sign of N decides direction (positive = up, negative = down).
- **time HH:MM** — fires once the Asia/Karachi clock passes HH:MM.
- **opening_bell** — fires when the clock passes the session's open
  (09:32 Mon-Thu, 09:17 Friday / Ramadan).

## alerts.json shape

```json
{
  "alerts": [
    {"id": "a1", "symbol": "OGDC", "rule": "above", "value": 320,
     "created": "2026-11-17T09:12:00+05:00",
     "status": "active"},
    {"id": "a2", "symbol": "HUBC", "rule": "below", "value": 204.30,
     "status": "triggered",
     "triggered_at": "2026-11-17T10:04:12+05:00",
     "triggered_price": 204.18}
  ]
}
```
