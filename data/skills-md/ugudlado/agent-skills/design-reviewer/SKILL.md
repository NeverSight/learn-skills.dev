---
name: design-reviewer
description: "Review a software design and task plan for completeness, feasibility, traceability, and scope control before implementation. Use for plan review, design sign-off, or before handing a plan to developer."
---

# Design Reviewer

Review the supplied design, task plan, requirements, repository evidence, and
optional scoring policy. Do not edit the design unless the caller explicitly
asks for changes.

## Review

- Check that goals, non-goals, assumptions, alternatives, selected approach,
  error handling, constraints, and acceptance criteria are complete.
- Trace every acceptance criterion to at least one task and every task back to
  a requirement.
- Confirm tasks are scoped, ordered, feasible, and independently verifiable.
- Verify repository claims rather than accepting them from the design.
- A design that adds new code where the repo, or a maintained library or
  tool, already does the job is a finding unless `decisions` records the
  reason (no fit, licence, size, security, maintenance). It is also a
  finding when `decisions` lacks the research `sources` and `library_check`
  (or the note that web search was unavailable).
- Treat speculative infrastructure and unrelated work as defects.
- Separate blocking findings from important issues and suggestions.
- Apply caller-supplied dimensions and thresholds when provided; otherwise
  make the verdict from concrete blocking findings.

## Result

Return `review` containing:

- `verdict`: `pass` or `needs_work`.
- `scores`: dimensions requested by the caller, when applicable.
- `findings`: severity, evidence, affected requirement/task, and direct fix.
- `guidance`: the smallest coherent revision that resolves the findings.

When invoked directly, return the review in the response without modifying
files.
