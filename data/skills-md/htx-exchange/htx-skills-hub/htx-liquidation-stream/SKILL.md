---
name: htx-liquidation-stream
version: 1.0.0
description: Query HTX USDT-M perpetual liquidation orders — recent forced-liquidation events for long/short squeeze monitoring and cluster detection. Public, no API key required.
auth_required: false
risk_level: none
---

# HTX Liquidation Stream

Focused skill for **liquidation orders** on HTX USDT-M perpetuals. Use to detect short-squeezes, long-squeezes, and price levels where stop-cascades have been triggered.

## When to use this skill

Load this skill when the user asks about:

- "Recent BTC liquidations"
- "How much was liquidated in the last 24h?"
- "Were there any large liquidations near $X price?"
- "Long squeeze on ETH?"
- "Where did the recent liquidation cluster happen?"
- "Liquidation volume by side (long vs short)"

For aggregated *cross-exchange* liquidation heatmaps, HTX does not expose this — you would need to integrate CoinGlass externally.

## Underlying tool

Drives `htx-cli`. Binary on `$PATH` or `$HTX_CLI_BIN`. Always pass `--json`.

## Endpoint catalog (1)

| # | Method | Endpoint | CLI invocation | Description |
|---|--------|----------|----------------|-------------|
| 1 | GET | `/linear-swap-api/v1/swap_liquidation_orders` | `htx-cli futures market liquidation-orders <contract-code> --json` | Recent forced-liquidation orders for one contract |

## Query parameters

The convenience command auto-fills sensible defaults. For custom filtering use the underlying call form:

```bash
htx-cli futures call GET /linear-swap-api/v1/swap_liquidation_orders \
  --query contract_code=BTC-USDT&trade_type=0&create_date=7&page_size=50 \
  --json
```

| Param | Values | Meaning |
|-------|--------|---------|
| `trade_type` | `0` (all), `1` (closed long forced), `2` (closed short forced), `3` (long order forced), `4` (short order forced) | Filter by liquidation direction |
| `create_date` | `7`, `14`, `30`, `60`, `90` | Days lookback |
| `page_size` | 1–50 | Records per page |
| `page_index` | int (default 1) | Pagination |

## Contract code format

USDT-M perpetual codes follow `<BASE>-USDT` (e.g. `BTC-USDT`).

## Typical queries → CLI

| User question | CLI command |
|---------------|-------------|
| "BTC liquidations last 7d" | `htx-cli futures market liquidation-orders BTC-USDT --json` |
| "ETH long liquidations last 30d" | `htx-cli futures call GET /linear-swap-api/v1/swap_liquidation_orders --query contract_code=ETH-USDT&trade_type=1&create_date=30 --json` |
| "Largest liquidations on SOL last 24h" | Pull `--query contract_code=SOL-USDT&page_size=50 --json` then sort client-side by `volume * price`, filter to last 24h |

## Output guidance

When summarizing liquidations, return:
- **Total liq value (USD)** in the requested window
- **Long liq vs short liq breakdown** (% / absolute)
- **Top 5 single events** by USD value (price + side + time)
- **Cluster zones**: price ranges where ≥ 3 liq events happened within ±0.5%
- **Time-of-day pattern** if relevant (e.g. concentrated during US open)

## Squeeze interpretation

| Pattern | Signal |
|---------|--------|
| Heavy long liqs + price ↓ | Capitulation cascade — potential reversal zone |
| Heavy short liqs + price ↑ | Short squeeze — potential exhaustion as squeeze fuel runs out |
| Liq cluster at round number | Stop-loss bunch — price often retests |

## Related skills

- `https://github.com/htx-exchange/htx-skills-hub/funding-rate` — pre-squeeze crowdedness
- `https://github.com/htx-exchange/htx-skills-hub/oi-tracker` — post-squeeze OI drop confirms cascade
- `https://github.com/htx-exchange/htx-skills-hub/derivatives-analyst` — *(planned Layer 2)* combines liq + funding + OI for unified pressure score
