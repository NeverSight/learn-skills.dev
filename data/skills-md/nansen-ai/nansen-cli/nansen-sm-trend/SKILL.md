---
name: nansen-sm-trend
description: "Has SM been in this token for weeks, or did they just enter? Are they still buying?"
---
```bash
TOKEN=<address> CHAIN=ethereum
nansen research smart-money netflow --chain $CHAIN --limit 200
# → filter by token_address; net_flow_1h_usd, net_flow_24h_usd, net_flow_7d_usd, net_flow_30d_usd
nansen research token holders --token $TOKEN --chain $CHAIN --smart-money --limit 20
# → address_label, value_usd, balance_change_24h, balance_change_7d, balance_change_30d
nansen research token flow-intelligence --token $TOKEN --chain $CHAIN
# → smart_trader_net_flow_usd, whale_net_flow_usd, fund_net_flow_usd, fresh_wallets_net_flow_usd
nansen research token dex-trades --token $TOKEN --chain $CHAIN --limit 50
# → block_timestamp, action, trader_address_label — find oldest SM-labeled BUY
```
1h/24h+ & 7d/30d+ = sustained accumulation. 24h+ & 7d− = fresh entry.
24h− & 7d+ = reducing. All negative = distribution.
