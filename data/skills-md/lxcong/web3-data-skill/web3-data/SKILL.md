---
name: web3-data
description: >
  Explore Web3 on-chain data using Chainbase APIs. Use this skill when the user asks about
  blockchain data, token holders, wallet addresses, token prices, ENS domains, transactions,
  DeFi portfolios, or any on-chain analytics. Triggers include: "top holders of", "who holds",
  "wallet address", "token price", "token transfers",
  "ENS domain", "on-chain data", "blockchain query", "SQL query on-chain", or any request
  to look up, analyze, or explore Web3/blockchain data across Ethereum, BSC, Polygon, Arbitrum,
  Optimism, Base, Avalanche, zkSync, and other EVM chains.
---

# Web3 Data Explorer (Chainbase)

Query on-chain data via the [Chainbase CLI](https://github.com/chainbase-labs/cli).

## Quick Reference

**Install**: `npm install -g chainbase-cli` (or use `npx chainbase-cli`)

**Auth**: Set API key via `chainbase config set api-key YOUR_KEY`, or env `CHAINBASE_API_KEY`. Falls back to `demo` key. If rate-limited, direct user to https://platform.chainbase.com to get a key.

**x402 Payment**: Supports pay-per-call micropayments via `--x402` flag. Setup: `chainbase config set private-key 0x...`

```bash
# Top token holders
chainbase token top-holders 0xdAC17F958D2ee523a2206206994597C13D831ec7 --chain 1 --limit 10

# Token price
chainbase token price 0xdAC17F958D2ee523a2206206994597C13D831ec7

# ENS resolve
chainbase domain ens-resolve vitalik.eth

# SQL query
chainbase sql execute "SELECT * FROM ethereum.blocks ORDER BY number DESC LIMIT 5"
```

Use `--json` for machine-parseable output. Use `--chain <id>` to target a specific chain.

## Chain IDs

| Chain | ID | Chain | ID |
|---|---|---|---|
| Ethereum | 1 | Optimism | 10 |
| BSC | 56 | Base | 8453 |
| Polygon | 137 | zkSync | 324 |
| Avalanche | 43114 | Arbitrum | 42161 |

Default to Ethereum (chain 1) unless user specifies otherwise.

## Routing Logic

Match user intent to the right CLI command:

| User wants | CLI command |
|---|---|
| Latest block number | `chainbase block latest` |
| Block details | `chainbase block detail <number>` |
| Transaction detail | `chainbase tx detail <hash>` |
| Wallet transaction history | `chainbase tx list <address>` |
| Token info (name, symbol, supply) | `chainbase token metadata <contract>` |
| Token price | `chainbase token price <contract>` |
| Historical token price | `chainbase token price-history <contract> --from <ts> --to <ts>` |
| List of holder addresses | `chainbase token holders <contract>` |
| Top token holders / who holds a token | `chainbase token top-holders <contract>` |
| Token transfer history | `chainbase token transfers --contract <addr>` |
| Native token balance (ETH/BNB) | `chainbase balance native <address>` |
| ERC20 token balances of wallet | `chainbase balance tokens <address>` |
| DeFi portfolio positions | `chainbase balance portfolios <address>` |
| ENS domains held by address | `chainbase domain ens <address>` |
| ENS name → address | `chainbase domain ens-resolve <name>` |
| Address → ENS name | `chainbase domain ens-reverse <address>` |
| Space ID resolve (BSC) | `chainbase domain spaceid-resolve <domain>` |
| Space ID reverse (BSC) | `chainbase domain spaceid-reverse <address>` |
| Call smart contract function | `chainbase contract call --address <contract> --function "fn" --abi '[...]' --params '[...]'` |
| **Anything not covered above** | **SQL API**: `chainbase sql execute "SELECT ..."` |

## Workflow

1. **Identify intent** — Determine what data the user needs
2. **Resolve identifiers** — If user gives token name (e.g. "USDT"), look up the contract address. Common tokens:
   - USDT: `0xdAC17F958D2ee523a2206206994597C13D831ec7` (ETH)
   - USDC: `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48` (ETH)
   - WETH: `0xC02aaA39b223FE8D0A0e5c4F27eAD9083C756Cc2` (ETH)
   - DAI: `0x6B175474E89094C44Da98b954EedeAC495271d0F` (ETH)
   - WBTC: `0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599` (ETH)
   - If unknown, use `chainbase token metadata <contract>` or ask the user for the contract address
3. **Select command** — Use the routing table above; fall back to SQL API for complex/custom queries
4. **Execute** — Run the CLI command. Add `--json` when you need to parse the output programmatically
5. **Present results** — Format data clearly with tables for lists, highlight key insights

## Global Options

All commands support these options:

| Option | Description | Default |
|---|---|---|
| `--chain <id>` | Target chain | `1` (Ethereum) |
| `--json` | Machine-parseable JSON output | `false` |
| `--page <n>` | Page number for paginated results | `1` |
| `--limit <n>` | Results per page | `20` |
| `--x402` | Enable x402 micropayment mode | `false` |

## SQL API Fallback

When CLI commands don't cover the query, translate user intent to SQL:

```bash
chainbase sql execute "SELECT from_address, SUM(value) as total FROM ethereum.token_transfers WHERE contract_address = '0x...' GROUP BY from_address ORDER BY total DESC LIMIT 20"
```

Common table patterns (replace `ethereum` with chain name):
- `{chain}.blocks` — Block data
- `{chain}.transactions` — Transactions
- `{chain}.token_transfers` — ERC20 transfers
- `{chain}.token_metas` — Token metadata
- `{chain}.logs` — Event logs

SQL constraints: max 100,000 results per query.

For full command help, run `chainbase --help` or `chainbase <command> --help`.
