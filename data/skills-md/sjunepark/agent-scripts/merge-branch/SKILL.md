---
name: merge-branch
description: "Integrate Git branches deliberately: plan or dry-run merges, transplant work, resolve conflicts, or audit completed or in-progress merges."
---

# Merge Branch

Integrate branch intent, not just patches. Prefer Git's merge machinery as a draft, then edit, refactor, audit, validate, and report the deliberate result.

Use clear branch terms throughout the task: the current `HEAD` branch is the destination branch, and `<source>` is the branch being integrated into it. If the user says "target branch" ambiguously, confirm whether they mean the source branch to merge or the destination branch to receive the work.

## Choose One Mode

- **Dry plan:** When the user asks to analyze or plan without changing repository state, read and follow [modes/dry-plan.md](modes/dry-plan.md). A plan-only request finishes with the plan and any unresolved decisions.
- **Audit:** When the user asks to review a completed or in-progress merge result, read and follow [modes/audit.md](modes/audit.md). Do not start or redo a merge unless separately authorized.
- **Integrate:** When the user asks to perform a merge, transplant branch work, or resolve conflicts, read and follow [modes/integrate.md](modes/integrate.md) through the authorized committed or uncommitted endpoint.

If the request combines assessment and integration, complete the read-only mode first, then perform the already authorized integration. Ask only for consequential decisions or authority still missing from the request and inspected evidence.

## Shared Guardrail

Do not move, force-update, or delete the source branch automatically. Convergence means the source tip is reachable from destination `HEAD`; aligning branch refs requires explicit approval.
