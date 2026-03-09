---
name: nansen-token-discovery
description: "Discover trending tokens — screener, SM holdings, Nansen indicators, and flow intelligence for promising finds. Use when scanning for new tokens or screening what's hot."
---

# Token Discovery

**Answers:** "What tokens are trending and worth a deeper look?"

```bash
CHAIN=solana

# Screen top tokens by volume
nansen research token screener --chain $CHAIN --timeframe 24h --limit 20
# → token_symbol, price_usd, price_change, volume, buy_volume, market_cap_usd, fdv, liquidity, token_age_days

# Smart money only
nansen research token screener --chain $CHAIN --timeframe 24h --smart-money --limit 20

# Search within screener results (client-side filter)
nansen research token screener --chain $CHAIN --search "bonk"

# Smart money holdings — what SM wallets are holding
nansen research smart-money holdings --chain $CHAIN --labels "Smart Trader" --limit 20
# → token_symbol, value_usd, holders_count, balance_24h_percent_change, share_of_holdings_percent

# Nansen indicators for a specific token
TOKEN=<address>
nansen research token indicators --token $TOKEN --chain $CHAIN
# → risk_indicators, reward_indicators (each with score, signal, signal_percentile)

# Flow intelligence — only use for promising tokens from screener/indicators above
nansen research token flow-intelligence --token $TOKEN --chain $CHAIN
# → net_flow_usd per label: smart_trader, whale, exchange, fresh_wallets, public_figure
```

Screener timeframes: `5m`, `10m`, `1h`, `6h`, `24h`, `7d`, `30d`

Indicators: score is "bullish"/"bearish"/"neutral". signal_percentile > 70 = historically significant. Some tokens return empty indicators — not an error.

Flow intelligence is credit-heavy. Use it to confirm SM conviction on tokens that already look promising from screener + indicators, not as a first pass on every token.
