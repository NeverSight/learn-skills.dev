---
name: trade-tokens
description: Swap or trade tokens on Base network. Use when you or the user want to trade, swap, exchange, buy, sell, or convert between tokens like USDC, ETH, and WETH. Covers phrases like "buy ETH", "sell ETH for USDC", "convert USDC to ETH", "get some ETH", "swap tokens", "trade USDC for WETH".
user-invocable: true
disable-model-invocation: false
allowed-tools: ["Bash(npx agnic@latest status*)", "Bash(npx agnic@latest trade *)", "Bash(npx agnic@latest balance*)"]
---

# Trading Tokens

Use the `npx agnic@latest trade` command to swap tokens on Base network. You must be authenticated to trade.

## Confirm wallet is initialized and authed

```bash
npx agnic@latest status
```

If the wallet is not authenticated, refer to the `authenticate-wallet` skill.

## Command Syntax

```bash
npx agnic@latest trade <amount> <from> <to> [options]
```

## Arguments

| Argument | Description                                                            |
| -------- | ---------------------------------------------------------------------- |
| `amount` | Amount to swap (see Amount Formats below)                              |
| `from`   | Source token: alias (usdc, eth, weth) or contract address (0x...)      |
| `to`     | Destination token: alias (usdc, eth, weth) or contract address (0x...) |

## Amount Formats

| Format        | Example                | Description                            |
| ------------- | ---------------------- | -------------------------------------- |
| Dollar prefix | `'$1.00'`, `'$0.50'`  | USD notation (decimals based on token) |
| Decimal       | `1.0`, `0.50`, `0.001` | Human-readable with decimal point      |
| Whole number  | `5`, `100`             | Interpreted as whole tokens            |
| Atomic units  | `500000`               | Large integers treated as atomic units |

**Auto-detection**: Large integers without a decimal point are treated as atomic units. For example, `500000` for USDC (6 decimals) = $0.50.

**IMPORTANT**: Always single-quote amounts that use `$` to prevent bash variable expansion (e.g. `'$1.00'` not `$1.00`).

## Token Aliases

| Alias | Token | Decimals | Address                                    |
| ----- | ----- | -------- | ------------------------------------------ |
| usdc  | USDC  | 6        | 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 |
| eth   | ETH   | 18       | 0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE |
| weth  | WETH  | 18       | 0x4200000000000000000000000000000000000006   |

## Options

| Option               | Description                                   |
| -------------------- | --------------------------------------------- |
| `-s, --slippage <n>` | Slippage tolerance in basis points (100 = 1%) |
| `--json`             | Output result as JSON                         |

## Input Validation

Before constructing the command, validate all user-provided values to prevent shell injection:

- **amount**: Must match `^\$?[\d.]+$` (digits, optional decimal point, optional `$` prefix). Reject if it contains spaces, semicolons, pipes, backticks, or other shell metacharacters.
- **from / to**: Must be a known alias (`usdc`, `eth`, `weth`) or a valid `0x` hex address (`^0x[0-9a-fA-F]{40}$`). Reject any other value.
- **slippage**: Must be a positive integer (`^\d+$`).

Do not pass unvalidated user input into the command.

## Examples

```bash
# Swap $1 USDC for ETH (dollar prefix — note the single quotes)
npx agnic@latest trade '$1' usdc eth

# Swap 0.50 USDC for ETH (decimal format)
npx agnic@latest trade 0.50 usdc eth

# Swap 0.01 ETH for USDC
npx agnic@latest trade 0.01 eth usdc

# Swap with custom slippage (2%)
npx agnic@latest trade '$5' usdc eth --slippage 200

# Get JSON output
npx agnic@latest trade '$1' usdc eth --json
```

## Prerequisites

- Must be authenticated (`npx agnic@latest status` to check)
- Wallet must have sufficient balance of the source token
- Trading is only available on Base mainnet

## Error Handling

Common errors:

- "Not authenticated" — Run `npx agnic@latest auth login` first
- "Invalid token" — Use a valid alias (usdc, eth, weth) or 0x address
- "Cannot swap a token to itself" — From and to must be different
- "Swap failed: TRANSFER_FROM_FAILED" — Insufficient balance or approval issue
- "No liquidity" — Try a smaller amount or different token pair
- "Amount has X decimals but token only supports Y" — Too many decimal places
