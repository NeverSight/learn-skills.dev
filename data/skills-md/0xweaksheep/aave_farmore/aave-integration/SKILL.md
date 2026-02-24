---
name: aave-integration
description: This skill should be used when the user needs to interact with AAVE V3 protocol contracts directly, read on-chain data, get reserve configurations, fetch current APY rates, simulate position changes, or execute protocol operations programmatically. Provides low-level access to AAVE Pool contracts, UI Pool Data Provider, and quote generation for supply, borrow, repay, and withdraw operations on Ethereum and Arbitrum.
license: MIT
metadata:
  author: AAVE AI Contributors
  version: 1.0.0
---

# AAVE V3 Integration

Low-level integration with AAVE V3 protocol contracts for reading on-chain data and generating operation quotes.

## Overview

This skill provides:

1. **Contract Interface Definitions** - ABIs for AAVE V3 contracts
2. **Quote Generation** - Scripts to get supply, borrow, repay, withdraw quotes
3. **APY Data** - Scripts to fetch current supply/borrow APY for all assets
4. **Position Simulation** - Scripts to preview how actions affect Health Factor and risk
5. **Reserve Configuration** - Reading asset parameters from chain
6. **User Account Data** - Reading user positions and health metrics

## Contract Addresses

### Ethereum Mainnet (chainId: 1)

| Contract | Address |
|----------|---------|
| PoolAddressesProvider | \`0x2f39d218133AFaB8F2B819B1066c7E434Ad94E9e\` |
| Pool (Proxy) | \`0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2\` |
| UiPoolDataProvider | \`0x91c0eA31b49B69Ea18607702c5d9aC360bf3dE7d\` |
| PoolDataProvider | \`0x7B4EB56E7CD4b454BA8ff71E4518426369a138a3\` |

### Arbitrum One (chainId: 42161)

| Contract | Address |
|----------|---------|
| PoolAddressesProvider | \`0xa97684ead0e402dC232d5A977953DF7ECBaB3CDb\` |
| Pool (Proxy) | \`0x794a61358D6845594F94dc1DB02A252b5b4814aD\` |
| UiPoolDataProvider | \`0x5c5228aC8BC1528482514aF3e27D692c20E5c41F\` |
| PoolDataProvider | \`0x69FA688f1Dc47d4B5d8029D5a35FB7a548310654\` |

## Quote Interfaces

### Supply Quote

\`\`\`typescript
interface SupplyQuote {
  token: string;
  tokenAddress: string;
  amount: string;
  amountWei: string;
  apy: string;
  aTokenAddress: string;
  usageRatio: string;
  totalLiquidity: string;
}
\`\`\`

## Token Address Reference

### Ethereum (chainId: 1)

| Symbol | Address | Decimals |
|--------|---------|----------|
| USDC | \`0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48\` | 6 |
| USDT | \`0xdAC17F958D2ee523a2206206994597C13D831ec7\` | 6 |
| WETH | \`0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2\` | 18 |
| WBTC | \`0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599\` | 8 |
| DAI | \`0x6B175474E89094C44Da98b954EedeAC495271d0F\` | 18 |

### Arbitrum (chainId: 42161)

| Symbol | Address | Decimals |
|--------|---------|----------|
| USDC | \`0xaf88d065e77c8cC2239327C5EDb3A432268e5831\` | 6 |
| USDT | \`0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9\` | 6 |
| WETH | \`0x82aF49447D8a07e3bd95BD0d56f35241523fBab1\` | 18 |
| WBTC | \`0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f\` | 8 |
| DAI | \`0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1\` | 18 |

## Scripts

### quote-apy.ts

Fetches current APY data for all whitelisted assets.

\`\`\`bash
npx tsx packages/plugins/aave-integration/scripts/quote-apy.ts <chainId>
\`\`\`

### simulate-position.ts

Simulates how an action would affect a user's position.

\`\`\`bash
npx tsx packages/plugins/aave-integration/scripts/simulate-position.ts <chainId> <userAddress> <action> <token> <amount>
\`\`\`

## External Documentation

- AAVE V3 Developer Docs: https://docs.aave.com/developers
- AAVE V3 Core Contracts: https://github.com/aave/aave-v3-core
- AAVE Address Book: https://github.com/aave/aave-address-book
