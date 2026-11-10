---
name: unit-economics-health-check
description: Computes LTV:CAC ratio and CAC payback period via a bundled calculator that models churn decaying realistically over the customer lifetime, instead of the naive ARPU-over-flat-churn shortcut that overstates LTV whenever churn is front-loaded (which it almost always is). Use whenever the user wants to check if growth spend is healthy, is deciding whether to increase customer acquisition budget, needs an LTV:CAC number for a board or investor update, or has an LTV calculation that assumes one flat churn rate forever.
---

# Unit Economics Health Check

## When to use
Use whenever a growth or marketing budget decision depends on whether acquiring customers is actually creating value, not just revenue — before increasing acquisition spend, before a board or investor conversation that needs an LTV:CAC number, or whenever an existing LTV calculation uses the shortcut formula (average revenue ÷ churn rate) without checking whether churn is actually flat over time.

## What it does
Models customer lifetime value month by month using an actual (or estimated) churn curve rather than one flat churn rate, discounts future contribution margin back to present value, and computes LTV:CAC ratio and CAC payback period via a bundled calculator — catching the single most common way unit economics get overstated: assuming the low, stable churn rate of a mature cohort applies from month one, when new customers almost always churn faster than tenured ones.

## Method
1. **Gather CAC**: fully loaded cost per acquired customer, including sales and marketing spend, not just ad spend — a CAC that excludes sales team cost or content production cost is understated and will inflate the ratio.
2. **Gather monthly revenue per customer and gross margin percentage** — LTV should be built on contribution margin, not revenue, since revenue ignores the cost of serving the customer.
3. **Build or estimate a monthly churn curve for at least the first 12 months**, not a single flat rate. If actual cohort data exists, use it directly; if not, a reasonable estimate (higher churn in months 1-3, declining toward a stable rate by month 6-12) is far more honest than assuming the eventual stable rate applies from day one.
4. **Run the bundled calculator** (`scripts/unit_economics.py`) to get month-by-month survival, contribution margin, cumulative discounted LTV over a 36-month horizon, LTV:CAC ratio, and CAC payback period.
5. **Read the LTV:CAC ratio against the standard benchmark**: 3 or higher is generally healthy, 1.5-3 is marginal (growth may be adding revenue while destroying value per customer), below 1.5 means acquisition is likely destroying value regardless of top-line growth.
6. **Read the payback period alongside the ratio** — a healthy LTV:CAC ratio with a very long payback period (18+ months) still creates a real cash problem, since the business has to fund the gap between spending on CAC and recovering it, and that's a different problem than the ratio alone reveals.
7. **Segment the calculation by channel or cohort where the inputs differ materially** — a blended LTV:CAC can hide a channel that's badly underwater subsidized by one that's strongly profitable; the same discipline as market-mapping's disaggregation applies here.
8. **Recompute periodically, not once** — churn curves and CAC both drift as channels saturate and competition changes; a unit economics read from a year ago is not a current read.

## Inputs
- CAC (fully loaded, by channel/cohort if available)
- Monthly revenue per customer and gross margin percentage
- Monthly churn rate for at least the first 12 months, ideally from actual cohort data
- Discount rate (or use a standard 10-15% annual default if none exists)
- Config saved as JSON matching the format documented at the top of `scripts/unit_economics.py`

## Output format
Month-by-month survival and contribution margin table; discounted LTV, LTV:CAC ratio, and CAC payback period; a plain health read (healthy / marginal / value-destroying) against standard benchmarks; a flag if payback period creates a cash-funding risk even when the ratio looks fine.

## Example
A subscription business assumes a flat 3% monthly churn (its eventual stable rate) and calculates a healthy LTV:CAC of 4.2. Rebuilding the model with the actual first-year churn curve — 8% in month one, declining to 3% by month six — shows the real ratio is 2.3, solidly in marginal territory, with a 10-month payback that's fine on its own but means the growth budget can't scale as fast as the flat-churn model implied without straining cash.

## Common pitfalls
- Using the flat "ARPU divided by churn rate" LTV shortcut, which silently assumes the eventual stable churn rate applies from month one and materially overstates LTV.
- Calculating LTV on revenue instead of contribution margin, ignoring the cost of serving the customer.
- Reading the ratio without the payback period, missing a real cash-funding constraint even when the ratio looks healthy.
- Computing one blended LTV:CAC across all channels, hiding a channel that's destroying value subsidized by one that isn't.
