---
name: nansen-portfolio-history
description: "How has a wallet's portfolio changed over time? Historical balances, current snapshot, and per-token PnL."
---

# Portfolio History

**Answers:** "How has this wallet's portfolio evolved over the past month?"

```bash
ADDR=<address> CHAIN=ethereum

nansen research profiler historical-balances --address $ADDR --chain $CHAIN --days 30 --limit 20
# → block_timestamp, token_symbol, token_amount, value_usd, chain

nansen research profiler balance --address $ADDR --chain $CHAIN
# → token_symbol, token_name, token_amount, price_usd, value_usd

nansen research profiler pnl --address $ADDR --chain $CHAIN --days 30 --limit 20
# → token_symbol, pnl_usd_realised, roi_percent_realised, bought_usd, sold_usd, holding_usd, nof_buys, nof_sells
```

Compare historical-balances over time against current balance to see what was added/removed. PnL shows trade performance.
