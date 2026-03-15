---
name: reputation
description: "ERC-8004 on-chain agent reputation management — submit and revoke feedback, append responses, approve clients, and query reputation summaries, feedback entries, and client lists."
metadata:
  author: "whoabuddy"
  author-agent: "Trustless Indra"
  user-invocable: "false"
  arguments: "give-feedback | revoke-feedback | append-response | approve-client | get-summary | read-feedback | read-all-feedback | get-clients | get-feedback-count | get-approved-limit | get-last-index"
  entry: "reputation/reputation.ts"
  requires: "wallet"
  tags: "l2, write"
---

# Reputation Skill

Provides ERC-8004 on-chain agent reputation operations using the reputation-registry contract. Read operations (get-summary, read-feedback, read-all-feedback, get-clients, get-feedback-count, get-approved-limit, get-last-index) work without a wallet. Write operations (give-feedback, revoke-feedback, append-response, approve-client) require an unlocked wallet.

## Usage

```
bun run reputation/reputation.ts <subcommand> [options]
```

## Subcommands

### give-feedback

Submit feedback for an agent in the ERC-8004 reputation registry. Requires an unlocked wallet.

```
bun run reputation/reputation.ts give-feedback --agent-id <id> --value <value> [--value-decimals <decimals>] [--tag1 <tag>] [--tag2 <tag>] [--endpoint <endpoint>] [--feedback-uri <uri>] [--feedback-hash <hex>] [--fee <fee>] [--sponsored]
```

Options:
- `--agent-id` (required) — Agent ID to give feedback for (non-negative integer)
- `--value` (required) — Feedback value (signed integer, e.g., 5 for positive, -2 for negative)
- `--value-decimals` (optional, default 0) — Decimal precision for the value (non-negative integer)
- `--tag1` (optional) — Primary classification tag (e.g., "helpful", "accuracy")
- `--tag2` (optional) — Secondary classification tag
- `--endpoint` (optional) — Endpoint or context identifier for the feedback
- `--feedback-uri` (optional) — URI pointing to detailed feedback data
- `--feedback-hash` (optional) — 32-byte SHA-256 hash of the feedback data as a hex string
- `--fee` (optional) — Fee preset (`low`, `medium`, `high`) or micro-STX amount
- `--sponsored` (flag) — Submit as a sponsored transaction

Output:
```json
{
  "success": true,
  "txid": "0xabc...",
  "message": "Feedback submitted for agent 42.",
  "agentId": 42,
  "value": 5,
  "valueDecimals": 0,
  "network": "mainnet",
  "explorerUrl": "https://explorer.hiro.so/txid/0xabc..."
}
```

### revoke-feedback

Revoke previously submitted feedback. Only the original feedback submitter (tx-sender) can revoke their own feedback. Requires an unlocked wallet.

```
bun run reputation/reputation.ts revoke-feedback --agent-id <id> --index <index> [--fee <fee>] [--sponsored]
```

Options:
- `--agent-id` (required) — Agent ID whose feedback you want to revoke (non-negative integer)
- `--index` (required) — Feedback index to revoke (non-negative integer)
- `--fee` (optional) — Fee preset (`low`, `medium`, `high`) or micro-STX amount
- `--sponsored` (flag) — Submit as a sponsored transaction

Output:
```json
{
  "success": true,
  "txid": "0xdef...",
  "message": "Feedback index 0 revoked for agent 42.",
  "agentId": 42,
  "index": 0,
  "network": "mainnet",
  "explorerUrl": "https://explorer.hiro.so/txid/0xdef..."
}
```

### append-response

Append a response to a feedback entry. Any principal can append a response; the contract tracks unique responders per feedback entry. Requires an unlocked wallet.

```
bun run reputation/reputation.ts append-response --agent-id <id> --client <address> --index <index> --response-uri <uri> --response-hash <hex> [--fee <fee>] [--sponsored]
```

Options:
- `--agent-id` (required) — Agent ID associated with the feedback (non-negative integer)
- `--client` (required) — Stacks address of the original feedback submitter
- `--index` (required) — Feedback index to respond to (non-negative integer)
- `--response-uri` (required) — URI pointing to the response data
- `--response-hash` (required) — 32-byte SHA-256 hash of the response data as a hex string
- `--fee` (optional) — Fee preset (`low`, `medium`, `high`) or micro-STX amount
- `--sponsored` (flag) — Submit as a sponsored transaction

Output:
```json
{
  "success": true,
  "txid": "0xghi...",
  "message": "Response appended to feedback index 0 for agent 42.",
  "agentId": 42,
  "client": "SP2...",
  "index": 0,
  "responseUri": "ipfs://response...",
  "network": "mainnet",
  "explorerUrl": "https://explorer.hiro.so/txid/0xghi..."
}
```

### approve-client

Approve a client address to submit feedback for an agent up to a specified index limit. Caller must be the agent owner or an approved operator. Requires an unlocked wallet.

```
bun run reputation/reputation.ts approve-client --agent-id <id> --client <address> --index-limit <limit> [--fee <fee>] [--sponsored]
```

Options:
- `--agent-id` (required) — Agent ID to configure approval for (non-negative integer)
- `--client` (required) — Stacks address of the client to approve
- `--index-limit` (required) — Maximum number of feedback entries the client may submit (non-negative integer)
- `--fee` (optional) — Fee preset (`low`, `medium`, `high`) or micro-STX amount
- `--sponsored` (flag) — Submit as a sponsored transaction

Output:
```json
{
  "success": true,
  "txid": "0xjkl...",
  "message": "Client SP3... approved for agent 42 up to index limit 10.",
  "agentId": 42,
  "client": "SP3...",
  "indexLimit": 10,
  "network": "mainnet",
  "explorerUrl": "https://explorer.hiro.so/txid/0xjkl..."
}
```

### get-summary

Get the aggregated reputation summary for an agent. Returns total feedback count and WAD-averaged summary value. Does not require a wallet.

```
bun run reputation/reputation.ts get-summary --agent-id <id>
```

Options:
- `--agent-id` (required) — Agent ID to query (non-negative integer)

Output:
```json
{
  "success": true,
  "agentId": 42,
  "totalFeedback": 7,
  "summaryValue": "5000000000000000000",
  "summaryValueDecimals": 18,
  "network": "mainnet"
}
```

### read-feedback

Read a specific feedback entry by agent ID, client address, and feedback index. Does not require a wallet.

```
bun run reputation/reputation.ts read-feedback --agent-id <id> --client <address> --index <index>
```

Options:
- `--agent-id` (required) — Agent ID to query (non-negative integer)
- `--client` (required) — Stacks address of the feedback submitter
- `--index` (required) — Feedback index to read (non-negative integer)

Output:
```json
{
  "success": true,
  "agentId": 42,
  "client": "SP2...",
  "index": 0,
  "value": 5,
  "valueDecimals": 0,
  "wadValue": "5000000000000000000",
  "tag1": "helpful",
  "tag2": "",
  "isRevoked": false,
  "network": "mainnet"
}
```

### read-all-feedback

Get a paginated list of all feedback entries for an agent. Supports optional tag filtering and cursor-based pagination (page size: 14). Does not require a wallet.

```
bun run reputation/reputation.ts read-all-feedback --agent-id <id> [--tag1 <tag>] [--tag2 <tag>] [--include-revoked] [--cursor <cursor>]
```

Options:
- `--agent-id` (required) — Agent ID to query (non-negative integer)
- `--tag1` (optional) — Filter by primary tag
- `--tag2` (optional) — Filter by secondary tag
- `--include-revoked` (flag) — Include revoked feedback entries in results
- `--cursor` (optional) — Pagination cursor from a previous response

Output:
```json
{
  "success": true,
  "agentId": 42,
  "items": [
    {
      "client": "SP2...",
      "index": 0,
      "value": 5,
      "valueDecimals": 0,
      "wadValue": "5000000000000000000",
      "tag1": "helpful",
      "tag2": "",
      "isRevoked": false
    }
  ],
  "cursor": null,
  "network": "mainnet"
}
```

### get-clients

Get a paginated list of client addresses that have given feedback for an agent. Cursor-based pagination with page size 14. Does not require a wallet.

```
bun run reputation/reputation.ts get-clients --agent-id <id> [--cursor <cursor>]
```

Options:
- `--agent-id` (required) — Agent ID to query (non-negative integer)
- `--cursor` (optional) — Pagination cursor from a previous response

Output:
```json
{
  "success": true,
  "agentId": 42,
  "clients": ["SP2...", "SP3..."],
  "cursor": null,
  "network": "mainnet"
}
```

### get-feedback-count

Get the total feedback count for an agent. Does not require a wallet.

```
bun run reputation/reputation.ts get-feedback-count --agent-id <id>
```

Options:
- `--agent-id` (required) — Agent ID to query (non-negative integer)

Output:
```json
{
  "success": true,
  "agentId": 42,
  "feedbackCount": 7,
  "network": "mainnet"
}
```

### get-approved-limit

Check the approved feedback index limit for a client on an agent. Returns 0 if the client has no explicit approval. Does not require a wallet.

```
bun run reputation/reputation.ts get-approved-limit --agent-id <id> --client <address>
```

Options:
- `--agent-id` (required) — Agent ID to query (non-negative integer)
- `--client` (required) — Stacks address of the client to check

Output:
```json
{
  "success": true,
  "agentId": 42,
  "client": "SP3...",
  "approvedLimit": 10,
  "network": "mainnet"
}
```

### get-last-index

Get the last feedback index for a client on an agent. Returns 0 if the client has not given any feedback. Does not require a wallet.

```
bun run reputation/reputation.ts get-last-index --agent-id <id> --client <address>
```

Options:
- `--agent-id` (required) — Agent ID to query (non-negative integer)
- `--client` (required) — Stacks address of the client to check

Output:
```json
{
  "success": true,
  "agentId": 42,
  "client": "SP3...",
  "lastIndex": 2,
  "network": "mainnet"
}
```

## Notes

- Read operations (get-summary, read-feedback, read-all-feedback, get-clients, get-feedback-count, get-approved-limit, get-last-index) work without a wallet
- Write operations require an unlocked wallet (`bun run wallet/wallet.ts unlock`)
- Feedback values are signed integers; use `--value-decimals` to express fractional precision
- `--feedback-hash` and `--response-hash` must be exactly 32 bytes (64 hex characters)
- `revoke-feedback` can only be called by the original feedback submitter (tx-sender must match the client who submitted)
- `approve-client` can only be called by the agent owner or an approved identity operator
- Pagination uses cursor-based navigation; pass the `cursor` from one response into the next call
