---
name: bns
description: "Bitcoin Name System (BNS) operations — lookup names, reverse-lookup addresses, check availability, get pricing, list domains, and register new .btc names using single-transaction claim or two-step preorder/register flow."
metadata:
  author: "whoabuddy"
  author-agent: "Trustless Indra"
  user-invocable: "false"
  arguments: "lookup | reverse-lookup | get-info | check-availability | get-price | list-user-domains | claim-fast | preorder | register"
  entry: "bns/bns.ts"
  mcp-tools: "lookup_bns_name, reverse_bns_lookup, get_bns_info, check_bns_availability, get_bns_price, list_user_domains, claim_bns_name_fast, preorder_bns_name, register_bns_name"
  requires: "wallet"
  tags: "l2, write, requires-funds"
---

# BNS Skill

Provides Bitcoin Name System (BNS) operations for .btc domain names using BNS V2 (recommended for .btc) with fallback to BNS V1. Read operations work without a wallet. Write operations (claim-fast, preorder, register) require an unlocked wallet.

## Usage

```
bun run bns/bns.ts <subcommand> [options]
```

## Subcommands

### lookup

Resolve a .btc domain name to its Stacks address.

```
bun run bns/bns.ts lookup --name <name>
```

Options:
- `--name` (required) — BNS name to lookup (e.g., `alice.btc` or `alice`)

Output:
```json
{
  "name": "alice.btc",
  "found": true,
  "address": "SP1...",
  "namespace": "btc",
  "expireBlock": 900000,
  "network": "mainnet"
}
```

### reverse-lookup

Get all BNS domain names owned by an address.

```
bun run bns/bns.ts reverse-lookup [--address <addr>]
```

Options:
- `--address` (optional) — Stacks address to lookup (uses active wallet if omitted)

Output:
```json
{
  "address": "SP1...",
  "network": "mainnet",
  "namesCount": 2,
  "names": ["alice.btc", "myname.btc"]
}
```

### get-info

Get detailed information about a BNS domain name.

```
bun run bns/bns.ts get-info --name <name>
```

Options:
- `--name` (required) — BNS name to look up (e.g., `alice.btc`)

Output:
```json
{
  "network": "mainnet",
  "found": true,
  "name": "alice.btc",
  "namespace": "btc",
  "address": "SP1...",
  "expireBlock": 900000,
  "gracePeriod": 0,
  "status": "active"
}
```

### check-availability

Check if a BNS domain name is available for registration.

```
bun run bns/bns.ts check-availability --name <name>
```

Options:
- `--name` (required) — BNS name to check (e.g., `alice` or `alice.btc`)

Output:
```json
{
  "name": "alice.btc",
  "available": true,
  "network": "mainnet"
}
```

### get-price

Get the registration price for a BNS domain name in STX.

```
bun run bns/bns.ts get-price --name <name>
```

Options:
- `--name` (required) — BNS name to check (e.g., `alice` or `alice.btc`)

Output:
```json
{
  "name": "alice.btc",
  "network": "mainnet",
  "price": {
    "units": "ustx",
    "microStx": "2000000",
    "stx": "2 STX"
  }
}
```

### list-user-domains

List all BNS domains owned by an address.

```
bun run bns/bns.ts list-user-domains [--address <addr>]
```

Options:
- `--address` (optional) — Stacks address to check (uses active wallet if omitted)

Output:
```json
{
  "address": "SP1...",
  "network": "mainnet",
  "domainsCount": 1,
  "domains": ["alice.btc"]
}
```

### claim-fast

Register a BNS domain name in a single transaction (recommended method for .btc names). Burns the name price in STX and mints the BNS NFT atomically. Requires an unlocked wallet.

```
bun run bns/bns.ts claim-fast --name <name> [--send-to <addr>]
```

Options:
- `--name` (required) — BNS name to claim (e.g., `myname` or `myname.btc`)
- `--send-to` (optional) — Recipient address (defaults to wallet's own address)

Output:
```json
{
  "success": true,
  "method": "name-claim-fast (single transaction)",
  "name": "myname.btc",
  "sendTo": "SP1...",
  "txid": "0xabc...",
  "network": "mainnet",
  "price": { "microStx": "2000000", "stx": "2 STX" },
  "message": "Name \"myname.btc\" claimed! Once confirmed (~10 min), it will be registered.",
  "explorerUrl": "https://explorer.hiro.so/txid/0xabc..."
}
```

### preorder

Preorder a BNS domain name (step 1 of 2-step registration). Use this only when claim-fast is unavailable. Save the returned salt — you need it for the register step. Requires an unlocked wallet.

```
bun run bns/bns.ts preorder --name <name> [--salt <hex>]
```

Options:
- `--name` (required) — BNS name to preorder
- `--salt` (optional) — Hex salt for the preorder hash (auto-generated if omitted)

Output:
```json
{
  "success": true,
  "step": "1 of 2 (preorder)",
  "name": "myname.btc",
  "salt": "a1b2c3...",
  "txid": "0xdef...",
  "network": "mainnet",
  "nextStep": "Wait ~10 minutes, then call register with the same name and salt."
}
```

### register

Register a BNS domain name after preorder is confirmed (step 2 of 2-step registration). Must use the same salt from the preorder step. Requires an unlocked wallet.

```
bun run bns/bns.ts register --name <name> --salt <hex>
```

Options:
- `--name` (required) — BNS name to register (must match the preordered name)
- `--salt` (required) — The hex salt used in the preorder step

Output:
```json
{
  "success": true,
  "step": "2 of 2 (register)",
  "name": "myname.btc",
  "txid": "0xghi...",
  "network": "mainnet",
  "message": "Registration submitted! Once confirmed, \"myname.btc\" will be registered.",
  "explorerUrl": "https://explorer.hiro.so/txid/0xghi..."
}
```

## Notes

- Read operations (lookup, reverse-lookup, get-info, check-availability, get-price, list-user-domains) work without a wallet
- Write operations (claim-fast, preorder, register) require an unlocked wallet (`bun run wallet/wallet.ts unlock`)
- For .btc registration, prefer `claim-fast` — it registers in a single transaction without a waiting period
- Use the 2-step preorder/register flow only for non-.btc namespaces or if claim-fast is unavailable
- BNS V2 is used for .btc names; BNS V1 is used as fallback for other namespaces
