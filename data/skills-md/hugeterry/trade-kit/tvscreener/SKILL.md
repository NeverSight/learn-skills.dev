---
name: tvscreener
description: Query TradingView screener data for stocks (HK/A-share/US/global), crypto, forex, bonds, futures, and coins via deepentropy/tvscreener. Supports technical indicators, fundamental screening, sector/industry filters, cross signals, field presets, streaming, and MCP server integration.
---

# tvscreener

Use this skill for market queries with simple scripts first, then native Python when needed.

Supports 6 asset types: **Stock**, **Crypto**, **Forex**, **Bond**, **Futures**, **Coin**.

## Install

```bash
python3 -m pip install -U tvscreener

# For MCP server support (optional)
python3 -m pip install -U "tvscreener[mcp]"
```

Python must be `>=3.10`.

## Quick commands (run from skill root)

> Use Python 3.10+ in your preferred environment (venv/pyenv/system Python).

### Stock queries

```bash
# Single-symbol snapshot (recommended for stock)
python3 scripts/query_symbol.py --symbol HKEX:700 --market HONGKONG

# Custom query with fields + filters
python3 scripts/custom_query.py \
  --type stock --market CHINA \
  --symbol SHSE:600519 \
  --fields 'NAME,PRICE,CHANGE_PERCENT,VOLUME,RELATIVE_STRENGTH_INDEX_14,MACD_LEVEL_12_26,MACD_SIGNAL_12_26,MACD_HIST,SIMPLE_MOVING_AVERAGE_20,SIMPLE_MOVING_AVERAGE_50,SIMPLE_MOVING_AVERAGE_200,EXPONENTIAL_MOVING_AVERAGE_20,EXPONENTIAL_MOVING_AVERAGE_50,EXPONENTIAL_MOVING_AVERAGE_200,BOLLINGER_UPPER_BAND_20,BOLLINGER_LOWER_BAND_20,STOCHASTIC_PERCENTK_14_3_3,STOCHASTIC_PERCENTD_14_3_3,AVERAGE_TRUE_RANGE_14,MOVING_AVERAGES_RATING' \
  --filter 'NAME=600519'

# Top US stocks by volume
python3 scripts/custom_query.py --type stock --market AMERICA --sort -VOLUME --limit 20
```

### Crypto / Forex / Other asset queries

```bash
# Bitcoin
python3 scripts/custom_query.py --type crypto --filter "NAME=BTCUSD"

# Top 20 crypto by 24h volume
python3 scripts/custom_query.py --type crypto --sort -VOLUME_24H_IN_USD --limit 20

# EUR/USD forex pair
python3 scripts/custom_query.py --type forex --filter "NAME=EURUSD"

# Bonds / Futures / Coins
python3 scripts/custom_query.py --type bond --limit 20
python3 scripts/custom_query.py --type futures --limit 20
python3 scripts/custom_query.py --type coin --sort -VOLUME_24H_IN_USD --limit 20
```

### Field discovery

```bash
python3 scripts/discover_fields.py --keyword macd --limit 20
```

### Shell quoting notes

- Wrap `--fields` and `--filter` in single quotes.
- If you use interval syntax like `FIELD|60`, quoting is mandatory to avoid shell pipe parsing.

## custom_query.py arguments

| Arg | Default | Description |
|-----|---------|-------------|
| `--type` | `stock` | Asset type: stock, crypto, forex, bond, futures, coin |
| `--market` | (none) | Market enum name (stock only): HONGKONG, CHINA, AMERICA, etc. |
| `--symbol` | (none) | Exact symbol preference, e.g. HKEX:700 |
| `--fields` | (per-type defaults) | Comma-separated Field names; supports FIELD\|60 interval syntax |
| `--filter` | (none) | Filter expression: PRICE>100, NAME=600519 (repeatable) |
| `--sort` | (none) | Sort field; prefix `-` for descending: -VOLUME |
| `--limit` | 100 | Max results |
| `--csv` | (none) | Optional CSV output path |

## Query rules

- Core technical set (recommended): `PRICE`, `CHANGE_PERCENT`, `VOLUME`, `RELATIVE_STRENGTH_INDEX_14`, `MACD_LEVEL_12_26`, `MACD_SIGNAL_12_26`, `MACD_HIST`, `SIMPLE_MOVING_AVERAGE_20/50/200`, `EXPONENTIAL_MOVING_AVERAGE_20/50/200`, `BOLLINGER_UPPER_BAND_20`, `BOLLINGER_LOWER_BAND_20`, `STOCHASTIC_PERCENTK_14_3_3`, `STOCHASTIC_PERCENTD_14_3_3`, `AVERAGE_TRUE_RANGE_14`, `MOVING_AVERAGES_RATING`
- Interval fields syntax: `FIELD|60` / `FIELD|240` (example: `RELATIVE_STRENGTH_INDEX_14|60`)
  - **Current caveat**: interval fields may fail in `scripts/custom_query.py` with `FieldWithInterval` attribute errors in some tvscreener versions.
  - Workaround: run without interval fields, or use `scripts/query_symbol.py` for stable single-symbol technical snapshots.
- Script filter ops: `=`, `!=`, `>`, `<`, `>=`, `<=`
- Native Python also supports: `CROSSES`, `CROSSES_UP`, `CROSSES_DOWN`, `MATCH`, `between()`, `isin()` (see references)

## MCP Server (v0.2.0+)

tvscreener includes a built-in MCP server that exposes screener tools directly to Claude — no scripts needed.

```bash
# Start server
tvscreener-mcp

# Register with Claude
claude mcp add tvscreener -- tvscreener-mcp
```

Available MCP tools: `search_fields`, `get_field_categories`, `custom_screen`, `screen_stocks`, `screen_crypto`, `screen_forex`.

See `references/api/mcp_server.md` for full details.

## Troubleshooting

- `ImportError: cannot import name 'Market' from 'tvscreener'`
  - Usually caused by mismatched Python/site-packages or multiple Python environments.
  - Fix: ensure commands and installation use the same Python (3.10+), then reinstall:
    - `python3 -m pip install -U tvscreener`
- `zsh: command not found: 60,...`
  - Cause: unquoted `FIELD|60` interpreted as shell pipes.
  - Fix: single-quote the full `--fields` string.
- `--market` ignored for non-stock types
  - Market filtering only applies to `--type stock`. Other screener types use their own default markets.

## References

- Workflow + patterns: `references/README_USAGE.md`
- API details:
  - `references/api/screeners.md` — Screener classes, methods, streaming, beautify
  - `references/api/fields.md` — Field enums, presets, discovery, intervals, history
  - `references/api/filters.md` — Filter operators, cross signals, auto-merge
  - `references/api/enums.md` — Market, Sector, Industry, Country, Region, IndexSymbol, SymbolType, Rating
  - `references/api/mcp_server.md` — MCP server tools and setup

If scripts are insufficient, read references and write direct Python using tvscreener native API.

## Regression test

```bash
bash scripts/test_markets.sh
```

Covers Tencent (HK), Moutai (A), A-share ETF (510300), and BIDU (US).
