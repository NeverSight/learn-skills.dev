---
name: polymarket
description: |
  Full Python SDK for Polymarket prediction markets platform. Use when:
  (1) Trading on Polymarket - placing, cancelling, managing orders
  (2) Researching markets - discovering events, analyzing prices, tracking positions
  (3) Building trading bots - WebSocket streaming, real-time data feeds
  (4) Managing funds - deposits, withdrawals via Bridge API
  (5) Any task involving prediction markets or Polymarket APIs
---

# Polymarket SDK

Async Python SDK for the Polymarket prediction market platform.

## Quick Start

```python
from polymarket import PolymarketClient

async with PolymarketClient() as client:
    # List active markets
    markets = await client.markets.list_markets(active=True, limit=10)
    for market in markets:
        print(f"{market.question}: {market.outcome_prices}")
```

## Installation

```bash
pip install httpx pydantic websockets eth-account
```

Then copy the SDK to your project:
```bash
cp -r scripts/polymarket /path/to/your/project/
```

## Services

| Service | Description | Auth |
|---------|-------------|------|
| `client.markets` | Market discovery, events, metadata | Public |
| `client.orderbook` | Order book, prices, spreads | Public |
| `client.positions` | User positions, analytics | Public |
| `client.bridge` | Deposits, withdrawals | Public |
| `client.orders` | Place/cancel orders | L2 Auth |
| `client.trades` | Trade history | L2 Auth |
| `client.account` | Balance, allowance | L2 Auth |

## Authentication

### Public Endpoints (No Auth)
```python
async with PolymarketClient() as client:
    markets = await client.markets.list_markets()
    book = await client.orderbook.get_book(token_id)
```

### Authenticated Trading
```python
from polymarket import PolymarketClient, Credentials

credentials = Credentials(
    api_key="your-api-key",
    secret="your-secret",
    passphrase="your-passphrase",
)

async with PolymarketClient(
    private_key="0x...",
    credentials=credentials,
) as client:
    # Build and place order
    order = client.order_builder.buy(token_id, price=0.55, size=100).build()
    result = await client.orders.place_order(order)
```

### Creating Credentials
```python
async with PolymarketClient(private_key="0x...") as client:
    credentials = await client.create_api_credentials()
    # Save credentials for future use
```

## Common Workflows

### Search Markets
```python
results = await client.markets.search(query="election", limit_per_type=10)
for event in results.events:
    print(event.title)
```

### Get Prices
```python
spread = await client.orderbook.get_spread(token_id)
print(f"Bid: {spread.bid}, Ask: {spread.ask}")
```

### Check Positions
```python
positions = await client.positions.get_positions(user="0x...")
for pos in positions:
    print(f"{pos.outcome}: {pos.size} @ {pos.avg_price}")
```

### Stream Real-time Data
```python
async with client.market_stream as stream:
    async for event in stream.subscribe([token_id]):
        if isinstance(event, WsPriceChangeMessage):
            print(f"Price: {event.price_changes[0].price}")
```

## Reference Documentation

For detailed information, see:
- [API Quick Reference](references/api-quick-ref.md) - All endpoints
- [Trading Workflows](references/trading-workflows.md) - Order lifecycle, risk management
- [Market Research](references/market-research.md) - Discovery, analysis patterns
- [Authentication](references/authentication.md) - L1/L2 auth flows
- [WebSocket Guide](references/websocket-guide.md) - Real-time streaming

## Examples

Run examples from `assets/examples/`:

```bash
# Discover markets (no auth)
python market_scanner.py

# Track positions (no auth, needs wallet address)
python get_positions.py 0x...

# Stream order book (no auth, needs token ID)
python stream_orderbook.py 71321...

# Place orders (requires POLY_PRIVATE_KEY)
POLY_PRIVATE_KEY=0x... python place_order.py <token_id> BUY 0.55 10
```

## Key Concepts

### Token IDs vs Condition IDs
- **Token ID**: ERC1155 token for a specific outcome (YES/NO)
- **Condition ID**: Market identifier (contains multiple tokens)

### Order Types
- **GTC**: Good-Til-Cancelled
- **GTD**: Good-Til-Date (with expiration)
- **FOK**: Fill-Or-Kill (all or nothing)
- **FAK**: Fill-And-Kill (partial fills OK)

### Signature Types
- **EOA (0)**: MetaMask, hardware wallets
- **POLY_PROXY (1)**: Magic Link users
- **GNOSIS_SAFE (2)**: Most common (default)
