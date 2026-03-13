---
name: strategy-startup-guardrails
description: Prevent and triage strategy startup crashes (imports, time module misuse, missing master contracts, env/config gaps). Use when strategies fail immediately at launch or after restart.
---

# Strategy Startup Guardrails

## Quick Checklist (before launch)
- Imports: avoid shadowing `time`; use `from datetime import time as dt_time` and `import time as time_module` for timestamps.
- Market hours helpers: call `dt_time(...)`, not `time(...)` if `time` is a module.
- Config/env: confirm `OPENALGO_APIKEY`, broker creds, and host/port.
- Data readiness: master contracts downloaded for required exchanges/symbols.
- History preflight: run one manual history request with real payload (see `history-payload-validator`).

## Fast Triage Steps
1) Read the latest strategy log for the traceback.
2) If `TypeError: 'module' object is not callable`, search for `time(` with a module import:
   ```bash
   rg "import time" openalgo/strategies | head
   rg "time\\(" openalgo/strategies/scripts
   ```
   Ensure you call `dt_time(...)` for market hours and `time_module.time()` for timestamps.
3) If crash happens before first request, check missing env vars or config JSON.
4) If crash is on history fetch, switch to `history-payload-validator`.
5) Restart only after the above checks pass.

## Safe Patterns
- Import pattern:
  ```python
  from datetime import time as dt_time
  import time as time_module
  # use dt_time(9, 15); use time_module.time()
  ```
- Guard market hours:
  ```python
  if not is_market_open():
      logger.info("Market closed; exiting")
      return
  ```
- Validate dependencies at start: raise clear errors if env/config is missing.

## Post-Fix Verification
- Rerun the strategy and ensure logs show:
  - Startup banner
  - Successful history fetch
  - No immediate traceback within the first minute
- Keep tailing logs for 2–3 minutes after restart to confirm stability.
