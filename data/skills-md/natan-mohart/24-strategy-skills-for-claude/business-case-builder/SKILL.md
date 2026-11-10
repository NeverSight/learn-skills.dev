---
name: business-case-builder
description: Builds a driver-based economic model — NPV, IRR, payback, and a real sensitivity grid — using a bundled calculator, then states the specific conditions required for the case to hold. Use whenever the user wants to build, check, or challenge a business case, ROI, or investment case, is deciding whether to fund an initiative, or has a business case that's just a single-point revenue projection with no sensitivity analysis.
---

# Business Case Builder

## When to use
Use whenever an initiative needs a funding decision and the "case" so far is a single optimistic revenue line with no downside scenario, no discount rate, and no stated conditions for success. Also use to stress-test someone else's business case before approving it.

## What it does
Builds a driver-based (not top-line-only) economic model: revenue, cost structure, and investment broken into their actual drivers, run through the bundled NPV/IRR calculator, and stress-tested with a real sensitivity grid across revenue and discount-rate assumptions — producing not just a number, but the conditions under which that number holds.

## Method
1. **Decompose revenue into real drivers**, not a single top-line growth assumption: volume × price, or customers × ARPU × retention — whichever actually governs this business. A one-line revenue forecast is not a model, it's a guess with decimals.
2. **Decompose cost into COGS (variable, scales with revenue) and opex (largely fixed in the near term)** by year, and be explicit about which costs actually scale and which don't — this is where most hand-built cases quietly overstate margin improvement.
3. **State the initial investment fully**: capex, working capital, and one-time launch costs, not just the visible capex line.
4. **Run the bundled calculator** (`scripts/npv_case.py`) with a JSON config of discount rate, initial investment, and per-year revenue/COGS%/opex. It returns annual cash flows, NPV, IRR (via bisection, no external dependencies), and payback period.
5. **Generate the sensitivity grid** (built into the same script): NPV across a range of revenue swings and discount-rate swings. This is the step that turns a single confident number into an honest range.
6. **Read the grid for the breakeven condition**: find the combination of revenue shortfall and discount rate at which NPV turns negative — that is the real risk boundary of the case, and it should be stated explicitly, not buried in an appendix.
7. **State the conditions required for the case to hold** in plain language: "this case requires revenue to reach at least X% of plan by year 2, and holds at discount rates up to Y%" — tied directly to the sensitivity grid, not a vague "assumptions may vary" disclaimer.

## Inputs
- Revenue drivers (volume, price, or customers/ARPU/retention) by year
- COGS % and opex by year
- Initial investment (capex + working capital + one-time costs)
- Discount rate (company's cost of capital or hurdle rate)
- Config saved as JSON matching the format documented at the top of `scripts/npv_case.py`

## Output format
Annual cash flow table; NPV, IRR, payback period; the revenue × discount-rate NPV sensitivity grid; a plain-language statement of the conditions required for the case to hold, anchored to where the grid turns negative.

## Example
An initiative shows a headline NPV of $3.35M at a 10% discount rate. The sensitivity grid shows NPV stays positive even at -20% revenue and +2pt discount rate — a genuinely robust case. A second initiative shows a similar headline NPV but turns negative at -10% revenue, meaning it only works if the plan is hit almost exactly — a much weaker case that looked identical before the grid was run.

## Common pitfalls
- Presenting a single-point NPV with no sensitivity, which hides how fragile the case actually is.
- Modeling revenue as one growth-rate line instead of real volume/price or customer/ARPU drivers.
- Leaving out working capital or one-time costs from the initial investment, overstating the return.
- Choosing a discount rate that flatters the case instead of using the company's actual cost of capital.
