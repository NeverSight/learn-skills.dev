---
name: tokens
description: SIP-010 fungible token operations on Stacks L2 — check balances, transfer tokens, get token metadata, list all tokens owned by an address, and get top token holders. Supports well-known tokens by symbol (sBTC, USDCx, ALEX, DIKO) or full contract ID.
author: whoabuddy
author_agent: Trustless Indra
user-invocable: false
arguments: get-balance | transfer | get-info | list-user-tokens | get-holders
entry: tokens/tokens.ts
requires: [wallet]
tags: [l2, write]
---

# Tokens Skill

Provides SIP-010 fungible token operations on Stacks L2. Transfer operations require an unlocked wallet (use `bun run wallet/wallet.ts unlock` first). Balance and info queries work without a wallet.

Supports well-known tokens by symbol: `sBTC`, `USDCx`, `ALEX`, `DIKO`
Or use the full contract ID: `SP2...address.contract-name`

## Usage

```
bun run tokens/tokens.ts <subcommand> [options]
```

## Subcommands

### get-balance

Get the balance of any SIP-010 token for a wallet address.

```
bun run tokens/tokens.ts get-balance --token <symbol-or-id> [--address <addr>]
```

Options:
- `--token` (required) — Token symbol (e.g., `USDCx`, `sBTC`) or contract ID
- `--address` (optional) — Stacks address to check (uses active wallet if omitted)

Output:
```json
{
  "address": "SP2...",
  "network": "mainnet",
  "token": {
    "contractId": "SP2...address.usdc-token",
    "symbol": "USDCx",
    "name": "USD Coin",
    "decimals": 6
  },
  "balance": {
    "raw": "1000000",
    "formatted": "1 USDCx"
  }
}
```

### transfer

Transfer any SIP-010 token to a recipient address. Requires an unlocked wallet.

```
bun run tokens/tokens.ts transfer --token <symbol-or-id> --recipient <addr> --amount <amount> [--memo <text>] [--fee low|medium|high|<microStx>]
```

Options:
- `--token` (required) — Token symbol or contract ID
- `--recipient` (required) — Stacks address to send to
- `--amount` (required) — Amount in smallest unit (depends on token decimals)
- `--memo` (optional) — Memo message (max 34 bytes)
- `--fee` (optional) — Fee preset (low|medium|high) or micro-STX amount; auto-estimated if omitted

Output:
```json
{
  "success": true,
  "txid": "abc123...",
  "from": "SP2...",
  "recipient": "SP3...",
  "token": "USDCx",
  "amount": "1000000",
  "network": "mainnet",
  "explorerUrl": "https://explorer.hiro.so/txid/abc123...?chain=mainnet"
}
```

### get-info

Get metadata for a SIP-010 token (name, symbol, decimals, total supply).

```
bun run tokens/tokens.ts get-info --token <symbol-or-id>
```

Options:
- `--token` (required) — Token symbol or contract ID

Output:
```json
{
  "network": "mainnet",
  "contractId": "SP2...address.usdc-token",
  "name": "USD Coin",
  "symbol": "USDCx",
  "decimals": 6,
  "totalSupply": "1000000000000",
  "tokenUri": "https://..."
}
```

### list-user-tokens

List all fungible tokens owned by an address.

```
bun run tokens/tokens.ts list-user-tokens [--address <addr>]
```

Options:
- `--address` (optional) — Stacks address to check (uses active wallet if omitted)

Output:
```json
{
  "address": "SP2...",
  "network": "mainnet",
  "tokenCount": 2,
  "tokens": [
    { "contractId": "SP2....usdc-token::usdcx", "balance": "1000000" },
    { "contractId": "SP3....alex-token::alex", "balance": "500000000" }
  ]
}
```

### get-holders

Get the top holders of a SIP-010 token.

```
bun run tokens/tokens.ts get-holders --token <symbol-or-id> [--limit <n>] [--offset <n>]
```

Options:
- `--token` (required) — Token symbol or contract ID
- `--limit` (optional) — Maximum number of holders to return (default: 20)
- `--offset` (optional) — Offset for pagination (default: 0)

Output:
```json
{
  "token": "USDCx",
  "network": "mainnet",
  "total": 1234,
  "holders": [
    { "address": "SP2...", "balance": "50000000000" },
    { "address": "SP3...", "balance": "25000000000" }
  ]
}
```

## Notes

- Token balance and info queries use the public Hiro API (no authentication required)
- Transfer operations require an unlocked wallet
- Well-known token symbols: `sBTC`, `USDCx`, `ALEX`, `DIKO` — or use the full contract ID
- Token amounts are in the smallest unit — check `decimals` field to convert to human-readable values
