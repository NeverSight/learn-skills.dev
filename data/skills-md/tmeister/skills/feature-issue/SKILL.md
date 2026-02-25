---
name: feature-issue
description: Implement a feature from a GitHub issue with a structured, review-first workflow.
---

# Feature Issue

Use this skill to implement a feature from a GitHub issue with clear planning, validation, and a review-first flow.

## Workflow

1. **Issue analysis**
   - Require an issue number argument. If missing, ask for it.
   - `gh issue view <issue-number>`
   - Summarize requirements and acceptance criteria before coding.
   - If anything is unclear, interview the user for clarification before continuing.

2. **Environment setup**
   - Ensure the default branch is up to date.
   - Create a feature branch named `feature/<short-title>-<issue-number>`.

3. **Planning**
   - Break work into small, verifiable steps.
   - Identify affected files and data changes.
   - For larger or unclear scopes, suggest running `/prd-discovery` and `/prd-to-json` to create a small tasks document before implementation.

4. **Implementation**
   - Build incrementally.
   - Follow project conventions and add tests where appropriate.

5. **Validation**
   - Run relevant checks and tests.
   - Fix diagnostics and lint issues before proceeding.

6. **Review-first checkpoint**
   - Summarize the changes and request a user review.
   - Do not start a commit. The user initiates the commit process when ready.
