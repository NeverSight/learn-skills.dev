---
name: nansen-perp-scan
description: "What is the state of the Hyperliquid perp market? Top contracts by volume/OI, trader leaderboard, and SM perp activity."
---

# Perp Market Scan

**Answers:** "What's the state of the Hyperliquid perp market right now?"

```bash
nansen research perp screener --sort volume:desc --limit 20
# → token_symbol, volume, buy/sell_volume, buy_sell_pressure, open_interest, funding, mark_price

nansen research perp leaderboard --days 7 --limit 20
# → trader_address, trader_address_label, total_pnl, roi, account_value

nansen research smart-money perp-trades --limit 20
# → token_symbol, side, action (Open/Close), value_usd, price_usd, trader_address_label
```
