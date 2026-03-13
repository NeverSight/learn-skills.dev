---
name: workflow-hotfix
version: 1.0.0
description: '[Workflow] Trigger Hotfix workflow — production emergency P0/P1 urgent fix with minimal ceremony.'
---

Activate the `hotfix` workflow. Run `/workflow-start hotfix` with the user's prompt as context.

**Steps:** /scout → /plan → /plan-review → /fix → /prove-fix → /tdd-spec → /tdd-spec-review → /test-specs-docs → /test → /review-changes → /sre-review → /watzup → /workflow-end
