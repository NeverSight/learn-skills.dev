---
name: journal-entries
description: Create or review journal entries, accruals, amortization, depreciation, payroll, revenue, and adjustments.
---

## Core Entry Patterns by Accounting Cycle

### Vendor & Expense Accruals

Record obligations for goods received or services consumed when no invoice has arrived by the reporting cut-off.

**Entry template:**
- DR: Appropriate expense (or asset if capitalizable)
- CR: Accrued liabilities

**Estimation sources:**
- Purchase orders showing confirmed delivery
- Service agreements with work performed but unbilled
- Standing vendor arrangements (utilities, professional fees, SaaS)
- Staff reimbursement claims awaiting processing

**Operational guidance:**
- Configure for automatic reversal at the start of the subsequent period
- Apply the same estimation technique from period to period for comparability
- Record the basis of each estimate (contract value, PO total, trailing average)
- Compare prior-period estimates to eventual actuals and refine methodology

### Tangible & Intangible Asset Charges

Systematically allocate the cost of long-lived assets over their service lives.

**Entry template:**
- DR: Depreciation or amortization expense (allocated to cost center)
- CR: Contra-asset (accumulated depreciation or amortization)

**Allocation approaches:**
- **Even-line:** (Acquisition cost minus residual) divided by expected life — the default for most financial reporting
- **Accelerated:** Apply a declining percentage to the remaining book value each period
- **Activity-based:** Charge proportional to actual output versus total expected output

**Operational guidance:**
- Source the entry from the fixed-asset or intangible-asset subledger
- Confirm newly capitalized items carry the correct useful life and method
- Check for retired or impaired assets requiring a write-off entry
- Maintain parallel tracking for book versus tax depreciation where they diverge

### Prepaid Cost Amortization

Release advance payments to expense as the underlying benefit is consumed.

**Entry template:**
- DR: Relevant expense category (insurance, licenses, rent, maintenance)
- CR: Prepaid asset

**Frequently encountered prepaids:**
- Annual insurance policies
- Multi-period software or platform subscriptions
- Advance rent payments
- Service and maintenance agreements
- Deposits for conferences or events

**Operational guidance:**
- Maintain an amortization register showing coverage dates and monthly charge amounts
- Expense immaterial prepayments immediately rather than building a schedule
- Accelerate remaining amortization when a contract is cancelled or terminated early
- Add new prepaid items to the register promptly upon payment

### Compensation Accruals

Capture all people costs attributable to the reporting period.

**Entry templates:**

*Wages for partial pay-period overlap:*
- DR: Wage expense (by department)
- CR: Accrued compensation

*Incentive compensation:*
- DR: Bonus expense (by department)
- CR: Accrued bonuses

*Employer benefit obligations:*
- DR: Benefits expense
- CR: Accrued benefits

*Employer payroll taxes:*
- DR: Payroll tax expense
- CR: Accrued payroll taxes

**Operational guidance:**
- Pro-rate salary accruals based on business days falling inside the period versus the total pay cycle
- Incentive accruals should mirror plan design: target payout, performance multipliers, and expected distribution timing
- Include employer-borne costs — social security, unemployment insurance, health plans, retirement matching
- Accrue for earned but unused paid time off where required by law or company policy

### Contract Revenue Recognition

Record revenue consistent with the transfer of promised goods or services to the customer.

**Entry templates:**

*Release of advance billings:*
- DR: Contract liability (deferred revenue)
- CR: Revenue

*Recognize with simultaneous receivable:*
- DR: Trade receivables
- CR: Revenue

*Collect or bill before delivery:*
- DR: Cash or trade receivables
- CR: Contract liability (deferred revenue)

**Operational guidance:**
- Apply the ASC 606 five-step model: (1) identify the contract, (2) identify performance obligations, (3) determine the transaction price, (4) allocate price across obligations, (5) recognize upon satisfaction
- Maintain contract-level schedules that map obligations to delivery milestones
- Handle variable consideration (discounts, rebates, penalties) using the expected-value or most-likely-amount method
- Retain documentation sufficient to support external audit review

## Documentation Standards

Each posted entry must include:

1. **Narrative memo:** A plain-language explanation of what economic event the entry captures and the reason it is required
2. **Quantitative support:** The formula, schedule, or data extract that produces the recorded amounts
3. **Source references:** Identifiers linking to underlying evidence — PO numbers, invoice references, contract IDs, payroll registers
4. **Applicable period:** The fiscal period to which the entry relates
5. **Preparer identity:** Name and timestamp of the individual who built the entry
6. **Authorization evidence:** Sign-off from the appropriate approver per the delegation matrix
7. **Reversal flag:** Indication of whether the entry will auto-reverse, and the reversal date

## Authorization Framework

### Delegation Matrix

| Entry Classification | Dollar Range | Required Approver |
|---|---|---|
| Recurring / template-based | All amounts | Accounting manager |
| Ad hoc or non-standard | Under $50K | Accounting manager |
| Ad hoc or non-standard | $50K -- $250K | Controller |
| Ad hoc or non-standard | Over $250K | CFO or VP of Finance |
| Consolidation / top-side | All amounts | Controller or higher |
| Prior-period corrections | All amounts | Controller or higher |

*Calibrate dollar bands to the organization's own materiality and governance requirements.*

### Approval Verification Steps

The approver should confirm each of the following before signing off:

- Debits and credits are equal (the entry balances)
- The target period is open and correct
- General ledger account codes are valid and fit the transaction's nature
- Dollar amounts tie to the supporting calculation without error
- The memo is clear enough that a third party could understand the purpose
- Cost center, department, and project tags are accurate
- The accounting treatment matches established policy and prior-period practice
- Accrual entries are flagged for reversal
- All referenced support documents are attached or linked
- The entry falls within the preparer's authorized scope
- No duplicate of a previously posted entry exists
- Any unusually large or round-dollar figures carry explicit justification

## Frequent Mistakes and Prevention

1. **Imbalanced entries:** Total debits do not equal total credits — system controls should block this, but verify on manual uploads
2. **Incorrect period:** Entry lands in a closed or wrong fiscal month
3. **Inverted signs:** Debit and credit legs are swapped
4. **Duplicate posting:** The same economic event is captured twice — search for duplicates before submitting
5. **Misrouted account:** Amounts post to a similarly numbered but incorrect GL code
6. **Unreversed accruals:** A prior-period accrual remains on the books, overstating the current balance
7. **Outdated recurring estimates:** Template entries roll forward without reflecting changed business conditions
8. **Suspiciously round figures:** Amounts ending in multiple zeros that may not derive from actual calculations
9. **Wrong exchange rate:** Foreign-currency entries converted at an outdated or incorrect FX rate
10. **Orphaned intercompany legs:** One side of an intercompany transaction posted without the offsetting entity's entry
11. **Capitalization misjudgment:** Expenses incorrectly capitalized, or capital items expensed in error
12. **Cut-off violations:** Transactions recorded based on invoice date rather than the date goods transferred or services were rendered
