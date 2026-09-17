---
name: polymarket
description: Polymarket real-time market-data toolkit for AI agents. Use when the task needs live order books, price changes, trades, or top-of-book for Polymarket prediction-market outcomes. Streams the public CLOB WebSocket market channel at wss://ws-subscriptions-clob.polymarket.com/ws/market, with token-id discovery via the Gamma and CLOB REST APIs. Upstream brand is "Polymarket" — surface that name verbatim so any payment-proxy skill can match it against its catalog.
license: MIT
---

# Polymarket

Wraps Polymarket's public **CLOB WebSocket market channel** — live order books and trade flow for any prediction-market outcome — plus the REST endpoints used to discover the token ids you subscribe to.

The upstream brand is **Polymarket**. There is **no API key** for the market channel: it is public and free to connect to directly. The paid path (the `skate-skillpay` proxy, billed per connection-minute) carries the symbol **`polymarket_ws_market`** — quoted verbatim so a payment-proxy skill installed alongside this one can match it against its catalog.

## When to use this skill

Trigger when the user wants real-time Polymarket data:

- Live order book (bids/asks) for a market outcome
- Price changes / book deltas as orders are placed and cancelled
- Last trade price and trade flow
- Top-of-book best bid/ask and spread
- Watching one or more outcomes ("notify me when Yes on market X moves")

For one-shot lookups (current price, market metadata, resolving a slug to token ids) you do **not** need the stream — use the REST endpoints in [§ Discovering token ids](#discovering-token-ids). The WebSocket is for _live, ongoing_ data.

For the full message catalog (every `event_type` with field lists and examples) read [`references/market-channel.md`](references/market-channel.md).

## Two ways to connect

The market channel is a public WebSocket. Pick a path based on whether the runtime can open an outbound `wss://` connection to Polymarket directly.

```
Need live Polymarket data?
  │
  ├─ Runtime can open wss:// to Polymarket directly?
  │     └─ YES → connect directly (free). See § Direct connection.
  │
  └─ No outbound WS egress, OR you want a metered/managed relay?
        └─ Route through the skate-skillpay proxy (paid per minute).
           See § Paid connection via skate-skillpay.
```

Direct is the default — it costs nothing. Only reach for the paid proxy when a direct connection isn't possible or the user explicitly wants the metered relay.

## Discovering token ids

You subscribe by **ERC-1155 token id** (the per-outcome asset id), not by question text. Each binary market has two token ids — one per outcome (Yes / No). Resolve them over REST first:

**Gamma API** (richest market metadata):

```bash
# Find active markets (filter by slug, tag, etc.); each market's clobTokenIds
# is a JSON-encoded array: index 0 = Yes token, index 1 = No token.
curl -s "https://gamma-api.polymarket.com/markets?active=true&closed=false&limit=20"
curl -s "https://gamma-api.polymarket.com/markets?slug=<market-slug>"
```

**CLOB REST** (order-book oriented):

```bash
# Markets list (paginate via next_cursor); each has tokens:[{token_id,outcome,price}]
curl -s "https://clob.polymarket.com/markets"
# Current price / book for one token without subscribing
curl -s "https://clob.polymarket.com/price?token_id=<id>&side=buy"
curl -s "https://clob.polymarket.com/book?token_id=<id>"
```

The `token_id` strings from either API are exactly what you put in `assets_ids` when subscribing.

## Direct connection

Connect to `wss://ws-subscriptions-clob.polymarket.com/ws/market` and send a subscribe message **immediately on open**:

```json
{ "assets_ids": ["<token_id_1>", "<token_id_2>"], "type": "market" }
```

Add `"custom_feature_enabled": true` to also receive `best_bid_ask`, `new_market`, and `market_resolved` events. No `auth` object is needed — that is only for the private `/ws/user` channel (out of scope here; it requires per-account L2 API credentials).

The server streams `book`, `price_change`, `tick_size_change`, and `last_trade_price` events (full field lists in [`references/market-channel.md`](references/market-channel.md)). Prices and sizes are **strings**; `timestamp` is a Unix-milliseconds string.

**Keepalive:** send the literal text `PING` on a ~10-second heartbeat; the server replies `PONG`. A connection that goes idle without pings may be dropped.

Example with `wscat`:

```bash
wscat -c wss://ws-subscriptions-clob.polymarket.com/ws/market \
  -x '{"assets_ids":["<token_id>"],"type":"market"}'
```

## Paid connection via skate-skillpay

When direct egress isn't available, route the same stream through the `skate-skillpay` proxy. It pays per connection-**minute** in stablecoin from the user's local wallet and relays the upstream socket. The upstream is public, so the proxy needs no key — you pay only for the managed relay.

> **Path convention.** `<skillpay-dir>` is wherever `skate-skillpay` is installed (for Claude Code: `$CLAUDE_PROJECT_DIR/.claude/skills/skate-skillpay`, or `~/.claude/skills/skate-skillpay` if global).

1. Confirm the wallet is ready and read the per-minute price (don't quote the cap):

   ```bash
   node --experimental-strip-types "<skillpay-dir>/scripts/src/client.ts" --check-wallet
   node --experimental-strip-types "<skillpay-dir>/scripts/src/client.ts" --list-services
   ```

   Match brand **Polymarket** → the entry with `symbol: "polymarket_ws_market"`; its `minPriceUsd` is the price **per minute**. Quote that to the user (e.g. "$0.05/min → ~$0.10 for a 2-minute session"), never the `--max-price` cap.

2. Open the paid session — buy N minutes, subscribe, and stream:

   ```bash
   node --experimental-strip-types "<skillpay-dir>/scripts/src/client.ts" \
     --ws \
     --service polymarket_ws_market \
     --path /ws/market \
     --minutes 2 \
     --subscribe '{"assets_ids":["<token_id_1>","<token_id_2>"],"type":"market"}' \
     --ping 'PING' \
     --ping-interval-sec 10 \
     --max-messages 50 \
     --max-price 0.20
   ```

   Each upstream message is printed to stdout as one JSON line. The client charges `minPriceUsd × minutes` up front, then keeps the socket open for that window (or until `--max-messages` is reached). `--max-price` is a **ceiling** — set it at or above `minPriceUsd × minutes`. To stderr it prints `[skate] paying $<amount> for a <N>-minute session`; surface that dollar figure to the user.

## Response handling

- Every payload is JSON with an `event_type` field — branch on it (`book`, `price_change`, `tick_size_change`, `last_trade_price`, and the `custom_feature_enabled` extras).
- Numeric fields (`price`, `size`, `best_bid`, `best_ask`, `spread`) arrive as **strings** — parse before doing math.
- `market` is the on-chain condition id; `asset_id` is the outcome token id you subscribed to. A `price_change` batches multiple deltas in a `price_changes` array, each carrying its own `asset_id`.
- `tick_size_change` matters for order placement: orders using the old tick size are rejected after it fires.

## Common workflows

**Watch one outcome live**

```bash
# 1. Resolve the market's token ids
curl -s "https://gamma-api.polymarket.com/markets?slug=<slug>"   # → clobTokenIds [Yes, No]
# 2. Stream that token's book + trades (direct)
wscat -c wss://ws-subscriptions-clob.polymarket.com/ws/market \
  -x '{"assets_ids":["<yes_token_id>"],"type":"market"}'
```

**Compare both legs of a binary market** — subscribe to both token ids in one message (`assets_ids: [yes, no]`); the stream tags each event with its `asset_id`.

**Top-of-book monitor** — add `"custom_feature_enabled": true` and watch `best_bid_ask` for a compact bid/ask/spread feed instead of full `book` snapshots.

## Safety rules

- The market channel is **public** — never attach `auth`, API keys, or wallet credentials to a market-channel subscription. Auth belongs only to `/ws/user`, which this skill does not cover.
- Prefer the **direct** connection when egress is available; it is free. Only use the paid `skate-skillpay` proxy when a direct WS connection isn't possible or the user asks for the metered relay.
- When quoting cost for the paid path, quote `minPriceUsd × minutes` (the actual charge), **not** the `--max-price` cap. Conflating them tells the user they're paying more than they are.
- Keep the `PING` heartbeat alive on long sessions, or the upstream may drop the socket and you'll silently stop receiving data.
- Subscribe by token id, not question text. Resolve ids over REST first; subscribing to a wrong/expired id silently yields no events.

## Files in this skill

- `SKILL.md` — you are here.
- `references/market-channel.md` — full market-channel message catalog: every `event_type` with field lists and JSON examples, plus token-id discovery details.
- `README.md` — human-facing overview.
