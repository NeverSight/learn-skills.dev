---
name: nansen-polymarket-trader
description: "What is a Polymarket trader betting on? Trades by address, PnL breakdown, and market context. Use when analysing a specific Polymarket wallet."
---

# Polymarket Wallet Activity

**Answers:** "What is this Polymarket trader betting on? Are they profitable?"

**Finding an active trader address:** Source from `trades-by-market` (guarantees trade history) rather than `top-holders` (position holders may have no recorded trades):

```bash
# Step 1: find active traders from a market
nansen research pm trades-by-market --market-id <market_id> --limit 5
# → seller/buyer addresses with confirmed trade history — use one as ADDR below
```

```bash
ADDR=<polymarket_address>

nansen research pm trades-by-address --address $ADDR --limit 20
# → timestamp, market_question, event_title, taker_action, side, size, price, usdc_value

nansen research pm pnl-by-address --address $ADDR --limit 20
# → question, event_title, side_held, net_buy_cost_usd, unrealized_value_usd, total_pnl_usd, market_resolved
```

Note: addresses sourced from `top-holders` may return empty trade history — use `trades-by-market` to find addresses with confirmed activity.

Look at PnL across resolved vs unresolved markets to gauge trader skill. Large positions in trending categories signal conviction.
