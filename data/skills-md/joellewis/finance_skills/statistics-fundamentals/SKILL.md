---
name: statistics-fundamentals
description: "Apply statistical methods to financial data including descriptive statistics, covariance estimation, regression, hypothesis testing, and resampling. Use when the user asks about return distributions, correlation between assets, building a covariance matrix, running a CAPM regression, testing whether alpha is significant, checking if returns are normal, or estimating confidence intervals. Also trigger when users mention 'volatility', 'how correlated are these', 'fat tails', 'skewness', 'R-squared', 'beta of a fund', 'bootstrap a Sharpe ratio', 'shrinkage estimator', 'Ledoit-Wolf', or ask why their optimizer produces unstable weights."
---

# Statistics Fundamentals

## Purpose
This skill enables Claude to apply core statistical methods to financial data, including descriptive statistics, covariance estimation, linear regression, hypothesis testing, and resampling techniques. These methods form the quantitative backbone for portfolio construction, risk measurement, and factor modeling.

## Layer
0 — Mathematical Foundations

## Direction
both

## When to Use
- Analyzing return distributions
- Estimating correlations or covariance matrices
- Running regression analysis on financial data
- Testing hypotheses about returns
- Building factor models

## Core Concepts

### Descriptive Statistics

**Mean (Expected Value):**

$$\mu = E[X] = \frac{1}{n} \sum_{i=1}^{n} x_i$$

The arithmetic average of observed values. For financial returns, this represents the central tendency of the return distribution.

**Variance:**

Population variance:

$$\sigma^2 = \frac{1}{n} \sum_{i=1}^{n} (x_i - \mu)^2$$

Sample variance (Bessel's correction):

$$s^2 = \frac{1}{n-1} \sum_{i=1}^{n} (x_i - \bar{x})^2$$

**Standard Deviation:**

$$\sigma = \sqrt{\sigma^2}$$

In finance, standard deviation of returns is commonly called **volatility**. Annualized volatility from monthly data: `sigma_annual = sigma_monthly * sqrt(12)`.

**Skewness:**

$$\gamma = \frac{E[(X - \mu)^3]}{\sigma^3}$$

Measures asymmetry of the distribution. Negative skewness (left tail) is common in equity returns and indicates a higher probability of large losses than large gains.

**Excess Kurtosis:**

$$\kappa = \frac{E[(X - \mu)^4]}{\sigma^4} - 3$$

Measures tail thickness relative to the normal distribution (which has excess kurtosis of 0). Financial returns typically exhibit positive excess kurtosis (leptokurtosis), meaning fat tails and more frequent extreme events than a normal distribution would predict.

### Covariance and Correlation

**Covariance:**

$$\text{Cov}(X, Y) = E[(X - \mu_X)(Y - \mu_Y)]$$

Sample covariance:

$$\hat{\text{Cov}}(X, Y) = \frac{1}{n-1} \sum_{i=1}^{n} (x_i - \bar{x})(y_i - \bar{y})$$

Covariance measures the linear co-movement between two variables. Positive covariance means they tend to move together; negative means they move inversely.

**Correlation (Pearson):**

$$\rho(X, Y) = \frac{\text{Cov}(X, Y)}{\sigma_X \times \sigma_Y}$$

Correlation normalizes covariance to the range `[-1, +1]`, making it unit-free and comparable across variable pairs.

### Covariance Matrix Estimation

For a set of `p` assets with `n` return observations, the sample covariance matrix is:

$$\hat{\Sigma} = \frac{1}{n-1} (X - \bar{X})^T (X - \bar{X})$$

where `X` is the `n x p` matrix of returns.

**The curse of dimensionality:** When `p` (number of assets) is large relative to `n` (number of observations), the sample covariance matrix becomes poorly conditioned or singular, leading to unstable portfolio optimizations.

### Ledoit-Wolf Shrinkage Estimator

Shrinkage blends the sample covariance matrix with a structured target (e.g., the identity matrix scaled by average variance) to produce a more stable estimate:

$$\hat{\Sigma}_{shrunk} = \delta \cdot F + (1 - \delta) \cdot \hat{\Sigma}$$

where:
- `F` = the shrinkage target (structured estimator)
- `delta` = the optimal shrinkage intensity (estimated analytically)
- `Sigma_hat` = the sample covariance matrix

Ledoit-Wolf determines the optimal `delta` that minimizes expected squared Frobenius distance to the true covariance matrix. This produces better-conditioned matrices and more stable portfolio weights.

### OLS Regression

Ordinary Least Squares estimates the linear relationship `y = X * beta + epsilon` by minimizing the sum of squared residuals.

**Coefficient Estimate:**

$$\hat{\beta} = (X^T X)^{-1} X^T y$$

**Key Regression Diagnostics:**

**R-squared (Coefficient of Determination):**

$$R^2 = 1 - \frac{SS_{res}}{SS_{tot}} = 1 - \frac{\sum(y_i - \hat{y}_i)^2}{\sum(y_i - \bar{y})^2}$$

Represents the proportion of variance in the dependent variable explained by the model.

**Adjusted R-squared:**

$$\bar{R}^2 = 1 - (1 - R^2) \frac{n - 1}{n - k - 1}$$

where `k` = number of regressors. Penalizes additional regressors that do not improve fit.

**Standard Errors:**

$$SE(\hat{\beta}) = \sqrt{\hat{\sigma}^2 \cdot \text{diag}((X^T X)^{-1})}$$

where `sigma_hat^2 = SS_res / (n - k - 1)`.

**t-statistic:**

$$t = \frac{\hat{\beta}_j}{SE(\hat{\beta}_j)}$$

Tests whether each coefficient is significantly different from zero.

In finance, the single-factor regression `R_i - R_f = alpha + beta * (R_m - R_f) + epsilon` is the CAPM regression, where `alpha` is the risk-adjusted excess return and `beta` is market sensitivity.

### Common Distributions in Finance

**Normal Distribution:** Symmetric, fully characterized by mean and variance. Used as a baseline model for returns, though real returns deviate from normality.

**Log-Normal Distribution:** If `ln(X)` is normal, then `X` is log-normal. Asset prices (not returns) are often modeled as log-normal, ensuring prices cannot go negative.

**Student-t Distribution:** Has heavier tails than the normal. Parameterized by degrees of freedom `nu`; lower `nu` means fatter tails. Commonly used to model financial returns more realistically. As `nu -> infinity`, converges to the normal.

**Chi-Squared Distribution:** The distribution of a sum of squared standard normal variables. Used in variance tests and as the sampling distribution of `(n-1)*s^2 / sigma^2`.

### Bootstrap Methods

Non-parametric resampling technique for estimating the sampling distribution of a statistic.

**Algorithm:**
1. From the original dataset of size `n`, draw `B` bootstrap samples, each of size `n`, with replacement.
2. Compute the statistic of interest on each bootstrap sample.
3. Use the distribution of the `B` bootstrap statistics to estimate confidence intervals, standard errors, or bias.

**Confidence Interval (Percentile Method):**
The `(1 - alpha)` confidence interval is given by the `alpha/2` and `1 - alpha/2` percentiles of the bootstrap distribution.

Bootstrap is especially useful in finance when:
- Analytical formulas for standard errors are unavailable (e.g., Sharpe ratio)
- The underlying distribution is unknown or non-normal
- Small sample sizes make asymptotic results unreliable

### Hypothesis Testing

**t-test (mean):** Tests whether a sample mean differs significantly from a hypothesized value.

$$t = \frac{\bar{x} - \mu_0}{s / \sqrt{n}}$$

with `n - 1` degrees of freedom.

**F-test (joint significance):** Tests whether a group of regression coefficients are jointly zero. Used in multi-factor models.

$$F = \frac{(SS_{restricted} - SS_{unrestricted}) / q}{SS_{unrestricted} / (n - k - 1)}$$

where `q` = number of restrictions.

**Jarque-Bera Test (normality):** Tests whether sample skewness and kurtosis are consistent with a normal distribution.

$$JB = \frac{n}{6} \left(\gamma^2 + \frac{\kappa^2}{4}\right)$$

where `gamma` = sample skewness and `kappa` = sample excess kurtosis. Under the null of normality, JB follows a chi-squared distribution with 2 degrees of freedom. Financial return series almost always reject normality due to fat tails and skewness.

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| Sample Mean | `x_bar = (1/n) * sum(x_i)` | Central tendency |
| Sample Variance | `s^2 = (1/(n-1)) * sum((x_i - x_bar)^2)` | Dispersion |
| Annualized Volatility | `sigma_annual = sigma_period * sqrt(periods_per_year)` | Risk standardization |
| Skewness | `gamma = E[(X-mu)^3] / sigma^3` | Asymmetry |
| Excess Kurtosis | `kappa = E[(X-mu)^4] / sigma^4 - 3` | Tail thickness |
| Covariance | `Cov(X,Y) = E[(X-mu_X)(Y-mu_Y)]` | Co-movement |
| Correlation | `rho = Cov(X,Y) / (sigma_X * sigma_Y)` | Standardized co-movement |
| Shrinkage Estimator | `Sigma_shrunk = delta*F + (1-delta)*Sigma_hat` | Stable covariance matrix |
| OLS Coefficients | `beta_hat = (X'X)^(-1) X'y` | Linear regression |
| R-squared | `1 - SS_res / SS_tot` | Model explanatory power |
| t-statistic | `t = beta_hat_j / SE(beta_hat_j)` | Coefficient significance |
| Jarque-Bera | `JB = (n/6) * (gamma^2 + kappa^2/4)` | Normality test |

## Worked Examples

### Example 1: Compute Descriptive Statistics and Test for Normality
**Given:** Monthly returns (in %) for a fund over 12 months:
`[2.1, -0.5, 1.8, -3.2, 4.5, 0.3, -1.1, 2.7, -0.8, 3.4, 1.2, -0.6]`

**Calculate:** Mean, volatility, skewness, excess kurtosis, and Jarque-Bera test statistic.

**Solution:**

**Mean:**
```
x_bar = (2.1 + (-0.5) + 1.8 + (-3.2) + 4.5 + 0.3 + (-1.1) + 2.7 + (-0.8) + 3.4 + 1.2 + (-0.6)) / 12
x_bar = 9.8 / 12
x_bar = 0.8167% per month
```

**Annualized return** (approximate): `0.8167% * 12 = 9.8%`

**Sample Standard Deviation:**
```
Deviations from mean: [1.283, -1.317, 0.983, -4.017, 3.683, -0.517, -1.917, 1.883, -1.617, 2.583, 0.383, -1.417]
Squared deviations:   [1.646, 1.734, 0.967, 16.133, 13.566, 0.267, 3.674, 3.547, 2.614, 6.674, 0.147, 2.007]
Sum of squared deviations = 52.977
s^2 = 52.977 / 11 = 4.816
s = sqrt(4.816) = 2.195% per month
```

**Annualized volatility:** `2.195% * sqrt(12) = 7.60%`

**Skewness:**
```
Sum of cubed standardized deviations:
gamma = (1/n) * sum[((x_i - x_bar)/s)^3]  (using adjusted formula for sample)
gamma approx 0.075 (slightly positive, near symmetric)
```

**Excess Kurtosis:**
```
kappa = (1/n) * sum[((x_i - x_bar)/s)^4] - 3
kappa approx -0.42 (platykurtic, lighter tails than normal)
```

**Jarque-Bera Test:**
```
JB = (12/6) * (0.075^2 + (-0.42)^2 / 4)
JB = 2 * (0.00563 + 0.04410)
JB = 2 * 0.04973
JB = 0.099
```

The JB critical value at 5% significance (chi-squared, df=2) is 5.99. Since `0.099 < 5.99`, we **fail to reject** the null hypothesis of normality. With only 12 observations, however, the test has low power, and we should not conclude the data is truly normal.

### Example 2: Regress Fund Returns on Market Factor (CAPM)
**Given:** 24 monthly observations:
- Fund excess returns (`R_i - R_f`): mean = 0.8%, std = 4.2%
- Market excess returns (`R_m - R_f`): mean = 0.6%, std = 3.8%
- Sample correlation between fund and market: 0.85

**Calculate:** CAPM alpha and beta, R-squared, and assess statistical significance.

**Solution:**

**Beta:**
```
beta = Cov(R_i, R_m) / Var(R_m)
     = rho * sigma_i * sigma_m / sigma_m^2
     = rho * sigma_i / sigma_m
     = 0.85 * 4.2 / 3.8
     = 0.939
```

**Alpha:**
```
alpha = mean(R_i - R_f) - beta * mean(R_m - R_f)
      = 0.8% - 0.939 * 0.6%
      = 0.8% - 0.564%
      = 0.236% per month (approximately 2.84% annualized)
```

**R-squared:**
```
R^2 = rho^2 = 0.85^2 = 0.7225
```

72.25% of the fund's return variance is explained by the market factor.

**Standard Error and t-statistic for alpha:**
```
Residual std = sigma_i * sqrt(1 - R^2) = 4.2% * sqrt(1 - 0.7225) = 4.2% * 0.5268 = 2.213%
SE(alpha) = residual_std / sqrt(n) = 2.213% / sqrt(24) = 0.452%
t(alpha) = 0.236 / 0.452 = 0.522
```

With 22 degrees of freedom (n - 2), the critical t-value at 5% significance (two-tailed) is approximately 2.074. Since `|0.522| < 2.074`, the alpha is **not statistically significant**. Despite the positive point estimate, we cannot conclude the fund generates genuine risk-adjusted outperformance with this sample size.

**Standard Error and t-statistic for beta:**
```
SE(beta) = residual_std / (sigma_m * sqrt(n-1)) = 2.213% / (3.8% * sqrt(23)) = 2.213% / 18.226% = 0.121
t(beta) = 0.939 / 0.121 = 7.76
```

Since `|7.76| >> 2.074`, the beta is **highly statistically significant**, confirming the fund has meaningful market exposure.

## Common Pitfalls
- Using population variance instead of sample variance: always use `n - 1` (Bessel's correction) in the denominator when estimating variance from a sample. Using `n` underestimates the true variance.
- Assuming normality when financial returns have fat tails: equity returns typically exhibit negative skewness and positive excess kurtosis. Models relying on normality (e.g., standard VaR) underestimate tail risk. Use the Student-t distribution or non-parametric methods for more robust estimates.
- Ignoring non-stationarity in time series: financial return distributions change over time (regime shifts, volatility clustering). Rolling-window estimation or GARCH models may be more appropriate than full-sample statistics.
- Overfitting with too many regressors: adding more factors to a regression always increases R-squared but may not improve out-of-sample explanatory power. Use adjusted R-squared, information criteria (AIC/BIC), or cross-validation to guard against overfitting.
- Unstable covariance matrices with small samples: when the number of assets `p` approaches or exceeds the number of observations `n`, the sample covariance matrix becomes singular or poorly conditioned. Apply Ledoit-Wolf shrinkage or factor-based covariance models to obtain stable, invertible matrices for portfolio optimization.

## Cross-References
- **return-calculations** (core plugin, Layer 0): Arithmetic and geometric mean returns, log returns for statistical modeling
- **time-value-of-money** (core plugin, Layer 0): Discount rate estimation via CAPM regression; NPV and IRR calculations use statistical inputs

## Reference Implementation
See `scripts/statistics_fundamentals.py` for computational helpers.
