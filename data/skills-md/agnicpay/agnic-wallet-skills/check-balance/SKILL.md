---
name: check-balance
description: Check USDC balance across networks. Use when you or the user want to check balance, see how much money is in the wallet, view funds, or check available USDC. Covers phrases like "check my balance", "how much USDC do I have", "what's my balance", "show funds", "wallet balance".
user-invocable: true
disable-model-invocation: false
allowed-tools: ["Bash(npx agnic@latest status*)", "Bash(npx agnic@latest balance*)"]
---

# Checking USDC Balance

Use the `npx agnic@latest balance` command to check USDC balance across supported networks.

## Confirm wallet is initialized and authed

```bash
npx agnic@latest status
```

If the wallet is not authenticated, refer to the `authenticate-wallet` skill.

## Command Syntax

```bash
npx agnic@latest balance [--network <network>] [--json]
```

## Options

| Option               | Description                                |
| -------------------- | ------------------------------------------ |
| `--network <name>`   | Filter by network (default: all networks)  |
| `--json`             | Output result as JSON                      |

## Supported Networks

| Network        | Description           |
| -------------- | --------------------- |
| `base`         | Base mainnet (primary) |
| `base-sepolia` | Base testnet          |
| `solana`       | Solana mainnet        |
| `solana-devnet`| Solana devnet         |

## Examples

```bash
# Check balance on all networks
npx agnic@latest balance

# Check balance on Base mainnet only
npx agnic@latest balance --network base

# Get JSON output
npx agnic@latest balance --json
```

## Expected Output

```
Network       Balance      Address
base          125.50 USDC  0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb7
base-sepolia    0.00 USDC  0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb7
solana          0.00 USDC  N/A
solana-devnet   0.00 USDC  N/A
```

## Prerequisites

- Must be authenticated (`npx agnic@latest status` to check)

## Error Handling

Common errors:

- "Not authenticated" — Run `npx agnic@latest auth login` first
- Network timeout — Try again or specify a single network with `--network base`
