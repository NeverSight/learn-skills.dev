---
name: aster-api-trading-v1
description: Place, cancel, batch, countdown-cancel, and query orders for Aster Futures API v1 (/fapi/v1/). Use when placing/canceling orders or querying open/historical. Signed; see aster-api-auth-v1.
---

# Aster API Trading (v1)

**Base:** https://fapi.asterdex.com. Signed (TRADE/USER_DATA). POST/DELETE: body application/x-www-form-urlencoded.

## New order

**POST /fapi/v1/order** (W: 1)

| Parameter | Req | Notes |
|-----------|-----|--------|
| symbol, side, type | Y | side: BUY/SELL; type → see below |
| positionSide | N | BOTH or LONG/SHORT (hedge); req. in Hedge Mode |
| timeInForce | N | GTC, IOC, FOK, GTX, HIDDEN |
| quantity | N | Not with closePosition=true |
| reduceOnly | N | "true"/"false"; not with closePosition/hedge |
| price, stopPrice | N | stopPrice for STOP*/TAKE_PROFIT* |
| closePosition | N | "true"/"false"; STOP_MARKET/TAKE_PROFIT_MARKET only; no quantity/reduceOnly |
| activationPrice, callbackRate | N | TRAILING_STOP_MARKET; callbackRate 0.1–5 (1=1%) |
| workingType | N | MARK_PRICE, CONTRACT_PRICE (default) |
| priceProtect | N | "TRUE"/"FALSE" |
| newClientOrderId | N | Unique; `^[\.A-Z\:/a-z0-9_-]{1,36}$` |
| newOrderRespType | N | ACK (default), RESULT |

**Type-specific required:** LIMIT → timeInForce, quantity, price. MARKET → quantity. STOP/TAKE_PROFIT → quantity, price, stopPrice. STOP_MARKET/TAKE_PROFIT_MARKET → stopPrice. TRAILING_STOP_MARKET → callbackRate.

**Trigger rules:** STOP/STOP_MARKET: BUY → latest ≥ stopPrice; SELL → latest ≤ stopPrice. TAKE_PROFIT/TAKE_PROFIT_MARKET: BUY → latest ≤ stopPrice; SELL → latest ≥ stopPrice. TRAILING_STOP_MARKET: BUY → low ≤ activationPrice and latest ≥ low×(1+callbackRate); SELL → high ≥ activationPrice and latest ≤ high×(1-callbackRate). activationPrice: BUY &lt; latest, SELL &gt; latest (else -2021). closePosition=true: close all long (SELL) or short (BUY); no quantity/reduceOnly; hedge: no BUY for LONG / SELL for SHORT.

## Batch / Cancel / Countdown / Query

- **POST /fapi/v1/batchOrders** (W: 5): `batchOrders` array, max 5; same params as order; responses match order.
- **DELETE /fapi/v1/order** (W: 1): symbol + orderId or origClientOrderId.
- **DELETE /fapi/v1/allOpenOrders** (W: 1): symbol.
- **DELETE /fapi/v1/batchOrders** (W: 1): symbol + orderIdList or origClientOrderIdList (max 10).
- **POST /fapi/v1/countdownCancelAll** (W: 10): symbol, countdownTime (ms). Cancel all at countdown end; 0 = cancel timer. Heartbeat to extend (e.g. 30s with 120000 ms). Checks ~10 ms.
- **GET /fapi/v1/order**, **openOrder** (W: 1): symbol + orderId or origClientOrderId.
- **GET /fapi/v1/openOrders** (W: 1 or 40): symbol optional; no symbol = all (40).
- **GET /fapi/v1/allOrders** (W: 5): symbol req.; orderId, startTime, endTime, limit (500 default, 1000 max). Window &lt; 7 days; orderId → orders ≥ that id. CANCELED/EXPIRED &gt;7d with no fills may be missing.

Payload shapes: [reference.md](reference.md).
