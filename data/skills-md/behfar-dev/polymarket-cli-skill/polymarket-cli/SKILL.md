---
name: polymarket-cli
description: "Guide for using the Polymarket CLI — a Rust-based command-line tool for browsing prediction markets, placing trades, managing wallets, and interacting with on-chain contracts on Polymarket. Use this skill whenever the user mentions Polymarket, prediction markets CLI, polymarket-cli, trading from terminal, market odds, CLOB order book, conditional tokens (CTF), or wants to browse/trade prediction markets programmatically. Also trigger when the user wants to script against Polymarket data, check market prices, place limit or market orders, manage positions, or interact with Polymarket's API from a terminal or automated workflow."
---

# Polymarket CLI Skill

The Polymarket CLI is an open-source Rust tool that lets you browse prediction markets, place orders, manage positions, and interact with on-chain contracts — all from a terminal. It also works as a JSON API for scripts and agents.

> **This is early, experimental software.** Use small amounts only. APIs and behavior may change without notice. Always verify transactions before confirming.

## When to Read Reference Files

This SKILL.md covers the conceptual overview, installation, configuration, and common workflows. For detailed command references with every flag and option, read the appropriate file in `references/`:

- `references/commands-browsing.md` — Markets, events, tags, series, comments, profiles, sports (read-only, no wallet needed)
- `references/commands-trading.md` — CLOB trading, order management, balances, rewards, API keys (wallet required)
- `references/commands-onchain.md` — CTF operations (split/merge/redeem), contract approvals, bridging, on-chain data queries
- `references/commands-wallet.md` — Wallet creation/import, setup wizard, shell mode, upgrade

## Installation

Three ways to install:

**Homebrew (macOS/Linux):**
```bash
brew tap Polymarket/polymarket-cli https://github.com/Polymarket/polymarket-cli
brew install polymarket
```

**Shell script:**
```bash
curl -sSL https://raw.githubusercontent.com/Polymarket/polymarket-cli/main/install.sh | sh
```

**Build from source** (requires Rust 1.88+):
```bash
git clone https://github.com/Polymarket/polymarket-cli
cd polymarket-cli
cargo install --path .
```

## Architecture Overview

The CLI is built in Rust with `clap` for argument parsing and `tokio` for async I/O. It wraps the `polymarket-client-sdk` crate, which handles all API communication and on-chain interactions.

The code is organized as:
- `main.rs` — CLI entry point, clap parsing, error handling
- `auth.rs` — Wallet resolution, RPC provider setup, CLOB authentication
- `config.rs` — Config file management at `~/.config/polymarket/config.json`
- `shell.rs` — Interactive REPL with command history
- `commands/` — One module per command group (markets, clob, ctf, data, etc.)
- `output/` — Table and JSON rendering for each command group

The tool connects to three main backends: the Gamma API (market metadata, search), the CLOB API (order book, trading), and Polygon RPC (on-chain operations like approvals and CTF token management).

## Configuration

### Private Key Resolution

The CLI resolves the private key in this priority order:
1. `--private-key 0xabc...` flag (per-command override)
2. `POLYMARKET_PRIVATE_KEY` environment variable
3. Config file at `~/.config/polymarket/config.json`

### Config File Format

```json
{
  "private_key": "0x...",
  "chain_id": 137,
  "signature_type": "proxy"
}
```

The config directory and file are created with restricted permissions (0700/0600 on Unix) to protect the private key.

### Signature Types

- `proxy` (default) — Uses Polymarket's proxy wallet system. This is what most users want.
- `eoa` — Signs directly with the private key. Use if you don't have a proxy wallet.
- `gnosis-safe` — For multisig wallets.

Override per-command: `--signature-type eoa` or via `POLYMARKET_SIGNATURE_TYPE` env var.

### What Needs a Wallet

Most commands work without a wallet — anything that just reads data. You only need a wallet configured for:
- Placing and canceling orders (`clob create-order`, `clob market-order`, `clob cancel-*`)
- Checking your balances and trades (`clob balance`, `clob trades`, `clob orders`)
- On-chain operations (`approve set`, `ctf split/merge/redeem`)
- Reward and API key management (`clob rewards`, `clob create-api-key`)

## Output Formats

Every command supports two output formats, controlled globally:

- `--output table` (default, or `-o table`) — Human-readable formatted tables
- `--output json` (or `-o json`) — Machine-readable JSON, ideal for piping to `jq` or scripting

Errors follow the same pattern: table mode prints `Error: ...` to stderr, JSON mode prints `{"error": "..."}` to stdout. Non-zero exit code either way.

The `-o` flag is global and must appear before the subcommand:
```bash
polymarket -o json markets list --limit 3
```

## Key Concepts

### Markets vs Events
A **market** is a single yes/no question (e.g., "Will BTC hit $100k?"). An **event** groups related markets (e.g., "2024 Election" contains multiple yes/no markets for different candidates). Markets are identified by numeric IDs or URL slugs. Events have numeric IDs.

### Token IDs
Each market outcome has a **token ID** — a large numeric string (not hex). This is used for CLOB operations like checking prices, viewing order books, and placing orders. Token IDs are different from condition IDs (which are 0x-prefixed 32-byte hex).

### Condition IDs
A **condition ID** is a 0x-prefixed 32-byte hex string that uniquely identifies a market's condition on-chain. Used for CTF operations, market-level CLOB queries, and data lookups.

### CLOB (Central Limit Order Book)
Polymarket uses an off-chain order book for matching trades. The CLOB handles prices, order books, order placement, and trade execution. Read operations are unauthenticated; write operations require a configured wallet and CLOB authentication.

### CTF (Conditional Token Framework)
On-chain ERC-1155 tokens representing market outcomes. You can split USDC into YES/NO tokens, merge them back, or redeem winning tokens after resolution. These operations require MATIC for gas on Polygon.

### Neg-Risk
Some markets use a "neg-risk" structure where the exchange and adapter are different contracts. The CLI handles this transparently for most operations.

## Common Workflows

### Browse and Research (No Wallet Needed)

```bash
# Search for markets about a topic
polymarket markets search "bitcoin" --limit 5

# Get details on a specific market (by slug or ID)
polymarket markets get bitcoin-above-100k

# View the order book for a token
polymarket clob book 48331043336612883...

# Check price history
polymarket clob price-history 48331043336612883... --interval 1d

# Browse by category
polymarket events list --tag politics --active true

# Check leaderboards
polymarket data leaderboard --period month --order-by pnl --limit 10
```

### First-Time Setup

```bash
# Option 1: Guided wizard
polymarket setup

# Option 2: Manual steps
polymarket wallet create           # Generate new key
polymarket approve set             # Approve contracts (needs MATIC for gas)
polymarket bridge deposit 0xADDR   # Get deposit addresses
```

### Place and Manage Orders

```bash
# Check balance first
polymarket clob balance --asset-type collateral

# Place a limit order: buy 10 shares at $0.50
polymarket clob create-order --token TOKEN_ID --side buy --price 0.50 --size 10

# Place a market order: buy $5 worth
polymarket clob market-order --token TOKEN_ID --side buy --amount 5

# View open orders
polymarket clob orders

# Cancel a specific order
polymarket clob cancel ORDER_ID

# Cancel everything
polymarket clob cancel-all
```

### Monitor Portfolio

```bash
polymarket data positions 0xYOUR_ADDRESS
polymarket data value 0xYOUR_ADDRESS
polymarket clob orders
polymarket clob trades
```

### Scripting with JSON Output

```bash
# Pipe market data to jq
polymarket -o json markets list --limit 100 | jq '.[].question'

# Check prices programmatically
polymarket -o json clob midpoint TOKEN_ID | jq '.mid'

# Error handling in scripts
if ! result=$(polymarket -o json clob balance --asset-type collateral 2>/dev/null); then
  echo "Failed to fetch balance"
fi
```

### Interactive Shell

```bash
polymarket shell
# polymarket> markets list --limit 3
# polymarket> clob book 48331043336612883...
# polymarket> exit
```

All commands work the same way inside the shell, just without the `polymarket` prefix. Supports command history.

## Order Types

- **GTC** (Good Till Cancelled) — Default. Order stays open until filled or cancelled.
- **FOK** (Fill Or Kill) — Must fill completely immediately, or cancel entirely.
- **GTD** (Good Till Date) — Expires at a specific time.
- **FAK** (Fill And Kill) — Fill whatever is available immediately, cancel the rest.

Use `--order-type GTC` (or FOK, GTD, FAK) when creating orders. Market orders default to FOK.

## Gas and Fees

- **CLOB trading** (limit/market orders): No gas fees, orders are off-chain.
- **Contract approvals** (`approve set`): Requires MATIC for gas on Polygon. Sends 6 transactions.
- **CTF operations** (split/merge/redeem): Requires MATIC for gas.
- **Bridge deposits**: Cross-chain fees depend on the source chain.

## Troubleshooting

**"No wallet configured"** — Run `polymarket wallet create` or `polymarket wallet import <key>`. Or set `POLYMARKET_PRIVATE_KEY` env var.

**"Failed to authenticate with Polymarket CLOB"** — Check that your private key is valid and you have the right signature type configured. Try `--signature-type eoa` if proxy isn't working.

**"Geoblock"** — Check `polymarket clob geoblock` to see if your IP is blocked. Polymarket restricts access from certain jurisdictions.

**Transaction failures on approve/CTF** — Make sure you have MATIC in your wallet for gas on Polygon. The RPC endpoint is `https://polygon.drpc.org`.

**Amounts and precision** — USDC amounts support up to 6 decimal places. Prices are decimals between 0 and 1 (e.g., 0.50 for 50 cents). Sizes are in shares.
