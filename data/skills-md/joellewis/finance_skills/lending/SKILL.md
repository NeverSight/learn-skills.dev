---
name: lending
description: "Analyze lending products including mortgages, HELOCs, and personal loans with amortization and comparison tools. Use when the user asks about mortgage comparison, fixed vs ARM rates, loan qualification, amortization schedules, extra payments, or buying points. Also trigger when users mention 'monthly payment calculation', '15-year vs 30-year mortgage', 'PMI', 'APR vs interest rate', 'HELOC', 'home equity', 'should I buy down the rate', 'biweekly payments', or ask how much house they can afford."
---

# Lending Analysis

## Purpose
Analyze lending products including mortgages, HELOCs, and personal loans. This skill covers loan comparison, qualification assessment, fixed vs adjustable rate analysis, amortization with extra payments, and home equity line of credit evaluation.

## Layer
6 — Personal Finance

## Direction
both

## When to Use
- Shopping for a mortgage and comparing loan offers (fixed vs ARM, 15-year vs 30-year)
- Computing monthly payments, total interest, and amortization schedules
- Evaluating the impact of extra principal payments on loan term and interest savings
- Deciding whether to buy points (prepaid interest) and computing breakeven
- Comparing APR vs interest rate across loan offers
- Assessing loan qualification (FICO, DTI, LTV, reserves)
- Analyzing HELOC options and combined loan-to-value ratios
- Evaluating PMI costs and strategies to eliminate PMI

## Core Concepts

### Fixed-Rate Mortgage
The interest rate and monthly payment remain constant for the life of the loan:

- **Advantages:** Predictable payments, protection against rising rates, simpler budgeting
- **Disadvantages:** Higher initial rate than ARM, no benefit if rates decline (must refinance)
- Most common terms: 30-year and 15-year fixed

### Adjustable-Rate Mortgage (ARM)
Rate is fixed for an initial period, then adjusts periodically based on an index plus a margin:

- **Notation:** 5/1 ARM = fixed for 5 years, adjusts annually thereafter; 7/1, 10/1 similarly
- **Fully indexed rate:** Index (e.g., SOFR, 1-year Treasury) + margin (e.g., 2.75%)
- **Rate caps** protect against extreme adjustments:
  - Initial adjustment cap (e.g., 2%): maximum first adjustment
  - Periodic cap (e.g., 2%): maximum change per adjustment period
  - Lifetime cap (e.g., 5%): maximum total increase over initial rate
- **When ARM may be appropriate:** Planning to sell or refinance before the fixed period ends, expecting rates to decline, or comfortable with rate variability

### Monthly Payment Calculation
The standard amortization formula for a fixed-rate loan:

- PMT = P × [r(1+r)^n] / [(1+r)^n - 1]
- Where: P = principal (loan amount), r = monthly interest rate (annual rate / 12), n = total number of payments (term in months)
- Each payment splits into interest (decreasing) and principal (increasing) components:
  - Interest portion: remaining balance × monthly rate
  - Principal portion: PMT - interest portion

### Total Interest Paid
- Total interest = (n × PMT) - P
- For a $400K, 30-year loan at 6.5%: PMT = $2,528, total payments = $910,178, total interest = $510,178

### Extra Payments
Additional principal payments reduce the outstanding balance, shorten the loan term, and reduce total interest:

- Each extra dollar goes entirely to principal reduction
- Impact compounds: earlier extra payments save more interest than later ones
- Methods: lump sum, fixed monthly extra, biweekly payments (26 half-payments = 13 full payments per year)

### Mortgage Points
Prepaid interest that reduces the loan's interest rate:

- **1 point = 1% of the loan amount** (e.g., 1 point on $400K = $4,000)
- Typically reduces the rate by approximately 0.25% (varies by lender and market)
- **Breakeven calculation:** Points cost / monthly savings = months to recoup
- Points make sense when: planning to hold the loan beyond breakeven, itemizing deductions (points may be tax-deductible in year of purchase)

### APR vs Interest Rate
- **Interest rate:** The cost of borrowing the principal, expressed annually
- **APR (Annual Percentage Rate):** Includes the interest rate plus certain fees and costs (origination fees, points, PMI), annualized over the loan term
- **APR > interest rate** (always, when there are fees)
- APR is the better metric for comparing loan offers with different fee structures

### HELOC (Home Equity Line of Credit)
A revolving credit line secured by home equity:

- **Combined LTV (CLTV):** (First mortgage balance + HELOC limit) / home value
  - Most lenders require CLTV ≤ 80-90%
- **Draw period** (typically 10 years): borrow and repay flexibly, often interest-only payments
- **Repayment period** (typically 20 years): no new draws, fully amortizing payments
- **Variable rate:** Typically prime rate + margin; rate fluctuates with market
- **Use cases:** Home improvements, debt consolidation, emergency backup (but not as primary emergency fund)
- **Risk:** Home is collateral — default means foreclosure

### Loan Qualification Criteria
- **FICO score:** 620+ for conventional, 580+ for FHA, 700+ for best rates
- **DTI:** Front-end ≤ 28%, back-end ≤ 36-43% (varies by program)
- **LTV (Loan-to-Value):** Loan amount / property value; lower LTV = lower risk = better terms
- **Reserves:** Months of payments held in liquid assets after closing (2-6 months typical)
- **Employment/income:** Stable income history, typically 2 years documentation

### PMI (Private Mortgage Insurance)
Required when conventional loan LTV exceeds 80%:

- **Cost:** 0.5-1.5% of loan amount annually, added to monthly payment
- **Removal:** Automatic at 78% LTV (based on original amortization), requestable at 80% LTV
- **Avoidance strategies:** 20% down payment, piggyback loan (80/10/10), lender-paid PMI (higher rate), VA loan (no PMI)
- PMI benefits the lender, not the borrower — it is pure cost to the borrower

### 15-Year vs 30-Year Comparison
- **15-year:** Higher monthly payment, lower interest rate (typically 0.5-0.75% less), dramatically less total interest, builds equity faster
- **30-year:** Lower required payment, more flexibility, higher total interest cost
- **Hybrid approach:** Take a 30-year for flexibility, make extra payments as if it were a 15-year

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| Monthly payment | PMT = P × [r(1+r)^n] / [(1+r)^n - 1] | Fixed-rate loan payment |
| Total interest | n × PMT - P | Total cost of borrowing |
| Remaining balance after k payments | B_k = P × [(1+r)^n - (1+r)^k] / [(1+r)^n - 1] | Balance at any point |
| Points breakeven | Cost of points / monthly savings | Months to recoup points |
| LTV | Loan amount / property value | Risk and PMI assessment |
| CLTV | (First mortgage + HELOC) / home value | Combined leverage |
| ARM fully indexed rate | Index + margin | Rate after fixed period |

## Worked Examples

### Example 1: 30-year vs 15-year mortgage comparison
**Given:** Home price $500K, down payment $100K, loan amount $400K. 30-year rate: 6.5%. 15-year rate: 5.9%.
**Calculate:** Monthly payments, total interest, and interest savings.
**Solution:**
1. **30-year monthly payment:** PMT = $400,000 × [0.005417 × (1.005417)^360] / [(1.005417)^360 - 1]
   - r = 6.5%/12 = 0.005417, n = 360
   - PMT = **$2,528/month**
2. **30-year total interest:** 360 × $2,528 - $400,000 = **$510,178**
3. **15-year monthly payment:** PMT = $400,000 × [0.004917 × (1.004917)^180] / [(1.004917)^180 - 1]
   - r = 5.9%/12 = 0.004917, n = 180
   - PMT = **$3,357/month**
4. **15-year total interest:** 180 × $3,357 - $400,000 = **$204,299**
5. **Payment difference:** $3,357 - $2,528 = **$829/month more** for 15-year.
6. **Interest savings:** $510,178 - $204,299 = **$305,879 saved** by choosing 15-year.
7. The 15-year costs 33% more per month but saves 60% in total interest.

### Example 2: Extra payment impact
**Given:** $300K 30-year mortgage at 6.5% (payment = $1,896/mo). Borrower adds $200/month extra to principal.
**Calculate:** Years saved and interest saved.
**Solution:**
1. **Without extra payments:** 30 years (360 months), total interest = $282,632.
2. **With $200/month extra ($2,096 total):** Solve for n: n = -ln(1 - ($300,000 × 0.005417) / $2,096) / ln(1.005417)
   - n ≈ 274 months = **22.8 years** (saves ~7.2 years).
3. **Total payments with extra:** 274 × $2,096 = $574,304. Total interest = $574,304 - $300,000 = $274,304.
4. Wait — we must account for the extra payments reducing principal faster. Using iterative amortization:
   - Actual payoff: approximately **272 months (22 years 8 months)**
   - Total interest paid: approximately **$210,000**
5. **Interest saved:** $282,632 - $210,000 ≈ **$72,600 saved** with just $200/month extra.
6. Total extra paid: 272 × $200 = $54,400. Return on extra payments: $72,600 / $54,400 = 133% return.

## Common Pitfalls
- Comparing interest rate instead of APR — APR captures fees and gives a truer cost comparison
- ARM teaser rates creating payment shock when the fixed period ends and rates adjust upward
- Points breakeven: buying points is not worth it if selling or refinancing before the breakeven point
- HELOC variable rate risk during rising rate environments — budget for rate increases
- PMI costs making high-LTV loans more expensive than they appear — factor PMI into total monthly cost
- Ignoring opportunity cost: extra mortgage payments at 3-4% vs investing at 7-10% expected return
- Not shopping multiple lenders — rate quotes can vary 0.5%+ for the same borrower
- Resetting to a 30-year term when refinancing — extends total payoff even if rate is lower
- Ignoring closing costs in refinancing decisions (see debt-management refinance breakeven)

## Cross-References
- **debt-management** (wealth-management plugin, Layer 6): refinancing analysis, debt payoff vs investing decisions, DTI calculations
- **emergency-fund** (wealth-management plugin, Layer 6): adequate reserves required for loan qualification and financial safety
- **tax-efficiency** (wealth-management plugin, Layer 5): mortgage interest deductibility, points deduction
- **savings-goals** (wealth-management plugin, Layer 6): down payment saving is a common goal-based savings target
- **liquidity-management** (wealth-management plugin, Layer 6): mortgage payments are the largest fixed obligation in most household cash flow plans

## Reference Implementation
See `scripts/lending.py` for computational helpers.
