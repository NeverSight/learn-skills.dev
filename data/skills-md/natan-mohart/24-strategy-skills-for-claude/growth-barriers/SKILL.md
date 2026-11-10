---
name: growth-barriers
description: Diagnoses stalled or slowing growth by decomposing the funnel and cohort data to isolate the single binding constraint, using Theory of Constraints logic rather than fixing whatever complaint is loudest. Use whenever the user says growth has stalled, plateaued, or slowed, asks "why aren't we growing," wants to fix churn/acquisition/expansion, or is about to launch initiatives across multiple teams without knowing which one actually matters.
---

# Growth Barriers

## When to use
Use when growth has flattened or reversed and the organization has several competing theories (marketing says demand is soft, product says onboarding is broken, sales says pricing is off) but no one has tested which one is actually binding. Also use before greenlighting a growth initiative portfolio, so effort isn't spread across five fixes when only one is load-bearing.

## What it does
Applies Theory of Constraints to the growth funnel: decomposes the funnel stage by stage and cohort by cohort, finds the stage where the conversion or retention curve breaks compared to its historical or peer baseline, and separates the one binding constraint from everything else that is a real but non-limiting weakness. Fixing a non-binding weakness does not move the growth rate — this is the method's core discipline.

## Method
1. **Map the full funnel with real stages**: awareness → acquisition → activation → retention → expansion → referral (adapt labels to the business, but keep every stage — don't start the analysis mid-funnel).
2. **Baseline each stage's conversion rate against its own trailing 12-month trend and, where available, a comparable peer/benchmark** — not against a gut-feel target.
3. **Cut by cohort, not blended aggregate.** Growth problems almost always live in one acquisition cohort, channel, segment, or vintage; a blended trend can look "slowly declining" when the truth is "healthy legacy cohort masking a collapsed new cohort."
4. **Apply the Theory of Constraints test at each stage**: if you fixed this stage in isolation, would overall growth improve, or would the next stage immediately cap it? The true constraint is the stage where fixing it visibly moves the end metric; everything downstream of a worse constraint is not yet the bottleneck, even if it also has a low conversion rate.
5. **Quantify the constraint's ceiling**: model what growth rate is achievable if the binding stage were fixed to benchmark, holding all other stages constant. This becomes the size-of-the-prize.
6. **Rule out false positives**: check whether the apparent constraint is actually a lagging symptom of an earlier stage (e.g., "poor activation" that is really "wrong-fit users from a broad top-of-funnel channel").
7. **Name the single binding constraint and the two or three next-most-binding stages**, explicitly ranked — resist producing an unranked list of "areas for improvement."

## Inputs
- Funnel-stage conversion data, ideally 12+ months, by cohort/channel/segment
- Historical growth rate and the target growth rate
- Any prior initiatives already tried at each stage and their measured effect

## Output format
Funnel diagram with stage-by-stage conversion vs. baseline; cohort cuts showing where the break is concentrated; the named binding constraint with the Theory-of-Constraints logic for why it's binding (not just weak); size-of-the-prize if it's fixed; ranked list of secondary constraints to revisit once the primary one is resolved.

## Example
Growth has stalled at a SaaS company. Marketing wants more ad spend; product wants to rebuild onboarding. The funnel cut shows top-of-funnel and activation are both flat and in line with benchmark — the break is in month-2 retention for the cohort acquired via a specific paid channel launched two quarters ago. Fixing onboarding would not move growth, because those users already activate fine; the constraint is a fit problem in one acquisition channel, not a product problem.

## Common pitfalls
- Fixing the loudest complaint instead of the measured constraint.
- Analyzing a blended funnel and missing a cohort-concentrated break.
- Confusing a symptom (low activation) with the actual constraint (wrong-fit top-of-funnel).
- Producing a flat list of "opportunities" instead of one ranked, evidenced binding constraint.
