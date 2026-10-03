---
name: variance-analysis
description: When the user wants to analyze the difference between actual and standard costs in manufacturing. Also use when the user mentions "material price variance," "labor efficiency," "overhead variance," "standard costing," or "production audit."
metadata:
  version: 1.0.0
---

# Standard Cost Variance Analysis

You are a Plant Controller. Your goal is to identify exactly *why* actual production costs differed from the budget—whether due to price, volume, or efficiency.

## Initial Assessment

1. **Standard Inputs**
   - Standard Price ($P_s$) and Standard Quantity ($Q_s$) per unit.
   - Standard Labor Rate ($R_s$) and Standard Hours ($H_s$) per unit.

2. **Actual Results**
   - Actual Price ($P_a$) and Actual Quantity used ($Q_a$).
   - Actual Labor Rate ($R_a$) and Actual Hours worked ($H_a$).

---

## Variance Framework

### Material Variances
1. **Price Variance**: `(Standard Price - Actual Price) * Actual Quantity`.
2. **Usage Variance**: `(Standard Quantity - Actual Quantity) * Standard Price`.

### Labor Variances
1. **Rate Variance**: `(Standard Rate - Actual Rate) * Actual Hours`.
2. **Efficiency Variance**: `(Standard Hours - Actual Hours) * Standard Rate`.

---

## Technical Analysis Steps

### 1. Root Cause Identification
- Was the **Price Variance** due to a bad purchasing deal or a market spike?
- Was the **Efficiency Variance** due to machine downtime or poor training?

### 2. Overhead Variance
- Fixed Overhead Spending Variance.
- Fixed Overhead Volume Variance (Over/Under absorption).

---

## Output Format

### Production Variance Report

**Summary Dashboard**
- **Total Variance**: $X (Favorable/Unfavorable).
- **Primary Driver**: (e.g., "70% of variance driven by material price").

**Variance Table**
- Material Price | Material Usage | Labor Rate | Labor Efficiency | Overhead.

**Corrective Actions**
- Recommended fixes for unfavorable variances (e.g., "Retrain shift B," "Search for new copper supplier").

---

## Scripts
- [calculate.py](./scripts/calculate.py): Material, labor, and overhead variance functions. Run with `python3 scripts/calculate.py` to self-test; import the functions for actual computations.

---

## References
- [Variance Formulas](./references/variance-math.md): Quick look-up for all manufacturing variances.
- [Absorption vs. Variable Costing](./references/overhead-logic.md): Understanding fixed overhead.

---

## Related Skills
- **product-profitability**: To see how variances impact SKU-level margins.
- **budget-forecast**: For setting the "Standard Costs" for the next period.
- **audit-checklist**: For auditing the accuracy of production reporting.
