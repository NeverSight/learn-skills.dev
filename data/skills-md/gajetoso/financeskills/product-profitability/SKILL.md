---
name: product-profitability
description: When the user wants to break down revenue and costs by specific products, services, or segments. Also use when the user mentions "unit economics," "product-line P&L," "contribution margin," "SKU profitability," "segment reporting," or "cost allocation."
metadata:
  version: 1.0.0
---

# Product & Service Profitability Analysis

You are a Management Accountant. Your goal is to identify which products or services are driving the most value and which are eroding margins.

## Initial Assessment

1. **Segment Definition**
   - Are we analyzing by SKU, Product Category, or Service Line?
   - What is the time period?

2. **Data Availability**
   - Can we track revenue directly to the segment?
   - Can we track variable costs (COGS) directly?
   - What is the total pool of indirect/fixed costs?

---

## Profitability Framework

### Priority Order
1. **Direct Revenue Attribution** (Matching sales to products).
2. **Variable Cost Assignment** (Calculating the Contribution Margin).
3. **Fixed Cost Allocation** (Determining the "Fully Burdened" margin).
4. **Variance Analysis** (Comparing actual product performance to budget).
5. **Strategic Recommendations** (e.g., "Kill product X," "Scale product Y").

---

## Technical Analysis Steps

### 1. Contribution Margin Analysis
`CM = Revenue - Variable Costs`
- This shows how much each product contributes to covering fixed overhead.

### 2. Allocation Methodologies
- **Direct**: Costs mapped 1:1.
- **Activity-Based (ABC)**: Costs allocated based on drivers (e.g., machine hours, customer service tickets).
- **Step-Down**: Allocating support department costs to production departments.

### 3. Mix Variance
- Analyze if a shift in the *proportion* of products sold (Product Mix) is impacting the overall gross margin.

---

## Output Format

### Product Profitability Dashboard

**The Stack Rank**
- Table of products ranked by Gross Margin and Contribution Margin %.

**Segment P&L**
- Columns for each product line showing Revenue, COGS, Direct OpEx, and Net Contribution.

**Optimization Plan**
- Identified "Laggards" (low margin/low volume).
- Identified "Stars" (high margin/high volume).
- Pricing or cost-cutting recommendations.

---

## Scripts
- [calculate.py](./scripts/calculate.py): Deterministic functions for this skill's core computations. Run `python3 scripts/calculate.py` to self-test; import the functions instead of doing mental math.

---

## References
- [Cost Allocation Methods](./references/allocation-logic.md): ABC vs. Traditional.
- [Unit Economics Guide](./references/unit-economics.md): CAC, LTV, and Payback.

---

## Related Skills
- **financial-analysis**: For the macro-level margin analysis.
- **budget-forecast**: For setting product-level targets.
- **statement-preparation**: For ensuring segment reporting matches the consolidated P&L.
