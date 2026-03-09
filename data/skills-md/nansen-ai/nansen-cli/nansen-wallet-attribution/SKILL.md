---
name: nansen-wallet-attribution
description: "Cluster and attribute related wallets — funding chains, shared signers, CEX deposit patterns. Use when tracing wallet ownership, comparing two wallets, finding wallet relationships, governance voters, or related address clusters."
---

# Wallet Clustering & Attribution

**Answers:** "Who controls this wallet? Are these wallets related?"

**Chain detection:** Inspect the address format before running any command.
- Starts with `0x` → `--chain ethereum` (also works for base, arbitrum, optimism, polygon)
- Base58 (32–44 chars, no `0x`) → `--chain solana`

Run steps 1-2 on the seed address. For every new address found, ask the human: **"Found `<addr>` via `<signal>` (`<label>`). Want me to query it?"** On confirm, re-run steps 1-2 on it. Reserve step 3 for the seed address only. Keep expanding until no new addresses or confidence is Low.

```bash
ADDR=<address>
# Detect chain from address format above
CHAIN=<detected>  # ethereum | solana | base | ...

# 1. Labels
nansen research profiler labels --address $ADDR --chain $CHAIN
# → label, category (e.g. "Smart Trader", "Fund", ENS names)

# 2. Related wallets (First Funder, Signer, Deployed via)
# Repeat with --page N+1 until is_last_page: true
nansen research profiler related-wallets --address $ADDR --chain $CHAIN
# → address, address_label, relation, block_timestamp, chain

# 3. Counterparties — start with 90d
# Repeat with --page N+1 until is_last_page: true
nansen research profiler counterparties --address $ADDR --chain $CHAIN --days 90
# → counterparty_address, counterparty_address_label, interaction_count, total_volume_usd
# If empty, retry with --days 365
# EVM only — also check L2s (4 extra API calls per address):
# nansen research profiler counterparties --address $ADDR --chain base --days 365
# nansen research profiler counterparties --address $ADDR --chain arbitrum --days 365
# nansen research profiler counterparties --address $ADDR --chain optimism --days 365
# nansen research profiler counterparties --address $ADDR --chain polygon --days 365

# 4. Batch profile the cluster
# Use addresses collected from steps 1-3
nansen research profiler batch --addresses "<addr1>,<addr2>,..." --chain $CHAIN --include labels,balance,pnl
# → per-address: labels, balance, pnl_summary

# 5. Compare pairs
nansen research profiler compare --addresses "<addr1>,<addr2>" --chain $CHAIN
# → shared_counterparties, shared_tokens, overlap_score

# 6. Coordinated balance movements
# Repeat with --page N+1 until is_last_page: true
nansen research profiler historical-balances --address $ADDR --chain $CHAIN --days 90
# → token_symbol, balance snapshots over time

# 7. Multi-hop trace — only if steps 2-3 are inconclusive
nansen research profiler trace --address $ADDR --chain $CHAIN --depth 2 --width 3
# → root, nodes (address list), edges (from→to with volume), stats (nodes_visited, edges_found)
```

**Stop expanding when:** address is a known protocol/CEX · confidence is Low · already visited · cluster > 10 wallets.

## Attribution Rules

- CEX withdrawal → wallet owner (NOT the CEX)
- Smart account/DCA bot → end-user who funds it (NOT the protocol)
- Safe deployer ≠ owner — identical signer sets across Safes = same controller

| Confidence | Signals |
|------------|---------|
| **High** | First Funder / shared Safe signers / same CEX deposit address |
| **Medium** | Coordinated balance movements / related-wallets + label match |
| **Exclude** | ENS alone, single CEX withdrawal, single deployer |

**Output:** `address` · `owner` · `confidence (H/M/L)` · `signals` · `role`
Warning: `trace` is credit-heavy; keep `--width 3` or lower. L2 counterparty loop adds 4 API calls per address. Historical balances reveal past holdings on drained wallets — useful fingerprint.
