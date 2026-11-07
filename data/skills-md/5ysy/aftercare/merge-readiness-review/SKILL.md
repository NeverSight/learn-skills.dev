---
name: merge-readiness-review
description: determine whether completed work is safe to merge, mergeable with follow-up, or should be held for refactor. use before merge, before calling work complete, after aftercare review findings have been addressed or deferred, or when a change has been sitting in review limbo and needs a final verdict.
---

# Merge Readiness Review

Announce at the start: "I'm using merge-readiness-review to produce one verdict with a risk-accounted reason."

## Core idea

The job here is judgment, not perfectionism. A change either ships, ships with named follow-ups, or holds. Each verdict is a bet against a specific kind of risk; the review makes the bet explicit and accountable. No verdict is "reviewed and unclear" — ambiguity itself is a decision to hold.

## Workflow

1. Collect the inputs:
   - All review findings from prior aftercare passes (architecture, boundary, pipeline, observability, dependency).
   - Evidence of fixes and deferrals for each finding.
   - Current test and verification confidence (what passes, what is flaky, what is unrun).
   - Handling-review-feedback summary, if applicable.
2. Walk [`checklist.md`](./checklist.md): gates for correctness, boundary damage, pipeline safety, observability floor, deferred findings.
3. Match the state against [`rubric.md`](./rubric.md) to assign one of three verdicts with a risk-accounted reason.
4. Write the verdict using [`report-template.md`](./report-template.md).
5. Compare to [`examples/go.md`](./examples/go.md) and [`examples/no-go.md`](./examples/no-go.md) to sanity-check the framing.

## The three verdicts

- **safe to merge** — no known merge-blocking risk; remaining findings are Low or accepted Medium follow-ups with owners.
- **merge with follow-up** — there are named High or Medium findings that will be addressed in a tracked follow-up with a deadline/trigger, and merging now is lower-cost than holding.
- **hold for refactor** — there are Critical findings, or unresolved High findings that cannot be safely deferred.

No fourth option. If you cannot assign one, you have not finished the review.

## Heuristics

- Prefer "safe to merge" over "merge with follow-up" when follow-ups are speculative rather than tracked.
- Prefer "hold" over "merge with follow-up" when the follow-up has no named owner or concrete trigger — "we'll get to it" is not a plan.
- A change that has been sitting in review for weeks is a signal the scope or the findings are unclear; clarify before assigning a verdict.

## Do not

- produce "looks good, just a few small things" as a verdict
- merge with unresolved Critical findings, even with apology
- hold indefinitely on Medium findings that are legitimately deferrable
- use "merge with follow-up" as a polite way to hide a "hold"

## Supporting files

- [`checklist.md`](./checklist.md) — pre-merge gates by category.
- [`rubric.md`](./rubric.md) — verdict categories with risk accounting, extending [`../../references/severity-model.md`](../../references/severity-model.md).
- [`report-template.md`](./report-template.md) — merge-verdict format extending [`../../references/report-templates.md`](../../references/report-templates.md).
- [`examples/go.md`](./examples/go.md) and [`examples/no-go.md`](./examples/no-go.md) — contrasting verdict examples.

## Output

One verdict, written using [`report-template.md`](./report-template.md), with risk and future cost — not taste — as the basis.
