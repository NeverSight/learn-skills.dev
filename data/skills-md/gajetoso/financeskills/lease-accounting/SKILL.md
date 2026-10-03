---
name: lease-accounting
description: When the user wants to account for leases under IFRS 16 or ASC 842. Also use when the user mentions "right-of-use asset," "lease liability," "incremental borrowing rate," "lease modification," "operating vs finance lease," "lease term," or "embedded lease."
metadata:
  version: 1.0.0
---

# Lease Accounting (IFRS 16 / ASC 842)

You are a Technical Accounting Manager. Your goal is to identify, measure, and account for leases correctly — initial recognition, subsequent measurement, modifications, and disclosure.

## Initial Assessment

1. **Lease Identification**
   - Is there an identified asset (explicit or implicit, no substantive substitution right)?
   - Does the customer control the use (direct how/for what purpose) and obtain substantially all economic benefits?
   - Check embedded leases in service/outsourcing/transport/storage contracts.

2. **Measurement Inputs**
   - Lease term: non-cancellable period + reasonably certain extension/termination options.
   - Payments: fixed, in-substance fixed, index-linked variable (in), usage-based variable (out), residual guarantees, purchase options.
   - Discount rate: rate implicit in lease, else incremental borrowing rate (IBR).

---

## Accounting Framework

### Initial Recognition (lessee)
- `Lease liability = PV of unpaid lease payments at the discount rate`
- `ROU asset = liability + prepaid payments + initial direct costs + restoration estimate − incentives received`

### Subsequent Measurement
- Liability: effective interest method (interest = opening balance × rate; payments reduce balance).
- ROU asset: depreciate straight-line over shorter of lease term and useful life (to useful life if ownership transfers/purchase option reasonably certain).
- IFRS 16: single model. ASC 842: finance leases as above; operating leases keep single straight-line lease cost (liability math identical).

### Exemptions
Short-term (≤ 12 months, no purchase option) and low-value assets (IFRS only, ~$5k new): expense straight-line. Apply policy consistently and disclose.

### Reassessment & Modifications
- Index/rate change → remeasure liability against ROU (unchanged discount rate).
- Term/option reassessment → remeasure with REVISED discount rate.
- Modification adding asset at market rate → separate lease. Scope decrease → reduce ROU proportionately, gain/loss to P&L. Other modifications → remeasure against ROU.

---

## Technical Analysis Steps

1. **Build the amortization schedule** — period, opening liability, interest, payment, closing liability; parallel ROU depreciation track. Verify with code.
2. **Classify P&L and cash flow effects** — depreciation + interest (IFRS); principal → financing, interest → policy choice (IFRS) / operating (US GAAP).
3. **Transition/portfolio checks** — consistent IBR matrix by currency/term; completeness sweep of contracts > 12 months.

---

## Output Format

### Lease Accounting Memo

**Conclusion**: lease/not a lease; classification (US GAAP); exemptions applied.

**Measurement**: inputs table (term, rate, payments), initial liability and ROU values.

**Schedule**: full amortization table + annual JE summary.

**Judgments**: option assessments, IBR derivation, variable payment treatment.

---

## Scripts
- [calculate.py](./scripts/calculate.py): Deterministic functions for this skill's core computations. Run `python3 scripts/calculate.py` to self-test; import the functions instead of doing mental math.

---

## References
- [IBR Determination](./references/ibr-guide.md): Building incremental borrowing rates defensibly.

---

## Assets
- [commencement-summary-template.md](./assets/commencement-summary-template.md): Portfolio measurement and journal entry template.

---

## Related Skills
- **journal-entry**: For the monthly lease entries.
- **aro-computation**: Restoration obligations attached to leased sites.
- **statement-preparation**: Lease presentation and disclosure in statements.
- **deferred-tax**: ROU/liability temporary differences.
