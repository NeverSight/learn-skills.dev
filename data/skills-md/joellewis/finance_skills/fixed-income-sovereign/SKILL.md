---
name: fixed-income-sovereign
description: "Analyze government bonds including US Treasuries, yield curves, duration, convexity, and TIPS. Use when the user asks about Treasury bonds, sovereign debt, yield curve construction, interest rate risk, duration, convexity, TIPS, or breakeven inflation rates. Also trigger when users mention 'T-bills', 'T-notes', 'bond pricing', 'yield to maturity', 'inverted yield curve', 'forward rates', 'spot rates', 'DV01', 'real yields', or ask how bonds react to interest rate changes."
---

# Fixed Income — Sovereign

## Purpose
Analyze government bonds including US Treasuries and sovereign debt. This skill covers bond pricing, yield curve construction, duration and convexity analytics, TIPS mechanics, forward rate derivation, and auction processes critical for interest rate risk management.

## Layer
2 — Asset Classes

## Direction
both

## When to Use
- User asks about government bonds, Treasuries, or sovereign debt
- User asks about yield curves, spot rates, or forward rates
- User asks about interest rate risk, duration, or convexity
- User asks about TIPS, breakeven inflation, or real yields
- User asks about bond pricing or yield to maturity calculations
- User asks about key rate duration or yield curve shape analysis

## Core Concepts

### Bond Pricing
The price of a bond is the present value of its future cash flows:

P = sum(t=1 to n) [C / (1+y)^t] + F / (1+y)^n

where C = coupon payment per period, y = yield to maturity per period, F = face value, n = total number of periods. For semi-annual bonds, divide the annual coupon by 2 and the annual yield by 2, and double the number of years to get n.

### Yield to Maturity (YTM)
The discount rate y that solves the bond pricing equation — the single rate that equates the bond's market price to the present value of all future cash flows. Assumes reinvestment of coupons at the YTM rate. It is the standard yield measure for bonds.

### Current Yield
Current Yield = Annual Coupon / Price. A simple income measure that ignores capital gains/losses and the time value of money.

### Yield Curve: Spot Rates, Forward Rates, Par Curve
The spot curve gives zero-coupon yields for each maturity. The par curve gives coupon rates at which bonds would price at par. Forward rates are implied future rates derived from spot rates. The three curves contain equivalent information and can be derived from one another.

### Bootstrapping the Spot Curve
Extract spot (zero-coupon) rates from par yields by starting at the shortest maturity and working outward. Each step uses previously derived spot rates to solve for the next spot rate.

### Forward Rate
The implied rate between two future dates derived from spot rates:

f(t1,t2) = [(1+s_t2)^t2 / (1+s_t1)^t1]^(1/(t2-t1)) - 1

where s_t1 and s_t2 are spot rates for maturities t1 and t2.

### Duration (Macaulay)
The weighted average time to receive cash flows, where weights are the present value of each cash flow as a proportion of the bond's price:

D_mac = (1/P) × sum(t × CF_t / (1+y)^t)

Measured in years. Longer maturity, lower coupon, and lower yield all increase duration.

### Modified Duration
D_mod = D_mac / (1 + y/m)

where m = number of coupon periods per year. Gives the approximate percentage price change for a 1 percentage point change in yield: dP/P ≈ -D_mod × dy.

### Dollar Duration (DV01)
The dollar change in price for a 1 basis point change in yield:

DV01 ≈ -D_mod × P × 0.0001

Used for hedging — match DV01 exposures to immunize a portfolio against parallel rate shifts.

### Convexity
Measures the curvature of the price-yield relationship (second derivative):

C = (1/P) × sum(t(t+1) × CF_t / (1+y)^(t+2))

For option-free bonds, convexity is always positive — duration alone overstates losses and understates gains.

### Price Change Approximation
ΔP/P ≈ -D_mod × Δy + 0.5 × Convexity × (Δy)²

The convexity term is a correction that becomes important for large yield changes.

### TIPS (Treasury Inflation-Protected Securities)
Principal adjusts with CPI. The coupon rate is fixed but applied to the inflation-adjusted principal. Real yield = TIPS yield. Breakeven inflation = nominal Treasury yield - TIPS real yield. TIPS have a deflation floor that protects par value at maturity.

### Key Rate Duration
Sensitivity to specific points on the yield curve (e.g., 2yr, 5yr, 10yr, 30yr). Allows analysis of non-parallel yield curve shifts such as steepening, flattening, or butterfly moves. Sum of key rate durations equals effective duration.

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| Bond Price | P = sum C/(1+y)^t + F/(1+y)^n | Price from yield |
| Current Yield | Annual Coupon / Price | Simple income measure |
| Forward Rate | f(t1,t2) = [(1+s_t2)^t2 / (1+s_t1)^t1]^(1/(t2-t1)) - 1 | Implied future rate |
| Macaulay Duration | (1/P) × sum(t × CF_t / (1+y)^t) | Weighted avg time to cash flows |
| Modified Duration | D_mac / (1 + y/m) | % price sensitivity to yield |
| DV01 | D_mod × P × 0.0001 | Dollar price change per 1bp |
| Convexity | (1/P) × sum(t(t+1) × CF_t / (1+y)^(t+2)) | Curvature of price-yield curve |
| Price Change | ΔP/P ≈ -D_mod×Δy + 0.5×Convexity×(Δy)² | Estimate price impact of rate move |

## Worked Examples

### Example 1: Price a 5-Year 4% Semi-Annual Coupon Bond at 5% YTM
**Given:** Face = $1,000, coupon = 4% (semi-annual), YTM = 5%, maturity = 5 years
**Calculate:** Bond price
**Solution:**
Semi-annual coupon = $1,000 × 4% / 2 = $20
Semi-annual yield = 5% / 2 = 2.5%
Number of periods = 5 × 2 = 10
P = $20 × [(1 - (1.025)^(-10)) / 0.025] + $1,000 / (1.025)^10
P = $20 × 8.7521 + $1,000 × 0.7812
P = $175.04 + $781.20 = $956.24

The bond trades at a discount ($956.24 < $1,000) because the coupon rate (4%) is below the market yield (5%).

### Example 2: Modified Duration and Price Change Estimate
**Given:** A bond with Macaulay duration = 4.5 years, YTM = 5% (semi-annual), price = $956.24, convexity = 22.5
**Calculate:** Estimated price change for a +50bp rate increase
**Solution:**
D_mod = 4.5 / (1 + 0.05/2) = 4.5 / 1.025 = 4.39 years
ΔP/P ≈ -4.39 × 0.005 + 0.5 × 22.5 × (0.005)²
ΔP/P ≈ -0.02195 + 0.000281 = -0.02167 = -2.167%
ΔP ≈ -2.167% × $956.24 = -$20.72
New price ≈ $956.24 - $20.72 = $935.52

Duration alone would estimate -2.195%; the convexity correction reduces the estimated loss by about 3bp.

## Common Pitfalls
- Confusing Macaulay and modified duration — Macaulay is in years, modified gives price sensitivity
- Ignoring convexity for large yield changes — duration alone overstates losses and understates gains
- Day count conventions (30/360 vs actual/actual) — Treasuries use actual/actual, corporates use 30/360
- Clean price vs dirty price (accrued interest) — quoted prices exclude accrued interest, but settlement requires paying it

## Cross-References
- **time-value-of-money** (core plugin, Layer 0): discounting and present value fundamentals
- **fixed-income-corporate** (wealth-management plugin, Layer 2): credit spreads over the sovereign curve
- **fixed-income-municipal** (wealth-management plugin, Layer 2): muni-to-Treasury yield ratios
- **asset-allocation** (wealth-management plugin, Layer 3): bonds as an asset class in portfolio construction

## Reference Implementation
See `scripts/fixed_income_sovereign.py` for computational helpers.
