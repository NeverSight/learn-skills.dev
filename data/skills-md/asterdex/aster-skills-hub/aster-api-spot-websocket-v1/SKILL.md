---
name: aster-api-spot-websocket-v1
description: WebSocket market + user data streams for Aster Spot API v1. Subscription model, stream names, listenKey (/api/v1/listenKey). Use when implementing real-time spot market or user events. listenKey = USER_STREAM; see aster-api-spot-auth-v1.
---

# Aster Spot API WebSocket (v1)

**Base:** wss://sstream.asterdex.com. **Raw:** `/ws/<streamName>`. **Combined:** `/stream?streams=name1/name2/...` → `{"stream":"<name>","data":<payload>}`. Stream names **lowercase** (e.g. btcusdt).

**Limits:** Connection 24h; ping every 5 min → pong within 15 min; 5 msg/s; max 1024 streams.

## Market: subscribe / unsubscribe

JSON: **Subscribe** `{"method":"SUBSCRIBE","params":["btcusdt@aggTrade","btcusdt@depth"],"id":1}` → `{"result":null,"id":1}`. **Unsubscribe:** `UNSUBSCRIBE` + params. **List:** `LIST_SUBSCRIPTIONS`.

## Stream names (market)

| Stream | Description |
|--------|-------------|
| `<symbol>@aggTrade` | Aggregate trades |
| `<symbol>@trade` | Tick-by-tick trades |
| `<symbol>@kline_<interval>` | Kline (e.g. 1m, 1h) |
| `<symbol>@depth`, `@depth@100ms` | Diff. book depth (1000ms or 100ms) |
| `<symbol>@miniTicker` | 24h mini ticker |
| `!miniTicker@arr` | All mini tickers |
| `<symbol>@ticker` | 24h ticker |
| `!ticker@arr` | All tickers |
| `<symbol>@bookTicker` | Best bid/ask |
| `!bookTicker` | All book tickers |

## User data stream (USER_STREAM)

1. **Start:** POST /api/v1/listenKey → `{ "listenKey": "..." }` (existing key extended 60 min). API key in header.
2. **Connect:** wss://sstream.asterdex.com/ws/<listenKey>.
3. **Keepalive:** PUT /api/v1/listenKey with listenKey (e.g. every 30 min).
4. **Close:** DELETE /api/v1/listenKey with listenKey.

**Events:** outboundAccountPosition (balance), executionReport (order update).

## Order book sync (depth)

1. Subscribe to `<symbol>@depth`; buffer events.
2. Snapshot: GET /api/v1/depth?symbol=SYMBOL&limit=1000.
3. Discard events with `u` ≤ lastUpdateId; first valid: `U` ≤ lastUpdateId+1 and `u` ≥ lastUpdateId+1.
4. Each event: `pu` = previous `u`; else re-sync. Qty absolute; 0 = remove level.

Payload shapes: [reference.md](reference.md).
