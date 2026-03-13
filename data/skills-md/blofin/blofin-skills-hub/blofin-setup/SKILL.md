---
name: blofin-setup
description: "Set up and configure the BloFin MCP server. Guides through API key creation, MCP configuration, connection verification, and switching between demo/production environments."
version: 1.0.0
license: Apache-2.0
metadata:
  openclaw:
    emoji: "🔧"
    requires:
      bins:
        - node
        - npm
      env:
        - BLOFIN_API_KEY
        - BLOFIN_API_SECRET
        - BLOFIN_PASSPHRASE
    primaryEnv: BLOFIN_API_KEY
---

# BloFin Setup

Guide users through setting up and configuring the BloFin MCP server for trading on BloFin exchange.

## Prerequisites

- Node.js (v18+) and npm installed
- A BloFin account at [blofin.com](https://blofin.com)

## Setup Steps

### 1. Install blofin-mcp

```bash
npm install -g blofin-mcp
```

Or install locally:

```bash
git clone https://github.com/your-org/blofin-mcp.git
cd blofin-mcp
npm install
npm run build
```

### 2. Create BloFin API Keys

Direct the user to [BloFin API Management](https://blofin.com/account/apis):

1. Log in to BloFin
2. Navigate to **Account** > **API Management**
3. Click **Create API Key**
4. Set permissions:
   - `READ` — view balances, order history, positions
   - `TRADE` — place and cancel orders
   - `TRANSFER` — move funds between accounts
5. Set a **Passphrase** (remember this)
6. (Recommended) Bind to IP whitelist for security
7. Save the **API Key** and **Secret Key** — the secret is shown only once

### 3. Configure MCP Server

Add the blofin MCP server to your agent's MCP configuration (e.g. `mcp.json` or `settings.json`):

```json
{
  "mcpServers": {
    "blofin": {
      "command": "node",
      "args": ["/path/to/blofin-mcp/dist/index.js"],
      "env": {
        "BLOFIN_API_KEY": "your-api-key",
        "BLOFIN_API_SECRET": "your-api-secret",
        "BLOFIN_PASSPHRASE": "your-passphrase",
        "BLOFIN_BROKER_ID": "your-broker-id (optional)",
        "BLOFIN_BASE_URL": "https://openapi.blofin.com"
      }
    }
  }
}
```

Replace `/path/to/blofin-mcp` with the actual installation path (e.g., the global npm path or the local clone directory).

### 4. Base URL Configuration

| Environment | Base URL | Use Case |
|-------------|----------|----------|
| **Demo Trading** | `https://demo-trading-openapi.blofin.com` | Testing, learning, paper trading |
| **Production** | `https://openapi.blofin.com` | Real money trading |

- Default is demo trading if `BLOFIN_BASE_URL` is not set
- **Always start with demo trading** to verify your setup works correctly
- Switch to production only after successful demo testing

### 5. Verify Connection

After configuration, verify the setup works:

1. Use `get_apikey_info` to verify API key permissions and status
2. Use `get_tickers` with `instId: "BTC-USDT"` to test public data access
3. Use `get_balance` to verify authenticated access
4. Check that the API key has the expected permissions (`readOnly` field: 0 = Read+Write, 1 = Read only)

### 6. Troubleshooting

| Issue | Solution |
|-------|----------|
| Signature verification failed | Check that API secret and passphrase are correct; ensure no extra spaces |
| IP not in whitelist (152406) | Add your current IP to the API key's whitelist on BloFin |
| Access key expired (152402) | Keys without IP binding expire after 90 days; recreate or bind an IP |
| Rate limit (429) | Reduce request frequency; REST API limit is 500/min per IP |
| Connection timeout | Check your network; verify the base URL is correct |

## Environment Variables Reference

| Variable | Required | Description |
|----------|:--------:|-------------|
| `BLOFIN_API_KEY` | Yes | Your BloFin API key |
| `BLOFIN_API_SECRET` | Yes | Your BloFin API secret key |
| `BLOFIN_PASSPHRASE` | Yes | The passphrase set when creating the API key |
| `BLOFIN_BROKER_ID` | No | Broker ID for order attribution (provided by BloFin) |
| `BLOFIN_BASE_URL` | No | API base URL (defaults to demo trading endpoint) |

## Security Best Practices

- Never share or expose your API secret and passphrase
- Always bind API keys to specific IP addresses in production
- Use the minimum required permissions for your use case
- Regularly rotate API keys
- Start with `READ` permission only and upgrade as needed
