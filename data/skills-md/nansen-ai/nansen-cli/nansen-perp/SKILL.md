---
name: nansen-perp
description: Perpetuals analytics on Hyperliquid — screener, leaderboard. Use when checking perp markets, funding rates, or top perp traders.
allowed-tools: Bash
---

# Perps (Hyperliquid)

No `--chain` flag needed — Hyperliquid only.

## Screener

```bash
# Top perp markets by volume
nansen research perp screener --sort volume:desc --limit 20

# By open interest
nansen research perp screener --sort open_interest:desc --limit 10
```

## Leaderboard

```bash
# Top perp traders by PnL
nansen research perp leaderboard --days 7 --limit 20
```

## Flags

| Flag | Purpose |
|------|---------|
| `--sort` | Sort field:direction (e.g. `volume:desc`) |
| `--limit` | Number of results |
| `--days` | Lookback period (default 30) |
| `--fields` | Select specific fields |
| `--table` | Human-readable table output |
| `--format csv` | CSV export |

## Notes

- For token-specific perp data, use `nansen research token perp-trades --symbol BTC`.
- For wallet-specific perp data, use `nansen research profiler perp-positions --address <addr>`.
- Portfolio perp exposure: `nansen research portfolio defi --wallet <addr>`.
