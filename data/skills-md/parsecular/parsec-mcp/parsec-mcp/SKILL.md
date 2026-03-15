---
name: parsec-mcp
description: Trade and monitor prediction markets across Polymarket, Kalshi, Opinion, Limitless, and PredictFun — unified data, live streaming, and execution from any AI agent
---

# Parsec

Unified prediction market trading across Polymarket, Kalshi, Opinion, Limitless, and PredictFun — real-time data, live orderbooks, and order execution from any AI agent. One API key, one interface, five exchanges.

## Setup

Ask the user for their Parsec API key. If they don't have one, direct them to [app.parsecapi.com](https://app.parsecapi.com) to create an account. Then pick one of the options below and substitute the key. After setup, restart the session for the MCP server to become available.

### Option A: Remote server (recommended)

No install needed. Add the hosted MCP server to your client config:

**Claude Code:**
```bash
claude mcp add parsec --transport http https://mcp.parsecapi.com/mcp -H "Authorization: Bearer pk_live_..."
```

**Claude Desktop / Cursor / VS Code / Windsurf / Cline:**
```json
{
  "mcpServers": {
    "parsec": {
      "url": "https://mcp.parsecapi.com/mcp",
      "headers": { "Authorization": "Bearer pk_live_..." }
    }
  }
}
```

### Option B: Local server

Run the MCP server on your machine via npx:

**Claude Code:**
```bash
claude mcp add parsec -- env PARSEC_API_KEY=pk_live_... npx -y parsec-mcp
```

**Claude Desktop / Cursor / VS Code / Windsurf / Cline:**
```json
{
  "mcpServers": {
    "parsec": {
      "command": "npx",
      "args": ["-y", "parsec-mcp"],
      "env": { "PARSEC_API_KEY": "pk_live_..." }
    }
  }
}
```

## Key Concept

`parsec_id` is the universal market identifier: `{exchange}:{native_id}` (e.g. `kalshi:BTC-100K-2026`, `polymarket:0x1a2b...`). Every tool that takes a market uses this format. Outcomes are named strings like `"Yes"`, `"No"`, or categorical labels.

## Rules

- **Start with composite tools.** `find_market`, `get_market_snapshot`, `preview_order`, and `open_market_feed` handle multi-step resolution automatically — prefer them over low-level tools.
- **Always preview before trading.** Call `parsec.trade.preview_order` before `parsec.trade.create_order`. Never place an order without explicit user confirmation.
- **Dangerous tools** — `create_order`, `cancel_order`, and `delete_user` can lose money or are irreversible. Always confirm with the user first.
- **`find_market` for natural language, `list_markets` for structured queries.** Don't mix them up. `list_markets` requires a scope + selector — it rejects empty calls.
- **Credential handling:** Never echo, log, or surface API keys or exchange credentials in responses.

## Workflows

### Market Research

1. `parsec.market.find_market` — search by topic
2. `parsec.market.get_market_snapshot` — metadata + orderbook + recent trades in one call

### Trading

1. `parsec.account.get_trading_setup_status` — verify account is ready
2. `parsec.trade.preview_order` — estimate cost, show balance
3. **Get explicit user confirmation**
4. `parsec.trade.create_order` — execute
5. `parsec.trade.get_order` — monitor status

### Live Streaming

1. `parsec.stream.open_market_feed` — opens, authenticates, and subscribes in one call
2. `parsec.stream.read` — consume orderbook snapshots, deltas, and trades
3. `parsec.stream.close` — clean up when done (sessions auto-close after 10 min idle, max 8 concurrent)

## Tool Reference

### Composite Tools (Start Here)

| Tool | Description |
|------|-------------|
| `parsec.market.find_market` | Search for markets by keyword, parsec_id, or exchange-native ID |
| `parsec.market.get_market_snapshot` | Market metadata + orderbook + recent trades in one call |
| `parsec.trade.preview_order` | Simulate an order with execution price and balance context |
| `parsec.account.get_trading_setup_status` | Check if the account is ready to trade |
| `parsec.stream.open_market_feed` | One-step real-time WebSocket feed setup |

### Market Data

| Tool | Description |
|------|-------------|
| `parsec.market.list_exchanges` | List supported exchanges and their status |
| `parsec.market.list_markets` | Search, filter, and resolve markets with cursor pagination |
| `parsec.market.get_orderbook` | Live bid/ask levels for a market outcome |
| `parsec.market.get_execution_price` | Estimate fill price for a hypothetical order |
| `parsec.market.get_price` | Current mid-market price for an outcome |
| `parsec.market.list_trades` | Recent trades for a market |
| `parsec.market.list_events` | List multi-market event groups |

### Trading

| Tool | Description |
|------|-------------|
| `parsec.trade.create_order` | Place a live order on any exchange |
| `parsec.trade.cancel_order` | Cancel an open order |
| `parsec.trade.list_orders` | List orders with status/exchange filters |
| `parsec.trade.get_order` | Get order details by ID |
| `parsec.trade.list_positions` | Current open positions |
| `parsec.trade.list_fills` | Executed trade fills |
| `parsec.trade.get_balance` | Exchange balance (total, available, reserved) |

### Real-Time Streaming

| Tool | Description |
|------|-------------|
| `parsec.stream.open_market_feed` | One-step feed setup (recommended) |
| `parsec.stream.connect` | Open a WebSocket session |
| `parsec.stream.auth` | Authenticate a session |
| `parsec.stream.subscribe` | Subscribe to market feeds |
| `parsec.stream.unsubscribe` | Remove subscriptions |
| `parsec.stream.resync` | Request orderbook resync |
| `parsec.stream.read` | Read buffered messages |
| `parsec.stream.close` | Close a session |

### Account & Wallet

| Tool | Description |
|------|-------------|
| `parsec.account.ping` | Check API connectivity |
| `parsec.account.get_usage` | API usage stats |
| `parsec.account.get_ws_usage` | WebSocket usage stats |
| `parsec.account.get_user_activity` | Recent account activity |
| `parsec.account.onboard` | Complete account onboarding |
| `parsec.wallet.get_state` | Wallet and exchange link status |

### Builder (Multi-Tenant)

| Tool | Description |
|------|-------------|
| `parsec.builder.create_user` | Create an end-user |
| `parsec.builder.list_users` | List all end-users |
| `parsec.builder.get_user` | Get end-user details |
| `parsec.builder.update_user` | Update end-user profile |
| `parsec.builder.delete_user` | Delete an end-user (irreversible) |
| `parsec.builder.onboard_user` | Onboard end-user for trading |
| `parsec.builder.get_pool` | Liquidity pool status |
| `parsec.builder.get_escrow_config` | Escrow configuration |

### Polymarket CTF

| Tool | Description |
|------|-------------|
| `parsec.ctf.split` | Split USDC into conditional tokens |
| `parsec.ctf.merge` | Merge tokens back into USDC |
| `parsec.ctf.redeem` | Redeem winning tokens after resolution |

## Example Prompts

- "What prediction markets are available about Bitcoin?"
- "Show me the orderbook for the Trump 2028 market on Polymarket"
- "What's my Kalshi balance?"
- "Preview buying 50 Yes contracts on that market"
- "Open a live feed for the ETH price market"
- "Am I set up to trade?"

## Pricing & Rate Limits

Free tier included — no credit card required.

| Tier | Price | Requests/sec | Burst | Monthly Quota | WS Subscriptions | Orderbook Depth | History |
|------|-------|-------------|-------|--------------|-------------------|-----------------|---------|
| **Free** | $0 | 5 | 5 | 10,000 | 3 | 10 levels | 5 days |
| **Pro** | $75/mo | 60 | 120 | 5,000,000 | 500 | 100 levels | 30 days |
| **Scale** | $250/mo | 200 | 400 | Unlimited | 2,000 | 100 levels | Unlimited |
| **Enterprise** | Custom | Custom | Custom | Unlimited | Custom | Custom | Unlimited |

Sign up at [app.parsecapi.com](https://app.parsecapi.com).

## Docs

Full documentation: [docs.parsecapi.com](https://docs.parsecapi.com)
