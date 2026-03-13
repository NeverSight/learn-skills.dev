---
name: volatility-modeling
description: "Model, forecast, and interpret volatility using time-series models and options-implied measures. Use when the user asks about EWMA, GARCH models, implied volatility, volatility surfaces, volatility term structure, or the VIX. Also trigger when users mention 'volatility smile', 'volatility skew', 'realized vs implied vol', 'volatility risk premium', 'vol clustering', 'mean-reverting volatility', 'options pricing inputs', 'RiskMetrics', 'decay factor', or ask how to forecast future volatility for risk management."
---

# Volatility Modeling

## Purpose
Model, forecast, and interpret volatility using time-series models and options-implied measures. This skill covers EWMA and GARCH(1,1) for volatility forecasting, implied volatility extraction, volatility smile/skew/surface construction, the volatility term structure, the realized-vs-implied volatility gap (volatility risk premium), and the VIX index. These tools are foundational for options pricing, risk management, and trading strategy development.

## Layer
1b — Forward-Looking Risk

## Direction
Prospective

## When to Use
- Forecasting future volatility for risk management or position sizing
- Building EWMA or GARCH models to capture volatility clustering and mean reversion
- Extracting implied volatility from option prices using Black-Scholes or other models
- Constructing or interpreting volatility smiles, skews, and surfaces
- Analyzing the volatility term structure across different maturities
- Comparing realized (historical) volatility to implied volatility to assess the volatility risk premium
- Understanding VIX and its relationship to market sentiment and expected risk

## Core Concepts

### EWMA (Exponentially Weighted Moving Average)
A simple volatility model that gives more weight to recent observations. RiskMetrics popularized this approach with a standard decay factor.

```
sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}
```

where:
- lambda = decay factor (RiskMetrics standard: 0.94 for daily, 0.97 for monthly)
- r_{t-1} = return in period t-1 (typically demeaned, but for daily returns the mean is often assumed to be zero)
- sigma^2_{t-1} = previous period's variance estimate

**Properties:**
- Assigns exponentially decaying weights to past squared returns.
- Effective window is approximately 1/(1 - lambda) observations. For lambda = 0.94, effective window is approximately 17 days.
- No mean reversion: the model is equivalent to IGARCH (integrated GARCH) where alpha + beta = 1. Volatility shocks persist indefinitely.
- Simple to implement and requires only one parameter.

### GARCH(1,1)
The Generalized Autoregressive Conditional Heteroskedasticity model adds a constant term that induces mean reversion in volatility.

```
sigma^2_t = omega + alpha * r^2_{t-1} + beta * sigma^2_{t-1}
```

where:
- omega > 0: constant term (determines long-run variance level)
- alpha >= 0: reaction coefficient (sensitivity to recent shocks)
- beta >= 0: persistence coefficient (memory of past variance)

**Stationarity condition:** alpha + beta < 1. This ensures the process is covariance-stationary and mean-reverting.

**Long-run (unconditional) variance:**

```
V_L = omega / (1 - alpha - beta)
```

Long-run annualized volatility: sigma_L = sqrt(V_L * 252).

**Persistence:** The quantity alpha + beta measures how quickly volatility reverts to its long-run level. Higher persistence means slower mean reversion.

**Half-life of volatility shocks:** The number of periods for a volatility shock to decay by half:

```
h = -ln(2) / ln(alpha + beta)
```

Since alpha + beta < 1, ln(alpha + beta) < 0, and h is positive.

**Multi-step forecasts:** The h-step-ahead GARCH(1,1) forecast:

```
E[sigma^2_{t+h}] = V_L + (alpha + beta)^h * (sigma^2_t - V_L)
```

The forecast converges to V_L as h approaches infinity.

### Implied Volatility
The volatility value that, when plugged into an option pricing model (typically Black-Scholes), produces a theoretical price equal to the observed market price.

For a European call under Black-Scholes:

```
C = S * N(d1) - K * exp(-rT) * N(d2)

d1 = [ln(S/K) + (r + sigma^2/2) * T] / (sigma * sqrt(T))
d2 = d1 - sigma * sqrt(T)
```

Implied volatility is the sigma that solves C_model(sigma) = C_market. There is no closed-form solution; it must be found numerically (e.g., Newton-Raphson, bisection).

### Volatility Smile and Skew
In practice, implied volatility varies by strike price, contradicting the constant-volatility assumption of Black-Scholes.

- **Volatility smile:** IV is higher for both deep in-the-money and deep out-of-the-money options, forming a U-shape. Common in FX markets.
- **Volatility skew (smirk):** IV increases for lower strikes (OTM puts have higher IV than OTM calls). This is the dominant pattern in equity markets and reflects demand for downside protection and the reality of fat left tails.
- **Skew is often quantified** as the difference in IV between a 25-delta put and a 25-delta call, or between 90% moneyness and 110% moneyness strikes.

### Volatility Term Structure
Implied volatility varies across option expiration dates.

- **Normal (upward-sloping):** Longer-dated options have higher IV. Reflects uncertainty increasing over time.
- **Inverted (downward-sloping):** Near-term IV exceeds long-term IV. Common during market stress when short-term uncertainty spikes (e.g., around earnings, elections, crises).
- **Humped:** IV peaks at an intermediate maturity. May occur around a specific anticipated event.

### Volatility Surface
The two-dimensional surface of implied volatility across both strike (or delta/moneyness) and maturity. The volatility surface is the most complete representation of the options market's view of future uncertainty.

Practitioners interpolate the surface to price options at arbitrary strike/maturity combinations. Surface dynamics (how the surface shifts, tilts, and bends) are critical for options portfolio risk management.

### Realized vs Implied Volatility: The Volatility Risk Premium
Implied volatility systematically exceeds subsequent realized volatility on average. This gap is the **volatility risk premium (VRP)**.

```
VRP = IV - RV_subsequent
```

The VRP exists because investors are willing to pay a premium for options (insurance), and option sellers demand compensation for bearing tail risk. The VRP is typically positive and has been a persistent source of return for volatility sellers.

Key considerations:
- The VRP varies over time and is larger during periods of market stress.
- Selling volatility (harvesting VRP) earns a steady premium but is exposed to large, infrequent losses.
- The VRP can turn negative during extreme events.

### VIX Index
The CBOE Volatility Index measures the market's expectation of 30-day forward volatility, derived from S&P 500 option prices.

- VIX is quoted in annualized percentage points (e.g., VIX = 20 means approximately 20% expected annualized vol).
- VIX is computed from a wide strip of OTM put and call options, not from the Black-Scholes model.
- VIX levels: 12-15 = low/complacent, 15-20 = normal, 20-30 = elevated, 30+ = high stress, 40+ = crisis.
- VIX has strong mean-reverting properties and tends to spike during market selloffs ("fear gauge").

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| EWMA Variance | sigma^2_t = lambda * sigma^2_{t-1} + (1-lambda) * r^2_{t-1} | Simple volatility forecast |
| GARCH(1,1) Variance | sigma^2_t = omega + alpha * r^2_{t-1} + beta * sigma^2_{t-1} | Mean-reverting vol forecast |
| GARCH Long-Run Variance | V_L = omega / (1 - alpha - beta) | Unconditional variance level |
| GARCH Half-Life | h = -ln(2) / ln(alpha + beta) | Speed of mean reversion |
| GARCH h-Step Forecast | V_L + (alpha+beta)^h * (sigma^2_t - V_L) | Multi-period vol forecast |
| Black-Scholes Call | S * N(d1) - K * exp(-rT) * N(d2) | Option pricing (IV extraction) |
| Volatility Risk Premium | IV - RV_subsequent | Premium earned by vol sellers |
| EWMA Effective Window | approximately 1 / (1 - lambda) | Implicit lookback period |

## Worked Examples

### Example 1: EWMA Variance Update
**Given:** Yesterday's variance estimate sigma^2_{t-1} = 0.0004 (daily vol = 2%), yesterday's return r_{t-1} = -3% (i.e., r = -0.03), and lambda = 0.94.

**Calculate:** Today's EWMA variance estimate and daily volatility.

**Solution:**

```
sigma^2_t = 0.94 * 0.0004 + (1 - 0.94) * (-0.03)^2
          = 0.94 * 0.0004 + 0.06 * 0.0009
          = 0.000376 + 0.000054
          = 0.000430
```

Daily volatility:

```
sigma_t = sqrt(0.000430) = 0.02074 = 2.074%
```

The large negative return (-3%) caused the volatility estimate to increase from 2.0% to 2.074%. The EWMA responded to the shock, but the high lambda (0.94) dampened the reaction.

### Example 2: GARCH(1,1) Long-Run Volatility and Half-Life
**Given:** GARCH(1,1) parameters estimated from daily S&P 500 returns: omega = 0.000002, alpha = 0.08, beta = 0.91.

**Calculate:** Long-run daily variance, long-run annualized volatility, and half-life of volatility shocks.

**Solution:**

**Stationarity check:** alpha + beta = 0.08 + 0.91 = 0.99 < 1 (stationary, but highly persistent).

**Long-run variance:**

```
V_L = 0.000002 / (1 - 0.99) = 0.000002 / 0.01 = 0.0002
```

**Long-run daily volatility:**

```
sigma_L = sqrt(0.0002) = 0.01414 = 1.414%
```

**Annualized:**

```
sigma_annual = 0.01414 * sqrt(252) = 22.45%
```

**Half-life:**

```
h = -ln(2) / ln(0.99) = -0.6931 / (-0.01005) = 68.97 ~ 69 trading days
```

Interpretation: After a volatility shock, it takes approximately 69 trading days (about 3 months) for the excess volatility to decay by half. This high persistence (alpha + beta = 0.99) is typical for equity index returns.

### Example 3: Implied Volatility Interpretation
**Given:** A stock trades at $100. A 3-month ATM call (K = $100) trades at $6.50. The risk-free rate is 5%. Using Black-Scholes, the implied volatility is determined (via numerical solver) to be 30%.

**Calculate:** What does this tell us, and how does it compare to realized vol of 22%?

**Solution:**

The implied volatility of 30% represents the market's consensus forecast of annualized volatility over the next 3 months, as embedded in option prices.

Comparing to realized (historical) volatility of 22%:

```
VRP = IV - RV = 30% - 22% = 8%
```

The positive 8-percentage-point gap is the volatility risk premium. Possible interpretations:
- The market expects volatility to rise above recent realized levels.
- Option sellers are demanding a premium for bearing tail risk.
- There may be an upcoming event (earnings, regulatory decision) that could cause a volatility spike.

A systematic vol-selling strategy would sell this option, expecting to profit from the VRP if realized vol remains near 22%. However, the seller bears the risk that realized vol could exceed 30%.

## Common Pitfalls
- **GARCH stationarity:** alpha + beta must be strictly less than 1 for the GARCH(1,1) process to be covariance-stationary. If alpha + beta >= 1, the long-run variance is undefined and the model is IGARCH (or explosive). Always check this condition after estimation.
- **EWMA has no mean reversion:** EWMA is equivalent to IGARCH (alpha + beta = 1), so volatility shocks never decay. This makes EWMA unsuitable for long-horizon volatility forecasts where mean reversion is expected.
- **Implied volatility is model-dependent:** IV extracted using Black-Scholes assumes log-normal returns, constant volatility, continuous trading, and no jumps. The "smile" and "skew" exist precisely because these assumptions are violated. IV is a quoting convention, not a true forecast.
- **Conflating historical vol with forward-looking vol:** Historical (realized) volatility measures what has happened. Implied volatility reflects market expectations about the future. They address different questions and can diverge substantially.
- **Using daily GARCH for long-horizon forecasts without term structure adjustment:** Daily GARCH forecasts converge to the unconditional variance at long horizons. Use the multi-step forecast formula E[sigma^2_{t+h}] = V_L + (alpha+beta)^h * (sigma^2_t - V_L) and aggregate appropriately.
- **Overfitting GARCH models:** Higher-order GARCH(p,q) models or extensions (EGARCH, TGARCH, GJR-GARCH) can overfit in-sample. GARCH(1,1) is remarkably hard to beat out-of-sample for most financial return series. Start with GARCH(1,1) and justify added complexity.
- **Lambda selection for EWMA:** The choice of lambda significantly affects responsiveness. lambda = 0.94 responds quickly to shocks (effective window approximately 17 days); lambda = 0.97 is smoother (effective window approximately 33 days). The choice should match the application's horizon.

## Cross-References
- **historical-risk** (wealth-management plugin, Layer 1a): Close-to-close, Parkinson, and Yang-Zhang volatility estimators provide the realized volatility benchmarks against which GARCH forecasts and implied volatility are compared.
- **forward-risk** (wealth-management plugin, Layer 1b): Volatility forecasts from EWMA and GARCH are direct inputs to parametric and Monte Carlo VaR calculations.
- **performance-metrics** (wealth-management plugin, Layer 1a): Volatility estimates affect the denominators of Sharpe, Sortino, and other risk-adjusted ratios. Using forward-looking (GARCH) volatility can produce conditional performance ratios.

## Reference Implementation
See `scripts/volatility_modeling.py` for computational helpers.
