---
name: connecting-to-base-network
description: Provides Base network configuration including RPC endpoints, chain IDs, and explorer URLs. Use when connecting wallets, configuring development environments, or setting up Base Mainnet or Sepolia testnet. Covers phrases like "Base RPC URL", "Base chain ID", "connect to Base", "add Base to wallet", "Base Sepolia config", "Base explorer URL", "what network is Base", or "Base testnet setup".
---

# Connecting to Base Network

## Mainnet

| Property | Value |
|----------|-------|
| Network Name | Base |
| Chain ID | 8453 |
| RPC Endpoint | `https://mainnet.base.org` |
| Currency | ETH |
| Explorer | https://basescan.org |

## Testnet (Sepolia)

| Property | Value |
|----------|-------|
| Network Name | Base Sepolia |
| Chain ID | 84532 |
| RPC Endpoint | `https://sepolia.base.org` |
| Currency | ETH |
| Explorer | https://sepolia.basescan.org |

## Security

- **Never use public RPC endpoints in production** — they are rate-limited and offer no privacy guarantees; use a dedicated node provider or self-hosted node
- **Never embed RPC API keys in client-side code** — proxy requests through a backend to protect provider credentials
- **Validate chain IDs** before signing transactions to prevent cross-chain replay attacks
- **Use HTTPS RPC endpoints only** — reject any `http://` endpoints to prevent credential interception

## Critical Notes

- Public RPC endpoints are **rate-limited** - not for production
- For production: use node providers or run your own node
- Testnet ETH available from faucets in Base documentation

## Wallet Setup

1. Add network with chain ID and RPC from tables above
2. For testnet, use Sepolia configuration
3. Bridge ETH from Ethereum or use faucets
