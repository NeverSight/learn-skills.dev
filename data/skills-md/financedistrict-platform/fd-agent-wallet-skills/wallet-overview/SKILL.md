---
name: wallet-overview
description: Check wallet balances, token holdings, and transaction history across all supported chains. Use when you or the user want to see their balance, check holdings, view portfolio, see what tokens they have, look up recent transactions, check activity, or get their wallet address. Covers "what's in my wallet?", "show my balance", "what's my address?", "show recent transactions".
user-invocable: true
disable-model-invocation: false
allowed-tools: ["Bash(fdx status*)", "Bash(fdx call getWalletOverview*)", "Bash(fdx call getAccountActivity*)", "Bash(fdx call getMyInfo*)"]
---

# Wallet Overview & Activity

View wallet balances, token holdings, and transaction history across all supported EVM chains and Solana.

## Confirm wallet is authenticated

```bash
fdx status
```

If the wallet is not authenticated, refer to the `authenticate` skill.

## Getting Wallet Information

### User profile and wallet identity

```bash
fdx call getMyInfo
```

Returns the authenticated user's profile and wallet details.

### Wallet balances and holdings

```bash
# All chains — full portfolio overview
fdx call getWalletOverview

# Specific chain
fdx call getWalletOverview --chainKey ethereum

# Specific account on a chain
fdx call getWalletOverview --chainKey ethereum --accountAddress 0x1234...abcd
```

Returns token balances, holdings, and wallet addresses for the specified scope.

### Transaction history

```bash
# Recent activity across all chains
fdx call getAccountActivity

# Specific chain
fdx call getAccountActivity --chainKey ethereum

# Specific account with pagination
fdx call getAccountActivity --chainKey ethereum --accountAddress 0x1234...abcd --limit 20 --offset 0
```

## Parameters

### getWalletOverview

| Parameter          | Required | Description                                                                |
| ------------------ | -------- | -------------------------------------------------------------------------- |
| `--chainKey`       | No       | Filter by chain (e.g. `ethereum`, `polygon`, `arbitrum`, `base`, `solana`) |
| `--accountAddress` | No       | Filter by specific account address                                         |

### getAccountActivity

| Parameter          | Required | Description                        |
| ------------------ | -------- | ---------------------------------- |
| `--chainKey`       | No       | Filter by chain                    |
| `--accountAddress` | No       | Filter by specific account address |
| `--limit`          | No       | Number of transactions to return   |
| `--offset`         | No       | Pagination offset                  |

## Supported Chains

The Finance District wallet supports all EVM-compatible chains and Solana. Common chain keys include:

| Chain Key   | Network           |
| ----------- | ----------------- |
| `ethereum`  | Ethereum mainnet  |
| `polygon`   | Polygon           |
| `arbitrum`  | Arbitrum One      |
| `base`      | Base              |
| `optimism`  | Optimism          |
| `avalanche` | Avalanche C-Chain |
| `bsc`       | BNB Smart Chain   |
| `solana`    | Solana            |

## Example Session

```bash
# Check auth
fdx status

# See who I am
fdx call getMyInfo

# Check full portfolio
fdx call getWalletOverview

# Drill into Ethereum holdings
fdx call getWalletOverview --chainKey ethereum

# See recent Ethereum transactions
fdx call getAccountActivity --chainKey ethereum --limit 10
```

## Prerequisites

- Must be authenticated (`fdx status` to check, see `authenticate` skill)

## Error Handling

- "Not authenticated" — Run `fdx setup` first, or see `authenticate` skill
- "AUTH_REFRESH_FAILED" — Token expired; run `fdx setup` to re-authenticate
