---
name: send-token
description: Transfer tokens from OpenAnt wallet on Solana or Base. Use when the user wants to send, transfer, or pay tokens via OpenAnt. Supports native coins (SOL, ETH) and tokens (USDC) by name, plus arbitrary tokens by mint/contract address. Covers "send SOL", "transfer USDC", "send tokens", "pay someone", "send ETH on Base", "transfer to address", "OpenAnt wallet send".
user-invocable: true
disable-model-invocation: false
allowed-tools: ["Bash(npx @openant-ai/cli@latest wallet send *)", "Bash(npx @openant-ai/cli@latest wallet balance*)", "Bash(npx @openant-ai/cli@latest wallet addr*)", "Bash(npx @openant-ai/cli@latest status*)"]
---

# Sending Tokens on OpenAnt

Use the `npx @openant-ai/cli@latest` CLI to transfer tokens on Solana or Base. Supports native coins (SOL, ETH), named tokens (USDC), and arbitrary tokens by mint/contract address.

**Always append `--json`** to every command for structured, parseable output.

## Confirm Authentication and Balance

```bash
npx @openant-ai/cli@latest status --json
npx @openant-ai/cli@latest wallet balance --json
```

If not authenticated, refer to the `authenticate-openant` skill. If balance is insufficient, inform the user.

## Command Syntax

```bash
npx @openant-ai/cli@latest wallet send <chain> <token> <amount> <to> [--json] [--rpc <url>]
```

### Arguments

| Argument | Description |
|----------|-------------|
| `chain` | Target chain: `solana` (or `sol`), `base` (or `eth`) |
| `token` | Token: `sol`, `eth`, `usdc`, or a mint/contract address |
| `amount` | Amount in display units (e.g. `10` = 10 USDC, `0.5` = 0.5 SOL) |
| `to` | Destination address (Solana pubkey or EVM 0x address) |

### Options

| Option | Description |
|--------|-------------|
| `--json` | Machine-readable JSON output |
| `--rpc <url>` | Override the default RPC URL for the chain |

## Supported Chains and Tokens

| Chain | Named tokens | Native coin |
|-------|-------------|-------------|
| `solana` / `sol` | `usdc`, or any SPL mint address | `sol` |
| `base` / `eth` | `usdc`, or any ERC20 contract address | `eth` |

For arbitrary tokens, pass the mint address (Solana) or contract address (Base) directly as the `token` argument.

## Examples

### Send native SOL

```bash
npx @openant-ai/cli@latest wallet send solana sol 1.5 7xKabc123... --json
# -> { "success": true, "data": { "chain": "solana", "txSignature": "5xYz..." } }
```

### Send USDC on Solana

```bash
npx @openant-ai/cli@latest wallet send solana usdc 100 7xKabc123... --json
# -> { "success": true, "data": { "chain": "solana", "txSignature": "3aBc..." } }
```

### Send ETH on Base

```bash
npx @openant-ai/cli@latest wallet send base eth 0.05 0xAbCdEf... --json
# -> { "success": true, "data": { "chain": "base", "txHash": "0x1a2b..." } }
```

### Send USDC on Base

```bash
npx @openant-ai/cli@latest wallet send base usdc 50 0xAbCdEf... --json
# -> { "success": true, "data": { "chain": "base", "txHash": "0x9f8e..." } }
```

### Send arbitrary SPL token by mint address

```bash
npx @openant-ai/cli@latest wallet send solana 4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU 25 7xKabc123... --json
```

### Send arbitrary ERC20 on Base by contract address

```bash
npx @openant-ai/cli@latest wallet send base 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 10 0xAbCdEf... --json
```

## Natural Language Mapping

When the user says something like:

- "帮我 base 上转 10 usdc 给 0xAbc..." → `wallet send base usdc 10 0xAbc... --json`
- "帮我 solana 上转 1.5 sol 给 7xK..." → `wallet send solana sol 1.5 7xK... --json`
- "Send 50 USDC to 0xDef... on Base" → `wallet send base usdc 50 0xDef... --json`
- "Transfer 0.1 ETH to 0x123..." → `wallet send base eth 0.1 0x123... --json`
- "帮我 solana 上转 10 <mint_address> 给 <recipient>" → `wallet send solana <mint_address> 10 <recipient> --json`

Extract: chain, token (name or address), amount, and destination address.

## Autonomy

**Token transfers are irreversible.** Always confirm with the user before executing:

1. Verify the chain, token, amount, and destination address with the user
2. Check wallet balance first to ensure sufficient funds
3. Only execute after explicit user confirmation

Read-only commands (`status`, `wallet balance`, `wallet addresses`) can be executed immediately.

## NEVER

- **NEVER send without the user explicitly confirming the destination address** — blockchain transfers are irreversible. Show the full address and ask the user to verify it before executing.
- **NEVER send Solana tokens to a Base address, or vice versa** — the chains are incompatible. Solana addresses are base58 strings (32–44 chars), Base addresses start with `0x`. If the address format doesn't match the chain, stop and clarify with the user.
- **NEVER assume the displayed balance accounts for gas** — Solana transactions require a small SOL fee (~0.000005 SOL); Base transactions require ETH for gas. If the user is sending their entire balance, leave a small reserve or the transaction will fail.
- **NEVER infer the chain from the token alone** — USDC exists on both Solana and Base. Always confirm which chain the user intends before sending.
- **NEVER send to an address the user typed casually without double-checking** — if the user typed the address in the middle of a sentence or abbreviated it, ask them to paste the full address again to confirm.

## Prerequisites

- Must be authenticated (`npx @openant-ai/cli@latest status --json`)
- Wallet must have sufficient balance for the transfer plus gas/fees
- For SPL token transfers, the sender must hold the token

## Error Handling

- "No Turnkey credentials found" — Run `authenticate-openant` skill first
- "Insufficient balance" / "Attempt to debit" — Wallet lacks funds; check `wallet balance`
- "Unknown chain" — Supported: `sol`, `base`, `eth`
- "No Base wallet found" / "No Solana wallet found" — Re-login to provision wallets
- "Cannot read decimals for mint" — Invalid or non-existent token mint address
- Transaction simulation failed — Check balance and recipient address validity
