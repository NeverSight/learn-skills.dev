---
name: dapp-integration
description: Build Midnight dApps with TypeScript integration, wallet connectivity, and contract deployment. Use when connecting wallets, deploying contracts, or building dApp frontends. Triggers on wallet, provider, Next.js, deployment, or TypeScript integration questions.
---

# Midnight dApp Integration

Build privacy-preserving dApps with TypeScript, React/Next.js, and Midnight Network integration.

## Quick Start

```typescript
// Connect to Lace wallet
const connector = window.midnight?.mnLace;
if (connector) {
  const api = await connector.enable();
  const state = await api.state();
  console.log('Connected:', state.address);
}
```

## Core Concepts

| Component          | Purpose                             |
| ------------------ | ----------------------------------- |
| **DApp Connector** | Wallet detection & connection       |
| **Providers**      | Contract interaction infrastructure |
| **Contract API**   | Type-safe circuit calls             |
| **Proof Server**   | ZK proof generation                 |

## Reference Files

| Topic                   | Resource                                                           |
| ----------------------- | ------------------------------------------------------------------ |
| **Wallet Connection**   | [references/wallet-connection.md](references/wallet-connection.md) |
| **Provider Setup**      | [references/providers.md](references/providers.md)                 |
| **Contract Deployment** | [references/deployment.md](references/deployment.md)               |
| **Next.js Setup**       | [references/nextjs-setup.md](references/nextjs-setup.md)           |

## Assets

| Asset                                          | Description            |
| ---------------------------------------------- | ---------------------- |
| [assets/wallet-hook.md](assets/wallet-hook.md) | React hook for wallet  |
| [assets/providers.md](assets/providers.md)     | Provider configuration |
| [assets/deploy.md](assets/deploy.md)           | Deployment template    |

## Installation

```bash
npm install @midnight-ntwrk/dapp-connector-api \
  @midnight-ntwrk/midnight-js-contracts \
  @midnight-ntwrk/midnight-js-types \
  @midnight-ntwrk/midnight-js-network-id
```

> Note: The `@midnight-ntwrk/dapp-connector-api` npm page currently warns that its source repo
> "hasn't been fully migrated" and points to
> <https://github.com/input-output-hk/midnight-dapp-connector-api>.
> Use the Network Support Matrix for version compatibility.

## Wallet Detection

```typescript
// Check if Lace wallet is installed
function isWalletInstalled(): boolean {
  return typeof window !== 'undefined' && !!window.midnight?.mnLace;
}

// Type definition
import '@midnight-ntwrk/dapp-connector-api';
// Types are augmented on window.midnight.mnLace
```

## Provider Stack

```text
┌─────────────────────────────────────┐
│         Contract Instance           │
├─────────────────────────────────────┤
│      midnightProvider (wallet)      │
├─────────────────────────────────────┤
│    zkConfigProvider (circuit cfg)   │
├─────────────────────────────────────┤
│   publicDataProvider (indexer)      │
├─────────────────────────────────────┤
│  privateStateProvider (local state) │
└─────────────────────────────────────┘
```

## Basic Flow

1. **Detect wallet** - Check `window.midnight`
2. **Connect** - Call `connector.enable()`
3. **Setup providers** - Configure state, indexer, ZK
4. **Deploy/Connect** - Deploy new or connect to existing
5. **Call circuits** - Type-safe contract interaction

## Network Configuration

```typescript
// Testnet endpoints
const TESTNET = {
  indexer: 'https://indexer.testnet-02.midnight.network/api/v1/graphql',
  indexerWS: 'wss://indexer.testnet-02.midnight.network/api/v1/graphql/ws',
  proofServer: 'http://localhost:6300',
  node: 'https://rpc.testnet-02.midnight.network',
};
```

## Best Practices

- ✅ Always check wallet availability before operations
- ✅ Handle connection errors gracefully
- ✅ Use typed providers for all Midnight APIs
- ✅ Cache provider instances
- ❌ Don't expose private state
- ❌ Don't skip transaction confirmation

## Resources

- [Midnight.js Docs](https://docs.midnight.network/develop/reference/midnight-js/)
- [DApp Examples](https://github.com/midnightntwrk/midnight-awesome-dapps)
