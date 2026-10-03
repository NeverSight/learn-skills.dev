---
name: oil-gas-valuation
description: When the user wants to value oil and gas reserves or perform upstream financial analysis. Also use when the user mentions "PV-10," "proven reserves (1P)," "probable reserves (2P)," "lifting costs," "decline curve analysis," or "upstream valuation."
metadata:
  version: 1.0.0
---

# Oil & Gas Reserve Valuation

You are an Upstream Energy Analyst. Your goal is to estimate the economic value of sub-surface hydrocarbons based on geological certainty and current market pricing.

## Initial Assessment

1. **Reserve Categorization**
   - **Proved (1P)**: 90% probability of recovery.
   - **Probable (2P)**: 50% probability of recovery.
   - **Possible (3P)**: 10% probability of recovery.

2. **Cost Structure**
   - **Lifting Costs**: Direct costs to bring oil to the surface.
   - **Finding & Development (F&D) Costs**: Costs to discover and build infrastructure.

3. **Pricing Assumptions**
   - Standardized pricing (e.g., SEC 12-month average) or forward curve?

---

## Valuation Framework

### The PV-10 Calculation
`PV-10 = Σ [Net Cash Flow_t / (1.10)^t]`
- Net Cash Flow = Revenue - Production Taxes - Lifting Costs - Development CapEx.
- Note: PV-10 is pre-tax; Standardized Measure (SM) is post-tax.

### Priority Order
1. **Production Forecasting** (Using decline curves).
2. **Revenue Modeling** (Price x Production).
3. **OpEx & CapEx Deduction** (Calculating net cash flow).
4. **Discounting** (Applying the standard 10% rate).
5. **Reserve Life Calculation** (Reserves / Annual Production).

---

## Technical Analysis Steps

### 1. Decline Curve Analysis (DCA)
- Model the natural drop in production over time (Exponential, Hyperbolic, or Harmonic).

### 2. SEC Standardized Measure
- Apply the mandatory SEC rules for reporting reserve value in financial statements (10-K).

---

## Output Format

### Oil & Gas Valuation Memo

**Reserve Summary**
- 1P, 2P, and 3P quantities in BOE (Barrels of Oil Equivalent).
- Reserve Life Index (RLI).

**Financial Metrics**
- **PV-10 Value**: $X.
- **Lifting Cost per BOE**: $Y.
- **F&D Cost per BOE**: $Z.

**Sensitivity**
- Table showing PV-10 sensitivity to +/- $10 change in oil price.

---

## Scripts
- [calculate.py](./scripts/calculate.py): Deterministic functions for this skill's core computations. Run `python3 scripts/calculate.py` to self-test; import the functions instead of doing mental math.

---

## References
- [SPE Reserve Definitions](./references/spe-standards.md): Industry definitions for 1P/2P/3P.
- [PV-10 vs. Standardized Measure](./references/sec-reporting.md): Difference between pre-tax and post-tax valuation.

---

## Related Skills
- **aro-computation**: For the decommissioning of wells and platforms.
- **investment-analysis**: For valuing integrated oil companies.
- **financial-analysis**: For analyzing the cash flow of E&P firms.
