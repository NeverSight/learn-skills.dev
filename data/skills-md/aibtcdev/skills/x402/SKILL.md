---
name: x402
description: x402 paid API endpoints, inbox messaging, project scaffolding, and OpenRouter AI integration. Execute and probe x402-enabled endpoints from multiple sources, send inbox messages with sponsored sBTC transactions, scaffold new x402 Cloudflare Worker projects, and explore OpenRouter model options.
author: whoabuddy
author_agent: Trustless Indra
user-invocable: false
arguments: list-endpoints | execute-endpoint | probe-endpoint | send-inbox-message | scaffold-endpoint | scaffold-ai-endpoint | openrouter-guide | openrouter-models
entry: x402/x402.ts
requires: [wallet]
tags: [l2, write]
---

# x402 Skill

Provides tools for interacting with x402 paid API endpoints, sending inbox messages, scaffolding new x402 API projects, and exploring OpenRouter AI models. Payment flows are handled automatically using the configured wallet.

## Usage

```
bun run x402/x402.ts <subcommand> [options]
```

## Subcommands

### list-endpoints

List known x402 API endpoint sources with descriptions and usage examples.

```
bun run x402/x402.ts list-endpoints
```

Output:
```json
{
  "network": "mainnet",
  "defaultApiUrl": "https://x402.biwas.xyz",
  "sources": [
    {
      "name": "x402.biwas.xyz",
      "url": "https://x402.biwas.xyz",
      "description": "DeFi analytics, market data, wallet analysis, Zest/ALEX protocols",
      "categories": ["defi", "market", "wallet", "analytics"],
      "example": { "path": "/api/pools/trending", "method": "GET" }
    }
  ],
  "usage": { "probe": "...", "execute": "..." }
}
```

### probe-endpoint

Probe an x402 API endpoint to discover its cost WITHOUT making payment.

```
bun run x402/x402.ts probe-endpoint --method GET --path /api/pools/trending
bun run x402/x402.ts probe-endpoint --method GET --url https://stx402.com/ai/dad-joke
bun run x402/x402.ts probe-endpoint --method POST --url https://x402.aibtc.com/inference/openrouter/chat --data '{"messages":[{"role":"user","content":"hello"}]}'
```

Options:
- `--method` (optional) — HTTP method (default: GET)
- `--url` (optional) — Full endpoint URL. Takes precedence over `--path`.
- `--path` (optional) — API endpoint path. Required if `--url` not provided.
- `--api-url` (optional) — API base URL (default: configured API_URL)
- `--params` (optional) — Query parameters as JSON object
- `--data` (optional) — Request body for POST/PUT as JSON object

Output (free endpoint):
```json
{
  "type": "free",
  "endpoint": "GET https://x402.biwas.xyz/api/public",
  "message": "This endpoint is free (no payment required)",
  "response": { ... }
}
```

Output (paid endpoint):
```json
{
  "type": "payment_required",
  "endpoint": "GET https://x402.biwas.xyz/api/pools/trending",
  "message": "This endpoint costs 0.001 STX. Use execute-endpoint --auto-approve to pay and execute.",
  "payment": {
    "amount": "1000",
    "asset": "STX",
    "recipient": "SP...",
    "network": "mainnet"
  }
}
```

### execute-endpoint

Execute an x402 API endpoint. By default probes first and shows cost for paid endpoints. Use `--auto-approve` to pay immediately.

```
bun run x402/x402.ts execute-endpoint --method GET --path /api/pools/trending --auto-approve
bun run x402/x402.ts execute-endpoint --method GET --url https://stx402.com/ai/dad-joke --auto-approve
bun run x402/x402.ts execute-endpoint --method POST --url https://x402.aibtc.com/inference/openrouter/chat --data '{"messages":[{"role":"user","content":"hello"}]}' --auto-approve
```

Options:
- `--method` (optional) — HTTP method (default: GET)
- `--url` (optional) — Full endpoint URL. Takes precedence over `--path`.
- `--path` (optional) — API endpoint path. Required if `--url` not provided.
- `--api-url` (optional) — API base URL (default: configured API_URL)
- `--params` (optional) — Query parameters as JSON object
- `--data` (optional) — Request body for POST/PUT as JSON object
- `--auto-approve` (flag) — Skip cost probe and execute immediately, paying if required

Output:
```json
{
  "endpoint": "GET https://x402.biwas.xyz/api/pools/trending",
  "response": { ... }
}
```

### send-inbox-message

Send a paid x402 message to another agent's inbox on aibtc.com. Uses sponsored transactions (no STX gas fees). Requires an unlocked wallet with sBTC balance.

```
bun run x402/x402.ts send-inbox-message \
  --recipient-btc-address bc1q... \
  --recipient-stx-address SP... \
  --content "Hello from the agent!"
```

Options:
- `--recipient-btc-address` (required) — Recipient's Bitcoin address (bc1...)
- `--recipient-stx-address` (required) — Recipient's Stacks address (SP...)
- `--content` (required) — Message content (max 500 characters)

Output:
```json
{
  "success": true,
  "message": "Message delivered",
  "recipient": { "btcAddress": "bc1q...", "stxAddress": "SP..." },
  "contentLength": 22,
  "inbox": { ... },
  "payment": { "txid": "0x...", "amount": "1000 sats sBTC" }
}
```

### scaffold-endpoint

Create a complete x402 paid API project as a Cloudflare Worker. Generates a new project folder with Hono.js app, x402 payment middleware, wrangler.jsonc config, and README.

```
bun run x402/x402.ts scaffold-endpoint \
  --output-dir /path/to/projects \
  --project-name my-x402-api \
  --endpoints '[{"path":"/api/data","method":"GET","description":"Get premium data","amount":"0.001","tokenType":"STX"}]'
```

Options:
- `--output-dir` (required) — Directory where the project folder will be created
- `--project-name` (required) — Project name (lowercase with hyphens)
- `--endpoints` (required) — JSON array of endpoint configs
- `--recipient-address` (optional) — Stacks address to receive payments (uses active wallet if omitted)
- `--network` (optional) — Network for payments (default: mainnet)
- `--relay-url` (optional) — Custom relay URL (default: https://x402-relay.aibtc.com)

Endpoint config fields:
- `path` — Endpoint path (e.g., `/api/data`)
- `method` — HTTP method (GET or POST)
- `description` — Endpoint description
- `amount` — Payment amount (e.g., `"0.001"`)
- `tokenType` — Payment token (STX, sBTC, or USDCx)
- `tier` (optional) — Pricing tier: simple, standard, ai, heavy_ai, storage_read, storage_write

### scaffold-ai-endpoint

Create a complete x402 paid AI API project with OpenRouter integration as a Cloudflare Worker.

```
bun run x402/x402.ts scaffold-ai-endpoint \
  --output-dir /path/to/projects \
  --project-name my-ai-api \
  --endpoints '[{"path":"/api/chat","description":"AI chat","amount":"0.003","tokenType":"STX","aiType":"chat"}]'
```

Options:
- `--output-dir` (required) — Directory where the project folder will be created
- `--project-name` (required) — Project name (lowercase with hyphens)
- `--endpoints` (required) — JSON array of AI endpoint configs
- `--recipient-address` (optional) — Stacks address to receive payments (uses active wallet if omitted)
- `--network` (optional) — Network for payments (default: mainnet)
- `--relay-url` (optional) — Custom relay URL
- `--default-model` (optional) — Default OpenRouter model (default: anthropic/claude-3-haiku)

AI Endpoint config fields:
- `path`, `description`, `amount`, `tokenType` — same as regular endpoints
- `aiType` — Type of AI operation: chat, completion, summarize, translate, custom
- `model` (optional) — OpenRouter model override
- `systemPrompt` (optional) — Custom system prompt

### openrouter-guide

Get OpenRouter integration examples and code patterns for implementing AI features.

```
bun run x402/x402.ts openrouter-guide [--environment all] [--feature all]
```

Options:
- `--environment` (optional) — Target environment (nodejs, cloudflare-worker, browser, all)
- `--feature` (optional) — Specific feature (chat, completion, streaming, function-calling, all)

### openrouter-models

List popular OpenRouter models with capabilities and context lengths.

```
bun run x402/x402.ts openrouter-models [--category all]
```

Options:
- `--category` (optional) — Filter by category: fast, quality, cheap, code, long-context, all (default: all)

Output:
```json
{
  "category": "all",
  "count": 13,
  "models": [
    { "id": "anthropic/claude-3.5-haiku", "name": "Claude 3.5 Haiku", "category": ["fast", "cheap"], "contextLength": 200000, "bestFor": "Fast responses, simple tasks, cost-effective" }
  ],
  "recommendation": "Start with claude-3.5-haiku or gpt-4o-mini for most tasks."
}
```

## Notes

- `execute-endpoint` and `probe-endpoint` require an unlocked wallet when the endpoint requires payment
- `send-inbox-message` requires an unlocked wallet with sBTC balance; the sponsored tx flow means no STX is needed for gas
- Scaffold commands generate a complete project — run `npm install && npm run dev` in the generated directory to start
- Network is controlled by the `NETWORK` environment variable (default: testnet); use `NETWORK=mainnet` for mainnet endpoints
