---
name: chain-analyst
description: "Analyze onchain activity across EVM networks using HyperSync for historical data, RPC for current state, Etherscan for ABI lookup, and CoinGecko for pricing. Use when users ask to decode transactions, trace token flow, query contract state, compute balances from logs, identify event emitters, or produce reproducible protocol-level analysis with commands and evidence."
license: MIT
compatibility: "Requires bash, curl, jq, bc. Optional: cast (Foundry), node with viem. Needs internet access for HyperSync, Etherscan, and CoinGecko APIs."
metadata:
  author: lutr0
  version: "1.0.0"
---

# Chain Analyst

Use this skill to produce reproducible blockchain analysis from raw chain data.

## Run Core Workflows

Resolve the skill path first:

```bash
for d in .agents .deepagents .claude .cursor .codex .opencode; do
  [ -f "$d/skills/chain-analyst/SKILL.md" ] && SKILL="$d/skills/chain-analyst" && break
done
```

Run the minimum-viable tool for each task:

```bash
# Analyze one tx end-to-end (tx/logs/traces + ABI fetch attempts)
bash "$SKILL/scripts/analyze-tx.sh" <tx_hash> [network]

# Query historical data with HyperSync
# output mode: stream (default) or aggregate
bash "$SKILL/scripts/hypersync-query.sh" <network> <query.json> [max_pages] [stream|aggregate]

# Query current contract state via RPC
bash "$SKILL/scripts/query-contract.sh" <method> <contract> [args...] [network]

# Fetch verified ABI
bash "$SKILL/scripts/get-contract-abi.sh" <address> [network]

# Fetch current or historical token price
bash "$SKILL/scripts/get-token-price.sh" <coin_id> [currency] [dd-mm-yyyy]

# Batch contract reads
bash "$SKILL/scripts/multicall.sh" <network> <calls.json>
```

## Configure Environment

Set required keys in a `.env` or `.env.local` file:

- `HYPERSYNC_API_TOKEN` (required)
- `ETHERSCAN_API_KEY` (required)
- `COINGECKO_API_KEY` (optional)

Scripts search these locations in order (last found value wins):

1. Workspace `.env` / `.env.local`
2. Skill folder `.env` / `.env.local`

Use only `KEY=VALUE` lines in env files. Scripts treat env files as data and do not execute shell expressions.

## Select Query Strategy

Use this decision order:

1. Use `analyze-tx.sh` for a single transaction investigation.
2. Use `hypersync-query.sh` for historical searches over logs/traces/transactions.
3. Use `query-contract.sh` for latest state reads.
4. Use `multicall.sh` when reading many contracts/methods in one run.

## Common HyperSync Patterns

HyperSync can query across millions of blocks in one request. Build queries using three top-level filters — `transactions`, `logs`, and `traces` — each narrowed by fields like address, topic, from/to.

**Transaction queries:**

- **All transactions for an address**: filter `transactions.from` or `transactions.to` (or both as separate entries for union)
- **Transactions to a specific contract**: filter `transactions.to` = contract address

**Log queries** (ERC20 `Transfer(address,address,uint256)` emits topic0 = signature hash, topic1 = from, topic2 = to — pad addresses to 32 bytes):

- **ERC20 transfers to an address**: filter `topics[0]` = Transfer hash, `topics[2]` = padded recipient
- **ERC20 transfers from an address**: filter `topics[0]` = Transfer hash, `topics[1]` = padded sender
- **USDC/specific token transfers**: add `logs.address` = token contract to any Transfer filter
- **Swap history on a pool**: filter `topics[0]` = Swap event hash, `logs.address` = pool
- **NFT mints**: filter `topics[0]` = Transfer hash, `topics[1]` = zero address
- **All events on a contract**: filter `logs.address` = contract (no topic filter)

**Trace queries:**

- **Internal call traces to a contract**: filter `traces.to` = contract, `traces.call_type` = `["call", "delegatecall"]`
- **Contract creation traces**: filter `traces.kind` = `["create"]`

See `references/hypersync-api.md` for full query structure, field names, and ready-made recipes.

## Use Network Names

Built-in networks (with aliases): `ethereum` (`eth`, `mainnet`), `base`, `arbitrum`, `optimism` (`op`), `polygon` (`matic`).

For any other EVM chain, pass its canonical lowercase name directly (e.g. `scroll`, `zksync`, `bsc`, `linea`, `avalanche`). The scripts resolve URLs using these patterns:

- HyperSync: `https://{name}.hypersync.xyz`
- RPC: `https://{name}.drpc.org`

For ABI lookup via `get-contract-abi.sh`, chains outside the top 5 require a numeric chain ID instead of a name. Look up the chain ID at https://chainlist.org if needed.

## Produce Final Analysis Output

For every final answer, include:

1. Exact commands run.
2. Contract and wallet addresses involved.
3. Quantities with units and decimals applied.
4. Event/topic evidence supporting each claim.
5. Any assumptions or unresolved ambiguity.

Use `assets/analysis-report-template.md` when you need a structured report.

## Load References Only When Needed

Read references selectively:

- Read `references/hypersync-api.md` when building or debugging HyperSync queries.
- Read `references/etherscan-api.md` when ABI lookup fails or chain ID mapping is unclear.
- Read `references/coingecko-api.md` when coin IDs/currencies or historical endpoints are uncertain.

## Handle Common Failure Modes

- If a tx query returns no rows, verify tx hash length and network.
- If ABI fetch fails, check verification status and chain mapping.
- If price lookup fails, resolve the canonical CoinGecko coin id first.
- If RPC reads fail, retry on canonical network token and verify method signature.

## Validate Before Returning

Before returning conclusions:

1. Re-run at least one key command that supports the core claim.
2. Ensure numeric conversions are consistent with token decimals.
3. Ensure addresses in explanation match command output exactly.
