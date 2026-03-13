---
name: workflow-quality-audit
version: 1.0.0
description: '[Workflow] Trigger Quality Audit workflow — audit code quality, review for best practices, find flaws and suggest enhancements.'
---

Activate the `quality-audit` workflow. Run `/workflow-start quality-audit` with the user's prompt as context.

**Steps:** /code-review → /plan → /plan-review → /plan-validate → /code → /tdd-spec → /tdd-spec-review → /review-changes → /test → /watzup → /workflow-end
