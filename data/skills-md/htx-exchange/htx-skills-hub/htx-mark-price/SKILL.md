---
name: htx-mark-price
version: 1.0.0
description: Mark price, premium index, and basis kline series for HTX USDT-M perpetuals — fair-value pricing for liquidation reference and basis monitoring. Public, no API key required.
auth_required: false
risk_level: none
---

# HTX Mark Price, Premium Index & Basis

Focused skill for **mark price**, **premium index**, and **basis** kline series on HTX USDT-M perpetuals. Mark price drives liquidation; premium index drives funding rate; basis = mark − index price (the spread vs spot reference). All public.

## When to use this skill

Load this skill when the user asks about:

- "BTC mark price kline 4h"
- "Show me premium index for ETH-USDT"
- "Why is the mark price different from last trade?"
- "Premium index history before this funding settlement"
- "Mark price vs index price spread on SOL"
- "Is the perpetual trading at premium or discount?"
- "BTC basis history"

## Underlying tool

Drives `htx-cli`. Binary on `$PATH` or `$HTX_CLI_BIN`. Always pass `--json`.

## Endpoint catalog (2)

| # | Method | Endpoint | CLI invocation | Description |
|---|--------|----------|----------------|-------------|
| 1 | GET | `/linear-swap-ex/market/history/mark_price_kline` | `htx-cli futures call GET /linear-swap-ex/market/history/mark_price_kline --query contract_code=<code>&period=<period>&size=<N> --json` | Mark price kline (used for liquidation, position PnL) |
| 2 | GET | `/linear-swap-ex/market/history/premium_index_kline` | `htx-cli futures call GET /linear-swap-ex/market/history/premium_index_kline --query contract_code=<code>&period=<period>&size=<N> --json` | Premium index kline (deviation of perpetual from spot, drives funding) |

## Period values

- `1min`, `5min`, `15min`, `30min`, `60min`, `4hour`, `1day`

`size` range: 1–2000 (typical: 200).

## Contract code format

USDT-M perpetual codes follow `<BASE>-USDT` (e.g. `BTC-USDT`).

## Concept reference

| Term | Definition |
|------|------------|
| **Mark price** | Fair-value reference price = index price × (1 + premium index over a moving window). Used for **liquidation triggers** and **unrealized PnL**, NOT for matching trades. |
| **Index price** | Spot-based reference, weighted basket of major spot exchanges. |
| **Premium index** | `(Mark - Index) / Index`. Positive = perpetual trading at premium (longs heavy); negative = discount. |
| **Funding rate** | Calculated from a smoothed premium index + interest rate component. Reset every 8h. |

## Typical queries → CLI

| User question | CLI command |
|---------------|-------------|
| "BTC mark 1h kline last 200 bars" | `htx-cli futures call GET /linear-swap-ex/market/history/mark_price_kline --query contract_code=BTC-USDT&period=60min&size=200 --json` |
| "ETH premium 15m kline" | `htx-cli futures call GET /linear-swap-ex/market/history/premium_index_kline --query contract_code=ETH-USDT&period=15min&size=200 --json` |
| "Is SOL trading at premium right now?" | Pull premium kline size=1 → check sign and magnitude |
| "BTC basis 1h kline last 100" | `htx-cli futures call GET /index/market/history/linear_swap_basis -p contract_code=BTC-USDT -p period=60min -p basis_price_type=close -p size=100 --json` |

## Output guidance

Return:
- Latest mark/premium values
- 1h / 4h / 24h change
- For premium index: label as `discount (>−0.05%)`, `neutral (±0.05%)`, `mild premium (0.05%-0.2%)`, `heavy premium (>0.2%)`

## Related skills

- `https://github.com/htx-exchange/htx-skills-hub/funding-rate` — premium drives funding direction
- `https://github.com/htx-exchange/htx-skills-hub/futures-market` — index price endpoint (basis denominator)
- `https://github.com/htx-exchange/htx-skills-hub/derivatives-analyst` — *(planned Layer 2)* combines mark/premium/funding/OI into pressure score
