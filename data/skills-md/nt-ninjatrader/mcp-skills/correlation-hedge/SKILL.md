---
name: correlation-hedge
description: Compute historical Pearson correlation and OLS regression beta between two futures symbols, on log-returns. Turn that result into a dollar-neutral hedge proposal for an open position. Covers cross-underlying relationships — ES vs NQ, CL vs NG, GC vs SI, bonds vs stocks, and currencies vs DX. For same-underlying siblings like ES/MES, use contract-intel instead. Produces sized hedge candidates with raw qty, rounded qty, residual exposure percentage, and coverage percentage. Always informational — never emits order payloads. Use when the user asks about "correlation between X and Y", "hedge this", "how do I hedge", "what could I short to offset", "beta", "X vs Y correlation", "cross-asset", "co-move", "correlated exposure", or "am I already long the market".
compatibility: This skill requires the NinjaTrader MCP server, connected through a client with MCP support.
---

# correlation-hedge

## Purpose

Two linked jobs:

1. **Measure** — historical Pearson correlation and OLS regression β between any two futures symbols. Uses log-return series over a lookback window.
2. **Size** — turn an open position's dollar exposure into a dollar-neutral hedge proposal. Use β and value-per-point math.

## Environment routing

Symbol/market data only — no account binding. A sibling skill's account resolution might already pin the session to demo (simulation) or live. If so, stay on that same MCP server.

## MCP tools used

Tool names below are bare. The NinjaTrader MCP server provides them. Your client adds its own prefix. See `AGENTS.md` at the repo root.

- `market_history` — aligned bar closes for two symbols over the lookback window
- `my_portfolio` — open positions for hedge-mode input (qty, netPrice). Prune with `fields=["positions[].symbol","positions[].netPos","positions[].netPrice","account.netLiq"]`.
- `market_snapshot` — `valuePerPoint`, `tickSize`, current mark for the hedge candidate. Prune with `fields=["snapshots[].symbol","snapshots[].valuePerPoint","snapshots[].tickSize","snapshots[].lastPrice"]`.
- `search_contracts` — resolve bare product codes to contract symbols for both legs
- `user_profile` — discover available account names when the account is unknown

## Workflow

### 1. Classify the ask

| User phrasing | Mode |
|---------------|------|
| "correlation between X and Y", "X vs Y", "how correlated" | correlation only |
| "hedge my ES", "what should I short to offset" | correlation → hedge sizing |
| "am I already long the market?" | correlation + portfolio cross-check |
| "beta of NQ on ES" | correlation (β output) |

### 2. Gather aligned history

Pick a lookback (default 30–90 sessions for cross-family, 5–30 sessions for within-family):

```
market_history(symbol=SYM_A, barType="Daily", barSize=1, from=<ISO-8601>, to=<ISO-8601>)
market_history(symbol=SYM_B, barType="Daily", barSize=1, from=<ISO-8601>, to=<ISO-8601>)
```

For hourly bars use `barType="Minute", barSize=60`. `from` requires `to`. For "last N bars", pass `count=` instead of a range.

**Bar-size choice matters:**
- Daily bars: most stable correlation, regime-level signal
- 60-minute bars: captures intra-session drift, more noise
- Avoid sub-hour for cross-product hedging — microstructure noise
  dominates the signal

### 3. Compute correlation + β

Save the two symbols' `market_history` responses to a file (shape `{"series": {SYM_A: [...], SYM_B: [...]}}`) and pass its path with `--file`. Never re-type or inline the bar arrays into the command.

```bash
python3 scripts/correlation.py --file series.json --window 30
```

The script aligns bars on shared timestamps, computes log returns, then reports:
- `pearson_r` — linear correlation of returns (−1 to 1)
- `beta_B_on_A` — OLS slope of B's returns regressed on A's. Use A as the position symbol, B as the hedge candidate.
- `vol_A`, `vol_B` — return stdev of each
- `rolling` (optional, with `--window`) — current r vs rolling mean/stdev + regime flag (`tightening`/`loosening`/`stable`)

**Compare to priors** in `references/hedge-patterns.md`. If the live r is way outside the typical range for that pair, call it out. The cause may be a regime shift, a data quality issue, or a rare moment.

### 4. Size the hedge (if asked)

**Account resolution.** Position data (qty, direction, basis) comes from `my_portfolio(account=<name>)` — the MCP requires `account=`. If the account name is unknown, call `user_profile()` first and pull `accounts[].name` to discover available accounts.

Pull the position + hedge candidate market snapshot, then:

```bash
python3 scripts/hedge_sizing.py --file hedge_input.json
```

where `hedge_input.json` holds the position + hedge candidate:

```json
{
  "position": {
    "symbol": "ESU6", "direction": "long", "qty": 4,
    "price": 7170.0, "value_per_point": 50.0
  },
  "hedge_candidate": {
    "symbol": "NQU6", "price": 22640.0, "value_per_point": 20.0,
    "beta": 2.59
  }
}
```

Output fields:
- `hedge.side` — `Buy` or `Sell`. Opposite of the position side when β > 0 (typical); same side when β < 0 (stock/bond hedge).
- `hedge.raw_qty` — unrounded contracts (e.g., 3.4 NQ)
- `hedge.rounded_qty` — whole contracts at `--round` mode (`nearest`/`up`/`down`)
- `hedge.residual_pct` — |raw - rounded| / raw × 100
- `coverage.coverage_pct` — how much of the $ exposure the rounded hedge actually covers
- `coverage.residual_exposure_dollars` — uncovered $ per 1%

**When `rounded_qty = 0`** or `residual_pct > 30%`, the script emits a `note` that suggests a micro (MES/MNQ/MCL/MGC) for finer sizing. Surface that verbatim.

### 5. Multi-candidate hedge comparison

Run `hedge_sizing.py` N times with different candidates. Rank by `coverage_pct` near 100% with low `residual_pct`. Pick the best trade-off between coverage and rounding precision.

This skill ships no `basket.py` script. Loop over the candidates instead:

```bash
for cand in 'NQ 22640 20 2.59' 'MES 7170 5 1.0' 'YM 43500 5 0.9' 'RTY 2400 50 0.7'; do
  # build JSON, pipe to hedge_sizing.py, collect coverage_pct
done
```

### 6. Narrate — with regime context

Pair the sizing output with the live correlation, so the user sees the assumption behind it. See `references/regime-caveat.md` for framing patterns.

## Output idioms

**Correlation-only:**

> "ES/NQ over last 16 daily bars: Pearson r 0.99 (very tight),
> β_NQ_on_ES = 2.59 (NQ moves ~2.6× ES in log returns over this
> window). Rolling 8-bar window shows r stable at 0.99. This is
> slightly above the typical 0.85-0.95 range — tight regime."

**Hedge proposal:**

> "You're long 4 ES @ 7170 (\$14,340 per 1% ES move).
>
> Short 1 NQ at 22640 covers 82% (\$11,739 offset). Residual \$2,601
> long ES. One-NQ rounds down from raw 1.22; a second NQ would
> over-hedge. Consider 1 NQ + 2 MNQ for finer coverage.
>
> Math assumes ES/NQ correlation holds (0.99 tight right now, but
> pairs can decouple in regime shifts). This isn't a guaranteed
> protection — it's a dollar-neutral offset conditional on the
> correlation staying similar."

**Portfolio cross-check:**

> "You're long 4 ES AND long 2 NQ. With β=2.59, the 2 NQ longs
> are effectively +5.2 ES-equivalents of additional exposure —
> you're 9.2 ES-equivalents long the market, not 6. If that's
> not intended, consider flattening one or adjusting size."

## Disambiguation

- **vs `contract-intel`**: contract-intel handles SAME-underlying pairs (ES vs MES — fungible siblings). correlation-hedge handles CROSS-underlying (ES vs NQ, CL vs NG). Different math, different use cases.
- **vs `market-context`'s `cross_symbol.py`**: that script does INTRADAY relative strength (who led today). correlation-hedge does HISTORICAL correlation over a lookback window. Distinct semantics — do not mix them.
- **vs `scale-manager`**: this skill is informational (what is the hedge?). scale-manager converts a hedge decision into exact `place_order` payloads. Run correlation-hedge first, then route the chosen hedge through scale-manager for the execution plan.
- **vs `position-watchdog`**: watchdog reports current position health per-symbol. correlation-hedge reports cross-symbol exposure interactions. They are complementary.

## Explicit non-goals

- **No order payloads.** Informational sizing only.
- **No rule endorsement.** One computation is not a rule (see `references/regime-caveat.md`).
- **No basket optimization** today. Loop over candidates in the skill workflow instead. A future release may add a multi-position optimizer.
- **No options hedging.** Correlation- and beta-based sizing is not the right model for options. Options need greeks-based hedging instead. If the user asks about an options hedge, redirect to an external tool.
- **No event hedging.** Tail-risk hedging against specific events (CPI surprise, FOMC shock) is not correlation-sized. Route to `event-watch` for event-window alert sizing instead.

## Resource layout

- `scripts/correlation.py` — time-aligned Pearson r + OLS β on log returns of two symbols. Supports `--window N` for rolling r with regime flagging. Requires ≥3 overlapping bars minimum.
- `scripts/hedge_sizing.py` — dollar-neutral hedge sizing from position + hedge candidate + β. Reports raw/rounded qty, coverage %, residual $ exposure. Flags rounded=0 and residual>30% with micro-contract suggestion. Supports `--round nearest|up|down`.
- `scripts/fixtures/es_nq_synthetic.json` — a 17-bar ES+NQ fixture that produces a near-perfect correlation, for smoke testing.
- `references/hedge-patterns.md` — typical correlation ranges for 7 product families (equity indexes, energy, metals, bonds, currencies, grains, cross-family). Priors only — always validate with live data. Load it when you compare a live r or β to the typical range.
- `references/regime-caveat.md` — the stationarity-assumption framing. It explains how to narrate a hedge honestly, when to flag a regime shift, and why tail risk matters. Load it when you narrate a hedge recommendation.
