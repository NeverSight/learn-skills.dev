---
name: goldrush-cli
description: "GoldRush CLI — terminal-first blockchain data tool with MCP support for Claude Desktop and Claude Code. Use this skill whenever the user wants to query blockchain data from the command line, stream DEX pairs or wallet activity in a terminal, set up GoldRush as an MCP tool provider, or run quick one-off queries without writing code (e.g., 'check a wallet balance', 'what's the gas price', 'search for a token'). Also use this when the user mentions 'goldrush' CLI commands, 'npx @covalenthq/goldrush-cli', or MCP integration with GoldRush. The CLI is the fastest path for ad-hoc blockchain lookups from the terminal. If the user needs programmatic API access in an application, use goldrush-foundational-api or goldrush-streaming-api instead. If the user needs pay-per-request access without an API key, use goldrush-x402 instead."
---

# GoldRush CLI

Terminal-first blockchain data tool with MCP support for AI agents. Query wallets, stream DEX pairs, and pipe live on-chain data directly into Claude — all from the command line.

## Quick Start

```bash
# Install and authenticate
npx @covalenthq/goldrush-cli auth

# Query wallet balances
goldrush balances eth-mainnet vitalik.eth

# Stream new DEX pairs
goldrush new_pairs solana-mainnet raydium

# Set up MCP for Claude
goldrush install
```

## Commands

Commands span portfolio management, market discovery, trading intelligence, and utilities. For the full reference with all parameters and examples, see [overview.md](references/overview.md).

### Portfolio & Wallets
- `goldrush balances <chain> <address>` — full token portfolio with USD values and 24h changes
- `goldrush transfers <address> <chain>` — transfer history for any wallet
- `goldrush watch <address> <chain>` — real-time wallet activity streaming

### Market Discovery
- `goldrush new_pairs <chain> [protocols...]` — live stream of new DEX liquidity pairs
- `goldrush ohlcv_pairs <pair> <chain> [-i interval]` — live OHLCV candlestick charts in ASCII

### Trading Intelligence
- `goldrush traders <token> <chain>` — top traders ranked by unrealized PnL
- `goldrush gas [chain]` — real-time gas price estimates
- `goldrush search <query>` — find tokens by name, symbol, or address

### Utilities
- `goldrush chains` — list supported chains
- `goldrush auth` — set API key (stored in OS keychain)
- `goldrush install` — configure Claude for MCP integration
- `goldrush config` — view/update settings
- `goldrush status` — check API key and connectivity
- `goldrush logout` — clear session data

## Critical Rules

1. **Chain names use kebab-case** — `eth-mainnet`, `solana-mainnet` (same as Foundational API)
2. **Authentication** — API key stored in OS keychain via `goldrush auth`, not environment variables
3. **MCP requires setup** — run `goldrush install` before Claude can use GoldRush tools
4. **Streaming commands** — `new_pairs`, `ohlcv_pairs`, and `watch` use the Streaming API under the hood
5. **Output is formatted tables** — designed for human-readable terminal output; pipe into Claude for AI processing

## MCP Integration

The CLI is an MCP server. Running `goldrush install` registers GoldRush as a tool provider for Claude. Agents can then call GoldRush commands natively — no wrappers or manual configuration needed.

## Reference Files

| File | When to read |
|------|-------------|
| [overview.md](references/overview.md) | Need full command reference with parameters, usage examples, or MCP setup details |
