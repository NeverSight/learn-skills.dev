---
name: product-review
description: Run a structured review of a product bet, initiative, roadmap, launch, or evidence packet and return a decision with gaps and next actions. Use when the user asks for critique, a product review, a go/no-go decision, an executive review, or an audit across value, usability, feasibility, viability, evidence, and operations.
---

# Product Review

Review a product decision against its declared outcome and evidence, then identify the smallest set of gaps that block a responsible decision.

## Inputs

- Artifact or proposal under review
- Decision requested and decision owner
- Target customer, outcome, and strategy
- Evidence and source dates
- Constraints, dependencies, and launch horizon
- Known dissent and open risks

## Workflow

1. State the requested decision and falsifiable success criterion.
2. Reconstruct the product bet: customer, problem, intervention, mechanism, outcome, and business value.
3. Audit evidence provenance and separate observed, reported, inferred, and assumed claims.
4. Review value, usability, feasibility, and business viability.
5. Review strategy fit, alternatives, non-goals, and opportunity cost.
6. Review metrics, experiment logic, instrumentation, guardrails, and stop rules.
7. Review operational readiness, ownership, dependencies, failure recovery, and stakeholder alignment.
8. Rank gaps as blocker, important, or monitor.
9. Decide: proceed, proceed with conditions, run a targeted test, rework, pause, or stop.

## Output contract

Return executive decision, reconstructed bet, evidence ledger, four-risk assessment, strategic fit, measurement review, readiness review, ranked gaps, required actions with owners, and next review trigger.

## Quality gate

- The decision is explicit and owned.
- Blockers are tied to consequence, not preference.
- Positive evidence receives the same provenance scrutiny as negative evidence.
- Conditions are observable and time-bounded.
- The review names what was not verified.

## Avoid

- Vague “looks good” feedback
- Reviewing polish while ignoring the decision
- Treating stakeholder agreement as customer evidence
- Adding a long wish list unrelated to launch risk
- Approving plumbing, plans, or prototypes as proof of real behavior

## Source grounding

Operational synthesis combining the four product risks from *Inspired*, evidence and assumption practices from *Continuous Discovery Habits* and *The Mom Test*, strategy coherence from *Good Strategy/Bad Strategy*, outcome discipline from *Escaping the Build Trap*, lifecycle metrics from *Lean Analytics*, and AI-system readiness principles from *Building AI-Powered Products* and *Designing Machine Learning Systems*.
