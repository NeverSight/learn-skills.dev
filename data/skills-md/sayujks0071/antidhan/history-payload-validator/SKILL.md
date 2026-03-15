---
name: history-payload-validator
description: Validate and fix OpenAlgo history API payloads before strategy runs. Use when /api/v1/history returns 400/404, symbols are missing, intervals are invalid, or master contracts need refreshing.
---

# History Payload Validator

## Quick Start
- Check logs for `/api/v1/history` errors (400/404, missing fields, symbol not found).
- Verify payload has: `symbol`, `exchange`, `interval` (e.g., 1m/3m/5m/15m/30m/1h/4h/D), `start_date`, `end_date` (ISO), and any required `resolution`/`from`/`to` fields per endpoint variant.
- Confirm master contracts are present for the exchange/symbol before requesting history.
- Send a manual test call; only start strategies after it succeeds.

## Required Fields Checklist
- `symbol`: Exact broker symbol (e.g., `NIFTY`, `BANKNIFTY`, or contract code).
- `exchange`: `NSE`, `NFO`, `MCX`, etc.
- `interval`: Use allowed values; avoid raw seconds unless API supports it.
- Date range: `start_date` and `end_date` in `YYYY-MM-DD` (or datetime ISO if needed).
- Optional legacy fields: include `resolution`, `from`, `to` if the endpoint expects TradingView-style params.

## Master Contract Precheck
- Ensure master contracts exist for the exchange:
  - If missing: run the platform’s master contract download/refresh step.
  - Re-test history after refresh.

## Manual Test Template
```bash
curl -X POST http://127.0.0.1:5001/api/v1/history \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "NIFTY",
    "exchange": "NSE",
    "interval": "5m",
    "start_date": "2026-01-29",
    "end_date": "2026-01-29",
    "resolution": "5"
  }'
```
- If this passes, align strategy payload builders to match.

## Debug Workflow
1) Read the failing log entry to see which fields were rejected.
2) Open the strategy payload builder and confirm every required field is populated.
3) Validate interval value against allowed list.
4) Confirm symbol exists in master contracts (and exchange matches).
5) Re-run the manual test; then restart the strategy.

## Preventive Steps
- Add unit-style checks in strategy code to assert payload completeness before calling history.
- Default to a safe interval (e.g., `5m`) when config is missing.
- Log the payload (without secrets) when a 400 occurs to speed up triage.
