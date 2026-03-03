---
name: nansen-token
description: Token analytics — screener, indicators, OHLCV, holders, flows, PnL, DEX trades, flow intelligence. Use when researching a specific token, checking smart money holders, or screening trending tokens.
allowed-tools: Bash
---

# Token Analytics

All commands: `nansen research token <sub> [options]`

`--chain` required. Use `--token <address>` for token-specific endpoints.

## Screener

```bash
# Top tokens by volume
nansen research token screener --chain solana --timeframe 24h --limit 20

# Smart money only
nansen research token screener --chain solana --timeframe 24h --smart-money --limit 20

# Search within screener results (client-side filter)
nansen research token screener --chain solana --search "bonk"
```

Timeframes: `5m`, `10m`, `1h`, `6h`, `24h`, `7d`, `30d`

## Token Info & Indicators

```bash
nansen research token info --token <addr> --chain solana
nansen research token indicators --token <addr> --chain ethereum
```

`indicators` returns Nansen Score: risk indicators (BTC-reflexivity, token-supply-inflation) and reward indicators (funding-rate, price-momentum) with signal percentiles.

## OHLCV

```bash
nansen research token ohlcv --token <addr> --chain solana --timeframe 1h
```

Timeframes: `1m`, `5m`, `15m`, `30m`, `1h`, `2h`, `4h`, `1d`, `1w`, `1M`

## Holders

```bash
nansen research token holders --token <addr> --chain solana
nansen research token holders --token <addr> --chain solana --smart-money
```

## Flows

```bash
nansen research token flows --token <addr> --chain solana --days 7
nansen research token flow-intelligence --token <addr> --chain solana
nansen research token who-bought-sold --token <addr> --chain solana
```

`flow-intelligence` breaks down by label: whales, smart traders, exchanges, fresh wallets, public figures.

## DEX Trades, PnL & Transfers

```bash
nansen research token dex-trades --token <addr> --chain solana --limit 20
nansen research token pnl --token <addr> --chain solana --sort total_pnl_usd:desc
nansen research token transfers --token <addr> --chain solana --enrich
```

`--enrich` on transfers adds Nansen labels to from/to addresses.

## Perps & DCA (no --chain)

```bash
nansen research token perp-trades --symbol ETH --days 7
nansen research token perp-positions --symbol BTC
nansen research token perp-pnl-leaderboard --symbol SOL
nansen research token jup-dca --token <addr>
```

## Flags

| Flag | Purpose |
|------|---------|
| `--chain` | Required (ethereum, solana, base, etc.) |
| `--token` | Token address (alias: `--token-address`) |
| `--symbol` | Token symbol for perp endpoints (e.g. BTC) |
| `--timeframe` | Screener or OHLCV interval |
| `--smart-money` | Filter to SM wallets only (screener, holders) |
| `--days` | Lookback period (default 30) |
| `--sort` | Sort field:direction (e.g. `total_pnl_usd:desc`) |
| `--enrich` | Add Nansen labels to transfer addresses |
| `--fields` | Select specific fields |
| `--table` | Human-readable table output |
| `--format csv` | CSV export |

## Notes

- Perp endpoints use `--symbol` (e.g. BTC), not `--token`.
- `jup-dca` is Solana-only.
- `holders --smart-money` returns UNSUPPORTED_FILTER for tokens without SM tracking.
- `flow-intelligence` may return all-zero flows for illiquid tokens.
