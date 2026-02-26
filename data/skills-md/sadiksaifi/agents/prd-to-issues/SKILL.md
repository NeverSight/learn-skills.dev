---
name: prd-to-issues
description: >-
  Breaks a PRD into independently-grabbable GitHub issues using vertical
  slices (tracer bullets). Use when decomposing a PRD into implementation
  work, creating tracer-bullet issues, or when the user says "break down
  PRD," "create issues from PRD," or "/prd-to-issues."
compatibility: Requires gh CLI (authenticated) and git
---

# PRD to Issues

Break a PRD into independently-grabbable GitHub issues using vertical slices (tracer bullets).

## Process

### 1. Locate the PRD

Ask the user for the PRD GitHub issue number (or URL). Fetch it with `gh issue view <number>`. Read and internalize the full PRD content (with all comments).

### 2. Explore the codebase

Read the key modules and integration layers referenced in the PRD. Identify:

- The distinct integration layers the feature touches (e.g. DB/schema, API/backend, UI, tests, config)
- Existing patterns for similar features
- Natural seams where work can be parallelized

### 3. Draft vertical slices

Break the PRD into **tracer bullet** issues. Each issue is a thin vertical slice that cuts through ALL integration layers end-to-end, NOT a horizontal slice of one layer.

<vertical-slice-rules>
- Each slice delivers a narrow but COMPLETE path through every layer (schema, API, UI, tests)
- A completed slice is demoable or verifiable on its own
- Prefer many thin slices over few thick ones
- The first slice should be the simplest possible end-to-end path (the "hello world" tracer bullet)
- Later slices add breadth: edge cases, additional user stories, polish
</vertical-slice-rules>

### 4. Quiz the user

Present the proposed breakdown as a numbered list. For each slice, show:

- **Title**: short descriptive name
- **Layers touched**: which integration layers this slice cuts through
- **Blocked by**: which other slices (if any) must complete first
- **User stories covered**: which user stories from the PRD this addresses

Ask the user:

- Does the granularity feel right? (too coarse / too fine)
- Are the dependency relationships correct?
- Should any slices be merged or split further?
- Is the ordering right for the first tracer bullet?
- Are there any slices missing?

Iterate until the user approves the breakdown.

### 5. Create the GitHub issues

For each approved slice, create a GitHub issue using `gh issue create`. Use the [issue body template](references/issue-template.md).

Create issues in dependency order (blockers first) so you can reference real issue numbers in the "Blocked by" field.

After creating all issues, print a summary table:

```
| # | Title | Blocked by | Status |
|---|-------|-----------|--------|
| 42 | Basic widget creation | None | Ready |
| 43 | Widget listing | #42 | Blocked |
```

Do NOT close or modify the parent PRD issue.
