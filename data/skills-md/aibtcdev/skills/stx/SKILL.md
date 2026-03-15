---
name: stx
description: "Stacks L2 STX token operations — check balances, transfer STX, broadcast pre-signed transactions, call Clarity contracts, deploy contracts, and check transaction status. Transfer and contract operations require an unlocked wallet."
metadata:
  author: "whoabuddy"
  author-agent: "Trustless Indra"
  user-invocable: "false"
  arguments: "get-balance | transfer | broadcast-transaction | call-contract | deploy-contract | get-transaction-status"
  entry: "stx/stx.ts"
  mcp-tools: "get_stx_balance, transfer_stx, broadcast_transaction, call_contract, deploy_contract, get_transaction_status"
  requires: "wallet"
  tags: "l2, write, requires-funds"
---

# STX Skill

Provides Stacks L2 STX token and contract operations using the Hiro API. Transfer and contract write operations require an unlocked wallet (use `bun run wallet/wallet.ts unlock` first). Balance and status queries work with just an address.

## Usage

```
bun run stx/stx.ts <subcommand> [options]
```

## Subcommands

### get-balance

Get the STX balance for a Stacks address. Returns balance in both micro-STX and STX.

```
bun run stx/stx.ts get-balance [--address <addr>]
```

Options:
- `--address` (optional) — Stacks address to check (uses active wallet if omitted)

Output:
```json
{
  "address": "SP2...",
  "network": "mainnet",
  "balance": {
    "microStx": "1000000",
    "stx": "1 STX"
  },
  "locked": {
    "microStx": "0",
    "stx": "0 STX"
  },
  "explorerUrl": "https://explorer.hiro.so/address/SP2...?chain=mainnet"
}
```

### transfer

Transfer STX to a recipient. Requires an unlocked wallet.

1 STX = 1,000,000 micro-STX. Specify `--amount` in micro-STX.

```
bun run stx/stx.ts transfer --recipient <addr> --amount <microStx> [--memo <text>] [--fee low|medium|high|<microStx>]
```

Options:
- `--recipient` (required) — Stacks address to send to (starts with SP or ST)
- `--amount` (required) — Amount in micro-STX (e.g., "2000000" for 2 STX)
- `--memo` (optional) — Memo message to include with the transfer
- `--fee` (optional) — Fee preset (low|medium|high) or micro-STX amount; auto-estimated if omitted

Output:
```json
{
  "success": true,
  "txid": "abc123...",
  "from": "SP2...",
  "recipient": "SP3...",
  "amount": "2 STX",
  "amountMicroStx": "2000000",
  "network": "mainnet",
  "explorerUrl": "https://explorer.hiro.so/txid/abc123...?chain=mainnet"
}
```

### broadcast-transaction

Broadcast a pre-signed Stacks transaction to the network.

```
bun run stx/stx.ts broadcast-transaction --signed-tx <hex>
```

Options:
- `--signed-tx` (required) — The signed transaction as a hex string

Output:
```json
{
  "success": true,
  "txid": "abc123...",
  "network": "mainnet",
  "explorerUrl": "https://explorer.hiro.so/txid/abc123...?chain=mainnet"
}
```

### call-contract

Call a function on a Stacks smart contract. Signs and broadcasts the transaction. Requires an unlocked wallet.

```
bun run stx/stx.ts call-contract --contract-address <addr> --contract-name <name> --function-name <fn> [--args <json>] [--post-condition-mode allow|deny] [--post-conditions <json>] [--fee low|medium|high|<microStx>]
```

Options:
- `--contract-address` (required) — Contract deployer's address (e.g., SP2...)
- `--contract-name` (required) — Contract name (e.g., my-token)
- `--function-name` (required) — Function to call
- `--args` (optional) — Function arguments as JSON array (default: "[]"). For typed args: `[{"type":"uint","value":100}]`
- `--post-condition-mode` (optional) — `deny` (default) blocks unexpected transfers; `allow` permits any
- `--post-conditions` (optional) — Post conditions as JSON array. See SKILL.md for format.
- `--fee` (optional) — Fee preset or micro-STX; auto-estimated if omitted

Post condition format:
- STX: `{"type":"stx","principal":"SP...","conditionCode":"eq","amount":"1000000"}`
- FT: `{"type":"ft","principal":"SP...","asset":"SP...contract","assetName":"token-name","conditionCode":"eq","amount":"1000"}`
- NFT: `{"type":"nft","principal":"SP...","asset":"SP...contract","assetName":"nft-name","tokenId":"1"}`

Output:
```json
{
  "success": true,
  "txid": "abc123...",
  "contract": "SP2....my-token",
  "function": "transfer",
  "network": "mainnet",
  "explorerUrl": "https://explorer.hiro.so/txid/abc123...?chain=mainnet"
}
```

### deploy-contract

Deploy a Clarity smart contract to the Stacks blockchain. Requires an unlocked wallet.

```
bun run stx/stx.ts deploy-contract --contract-name <name> --code-body <clarity-source> [--fee low|medium|high|<microStx>]
```

Options:
- `--contract-name` (required) — Unique name for the contract (lowercase, hyphens allowed)
- `--code-body` (required) — The complete Clarity source code
- `--fee` (optional) — Fee preset or micro-STX; auto-estimated if omitted

Output:
```json
{
  "success": true,
  "txid": "abc123...",
  "contractId": "SP2....my-contract",
  "network": "mainnet",
  "explorerUrl": "https://explorer.hiro.so/txid/abc123...?chain=mainnet"
}
```

### get-transaction-status

Check the status of a Stacks transaction by its txid.

```
bun run stx/stx.ts get-transaction-status --txid <txid>
```

Options:
- `--txid` (required) — The transaction ID (64 character hex string)

Output:
```json
{
  "txid": "abc123...",
  "status": "success",
  "block_height": 150000,
  "network": "mainnet",
  "explorerUrl": "https://explorer.hiro.so/txid/abc123...?chain=mainnet"
}
```

## Notes

- Balance queries use the public Hiro API (no authentication required unless you set HIRO_API_KEY)
- Transfer and contract operations require an unlocked wallet (use `bun run wallet/wallet.ts unlock` first)
- Fees are auto-estimated if `--fee` is omitted; use presets (low|medium|high) or exact micro-STX amounts
- Post condition mode `deny` (default) prevents unintended asset movements; use `allow` only when necessary
