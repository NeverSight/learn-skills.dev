---
name: pricing-strategy
description: Sets or tests pricing using willingness-to-pay research (Van Westendorp) and price elasticity revenue/margin modeling, both run through a bundled calculator, instead of cost-plus guessing or copying a competitor's price. Use whenever the user wants to set, raise, lower, or test a price, is launching a new product/tier, asks "what should we charge," or is about to price based on cost-plus or "what competitors charge" alone.
---

# Pricing Strategy

## When to use
Use whenever a price needs to be set or changed and the current approach is cost-plus (price = cost + target margin, ignoring what the customer will actually pay) or competitor-matching (copying a rival's price without checking whether your value proposition is comparable). Also use to test a proposed price change before committing to it.

## What it does
Grounds pricing in two independent, complementary methods run through a bundled calculator: Van Westendorp Price Sensitivity (four-question willingness-to-pay survey, giving an acceptable price range and a floor below which customers doubt quality) and price elasticity modeling (revenue and margin at each price point given an estimated or tested elasticity coefficient) — so the recommendation is bounded by real customer behavior, not internal cost structure alone.

## Method
1. **Run or collect Van Westendorp responses**: ask a representative sample four questions per product — at what price is this so cheap you'd doubt the quality; a bargain; starting to feel expensive; so expensive you wouldn't consider it. Minimum ~30 responses for a directional read, 100+ before a launch-critical decision.
2. **Run the bundled calculator's Van Westendorp module** (`scripts/pricing_calculator.py`) to get the four crossing points and the acceptable price range — the floor (below which quality is doubted) and ceiling (above which it's rejected outright) bound your pricing options before elasticity is even considered.
3. **Estimate or obtain a price elasticity coefficient** — from a real price test if you have one, from category benchmarks if you don't (call this out explicitly as an assumption, not a fact, if it's a benchmark).
4. **Run the elasticity module** across a realistic price-test range to see revenue and margin at each point — these two often peak at different prices, and the choice between them is a real strategic call, not a math problem.
5. **Overlay the Van Westendorp range on the elasticity table**: discard any price points outside the acceptable range regardless of what the elasticity model says, since a price outside the willingness-to-pay range risks brand/quality perception damage the elasticity model doesn't capture.
6. **Check for a Kano-style structure if pricing tiers/packaging**: which features are must-haves (expected, don't differentiate price), performance features (linear value, price scales with them), and delighters (disproportionate willingness to pay) — use this to decide what goes in which tier, not just what's cheap to build.
7. **Recommend a price with the explicit trade-off named**: "recommend $X, which is the revenue-maximizing point within the Van Westendorp acceptable range; margin-maximizing would be $Y but falls outside/inside the range for reason Z."

## Inputs
- Van Westendorp survey responses (or a plan to collect them) as arrays of four values per respondent
- Current price, volume, and unit cost
- An elasticity coefficient (measured or benchmarked) and a realistic price-test range
- Config saved as JSON matching the format documented at the top of `scripts/pricing_calculator.py`

## Output format
Van Westendorp acceptable price range with all four crossing points; elasticity table showing volume/revenue/margin at each tested price with the revenue-max and margin-max points flagged; a single recommended price with the trade-off named explicitly; any tier/packaging implications from the Kano check.

## Example
A SaaS product currently priced at $29 shows a Van Westendorp acceptable range of $24-$37, and the elasticity table shows revenue peaks at $24 but margin peaks at $29. Since both are inside the acceptable range, the recommendation names the actual choice: hold at $29 for margin, or move to $24 to prioritize growth/market share — a decision for the business, not a number the model can pick alone.

## Common pitfalls
- Setting price purely from cost-plus math, ignoring what customers will actually pay.
- Treating an elasticity coefficient pulled from a generic benchmark as if it were measured for this specific product and audience.
- Optimizing for revenue or margin without checking the price against the Van Westendorp range, risking a technically "optimal" price that customers reject on sight.
