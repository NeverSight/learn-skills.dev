---
name: midnight-network
description: Configure and operate Midnight Network infrastructure including proof servers, indexers, and network endpoints. Use when setting up development environment, troubleshooting connections, or configuring deployments. Triggers on network, proof server, indexer, or testnet questions.
---

# Midnight Network Infrastructure

Configure and manage Midnight Network components for dApp development.

## Quick Reference

| Service          | Testnet-02 URL                                                |
| ---------------- | ------------------------------------------------------------- |
| **Indexer**      | `https://indexer.testnet-02.midnight.network/api/v1/graphql`  |
| **Indexer WS**   | `wss://indexer.testnet-02.midnight.network/api/v1/graphql/ws` |
| **RPC Node**     | `https://rpc.testnet-02.midnight.network`                     |
| **Proof Server** | `http://localhost:6300` (local)                               |
| **Faucet**       | `https://faucet.testnet-02.midnight.network`                  |

## Reference Files

| Topic               | Resource                                                       |
| ------------------- | -------------------------------------------------------------- |
| **Network Config**  | [references/network-config.md](references/network-config.md)   |
| **Proof Server**    | [references/proof-server.md](references/proof-server.md)       |
| **Indexer Queries** | [references/indexer-graphql.md](references/indexer-graphql.md) |
| **Troubleshooting** | [references/troubleshooting.md](references/troubleshooting.md) |

## Development Setup

### 1. Start Proof Server

```bash
docker run -p 6300:6300 midnightnetwork/proof-server -- \
  midnight-proof-server --network testnet
```

### 2. Install Lace Wallet

Download from [lace.io](https://www.lace.io/) and enable Midnight mode.

### 3. Get Testnet Tokens

Visit the faucet to receive tDUST for testing.

## Architecture

```text
┌──────────────┐     ┌───────────────┐     ┌──────────────┐
│  Your dApp   │────▶│  Proof Server │────▶│   Midnight   │
│  (Browser)   │     │   (localhost) │     │   Network    │
└──────────────┘     └───────────────┘     └──────────────┘
       │                                          │
       │              ┌───────────────┐           │
       └─────────────▶│    Indexer    │◀──────────┘
                      │   (GraphQL)   │
                      └───────────────┘
```

## Network IDs

```typescript
import { NetworkId, setNetworkId } from '@midnight-ntwrk/midnight-js-network-id';

// Always set before using providers
setNetworkId(NetworkId.TestNet);

// Available networks
enum NetworkId {
  DevNet = 'DevNet', // Developer network (not persistent)
  TestNet = 'TestNet', // Persistent testnet
  MainNet = 'MainNet', // Midnight mainnet
  Undeployed = 'Undeployed', // Local testing
}
```

## Health Checks

```bash
# Check proof server
curl http://localhost:6300/health

# Check indexer
curl https://indexer.testnet-02.midnight.network/api/v1/graphql \
  -H 'Content-Type: application/json' \
  -d '{"query":"{ __typename }"}'
```

## Common Issues

| Issue                    | Solution                                 |
| ------------------------ | ---------------------------------------- |
| Proof generation timeout | Increase timeout, check Docker resources |
| Connection refused       | Ensure proof server is running           |
| Network mismatch         | Verify NetworkId matches wallet          |
| Insufficient funds       | Get tDUST from faucet                    |

## Best Practices

- ✅ Start proof server before dApp
- ✅ Use wallet's service URIs when available
- ✅ Set NetworkId before provider initialization
- ✅ Monitor proof server logs for errors
- ❌ Don't hardcode network URLs (use config)
