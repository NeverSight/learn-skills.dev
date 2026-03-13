---
name: forward-risk
description: "Estimate potential future losses using VaR, Expected Shortfall, Monte Carlo simulation, and stress testing. Use when the user asks about Value-at-Risk, CVaR, Expected Shortfall, scenario analysis, stress testing, or factor-based risk decomposition. Also trigger when users mention 'how much could I lose', 'worst-case scenario', 'tail risk', 'risk budget', 'component VaR', 'marginal VaR', '99% confidence loss', 'Monte Carlo simulation', or ask how to project portfolio risk forward."
---

# Forward-Looking Risk Analysis

## Purpose
Estimate potential future losses and risk exposures using parametric models, simulation, and scenario analysis. This skill covers parametric and Monte Carlo Value-at-Risk, Conditional VaR (Expected Shortfall), component and marginal VaR, stress testing, scenario analysis, and factor-based risk decomposition. These tools are essential for portfolio risk management and regulatory capital calculations.

## Layer
1b — Forward-Looking Risk

## Direction
Prospective

## When to Use
- Estimating potential future losses for a portfolio or position
- Computing parametric VaR (variance-covariance method) for normally distributed returns
- Running Monte Carlo simulations to estimate VaR for non-normal distributions
- Computing CVaR / Expected Shortfall to understand tail risk beyond VaR
- Decomposing portfolio risk into component and marginal contributions
- Performing scenario analysis with historical or hypothetical shocks
- Stress testing portfolios under extreme but plausible conditions
- Breaking down risk into systematic factor risk and idiosyncratic risk

## Core Concepts

### Parametric (Variance-Covariance) VaR
Assumes returns are normally distributed. For a single asset or portfolio in dollar terms (assuming zero expected return over short horizons):

```
VaR = W * z_alpha * sigma_p
```

where:
- W = portfolio value
- z_alpha = z-score for confidence level (1.645 for 95%, 2.326 for 99%)
- sigma_p = portfolio volatility over the relevant horizon

More generally, including expected return:

```
VaR_alpha = mu - z_alpha * sigma
```

To convert from 1-day VaR to h-day VaR (assuming i.i.d. returns):

```
VaR_h = VaR_1 * sqrt(h)
```

### Portfolio VaR (Multiple Assets)
For a portfolio with weight vector w and covariance matrix Sigma:

```
sigma_p = sqrt(w' * Sigma * w)
VaR_p   = W * z_alpha * sqrt(w' * Sigma * w)
```

The covariance matrix captures both individual volatilities and correlations between assets.

### Monte Carlo VaR
Simulate a large number of portfolio return scenarios (e.g., 10,000+), then take the alpha-percentile of the simulated loss distribution.

Steps:
1. Estimate the return distribution parameters (mean vector, covariance matrix, or use a copula model).
2. Generate N random return scenarios (e.g., via Cholesky decomposition of the covariance matrix for multivariate normal).
3. Compute portfolio return for each scenario.
4. Sort results and identify the alpha-percentile loss.

Monte Carlo VaR can accommodate non-normal distributions, fat tails, path-dependent instruments, and nonlinear payoffs (e.g., options).

### Conditional VaR (CVaR) / Expected Shortfall
CVaR answers: "Given that losses exceed VaR, what is the expected loss?"

```
ES_alpha = E[Loss | Loss > VaR_alpha]
```

For a normal distribution:

```
ES_alpha = mu + sigma * phi(z_alpha) / (1 - alpha)
```

where phi is the standard normal PDF.

CVaR is a **coherent risk measure** (unlike VaR) because it satisfies subadditivity: CVaR(A+B) <= CVaR(A) + CVaR(B). This means diversification always reduces or maintains CVaR, which is not guaranteed for VaR.

### Component VaR
Decomposes total portfolio VaR into contributions from each position. Component VaRs sum to total VaR.

```
CVaR_i = w_i * beta_i * VaR_p
```

where beta_i = Cov(R_i, R_p) / Var(R_p) is the asset's beta to the portfolio.

Equivalently:

```
CVaR_i = w_i * (partial VaR / partial w_i)
sum(CVaR_i) = VaR_p
```

This decomposition identifies which positions are the largest contributors to portfolio risk.

### Marginal VaR
Measures the rate of change of portfolio VaR with respect to a small increase in a position's weight.

```
MVaR_i = partial(VaR_p) / partial(w_i) = z_alpha * (Sigma * w)_i / sigma_p
```

Marginal VaR is used for position sizing: adding to a position with low marginal VaR reduces portfolio risk more efficiently.

### Scenario Analysis
Apply specific historical or hypothetical market moves to the current portfolio to estimate P&L impact.

- **Historical scenarios:** Replay actual market events (e.g., 2008 GFC, 2020 COVID crash, 2022 rate hiking cycle) with current holdings.
- **Hypothetical scenarios:** Construct custom shocks (e.g., "equities -20%, rates +200bp, credit spreads +300bp, USD +10%").

Scenario P&L is computed by applying the scenario returns to current position exposures and revaluing.

### Stress Testing
A structured framework for assessing portfolio resilience under extreme but plausible conditions.

Common stress scenarios:
- Equity crash: S&P 500 -30% to -40%
- Interest rate shock: +300bp parallel shift
- Credit crisis: investment-grade spreads +200bp, high-yield +800bp
- Liquidity freeze: bid-ask spreads widen 10x, forced selling at discount
- Currency shock: major currency pair moves 15-20%
- Stagflation: inflation +5%, GDP -3%, rates +200bp

Stress tests should include second-order effects: margin calls, liquidity demands, correlation spikes, counterparty risk.

### Factor-Based Risk Decomposition
Separate total portfolio risk into systematic factor risk and idiosyncratic (security-specific) risk.

```
sigma^2_p = b' * Sigma_f * b + sum(w_i^2 * sigma^2_epsilon_i)
```

where:
- b = vector of portfolio factor exposures
- Sigma_f = factor covariance matrix
- sigma^2_epsilon_i = idiosyncratic variance of asset i

Common factor models: Fama-French (market, size, value, momentum), Barra risk models, PCA-based statistical factors.

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| Parametric VaR (single) | W * z_alpha * sigma | Simple position VaR |
| Portfolio VaR | W * z_alpha * sqrt(w' * Sigma * w) | Multi-asset VaR |
| Multi-day VaR | VaR_1 * sqrt(h) | Scale to h-day horizon |
| CVaR (normal) | mu + sigma * phi(z_alpha) / (1 - alpha) | Expected tail loss |
| Component VaR | w_i * beta_i * VaR_p | Risk contribution per position |
| Marginal VaR | z_alpha * (Sigma * w)_i / sigma_p | Sensitivity to weight change |
| Factor Risk | b' * Sigma_f * b | Systematic risk component |
| Idiosyncratic Risk | sum(w_i^2 * sigma^2_epsilon_i) | Security-specific risk |

## Worked Examples

### Example 1: Parametric 95% VaR
**Given:** A $1,000,000 equity portfolio with an annualized volatility of 15%.

**Calculate:** 1-day 95% parametric VaR (assuming 252 trading days and zero expected daily return).

**Solution:**

Daily volatility:

```
sigma_daily = 0.15 / sqrt(252) = 0.15 / 15.875 = 0.00945
```

1-day 95% VaR:

```
VaR = $1,000,000 * 1.645 * 0.00945 = $15,545
```

Alternatively, computing directly from annual figures:

```
VaR_annual = $1,000,000 * 1.645 * 0.15 = $246,750
VaR_1day   = $246,750 / sqrt(252)       = $15,545
```

Interpretation: There is a 5% chance of losing more than $15,545 in a single day under normal market conditions.

### Example 2: Monte Carlo VaR
**Given:** A two-asset portfolio (60% equities, 40% bonds). Equities: mu = 10%, sigma = 18%. Bonds: mu = 4%, sigma = 5%. Correlation rho = -0.2. Portfolio value = $1,000,000.

**Calculate:** 95% annual VaR via Monte Carlo simulation (conceptual steps).

**Solution:**

1. **Construct covariance matrix:**

```
Sigma = | 0.0324  -0.0018 |
        | -0.0018  0.0025 |
```

2. **Cholesky decomposition** of Sigma to get lower triangular matrix L.

3. **Simulate 10,000 scenarios:** For each simulation, draw z ~ N(0, I), compute r = mu + L*z, then portfolio return R_p = w' * r.

4. **Compute portfolio P&L** for each scenario: P&L = $1,000,000 * R_p.

5. **Sort P&L** from worst to best. The 500th worst (5th percentile) is the 95% VaR.

For this portfolio, the analytical answer provides a benchmark:

```
sigma_p = sqrt(0.6^2 * 0.0324 + 0.4^2 * 0.0025 + 2 * 0.6 * 0.4 * (-0.0018))
        = sqrt(0.01105)
        = 10.51%

VaR_95% = $1,000,000 * 1.645 * 0.1051 = $172,890
```

The Monte Carlo result should converge to approximately this value for a multivariate normal assumption.

### Example 3: Expected Shortfall
**Given:** From the Monte Carlo simulation above, the losses exceeding VaR (the worst 500 out of 10,000 scenarios) have an average loss of $225,000.

**Calculate:** 95% CVaR.

**Solution:**

```
CVaR_95% = $225,000
```

Interpretation: When losses exceed the 95% VaR threshold, the average loss is $225,000. This is 30% worse than the VaR figure, highlighting the severity of tail events.

## Common Pitfalls
- **VaR says nothing about tail shape:** VaR only identifies a threshold. Two portfolios with identical VaR can have vastly different tail losses. Always compute CVaR alongside VaR to understand tail severity.
- **Parametric VaR assumes normality:** Financial returns exhibit fat tails and skewness. Parametric VaR systematically underestimates tail risk. Use Monte Carlo with fat-tailed distributions or historical simulation for more realistic estimates.
- **Correlation breakdown in crises:** Correlations spike toward 1.0 during market stress, precisely when diversification is most needed. Stress tests should use crisis-period correlations, not calm-period correlations.
- **Using too short a lookback for covariance estimation:** Too short a window is noisy; too long a window includes stale data from different market regimes. A common compromise is 1-3 years of daily data, or use EWMA-weighted covariances.
- **Not distinguishing between absolute VaR and relative VaR:** Absolute VaR includes expected return (VaR = -mu + z*sigma); relative VaR excludes it (VaR = z*sigma). For short horizons (1-10 days), the expected return is negligible and the distinction is minor. For longer horizons, it matters.
- **Square-root-of-time scaling limitations:** VaR_h = VaR_1 * sqrt(h) assumes i.i.d. returns. With serial correlation or volatility clustering, this scaling is inaccurate.

## Cross-References
- **historical-risk** (wealth-management plugin, Layer 1a): Historical VaR and realized volatility serve as non-parametric alternatives and calibration benchmarks for the forward-looking models in this skill.
- **performance-metrics** (wealth-management plugin, Layer 1a): VaR and CVaR can be used as risk denominators in modified risk-adjusted ratios (e.g., return/CVaR).
- **volatility-modeling** (wealth-management plugin, Layer 1b): EWMA and GARCH volatility forecasts provide the volatility inputs (sigma) for parametric and Monte Carlo VaR.

## Reference Implementation
See `scripts/forward_risk.py` for computational helpers.
