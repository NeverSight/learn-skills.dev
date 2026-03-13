---
name: gate-mcp-openclaw-installer
description: One-click installer for all Gate.com MCP servers including spot/futures trading, DEX, market info, and news. Use when users need to install, configure, or manage Gate MCP servers with mcporter.
---

# Gate MCP

Complete Gate.com MCP server installer for OpenClaw.

## Quick Start

```bash
# Install all Gate MCP servers (default)
./scripts/install.sh

# Selective installation
./scripts/install.sh --select
```

## MCP Servers

| Server | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `gate` | `npx -y gate-mcp` | API Key + Secret | Spot/Futures/Options trading |
| `gate-dex` | `https://api.gatemcp.ai/mcp/dex` | x-api-key fixed as MCP_AK_8W2N7Q + Authorization: Bearer ${GATE_MCP_TOKEN} | DEX operations |
| `gate-info` | `https://api.gatemcp.ai/mcp/info` | None | Market data |
| `gate-news` | `https://api.gatemcp.ai/mcp/news` | None | News feed |

## Installation Modes

### 1. Install All (Default)
```bash
./scripts/install.sh
```
Installs all 4 servers. Prompts for API credentials when needed.

### 2. Selective Install
```bash
./scripts/install.sh --select
# or
./scripts/install.sh -s
```
Interactive menu to choose specific server.

## Common Commands

```bash
# Market data (no auth)
mcporter call gate-info.list_tickers currency_pair=BTC_USDT
mcporter call gate-news.list_news

# Trading (requires auth)
mcporter call gate.list_spot_accounts
mcporter call gate.list_tickers currency_pair=ETH_USDT

# Wallet (requires auth)
mcporter call gate-dex.list_balances
```

## API Configuration

### Getting API Keys
1. Visit https://www.gate.com/myaccount/profile/api-key/manage
2. Create API key with permissions:
   - **Read** - Market data, account info
   - **Trade** - Spot/Margin/Futures trading
   - **Withdraw** - Wallet operations

### Gate-Dex authorization
When a **gate-dex** query (e.g. list_balances, transfer, swap) returns "need authorization": (1) Open [https://web3.gate.com/](https://web3.gate.com/) to create or bind a wallet if needed; (2) The assistant will return a **clickable** Google authorization link—click it to complete OAuth. The installer uses a fixed x-api-key.

### Storing Credentials
The installer securely stores credentials in mcporter config.

## Troubleshooting

**mcporter not found**
```bash
npm install -g mcporter
```

**Connection failed**
- Verify API keys are correct
- Check network connectivity
- Ensure mcporter daemon is running: `mcporter daemon status`

## References

- [Gate MCP GitHub](https://github.com/gate/gate-mcp)
- [Gate Skills](https://github.com/gate/gate-skills)
- [Gate API Docs](https://www.gate.com/docs/developers/apiv4/en/)
