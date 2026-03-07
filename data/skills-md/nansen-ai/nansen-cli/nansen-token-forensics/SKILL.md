---
name: nansen-token-forensics
description: "Where is this token moving and why? Large transfers, flow trends over time, and breakdown by wallet label."
---

# Token Forensics

**Answers:** "Where is this token moving? Who is sending it and where?"

```bash
TOKEN=<address> CHAIN=ethereum
# Examples: UNI on ethereum (0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984)
#           BONK on solana (DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263)
# Note: token flows does NOT support stablecoins (USDC, USDT, etc.) — use non-stablecoin tokens

nansen research token transfers --token $TOKEN --chain $CHAIN --days 7 --limit 20
# → from_address_label, to_address_label, transfer_amount, transfer_value_usd

nansen research token flows --token $TOKEN --chain $CHAIN --days 7 --limit 20
# → date, price_usd, holders_count, total_inflows_count, total_outflows_count
# ⚠ Returns HTTP 422 for stablecoins — skip this command if TOKEN is a stablecoin

nansen research token flow-intelligence --token $TOKEN --chain $CHAIN
# → net_flow_usd per label: smart_trader, whale, exchange, fresh_wallets, public_figure
```

Rising exchange_net_flow + large transfers to exchange addresses = potential sell pressure. Fresh wallet inflows may signal new interest or wash trading.
