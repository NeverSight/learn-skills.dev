---
name: aster-api-spot-trading-v1
description: Place, cancel, and query spot orders for Aster Spot API v1 (/api/v1/). Use when placing/canceling spot orders or querying open/historical. Signed; see aster-api-spot-auth-v1.
---

# Aster Spot API Trading (v1)

**Base:** https://sapi.asterdex.com. Signed (TRADE/USER_DATA). POST/DELETE: body application/x-www-form-urlencoded.

## New order

**POST /api/v1/order** (W: 1)

| Parameter | Req | Notes |
|-----------|-----|--------|
| symbol, side, type | Y | side: BUY/SELL; type → see below |
| timeInForce | N | GTC, IOC, FOK, GTX |
| quantity, quoteOrderQty | N | MARKET BUY: quantity or quoteOrderQty; MARKET SELL: quantity |
| price, stopPrice | N | stopPrice for STOP*, TAKE_PROFIT* |
| newClientOrderId | N | Unique client order ID |
| newOrderRespType | N | ACK, RESULT, FULL |

**Type-specific required:** LIMIT → timeInForce, quantity, price. MARKET → quantity or quoteOrderQty (BUY). STOP/TAKE_PROFIT → quantity, price, stopPrice. STOP_MARKET/TAKE_PROFIT_MARKET → quantity, stopPrice.

**Order types:** LIMIT, MARKET, STOP, TAKE_PROFIT, STOP_MARKET, TAKE_PROFIT_MARKET.

## Cancel / Query

- **DELETE /api/v1/order** (W: 1): symbol + orderId or origClientOrderId.
- **GET /api/v1/order** (W: 1): symbol + orderId or origClientOrderId.
- **GET /api/v1/openOrders** (W: 1 or 40): symbol optional; no symbol = all (40).
- **DELETE /api/v1/allOpenOrders** (W: 1): symbol (required); optional orderIdList or origClientOrderIdList for batch cancel.
- **GET /api/v1/allOrders** (W: 5): symbol req.; orderId, startTime, endTime, limit (500 default, 1000 max). Max range 7 days.

No POST batchOrders (create); batch cancel via allOpenOrders with list params.

Payload shapes: [reference.md](reference.md).
