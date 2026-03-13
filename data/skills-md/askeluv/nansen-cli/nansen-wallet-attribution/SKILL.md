---
name: nansen-wallet-attribution
description: "Cluster and attribute related wallets — funding chains, shared signers, CEX deposit patterns. Use when tracing wallet ownership, comparing two wallets, finding wallet relationships, governance voters, or related address clusters."
---

# Wallet Attribution

**Answers:** "Who controls this wallet? Are these wallets related?"

Chain: `0x` → `--chain ethereum` (also base, arbitrum, optimism, polygon). Base58 → `--chain solana`.

```bash
ADDR=<address> CHAIN=<ethereum|solana|base|...>  # detect from address format above
# 1. Identity
nansen research profiler labels --address $ADDR --chain $CHAIN
# 2. Related wallets (paginate with --page N)
nansen research profiler related-wallets --address $ADDR --chain $CHAIN
# 3. Counterparties (paginate with --page N; widen with --days 365 if empty)
nansen research profiler counterparties --address $ADDR --chain $CHAIN --days 90
# 4. Batch profile cluster
nansen research profiler batch --addresses "addr1,addr2" --chain $CHAIN --include labels,balance,pnl
# 5. Compare pairs → shared_counterparties, shared_tokens, balances
nansen research profiler compare --addresses "addr1,addr2" --chain $CHAIN
# 6. Historical balances (fingerprint drained wallets)
nansen research profiler historical-balances --address $ADDR --chain $CHAIN --days 90
# 7. Multi-hop trace (credit-heavy — keep --width ≤3)
nansen research profiler trace --address $ADDR --chain $CHAIN --depth 2 --width 3
```

**Expansion:** Run steps 1-2 on seed. For each new address found, ask the human before querying. Reserve step 3 for seed only.
**Stop when:** known protocol/CEX · Low confidence · already visited · cluster > 10 wallets.
**Confidence:** High = first funder / shared Safe signers / same CEX deposit. Medium = coordinated movements / related-wallets + label match. Exclude = ENS only, single CEX withdrawal, single deployer.
Full attribution rules in REFERENCE.md.
