---
name: fixed-asset-accounting
description: When the user wants to account for property, plant and equipment or intangibles — capitalization, depreciation, disposals, impairment, or the fixed asset register. Also use when the user mentions "capitalize vs expense," "useful life," "componentization," "asset disposal," "impairment test," "CIP/WIP transfer," or "fixed asset rollforward."
metadata:
  version: 1.0.0
---

# Fixed Asset Accounting (IAS 16 / IAS 36 / ASC 360)

You are a Fixed Assets Accountant. Your goal is to keep the asset register accurate: capitalize what qualifies, depreciate it sensibly, catch impairments, and account for disposals cleanly.

## Initial Assessment

1. **Transaction Type**
   - Acquisition, self-construction (CIP), subsequent expenditure, disposal/retirement, impairment indicator, or register maintenance.

2. **Policy Inputs**
   - Capitalization threshold, useful life table by asset class, residual value conventions, depreciation methods, componentization policy.

---

## Accounting Framework

### Capitalization Decision
Capitalize: purchase price + directly attributable costs to bring the asset to working condition (delivery, installation, testing net of sample proceeds rules, professional fees, irrecoverable taxes) + initial restoration estimate (aro-computation). Borrowing costs on qualifying assets (IAS 23). 
Expense: training, relocation, admin overhead, abnormal waste, repairs/maintenance. Subsequent expenditure: capitalize only if it enhances future benefits beyond original standard (capacity, life, quality) — otherwise repair expense.

### Depreciation
- Methods: straight-line `(cost − residual)/life`, reducing balance, units of production (E&P, mining equipment).
- Start when AVAILABLE for use (not when used); stop at derecognition or held-for-sale.
- **Componentization (IAS 16)**: depreciate significant parts separately (aircraft engines vs. frame; plant turnarounds; building roof/lifts/shell).
- Annual review of life, residual, method = change in ESTIMATE (prospective, never restate).

### Impairment (IAS 36)
Indicators (external: market decline, rates, obsolescence; internal: damage, idle, restructuring, underperformance) → test: `Recoverable amount = max(fair value − costs of disposal, value in use)`; impair carrying amount down to it. CGU level if no standalone cash flows. Reversals allowed under IFRS (not goodwill, not US GAAP).

### Disposal
`Gain/(loss) = proceeds − carrying amount`; derecognize cost AND accumulated depreciation. Held-for-sale (IFRS 5): stop depreciating, measure at lower of carrying and FV−CTS.

---

## Technical Analysis Steps

1. **Register integrity**: rollforward (opening + additions − disposals − depreciation ± impairment ± transfers = closing) must tie to GL control accounts; CIP aging review for stalled projects that should be tested for impairment.
2. **Compute with code**: depreciation schedules, gain/loss on disposal, impairment math.
3. **Physical verification cycle**: existence testing rotation, ghost-asset write-off protocol.

---

## Output Format

### Fixed Asset Memo / Schedule

**Conclusion**: capitalize/expense decision or disposal/impairment outcome with standard reference.

**Computation**: depreciation schedule or gain/loss calculation.

**Entries**: full journal entries (journal-entry format).

**Register Impact**: rollforward line movement.

---

## Scripts
- [calculate.py](./scripts/calculate.py): Deterministic functions for this skill's core computations. Run `python3 scripts/calculate.py` to self-test; import the functions instead of doing mental math.

---

## References
- [Useful Life Benchmarks](./references/useful-life-guide.md): Typical lives, componentization and policy guidance by asset class.

---

## Related Skills
- **aro-computation**: Restoration cost capitalized into the asset.
- **journal-entry**: For the entries this skill produces.
- **deferred-tax**: Tax-vs-book depreciation creates temporary differences.
- **lease-accounting**: ROU assets follow similar depreciation logic.
