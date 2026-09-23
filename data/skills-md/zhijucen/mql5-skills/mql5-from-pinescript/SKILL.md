---
name: mql5-from-pinescript
description: >
  Port TradingView Pine Script indicators to MQL5. Fetch open-source Pine
  via the pine-facade endpoint (no login/browser), map Pine constructs
  (offsets, fill, plotshape, request.security, alertcondition, var-state)
  onto MQL5 buffers/chart objects with a shift-invariance + closed-bar
  state-machine model, compile via mql5_helper, and record every deviation.
license: MIT
metadata:
  version: "0.1"
  ports:
    - 0001-modern-ichimoku-cloud
    - 0002-adaptive-decycler-supertrend
    - 0003-directional-kernel-filter
    - 0004-supertrend-regime-confluence
    - 0005-macd-pullback-sniper
    - 0006-aurora-kama
---

# Pine Script → MQL5 Porting Skill

Turn an open-source TradingView Pine indicator into an MQL5 indicator
(`.mq5`, chart window or subwindow) with an explicit, recorded fidelity
contract. Ports live in `assets/mql5/`; the fetched Pine original is kept
verbatim in `assets/pine-scripts/` as the fixed source asset.

## When to use

- User points at a TradingView script URL and wants it in MQL5/MT5.
- A Pine port needs review: fidelity check, deviation audit, re-compile.
- deciding whether a script is portable at all (open-source? plots only?
  drawing-heavy? repainting strategies are out of scope).

Out of scope: closed-source scripts (masked) — ask the user for the Pine
source; never decompile or screenshot-transcribe. Pine *strategies*
(`strategy.*`, order simulation) port to an **EA** only after the user
asks for trading logic; this skill's default target is indicators.

## Step 1 — Fetch the Pine source (open-source first)

```bash
# writes the verbatim source + prints metadata
python skills/mql5-from-pinescript/scripts/extract_pine.py fetch \
  "https://www.tradingview.com/script/<id>-<slug>/" \
  -o skills/mql5-from-pinescript/assets/pine-scripts/<name>.pine

# later: prove the asset still matches the published source
python .../extract_pine.py fetch "<url>" --check assets/pine-scripts/<name>.pine
```

How it works: page HTML embeds `"script_id_part":"PUB;<hex>"` →
`https://pine-facade.tradingview.com/pine-facade/get/PUB%3B<hex>/1`
returns JSON with `source`, `scriptAccess`, `version`.
(`scriptAccess != "open_no_auth"` → warn, source may be masked.)

**Never** copy from the rendered code viewer: it renders spaces as
U+00A0 and silently corrupts the file (this happened — see
`assets/pine-scripts/PROVENANCE.md`). Also record provenance (URL, id,
version, fetch date, normalization) in a `PROVENANCE.md` next to the
asset.

## Step 2 — Triage before writing code

Read the whole Pine file once. Classify every construct:

| Class | Examples | Port strategy |
|-------|----------|---------------|
| Direct | `plot`, math, `input.*`, crossovers | buffers + `input` (mapping table below) |
| Shifted plot | `offset=±k` | value remap at write time, EMPTY slots where data doesn't exist yet |
| Fill | `fill()` | `DRAW_FILLING` (only 2 dynamic colors — see D1 pattern) |
| Shapes/labels/tables | `plotshape`, `label`, `table` | `DRAW_ARROW` / `OBJ_TEXT` / `OBJ_LABEL` grid |
| Background | `bgcolor` | impossible → corner readout, record deviation |
| MTF | `request.security` | hand-built HTF series + closed-bar margin |
| State | `var`, `barstate.isconfirmed` | one state class + closed-bar state machine |
| Alerts | `alertcondition` | `Alert()` on realtime-closed bars only |
| Strategy orders | `strategy.entry/exit` | out of scope (EA, ask user) |

Estimate object counts (`line`/`label`/`table` creations): every Pine
object becomes a chart object — cap them (FIFO) or drop the feature and
record it.

## Step 3 — Apply the mapping

Full table + rules: `references/pine-to-mql5.md`. When a construct's
semantics are unclear, consult the curated excerpts in
`references/pine-script-docs/` (manual pages + API entries actually
used by ports — see its README) before guessing. The four rules that
decide correctness:

1. **Shift-invariance** — displayed values are intrinsic per bar; compute
   once, let MT5's buffer shifting carry them. Refresh only index 0 (per
   tick) and slots whose supplier bar was just born.
2. **Closed-bar state machine** — `var`/`isconfirmed` logic runs exactly
   once per closed bar, chronologically, guarded by
   `m_lastProcessedTime`; bulk backfill on the first call.
3. **Realtime-only alerts** — backfill accumulates, never alerts.
4. **ATR parity** — Pine `ta.atr` is Wilder RMA; MQL5 `iATR` is SMA of
   TR. Compute RMA inline; never use `iATR` when the port must match TV.

## Step 4 — Write the `.mq5`

- Target path: `skills/mql5-from-pinescript/assets/mql5/<Name>.mq5`.
- Follow the MQL5 code style (`skills/mql5/references/quick-ref-code-style.md`):
  PascalCase functions/methods, `C`+PascalCase classes, `m_`+camelCase
  members, ALL_CAPS constants, K&R braces, 4-space indent.
- One state class for `var` state (members reset in `OnInit`, objects
  deleted in `OnDeinit` via `ObjectsDeleteAll(chart, prefix)`); free
  functions for pure math (blend, percentile, RMA, bounds-checked
  highest/lowest).
- Every input mirrors a Pine input 1:1 (same default!) under an
  `input group` / `[Group]` comment matching Pine's `group = ...`.
- Header comment block: port number, Pine source path, deviations
  summary (D-numbers from the port record).

## Step 5 — Compile & verify

```bash
python skills/mql5/scripts/mql5_helper.py check  assets/mql5/<Name>.mq5
python skills/mql5/scripts/mql5_helper.py compile assets/mql5/<Name>.mq5
```

Wine exit 0 ≠ success: require a fresh `.ex5` + `.log` next to the source
(Pitfall #17 in `skills/mql5/SKILL.md`). Then run the checklist in
`references/pine-to-mql5.md` §5 — the two invariants that catch most
port bugs:

- **idempotence**: no new bar ⇒ no buffer/object changes;
- **no repaint**: a closed bar's values/objects never change afterwards.

## Step 6 — Record the port

Create `references/ports/NNNN-<name>.md` (zero-padded, next free number)
with: source/port/provenance table, faithful list, ATR/semantics
decisions, **numbered deviations D1…Dn (mandatory, even when empty)**,
and open verification tasks. Register the port id in this SKILL.md's
`metadata.ports`.

## Layout

```
skills/mql5-from-pinescript/
├── SKILL.md
├── scripts/
│   ├── extract_pine.py            # pine-facade fetch/check CLI
│   └── fetch_pine_docs.py         # manual-page excerpt fetcher
├── references/
│   ├── pine-to-mql5.md            # construct mapping + rules + checklist
│   ├── ports/0001…0006-*.md       # port records (D-numbered deviations)
│   └── pine-script-docs/          # curated Pine docs: 14 manual pages +
│                                  #   6 API-reference excerpt files (README=index)
└── assets/
    ├── pine-scripts/*.pine        # verbatim fixed sources (+PROVENANCE.md)
    ├── mql5/*.mq5                 # ports 0001–0003 indicators, 0004–0006 EAs
    │                              #   (+ strategy-common.mqh shared plumbing)
    └── mql5-side/                 # tester INIs + BufferDump parity harness
```

## Current ports

- **0001** Modern Ichimoku Cloud [GBB] → `assets/mql5/ModernIchimokuCloud.mq5`
  (Layers 0–4: five lines, normalised geometry grades, qualified signals,
  flat levels, HTF readout + stats table + alerts; 10 documented
  deviations — start review at `references/ports/0001-modern-ichimoku-cloud.md`).
- **0002** Adaptive Decycler Supertrend [SchizoQuant] →
  `assets/mql5/AdaptiveDecyclerSupertrend.mq5`
  (adaptive Ehlers decycler + residual-RMS envelope + persistent trail
  regime + flip signals; MPL-2.0, 6 deviations D1–D6 —
  `references/ports/0002-adaptive-decycler-supertrend.md`).
- **0003** Directional Kernel Filter [BackQuant] →
  `assets/mql5/DirectionalKernelFilter.mq5`
  (Gaussian base kernel + directional re-weighting, fast/slow trend
  lines + ribbon + 4 diagnostics; Wilder-ATR normalisation; MPL-2.0,
  6 deviations D1–D6 — `references/ports/0003-directional-kernel-filter.md`).

Both MPL-2.0 indicator ports keep the original copyright/license
header in the `.mq5` (file-level copyleft).

### Strategy ports (= EAs, ports 0004-0006)

Chosen from `?script_type=strategies` (all `open_no_auth`), each with a
tester INI that follows the **author's recommended instrument**:

- **0004** SuperTrend Regime Confluence [DefinedEdge] →
  `assets/mql5/SuperTrendRegimeConfluence-EA.mq5` — regime-adaptive
  SuperTrend +5-factor confluence score; **BTCUSDT ·4H**
  (`assets/mql5-side/0004-supertrend-regime-confluence.ini`); MPL-2.0;
 8 deviations D1-D8.
- **0005** MACD Pullback Sniper [blitz_locked] →
  `assets/mql5/MACDPullbackSniper-EA.mq5` — MACD cross gated by
  EMA200/zero-line/ADX, ATR stop +2R; trending **1H/4H/Daily**, sizing
  fits crypto/stocks → INI **BTCUSD · H4**; MPL-2.0; D1-D6.
- **0006** Aurora KAMA Trend [blitz_locked] →
  `assets/mql5/AuroraKamaTrend-EA.mq5` — KAMA slope persistence +
  delayed trailing stop; author: **DAILY BTCUSD/ES/SPY/QQQ** → INI
  **BTCUSD · D1**; **no license in source** (see PROVENANCE); D0-D7.

Shared EA plumbing: `assets/mql5/strategy-common.mqh` (closed-bar
series backfill, Pine-faithful EMA/RMA/SMA/ADX states, next-bar-open
bracket entries with gap/stop handling, risk/notional sizing, markers).
Execution model and deviations live in each port record.
