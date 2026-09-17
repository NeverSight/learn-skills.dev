---
name: subagent-driven-development
description: Use when an approved implementation benefits from permitted delegation of substantial, well-bounded tasks.
---

# Coordinate Bounded Implementation

Use `applying-development-principles`. Delegation is an execution choice, not a
mandatory stage after planning. Keep work inline when that is simpler or when
agents are unavailable.

Give each implementer the relevant requirements, dependencies, existing patterns,
owned files, acceptance checks, and explicit limits on writes and commits. Use
`implementer-prompt.md` as a prompt aid, not a required report-file format.
Do not require a fresh agent per tiny step or copy the entire conversation into
every brief.

Coordinate shared state as described in `dispatching-parallel-agents`. The
controller owns integration and delivery. Children do not delegate recursively
unless the controller explicitly assigns that responsibility.

Inspect each returned diff and test evidence. Use independent review at meaningful
risk boundaries or when policy requires it, not a fixed number of review rounds
per task. `task-reviewer-prompt.md` and `re-review-prompt.md` support scoped review.
Reuse an implementer's context for fixes when the host permits it.

Resolve substantive findings and verify the integrated result. Stop and surface
missing authority or a consequential unresolved decision, not every routine
implementation detail. Follow the user's agreed delivery path.

The existing `scripts/task-brief`, `scripts/review-package`, and
`scripts/sdd-workspace` helpers remain available for larger handoffs. They are
optional; inspect their usage before relying on their plan format or output.
