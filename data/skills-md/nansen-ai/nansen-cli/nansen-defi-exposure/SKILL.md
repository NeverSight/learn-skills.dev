---
name: nansen-defi-exposure
description: "What DeFi positions does a wallet hold? Protocol-by-protocol breakdown of assets, debts, and rewards across chains."
---

# DeFi Exposure

**Answers:** "What DeFi positions does this wallet have across protocols?"

```bash
ADDR=<address>

nansen research portfolio defi --wallet $ADDR
# → protocol_name, chain, total_value_usd, total_assets_usd, total_debts_usd, total_rewards_usd, tokens

nansen research profiler balance --address $ADDR --chain ethereum
# → token_symbol, token_name, token_amount, value_usd per holding

nansen research profiler balance --address $ADDR --chain base
```

Combine DeFi positions (lending, LPs, staking) with spot balances for a complete picture of on-chain exposure.

Note: portfolio defi may return empty for wallets with no tracked DeFi positions.
