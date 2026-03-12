---
name: aster-api-websocket-v1
description: WebSocket market + user data streams for Aster Futures API v1. Subscription model, stream names, listenKey (/fapi/v1/listenKey). Use when implementing real-time market or user events (orders, balance, positions). listenKey = signed; see aster-api-auth-v1.
---

# Aster API WebSocket (v1)

**Base:** wss://fstream.asterdex.com. **Raw:** `/ws/<streamName>`. **Combined:** `/stream?streams=name1/name2/...` → `{"stream":"<name>","data":<payload>}`. Stream names **lowercase** (e.g. btcusdt).

**Limits:** Connection 24h; ping every 5 min → pong within 15 min; 10 msg/s; max 200 streams.

## Market: subscribe / unsubscribe

JSON: **Subscribe** `{"method":"SUBSCRIBE","params":["btcusdt@aggTrade","btcusdt@depth"],"id":1}` → `{"result":null,"id":1}`. **Unsubscribe:** `UNSUBSCRIBE` + params. **List:** `LIST_SUBSCRIPTIONS`. `id` = unsigned int.

## Stream names (market)

| Stream | Description |
|--------|-------------|
| `<symbol>@aggTrade` | Aggregate trades (100ms) |
| `<symbol>@depth` | Diff. book depth (250/500/100ms: `@depth@500ms`, `@depth@100ms`) |
| `<symbol>@depth5`, `@depth10`, `@depth20` | Partial book depth |
| `<symbol>@kline_<interval>` | Kline (e.g. 1m, 1h); interval as in REST |
| `<symbol>@markPrice`, `<symbol>@markPrice@1s` | Mark price (3s or 1s) |
| `!markPrice@arr`, `!markPrice@arr@1s` | All symbols mark price |
| `<symbol>@miniTicker` | 24h mini ticker (500ms) |
| `!miniTicker@arr` | All mini tickers (1000ms) |
| `<symbol>@ticker` | 24h ticker (500ms) |
| `!ticker@arr` | All tickers (1000ms) |
| `<symbol>@bookTicker` | Best bid/ask (real-time) |
| `!bookTicker` | All book tickers |
| `<symbol>@forceOrder` | Liquidation snapshot (1000ms) |
| `!forceOrder@arr` | All liquidations |

## User data stream (signed)

1. **Start:** POST /fapi/v1/listenKey → `{ "listenKey": "..." }` (existing key extended 60 min).
2. **Connect:** wss://fstream.asterdex.com/ws/<listenKey>.
3. **Keepalive:** PUT /fapi/v1/listenKey &lt;60 min (e.g. 30 min).
4. **Close:** DELETE /fapi/v1/listenKey.

Events not guaranteed in order; use `E` for ordering. **Events:** ACCOUNT_UPDATE, ORDER_TRADE_UPDATE, ACCOUNT_CONFIG_UPDATE, MARGIN_CALL, listenKeyExpired.

## Order book sync (depth)

1. Connect to `btcusdt@depth`; buffer events.
2. Snapshot: GET /fapi/v1/depth?symbol=BTCUSDT&limit=1000.
3. Drop events with `u` &lt; lastUpdateId; first valid: `U` ≤ lastUpdateId and `u` ≥ lastUpdateId.
4. Each event: `pu` = previous `u`; else re-sync from step 2. Qty absolute; 0 = remove level.

Payload shapes: [reference.md](reference.md).
