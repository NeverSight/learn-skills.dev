---
name: mql5-ta
description: Technical analysis for MQL5 development using TA-Lib in Python. Aligns MT5-exported quote CSVs (detects mixed/hidden timeframes in historical data), maps MQL5 indicator families (iMA, iMACD, iATR, ...) to TA-Lib functions with interface-difference notes, and computes indicators on OHLCV series.
---

# MQL5 Technical Analysis (TA-Lib)

Compute technical indicators on MT5 quote data using the Python `TA-Lib`
library, with a mapping layer that relates every MQL5 built-in indicator
(`iMA`, `iMACD`, `iATR`, ...) to its TA-Lib counterpart — or documents why
no counterpart exists.

## When to use

- The user provides MT5-exported quote files and wants indicators computed
  in Python (TA-Lib) rather than inside MQL5.
- The user asks how an MQL5 indicator corresponds to a TA-Lib function
  (parameters, outputs, boundary behaviour).
- The user's quote data must be aligned to a single timeframe before any
  indicator work.

## Step 1 — Load & align quotes

MT5 exports are nominally TSV with bracketed headers:

```
<DATE>\t<TIME>\t<OPEN>\t<HIGH>\t<LOW>\t<CLOSE>\t<TICKVOL>\t<VOL>\t<SPREAD>
2024.01.02	01:00:00	2065.46	2066.49	2063.23	2063.70	2329	0	0
```

Be flexible: delimiters may be tab/comma/semicolon, headers may be plain
(`DATE`, `time`, `Close`), and `SPREAD`/`VOL` columns may be absent.

### The hidden-timeframe problem

Quote vendors backfill **old history at a coarser timeframe than the file's
nominal timeframe** — e.g. an "M1" file whose months-old half is actually
H1-spaced bars. This is invisible to the eye and silently corrupts every
indicator. Always run alignment before computing anything:

```bash
# report only (auto-detect nominal TF and coarse segments)
uv run python scripts/align_quotes.py <quotes.csv>

# target M1: coarse segments cannot be synthesized upward -> dropped
uv run python scripts/align_quotes.py <quotes.csv> --tf M1 --out aligned.tsv

# target H1 (>= coarsest segment): aggregate the WHOLE file, coarse part fully used
uv run python scripts/align_quotes.py <quotes.csv> --tf H1 --out aligned.tsv
```

Alignment rules (in this order):

1. Parse flexibly, merge date+time into one datetime, sort **ascending by
   time**, drop duplicate timestamps.
2. Infer each bar's spacing; classify spacing > 6 h as a session gap
   (overnight maintenance / weekend) — gaps are normal, do NOT treat them
   as data errors and do NOT fill them.
3. When several timeframes are present (or multiple files are combined):
   - If a segment's period, after any permitted change, is still coarser
     than the target timeframe → **remove** those records.
   - If synthesis (aggregating finer bars) makes the target equal to or
     coarser than the anomalous segment's period → **fully utilize** that
     segment (aggregate the whole series to the target).
4. Validate: `high >= max(open, close)`, `low <= min(open, close)`,
   monotonic timestamps, no duplicates. Report violations; never silently fix.

Reference asset: `assets/quotes/abnormals/XAUUSD_M1_202401020100_202403012354.csv`
is a real M1 file whose 2024-01-02..2024-02-23 portion is actually H1-spaced
(`SPREAD` also drops to 0 there). Use it as the regression case for any
alignment change.

### Volume caveat

FX/CFD quotes have `<VOL>` (real volume) = 0. For volume-based indicators
(MFI, OBV, AD) use `<TICKVOL>` and state the limitation in the output.

## Step 2 — Compute indicators with TA-Lib

Use the **Function API** (not the Abstract API) throughout:

```python
import talib
sma = talib.SMA(df["<CLOSE>"], timeperiod=10)
macd, signal, hist = talib.MACD(df["<CLOSE>"], 12, 26, 9)
```

Key semantics (see `references/docs-talib/func.md`):

- Outputs are aligned with the input; the first `lookback` values are `NaN`.
  Lookback can exceed `timeperiod` (e.g. `RSI(14)` needs 15 observations).
- Prices are plain arrays — the "applied price" of MQL5 is expressed by
  choosing the column (`<CLOSE>`, `(h+l)/2`, `hlc3`, ...).
- TA-Lib requires the C library installed: `references/docs-talib/install.md`.

## Step 3 — Map MQL5 indicators to TA-Lib

Consult `references/indicator-mappings/` (start at `0000-index.md` —
series direction, lookback/NaN, applied-price column table, MA-method
table, coverage marks ✅/⚠️/✗):

- `01-trend.md` — iMA, iBands, iADX(Wilder), iSAR, iStdDev, iDEMA/iTEMA,
  iTRIX, iAMA/iFrAMA/iVIDyA, iEnvelopes, iIchimoku, iAlligator
- `02-oscillators.md` — iRSI, iMACD/iOsMA, iStochastic, iCCI, iATR,
  iMomentum (name trap → `ROC`), iWPR, iBulls/iBears Power, ...
- `03-volumes.md` — iAD, iMFI, iOBV, iChaikin (≡ `ADOSC`), iBWMFI
- `04-bill-williams.md` — iAC, iAO, iAlligator, iFractals, iGator (all compose)
- `05-talib-only.md` — TA-Lib functions with no MQL5 native counterpart
  (61 CDL* patterns, HT_* cycle family, stat/math functions)

Three coverage classes:

1. **Same-name counterparts** with differences flagged — e.g. MQL5
   `iMomentum` is percentage change (→ TA-Lib `ROC`, not `MOM`); MQL5 MACD
   signal line is SMA-smoothed while TA-Lib uses EMA; MQL5 MACD has no
   histogram buffer (TA-Lib `macd_hist` ≡ MQL5 `iOsMA`); MQL5 `iADX`
   differs from `talib.ADX` — use `iADXWilder` for parity.
2. **MQL5-only indicators** (iAlligator, iFractals, iIchimoku, iAC/iAO,
   iBears/iBulls Power, iRVI, iDeMarker, iForce, iFrAMA, iVIDyA, iBWMFI)
   — compose from primitives; recipes in the mapping files.
3. **TA-Lib-only indicators** (CDL* patterns, HT_* transforms, statistic
   and math functions) — use TA-Lib directly.

Also mind the **index-direction** conversion: TA-Lib output is index 0 =
oldest; MQL5 `CopyBuffer` is (by default) as-series, index 0 = newest.

## Step 4 — Verify numeric parity with MQL5

Mapping notes claim which indicators agree; `scripts/parity_check.py`
proves it against real MQL5 output:

1. Run `assets/mql5-side/TAParity-S.mq5` once in a live terminal
   (drag onto any chart; symbol/timeframe come from the script inputs).
   It writes `MQL5/Files/ta_parity_<SYMBOL>_<TF>.csv`: the last 1000 bars
   **plus** MQL5 values of 17 indicator/buffer pairs, ascending by time.
2. Compare:

```bash
uv run python scripts/parity_check.py ~/.wine/drive_c/.../MQL5/Files/ta_parity_XAUUSD_M1.csv
uv run python scripts/parity_check.py --selftest   # checker self-test, no MT5 needed
```

Verdicts: `PASS` (identical within 1e-6 after the `BURN_IN = 250`-bar
head — history-seeded indicators need warm-up, see 0000-index.md),
`EXPECTED_DIFF` (documented difference), `FAIL` (undocumented mismatch).
Verified 18/18 OK against a live XAUUSD M1 export. Findings baked into
the parity recipes: **MQL5 `iATR` = SMA of True Range** (not Wilder) and
**`iStochastic` smooths numerator/denominator separately** (not SMA of
raw %K) — both differ from TA-Lib defaults; recipes in
`references/indicator-mappings/02-oscillators.md`.

## Assets

- `assets/examples/using_talib_examples.py` — Function-API examples for
  all four classes (same-name / traps / MQL5-only compose / TA-Lib-only).
- `assets/mql5-side/TAParity-S.mq5` — live-terminal export for parity
  checks (bars + MQL5 indicator values in one CSV).
- `scripts/align_quotes.py` — quote loading, mixed-TF detection,
  alignment (Step 1).
- `scripts/parity_check.py` — MQL5 ↔ TA-Lib numeric parity checker (Step 4).
- `assets/quotes/` — clean XAUUSD M1/M15 samples; `assets/quotes/abnormals/`
  — mixed-timeframe regression file (see Step 1).

## References

- `references/docs-talib/` — TA-Lib documentation (function API, per-group
  function reference).
- `references/indicator-mappings/` — MQL5 ↔ TA-Lib mapping tables.
