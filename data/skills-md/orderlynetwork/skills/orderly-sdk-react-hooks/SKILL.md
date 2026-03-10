---
name: orderly-sdk-react-hooks
description: Reference guide for using Orderly React SDK hooks - useOrderEntry, usePositionStream, useOrderbookStream, useCollateral, and more
---

# Orderly Network: SDK React Hooks Reference

Complete reference for all hooks provided by `@orderly.network/hooks`.

## When to Use

- Building React applications with Orderly
- Quick reference for hook signatures
- Understanding hook return values and parameters

## Prerequisites

- React 18+
- `@orderly.network/hooks` installed
- OrderlyConfigProvider wrapping your app

## Installation

```bash
npm install @orderly.network/hooks @orderly.network/types

# Or with yarn
yarn add @orderly.network/hooks @orderly.network/types
```

## Setup

```typescript
import { OrderlyAppProvider } from '@orderly.network/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <OrderlyAppProvider
        brokerId="woofi_dex"
        chainFilter={[42161, 421614]}
      >
        <YourApp />
      </OrderlyAppProvider>
    </QueryClientProvider>
  );
}
```

---

## Account Hooks

### useAccount

Access account state and actions.

```typescript
import { useAccount } from '@orderly.network/hooks';

const { account, state } = useAccount();

// State
state.status: 'notConnected' | 'connecting' | 'connected' | 'disconnecting'
state.address: string | null

// Account
account.accountId: string
account.address: string
account.connect(): Promise<void>
account.disconnect(): Promise<void>
account.setAddress(address, options): void

// Example
function AccountInfo() {
  const { account, state } = useAccount();

  if (state.status !== 'connected') {
    return <button onClick={() => account.connect()}>Connect</button>;
  }

  return (
    <div>
      <p>Account: {account.accountId}</p>
      <p>Address: {account.address}</p>
      <button onClick={() => account.disconnect()}>Disconnect</button>
    </div>
  );
}
```

### useWalletConnector

Manage wallet connection.

```typescript
import { useWalletConnector } from '@orderly.network/hooks';

const wallet = useWalletConnector();

// State
wallet.connected: boolean
wallet.connecting: boolean
wallet.connectedChain: { id: string } | null
wallet.address: string | null

// Actions
wallet.connect(): Promise<void>
wallet.disconnect(): Promise<void>
wallet.setChain(options): Promise<void>

// Example
function WalletButton() {
  const wallet = useWalletConnector();

  if (wallet.connecting) {
    return <span>Connecting...</span>;
  }

  if (wallet.connected) {
    return (
      <div>
        <span>{wallet.address?.slice(0, 6)}...{wallet.address?.slice(-4)}</span>
        <button onClick={() => wallet.disconnect()}>Disconnect</button>
      </div>
    );
  }

  return <button onClick={() => wallet.connect()}>Connect Wallet</button>;
}
```

---

## Trading Hooks

### useOrderEntry

Create and submit orders.

```typescript
import { useOrderEntry, OrderSide, OrderType } from '@orderly.network/hooks';

const {
  submit,
  setValue,
  getValue,
  helper,
  reset,
  isSubmitting,
  errors,
} = useOrderEntry(symbol, options);

// Options
interface OrderEntryOptions {
  initialOrder?: {
    side?: OrderSide;
    order_type?: OrderType;
    price?: string;
    order_quantity?: string;
  };
  onSuccess?: (result) => void;
  onError?: (error) => void;
}

// Methods
setValue(field: string, value: any): void
getValue(field: string): any
helper.validate(): Promise<boolean>
submit(): Promise<void>
reset(): void

// Example
function OrderForm({ symbol }: { symbol: string }) {
  const { submit, setValue, getValue, helper, isSubmitting } = useOrderEntry(symbol, {
    initialOrder: {
      side: OrderSide.BUY,
      order_type: OrderType.LIMIT,
    },
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const valid = await helper.validate();
    if (valid) {
      await submit();
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <select onChange={(e) => setValue('side', e.target.value)}>
        <option value={OrderSide.BUY}>Buy</option>
        <option value={OrderSide.SELL}>Sell</option>
      </select>

      <input
        placeholder="Price"
        onChange={(e) => setValue('price', e.target.value)}
      />

      <input
        placeholder="Quantity"
        onChange={(e) => setValue('order_quantity', e.target.value)}
      />

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Placing...' : 'Place Order'}
      </button>
    </form>
  );
}
```

### useOrderStream

Stream orders in real-time.

```typescript
import { useOrderStream, OrderStatus } from '@orderly.network/hooks';

const [orders, actions] = useOrderStream(options);

// Options
interface OrderStreamOptions {
  status?: OrderStatus | OrderStatus[];
  symbol?: string;
  side?: OrderSide;
}

// Orders
orders: Order[]

// Order type
interface Order {
  order_id: number;
  symbol: string;
  side: 'BUY' | 'SELL';
  order_type: string;
  price: string;
  order_qty: string;
  filled_qty: string;
  status: string;
  created_at: number;
  updated_at: number;
}

// Actions
actions.cancelOrder(orderId: number | string): Promise<void>
actions.cancelAllOrders(options?): Promise<void>
actions.editOrder(orderId, updates): Promise<void>

// Example
function OpenOrders() {
  const [orders, { cancelOrder, cancelAllOrders }] = useOrderStream({
    status: OrderStatus.INCOMPLETE,
  });

  return (
    <div>
      <button onClick={() => cancelAllOrders()}>Cancel All</button>
      {orders.map((order) => (
        <div key={order.order_id}>
          {order.symbol} {order.side} {order.order_qty} @ {order.price}
          <button onClick={() => cancelOrder(order.order_id)}>Cancel</button>
        </div>
      ))}
    </div>
  );
}
```

---

## Position Hooks

### usePositionStream

Stream positions with real-time PnL.

```typescript
import { usePositionStream } from '@orderly.network/hooks';

const { rows, aggregated, totalUnrealizedROI, isLoading } = usePositionStream();

// Return values
rows: Position[]
aggregated: {
  totalUnrealizedPnl: number;
  totalNotional: number;
  totalCollateral: number;
}
totalUnrealizedROI: number
isLoading: boolean

// Position type
interface Position {
  symbol: string;
  position_qty: number;
  average_open_price: number;
  mark_price: number;
  unrealized_pnl: number;
  unrealized_pnl_roi: number;
  leverage: number;
  liq_price: number;
  mmr: number;
  imr: number;
  notional: number;
}

// Example
function PositionsSummary() {
  const { rows, aggregated, totalUnrealizedROI } = usePositionStream();

  return (
    <div>
      <h3>Total PnL: ${aggregated?.totalUnrealizedPnl?.toFixed(2)}</h3>
      <p>ROI: {(totalUnrealizedROI * 100).toFixed(2)}%</p>
      <table>
        {rows.map((pos) => (
          <tr key={pos.symbol}>
            <td>{pos.symbol}</td>
            <td>{pos.position_qty}</td>
            <td>${pos.unrealized_pnl.toFixed(2)}</td>
          </tr>
        ))}
      </table>
    </div>
  );
}
```

### useTPSLOrder

Manage Take-Profit and Stop-Loss orders.

```typescript
import { useTPSLOrder } from '@orderly.network/hooks';

const [computed, actions] = useTPSLOrder(position);

// Position with position_qty and average_open_price
interface PositionForTPSL {
  symbol: string;
  position_qty: number;
  average_open_price: number;
}

// Computed values
computed: {
  tpTriggerPrice?: string;
  slTriggerPrice?: string;
  tpOffsetPercentage?: number;
  slOffsetPercentage?: number;
}

// Actions
actions.setValue(field: string, value: any): void
actions.validate(): Promise<boolean>
actions.submit(): Promise<void>
actions.reset(): void

// Example
function TPSSForm({ position }: { position: Position }) {
  const [_, { setValue, validate, submit }] = useTPSLOrder(position);

  const handleSetTPSL = async () => {
    setValue('tp_trigger_price', '3500');
    setValue('sl_trigger_price', '2800');

    if (await validate()) {
      await submit();
    }
  };

  return <button onClick={handleSetTPSL}>Set TP/SL</button>;
}
```

---

## Market Data Hooks

### useOrderbookStream

Real-time orderbook data.

```typescript
import { useOrderbookStream } from '@orderly.network/hooks';

const { asks, bids, isLoading } = useOrderbookStream(symbol);

// Return values
asks: [string, string][]  // [price, quantity] - ascending by price
bids: [string, string][]  // [price, quantity] - descending by price
isLoading: boolean

// Example
function Orderbook({ symbol }: { symbol: string }) {
  const { asks, bids } = useOrderbookStream(symbol);

  return (
    <div className="orderbook">
      <div className="asks">
        {asks.slice(0, 10).map(([price, qty], i) => (
          <div key={i} className="ask-row">
            <span className="price">{price}</span>
            <span className="qty">{qty}</span>
          </div>
        ))}
      </div>
      <div className="bids">
        {bids.slice(0, 10).map(([price, qty], i) => (
          <div key={i} className="bid-row">
            <span className="price">{price}</span>
            <span className="qty">{qty}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
```

### useMarkPrice

Current mark price for a symbol.

```typescript
import { useMarkPrice } from '@orderly.network/hooks';

const markPrice = useMarkPrice(symbol);
// Returns: number

// Example
function PriceDisplay({ symbol }: { symbol: string }) {
  const markPrice = useMarkPrice(symbol);
  return <span>${markPrice?.toFixed(2)}</span>;
}
```

### useTickerStream

24-hour ticker statistics.

```typescript
import { useTickerStream } from '@orderly.network/hooks';

const ticker = useTickerStream(symbol);

// Ticker type
interface Ticker {
  symbol: string;
  last_price: string;
  high_24h: string;
  low_24h: string;
  volume_24h: string;
  quote_volume_24h: string;
  open: string;
  price_change_24h: string;
  price_change_percent_24h: string;
}
```

### useSymbolInfo

Get trading rules for a symbol.

```typescript
import { useSymbolInfo } from '@orderly.network/hooks';

const symbolInfo = useSymbolInfo(symbol);

// Symbol info type
interface SymbolInfo {
  symbol: string;
  base_currency: string;
  quote_currency: string;
  base_min: number;
  base_max: number;
  base_tick: number;
  quote_min: number;
  quote_max: number;
  quote_tick: number;
  min_notional: number;
  price_range: number;
  leverage_max: number;
}
```

---

## Balance Hooks

### useCollateral

Account collateral information.

```typescript
import { useCollateral } from '@orderly.network/hooks';

const { totalCollateral, freeCollateral, availableBalance } = useCollateral({ dp: 2 });

// Return values
totalCollateral: number     // Total account value
freeCollateral: number      // Available for new positions
availableBalance: number    // Free balance

// Example
function AccountSummary() {
  const { totalCollateral, freeCollateral } = useCollateral({ dp: 2 });

  return (
    <div>
      <p>Total: ${totalCollateral}</p>
      <p>Available: ${freeCollateral}</p>
    </div>
  );
}
```

### useBalance

Token balance on Orderly.

```typescript
import { useBalance } from '@orderly.network/hooks';

const balance = useBalance();
// Returns: { USDC: string, USDT: string, ... }

// Example
function BalanceDisplay() {
  const balance = useBalance();
  return <span>USDC: {balance?.USDC || '0'}</span>;
}
```

---

## Chain Hooks

### useChains

Get supported chains.

```typescript
import { useChains } from '@orderly.network/hooks';

const [chains, { findByChainId }] = useChains();

// Chain type
interface Chain {
  id: number;
  name: string;
  network: string;
  chain_id: string;
  explorer: string;
}

// Example
function ChainSelector() {
  const [chains] = useChains();

  return (
    <select>
      {chains.map((chain) => (
        <option key={chain.id} value={chain.id}>
          {chain.name}
        </option>
      ))}
    </select>
  );
}
```

---

## Deposit/Withdraw Hooks

### useDeposit

Handle deposits.

```typescript
import { useDeposit } from '@orderly.network/hooks';

const {
  balance,
  allowance,
  approve,
  deposit,
  depositFee,
  setQuantity,
  fetchBalance,
} = useDeposit(options);

// Options
interface DepositOptions {
  address: string;      // Token contract address
  decimals: number;     // Token decimals
  srcToken: string;     // Token symbol
  srcChainId: number;   // Source chain ID
}

// Example
function DepositUSDC() {
  const { balance, allowance, approve, deposit, isApproving, isDepositing } = useDeposit({
    address: '0xaf88d065e77c8cC2239327C5EDb3A432268e5831',
    decimals: 6,
    srcToken: 'USDC',
    srcChainId: 42161,
  });

  const amount = '100';

  const handleDeposit = async () => {
    if (parseFloat(allowance) < 100) {
      await approve();
    }
    await deposit(amount);
  };

  return (
    <button onClick={handleDeposit} disabled={isApproving || isDepositing}>
      Deposit
    </button>
  );
}
```

### useWithdraw

Handle withdrawals.

```typescript
import { useWithdraw } from '@orderly.network/hooks';

const { withdraw, isLoading, withdrawFee } = useWithdraw();

// Withdraw options
interface WithdrawOptions {
  symbol: string;
  amount: string;
  address: string; // Destination address
  chainId: number;
  network: string;
}

// Example
const { withdraw, isLoading } = useWithdraw();

await withdraw({
  symbol: 'USDC',
  amount: '100',
  address: '0x...',
  chainId: 42161,
  network: 'arbitrum',
});
```

---

## Leverage Hook

### useLeverage

Get and set leverage.

```typescript
import { useLeverage } from '@orderly.network/hooks';

const { leverage, maxLeverage, setLeverage, isLoading } = useLeverage(symbol);

// Return values
leverage: number
maxLeverage: number
setLeverage(value: number): Promise<void>
isLoading: boolean

// Example
function LeverageControl({ symbol }: { symbol: string }) {
  const { leverage, maxLeverage, setLeverage } = useLeverage(symbol);

  return (
    <input
      type="range"
      min={1}
      max={maxLeverage}
      value={leverage}
      onChange={(e) => setLeverage(parseInt(e.target.value))}
    />
  );
}
```

---

## Common Patterns

### Combined Trading Interface

```typescript
import {
  useAccount,
  useOrderEntry,
  usePositionStream,
  useOrderbookStream,
  useCollateral,
  OrderSide,
  OrderType,
} from '@orderly.network/hooks';

function TradingInterface({ symbol }: { symbol: string }) {
  const { state } = useAccount();
  const { rows: positions } = usePositionStream();
  const { asks, bids } = useOrderbookStream(symbol);
  const { freeCollateral } = useCollateral();
  const { submit, setValue, getValue, helper } = useOrderEntry(symbol);

  if (state.status !== 'connected') {
    return <ConnectWallet />;
  }

  return (
    <div className="trading-interface">
      <div className="left-panel">
        <Orderbook asks={asks} bids={bids} />
      </div>
      <div className="center-panel">
        <OrderForm
          submit={submit}
          setValue={setValue}
          getValue={getValue}
          validate={helper.validate}
          freeCollateral={freeCollateral}
        />
        <PositionsList positions={positions} />
      </div>
    </div>
  );
}
```

## Related Skills

- **orderly-ui-components** - Pre-built UI components
- **orderly-trading-orders** - Order management details
- **orderly-positions-tpsl** - Position management
- **orderly-websocket-streaming** - Underlying WebSocket implementation
