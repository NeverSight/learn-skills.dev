---
name: orderly-websocket-streaming
description: Establish authenticated WebSocket connections for real-time orderbook, execution reports, positions, and balance updates
---

# Orderly Network: WebSocket Streaming

This skill covers establishing WebSocket connections, authentication, and subscribing to real-time data streams on Orderly Network.

## When to Use

- Building real-time trading interfaces
- Streaming orderbook data
- Receiving execution notifications
- Monitoring position updates

## Prerequisites

- Orderly account ID
- Ed25519 private key for signing
- WebSocket client library (native WebSocket, socket.io, etc.)

## WebSocket Endpoints

| Environment     | URL                                                                          |
| --------------- | ---------------------------------------------------------------------------- |
| Mainnet Public  | `wss://ws.orderly.org/ws/stream`                                             |
| Mainnet Private | `wss://ws-private-evm.orderly.org/v2/ws/private/stream/{account_id}`         |
| Testnet Public  | `wss://testnet-ws.orderly.org/ws/stream`                                     |
| Testnet Private | `wss://testnet-ws-private-evm.orderly.org/v2/ws/private/stream/{account_id}` |

## Connection Flow

```
1. Connect to WebSocket endpoint
2. Authenticate (for private streams)
3. Subscribe to topics
4. Receive real-time messages
5. Handle reconnection/heartbeat
```

## Public Streams (No Authentication)

### Connect and Subscribe

```typescript
const ws = new WebSocket('wss://ws.orderly.org/ws/stream');

ws.onopen = () => {
  // Subscribe to orderbook
  ws.send(
    JSON.stringify({
      id: 'sub_ob_1',
      event: 'subscribe',
      topic: 'PERP_ETH_USDC@orderbook',
    })
  );

  // Subscribe to trades
  ws.send(
    JSON.stringify({
      id: 'sub_trades_1',
      event: 'subscribe',
      topic: 'PERP_ETH_USDC@trade',
    })
  );

  // Subscribe to 24h ticker
  ws.send(
    JSON.stringify({
      id: 'sub_ticker_1',
      event: 'subscribe',
      topic: 'PERP_ETH_USDC@24hrTicker',
    })
  );
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
};
```

### Available Public Topics

| Topic                       | Description              |
| --------------------------- | ------------------------ |
| `{symbol}@orderbook`        | Full orderbook snapshot  |
| `{symbol}@orderbookupdate`  | Incremental updates      |
| `{symbol}@trade`            | Trade executions         |
| `{symbol}@kline_{interval}` | Kline/candlestick data   |
| `{symbol}@markprice`        | Mark price updates       |
| `{symbol}@indexprice`       | Index price updates      |
| `{symbol}@24hrTicker`       | 24h statistics           |
| `markprice`                 | All symbols mark prices  |
| `indexprice`                | All symbols index prices |

### Orderbook Stream

```typescript
interface OrderbookMessage {
  topic: string;
  ts: number;           // Timestamp
  data: {
    asks: [string, string][];  // [price, quantity]
    bids: [string, string][];
    prevTs: number;      // Previous timestamp for sequencing
  };
}

// Subscribe
{ "event": "subscribe", "topic": "PERP_ETH_USDC@orderbookupdate" }

// Maintain local orderbook
let orderbook = { asks: [], bids: [] };

ws.onmessage = (event) => {
  const msg = JSON.parse(event.data);

  if (msg.topic?.includes('orderbookupdate')) {
    // Apply incremental updates
    for (const [price, qty] of msg.data.asks) {
      updateLevel(orderbook.asks, price, qty);
    }
    for (const [price, qty] of msg.data.bids) {
      updateLevel(orderbook.bids, price, qty);
    }
  }
};

function updateLevel(levels: [string, string][], price: string, qty: string) {
  const idx = levels.findIndex(l => l[0] === price);
  if (qty === '0') {
    // Remove level
    if (idx !== -1) levels.splice(idx, 1);
  } else {
    // Update or insert
    if (idx !== -1) {
      levels[idx] = [price, qty];
    } else {
      levels.push([price, qty]);
      // Sort (asks ascending, bids descending)
      levels.sort((a, b) => parseFloat(a[0]) - parseFloat(b[0]));
    }
  }
}
```

### Kline Stream

```typescript
// Available intervals: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M

ws.send(JSON.stringify({
  id: 'sub_kline',
  event: 'subscribe',
  topic: 'PERP_ETH_USDC@kline_1m',
}));

// Message format
{
  "topic": "PERP_ETH_USDC@kline_1m",
  "ts": 1699123456789,
  "data": {
    "t": 1699123440000,  // Kline start time
    "o": "3000.00",      // Open
    "h": "3010.00",      // High
    "l": "2995.00",      // Low
    "c": "3005.00",      // Close
    "v": "123.45",       // Volume
    "qv": "370350.00"    // Quote volume
  }
}
```

## Private Streams (Authentication Required)

### Authentication

```typescript
import { signAsync } from '@noble/ed25519';

const accountId = 'your_account_id';
const privateKey = new Uint8Array(32); // Your Ed25519 private key

const ws = new WebSocket(`wss://ws-private-evm.orderly.org/v2/ws/private/stream/${accountId}`);

ws.onopen = async () => {
  const timestamp = Date.now();
  const message = timestamp.toString();

  const signature = await signAsync(new TextEncoder().encode(message), privateKey);

  // Encode as base64url (browser & Node.js compatible)
  const base64 = btoa(String.fromCharCode(...signature));
  const base64url = base64.replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');

  // Send authentication
  ws.send(
    JSON.stringify({
      id: 'auth_1',
      event: 'auth',
      params: {
        orderly_key: `ed25519:${publicKeyBase58}`,
        sign: base64url,
        timestamp: timestamp,
      },
    })
  );
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);

  if (data.event === 'auth' && data.success) {
    console.log('Authenticated successfully');
    // Now subscribe to private topics
    subscribePrivateTopics();
  }
};
```

### Private Topics

| Topic                 | Description            |
| --------------------- | ---------------------- |
| `executionreport`     | Order status updates   |
| `position`            | Position changes       |
| `balance`             | Balance updates        |
| `liquidationsaccount` | Liquidation warnings   |
| `wallet`              | Wallet/deposit updates |
| `account`             | Account updates        |
| `settle`              | Settlement updates     |
| `notifications`       | General notifications  |

### Execution Report Stream

```typescript
function subscribePrivateTopics() {
  // Subscribe to order updates
  ws.send(
    JSON.stringify({
      id: 'sub_exec',
      event: 'subscribe',
      topic: 'executionreport',
      // Optional: filter by symbol
      params: { symbol: 'PERP_ETH_USDC' },
    })
  );
}

// Message format
interface ExecutionReport {
  topic: 'executionreport';
  ts: number;
  data: {
    orderId: string;
    clientOrderId?: string;
    symbol: string;
    side: 'BUY' | 'SELL';
    orderType: string;
    status: 'NEW' | 'PARTIAL_FILLED' | 'FILLED' | 'CANCELLED' | 'REJECTED';
    price: string;
    quantity: string;
    executedQty: string;
    avgPrice?: string;
    leavesQty: string;
    lastExecutedPrice?: string;
    lastExecutedQty?: string;
    fee?: string;
    feeToken?: string;
    reason?: string;
  };
}
```

### Position Stream

```typescript
ws.send(JSON.stringify({
  id: 'sub_position',
  event: 'subscribe',
  topic: 'position',
}));

// Message format
{
  "topic": "position",
  "ts": 1699123456789,
  "data": {
    "symbol": "PERP_ETH_USDC",
    "positionQty": 0.5,
    "averageOpenPrice": 3000,
    "markPrice": 3100,
    "unrealizedPnl": 50,
    "leverage": 10,
    "liqPrice": 2700,
    "mmr": 0.01,
    "imr": 0.02
  }
}
```

### Balance Stream

```typescript
ws.send(JSON.stringify({
  id: 'sub_balance',
  event: 'subscribe',
  topic: 'balance',
}));

// Message format
{
  "topic": "balance",
  "ts": 1699123456789,
  "data": {
    "token": "USDC",
    "total": "10000.00",
    "free": "8000.00",
    "locked": "2000.00",
    "unsettledPnl": "500.00"
  }
}
```

## React SDK: Built-in Streaming

The Orderly SDK handles WebSocket connections automatically:

```typescript
import {
  useOrderbookStream,
  usePositionStream,
  useOrderStream,
  useBalance
} from '@orderly.network/hooks';

function TradingInterface({ symbol }: { symbol: string }) {
  // Orderbook - automatically connects to WebSocket
  const { asks, bids } = useOrderbookStream(symbol);

  // Positions - real-time updates
  const { rows: positions } = usePositionStream();

  // Orders - real-time updates
  const [orders] = useOrderStream({ status: OrderStatus.INCOMPLETE });

  // Balance
  const balance = useBalance();

  return (
    <div>
      <OrderbookWidget asks={asks} bids={bids} />
      <PositionsTable positions={positions} />
      <OrdersTable orders={orders} />
      <BalanceDisplay balance={balance} />
    </div>
  );
}
```

## Connection Management

### Heartbeat

```typescript
// Orderly sends ping, you respond with pong
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);

  if (data.event === 'ping') {
    ws.send(JSON.stringify({ event: 'pong' }));
  }
};

// Or use native WebSocket ping/pong
ws.onopen = () => {
  // Some clients need explicit ping
  setInterval(() => {
    if (ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ event: 'ping' }));
    }
  }, 30000);
};
```

### Reconnection

```typescript
class OrderlyWebSocket {
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private subscriptions: string[] = [];

  connect() {
    this.ws = new WebSocket(this.url);

    this.ws.onopen = () => {
      this.reconnectAttempts = 0;
      this.authenticate();
      this.resubscribe();
    };

    this.ws.onclose = () => {
      if (this.reconnectAttempts < this.maxReconnectAttempts) {
        setTimeout(
          () => {
            this.reconnectAttempts++;
            this.connect();
          },
          Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000)
        );
      }
    };
  }

  private resubscribe() {
    for (const topic of this.subscriptions) {
      this.ws?.send(
        JSON.stringify({
          event: 'subscribe',
          topic,
        })
      );
    }
  }

  subscribe(topic: string) {
    this.subscriptions.push(topic);
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(
        JSON.stringify({
          event: 'subscribe',
          topic,
        })
      );
    }
  }
}
```

## Error Handling

```typescript
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);

  if (data.success === false) {
    console.error('WebSocket error:', data.errorMsg);

    switch (data.errorMsg) {
      case 'invalid symbol':
        // Handle invalid symbol
        break;
      case 'authentication failed':
        // Re-authenticate
        break;
      case 'rate limit exceeded':
        // Slow down subscription requests
        break;
    }
  }
};

// Error response format
{
  "id": "sub_ob_1",
  "event": "subscribe",
  "success": false,
  "errorMsg": "invalid symbol"
}
```

## Rate Limits

| Action                       | Limit |
| ---------------------------- | ----- |
| Subscriptions per connection | 100   |
| Messages per second          | 50    |
| Connection per IP            | 10    |

## Common Issues

### "Authentication failed" error

- Check timestamp is current (not future/past)
- Verify signature encoding (base64url)
- Ensure orderly_key format is `ed25519:{publicKey}`

### Connection drops frequently

- Implement heartbeat/pong
- Check network stability
- Use reconnection logic

### Missing messages

- Check if subscription was successful
- Verify topic name format
- Monitor for error messages

### Orderbook out of sync

- Use `prevTs` to detect missed messages
- Re-subscribe to get fresh snapshot
- Implement sequence validation

## Related Skills

- **orderly-api-authentication** - Ed25519 signing details
- **orderly-trading-orders** - Order management
- **orderly-positions-tpsl** - Position monitoring
- **orderly-sdk-react-hooks** - SDK streaming hooks
