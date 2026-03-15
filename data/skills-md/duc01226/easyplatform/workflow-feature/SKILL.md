---
name: workflow-feature
version: 1.0.0
description: '[Workflow] Trigger Feature Implementation workflow — implement a well-defined feature with investigation, planning, implementation, and review.'
---

> **[IMPORTANT]** This skill activates a full workflow. You MUST create todo tasks for ALL steps and execute them in sequence. Do NOT skip any step.

Activate the `feature` workflow. Run `/workflow-start feature` with the user's prompt as context.

**Steps:** /scout → /feature-investigation → /plan → /plan-review → /plan-validate → /why-review → /tdd-spec → /tdd-spec-review → /plan → /plan-review → /cook → /tdd-spec → /tdd-spec-review → /test-specs-docs → /code-simplifier → /review-changes → /code-review → /sre-review → /security → /performance → /changelog → /test → /docs-update → /watzup → /workflow-end

## Conditional UI Planning

When a feature involves UI changes (detected during `/scout` or `/feature-investigation`):

- If image/wireframe/Figma URL is provided → route to `/wireframe-to-spec` or `/figma-design` before `/plan`
- If `/plan` detects frontend phases → ensure `ui-wireframe-protocol.md` sections are included in plan phases
- This is advisory — NOT a mandatory workflow step change. The existing workflow sequence remains unchanged.
