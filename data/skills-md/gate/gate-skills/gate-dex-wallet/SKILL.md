---
name: gate-dex-wallet
version: "2026.3.12-1"
updated: "2026-03-12"
description: "Gate DEX comprehensive wallet skill. Unified entry point supporting: authentication login, asset queries, transfer execution, DApp interactions, CLI command-line for five major modules. Use when users mention login, check balance, transfer, DApp interaction, signing, gate-wallet, CLI, command-line, openapi-swap and other wallet-related operations. Route to specific operation reference files through sub-function routing."
---

# Gate DEX Wallet

> **Comprehensive Wallet Skill** — Unified entry point for authentication, assets, transfers, DApp interactions, and CLI command-line. 5 major modules through sub-function routing distribution.

**Trigger Scenarios**: Use this Skill when users mention "login", "check balance", "transfer", "DApp", "sign", "wallet", "assets", "gate-wallet", "CLI", "command-line", "openapi-swap" and other wallet-related operations.

---

## Core Modules

| Module | Description | Typical Scenarios |
|------|------|---------|
| 🔐 **Authentication** | Google OAuth login, Token management | "login", "logout", "token expired" |
| 💰 **Assets** | Balance queries, address retrieval, transaction history | "check balance", "total assets", "transaction history" |
| 💸 **Transfer** | Gas estimation, transaction building, signature broadcast | "transfer", "send tokens", "batch transfer" |
| 🎯 **DApp** | Wallet connection, message signing, contract interaction | "connect DApp", "sign message", "Approve" |
| 🖥️ **CLI** | gate-wallet CLI dual-channel (MCP custodial signing + OpenAPI hybrid mode) | "gate-wallet", "CLI", "command-line", "openapi-swap", "hybrid swap" |

---

## Routing Rules

Route to corresponding sub-function reference files based on user intent:

| User Intent | Example Keywords | Reference File |
|---------|-----------|---------|
| **Authentication login** | "login", "login", "auth", "token expired", "session" | [references/auth.md](./references/auth.md) |
| **Asset queries** | "check balance", "total assets", "wallet address", "transaction history", "Swap history" | Keep current SKILL.md main flow |
| **Transfer operations** | "transfer", "send", "transfer", "batch transfer", "Gas fee" | [references/transfer.md](./references/transfer.md) |
| **DApp interactions** | "DApp", "sign message", "Approve", "connect wallet", "contract call" | [references/dapp.md](./references/dapp.md) |
| **CLI operations** | "gate-wallet", "CLI", "command-line", "openapi-swap", "hybrid swap", "hybrid mode swap" | [references/cli.md](./references/cli.md) |

---

## MCP Server Connection Detection

### Initial Session Detection

**Execute connection probe once before first MCP tool call in session to confirm Gate Wallet MCP Server availability. No need to repeat detection for subsequent operations.**

```text
CallMcpTool(server="gate-wallet", toolName="chain.config", arguments={chain: "eth"})
```

| Result | Handling |
|------|------|
| Success | MCP Server available, continue executing user-requested specific operations |
| Failure | Show configuration guidance based on error type (see error handling below) |

### Runtime Error Fallback

For subsequent operations, if business tool calls fail (connection error, timeout, etc.), handle according to the following rules:

| Error Type | Keywords | Handling |
|---------|--------|------|
| MCP Server not configured | `server not found`, `unknown server` | Show MCP Server configuration guidance |
| Remote service unreachable | `connection refused`, `timeout`, `DNS error` | Suggest checking server status and network connection |
| Authentication failure | `401`, `unauthorized`, `x-api-key` | Suggest contacting administrator for API Key |

---

## Authentication State Management

All operations requiring authentication (asset queries, transfers, DApp interactions) need valid `mcp_token`:

- If currently no `mcp_token` → Guide to `references/auth.md` to complete login then return
- If `mcp_token` expired (MCP Server returns token expired error) → First try `auth.refresh_token` silent refresh, guide to re-login if failed

---

## MCP Tool Call Specifications (Asset Query Module)

### 1. `wallet.get_token_list` — Query Token Balances

Query token balance list for specified chain or all chains.

| Field | Description |
|------|------|
| **Tool Name** | `wallet.get_token_list` |
| **Parameters** | `{ chain?: string, network_keys?: string, account_id?: string, mcp_token: string, page?: number, page_size?: number }` |
| **Return Value** | Token array, each item contains `symbol`, `balance`, `price`, `value`, `chain`, `contract_address`, etc. |

Call example:

```text
CallMcpTool(
  server="gate-wallet",
  toolName="wallet.get_token_list",
  arguments={ chain: "ETH", mcp_token: "<mcp_token>" }
)
```

### 2. `wallet.get_total_asset` — Query Total Asset Value

| Field | Description |
|------|------|
| **Tool Name** | `wallet.get_total_asset` |
| **Parameters** | `{ account_id: string, mcp_token: string }` |
| **Return Value** | `{ total_value_usd: number, chains: Array<{chain: string, value_usd: number}> }` |

### 3. `wallet.get_addresses` — Get Wallet Addresses

| Field | Description |
|------|------|
| **Tool Name** | `wallet.get_addresses` |
| **Parameters** | `{ account_id: string, mcp_token: string }` |
| **Return Value** | Wallet address objects for each chain |

### 4. `chain.config` — Chain Configuration Info

| Field | Description |
|------|------|
| **Tool Name** | `chain.config` |
| **Parameters** | `{ chain: string, mcp_token: string }` |
| **Return Value** | Chain configuration info (RPC, block explorer, etc.) |

### 5. `tx.list` — Wallet comprehensive (auth, assets, transfer, DApp) transaction list

| Field | Description |
|------|------|
| **Tool Name** | `tx.list` |
| **Parameters** | `{ account_id: string, chain?: string, page?: number, limit?: number, mcp_token: string }` |
| **Return Value** | Transaction history array |

### 6. `tx.detail` — Transaction Details

| Field | Description |
|------|------|
| **Tool Name** | `tx.detail` |
| **Parameters** | `{ hash_id: string, chain: string, mcp_token: string }` |
| **Return Value** | Detailed transaction information |

### 7. `tx.history_list` — Swap History Records

| Field | Description |
|------|------|
| **Tool Name** | `tx.history_list` |
| **Parameters** | `{ account_id: string, chain?: string, page?: number, limit?: number, mcp_token: string }` |
| **Return Value** | Swap history array |

---

## Operation Flows

### Flow A: Query Token Balances

```text
Step 0: MCP Server connection detection
  ↓ Success

Step 1: Authentication check
  Confirm holding valid mcp_token and account_id
  No token → Route to references/auth.md
  ↓

Step 2: Execute query
  Call wallet.get_token_list({ chain?, network_keys?, mcp_token })
  ↓

Step 3: Format display
  Group by chain, sort by value, filter zero balances
```

### Flow B: Query Total Asset Value

```text
Step 0-1: Same as Flow A
  ↓

Step 2: Execute query
  Call wallet.get_total_asset({ account_id, mcp_token })
  ↓

Step 3: Format display
  Total value + distribution by chain
```

### Flow C-G: Other Asset Query Flows

Similar to above flows, detailed specifications see original SKILL.md content.

---

## Skill Routing

Post-asset viewing follow-up operation guidance:

| User Intent | Target |
|---------|------|
| View token prices, K-line charts | `gate-dex-market` |
| View token security audits | `gate-dex-market` |
| Transfer, send tokens | This Skill `references/transfer.md` |
| Swap/Exchange tokens | `gate-dex-trade` |
| Interact with DApps | This Skill `references/dapp.md` |
| Login/Auth expired | This Skill `references/auth.md` |
| Use CLI / command-line operations / hybrid mode Swap | This Skill `references/cli.md` |

---

## Cross-Skill Collaboration

This Skill serves as **wallet data center**, called by other Skills:

| Caller | Scenario | Used Tools |
|--------|------|---------|
| `gate-dex-trade` | Pre-swap balance validation, token address resolution | `wallet.get_token_list` |
| `gate-dex-trade` | Get chain-specific wallet address | `wallet.get_addresses` |
| `gate-dex-market` | Guide to view holdings after market data query | `wallet.get_token_list` |
| CLI sub-module | CLI dual-channel operations (MCP custodial signing / OpenAPI hybrid Swap) | `references/cli.md` |

---

## Supported Chains

| Chain ID | Network Name | Type |
|--------|----------|------|
| `eth` | Ethereum | EVM |
| `bsc` | BNB Smart Chain | EVM |
| `polygon` | Polygon | EVM |
| `arbitrum` | Arbitrum One | EVM |
| `optimism` | Optimism | EVM |
| `avax` | Avalanche C-Chain | EVM |
| `base` | Base | EVM |
| `sol` | Solana | Non-EVM |

---

## Security Rules

1. **Authentication check**: Check `mcp_token` validity before all operations
2. **Sensitive information**: `mcp_token` must not be displayed in plain text in conversations
3. **Auto refresh**: Prioritize silent refresh when token expires
4. **Guidance mechanism**: Guide to `references/auth.md` when authentication fails
5. **Cross-Skill security**: Provide secure balance validation and address retrieval for other Skills