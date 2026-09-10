---
name: risk-report
description: Generate a one-page risk summary from a returns series. Computes Sharpe, Sortino, max DD, CVaR, tail ratio, rolling correlation. Use when analyzing backtest or live P&L output.
---

# Risk Report Skill

Generate a standardized one-page risk summary. Ask for the returns series location (CSV path or Python variable). Default: daily returns.

## Metrics to compute

### Return
- Total return (cumulative)
- CAGR (compounded annual)
- Monthly return distribution (mean, median, stdev)

### Risk
- Annualized volatility
- Max drawdown (depth + duration)
- Ulcer index
- Downside deviation

### Risk-adjusted
- Sharpe (rf = 0 unless specified)
- Sortino
- Calmar (CAGR / max DD)
- Omega (threshold = 0)

### Tails
- 95% / 99% VaR (historical)
- 95% / 99% CVaR / Expected Shortfall
- Tail ratio (95th percentile / 5th percentile absolute)
- Skew, kurtosis

### Correlation
- Beta vs. BTC
- Beta vs. SPY
- Rolling 30d correlation (chart description)

### Stability
- Monthly hit rate
- Worst 3 months
- Best 3 months
- Drawdown distribution: number of DDs > 5%, > 10%, > 20%

## Code template

```python
import numpy as np
import pandas as pd

def risk_report(returns: pd.Series, periods_per_year: int = 252) -> dict:
    r = returns.dropna()
    cum = (1 + r).cumprod()
    dd = cum / cum.cummax() - 1

    downside = r[r < 0]
    var95 = np.percentile(r, 5)
    cvar95 = r[r <= var95].mean()

    return {
        "total_return":      cum.iloc[-1] - 1,
        "cagr":              cum.iloc[-1] ** (periods_per_year / len(r)) - 1,
        "vol_annual":        r.std() * np.sqrt(periods_per_year),
        "sharpe":            r.mean() / r.std() * np.sqrt(periods_per_year),
        "sortino":           r.mean() / downside.std() * np.sqrt(periods_per_year),
        "max_dd":            dd.min(),
        "dd_duration_days":  (dd < 0).astype(int).groupby(dd.eq(0).cumsum()).sum().max(),
        "calmar":            (cum.iloc[-1] ** (periods_per_year / len(r)) - 1) / abs(dd.min()),
        "var_95":            var95,
        "cvar_95":           cvar95,
        "skew":              r.skew(),
        "kurtosis":          r.kurtosis(),
        "hit_rate":          (r > 0).mean(),
    }
```

## Output format

Always present as a single markdown table, grouped by category (Return / Risk / Risk-adjusted / Tails / Stability). Highlight any metric outside sane ranges:
- Sharpe > 3 → suspicious
- Max DD > 40% → risk
- Skew < -1 → tail-heavy losses
- Kurtosis > 5 → fat tails
