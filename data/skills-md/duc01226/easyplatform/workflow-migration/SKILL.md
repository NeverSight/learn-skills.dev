---
name: workflow-migration
version: 1.0.0
description: '[Workflow] Trigger Database Migration workflow — schema changes, data migrations, EF migrations with review and testing.'
---

Activate the `migration` workflow. Run `/workflow-start migration` with the user's prompt as context.

**Steps:** /scout → /feature-investigation → /plan → /plan-review → /plan-validate → /code → /review-changes → /code-review → /sre-review → /test → /docs-update → /watzup → /workflow-end
