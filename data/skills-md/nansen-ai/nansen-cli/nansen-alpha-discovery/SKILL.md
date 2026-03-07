---
name: nansen-alpha-discovery
description: "What tokens is smart money accumulating before they pump? Token screener with SM filter cross-referenced against netflow."
---

# Alpha Discovery

**Answers:** "What tokens is smart money accumulating before they pump?"

```bash
CHAIN=solana

nansen research token screener --chain $CHAIN --timeframe 24h --smart-money --limit 20
# → token_symbol, price_usd, price_change, volume, buy_volume, market_cap_usd, fdv, liquidity, token_age_days

nansen research smart-money netflow --chain $CHAIN --labels "Smart Trader" --limit 10
# → token_symbol, net_flow_1h/24h/7d/30d_usd, trader_count

# Confirm SM flow on a specific token from screener results
TOKEN=<address_from_screener>
nansen research token flow-intelligence --token $TOKEN --chain $CHAIN
# → net_flow_usd per label: smart_trader, whale, exchange, fresh_wallets
```

Cross-reference screener results with positive netflow to find early accumulation.
