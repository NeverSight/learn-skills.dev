---
name: historical-risk
description: "Quantify realized risk from historical data using volatility estimators, drawdown analysis, and downside risk metrics. Use when the user asks about historical volatility, maximum drawdown, drawdown duration, historical VaR, downside deviation, semi-variance, or tracking error. Also trigger when users mention 'how risky has this been', 'worst decline', 'Parkinson estimator', 'Yang-Zhang', 'peak-to-trough loss', 'recovery time', 'annualized volatility', or ask how to measure past investment risk."
---

# Historical Risk Analysis

## Purpose
Quantify how risky an investment or portfolio has been using historical return and price data. This skill covers volatility estimation (close-to-close, Parkinson, Yang-Zhang), drawdown analysis, historical Value-at-Risk, downside deviation, tracking error, and semi-variance. All measures are backward-looking and computed from observed data.

## Layer
1a — Realized Risk & Performance

## Direction
Retrospective

## When to Use
- Understanding how risky an investment has been over a past period
- Computing historical (realized) volatility using various estimators
- Measuring drawdowns: maximum drawdown, drawdown duration, and recovery time
- Calculating historical VaR (non-parametric, directly from the return distribution)
- Computing downside deviation or semi-variance for asymmetric risk assessment
- Measuring tracking error of a portfolio relative to a benchmark

## Core Concepts

### Close-to-Close Volatility
The simplest and most common volatility estimator. Compute the standard deviation of log returns and annualize.

```
sigma_annual = sigma_daily * sqrt(N)
```

where N = number of trading periods per year (typically 252 for daily, 52 for weekly, 12 for monthly).

Log returns are preferred: r_t = ln(P_t / P_{t-1}).

### Parkinson (High-Low) Estimator
Uses intraday high and low prices to capture intraday volatility that close-to-close misses. More efficient than close-to-close when the true process is continuous.

```
sigma^2_Park = (1 / (4 * n * ln(2))) * sum( ln(H_i / L_i)^2 )
```

This estimator is roughly 5x more efficient than close-to-close for a diffusion process, but is biased downward when there are jumps or when the range is discretized.

### Yang-Zhang Estimator
Combines overnight (close-to-open), open-to-close, and Rogers-Satchell components. It is unbiased for processes with both drift and opening jumps.

```
sigma^2_YZ = sigma^2_overnight + k * sigma^2_open-to-close + (1 - k) * sigma^2_RS
```

where k is chosen to minimize estimator variance, and sigma^2_RS is the Rogers-Satchell estimator that uses all four OHLC prices within each period.

### Drawdown Analysis
Drawdown at time t measures the decline from the running peak:

```
DD_t = (Peak_t - Value_t) / Peak_t
```

where Peak_t = max(Value_s) for all s <= t.

- **Maximum Drawdown (MDD):** MDD = max(DD_t) over the evaluation period.
- **Drawdown Duration:** The number of periods from a peak until a new peak is reached.
- **Recovery Time:** The number of periods from the trough back to the prior peak level.

### Historical VaR
The non-parametric (empirical) Value-at-Risk is simply the alpha-percentile of the historical return distribution. No distributional assumptions are made.

```
VaR_alpha = -Percentile(R, alpha)
```

For example, 95% VaR uses the 5th percentile of returns. The negative sign is a convention so that VaR is expressed as a positive loss number.

### Downside Deviation
Measures dispersion of returns below a Minimum Acceptable Return (MAR):

```
sigma_d = sqrt( (1/n) * sum( min(R_i - MAR, 0)^2 ) )
```

Common choices for MAR: 0%, the risk-free rate, or the mean return.

### Tracking Error
Standard deviation of the difference between portfolio and benchmark returns, annualized:

```
TE = std(R_p - R_b) * sqrt(N)
```

This measures how consistently the portfolio tracks (or deviates from) its benchmark.

### Semi-Variance
Variance computed using only returns below the mean (or below a threshold):

```
SV = (1/n) * sum( min(R_i - mean(R), 0)^2 )
```

Semi-variance isolates downside risk and is the foundation for the Sortino ratio (see performance-metrics).

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| Annualized Volatility | sigma_ann = sigma_period * sqrt(N) | Convert period vol to annual vol |
| Log Return | r_t = ln(P_t / P_{t-1}) | Compute continuously compounded returns |
| Parkinson Variance | sigma^2 = (1 / (4n ln2)) * sum(ln(H/L)^2) | Volatility from high-low data |
| Drawdown | DD_t = (Peak_t - Value_t) / Peak_t | Measure peak-to-trough decline |
| Max Drawdown | MDD = max(DD_t) | Worst historical decline |
| Historical VaR (95%) | 5th percentile of return series | Non-parametric loss estimate |
| Downside Deviation | sigma_d = sqrt((1/n) * sum(min(R_i - MAR, 0)^2)) | Asymmetric risk below MAR |
| Tracking Error | TE = std(R_p - R_b) * sqrt(N) | Portfolio vs benchmark deviation |
| Semi-Variance | (1/n) * sum(min(R_i - mean(R), 0)^2) | Below-mean variance |

## Worked Examples

### Example 1: Annualized Volatility from Daily Returns
**Given:** A stock has daily log returns with a sample standard deviation of 1.2%. Assume 252 trading days per year.

**Calculate:** Annualized volatility.

**Solution:**

```
sigma_annual = 0.012 * sqrt(252)
             = 0.012 * 15.875
             = 0.1905
             ~ 19.05%
```

The stock's annualized volatility is approximately 19%.

### Example 2: Maximum Drawdown from a Price Series
**Given:** A fund's NAV follows this path over six months: $120, $135, $150, $130, $105, $125.

**Calculate:** Maximum drawdown and identify the peak and trough.

**Solution:**

Running peaks: $120, $135, $150, $150, $150, $150.

Drawdowns at each point:
- $120: (120-120)/120 = 0%
- $135: (135-135)/135 = 0%
- $150: (150-150)/150 = 0%
- $130: (150-130)/150 = 13.3%
- $105: (150-105)/150 = 30.0%
- $125: (150-125)/150 = 16.7%

**Maximum Drawdown = 30.0%**, occurring from the peak of $150 to the trough of $105. As of the last observation ($125), the drawdown has not yet fully recovered.

### Example 3: Historical VaR
**Given:** 500 daily returns sorted from worst to best. The 25th-worst return is -2.8% and the 26th-worst is -2.6%.

**Calculate:** 95% 1-day historical VaR.

**Solution:**

The 5th percentile corresponds to the 25th observation out of 500 (500 * 0.05 = 25).

```
VaR_95% = -(-2.8%) = 2.8%
```

Interpretation: On 95% of days, the loss is expected not to exceed 2.8% based on the historical distribution.

## Common Pitfalls
- **Not annualizing volatility correctly:** Volatility scales with the square root of time (multiply by sqrt(N)), not linearly. Multiplying daily vol by 252 instead of sqrt(252) produces wildly inflated numbers.
- **Using calendar days vs trading days inconsistently:** Use 252 trading days (not 365 calendar days) for equity markets when annualizing. Bond markets and some international markets may differ.
- **Survivorship bias in historical data:** Data sets that exclude delisted or failed securities understate realized risk.
- **Lookback period sensitivity:** A 1-year lookback captures different risk regimes than a 5-year lookback. Always state the lookback window and consider whether it spans relevant market conditions.
- **Confusing VaR confidence level direction:** 95% VaR corresponds to the 5th percentile of returns (the loss tail). The "95%" refers to the confidence level, not the percentile of gains.
- **Log returns vs simple returns:** For volatility estimation, log returns are preferred because they are additive across time. For reporting cumulative performance, simple returns are more intuitive.

## Cross-References
- **performance-metrics** (wealth-management plugin, Layer 1a): Uses volatility, downside deviation, tracking error, and max drawdown as denominators in risk-adjusted ratios (Sharpe, Sortino, Information Ratio, Calmar).
- **forward-risk** (wealth-management plugin, Layer 1b): Historical VaR and historical volatility serve as inputs to forward-looking VaR models and stress tests.
- **volatility-modeling** (wealth-management plugin, Layer 1b): EWMA and GARCH models extend the simple historical volatility estimators covered here into forecasting frameworks.

## Reference Implementation
See `scripts/historical_risk.py` for computational helpers.
