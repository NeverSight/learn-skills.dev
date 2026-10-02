---
name: vertex
description: "Vertex Protocol cross-chain DEX — spot trading, perpetual contracts, money markets (lend/borrow), Vertex Edge cross-chain architecture, gas-free trading, Python SDK, WebSocket/REST gateway, subscriptions API, trigger orders, and margin management."
license: Apache-2.0
metadata:
  author: 0xinit
  version: "1.0"
  chain: multichain
  category: Trading
tags:
  - vertex
  - perpetuals
  - spot
  - money-market
  - dex
  - cross-chain
---

# Vertex Protocol

Vertex is a cross-chain DEX combining spot trading, perpetual contracts, and money markets (lend/borrow) under a unified cross-margin portfolio. The off-chain sequencer matches orders in 5-15ms and batches settlements on-chain, providing gas-free trading with MEV protection. Vertex Edge synchronizes orderbook liquidity across Arbitrum, Base, Mantle, Sei, Blast, Sonic, and other EVM chains — trades match cross-chain at the sequencer level and settle on each user's origin chain.

## What You Probably Got Wrong

> LLMs have stale training data. These are the most common mistakes.

- **"Vertex is Arbitrum-only"** → Vertex started on Arbitrum but Vertex Edge now unifies liquidity across Arbitrum, Base, Mantle, Sei, Blast, Sonic, and more. The sequencer aggregates orders cross-chain and settles locally on each origin chain.
- **"Product IDs are just 1, 2, 3"** → Product ID 0 is USDC (the quote asset). Spot products use odd IDs (1=wBTC, 3=wETH, 5=wARB...). Perps use even IDs (2=BTC-PERP, 4=ETH-PERP, 6=ARB-PERP...). Getting this wrong sends orders to the wrong market.
- **"Prices are in float"** → All prices and amounts use fixed-point x18 representation (multiply by 10^18). The SDK provides `to_x18()` and `to_pow_10()` helpers. Passing raw floats produces nonsensical orders.
- **"Signing is standard EIP-712"** → Vertex uses EIP-712 typed data but the `sender` field is `bytes32` — a 20-byte address concatenated with a 12-byte subaccount identifier. The SDK handles this with `subaccount_to_bytes32()`, but raw API callers must construct it correctly.
- **"Gas-free means no wallet interaction"** → You still sign EIP-712 typed data per order. The sequencer batches and submits the on-chain transaction, so you pay no gas — but you must sign every execute action.
- **"Money markets are a separate product"** → Lending/borrowing is embedded. Depositing any spot asset automatically earns interest. Borrowing happens implicitly when your spot balance goes negative (e.g., selling spot you don't hold). There is no separate "borrow" action.
- **`pip install vertex`** → The package name is `vertex-protocol`, not `vertex`. `pip install vertex` installs an unrelated package.
- **"Nonces are sequential"** → Order nonces are NOT sequential counters. Use `gen_order_nonce()` from the SDK — it encodes a timestamp-based random nonce. Using sequential integers causes order rejection.
- **"OrderType.DEFAULT is a market order"** → `OrderType.DEFAULT` is a limit GTC (good-till-cancel) order. For IOC (immediate-or-cancel / market-like), use `OrderType.IOC`. For post-only (maker), use `OrderType.POST_ONLY`.

## Architecture Overview

```
┌──────────────────────────────────────────────────┐
│                  Vertex Edge                      │
│         (Cross-Chain Sequencer Layer)             │
│                                                   │
│   Arbitrum ─┐                                     │
│   Base ─────┤                                     │
│   Mantle ───┼── Unified CLOB ── 5-15ms matching  │
│   Sei ──────┤                                     │
│   Blast ────┤                                     │
│   Sonic ────┘                                     │
│                                                   │
│   ┌─────────────┐  ┌──────────┐  ┌────────────┐  │
│   │ Spot Markets │  │  Perps   │  │Money Market│  │
│   │ (odd IDs)   │  │(even IDs)│  │ (embedded) │  │
│   └─────────────┘  └──────────┘  └────────────┘  │
│                                                   │
│   Cross-Margin Portfolio (unified collateral)     │
└──────────────┬───────────────────────────────────┘
               │ On-chain settlement per origin chain
               ▼
       Smart Contracts (risk engine, clearing)
```

**Key concepts:**

- **Sequencer**: Off-chain CLOB node. Receives signed orders, matches at 5-15ms latency, batches settlement on-chain. Gas costs are absorbed by the protocol.
- **Vertex Edge**: Splits sequencer state across chains. A user on Base and a user on Arbitrum can be matched in the same orderbook. Settlement happens on each user's origin chain.
- **Cross-margin**: All spot deposits, perp positions, and money market balances contribute to a single margin health calculation per subaccount.
- **Subaccounts**: Each wallet can create multiple subaccounts (identified by a 12-byte name appended to the address). Subaccounts isolate margin — a liquidation in one does not affect another.

## Installation

```bash
pip install vertex-protocol
```

Or with uv:

```bash
uv pip install vertex-protocol
```

Verify:

```python
import vertex_protocol
print(vertex_protocol.__version__)
```

## Client Setup

```python
from vertex_protocol.client import create_vertex_client, VertexClientMode

client = create_vertex_client(VertexClientMode.MAINNET, private_key)
```

Available modes:

| Mode | Value | Description |
|------|-------|-------------|
| Mainnet (Arbitrum) | `VertexClientMode.MAINNET` | Production on Arbitrum |
| Testnet | `VertexClientMode.SEPOLIA_TESTNET` | Arbitrum Sepolia testnet |
| Base Mainnet | `VertexClientMode.BASE_MAINNET` | Production on Base |
| Mantle Mainnet | `VertexClientMode.MANTLE_MAINNET` | Production on Mantle |
| Sei Mainnet | `VertexClientMode.SEI_MAINNET` | Production on Sei |
| Blast Mainnet | `VertexClientMode.BLAST_MAINNET` | Production on Blast |
| Sonic Mainnet | `VertexClientMode.SONIC_MAINNET` | Production on Sonic |

## Product ID System

Products are grouped into health groups. Each group pairs a spot asset with its perp market.

| Product ID | Type | Market | Health Group |
|------------|------|--------|-------------|
| 0 | Quote | USDC | — |
| 1 | Spot | wBTC/USDC | BTC |
| 2 | Perp | BTC-PERP | BTC |
| 3 | Spot | wETH/USDC | ETH |
| 4 | Perp | ETH-PERP | ETH |
| 5 | Spot | wARB/USDC | ARB |
| 6 | Perp | ARB-PERP | ARB |
| 7 | Spot | wOP/USDC | OP |
| 8 | Perp | OP-PERP | OP |
| 31 | Spot | wSOL/USDC | SOL |
| 32 | Perp | SOL-PERP | SOL |

**Rule**: Odd IDs = spot, Even IDs = perps, 0 = USDC quote. Query the full list at runtime:

```python
products = client.context.engine_client.get_all_products()
for product in products.spot_products:
    print(f"Spot ID={product.product_id} — {product.book_info}")
for product in products.perp_products:
    print(f"Perp ID={product.product_id} — {product.book_info}")
```

## Utility Functions

Vertex uses x18 fixed-point math. The SDK provides essential helpers:

```python
from vertex_protocol.utils.math import to_x18, to_pow_10, from_x18
from vertex_protocol.utils.nonce import gen_order_nonce
from vertex_protocol.utils.expiration import get_expiration_timestamp, OrderType
from vertex_protocol.utils.subaccount import SubaccountParams, subaccount_to_bytes32

# Price: $2000.50 → x18 representation
price = to_x18(2000.5)

# Amount: 0.1 ETH → integer with 18 decimals
amount = to_pow_10(1, 17)  # 1 * 10^17 = 0.1 * 10^18

# Negative amount = sell
sell_amount = -to_pow_10(1, 17)

# Order nonce — timestamp-based, not sequential
nonce = gen_order_nonce()

# Expiration with order type
import time
expiration = get_expiration_timestamp(
    OrderType.POST_ONLY,
    int(time.time()) + 3600  # 1 hour
)

# Subaccount bytes32
sender = subaccount_to_bytes32(
    SubaccountParams(
        subaccount_owner="0xYourAddress",
        subaccount_name="default"
    )
)
```

## Placing Orders

### Spot Limit Order

```python
import time
from vertex_protocol.engine_client.types.execute import (
    PlaceOrderParams,
    OrderParams,
)
from vertex_protocol.utils.math import to_x18, to_pow_10
from vertex_protocol.utils.nonce import gen_order_nonce
from vertex_protocol.utils.expiration import get_expiration_timestamp, OrderType
from vertex_protocol.utils.subaccount import SubaccountParams

owner = client.context.engine_client.signer.address

order = OrderParams(
    sender=SubaccountParams(
        subaccount_owner=owner,
        subaccount_name="default",
    ),
    priceX18=to_x18(65000),
    amount=to_pow_10(1, 16),  # 0.01 wBTC (positive = buy)
    expiration=get_expiration_timestamp(OrderType.DEFAULT, int(time.time()) + 86400),
    nonce=gen_order_nonce(),
)

res = client.market.place_order(
    PlaceOrderParams(product_id=1, order=order)
)
print(f"Order digest: {res.digest}")
```

### Perp Market Order (IOC)

```python
order = OrderParams(
    sender=SubaccountParams(
        subaccount_owner=owner,
        subaccount_name="default",
    ),
    priceX18=to_x18(70000),  # worst acceptable price (slippage bound)
    amount=-to_pow_10(1, 17),  # -0.1 BTC = short
    expiration=get_expiration_timestamp(OrderType.IOC, int(time.time()) + 60),
    nonce=gen_order_nonce(),
)

res = client.market.place_order(
    PlaceOrderParams(product_id=2, order=order)
)
```

### Cancel Orders

```python
from vertex_protocol.engine_client.types.execute import CancelOrdersParams

res = client.market.cancel_orders(
    CancelOrdersParams(
        sender=SubaccountParams(
            subaccount_owner=owner,
            subaccount_name="default",
        ),
        product_ids=[1, 2],
        digests=["0xorderdigest1...", "0xorderdigest2..."],
        nonce=gen_order_nonce(),
    )
)
```

### Cancel and Replace (Atomic)

```python
from vertex_protocol.engine_client.types.execute import CancelAndPlaceParams

res = client.market.cancel_and_place(
    CancelAndPlaceParams(
        cancel_orders=CancelOrdersParams(
            sender=SubaccountParams(
                subaccount_owner=owner,
                subaccount_name="default",
            ),
            product_ids=[2],
            digests=["0xoldorderdigest..."],
            nonce=gen_order_nonce(),
        ),
        place_order=PlaceOrderParams(
            product_id=2,
            order=OrderParams(
                sender=SubaccountParams(
                    subaccount_owner=owner,
                    subaccount_name="default",
                ),
                priceX18=to_x18(66000),
                amount=to_pow_10(1, 17),
                expiration=get_expiration_timestamp(
                    OrderType.POST_ONLY, int(time.time()) + 3600
                ),
                nonce=gen_order_nonce(),
            ),
        ),
    )
)
```

## Querying Data

### Subaccount Info

```python
from vertex_protocol.utils.subaccount import SubaccountParams

info = client.context.engine_client.get_subaccount_info(
    subaccount=SubaccountParams(
        subaccount_owner=owner,
        subaccount_name="default",
    )
)

print(f"Exists: {info.exists}")
print(f"Health (initial): {info.healths.initial}")
print(f"Health (maintenance): {info.healths.maintenance}")

for balance in info.spot_balances:
    print(f"Spot product {balance.product_id}: {balance.balance}")
for balance in info.perp_balances:
    print(f"Perp product {balance.product_id}: {balance.balance}")
```

### Market Prices

```python
market_price = client.context.engine_client.get_market_price(product_id=2)
print(f"BTC-PERP bid: {market_price.bid}")
print(f"BTC-PERP ask: {market_price.ask}")
```

### All Products

```python
products = client.context.engine_client.get_all_products()
for spot in products.spot_products:
    print(f"ID {spot.product_id}: {spot.book_info}")
```

### Fee Rates

```python
fees = client.context.engine_client.get_fee_rates(
    sender=SubaccountParams(
        subaccount_owner=owner,
        subaccount_name="default",
    )
)
print(f"Maker fee: {fees.maker_fee_rate}")
print(f"Taker fee: {fees.taker_fee_rate}")
```

## Deposits and Withdrawals

### Deposit Collateral

Deposits go through the on-chain Endpoint contract. Approve USDC first, then deposit:

```python
from vertex_protocol.contracts.types import DepositCollateralParams

approve_tx = client.spot.approve_allowance(
    product_id=0,  # USDC
    amount=to_pow_10(1000, 6),  # 1000 USDC (6 decimals on-chain)
)
print(f"Approve tx: {approve_tx}")

deposit_tx = client.spot.deposit(
    DepositCollateralParams(
        subaccount_name="default",
        product_id=0,
        amount=to_pow_10(1000, 6),
    )
)
print(f"Deposit tx: {deposit_tx}")
```

### Withdraw Collateral

Withdrawals are signed executes processed by the sequencer:

```python
from vertex_protocol.engine_client.types.execute import WithdrawCollateralParams

res = client.spot.withdraw(
    WithdrawCollateralParams(
        sender=SubaccountParams(
            subaccount_owner=owner,
            subaccount_name="default",
        ),
        product_id=0,
        amount=to_pow_10(500, 6),
        nonce=gen_order_nonce(),
    )
)
```

## Money Markets (Lend/Borrow)

Lending and borrowing are implicit — no separate actions needed:

- **Lending**: Depositing any spot asset automatically earns the prevailing interest rate. Your idle USDC, wETH, or wBTC generates yield passively.
- **Borrowing**: When your spot balance for an asset goes negative (by selling spot you don't hold, or by explicit borrow), you automatically pay the borrow rate. Your cross-margin health must remain positive.

Check interest rates:

```python
products = client.context.engine_client.get_all_products()
for spot in products.spot_products:
    print(
        f"Product {spot.product_id}: "
        f"deposit APR={spot.product.long_weight_initial}, "
        f"borrow APR={spot.product.short_weight_initial}"
    )
```

## Subscriptions (WebSocket Streams)

Connect to the subscriptions endpoint for real-time data:

```python
import json
import websocket

WS_URL = "wss://gateway.prod.vertexprotocol.com/v1/subscribe"

def on_message(ws, message):
    data = json.loads(message)
    print(data)

def on_open(ws):
    ws.send(json.dumps({
        "method": "subscribe",
        "stream": {
            "type": "best_bid_offer",
            "product_id": 2,
        },
    }))

ws = websocket.WebSocketApp(
    WS_URL,
    on_message=on_message,
    on_open=on_open,
)
ws.run_forever()
```

Available stream types:

| Stream Type | Fields | Description |
|-------------|--------|-------------|
| `best_bid_offer` | `product_id` | Top of book bid/ask |
| `trade` | `product_id` | Executed trades |
| `book_depth` | `product_id` | Full orderbook snapshot |
| `fill` | `product_id`, `subaccount` | Your order fills |
| `position_change` | `subaccount` | Position updates |
| `order_update` | `product_id`, `subaccount` | Order status changes |

## Trigger Orders (Stop Loss / Take Profit)

Trigger orders are submitted to a separate trigger endpoint and execute when price conditions are met:

```python
import requests
import json

TRIGGER_URL = "https://trigger.prod.vertexprotocol.com/v1"

trigger_payload = {
    "place_order": {
        "product_id": 2,
        "order": {
            "sender": sender_bytes32,
            "priceX18": str(to_x18(60000)),
            "amount": str(-to_pow_10(1, 17)),  # sell 0.1 BTC
            "expiration": str(get_expiration_timestamp(
                OrderType.DEFAULT, int(time.time()) + 86400 * 30
            )),
            "nonce": str(gen_order_nonce()),
        },
        "trigger": {
            "price_above": None,
            "price_below": str(to_x18(62000)),  # trigger when price drops below 62k
        },
        "signature": "0x...",  # EIP-712 signature
    }
}

resp = requests.post(
    f"{TRIGGER_URL}/execute",
    json=trigger_payload,
    headers={"Content-Type": "application/json"},
)
print(resp.json())
```

## Indexer (Historical Data)

The archive/indexer API provides historical data not available from the gateway:

```python
matches = client.context.indexer_client.get_matches(
    subaccount=SubaccountParams(
        subaccount_owner=owner,
        subaccount_name="default",
    ),
    product_ids=[2, 4],
    limit=50,
)

for match in matches:
    print(f"Product {match.product_id}: {match.order.amount} @ {match.order.price}")
```

Available indexer queries:

| Method | Description |
|--------|-------------|
| `get_matches` | Historical fills for a subaccount |
| `get_orders` | Historical orders placed |
| `get_funding_rate` | 24h funding rate for perp products |
| `get_interest_and_funding_payments` | Interest/funding payment history |
| `get_linked_signer` | Current linked signer for a subaccount |
| `get_subaccounts` | List all subaccounts for a wallet |
| `get_rewards` | Trading rewards earned |
| `get_candlesticks` | OHLCV candle data |

## Linked Signers

A linked signer is a secondary key authorized to sign on behalf of your subaccount. Useful for bot trading — keep your main key in cold storage and link a hot key with rate limits:

```python
from vertex_protocol.engine_client.types.execute import LinkSignerParams

res = client.context.engine_client.link_signer(
    LinkSignerParams(
        sender=SubaccountParams(
            subaccount_owner=owner,
            subaccount_name="default",
        ),
        signer=SubaccountParams(
            subaccount_owner="0xHotWalletAddress",
            subaccount_name="default",
        ),
        nonce=gen_order_nonce(),
    )
)
```

## API Endpoints Reference

### Arbitrum (Mainnet)

| Service | URL |
|---------|-----|
| Gateway REST | `https://gateway.prod.vertexprotocol.com/v1` |
| Gateway WebSocket | `wss://gateway.prod.vertexprotocol.com/v1/ws` |
| Subscriptions | `wss://gateway.prod.vertexprotocol.com/v1/subscribe` |
| Indexer/Archive | `https://archive.prod.vertexprotocol.com/v1` |
| Trigger | `https://trigger.prod.vertexprotocol.com/v1` |

### Base

| Service | URL |
|---------|-----|
| Gateway REST | `https://gateway.base-prod.vertexprotocol.com/v1` |
| Gateway WebSocket | `wss://gateway.base-prod.vertexprotocol.com/v1/ws` |
| Subscriptions | `wss://gateway.base-prod.vertexprotocol.com/v1/subscribe` |
| Indexer/Archive | `https://archive.base-prod.vertexprotocol.com/v1` |
| Trigger | `https://trigger.base-prod.vertexprotocol.com/v1` |

### Testnet (Sepolia)

| Service | URL |
|---------|-----|
| Gateway REST | `https://gateway.sepolia-test.vertexprotocol.com/v1` |
| Gateway WebSocket | `wss://gateway.sepolia-test.vertexprotocol.com/v1/ws` |
| Subscriptions | `wss://gateway.sepolia-test.vertexprotocol.com/v1/subscribe` |
| Indexer/Archive | `https://archive.sepolia-test.vertexprotocol.com/v1` |
| Trigger | `https://trigger.sepolia-test.vertexprotocol.com/v1` |

## Common Patterns

### Check Health Before Trading

```python
info = client.context.engine_client.get_subaccount_info(
    subaccount=SubaccountParams(
        subaccount_owner=owner,
        subaccount_name="default",
    )
)

initial_health = float(info.healths.initial.health)
if initial_health < 0:
    print("Account unhealthy — reduce positions or add collateral")
```

### Poll for Order Fill

```python
import time

digest = res.digest

for _ in range(30):
    order = client.context.engine_client.get_order(
        product_id=2,
        digest=digest,
    )
    if order.status == "filled":
        print("Order filled")
        break
    time.sleep(1)
```

### Multi-Subaccount Isolation

```python
hedge_sub = SubaccountParams(subaccount_owner=owner, subaccount_name="hedge")
spec_sub = SubaccountParams(subaccount_owner=owner, subaccount_name="spec")
```

## Resources

- [Vertex Documentation](https://docs.vertexprotocol.com/)
- [Python SDK Docs](https://vertex-protocol.github.io/vertex-python-sdk/)
- [Python SDK GitHub](https://github.com/vertex-protocol/vertex-python-sdk)
- [TypeScript SDK GitHub](https://github.com/vertex-protocol/vertex-typescript-sdk)
- [Vertex Edge Blog Post](https://blog.vertexprotocol.com/vertex-edge-a-unichain-for-perps/)
- [API Gateway Docs](https://docs.vertexprotocol.com/developer-resources/api/gateway)
