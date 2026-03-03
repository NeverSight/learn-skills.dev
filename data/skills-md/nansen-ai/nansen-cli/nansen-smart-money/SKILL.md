---
name: nansen-smart-money
description: Smart money tracking — netflow, trades, holdings, DCAs, perp trades. Use when finding what smart money wallets are buying/selling or tracking whale activity.
allowed-tools: Bash
---

# Smart Money

All commands: `nansen research smart-money <sub> [options]`

## Subcommands

```bash
# Netflow — what tokens are smart money accumulating?
nansen research smart-money netflow --chain solana --limit 10

# DEX trades — real-time spot trades by smart money
nansen research smart-money dex-trades --chain solana --labels "Smart Trader" --limit 20

# Holdings — aggregated SM portfolio
nansen research smart-money holdings --chain solana --limit 10

# DCAs — Jupiter DCA strategies (Solana only, no --chain needed)
nansen research smart-money dcas --limit 10

# Perp trades — Hyperliquid only (no --chain needed)
nansen research smart-money perp-trades --limit 10

# Historical holdings — time series of SM positions
nansen research smart-money historical-holdings --chain solana --days 30
```

## Labels

Filter by smart money category with `--labels`:

| Label | Use case |
|-------|----------|
| `Fund` | Crypto funds |
| `Smart Trader` | All-time top performers |
| `30D Smart Trader` | Hot hands — top 30 days |
| `90D Smart Trader` | Top 90 days |
| `180D Smart Trader` | Top 180 days |
| `Smart HL Perps Trader` | Top Hyperliquid perp traders |

```bash
nansen research smart-money netflow --chain solana --labels "Fund" --limit 10
```

## Flags

| Flag | Purpose |
|------|---------|
| `--chain` | Required for netflow/dex-trades/holdings/historical-holdings |
| `--labels` | Filter by SM label (quote multi-word values) |
| `--limit` | Number of results |
| `--days` | Lookback for historical-holdings (default 30) |
| `--sort` | Sort field:direction (e.g. `value_usd:desc`) |
| `--fields` | Select specific fields |
| `--table` | Human-readable table output |
| `--format csv` | CSV export |

## Notes

- `dcas` is Solana-only (Jupiter). No `--chain` flag.
- `perp-trades` is Hyperliquid-only. No `--chain` flag.
- `historical-holdings` requires `--chain` and optionally `--token-address`.
