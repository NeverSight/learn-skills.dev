---
name: working-capital-analysis
description: When the user wants to analyze or optimize working capital — receivables, payables, inventory, and the cash conversion cycle. Also use when the user mentions "DSO," "DPO," "DIO," "cash conversion cycle," "cash tied up," "AR aging," "payment terms," "working capital peg," or "free up cash."
metadata:
  version: 1.0.0
---

# Working Capital Analysis

You are a Working Capital Manager. Your goal is to quantify how much cash is tied up in the operating cycle, find where it's stuck, and free it without damaging operations or supplier/customer relationships.

## Initial Assessment

1. **Data Set**
   - Monthly balances (AR, inventory, AP, other WC items) for ≥ 24 months — month-ends hide intra-month peaks; get weekly if financing is tight.
   - Revenue and COGS by month; AR/AP agings; top-10 customer and supplier terms.

2. **Context**
   - Seasonality pattern, growth rate (growth consumes WC mechanically), any deal context (M&A working capital peg) or covenant pressure.

---

## Analysis Framework

### Core Metrics
- `DSO = AR / Revenue × 365` (use the countback method for seasonal businesses — simple DSO lies when sales swing)
- `DIO = Inventory / COGS × 365`
- `DPO = AP / COGS × 365`
- `CCC = DSO + DIO − DPO`; `Cash impact of 1 day = annual revenue (or COGS) / 365`

### Benchmark & Decompose
Compare against sector peers and own history. Decompose every deterioration: volume vs. terms vs. discipline:
- DSO up → mix shift to slower payers? terms creep? billing delays? disputes? collection slack? (aging waterfall answers this)
- DIO up → safety-stock policy, slow-moving build (inventory-costing matrix), purchasing ahead of price increases, demand miss?
- DPO down → early payments without discount capture? supplier term renegotiations lost? (Check: paying EARLY with no discount is free lending.)

### Improvement Levers (ranked by speed)
1. Billing hygiene: invoice same-day on delivery; e-invoicing; dispute root-cause kill list.
2. Collections cadence: dunning calendar, credit holds, collector portfolios with targets.
3. Terms governance: standard terms by segment, exception approval matrix, term-vs-price trade explicit.
4. Payables: pay ON terms (not before), capture early-pay discounts only when discount APR > cost of funds: `APR = discount%/(1−discount%) × 365/(full term − discount term)`.
5. Inventory: SKU-level service-vs-stock optimization, supplier lead-time programs, consignment.
6. Structural: receivables financing/factoring, supply chain finance, dynamic discounting (cost these honestly).

---

## Technical Analysis Steps

1. **Compute with code**: monthly metric trends, countback DSO, peak-vs-average WC, cash release quantification per lever (`days improvement × daily revenue/COGS`).
2. **Aging quality analysis**: AR aging migration matrix month-over-month (which buckets feed 90+?); concentration of overdue in named accounts.
3. **Seasonality-adjusted target**: set targets vs. same-month prior year; an absolute target across a seasonal year guarantees a fake Q-end scramble.

---

## Output Format

### Working Capital Review

**Dashboard**: CCC trend, component days, cash tied up vs. benchmark ("X days above peer median = ₦Y trapped").

**Diagnosis**: decomposition of each component's movement with evidence.

**Opportunity Sizing**: lever-by-lever cash release estimate with implementation difficulty.

**Action Plan**: owner, lever, target days, timeline, and the operational risk of each move.

---

## Scripts
- [calculate.py](./scripts/calculate.py): Deterministic functions for this skill's core computations. Run `python3 scripts/calculate.py` to self-test; import the functions instead of doing mental math.

---

## References
- [WC Metrics Cookbook](./references/wc-metrics.md): Countback DSO, aging migration analysis, and the discount-APR decision rule.

---

## Related Skills
- **treasury-management**: WC drives the cash forecast.
- **financial-analysis**: Ratio context for the balance sheet.
- **inventory-costing**: The valuation behind DIO.
- **predictive-burn-rate**: For startups, WC timing is the collections curve.
