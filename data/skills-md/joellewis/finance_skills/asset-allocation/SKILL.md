---
name: asset-allocation
description: "Asset allocation frameworks: strategic (SAA), tactical (TAA), mean-variance optimization, Black-Litterman, risk parity, glide paths."
allowed-tools: ["Bash", "Read", "Write", "Edit"]
---

# Asset Allocation

## Purpose
Provides frameworks for determining how to distribute capital across asset classes and strategies. Covers strategic and tactical allocation, mean-variance optimization, Black-Litterman, risk parity, glide paths, and practical implementation approaches. Asset allocation is the primary driver of long-term portfolio performance and risk.

## Layer
4 — Portfolio Construction

## Direction
both

## When to Use
- Setting long-term strategic asset allocation targets
- Making tactical allocation decisions based on market views
- Running mean-variance optimization with constraints
- Implementing Black-Litterman to blend market equilibrium with investor views
- Building risk parity or equal risk contribution portfolios
- Designing glide paths for target-date or lifecycle strategies
- Evaluating core-satellite portfolio structures
- Matching assets to liabilities for pensions or insurance portfolios

## Core Concepts

### Strategic Asset Allocation (SAA)
The long-term policy portfolio based on an investor's risk tolerance, return objectives, time horizon, and constraints. SAA determines the baseline target weights (e.g., 60% equity / 30% bonds / 10% alternatives) and is the dominant driver of long-term portfolio returns. SAA should be revisited when investor circumstances change, not in response to market movements.

### Tactical Asset Allocation (TAA)
Short-to-medium-term deviations from the SAA based on market views, valuations, or momentum signals. TAA requires a disciplined process to avoid becoming ad hoc market timing. Key considerations:
- Define allowable deviation bands (e.g., +/- 10% from SAA)
- Have a clear signal framework (valuation, momentum, macro)
- Set reversion rules: when to return to SAA weights

### Mean-Variance Optimization (MVO)
Markowitz's framework for finding optimal portfolio weights that maximize risk-adjusted return:

max w'*mu - (lambda/2) * w'*Sigma*w

subject to: sum(w_i) = 1, w_i >= 0 (if long-only), and any additional constraints.

Where:
- w = weight vector
- mu = expected return vector
- Sigma = covariance matrix
- lambda = risk aversion parameter

MVO requires three inputs: expected returns, the covariance matrix, and risk aversion. The solution is highly sensitive to expected return inputs.

### Black-Litterman Model
Combines market equilibrium returns with investor views to produce more stable, intuitive portfolio weights. Two-step process:

**Step 1 — Implied Equilibrium Returns:**
Pi = lambda * Sigma * w_mkt

where w_mkt is the market-capitalization weight vector, lambda is the risk aversion parameter, and Sigma is the covariance matrix. These are the returns the market implicitly expects given current prices.

**Step 2 — Blending with Views:**
E(R) = [(tau*Sigma)^(-1) + P'*Omega^(-1)*P]^(-1) * [(tau*Sigma)^(-1)*Pi + P'*Omega^(-1)*Q]

where:
- tau = scalar (uncertainty of equilibrium, typically 0.025-0.05)
- P = pick matrix (identifies assets in each view)
- Q = view vector (expected returns from views)
- Omega = diagonal matrix of view uncertainties

The result is a posterior expected return vector that tilts away from equilibrium toward the investor's views, proportional to confidence.

### Risk Parity
Equalizes the risk contribution from each asset (or factor) rather than equalizing capital allocation:

RC_i = w_i * (Sigma*w)_i / sigma_p

Set RC_i = RC_j for all i, j.

In a simple two-asset case with no correlation:
w_i is proportional to 1/sigma_i

Risk parity portfolios allocate more capital to lower-volatility assets (typically bonds) and often require leverage to achieve competitive return targets.

### Glide Path
An age-based or time-based allocation that systematically shifts from growth assets to defensive assets as the investor ages or the target date approaches:

Common rule of thumb: Equity % = 110 - Age

Target-date fund glide paths typically:
- Start at 90% equity for young investors
- Decrease by ~1-2% per year
- Reach 30-40% equity at retirement
- Continue to "through" allocation post-retirement

### Core-Satellite
A hybrid approach combining:
- **Core (60-80%):** Low-cost, broadly diversified index funds or ETFs
- **Satellites (20-40%):** Active strategies, factor tilts, alternatives, or concentrated positions

This structure captures the market return efficiently (core) while allowing alpha generation or specific exposures (satellites).

### Asset-Liability Matching
For investors with defined liabilities (pensions, insurance, endowments with spending rules):
- Match asset duration and cash flows to liability duration and timing
- Surplus optimization: optimize the portfolio relative to liabilities, not absolute return
- Liability-driven investing (LDI): hedge liability risk with duration-matched bonds, invest surplus in return-seeking assets

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| MVO Objective | max w'*mu - (lambda/2)*w'*Sigma*w | Optimal portfolio weights |
| Equilibrium Returns | Pi = lambda * Sigma * w_mkt | Black-Litterman starting point |
| BL Posterior | E(R) = [(tau*Sigma)^(-1) + P'*Omega^(-1)*P]^(-1) * [(tau*Sigma)^(-1)*Pi + P'*Omega^(-1)*Q] | Blended expected returns |
| Risk Contribution | RC_i = w_i * (Sigma*w)_i / sigma_p | Risk parity target |
| Risk Parity Condition | RC_i = RC_j for all i, j | Equal risk contribution |
| Glide Path Rule | Equity % = 110 - Age | Age-based allocation |

## Worked Examples

### Example 1: Three-Asset Mean-Variance Optimization
**Given:**
- Assets: US Equity (mu=8%, sigma=16%), Int'l Equity (mu=7%, sigma=18%), US Bonds (mu=3%, sigma=4%)
- Correlations: US/Intl Equity = 0.75, US Equity/Bonds = 0.10, Intl Equity/Bonds = 0.05
- Risk aversion: lambda = 4
- Constraints: long-only, fully invested

**Calculate:** Optimal weights

**Solution:**

Covariance matrix:
- Cov(US,US) = 0.16^2 = 0.0256
- Cov(Intl,Intl) = 0.18^2 = 0.0324
- Cov(Bond,Bond) = 0.04^2 = 0.0016
- Cov(US,Intl) = 0.75 * 0.16 * 0.18 = 0.0216
- Cov(US,Bond) = 0.10 * 0.16 * 0.04 = 0.00064
- Cov(Intl,Bond) = 0.05 * 0.18 * 0.04 = 0.00036

MVO with lambda=4 (solving numerically or via quadratic programming):

Optimal weights (approximate):
- US Equity: 35%
- Int'l Equity: 15%
- US Bonds: 50%

Portfolio: expected return = 5.25%, volatility = 7.8%

Note: The high bond allocation results from the optimization penalizing variance heavily (lambda=4). Reducing lambda or adding a minimum equity constraint would shift toward equities.

### Example 2: Black-Litterman with a View on Emerging Markets
**Given:**
- Market-cap weights: US 55%, Developed Ex-US 30%, EM 15%
- Equilibrium returns (from Pi = lambda*Sigma*w_mkt): US 6.5%, Dev Ex-US 5.8%, EM 7.2%
- Investor view: EM will outperform US by 2% (medium confidence)
- tau = 0.05

**Calculate:** Posterior expected returns and implied weight shift

**Solution:**

View specification:
- P = [-1, 0, 1] (EM minus US)
- Q = [2%] (EM outperforms US by 2%)
- Omega = [0.001] (medium confidence; lower = higher confidence)

After applying the Black-Litterman formula:

Posterior expected returns (approximate):
- US: 6.2% (decreased from 6.5%)
- Dev Ex-US: 5.9% (slight increase due to correlation effects)
- EM: 7.8% (increased from 7.2%)

The posterior tilts returns toward the view. When these posterior returns are fed into MVO, the resulting weights shift from market-cap weights toward EM and away from US, but the shift is moderate and proportional to confidence, avoiding the extreme concentrations that raw MVO can produce.

## Common Pitfalls
- MVO is highly sensitive to expected return inputs and has been called an "error maximizer" — small changes in returns produce large changes in weights
- Unconstrained MVO often produces extreme, concentrated positions — always add constraints (long-only, max weight, turnover limits)
- Black-Litterman requires the analyst to specify confidence in views (Omega), which is itself uncertain
- Risk parity portfolios require leverage to achieve equity-like returns, introducing borrowing costs and leverage risk
- Ignoring implementation costs: transaction costs, bid-ask spreads, and taxes can significantly erode theoretical optimal returns
- Ignoring liquidity constraints: some asset classes (private equity, real estate) cannot be rebalanced quickly
- Glide paths assume a generic investor — individual circumstances may require customization
- Over-reliance on historical covariance matrices that may not reflect future relationships

## Cross-References
- **historical-risk** (wealth-management plugin, Layer 1a): volatility and correlation inputs for mean-variance optimization
- **forward-risk** (wealth-management plugin, Layer 1b): expected return forecasts and scenario analysis for portfolio optimization
- **diversification** (wealth-management plugin, Layer 4): diversification principles underpin all allocation frameworks
- **bet-sizing** (wealth-management plugin, Layer 4): position sizing within the allocated asset classes
- **rebalancing** (wealth-management plugin, Layer 4): maintaining allocation targets over time
- **quantitative-valuation** (wealth-management plugin, Layer 3): valuation signals can inform TAA decisions

## Reference Implementation
See `scripts/asset_allocation.py` for computational helpers.
