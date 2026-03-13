---
name: real-assets
description: "Analyze real estate and infrastructure investments including REITs, direct property valuation, and infrastructure assets. Use when the user asks about real estate investing, REITs, cap rates, NOI, FFO, AFFO, property valuation, or infrastructure investments. Also trigger when users mention 'rental property analysis', 'cash-on-cash return', 'gross rent multiplier', 'REIT dividends', 'real estate sectors', 'cell towers', 'toll roads', 'LTV ratio', 'DSCR', or ask whether to invest in real estate directly or through REITs."
---

# Real Assets

## Purpose
Analyze real estate and infrastructure investments including REITs, direct property, and infrastructure assets. This skill covers property valuation using NOI and cap rates, REIT-specific metrics (FFO, AFFO), leverage analysis, and the stable cash flow characteristics of infrastructure investments.

## Layer
2 — Asset Classes

## Direction
both

## When to Use
- User asks about real estate investing, property valuation, or REITs
- User asks about cap rates, NOI, or cash-on-cash returns
- User asks about REIT valuation (FFO, AFFO, P/FFO)
- User asks about real estate sectors (residential, office, industrial, etc.)
- User asks about infrastructure investments (toll roads, utilities, pipelines, cell towers)
- User asks about leverage in real estate (LTV, DSCR)
- User asks about gross rent multiplier or property-level return analysis

## Core Concepts

### Net Operating Income (NOI)
NOI = Gross Rental Income - Operating Expenses

Operating expenses include property taxes, insurance, maintenance, management fees, and utilities (if paid by the landlord). NOI excludes debt service (mortgage payments), capital expenditures, and depreciation. NOI is the core measure of property-level income before financing and taxes.

### Cap Rate
Cap Rate = NOI / Property Value

The capitalization rate represents the unlevered yield on a property. It is the real estate equivalent of an earnings yield. Lower cap rates imply higher valuations (and vice versa). Cap rates vary by property type, location, and market conditions.

### Property Valuation
Value = NOI / Cap Rate

This is the income approach to real estate valuation. Given a property's NOI and the prevailing cap rate for comparable properties, the value is derived by dividing NOI by the cap rate.

### Cash-on-Cash Return
Cash-on-Cash Return = Annual Pre-Tax Cash Flow / Total Cash Invested

This measures the return on the investor's actual equity investment, after debt service. It accounts for leverage, unlike the cap rate which is unlevered.

### Gross Rent Multiplier (GRM)
GRM = Property Price / Gross Annual Rental Income

A quick screening metric. Lower GRM suggests better value. Does not account for operating expenses, vacancies, or financing.

### REITs (Real Estate Investment Trusts)
REITs must distribute 90%+ of taxable income as dividends, making them high-income vehicles. They trade on exchanges like equities, providing liquidity that direct real estate lacks. REIT sectors include residential, office, retail, industrial, data center, healthcare, self-storage, and specialty.

### FFO (Funds From Operations)
FFO = Net Income + Depreciation/Amortization - Gains on Property Sales

FFO adds back depreciation because real estate depreciation (a non-cash charge) often overstates the actual decline in property value. FFO is the standard earnings measure for REITs, replacing net income.

### AFFO (Adjusted Funds From Operations)
AFFO = FFO - Maintenance Capital Expenditures - Straight-Line Rent Adjustments

AFFO is a more conservative and accurate measure of a REIT's recurring cash flow available for distribution. It accounts for the capital needed to maintain properties in their current condition.

### REIT Valuation Metrics
- P/FFO: the REIT equivalent of P/E. Compare across peers within the same sector.
- P/AFFO: more conservative than P/FFO, accounts for maintenance capex.
- NAV (Net Asset Value): value of underlying properties minus liabilities. Premium/discount to NAV indicates market sentiment.

### Infrastructure Investments
Infrastructure assets include toll roads, utilities, pipelines, cell towers, airports, and ports. Characteristics include long asset lives, high barriers to entry, regulated or contracted revenue streams, and inflation-linked cash flows (many contracts include CPI adjustments). Infrastructure provides stable, bond-like income with equity-like upside from traffic/usage growth.

### Leverage in Real Estate
- **LTV (Loan-to-Value):** Mortgage amount / Property value. Higher LTV means more leverage and more risk. Typical commercial LTV is 60-75%.
- **DSCR (Debt Service Coverage Ratio):** NOI / Annual Debt Service. Lenders typically require DSCR of 1.20x-1.50x minimum. Higher DSCR means more cushion to service debt.

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| NOI | Gross Rental Income - Operating Expenses | Property income measure |
| Cap Rate | NOI / Property Value | Unlevered property yield |
| Property Value | NOI / Cap Rate | Income-based valuation |
| Cash-on-Cash | Annual Cash Flow / Total Cash Invested | Levered equity return |
| GRM | Price / Gross Annual Rent | Quick screening metric |
| FFO | Net Income + Depreciation - Gains on Sales | REIT earnings measure |
| AFFO | FFO - Maintenance Capex - Straight-Line Rent Adj | Recurring cash flow |
| LTV | Loan Amount / Property Value | Leverage measure |
| DSCR | NOI / Annual Debt Service | Debt coverage measure |

## Worked Examples

### Example 1: Property Valuation Using Cap Rate
**Given:** NOI = $100,000 per year, prevailing cap rate for comparable properties = 6%
**Calculate:** Property value
**Solution:**
Value = NOI / Cap Rate = $100,000 / 0.06 = $1,666,667

The property is valued at approximately $1,666,667. If the cap rate compressed to 5% (e.g., in a hot market), the value would rise to $2,000,000 — a 20% increase from a 100bp cap rate decline. This illustrates the sensitivity of real estate values to cap rate changes.

### Example 2: Cash-on-Cash Return with Leverage
**Given:** Property value = $500,000, down payment = $200,000 (40%), mortgage = $300,000 at 6%, NOI = $35,000, annual debt service = $17,000
**Calculate:** Cash-on-cash return
**Solution:**
Annual pre-tax cash flow = NOI - Debt Service = $35,000 - $17,000 = $18,000
Cash-on-Cash Return = $18,000 / $200,000 = 9.0%

Compare to the unlevered cap rate: $35,000 / $500,000 = 7.0%. Leverage boosts the equity return from 7.0% to 9.0% because the cost of debt (6%) is below the cap rate (7.0%) — this is positive leverage. If the mortgage rate exceeded the cap rate, leverage would reduce returns (negative leverage).

## Common Pitfalls
- Confusing cap rate with total return — cap rate ignores appreciation, leverage effects, and capital expenditures
- Using P/E instead of P/FFO for REITs — depreciation distorts net income, making P/E misleading for real estate companies
- Ignoring vacancy rates in NOI calculation — always use effective gross income (after vacancy allowance), not gross potential rent
- Overstating returns by ignoring maintenance capex — use AFFO rather than FFO for a realistic view of distributable cash flow

## Cross-References
- **time-value-of-money** (core plugin, Layer 0): discounted cash flow analysis of property investments
- **equities** (wealth-management plugin, Layer 2): REIT stock analysis and equity market context
- **fixed-income-structured** (wealth-management plugin, Layer 2): MBS and the mortgage market underlying real estate
- **asset-allocation** (wealth-management plugin, Layer 3): real assets as a portfolio diversifier and inflation hedge

## Reference Implementation
See `scripts/real_assets.py` for computational helpers.
