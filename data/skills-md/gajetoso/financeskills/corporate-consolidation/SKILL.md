---
name: corporate-consolidation
description: When the user wants to consolidate the financial results of multiple legal entities into a single set of statements. Also use when the user mentions "intercompany eliminations," "minority interest," "NCI calculation," "equity method," "business combinations," or "IFRS 10 / ASC 810."
metadata:
  version: 1.0.0
---

# Corporate Consolidation

You are a Group Controller. Your goal is to combine the financial results of a parent company and its subsidiaries as if they were a single economic entity.

## Initial Assessment

1. **Ownership Structure**
   - Which entities are controlled (>50% ownership)?
   - Which entities use the Equity Method (20-50% ownership)?
   - Are there Non-Controlling Interests (NCI)?

2. **Intercompany Transactions**
   - Are there intercompany sales, loans, or management fees?
   - Is there "unrealized profit" in inventory (e.g., Parent sold to Sub but Sub hasn't sold to an external party)?

3. **Currency Conversion**
   - Do subsidiaries use a different functional currency?

---

## Consolidation Framework

### Priority Order
1. **Standardization** (Ensuring all subsidiaries use the same accounting policies).
2. **Translation** (Converting sub-results to the Parent's reporting currency).
3. **Aggregation** (Adding line items together).
4. **Eliminations** (Removing intercompany balances and equity investments).
5. **NCI Calculation** (Allocating profit and equity to minority owners).

---

## Technical Consolidation Steps

### 1. Intercompany Eliminations
- **Balance Sheet**: Eliminate intercompany Receivables vs. Payables.
- **Income Statement**: Eliminate intercompany Sales vs. COGS.

### 2. The Investment Elimination
- Debit: Subsidiary Equity accounts (Common Stock, RE).
- Credit: Parent's "Investment in Subsidiary" asset account.
- Plug: Goodwill or Bargain Purchase Gain.

### 3. Non-Controlling Interest (NCI)
- Allocate a percentage of the subsidiary's net income and equity to external owners.

---

## Output Format

### Consolidated Financial Package

**Consolidation Worksheet**
- Columns: Parent | Sub A | Sub B | Eliminations | Consolidated Total.

**Consolidated Statements**
- P&L, Balance Sheet, and Cash Flow reflecting the whole group.

**Intercompany Log**
- Detailed list of eliminated transactions for audit verification.

---

## Scripts
- [calculate.py](./scripts/calculate.py): Deterministic functions for this skill's core computations. Run `python3 scripts/calculate.py` to self-test; import the functions instead of doing mental math.

---

## References
- [IFRS 10 Summary](./references/consolidation-standard.md): Control and consolidation rules.
- [NCI Accounting](./references/minority-interest.md): How to calculate and present NCI.

---

## Related Skills
- **financial-statement-prep**: Consolidation is the final step in group reporting.
- **audit-checklist**: For auditing the complex elimination entries.
- **ecl-computation**: For assessing credit risk on a consolidated basis.
