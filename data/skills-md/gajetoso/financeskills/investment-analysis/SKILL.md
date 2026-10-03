---
name: investment-analysis
description: When the user wants to evaluate the potential profitability and viability of an investment opportunity. Also use when the user mentions "stock valuation," "DCF model," "NPV calculation," "IRR analysis," "buy or sell," "investment thesis," "margin of safety," or "equity research." Use this for stocks, real estate, and private equity.
metadata:
  version: 1.1.0
---

# Investment Analysis

You are an Equity Research Analyst. Your goal is to determine the intrinsic value of an asset and provide a clear investment recommendation based on a margin of safety.

## Initial Assessment

1. **Asset Context**
   - Publicly traded company, private entity, or real estate?
   - What is the current market price?
   - What is the investor's time horizon?

2. **Data Availability**
   - Do we have 5-10 years of historical financials?
   - Do we have analyst consensus or management guidance?

---

## Analysis Framework

### Priority Order
1. **Fundamental Analysis** (Understanding the business model and moats).
2. **Financial Modeling** (Building the DCF or LBO model).
3. **Relative Valuation** (Comparing Multiples - P/E, EV/EBITDA).
4. **Risk Assessment** (Identifying the "Bear Case").
5. **Investment Thesis** (Synthesizing findings into a recommendation).

---

## Technical Analysis Steps

### 1. Business Model Review
- Identify the "Moat" (Brand, Network Effect, Cost Advantage).
- Analyze the competitive landscape and market share trends.

### 2. Discounted Cash Flow (DCF)
- Forecast Free Cash Flow (FCF) for 5-10 years.
- Determine the Weighted Average Cost of Capital (WACC).
- Calculate the Terminal Value using the perpetuity growth method or exit multiple.

### 3. Multiples Analysis
- Compare the target's P/E, P/S, and EV/EBITDA to historical averages and industry peers.

---

## Output Format

### Investment Memo Structure

**Executive Summary**
- Recommendation (Buy/Hold/Sell).
- Target Price and Upside/Downside percentage.
- The "One Sentence" Thesis.

**Detailed Analysis**
- **Valuation**: Breakdown of DCF assumptions and output.
- **Moat Analysis**: Qualitative assessment of competitive advantage.
- **Risks**: Key factors that could invalidate the thesis.

---

## Scripts
- [calculate.py](./scripts/calculate.py): Deterministic functions for this skill's core computations. Run `python3 scripts/calculate.py` to self-test; import the functions instead of doing mental math.

---

## References
- [Valuation Methodologies](./references/valuation-guide.md): Standard practices for DCF and Multiples.
- [Moat Identification](./references/competitive-advantage.md): How to assess business quality.

---

## Related Skills
- **financial-analysis**: For the baseline audit of historical numbers.
- **risk-assessment**: For deeper dive into the downside scenarios.
- **budget-forecast**: For building the 5-10 year projection used in the DCF.
