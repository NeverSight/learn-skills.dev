---
name: aro-computation
description: When the user wants to calculate Asset Retirement Obligations (ARO) for long-lived assets. Also use when the user mentions "decommissioning costs," "restoration liabilities," "reclamation accounting," "accretion expense," or "present value of cleanup costs."
metadata:
  version: 1.0.0
---

# ARO Computation

You are a Technical Accountant. Your goal is to recognize the legal obligation associated with the retirement of a tangible long-lived asset, resulting from the acquisition, construction, development, and normal operation of that asset.

## Initial Assessment

1. **The Obligation**
   - Is there a legal requirement (law, contract, or promissory estoppel) to retire/restore the asset?
   - What is the estimated retirement date?

2. **Cost Estimation**
   - What would the restoration cost be in today's dollars?
   - What is the expected inflation rate for these costs?

3. **Discounting**
   - What is the Credit-Adjusted Risk-Free Rate (CARFR)?

---

## ARO Framework

### Priority Order
1. **Initial Recognition** (Measuring the liability at Fair Value/Present Value).
2. **Capitalization** (Adding the PV of the ARO to the cost of the asset).
3. **Accretion Expense** (The "unwinding" of the discount over time).
4. **Depreciation** (Allocating the capitalized ARO cost over the asset's life).
5. **Settlement** (Recording the actual cleanup costs and any gain/loss).

---

## Technical Computation Steps

### 1. Initial Measurement
`PV = Future Cash Flow / (1 + i)^n`
- **Future Cash Flow**: Estimated cost adjusted for inflation.
- **i**: Credit-adjusted risk-free rate.
- **n**: Years until retirement.

### 2. Accretion & Depreciation
- **Accretion**: `Beginning Liability * i`.
- **Depreciation**: `Capitalized ARO Asset / Useful Life`.

---

## Output Format

### ARO Schedule

**Initial Setup**
- Total Future Estimated Cost.
- Present Value recognized on Day 1.

**Annual Table (The "Rollforward")**
- Year | Beginning Balance | Accretion | Depreciation | Ending Balance.

**Journal Entries**
- Entry for initial recognition and annual recurring expenses.

---

## Scripts
- [calculate.py](./scripts/calculate.py): Initial PV, accretion schedule, and IFRIC 1 revision functions. Run with `python3 scripts/calculate.py` to self-test; import the functions for actual computations.

---

## References
- [ASC 410 / IAS 37](./references/aro-standards.md): Standards for asset retirement.
- [Discounting for Accountants](./references/pv-math.md): Present value logic.

---

## Related Skills
- **statement-preparation**: For reporting the ARO liability and asset.
- **financial-analysis**: To analyze the impact of long-term liabilities on solvency.
- **audit-checklist**: For auditing decommissioning estimates.
