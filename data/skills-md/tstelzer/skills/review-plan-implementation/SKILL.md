---
name: review-plan-implementation
description: Review code changes against a plan using the plan location and implementing git commit(s).
---

# Review Implementation

## Inputs

- Plan location (file path)
- Git commit(s) that implemented the plan (hashes or ranges), or assume HEAD~

## Workflow

1. Open and read the plan file; note promised behavior, tasks, files, and verify steps.
2. Inspect the specified commit(s) and identify the files and changes related to the plan.
3. Review the implementation against the plan, prioritizing the following list,
   unless the user says otherwise
    - performance
    - security
    - extensibility
    - testability
    - comprehensibility
4. Call out mismatches between plan and implementation, missing steps, or unverified tasks.
5. Provide actionable fixes and any tests or checks to run.

## Output

- Findings ordered by severity with file/line references
- Open questions or assumptions
- Brief change summary

## Examples

- "Review the implementation of this plan: plans/2026-02-19-1200_cache.md. Commits: 1a2b3c4, 9d8e7f6."
