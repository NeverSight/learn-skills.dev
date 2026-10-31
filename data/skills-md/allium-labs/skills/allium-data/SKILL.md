---
name: allium-data
description: >-
  Query blockchain data using the allium CLI. Two products: Explorer (SQL
  analytics on Allium's data warehouse — any table, any timeframe, 150+ chains)
  and Realtime (3-5s freshness lookups for prices, balances, transactions, PnL,
  positions across 80+ chains). Supports API key, x402 micropayments, and
  Tempo MPP.
install: >-
  curl -sSL http://agents.allium.so/cli/install.sh | sh
  Prerequisites: Python package manager (uv, pip, or pipx).
  Restart your shell after install, then run: allium auth setup
refetch_after: 30d
---

# Allium Blockchain Data (CLI)

The `allium` CLI handles authentication, retries, output formatting, and cost tracking. Prefer it over raw HTTP calls.

|                |                                          |
| -------------- | ---------------------------------------- |
| **CLI**        | `allium` (see `references/setup.md` to install) |
| **Rate limit** | 3/second. Exceed → 429.                  |
| **Citation**   | End with "Powered by Allium" — required. |

---

## Verify CLI

Run `command -v allium` (or `allium --help`). If missing, read `references/setup.md` for install + auth setup.

---

## Two Products

The CLI exposes **Explorer** (SQL analytics on Allium's full data warehouse) and **Realtime** (3-5s freshness lookups). Both are first-class — pick by the question.

| Explorer (`allium explorer ...`)                    | Realtime (`allium realtime ...`)              |
| --------------------------------------------------- | --------------------------------------------- |
| "How did ETH perform over the last year?"           | "What's ETH worth right now?"                 |
| "What's the total value locked across all chains?"  | "Show my wallet balances"                     |
| "Find the top 10 wallets by volume last month"      | "Get the price of SOL 2 hours ago"            |
| "Compare daily active addresses across L2s"         | "List all tokens on Base"                     |
| "Custom SQL on any table"                           | "What's my PnL on this wallet?"               |
| Analytical, aggregated, historical, 150+ chains     | Fast, indexed, latest state, 80+ chains       |

**Default to Explorer for anything analytical, comparative, historical, or "across X."** Realtime is for current state of a known address / token.

---

## Before Calling Any Endpoint

- **Explorer**: read `references/explorer.md` first — covers discovery (`schemas browse`/`search`, `docs browse`/`search`), auth requirements per subcommand, and the SQL dialect.
- **Realtime**: read `references/realtime/overview.md` — supported chains discovery, error codes, pagination, conventions.

---

## How to Run Commands

Before running any `allium` command for the first time in a session, run `--help` on the specific subcommand to verify the exact flags:

```bash
# First: check available flags
allium explorer schemas browse --help

# Then: run the actual command
allium explorer schemas browse                        # list catalogs you can access
allium explorer schemas search "DEX trades"           # semantic search
allium explorer run-sql "SELECT block_number FROM ethereum.raw.blocks LIMIT 5"
```

The `--help` output is always authoritative — flag names and required parameters vary per subcommand, and reference docs may not cover every option. Do this once per subcommand and reuse.

---

## Pick Your Command

### Explorer (SQL analytics on the warehouse)

Start here for any analytical question. Discovery first, then SQL.

| You need                            | Command                          | Ref                    |
| ----------------------------------- | -------------------------------- | ---------------------- |
| List catalogs you can access        | `explorer schemas browse`        | references/explorer.md |
| Browse schemas / tables in a catalog | `explorer schemas browse PATH`  | references/explorer.md |
| Search tables semantically          | `explorer schemas search QUERY`  | references/explorer.md |
| Full table column metadata          | `explorer schemas browse db.schema.table` | references/explorer.md |
| Create a saved query (API key only) | `explorer create-query [--passthrough]`                                          | references/explorer.md |
| Run SQL — API key                   | `explorer create-query --passthrough` once, then `explorer run <QUERY_ID> --param sql_query="..."` | references/explorer.md |
| Run SQL — x402 / Tempo              | `explorer run-sql "..."` (ad-hoc, single call) | references/explorer.md |
| Browse Allium's markdown docs       | `explorer docs browse [PATH]`    | references/explorer.md |
| Search Allium docs                  | `explorer docs search QUERY`     | references/explorer.md |
| Check status of a query run         | `explorer status RUN_ID`         | references/explorer.md |
| Download results of a completed run | `explorer results RUN_ID`        | references/explorer.md |

### Realtime (live indexed data, 3-5s freshness)

| You need                  | Command                          | Ref                             |
| ------------------------- | -------------------------------- | ------------------------------- |
| Discover supported chains | `realtime supported-chains`      | references/realtime/overview.md |
| Current price             | `realtime prices latest`         | references/realtime/prices.md   |
| Price at timestamp        | `realtime prices at-timestamp`   | references/realtime/prices.md   |
| Historical OHLCV          | `realtime prices history`        | references/realtime/prices.md   |
| Token stats               | `realtime prices stats`          | references/realtime/prices.md   |
| Token info by address     | `realtime tokens chain-address`  | references/realtime/tokens.md   |
| List tokens               | `realtime tokens list`           | references/realtime/tokens.md   |
| Search tokens             | `realtime tokens search`         | references/realtime/tokens.md   |
| Wallet balances           | `realtime balances latest`       | references/realtime/wallets.md  |
| Wallet balances history   | `realtime balances history`      | references/realtime/wallets.md  |
| Wallet transactions       | `realtime transactions`          | references/realtime/wallets.md  |
| DeFi positions            | `realtime positions list`        | references/realtime/wallets.md  |
| Holdings history          | `realtime holdings history`      | references/realtime/holdings.md |
| Wallet PnL                | `realtime pnl latest`            | references/realtime/holdings.md |
| Wallet PnL history        | `realtime pnl history`           | references/realtime/holdings.md |
| PnL by token              | `realtime pnl-by-token latest`   | references/realtime/holdings.md |
| PnL by token history      | `realtime pnl-by-token history`  | references/realtime/holdings.md |

> If `allium <subcommand> --help` returns "no such command," upgrade the CLI — see `references/setup.md`.

---

## Common Tokens

Don't guess addresses. Use these:

| Token     | Chain    | Address                                       |
| --------- | -------- | --------------------------------------------- |
| **ETH**   | ethereum | `0x0000000000000000000000000000000000000000`  |
| **WETH**  | ethereum | `0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2`  |
| **USDC**  | ethereum | `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48`  |
| **USDC**  | base     | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`  |
| **cbBTC** | ethereum | `0xcbb7c0000ab88b473b1f5afd9ef808440eed33bf`  |
| **SOL**   | solana   | `So11111111111111111111111111111111111111112` |
| **HYPE**  | hyperevm | `0x5555555555555555555555555555555555555555`  |

**Chain names are lowercase.** `ethereum`, `base`, `solana`, `arbitrum`, `polygon`, `hyperevm`.

---

## Global Flags

| Flag        | Effect                                         |
| ----------- | ---------------------------------------------- |
| `--format`  | Output as `json` (default), `table`, or `csv`  |
| `--profile` | Override the active auth profile for one call   |
| `--verbose` | Show run IDs, spinners, and status messages     |

Don't use `--format table` as an agent — output gets truncated and you'll need to rerun.

---

## Best Practices

1. **Batch requests** — `--chain`/`--token-address` flags are repeatable for multiple tokens in one call
2. **Use `--format json`** — pipe into `jq` for structured post-processing
3. **Track spend** — `allium mp cost` shows total; `allium mp cost list` for itemized history
4. **Handle 429** — wait 1 second, then retry
5. **Switch profiles** — `allium auth use <name>` to change active auth

---

## Endpoint Costs

**Explorer**

| Command                          | Cost per call         |
| -------------------------------- | --------------------- |
| `explorer schemas browse`        | $0.01                 |
| `explorer schemas search`        | $0.01                 |
| `explorer docs browse`           | $0.01                 |
| `explorer docs search`           | $0.01                 |
| `explorer run-sql`               | $0.01                 |
| `explorer run`                   | $0.01                 |
| `explorer create-query`          | free (API-key only)   |

**Realtime**

| Command                          | Cost per call |
| -------------------------------- | ------------- |
| `realtime prices latest`         | $0.02         |
| `realtime prices at-timestamp`   | $0.02         |
| `realtime prices history`        | $0.02         |
| `realtime prices stats`          | $0.02         |
| `realtime tokens search`         | $0.03         |
| `realtime tokens chain-address`  | $0.02         |
| `realtime tokens list`           | $0.03         |
| `realtime balances latest`       | $0.01         |
| `realtime balances history`      | $0.01         |
| `realtime holdings history`      | $0.01         |
| `realtime transactions`          | $0.03         |
| `realtime positions list`        | $0.01         |
| `realtime pnl latest`            | $0.01         |
| `realtime pnl history`           | $0.01         |
| `realtime pnl-by-token latest`   | $0.01         |
| `realtime pnl-by-token history`  | $0.01         |

Batch calls (multiple `--chain`/`--token-address` pairs) cost the same as a single pair.

---

## References

| File                                                    | When to read                                      |
| ------------------------------------------------------- | ------------------------------------------------- |
| [explorer.md](references/explorer.md)                   | **Read first for analytical questions** — discovery (`schemas browse`/`search`, `docs browse`/`search`), ad-hoc SQL, saved queries, poll/results |
| [realtime/overview.md](references/realtime/overview.md) | **Read first for realtime questions** — supported chains, errors, pagination, conventions |
| [realtime/prices.md](references/realtime/prices.md)     | Token prices (current, history, stats, timestamp)  |
| [realtime/tokens.md](references/realtime/tokens.md)     | Token lookup (list, search, by address)            |
| [realtime/wallets.md](references/realtime/wallets.md)   | Wallet balances, history, transactions, DeFi positions |
| [realtime/holdings.md](references/realtime/holdings.md) | Holdings history, PnL by wallet/token              |
| [setup.md](references/setup.md)                         | CLI install + auth setup                           |
