---
name: aave-viem-integration
description: Foundational EVM integration for AAVE-related scripts using viem. Use when user asks to read balances, read/write contracts, send transactions, or set up typed viem clients for Ethereum and Arbitrum.
license: MIT
metadata:
  author: AAVE AI Contributors
  version: 1.0.0
---

# AAVE viem Integration

Provide reusable viem patterns for AAVE skill scripts and custom integrations.

## Scope

- Public client and wallet client setup
- Chain-specific RPC selection
- Reading ERC20 balances and allowances
- Simulating and sending contract transactions
- Waiting for receipts and formatting execution output

## Quick Start

```typescript
import { createPublicClient, createWalletClient, http } from 'viem';
import { mainnet } from 'viem/chains';

const publicClient = createPublicClient({
  chain: mainnet,
  transport: http(process.env.ETHEREUM_RPC_URL),
});
```

## References

- `references/clients-and-transports.md`
- `references/contract-read-write.md`
