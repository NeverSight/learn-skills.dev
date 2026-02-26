---
name: send-tokens
description: Send or transfer tokens to any address on any supported chain (EVM or Solana). Use when you or the user want to send money, pay someone, transfer tokens, tip, donate, or move funds to another wallet address. Covers phrases like "send 10 USDC to", "pay 0x...", "transfer ETH to", "move tokens to my other wallet".
user-invocable: true
disable-model-invocation: false
allowed-tools: ["Bash(fdx status*)", "Bash(fdx call transferTokens*)", "Bash(fdx call getWalletOverview*)"]
---

# Sending Tokens

Use the `fdx call transferTokens` command to transfer tokens from the wallet to any address on any supported EVM chain or Solana.

## Confirm wallet is authenticated

```bash
fdx status
```

If the wallet is not authenticated, refer to the `authenticate` skill.

## Check Balance Before Sending

Always verify the wallet has sufficient balance before initiating a transfer:

```bash
fdx call getWalletOverview --chainKey <chain>
```

## Sending Tokens

```bash
fdx call transferTokens \
  --chainKey <chain> \
  --recipientAddress <address> \
  --amount <amount>
```

### Parameters

| Parameter                | Required | Description                                                      |
| ------------------------ | -------- | ---------------------------------------------------------------- |
| `--chainKey`             | Yes      | Target blockchain (e.g. `ethereum`, `polygon`, `base`, `solana`) |
| `--recipientAddress`     | Yes      | Destination wallet address                                       |
| `--amount`               | Yes      | Amount to send (human-readable, e.g. `10`, `0.5`)                |
| `--fromAccountAddress`   | No       | Source account address (if wallet has multiple accounts)         |
| `--tokenAddress`         | No       | Token contract address (omit for native token like ETH or SOL)   |
| `--memo`                 | No       | Optional memo or note for the transaction                        |
| `--maxPriorityFeePerGas` | No       | EVM gas tip override                                             |
| `--maxFeePerGas`         | No       | EVM max gas fee override                                         |

## Examples

### Send native tokens

```bash
# Send 0.1 ETH on Ethereum
fdx call transferTokens \
  --chainKey ethereum \
  --recipientAddress 0x1234...abcd \
  --amount 0.1

# Send 1 SOL on Solana
fdx call transferTokens \
  --chainKey solana \
  --recipientAddress AbCd...1234 \
  --amount 1
```

### Send ERC-20 tokens

```bash
# Send 100 USDC on Ethereum (specify token contract)
fdx call transferTokens \
  --chainKey ethereum \
  --recipientAddress 0x1234...abcd \
  --amount 100 \
  --tokenAddress 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48

# Send 50 USDC on Base
fdx call transferTokens \
  --chainKey base \
  --recipientAddress 0x1234...abcd \
  --amount 50 \
  --tokenAddress 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913
```

### Send with memo

```bash
fdx call transferTokens \
  --chainKey ethereum \
  --recipientAddress 0x1234...abcd \
  --amount 10 \
  --tokenAddress 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 \
  --memo "Payment for invoice #42"
```

## Flow

1. Check authentication with `fdx status`
2. Check balance with `fdx call getWalletOverview --chainKey <chain>`
3. Confirm the transfer details with the human (amount, recipient, chain, token)
4. Execute with `fdx call transferTokens`
5. Report the transaction result to the human

**Important:** Always confirm the recipient address and amount with your human before executing, especially for large amounts. Blockchain transactions are irreversible.

## Prerequisites

- Must be authenticated (`fdx status` to check, see `authenticate` skill)
- Wallet must have sufficient balance on the target chain
- If sending insufficient funds, suggest using the `fund-wallet` skill

## Error Handling

- "Not authenticated" — Run `fdx setup` first, or see `authenticate` skill
- "Insufficient balance" — Check balance with `getWalletOverview`; see `fund-wallet` skill
- "Invalid recipient" — Verify the address format matches the target chain
