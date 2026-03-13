---
name: performance-attribution
description: "Decompose portfolio returns into explainable components to identify where value was added or lost. Use when the user asks about Brinson attribution, allocation vs selection effects, factor-based attribution, fixed-income attribution, or currency attribution. Also trigger when users mention 'what drove my returns', 'was it stock picking or sector bets', 'alpha decomposition', 'multi-period linking', 'interaction effect', 'active return breakdown', or ask why their portfolio outperformed or underperformed the benchmark."
---

# Performance Attribution

## Purpose
Decompose portfolio returns into explainable components to understand where value was added or lost. This skill covers equity attribution (Brinson-Fachler), factor-based attribution, fixed-income attribution, currency effects, and multi-period linking methods.

## Layer
5 — Policy & Planning

## Direction
retrospective

## When to Use
- Explaining where portfolio returns came from relative to a benchmark
- Evaluating whether a manager added value through allocation, selection, or both
- Decomposing returns into systematic factor exposures and residual alpha
- Attributing fixed-income returns to yield, curve, spread, and credit components
- Handling currency effects in international portfolio attribution
- Linking single-period attribution results across multiple periods
- Conducting holdings-based vs returns-based attribution analysis

## Core Concepts

### Brinson-Fachler Attribution (Single Period)
The classic equity attribution model decomposes active return (portfolio return minus benchmark return) into three effects:

- **Allocation effect:** Value added by over/underweighting sectors relative to the benchmark
  - A_i = (w_p,i - w_b,i) × (R_b,i - R_b)
  - Rewards overweighting sectors that outperform the total benchmark
- **Selection effect:** Value added by picking better securities within each sector
  - S_i = w_b,i × (R_p,i - R_b,i)
  - Rewards outperforming the sector benchmark regardless of weight
- **Interaction effect:** Combined effect of both overweighting and outperforming (or vice versa)
  - I_i = (w_p,i - w_b,i) × (R_p,i - R_b,i)
  - Captures the joint benefit of overweighting a sector AND selecting better securities in it
- **Total active return:** R_p - R_b = Σ A_i + Σ S_i + Σ I_i

Where: w_p,i = portfolio weight in sector i, w_b,i = benchmark weight in sector i, R_p,i = portfolio return in sector i, R_b,i = benchmark return in sector i, R_b = total benchmark return.

### Multi-Period Attribution
Single-period attribution does not compound across periods. Geometric linking methods are required:

- **Carino method:** Applies a smoothing factor to make arithmetic effects compound to the correct geometric total
- **Menchero method:** Uses a logarithmic approach for smoother decomposition
- **GRAP (Geometric Return Attribution Program):** Converts arithmetic effects to geometric equivalents
- Key principle: the sum of linked attribution effects must equal the total geometric active return over the full period

### Factor-Based Attribution
Decomposes returns into exposures to systematic risk factors:

- **Model:** R_p = Σ β_k × F_k + α
  - β_k = portfolio's exposure (loading) to factor k
  - F_k = return of factor k during the period
  - α = residual return unexplained by factors (true alpha)
- **Common factors:** Market (MKT), Size (SMB), Value (HML), Momentum (UMD), Quality (QMJ), Low Volatility (BAB)
- **Factor contribution:** β_k × F_k for each factor
- **Active factor contribution:** (β_p,k - β_b,k) × F_k
- The model chosen (Fama-French 3, Carhart 4, Fama-French 5, Barra, Axioma) affects results

### Fixed-Income Attribution
Decomposes bond portfolio returns into component sources:

- **Yield return (income):** Coupon income accrued during the period (yield × time)
- **Roll return:** Price appreciation as bonds "roll down" the yield curve toward maturity
- **Curve change return:** Impact of parallel and non-parallel yield curve shifts
  - Duration effect: -D × Δy (parallel shift)
  - Curve reshaping: key rate duration contributions
- **Spread change return:** Impact of credit spread changes: -spread_duration × Δspread
- **Credit/default return:** Losses from defaults or credit events
- **Residual:** Unexplained return (convexity effects, model error)

### Currency Attribution
For international portfolios, returns decompose into:

- **Local return:** Return of the asset in its local currency
- **Currency return:** Gain/loss from exchange rate movements
- **Cross-product:** Interaction between local return and currency return
- **Total return (base currency):** R_base ≈ R_local + R_currency + R_local × R_currency
- **Hedged return:** Local return + hedge cost (forward premium/discount)
- Attribution of active currency decisions: actual currency exposure vs benchmark currency exposure

### Holdings-Based vs Returns-Based Attribution
- **Holdings-based:** Uses actual portfolio positions; more accurate but requires detailed holdings data at each evaluation point
- **Returns-based (style analysis):** Regresses portfolio returns against a set of style indices (e.g., Sharpe style analysis); less precise but requires only return series
- **Transaction-based:** Most accurate; accounts for intra-period trading by using actual transaction records

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| Allocation effect (sector i) | A_i = (w_p,i - w_b,i) × (R_b,i - R_b) | Sector weighting decisions |
| Selection effect (sector i) | S_i = w_b,i × (R_p,i - R_b,i) | Security selection within sector |
| Interaction effect (sector i) | I_i = (w_p,i - w_b,i) × (R_p,i - R_b,i) | Joint allocation-selection effect |
| Total active return | R_p - R_b = Σ(A_i + S_i + I_i) | Sum of all effects equals active return |
| Factor return contribution | C_k = β_k × F_k | Return from factor k exposure |
| Duration effect | ΔP/P ≈ -D × Δy | Bond price change from yield shift |
| Currency return | R_fx = (S_end - S_start) / S_start | Exchange rate impact |

## Worked Examples

### Example 1: Brinson-Fachler equity attribution
**Given:** Two-sector portfolio (Tech and Healthcare). Portfolio: 35% Tech (returned 15%), 65% Healthcare (returned 8%). Benchmark: 25% Tech (returned 12%), 75% Healthcare (returned 6%). Total benchmark return: 0.25×12% + 0.75×6% = 7.5%.
**Calculate:** Allocation, selection, and interaction effects for each sector, and total active return.
**Solution:**
1. **Total portfolio return:** 0.35×15% + 0.65×8% = 5.25% + 5.20% = 10.45%.
2. **Total active return:** 10.45% - 7.50% = **2.95%**.
3. **Tech allocation effect:** (0.35 - 0.25) × (12% - 7.5%) = 0.10 × 4.5% = **+0.45%** (overweight a sector that beat the benchmark).
4. **Tech selection effect:** 0.25 × (15% - 12%) = 0.25 × 3% = **+0.75%** (stock picks in Tech beat Tech benchmark).
5. **Tech interaction effect:** (0.35 - 0.25) × (15% - 12%) = 0.10 × 3% = **+0.30%** (overweight AND outperformed).
6. **Healthcare allocation effect:** (0.65 - 0.75) × (6% - 7.5%) = -0.10 × -1.5% = **+0.15%** (underweight a sector that lagged the benchmark).
7. **Healthcare selection effect:** 0.75 × (8% - 6%) = 0.75 × 2% = **+1.50%** (stock picks in Healthcare beat Healthcare benchmark).
8. **Healthcare interaction effect:** (0.65 - 0.75) × (8% - 6%) = -0.10 × 2% = **-0.20%** (underweight but outperformed — interaction is negative).
9. **Totals:** Allocation = 0.45 + 0.15 = **0.60%**. Selection = 0.75 + 1.50 = **2.25%**. Interaction = 0.30 + (-0.20) = **0.10%**. Sum = 0.60 + 2.25 + 0.10 = **2.95%** ✓.

### Example 2: Factor-based attribution
**Given:** A fund has factor loadings: β_mkt = 1.1, β_smb = 0.3, β_hml = -0.2. During the period: MKT = 5%, SMB = 2%, HML = -1%. Risk-free rate = 1%. Fund excess return = 7%.
**Calculate:** Factor contributions and alpha.
**Solution:**
1. **Market contribution:** 1.1 × 5% = **5.50%**.
2. **Size (SMB) contribution:** 0.3 × 2% = **0.60%**.
3. **Value (HML) contribution:** -0.2 × (-1%) = **+0.20%**.
4. **Total factor-explained return:** 5.50 + 0.60 + 0.20 = **6.30%**.
5. **Alpha (residual):** 7.00% - 6.30% = **+0.70%**.
6. **Interpretation:** The fund's excess return of 7% is mostly explained by above-market beta (5.5%) and a small-cap tilt (0.6%). The negative value loading helped (+0.2%) as value underperformed. After accounting for all factors, the manager generated 0.70% of true alpha.

## Common Pitfalls
- Interaction effect is hard to interpret — some attribution models fold it into allocation or selection, which changes reported results significantly
- Multi-period attribution requires geometric linking — simple arithmetic attribution does not compound correctly and residuals grow over time
- Returns-based attribution (style analysis) may not reflect actual holdings, especially for managers who trade actively or change style
- Factor attribution results depend heavily on the chosen factor model — different models yield different alpha estimates
- Currency attribution is often overlooked in international portfolios, hiding or inflating apparent skill
- Survivorship bias in manager evaluation: only surviving funds are analyzed, overstating average skill
- Confusing gross-of-fee and net-of-fee returns when comparing to benchmarks
- Using inappropriate benchmarks that do not match the portfolio's investment universe

## Cross-References
- **investment-policy** (wealth-management plugin, Layer 5): Benchmark selection in IPS directly feeds performance attribution analysis
- **tax-efficiency** (wealth-management plugin, Layer 5): After-tax attribution requires adjusting returns for tax impact
- **savings-goals** (wealth-management plugin, Layer 6): Attribution helps assess whether investment strategy is on track to meet goals
- **liquidity-management** (wealth-management plugin, Layer 6): Cash drag from liquidity reserves affects portfolio-level attribution
- **client-review-prep** (advisory-practice plugin, Layer 10): attribution analysis highlights are key talking points in client review meetings
- **tax-loss-harvesting** (wealth-management plugin, Layer 5): tax alpha from TLH should be tracked and attributed separately

## Reference Implementation
See `scripts/performance_attribution.py` for computational helpers.
