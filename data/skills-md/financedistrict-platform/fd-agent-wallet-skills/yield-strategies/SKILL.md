---
name: yield-strategies
description: Discover, deposit into, and withdraw from DeFi yield generation strategies across multiple chains and protocols. Use when you or the user want to earn yield, find APY, stake tokens, explore DeFi, farm, deposit into a protocol, withdraw earnings, check yield opportunities, or grow their holdings. Covers "how can I earn on my USDC?", "find me yield", "stake my ETH", "where can I get the best APY?", "withdraw from Aave".
user-invocable: true
disable-model-invocation: false
allowed-tools: ["Bash(fdx status*)", "Bash(fdx call discoverYieldStrategies*)", "Bash(fdx call depositForYield*)", "Bash(fdx call withdrawFromYield*)", "Bash(fdx call getWalletOverview*)"]
---

# DeFi Yield Strategies

Discover yield opportunities across DeFi protocols (Aave, Compound, and others), deposit tokens to earn yield, and withdraw when ready. This is a full lifecycle skill covering discovery through to exit.

## Confirm wallet is authenticated

```bash
fdx status
```

If the wallet is not authenticated, refer to the `authenticate` skill.

## Step 1: Discover Yield Strategies

Search for available yield opportunities:

```bash
# Browse all available strategies
fdx call discoverYieldStrategies

# Filter by chain
fdx call discoverYieldStrategies --chainKey ethereum

# Filter by token
fdx call discoverYieldStrategies --chainKey ethereum --tokenAddress 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48

# Filter by minimum APY and risk level
fdx call discoverYieldStrategies --chainKey ethereum --minApy 5 --maxRisk low

# Sort results
fdx call discoverYieldStrategies --chainKey ethereum --sortBy apy
```

### discoverYieldStrategies Parameters

| Parameter        | Required | Description                                                           |
| ---------------- | -------- | --------------------------------------------------------------------- |
| `--chainKey`     | No       | Filter by blockchain (e.g. `ethereum`, `polygon`, `arbitrum`, `base`) |
| `--tokenAddress` | No       | Filter by token contract address                                      |
| `--minApy`       | No       | Minimum APY percentage (e.g. `5` for 5%)                              |
| `--maxRisk`      | No       | Maximum risk level filter (e.g. `low`, `medium`, `high`)              |
| `--sortBy`       | No       | Sort results (e.g. `apy`, `risk`)                                     |

## Step 2: Deposit for Yield

Once a strategy is selected, deposit tokens into it:

```bash
fdx call depositForYield \
  --chainKey <chain> \
  --strategyId <strategyId> \
  --amount <amount>
```

### depositForYield Parameters

| Parameter        | Required | Description                                                |
| ---------------- | -------- | ---------------------------------------------------------- |
| `--chainKey`     | Yes      | Blockchain where the strategy runs                         |
| `--strategyId`   | Yes      | Strategy identifier from `discoverYieldStrategies` results |
| `--amount`       | Yes      | Amount to deposit (human-readable)                         |
| `--tokenAddress` | No       | Token to deposit (if strategy accepts multiple tokens)     |

## Step 3: Withdraw from Yield

Exit a position and retrieve tokens:

```bash
fdx call withdrawFromYield \
  --chainKey <chain> \
  --positionId <positionId>
```

### withdrawFromYield Parameters

| Parameter      | Required | Description                                       |
| -------------- | -------- | ------------------------------------------------- |
| `--chainKey`   | Yes      | Blockchain of the position                        |
| `--positionId` | Yes      | Position identifier from the deposit result       |
| `--amount`     | No       | Amount to withdraw (omit for full withdrawal)     |
| `--recipient`  | No       | Custom recipient address (defaults to own wallet) |

## Example Session

```bash
# Check auth and balance
fdx status
fdx call getWalletOverview --chainKey ethereum

# Discover USDC yield strategies on Ethereum with at least 3% APY
fdx call discoverYieldStrategies \
  --chainKey ethereum \
  --tokenAddress 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 \
  --minApy 3 \
  --sortBy apy

# Deposit 1000 USDC into a chosen strategy
fdx call depositForYield \
  --chainKey ethereum \
  --strategyId <strategyId-from-discovery> \
  --amount 1000

# Later: withdraw the full position
fdx call withdrawFromYield \
  --chainKey ethereum \
  --positionId <positionId-from-deposit>
```

## Flow

1. Check authentication with `fdx status`
2. Check available balance with `fdx call getWalletOverview --chainKey <chain>`
3. Discover strategies with `fdx call discoverYieldStrategies` — present options to the human
4. Human selects a strategy — confirm the choice, risks, and deposit amount
5. Execute deposit with `fdx call depositForYield`
6. When the human wants to exit, withdraw with `fdx call withdrawFromYield`

**Important:** DeFi protocols carry smart contract risk. Always present the risk level to your human and let them make the final decision on which strategy to use and how much to deposit.

## Prerequisites

- Must be authenticated (`fdx status` to check, see `authenticate` skill)
- Wallet must hold sufficient balance of the deposit token on the target chain
- If insufficient funds, suggest using the `fund-wallet` skill or `swap-tokens` skill to acquire the needed token

## Error Handling

- "Not authenticated" — Run `fdx setup` first, or see `authenticate` skill
- "Insufficient balance" — Check balance; see `fund-wallet` skill
- "Invalid strategyId" — Re-run `discoverYieldStrategies` to get current strategy IDs
- "Invalid positionId" — The position may have already been withdrawn
