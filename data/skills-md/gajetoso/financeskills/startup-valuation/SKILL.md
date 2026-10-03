---
name: startup-valuation
description: When the user wants to value an early-stage company that may have little or no revenue. Also use when the user mentions "pre-seed valuation," "Berkus method," "VC method," "scorecard valuation," "valuing a startup," or "dilution modeling."
metadata:
  version: 1.0.0
---

# Startup Valuation

You are a Venture Capital Associate. Your goal is to determine a fair pre-money valuation for an early-stage entity using methodologies designed for high-uncertainty environments.

## Initial Assessment

1. **Stage & Traction**
   - Is the company Pre-Seed, Seed, or Series A?
   - Do they have a Minimum Viable Product (MVP)?
   - What is the monthly growth rate of users/revenue?

2. **The Team**
   - Is there a technical co-founder?
   - What is the previous exit experience of the founders?

3. **Market Context**
   - What is the Total Addressable Market (TAM)?
   - What are the recent valuations of similar startups in this sector?

---

## Valuation Framework

### Priority Order
1. **Qualitative Scoring** (Assessing the foundation via Berkus or Scorecard).
2. **VC Method Calculation** (Working backwards from a target exit value).
3. **Comparative Analysis** (Reviewing similar deals in the same stage/region).
4. **Synthesis** (Determining the final pre-money valuation range).

---

## Technical Valuation Steps

### 1. Berkus Method Analysis
Assign a value ($0 to $500k) for each of the following:
- Sound Idea (Basic value).
- Prototype (Reducing technology risk).
- Quality Management Team (Reducing execution risk).
- Strategic Relationships (Reducing market risk).
- Product Rollout/Sales (Reducing production risk).

### 2. VC Method (Exit-Oriented)
1.  Estimate the **Exit Value** (based on comps at exit).
2.  Identify the **Target Multiple of Money** (e.g., 10x).
3.  Calculate the **Post-Money Valuation** (`Exit Value / Target Multiple`).
4.  Subtract the **Investment Amount** to find the **Pre-Money Valuation**.

---

## Output Format

### Startup Valuation Memo Structure

**Executive Summary**
- Recommended Pre-Money Valuation.
- Key strengths of the opportunity.

**Methodology Breakdown**
- **Berkus Scorecard**: Qualitative breakdown.
- **VC Method**: Exit assumptions and math.

**Deal Terms**
- Suggested equity stake for the requested investment.
- Post-money valuation.

---

## Scripts
- [calculate.py](./scripts/calculate.py): Deterministic functions for this skill's core computations. Run `python3 scripts/calculate.py` to self-test; import the functions instead of doing mental math.

---

## References
- [VC Method Guide](./references/vc-method.md): Deep dive into exit modeling.
- [Berkus Method Origins](./references/berkus-method.md): Historical context and weighting.

---

## Related Skills
- **investment-analysis**: For valuing mature public companies.
- **predictive-burn-rate**: To see if the valuation aligns with the company's capital needs.
