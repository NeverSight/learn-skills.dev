---
name: orderly-positions-tpsl
description: Monitor positions in real-time, configure Take-Profit/Stop-Loss orders, and manage risk with leverage settings
---

# Orderly Network: Positions & TP/SL

This skill covers position management, PnL tracking, leverage settings, and configuring Take-Profit (TP) and Stop-Loss (SL) orders for risk management.

## When to Use

- Building a position management interface
- Implementing risk management with TP/SL
- Tracking unrealized PnL
- Adjusting leverage settings

## Prerequisites

- Open positions on Orderly
- Understanding of perpetual futures
- API key with `read` and `trading` scopes

## Position Data Structure

```typescript
interface Position {
  symbol: string; // e.g., "PERP_ETH_USDC"
  position_qty: number; // Positive = long, Negative = short
  average_open_price: number; // Entry price
  mark_price: number; // Current mark price
  unrealized_pnl: number; // Unrealized profit/loss
  unrealized_pnl_roi: number; // ROI percentage
  mmr: number; // Maintenance margin ratio
  imr: number; // Initial margin ratio
  notional: number; // Position value
  leverage: number; // Current leverage
  est_liq_price: number; // Estimated liquidation price
  cost_position: number; // Position cost
  settle_price: number; // Settlement price
  unsettled_pnl: number; // Unsettled PnL
}
```

## Get Positions (REST API)

```typescript
// Get all positions
GET /v1/positions

// Get position for specific symbol
GET /v1/position/{symbol}

// Example response
{
  "success": true,
  "data": {
    "rows": [
      {
        "symbol": "PERP_ETH_USDC",
        "position_qty": 0.5,
        "average_open_price": 3000,
        "mark_price": 3100,
        "unrealized_pnl": 50,
        "unrealized_pnl_roi": 0.0333,
        "mmr": 0.01,
        "imr": 0.02,
        "notional": 1550,
        "leverage": 10,
        "est_liq_price": 2700
      }
    ]
  }
}
```

## React SDK: usePositionStream

Stream positions in real-time with automatic PnL updates:

```typescript
import { usePositionStream } from '@orderly.network/hooks';

function PositionsTable() {
  const {
    rows,
    aggregated,
    totalUnrealizedROI,
    isLoading
  } = usePositionStream();

  if (isLoading) return <div>Loading positions...</div>;

  return (
    <div>
      <div className="summary">
        <h3>Total Unrealized PnL: {aggregated?.totalUnrealizedPnl?.toFixed(2)} USDC</h3>
        <p>ROI: {(totalUnrealizedROI * 100).toFixed(2)}%</p>
      </div>

      <table>
        <thead>
          <tr>
            <th>Symbol</th>
            <th>Size</th>
            <th>Entry Price</th>
            <th>Mark Price</th>
            <th>Unrealized PnL</th>
            <th>Leverage</th>
            <th>Liq. Price</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((position) => (
            <tr key={position.symbol}>
              <td>{position.symbol}</td>
              <td className={position.position_qty > 0 ? 'long' : 'short'}>
                {position.position_qty > 0 ? '+' : ''}{position.position_qty}
              </td>
              <td>{position.average_open_price.toFixed(2)}</td>
              <td>{position.mark_price.toFixed(2)}</td>
              <td className={position.unrealized_pnl >= 0 ? 'profit' : 'loss'}>
                {position.unrealized_pnl.toFixed(2)} USDC
              </td>
              <td>{position.leverage}x</td>
              <td>{position.liq_price.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
```

## Close Position

### Partial Close

```typescript
import { usePositionClose } from '@orderly.network/hooks';

function ClosePositionButton({ symbol, positionQty }: { symbol: string; positionQty: number }) {
  const { closePosition, isClosing } = usePositionClose();

  const handleClose = async (percentage: number) => {
    const quantity = Math.abs(positionQty) * (percentage / 100);
    await closePosition({
      symbol,
      qty: quantity,
      side: positionQty > 0 ? 'SELL' : 'BUY',
    });
  };

  return (
    <div>
      <button onClick={() => handleClose(25)} disabled={isClosing}>Close 25%</button>
      <button onClick={() => handleClose(50)} disabled={isClosing}>Close 50%</button>
      <button onClick={() => handleClose(100)} disabled={isClosing}>Close 100%</button>
    </div>
  );
}
```

### Market Close (REST API)

```typescript
// Close entire position at market price
POST /v1/order
Body: {
  symbol: 'PERP_ETH_USDC',
  side: positionQty > 0 ? 'SELL' : 'BUY',
  order_type: 'MARKET',
  order_quantity: Math.abs(positionQty).toString(),
  reduce_only: true,
}
```

## Leverage Management

### Get Current Leverage

```typescript
GET /v1/client/leverage?symbol={symbol}

// Response
{
  "success": true,
  "data": {
    "leverage": 10,
    "max_leverage": 25
  }
}
```

### Set Leverage

```typescript
POST /v1/client/leverage
Body: {
  symbol: 'PERP_ETH_USDC',
  leverage: 15,  // New leverage value
}

// React SDK
import { useLeverage } from '@orderly.network/hooks';

function LeverageSlider({ symbol }: { symbol: string }) {
  const { leverage, maxLeverage, setLeverage, isLoading } = useLeverage(symbol);

  const handleChange = async (newLeverage: number) => {
    try {
      await setLeverage(newLeverage);
    } catch (error) {
      console.error('Failed to set leverage:', error);
    }
  };

  return (
    <div>
      <label>Leverage: {leverage}x</label>
      <input
        type="range"
        min="1"
        max={maxLeverage}
        value={leverage}
        onChange={(e) => handleChange(parseInt(e.target.value))}
        disabled={isLoading}
      />
    </div>
  );
}
```

## Take-Profit / Stop-Loss Orders

### TP/SL Order Types

| Type            | Description                                |
| --------------- | ------------------------------------------ |
| `TAKE_PROFIT`   | Trigger when price reaches target (profit) |
| `STOP_LOSS`     | Trigger when price drops below threshold   |
| `TRAILING_STOP` | Dynamic stop that follows price            |

### Using useTPSLOrder Hook

```typescript
import { useTPSLOrder } from '@orderly.network/hooks';

function TPSSettings({ position }: { position: Position }) {
  const [computed, { setValue, submit, validate, reset }] = useTPSLOrder(position);

  const handleSubmit = async () => {
    try {
      await validate();
      await submit();
      console.log('TP/SL order placed');
    } catch (error) {
      console.error('TP/SL failed:', error);
    }
  };

  return (
    <div className="tpsl-form">
      <h4>Take Profit</h4>
      <div>
        <label>Trigger Price</label>
        <input
          type="number"
          placeholder="TP Price"
          onChange={(e) => setValue('tp_trigger_price', e.target.value)}
        />
      </div>
      <div>
        <label>Or Offset %</label>
        <input
          type="number"
          placeholder="e.g., 5 for 5%"
          onChange={(e) => setValue('tp_offset_percentage', parseFloat(e.target.value))}
        />
      </div>

      <h4>Stop Loss</h4>
      <div>
        <label>Trigger Price</label>
        <input
          type="number"
          placeholder="SL Price"
          onChange={(e) => setValue('sl_trigger_price', e.target.value)}
        />
      </div>
      <div>
        <label>Or Offset %</label>
        <input
          type="number"
          placeholder="e.g., -5 for -5%"
          onChange={(e) => setValue('sl_offset_percentage', parseFloat(e.target.value))}
        />
      </div>

      <button onClick={handleSubmit}>Set TP/SL</button>
    </div>
  );
}
```

### REST API: Algo Orders for TP/SL

```typescript
// Place TP/SL order (creates both TP and SL as child orders)
POST /v1/algo/order
Body: {
  symbol: 'PERP_ETH_USDC',
  algo_type: 'TP_SL',
  quantity: 5.5,
  trigger_price_type: 'MARK_PRICE',
  child_orders: [
    {
      symbol: 'PERP_ETH_USDC',
      algo_type: 'TAKE_PROFIT',
      side: 'SELL',
      type: 'MARKET',
      trigger_price: 3500,
      reduce_only: true
    },
    {
      symbol: 'PERP_ETH_USDC',
      algo_type: 'STOP_LOSS',
      side: 'SELL',
      type: 'MARKET',
      trigger_price: 2800,
      reduce_only: true
    }
  ]
}

// Positional TP/SL (attached to entire position)
POST /v1/algo/order
Body: {
  symbol: 'PERP_ETH_USDC',
  algo_type: 'POSITIONAL_TP_SL',
  trigger_price_type: 'MARK_PRICE',
  child_orders: [
    {
      symbol: 'PERP_ETH_USDC',
      algo_type: 'TAKE_PROFIT',
      side: 'SELL',
      type: 'CLOSE_POSITION',
      trigger_price: 3500,
      reduce_only: true
    },
    {
      symbol: 'PERP_ETH_USDC',
      algo_type: 'STOP_LOSS',
      side: 'SELL',
      type: 'CLOSE_POSITION',
      trigger_price: 2800,
      reduce_only: true
    }
  ]
}
```

### STOP Orders (Stop Market)

```typescript
POST /v1/algo/order
Body: {
  symbol: 'PERP_ETH_USDC',
  algo_type: 'STOP',
  quantity: 5.5,
  side: 'BUY',
  type: 'LIMIT',
  trigger_price_type: 'MARK_PRICE',
  trigger_price: 4.203,
  price: 3.5  // Limit price for the triggered order
}
```

### Cancel TP/SL Orders

```typescript
// Cancel single algo order
DELETE /v1/algo/order?order_id={order_id}&symbol={symbol}

// Cancel all algo orders for symbol
DELETE /v1/algo/orders?symbol={symbol}

// React SDK
const [algoOrders, { cancelAlgoOrder }] = useAlgoOrderStream();
await cancelAlgoOrder(orderId);
```

## Position History

```typescript
GET /v1/position_history?symbol={symbol}&start={timestamp}&end={timestamp}

// Response includes closed positions with realized PnL
```

## PnL Calculations

### Unrealized PnL

```typescript
// For LONG positions
unrealizedPnL = (markPrice - averageOpenPrice) * positionQty;

// For SHORT positions
unrealizedPnL = (averageOpenPrice - markPrice) * Math.abs(positionQty);
```

### ROI

```typescript
// Return on Investment
roi = unrealizedPnL / ((averageOpenPrice * Math.abs(positionQty)) / leverage);
```

### Liquidation Price

```typescript
// For LONG positions
liqPrice = averageOpenPrice * (1 - mmr - 1 / leverage);

// For SHORT positions
liqPrice = averageOpenPrice * (1 + mmr + 1 / leverage);
```

## Risk Metrics

```typescript
// Available fields from GET /v1/positions response:
{
  "current_margin_ratio_with_orders": 1.2385,
  "free_collateral": 450315.09,
  "initial_margin_ratio": 0.1,
  "initial_margin_ratio_with_orders": 0.1,
  "maintenance_margin_ratio": 0.05,
  "maintenance_margin_ratio_with_orders": 0.05,
  "margin_ratio": 1.2385,
  "open_margin_ratio": 1.2102,
  "total_collateral_value": 489865.71,
  "total_pnl_24_h": 0
}
```

## Margin vs Collateral: Understanding the Hierarchy

Orderly uses a multi-layer risk system. Here's how the pieces fit together:

```
Your Deposit
     ↓
[Collateral Factor] → Determines effective collateral value
     ↓
Effective Collateral (what you can actually use)
     ↓
[IMR/MMR] → Required margin per position
     ↓
Used Collateral (locked in positions)
     ↓
Free Collateral (available for new trades)
```

### The Three Layers Explained

**1. Collateral Factor (Token Level)**

- Set per token by Orderly risk team
- Example: USDC = 1.0, USDT = 0.95
- Applied when you deposit: $1000 USDT × 0.95 = $950 effective collateral
- **Where to find it**: `GET /v1/public/token`

**2. IMR/MMR (Position Level)**

- **IMR (Initial Margin Ratio)**: Minimum collateral needed to OPEN a position
- **MMR (Maintenance Margin Ratio)**: Minimum collateral needed to KEEP a position open
- Determined by leverage: 10x leverage = 10% IMR, ~5% MMR
- Applied to position notional: $10,000 position × 10% IMR = $1,000 required
- **Where to find it**: Position object or symbol info

**3. Account Margin Ratio (Account Level)**

- `margin_ratio = total_collateral / total_notional`
- If this drops toward MMR, you're approaching liquidation
- **Where to find it**: `GET /v1/client/holding`

### Calculation Example

```
Deposit: $10,000 USDC (collateral_factor = 1.0)
Effective Collateral: $10,000

Open Position: $50,000 ETH-PERP at 10x leverage
IMR Required: $50,000 × 10% = $5,000
MMR Required: $50,000 × 5% = $2,500

After opening:
- Used Collateral: $5,000
- Free Collateral: $5,000
- Margin Ratio: $10,000 / $50,000 = 20%

Liquidation happens when:
- Margin Ratio drops to MMR (5%)
- That means your collateral drops to $2,500
- Or position grows to $200,000 notional
```

**Key Takeaway**: You need sufficient effective collateral (after collateral factor) to meet IMR requirements (determined by leverage). The margin_ratio tells you how close you are to liquidation (determined by MMR).

## Common Issues

### "Position would exceed max leverage" error

- Current notional with new leverage exceeds limits
- Reduce position size or increase collateral

### "Insufficient margin for TP/SL" error

- TP/SL orders require available margin
- Close some positions or add collateral

### TP/SL not triggering

- Check if trigger_price is valid
- Verify the order is in NEW status
- Market may have gapped past trigger

### Liquidation risk

- Monitor margin_ratio closely
- Set stop-losses early
- Watch funding rates for extended positions

## Related Skills

- **orderly-trading-orders** - Placing orders
- **orderly-websocket-streaming** - Real-time position updates
- **orderly-sdk-react-hooks** - Full SDK reference
- **orderly-api-authentication** - Signing requests
