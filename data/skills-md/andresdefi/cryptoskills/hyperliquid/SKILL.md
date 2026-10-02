---
name: hyperliquid
description: "Hyperliquid perpetual futures DEX — order placement (market/limit/trigger/TWAP), position management, leverage up to 50x, WebSocket streaming, vault strategies, and L1 architecture. REST and WebSocket APIs with wallet signing authentication. Python SDK and TypeScript patterns."
license: Apache-2.0
metadata:
  author: 0xinit
  version: "1.0"
  chain: multichain
  category: Trading
tags:
  - hyperliquid
  - perpetuals
  - futures
  - dex
  - trading
---

# Hyperliquid

Hyperliquid is a perpetual futures DEX running on its own L1 blockchain (HyperBFT consensus). It provides fully on-chain order book matching with sub-second finality, up to 50x leverage on perpetual contracts, and a spot DEX. The API uses EIP-712 wallet signing for authentication — there are no API keys. All trading actions are cryptographically signed by your wallet or an approved agent wallet.

Base URLs:
- **Mainnet**: `https://api.hyperliquid.xyz`
- **Testnet**: `https://api.hyperliquid-testnet.xyz`
- **WebSocket Mainnet**: `wss://api.hyperliquid.xyz/ws`
- **WebSocket Testnet**: `wss://api.hyperliquid-testnet.xyz/ws`

## What You Probably Got Wrong

> LLMs have stale training data. These are the most common mistakes.

- **"Hyperliquid uses API keys"** → There are no API keys. Every exchange action is an EIP-712 signed message from your wallet. You can approve "agent wallets" for automated trading, but the auth mechanism is always wallet signatures — never bearer tokens or API secrets.
- **"Use chain ID 1 or the Arbitrum chain ID for signing"** → L1 trading actions (orders, cancels, leverage changes) use chain ID `1337` with a "phantom agent" signing scheme. User-signed actions (agent approval, withdrawals) use chain ID `421614`. Getting this wrong produces `User or API Wallet does not exist` errors with no further explanation.
- **"Prices and sizes are numbers"** → All prices and sizes in the Exchange API are **strings**, not numbers. Sending `"p": 50000` instead of `"p": "50000"` will fail silently or produce incorrect signatures.
- **"Asset IDs are coin symbols"** → The Exchange API uses integer asset indices, not symbols. BTC might be `0`, ETH might be `1`. Query the `meta` endpoint to get the current universe mapping. Spot assets use `10000 + index`.
- **"I can place a $1 order"** → Minimum order notional is $10 for perpetuals. Orders below this are rejected with `Order must have minimum value of $10`.
- **"Rate limit is per-endpoint"** → Rate limiting is per-address across all endpoints: 1200 requests/minute base. Trading volume increases your cap. Stale `expiresAfter` cancellations consume 5x the normal weight.
- **"The Python SDK uses async"** → The official `hyperliquid-python-sdk` is synchronous. It uses `requests` under the hood. For async, use a community SDK or build your own with `aiohttp`.
- **"WebSocket subscriptions auto-reconnect"** → They do not. You must implement reconnection logic. Missed data during disconnection is not replayed — use the Info REST API to backfill.

## L1 Architecture

Hyperliquid runs its own L1 with HyperBFT consensus (modified HotStuff). Key properties:

- **Block time**: ~400ms
- **Finality**: Single-slot (sub-second)
- **Throughput**: 100,000+ orders/second
- **Settlement**: Fully on-chain order matching (not off-chain with on-chain settlement)
- **Bridge**: Native bridge to Arbitrum for USDC deposits/withdrawals (~5 min, $1 fee)
- **HyperEVM**: EVM-compatible execution layer for smart contracts alongside the native DEX

All positions, orders, and liquidations execute on the L1. The API is a gateway to this L1 — not a centralized matching engine.

## Authentication: EIP-712 Signing

Hyperliquid uses two signing schemes:

### L1 Actions (Trading)

Used for: orders, cancels, leverage changes, margin transfers.

- Chain ID: `1337`
- Signing scheme: **Phantom Agent** — the action is hashed, then a phantom agent struct is signed
- The wallet never signs the raw order; it signs a derived message

### User-Signed Actions (Account)

Used for: agent wallet approval, withdrawals, USD transfers.

- Chain ID: `421614` (Arbitrum Sepolia)
- Signing scheme: Direct EIP-712 with the action payload

### Agent Wallets

You can approve up to 4 agent wallets per account (1 unnamed + 3 named) for automated trading. Agent wallets sign L1 actions on behalf of the master account.

```python
from hyperliquid.exchange import Exchange
from hyperliquid.utils import constants
from eth_account import Account

wallet = Account.from_key("0x...")
exchange = Exchange(wallet, constants.MAINNET_API_URL)

# Approve an agent wallet for automated trading
approve_result = exchange.approve_agent(agent_address="0xAGENT_ADDRESS", agent_name="my-bot")
```

## Info API (Public Data — No Auth Required)

All Info requests are `POST https://api.hyperliquid.xyz/info` with a JSON body containing `type`.

### Market Metadata

```python
import requests

url = "https://api.hyperliquid.xyz/info"

# Universe: list of all perpetual markets with asset indices
meta = requests.post(url, json={"type": "meta"}).json()
for i, asset in enumerate(meta["universe"]):
    print(f"Asset {i}: {asset['name']} — maxLeverage: {asset['maxLeverage']}")
```

### Mid Prices

```python
mids = requests.post(url, json={"type": "allMids"}).json()
btc_mid = mids["BTC"]
eth_mid = mids["ETH"]
```

### L2 Order Book

```python
book = requests.post(url, json={
    "type": "l2Book",
    "coin": "BTC",
    "nSigFigs": 5
}).json()

for level in book["levels"][0][:5]:  # top 5 bids
    print(f"Bid: {level['px']} x {level['sz']}")
for level in book["levels"][1][:5]:  # top 5 asks
    print(f"Ask: {level['px']} x {level['sz']}")
```

### Candle Data

```python
import time

candles = requests.post(url, json={
    "type": "candleSnapshot",
    "req": {
        "coin": "ETH",
        "interval": "1h",
        "startTime": int(time.time() * 1000) - 86400000,
        "endTime": int(time.time() * 1000)
    }
}).json()
# Returns up to 5000 candles: T, o, h, l, c, v, n
```

### User State (Positions + Margin)

```python
state = requests.post(url, json={
    "type": "clearinghouseState",
    "user": "0xYOUR_ADDRESS"
}).json()

margin_summary = state["marginSummary"]
print(f"Account value: {margin_summary['accountValue']}")
print(f"Total margin used: {margin_summary['totalMarginUsed']}")

for pos in state["assetPositions"]:
    p = pos["position"]
    print(f"{p['coin']}: size={p['szi']} entry={p['entryPx']} unrealizedPnl={p['unrealizedPnl']}")
```

### Open Orders

```python
orders = requests.post(url, json={
    "type": "frontendOpenOrders",
    "user": "0xYOUR_ADDRESS"
}).json()

for o in orders:
    print(f"{o['coin']} {o['side']} {o['sz']}@{o['limitPx']} oid={o['oid']}")
```

### Funding Rates

```python
predicted = requests.post(url, json={"type": "predictedFundings"}).json()

history = requests.post(url, json={
    "type": "fundingHistory",
    "coin": "BTC",
    "startTime": int(time.time() * 1000) - 86400000
}).json()
```

### User Rate Limit

```python
rate = requests.post(url, json={
    "type": "userRateLimit",
    "user": "0xYOUR_ADDRESS"
}).json()
# nRequestsUsed, nRequestsCap, nRequestsSurplus, cumVlm
```

## Exchange API (Orders — Requires Signing)

All Exchange requests go to `POST https://api.hyperliquid.xyz/exchange` with a signed payload.

### Python SDK Setup

```bash
pip install hyperliquid-python-sdk
```

```python
from hyperliquid.info import Info
from hyperliquid.exchange import Exchange
from hyperliquid.utils import constants
from eth_account import Account

wallet = Account.from_key("0xYOUR_PRIVATE_KEY")
info = Info(constants.MAINNET_API_URL, skip_ws=True)
exchange = Exchange(wallet, constants.MAINNET_API_URL)
```

### Place a Limit Order

```python
result = exchange.order(
    name="ETH",
    is_buy=True,
    sz=0.1,
    limit_px=3000.0,
    order_type={"limit": {"tif": "Gtc"}},
    reduce_only=False
)
print(result)
# {"status": "ok", "response": {"type": "order", "data": {"statuses": [{"resting": {"oid": 123456}}]}}}
```

### Place a Market Order

```python
# market_open uses IOC with slippage tolerance (default 5%)
result = exchange.market_open(
    name="BTC",
    is_buy=True,
    sz=0.01,
    slippage=0.03  # 3% slippage tolerance
)
```

### Place a Trigger Order (Stop-Loss / Take-Profit)

```python
# Stop-loss: sell if price drops to 2800
result = exchange.order(
    name="ETH",
    is_buy=False,
    sz=0.1,
    limit_px=2790.0,  # limit price after trigger
    order_type={"trigger": {
        "triggerPx": "2800",
        "isMarket": True,  # execute as market when triggered
        "tpsl": "sl"       # "sl" for stop-loss, "tp" for take-profit
    }},
    reduce_only=True
)
```

### Batch Orders

```python
orders = [
    {
        "name": "BTC",
        "is_buy": True,
        "sz": 0.01,
        "limit_px": 95000.0,
        "order_type": {"limit": {"tif": "Gtc"}},
        "reduce_only": False
    },
    {
        "name": "ETH",
        "is_buy": True,
        "sz": 0.1,
        "limit_px": 3000.0,
        "order_type": {"limit": {"tif": "Gtc"}},
        "reduce_only": False
    }
]
result = exchange.bulk_orders(orders)
```

### TWAP Orders

```python
# TWAP: execute large order over time to minimize impact
result = exchange.twap_order(
    name="BTC",
    is_buy=True,
    sz=1.0,
    reduce_only=False,
    minutes=30,      # execute over 30 minutes
    randomize=True   # randomize slice timing
)

# Cancel a running TWAP
exchange.twap_cancel(twap_id=12345)
```

### Cancel Orders

```python
# Cancel by order ID
exchange.cancel(name="ETH", oid=123456)

# Cancel by client order ID
exchange.cancel_by_cloid(name="ETH", cloid="0x00000000000000000000000000000001")
```

### Schedule Cancel (Dead Man's Switch)

Cancels all open orders if no heartbeat received within the timeout. Minimum 5-second delay, maximum 10 triggers per day.

```python
import time

result = exchange.schedule_cancel(time=int(time.time() * 1000) + 30000)  # 30s from now
```

## Position Management

### Set Leverage

```python
# Cross leverage
exchange.update_leverage(name="BTC", leverage=10, is_cross=True)

# Isolated leverage
exchange.update_leverage(name="ETH", leverage=20, is_cross=False)
```

### Adjust Isolated Margin

```python
# Add margin to isolated position (positive = add, negative = remove)
exchange.update_isolated_margin(name="ETH", amount=100.0)
```

### Close Position

```python
# Market close entire position
exchange.market_close(name="BTC")

# Or close with a limit order
state = info.user_state("0xYOUR_ADDRESS")
for pos in state["assetPositions"]:
    p = pos["position"]
    if p["coin"] == "ETH":
        size = abs(float(p["szi"]))
        is_long = float(p["szi"]) > 0
        exchange.order(
            name="ETH",
            is_buy=not is_long,
            sz=size,
            limit_px=float(p["entryPx"]) * (1.01 if is_long else 0.99),
            order_type={"limit": {"tif": "Gtc"}},
            reduce_only=True
        )
```

## WebSocket Streaming

Connect to `wss://api.hyperliquid.xyz/ws` and send JSON subscription messages.

### Available Channels

| Channel | Params | Description |
|---------|--------|-------------|
| `allMids` | `dex` (optional) | All mid prices, real-time |
| `l2Book` | `coin` | L2 orderbook updates |
| `trades` | `coin` | Trade prints |
| `candle` | `coin`, `interval` | Candle updates |
| `bbo` | `coin` | Best bid/offer |
| `orderUpdates` | `user` | Order status changes |
| `userEvents` | `user` | All user events |
| `userFills` | `user` | Fill notifications |
| `userFundings` | `user` | Funding payments |
| `clearinghouseState` | `user`, `dex` | Position updates |
| `openOrders` | `user`, `dex` | Open order changes |
| `activeAssetCtx` | `coin` | Market context (funding, OI) |
| `twapStates` | `user`, `dex` | TWAP order progress |

### Subscribe/Unsubscribe Pattern

```json
{"method": "subscribe", "subscription": {"type": "trades", "coin": "BTC"}}
{"method": "subscribe", "subscription": {"type": "l2Book", "coin": "ETH"}}
{"method": "subscribe", "subscription": {"type": "userFills", "user": "0xYOUR_ADDRESS"}}
{"method": "unsubscribe", "subscription": {"type": "trades", "coin": "BTC"}}
```

### Python WebSocket Example

```python
import json
import websocket
import threading

def on_message(ws, message):
    data = json.loads(message)
    channel = data.get("channel")
    if channel == "trades":
        for trade in data["data"]:
            print(f"{trade['coin']} {trade['side']} {trade['sz']}@{trade['px']}")
    elif channel == "l2Book":
        book = data["data"]
        best_bid = book["levels"][0][0] if book["levels"][0] else None
        best_ask = book["levels"][1][0] if book["levels"][1] else None
        if best_bid and best_ask:
            print(f"BBO: {best_bid['px']} / {best_ask['px']}")

def on_open(ws):
    ws.send(json.dumps({
        "method": "subscribe",
        "subscription": {"type": "trades", "coin": "BTC"}
    }))
    ws.send(json.dumps({
        "method": "subscribe",
        "subscription": {"type": "l2Book", "coin": "BTC"}
    }))

def on_error(ws, error):
    print(f"WebSocket error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("WebSocket closed, reconnecting...")
    threading.Timer(5.0, connect).start()

def connect():
    ws = websocket.WebSocketApp(
        "wss://api.hyperliquid.xyz/ws",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever()

connect()
```

## Rate Limits

| Metric | Limit |
|--------|-------|
| Base request cap | 1200/minute per address |
| Weight per request | 1 (standard) |
| Stale `expiresAfter` cancel | 5x weight |
| Volume bonus | Higher trading volume increases cap |
| Burst | No documented burst limit — sustained rate |

Check your current usage:

```python
rate = requests.post("https://api.hyperliquid.xyz/info", json={
    "type": "userRateLimit",
    "user": "0xYOUR_ADDRESS"
}).json()
print(f"Used: {rate['nRequestsUsed']}/{rate['nRequestsCap']}")
```

You can reserve additional rate limit capacity at 0.0005 USDC per request via the `requestWeightReservation` exchange action.

## Vault Strategies

Vaults are on-chain managed accounts. A vault leader trades with depositors' funds and takes a profit share.

```python
# Deposit into a vault
exchange.vault_transfer(
    vault_address="0xVAULT_ADDRESS",
    is_deposit=True,
    usd=1000.0
)

# Query vault details
vault = requests.post("https://api.hyperliquid.xyz/info", json={
    "type": "vaultDetails",
    "vaultAddress": "0xVAULT_ADDRESS"
}).json()
print(f"TVL: {vault['summary']['tvl']}")
print(f"APR: {vault['summary']['apr']}")
```

Vault leaders trade by passing `vault_address` to exchange methods — the master account signs on behalf of the vault.

## Subaccounts

Subaccounts are separate trading accounts under a master wallet. They have their own positions and margin but no private key — the master account signs for them.

```python
# Create a subaccount
exchange.create_sub_account(name="arb-bot")

# Transfer USDC to subaccount
exchange.sub_account_transfer(
    sub_account_user="0xSUB_ADDRESS",
    is_deposit=True,
    usd=5000.0
)

# Query subaccounts
subs = requests.post("https://api.hyperliquid.xyz/info", json={
    "type": "subAccounts",
    "user": "0xMASTER_ADDRESS"
}).json()
```

## Liquidation Mechanics

- **Maintenance margin**: Varies by asset tier. Positions are liquidated when account margin drops below maintenance requirement.
- **Margin tiers**: Larger positions require more margin. A 10x BTC position has lower maintenance margin than a 50x one.
- **Liquidation price**: Visible via `clearinghouseState` — check `liquidationPx` on each position.
- **Insurance fund**: Backstops liquidations that cannot be filled at the bankruptcy price.
- **ADL (Auto-Deleveraging)**: Last resort when insurance fund is depleted. Profitable positions are reduced proportionally.

```python
state = info.user_state("0xYOUR_ADDRESS")
for pos in state["assetPositions"]:
    p = pos["position"]
    if p.get("liquidationPx"):
        print(f"{p['coin']}: liquidation at {p['liquidationPx']}")
```

## TypeScript Signing Pattern

For TypeScript integrations, use `ethers` or `viem` for EIP-712 signing. The SDK `@nktkas/hyperliquid` provides a typed client.

```typescript
import { privateKeyToAccount } from "viem/accounts";
import { type Hex, hashTypedData, signTypedData } from "viem";

const account = privateKeyToAccount(process.env.PRIVATE_KEY as Hex);

const EXCHANGE_URL = "https://api.hyperliquid.xyz/exchange";
const INFO_URL = "https://api.hyperliquid.xyz/info";

async function queryInfo(body: Record<string, unknown>): Promise<unknown> {
  const res = await fetch(INFO_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  return res.json();
}

// Info endpoints require no authentication
const meta = await queryInfo({ type: "meta" }) as { universe: Array<{ name: string }> };
const assetIndex = meta.universe.findIndex((a) => a.name === "ETH");
```

## Key Differences from CEX APIs

| Feature | CEX (Binance/Bybit) | Hyperliquid |
|---------|---------------------|-------------|
| Auth | API key + secret | EIP-712 wallet signature |
| Order ID | Server-assigned | OID + optional client order ID (CLOID) |
| Asset reference | Symbol string | Integer index from `meta` |
| Price/size format | Number | String |
| Rate limit | Per-endpoint | Per-address, all endpoints |
| Settlement | Database updates | On-chain L1 transactions |
| Withdrawals | Centralized | Bridge to Arbitrum (~5 min) |

## Official Resources

- **Docs**: https://hyperliquid.gitbook.io/hyperliquid-docs/
- **Python SDK**: https://github.com/hyperliquid-dex/hyperliquid-python-sdk
- **TypeScript SDK**: https://github.com/nktkas/hyperliquid
- **App**: https://app.hyperliquid.xyz
- **Testnet**: https://app.hyperliquid-testnet.xyz
- **Stats**: https://stats.hyperliquid.xyz
