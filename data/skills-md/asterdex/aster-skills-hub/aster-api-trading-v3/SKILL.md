---
name: aster-api-trading-v3
description: Place, cancel, batch, and query orders for Aster Futures API v3 (/fapi/v3/). Use when placing/canceling orders or querying open/historical. Signed; see aster-api-auth-v3.
---

# Aster API Trading

**Base:** https://fapi.asterdex.com. Signed (TRADE/USER_DATA). POST/DELETE: body application/x-www-form-urlencoded.

## New order

**POST /fapi/v3/order** (Weight: 1)

| Parameter | Req | Notes |
|-----------|-----|--------|
| symbol, side, type | Y | side: BUY/SELL; type → see below |
| positionSide | N | BOTH or LONG/SHORT (hedge); req. in Hedge Mode |
| timeInForce | N | GTC, IOC, FOK, GTX |
| quantity, reduceOnly | N | Not with closePosition; reduceOnly not in hedge |
| price, stopPrice | N | stopPrice for STOP*/TAKE_PROFIT* |
| closePosition | N | STOP_MARKET/TAKE_PROFIT_MARKET only; no quantity/reduceOnly |
| activationPrice, callbackRate | N | TRAILING_STOP_MARKET; callbackRate 0.1–5 (1=1%) |
| workingType, priceProtect | N | MARK_PRICE/CONTRACT_PRICE; "TRUE"/"FALSE" |
| newClientOrderId | N | Unique; `^[\.A-Z\:/a-z0-9_-]{1,36}$` |
| newOrderRespType | N | ACK (default), RESULT |

**Type-specific required:** LIMIT → timeInForce, quantity, price. MARKET → quantity. STOP/TAKE_PROFIT → quantity, price, stopPrice. STOP_MARKET/TAKE_PROFIT_MARKET → stopPrice. TRAILING_STOP_MARKET → callbackRate.

**Trigger rules:** STOP/STOP_MARKET: BUY → latest ≥ stopPrice; SELL → latest ≤ stopPrice. TAKE_PROFIT/TAKE_PROFIT_MARKET: opposite. TRAILING_STOP_MARKET: BUY → low ≤ activationPrice and latest ≥ low×(1+callbackRate); SELL → high ≥ activationPrice and latest ≤ high×(1-callbackRate). activationPrice: BUY &lt; latest, SELL &gt; latest (else -2021). closePosition=true: close all long (SELL) or short (BUY); hedge: no BUY for LONG / SELL for SHORT.

## Batch / Cancel / Query

- **POST /fapi/v3/batchOrders** (W: 5): `batchOrders` max 5; responses match order.
- **DELETE /fapi/v3/order** (W: 1): symbol + orderId or origClientOrderId.
- **DELETE /fapi/v3/allOpenOrders** (W: 1): symbol.
- **DELETE /fapi/v3/batchOrders** (W: 1): symbol + orderIdList or origClientOrderIdList (max 10).
- **GET /fapi/v3/order**, **openOrder** (W: 1): symbol + orderId or origClientOrderId.
- **GET /fapi/v3/openOrders** (W: 1 or 40): symbol optional; no symbol = all (40).
- **GET /fapi/v3/allOrders** (W: 5): symbol req.; orderId, startTime, endTime, limit (500 default, 1000 max). Window &lt; 7 days. CANCELED/EXPIRED &gt;7d no fills may be missing.

Payload shapes: [reference.md](reference.md).
