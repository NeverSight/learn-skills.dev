---
name: diversification
description: "Build diversified portfolios using correlation analysis, efficient frontier construction, and factor-based diversification. Use when the user asks about portfolio variance, correlation effects, the efficient frontier, minimum variance portfolios, diversification ratios, or factor diversification. Also trigger when users mention 'don't put all eggs in one basket', 'how many stocks do I need', 'correlation breakdown in a crisis', 'are my holdings really diversified', 'risk contributions', or ask why diversification fails during market crashes."
---

# Diversification

## Purpose
Provides the mathematical foundations and practical frameworks for building diversified portfolios. Covers portfolio variance, correlation effects, the efficient frontier, minimum variance portfolios, risk contributions, and factor-based diversification. Explains why diversification reduces risk and where it fails.

## Layer
4 — Portfolio Construction

## Direction
both

## When to Use
- Understanding why and how diversification reduces portfolio risk
- Computing portfolio variance and volatility for multi-asset portfolios
- Constructing the efficient frontier or minimum variance portfolio
- Analyzing risk contributions and diversification ratios
- Evaluating whether a portfolio is truly diversified across risk factors
- Assessing correlation stability and regime-dependent behavior
- Determining how many assets are needed for adequate diversification

## Core Concepts

### Portfolio Variance (2 Assets)
For a portfolio of two assets with weights w_1 and w_2, volatilities sigma_1 and sigma_2, and correlation rho_12:

sigma^2_p = w_1^2 * sigma_1^2 + w_2^2 * sigma_2^2 + 2 * w_1 * w_2 * sigma_1 * sigma_2 * rho_12

Diversification benefit arises whenever rho_12 < 1, because the portfolio volatility will be less than the weighted average of individual volatilities.

### Portfolio Variance (n Assets)
In matrix notation for n assets with weight vector w and covariance matrix Sigma:

sigma^2_p = w' * Sigma * w

This generalizes to any number of assets and captures all pairwise correlations.

### Diversification Benefit
Portfolio volatility is strictly less than the weighted average of individual volatilities whenever any pairwise correlation is below 1:

sigma_p < Sigma(w_i * sigma_i)  when rho_ij < 1 for some i,j

The lower the average correlation, the greater the diversification benefit.

### Efficient Frontier
The efficient frontier is the set of portfolios that offer the highest expected return for each level of risk (or equivalently, the lowest risk for each level of return). Portfolios below the frontier are suboptimal — they can be improved by reallocating weights.

### Minimum Variance Portfolio
The portfolio with the lowest possible volatility, regardless of expected returns:

w_mv = Sigma^(-1) * 1 / (1' * Sigma^(-1) * 1)

where 1 is a vector of ones. This portfolio depends only on the covariance matrix, not on expected returns, making it more robust to estimation error.

### Correlation Regimes
Correlations are not constant. In market crises, correlations between risky assets tend to increase sharply ("correlation breakdown" or "correlation tightening"), reducing the diversification benefit precisely when it is needed most. Key implications:
- Stress-test portfolios using crisis-period correlation matrices
- Diversification across asset classes (stocks, bonds, commodities, real assets) is more robust than within-asset-class diversification

### Diversification Ratio
A measure of how much diversification a portfolio achieves:

DR = (Sigma(w_i * sigma_i)) / sigma_p

A portfolio of perfectly correlated assets has DR = 1. Higher DR indicates more effective diversification. A fully diversified equal-volatility portfolio with zero correlations has DR = sqrt(n).

### Maximum Diversification Portfolio
The portfolio that maximizes the diversification ratio. This is an alternative to mean-variance optimization that does not require expected return inputs — it relies only on volatilities and correlations.

### Factor Diversification
True diversification means exposure to multiple independent risk factors, not merely holding many assets. Assets that share the same factor exposures (e.g., multiple tech stocks all driven by growth factor) provide less diversification than their number suggests. Key factors:
- Market, size, value, momentum, quality, low volatility
- Interest rate, credit, inflation
- Geographic, sector, currency

### Risk Contribution
The risk contribution of asset i to portfolio volatility:

RC_i = w_i * (Sigma * w)_i / sigma_p

where (Sigma * w)_i is the i-th element of the vector Sigma * w. The sum of all risk contributions equals the portfolio volatility. This decomposition reveals which assets truly drive portfolio risk.

### Marginal Risk Contribution
The rate of change of portfolio volatility with respect to the weight of asset i:

MRC_i = (Sigma * w)_i / sigma_p

Risk contribution = weight * marginal risk contribution: RC_i = w_i * MRC_i

### Diminishing Marginal Diversification
The diversification benefit of adding assets decreases rapidly. Empirically:
- 15-20 uncorrelated assets capture most of the diversification benefit
- Beyond 30 assets, incremental risk reduction is minimal
- The asymptotic portfolio variance equals the average covariance (systematic risk cannot be diversified away)

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| 2-Asset Portfolio Variance | sigma^2_p = w_1^2*sigma_1^2 + w_2^2*sigma_2^2 + 2*w_1*w_2*sigma_1*sigma_2*rho_12 | Two-asset risk calculation |
| n-Asset Portfolio Variance | sigma^2_p = w' * Sigma * w | General portfolio risk |
| Minimum Variance Weights | w_mv = Sigma^(-1)*1 / (1'*Sigma^(-1)*1) | Lowest-risk portfolio |
| Diversification Ratio | DR = Sigma(w_i*sigma_i) / sigma_p | Measure of diversification |
| Risk Contribution | RC_i = w_i * (Sigma*w)_i / sigma_p | Asset-level risk attribution |
| Marginal Risk Contribution | MRC_i = (Sigma*w)_i / sigma_p | Sensitivity of risk to weight |
| Asymptotic Variance | sigma^2_p → avg(cov_ij) as n → infinity | Diversification limit |

## Worked Examples

### Example 1: Two-Asset Portfolio Volatility
**Given:**
- Stock: sigma = 20%, weight = 60%
- Bond: sigma = 5%, weight = 40%
- Correlation: rho = 0.2

**Calculate:** Portfolio volatility

**Solution:**

sigma^2_p = (0.60)^2 * (0.20)^2 + (0.40)^2 * (0.05)^2 + 2 * (0.60) * (0.40) * (0.20) * (0.05) * (0.20)

sigma^2_p = 0.36 * 0.04 + 0.16 * 0.0025 + 2 * 0.60 * 0.40 * 0.20 * 0.05 * 0.20

sigma^2_p = 0.0144 + 0.0004 + 0.00096

sigma^2_p = 0.01576

sigma_p = sqrt(0.01576) = 0.1255 = **12.55%**

Weighted average volatility = 0.60 * 20% + 0.40 * 5% = 14.0%

Diversification benefit = 14.0% - 12.55% = **1.45 percentage points** of risk reduction.

### Example 2: Diversification Ratio for a 4-Asset Portfolio
**Given:**
- Assets: A (sigma=15%, w=25%), B (sigma=20%, w=25%), C (sigma=10%, w=25%), D (sigma=18%, w=25%)
- Portfolio volatility (computed from full covariance matrix): sigma_p = 10.5%

**Calculate:** Diversification ratio

**Solution:**

Weighted average volatility = 0.25*15% + 0.25*20% + 0.25*10% + 0.25*18%
= 3.75% + 5.0% + 2.5% + 4.5% = 15.75%

Diversification Ratio = 15.75% / 10.5% = **1.50**

Interpretation: The portfolio achieves significant diversification — the weighted average volatility is 50% higher than the actual portfolio volatility. A DR of 1.50 indicates meaningful correlation benefits. For comparison, a portfolio of perfectly correlated assets would have DR = 1.0.

## Common Pitfalls
- Diversification is not just about holding more assets — correlation structure is what matters; 50 highly correlated stocks provide less diversification than 10 uncorrelated ones
- Correlations are unstable and tend to increase during market stress, reducing the diversification benefit precisely when it is most needed
- Over-diversification (diworsification): holding too many positions dilutes high-conviction ideas and guarantees mediocre returns after costs
- Home country bias: investors systematically under-allocate to international assets, missing a major source of diversification
- Confusing asset diversification with factor diversification: a portfolio of 20 growth stocks is not diversified despite holding many names
- Using historical correlations without testing sensitivity to regime changes

## Cross-References
- **historical-risk** (wealth-management plugin, Layer 1a): volatility, correlation, and systematic vs. idiosyncratic risk foundations
- **asset-allocation** (wealth-management plugin, Layer 4): diversification principles feed directly into portfolio construction and optimization
- **rebalancing** (wealth-management plugin, Layer 4): maintaining diversification targets over time through rebalancing
- **bet-sizing** (wealth-management plugin, Layer 4): position sizing interacts with diversification — concentrated vs. diversified approaches

## Reference Implementation
See `scripts/diversification.py` for computational helpers.
