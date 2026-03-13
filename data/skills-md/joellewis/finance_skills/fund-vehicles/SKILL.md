---
name: fund-vehicles
description: "Compare and select investment vehicles including mutual funds, ETFs, index funds, and separately managed accounts. Use when the user asks about ETF vs mutual fund, expense ratios, fund tax efficiency, ETF creation/redemption, tracking error, or share class comparisons. Also trigger when users mention 'which fund should I buy', 'Vanguard vs Fidelity', 'index fund costs', '12b-1 fees', 'load vs no-load', 'SMA vs ETF', 'fund turnover ratio', 'securities lending', or ask how fees compound over time."
---

# Fund Vehicles

## Purpose
Analyze and compare investment vehicles including mutual funds, ETFs, index funds, and separately managed accounts (SMAs). This skill covers expense ratio analysis, tax efficiency comparisons, the ETF creation/redemption mechanism, fund selection criteria, and the long-term impact of fees on wealth accumulation.

## Layer
2 — Asset Classes

## Direction
both

## When to Use
- User asks about comparing fund types (ETF vs mutual fund vs SMA)
- User asks about expense ratios, fee analysis, or cost impact on returns
- User asks about ETF mechanics (creation/redemption, premiums/discounts)
- User asks about tax efficiency of different investment vehicles
- User asks about index fund tracking error or tracking difference
- User asks about fund selection criteria or share class comparisons
- User asks about 12b-1 fees, loads, or hidden fund costs
- User asks about securities lending revenue in funds

## Core Concepts

### Mutual Funds
Pooled investment vehicles priced at Net Asset Value (NAV) once daily at market close. Investors buy and sell shares directly from the fund at the NAV. Capital gains are distributed to all shareholders (creating taxable events even for buy-and-hold investors). Available in active and passive strategies.

### ETFs (Exchange-Traded Funds)
Trade on exchanges throughout the day like stocks. Priced at market price, which may differ slightly from NAV (premiums or discounts). Generally more tax-efficient than mutual funds due to the in-kind creation/redemption mechanism that avoids realizing capital gains. Lower expense ratios on average.

### Index Funds
Passively replicate a benchmark index, whether structured as mutual funds or ETFs. Extremely low cost (expense ratios as low as 0.01-0.05%). Tracking error arises from sampling, cash drag, rebalancing timing, and expenses. The primary value proposition is low cost and broad diversification.

### SMAs (Separately Managed Accounts)
The investor directly owns individual securities, rather than shares of a pooled fund. Benefits include direct tax-loss harvesting (sell specific lots), customization (exclude specific stocks or sectors), and transparency. Higher minimums (typically $100K-$1M+) and potentially higher fees than index ETFs.

### Expense Ratios
Total annual cost as a percentage of AUM, deducted from fund returns. Includes management fees, administrative costs, and sometimes 12b-1 distribution fees. The expense ratio is the single most predictive factor of future fund performance — lower-cost funds consistently outperform higher-cost funds within the same category.

### Tracking Difference
The actual return gap between a fund and its benchmark index over a period. Tracking difference = Fund Return - Index Return. Expense ratio is a floor for tracking difference, but additional factors (securities lending income, sampling, cash drag, trading costs) can make tracking difference better or worse than the expense ratio.

### Tax Efficiency
The general hierarchy: ETFs > index mutual funds > actively managed mutual funds.

ETFs are more tax-efficient because the creation/redemption mechanism allows authorized participants to exchange baskets of stocks for ETF shares (and vice versa) in-kind, avoiding the realization of capital gains. Mutual funds must sell securities to meet redemptions, potentially triggering gains distributed to remaining shareholders.

### Creation/Redemption Mechanism
Authorized Participants (APs) create new ETF shares by delivering a basket of the underlying securities to the fund in exchange for ETF shares (creation). To redeem, APs return ETF shares and receive the underlying securities. These in-kind transfers do not trigger capital gains, which is the key to ETF tax efficiency.

### Share Classes
Mutual funds may offer multiple share classes with different fee structures:
- **Institutional shares:** Lower expense ratios, higher minimums
- **Retail shares:** Higher expense ratios, lower minimums
- **Load shares:** Front-end load (paid at purchase) or back-end load/CDSC (paid at redemption)
- **No-load shares:** No sales charges

### Securities Lending Revenue
Funds can lend their holdings to short sellers in exchange for a fee. This revenue can partially or fully offset fund expenses, sometimes resulting in tracking difference better than the expense ratio. Large index funds are major securities lenders.

### Turnover Ratio
Measures how frequently a fund buys and sells its holdings. Higher turnover leads to more taxable capital gains distributions, higher transaction costs, and greater market impact. Typical turnover: index funds 3-10%, active funds 50-200%+.

### 12b-1 Fees and Loads
- **12b-1 fees:** Annual distribution and marketing fees (0.25-1.0%), included in the expense ratio. Named after the SEC rule that permits them.
- **Front-end loads:** One-time sales charge at purchase (typically 3-5.75%), reducing the initial investment
- **Back-end loads (CDSCs):** Contingent Deferred Sales Charges, paid upon redemption. Typically decline over a holding period (e.g., 5% in year 1, declining to 0% after 5-7 years).

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| Expense Drag (annual) | AUM × Expense Ratio | Annual cost of fund ownership |
| Tracking Difference | Fund Return - Index Return | Actual cost of indexing |
| Fee Impact (compounded) | FV = PV × (1 + r - ER)^n vs PV × (1 + r)^n | Long-term fee drag |
| Tax Cost Ratio | Pre-Tax Return - After-Tax Return | Tax efficiency measure |
| NAV | (Total Assets - Liabilities) / Shares Outstanding | Fund share value |

## Worked Examples

### Example 1: Long-Term Fee Impact
**Given:** $100,000 invested for 30 years at 8% gross return. Fund A: 0.03% expense ratio. Fund B: 0.75% expense ratio.
**Calculate:** Final values and fee drag for each fund
**Solution:**
Fund A: $100,000 × (1 + 0.08 - 0.0003)^30 = $100,000 × (1.0797)^30 = $976,611
Fund B: $100,000 × (1 + 0.08 - 0.0075)^30 = $100,000 × (1.0725)^30 = $816,627
Difference: $976,611 - $816,627 = $159,984

The 0.72% annual fee difference (0.75% - 0.03%) compounds to $159,984 over 30 years — approximately 16% of the low-cost fund's terminal value. This is wealth destroyed by fees for an identical gross return.

### Example 2: ETF vs Mutual Fund Tax Efficiency
**Given:** Identical S&P 500 portfolios. ETF distributes $0 in capital gains (uses in-kind redemptions). Mutual fund distributes 2% of NAV in capital gains annually. Investor is in the 20% LTCG bracket. Both have 0.03% expense ratio. Gross return 10%.
**Calculate:** After-tax return differential over 20 years on $100,000
**Solution:**
ETF: Gains are deferred. After-tax return ≈ 10% - 0.03% = 9.97% annually until sale.
After 20 years: $100,000 × (1.0997)^20 = $668,965
Tax on liquidation: ($668,965 - $100,000) × 20% = $113,793
After-tax value: $668,965 - $113,793 = $555,172

Mutual fund: 2% distribution taxed annually. Net of tax on distributions: 10% - (2% × 20%) = 10% - 0.4% = 9.6% effective annual return (simplified).
After 20 years: $100,000 × (1.096)^20 = $627,641
Remaining gain tax: estimated tax on sale of appreciated but partially-taxed holdings ≈ lower.
Approximate after-tax value: ~$535,000-$545,000

The ETF's tax deferral advantage is worth approximately $10,000-$20,000 over 20 years on this $100,000 investment.

## Common Pitfalls
- Ignoring tracking difference — it can be worse than the expense ratio due to cash drag, sampling, and trading costs
- Not considering tax efficiency when comparing returns — pre-tax fund returns overstate what taxable investors actually keep
- Confusing NAV with market price for ETFs — ETFs can trade at premiums or discounts to NAV, especially in volatile markets or for illiquid underlying assets
- Overlooking securities lending income that offsets expenses — some index funds achieve tracking difference better than their expense ratio

## Cross-References
- **equities** (wealth-management plugin, Layer 2): equity fund selection and equity index tracking
- **fixed-income-sovereign** (wealth-management plugin, Layer 2): bond fund considerations (see also **fixed-income-corporate**)
- **tax-efficiency** (wealth-management plugin, Layer 5): comprehensive after-tax investment analysis
- **portfolio-construction** (wealth-management plugin, Layer 3): selecting vehicles within an asset allocation

## Reference Implementation
See `scripts/fund_vehicles.py` for computational helpers.
