---
name: workflow-bugfix
version: 1.0.0
description: '[Workflow] Trigger Bug Fix workflow — systematic debugging with root cause investigation, fix, and verification.'
---

> **[IMPORTANT]** This skill activates a full workflow. You MUST create todo tasks for ALL steps and execute them in sequence. Do NOT skip any step.

Activate the `bugfix` workflow. Run `/workflow-start bugfix` with the user's prompt as context.

**Steps:** /scout → /feature-investigation → /debug → /plan → /plan-review → /plan-validate → /why-review → /fix → /prove-fix → /tdd-spec → /tdd-spec-review → /test-specs-docs → /code-simplifier → /review-changes → /code-review → /changelog → /test → /docs-update → /watzup → /workflow-end
