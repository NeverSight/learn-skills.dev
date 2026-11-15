---
name: annual-operating-plan
description: Reconciles leadership's top-down target against the driver-based bottom-up build line by line via a bundled calculator, flagging every gap over 10% instead of quietly averaging the two into a number nobody actually believes. Use whenever the user is building the annual operating plan, needs to reconcile a leadership target with a bottoms-up model, or has a plan where the top-down ask and the bottom-up build were never actually compared line by line.
---

# Annual Operating Plan

## When to use
Use whenever the annual plan needs to reconcile what leadership wants (a top-down growth or margin target, often set for investor or board reasons) against what a driver-based bottom-up model actually produces. Especially use when the current "plan" is really just the top-down number with a supporting narrative built backward to justify it, rather than a genuine reconciliation.

## What it does
Compares top-down target and bottom-up build line by line via a bundled calculator, computes the gap and gap percentage for every line item, and flags any line with more than a 10% gap — forcing an explicit resolution (revise the target, find real drivers to close the gap, or accept it with a named owner) instead of letting the two numbers get quietly blended into a plan nobody actually built.

## Method
1. **Build the bottom-up plan first, independently.** Use driver-based-budget-builder's discipline: real volume, price, and cost drivers by department, not a top-down number divided by twelve.
2. **State the top-down target explicitly** — the number leadership or the board has in mind, and why (a growth rate expected by investors, a margin target tied to a prior commitment).
3. **Run the bundled calculator** (`scripts/aop_reconciliation.py`) to compare every line item, revenue, margin, opex, and any other planned metric, top-down versus bottom-up, with the gap and gap percentage shown.
4. **Treat every flagged gap (over 10%) as requiring one of three resolutions**, not a rounding error to smooth over: revise the top-down target to something the bottom-up model can actually support, find specific additional drivers (a new channel, a price change, a cost action) that would close the gap for real, or explicitly accept the gap with a named owner and a plan to close it during the year.
5. **Never let the published plan silently split the difference** between top-down and bottom-up without documenting which resolution was chosen and why — a plan that's an unexplained average of two numbers is not a real plan, it's a compromise nobody can defend later.
6. **Revisit the reconciliation at each planning checkpoint** (quarterly re-forecast), not just once at the start of the year — the gap-closing actions from step 4 need to actually show up in the numbers, or the same gap reappears next cycle.

## Inputs
- Top-down targets by line item with the rationale behind each
- Bottom-up, driver-based build for the same line items
- Config saved as JSON matching the format documented at the top of `scripts/aop_reconciliation.py`

## Output format
Line-by-line table of top-down target, bottom-up build, gap, and gap percentage; explicit flag for every line item over a 10% gap; required resolution stated for each flagged item (revised target, closing drivers, or accepted gap with owner).

## Example
Leadership's top-down revenue target is $24M; the bottom-up build, based on realistic sales capacity and conversion rates, comes to $21.5M, a 10.4% gap the calculator flags immediately. Rather than publishing $24M with a hopeful narrative, the resolution names two specific closing drivers (a new outbound motion and a price increase on renewals) sized to close roughly half the gap, with the remaining gap explicitly accepted and owned by the sales VP with a Q2 checkpoint.

## Common pitfalls
- Publishing the top-down number as the plan without ever showing the bottom-up build that was supposed to support it.
- Averaging top-down and bottom-up into a compromise number with no stated rationale for the blend.
- Reconciling once at the start of the year and never revisiting whether the gap-closing actions actually materialized.
