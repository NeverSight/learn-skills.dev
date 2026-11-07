---
name: htx-elite-positioning
version: 1.0.0
description: Top-trader long/short ratio on HTX USDT-M perpetuals — both account-based and position-based ratios, the core sentiment signal that distinguishes "smart money" from retail. Public, no API key.
auth_required: false
risk_level: none
---

# HTX Elite Positioning

Focused skill for **elite (top-trader) long/short ratio** on HTX USDT-M perpetuals. Distinguishes signals from sophisticated traders vs. retail crowd. Public — agent may call freely.

## When to use this skill

Load this skill when the user asks about:

- "Are top traders long or short on BTC?"
- "Smart money positioning on ETH"
- "Top-trader long/short ratio for SOL"
- "Is the elite cohort crowded long?"
- "Compare account vs position ratio for BTC perpetual"
- "Which side are the whales on?"

For **retail / market-wide** ratio, HTX does not currently expose a non-elite long/short endpoint — that's a data gap. Document this in your reply if the user asks for it.

## Underlying tool

Drives `htx-cli`. Binary on `$PATH` or `$HTX_CLI_BIN`. Always pass `--json`.

## Endpoint catalog (2)

| # | Method | Endpoint | CLI invocation | Description |
|---|--------|----------|----------------|-------------|
| 1 | GET | `/linear-swap-api/v1/swap_elite_account_ratio` | `htx-cli futures call GET /linear-swap-api/v1/swap_elite_account_ratio --query contract_code=<code>&period=<period> --json` | Top-trader **account-count** long/short ratio (1 trader = 1 vote) |
| 2 | GET | `/linear-swap-api/v1/swap_elite_position_ratio` | `htx-cli futures call GET /linear-swap-api/v1/swap_elite_position_ratio --query contract_code=<code>&period=<period> --json` | Top-trader **position-size** long/short ratio (size-weighted) |

## Why two ratios?

The two ratios answer different questions:

| Ratio | Question | Strength |
|-------|----------|----------|
| **Account ratio** | How many top traders are net long vs short? | Reflects breadth of conviction |
| **Position ratio** | How much capital is net long vs short? | Reflects size-weighted exposure |

**Divergence is informative**: e.g. account ratio 1.2 (slight long majority) but position ratio 0.6 (heavy short capital) → a few top traders are very heavily short.

## Period values

Both endpoints accept `period`:
- `5min`, `15min`, `30min`, `60min`, `4hour`, `12hour`, `1day`

Returns a time series, typically last 48 data points.

## Contract code format

USDT-M perpetual codes follow `<BASE>-USDT` (e.g. `BTC-USDT`).

## Typical queries → CLI

| User question | CLI command |
|---------------|-------------|
| "BTC top-trader long/short by account" | `htx-cli futures call GET /linear-swap-api/v1/swap_elite_account_ratio --query contract_code=BTC-USDT&period=1hour --json` |
| "ETH top-trader L/S by position size" | `htx-cli futures call GET /linear-swap-api/v1/swap_elite_position_ratio --query contract_code=ETH-USDT&period=4hour --json` |
| "Is smart money crowded long on SOL?" | Both endpoints + interpret divergence |

## Output guidance

Return both ratios when relevant. Compute and label:

| Ratio range | Label |
|-------------|-------|
| `> 2.0` | Heavily long (extreme) |
| `1.3 – 2.0` | Long-leaning |
| `0.77 – 1.3` | Balanced |
| `0.5 – 0.77` | Short-leaning |
| `< 0.5` | Heavily short (extreme) |

(Ratios are symmetric on log scale — `2.0` and `0.5` are equally extreme.)

Always show:
- Current value of both ratios
- Direction of change vs. prior period (rising / falling)
- **Divergence flag** if account ratio and position ratio disagree by > 30%

## Important caveat

- HTX defines "elite" as the top tier of traders by performance/volume on the platform, not "VIP" tier
- The exact constituency is determined by HTX (not user-configurable)
- Elite ratio is **HTX-only** — do not compare 1-to-1 with other exchanges' "top trader" ratios

## Related skills

- `https://github.com/htx-exchange/htx-skills-hub/funding-rate` — combine with funding for crowdedness picture
- `https://github.com/htx-exchange/htx-skills-hub/oi-tracker` — combine with OI for new positioning vs. unwinding
- `https://github.com/htx-exchange/htx-skills-hub/sentiment-analyst` — *(planned Layer 2)* uses elite ratio as a sentiment input
