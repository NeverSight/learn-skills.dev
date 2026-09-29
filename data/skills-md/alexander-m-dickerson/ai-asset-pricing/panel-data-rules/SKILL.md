---
name: panel-data-rules
description: "Rules and gotchas for CRSP, Compustat, and financial panel data: safe lagging/leading with date gap checks, look-ahead bias prevention, CCM linking, book equity construction, and missing value conventions. Auto-apply when working with CRSP, Compustat, or financial panel data."
---

# Financial Panel Data Rules

Apply these rules whenever writing code that manipulates CRSP, Compustat, OptionMetrics, or any financial panel data. These are hard-won lessons — violating them causes silent data errors.

## Rule 1: Safe Lagging/Leading (MANDATORY)

**Every `groupby().shift()` and `.diff()` MUST be followed by a date gap check.** Data is rarely contiguous — missing quarters, fiscal year changes, and delistings create gaps. A bare `shift(1)` will silently pair non-adjacent observations.

After any shift(k), auto-insert this validation:
```python
df["_date_shifted"] = df.groupby(id_col)[date_col].shift(k)
day_gap = (df[date_col] - df["_date_shifted"]).dt.days
df.loc[(day_gap > max_gap) | (day_gap < min_gap), shifted_col] = np.nan
df.drop(columns=["_date_shifted"], inplace=True)
```

**Thresholds by data source** (validated against real WRDS data):

| Source | shift(1) max gap | shift(1) min gap | Notes |
|--------|------------------|------------------|-------|
| CRSP `msf`/`msf_v2` (month-end normalized) | 31 days | 28 days | 2.26M obs: max gap = 31 days exactly (v2: `mthcaldt`) |
| CRSP `msf`/`msf_v2` (raw trading dates) | 33 days | 28 days | Raw dates vary by last trading day |
| Compustat `fundq` | 100 days | 80 days | 99.89% in [90,92]; >100 = missing quarter |
| Compustat `funda` | 380 days | 350 days | <350 = FYE change (correctly flagged) |
| CRSP `dsf`/`dsf_v2` | 5 days | 0 days | Weekends/holidays (v2: `dlycaldt`) |

For shift(k): `max_gap = k * single_max`, `min_gap = k * single_min`.

**Infer frequency from data source** (table name, column names). Columns ending in `q` (ibq, atq, seqq) → quarterly. If source unknown, ask the user.

**CRSP month-end normalization (do this FIRST, before any gap checks or merges):**
```python
df["date"] = df["date"].dt.to_period("M").dt.to_timestamp("M")
```
This converts raw trading dates to calendar month-end. Required for: (1) gap checks to use the 31-day threshold, (2) matching CRSP to Compustat/JKP data, (3) consistent date joins across datasets.

## Rule 2: Accounting Data Timing (Compustat Only)

**Does NOT apply to JKP/Global Factor Data** — JKP already has point-in-time alignment built in.

- **Annual:** Available 4 months after fiscal year end: `datadate + DateOffset(months=4)`
- **Quarterly earnings (IBQ, Roe, dRoe):** Available after RDQ; if RDQ missing, fallback to `datadate + DateOffset(months=4)`. RDQ timing is specific to earnings/income variables.
- **Staleness filter:** Ask the user before applying. Some methodologies set earnings variables to NaN if fiscal quarter end is >6 months before panel date.
- **merge_asof staleness:** `direction='backward'` has **no max-age limit** — it will match data from years ago if nothing newer exists. In the BM battle test, some stocks carried BE data 11+ years old. Consider capping staleness (e.g., 18-24 months for annual signals), but ask the user first.
- **Compustat required filters:** Every `comp.funda`/`comp.fundq` query MUST include `indfmt='INDL' AND datafmt='STD' AND popsrc='D' AND consol='C'`. Omitting these creates duplicate gvkey-datadate rows silently.
- **merge_asof pattern:**
  ```python
  # CORRECT — sort by ON key only (hard requirement)
  left = left.sort_values('date').reset_index(drop=True)
  right = right.sort_values('date').reset_index(drop=True)
  pd.merge_asof(left, right, by='gvkey', on='date', direction='backward')
  ```
  Sorting by `[gvkey, date]` raises `ValueError: left keys must be sorted` because dates restart at each new gvkey, breaking global monotonicity.

## Rule 3: Panel Identifiers & CCM Linking

**ID columns:**
| Context | Primary ID | Group-by for shift/diff |
|---------|-----------|------------------------|
| CRSP only | `permno` | `permno` |
| Compustat only | `gvkey` | `gvkey` |
| Merged CRSP-Compustat | `permno` | `permno` |

**CCM linking:**
- Join on `permno`, filter `linktype IN ('LC','LU')`, filter `date >= linkdt AND date <= linkenddt`
- **SQL column name:** CCM table column is `lpermno` (double precision), not `permno`. Always alias: `l.lpermno::int AS permno`
- Set null `linkenddt` to `'9999-12-31'` sentinel before filtering
- **Pandas gotcha:** `pd.to_datetime('9999-12-31')` overflows nanosecond timestamps. Replace sentinel with `'2099-12-31'` before converting: `ccm["linkenddt"] = ccm["linkenddt"].astype(str).str.replace("9999-12-31", "2099-12-31")`
- Validated: zero duplicate (permno, date) with linktype LC/LU filter

**Always assert no duplicates after merge:**
```python
assert not df.duplicated(subset=['permno','date']).any()
```

**Multi-class firms:** Firms with multiple PERMNOs per GVKEY exist (2-4 share classes). For firm-level ME: `groupby(['gvkey','date'])['me'].transform('sum')`.

## Rule 4: Stock Universe Filters — ALWAYS ASK USER

Never apply filters by default. Present options:
- SHRCD in (10,11) — common stocks
- EXCHCD in (1,2,3) — NYSE, AMEX, NASDAQ
- SIC 6000-6999 — financials
- BE > 0, price/mcap minimums

v2 equivalents (string codes):
- Common stock: `sharetype='NS' AND securitytype='EQTY' AND securitysubtype='COM'`
- US incorporated: `usincflg='Y'`
- Major exchanges: `primaryexch IN ('N','A','Q')`
- Active: `tradingstatusflg='A'`

## Rule 5: Missing Values (Compustat-Specific)

**Fill with 0 (standard convention):**

| Column | Table | Reason |
|--------|-------|--------|
| `txditc`, `txditcq` | funda/fundq | Deferred taxes — missing = zero |
| `xrd` | funda | R&D — missing = no R&D |
| `drc`, `drlt` | funda | Deferred revenue — missing = zero |
| `dltt`, `dlc` | funda | Debt — missing in ratio = no debt |
| `dvpsxq` | fundq | Dividends per share — missing = no dividend |
| `rect`, `invt`, `xpp`, `ap`, `xacc` | funda | Working capital — missing CHANGE = 0 |

**Set to NaN:** Ratios with AT ≤ 0 or BEQ ≤ 0 denominators.

## Rule 6: Book Equity Hierarchies

**Annual BE (Davis-Fama-French 2000):**
```
SHE = SEQ → (CEQ + PSTK) → (AT - LT)
PS  = PSTKRV → PSTKL → PSTK
BE  = SHE + TXDITC(fillna 0) - PS(fillna 0)
```

**Quarterly BEQ:**
```
SHEQ = SEQQ → (CEQQ + PSTKQ) → (ATQ - LTQ)
PSQ  = PSTKRQ → PSTKQ          ← PSTKRQ first!
BEQ  = SHEQ + TXDITCQ(fillna 0) - PSQ(fillna 0)
```

**Q4 supplement:** If FQTR == 4 and BEQ missing, use annual BE from matching FYEARQ.

## Rule 7: Winsorization — ASK USER FIRST

Do NOT winsorize by default. Confirm: whether to winsorize, which variables, cutoffs (1/99 standard), cross-sectional by month vs pooled.

Standard pattern when confirmed:
```python
def winsorize_by_month(df, col, date_col="date", lo=0.01, hi=0.99):
    def _w(s):
        x = s.dropna()
        if x.empty: return s
        return s.clip(np.nanpercentile(x, lo*100), np.nanpercentile(x, hi*100))
    df[f"{col}_w"] = df.groupby(date_col)[col].transform(_w)
```

## Rule 8: Quarterly Data Gotchas

- **Q4 supplements:** CSHOQ/AJEXQ missing in Q4 → use annual CSHO/AJEX
- **Clean surplus imputation:** Impute missing BEQ forward up to 4 quarters: `BEQ_t = BEQ_{t-j} + sum(IBQ) - sum(DVQ)` for j in 1..4
- **Fiscal quarter:** Use FQTR column, not calendar month
- **Dividends:** DVQ = DVPSXQ * CSHOQ * AJEXQ (units: millions)
