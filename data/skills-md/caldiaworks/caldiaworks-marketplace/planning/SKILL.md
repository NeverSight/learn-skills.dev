---
name: planning
version: 0.3.0
description: "Plan work by analyzing GitHub Issues, identifying dependencies, proposing execution order, and defining work units that map to feature branches. Outputs a persistent plan document. Use when: plan work, planning, prioritize issues, organize issues, create a plan, work breakdown, define work units, what should I work on first, /planning."
---

# Work Planning

Analyze a set of GitHub Issues, identify dependencies, propose an execution order, and define work units. Output a persistent plan document that survives context loss.

Works in any project with GitHub Issues.

## Workflow

### Step 1: Analyze Issues

1. Accept a parent issue number from the user (or a list of issue numbers).
2. Read the issue hierarchy using `gh sub-issue list <number>` recursively.
3. For each issue, read the title, labels, body, and parent-child relationships.
4. Display a summary of all issues to the user:
   - Issue number and title
   - Labels
   - Parent-child hierarchy (indented tree)

If reading issues from GitHub fails, display the error message and stop.
If the specified parent issue has no sub-issues, inform the user there are no issues to plan.

### Step 2: Identify Dependencies and Determine Order

1. Analyze dependencies between issues based on:
   - Explicit references in issue bodies (e.g., "depends on #X", "blocked by #X")
   - Hierarchy: parent issues depend on child issues being resolved
   - Content: issues that produce artifacts needed by other issues
2. Determine an execution order based on dependencies and priorities.

When determining order, consider practical benefits: foundational tools first (e.g., a commit skill before other skills, so it can be used during their development).

### Step 3: Define Work Units

Group related issues into work units. Each work unit:
- Corresponds to a single feature branch
- Contains issues that are closely related and make sense to implement together
- Has a clear, concise description

A work unit may contain a single issue or multiple related issues.

### Step 4: Output Plan Document

Generate a Markdown plan document and save it to `.docs/plans/`.

The document contains:

```markdown
# Plan: {Title}

- Date: {YYYY-MM-DD}
- Parent Issue: #{number}
- Requirements Document: {REQ-DOC-ID, if applicable}

## Dependencies

| REQ/Issue | Description | Depends On |
|-----------|-------------|------------|
| #{number} | {title} | {dependencies} |

## Execution Order

| Order | Work Unit | Issue(s) | Branch | Status |
|-------|-----------|----------|--------|--------|
| 1 | {description} | #{number} | TBD | Pending |

## Rationale

- **Order 1 ({description})**: {why this order}

## Next Action

Work Unit 1: {description} (#{number}).
```

After the plan is finalized, display the first work unit and its associated issues as the next action.

## Before Finishing

After generating the plan document, verify it stands on its own:

- **Survives context loss?** If the conversation is lost and only the plan file remains, can someone resume work from it? Every work unit should reference concrete issue numbers, not just descriptions.
- **Actionable?** Does each work unit have enough detail to create a branch and start working without re-reading the full issue thread?

## Constraints

- Do not modify issues (no labels, assignees, or status changes) -- planning is read-only.
- Do not create branches or start implementation -- planning produces a document only.
- Always persist the plan to a file so it survives context loss.
