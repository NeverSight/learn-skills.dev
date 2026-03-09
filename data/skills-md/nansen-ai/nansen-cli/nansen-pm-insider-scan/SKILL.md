---
name: nansen-pm-insider-scan
description: "Scan a resolved Polymarket market for wallets exhibiting suspicious trading patterns: fresh funding, single-market focus, extreme ROI, late entry at high prices."
---

# PM Suspicious Wallet Scanner

**Answers:** "Are there wallets with suspicious trading patterns in this Polymarket market?"

```bash
# 1. Find the resolved market
nansen research prediction-market market-screener --query "<market name>" --status closed --limit 5
# → market_id, question, volume, last_trade_price

# 2. Get top winners (positive PnL) — paginate if needed, keep per_page <= 10
MID=<market_id>
nansen research prediction-market pnl-by-market --market-id $MID --limit 10
# → address (proxy), owner_address (wallet), side_held, net_buy_cost_usd, total_pnl_usd

# 3. For each top winner, run these three calls (use proxy address for PM, owner for profiler):
PROXY=<address_from_pnl>
nansen research prediction-market trades-by-address --address $PROXY --limit 100
# → market_id, market_question, side, price, size, usdc_value, taker_action, timestamp

OWNER=<owner_address_from_pnl>
nansen research profiler historical-balances --address $OWNER --chain polygon --days 365 --sort block_timestamp:asc --limit 100
# → block_timestamp, value_usd, token_symbol — first non-zero value_usd = wallet funding date

nansen research profiler labels --address $OWNER --chain polygon
# → label, category
```

For each winner, compute ROI = total_pnl_usd / net_buy_cost_usd * 100 (skip ROI flags if net_buy_cost_usd <= 0), then score (0–13). Within each tier group, apply only the highest matching flag:

| Flag | Pts | Trigger |
|---|---|---|
| NEW_WALLET | 3 | First funded within 7 days of now |
| YOUNG_WALLET | 1 | First funded 8–28 days ago (skip if NEW_WALLET fires) |
| SINGLE_MARKET | 3 | trades-by-address shows only 1 distinct market_id |
| FEW_MARKETS | 1 | 2–3 distinct market_ids (skip if SINGLE_MARKET fires) |
| EXTREME_ROI | 3 | ROI >= 500% |
| HIGH_ROI | 2 | ROI 200–499% (skip if EXTREME_ROI fires) |
| LATE_ENTRY | 2 | Any trade on this market at price >= 0.80 |
| LARGE_POSITION | 2 | net_buy_cost_usd >= $10k |
| KNOWN_ENTITY | -2 | Has Nansen labels |

Flagged at score >= 3. High risk at >= 7. High-confidence suspicious pattern: NEW_WALLET + SINGLE_MARKET + EXTREME_ROI (score 9+).

If owner_address is invalid (e.g. "0x"), use the proxy address for profiler calls too. If historical-balances returns no records with value_usd > 0, the wallet may predate the 365-day window — treat wallet age as unknown and skip NEW_WALLET / YOUNG_WALLET flags. Pause ~1.5s between wallets to avoid rate limits. Skip wallets that error and continue scanning.
