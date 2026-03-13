---
name: plan-jira-ticket
description: >
  Fetches a Jira ticket and starts implementation with a branch and plan.
  Use when (1) starting work on a Jira ticket,
  (2) creating a feature branch from a Jira issue,
  (3) beginning implementation of a story or task,
  (4) picking up a ticket from the backlog,
  or (5) user provides a Jira ticket ID to work on.
argument-hint: "TICKET-ID (e.g. PROJ-123)"
disable-model-invocation: true
compatibility: Requires acli (Atlassian CLI) and git
---

# Plan Jira Ticket

Ticket ID: $ARGUMENTS

Ticket details:
`acli jira workitem view $ARGUMENTS`

## Workflow

1. **Parse ticket** — Extract summary, description, acceptance criteria, linked issues, and attachments from the ticket details above.
2. **Create or switch to branch** — Follow Branch Naming. Check for an existing branch matching this ticket before creating a new one.
3. **Transition ticket** — Run `acli jira workitem update $ARGUMENTS --status "In Progress"`.
4. **Enter plan mode** — Call EnterPlanMode.
5. **Create implementation plan** — Write a plan covering:
   - Ticket ID and summary as the plan title
   - Acceptance criteria from the ticket (verbatim when available)
   - Technical approach with specific files to create or modify
   - Testing strategy
   - Out-of-scope items (what NOT to change)

## Branch Naming

Format: `{TICKET-ID}-{slugified-summary}`

| Rule | Detail |
|------|--------|
| Preserve ticket ID case | `PROJ-123` stays `PROJ-123` |
| Slugify summary | Lowercase, replace spaces and special characters with hyphens, collapse consecutive hyphens |
| Truncate slug | 50 characters max, break at word boundary |
| Remove trailing hyphens | `add-user-login-` becomes `add-user-login` |

Result: `PROJ-123-add-user-login-page`

### Branch Check

1. List local branches: `git branch --list '*{TICKET-ID}*'`
2. List remote branches: `git branch -r --list '*{TICKET-ID}*'`
3. Match found → `git checkout {branch}`. Pull latest if remote tracking branch exists.
4. No match → `git checkout -b {new-branch-name}`.

## Plan Requirements

**Include:**
- Ticket ID and summary as the plan title
- Acceptance criteria extracted from the ticket (verbatim when present)
- Files to create or modify with rationale
- Testing approach
- Dependencies or blockers from the ticket

**Exclude:**
- Work outside the ticket scope
- Speculative features not in the ticket
- Refactoring unrelated to ticket objectives

## Error Handling

| Error | Action |
|-------|--------|
| `acli` not found | Stop. Instruct user to install Atlassian CLI. |
| Ticket ID not found | Stop. Report invalid ticket ID. |
| Branch creation fails | Check for name conflicts. Report error. |
| Status transition fails | Log warning. Continue — ticket may already be In Progress or use a different workflow. |
| No `$ARGUMENTS` provided | Stop. Prompt user for a ticket ID. |
