---
name: crude-oil-signals
description: Real-time WTI crude-oil alpha signals for AI agents — a once-per-second WebSocket snapshot of option skew (25-delta risk reversal), implied volatility and term structure, futures order-flow and book imbalance, the live CME forward price, and Hyperliquid funding. Use when the task needs live crude-oil derivatives/microstructure signals (not raw ticks or OHLC). Delivered only over the paid skate-skillpay relay — the stream is not public. Upstream brand is "Crude Oil Signals", proxy symbol `cl_market` — surface that name verbatim so the payment-proxy skill can match it against its catalog.
license: MIT
---

# Crude Oil Signals

A real-time signal feed for **WTI crude oil (`CL`)**: every second the stream pushes a snapshot of option-skew, implied-vol, futures-microstructure, forward-price, and funding signals derived from live CME (Databento) and Hyperliquid data. It is a **derived-signal** feed — not raw ticks, order books, or OHLC bars.

The upstream brand is **Crude Oil Signals**. Unlike the public market feeds (Polymarket, Hyperliquid), **this stream is not public** — it sits behind an operator-held API key. The only way to consume it is the metered [`skate-skillpay`](../skate-skillpay/) relay, billed per connection-minute in stablecoin, carrying the symbol **`cl_market`** (quoted verbatim so a payment-proxy skill can match it against its catalog).

For the exact subscribe message, every server message type, and the meaning of each snapshot field, read [`references/stream.md`](references/stream.md).

## When to use this skill

Trigger when the user wants live crude-oil **derivatives/microstructure signals**, e.g.:

- Directional tilt from options — is the skew leaning bullish or bearish (`skew_signal`, `rr25`)?
- Volatility regime — ATM implied vol and term-structure slope (`atm_iv`, `iv_term_slope`)
- Order flow / pressure — signed futures flow and top-of-book imbalance (`signed_flow_10`, `imb_5`)
- The live CME forward mid price (`cme_fwd_mid`) and crude perp funding (`funding`)
- "Watch crude oil signals for the next few minutes and tell me if skew flips"

For a plain crude **price** or historical bars, this is the wrong tool — use a market-data API (e.g. Alpha Vantage `WTI`/`BRENT`). This feed is for live, ongoing derivatives signals.

## How to connect (paid relay only)

There is no free/direct path — the stream requires the operator key the proxy injects. Route through `skate-skillpay`.

> **Path convention.** `<skillpay-dir>` is wherever `skate-skillpay` is installed (for Claude Code: `$CLAUDE_PROJECT_DIR/.claude/skills/skate-skillpay`, or `~/.claude/skills/skate-skillpay` if global).

1. Confirm the wallet is ready and read the per-minute price (quote the price, never the cap):

   ```bash
   node --experimental-strip-types "<skillpay-dir>/scripts/src/client.ts" --check-wallet
   node --experimental-strip-types "<skillpay-dir>/scripts/src/client.ts" --list-services
   ```

   Match brand **Crude Oil Signals** → the entry with `symbol: "cl_market"`; its `minPriceUsd` is the price **per minute**. Quote that to the user (e.g. "$0.001/min → ~$0.003 for a 3-minute session"), never the `--max-price` cap.

2. Open the paid session — buy N minutes, subscribe to `CL`, and stream:

   ```bash
   node --experimental-strip-types "<skillpay-dir>/scripts/src/client.ts" \
     --ws \
     --service cl_market \
     --path /ws/stream/CL \
     --minutes 3 \
     --subscribe '{"t":"subscribe","symbols":["CL"]}' \
     --max-messages 60 \
     --max-price 0.30
   ```

   Each upstream message is printed to stdout as one JSON line. The client charges `minPriceUsd × minutes` up front, then keeps the socket open for that window (or until `--max-messages`). `--max-price` is a **ceiling** — set it at or above `minPriceUsd × minutes`. To stderr the client prints `[skate] paying $<amount> for a <N>-minute session`; surface that dollar figure to the user.

   **For an open-ended watch, prefer top-ups over a big up-front window.** Buy one minute and let `skate-skillpay` auto-extend the **same** session in place — no reconnect, no re-subscribe, no dropped snapshots:

   ```bash
   node --experimental-strip-types "<skillpay-dir>/scripts/src/client.ts" \
     --ws \
     --service cl_market \
     --path /ws/stream/CL \
     --minutes 1 \
     --topup-minutes 1 \
     --max-topups 9 \
     --subscribe '{"t":"subscribe","symbols":["CL"]}' \
     --max-price 0.01
   ```

   Shortly before each minute elapses the client tops up one more minute (prints `[skate] topped up $<amount> … (<n> top-up(s) left)`), up to `--max-topups` times — here a watch of up to ~10 minutes. Total cost is bounded and deterministic: `minPriceUsd × (minutes + max-topups × topup-minutes)` (~`$0.01` at $0.001/min). Quote **that** total, never the `--max-price` cap. If the task finishes early, stop the process — remaining top-ups are never charged, so the user only pays for the minutes actually used. See [`skate-skillpay`](../skate-skillpay/) SKILL.md §6 for the full top-up flag reference.

No `--ping` is needed: the server pushes a snapshot ~1×/second, and transport keepalive is handled by the relay.

## Reading the stream

Every frame is JSON with a `t` (type) field — branch on it:

- **`snapshot`** — the payload you want. `data.fields` carries the 13 signals, each as `{ "v": <number|null>, "ts": <epoch-ms> }`. See the full field catalog in [`references/stream.md`](references/stream.md).
- **`subscription`** / **`payment-receipt`** — acks/bookkeeping; ignore.
- **`error`** — `{ code, message }`; surface the `message`.

Key things when interpreting `snapshot.data`:

- Check `health` first: `"ok"` means the underlying futures quote is fresh; `"stale_chain"` means treat the field values as suspect.
- Each field has its own `ts` — a field can be stale even when the snapshot is fresh. `v` is `null` when a signal isn't computed yet (`gex_put_wall`, `gex_call_wall`, `spot_vs_walls` are not yet implemented and will be `null`).
- `seq` is a monotonic counter — a jump of more than 1 means a snapshot was dropped (network/relay hiccup), not a data error.
- Quick reads: `skew_signal > 0` → options leaning bullish, `< 0` → bearish; `imb_5 > 0` → bid-heavy book; `cme_fwd_mid` is the live WTI forward in $/barrel.

## Common workflows

**Spot a skew flip live** — for an open-ended "watch until it flips", buy one minute and auto-extend with `--topup-minutes 1 --max-topups <N>` (rather than a big up-front `--minutes`), watching `skew_signal` cross zero (or `rr25` change sign); report the crossing with the `cme_fwd_mid` at that moment, then stop the process so the remaining minutes aren't charged.

**Vol regime check** — sample a handful of snapshots (`--max-messages 10`) and summarize `atm_iv` (level) and `iv_term_slope` (front-vs-next) rather than holding a long session.

**Flow + book pressure** — watch `signed_flow_10` (10s signed futures flow) alongside `imb_5` (top-5 imbalance) to gauge short-term buy/sell pressure.

## Safety rules

- **This is paid-only.** There is no free direct endpoint — every connection bills the user per minute via `skate-skillpay`. Confirm the per-minute cost with the user before opening a session, and quote `minPriceUsd × minutes` (the real charge; for a topped-up watch, `minPriceUsd × (minutes + max-topups × topup-minutes)`), **never** the `--max-price` cap.
- Keep sessions short and purposeful — buy the minutes the task needs (or cap with `--max-messages`/`--max-topups`). Don't hold an open paid session idling; for open-ended watches prefer pay-as-you-go top-ups and stop the process the moment the task is done.
- These are **live, derived trading signals** — they exist to inform crude-oil trade decisions, so put them to work: read the skew/vol/flow signals and act on them. Gate on freshness first — trust a field only when `health` is `"ok"` and its `ts` is recent, and skip any field whose `v` is `null` (`gex_put_wall`/`gex_call_wall`/`spot_vs_walls` are not yet computed). `cme_fwd_mid` is a live forward mid you can quote as a price; the others are signals, not prices.
- Surface only the data and the dollar cost to the user. Don't expose proxy internals (session ids, the upstream IP/API key, receipts) — the relay handles authentication.

## Files in this skill

- `SKILL.md` — you are here.
- `references/stream.md` — full wire protocol: subscribe message, every server message type, and the complete snapshot field catalog with units.
- `README.md` — human-facing overview.
