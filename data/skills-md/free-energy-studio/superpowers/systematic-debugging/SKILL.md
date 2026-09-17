---
name: systematic-debugging
description: Use when a bug, test failure, or unexpected behavior needs causal investigation before choosing a fix.
---

# Debug from Evidence

Apply `applying-development-principles`. Establish what happened, what should have
happened, and the smallest useful reproduction or trace. Inspect the relevant code
and recent changes. Keep observations separate from hypotheses.

CURE: correct underlying causes, not effects. Establish the supported causal chain
before choosing a permanent repair. An incident mitigation is not proof of cause.

Trace the failure through the affected boundaries until you can explain its cause.
Use existing logs and tests first. Add focused diagnostics only when evidence is
missing. For production, prefer read-only checks and follow the environment's
access and data-safety rules.

Test the likeliest hypothesis with the smallest discriminating check. Change one
relevant variable at a time where practical. After a failed hypothesis, update the
explanation; do not stack speculative patches or diagnose an architecture problem
merely because a fixed number of attempts failed.

When the user requested diagnosis, report the cause, evidence, uncertainty, and
recommended fix. Do not implement without authorization. During an incident, an
authorized mitigation can precede a complete root-cause analysis; clearly distinguish
restoring service from understanding or permanently fixing the bug.

For an authorized fix:

- Correct the responsible boundary, rather than masking the symptom elsewhere.
- Add a focused regression test when the behavior is testable.
- Check related callers when the cause suggests the same defect could affect them.
- Verify the changed path and relevant integration behavior.

Keep the repair proportional. Do not turn one defect into a speculative rewrite.

## Model-behavior failures

Reconstruct the exact model-visible situation: prompts, retrieved context,
filtering and transformations, tools, permissions, lifecycle state, and available
evidence. Identify which condition for successful reasoning was missing or wrong.
Choose the least brittle structural correction using the core skill's SCENE
principle. Cover the reasoning/failure class, not only one recorded conversation.

When tracking the investigation in Linear, read
[the Linear workflow](../applying-development-principles/references/linear.md).

Supporting techniques, when relevant:
`root-cause-tracing.md`, `condition-based-waiting.md`, and `defense-in-depth.md`.
The `find-polluter.sh` helper can isolate order-dependent test failures.
