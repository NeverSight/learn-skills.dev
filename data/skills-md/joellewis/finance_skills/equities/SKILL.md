---
name: equities
description: "Analyze equity securities, factor models, and equity portfolio construction. Use when the user asks about stocks, equity valuation ratios, index construction methods, or style analysis. Also trigger when users mention 'P/E ratio', 'growth vs value', 'market cap weighting', 'sector allocation', 'GICS classification', 'earnings per share', 'Fama-French factors', 'CAPM', 'dividend yield', 'PEG ratio', 'EV/EBITDA', or ask which factors explain equity returns."
---

# Equities

## Purpose
Analyze equity securities including individual stocks, equity indices, and equity portfolios. This skill covers factor models, valuation ratios, index construction methodologies, style analysis, earnings mechanics, and sector classification frameworks essential for equity market analysis.

## Layer
2 — Asset Classes

## Direction
both

## When to Use
- User asks about stocks, equity securities, or equity portfolio analysis
- User asks about equity factor models (CAPM, Fama-French, momentum, quality, low vol)
- User asks about index weighting methodologies (cap-weighted, equal-weighted, fundamental)
- User asks about valuation ratios (P/E, P/B, EV/EBITDA, dividend yield)
- User asks about earnings mechanics (EPS, diluted EPS, forward P/E, PEG ratio)
- User asks about sector or industry classification (GICS)
- User asks about style analysis (value vs growth, large vs small cap)
- User asks about return decomposition (price return vs total return)

## Core Concepts

### Market Cap Weighting vs Equal Weighting vs Fundamental Weighting
Cap-weighted indices weight each stock by its market capitalization, meaning larger companies dominate the index. Equal-weighted indices assign the same weight to every constituent, giving more influence to smaller names and requiring periodic rebalancing. Fundamental weighting uses metrics like revenue, earnings, or book value to determine weights, attempting to break the link between price and portfolio weight.

### Factor Models
Factor models explain equity returns through systematic exposures. The single-factor CAPM uses market beta. Multi-factor models add Size (SMB — Small Minus Big), Value (HML — High Minus Low book-to-market), Momentum (UMD — Up Minus Down), Quality (profitable minus unprofitable), and Low Volatility. Factor exposures are estimated via time-series regression of excess returns on factor returns.

CAPM: E(R_i) = R_f + beta_i × (E(R_m) - R_f)

Fama-French 3-Factor: R_i - R_f = alpha + beta_m×(R_m - R_f) + beta_s×SMB + beta_v×HML + epsilon

### Style Box Classification
The Morningstar style box maps funds and portfolios along two dimensions: Value/Blend/Growth (horizontal) and Large/Mid/Small cap (vertical), producing a 3x3 grid. Style is determined by valuation ratios (P/E, P/B) and growth metrics (earnings growth, sales growth). Style analysis regresses fund returns against style benchmark indices to determine effective exposures.

### Valuation Ratios
- P/E Ratio = Price / Earnings Per Share
- P/B Ratio = Price / Book Value Per Share
- EV/EBITDA = Enterprise Value / EBITDA
- Dividend Yield = Annual Dividends Per Share / Price
- Earnings Yield = EPS / Price (inverse of P/E)

### Earnings Mechanics
- EPS (Earnings Per Share) = Net Income / Shares Outstanding
- Diluted EPS accounts for stock options, convertibles, and other dilutive securities
- Forward P/E uses analyst consensus estimated future earnings
- PEG Ratio = P/E / Earnings Growth Rate (a growth-adjusted valuation measure)

### Sector and Industry Classification (GICS)
The Global Industry Classification Standard organizes equities into 11 sectors, 25 industry groups, 74 industries, and 163 sub-industries. Sector analysis helps identify concentration risk in portfolios and provides a framework for relative valuation comparisons.

### Index Construction
- Price-weighted (DJIA): weight proportional to share price, biased toward high-priced stocks
- Cap-weighted (S&P 500): weight proportional to market cap, reflects aggregate market value
- Equal-weighted: same weight to each constituent, requires periodic rebalancing

### Return Decomposition
Total Return = Price Return + Dividend Return. Price return captures capital gains only. Total return includes reinvested dividends and is the appropriate measure for performance comparison.

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| CAPM Expected Return | E(R_i) = R_f + beta_i × (E(R_m) - R_f) | Single-factor expected return |
| Fama-French 3-Factor | R_i - R_f = alpha + beta_m×(R_m-R_f) + beta_s×SMB + beta_v×HML + epsilon | Multi-factor return attribution |
| P/E Ratio | Price / EPS | Relative valuation |
| Earnings Yield | EPS / Price | Inverse of P/E, comparable to bond yields |
| PEG Ratio | (P/E) / Earnings Growth Rate | Growth-adjusted valuation |
| EV/EBITDA | (Market Cap + Debt - Cash) / EBITDA | Capital-structure-neutral valuation |
| Dividend Yield | Annual Dividends / Price | Income return measure |
| Total Return | Price Return + Dividend Return | Complete performance measure |

## Worked Examples

### Example 1: CAPM Expected Return
**Given:** beta = 1.2, R_f = 4%, E(R_m) = 10%
**Calculate:** Expected return using CAPM
**Solution:**
Equity risk premium = E(R_m) - R_f = 10% - 4% = 6%
E(R_i) = R_f + beta × ERP = 4% + 1.2 × 6% = 4% + 7.2% = 11.2%

The stock's expected return is 11.2%, reflecting a 7.2% risk premium for bearing 1.2x market risk.

### Example 2: Style Analysis via Regression
**Given:** A fund's monthly excess returns regressed on Russell 1000 Value and Russell 1000 Growth index excess returns over 36 months.
**Calculate:** Style tilt of the fund
**Solution:**
Regression: R_fund - R_f = alpha + beta_V×(R_Value - R_f) + beta_G×(R_Growth - R_f) + epsilon
Suppose results: beta_V = 0.70, beta_G = 0.25, alpha = 0.05%/month
Interpretation: The fund has a 74% value tilt (0.70 / (0.70 + 0.25)) and 26% growth tilt. The positive alpha of 0.05%/month (roughly 0.6%/year) suggests modest skill beyond style exposures. Total beta of 0.95 indicates slight cash drag.

## Common Pitfalls
- Using trailing P/E when forward P/E is more relevant for valuation — trailing earnings reflect the past, not the future
- Ignoring sector concentration in cap-weighted indices — a single sector can dominate 30%+ of the index
- Survivorship bias in backtested factor strategies — failed companies drop out, inflating historical returns
- Confusing price return with total return — dividends contribute significantly to long-term equity returns

## Cross-References
- **historical-risk** (wealth-management plugin, Layer 1a): beta, volatility, and Sharpe ratio fundamentals
- **fund-vehicles** (wealth-management plugin, Layer 2): equity fund selection (ETFs, mutual funds, SMAs)
- **currencies-and-fx** (wealth-management plugin, Layer 2): international equity currency effects
- **portfolio-construction** (wealth-management plugin, Layer 3): equity allocation within multi-asset portfolios

## Reference Implementation
See `scripts/equities.py` for computational helpers.
