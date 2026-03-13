---
name: workflow-package-upgrade
version: 1.0.0
description: '[Workflow] Trigger Package Upgrade workflow — upgrade dependencies, npm update, NuGet upgrade with testing.'
---

Activate the `package-upgrade` workflow. Run `/workflow-start package-upgrade` with the user's prompt as context.

**Steps:** /scout → /feature-investigation → /plan → /plan-review → /plan-validate → /code → /test → /review-changes → /watzup → /workflow-end
