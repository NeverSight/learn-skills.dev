---
name: nansen-perp-trader
description: "Deep dive on a Hyperliquid perp trader. Identity, open positions, recent trades, and overall PnL."
---

# Perp Trader

**Answers:** "What is this perp trader doing? What are their positions and track record?"

```bash
ADDR=<address>

nansen research profiler labels --address $ADDR --chain ethereum
# → label, category (identity, SM labels)

nansen research profiler perp-positions --address $ADDR
# → asset_positions, margin_summary_account_value_usd, margin_summary_total_margin_used_usd

nansen research profiler perp-trades --address $ADDR --days 7 --limit 20
# → timestamp, token_symbol, side, action (Open/Close/Reduce), price, size, value_usd, closed_pnl, fee_usd

nansen research perp leaderboard --days 7 --limit 50
# → trader_address, total_pnl, roi, account_value (check if ADDR appears)
```

Cross-reference perp-trades with perp-positions to see if the trader is scaling in/out. Leaderboard shows relative standing.
