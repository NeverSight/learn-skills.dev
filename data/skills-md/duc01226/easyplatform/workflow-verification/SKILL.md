---
name: workflow-verification
version: 1.0.0
description: '[Workflow] Trigger Verification & Validation workflow — verify, validate, and confirm correctness with investigation and testing.'
---

> **[IMPORTANT]** This skill activates a full workflow. You MUST create todo tasks for ALL steps and execute them in sequence. Do NOT skip any step.

Activate the `verification` workflow. Run `/workflow-start verification` with the user's prompt as context.

**Steps:** /scout → /feature-investigation → /test → /plan → /plan-review → /plan-validate → /fix → /prove-fix → /tdd-spec → /tdd-spec-review → /test-specs-docs → /code-simplifier → /review-changes → /code-review → /test → /watzup → /workflow-end
