---
name: risk-mitigation
description: Scores strategic and execution risks on likelihood, impact, AND velocity (how fast a risk could hit) via a bundled calculator — catching fast-moving risks a standard 2-factor heat map underranks — then forces a named owner and mitigation for every high-priority item. Use whenever the user wants a risk register, risk assessment, or mitigation plan for a strategy or initiative, or has a risk list with no prioritization, owners, or mitigation actions attached.
---

# Risk Mitigation

## When to use
Use whenever a strategy, initiative, or business case needs a real risk assessment — especially replacing a risk list that's just a bulleted set of concerns with no scoring, no owners, and no distinction between a risk that's a slow background hum and one that could hit within weeks.

## What it does
Scores every risk on likelihood, impact, AND velocity via a bundled calculator, producing a priority tier that a plain likelihood×impact heat map would get wrong for fast-moving risks — a moderate-score, high-velocity risk (like an active regulatory change) needs urgent attention even though its raw score looks unremarkable next to a high-score, low-velocity one. It also flags any critical risk with no documented mitigation, so nothing dangerous slips through unowned.

## Method
1. **Inventory risks across categories**: strategic (market/competitive), operational (execution/delivery), financial (funding/covenant), regulatory/compliance, and reputational — don't limit the list to whatever category the requester happens to be worried about today.
2. **Score each risk 1-5 on likelihood** (probability it occurs in the relevant time horizon) and **1-5 on impact** (severity if it does) — with a one-line justification for each score, not just a number.
3. **Score each risk 1-5 on velocity**: how fast could it go from "not happening" to "fully materialized" — 1 for a risk that would take years to develop (giving time to react), 5 for one that could hit within weeks (leaving little reaction time even with good monitoring).
4. **Run the bundled calculator** (`scripts/risk_matrix.py`) to get the likelihood×impact score, a priority tier, and two flags: any critical risk missing a documented mitigation, and any moderate-score risk with high velocity that a plain heat map would underrank.
5. **Assign a named owner and a specific mitigation action to every risk tiered HIGH or CRITICAL** — "monitor closely" is not a mitigation; a mitigation names what specifically reduces likelihood or impact, and by when.
6. **For velocity-flagged risks, design a monitoring trigger, not just a mitigation plan** — the point of high velocity is that mitigation alone may not be enough; you also need an early-warning signal because there's little time to react once it starts.
7. **Review the register on a cadence matched to its content**: critical/high items reviewed monthly at minimum, moderate quarterly, low annually — a risk register that's built once and never revisited is closer to theater than to actual risk management.

## Inputs
- List of candidate risks across strategic/operational/financial/regulatory/reputational categories
- Likelihood, impact, and velocity scores (1-5) with justification for each
- Any existing mitigation already in place per risk
- Config saved as JSON matching the format documented at the top of `scripts/risk_matrix.py`

## Output format
Scored and tiered risk register (likelihood × impact × velocity); flagged critical risks with no mitigation; flagged high-velocity risks a static heat map would underrank; named owner and mitigation action per HIGH/CRITICAL risk; monitoring trigger per high-velocity risk; review cadence.

## Example
A regulatory change risk scores only 10 on likelihood×impact (moderate) but carries a velocity of 5/5 — it could hit within weeks once triggered. A plain heat map would file it below several higher-scoring but slow-moving risks; the velocity flag surfaces it for urgent monitoring anyway, with a named early-warning signal (a specific legislative tracking service) rather than a quarterly check-in that would be too slow to matter.

## Common pitfalls
- Building a risk register once and never revisiting it, so it stops reflecting reality within a quarter.
- Scoring only likelihood and impact, missing that a fast-moving moderate risk can be more dangerous than a slow-moving severe one because there's no time to react.
- Listing risks with no owner or mitigation action, which produces a document that looks thorough but changes nothing.
