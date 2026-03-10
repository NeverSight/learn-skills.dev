---
name: orderly-trading-orders
description: Place, manage, and cancel orders using REST API or SDK hooks. Covers market, limit, IOC, FOK, POST_ONLY order types and batch operations
---

# Orderly Network: Trading Orders

This skill covers all aspects of order management on Orderly Network - placing, modifying, and canceling orders through REST API and React SDK.

## When to Use

- Building a trading interface
- Implementing order placement logic
- Managing order lifecycle
- Creating automated trading bots

## Prerequisites

- Orderly account registered
- Ed25519 API key with `trading` scope
- Sufficient collateral in account

## Order Types

| Type        | Description                     | Use Case                |
| ----------- | ------------------------------- | ----------------------- |
| `LIMIT`     | Order at specific price         | Precise entry/exit      |
| `MARKET`    | Execute at best available price | Immediate execution     |
| `IOC`       | Immediate-or-Cancel             | Partial fill acceptable |
| `FOK`       | Fill-or-Kill                    | All or nothing          |
| `POST_ONLY` | Maker-only order                | Earn maker rebates      |
| `ASK`       | Best ask price guaranteed       | Quick sell              |
| `BID`       | Best bid price guaranteed       | Quick buy               |

## REST API: Place Order

### Endpoint

```
POST /v1/order
```

### Request Body

```typescript
interface OrderRequest {
  symbol: string; // e.g., "PERP_ETH_USDC"
  side: 'BUY' | 'SELL';
  order_type: 'LIMIT' | 'MARKET' | 'IOC' | 'FOK' | 'POST_ONLY' | 'ASK' | 'BID';
  order_price?: number; // Required for LIMIT orders
  order_quantity: number; // Base asset quantity
  visible_quantity?: number; // For hidden orders (0 = hidden)
  client_order_id?: string; // Your custom ID
  trigger_price?: string; // For stop orders
}
```

### Example

```typescript
import { signAsync } from '@noble/ed25519';

async function placeOrder(order: OrderRequest) {
  const timestamp = Date.now();
  const body = JSON.stringify(order);
  const message = `${timestamp}POST/v1/order${body}`;

  const signature = await signAsync(new TextEncoder().encode(message), privateKey);

  // Encode as base64url (browser & Node.js compatible)
  const base64 = btoa(String.fromCharCode(...signature));
  const base64url = base64.replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');

  const response = await fetch('https://api.orderly.org/v1/order', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'orderly-timestamp': String(timestamp),
      'orderly-account-id': accountId,
      'orderly-key': `ed25519:${publicKeyBase58}`,
      'orderly-signature': base64url,
    },
    body,
  });

  return response.json();
}

// Place a limit buy order
const order = await placeOrder({
  symbol: 'PERP_ETH_USDC',
  side: 'BUY',
  order_type: 'LIMIT',
  order_price: 3000,
  order_quantity: 0.1,
});
```

## React SDK: useOrderEntry

The SDK provides a convenient hook for order entry:

```typescript
import { useOrderEntry, OrderSide, OrderType } from '@orderly.network/hooks';

function OrderForm({ symbol }: { symbol: string }) {
  const {
    submit,
    setValue,
    getValue,
    helper,
    reset,
    isSubmitting
  } = useOrderEntry(symbol, {
    initialOrder: {
      side: OrderSide.BUY,
      order_type: OrderType.LIMIT,
      price: '',
      order_quantity: '',
    },
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Validate before submission
    const validationResult = await helper.validate();
    if (!validationResult) {
      console.error('Validation failed');
      return;
    }

    try {
      await submit();
      reset();
      console.log('Order placed successfully');
    } catch (error) {
      console.error('Order failed:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <select
        onChange={(e) => setValue('side', e.target.value as OrderSide)}
        value={getValue('side')}
      >
        <option value={OrderSide.BUY}>Buy</option>
        <option value={OrderSide.SELL}>Sell</option>
      </select>

      <select
        onChange={(e) => setValue('order_type', e.target.value as OrderType)}
        value={getValue('order_type')}
      >
        <option value={OrderType.LIMIT}>Limit</option>
        <option value={OrderType.MARKET}>Market</option>
      </select>

      <input
        type="text"
        placeholder="Price"
        value={getValue('price') || ''}
        onChange={(e) => setValue('price', e.target.value)}
      />

      <input
        type="text"
        placeholder="Quantity"
        value={getValue('order_quantity') || ''}
        onChange={(e) => setValue('order_quantity', e.target.value)}
      />

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Placing...' : 'Place Order'}
      </button>
    </form>
  );
}
```

## Order Validation

Before submission, validate order parameters:

```typescript
// Get order rules for a symbol
const rulesResponse = await fetch('https://api.orderly.org/v1/public/info/PERP_ETH_USDC');
const rules = await rulesResponse.json();

/*
Rules include:
- base_min: Minimum order size
- base_max: Maximum order size
- base_tick: Size increment
- quote_min: Minimum price
- quote_max: Maximum price
- quote_tick: Price increment
- min_notional: Minimum order value
*/

function validateOrder(order: OrderRequest, rules: OrderRules): boolean {
  // Price filter
  if (order.order_price) {
    const price = parseFloat(order.order_price);
    if (price < rules.quote_min || price > rules.quote_max) {
      throw new Error('Price out of range');
    }
    if ((price - rules.quote_min) % rules.quote_tick !== 0) {
      throw new Error('Invalid price tick');
    }
  }

  // Size filter
  const quantity = parseFloat(order.order_quantity);
  if (quantity < rules.base_min || quantity > rules.base_max) {
    throw new Error('Quantity out of range');
  }
  if ((quantity - rules.base_min) % rules.base_tick !== 0) {
    throw new Error('Invalid quantity tick');
  }

  // Min notional
  const notional = (parseFloat(order.order_price) || 0) * quantity;
  if (notional < rules.min_notional) {
    throw new Error(`Minimum order value is ${rules.min_notional}`);
  }

  return true;
}
```

## Cancel Orders

### Cancel Single Order

```typescript
// REST API
DELETE /v1/order?order_id={order_id}&symbol={symbol}

// React SDK
import { useOrderStream } from '@orderly.network/hooks';

function OrderList() {
  const [orders, { cancelOrder }] = useOrderStream({
    status: OrderStatus.INCOMPLETE,
  });

  return orders.map((order) => (
    <div key={order.order_id}>
      {order.symbol} - {order.side} - {order.order_qty}
      <button onClick={() => cancelOrder(order.order_id)}>
        Cancel
      </button>
    </div>
  ));
}
```

### Cancel All Orders

```typescript
// REST API - Cancel all open orders
DELETE /v1/orders?symbol={symbol}  // Optional symbol filter

// React SDK
const [orders, { cancelAllOrders }] = useOrderStream();

await cancelAllOrders(); // Cancel all
await cancelAllOrders({ symbol: 'PERP_ETH_USDC' }); // Cancel for specific symbol
```

### Cancel by Client Order ID

```typescript
DELETE /v1/client/order?client_order_id={client_order_id}&symbol={symbol}
```

## Batch Orders

Place or cancel multiple orders in a single request:

```typescript
// Batch create (max 10 orders)
POST /v1/batch-order
Body: {
  orders: [
    { symbol: 'PERP_ETH_USDC', side: 'BUY', order_type: 'LIMIT', order_price: 3000, order_quantity: 0.1 },
    { symbol: 'PERP_BTC_USDC', side: 'BUY', order_type: 'LIMIT', order_price: 50000, order_quantity: 0.01 }
  ]
}

// Batch cancel (max 10 orders)
DELETE /v1/batch-order?order_ids={id1},{id2},...

// Example
const batchResponse = await fetch('https://api.orderly.org/v1/batch-order', {
  method: 'POST',
  headers: { /* auth headers */ },
  body: JSON.stringify({
    orders: [
      { symbol: 'PERP_ETH_USDC', side: 'BUY', order_type: 'LIMIT', order_price: 3000, order_quantity: 0.1 },
      { symbol: 'PERP_BTC_USDC', side: 'BUY', order_type: 'LIMIT', order_price: 50000, order_quantity: 0.01 }
    ]
  }),
});
```

## Edit Orders

Modify price or quantity of an existing order:

```typescript
// REST API
PUT /v1/order
Body: {
  order_id: '123456',
  order_price: '3100',      // New price
  order_quantity: '0.2',    // New quantity
}
```

## Order Stream (Real-time)

Monitor orders in real-time:

```typescript
import { useOrderStream, OrderStatus } from '@orderly.network/hooks';

function OrderMonitor() {
  const [orders, { cancelOrder }] = useOrderStream({
    status: OrderStatus.INCOMPLETE,
  });

  return (
    <table>
      <thead>
        <tr>
          <th>Symbol</th>
          <th>Side</th>
          <th>Price</th>
          <th>Quantity</th>
          <th>Filled</th>
          <th>Status</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        {orders.map((order) => (
          <tr key={order.order_id}>
            <td>{order.symbol}</td>
            <td>{order.side}</td>
            <td>{order.price}</td>
            <td>{order.order_qty}</td>
            <td>{order.filled_qty}</td>
            <td>{order.status}</td>
            <td>
              <button onClick={() => cancelOrder(order.order_id)}>
                Cancel
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
```

## Algo Orders (Stop, TP/SL)

For Take-Profit and Stop-Loss orders, see the **orderly-positions-tpsl** skill.

```typescript
// Basic algo order structure
POST /v1/algo/order
Body: {
  symbol: 'PERP_ETH_USDC',
  type: 'CLOSE_POSITION',
  algoType: 'TAKE_PROFIT',
  trigger_price: '3500',
  quantity: '0.1',
}
```

## Rate Limits

| Endpoint               | Rate Limit |
| ---------------------- | ---------- |
| POST /v1/order         | 10 req/sec |
| DELETE /v1/order       | 10 req/sec |
| PUT /v1/order          | 10 req/sec |
| POST /v1/batch-order   | 1 req/sec  |
| DELETE /v1/batch-order | 10 req/sec |

## Order Status Flow

```
NEW → PARTIAL_FILLED → FILLED
                    ↘ CANCELLED
         ↘ REJECTED (invalid orders)
         ↘ EXPIRED (GTD orders)
```

## Common Issues

### "Insufficient margin" error

- Check free collateral: `GET /v1/client/holding`
- Reduce order size or add collateral

### "Price out of range" error

- Order price must be within `price_range` of mark price
- For BUY: price ≤ mark_price × (1 + price_range)
- For SELL: price ≥ mark_price × (1 - price_range)

### "Invalid tick size" error

- Price must be multiple of `quote_tick`
- Quantity must be multiple of `base_tick`

### Order rejected immediately

- Check `GET /v1/public/info/{symbol}` for order rules
- Verify min_notional, price range, size limits

## Related Skills

- **orderly-api-authentication** - How to sign requests
- **orderly-positions-tpsl** - Managing positions and TP/SL
- **orderly-websocket-streaming** - Real-time order updates
- **orderly-sdk-react-hooks** - Full SDK reference
