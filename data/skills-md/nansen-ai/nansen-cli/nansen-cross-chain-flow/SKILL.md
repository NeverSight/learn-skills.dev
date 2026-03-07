---
name: nansen-cross-chain-flow
description: "Is SM buying this token on one chain but selling on another? Detect capital rotation."
---
```bash
TOKEN_SYMBOL=<symbol e.g. "AAVE"> CHAINS=(ethereum solana base bnb)
for chain in "${CHAINS[@]}"; do
  nansen research smart-money netflow --chain $chain --limit 200
  # Filter by token_symbol; → net_flow_1h_usd, net_flow_24h_usd, net_flow_7d_usd, net_flow_30d_usd
done
```
Absent from results = SM activity below threshold on that chain, not necessarily unsupported. Use --limit 200; --limit 100 silently drops mid-tier tokens.
ETH+ & SOL− = rotating from SOL→ETH. One chain positive only = chain-specific play.
24h/7d divergence across chains is the rotation signal, not 1h.
