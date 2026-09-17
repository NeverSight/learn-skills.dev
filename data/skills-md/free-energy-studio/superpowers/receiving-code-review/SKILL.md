---
name: receiving-code-review
description: Use when evaluating code review feedback before deciding what to change.
---

# Evaluate Feedback

Read the finding, inspect the relevant code, and understand the failure or
maintenance cost it identifies. Feedback is a claim to evaluate, not an instruction
to obey mechanically.

Fix demonstrated defects and missed requirements. Ask a focused question when a
finding is unclear. Explain disagreements using contracts, callers, or tests—not
defensiveness, automatic agreement, or performative praise.

For a proposed field, layer, validation, fallback, or abstraction, ask what current
requirement needs it. Review is also an opportunity to remove unnecessary code.
Do not implement speculative safeguards simply because a reviewer suggested them.

Prioritize by actual impact. Keep unrelated improvements out of the patch unless
the user authorizes them. Verify each meaningful correction with relevant checks.
Report what was addressed, what remains, and why; do not mark a finding resolved
until the code or evidence supports that claim.
