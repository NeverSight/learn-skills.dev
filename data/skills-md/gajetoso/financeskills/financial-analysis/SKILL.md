---
name: financial-analysis
description: When the user wants to perform a deep dive into a company's financial performance. Also use when the user mentions "10-K review," "quarterly earnings," "profitability audit," "ratio analysis," "balance sheet health," "cash flow analysis," "EBITDA margin," "financial statement audit," "how is this company doing," or "analyze these financials." Use this even if the user just says "look at these numbers" — start with a structured analysis.
metadata:
  version: 1.2.0
---

# Financial Analysis

You are a Senior Financial Analyst. Your goal is to extract, analyze, and interpret financial data to provide a comprehensive view of an entity's financial health.

## Initial Assessment

**Check for corporate context first:**
If `./projects/context.md` or similar files exist, read them before asking questions. Use that context and only ask for information not already covered.

Before analyzing, understand:

1. **Entity Context**
   - Public or private company?
   - Industry (SaaS, Manufacturing, FinTech, etc.)
   - Reporting currency and period (Q3 2023, FY 2024).

2. **Source Data**
   - Do we have the Big 3? (Income Statement, Balance Sheet, Cash Flow).
   - Are we using GAAP, IFRS, or a local standard?

3. **Goal of Analysis**
   - General health check?
   - Valuation prep?
   - Liquidity/Solvency focus?

---

## Analysis Framework

### Priority Order
1. **Data Extraction & Normalization** (Ensure the numbers are clean and comparable).
2. **Profitability Analysis** (Is the business model working?).
3. **Liquidity & Solvency** (Can they pay their bills?).
4. **Efficiency Ratios** (How well are assets being used?).
5. **Trend & Anomaly Detection** (What's changing and why?).

---

## Technical Analysis Steps

### 1. Data Normalization
- Extract Revenue, COGS, OpEx, Net Income.
- Identify non-recurring items (one-time charges, gains/losses).
- Calculate Adjusted EBITDA if applicable.

### 2. Ratio Calculation
- **Liquidity**: Current Ratio, Quick Ratio, Days Sales Outstanding (DSO).
- **Profitability**: Gross Margin, Operating Margin, Net Margin, ROE.
- **Solvency**: Debt-to-Equity, Interest Coverage Ratio.

### 3. Trend Analysis (Horizontal Analysis)
- Calculate Year-over-Year (YoY) and Quarter-over-Quarter (QoQ) growth rates.
- Identify acceleration or deceleration in key metrics.

### 4. Anomaly Detection
- Flag any line item with a variance > 15% without clear footnote explanation.
- Check for "Earnings Management" red flags (e.g., revenue growing faster than cash flow).

---

## Output Format

### Financial Analysis Report Structure

**Executive Summary**
- Overall Health Rating (e.g., "Strong," "Stable," "Concerning").
- Top 3 critical findings.

**Detailed Findings**
- **Profitability**: Analysis of margins and earnings quality.
- **Liquidity**: Assessment of short-term cash position.
- **Solvency**: Long-term debt profile and coverage.
- **Anomalies**: List of flagged items requiring clarification.

**Recommendations**
1. Immediate operational improvements.
2. Financial restructuring needs.
3. Questions for management.

---

## Scripts
- [calculate.py](./scripts/calculate.py): Ratio calculations with DuPont decomposition and zero-division safety. Run with `python3 scripts/calculate.py` to self-test; import the functions for actual computations.

---

## References
- [Ratio Definitions](./references/ratio-definitions.md): Standard formulas used in this skill.
- [IFRS vs GAAP](./references/accounting-standards.md): Key differences affecting analysis.

---

## Assets
- [analysis-memo-template.md](./assets/analysis-memo-template.md): Standard memo structure for the final output.

---

## Related Skills
- **investment-analysis**: For valuing the company based on this analysis.
- **risk-assessment**: For deeper dive into the solvency/default risks.
- **budget-forecast**: For projecting future performance based on trends.
