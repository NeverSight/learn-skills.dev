---
name: swap-tokens
description: Swap or trade tokens via decentralized exchanges on any supported chain. Use when you or the user want to trade, swap, exchange, buy, sell, or convert between tokens like USDC, ETH, WETH, SOL, or any other token. Covers phrases like "buy ETH with USDC", "sell ETH for USDC", "convert USDC to ETH", "swap tokens", "get some ETH".
user-invocable: true
disable-model-invocation: false
allowed-tools: ["Bash(fdx status*)", "Bash(fdx call swapTokens*)", "Bash(fdx call getWalletOverview*)"]
---

# Swapping Tokens

Use the `fdx call swapTokens` command to swap between tokens via decentralized exchanges on any supported chain. Unlike centralized exchange swaps, these execute directly on-chain through DEX protocols.

## Confirm wallet is authenticated

```bash
fdx status
```

If the wallet is not authenticated, refer to the `authenticate` skill.

## Check Balance Before Swapping

Verify the wallet holds enough of the source token:

```bash
fdx call getWalletOverview --chainKey <chain>
```

## Executing a Swap

```bash
fdx call swapTokens \
  --chainKey <chain> \
  --tokenIn <token> \
  --tokenOut <token> \
  --amount <amount>
```

### Parameters

| Parameter           | Required | Description                                                          |
| ------------------- | -------- | -------------------------------------------------------------------- |
| `--chainKey`        | Yes      | Blockchain to swap on (e.g. `ethereum`, `polygon`, `base`, `solana`) |
| `--tokenIn`         | Yes      | Source token — symbol (e.g. `USDC`, `ETH`) or contract address       |
| `--tokenOut`        | Yes      | Destination token — symbol or contract address                       |
| `--amount`          | Yes      | Amount of `tokenIn` to swap (human-readable)                         |
| `--mode`            | No       | Swap mode (e.g. exact input, exact output)                           |
| `--objective`       | No       | Optimization objective (e.g. best price, lowest gas)                 |
| `--maxSlippageBps`  | No       | Maximum slippage tolerance in basis points (100 = 1%)                |
| `--deadlineSeconds` | No       | Transaction deadline in seconds                                      |

## Examples

### Basic swaps

```bash
# Swap 100 USDC for ETH on Ethereum
fdx call swapTokens \
  --chainKey ethereum \
  --tokenIn USDC \
  --tokenOut ETH \
  --amount 100

# Swap 0.05 ETH for USDC on Base
fdx call swapTokens \
  --chainKey base \
  --tokenIn ETH \
  --tokenOut USDC \
  --amount 0.05

# Swap SOL for USDC on Solana
fdx call swapTokens \
  --chainKey solana \
  --tokenIn SOL \
  --tokenOut USDC \
  --amount 2
```

### Swap with slippage control

```bash
# Swap with 0.5% max slippage
fdx call swapTokens \
  --chainKey ethereum \
  --tokenIn USDC \
  --tokenOut ETH \
  --amount 500 \
  --maxSlippageBps 50
```

### Swap using contract addresses

```bash
# Swap using explicit token contract addresses
fdx call swapTokens \
  --chainKey ethereum \
  --tokenIn 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 \
  --tokenOut 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2 \
  --amount 100
```

## Flow

1. Check authentication with `fdx status`
2. Check balance with `fdx call getWalletOverview --chainKey <chain>`
3. Confirm the swap details with the human (amount, tokens, chain, slippage)
4. Execute with `fdx call swapTokens`
5. Optionally check updated balance with `fdx call getWalletOverview`

**Important:** DEX swaps are subject to slippage — the final output amount may differ slightly from the quoted amount. For large swaps, consider setting `--maxSlippageBps` explicitly.

## Prerequisites

- Must be authenticated (`fdx status` to check, see `authenticate` skill)
- Wallet must hold sufficient balance of the source token on the target chain
- If the wallet has insufficient funds, suggest using the `fund-wallet` skill

## Error Handling

- "Not authenticated" — Run `fdx setup` first, or see `authenticate` skill
- "Insufficient balance" — Check balance with `getWalletOverview`; see `fund-wallet` skill
- "Cannot swap a token to itself" — `tokenIn` and `tokenOut` must be different
- "No liquidity" — Try a smaller amount or a different token pair
- "Swap failed" — May be a slippage issue; try with a higher `--maxSlippageBps`
