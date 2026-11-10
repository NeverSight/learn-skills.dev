---
name: capital-reallocation-review
description: Scores a multi-business portfolio on a weighted GE-McKinsey 9-box via a bundled calculator, then measures how aggressively capital actually moves between business units year over year — grounded in McKinsey's own "Power of Capital Reallocation" research, which found companies that reallocate capital most aggressively deliver materially higher shareholder returns than those that don't. Use whenever the user wants a portfolio review, capital allocation recommendation, or investment committee prep, or when budget-setting is just "last year's allocation plus a few percent" with no real reallocation happening.
---

# Capital Reallocation Review

## When to use
Use whenever a company has multiple business units, product lines, or major initiatives competing for capital and needs an objective view of where to invest, hold, or exit — and especially when the annual budgeting process is actually just incremental adjustment of last year's numbers rather than a genuine reallocation decision. McKinsey's long-running capital reallocation research (tracking thousands of companies over decades) found that companies in the top quintile of capital reallocation intensity delivered meaningfully higher total shareholder returns than companies in the bottom quintile — and that most companies reallocate far less than they think they do.

## What it does
Scores each business unit on a weighted, multi-factor industry attractiveness axis and a weighted, multi-factor competitive strength axis (the GE-McKinsey 9-box method), computes a zone recommendation per unit via the bundled calculator, and separately measures the company's actual reallocation intensity — how much capital genuinely moved between units over the past 3-5 years — against the attractiveness/strength findings, surfacing the gap between where capital should go and where it's actually going.

## Method
1. **Define attractiveness factors and weights**: market growth, market size, profitability, competitive intensity (inverted) are a solid default — agree weights with the decision-maker before scoring, not after.
2. **Define strength factors and weights**: relative market share, margin versus peers, brand strength, capability fit to the parent's core competencies.
3. **Score every business unit 1-10 on every factor** with evidence behind each score.
4. **Run the bundled calculator** (`scripts/portfolio_matrix.py`) to get weighted attractiveness/strength, 9-box zone placement per unit, and the share of total revenue sitting in each zone.
5. **Measure actual reallocation intensity**: pull capital/budget allocation by business unit for each of the past 3-5 years and compute what percentage of total capital has genuinely shifted between units year over year (not organic growth within a unit — actual reallocation of the budget base). McKinsey's research uses this as the single clearest predictor of whether a "portfolio strategy" is real or just a slide.
6. **Compare reallocation intensity to peer benchmarks** where available — companies in the top quintile of McKinsey's studies typically reallocated a materially larger share of capital annually than median performers; a company reallocating in the low single digits per year is very likely under-reallocating relative to what the evidence supports.
7. **Overlay the 9-box zones onto the reallocation history**: are invest/grow units actually receiving more capital year over year, and are harvest/divest units actually shrinking? If the zones and the money flow disagree, that's the central finding — a strategy that exists on a slide but isn't showing up in the budget.
8. **Recommend a specific reallocation move**: name the amount and the from/to units, tied directly to the 9-box zones, sized against what the reallocation-intensity benchmark suggests is achievable without destabilizing the business.

## Inputs
- List of business units/products with revenue
- Agreed attractiveness and strength factors/weights, with evidence-backed scores
- Capital/budget allocation by business unit for the past 3-5 years
- Config saved as JSON matching the format documented at the top of `scripts/portfolio_matrix.py`

## Output format
9-box placement per business unit; portfolio-level revenue share by zone; measured reallocation intensity (% of capital that moved between units per year) against benchmark; explicit comparison of where the 9-box says capital should go vs. where it's actually gone; a specific, sized reallocation recommendation by unit.

## Example
A three-unit portfolio shows the legacy line correctly flagged as harvest/divest (36% of revenue), but the 5-year capital history shows its budget has only shrunk 2% over that period while the invest/grow core product's budget grew just 3% — reallocation intensity is far below what the evidence-based benchmark would suggest for a healthy portfolio. The recommendation: a specific 3-year glide path moving a stated dollar amount from the legacy line to the core product and the selectively-funded new bet, not just a one-time "let's discuss reallocation" conversation that produces no actual budget change.

## Common pitfalls
- Producing 9-box placements as a static one-time exercise without checking whether the company's actual budget process ever reflects them.
- Treating organic growth within a unit as "reallocation" when the real question is whether capital moved between units.
- Recommending reallocation without sizing it against what's actually achievable — a number too aggressive to be credible gets ignored, a number too timid doesn't move the portfolio.
