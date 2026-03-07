---
name: nansen-fund-watch
description: "What are crypto funds and VCs holding right now? Cross-chain fund portfolios and net accumulation signals."
---

# Fund Watch

**Answers:** "What are crypto funds and VCs holding right now?"

```bash
nansen research smart-money holdings --chain ethereum --labels "Fund" --limit 20
# → token_symbol, value_usd, holders_count, balance_24h_percent_change, share_of_holdings_percent

nansen research smart-money holdings --chain solana --labels "Fund" --limit 20

nansen research smart-money netflow --chain ethereum --labels "Fund" --limit 10
# → token_symbol, net_flow_1h/24h/7d/30d_usd, market_cap_usd, trader_count

nansen research smart-money netflow --chain solana --labels "Fund" --limit 10
```

Cross-reference holdings with netflow to see directional conviction. Positive net_flow_24h = active accumulation.
