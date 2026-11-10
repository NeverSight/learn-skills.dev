---
name: initiative-prioritizer
description: Ranks competing initiatives with a bundled RICE (Reach x Impact x Confidence / Effort) calculator that also flags when a lower-scoring initiative has a much higher cost of delay and should be sequenced earlier anyway. Use whenever the user has a backlog or roadmap of competing initiatives to prioritize, needs to decide what to work on first, or is prioritizing by gut feel, HiPPO (highest paid person's opinion), or squeaky-wheel urgency.
---

# Initiative Prioritizer

## When to use
Use whenever more initiatives exist than capacity to do them, and the current prioritization method is either informal (whoever argues loudest, or the most senior person's preference) or a single flat "priority: high/medium/low" tag that doesn't actually rank anything against anything else.

## What it does
Scores every initiative on RICE (Reach × Impact × Confidence ÷ Effort) via a bundled calculator for a defensible relative ranking, then overlays a cost-of-delay check — because RICE alone ranks by expected value per unit of effort and says nothing about urgency, which means a slower-but-time-sensitive initiative (a closing market window, a compliance deadline) can get silently mis-sequenced if the RICE rank is applied mechanically.

## Method
1. **Score Reach**: how many customers/users/dollars this touches in a defined time period (e.g., per quarter) — use a real number, not a category.
2. **Score Impact** on the standard RICE scale: 3 = massive, 2 = high, 1 = medium, 0.5 = low, 0.25 = minimal. Resist inflating everything to "high impact" — this is the step most prioritization exercises fudge.
3. **Score Confidence** as a percentage reflecting how solid the evidence behind reach/impact estimates actually is — 100% only for measured/proven effects, 80% for strong indirect evidence, 50% or below for a hypothesis with little backing.
4. **Estimate Effort** in person-weeks (or another consistent unit) — including the realistic full cost, not just the most visible engineering piece.
5. **Estimate cost of delay** for each initiative where it applies: monthly value lost by not shipping it now (lost revenue, compounding risk, closing window, deadline penalty). Zero is a valid answer for initiatives with no real urgency.
6. **Run the bundled calculator** (`scripts/rice_prioritizer.py`) to get the RICE score per initiative and a flag whenever the highest-cost-of-delay initiative isn't also the top RICE-ranked one.
7. **Resolve flagged conflicts explicitly** with the decision-maker: is the urgency real enough to sequence ahead of a higher-RICE item, or is it manufactured urgency that shouldn't override the evidence-based ranking? Write down the answer and why.
8. **Publish the ranked list with the reasoning visible** (scores, not just the final order) so the prioritization can be challenged and defended on the actual inputs, not just trusted blindly.

## Inputs
- List of candidate initiatives with reach, impact, confidence, and effort estimates
- Monthly value-if-delayed estimate per initiative, where applicable
- Config saved as JSON matching the format documented at the top of `scripts/rice_prioritizer.py`

## Output format
RICE-ranked table with reach/impact/confidence/effort inputs shown; cost-of-delay column; explicit flag and resolution note for any initiative where cost-of-delay contradicts the RICE rank; final published priority order with visible reasoning.

## Example
A compliance certification scores low on RICE (narrow reach, modest confidence, high effort) but carries a $40,000/month cost of delay tied to a hard regulatory deadline — the calculator flags it as out of step with its RICE rank. The team explicitly overrides the RICE order for this one item, documents why, and keeps RICE as the default rule for everything else — rather than either blindly following RICE or letting every "urgent" request jump the queue unchallenged.

## Common pitfalls
- Letting the loudest stakeholder's "this is urgent" claim skip the queue without a documented cost-of-delay to back it up.
- Inflating impact scores across the board so every initiative looks like a 2 or 3, which collapses the ranking's usefulness.
- Applying the RICE rank mechanically and missing a genuinely time-sensitive initiative that needed to move earlier.
