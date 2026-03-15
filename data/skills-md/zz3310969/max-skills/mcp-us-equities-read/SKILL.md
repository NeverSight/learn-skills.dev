---
name: mcp-us-equities-read
description: "US equities MCP read tools via VPS endpoint (direct rw call)."
---

# MCP US Equities Read

## Purpose
Use this skill when the user needs read-only market research queries against the VPS-hosted MCP server.
This skill is US-only: US equities and US ETFs.

## Prerequisites
1. Install `rw` CLI:
```bash
curl -fsSL https://raw.githubusercontent.com/zz3310969/max-skills/main/scripts/install-rw.sh | bash
```
2. Configure VPS MCP endpoint:
```bash
rw setup --server-url http://113.44.56.214:18080/mcp/
rw doctor
rw tools
```
3. For all examples below, use `rw call --tool ...` (do not use legacy shortcut commands).

## Preflight (required before any rw call)
Run this guard first to avoid stale `rw` versions:

```bash
if ! command -v rw >/dev/null 2>&1; then
  curl -fsSL https://raw.githubusercontent.com/zz3310969/max-skills/main/scripts/install-rw.sh | bash
fi
rw --version || true
rw doctor
```

If `rw doctor` fails due to protocol/auth/session issues, force reinstall:

```bash
curl -fsSL https://raw.githubusercontent.com/zz3310969/max-skills/main/scripts/install-rw.sh | bash
rw doctor
```

## Tool Selection

### Daily/Historical Data
- Company profile and latest context: `read_company_overview`
- Multi-ticker latest snapshot: `read_market_snapshot`
- OHLCV history: `read_price_history`
- Signal stream: `read_signals`
- Research content: `read_reports`
- Upstream/downstream graph: `read_supply_chain_graph`

### Intraday Data (see `mcp-us-equities-intraday` skill for details)
- Bid/ask spread + VWAP: `read_intraday_snapshot`
- Large trades (institutional flow): `read_large_trades`
- Options Greeks: `read_options_greeks`
- Pre-market auction: `read_auction_imbalance`

## US Scope Guardrails
- Tickers must be uppercase tradable US symbols.
- Reject internal material-style codes like `MAT_*`.
- If response `error.code` is `INVALID_MARKET_SCOPE`, ask for a US-listed ticker.

## Direct Query Commands

### `read_company_overview`
```bash
rw call --tool read_company_overview --args '{"ticker":"NVDA"}'
```

### `read_market_snapshot`
```bash
rw call --tool read_market_snapshot --args '{"tickers":["NVDA","AAPL","QQQ"],"fields":["price","technicals","options_flow"]}'
```

### `read_price_history`
```bash
rw call --tool read_price_history --args '{"ticker":"MSFT","start":"2026-01-01T00:00:00Z","end":"2026-03-01T00:00:00Z","limit":300,"order":"desc"}'
```

### `read_signals`
```bash
rw call --tool read_signals --args '{"entity":"NVDA","severity_min":3,"status":"open","limit":50,"order":"desc"}'
```

### `read_reports`
```bash
rw call --tool read_reports --args '{"ticker":"AVGO","since":"2026-01-01T00:00:00Z","sources":["research_reports","expert_rss"],"limit":30,"order":"desc"}'
```

### `read_supply_chain_graph`
```bash
rw call --tool read_supply_chain_graph --args '{"ticker":"TSM","direction":"both","max_depth":2}'
```

## Result Handling
Treat response by the v2 envelope:
- `ok=true`: read from `data`; trace timing/source in `meta`.
- `ok=false`: follow `error.code`, `error.suggestion`, and `error.retryable`.
- `warnings`: data is usable but partial.

Reference mapping: `docs/mcp-tool-map-v2.md`.
