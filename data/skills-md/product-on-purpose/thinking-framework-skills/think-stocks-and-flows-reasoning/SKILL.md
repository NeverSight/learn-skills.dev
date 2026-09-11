---
name: think-stocks-and-flows-reasoning
description: Produces a stock-flow map by separating a quantity that accumulates from the inflows and outflows that change it, then reasoning about the stock's trajectory from the net flow rather than the direction of any single flow. Use when a problem involves an accumulation (cash, debt, backlog, headcount, customer base, technical debt, emissions) and intuition about whether it is rising or falling may be wrong.
license: Apache-2.0
metadata:
  id: thinking-framework-skills.stocks-and-flows-reasoning
  family: systems-and-consequences
  evidence-tier: "S"
  version: 0.1.0
  standard: "0.8"
---
<!-- thinking-framework-skills | https://github.com/product-on-purpose/thinking-framework-skills | Apache-2.0 -->
# Stocks and Flows Reasoning

People systematically misjudge accumulations. They confuse a stock (a quantity that builds up: cash, debt, a customer base, a backlog, technical debt) with the flows that change it, and infer the stock's direction from a flow's direction. The classic error: "the inflow is falling, so the stock is falling." It is not - the stock keeps rising while inflow exceeds outflow. This skill makes the structure explicit: name the stock, name its inflows and outflows separately, and reason about its trajectory from the net flow. The output is a **stock-flow map**. It corrects a specific, well-evidenced accumulation error; it does not claim to teach systems thinking wholesale.

## When to Use

- A quantity accumulates over time (runway, debt, backlog, headcount, customer base, reserves, technical debt) and the question is whether it is rising or falling.
- A trend in a flow is being used to infer the stock ("churn dropped, so the base is growing").
- Before acting on an "it's getting better/worse" intuition about an accumulation.

## When NOT to Use

- The quantity does not accumulate (a one-off event, a ratio with no stock).
- A simple direct relationship with no accumulation is all that is at play.
- Mapping forward consequences (use futures-wheel) or systemic causes (use iceberg-model); this is specifically about accumulation dynamics.

## Instructions

When asked to reason about an accumulating quantity, follow these steps:

1. **Name the stock.** The quantity that accumulates, and its current level if known. Make sure it is a stock (a level), not a flow (a rate).
2. **List the inflows.** What adds to the stock, and at what rate / trend.
3. **List the outflows.** What drains the stock, and at what rate / trend. Do not skip the outflow - ignoring it is a common error.
4. **Compute the net flow.** Inflow minus outflow: is the stock currently gaining or losing, and is the net flow itself trending up or down?
5. **State the corrected trajectory.** What the stock actually does (rises / falls / plateaus and when), derived from the net flow, not from any single flow's direction.
6. **Name the naive intuition it corrects.** What someone would wrongly conclude from the flow alone, and why it is wrong.
7. **Emit the stock-flow map** per `references/TEMPLATE.md`.

## Output Format

Use the template in `references/TEMPLATE.md`. The deliverable is the stock-flow map with the corrected trajectory, not prose.

## Quality Checklist

Before finalizing, verify:

- [ ] The stock is genuinely a level (accumulation), not a flow/rate.
- [ ] Both inflows and outflows are listed; the outflow is not ignored.
- [ ] The trajectory is derived from the net flow, not from one flow's direction.
- [ ] The naive intuition being corrected is named.
- [ ] No overclaim: it corrects an accumulation error, it does not teach systems thinking wholesale (see `evidence/dossier.md`).
- [ ] The output is the stock-flow map artifact, not prose.

## Evidence

Tier **S**. The underlying failure is robustly demonstrated: across repeated experiments, including with highly educated subjects, people misread stock/flow relationships and infer stock direction from flow direction (Sterman's accumulation experiments; Cronin, Gonzalez & Sterman 2009; Meadows, *Thinking in Systems*). The strong evidence is that the error is real and that making the structure explicit removes it on a given problem; it is not a claim of broad systems-thinking transfer. Evidence is from human reasoners, transferred to AI use, not AI-validated. Full grading: `evidence/dossier.md`.

## Examples

See `references/EXAMPLE.md` for a completed stock-flow map.
