---
name: debt-management
description: "Provide frameworks for managing and paying off personal debt effectively. Use when the user asks about debt payoff strategies (avalanche vs snowball), refinancing decisions, debt consolidation, debt-to-income ratios, or the opportunity cost of paying off debt vs investing. Also trigger when users mention 'which debt to pay first', 'should I refinance', 'credit card debt', 'student loan payoff', 'DTI for mortgage', 'balance transfer', 'good debt vs bad debt', or ask how to get out of debt faster."
---

# Debt Management

## Purpose
Provide frameworks for managing personal debt effectively, including prioritization strategies (avalanche vs snowball), refinancing decisions, debt consolidation evaluation, and debt-to-income ratio management. This skill balances mathematical optimization with behavioral psychology.

## Layer
6 — Personal Finance

## Direction
both

## When to Use
- Deciding how to prioritize paying off multiple debts
- Comparing avalanche vs snowball payoff strategies with specific debt profiles
- Evaluating whether to refinance a loan (breakeven analysis)
- Assessing debt consolidation offers
- Computing debt-to-income ratios for mortgage qualification or financial health assessment
- Deciding between paying off debt vs investing (opportunity cost analysis)
- Building a debt payoff plan with timeline and interest cost projections

## Core Concepts

### Debt Avalanche
Pay minimum payments on all debts, then direct all extra payment to the debt with the **highest interest rate** first:

- **Mathematically optimal:** Minimizes total interest paid over the life of all debts
- Once the highest-rate debt is paid off, the freed-up payment rolls to the next highest rate
- Requires discipline — the highest-rate debt may also be the largest balance, meaning slow visible progress initially
- Always saves money compared to snowball, though the difference varies by debt profile

### Debt Snowball
Pay minimum payments on all debts, then direct all extra payment to the debt with the **smallest balance** first:

- **Psychologically effective:** Quick wins build momentum and motivation
- Research (Kellogg School) shows people are more likely to stick with snowball and actually become debt-free
- May cost more in total interest than avalanche, but adherence is higher
- Best for individuals who need motivational wins to stay committed

### Debt-to-Income Ratio (DTI)
Total monthly debt payments expressed as a percentage of gross monthly income:

- **Front-end DTI (housing ratio):** Monthly housing costs (PITI: principal, interest, taxes, insurance) / gross monthly income
  - Guideline: < 28%
- **Back-end DTI (total debt ratio):** All monthly debt payments (housing + car + student loans + credit cards + other) / gross monthly income
  - Guideline: < 36% (conventional), up to 43% (FHA), some lenders allow up to 50% for qualified borrowers
- DTI is a key factor in mortgage qualification and overall financial health assessment

### Refinancing Analysis
Compare the total cost of the existing loan vs the new loan, accounting for closing costs:

- **Monthly savings:** Old payment - new payment
- **Breakeven months:** Total closing costs / monthly savings
- **Total cost comparison:** Sum of all remaining payments (old) vs sum of all payments (new) + closing costs
- If you plan to keep the loan beyond the breakeven point, refinancing saves money
- Consider: remaining term, resetting the amortization clock, and cash-out implications

### Debt Consolidation
Combine multiple debts into a single loan, ideally at a lower interest rate:

- **Potential benefits:** Lower rate, single payment, simplified management
- **Risks:** Longer term may increase total interest even at lower rate; freed-up credit lines may tempt new borrowing
- **Evaluate:** Compare total interest paid (all debts independently) vs total interest paid (consolidated loan)
- Balance transfer cards (0% intro rate) can be effective but require payoff before the rate expires

### Good Debt vs Bad Debt
- **Good debt:** Low interest rate, potentially tax-deductible, finances an appreciating asset or increases earning power (mortgage, student loans, business loans)
- **Bad debt:** High interest rate, finances depreciating assets or consumption (credit cards, payday loans, auto loans on luxury vehicles)
- The line is not absolute — a low-rate auto loan for a reliable commuter car can be reasonable

### Opportunity Cost Analysis
When debt carries a low interest rate, paying it off aggressively may not be optimal:

- **Decision rule:** If expected after-tax investment return > after-tax debt interest rate, investing the extra cash may build more wealth
- **Example:** 3.5% mortgage (2.5% after tax deduction) vs 7-10% expected equity returns — investing likely wins mathematically
- **Caveats:** Investment returns are uncertain, debt payoff is guaranteed; psychological benefit of being debt-free has real value
- Consider risk tolerance: guaranteed 3.5% return (debt payoff) vs variable 7-10% (investing)

### Debt Payoff Timeline
Amortization calculation with extra payments:

- Standard amortization: n = -ln(1 - (P×r)/PMT) / ln(1+r)
- With extra payment: replace PMT with PMT + extra, recalculate n
- Total interest = (n × PMT) - P (adjusting for extra payments)

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| Front-end DTI | Housing payments / gross monthly income | Mortgage qualification |
| Back-end DTI | All debt payments / gross monthly income | Overall debt health |
| Refinance breakeven | Closing costs / monthly savings | Months to recoup refi costs |
| Months to payoff | n = -ln(1 - Pr/PMT) / ln(1+r) | Debt payoff timeline |
| Total interest paid | (n × PMT) - Principal | Cost of borrowing |
| Effective rate (after tax) | r × (1 - marginal_tax_rate) | Tax-deductible debt comparison |

## Worked Examples

### Example 1: Avalanche vs snowball comparison
**Given:** Three debts with $500/month available for extra payments (above minimums):
- Credit card: $5,000 balance, 22% APR, $100 minimum
- Student loan: $12,000 balance, 6% APR, $200 minimum
- Personal loan: $3,000 balance, 15% APR, $75 minimum

**Calculate:** Order of payoff, total months, and total interest for each strategy.
**Solution — Avalanche (highest rate first: 22% → 15% → 6%):**
1. Pay minimums on all ($375/mo). Extra $500 goes to credit card ($600/mo total to CC).
2. Credit card ($5K at 22%, $600/mo): paid off in ~9 months, ~$450 interest.
3. Freed payment → personal loan ($75 + $600 = $675/mo to PL). Remaining ~$2,300 at 15%: paid off in ~4 months, ~$100 interest.
4. All payments → student loan ($200 + $675 = $875/mo). Remaining ~$10,400 at 6%: paid off in ~12 months, ~$350 interest.
5. **Total: ~25 months, ~$900 total interest.**

**Solution — Snowball (smallest balance first: $3K → $5K → $12K):**
1. Extra $500 goes to personal loan ($575/mo total to PL).
2. Personal loan ($3K at 15%, $575/mo): paid off in ~6 months, ~$140 interest.
3. Freed payment → credit card ($100 + $575 = $675/mo). Remaining ~$4,700 at 22%: paid off in ~8 months, ~$430 interest.
4. All payments → student loan. Remaining ~$10,200 at 6%: paid off in ~12 months, ~$340 interest.
5. **Total: ~26 months, ~$910 total interest.**

**Comparison:** Avalanche saves ~$10 and 1 month in this scenario. The difference is modest because the highest-rate debt is not the largest. Snowball gives a quicker first win (6 months vs 9 months to first payoff).

### Example 2: Refinance breakeven
**Given:** Current mortgage: $300K remaining, 6.5%, 25 years left, payment $2,028/mo. New offer: 5.5%, 25 years, closing costs $6,000, payment $1,838/mo.
**Calculate:** Breakeven period and total interest savings.
**Solution:**
1. Monthly savings: $2,028 - $1,838 = **$190/month**.
2. Breakeven: $6,000 / $190 = **31.6 months ≈ 32 months (2 years 8 months)**.
3. If staying in the home beyond 32 months, refinancing saves money.
4. Total payments (old): 25 × 12 × $2,028 = $608,400 → total interest = $608,400 - $300,000 = $308,400.
5. Total payments (new): 25 × 12 × $1,838 + $6,000 = $557,400 → total interest = $557,400 - $300,000 = $257,400.
6. **Total interest savings: $308,400 - $257,400 = $51,000.**

## Common Pitfalls
- Ignoring psychological factors — snowball works better for many people despite costing slightly more in interest
- Not including all closing costs in refinancing analysis (origination fees, appraisal, title insurance, points)
- Consolidation at a lower rate but longer term may cost more in total interest — always compare total cost
- Paying off low-rate debt instead of investing (opportunity cost) without considering risk tolerance and guaranteed vs uncertain returns
- Not considering tax deductibility of mortgage or student loan interest when comparing effective rates
- Making only minimum payments on high-interest debt while saving in low-yield accounts
- Consolidation freeing up credit lines that lead to new debt accumulation
- Ignoring the amortization reset: refinancing to a new 30-year term extends the payoff date

## Cross-References
- **lending** (wealth-management plugin, Layer 6): mortgage analysis, loan terms, and amortization calculations
- **emergency-fund** (wealth-management plugin, Layer 6): adequate emergency fund prevents taking on new high-interest debt during crises
- **savings-goals** (wealth-management plugin, Layer 6): debt payoff competes with savings goals for cash flow allocation
- **tax-efficiency** (wealth-management plugin, Layer 5): tax deductibility of certain debt interest affects optimal payoff order
- **liquidity-management** (wealth-management plugin, Layer 6): debt payments are fixed obligations in cash flow planning
- **financial-planning-workflow** (advisory-practice plugin, Layer 10): debt payoff strategies are evaluated during the cash flow and recommendation phases of financial planning

## Reference Implementation
See `scripts/debt_management.py` for computational helpers.
