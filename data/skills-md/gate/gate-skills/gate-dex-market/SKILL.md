---
name: gate-dex-market
description: "Gate DEX market data skill. Uses AK/SK authentication to call Gate DEX OpenAPI, providing token and market quote read-only queries. Use when users mention quotes, prices, token information, rankings, security audits."
---

# Gate DEX Market

> **Market Data Skill** — OpenAPI mode, AK/SK authentication for direct API calls

**Trigger Scenarios**: Use when users mention "quotes", "K-line", "prices", "token information", "rankings", "security audit", "market data", and other related operations.

---

## 🎯 Architecture

| Mode | Connection Method | Advantages | Use Cases |
|------|---------|------|---------|
| ⚡ **OpenAPI Mode** | AK/SK direct calls | Strong independence, fast response | Market data queries, token information, security audits |

---

## 📋 Environment Detection

Before first API call, check if credentials are configured:

| Condition | Handling |
|--------|---------|
| `~/.gate-dex-openapi/config.json` exists | Read credentials and proceed with API calls |
| Config file not found | Auto-create with default credentials, prompt user to configure dedicated AK/SK |

---

## 🔧 Configuration

**Config file**: `~/.gate-dex-openapi/config.json`

```json
{
  "api_key": "your_api_key",
  "secret_key": "your_secret_key"
}
```

**First use**: If file doesn't exist, Skill will auto-create config with built-in default credentials; recommend visiting [Gate DEX Developer Platform](https://www.gatedex.com/developer) to create dedicated AK/SK for better rate limiting and experience.

---

## 📖 Complete Specification

All API call specifications, signature algorithms, request/response formats are documented in:

**→ [references/openapi.md](./references/openapi.md)**

This includes:
- HMAC-SHA256 signature algorithm
- 9 API actions (6 token-type + 3 market-type)
- Request/response examples
- Error handling

---

## Skill Routing

Post-market data query follow-up operation guidance:

| User Intent | Target Skill |
|---------|-----------|
| Buy/sell tokens | `gate-dex-trade` |
| Transfer tokens | `gate-dex-wallet/references/transfer` |
| View holdings | `gate-dex-wallet` |
| View trading/Swap history | `gate-dex-wallet` |
| Interact with DApp | `gate-dex-wallet/references/dapp` |

---

## Cross-Skill Workflows

### Called by Other Skills

This Skill serves as market data and security information provider, commonly called by these Skills:

| Caller | Call Scenario | Tool Used |
|--------|---------|---------|
| `gate-dex-trade` | Query token info before Swap to help parse addresses | `token_get_coin_info` |
| `gate-dex-trade` | Security audit target token before Swap | `token_get_risk_info` |
| `gate-dex-trade` | Query available token list before Swap | `token_list_swap_tokens` |
| `gate-dex-trade` | Query available tokens on target chain before cross-chain bridge | `token_list_cross_chain_bridge_tokens` |
| `gate-dex-wallet/references/dapp` | Contract security audit before DApp transactions | `token_get_risk_info` |

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

1. **Credential Security**: `secret_key` must not be displayed in plain text
2. **Read-only Nature**: All operations are data queries only, no on-chain writes involved
3. **Objective Display**: Price, rankings, and other data presented objectively, no investment advice provided