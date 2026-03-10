---
name: orderly-ui-components
description: Build trading interfaces using pre-built React components - OrderEntry, Positions, TradingPage, WalletConnect, Sheets, Tables
---

# Orderly Network: UI Components

This skill covers building trading interfaces using Orderly's pre-built React components from `@orderly.network/react`.

## When to Use

- Rapidly building a trading UI
- Using pre-built, styled components
- Implementing standard trading interface patterns

## Prerequisites

- React 18+
- `@orderly.network/react` installed
- Tailwind CSS (recommended for styling)

## Installation

```bash
npm install @orderly.network/react @orderly.network/hooks @orderly.network/types

# Or with yarn
yarn add @orderly.network/react @orderly.network/hooks @orderly.network/types
```

## Core Providers

Wrap your app with the required providers:

```typescript
import {
  OrderlyAppProvider,
  TradingPageProvider,
  SymbolProvider,
  WalletConnector
} from '@orderly.network/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <OrderlyAppProvider
        brokerId="woofi_dex"
        chainFilter={[42161, 421614]}
      >
        <SymbolProvider>
          <TradingPageProvider>
            <Layout>
              <WalletConnector />
              <TradingPage />
            </Layout>
          </TradingPageProvider>
        </SymbolProvider>
      </OrderlyAppProvider>
    </QueryClientProvider>
  );
}
```

---

## Order Entry Component

### Basic Order Entry

```typescript
import { OrderEntry, OrderEntryProvider } from '@orderly.network/ui-order-entry';
import { useOrderEntry } from '@orderly.network/hooks';

function OrderEntryContainer() {
  const { onSubmit } = useOrderEntry();

  const handleSubmit = async (params: any) => {
    try {
      await onSubmit(params);
      console.log('Order submitted');
    } catch (e) {
      console.error('Order failed', e);
    }
  };

  return (
    <div className="bg-gray-900 rounded-lg p-4 border border-gray-800">
      <OrderEntry
        onSubmit={handleSubmit}
        defaultTab="limit"
        hideMarket={false}
      />
    </div>
  );
}

export function OrderEntryWidget() {
  return (
    <OrderEntryProvider symbol="PERP_BTC_USDC">
      <OrderEntryContainer />
    </OrderEntryProvider>
  );
}
```

### Order Entry Props

```typescript
interface OrderEntryProps {
  onSubmit?: (params: OrderParams) => Promise<void>;
  defaultTab?: 'limit' | 'market';
  hideMarket?: boolean;
  hideLimit?: boolean;
  showLeverage?: boolean;
  className?: string;
}
```

---

## Positions Component

### Basic Positions Table

```typescript
import { Positions } from '@orderly.network/ui-positions';

export function PositionsWidget() {
  const handleSymbolClick = (symbol: string) => {
    console.log('Navigate to:', symbol);
  };

  return (
    <div className="w-full">
      <Positions
        filter={{ symbol: 'PERP_ETH_USDC' }}  // Optional filter
        onSymbolClick={handleSymbolClick}
        showPagination={true}
      />
    </div>
  );
}
```

### Positions Props

```typescript
interface PositionsProps {
  filter?: {
    symbol?: string;
    side?: 'BUY' | 'SELL';
  };
  onSymbolClick?: (symbol: string) => void;
  showPagination?: boolean;
  pageSize?: number;
  className?: string;
}
```

---

## Orderbook Component

```typescript
import { Orderbook, OrderbookProvider } from '@orderly.network/ui-orderbook';

export function OrderbookWidget({ symbol }: { symbol: string }) {
  return (
    <OrderbookProvider symbol={symbol}>
      <Orderbook
        level={10}           // Number of levels to show
        showTotal={true}     // Show total column
        onItemClick={(price, side) => {
          console.log('Price clicked:', price, side);
        }}
      />
    </OrderbookProvider>
  );
}
```

---

## Wallet Connect Component

### Basic Wallet Connect

```typescript
import { WalletConnect } from '@orderly.network/react';

export function Header() {
  return (
    <header className="flex justify-between items-center p-4">
      <div className="logo">My DEX</div>
      <WalletConnect />
    </header>
  );
}
```

### Custom Wallet Button

```typescript
import { useAccount, useWalletConnector } from '@orderly.network/hooks';

export function CustomWalletButton() {
  const { account, state } = useAccount();
  const wallet = useWalletConnector();

  if (state.status !== 'connected') {
    return (
      <button
        onClick={() => wallet.connect()}
        className="btn-primary"
      >
        Connect Wallet
      </button>
    );
  }

  return (
    <div className="wallet-menu">
      <span>{account.address?.slice(0, 6)}...{account.address?.slice(-4)}</span>
      <button onClick={() => wallet.disconnect()}>
        Disconnect
      </button>
    </div>
  );
}
```

---

## Chart Components

### TradingView Widget

```typescript
import { TradingView } from '@orderly.network/ui-chart';

export function ChartWidget({ symbol }: { symbol: string }) {
  return (
    <div className="h-[500px]">
      <TradingView
        symbol={symbol}
        interval="1h"
        theme="dark"
        autosize={true}
      />
    </div>
  );
}
```

### Lightweight Charts

```typescript
import { LightweightChart } from '@orderly.network/ui-chart';

export function SimpleChart({ symbol }: { symbol: string }) {
  return (
    <div className="h-[400px]">
      <LightweightChart
        symbol={symbol}
        interval="15m"
        chartType="candlestick"
      />
    </div>
  );
}
```

---

## Data Table Component

### Generic Table

```typescript
import { Table } from '@orderly.network/ui';

type TradeRow = {
  id: string;
  price: number;
  size: number;
  time: string;
  side: 'BUY' | 'SELL';
};

export function TradesTable({ data }: { data: TradeRow[] }) {
  return (
    <Table<TradeRow>
      dataSource={data}
      columns={[
        {
          title: 'Price',
          dataIndex: 'price',
          render: (value, record) => (
            <span className={record.side === 'BUY' ? 'text-green-500' : 'text-red-500'}>
              {value.toFixed(2)}
            </span>
          ),
        },
        {
          title: 'Size',
          dataIndex: 'size',
          render: (value) => value.toFixed(4),
        },
        {
          title: 'Time',
          dataIndex: 'time',
        },
      ]}
      rowKey="id"
      pagination={{ pageSize: 20 }}
    />
  );
}
```

---

## Sheet (Drawer) Component

```typescript
import { Sheet, SheetTrigger, SheetContent, SheetHeader, SheetFooter } from '@orderly.network/ui';

export function OrderDetailsSheet({ order }: { order: Order }) {
  return (
    <Sheet>
      <SheetTrigger asChild>
        <button className="btn-secondary">View Details</button>
      </SheetTrigger>
      <SheetContent side="right">
        <SheetHeader>
          <h2>Order Details</h2>
        </SheetHeader>
        <div className="py-4">
          <div className="grid grid-cols-2 gap-2">
            <span>Symbol:</span>
            <span>{order.symbol}</span>
            <span>Side:</span>
            <span>{order.side}</span>
            <span>Price:</span>
            <span>{order.price}</span>
            <span>Quantity:</span>
            <span>{order.order_qty}</span>
            <span>Status:</span>
            <span>{order.status}</span>
          </div>
        </div>
        <SheetFooter>
          <button className="btn-primary">Close Position</button>
        </SheetFooter>
      </SheetContent>
    </Sheet>
  );
}
```

---

## Modal Component

```typescript
import { Modal, ModalTrigger, ModalContent, ModalHeader, ModalBody, ModalFooter } from '@orderly.network/ui';

export function ConfirmOrderModal({ order, onConfirm }: { order: Order; onConfirm: () => void }) {
  return (
    <Modal>
      <ModalTrigger asChild>
        <button className="btn-primary">Place Order</button>
      </ModalTrigger>
      <ModalContent>
        <ModalHeader>
          <h2>Confirm Order</h2>
        </ModalHeader>
        <ModalBody>
          <p>Are you sure you want to place this order?</p>
          <div className="order-summary">
            <p>{order.side} {order.quantity} {order.symbol} @ {order.price}</p>
          </div>
        </ModalBody>
        <ModalFooter>
          <button className="btn-secondary">Cancel</button>
          <button className="btn-primary" onClick={onConfirm}>Confirm</button>
        </ModalFooter>
      </ModalContent>
    </Modal>
  );
}
```

---

## Empty State Component

```typescript
import { NoData } from '@orderly.network/ui';

export function EmptyOrders() {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <NoData width={200} height={200} className="text-gray-500" />
      <p className="mt-4 text-gray-400">No open orders</p>
      <button className="mt-2 btn-secondary">Place Order</button>
    </div>
  );
}
```

---

## Notification/Toast Component

```typescript
import { Toast, ToastProvider, useToast } from '@orderly.network/ui';

function TradingPage() {
  const { toast } = useToast();

  const handleOrderSubmit = async () => {
    try {
      await submitOrder();
      toast({
        title: 'Order Placed',
        description: 'Your order has been submitted successfully',
        variant: 'success',
      });
    } catch (error) {
      toast({
        title: 'Order Failed',
        description: error.message,
        variant: 'error',
      });
    }
  };

  return <button onClick={handleOrderSubmit}>Place Order</button>;
}

// In your app root
function App() {
  return (
    <ToastProvider>
      <TradingPage />
    </ToastProvider>
  );
}
```

---

## Complete Trading Page Example

```typescript
import {
  OrderlyAppProvider,
  TradingPageProvider,
  SymbolProvider,
  WalletConnect,
} from '@orderly.network/react';
import { OrderEntry, OrderEntryProvider } from '@orderly.network/ui-order-entry';
import { Positions } from '@orderly.network/ui-positions';
import { Orderbook, OrderbookProvider } from '@orderly.network/ui-orderbook';
import { TradingView } from '@orderly.network/ui-chart';
import { useOrderEntry } from '@orderly.network/hooks';

function TradingPage() {
  const symbol = 'PERP_BTC_USDC';

  return (
    <div className="trading-layout">
      {/* Header */}
      <header className="flex justify-between items-center p-4 border-b">
        <h1>My DEX</h1>
        <WalletConnect />
      </header>

      {/* Main Content */}
      <div className="grid grid-cols-12 gap-4 p-4">
        {/* Left: Orderbook */}
        <div className="col-span-2">
          <OrderbookProvider symbol={symbol}>
            <Orderbook level={15} />
          </OrderbookProvider>
        </div>

        {/* Center: Chart + Order Entry */}
        <div className="col-span-7">
          <div className="h-[500px] mb-4">
            <TradingView symbol={symbol} />
          </div>
          <OrderEntryProvider symbol={symbol}>
            <OrderEntry defaultTab="limit" />
          </OrderEntryProvider>
        </div>

        {/* Right: Positions */}
        <div className="col-span-3">
          <Positions showPagination={false} />
        </div>
      </div>
    </div>
  );
}

export function App() {
  return (
    <OrderlyAppProvider brokerId="woofi_dex">
      <SymbolProvider>
        <TradingPageProvider>
          <TradingPage />
        </TradingPageProvider>
      </SymbolProvider>
    </OrderlyAppProvider>
  );
}
```

---

## Styling

Orderly components use Tailwind CSS classes. Customize with:

```css
/* Override component styles */
.order-entry-root {
  /* Your styles */
}

.positions-table {
  /* Your styles */
}

/* Use Tailwind dark mode */
.dark .order-entry-root {
  /* Dark mode styles */
}
```

---

## Common Issues

### Components not rendering

- Ensure all providers are wrapped correctly
- Check that `SymbolProvider` is above symbol-dependent components
- Verify Tailwind CSS is configured

### Styling conflicts

- Components use Tailwind utility classes
- Override with higher-specificity CSS
- Use `className` prop when available

### Data not updating

- Check WebSocket connection status
- Verify account is connected
- Ensure hooks are called inside provider components

## Related Skills

- **orderly-sdk-react-hooks** - Hook reference
- **orderly-trading-orders** - Order management
- **orderly-websocket-streaming** - Real-time data
