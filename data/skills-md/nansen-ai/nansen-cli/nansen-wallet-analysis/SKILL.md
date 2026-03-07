---
name: nansen-wallet-analysis
description: "Who is this wallet and what have they been doing? Identity labels, balance, PnL summary, recent transactions, perp positions, and counterparties."
---

# Wallet Analysis

**Answers:** "Who is this wallet and what have they been doing?"

```bash
ADDR=<address> CHAIN=ethereum

nansen research profiler labels --address $ADDR --chain $CHAIN
# → label, category (e.g. "Smart Trader", "Fund", "Public Figure", ENS names)

nansen research profiler balance --address $ADDR --chain $CHAIN
# → token_symbol, token_name, token_amount, price_usd, value_usd per holding

nansen research profiler pnl-summary --address $ADDR --chain $CHAIN --days 30
# → realized_pnl_usd, realized_pnl_percent, win_rate, traded_token_count, traded_times, top5_tokens

nansen research profiler transactions --address $ADDR --chain $CHAIN --limit 20
# → block_timestamp, method, tokens_sent, tokens_received, volume_usd, source_type

nansen research profiler perp-positions --address $ADDR
# → asset_positions, margin_summary_account_value_usd, margin_summary_total_margin_used_usd

nansen research profiler counterparties --address $ADDR --chain $CHAIN --days 30
# → counterparty_address, counterparty_address_label, interaction_count, total_volume_usd, volume_in/out_usd
```

perp-positions returns Hyperliquid data — returns empty if the wallet has no open perps.
