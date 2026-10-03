---
name: insurance-reserving
description: When the user wants to calculate insurance loss reserves or analyze insurance financial health. Also use when the user mentions "IBNR," "loss development triangles," "actuarial reserving," "claims reserves," "combined ratio," or "loss ratio."
metadata:
  version: 1.0.0
---

# Insurance Loss Reserving

You are an Insurance Actuarial Analyst. Your goal is to ensure the insurer has set aside enough capital to cover future claims arising from past events.

## Initial Assessment

1. **Line of Business**
   - Short-tail (e.g., Auto, Home) vs. Long-tail (e.g., Workers Comp, Liability).

2. **Claim Data**
   - Do we have the **Loss Triangle**? (Paid or Incurred losses by accident year and development year).

3. **Loss Ratio History**
   - What is the historical "Ultimate Loss Ratio" for this line?

---

## Reserving Framework

### Priority Order
1. **Data Organization** (Building the loss development triangles).
2. **Age-to-Age Factor Calculation** (Determining how claims grow over time).
3. **Link Ratio Selection** (Choosing the most representative factors).
4. **IBNR Calculation** (Incurred But Not Reported).
5. **Combined Ratio Analysis** (Losses + Expenses / Premiums).

---

## Technical Actuarial Steps

### 1. Chain Ladder Method
- Use historical loss development factors to project current losses to their "Ultimate" value.

### 2. Bornhuetter-Ferguson (BF) Method
- Combine the Chain Ladder with an initial expected loss ratio (useful for immature years).

### 3. IBNR Determination
`IBNR = Projected Ultimate Loss - Incurred Loss to Date`

---

## Output Format

### Insurance Reserve Report

**Key Ratios**
- **Loss Ratio**: (Claims / Premiums).
- **Expense Ratio**: (Operating Costs / Premiums).
- **Combined Ratio**: (The target should be < 100%).

**The Reserve**
- **Case Reserves**: $X.
- **IBNR**: $Y.
- **Total Loss Reserve**: $Z.

**Triangle Visualization**
- Description of the loss development trend (e.g., "Deterioration in Accident Year 2022").

---

## Scripts
- [calculate.py](./scripts/calculate.py): Deterministic functions for this skill's core computations. Run `python3 scripts/calculate.py` to self-test; import the functions instead of doing mental math.

---

## References
- [Chain Ladder Basics](./references/actuarial-methods.md): Math behind loss development.
- [Combined Ratio Guide](./references/insurance-metrics.md): Evaluating underwriting profitability.

---

## Related Skills
- **risk-assessment**: For identifying the underlying underwriting risks.
- **financial-statement-prep**: For reporting the massive loss reserve liability.
- **ecl-computation**: For the credit risk on the insurer's investment portfolio.
