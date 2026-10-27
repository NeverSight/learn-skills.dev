---
name: alchemy-api
description: Wire Alchemy into application code (server, backend, dApp, script) using a standard API key. Preferred app-integration path for normal server/backend usage. Covers EVM JSON-RPC, WebSocket subscriptions, Simulation, Webhooks/Notify, Solana RPC, Solana DAS, Solana Yellowstone gRPC, Sui gRPC, Wallets/Account Kit, Account Abstraction, and operational topics. Requires `$ALCHEMY_API_KEY`. For app code without an API key (autonomous agent paying per-request, or explicit x402/MPP), use `alchemy-agentic-gateway` instead.
license: MIT
compatibility: Requires network access and `$ALCHEMY_API_KEY` environment variable. Works across Claude.ai, Claude Code, Cursor, Codex, and API.
metadata:
  author: alchemyplatform
  version: "2.0"
scope_in: >-
  Building production application code on Alchemy infrastructure with an Alchemy API key —
  EVM JSON-RPC, WebSocket subscriptions, webhooks/notify, Account Kit, Account Abstraction,
  transaction simulation, Solana RPC/DAS/Yellowstone gRPC, and Sui gRPC.
scope_out: >-
  Pay-per-call keyless access to Alchemy without an API key → `alchemy-agentic-gateway`.
  Onchain data analytics, prices, balances, PnL, and custom SQL via the `allium` CLI (API key, x402, or Tempo auth) → `allium-data`.
---
# Alchemy API (with API Key)

Reference and integration guide for wiring Alchemy APIs into application code using a standard API key. This file alone is enough to ship a basic integration; the `references/` directory contains deeper coverage of every product surface.

## When to use this skill

Use `alchemy-api` when **all** of the following are true:

- The user is wiring Alchemy into **application code** (server, backend, dApp, worker, script) that runs **outside** the current agent session
- They have, or are willing to create, an Alchemy API key (free at [dashboard.alchemy.com](https://dashboard.alchemy.com/))

This is the **preferred app-integration path** for normal server/backend usage.

## When to use a different skill

| Situation | Use this skill instead |
| --- | --- |
| Live agent work in this session (queries, admin, on-machine automation) and `@alchemy/cli` is installed locally — or both CLI and MCP are available | `alchemy-cli` |
| Live agent work in this session and only MCP is wired into the client (no CLI) | `alchemy-mcp` |
| Live agent work and neither is available | install `alchemy-cli` and use `alchemy-cli` |
| Application code without an API key — autonomous agent paying per-request, or user explicitly wants x402/MPP | `agentic-gateway` |

Do **not** use this skill to run ad-hoc live queries from inside the agent session — that's the `alchemy-cli` / `alchemy-mcp` path. This skill is for code that ships.

## Mandatory preflight gate

Before writing application code or making any network call:

1. Confirm the user is building **application code** (not asking the agent to run a live query). If the user is asking for live work, redirect to `alchemy-cli` (preferred) or `alchemy-mcp`.
2. Check `$ALCHEMY_API_KEY` is set (e.g. `echo $ALCHEMY_API_KEY`).
3. If `$ALCHEMY_API_KEY` is unset or empty, take the first of these that applies:
   - **CLI bridge (recommended if `@alchemy/cli` is installed locally):** the CLI can fetch a key from the user's Alchemy account so they never have to leave the terminal. See [Bridging from the CLI to an API key](#bridging-from-the-cli-to-an-api-key) below.
   - Tell the user they can create a free API key at [https://dashboard.alchemy.com/](https://dashboard.alchemy.com/), **or**
   - Switch to the `agentic-gateway` skill (x402/MPP gateway, wallet-based auth, no API key needed).

You MUST NOT call any keyless or public fallback (including `.../v2/demo`) unless the user explicitly asks for that endpoint. No public RPC endpoints (publicnode, llamarpc, cloudflare-eth, etc.) as a fallback.

### Bridging from the CLI to an API key

If `@alchemy/cli` is installed locally (verify with `command -v alchemy`), use it to obtain a key without leaving the terminal **and persist it to the project's `.env` file** so it survives across terminal sessions and is available to the app at runtime.

> **Security:** NEVER echo, print, or otherwise surface the extracted API key value in conversation output. Refer to it only as `$ALCHEMY_API_KEY` after exporting. Treat it the same as a password.

```bash
# 1. Try to read a cached key from the CLI config (read-only, safe to run non-interactively).
KEY="$(alchemy --no-interactive --json --reveal config get api-key 2>/dev/null | jq -r .value)"

# 2. If empty/null (no key cached yet), run the interactive flow.
#    Note: auth login opens a browser and apps select shows a picker, so do NOT pass
#    --no-interactive here. If you already know the app id, pass it explicitly to skip
#    the picker: `alchemy --no-interactive --json apps select <id>`.
if [ -z "$KEY" ] || [ "$KEY" = "null" ]; then
  alchemy auth login              # opens browser; derives auth credentials
  alchemy --json apps select      # interactive picker (omit --no-interactive so it can render)
  KEY="$(alchemy --no-interactive --json --reveal config get api-key | jq -r .value)"
fi

# 3. Persist to the project's .env (standard practice for app code so the key
#    survives terminal restarts and is loaded by dotenv / framework env loaders).
#    Use .env.local instead if your framework expects that (e.g. Next.js).
ENV_FILE=".env"   # or ".env.local" depending on the project convention
touch "$ENV_FILE"
if grep -q '^ALCHEMY_API_KEY=' "$ENV_FILE"; then
  # Replace existing line in-place (portable across BSD/GNU sed)
  sed -i.bak "s|^ALCHEMY_API_KEY=.*|ALCHEMY_API_KEY=$KEY|" "$ENV_FILE" && rm "$ENV_FILE.bak"
else
  echo "ALCHEMY_API_KEY=$KEY" >> "$ENV_FILE"
fi

# 4. Make sure the env file is git-ignored.
grep -qxF "$ENV_FILE" .gitignore 2>/dev/null || echo "$ENV_FILE" >> .gitignore

# 5. Also export to the current shell so the agent can immediately call the API.
export ALCHEMY_API_KEY="$KEY"
```

> **Why we persist to `.env`:** without it, the key is only set for the current shell session and disappears when the terminal tab closes. App code typically loads `.env` via `dotenv` (Node), `python-dotenv` (Python), `direnv`, or framework-native loaders (Next.js, Vite, Bun, Deno, Rails, etc.), so writing to `.env` is the canonical way to make the key durable for both `npm run dev` and the deployed app's local copy.

> **Why this whole flow works:** the CLI is a runtime executor (`alchemy-cli` skill). When the user has it installed, you can use it to provision the credential that this app-code skill needs, write it to a place the application will load, then hand off to the rest of the `alchemy-api` flow. After step 5, continue with the [Base URLs + auth](#base-urls--auth-cheat-sheet) and [Quickstart](#one-file-quickstart-copypaste) below.

> **Gotcha:** if `auth login` succeeded but `config get api-key` still returns "not found," the CLI's `setup status` may have falsely reported `complete: true` with only an `auth_token`. Re-run `alchemy --json apps select` (or pass an explicit `<id>` with `--no-interactive`) to bind a default app, then retry. See the `alchemy-cli` skill for the same gotcha documented under Preflight.

## Summary

A self-contained guide for AI agents integrating Alchemy APIs using an API key. This file alone should be enough to ship a basic integration. Use the reference files for depth, edge cases, and advanced workflows.

Developers can always create a free API key at [https://dashboard.alchemy.com/](https://dashboard.alchemy.com/).

## Do this first

1. Confirm app-integration scope (see [Mandatory preflight gate](#mandatory-preflight-gate)).
2. Choose the right product using the [Endpoint selector](#endpoint-selector-top-tasks) below.
3. Use the [Base URLs + auth](#base-urls--auth-cheat-sheet) table for the correct endpoint and headers.
4. Copy a [Quickstart example](#one-file-quickstart-copypaste) and test against a testnet first.

## Base URLs + auth (cheat sheet)
| Product | Base URL | Auth | Notes |
| --- | --- | --- | --- |
| Ethereum RPC (HTTPS) | `https://eth-mainnet.g.alchemy.com/v2/$ALCHEMY_API_KEY` | API key in URL | Standard EVM reads and writes. |
| Ethereum RPC (WSS) | `wss://eth-mainnet.g.alchemy.com/v2/$ALCHEMY_API_KEY` | API key in URL | Subscriptions and realtime. |
| Base RPC (HTTPS) | `https://base-mainnet.g.alchemy.com/v2/$ALCHEMY_API_KEY` | API key in URL | EVM L2. |
| Base RPC (WSS) | `wss://base-mainnet.g.alchemy.com/v2/$ALCHEMY_API_KEY` | API key in URL | Subscriptions and realtime. |
| Arbitrum RPC (HTTPS) | `https://arb-mainnet.g.alchemy.com/v2/$ALCHEMY_API_KEY` | API key in URL | EVM L2. |
| Arbitrum RPC (WSS) | `wss://arb-mainnet.g.alchemy.com/v2/$ALCHEMY_API_KEY` | API key in URL | Subscriptions and realtime. |
| BNB RPC (HTTPS) | `https://bnb-mainnet.g.alchemy.com/v2/$ALCHEMY_API_KEY` | API key in URL | EVM L1. |
| BNB RPC (WSS) | `wss://bnb-mainnet.g.alchemy.com/v2/$ALCHEMY_API_KEY` | API key in URL | Subscriptions and realtime. |
| Solana RPC (HTTPS) | `https://solana-mainnet.g.alchemy.com/v2/$ALCHEMY_API_KEY` | API key in URL | Solana JSON-RPC. |
| Solana Yellowstone gRPC | `https://solana-mainnet.g.alchemy.com` | `X-Token: $ALCHEMY_API_KEY` | gRPC streaming (Yellowstone). |
| Sui gRPC | `sui-mainnet.g.alchemy.com:443` | `Authorization: Bearer $ALCHEMY_API_KEY` | Sui gRPC API (objects, txs, balances, streaming). |
| Notify API | `https://dashboard.alchemy.com/api` | `X-Alchemy-Token: <ALCHEMY_NOTIFY_AUTH_TOKEN>` | Generate token in dashboard. |

## Endpoint selector (top tasks)
| You need | Use this | Skill / file |
| --- | --- | --- |
| EVM read/write | JSON-RPC `eth_*` | `references/node-json-rpc.md` |
| Realtime events | `eth_subscribe` | `references/node-websocket-subscriptions.md` |
| Simulate tx | `alchemy_simulateAssetChanges` | `references/data-simulation-api.md` |
| Create webhook | `POST /create-webhook` | `references/webhooks-details.md` |
| Solana DAS | `getAssetsByOwner` (DAS) | `references/solana-das-api.md` |
| Sui objects/txs | `GetObject`, `GetTransaction` (gRPC) | `references/sui-grpc-objects-and-ledger.md` |
| Sui balances | `GetBalance`, `ListBalances` (gRPC) | `references/sui-grpc-state-and-balances.md` |
| Sui checkpoints stream | `SubscribeCheckpoints` (gRPC) | `references/sui-grpc-subscriptions.md` |

## One-file quickstart (copy/paste)

> **No API key?** Use the `agentic-gateway` skill instead. Replace API-key URLs with `https://x402.alchemy.com/eth-mainnet/v2` and add `Authorization: SIWE <token>` (or `SIWS <token>` for a Solana wallet). See the `agentic-gateway` skill for setup.

### EVM JSON-RPC (read)
```bash
curl -s https://eth-mainnet.g.alchemy.com/v2/$ALCHEMY_API_KEY \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"eth_blockNumber","params":[]}'
```

### Create Notify webhook
```bash
curl -s -X POST "https://dashboard.alchemy.com/api/create-webhook" \
  -H "Content-Type: application/json" \
  -H "X-Alchemy-Token: $ALCHEMY_NOTIFY_AUTH_TOKEN" \
  -d '{"network":"ETH_MAINNET","webhook_type":"ADDRESS_ACTIVITY","webhook_url":"https://example.com/webhook","addresses":["0x00000000219ab540356cbb839cbe05303d7705fa"]}'
```

### Verify webhook signature (Node)
```ts
import crypto from "crypto";

export function verify(rawBody: string, signature: string, secret: string) {
  const hmac = crypto.createHmac("sha256", secret).update(rawBody).digest("hex");
  return crypto.timingSafeEqual(Buffer.from(hmac), Buffer.from(signature));
}
```

## Network naming rules
- JSON-RPC and most APIs use lowercase network enums like `eth-mainnet`.
- Notify API uses uppercase enums like `ETH_MAINNET`.

## Common token addresses
| Token | Chain | Address |
| --- | --- | --- |
| ETH | ethereum | `0x0000000000000000000000000000000000000000` |
| WETH | ethereum | `0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2` |
| USDC | ethereum | `0xA0b86991c6218b36c1d19d4a2e9eb0ce3606eB48` |
| USDC | base | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |

## Failure modes + retries
- HTTP `429` means rate limit. Use exponential backoff with jitter.
- JSON-RPC errors come in `error` fields even with HTTP 200.
- Use `pageKey` to resume pagination after failures.
- De-dupe websocket events on reconnect.

## Skill map

For the complete reference index organized by product area, see `references/skill-map.md`.

Quick category overview:
- **Node**: JSON-RPC, WebSocket, Debug, Trace, Enhanced APIs, Utility
- **Webhooks**: Address Activity, Custom (GraphQL), NFT Activity, Payloads, Signatures
- **Solana**: JSON-RPC, DAS, Yellowstone gRPC (streaming), Wallets
- **Sui gRPC**: Objects, Transactions, Balances, Move Packages, Name Service, Subscriptions, Signature Verification
- **Wallets**: Account Kit, Bundler, Gas Manager, Wallet APIs (formerly "Smart Wallets")
- **Rollups**: L2/L3 deployment overview
- **Recipes**: simulation, pending tx subscriptions, webhook flows
- **Operational**: Auth, Rate Limits, Best Practices

## Handing off to other skills

| The user wants to... | Hand off to |
| --- | --- |
| Run a one-off live query, admin command, or on-machine automation in this session (CLI installed) | `alchemy-cli` |
| Run a one-off live query in this session (only MCP wired in) | `alchemy-mcp` |
| Build app code without an API key (autonomous agent, or explicit x402/MPP) | `agentic-gateway` |

## Troubleshooting

### API key not working
- Verify `$ALCHEMY_API_KEY` is set: `echo $ALCHEMY_API_KEY`
- Confirm the key is valid at [dashboard.alchemy.com](https://dashboard.alchemy.com/)
- Check if allowlists restrict the key to specific IPs/domains (see `references/operational-allowlists.md`)

### HTTP 429 (rate limited)
- Use exponential backoff with jitter before retrying
- Check your compute unit budget in the Alchemy dashboard
- See `references/operational-rate-limits-and-compute-units.md` for limits per plan

### Wrong network slug
- JSON-RPC and most APIs use lowercase: `eth-mainnet`, `base-mainnet`
- Notify API uses uppercase: `ETH_MAINNET`, `BASE_MAINNET`
- See `references/operational-supported-networks.md` for the full list

### JSON-RPC error with HTTP 200
- Alchemy returns JSON-RPC errors inside the `error` field even with a 200 status code
- Always check `response.error` in addition to HTTP status

## Official links
- [Developer docs](https://www.alchemy.com/docs)
- [Get Started guide](https://www.alchemy.com/docs/get-started)
- [Create a free API key](https://dashboard.alchemy.com/)
