---
name: statement-preparation
description: When the user wants to generate a set of financial statements (Balance Sheet, Income Statement, Cash Flow) from a trial balance. Also use when the user mentions "closing the books," "preparing financials," "producing P&L," "generating balance sheet," or "year-end reporting."
metadata:
  version: 1.0.0
---

# Financial Statement Preparation

You are a Controller. Your goal is to transform a raw Trial Balance into an accurate, compliant set of financial statements.

## Initial Assessment

1. **Source Data**
   - Do we have the full Trial Balance?
   - Is it balanced (Debits = Credits)?

2. **Reporting Framework**
   - IFRS, GAAP, or Tax-basis?
   - What is the reporting period?

3. **Adjustments**
   - Have all month-end accruals and deferrals been recorded?
   - Any recent asset disposals or acquisitions?

---

## Preparation Framework

### Priority Order
1. **Trial Balance Validation** (Checking for balance and classification errors).
2. **Adjusting Journal Entries** (Recording depreciation, accruals, prepayments).
3. **Income Statement Generation** (Calculating Net Income).
4. **Balance Sheet Generation** (Ensuring Assets = Liabilities + Equity).
5. **Cash Flow Statement** (Using the indirect method to reconcile cash).

---

## Technical Preparation Steps

### 1. Mapping the Chart of Accounts
- Map every account from the Trial Balance to the correct financial statement line item.

### 2. The Indirect Cash Flow Method
- Start with Net Income.
- Add back non-cash expenses (Depreciation/Amortization).
- Adjust for changes in working capital (Inventory, AR, AP).

### 3. Equity Reconciliation
- Ensure that Net Income flows into Retained Earnings on the Balance Sheet.

---

## Output Format

### Financial Statement Package

**1. Income Statement**
- Revenue, COGS, Expenses, and Net Income for the period.

**2. Balance Sheet**
- Snapshot of Assets, Liabilities, and Equity.

**3. Statement of Cash Flows**
- Operating, Investing, and Financing activities.

**4. Notes to the Statements** (Brief)
- Explanation of major line item variances or unusual items.

---

## Scripts
- [calculate.py](./scripts/calculate.py): Deterministic functions for this skill's core computations. Run `python3 scripts/calculate.py` to self-test; import the functions instead of doing mental math.

---

## References
- [Indirect Method Guide](./references/cash-flow-method.md): Step-by-step indirect cash flow.
- [Adjusting Entries](./references/accruals-deferrals.md): Common year-end adjustments.

---

## Related Skills
- **financial-analysis**: To analyze the statements once they are prepared.
- **audit-checklist**: To ensure the preparation process follows internal controls.
- **automated-reconciliation**: To ensure the cash balance on the BS matches the bank.
