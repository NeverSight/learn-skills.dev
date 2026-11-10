---
name: full-potential-diagnostic
description: Sizes the dollar value at stake between current performance and top-quartile benchmark on every relevant P&L and working-capital metric via a bundled calculator — the actual "full potential" framing used to size transformation programs, not a vague sense that "there's room to improve." Use whenever the user wants to size a transformation opportunity, benchmark performance against best practice, build the case for a performance improvement program, or has a transformation ambition with no quantified size of the prize behind it.
---

# Full-Potential Diagnostic

## When to use
Use at the start of any performance improvement or transformation program to size the actual opportunity before committing to initiatives — replacing a vague "we think there's meaningful upside" with a quantified, metric-by-metric value-at-stake number. Also use to build the business case for launching a transformation, since a credible size-of-the-prize is usually what gets a program funded in the first place.

## What it does
Compares current performance to a top-quartile or best-practice benchmark across every relevant metric (margin, cost ratios, working capital efficiency, productivity), converts each gap into a dollar value via a bundled calculator, and rolls the metrics into a single total value-at-stake figure — giving the transformation program a size, not just a direction.

## Method
1. **Select the metrics that matter for this business**: typically gross margin, SG&A as % of revenue, working capital efficiency (inventory turns, DSO/DPO), and productivity metrics (revenue per employee) — chosen for relevance to this specific business, not a generic checklist applied blindly.
2. **Establish current performance** for each metric from actual financials, not estimates.
3. **Establish the benchmark**: top-quartile performance among true peers (same industry, similar scale) where available; where peer data doesn't exist, use the best internal benchmark (a comparable business unit, region, or plant) rather than an arbitrary aspirational number.
4. **Run the bundled calculator** (`scripts/full_potential_calc.py`) to convert each metric's gap into a dollar value at stake — percentage-of-revenue metrics translate directly; working-capital metrics translate through the capital freed by moving to benchmark efficiency.
5. **Sum to a total value-at-stake figure and express it as a percentage of revenue** — this is the number that anchors the transformation's ambition level in front of the board or investment committee.
6. **Apply a realistic capture-rate discount explicitly**, rather than presenting the raw gap as an expected outcome: real full-potential programs typically capture something well short of 100% of the identified gap within a realistic timeframe, and stating this openly is what makes the diagnostic credible rather than a sales pitch.
7. **Rank the metrics by value at stake and pass the top few into initiative-prioritizer or transformation planning** — the diagnostic sizes the opportunity, it does not by itself tell you how to capture it; that's the next step, not this one.
8. **Revisit the diagnostic periodically during the program** (not just once at the start) to track how much of the identified gap has actually closed — this connects directly to a value-realization discipline later in the program.

## Inputs
- Current financial performance by metric
- Peer or internal benchmark data for each metric
- Revenue base and, for working-capital metrics, the relevant working-capital base
- Config saved as JSON matching the format documented at the top of `scripts/full_potential_calc.py`

## Output format
Metric-by-metric table of current vs. benchmark vs. dollar value at stake; total value at stake as an absolute number and as % of revenue; explicit capture-rate caveat; ranked list of highest-value metrics to prioritize in the transformation plan.

## Example
A $120M-revenue business shows a combined value at stake of $23.2M (19% of revenue) across gross margin, SG&A ratio, and inventory turns gaps to top-quartile peers. Rather than presenting $23.2M as the transformation's expected outcome, the diagnostic states the realistic range (40-70% capture within 18-24 months, based on typical program performance) — giving the board a credible $9-16M target instead of an inflated headline number that erodes trust when the program under-delivers against it.

## Common pitfalls
- Presenting the full theoretical gap as the expected outcome instead of applying a realistic, stated capture-rate discount.
- Benchmarking against an aspirational or cherry-picked "best in class" example instead of a true, comparable peer set.
- Running the diagnostic once at kickoff and never returning to it during the program to check actual progress against the sized opportunity.
