---
name: quantitative-valuation
description: "Estimate intrinsic value of stocks and companies using DCF, dividend discount models, comparable multiples, and residual income. Use when the user asks about discounted cash flow, DCF models, WACC, terminal value, dividend discount models, comparable multiples, or sum-of-the-parts valuation. Also trigger when users mention 'what is this stock worth', 'fair value estimate', 'Gordon growth model', 'free cash flow valuation', 'cost of equity', 'sensitivity analysis', 'exit multiple', or ask whether a stock is overvalued or undervalued."
---

# Quantitative Valuation

## Purpose
Provides frameworks and formulas for estimating the intrinsic value of a stock or company using quantitative models. Covers discounted cash flow (DCF), dividend discount models (DDM), comparable multiples, residual income, and sum-of-the-parts valuation. Enables rigorous, assumption-driven valuation that can be stress-tested through sensitivity analysis.

## Layer
3 — Valuation

## Direction
prospective

## When to Use
- Valuing a stock or company from first principles
- Building a discounted cash flow (DCF) model
- Comparing a company's multiples to peers or its own history
- Estimating intrinsic value using dividend discount models
- Performing sum-of-the-parts valuation for a conglomerate
- Running sensitivity analysis on valuation assumptions
- Screening for undervalued or overvalued securities using relative multiples

## Core Concepts

### Discounted Cash Flow (DCF)
The DCF model values a company as the present value of its future free cash flows plus a terminal value:

V = Σ FCF_t / (1 + WACC)^t + TV / (1 + WACC)^n

where FCF_t is the free cash flow in year t, WACC is the weighted average cost of capital, and TV is the terminal value at the end of the explicit forecast period.

### Terminal Value — Gordon Growth Model
Estimates the value of all cash flows beyond the explicit forecast period assuming perpetual growth:

TV = FCF_n × (1 + g) / (WACC - g)

where g is the long-term sustainable growth rate (typically near nominal GDP growth, 2-4%).

### Terminal Value — Exit Multiple Method
Estimates terminal value by applying a market multiple to the final-year financial metric:

TV = EBITDA_n × EV/EBITDA multiple

The exit multiple is typically based on current peer trading multiples or long-run sector averages.

### Weighted Average Cost of Capital (WACC)
Blends the cost of equity and after-tax cost of debt weighted by their market-value proportions:

WACC = w_e × r_e + w_d × r_d × (1 - τ)

where w_e and w_d are equity and debt weights, r_e and r_d are their respective costs, and τ is the marginal tax rate.

### Cost of Equity — CAPM
The Capital Asset Pricing Model estimates the required return on equity:

r_e = R_f + β × (R_m - R_f)

where R_f is the risk-free rate, β is the stock's sensitivity to market returns, and (R_m - R_f) is the equity risk premium.

### Dividend Discount Model (DDM)
Values a stock as the present value of its future dividends. The Gordon Growth (single-stage) form:

P = D_1 / (r - g)

where D_1 is the next-period dividend, r is the required return, and g is the constant dividend growth rate.

### Multi-Stage DDM
Accommodates companies transitioning through growth phases:
- **Stage 1 (High growth):** Dividends grow at g_1 for n years
- **Stage 2 (Transition):** Growth declines linearly from g_1 to g_3
- **Stage 3 (Stable):** Dividends grow at g_3 in perpetuity (valued via Gordon Growth)

### Residual Income Model
Values a company as its book value plus the present value of economic profits:

V = BV_0 + Σ (ROE - r) × BV_{t-1} / (1 + r)^t

This model is useful when free cash flows are negative but the company earns above its cost of equity.

### Comparable Multiples
Relative valuation uses pricing ratios from a peer group to infer value:
- **P/E** (Price-to-Earnings): most common for profitable companies
- **EV/EBITDA** (Enterprise Value to EBITDA): capital-structure neutral
- **P/S** (Price-to-Sales): useful for unprofitable or early-stage companies
- **P/B** (Price-to-Book): useful for asset-heavy businesses (banks, REITs)

Use the median of the peer group to reduce outlier effects. Adjust for differences in growth, margins, and risk.

### Relative Valuation
Compare a stock's current multiple to:
- Its own historical average (time-series comparison)
- Sector or industry median (cross-sectional comparison)

A stock trading at a discount to both may be undervalued, or there may be fundamental deterioration.

### Sum-of-the-Parts (SOTP)
Value each business segment separately using the most appropriate method (DCF, multiples, or asset-based), then sum. Subtract net debt and add non-operating assets to arrive at equity value.

### Sensitivity Analysis
Vary key assumptions (WACC and terminal growth rate are the most impactful) in a two-way data table to understand the range of possible valuations. This exposes which assumptions drive the result.

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| DCF Value | V = Σ FCF_t/(1+WACC)^t + TV/(1+WACC)^n | Enterprise valuation from cash flows |
| Gordon Growth TV | TV = FCF_n×(1+g)/(WACC-g) | Terminal value assuming perpetual growth |
| Exit Multiple TV | TV = EBITDA_n × multiple | Terminal value using market multiples |
| WACC | WACC = w_e×r_e + w_d×r_d×(1-τ) | Blended discount rate |
| CAPM | r_e = R_f + β×(R_m - R_f) | Cost of equity estimation |
| Gordon Growth DDM | P = D_1/(r-g) | Stock value from dividends |
| Residual Income | V = BV_0 + Σ (ROE-r)×BV_{t-1}/(1+r)^t | Value from economic profit |
| Implied Value (Comps) | V = Metric × Peer Median Multiple | Relative valuation |

## Worked Examples

### Example 1: Two-Stage DCF
**Given:**
- Current FCF: $100M
- Stage 1: 15% FCF growth for 5 years
- Terminal growth rate: 3%
- WACC: 10%

**Calculate:** Enterprise value

**Solution:**

Projected free cash flows:
- Year 1: $100M × 1.15 = $115.0M
- Year 2: $115M × 1.15 = $132.3M
- Year 3: $132.3M × 1.15 = $152.1M
- Year 4: $152.1M × 1.15 = $174.9M
- Year 5: $174.9M × 1.15 = $201.1M

PV of Stage 1 cash flows:
- PV = $115.0/1.10 + $132.3/1.10² + $152.1/1.10³ + $174.9/1.10⁴ + $201.1/1.10⁵
- PV = $104.5 + $109.3 + $114.3 + $119.5 + $124.9 = $572.5M

Terminal value (Gordon Growth):
- TV = $201.1M × 1.03 / (0.10 - 0.03) = $207.2M / 0.07 = $2,959.6M
- PV of TV = $2,959.6M / 1.10⁵ = $1,837.3M

Enterprise Value = $572.5M + $1,837.3M = $2,409.8M

Note: Terminal value represents 76% of total value, which is typical but underscores the importance of terminal assumptions.

### Example 2: Comparable P/E Analysis
**Given:**
- Target company EPS: $5.00
- Peer group P/E ratios: 15x, 17x, 18x, 19x, 22x

**Calculate:** Implied share price using peer median

**Solution:**

Peer median P/E = 18x (middle value of the sorted set)

Implied share price = EPS × Peer Median P/E = $5.00 × 18 = $90.00

If the stock trades at $75, it appears undervalued relative to peers (16.7% discount). Before concluding, check whether lower growth, margins, or higher risk justify the discount.

## Common Pitfalls
- Terminal value dominates DCF output (often 60-80% of total value) — scrutinize terminal assumptions carefully
- Garbage-in-garbage-out: a DCF is only as good as its assumptions; false precision gives false confidence
- Using trailing multiples when forward multiples are more relevant for fast-growing or cyclical companies
- Not adjusting comparable multiples for differences in growth rates, margins, and capital structure
- Circular reference when WACC depends on market cap which depends on the WACC-derived valuation — iterate or use target capital structure
- Projecting high growth rates indefinitely without considering competitive dynamics and mean reversion
- Ignoring dilution from stock-based compensation in per-share value estimates

## Cross-References
- **historical-risk** (wealth-management plugin, Layer 1a): historical beta estimation for CAPM inputs
- **forward-risk** (wealth-management plugin, Layer 1b): cost of equity estimation via CAPM and factor models
- **financial-statements** (wealth-management plugin, Layer 2): FCF and EBITDA derivation from financials
- **qualitative-valuation** (wealth-management plugin, Layer 3): complements quantitative models with moat and quality analysis
- **asset-allocation** (wealth-management plugin, Layer 4): valuation outputs feed into portfolio construction decisions

## Reference Implementation
See `scripts/quantitative_valuation.py` for computational helpers.
