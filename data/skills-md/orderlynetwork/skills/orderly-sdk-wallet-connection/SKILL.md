---
name: orderly-sdk-wallet-connection
description: Comprehensive guide to integrating wallet connection in Orderly Network DEX applications, supporting both EVM (Ethereum, Arbitrum, etc.) and Solana wallets.
---

# Orderly Network: SDK Wallet Connection

A comprehensive guide to integrating wallet connection in Orderly Network DEX applications, supporting both EVM (Ethereum, Arbitrum, etc.) and Solana wallets.

## When to Use

- Setting up wallet connection for a new DEX
- Supporting multiple wallet types (MetaMask, Phantom, etc.)
- Implementing chain switching
- Managing authentication state

## Prerequisites

- Orderly SDK packages installed
- Providers configured (see `orderly-sdk-dex-architecture`)
- Wallet packages installed (`@web3-onboard/*`, `@solana/wallet-adapter-*`)

## Overview

Orderly Network supports **omnichain trading**, meaning users can connect wallets from multiple blockchain ecosystems:

- **EVM Chains**: Ethereum, Arbitrum, Optimism, Base, Polygon, BSC, Avalanche, etc.
- **Solana**: Mainnet and Devnet

The SDK provides a unified wallet connection layer that abstracts the differences between these ecosystems.

## Wallet Connector Package

> **Note**: The `@orderly.network/wallet-connector` package works out of the box with sensible defaults. Both `solanaInitial` and `evmInitial` props are **optional**.

```bash
# Main connector package
npm install @orderly.network/wallet-connector

# Optional: EVM wallet packages (for custom wallet config like WalletConnect)
npm install @web3-onboard/injected-wallets @web3-onboard/walletconnect

# Optional: Solana wallet packages (for custom Solana wallet config)
npm install @solana/wallet-adapter-base @solana/wallet-adapter-wallets
```

### Required Dependencies Summary

| Package                          | Purpose                                | Required For                    |
| -------------------------------- | -------------------------------------- | ------------------------------- |
| `@web3-onboard/injected-wallets` | MetaMask, Coinbase Wallet, Rabby, etc. | EVM wallet connection           |
| `@web3-onboard/walletconnect`    | WalletConnect protocol                 | Mobile & multi-platform wallets |
| `@solana/wallet-adapter-base`    | Solana wallet adapter base             | All Solana wallets              |
| `@solana/wallet-adapter-wallets` | Phantom, Solflare, Ledger adapters     | Solana wallet connection        |

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    WalletConnectorProvider                   │
│  ┌───────────────────────────────────────────────────────┐   │
│  │                   SolanaProvider                      │   │
│  │  (ConnectionProvider + WalletProvider + ModalProvider)│   │
│  │  ┌───────────────────────────────────────────────┐    │   │
│  │  │                   InitEvm                     │    │   │
│  │  │  (Web3OnboardProvider for EVM wallets)        │    │   │
│  │  │  ┌─────────────────────────────────────────┐  │    │   │
│  │  │  │                  Main                   │  │    │   │
│  │  │  │  (WalletConnectorContext - unified API) │  │    │   │
│  │  │  │  ┌─────────────────────────────────┐    │  │    │   │
│  │  │  │  │         Your App                │    │  │    │   │
│  │  │  │  └─────────────────────────────────┘    │  │    │   │
│  │  │  └─────────────────────────────────────────┘  │    │   │
│  │  └───────────────────────────────────────────────┘    │   │
│  └───────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘
```

## Basic Setup

**IMPORTANT**: The `networkId` must be consistent between `WalletConnectorProvider` (Solana network) and `OrderlyAppProvider`.

### 1. WalletConnectorProvider

Wrap your app with the `WalletConnectorProvider`.

**Minimal Setup (uses defaults):**

```tsx
import { WalletConnectorProvider } from '@orderly.network/wallet-connector';
import { OrderlyAppProvider } from '@orderly.network/react-app';
import type { NetworkId } from '@orderly.network/types';

function App() {
  const networkId: NetworkId = 'mainnet';

  return (
    <WalletConnectorProvider>
      <OrderlyAppProvider
        brokerId="your_broker_id"
        brokerName="Your DEX Name"
        networkId={networkId}
      >
        <YourApp />
      </OrderlyAppProvider>
    </WalletConnectorProvider>
  );
}
```

**Custom Setup (explicit wallet configuration):**

```tsx
import { WalletConnectorProvider } from '@orderly.network/wallet-connector';
import { WalletAdapterNetwork } from '@solana/wallet-adapter-base';
import { OrderlyAppProvider } from '@orderly.network/react-app';
import type { NetworkId } from '@orderly.network/types';

function App() {
  const networkId: NetworkId = 'mainnet';

  return (
    <WalletConnectorProvider
      solanaInitial={{
        network:
          networkId === 'mainnet' ? WalletAdapterNetwork.Mainnet : WalletAdapterNetwork.Devnet,
        wallets: getSolanaWallets(),
      }}
      evmInitial={{
        options: {
          wallets: getEvmWallets(),
          appMetadata: {
            name: 'My DEX',
            description: 'Decentralized Exchange',
          },
        },
      }}
    >
      <OrderlyAppProvider
        brokerId="your_broker_id"
        brokerName="Your DEX Name"
        networkId={networkId}
      >
        <YourApp />
      </OrderlyAppProvider>
    </WalletConnectorProvider>
  );
}
```

### 2. Configure EVM Wallets

```tsx
import injectedOnboard from '@web3-onboard/injected-wallets';
import walletConnectOnboard from '@web3-onboard/walletconnect';
import binanceWallet from '@binance/w3w-blocknative-connector';

export function getEvmWallets() {
  const walletConnectProjectId = 'YOUR_WALLETCONNECT_PROJECT_ID';

  return [
    // Injected wallets (MetaMask, Rabby, Coinbase, etc.)
    injectedOnboard(),

    // Binance Web3 Wallet
    binanceWallet({ options: { lng: 'en' } }),

    // WalletConnect (for mobile wallets)
    walletConnectOnboard({
      projectId: walletConnectProjectId,
      qrModalOptions: { themeMode: 'dark' },
      dappUrl: window.location.origin,
    }),
  ];
}
```

### 3. Configure Solana Wallets

```tsx
import { WalletAdapterNetwork } from '@solana/wallet-adapter-base';
import {
  PhantomWalletAdapter,
  SolflareWalletAdapter,
  LedgerWalletAdapter,
} from '@solana/wallet-adapter-wallets';

export function getSolanaWallets(networkId: 'mainnet' | 'testnet') {
  return [new PhantomWalletAdapter(), new SolflareWalletAdapter(), new LedgerWalletAdapter()];
}
```

## Using Wallet Connection

### Access Wallet Context

The SDK provides a unified `WalletConnectorContext`:

```tsx
import { useContext } from 'react';
import { WalletConnectorContext } from '@orderly.network/hooks';

function WalletStatus() {
  const {
    connect, // Connect wallet function
    disconnect, // Disconnect wallet function
    connecting, // Boolean: connection in progress
    wallet, // Connected wallet info
    connectedChain, // Current chain info
    setChain, // Switch chain function
    namespace, // "evm" | "solana" | null
  } = useContext(WalletConnectorContext);

  return (
    <div>
      {wallet ? (
        <>
          <p>Connected: {wallet.accounts[0].address}</p>
          <p>Chain: {connectedChain?.id}</p>
          <button onClick={disconnect}>Disconnect</button>
        </>
      ) : (
        <button onClick={() => connect({ chainId: 42161 })}>Connect Wallet</button>
      )}
    </div>
  );
}
```

### Connect to Specific Chain

```tsx
const { connect } = useContext(WalletConnectorContext);

// Connect to EVM chain (Arbitrum)
await connect({ chainId: 42161 });

// Connect to Solana
await connect({ chainId: 900900900 }); // Solana mainnet
```

### Switch Chains

```tsx
const { setChain, connectedChain } = useContext(WalletConnectorContext);

// Switch to Optimism
await setChain({ chainId: '0xa' }); // Hex format for EVM

// Switch to Base
await setChain({ chainId: '0x2105' });
```

## Account State Machine

After wallet connection, users need to complete Orderly account setup:

```
NotConnected (0) → Connected (1) → NotSignedIn (2) → SignedIn (3)
                                              ↓
                                        EnableTrading (5)
```

### Using useAccount Hook

```tsx
import { useAccount, AccountStatusEnum } from '@orderly.network/hooks';

function AccountStatus() {
  const { account, state, createOrderlyKey, createAccount, disconnect } = useAccount();

  switch (state.status) {
    case AccountStatusEnum.NotConnected:
      return <ConnectWalletButton />;

    case AccountStatusEnum.Connected:
      return <button onClick={() => createAccount()}>Create Orderly Account</button>;

    case AccountStatusEnum.NotSignedIn:
      return <button onClick={() => createOrderlyKey()}>Enable Trading</button>;

    case AccountStatusEnum.SignedIn:
      return <TradingInterface />;
  }
}
```

## UI Components for Wallet Connection

### WalletConnectorWidget

Pre-built wallet connection UI:

```tsx
import { WalletConnectorWidget, WalletConnectorModalId } from '@orderly.network/ui-connector';
import { modal } from '@orderly.network/ui';

// Show wallet connect modal
function ConnectButton() {
  return <button onClick={() => modal.show(WalletConnectorModalId)}>Connect Wallet</button>;
}
```

### AuthGuard

Wrap content that requires authentication:

```tsx
import { AuthGuard } from '@orderly.network/ui-connector';

function TradingPage() {
  return (
    <AuthGuard fallback={<ConnectPrompt />}>
      <OrderEntry symbol="PERP_ETH_USDC" />
    </AuthGuard>
  );
}
```

### useAuthGuard Hook

```tsx
import { useAuthGuard } from '@orderly.network/ui-connector';

function TradeButton() {
  const { isAuthenticated, triggerAuth } = useAuthGuard();

  const handleClick = () => {
    if (!isAuthenticated) {
      triggerAuth();
      return;
    }
    // Proceed with trade
  };

  return <button onClick={handleClick}>Trade</button>;
}
```

## Supported Chains

### EVM Mainnet Chains

| Chain     | Chain ID | Network |
| --------- | -------- | ------- |
| Ethereum  | 1        | mainnet |
| Arbitrum  | 42161    | mainnet |
| Optimism  | 10       | mainnet |
| Base      | 8453     | mainnet |
| Polygon   | 137      | mainnet |
| BSC       | 56       | mainnet |
| Avalanche | 43114    | mainnet |
| Mantle    | 5000     | mainnet |
| SEI       | 1329     | mainnet |

### EVM Testnet Chains

| Chain            | Chain ID | Network |
| ---------------- | -------- | ------- |
| Arbitrum Sepolia | 421614   | testnet |
| BSC Testnet      | 97       | testnet |
| Monad Testnet    | 10143    | testnet |

### Solana

| Network | Chain ID (Internal) |
| ------- | ------------------- |
| Mainnet | 900900900           |
| Devnet  | 901901901           |

## Chain Filtering

Restrict which chains users can connect to:

```tsx
<OrderlyAppProvider
  brokerId="your_broker_id"
  networkId="mainnet"
  chainFilter={{
    mainnet: [
      { id: 42161 }, // Arbitrum only
      { id: 10 },    // Optimism
    ],
    testnet: [
      { id: 421614 }, // Arbitrum Sepolia
    ],
  }}
>
```

## Handling Chain Changes

```tsx
<OrderlyAppProvider
  brokerId="your_broker_id"
  networkId="mainnet"
  onChainChanged={(chainId, { isTestnet }) => {
    console.log(`Switched to chain ${chainId}`);

    // Reload if switching between mainnet/testnet
    if (isTestnet && networkId === "mainnet") {
      localStorage.setItem("network", "testnet");
      window.location.reload();
    }
  }}
>
```

## Privy Integration (Alternative)

For social login support, use Privy:

```bash
npm install @orderly.network/wallet-connector-privy
```

```tsx
import { WalletConnectorPrivy } from "@orderly.network/wallet-connector-privy";

<WalletConnectorPrivy
  appId="YOUR_PRIVY_APP_ID"
  loginMethods={["email", "google", "twitter"]}
>
  <OrderlyAppProvider ...>
    <App />
  </OrderlyAppProvider>
</WalletConnectorPrivy>
```

## Error Handling

```tsx
import { useEventEmitter } from '@orderly.network/hooks';

function WalletErrorHandler() {
  const ee = useEventEmitter();

  useEffect(() => {
    const handleError = (error: { message: string }) => {
      toast.error(error.message);
    };

    ee.on('wallet:connect-error', handleError);

    return () => {
      ee.off('wallet:connect-error', handleError);
    };
  }, [ee]);

  return null;
}
```

## Best Practices

### 1. Check Wallet Connection Before Actions

```tsx
const { wallet } = useContext(WalletConnectorContext);
if (!wallet) {
  modal.show(WalletConnectorModalId);
  return;
}
```

### 2. Use AuthGuard for Protected Content

```tsx
<AuthGuard>
  <ProtectedTradingUI />
</AuthGuard>
```

### 3. Handle Network Mismatches

```tsx
const { connectedChain } = useContext(WalletConnectorContext);
const expectedChainId = networkId === 'mainnet' ? 42161 : 421614;

if (connectedChain?.id !== expectedChainId) {
  return <SwitchNetworkPrompt />;
}
```

### 4. Persist Network Selection

```tsx
const NETWORK_KEY = 'orderly_network_id';

function getNetworkId(): NetworkId {
  return (localStorage.getItem(NETWORK_KEY) as NetworkId) || 'mainnet';
}
```

## Related Skills

- **orderly-sdk-dex-architecture** - Provider setup and configuration
- **orderly-sdk-install-dependency** - Installing wallet packages
- **orderly-sdk-trading-workflows** - Trading implementation
- **orderly-sdk-debugging** - Troubleshooting wallet issues
- **orderly-api-authentication** - Understanding the auth flow
