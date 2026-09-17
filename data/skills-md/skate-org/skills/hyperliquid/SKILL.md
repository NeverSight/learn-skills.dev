---
name: hyperliquid
description: Hyperliquid real-time market-data toolkit for AI agents. Use when the task needs live mids, L2 order books, trades, candles, best bid/offer, or account-scoped feeds (fills, orders, funding) from the Hyperliquid perps/spot exchange. Streams the public WebSocket at wss://api.hyperliquid.xyz/ws and can tunnel info/exchange requests over the same socket via the post method. Upstream brand is "Hyperliquid" — surface that name verbatim so any payment-proxy skill can match it against its catalog.
license: MIT
---

# Hyperliquid

Wraps Hyperliquid's **WebSocket API** — live mids, order books, trades, candles, BBO, and account-scoped feeds — plus the `post` method that tunnels `info`/`exchange` requests over the same socket.

The upstream brand is **Hyperliquid**. The public market feeds need **no API key**: the socket is public and free to connect to directly. The paid path (the `skate-skillpay` proxy, billed per connection-minute) carries the symbol **`hyperliquid_ws`** — quoted verbatim so a payment-proxy skill installed alongside this one can match it against its catalog.

## When to use this skill

Trigger when the user wants real-time Hyperliquid data or wants to drive the API over a single socket:

- Live all-mids snapshot across every asset (`allMids`)
- L2 order book for a coin (`l2Book`), best bid/offer (`bbo`)
- Trade prints (`trades`), OHLC candles (`candle`)
- Asset context / mark price / funding (`activeAssetCtx`)
- Account-scoped feeds for a given address — fills, order updates, funding, ledger (`userFills`, `orderUpdates`, `userFundings`, …)
- Tunneling `info` (and signed `exchange`/action) requests over WS via the `post` method

For a single static read (one info query, current mids once) an HTTP `POST https://api.hyperliquid.xyz/info` is simpler than a socket. Use the WebSocket for _live, ongoing_ data or when multiplexing many feeds over one connection.

For the full subscription catalog (every `type`, its fields, and the data-message shapes) read [`references/subscriptions.md`](references/subscriptions.md).

## Two ways to connect

The WebSocket is public. Pick a path based on whether the runtime can open an outbound `wss://` connection to Hyperliquid directly.

```
Need live Hyperliquid data?
  │
  ├─ Runtime can open wss:// to Hyperliquid directly?
  │     └─ YES → connect directly (free). See § Direct connection.
  │
  └─ No outbound WS egress, OR you want a metered/managed relay?
        └─ Route through the skate-skillpay proxy (paid per minute).
           See § Paid connection via skate-skillpay.
```

Direct is the default — it costs nothing. Only reach for the paid proxy when a direct connection isn't possible or the user explicitly wants the metered relay.

## The message envelope

Everything is JSON. Subscribe / unsubscribe:

```json
{ "method": "subscribe",   "subscription": { "type": "trades", "coin": "SOL" } }
{ "method": "unsubscribe", "subscription": { "type": "trades", "coin": "SOL" } }
```

Each successful subscribe is acked with `{ "channel": "subscriptionResponse", "data": { ... } }`. Data messages arrive as `{ "channel": "<type>", "data": <payload> }`.

**Public subscription types** (no address): `allMids`, `l2Book` (`coin`), `trades` (`coin`), `candle` (`coin`, `interval`), `bbo` (`coin`), `activeAssetCtx` (`coin`).

**User-scoped types** (require `"user": "0x…"`): `notification`, `webData2`, `orderUpdates`, `userEvents`, `userFills`, `userFundings`, `userNonFundingLedgerUpdates`, `userTwapSliceFills`, `userTwapHistory`, and `activeAssetData` (also needs `coin`).

Full field lists and example data payloads are in [`references/subscriptions.md`](references/subscriptions.md).

**Keepalive:** the server closes any connection it hasn't _sent_ a message to in the last **60 seconds**. On a quiet subscription, send `{ "method": "ping" }` every ~30s; the server replies `{ "channel": "pong" }`.

## Direct connection

Connect to `wss://api.hyperliquid.xyz/ws` and send subscribe messages:

```bash
wscat -c wss://api.hyperliquid.xyz/ws \
  -x '{"method":"subscribe","subscription":{"type":"l2Book","coin":"BTC"}}'
```

You can send multiple subscribe messages on one connection. Per-IP WS limits: max 10 connections, 1000 subscriptions, 10 unique users across user-scoped subs, 2000 messages/min, 100 inflight `post` messages (see [`references/subscriptions.md`](references/subscriptions.md) § Rate limits).

## Paid connection via skate-skillpay

When direct egress isn't available, route the same stream through the `skate-skillpay` proxy. It pays per connection-**minute** in stablecoin from the user's local wallet and relays the upstream socket. The upstream is public, so the proxy needs no key — you pay only for the managed relay.

> **Path convention.** `<skillpay-dir>` is wherever `skate-skillpay` is installed (for Claude Code: `$CLAUDE_PROJECT_DIR/.claude/skills/skate-skillpay`, or `~/.claude/skills/skate-skillpay` if global).

1. Confirm the wallet is ready and read the per-minute price (don't quote the cap):

   ```bash
   node --experimental-strip-types "<skillpay-dir>/scripts/src/client.ts" --check-wallet
   node --experimental-strip-types "<skillpay-dir>/scripts/src/client.ts" --list-services
   ```

   Match brand **Hyperliquid** → the entry with `symbol: "hyperliquid_ws"`; its `minPriceUsd` is the price **per minute**. Quote that to the user (e.g. "$0.01/min → ~$0.02 for a 2-minute session"), never the `--max-price` cap.

2. Open the paid session — buy N minutes, subscribe, and stream:

   ```bash
   node --experimental-strip-types "<skillpay-dir>/scripts/src/client.ts" \
     --ws \
     --service hyperliquid_ws \
     --path /ws \
     --minutes 2 \
     --subscribe '{"method":"subscribe","subscription":{"type":"allMids"}}' \
     --ping '{"method":"ping"}' \
     --ping-interval-sec 30 \
     --max-messages 50 \
     --max-price 0.05
   ```

   Each upstream message is printed to stdout as one JSON line. Pass `--subscribe` multiple times to open several feeds on one paid session. The client charges `minPriceUsd × minutes` up front, then keeps the socket open for that window (or until `--max-messages` is reached). `--max-price` is a **ceiling** — set it at or above `minPriceUsd × minutes`. To stderr it prints `[skate] paying $<amount> for a <N>-minute session`; surface that dollar figure to the user.

## Driving info/exchange over WS (`post`)

Instead of opening a feed you can tunnel a request over the socket:

```json
{
  "method": "post",
  "id": 1,
  "request": { "type": "info", "payload": { "type": "l2Book", "coin": "BTC" } }
}
```

The reply is `{ "channel": "post", "data": { "id": 1, "response": { "type": "info" | "action" | "error", "payload": { ... } } } }`. Use a unique `id` to correlate; `type: "error"` carries a string mirroring the equivalent HTTP error. `post` messages are subject to Hyperliquid's address-based request weighting, same as the HTTP `info`/`exchange` endpoints.

## Response handling

- Every message is `{ "channel", "data" }`. Branch on `channel`; ignore/await `subscriptionResponse` and `pong` acks.
- Numeric fields (`px`, `sz`, mids, candle OHLC) are typically **strings** — parse before doing math.
- `userEvents` is **not** guaranteed to deliver every event; for authoritative account state use `userFills` / `orderUpdates`.
- For `candle`, intervals are `1m,3m,5m,15m,30m,1h,2h,4h,8h,12h,1d,3d,1w,1M`.

## Common workflows

**Live mids ticker** — subscribe `{"type":"allMids"}`; each `allMids` message carries `data.mids` as a `{ coin: price }` map.

**Single-coin book + trades** — two subscribes on one connection: `{"type":"l2Book","coin":"ETH"}` and `{"type":"trades","coin":"ETH"}`.

**Account monitor** — subscribe `{"type":"userFills","user":"0x…"}` and `{"type":"orderUpdates","user":"0x…"}` for a specific address (the address is public input; no signature needed for read-only feeds).

## Safety rules

- Public feeds need **no credentials**. User-scoped feeds take a plain `user` address (public) and are read-only — never attach private keys or signatures to a subscription. Signing is only needed for `exchange` _actions_ sent via `post`, which is an advanced, account-mutating path — confirm intent with the user before sending one.
- Prefer the **direct** connection when egress is available; it is free. Only use the paid `skate-skillpay` proxy when a direct WS connection isn't possible or the user asks for the metered relay.
- When quoting cost for the paid path, quote `minPriceUsd × minutes` (the actual charge), **not** the `--max-price` cap.
- Keep the `{"method":"ping"}` heartbeat alive (≤60s gaps) or the server will close the socket and you'll silently stop receiving data.
- Respect the per-IP WS limits; opening many connections or blasting subscribes can get the IP throttled.

## Files in this skill

- `SKILL.md` — you are here.
- `references/subscriptions.md` — full subscription catalog (public + user-scoped), data-message shapes, the `post` method, ping/pong, and rate limits.
- `README.md` — human-facing overview.
