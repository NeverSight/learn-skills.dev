---
name: hyperliquid-websocket
description: Subscribe to live Hyperliquid data over WebSocket from the desk computer - mids, order book, trades, candles, best bid/offer, and per-account fills, order updates and events - with raw JSON, Python SDK and TypeScript examples, plus how to run a supervised watch that logs to a file and alerts. Read-only. Use for monitoring, fill notifications and any watch that polling would make expensive.
license: MIT
metadata:
  version: "1.0.0"
  author: Galleon Labs
  category: hyperliquid
  network-default: testnet
---

# Hyperliquid WebSocket

Read-only, no key. Endpoints: `wss://api.hyperliquid.xyz/ws` (mainnet), `wss://api.hyperliquid-testnet.xyz/ws` (testnet). Prefer WebSocket over polling for anything continuous: fills, order updates, book and price watches.

## Protocol

Subscribe: `{"method": "subscribe", "subscription": {...}}`. Unsubscribe with `"method": "unsubscribe"`. The server acknowledges with `{"channel": "subscriptionResponse", ...}` then streams `{"channel": "<type>", "data": ...}`. Send `{"method": "ping"}` periodically (the SDKs do it for you; the server expects activity within about a minute) and expect `{"channel": "pong"}`.

Subscription types the desk uses:

| Type | Subscription JSON | Data |
| --- | --- | --- |
| Mids for all markets | `{"type":"allMids"}` (optional `"dex"`) | `{"mids": {"BTC": "97123.5", ...}}` |
| Order book | `{"type":"l2Book","coin":"ETH"}` (optional `nSigFigs`, `mantissa`, `fast: true` for 5 levels) | `{"coin","time","levels":[bids,asks]}`, up to 20 levels a side, pushed on each block at least 0.5 s after the last push |
| Trades | `{"type":"trades","coin":"ETH"}` | array of `{coin, side, px, sz, time, hash, tid, users}` |
| Candles | `{"type":"candle","coin":"ETH","interval":"1m"}` | `{t,T,s,i,o,c,h,l,v,n}` updated in place until the bar closes |
| Best bid/offer | `{"type":"bbo","coin":"ETH"}` | `{"coin","time","bbo":[bid, ask]}` |
| Asset context | `{"type":"activeAssetCtx","coin":"ETH"}` | funding, OI, mark, oracle, premium, volume for one market |
| Account fills | `{"type":"userFills","user":"0x..."}` | `{"user","isSnapshot","fills":[...]}` (first message is a snapshot) |
| Order updates | `{"type":"orderUpdates","user":"0x..."}` | array of `{order:{coin,side,limitPx,sz,oid,timestamp,origSz,cloid}, status, statusTimestamp}` |
| Account events | `{"type":"userEvents","user":"0x..."}` | fills, funding, liquidation, non-user cancels; arrives on channel `"user"` |
| Account funding | `{"type":"userFundings","user":"0x..."}` | hourly funding payments |
| Per-market account data | `{"type":"activeAssetData","user":"0x...","coin":"ETH"}` | leverage setting, max trade sizes, available to trade, mark (perps only) |
| Account state stream | `{"type":"clearinghouseState","user":"0x..."}` / `{"type":"openOrders","user":"0x..."}` | `{dex, user, clearinghouseState:{...REST shape...}}` / `{dex, user, orders:[...]}` (order items carry the frontend fields: `isTrigger`, `triggerPx`, `orderType`, `cloid`), pushed |
| TWAP state | `{"type":"twapStates","user":"0x...","dex":""}` / `{"type":"userTwapSliceFills","user":"0x..."}` | running TWAPs and their slice fills |
| Frontend snapshot | `{"type":"webData3","user":"0x..."}` | positions, orders and context in one stream (heavy) |

Limits per IP: up to 10 connections, 30 new connections per minute, 1000 subscriptions, 10 distinct users across user subscriptions, 2000 messages per minute. The server closes a connection silent for 60 seconds. One connection per watch process is plenty.

You can also send `/info` requests over the socket: `{"method":"post","id":1,"request":{"type":"info","payload":{"type":"allMids"}}}` returns `{"channel":"post","data":{"id":1,"response":{...}}}`. Useful inside a watch to avoid mixing REST and WS.

## Python (official SDK)

```python
import os, json, sys, time, signal
from hyperliquid.info import Info
from hyperliquid.utils import constants

NETWORK = os.environ.get("HYPERLIQUID_NETWORK", "testnet")
BASE = constants.MAINNET_API_URL if NETWORK == "mainnet" else constants.TESTNET_API_URL
ADDR = os.environ.get("HYPERLIQUID_ACCOUNT_ADDRESS")
LOG = open("/workspace/trading-desk/watch/ws.log", "a")

def on_msg(msg):
    line = json.dumps({"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "channel": msg.get("channel"), "data": msg.get("data")})
    LOG.write(line + "\n"); LOG.flush()
    if msg.get("channel") == "userFills" and not msg["data"].get("isSnapshot"):
        for f in msg["data"]["fills"]:
            print(f"FILL {f['coin']} {f['side']} {f['sz']} @ {f['px']} fee {f['fee']} oid {f['oid']} cloid {f.get('cloid')}", flush=True)

info = Info(BASE)                                   # skip_ws=False starts the socket thread
info.subscribe({"type": "allMids"}, on_msg)
info.subscribe({"type": "l2Book", "coin": "ETH"}, on_msg)
if ADDR:
    info.subscribe({"type": "userFills", "user": ADDR}, on_msg)
    info.subscribe({"type": "orderUpdates", "user": ADDR}, on_msg)   # one orderUpdates/userEvents subscription per Info

signal.signal(signal.SIGTERM, lambda *_: (info.disconnect_websocket(), sys.exit(0)))
while True:
    time.sleep(60)
```

The SDK's manager pings for you but does **not** reconnect on drop; run it under a supervisor (see below) and treat a silent log as a dead watch. It also only routes these subscription types to your callback: `allMids`, `l2Book`, `trades`, `candle`, `bbo`, `userEvents`, `userFills`, `orderUpdates`, `userFundings`, `userNonFundingLedgerUpdates`, `activeAssetCtx`, `activeAssetData`. Others in the table (`clearinghouseState`, `openOrders`, `twapStates`, `userTwapSliceFills`, `webData3`, `notification`) are acknowledged by the server but silently dropped by the Python SDK; use the raw socket or the TypeScript client for those. The SDK routes one more type, `webData2`, but do not subscribe to it: the live server rejects that frame on mainnet and testnet with `{"channel":"error"}` and the watch never starts. `webData2` survives only as an `/info` request; the frontend snapshot stream is `webData3`, which SDK 0.24.0 cannot route at all.

Run in the background from the desk computer:

```bash
mkdir -p /workspace/trading-desk/watch
nohup python3 /workspace/trading-desk/watch/ws_watch.py >> /workspace/trading-desk/watch/ws_watch.out 2>&1 &
echo $! > /workspace/trading-desk/watch/ws_watch.pid
```

Heartbeat check for a routine: `tail -1 /workspace/trading-desk/watch/ws.log` should be recent; if the pid is gone or the log is stale for more than a few minutes, restart it and note the gap.

## TypeScript (`@nktkas/hyperliquid`)

```ts
import { SubscriptionClient, WebSocketTransport } from "@nktkas/hyperliquid";
const isTestnet = (process.env.HYPERLIQUID_NETWORK ?? "testnet") !== "mainnet";
const transport = new WebSocketTransport({ isTestnet });     // auto-reconnect and re-subscribe by default
const subs = new SubscriptionClient({ transport });
const user = process.env.HYPERLIQUID_ACCOUNT_ADDRESS as `0x${string}`;

await subs.allMids((d) => console.log("mids", d.mids.ETH));
await subs.l2Book({ coin: "ETH" }, (d) => console.log("book", d.levels[0][0], d.levels[1][0]));
await subs.userFills({ user }, (d) => { if (!d.isSnapshot) console.log("fills", d.fills); });
const s = await subs.orderUpdates({ user }, (u) => console.log("orders", u), { onError: (e) => console.error(e) });
// await s.unsubscribe(); transport.close();
```

## Raw (websocat or any client)

```bash
websocat wss://api.hyperliquid-testnet.xyz/ws <<'EOF'
{"method":"subscribe","subscription":{"type":"allMids"}}
EOF
```

## Watch pattern

A watch is a condition plus an alert (`desk-monitoring`). Structure every watch as: subscribe, log everything to a file, evaluate the condition on each message, post the alert once (with value, threshold, source, UTC time), then either exit or keep watching, and never call `/exchange`.

## Pitfalls

- Treating the first `userFills` message as new fills; it is a snapshot (`isSnapshot: true`).
- Candle messages repeat for the open bar; act on bar close (`T` reached) unless you want intrabar updates.
- Spot coins are named `@<index>` on the wire (except a few like `PURR/USDC`); resolve via `spotMeta`.
- Silent disconnects. Log a heartbeat and supervise.
- Running many watches on the shared computer; each is a process. Keep it to what the desk needs.
