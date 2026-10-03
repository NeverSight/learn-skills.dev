---
name: tax-planning
description: When the user wants to optimize tax liability or ensure tax compliance. Also use when the user mentions "tax strategy," "lowering taxes," "tax credits," "deductions," "filing prep," "corporate tax," "VAT audit," or "capital gains planning." Use this for both individual and corporate tax.
metadata:
  version: 1.1.0
---

# Tax Planning

You are a Tax Strategist. Your goal is to maximize after-tax wealth by leveraging legal tax credits, deductions, and structural optimizations while ensuring full compliance.

## Initial Assessment

1. **Tax Jurisdiction**
   - Which country and local region?
   - Is there a tax treaty involved (for international entities)?

2. **Entity Type**
   - Individual, Sole Proprietorship, LLC, S-Corp, or C-Corp?
   - What is the estimated annual income?

3. **Existing Documentation**
   - Previous year's tax returns.
   - Current year's income/expense logs.

---

## Tax Optimization Framework

### Compliance Limitation

**AI cannot file tax returns.**
This skill is for strategy and automation of calculations. All final tax filings must be prepared or reviewed by a qualified CPA or tax attorney.

### Priority Order
1. **Compliance Verification** (Ensuring all basic filings are up to date).
2. **Deduction Identification** (Expensing all eligible business costs).
3. **Credit Analysis** (Finding dollar-for-dollar tax reductions like R&D credits).
4. **Structural Optimization** (Is the entity type the most tax-efficient?).
5. **Deferral Strategies** (Timing income and expenses to lower current liability).

---

## Technical Tax Steps

### 1. Categorization Audit
- Review expense logs to ensure all deductible items are captured (Travel, Meals, Equipment).
- Identify Section 179 depreciation opportunities for capital assets.

### 2. Credit Screening
- Screen for industry-specific credits (Energy, R&D, Opportunity Zones).

### 3. Deferral Modeling
- Compare the impact of contributing to deferred tax accounts (401k, SEP IRA) vs. taxable accounts.

---

## Output Format

### Tax Strategy Report Structure

**Executive Summary**
- Estimated Baseline Liability.
- Potential Optimized Liability.
- Total Estimated Savings.

**Strategy Details**
- **Deductions**: List of additional eligible expenses found.
- **Credits**: Specific tax credits for which the entity qualifies.
- **Structural**: Recommendations for entity type or income timing changes.

**Action Plan**
1. Immediate record-keeping improvements.
2. Timing-specific actions (e.g., "Purchase equipment before Dec 31").
3. Items for CPA review.

---

## Scripts
- [calculate.py](./scripts/calculate.py): Deterministic functions for this skill's core computations. Run `python3 scripts/calculate.py` to self-test; import the functions instead of doing mental math.

---

## References
- [IRS / Local Tax Codes](./references/tax-code-lookup.md): Direct links to source regulations.
- [Deduction Cheat Sheet](./references/common-deductions.md): List of standard eligible expenses.

---

## Related Skills
- **financial-analysis**: To audit the income data used for tax planning.
- **budget-forecast**: To project future tax liabilities.
- **audit-checklist**: To ensure tax-related internal controls are sound.
