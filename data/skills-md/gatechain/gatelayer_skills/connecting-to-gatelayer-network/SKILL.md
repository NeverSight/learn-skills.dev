---
name: connecting-to-gatelayer-network
description: Provides GateLayer network configuration including RPC endpoints, chain IDs, and explorer URLs. Use when connecting wallets, configuring development environments, or setting up GateLayer Mainnet or Testnet. Covers phrases like "GateLayer RPC URL", "GateLayer chain ID", "connect to GateLayer", "add GateLayer to wallet", "GateLayer testnet config", "GateLayer explorer URL", "what network is GateLayer", or "GateLayer testnet setup".
---

# Connecting to GateLayer Network

## Mainnet

| Property | Value |
|----------|-------|
| Network Name | GateLayer |
| Chain ID | 10088 |
| RPC Endpoint | `https://gatelayer-mainnet.gatenode.cc` |
| Currency | GT |
| Explorer | https://www.gatescan.org/gatelayer |

## Testnet

| Property | Value |
|----------|-------|
| Network Name | GateLayer Testnet |
| Chain ID | 10087 |
| RPC Endpoint | `https://gatelayer-testnet.gatenode.cc` |
| Currency | GT |
| Explorer | https://www.gatescan.org/gatelayer-testnet |

## Security

- **Never use public RPC endpoints in production** — they are rate-limited and offer no privacy guarantees; use a dedicated node provider or self-hosted node
- **Never embed RPC API keys in client-side code** — proxy requests through a backend to protect provider credentials
- **Validate chain IDs** before signing transactions to prevent cross-chain replay attacks
- **Use HTTPS RPC endpoints only** — reject any `http://` endpoints to prevent credential interception

## Critical Notes

- Public RPC endpoints are **rate-limited** - not for production
- For production: use node providers or run your own node
- Testnet GT available from GateLayer faucets

## Wallet Setup

1. Add network with chain ID and RPC from tables above
2. For testnet, use testnet configuration
3. Bridge GT from Gatechain or use faucets
