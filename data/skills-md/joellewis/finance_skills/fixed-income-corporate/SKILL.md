---
name: fixed-income-corporate
description: "Analyze corporate bonds and credit instruments including investment grade and high yield debt. Use when the user asks about corporate bonds, credit spreads (OAS, Z-spread, G-spread), credit ratings, default probabilities, callable bonds, or private credit. Also trigger when users mention 'junk bonds', 'fallen angel', 'yield-to-worst', 'covenant analysis', 'CDS spreads', 'recovery rates', 'direct lending', 'mezzanine debt', 'BBB downgrade risk', or ask how to evaluate corporate credit risk."
---

# Fixed Income — Corporate

## Purpose
Analyze corporate bonds and credit instruments including investment grade and high yield debt. This skill covers credit spread measurement (G-spread, Z-spread, OAS), credit rating frameworks, default and recovery analysis, callable bond structures, covenant analysis, and private credit fundamentals.

## Layer
2 — Asset Classes

## Direction
both

## When to Use
- User asks about corporate debt, corporate bonds, or credit risk
- User asks about credit spreads (OAS, Z-spread, G-spread)
- User asks about credit ratings, rating migration, or default probabilities
- User asks about investment grade vs high yield bonds
- User asks about callable bonds, yield-to-call, or yield-to-worst
- User asks about covenants, recovery rates, or loss given default
- User asks about private credit, direct lending, or mezzanine debt
- User asks about CDS (Credit Default Swaps) or market-implied default probabilities

## Core Concepts

### Credit Spreads
Compensation for default risk, liquidity risk, and downgrade risk above the risk-free rate. Multiple spread measures exist with increasing precision:

**G-spread (Government Spread):** Bond yield minus interpolated Treasury yield of the same maturity. Simple but assumes a flat term structure between benchmark maturities.

**Z-spread (Zero-Volatility Spread):** The constant spread added to each point on the risk-free spot rate curve such that the sum of discounted cash flows equals the bond's market price. Superior to G-spread because it accounts for the full shape of the term structure.

**OAS (Option-Adjusted Spread):** For bonds with embedded options, OAS = Z-spread minus the value of the embedded option. OAS represents the "true" credit compensation after removing the option component. Requires an interest rate model to compute.

### Credit Ratings
AAA/AA/A/BBB are investment grade. BB/B/CCC/CC/C/D are high yield (speculative grade). The BBB/BB boundary is the most consequential threshold — many institutional mandates prohibit sub-investment-grade holdings. A downgrade across this boundary ("fallen angel") forces selling by constrained investors.

### Migration Matrix
A transition matrix shows the probability of moving from one rating to another over a 1-year horizon. A BBB-rated issuer has roughly 85-90% probability of remaining BBB, 4-5% chance of upgrade, 4-5% chance of downgrade, and a small probability (~0.2%) of default. Migration matrices are published annually by rating agencies.

### Default Probability, Loss Given Default, and Recovery Rate
- PD = Probability of Default over a given horizon
- LGD = Loss Given Default (percentage of exposure lost)
- Recovery Rate (RR) = 1 - LGD
- Expected Loss: EL = PD × LGD × EAD (Exposure at Default)

Recovery rates vary by seniority: senior secured (60-65%), senior unsecured (40-50%), subordinated (20-30%).

### Callable Bonds
The issuer can redeem the bond early. Call schedules specify prices and dates. Yield-to-call (YTC) is calculated using the call date and call price. Yield-to-worst (YTW) is the minimum of YTM and all possible YTCs. For callable bonds, OAS is the appropriate spread measure (not G-spread or Z-spread).

### Covenants
**Maintenance covenants:** Tested periodically (e.g., quarterly). Issuer must maintain financial ratios at all times. Common in bank loans.

**Incurrence covenants:** Tested only when the issuer takes a specific action (e.g., issues new debt). Common in bond indentures. Key covenants include leverage ratio (Debt/EBITDA), interest coverage (EBITDA/Interest), and restricted payments.

### Private Credit
Direct lending by non-bank lenders to middle-market companies. Offers an illiquidity premium of 150-400bp over comparable syndicated loans. Typically features stronger covenant protection than public market deals. Valuations are mark-based (quarterly), which smooths reported volatility.

### CDS (Credit Default Swaps)
A derivative where the protection buyer pays a periodic spread and receives payment upon a credit event. CDS spreads can be used to derive market-implied default probabilities. CDS spreads are often more responsive to credit deterioration than bond spreads.

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| G-spread | Bond Yield - Interpolated Treasury Yield | Simple spread measure |
| Z-spread | Constant spread s: P = sum CF_t / (1+s_t+s)^t | Full curve spread |
| OAS | Z-spread - Option Cost | Spread for callable bonds |
| Expected Loss | EL = PD × LGD × EAD | Credit loss estimation |
| Recovery Rate | RR = 1 - LGD | Recovery from default |
| Yield-to-Worst | min(YTM, YTC_1, YTC_2, ...) | Conservative yield measure |

## Worked Examples

### Example 1: Compare Z-spread vs G-spread
**Given:** A 7-year corporate bond yields 5.8%. The 7-year interpolated Treasury yield is 4.5%. The Z-spread (computed using the full spot curve) is 118bp.
**Calculate:** G-spread and compare to Z-spread
**Solution:**
G-spread = 5.8% - 4.5% = 1.30% = 130bp
Z-spread = 118bp
The G-spread (130bp) exceeds the Z-spread (118bp) by 12bp. This difference arises because the G-spread uses a single interpolated benchmark point while the Z-spread properly accounts for the shape of the entire yield curve. In a steep curve environment, G-spread tends to overstate the true spread.

### Example 2: Expected Loss Calculation
**Given:** PD = 2% (annual), LGD = 60%, EAD = $1,000,000
**Calculate:** Expected annual loss
**Solution:**
EL = PD × LGD × EAD
EL = 0.02 × 0.60 × $1,000,000
EL = $12,000

The expected annual credit loss is $12,000, or 1.2% of the exposure. This represents the actuarial cost of credit risk — the spread must at least cover this expected loss, with additional compensation for unexpected losses and risk aversion.

## Common Pitfalls
- Using G-spread for callable bonds — use OAS instead, which removes the option component
- Ignoring liquidity premium in spread analysis — part of the spread compensates for illiquidity, not just default risk
- Rating agency lag vs market-implied credit quality — CDS spreads often move before rating actions
- Assuming recovery rates are constant — they vary significantly by seniority and economic cycle (lower in recessions)

## Cross-References
- **fixed-income-sovereign** (wealth-management plugin, Layer 2): the Treasury curve used as the risk-free benchmark
- **fixed-income-structured** (wealth-management plugin, Layer 2): CLOs and structured credit products
- **alternatives** (wealth-management plugin, Layer 2): private credit as an alternative investment
- **portfolio-construction** (wealth-management plugin, Layer 3): credit allocation in multi-asset portfolios

## Reference Implementation
See `scripts/fixed_income_corporate.py` for computational helpers.
