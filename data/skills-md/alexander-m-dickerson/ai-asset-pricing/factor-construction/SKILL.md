---
name: factor-construction
description: "Look-ahead bias prevention and portfolio formation rules for cross-sectional asset pricing factors. Covers signal timing, portfolio sorts, return alignment, and rebalancing conventions. Auto-apply when constructing factors, sorting stocks into portfolios, or computing long-short returns."
---

# Factor Construction Rules

These rules prevent look-ahead bias (LAB) when forming cross-sectional factors. LAB means using information beyond the portfolio formation date — it silently inflates factor returns and invalidates results.

## LAB Audit Checklist

Run this checklist whenever forming portfolios or constructing factors. Flag any violation.

### 1. Signal is point-in-time at formation date t

- [ ] Accounting signals use data available at t (raw Compustat: ≥4-month lag; JKP: already aligned)
- [ ] Market data (price, ME, volume) uses end-of-period t values
- [ ] Regression-based signals (beta, loading estimates) use windows ending at or before t
- [ ] No `.shift(-1)` or forward-looking operation on the signal
- [ ] Signal does not condition on future outcomes (e.g., future default, future delisting)

### 2. Universe defined at t

- [ ] Stock universe uses only t-available information (listing status, exchange, share type at t)
- [ ] Stocks that delist after t are included in the t-formation universe (you didn't know they'd delist)
- [ ] Stocks that IPO after t are excluded from the t-formation universe
- [ ] No survivorship conditioning (don't require stocks to exist for N future months)

### 3. Breakpoints computed at t

- [ ] If using NYSE breakpoints: NYSE membership determined at t
- [ ] Percentile cutoffs computed from the cross-section at t
- [ ] No future data in breakpoint calculation

### 4. Returns from t+1

- [ ] Portfolio holds from t+1 (month after formation)
- [ ] VW returns use ME at t as weights (not t+1 ME)
- [ ] Delisting returns compounded with final trading-day return in t+1

### 5. Output dating convention

- [ ] Portfolio return series re-dated to the earning period (see convention below)

## Core Convention: Lead Returns, Not Signals

**Preferred approach:** Keep signals at their natural date. Lead only the portfolio return series.

```
Step 1: At date t, sort stocks using signal known at t
Step 2: Compute portfolio return from stock returns at t+1
Step 3: Assign this return to date t+1 (the period it was earned)
```

Why this is preferred:
- You only lead one value (portfolio return), not N signal columns
- Signal dates stay interpretable ("BM as of June 2023")
- The gap check from panel-data-rules applies to the final return series

**Date re-alignment for the output:**
```python
# After computing portfolio returns, shift date to earning period
port_ret["date"] = port_ret["date"] + pd.offsets.MonthEnd(1)
```

## Monthly Rebalancing Template

```python
import pandas as pd
import numpy as np

def monthly_factor(df, signal_col, date_col="date", id_col="permno",
                   ret_col="ret", me_col="me", n_groups=5,
                   weighting="vw"):
    """
    Form monthly-rebalanced long-short factor.

    df must have: date (month-end), permno, signal (known at date t),
                  ret (return earned in month t), me (market equity at date t).

    Convention: signal_t is used to form portfolios. Returns from t+1
    are the out-of-sample returns. Output dated to t+1.
    """
    df = df.sort_values([date_col, id_col]).copy()

    # Signal must exist at formation date
    df = df.dropna(subset=[signal_col])

    # Sort into quantile portfolios each month
    df["port"] = df.groupby(date_col)[signal_col].transform(
        lambda x: pd.qcut(x, n_groups, labels=False, duplicates="drop")
    )

    # Forward return: use NEXT month's return for each stock
    df = df.sort_values([id_col, date_col])
    df["fwd_ret"] = df.groupby(id_col)[ret_col].shift(-1)
    df["fwd_date"] = df.groupby(id_col)[date_col].shift(-1)

    # Gap check: if next date is > 31 days away, set fwd_ret to NaN
    day_gap = (df["fwd_date"] - df[date_col]).dt.days
    df.loc[day_gap > 31, "fwd_ret"] = np.nan

    df = df.dropna(subset=["fwd_ret"])

    # Portfolio returns
    if weighting == "vw":
        # Value-weight using ME at formation date t (NOT t+1)
        df["weight"] = df.groupby([date_col, "port"])[me_col].transform(
            lambda x: x / x.sum()
        )
        port_ret = df.groupby([date_col, "port"]).apply(
            lambda g: (g["fwd_ret"] * g["weight"]).sum(),
            include_groups=False
        ).unstack("port")
    else:
        port_ret = df.groupby([date_col, "port"])["fwd_ret"].mean().unstack("port")

    # Long-short: top minus bottom
    port_ret["hml"] = port_ret[n_groups - 1] - port_ret[0]

    # Re-date to earning period
    port_ret.index = port_ret.index + pd.offsets.MonthEnd(1)
    port_ret.index.name = date_col

    return port_ret


# Usage:
# port_ret = monthly_factor(panel, signal_col="bm", n_groups=5, weighting="vw")
```

## Annual Rebalancing (Fama-French Style)

**Convention:** Sort at end of June using signals from the most recent December fiscal year-end (with 4-month lag ensuring availability by April).

```
Timeline:
  Dec t-1:  Fiscal year ends → accounting data (BE, etc.)
  Apr t:    Data becomes available (4-month lag)
  Jun t:    Sort stocks into portfolios using Dec t-1 accounting + Jun t ME
  Jul t - Jun t+1:  Hold portfolios, rebalance next June
```

```python
def annual_factor(df, signal_col, date_col="date", id_col="permno",
                  ret_col="ret", me_col="me", n_groups=5,
                  formation_month=6, weighting="vw"):
    """
    Annual rebalancing (Fama-French style).

    Signal is measured once per year at formation_month (default June).
    Portfolios held for 12 months (July through next June).
    """
    df = df.sort_values([id_col, date_col]).copy()

    # Identify formation months
    df["month"] = df[date_col].dt.month
    df["year"] = df[date_col].dt.year

    # At formation month: assign portfolios using signal
    formation = df[df["month"] == formation_month].dropna(subset=[signal_col]).copy()
    formation["port"] = formation.groupby("year")[signal_col].transform(
        lambda x: pd.qcut(x, n_groups, labels=False, duplicates="drop")
    )

    # Carry portfolio assignment forward for 12 months
    # Merge assignment back to full panel
    assign = formation[[id_col, "year", "port"]].copy()
    assign = assign.rename(columns={"year": "form_year"})

    # Each stock's holding period: Jul of form_year through Jun of form_year+1
    df["form_year"] = np.where(
        df["month"] <= formation_month, df["year"] - 1, df["year"]
    )
    df = df.merge(assign, on=[id_col, "form_year"], how="left")
    df = df.dropna(subset=["port"])

    # Forward return for out-of-sample performance
    df = df.sort_values([id_col, date_col])
    df["fwd_ret"] = df.groupby(id_col)[ret_col].shift(-1)
    df["fwd_date"] = df.groupby(id_col)[date_col].shift(-1)
    day_gap = (df["fwd_date"] - df[date_col]).dt.days
    df.loc[day_gap > 31, "fwd_ret"] = np.nan
    df = df.dropna(subset=["fwd_ret"])

    # Portfolio returns (VW using current-month ME)
    if weighting == "vw":
        df["weight"] = df.groupby([date_col, "port"])[me_col].transform(
            lambda x: x / x.sum()
        )
        port_ret = df.groupby([date_col, "port"]).apply(
            lambda g: (g["fwd_ret"] * g["weight"]).sum(),
            include_groups=False
        ).unstack("port")
    else:
        port_ret = df.groupby([date_col, "port"])["fwd_ret"].mean().unstack("port")

    port_ret["hml"] = port_ret[n_groups - 1] - port_ret[0]
    port_ret.index = port_ret.index + pd.offsets.MonthEnd(1)
    port_ret.index.name = date_col

    return port_ret
```

**Key differences from monthly:**
- Signal measured once per year at formation month (June)
- Portfolio assignment carried forward for 12 months
- VW weights updated monthly using current ME (standard for FF)
- Same forward-return and gap-check convention applies

## Breakpoint Conventions — ASK USER

The templates above use `pd.qcut` across **all stocks** (equal-count portfolios). Fama-French uses **NYSE-only breakpoints** applied to all stocks:

```python
# NYSE breakpoints (FF convention)
nyse_mask = df["exchcd"] == 1
breakpoints = df.loc[nyse_mask, signal_col].quantile(
    [i/n_groups for i in range(1, n_groups)]
)
df["port"] = pd.cut(df[signal_col], bins=[-np.inf] + list(breakpoints) + [np.inf],
                     labels=False)
```

This creates **unequal-sized portfolios** (many small NASDAQ stocks in extreme groups). Always confirm with the user which convention they want — all-stock quantiles vs NYSE breakpoints.

## Gotchas

**`pd.qcut` with `duplicates='drop'`** can silently produce fewer groups than requested when many stocks share identical signal values. Always verify the actual number of groups created:
```python
actual_groups = df["port"].nunique()
assert actual_groups == n_groups, f"Expected {n_groups} groups, got {actual_groups}"
```

**Delisting returns must be incorporated.** Factor returns that ignore delistings suffer from survivorship bias. In CRSP v2, `mthret`/`dlyret` already include delisting returns. In CRSP v1, you must manually compound `dlret` with the final trading return: `ret_adj = (1 + ret) * (1 + dlret) - 1`.

## Post-Construction Diagnostics

After building any factor, run these sanity checks:

1. **Monotonicity:** Are portfolio mean returns monotonically increasing (or decreasing) across sort groups? Non-monotonicity in a well-known factor suggests a data or construction error (though weak/absent monotonicity can be genuine in recent samples).
2. **Long-short t-statistic:** Is the HML spread statistically significant? `t = mean / (std / sqrt(T))`. For well-known factors over long samples, expect |t| > 2.
3. **Portfolio sizes:** Are there enough stocks per portfolio per month? Print `df.groupby(['date','port']).size().describe()`. Fewer than ~30 stocks per portfolio is a red flag.
4. **Date coverage:** Does the output span the expected date range with no gaps?
5. **Benchmark correlation:** If replicating a known factor (e.g., FF HML), correlate with the published series. Expect r > 0.8 for value-weighted decile sorts.
6. **Signal staleness:** For accounting-based signals, check how old the underlying data is: `(panel_date - datadate).median()`. Median should be reasonable (e.g., ~10 months for annual BE).
