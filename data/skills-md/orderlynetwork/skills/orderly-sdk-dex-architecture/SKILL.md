---
name: orderly-sdk-dex-architecture
description: Complete DEX architecture guide including project structure, provider hierarchy, network configuration, TradingView setup, and provider configuration.
---

# Orderly Network: SDK DEX Architecture

A comprehensive guide to architecting and scaffolding a complete DEX application using the Orderly Network Components SDK.

## When to Use

- Setting up a new DEX project
- Understanding the provider hierarchy
- Configuring network settings
- Setting up TradingView charts
- Understanding runtime configuration

## Prerequisites

- Node.js 18+ installed
- Orderly SDK packages installed (see `orderly-sdk-install-dependency`)
- React 18+ project with TypeScript
- Vite or similar build tool

## Overview

This skill covers the complete architecture for building a production-ready DEX:

- Project structure and setup
- Provider hierarchy and configuration
- **Network configuration (REQUIRED)** - mainnet/testnet and supported chains
- **TradingView chart setup (REQUIRED for charts)** - charting library files
- Routing and page components
- Runtime configuration
- Build and deployment

**Critical Configuration**: Every DEX must have:

1. `brokerId` - Your Orderly broker ID
2. `networkId` - Either "mainnet" or "testnet"
3. Proper wallet connector setup with matching network
4. TradingView charting library in `public/tradingview/` (for chart functionality)

## Project Structure

```
my-dex/
├── public/
│   ├── config.js              # Runtime configuration
│   ├── favicon.webp
│   ├── locales/               # i18n translations
│   │   ├── en.json
│   │   └── extend/            # Custom translations
│   ├── pnl/                   # PnL share poster backgrounds
│   │   ├── poster_bg_1.png
│   │   └── poster_bg_2.png
│   └── tradingview/           # TradingView library (REQUIRED for charts)
│       ├── chart.css          # Custom chart styles
│       └── charting_library/  # TradingView charting library files
├── src/
│   ├── main.tsx               # Entry point
│   ├── App.tsx                # Root component with router
│   ├── components/
│   │   ├── orderlyProvider/   # SDK provider setup
│   │   │   ├── index.tsx      # Main provider wrapper
│   │   │   └── walletConnector.tsx
│   │   ├── ErrorBoundary.tsx
│   │   └── LoadingSpinner.tsx
│   ├── pages/
│   │   ├── perp/              # Trading pages
│   │   ├── portfolio/         # Portfolio pages
│   │   ├── markets/           # Markets pages
│   │   └── leaderboard/       # Leaderboard pages
│   ├── utils/
│   │   ├── config.tsx         # App configuration
│   │   ├── walletConfig.ts    # Wallet setup
│   │   ├── runtime-config.ts  # Runtime config loader
│   │   └── storage.ts         # Local storage utils
│   └── styles/
│       └── index.css          # Global styles + Tailwind
├── .env                       # Build-time env vars
├── index.html
├── package.json
├── tailwind.config.ts
├── tsconfig.json
└── vite.config.ts
```

## Provider Hierarchy

The SDK requires a specific provider nesting order:

```
LocaleProvider (i18n)
└── WalletConnectorProvider (or Privy)
    └── OrderlyAppProvider
        ├── (internal) AppConfigProvider
        ├── (internal) OrderlyThemeProvider
        ├── (internal) OrderlyConfigProvider (from hooks)
        ├── (internal) AppStateProvider
        ├── (internal) UILocaleProvider
        ├── (internal) TooltipProvider
        ├── (internal) ModalProvider
        └── Your App
```

> **Note**: `TooltipProvider` and `ModalProvider` are managed internally by `OrderlyAppProvider`. You do **not** need to add them yourself.

## Main Provider Component

```tsx
// src/components/orderlyProvider/index.tsx
import { ReactNode, useCallback, Suspense, lazy } from 'react';
import { OrderlyAppProvider } from '@orderly.network/react-app';
import { LocaleProvider, LocaleCode, defaultLanguages } from '@orderly.network/i18n';
import type { NetworkId } from '@orderly.network/types';
import { useOrderlyConfig } from '@/utils/config';
import { getRuntimeConfig, getRuntimeConfigBoolean } from '@/utils/runtime-config';

const NETWORK_ID_KEY = 'orderly_network_id';

const getNetworkId = (): NetworkId => {
  if (typeof window === 'undefined') return 'mainnet';

  const disableMainnet = getRuntimeConfigBoolean('VITE_DISABLE_MAINNET');
  const disableTestnet = getRuntimeConfigBoolean('VITE_DISABLE_TESTNET');

  if (disableMainnet && !disableTestnet) return 'testnet';
  if (disableTestnet && !disableMainnet) return 'mainnet';

  return (localStorage.getItem(NETWORK_ID_KEY) as NetworkId) || 'mainnet';
};

const WalletConnector = lazy(() => import('./walletConnector'));

const OrderlyProvider = ({ children }: { children: ReactNode }) => {
  const config = useOrderlyConfig();
  const networkId = getNetworkId();

  const onChainChanged = useCallback((_chainId: number, { isTestnet }: { isTestnet: boolean }) => {
    const currentNetworkId = getNetworkId();
    if (
      (isTestnet && currentNetworkId === 'mainnet') ||
      (!isTestnet && currentNetworkId === 'testnet')
    ) {
      const newNetworkId: NetworkId = isTestnet ? 'testnet' : 'mainnet';
      localStorage.setItem(NETWORK_ID_KEY, newNetworkId);
      window.location.reload();
    }
  }, []);

  const onLanguageChanged = (lang: LocaleCode) => {
    const url = new URL(window.location.href);
    if (lang === 'en') {
      url.searchParams.delete('lang');
    } else {
      url.searchParams.set('lang', lang);
    }
    window.history.replaceState({}, '', url.toString());
  };

  return (
    <LocaleProvider onLanguageChanged={onLanguageChanged} locale="en" languages={defaultLanguages}>
      <Suspense fallback={<LoadingSpinner />}>
        <WalletConnector networkId={networkId}>
          <OrderlyAppProvider
            brokerId={getRuntimeConfig('VITE_ORDERLY_BROKER_ID')}
            brokerName={getRuntimeConfig('VITE_ORDERLY_BROKER_NAME')}
            networkId={networkId}
            onChainChanged={onChainChanged}
            appIcons={config.appIcons}
          >
            {children}
          </OrderlyAppProvider>
        </WalletConnector>
      </Suspense>
    </LocaleProvider>
  );
};

export default OrderlyProvider;
```

## Wallet Connector Setup

> **Note**: Both `solanaInitial` and `evmInitial` props on `WalletConnectorProvider` are **optional**. The provider has sensible defaults and the official templates use it with no props. Pass these props only if you need to customize wallet configuration.

**Minimal Setup (recommended — uses defaults):**

```tsx
// src/components/orderlyProvider/walletConnector.tsx
import { ReactNode } from 'react';
import { WalletConnectorProvider } from '@orderly.network/wallet-connector';
import type { NetworkId } from '@orderly.network/types';

interface Props {
  children: ReactNode;
  networkId: NetworkId;
}

const WalletConnector = ({ children, networkId }: Props) => {
  return <WalletConnectorProvider>{children}</WalletConnectorProvider>;
};

export default WalletConnector;
```

## Network Configuration (REQUIRED)

**IMPORTANT**: Every Orderly DEX must configure the network properly.

### Supported Networks

**Mainnet Chains (Production)**

| Chain    | Chain ID | Description           |
| -------- | -------- | --------------------- |
| Arbitrum | 42161    | Primary mainnet chain |
| Optimism | 10       | OP mainnet            |
| Base     | 8453     | Base mainnet          |
| Ethereum | 1        | Ethereum mainnet      |
| Solana   | N/A      | Solana mainnet        |

**Testnet Chains (Development)**

| Chain            | Chain ID  | Description           |
| ---------------- | --------- | --------------------- |
| Arbitrum Sepolia | 421614    | Primary testnet chain |
| Base Sepolia     | 84532     | Base testnet          |
| Solana Devnet    | 901901901 | Solana devnet         |

### Network ID Configuration

The `networkId` prop determines whether your DEX connects to mainnet or testnet.

```tsx
import type { NetworkId } from '@orderly.network/types';

// Network ID must be "mainnet" or "testnet"
const networkId: NetworkId = 'mainnet'; // or "testnet"
```

### Complete Provider Setup with Network Config

```tsx
<WalletConnectorProvider
  solanaInitial={{
    network: networkId === "mainnet"
      ? WalletAdapterNetwork.Mainnet
      : WalletAdapterNetwork.Devnet,
    wallets: [],
  }}
  evmInitial={{
    options: {
      wallets: [],
    },
  }}
>
  <OrderlyAppProvider
    brokerId="your_broker_id"
    brokerName="Your DEX Name"
    networkId={networkId}
    onChainChanged={onChainChanged}
  >
```

## Runtime Configuration

Use runtime configuration for deployment flexibility:

### public/config.js

```javascript
window.__RUNTIME_CONFIG__ = {
  VITE_ORDERLY_BROKER_ID: 'your_broker_id',
  VITE_ORDERLY_BROKER_NAME: 'Your DEX Name',
  VITE_DISABLE_MAINNET: 'false',
  VITE_DISABLE_TESTNET: 'false',
  VITE_DEFAULT_CHAIN: '42161',
};
```

### Runtime Config Loader

```tsx
// src/utils/runtime-config.ts

export function getRuntimeConfig(key: string): string {
  if (typeof window !== 'undefined' && window.__RUNTIME_CONFIG__?.[key]) {
    return window.__RUNTIME_CONFIG__[key];
  }
  return import.meta.env[key] || '';
}

export function getRuntimeConfigBoolean(key: string): boolean {
  return getRuntimeConfig(key) === 'true';
}

export function getRuntimeConfigArray(key: string): string[] {
  const value = getRuntimeConfig(key);
  if (!value) return [];
  return value
    .split(',')
    .map((s) => s.trim())
    .filter(Boolean);
}

declare global {
  interface Window {
    __RUNTIME_CONFIG__?: Record<string, string>;
  }
}
```

## App Root Component

```tsx
// src/App.tsx
import { Outlet } from 'react-router-dom';
import { Suspense } from 'react';
import OrderlyProvider from '@/components/orderlyProvider';
import { LoadingSpinner } from '@/components/LoadingSpinner';
import { ErrorBoundary } from '@/components/ErrorBoundary';

export default function App() {
  return (
    <ErrorBoundary>
      <OrderlyProvider>
        <Suspense fallback={<LoadingSpinner />}>
          <Outlet />
        </Suspense>
      </OrderlyProvider>
    </ErrorBoundary>
  );
}
```

## TradingView Chart Setup (REQUIRED)

> **CRITICAL**: The TradingView charting library must be manually added to your `public/tradingview/` folder.

### Required Files Structure

```
public/
└── tradingview/
    ├── chart.css                    # Optional: custom chart styling
    └── charting_library/            # REQUIRED: TradingView library
        ├── charting_library.js      # Main library script
        ├── charting_library.d.ts
        └── ... (other library files)
```

### How to Get TradingView Library

1. **Request access** from TradingView: https://www.tradingview.com/HTML5-stock-forex-bitcoin-charting-library/
2. **Download** the charting library package
3. **Copy** the `charting_library` folder to your `public/tradingview/` directory

### TradingView Configuration

```tsx
// In your TradingPage component
<TradingPage
  symbol={symbol}
  tradingViewConfig={{
    scriptSRC: '/tradingview/charting_library/charting_library.js',
    library_path: '/tradingview/charting_library/',
    customCssUrl: '/tradingview/chart.css',
    colorConfig: {
      upColor: '#26a69a',
      downColor: '#ef5350',
    },
  }}
/>
```

## Tailwind Configuration

### tailwind.config.ts

```ts
import type { Config } from 'tailwindcss';
import { OUITailwind } from '@orderly.network/ui';

export default {
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
    './node_modules/@orderly.network/**/*.{js,mjs}',
  ],
  presets: [OUITailwind.preset],
  theme: {
    extend: {},
  },
  plugins: [],
} satisfies Config;
```

### src/styles/index.css

```css
@import '@orderly.network/ui/dist/styles.css';

@tailwind base;
@tailwind components;
@tailwind utilities;
```

## Vite Configuration

> **Important**: The wallet connector packages use Node.js built-ins like `Buffer`. You must add polyfills.

```bash
npm install -D vite-plugin-node-polyfills
```

### vite.config.ts

```ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { nodePolyfills } from 'vite-plugin-node-polyfills';
import path from 'path';

export default defineConfig({
  plugins: [
    react(),
    nodePolyfills({
      include: ['buffer', 'crypto', 'stream', 'util'],
      globals: {
        Buffer: true,
        global: true,
        process: true,
      },
    }),
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});
```

## Checklist for Production

- [ ] Broker ID configured
- [ ] WalletConnect project ID (for mobile wallets)
- [ ] Runtime config.js deployed
- [ ] TradingView library (if using charts)
- [ ] Custom branding (logo, favicon, colors)
- [ ] Error tracking (Sentry, etc.)
- [ ] Analytics integration
- [ ] SSL/HTTPS enabled

## Related Skills

- **orderly-sdk-install-dependency** - SDK package installation
- **orderly-sdk-wallet-connection** - Wallet integration details
- **orderly-sdk-page-components** - Using pre-built page components
- **orderly-sdk-trading-workflows** - End-to-end trading implementation
- **orderly-sdk-theming** - Customizing the UI appearance
- **orderly-sdk-debugging** - Troubleshooting common issues
