---
name: aster-api-spot-websocket-v3
description: WebSocket market + user data streams for Aster Spot Testnet API v3. Subscription model, stream names, listenKey (/api/v3/listenKey). Use when implementing real-time spot testnet market or user events. listenKey = signed; see aster-api-spot-auth-v3.
---

# Aster Spot API WebSocket (v3 — Testnet)

**Base:** wss://sstream.asterdex-testnet.com. **Raw:** `/ws/<streamName>`. **Combined:** `/stream?streams=name1/name2/...` → `{"stream":"<name>","data":<payload>}`. Stream names **lowercase** (e.g. asterusdt).

**Limits:** Connection 24h; 5 msg/s; max 1024 streams.

## Market: subscribe / unsubscribe

JSON: **Subscribe** `{"method":"SUBSCRIBE","params":["asterusdt@aggTrade","asterusdt@depth"],"id":1}` → `{"result":null,"id":1}`. **Unsubscribe:** `UNSUBSCRIBE` + params. **List:** `LIST_SUBSCRIPTIONS`.

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

## User data stream (signed)

1. **Start:** POST /api/v3/listenKey (signed: user, signer, nonce, signature) → `{ "listenKey": "..." }`. Extends 60 min if valid key exists.
2. **Connect:** wss://sstream.asterdex-testnet.com/ws/<listenKey>.
3. **Keepalive:** PUT /api/v3/listenKey with listenKey (e.g. every 30 min). Signed.
4. **Close:** DELETE /api/v3/listenKey with listenKey. Signed.

**Events:** outboundAccountPosition (balance), executionReport (order update).

## Order book sync (depth)

1. Subscribe to `<symbol>@depth`; buffer events.
2. Snapshot: GET /api/v3/depth?symbol=SYMBOL&limit=1000.
3. Discard events with `u` ≤ lastUpdateId; first valid: `U` ≤ lastUpdateId+1 and `u` ≥ lastUpdateId+1.
4. Each event: `pu` = previous `u`; else re-sync. Qty absolute; 0 = remove level.

Payload shapes: [reference.md](reference.md).
