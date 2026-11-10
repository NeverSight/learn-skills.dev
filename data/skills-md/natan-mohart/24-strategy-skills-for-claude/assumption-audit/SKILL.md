---
name: assumption-audit
description: Surfaces every unstated belief a strategy or business case depends on, grades the evidence behind each one, and stress-tests the ones that would break the plan if wrong — using a load-bearing-assumption framework, not a generic risk brainstorm. Use before any strategy, business case, or major decision is finalized or presented, whenever the user asks "what could go wrong," "are we sure about this," or wants a pre-mortem, or when a plan has gone unchallenged for a while.
---

# Assumption Audit

## When to use
Use before finalizing or presenting any strategy, business case, or major decision — especially one that has been worked on for a while by a small group, since that's when unstated beliefs calcify into "known facts." Also use as a dedicated pre-mortem step before launch, and any time someone says "we all agree this will work" without anyone having named why.

## What it does
Extracts the assumptions a plan silently rests on (not just the ones people are willing to say out loud), classifies each by evidence quality, and identifies which ones are load-bearing — meaning if they're wrong, the plan doesn't just underperform, it fails. It then designs the cheapest test that would falsify each load-bearing assumption before real capital is committed.

## Method
1. **Reverse-engineer assumptions from the plan, don't just ask people what they assume.** For every claim, number, or causal link in the strategy ("customers will pay $X," "channel Y will scale," "competitor Z won't respond"), ask "what would have to be true for this to hold?" — that's the assumption.
2. **Classify each assumption's evidence base**: proven (direct evidence from this business), analogous (evidence from a comparable situation elsewhere), or belief (no real evidence, just conviction or precedent-by-repetition).
3. **Score each assumption on two axes**: how much the plan's outcome depends on it (impact if wrong), and how confident the evidence base is (confidence). Plot on a 2x2 — high impact / low confidence is the danger zone.
4. **Distinguish load-bearing from decorative.** A load-bearing assumption, if false, breaks the plan's core logic (e.g., "the market will pay a premium for X"). A decorative one just changes a detail (e.g., "the launch color will be blue"). Focus scrutiny only on load-bearing ones — auditing every assumption equally dilutes attention from the ones that matter.
5. **Run a pre-mortem on each high-impact/low-confidence assumption**: "assume this failed — what evidence would we see, and could we have seen it earlier?" This surfaces failure modes faster than asking "what could go wrong" in the abstract.
6. **Design the cheapest falsification test for each danger-zone assumption** — a pilot, a customer interview round, a pricing test, a competitor-response scenario — sequenced by which one, if it fails, kills the plan earliest and cheapest.
7. **Write the "if we're wrong" trigger**: for each load-bearing assumption, name the specific signal that would tell the team it's wrong in time to change course, not after the capital is spent.

## Inputs
- The strategy document, business case, or plan being audited
- Any existing supporting data or research behind key claims
- The team's actual timeline and capital already committed (affects which tests are still cheap)

## Output format
A table of assumptions with evidence class, impact, confidence, and load-bearing flag; an impact×confidence 2x2 highlighting the danger zone; a sequenced list of falsification tests for danger-zone assumptions; a named early-warning trigger for each load-bearing assumption.

## Example
A retailer's international expansion case rests on "brand awareness will transfer without local marketing spend." It's high-impact (the whole margin case assumes low customer acquisition cost) and low-confidence (belief, based on one adjacent market that had different distribution). It lands in the danger zone. The cheapest test: a small paid-media-free pilot in one city, measuring organic sign-up rate against the assumed number, before the full market entry budget is approved.

## Common pitfalls
- Auditing assumptions people are already comfortable stating, while missing the ones baked so deep into the plan that no one thinks to name them.
- Treating every assumption as equally worth testing instead of triaging to the load-bearing ones.
- Running the audit after the decision is effectively already made, turning it into theater instead of a real gate.
- Designing tests that are more expensive than just committing to the plan and watching what happens — defeats the purpose.
