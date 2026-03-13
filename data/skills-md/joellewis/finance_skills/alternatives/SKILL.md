---
name: alternatives
description: "Analyze alternative investments including hedge funds, private equity, and venture capital. Use when the user asks about hedge fund strategies (long/short, macro, event-driven), PE or VC performance metrics (IRR, TVPI, DPI), fee structures ('2-and-20', carry, hurdle rates), the J-curve effect, illiquidity premiums, lock-up periods, or hedge fund replication. Also trigger when users mention 'managed futures', 'CTA', 'fund of funds', 'vintage year', 'capital calls', 'distributions', 'carried interest', or ask how to evaluate an alternative investment manager."
---

# Alternatives

## Purpose
Analyze alternative investments including hedge funds, private equity, and venture capital. This skill covers strategy classification, fee structure analysis, performance metrics unique to alternatives (IRR, TVPI, DPI), the J-curve effect, illiquidity premiums, and the critical due diligence considerations for evaluating alternative investment managers.

## Layer
2 — Asset Classes

## Direction
both

## When to Use
- User asks about hedge funds or hedge fund strategies
- User asks about private equity, buyouts, or growth equity
- User asks about venture capital investing or VC metrics
- User asks about alternative investment fee structures (2-and-20, carry, hurdle rates)
- User asks about IRR, TVPI, DPI, or other PE performance metrics
- User asks about the J-curve effect in private equity
- User asks about illiquidity premiums or lock-up periods
- User asks about hedge fund replication or factor-based alternatives

## Core Concepts

### Hedge Fund Strategies
- **Long/Short Equity:** Combines long positions in undervalued stocks with short positions in overvalued stocks. Net exposure can range from net long to market neutral.
- **Market Neutral:** Targets zero beta to the market. Returns driven by stock selection alpha, not market direction.
- **Global Macro:** Takes positions in currencies, rates, equities, and commodities based on macroeconomic views. Highly discretionary.
- **Event-Driven:** Profits from corporate events — mergers (merger arbitrage), restructurings, spinoffs, bankruptcies.
- **Relative Value:** Exploits pricing discrepancies between related securities (convertible arbitrage, fixed income arbitrage, capital structure arbitrage).
- **Managed Futures/CTA:** Systematic trend-following strategies across futures markets. Historically provide positive convexity (perform well in crises).

### Fee Structures
The standard hedge fund fee is "2-and-20" — 2% annual management fee on AUM plus 20% performance fee on profits.

- **High-water mark:** Performance fees are only charged on new profits above the previous peak NAV. Protects investors from paying fees to recover losses.
- **Hurdle rate:** A minimum return (often a risk-free rate) that must be exceeded before performance fees apply.
- **Clawback:** Mechanism to recover performance fees if subsequent losses erode earlier gains (more common in PE).

### Private Equity Metrics
- **IRR (Internal Rate of Return):** The discount rate that sets the NPV of all cash flows (capital calls and distributions) to zero. Time-weighted, accounts for the timing of cash flows.
- **TVPI (Total Value to Paid-In):** (Distributions + Remaining Value) / Total Capital Called. A multiple of invested capital.
- **DPI (Distributions to Paid-In):** Distributions / Total Capital Called. Measures realized returns only — the "cash-on-cash" multiple.
- **RVPI (Residual Value to Paid-In):** Remaining Value / Total Capital Called. Measures unrealized value. TVPI = DPI + RVPI.

### J-Curve
Private equity funds typically show negative returns in the early years because management fees are charged on committed capital, initial investments are carried at cost or slightly written down, and returns have not yet materialized. As portfolio companies mature and are exited, returns improve. The characteristic shape — initial losses followed by gains — resembles the letter J.

### Vintage Year Diversification
PE fund performance is significantly influenced by the economic environment at the time of investment. Spreading commitments across multiple vintage years reduces the risk of investing all capital at unfavorable valuations.

### Illiquidity Premium
The expected excess return demanded for accepting illiquidity — the inability to sell quickly at fair value. Private equity, venture capital, and certain hedge funds impose lock-up periods (1-10+ years). The illiquidity premium is theoretically 150-400bp for PE and private credit, though estimates vary and are debated.

### Lock-Up Periods, Gates, and Side Pockets
- **Lock-up:** Period during which investors cannot redeem (typically 1-3 years for hedge funds, 7-12 years for PE).
- **Gates:** Limits on the percentage of fund assets that can be redeemed in any single period (e.g., 10-25% per quarter).
- **Side pockets:** Illiquid or hard-to-value positions segregated from the main portfolio. Investors cannot redeem side-pocketed assets until they are realized.

### Replication and Factor Exposure
Many hedge fund returns can be replicated with systematic factor exposure (equity market, size, value, momentum, credit, volatility selling). Research shows that a significant portion of hedge fund "alpha" is actually alternative beta — compensation for well-known risk factors. True alpha (manager skill net of factor exposure) is scarce and diminishing.

### Due Diligence
Key areas: operational risk (back-office, custody, valuation practices), strategy capacity (can the strategy scale?), manager skill vs factor exposure, transparency and reporting, alignment of interests, and regulatory compliance.

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| Management Fee | AUM × Management Fee Rate | Annual fee on assets |
| Performance Fee | max(0, Gains Above HWM) × Perf Fee Rate | Fee on profits |
| Net Return (2-and-20) | Gross Return - 2% - 20% × max(0, Gross - Hurdle) | After-fee return |
| TVPI | (Distributions + NAV) / Paid-In Capital | Total return multiple |
| DPI | Distributions / Paid-In Capital | Realized return multiple |
| RVPI | NAV / Paid-In Capital | Unrealized return multiple |
| IRR | Rate r: sum CF_t/(1+r)^t = 0 | Time-adjusted return |

## Worked Examples

### Example 1: Fee Drag on a Hedge Fund
**Given:** $10M invested, gross return = 8%, 2% management fee, 20% performance fee, no hurdle rate
**Calculate:** Net return and fee drag
**Solution:**
Management fee = $10M × 2% = $200,000
Gross profit = $10M × 8% = $800,000
Performance fee = ($800,000 - $200,000 is NOT how it works; fees are typically calculated independently)
Performance fee = 20% × $800,000 = $160,000
Total fees = $200,000 + $160,000 = $360,000
Net return = ($800,000 - $360,000) / $10,000,000 = 4.4%
Fee drag = 8.0% - 4.4% = 3.6 percentage points

The investor keeps 4.4% of the 8.0% gross return. Fees consume 45% of gross returns in this example. At lower gross returns, the fee drag as a percentage becomes even more severe.

### Example 2: Private Equity J-Curve and Multiples
**Given:** A PE fund calls $2M/year for 5 years (total $10M). Distributions: Year 4 = $1M, Year 5 = $3M, Year 6 = $5M, Year 7 = $8M, Year 8 = $4M. No residual value after Year 8.
**Calculate:** DPI, TVPI, and approximate IRR
**Solution:**
Total distributions = $1M + $3M + $5M + $8M + $4M = $21M
Total paid-in = $2M × 5 = $10M
DPI = $21M / $10M = 2.1x
TVPI = (21M + 0) / $10M = 2.1x (no residual, so TVPI = DPI)

Cash flows for IRR: Year 1: -$2M, Year 2: -$2M, Year 3: -$2M, Year 4: -$2M + $1M = -$1M, Year 5: -$2M + $3M = +$1M, Year 6: +$5M, Year 7: +$8M, Year 8: +$4M
Solving for IRR numerically yields approximately 18-20%.

The J-curve is visible: negative net cash flows in years 1-4, turning positive in year 5, with the bulk of value returned in years 6-7.

## Common Pitfalls
- IRR manipulation through subscription credit lines — borrowing at the fund level delays capital calls, artificially boosting early IRR without improving actual returns
- Survivorship and backfill bias in hedge fund databases — failed funds are removed and new entrants can backfill historical returns, inflating reported industry performance
- Illiquidity masking true volatility — PE and hedge fund returns are based on appraisals or marks, which smooth reported volatility and understate true risk
- Comparing PE IRR directly to public market time-weighted returns — use PME (Public Market Equivalent) for an apples-to-apples comparison

## Cross-References
- **historical-risk** (wealth-management plugin, Layer 1a): return measurement and risk-adjusted performance
- **equities** (wealth-management plugin, Layer 2): long/short equity strategies and factor exposures
- **fixed-income-corporate** (wealth-management plugin, Layer 2): private credit and leveraged loan markets
- **performance-attribution** (wealth-management plugin, Layer 5): evaluating manager alpha vs factor beta

## Reference Implementation
N/A — this skill is qualitative and does not require a computational script.
