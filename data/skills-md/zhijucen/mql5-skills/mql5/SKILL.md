---
name: mql5
description: >
  MQL5 development skill for MetaTrader 5 Expert Advisors, Indicators, Scripts,
  and Services. Focus on positions, orders, indicators, ticks, bars, risk
  management, backtesting, and multi-instance MT5 operations. Includes
  programming book and API reference documentation.
license: MIT
compatibility: >
  Target: MetaTrader 5 platform. Language: MQL5 (C++-like syntax).
  File extensions: *.mq5 (source), *.mqh (headers).
  Run time: Windows native, Linux via Wine, macOS via Wine.
metadata:
  version: "0.1"
  focus-areas:
    - positions
    - orders
    - indicators
    - ticks
    - bars
    - risk-management
    - backtesting
---

# MQL5 Development Skill

Expert development skill for MetaTrader 5. Covers EA, Indicator, Script,
and Service creation with emphasis on trading operations, technical
indicators, multi-timeframe analysis, risk management, and backtesting
workflows. Detailed reference material, code templates, and deal-debug
methodology live outside this file (see §10 for the index).

## 1. MQL5 Fundamentals

### Language and File Types

MQL5 syntax is similar to C++ with domain-specific additions.
Source: `*.mq5` (programs), `*.mqh` (headers). Compiled output:
`*.ex5` (same name as source). Compiler: built into MetaEditor IDE.

### Program Types

| Type           | Purpose            | Key Handler    | Directory          |
|----------------|--------------------|----------------|--------------------|
| Expert Advisor | Automated trading  | `OnTick()`     | `MQL5/Experts/`    |
| Indicator      | Technical analysis | `OnCalculate()`| `MQL5/Indicators/` |
| Script         | One-shot execution | `OnStart()`    | `MQL5/Scripts/`    |
| Service        | Background task    | `OnStart()`/`OnTimer()` | `MQL5/Services/` |

### MQL5 Directory Structure

Default: Windows — `$env:USERPROFILE\AppData\Roaming\MetaQuotes\Terminal\$INSTANT_HEX\MQL5`;
Linux/Wine — `~/.wine/drive_c/Program Files/MetaTrader 5/MQL5/`.

Key subdirs: `Experts/`, `Indicators/`, `Scripts/`, `Services/`,
`Include/Trade/` (CTrade, PositionInfo), `Include/Indicators/`,
`Include/Expert/`, `Include/Generic/`, `Files/`, `Logs/`.

### Multi-Instance MT5

Multiple MT5 instances can run concurrently (e.g. one per demo
account, one per broker). Each has its own `MQL5/`. To distinguish:
`AccountInfoInteger(ACCOUNT_LOGIN)`, `ACCOUNT_NAME`, `ACCOUNT_SERVER`.
**Use Magic Number** to distinguish EA trades across instances on
the same symbol — each instance should own a unique magic.

### Code Style and Conventions

Naming (classes `C`+PascalCase, methods PascalCase, members `m_`+camelCase),
class structure (private→protected→public), and MQH declaration/definition
split: `references/quick-ref-code-style.md`.

## 2. Trading Operations

### Order vs Deal vs Position

- **Order**: instruction to buy/sell (Market or Pending).
- **Deal**: executed exchange (buy at Ask, sell at Bid).
- **Position**: current obligation (long or short).

Full API: `references/docs/19-trading/` (34 files, pattern
`0801-trading-ordercalcprofit.md`). For functions not listed below,
read the corresponding doc file.

### CTrade Class (Standard Library)

```mql5
#include <Trade\Trade.mqh>
CTrade trade;
trade.SetExpertMagicNumber(EA_MAGIC);
trade.SetMarginMode();
trade.SetTypeFillingBySymbol(Symbol());
trade.SetDeviationInPoints(Slippage);
```

Key methods: `PositionOpen`, `PositionClose`, `PositionModify`,
`PositionClosePartial`, `Buy`/`Sell`, `BuyLimit`/`BuyStop`/etc.,
`ResultRetcode` (always check after open), `ResultDeal`. Full setup
template: `assets/templates/ea-skeleton.mq5`.

### Order Execution Pattern

```mql5
double price = (signal == ORDER_TYPE_BUY)
    ? SymbolInfoDouble(_Symbol, SYMBOL_ASK)
    : SymbolInfoDouble(_Symbol, SYMBOL_BID);
trade.PositionOpen(_Symbol, signal, lotSize, price, sl, tp, "EA Signal");
if (trade.ResultRetcode() != TRADE_RETCODE_DONE)
    Print("Trade failed: ", trade.ResultRetcode());
```

### Hedging vs Netting

```mql5
bool IsHedging = ((ENUM_ACCOUNT_MARGIN_MODE)
    AccountInfoInteger(ACCOUNT_MARGIN_MODE)
    == ACCOUNT_MARGIN_MODE_RETAIL_HEDGING);
```

- **Hedging**: multiple positions per symbol; iterate `PositionsTotal()`
  + match Magic Number.
- **Netting**: one position per symbol; use `PositionSelect(_Symbol)`.

## 3. Indicators and Multi-Timeframe

### Built-in Indicator Handles

| Indicator        | Function                                            |
|-----------------|-----------------------------------------------------|
| Moving Average  | `iMA(_Symbol, PERIOD, period, 0, mode, price)`      |
| RSI             | `iRSI(_Symbol, PERIOD, period, PRICE_CLOSE)`        |
| MACD            | `iMACD(_Symbol, PERIOD, fast, slow, sig, price)`    |
| Bollinger Bands | `iBands(_Symbol, PERIOD, period, 0, dev, price)`    |
| ADX             | `iADX(_Symbol, PERIOD, period)`                     |

Full API in `references/docs/26-indicators/` (41 files, pattern
`0969-indicators-i<name>.md` — e.g. `iadx`, `iatr`, `ifractals`).
Read the doc file rather than guessing the API for indicators not
listed above.

### Reading Indicator Values

```mql5
double buffer[];
ArraySetAsSeries(buffer, true);
if (CopyBuffer(handle, 0, 0, 3, buffer) != 3) { Print("No data"); return; }
// buffer[0] = current bar, buffer[1] = previous bar
```

### New Bar Detection + MTF

```mql5
datetime lastBarTime = 0;
void OnTick() {
    if (iTime(_Symbol, _Period, 0) == lastBarTime) return;
    lastBarTime = iTime(_Symbol, _Period, 0);
    // New bar — run analysis here
}
```

For multi-timeframe (H4 trend filter on H1 entry), keep two handles
at different `PERIOD_*` and combine `CopyBuffer` reads per bar;
MTF snippet in `assets/templates/ea-skeleton.mq5`.

## 4. Ticks and Bars

### Timeseries Access

Index 0 = current (unfinished) bar; array is reverse-ordered.

```mql5
MqlRates rates[];
ArraySetAsSeries(rates, true);
CopyRates(_Symbol, _Period, 0, 100, rates);
// rates[0].open .high .low .close .tick_volume .time
```

### Key Functions

`CopyRates()` (bulk OHLCV), `CopyOpen/High/Low/Close()` (individual
price arrays), `CopyTime()`, `CopyBuffer()` (indicator), `iBars()`,
`iTime()`, `SymbolInfoTick()` (`tick.bid .ask .last .volume .time`).

## 5. Risk Management and Lot Sizing

### Core Concept: PointValue

`PointValue` = profit-currency for a **1-point** move on **1 lot**.
Foundation for all risk formulas. `SYMBOL_TRADE_TICK_VALUE` is per
**tick** (broker step); `PointValue` is per **point** (smallest unit).
For most Forex: `TickSize == Point`, so they coincide. `loss =
points × PointValue × Lots`. Full implementation (Forex/CFD/Futures/Stocks)
in `assets/templates/risk-helpers.mqh`.

### Three Risk Formulas (pick one)

| Dir | Inputs                          | Output        |
|-----|---------------------------------|---------------|
| **A** | SL distance in points         | SL price      |
| **B** | balance + risk% + **fixed lots** | SL price      |
| **C** | balance + risk% + SL price      | **lot size**  |

**CRITICAL** (B and C): when `SYMBOL_CURRENCY_PROFIT != ACCOUNT_CURRENCY`
(e.g. USDJPY: profit=JPY, account=USD), convert the risk amount via a
live FX rate. Skipping this makes risk 100×+ too small.
Implementation: `CalcSLFromRisk` / `CalcLotsFromSL` in
`assets/templates/risk-helpers.mqh`.

### Profit Verification

```mql5
double profit;
OrderCalcProfit(ORDER_TYPE_BUY, symbol, lots, openPrice, closePrice, profit);
// Manual (Forex/CFD): profit = (close-open) * ContractSize * Lots
// Manual (Futures):   profit = (close-open) * TickValue / TickSize * Lots
```

### 7 Risk Rules

1. Risk ≤ 1–2% per trade.
2. Use Direction B **or** C — not both inverted.
3. **Verify with `OrderCalcProfit`** before opening. Compute actual loss
   for the intended lot and confirm within risk budget.
4. `NormalizeDouble(price, SYMBOL_DIGITS)` for SL/TP.
5. SL distance ≥ `SYMBOL_TRADE_STOPS_LEVEL × Point`.
6. Normalize lots to `SYMBOL_VOLUME_STEP`, clamp to
   `[VOLUME_MIN, VOLUME_MAX]`. If `rawLots < minLot` → clamp inflates
   risk; **skip the trade**.
7. Profit ≠ account currency → convert via FX rate.

## 6. Backtesting and Optimization

### Strategy Tester

Built-in to MT5. Modes: **Single Test**, **Optimization** (genetic),
**Custom Criterion** (`OnTester()`). Single tests run HEADLESSLY via
`terminal64.exe /portable /config:<INI>` (`metatester64.exe` = remote agents only).

### CLI Automation — What Can / Cannot Be Automated

| Task                          | CLI? | How                                              |
|-------------------------------|:---:|--------------------------------------------------|
| Syntax check                  | ✅  | `wine MetaEditor64.exe /compile:"path" /log /s`  |
| Compile `.mq5 → .ex5`         | ✅  | `wine MetaEditor64.exe /compile:"path" /log`     |
| Single test (backtest)        | ✅  | `mql5_helper.py tester INI` (headless `/config:`) |
| Optimization (Grid/genetic)   | ✅  | `mql5_helper.py tester INI` (set `Optimization=1/2` in INI) |
| Parse tester / optimizer      | ✅  | `scripts/parse_tester_report.py` / `parse_optimizer_report.py` |

Wine/MetaEditor **exit 0 ≠ compilation success** — require fresh
`.ex5` and the `.log` next to the source (Pitfall #17, §8).

### Script CLI Conventions (mandatory)

```
{python|uv run} scripts/SCRIPT.py SUB_COMMAND INPUT_FILE [OPTIONS] [-o OUT]
```

Sub-command is the first non-flag token; `--json` / `-o` must follow
`SUB_COMMAND INPUT_FILE`. `-o OUTPUT_FILE` is optional; `--json`
controls encoding, not by file extension.

### `.ini` Parameter Format (Optimization)

Optimizable `input`: `value||start||step||stop||Y` per line, **field
order fixed** — moving `step` before `start` or omitting the trailing
`Y/N` silently disables the parameter; booleans/enums use `step=0`.
`string` inputs and `sinput` (static input, never optimized) use a
BARE `name=value`. Example: `assets/Anonymous.XAUUSD.M15.ini`.

### Backtesting Workflow

Code (OnInit/OnTick/OnDeinit, OnTester) → CLI compile + check →
`mql5_helper.py init-ini FILE.mq5` (INI skeleton listing ALL inputs) →
review dates/model → `mql5_helper.py tester INI -o OUTDIR`
(headless single test or optimization; report artifacts copied to OUTDIR) →
optimization → analyze → out-of-sample validation. Pitfalls + error
strings: `references/quick-ref-tester-automation.md`.

### Report Analysis — Tester (HTML → JSON via `parse_tester_report.py`)

Apply in order. Skipping the first means metrics can be GIGO.

1. **Data quality** — History Quality ≥ 95% real ticks; modelling =
   Every tick / Every tick based on real ticks. Never trust
   "Open prices only" for final eval.
2. **Profitability** — Profit Factor Good > 1.5 / Warning 1.0–1.5 /
   Bad < 1.0. **PF < 1.0 = guaranteed loss** — rework strategy, not params.
3. **Drawdown** — Max DD% Safe < 20% / Risky > 50% (≈100% = wiped).
   Check both Balance and Equity DD (Equity captures floating).
4. **Consecutive losses** — < 5 tolerable; > 8 = catastrophic under
   martingale / grid. Max consec loss $ < 2× deposit; > deposit = capital risk.
5. **Stop-out detection** — deal `comment` contains `so`. Always a
   critical bug (margin insufficient, force-closed before SL).
   Causes: SL too far, lots too large, risk > capacity, margin drain
   from concurrency. Fix lots / SL / concurrency.
6. **Time-window stability** — `windows --count N` slices the
   backtest into N equal windows; flags `▲2σ` (|z|≥2 on ≥1 metric),
   `■EXT` (|z|≥5), or `-`. **Picking N**: start with `N ≈
   backtest_days // 30`; if `N<6`, switch to `N ≈ backtest_days // 14`.
   Always run `N=1` first (cross-check; 4 of 7 exact, 3 documented
   approximations: Balance DD Rel%, Recovery Factor, Sharpe Ratio).
   Scoring semantics: `references/quick-ref-optimizer-analysis.md` §9.
7. **Deal-level debugging** — drill in via the 6-step methodology
   (pair deals → risk check → SL distance → re-entry → volume →
   monthly): `references/quick-ref-tester-deal-debug.md`. Use
   `analyze` for automation, `report --json` for raw queries.
8. **Market regime filters** — trend / order-block strategies
   degrade in chop. ADX(14) on a higher TF > threshold (typically 25)
   gates entries. Time-based filter skips worst-performing hours
   from monthly breakdown.

### Optimization Report Analysis (XML → JSON via `parse_optimizer_report.py`)

Output is a SpreadsheetML XML workbook (`ReportOptimizer-*.xml`,
LibreOffice Calc compatible); one row per parameter pass.
`<DocumentProperties> Title` (`EA SYMBOL,PERIOD YYYY.MM.DD-YYYY.MM.DD`)
encodes the strategy environment; the same field also carries
Deposit / Leverage / Server / MT5 build / run timestamp. Wrong demo
server, wrong leverage, or stale build invalidates the run.

#### The 5-Step Top-Down Analysis

1. **Environment card** (quick-ref §1): EA / symbol / period /
   date range / deposit / server / build — any wrong field
   invalidates the run.
2. **Orthogonality**: `actual` passes vs `expected_cartesian`.
   Mismatch = passes skipped, table incomplete, per-parameter
   means biased.
3. **Dead parameters** — highest-value step. Two signals:
   `parameter_effect[X].dead_param == true` (per-group mean Profit
   range < 1% of max); or `dead_boolean_params[X]` (bit-identical
   true/false groups on Profit/PF/RF/Trades — usually a code path
   that never triggers, e.g. news/calendar filters on a server
   that can't load news).
4. **Best-pass across multiple criteria**: Profit (return) / PF
   (edge per unit risk) / RF (return per max DD) / Custom
   (`OnTester()`). They usually agree on top-3, diverge on the
   tail — pick the pass in multiple top-5 lists **with Trades near
   the median** for statistical significance.
5. **Trade-count distribution**: `corr_trades_vs_profit < -0.3`
   means overtrading (more trades, less profit);
   `corr_trades_vs_equity_dd > 0.3` means more DD per trade.
   Range of 14 trades across 432 passes = parameters adjust
   entry/exit timing, not the core signal.

### Per-Pass Outlier Scan (`outliers`)

Per-pass z-score over the 8 perf metrics (Result, Profit, EP, PF,
RF, SR, Custom, Equity DD %). Trades excluded from the scan; used
only as a low-Trades filter. Two disjoint sets sorted by `--sort`
priority (default `R↓, EP↓, PF↓, RF↓, SR↓, P↓, DD↑, C↓, T↓`).
Full table + sigma guidance:
`references/quick-ref-optimizer-analysis.md` §9.

#### Failure-Set Analysis (`failures`)

Passes satisfying **any** of 6 absolute criteria (Profit<0, PF<1.0,
EP<0.1, Equity DD%>60, RF<1, SR<1.0). Thresholds NOT z-scored —
satisfying every criterion = deployment-grade on absolute terms.
Per parameter, `pct_of_global` > 50% on a single value = smoking
gun; drop it from the grid or fix as a fundamental EA bug. Output:
`references/quick-ref-optimizer-analysis.md` §10.

### News-Aware Backtesting (`#resource`)

MT5 tester has **no internet access** → `CalendarValueHistory()`
returns empty. Pattern from MQL5 article 22196: export calendar on
a live terminal → embed via `#resource` array.

1. Run `assets/mql5.com-artical-22196-MetaQuotes/22196-attaches/ExportCalendarForTester-S.mq5`
   on a live terminal → dual `.bin` per currency (values + events).
2. Embed in EA with two `#resource` pragmas (one per file).
3. `OnInit()` branches on `MQLInfoInteger(MQL_TESTER)`: tester
   uses the resource; live calls `CalendarValueHistory()`.

`#resource` bakes data into `.ex5` at compile time — replacing a
`.bin` requires F7 recompile. Pitfalls (sizeof mismatch error 308,
build-order trap, char→string conversion, dual struct drift,
hermetic tester mode): `references/quick-ref-mql5-economic-calendar.md`.

### Strategy Iteration Workflow

When a strategy component underperforms and needs rollback /
iteration, follow a structured process. **Governing Invariant**:
every hypothesis must be compared against a reproducible baseline
in a **separate validation stage** — never combine rollback + new
signal + new order type in one unmeasured change.

**Rollback Checklist** (verify each layer): (1) Configuration;
(2) Lifecycle hooks; (3) Modules; (4) Order entry (direction +
price-relation); (5) Optimization plumbing; (6) Documentation
(reason, scope, consequences, user test gate).

**Hypothesis isolation**: only start the next experiment after
the user has confirmed the rollback baseline. Otherwise
performance changes cannot be attributed.

### Analysis Pitfalls

- **Rename-vs-Behaviour Trap**: a skill/script diff may be a real
  behaviour change **or** a cosmetic refactor. Don't repackage cosmetic
  diffs as behaviour changes. Identifier/comment-only differences =
  no behaviour change; confirm with the user before "porting".
- **Date-Only String Truncation**: storing window boundaries as
  `strftime("%Y.%m.%d")` loses sub-day precision. For non-whole-day
  windows (e.g. N=18 of 548 days = 30.44-day), `strptime` re-parses
  drift by up to ½ day. Fix: store `window_seconds` once; readers use it.
- **Window-Clipped vs Raw Trade Duration**: idle accounting uses
  `max(open, t_start) → min(close, t_end)`; per-trade Min/Max/Avg
  holding uses `close_time - open_time`. MT5's "Maximal position
  holding time" is the trade's full lifetime, NOT window-clipped.
  Window-clipping MaxHold produces a silent N=1 semantic bug.
- **Idle-Gap Decomposition**: for `MinIdle/MaxIdle/AvgIdle` with
  multi-position EAs (grid/hedging) the "gap between consecutive
  trades" formula is WRONG. Use sweep-line merge + complement.
- **Self-Test Before Inventing Diagnostics**: when a user reports
  a behaviour bug, check pre-existing diagnostic recipes in
  `references/quick-ref-*` first. Don't re-derive a known signature.

## 7. Event Handlers Reference

| Handler                | When Called             | Use Case                       |
|------------------------|-------------------------|--------------------------------|
| `OnInit()`             | EA/indicator starts     | Init handles, variables        |
| `OnDeinit()`           | EA/indicator stops      | Cleanup, release handles       |
| `OnTick()`             | New tick                | EA main logic                  |
| `OnTimer()`            | Timer event             | Periodic operations           |
| `OnTrade()`            | Trade event             | React to trade changes         |
| `OnTradeTransaction()` | Trade transaction       | Detailed trade tracking        |
| `OnChartEvent()`       | Chart interaction       | GUI buttons, objects           |
| `OnCalculate()`        | Indicator calculation   | Indicator main logic           |
| `OnTester()`           | Test complete           | Custom optimization criterion  |
| `OnTesterInit()`       | Optimization start      | Setup for optimization         |
| `OnTesterPass()`       | Each optimization pass  | Log intermediate results       |

## 8. Common Pitfalls

### General

1. Always check `ResultRetcode()` after `PositionOpen()` (success ≠ execution).
2. `SetExpertMagicNumber()` distinguishes your EA's trades.
3. `NormalizeDouble(price, SYMBOL_DIGITS)` on every SL/TP.
4. `Bars() > N` before trading (enough history).
5. `ArraySetAsSeries(true)` for timeseries (index 0 = latest).
6. Release handles in `OnDeinit()` with `IndicatorRelease()`.
7. Don't trade on `OnInit()` — wait for first `OnTick()`.
8. Hedging: iterate positions; netting: `PositionSelect`.
9. Spread: `SymbolInfoInteger(_Symbol, SYMBOL_SPREAD)`.
10. Tester `EventSetTimer()` in `OnInit()` (no hardcoded delays).

### SL/TP and Risk Calculation

11. **`PointValue ≠ TICK_VALUE`** — see §5.
12. **TickSize ≠ Point** — match formula to `SYMBOL_TRADE_CALC_MODE`.
    Forex/CFD: `loss = Δprice × ContractSize × Lots`. Futures:
    `loss = Δprice × TickValue/TickSize × Lots`.
13. **Profit ≠ Account currency** — convert via `FindFXRate` first
    (e.g. USDJPY: profit=JPY, account=USD). Skip → risk 100×+ too small.
14. **`NormalizeDouble` rounding** — verify with `OrderCalcProfit`
    (~0.01–0.02% deviation acceptable).
15. **Lot-step quantisation** — `MathFloor(rawLots / lotStep) * lotStep`
    leaves residual risk; verify final loss, don't trust the formula.
16. **`STOPS_LEVEL`** — SL ≥ `SYMBOL_TRADE_STOPS_LEVEL × Point`. If
    `stops_level ≤ 0` use a safety margin (~150 points).
17. **Wine exit-code 0 ≠ success** — require fresh `.ex5` + `.log`
    next to source. A helper that deploys to a different terminal
    tree compiles a different copy than the one you read.
18. **Verify deployed path** — after `mql5_helper.py deploy`, check
    the deployed `MQL5/` path + artifact timestamps.

## 9. EA Skeleton (template)

See `assets/templates/ea-skeleton.mq5` — minimal Expert Advisor
scaffold that includes `OnInit`/`OnTick`/`OnDeinit`/`OnTester`
lifecycle, `CTrade` setup (magic, margin mode, filling, slippage),
hedging vs netting detection, new-bar check + MTF pattern, risk-based
sizing using `risk-helpers.mqh`, and retcode checking on `PositionOpen`.

Copy to `MQL5/Experts/` (under your terminal tree), `#include
"risk-helpers.mqh"` with the path adjusted to your project layout
(see file header), then extend. Indicator/Script skeletons: copy
`ea-skeleton.mq5`, change `#property` + `OnInit` → `OnCalculate` or
`OnStart`, drop the `CTrade` setup.

## 10. References

- **Templates** (`assets/templates/`):
  - `ea-skeleton.mq5` — minimal EA scaffold (CTrade + risk-based SL/TP + magic isolation).
  - `risk-helpers.mqh` — `PointValue`, `FindFXRate`, `CalcSLFromRisk`, `CalcLotsFromSL`.
  - `assets/mql5.com-artical-22196-MetaQuotes/` — article 22196 source (export + validation EAs). `outputs/` gitignored.
- **Quick-refs** (`references/`):
  - `quick-ref-mql5-economic-calendar.md` — `MqlCalendarValue` 128-byte layout, `#resource` pitfalls.
  - `quick-ref-shadow-parameter-optimization.md` — shadow parameter compression (combo index).
  - `quick-ref-tester-deal-debug.md` — 6-step deal-level methodology for tester HTML.
  - `quick-ref-tester-automation.md` — headless `tester` recipe, pitfall list, Model enum.
  - `quick-ref-optimizer-analysis.md` — env-card, dead params, `outliers`, `failures`.
- **Book / API** (`references/`): `book/` (581-pg learning path; chapters `00-intro/` … `06-advanced/`); `docs/` (4135-pg API; top folders `19-trading/`, `16-series/`, `26-indicators/`, `24-customind/`, `13-event-handlers/`, `34-standardlibrary/`, `01-constants/`); `symbol-spec/specs-XAUUSD.csv`, `specs-USDJPY.csv`.
- **Scripts** (`scripts/`): `parse_tester_report.py` (`report`/`analyze`/`windows`); `parse_optimizer_report.py` (`report`/`analyze`/`outliers`/`failures`); `parse_mql_calendar_bin.py` (positional PATH); `verify_sl_tp_formulas.py verify [SYMBOL ...]`; `mql5_helper.py` (`compile`/`check`/`deploy`/`status`/`list`/`init-ini`/`tester`).
- **External**: [MQL5 Reference](https://www.mql5.com/en/docs), [MQL5 Book](https://www.mql5.com/en/book), [Strategy Tester Guide](https://www.mql5.com/en/terminal/strategytester).
