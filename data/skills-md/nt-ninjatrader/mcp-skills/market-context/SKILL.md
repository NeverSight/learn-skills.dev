---
name: market-context
description: Computes market metrics for futures from market_history output. Metrics include session VWAP, POC/VAH/VAL (value area), bar-level delta, cumulative delta, order-flow imbalance, ATR(N), realized volatility, and cross-symbol relative strength. It produces narrative summaries of market structure and the volatility regime. Use when the user asks about VWAP, POC, market profile, or value area. Also use for ATR, realized volatility, delta, cumulative delta, or order-flow imbalance. Also use for the volatility regime, or for intra-day relative strength between related symbols (e.g., ES vs NQ vs RTY). position-watchdog, pretrade-risk, scale-manager, chart-render, trade-replay, and trade-debrief consume this skill's output as input.
compatibility: This skill requires the NinjaTrader MCP server, connected through a client with MCP support.
---

# market-context

## Purpose

Compute session VWAP, POC / Value Area, ATR, realized-vol, price-vs-VWAP z-score, and cross-symbol relative strength from `market_history`. Produce opinionated narrative over the numbers — not raw JSON dumps.

**Descriptive, not predictive.** Every output describes the fetched bar window: session high, session low, and where volume clustered. It also reports the session's volatility level. Outputs do not forecast future prices or recommend trades. A user may ask about the future. An example is "will it break out?" For that kind of question, state the descriptive limit clearly in the narration. The skill can describe the conditions before past breakouts. It cannot predict the next one.

## Environment routing

Symbol/market data only — no account binding. A sibling skill's account resolution might already pin the session to demo (simulation) or live. If so, stay on that same MCP server.

## MCP tools used

Tool names below are bare. The NinjaTrader MCP server provides them. Your client adds its own prefix. See `AGENTS.md` at the repo root.

- `market_history` — the bar data for the symbol. Set `symbol`, `barType`, `barSize`, and `volumeProfile=true` for histogram-based VWAP or market profile.
- `market_snapshot` — fallback source for `tickSize` when `market_history` doesn't carry it.
- `search_contracts` — alternate source for `tickSize`.

## Workflow

### 1. Pull bars

Call `market_history` with:

- `symbol` — the contract symbol (e.g., `ESU6`)
- `barType` — `Minute` for intraday, `Daily` for daily
- `barSize` — e.g., `5` for 5-minute bars
- `volumeProfile: true` for histogram-based VWAP or market profile

For a typical session-context read, 5-minute bars over the RTH session are a reasonable default. For volatility-regime reads, use Daily bars across a 20–60 day lookback.

### 2. Get tick size (only for histogram mode)

`histogram[].price` is a **tick offset from bar.open**, not an absolute price. Actual price = `bar.open + histogram[i].price × tickSize`.

`tickSize` is **not** in the `market_history` response. Fetch it from one of these:

- `market_snapshot` with the same symbol
- `search_contracts`

For full detail and the common-products cheat sheet, see `references/histogram-offset.md`.

### 3. Pipe bars to the right script

Every script reads the `market_history` response as JSON and prints JSON to stdout. Save the tool result to a file and pass its path with `--file`. Never re-type or inline a large JSON payload into the command. You can still pipe input on stdin as a fallback.

**`--tick-size` is contract-specific** — source it from Step 2 (`market_snapshot.tickSize` or `search_contracts.tickSize`). Common values: ES/MES/NQ/MNQ `0.25`, YM/MYM `1.00`, ZB `0.03125`, ZN `0.015625`, CL/MCL `0.01`, GC `0.10`, SI `0.005`. A hardcoded `0.25` works for ES/NQ. It silently mis-prices YM (4× too small). It also mis-prices ZB (8× too large) and CL (25× too large). Always look it up. Never paste the example value.

**VWAP** (chooses histogram mode if `volumeProfile=true`, else typical-price):

```bash
python3 scripts/vwap.py --file market_history.json --tick-size <TICK_SIZE>
```

Output: `{vwap, mode, bars_used, total_volume, price_z_score}`.

**Market profile** (requires `volumeProfile=true`):

```bash
python3 scripts/profile.py --file market_history.json --tick-size <TICK_SIZE>
```

Output: `{poc, vah, val, value_area_pct, total_volume, levels_in_value_area, total_levels}`.

The optional `--value-area 0.70` is the default and matches CME convention. Lower values (e.g., `0.50`) give the tighter "developing value area."

**Bar delta + cumulative delta + order-flow imbalance** (no histogram or tick size required — reads `upVolume` / `downVolume` from the bar):

```bash
python3 scripts/delta.py --file market_history.json
```

Output: `{bars_used, total_up_volume, total_down_volume, net_delta, cumulative_delta_path, final_imbalance, bar_imbalance_path}`. The two `*_path` arrays are per-bar views. Feed them to a chart-render or a pattern detector.

**ATR + realized volatility + close z-score**:

```bash
python3 scripts/atr.py --file market_history.json --n 14
```

For intraday bars, pass `--periods-per-year` to match the bar count per trading year, so the annualized-vol output stays meaningful. Examples:

- Daily bars: `--periods-per-year 252` (default)
- 5-minute bars during RTH: 78 bars/day × 252 = `--periods-per-year 19656`
- 1-minute bars during RTH: 390 × 252 = `--periods-per-year 98280`

**Cross-symbol relative strength** (needs at least two symbol files):

```bash
python3 scripts/cross_symbol.py --symbol ES=es.json --symbol NQ=nq.json --symbol RTY=rty.json
```

Each `NAME=PATH` points to a saved `market_history` response. Output includes per-symbol change-today and pairwise spreads. This is **intra-day only**. Historical rolling correlation lives in `correlation-hedge`.

### 4. Narrate

Use `references/regime-narrative.md` to translate the numeric output into short, opinionated sentences. Rules of thumb:

- Lead with dollar / point values. Put R-multiples second, when there's a position context.
- Snap VWAP / POC to tick precision. Never report "7151.4328".
- State regime as fact, not forecast. Say "trading above VWAP"; not "headed higher".
- Never invent a baseline comparison. If no 20-day median exists, report the raw value and say so.

## Typical queries and their responses

- **"What's ES doing?"** → 5-minute bars with volumeProfile; run vwap.py + profile.py; narrate ("ES at 7151, inside value — VAL 7148, POC 7150, VAH 7154 — volume focused around open").
- **"Is ES volatile today?"** → Daily bars, 20-day lookback; atr.py with `--n 14`; narrate `realized_vol_annualized_pct` against the atr_n comparison.
- **"What's the delta on ES this morning?"** → Use 5-minute bars for the morning window. Run `delta.py`. Narrate `net_delta` and `final_imbalance`. Flag any bar in `bar_imbalance_path` with `|imbalance| > 0.4` as aggressive one-sided activity.
- **"How is ES doing vs NQ and RTY?"** → three `market_history` calls, saved to files, then run cross_symbol.py; narrate the largest `spread_pct`.
- **"Where's VWAP?"** → just vwap.py; report the number and the z-score narrative.

## Disambiguation

- vs `correlation-hedge`: this skill covers **intra-day** relative strength (who leads today). **Historical rolling correlation** across a lookback window lives in `correlation-hedge`.
- vs `chart-render`: this skill produces numbers and narrative. Chart-render draws them as a PNG.
- vs `trade-journal` / `trade-replay`: those skills look at the user's own trades. `market-context` is market-wide — no portfolio or fill data involved.

## Resource layout

- `scripts/vwap.py` — histogram-based VWAP with typical-price fallback
- `scripts/profile.py` — POC / VAH / VAL (default 70% volume area)
- `scripts/delta.py` — bar delta + cumulative delta + order-flow imbalance
- `scripts/atr.py` — ATR(N), realized-vol (annualized), close z-score
- `scripts/cross_symbol.py` — intra-day relative strength across N symbols
- `scripts/fixtures/` — a small synthetic `market_history` response for regression testing
- `references/histogram-offset.md` — the tick-offset convention. Load it when the user asks about histogram data or VWAP math.
- `references/regime-narrative.md` — output templates. Load it when you write narrative sentences.
