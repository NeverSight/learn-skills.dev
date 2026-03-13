---
name: gate-dex-trade
description: "Gate DEX trading comprehensive skill. Supports MCP and OpenAPI dual modes: MCP mode calls through gate-wallet service (requires authentication), OpenAPI mode calls directly through AK/SK. Use when users mention swap, exchange, buy, sell, quote, trade. Automatically select the most suitable calling method based on environment."
---

# Gate DEX Trade

> **Trading Comprehensive Skill** — MCP + OpenAPI dual mode support, intelligent routing selects optimal trading method

**Trigger Scenarios**: Use when users mention "swap", "exchange", "buy", "sell", "trade", "quote" and other related operations.

---

## 🎯 Dual Mode Architecture

| Mode | Connection Method | Advantages | Use Cases |
|------|------------------|-----------|-----------|
| 🔗 **MCP Mode** | gate-wallet MCP Server | Unified authentication, wallet ecosystem integration | Complete trading process, cross-Skill collaboration |
| ⚡ **OpenAPI Mode** | AK/SK direct calls | Independent execution, complete lifecycle | Fast trading, full chain control |

---

## 📋 Smart Routing Rules

System automatically selects calling mode based on following priorities:

| Priority | Condition | Selected Mode | Routing Target |
|----------|-----------|---------------|----------------|
| **1** | Explicitly mentions "OpenAPI", "AK/SK" | ⚡ OpenAPI | `references/openapi.md` |
| **2** | Exists `~/.gate-dex-openapi/config.json` | ⚡ OpenAPI | `references/openapi.md` |
| **3** | From wallet Skills cross-Skill calls | 🔗 MCP | Current SKILL.md main process |
| **4** | Default scenario | 🔗 MCP | Current SKILL.md main process |

**User Preferences**:
- Pursue complete ecosystem integration → MCP mode
- Pursue independent fast execution → OpenAPI mode

---

## MCP Server Connection Detection

### First Session Detection

**Before first MCP tool call in session, perform one connection probe to confirm Gate Wallet MCP Server availability. No need to repeat detection for subsequent operations.**

```
CallMcpTool(server="gate-wallet", toolName="chain.config", arguments={chain: "eth"})
```

| Result | Handling |
|--------|----------|
| Success | MCP Server available, subsequent operations directly call business tools, no need to probe again |
| Failure | Display configuration guidance based on error type (see error handling below) |

### Runtime Error Fallback

If business tool calls fail during subsequent operations (returning connection errors, timeouts etc.), handle according to following rules:

| Error Type | Keywords | Handling |
|------------|----------|----------|
| MCP Server not configured | `server not found`, `unknown server` | Display MCP Server configuration guidance |
| Remote service unreachable | `connection refused`, `timeout`, `DNS error` | Prompt to check server status and network connection |
| Authentication failed | `401`, `unauthorized`, `x-api-key` | Prompt to contact administrator for API Key |

---

## Authentication Description

All operations in MCP mode **require `mcp_token`**. Must confirm user is logged in before calling any tool.

- If currently no `mcp_token` → Guide to `gate-dex-wallet/references/auth` to complete login then return
- If `mcp_token` expired (MCP Server returns token expired error) → First try `auth.refresh_token` silent refresh, guide re-login if failed

---

## MCP Tool Call Specification (Main Process)

### 1. `tx.quote` — Get Swap Quote

Get Swap quote from input token to output token.

| Field | Description |
|-------|-------------|
| **Tool Name** | `tx.quote` |
| **Parameters** | `{ chain_id_in: string, chain_id_out: string, token_in: string, token_out: string, amount: string, slippage?: number, user_wallet: string, native_in?: boolean, native_out?: boolean, mcp_token: string }` |
| **Return** | Quote details including exchange rate, slippage, routing path, estimated Gas etc |

### 2. `tx.swap` — Execute Swap

One-shot Swap execution (Quote→Build→Sign→Submit single call).

| Field | Description |
|-------|-------------|
| **Tool Name** | `tx.swap` |
| **Parameters** | Same as `tx.quote` + `account_id` |
| **Return** | Transaction result |

### 3. `tx.swap_detail` — Query Swap Status

(Other MCP tool specifications...)

---

## Sub-module Routing

Route to specific implementation based on mode detection result and user intent:

| Routing Condition | Target | Description |
|-------------------|---------|-------------|
| OpenAPI environment + related intent | references/openapi.md | Complete OpenAPI call specification |
| MCP environment + trading intent | Current SKILL.md main process | MCP tool calls and three-step confirmation process |

---

## Operation Process

### Process A: Smart Mode Selection

```text
First session detection (if needed)
  ↓
Environment detection:
  1. Check ~/.gate-dex-openapi/config.json
  2. Check gate-wallet MCP Server
  ↓
Select calling mode based on detection result:
  → OpenAPI mode: references/openapi.md
  → MCP mode: Current main process
```

### Process B: MCP Swap Execution (Main Process)

```text
Authentication check → Balance verification → Trading pair confirmation 
  → tx.quote → Quote display → Signature authorization confirmation 
    → tx.swap → tx.swap_detail
```

---

## Cross-Skill Collaboration

| Caller | Scenario | Tool Used |
|--------|----------|-----------|
| `gate-dex-wallet` | User views balance then wants to exchange tokens | MCP mode call |
| `gate-dex-market` | User views market then wants to buy certain token | MCP mode call |

---

## Supported Chains

| Chain ID | Network Name | MCP Support | OpenAPI Support |
|----------|--------------|-------------|-----------------|
| `eth` / `1` | Ethereum | ✅ | ✅ |
| `bsc` / `56` | BNB Smart Chain | ✅ | ✅ |
| `polygon` / `137` | Polygon | ✅ | ✅ |
| `arbitrum` / `42161` | Arbitrum One | ✅ | ✅ |
| `optimism` / `10` | Optimism | ✅ | ✅ |
| `avax` / `43114` | Avalanche | ✅ | ✅ |
| `base` / `8453` | Base | ✅ | ✅ |
| `sol` / `501` | Solana | ✅ | ✅ |

---

## Security Rules

1. **Mode selection transparency**: Clearly inform users of current calling mode and reason
2. **Authentication isolation**: MCP mode uses `mcp_token`, OpenAPI mode uses AK/SK
3. **Three-step confirmation gating**: MCP mode includes trading pair confirmation → quote display → signature authorization confirmation
4. **Balance verification**: Mandatory check asset sufficiency before trading
5. **Risk alerts**: Mandatory warning when price difference > 5%, high slippage MEV risk alerts