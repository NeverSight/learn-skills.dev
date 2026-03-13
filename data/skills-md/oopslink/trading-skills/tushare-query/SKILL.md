---
name: tushare-query
description: Use when setting up tushare-cli token, choosing output formats, or getting an overview of available A-share market data query skills
---

# tushare-query: Setup & Overview

## Token Setup

```bash
tushare-cli config set-token <YOUR_TOKEN>
# or: export TUSHARE_TOKEN=<token>
```

## Common Flags

| Flag | Effect |
|------|--------|
| `--format json` | JSON output (pipe to `jq`) |
| `--format csv` | CSV output (redirect to file) |
| `--cache` | Cache result within session |

## Format Tips

- Date: always `YYYYMMDD` (e.g., `20240201`)
- ts_code: `XXXXXX.SZ` Shenzhen · `XXXXXX.SH` Shanghai · `XXXXXX.SI` Shenwan index
- Best combo: `--format json | jq 'sort_by(-.pct_chg) | .[:10]'`

## Skills by Domain

| Domain | Skill |
|--------|-------|
| Individual stocks, ETF, capital flow | `tushare-stock` |
| Shenwan index, sector constituents | `tushare-index` |
| Concept boards, volume anomaly | `tushare-concepts` |
| Sector rotation & ranking | `tushare-alpha` |
| Financial statements | `tushare-financial` |
| Futures contracts & holdings | `tushare-futures` |
| Forex rates | `tushare-forex` |
