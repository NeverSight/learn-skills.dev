---
name: orderly-sdk-install-dependency
description: Install Orderly SDK packages and related dependencies (hooks, UI, features, wallet connectors) using the preferred package manager.
---

# Orderly Network: SDK Install Dependency

Use this skill to add Orderly SDK packages to your project. The SDK is modular—install only what you need.

## When to Use

- Starting a new DEX project
- Adding Orderly SDK to an existing project
- Installing specific packages for custom integrations
- Setting up wallet connectors

## Prerequisites

- Node.js 18+ installed
- npm, yarn, or pnpm package manager
- React 18+ project (for UI packages)

## Quick Start (Full DEX)

> **IMPORTANT**: A functional DEX requires BOTH the Orderly packages AND the wallet connector dependencies. The `@orderly.network/wallet-connector` package needs `@web3-onboard/*` packages for EVM wallets and `@solana/wallet-adapter-*` packages for Solana wallets.
>
> **Note**: `@orderly.network/hooks` is included as a transitive dependency via `@orderly.network/react-app` — you do not need to install it separately for most DEX projects. Only install it directly if you are using the hooks-only integration path without `react-app`.

```bash
# Orderly SDK packages
npm install @orderly.network/react-app \
            @orderly.network/trading \
            @orderly.network/portfolio \
            @orderly.network/markets \
            @orderly.network/wallet-connector \
            @orderly.network/i18n

# REQUIRED: EVM wallet support (MetaMask, WalletConnect, etc.)
npm install @web3-onboard/injected-wallets @web3-onboard/walletconnect

# REQUIRED: Solana wallet support (Phantom, Solflare, etc.)
npm install @solana/wallet-adapter-base @solana/wallet-adapter-wallets
```

## Package Reference

### Core Packages

| Package                      | Description                                           | Key Exports                                                                                                                    |
| ---------------------------- | ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `@orderly.network/react-app` | Main app provider, config context, error boundary     | `OrderlyAppProvider`, `useAppContext`, `useAppConfig`, `ErrorBoundary`                                                         |
| `@orderly.network/hooks`     | React hooks for trading, account, orders, positions   | `useAccount`, `useOrderEntry`, `usePositionStream`, `useOrderStream`, `useDeposit`, `useWithdraw`, `useLeverage`, `useMarkets` |
| `@orderly.network/types`     | TypeScript type definitions and constants             | `API`, `OrderType`, `OrderSide`, `OrderStatus`, `NetworkId`, `ChainConfig`                                                     |
| `@orderly.network/ui`        | Base UI components (buttons, inputs, dialogs, tables) | `Button`, `Input`, `Dialog`, `Table`, `Tabs`, `Select`, `Tooltip`, `Modal`, `Spinner`, `toast`, `OrderlyThemeProvider`         |
| `@orderly.network/i18n`      | Internationalization (i18n) support                   | `LocaleProvider`, `useTranslation`, `i18n`, `defaultLanguages`                                                                 |
| `@orderly.network/utils`     | Utility functions (formatting, math, dates)           | `formatNumber`, `Decimal`, `dayjs`                                                                                             |

```bash
npm install @orderly.network/react-app @orderly.network/hooks @orderly.network/types @orderly.network/ui @orderly.network/i18n
```

## Feature Widgets (High-Level Pages)

Complete, pre-built page components with full functionality.

| Package                                | Description                                                  | Key Exports                                                                                                               |
| -------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------- |
| `@orderly.network/trading`             | Full trading page (chart, orderbook, order entry, positions) | `TradingPage`, `OrderBook`, `LastTrades`, `AssetView`, `RiskRate`, `SplitLayout`                                          |
| `@orderly.network/portfolio`           | Portfolio dashboard (positions, orders, assets, history)     | `OverviewModule`, `PositionsModule`, `OrdersModule`, `AssetsModule`, `HistoryModule`, `FeeTierModule`, `APIManagerModule` |
| `@orderly.network/markets`             | Markets listing page with prices and stats                   | `MarketsHomePage`, `MarketsProvider`, `MarketsList`, `SymbolInfoBar`, `FundingOverview`                                   |
| `@orderly.network/vaults`              | Vault/Earn products page                                     | `VaultsPage`                                                                                                              |
| `@orderly.network/affiliate`           | Referral/affiliate program page                              | `AffiliatePage`                                                                                                           |
| `@orderly.network/trading-leaderboard` | Trading competition leaderboard                              | `LeaderboardPage`                                                                                                         |
| `@orderly.network/trading-rewards`     | Trading rewards program page                                 | `TradingRewardsPage`                                                                                                      |
| `@orderly.network/trading-points`      | Trading points/merits program page                           | `TradingPointsPage`                                                                                                       |

```bash
npm install @orderly.network/trading @orderly.network/portfolio @orderly.network/markets
```

## Wallet Connectors

Choose **one** wallet connection strategy.

| Package                                   | Description                                         | Key Exports               |
| ----------------------------------------- | --------------------------------------------------- | ------------------------- |
| `@orderly.network/wallet-connector`       | Standard connector (Web3-Onboard + Solana adapters) | `WalletConnectorProvider` |
| `@orderly.network/wallet-connector-privy` | Privy connector (social login, embedded wallets)    | `PrivyConnectorProvider`  |

**Option A: Standard Wallet Connector (Recommended)**

Supports EVM (MetaMask, WalletConnect, Binance, etc.) and Solana (Phantom, Solflare).

> **Note**: The `@orderly.network/wallet-connector` works with sensible defaults. Installing the underlying wallet packages (`@web3-onboard/*`, `@solana/wallet-adapter-*`) is optional and only needed for custom wallet configuration (e.g., adding WalletConnect with a project ID). The official templates use `<WalletConnectorProvider>` with no props and no extra wallet packages.

```bash
# Main connector package
npm install @orderly.network/wallet-connector

# Optional: EVM wallet packages (for custom WalletConnect, etc.)
npm install @web3-onboard/injected-wallets @web3-onboard/walletconnect

# Optional: Solana wallet packages (for custom Solana wallet config)
npm install @solana/wallet-adapter-base @solana/wallet-adapter-wallets
```

**Option B: Privy Connector**

For social login (Google, email, etc.) and embedded wallets.

```bash
npm install @orderly.network/wallet-connector-privy @privy-io/react-auth
```

## UI Sub-Packages (Granular Components)

Individual UI modules for custom integrations. These are dependencies of `@orderly.network/trading` and `@orderly.network/portfolio`, but can be installed separately.

| Package                              | Description                                   | Key Exports                                                                                                |
| ------------------------------------ | --------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `@orderly.network/ui-scaffold`       | App layout scaffold, navigation, account menu | `Scaffold`, `MainNavWidget`, `BottomNavWidget`, `AccountMenuWidget`, `ChainMenuWidget`, `SideNavbarWidget` |
| `@orderly.network/ui-order-entry`    | Order entry form component                    | `OrderEntry`                                                                                               |
| `@orderly.network/ui-positions`      | Positions table component                     | `PositionsView`                                                                                            |
| `@orderly.network/ui-orders`         | Orders table component                        | `OrdersView`                                                                                               |
| `@orderly.network/ui-transfer`       | Deposit/withdraw/transfer dialogs             | `DepositWidget`, `WithdrawWidget`                                                                          |
| `@orderly.network/ui-leverage`       | Leverage selector component                   | `LeverageWidget`                                                                                           |
| `@orderly.network/ui-tpsl`           | Take profit / stop loss form                  | `TPSLWidget`                                                                                               |
| `@orderly.network/ui-share`          | PnL sharing card generator                    | `SharePnL`                                                                                                 |
| `@orderly.network/ui-chain-selector` | Chain/network selector dropdown               | `ChainSelector`                                                                                            |
| `@orderly.network/ui-connector`      | Wallet connect button & modal                 | `ConnectWalletButton`                                                                                      |
| `@orderly.network/ui-tradingview`    | TradingView chart wrapper                     | `TradingViewChart`                                                                                         |
| `@orderly.network/ui-notification`   | Notification center                           | `NotificationWidget`                                                                                       |

```bash
npm install @orderly.network/ui-scaffold @orderly.network/ui-order-entry
```

## Low-Level Packages

For advanced customization or non-React environments.

| Package                                   | Description                                          | Key Exports                                                   |
| ----------------------------------------- | ---------------------------------------------------- | ------------------------------------------------------------- |
| `@orderly.network/core`                   | Low-level API client, signing, key management        | `Account`, `ConfigStore`, `WalletAdapter`, `signMessage`      |
| `@orderly.network/perp`                   | Perpetual trading calculations (margin, liquidation) | `calcMargin`, `calcLiqPrice`, `calcPnL`, `calcIMR`, `calcMMR` |
| `@orderly.network/net`                    | Network/WebSocket layer                              | `WebSocketClient`, `EventEmitter`                             |
| `@orderly.network/default-evm-adapter`    | Default EVM wallet adapter                           | `EVMAdapter`                                                  |
| `@orderly.network/default-solana-adapter` | Default Solana wallet adapter                        | `SolanaAdapter`                                               |

```bash
npm install @orderly.network/core @orderly.network/perp
```

## Installation by Use Case

### Minimal Setup (Hooks Only)

For building fully custom UI with hooks.

```bash
npm install @orderly.network/react-app \
            @orderly.network/hooks \
            @orderly.network/types \
            @orderly.network/wallet-connector
```

### Full DEX with All Features

```bash
npm install @orderly.network/react-app \
            @orderly.network/trading \
            @orderly.network/portfolio \
            @orderly.network/markets \
            @orderly.network/vaults \
            @orderly.network/affiliate \
            @orderly.network/trading-leaderboard \
            @orderly.network/wallet-connector \
            @orderly.network/i18n \
            @orderly.network/ui
```

### Custom UI with Scaffold Layout

```bash
npm install @orderly.network/react-app \
            @orderly.network/hooks \
            @orderly.network/ui \
            @orderly.network/ui-scaffold \
            @orderly.network/ui-order-entry \
            @orderly.network/ui-positions \
            @orderly.network/wallet-connector
```

### Privy (Social Login) Setup

```bash
npm install @orderly.network/react-app \
            @orderly.network/trading \
            @orderly.network/wallet-connector-privy \
            @privy-io/react-auth
```

## Peer Dependencies

All packages require:

```json
{
  "peerDependencies": {
    "react": ">=18",
    "react-dom": ">=18"
  }
}
```

## Tailwind CSS Setup

The UI packages require Tailwind CSS with the Orderly preset:

```bash
npm install -D tailwindcss postcss autoprefixer
```

**tailwind.config.ts:**

```ts
import { OUITailwind } from '@orderly.network/ui';

export default {
  content: ['./src/**/*.{js,ts,jsx,tsx}', './node_modules/@orderly.network/**/*.{js,mjs}'],
  presets: [OUITailwind.preset],
};
```

**CSS entry file:**

> **Important**: Only `@orderly.network/ui` has a CSS file. Other packages (`trading`, `portfolio`, `markets`) do NOT have separate CSS files—they use the base UI styles.

```css
/* Only import from @orderly.network/ui - other packages don't have CSS files */
@import '@orderly.network/ui/dist/styles.css';

@tailwind base;
@tailwind components;
@tailwind utilities;
```

## Vite Polyfills (Required)

The wallet connector packages use Node.js built-ins like `Buffer`. You must add polyfills for browser compatibility:

```bash
npm install -D vite-plugin-node-polyfills
```

**vite.config.ts:**

```ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { nodePolyfills } from 'vite-plugin-node-polyfills';

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
});
```

## Version Compatibility

All `@orderly.network/*` packages should use the same version to ensure compatibility.

```json
{
  "dependencies": {
    "@orderly.network/react-app": "^2.8.0",
    "@orderly.network/trading": "^2.8.0",
    "@orderly.network/hooks": "^2.8.0",
    "@orderly.network/ui": "^2.8.0"
  }
}
```

## Package Manager Commands

**npm:**

```bash
npm install <package-name>
```

**yarn:**

```bash
yarn add <package-name>
```

**pnpm:**

```bash
pnpm add <package-name>
```

## Related Skills

- **orderly-sdk-dex-architecture** - Project structure and provider setup
- **orderly-sdk-wallet-connection** - Wallet integration details
- **orderly-sdk-page-components** - Using pre-built page components
- **orderly-sdk-trading-workflows** - End-to-end trading implementation
- **orderly-sdk-theming** - Customizing the UI appearance
