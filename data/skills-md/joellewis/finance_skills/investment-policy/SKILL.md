---
name: investment-policy
description: "Construct comprehensive Investment Policy Statements governing return objectives, risk tolerance, and portfolio constraints. Use when the user asks about building an IPS, setting return objectives, assessing risk tolerance, defining investment constraints, or establishing rebalancing and benchmark policies. Also trigger when users mention 'investment plan', 'policy portfolio', 'risk capacity vs willingness', 'spending rate for an endowment', 'foundation payout', 'manager selection criteria', or ask how to document their investment strategy."
---

# Investment Policy Statement Construction

## Purpose
Guide the construction of comprehensive Investment Policy Statements (IPS) that govern all investment decisions. This skill covers return objective setting, risk tolerance assessment, constraint identification, asset allocation policy, and ongoing review frameworks.

## Layer
5 — Policy & Planning

## Direction
prospective

## When to Use
- Building an investment policy statement for an individual, endowment, or foundation
- Defining return objectives (nominal and real) based on future liabilities or spending needs
- Assessing risk tolerance by reconciling financial capacity with psychological comfort
- Setting constraints across liquidity, legal/regulatory, time horizon, tax, and unique circumstances
- Establishing portfolio guidelines including asset allocation ranges and rebalancing triggers
- Selecting benchmarks and defining manager evaluation criteria
- Scheduling periodic IPS and performance reviews

## Core Concepts

### Investment Policy Statement (IPS)
The IPS is the governing document for all investment decisions. It specifies objectives (return and risk), constraints, asset allocation ranges, rebalancing policy, benchmark selection, and review schedule. Every portfolio action should be traceable back to IPS provisions.

### Return Objective
The required return is the rate that funds all future liabilities and goals.

- **Required return:** Solve for the discount rate that equates the present value of assets to the present value of future liabilities/spending needs.
- **Spending rate (endowments/foundations):** Typically set as a percentage of a rolling average of portfolio value (e.g., 5% of 3-year rolling average AUM). The required nominal return must cover spending + inflation + fees.
  - Required nominal return = spending rate + expected inflation + investment management fees

### Risk Tolerance
Risk tolerance has two dimensions that must be assessed independently:

- **Ability (financial capacity):** Determined by time horizon, wealth relative to liabilities, income stability, and liquidity needs. Longer horizons and greater surplus increase ability.
- **Willingness (psychological comfort):** Determined by behavioral assessment, past responses to losses, and stated preferences.
- **Conflict resolution rule:** When ability and willingness conflict, the lower of the two governs. A client with high ability but low willingness should be invested conservatively (with education to potentially raise willingness over time).

### Constraints (LLTU+U)
Five categories of constraints must be addressed in every IPS:

- **Liquidity:** Anticipated cash needs, emergency reserves, near-term spending requirements
- **Legal/Regulatory:** ERISA rules, trust provisions, foundation payout requirements, prudent investor standards
- **Time horizon:** Single-stage or multi-stage; longer horizons generally permit more risk
- **Tax:** Taxable vs tax-deferred vs tax-exempt status; impact on asset allocation and rebalancing
- **Unique circumstances:** ESG/SRI restrictions, concentrated stock positions, employer stock, legacy holdings, personal preferences

### Asset Allocation Policy
Strategic Asset Allocation (SAA) defines long-term target ranges:

- Example ranges: equity 50-70%, fixed income 20-40%, alternatives 0-15%
- Ranges permit tactical tilts within policy bounds
- Policy allocation is the primary driver of long-term returns (commonly cited as explaining ~90% of return variability across time)

### Rebalancing Policy
Specifies when and how the portfolio is brought back to target weights:

- **Calendar-based:** Rebalance at fixed intervals (quarterly, semi-annually)
- **Threshold-based (percentage-of-portfolio):** Rebalance when any asset class drifts beyond a specified band (e.g., ±5% absolute)
- **Combined:** Check at calendar intervals, rebalance only if thresholds are breached
- Wider bands reduce transaction costs but allow more drift; narrower bands maintain discipline but increase costs

### Benchmark Selection
An appropriate benchmark must be:

- **Investable:** Represents a viable passive alternative
- **Measurable:** Returns can be calculated on a timely basis
- **Specified in advance:** Chosen before the evaluation period, not after
- **Appropriate:** Matches the portfolio's asset classes, style, and risk profile
- **Owned by the manager:** The manager should agree the benchmark is fair

### Manager Selection Criteria (The Five Ps)
- **Philosophy:** Clear, coherent investment belief system
- **Process:** Systematic, repeatable approach consistent with philosophy
- **People:** Experienced, stable team with aligned incentives
- **Performance:** Track record evaluated against appropriate benchmark over full market cycles
- **Price:** Fees competitive relative to peers and value added

### Review Schedule
- **Annual IPS review:** Reassess objectives, constraints, and circumstances
- **Quarterly performance review:** Evaluate returns, attribution, and benchmark comparison
- **Trigger-based review:** Major life events, market dislocations, or material changes in circumstances

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| Required nominal return | R_nom = spending_rate + inflation + fees | Endowment/foundation return target |
| Required return (goal-based) | Solve: PV(assets) = Σ [CF_t / (1+R)^t] | Individual required return |
| Real return from nominal | R_real ≈ R_nom - inflation | Converting between real and nominal |
| Spending amount (rolling avg) | Spend = rate × (1/3)(AUM_t + AUM_{t-1} + AUM_{t-2}) | Endowment annual distribution |
| Rebalancing trigger | |w_actual - w_target| > threshold | Threshold-based rebalancing |

## Worked Examples

### Example 1: IPS for a 45-year-old pre-retiree
**Given:** Age 45, current portfolio $2M, needs $100K/year (today's dollars) starting at age 65, life expectancy 90, inflation 2.5%, portfolio fees 0.5%.
**Calculate:** Required nominal return.
**Solution:**
1. Time horizon: 20 years to retirement + 25 years in retirement = two-stage horizon.
2. At retirement, need $100K × (1.025)^20 = $163,862/year in nominal terms.
3. Required nest egg at 65 (25-year payout at ~5% real return): PV of $163,862/year annuity growing at 2.5% inflation, discounted at ~7.5% nominal ≈ $2.76M.
4. Required return: solve $2M × (1+R)^20 = $2.76M → R = (2.76/2.0)^(1/20) - 1 ≈ 1.6% nominal (if no additional contributions). With $0 contributions, the required return is modest.
5. If the client also contributes $30K/year, the required return is even lower, suggesting moderate risk tolerance is sufficient.
6. Risk tolerance: ability is moderate-to-high (long horizon, stable income); assess willingness via questionnaire. If willingness is moderate, adopt moderate allocation (e.g., 60/40).

### Example 2: Endowment spending policy
**Given:** $50M endowment, 5% spending rule on 3-year rolling average, expected inflation 2.5%, investment fees 0.5%.
**Calculate:** Required nominal return to maintain real value.
**Solution:**
1. Annual spending = 5% × $50M = $2.5M (assuming stable AUM at $50M).
2. To maintain purchasing power, the endowment must grow by at least inflation: 2.5%.
3. Required nominal return = spending rate + inflation + fees = 5.0% + 2.5% + 0.5% = **8.0%**.
4. This implies a growth-oriented allocation (e.g., 70% equity, 20% fixed income, 10% alternatives).
5. If 8% seems aggressive, the board may need to reduce spending rate or accept gradual real erosion.

## Common Pitfalls
- Setting return objectives higher than risk tolerance allows — the return target must be achievable within the risk budget
- Ignoring inflation in required return calculations — understating the true return hurdle
- Not revisiting the IPS when circumstances change — life events, market regimes, and regulatory changes demand updates
- Confusing risk ability with risk willingness — they are separate assessments and must be reconciled
- Setting constraints too rigid (reduces flexibility and increases costs) or too loose (provides no discipline)
- Choosing benchmarks after the fact to make performance look better
- Ignoring the interaction between constraints (e.g., tax considerations affecting asset allocation ranges)

## Cross-References
- **tax-efficiency** (wealth-management plugin, Layer 5): asset location and withdrawal sequencing affect IPS constraint section
- **performance-attribution** (wealth-management plugin, Layer 5): benchmark selection in IPS directly feeds performance evaluation
- **liquidity-management** (wealth-management plugin, Layer 6): liquidity constraint in IPS depends on cash flow analysis
- **savings-goals** (wealth-management plugin, Layer 6): return objectives often derived from goal-based planning
- **emergency-fund** (wealth-management plugin, Layer 6): emergency reserve requirement feeds into IPS liquidity constraint
- **client-review-prep** (advisory-practice plugin, Layer 10): IPS provides the reference framework for evaluating drift and suitability during reviews
- **financial-planning-workflow** (advisory-practice plugin, Layer 10): the financial plan informs and is codified in the investment policy statement
- **tax-loss-harvesting** (wealth-management plugin, Layer 5): IPS may specify TLH policy parameters (minimum loss threshold, approved replacement pairs)

## Reference Implementation
N/A — this skill is qualitative and does not require a computational script.
