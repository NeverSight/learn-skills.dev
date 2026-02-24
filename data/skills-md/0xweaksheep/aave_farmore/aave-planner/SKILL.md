---
name: aave-planner
description: This skill should be used when the user asks to "supply to aave", "deposit to aave", "lend on aave", "borrow from aave", "take loan on aave", "repay aave loan", "pay back aave", "withdraw from aave", "remove collateral", "aave lending", "earn yield on aave", or mentions AAVE V3 operations including supply, borrow, repay, or withdraw on Ethereum or Arbitrum.
license: MIT
metadata:
  author: AAVE AI Contributors
  version: 1.0.0
---

# AAVE V3 Planner

Plan and generate deep links for AAVE V3 lending operations on Ethereum and Arbitrum.

## Overview

Plan AAVE V3 operations by:

1. Gathering operation intent (action, token, amount, chain)
2. Validating token against whitelist
3. Checking interest rate mode compatibility (for borrow)
4. Generating a deep link or manual path for execution

Supported actions:
- **Supply**: Deposit assets to earn yield
- **Borrow**: Borrow assets against collateral
- **Repay**: Repay borrowed assets
- **Withdraw**: Withdraw supplied collateral

Supported chains:
- **Ethereum Mainnet** (chainId: 1)
- **Arbitrum One** (chainId: 42161)

## Whitelist Assets

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

> **Note**: Only **DAI** supports stable rate borrowing. All other assets default to variable rate.

## Deep Link Format

\`\`\`
https://app.aave.com/?marketName={market}&token={token}&amount={amount}&action={action}
\`\`\`

**Market mapping:**
- Ethereum: \`proto_mainnet_v3\`
- Arbitrum: \`proto_arbitrum_v3\`

**Action mapping:**
- supply → \`supply\`
- borrow → \`borrow\`
- repay → \`repay\`
- withdraw → \`withdraw\`

## Position Simulation

When users want to preview how an action would affect their position:

\`\`\`bash
npx tsx packages/plugins/aave-planner/scripts/simulate-position.ts <chainId> <userAddress> <action> <token> <amount>
\`\`\`

## External Resources

- AAVE V3 Documentation: https://docs.aave.com/
- AAVE App: https://app.aave.com
