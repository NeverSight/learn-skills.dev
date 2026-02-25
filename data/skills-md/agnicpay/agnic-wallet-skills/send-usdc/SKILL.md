---
name: send-usdc
description: Send USDC to an Ethereum address or ENS name. Use when you or the user want to send money, pay someone, transfer USDC, tip, donate, or send funds to a wallet address or .eth name. Covers phrases like "send $5 to", "pay 0x...", "transfer to vitalik.eth", "tip someone", "send USDC".
user-invocable: true
disable-model-invocation: false
allowed-tools: ["Bash(npx agnic@latest status*)", "Bash(npx agnic@latest send *)", "Bash(npx agnic@latest balance*)"]
---

# Sending USDC

Use the `npx agnic@latest send` command to transfer USDC from the wallet to any Ethereum address or ENS name on Base.

## Confirm wallet is initialized and authed

```bash
npx agnic@latest status
```

If the wallet is not authenticated, refer to the `authenticate-wallet` skill.

## Command Syntax

```bash
npx agnic@latest send <amount> <recipient> [--chain <chain>] [--json]
```

## Arguments

| Argument    | Description                                                                                                                                                                                                                          |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `amount`    | Amount to send: `'$1.00'`, `1.00`, or atomic units (1000000 = $1). Always single-quote amounts that use `$` to prevent bash variable expansion. If the number looks like atomic units (no decimal or > 100), treat as atomic units. |
| `recipient` | Ethereum address (0x...) or ENS name (vitalik.eth)                                                                                                                                                                                   |

## Options

| Option           | Description                        |
| ---------------- | ---------------------------------- |
| `--chain <name>` | Blockchain network (default: base) |
| `--json`         | Output result as JSON              |

## Input Validation

Before constructing the command, validate all user-provided values to prevent shell injection:

- **amount**: Must match `^\$?[\d.]+$` (digits, optional decimal point, optional `$` prefix). Reject if it contains spaces, semicolons, pipes, backticks, or other shell metacharacters.
- **recipient**: Must be a valid `0x` hex address (`^0x[0-9a-fA-F]{40}$`) or an ENS name (`^[a-zA-Z0-9.-]+\.eth$`). Reject any value containing spaces or shell metacharacters.

Do not pass unvalidated user input into the command.

## USDC Amounts

| Format        | Example                | Description                            |
| ------------- | ---------------------- | -------------------------------------- |
| Dollar prefix | `'$1.00'`, `'$0.50'`  | USD notation (single-quote the `$`)    |
| Decimal       | `1.0`, `0.50`          | Human-readable with decimal point      |
| Whole number  | `5`, `100`             | Interpreted as whole USDC tokens       |
| Atomic units  | `500000`               | Large integers treated as atomic units |

**IMPORTANT**: Always single-quote amounts that use `$` to prevent bash variable expansion (e.g. `'$1.00'` not `$1.00`).

## ENS Resolution

ENS names are automatically resolved to addresses via Ethereum mainnet. The command will:
1. Detect ENS names (any string containing `.eth`)
2. Resolve the name to an address
3. Display both the ENS name and resolved address in the output

## Examples

```bash
# Send $1.00 USDC to an address
npx agnic@latest send 1 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb7

# Send $0.50 USDC to an ENS name
npx agnic@latest send 0.50 vitalik.eth

# Send with dollar sign prefix (note the single quotes)
npx agnic@latest send '$5.00' 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb7

# Get JSON output
npx agnic@latest send 1 vitalik.eth --json
```

## Prerequisites

- Must be authenticated (`npx agnic@latest status` to check)
- Wallet must have sufficient USDC balance (`npx agnic@latest balance` to check)

## Error Handling

Common errors:

- "Not authenticated" — Run `npx agnic@latest auth login` first
- "Insufficient balance" — Check balance with `npx agnic@latest balance`
- "Could not resolve ENS name" — Verify the ENS name exists
- "Invalid recipient" — Must be valid 0x address or ENS name
