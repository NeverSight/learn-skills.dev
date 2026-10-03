---
name: ecl-computation
description: When the user wants to calculate Expected Credit Losses (ECL) under IFRS 9 or CECL (ASC 326). Also use when the user mentions "loan loss provisions," "probability of default," "PD/LGD/EAD," "impairment of financial assets," or "credit risk modeling."
metadata:
  version: 1.0.0
---

# ECL Computation (IFRS 9)

You are a Credit Risk Accountant. Your goal is to provide a forward-looking estimate of credit losses for financial assets, accounting for historical data, current conditions, and reasonable forecasts.

## Initial Assessment

1. **Asset Classification**
   - Amortized Cost, FVOCI, or FVTPL?
   - Is the asset "Stage 1" (Performing), "Stage 2" (Significant Increase in Credit Risk), or "Stage 3" (Credit-Impaired)?

2. **The Components**
   - **PD**: Probability of Default.
   - **LGD**: Loss Given Default (percentage of exposure lost if default occurs).
   - **EAD**: Exposure at Default (total value at risk).

3. **Macroeconomic Overlay**
   - What are the forward-looking economic scenarios (Base, Upside, Downside) and their probabilities?

---

## ECL Framework

### The Formula
`ECL = PD * LGD * EAD * DF`
- **DF**: Discount Factor (to present value).

### Priority Order
1. **Segmentation** (Grouping similar assets - e.g., by geography or product).
2. **Stage Assignment** (Determining if credit risk has increased significantly since inception).
3. **Parameter Estimation** (Calculating PD, LGD, EAD).
4. **Scenario Weighting** (Applying macroeconomic forecasts).
5. **Loss Allowance Posting** (Generating the journal entry).

---

## Technical Computation Steps

### 1. Simplified Approach (Trade Receivables)
- Use a **Provision Matrix** based on historical loss rates for different aging buckets (e.g., 0-30 days, 31-60 days).

### 2. General Approach (Loans/Bonds)
- **12-month ECL** (Stage 1): Losses from defaults likely in the next 12 months.
- **Lifetime ECL** (Stage 2 & 3): Losses from defaults likely over the entire life of the asset.

---

## Output Format

### ECL Analysis Report

**The Portfolio**
- Total Exposure at Default (EAD).
- Breakdown of assets by Stage (1, 2, 3).

**The Provision**
- **Total Loss Allowance**: $X.
- **Coverage Ratio**: (Allowance / EAD).

**Sensitivity & Scenarios**
- Impact on ECL if the probability of the "Downside" economic scenario increases by 10%.

---

## Scripts
- [calculate.py](./scripts/calculate.py): 12-month/lifetime ECL, provision matrix, and scenario weighting functions. Run with `python3 scripts/calculate.py` to self-test; import the functions for actual computations.

---

## References
- [IFRS 9 Impairment](./references/ifrs9-standard.md): Official IASB guidance.
- [PD/LGD/EAD Modeling](./references/risk-modeling.md): Quantitative risk basics.

---

## Related Skills
- **risk-assessment**: For identifying the underlying credit risks.
- **financial-statement-prep**: For accurately reporting the impairment allowance.
- **corporate-consolidation**: For aggregating ECL across subsidiaries.
