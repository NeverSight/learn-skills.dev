---
name: draft-issue
description: Research and draft a high quality GitHub issue before creating it.
---

# Draft Issue

Use this skill to research the codebase and draft a high quality GitHub issue.

## Rules

- Require an issue topic argument. If missing, ask for it.
- Research first. Do not draft the issue until you can summarize the current state.
- User approval is required before running `gh issue create`.

## Workflow

1. **Understand the request**
   - Restate the request in your own words.

2. **Research the codebase**
   - Use file search and reads to locate relevant areas.
   - Identify existing models, controllers, services, migrations, or configs involved.

3. **Summarize findings**
   - Provide a short summary of what exists today and where.

4. **Draft the issue**
   - Use the template below.

5. **Get approval**
   - Ask the user to approve the issue content.

6. **Create the issue**
   - Use `gh issue create` with the approved content and labels.

## Issue Template

```markdown
## Context
[Brief background - why is this needed?]

## Current State
[What exists now? Reference files, data, or behavior.]

## Requirements
- Requirement 1
- Requirement 2

## Tasks
- [ ] Task 1
- [ ] Task 2
- [ ] Verification/testing step

## Technical Notes
[Implementation hints, affected areas, gotchas]
```

## Labels

Use GitHub labels like `enhancement`, `bug`, `task`, `documentation`.
