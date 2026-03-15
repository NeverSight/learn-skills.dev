---
name: validation
description: "ERC-8004 on-chain agent validation management — request and respond to validations, and query validation status, summaries, and paginated lists by agent or validator."
metadata:
  author: "whoabuddy"
  author-agent: "Trustless Indra"
  user-invocable: "false"
  arguments: "request | respond | get-status | get-summary | get-agent-validations | get-validator-requests"
  entry: "validation/validation.ts"
  requires: "wallet"
  tags: "l2, write"
---

# Validation Skill

Provides ERC-8004 on-chain agent validation operations using the validation-registry contract. Read operations (get-status, get-summary, get-agent-validations, get-validator-requests) work without a wallet. Write operations (request, respond) require an unlocked wallet.

## Usage

```
bun run validation/validation.ts <subcommand> [options]
```

## Subcommands

### request

Request validation from a validator for an agent in the ERC-8004 validation registry. The request hash must be a 32-byte SHA-256 hash of the request data. Requires an unlocked wallet.

```
bun run validation/validation.ts request --validator <address> --agent-id <id> --request-uri <uri> --request-hash <hex> [--fee <fee>] [--sponsored]
```

Options:
- `--validator` (required) — Stacks address of the validator to request validation from
- `--agent-id` (required) — Agent ID to request validation for (non-negative integer)
- `--request-uri` (required) — URI pointing to the validation request data
- `--request-hash` (required) — 32-byte SHA-256 hash of the request data as a hex string
- `--fee` (optional) — Fee preset (`low`, `medium`, `high`) or micro-STX amount
- `--sponsored` (flag) — Submit as a sponsored transaction

Output:
```json
{
  "success": true,
  "txid": "0xabc...",
  "message": "Validation requested from SP2... for agent 42.",
  "validator": "SP2...",
  "agentId": 42,
  "requestUri": "ipfs://request...",
  "network": "mainnet",
  "explorerUrl": "https://explorer.hiro.so/txid/0xabc..."
}
```

### respond

Submit a validation response for a pending validation request. Only the validator specified in the original request can call this. Response must be an integer between 0 and 100. Can be called multiple times for progressive updates. Requires an unlocked wallet.

```
bun run validation/validation.ts respond --request-hash <hex> --response <value> --response-uri <uri> --response-hash <hex> [--tag <tag>] [--fee <fee>] [--sponsored]
```

Options:
- `--request-hash` (required) — 32-byte SHA-256 hash of the original request as a hex string
- `--response` (required) — Validation response score (integer between 0 and 100)
- `--response-uri` (required) — URI pointing to the validation response data
- `--response-hash` (required) — 32-byte SHA-256 hash of the response data as a hex string
- `--tag` (optional) — Classification tag for the validation response
- `--fee` (optional) — Fee preset (`low`, `medium`, `high`) or micro-STX amount
- `--sponsored` (flag) — Submit as a sponsored transaction

Output:
```json
{
  "success": true,
  "txid": "0xdef...",
  "message": "Validation response 85 submitted for request hash a3f2b1....",
  "response": 85,
  "responseUri": "ipfs://response...",
  "tag": "security",
  "network": "mainnet",
  "explorerUrl": "https://explorer.hiro.so/txid/0xdef..."
}
```

### get-status

Get the status of a validation request by its 32-byte request hash. Returns validator, agent ID, response score, response hash, tag, last update block, and whether a response has been submitted. Does not require a wallet.

```
bun run validation/validation.ts get-status --request-hash <hex>
```

Options:
- `--request-hash` (required) — 32-byte SHA-256 hash of the validation request as a hex string

Output:
```json
{
  "success": true,
  "requestHash": "a3f2b1...64hex",
  "validator": "SP2...",
  "agentId": 42,
  "response": 85,
  "responseHash": "b4e9c2...64hex",
  "tag": "security",
  "lastUpdate": 123456,
  "hasResponse": true,
  "network": "mainnet"
}
```

### get-summary

Get the aggregated validation summary for an agent. Returns the total validation count and average response score. Does not require a wallet.

```
bun run validation/validation.ts get-summary --agent-id <id>
```

Options:
- `--agent-id` (required) — Agent ID to query (non-negative integer)

Output:
```json
{
  "success": true,
  "agentId": 42,
  "count": 3,
  "avgResponse": 88,
  "network": "mainnet"
}
```

### get-agent-validations

Get a paginated list of validation request hashes for an agent. Returns request hashes as hex strings. Cursor-based pagination with page size 14. Does not require a wallet.

```
bun run validation/validation.ts get-agent-validations --agent-id <id> [--cursor <cursor>]
```

Options:
- `--agent-id` (required) — Agent ID to query (non-negative integer)
- `--cursor` (optional) — Pagination cursor (non-negative integer, from previous response)

Output:
```json
{
  "success": true,
  "agentId": 42,
  "validations": ["a3f2b1...64hex", "c5d8e4...64hex"],
  "cursor": null,
  "network": "mainnet"
}
```

### get-validator-requests

Get a paginated list of validation request hashes submitted to a validator. Returns request hashes as hex strings. Cursor-based pagination with page size 14. Does not require a wallet.

```
bun run validation/validation.ts get-validator-requests --validator <address> [--cursor <cursor>]
```

Options:
- `--validator` (required) — Stacks address of the validator to query
- `--cursor` (optional) — Pagination cursor (non-negative integer, from previous response)

Output:
```json
{
  "success": true,
  "validator": "SP2...",
  "requests": ["a3f2b1...64hex", "c5d8e4...64hex"],
  "cursor": null,
  "network": "mainnet"
}
```

## Notes

- Read operations (get-status, get-summary, get-agent-validations, get-validator-requests) work without a wallet
- Write operations require an unlocked wallet (`bun run wallet/wallet.ts unlock`)
- `--request-hash` and `--response-hash` must be exactly 32 bytes (64 hex characters); use SHA-256
- `--response` score must be an integer between 0 and 100 (inclusive)
- `respond` can only be called by the validator specified in the original validation request
- `respond` can be called multiple times on the same request for progressive updates
- Pagination uses cursor-based navigation; pass the `cursor` from one response into the next call
- Validation is a Stacks L2 operation — check transaction status with `stx get-transaction-status` after write calls
