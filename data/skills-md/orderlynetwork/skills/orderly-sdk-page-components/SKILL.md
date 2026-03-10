---
name: orderly-sdk-page-components
description: Use pre-built page components from Orderly SDK to quickly assemble complete DEX pages (TradingPage, Portfolio, Markets, Leaderboard, etc.)
---

# Orderly Network: SDK Page Components

Pre-built, full-featured page components for building a complete DEX. These components handle responsive design (desktop/mobile), state management, and UI out of the box.

## When to Use

- Building a complete DEX quickly
- Using pre-built, production-ready pages
- Implementing standard DEX pages (trading, portfolio, markets)
- Need responsive layouts out of the box

## Prerequisites

- Orderly SDK packages installed (`@orderly.network/trading`, `@orderly.network/portfolio`, `@orderly.network/markets`)
- Providers configured (see `orderly-sdk-dex-architecture`)
- Router set up (React Router)

## Overview

| Component                       | Package                                | Description                                             |
| ------------------------------- | -------------------------------------- | ------------------------------------------------------- |
| `TradingPage`                   | `@orderly.network/trading`             | Full trading interface with chart, orderbook, positions |
| `OverviewModule.OverviewPage`   | `@orderly.network/portfolio`           | Portfolio dashboard with assets, performance            |
| `PositionsModule.PositionsPage` | `@orderly.network/portfolio`           | Positions list with history, liquidations               |
| `OrdersModule.OrdersPage`       | `@orderly.network/portfolio`           | Orders list (open, pending, filled)                     |
| `AssetsModule.AssetsPage`       | `@orderly.network/portfolio`           | Asset balances, deposit/withdraw                        |
| `HistoryModule.HistoryPage`     | `@orderly.network/portfolio`           | Trade history, funding, settlements                     |
| `MarketsHomePage`               | `@orderly.network/markets`             | Markets listing with stats                              |
| `LeaderboardPage`               | `@orderly.network/trading-leaderboard` | Trading competition leaderboard                         |
| `TradingRewardsPage`            | `@orderly.network/trading-rewards`     | Rewards program page                                    |
| `Dashboard`                     | `@orderly.network/affiliate`           | Affiliate/referral dashboard                            |

## 1. TradingPage

The main trading interface with TradingView chart, orderbook, order entry, positions, and orders.

### Import

```tsx
import { TradingPage } from '@orderly.network/trading';
```

### Props

```tsx
interface TradingPageProps {
  // Required: Trading symbol (e.g., "PERP_ETH_USDC")
  symbol: string;

  // Callback when user changes symbol
  onSymbolChange?: (symbol: API.Symbol) => void;

  // TradingView chart configuration
  tradingViewConfig: {
    scriptSRC?: string; // Path to TradingView library
    library_path: string; // Path to charting_library folder
    customCssUrl?: string; // Custom CSS for chart
    colorConfig?: {
      chartBG?: string;
      upColor?: string;
      downColor?: string;
      pnlUpColor?: string;
      pnlDownColor?: string;
    };
  };

  // PnL sharing configuration
  sharePnLConfig?: {
    backgroundImages?: string[]; // Background images for share cards
    color?: string;
    profitColor?: string;
    lossColor?: string;
    brandColor?: string;
  };

  // Disable specific features
  disableFeatures?: TradingFeatures[];

  // Override specific sections with custom components
  overrideFeatures?: Record<TradingFeatures, ReactNode>;
}

enum TradingFeatures {
  Sider = 'sider',
  TopNavBar = 'topNavBar',
  Footer = 'footer',
  Header = 'header',
  Kline = 'kline',
  OrderBook = 'orderBook',
  TradeHistory = 'tradeHistory',
  Positions = 'positions',
  Orders = 'orders',
}
```

### Usage Example

```tsx
import { useCallback, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { TradingPage } from '@orderly.network/trading';
import { API } from '@orderly.network/types';

export default function TradingRoute() {
  const { symbol: paramSymbol } = useParams();
  const [symbol, setSymbol] = useState(paramSymbol || 'PERP_ETH_USDC');
  const navigate = useNavigate();

  const onSymbolChange = useCallback(
    (data: API.Symbol) => {
      setSymbol(data.symbol);
      navigate(`/perp/${data.symbol}`);
    },
    [navigate]
  );

  return (
    <TradingPage
      symbol={symbol}
      onSymbolChange={onSymbolChange}
      tradingViewConfig={{
        scriptSRC: '/tradingview/charting_library/charting_library.js',
        library_path: '/tradingview/charting_library/',
      }}
      sharePnLConfig={{
        backgroundImages: ['/pnl-bg-1.png', '/pnl-bg-2.png'],
      }}
    />
  );
}
```

### TradingView Setup

1. Download TradingView charting library from TradingView
2. Place in `public/tradingview/charting_library/`
3. Configure paths in `tradingViewConfig`

## 2. Portfolio Pages

Portfolio is organized into modules, each containing a complete page component.

### Import

```tsx
import {
  OverviewModule,
  PositionsModule,
  OrdersModule,
  AssetsModule,
  HistoryModule,
} from '@orderly.network/portfolio';
```

### OverviewModule.OverviewPage

Portfolio overview with assets summary, performance chart, and recent activity.

```tsx
interface OverviewPageProps {
  hideAffiliateCard?: boolean; // Hide affiliate promotion card
  hideTraderCard?: boolean; // Hide trader stats card
}

// Usage
import { OverviewModule } from '@orderly.network/portfolio';

function PortfolioOverview() {
  return <OverviewModule.OverviewPage hideAffiliateCard={false} hideTraderCard={false} />;
}
```

**Sections included:**

- Asset summary widget
- Asset allocation chart
- Performance metrics
- Funding history
- Distribution history

### PositionsModule.PositionsPage

Current and historical positions with liquidation history.

```tsx
import { PositionsModule } from '@orderly.network/portfolio';

function PositionsRoute() {
  return <PositionsModule.PositionsPage />;
}
```

**Tabs included:**

- Positions (current open positions)
- Position History
- Liquidation History

### OrdersModule.OrdersPage

Order management with open, pending, and filled orders.

```tsx
interface OrdersPageProps {
  sharePnLConfig?: SharePnLConfig; // For sharing closed PnL
}

import { OrdersModule } from '@orderly.network/portfolio';

function OrdersRoute() {
  return (
    <OrdersModule.OrdersPage
      sharePnLConfig={{
        backgroundImages: ['/pnl-bg-1.png'],
      }}
    />
  );
}
```

**Features:**

- Open orders with cancel functionality
- Pending orders (TP/SL)
- Order history with download

### AssetsModule.AssetsPage

Asset management with deposit/withdraw functionality.

```tsx
import { AssetsModule } from '@orderly.network/portfolio';

function AssetsRoute() {
  return <AssetsModule.AssetsPage />;
}
```

**Features:**

- USDC balance display
- Deposit/withdraw buttons
- Cross-chain transfers
- Transaction history

### HistoryModule.HistoryPage

Complete trade and transaction history.

```tsx
import { HistoryModule } from '@orderly.network/portfolio';

function HistoryRoute() {
  return <HistoryModule.HistoryPage />;
}
```

**Tabs included:**

- Trade history
- Funding payments
- Settlements

### Complete Portfolio Layout

```tsx
import { Outlet, NavLink } from 'react-router-dom';
import {
  OverviewModule,
  PositionsModule,
  OrdersModule,
  AssetsModule,
  HistoryModule,
} from '@orderly.network/portfolio';

// Portfolio layout with navigation
function PortfolioLayout() {
  return (
    <div className="portfolio-container">
      <nav className="portfolio-nav">
        <NavLink to="/portfolio">Overview</NavLink>
        <NavLink to="/portfolio/positions">Positions</NavLink>
        <NavLink to="/portfolio/orders">Orders</NavLink>
        <NavLink to="/portfolio/assets">Assets</NavLink>
        <NavLink to="/portfolio/history">History</NavLink>
      </nav>
      <main className="portfolio-content">
        <Outlet />
      </main>
    </div>
  );
}

// Router configuration
const portfolioRoutes = [
  {
    path: 'portfolio',
    element: <PortfolioLayout />,
    children: [
      { index: true, element: <OverviewModule.OverviewPage /> },
      { path: 'positions', element: <PositionsModule.PositionsPage /> },
      { path: 'orders', element: <OrdersModule.OrdersPage /> },
      { path: 'assets', element: <AssetsModule.AssetsPage /> },
      { path: 'history', element: <HistoryModule.HistoryPage /> },
    ],
  },
];
```

## 3. MarketsHomePage

Markets overview with all trading pairs, stats, and funding rates.

### Import

```tsx
import { MarketsHomePage } from '@orderly.network/markets';
```

### Props

```tsx
interface MarketsHomePageProps {
  // Current symbol (for highlighting)
  symbol?: string;

  // Callback when user clicks a symbol
  onSymbolChange?: (symbol: API.Symbol) => void;

  // Funding comparison configuration
  comparisonProps?: {
    exchanges?: string[]; // Exchanges to compare funding rates
  };

  // Custom class name
  className?: string;
}
```

### Usage

```tsx
import { useNavigate } from 'react-router-dom';
import { MarketsHomePage } from '@orderly.network/markets';

function MarketsRoute() {
  const navigate = useNavigate();

  return (
    <MarketsHomePage
      onSymbolChange={(symbol) => navigate(`/perp/${symbol.symbol}`)}
      comparisonProps={{
        exchanges: ['binance', 'okx', 'bybit'],
      }}
    />
  );
}
```

**Tabs included:**

- Markets (all trading pairs with 24h stats)
- Funding (funding rate comparison across exchanges)

## 4. LeaderboardPage

Trading competition leaderboard with campaigns and rankings.

### Import

```tsx
import { LeaderboardPage } from '@orderly.network/trading-leaderboard';
```

### Usage

```tsx
import { LeaderboardPage } from '@orderly.network/trading-leaderboard';

function LeaderboardRoute() {
  return <LeaderboardPage hideCampaignsBanner={false} />;
}
```

**Sections included:**

- Active campaigns banner
- Rewards summary
- General leaderboard rankings
- Campaign-specific leaderboards
- Trading rules

## 5. Router Setup

### Complete Router Example

```tsx
import { lazy, Suspense } from 'react';
import { createBrowserRouter, Navigate } from 'react-router-dom';
import App from './App';

// Lazy load pages for better performance
const TradingPage = lazy(() => import('./pages/Trading').then((m) => ({ default: m.default })));
const PortfolioOverview = lazy(() =>
  import('@orderly.network/portfolio').then((m) => ({
    default: m.OverviewModule.OverviewPage,
  }))
);
const MarketsPage = lazy(() =>
  import('@orderly.network/markets').then((m) => ({
    default: m.MarketsHomePage,
  }))
);
const LeaderboardPage = lazy(() =>
  import('@orderly.network/trading-leaderboard').then((m) => ({
    default: m.LeaderboardPage,
  }))
);

const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    children: [
      { index: true, element: <Navigate to="/perp/PERP_ETH_USDC" /> },
      {
        path: 'perp/:symbol',
        element: (
          <Suspense fallback={<div>Loading...</div>}>
            <TradingPage />
          </Suspense>
        ),
      },
      {
        path: 'portfolio',
        children: [{ index: true, element: <PortfolioOverview /> }],
      },
      { path: 'markets', element: <MarketsPage /> },
      { path: 'leaderboard', element: <LeaderboardPage /> },
    ],
  },
]);
```

## 6. Customizing Pages

### Disable Features

```tsx
import { TradingPage, TradingFeatures } from '@orderly.network/trading';

<TradingPage
  symbol="PERP_ETH_USDC"
  tradingViewConfig={config}
  disableFeatures={[TradingFeatures.Footer, TradingFeatures.SlippageSetting]}
/>;
```

### Override Sections

```tsx
import { TradingPage, TradingFeatures } from '@orderly.network/trading';

<TradingPage
  symbol="PERP_ETH_USDC"
  tradingViewConfig={config}
  overrideFeatures={{
    [TradingFeatures.Header]: <CustomHeader />,
    [TradingFeatures.Footer]: <CustomFooter />,
  }}
/>;
```

### Custom Styling

All components accept `className` prop and use Tailwind classes with `oui-` prefix:

```tsx
<MarketsHomePage className="custom-markets-page" />
```

```css
.custom-markets-page {
  --oui-color-primary: #7b61ff;
}
```

## 7. Responsive Design

All page components automatically handle desktop and mobile layouts:

- **Desktop**: Full multi-panel layouts
- **Mobile**: Stacked layouts with bottom navigation, sheets for detail views

```tsx
import { useScreen } from '@orderly.network/ui';

function MyPage() {
  const { isMobile, isTablet, isDesktop } = useScreen();

  return isMobile ? <MobileView /> : <DesktopView />;
}
```

## Installation

```bash
npm install @orderly.network/trading \
            @orderly.network/portfolio \
            @orderly.network/markets \
            @orderly.network/trading-leaderboard \
            @orderly.network/affiliate
```

## Best Practices

1. **Lazy load pages** for better initial bundle size
2. **Persist symbol** in localStorage for user convenience
3. **Handle symbol changes** with URL updates for bookmarkable pages
4. **Configure TradingView** with custom colors matching your theme
5. **Provide share backgrounds** for PnL sharing feature
6. **Use Suspense boundaries** for smooth loading states

## Related Skills

- **orderly-sdk-dex-architecture** - Project structure and providers
- **orderly-sdk-install-dependency** - Installing packages
- **orderly-sdk-trading-workflows** - Trading functionality
- **orderly-sdk-theming** - Customizing appearance
