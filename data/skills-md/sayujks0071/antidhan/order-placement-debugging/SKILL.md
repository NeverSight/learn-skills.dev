---
name: order-placement-debugging
description: Debug "no orders placed" and OpenAlgo placesmartorder API failures. Use when strategies signal but orders don't reach the broker, when seeing Order API / JSON parse errors, or when fixing or verifying smart-order integration.
---

# Order Placement Debugging

Systematic approach to fixing strategies that log entry/exit signals but do not place orders, or that hit OpenAlgo smart-order API errors. Use with the **order-placement-debugger** subagent and debug-mode workflow (hypotheses → instrument → reproduce → analyze → fix → verify).

## When to Use

- Strategy logs show `SIGNAL:` or `[ENTRY]`/`[EXIT]` but "Order ID: N/A" or no order ID
- Logs show: `Order API Error: Expecting value: line 1 column 1 (char 0)` or `TradingUtils - ERROR`
- HTTP log shows `POST .../smartorder "HTTP/1.1 200 OK"` but no order in order book
- Adding or fixing `placesmartorder` / `APIClient` in a strategy

## OpenAlgo Smart Order API (Reference)

### Endpoint

| Correct | Wrong |
|--------|--------|
| `POST {host}/api/v1/placesmartorder` | `POST {host}/api/v1/smartorder` |

Namespace in app: `path="/placesmartorder"` → full path is `/api/v1/placesmartorder`.

### Request Payload (Required Fields)

| Field | Type | Example | Notes |
|-------|------|--------|--------|
| `apikey` | string | OpenAlgo API key | Required |
| `strategy` | string | Strategy name | Required |
| `symbol` | string | e.g. GOLDM05FEB26FUT | Required |
| `action` | string | BUY, SELL | Required (not `transaction_type`) |
| `exchange` | string | MCX, NSE, NFO | Required |
| `pricetype` | string | MARKET, LIMIT, SL, SL-M | Required (not `order_type`) |
| `product` | string | MIS, CNC, NRML | Required |
| `quantity` | string | "1" | Required; send as string |
| `position_size` | string | "1" | Required; send as string |
| `price` | string | "0" | Optional in API docs but often expected |
| `trigger_price` | string | "0" | Optional |
| `disclosed_quantity` | string | "0" | Optional |

### Success Response (200)

```json
{ "orderid": "2016727642073505792", "status": "success" }
```

### Common Client-Side Bugs

1. **Wrong URL**  
   Using `/api/v1/smartorder` → server may return 200 with empty or non-JSON body → `response.json()` raises "Expecting value: line 1 column 1".

2. **Wrong payload keys**  
   - `transaction_type` → must be `action`  
   - `order_type` → must be `pricetype`

3. **Missing fields**  
   Omit `price`, `trigger_price`, `disclosed_quantity` → set to `"0"` if server expects them.

4. **Wrong types**  
   Sending `quantity`/`position_size` as int → send as string (e.g. `str(quantity)`).

5. **No handling for non-JSON 200**  
   Calling `response.json()` on 200 without try/except → on empty/HTML response, catch `ValueError`, log, and return a safe dict (e.g. `{"status": "success", "message": "Order placed (non-JSON response)"}` or similar) so strategy does not treat the call as a hard failure.

## Code Locations

| What | Where |
|------|--------|
| Client implementation | `openalgo/strategies/utils/trading_utils.py` → `APIClient.placesmartorder()` |
| Strategy usage | `openalgo/strategies/scripts/*.py` (e.g. `mcx_global_arbitrage_strategy.py`) |
| Server route | `openalgo/restx_api/__init__.py` → `path="/placesmartorder"` |
| Server handler | `openalgo/restx_api/place_smart_order.py` |
| Schema/docs | `openalgo/restx_api/schemas.py` (SmartOrderSchema), `openalgo/docs/userguide/12-smart-orders/README.md` |

## Hypotheses to Test (With Runtime Evidence)

Use instrumentation (e.g. NDJSON to `.cursor/debug.log`) to confirm or reject:

| Id | Hypothesis | What to log | Confirmed if |
|----|-------------|-------------|----------------|
| A | API client not passed or not initialized | In strategy `__init__`: `has_api_client`, `host` | Log shows `has_api_client: false` or missing host |
| B | `entry()` only logs, doesn’t call order API | Start of `entry()`: `side`, `price`, `has_api_client` | No "Attempting order placement" after "entry() called" |
| C | `exit()` only logs, doesn’t call order API | Start of `exit()`: `side`, `price`, `has_api_client` | No "Attempting exit order placement" after "exit() called" |
| D | Wrong endpoint or payload | In `placesmartorder()`: `url`, payload keys | URL is `/smartorder` or payload has `transaction_type`/`order_type` |
| E | Response not JSON or empty | After `httpx.post`: `status_code`, `content_type`, `content_length`; then parse | `content_type` not JSON or `response.json()` raises |

## Fix Checklist (trading_utils.py)

- [ ] URL is `f"{self.host}/api/v1/placesmartorder"`.
- [ ] Payload uses `action` (not `transaction_type`), `pricetype` (not `order_type`).
- [ ] Payload includes `price`, `trigger_price`, `disclosed_quantity` (e.g. `"0"`).
- [ ] `quantity` and `position_size` sent as strings.
- [ ] On 200, try `response.json()`; on `ValueError`, do not crash—log and return a safe dict.
- [ ] On non-200, log `response.text` and return error dict.
- [ ] On exception (e.g. timeout), log and return error dict.

## Verification

1. **Minimal test script**  
   Create a script that instantiates `APIClient(api_key=..., host=...)` and calls `placesmartorder(...)` with valid args. Run it and check:
   - Log: "Order Placed" with a real `orderid`.
   - No "Order API Error" or JSON decode error.

2. **Strategy run**  
   Run the strategy until it generates a signal; check strategy log for `[ENTRY]` or `[EXIT]` with a real order ID.

3. **Debug log**  
   If using NDJSON instrumentation, confirm entries for "Response parsed as JSON" and `has_orderid: true` / `status: "success"`.

## Related

- **Subagent:** `order-placement-debugger` — use for full workflow and evidence-based fixes.
- **Skills:** `trading-operations` (server/strategy status), `log-monitoring` (finding entries/errors in logs), `trading-strategy-development` (strategy structure).
- **Docs:** `openalgo/docs/userguide/12-smart-orders/README.md`, `openalgo/docs/api/order-management/placesmartorder.md`.

## Resolved Case (2026-01-29)

**Symptom:** MCX Global Arbitrage strategy logged signals and "Order placed" but "Order ID: N/A"; log showed `Order API Error: Expecting value: line 1 column 1 (char 0)`.

**Root cause:** `placesmartorder()` in `trading_utils.py` used wrong endpoint (`/api/v1/smartorder`), wrong payload keys (`transaction_type`, `order_type`), missing fields, and called `response.json()` on 200 without handling non-JSON body.

**Fix:** Switched to `/api/v1/placesmartorder`, payload with `action`, `pricetype`, `price`/`trigger_price`/`disclosed_quantity` as `"0"`, string `quantity`/`position_size`, and safe handling of non-JSON 200 response.

**Verification:** Test script called `placesmartorder`; response contained `orderid` and `status: "success"`. Debug log showed "Response parsed as JSON", `has_orderid: true`.
