---
name: htx-oi-tracker
version: 1.0.0
description: Track HTX USDT-M perpetual open interest — current OI snapshot per contract, plus historical OI time series for trend and surge detection. Public, no API key required.
auth_required: false
risk_level: none
---

# HTX Open Interest Tracker

Focused skill for **open interest (OI)** on HTX USDT-M perpetuals. Public endpoints — agent may call them freely.

## When to use this skill

Load this skill when the user asks about:

- "BTC perpetual OI right now"
- "How much has ETH OI changed in the last 24h?"
- "Show me OI trend for SOL-USDT"
- "Is OI surging on any contract?"
- "OI vs price divergence on BTC"
- "Total OI across all USDT-M perpetuals"

For combined OI + funding + multi-signal scoring, prefer `htx-derivatives-analyst` *(planned Layer 2)*.

## Underlying tool

Drives `htx-cli`. Binary on `$PATH` or `$HTX_CLI_BIN`. Always pass `--json`.

## Endpoint catalog (2)

| # | Method | Endpoint | CLI invocation | Description |
|---|--------|----------|----------------|-------------|
| 1 | GET | `/linear-swap-api/v1/swap_open_interest` | `htx-cli futures call GET /linear-swap-api/v1/swap_open_interest [--query contract_code=<code>] --json` | Current OI snapshot. Without `contract_code`, returns all contracts. |
| 2 | GET | `/linear-swap-ex/market/his_open_interest` | `htx-cli futures call GET /linear-swap-ex/market/his_open_interest --query contract_code=<code>&period=<period>&size=<N> --json` | Historical OI time series for trend / surge analysis. |

## Contract code format

USDT-M perpetual codes follow `<BASE>-USDT` (e.g. `BTC-USDT`).

## Period & size for historical OI

`his_open_interest` accepts:
- `period`: `60min`, `4hour`, `12hour`, `1day`
- `size`: 1 to 200

## Typical queries → CLI

| User question | CLI command |
|---------------|-------------|
| "BTC current OI" | `htx-cli futures call GET /linear-swap-api/v1/swap_open_interest --query contract_code=BTC-USDT --json` |
| "All-contract OI snapshot" | `htx-cli futures call GET /linear-swap-api/v1/swap_open_interest --json` |
| "ETH OI 4h trend last 200 bars" | `htx-cli futures call GET /linear-swap-ex/market/his_open_interest --query contract_code=ETH-USDT&period=4hour&size=200 --json` |
| "BTC OI 24h change %" | Pull 1d period size=2, compute `(latest - previous) / previous * 100` client-side |

## Output guidance

Return:
- **Current OI** in contracts (`amount`) and base currency (`volume` × multiplier)
- **24h Δ %** (compute from `his_open_interest` series)
- **Trend label**: surging (>10% in 4h), rising, stable, declining, plunging (<-10% in 4h)
- For all-contracts query: top 5 by absolute OI and top 5 by 24h growth

## OI signal interpretation

| Pattern | Signal |
|---------|--------|
| OI ↑ + price ↑ | New longs entering — bullish continuation |
| OI ↑ + price ↓ | New shorts entering — bearish continuation |
| OI ↓ + price ↑ | Shorts covering — squeeze risk |
| OI ↓ + price ↓ | Longs unwinding — capitulation |

## Related skills

- `https://github.com/htx-exchange/htx-skills-hub/funding-rate` — funding rate context for crowdedness
- `https://github.com/htx-exchange/htx-skills-hub/elite-positioning` — top-trader long/short ratio
- `https://github.com/htx-exchange/htx-skills-hub/derivatives-analyst` — *(planned Layer 2)* multi-signal pressure scoring
