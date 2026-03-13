---
name: jira
description: >
  Use acli to interact with Atlassian Jira from the command line. Use when the
  user wants to: create, view, edit, search, or delete Jira issues/work items,
  transition issue status (e.g. move to "In Progress" or "Done"), add or list
  comments, assign issues, search with JQL, manage sprints or boards, bulk
  create issues from CSV/JSON, manage projects, manage filters, or authenticate
  with a Jira instance.
---

# Jira Skill

Use `acli` to interact with Atlassian Jira from the command line.

## Tool Constraint

**Only use `acli` for all Jira operations.** Do not attempt alternative methods such as `curl`, REST API calls, Python scripts, or any other tool — even if an `acli` command fails or a flag seems unsupported. If something can't be done with `acli`, tell the user clearly rather than inventing a workaround.

## Prerequisites

Verify `acli` is installed:

```bash
which acli
```

If not found, tell the user:
> `acli` is not installed. Please install it: https://developer.atlassian.com/cloud/acli/guides/install-acli/

If a command fails with an authentication error, run `acli jira auth status` to check the current session. For auth setup, see [references/JIRA_AUTH.md](references/JIRA_AUTH.md).

## Rich Formatting (ADF)

To render headings, tables, lists, or code blocks in comments or descriptions, you must use Atlassian Document Format (ADF). See [references/JIRA_ADF_FORMATTING.md](references/JIRA_ADF_FORMATTING.md) for patterns and a Ruby builder.

## Jira Subcommand Reference

- [jira auth](references/JIRA_AUTH.md) — login, logout, status, switch
- [jira board](references/JIRA_BOARD.md) — list-sprints, search
- [jira dashboard](references/JIRA_DASHBOARD.md) — search
- [jira field](references/JIRA_FIELD.md) — cancel-delete, create, delete
- [jira filter](references/JIRA_FILTER.md) — add-favourite, change-owner, list, search
- [jira project](references/JIRA_PROJECT.md) — archive, create, delete, list, restore, update, view
- [jira sprint](references/JIRA_SPRINT.md) — list-workitems
- [jira workitem](references/JIRA_WORKITEM.md) — archive, assign, attachment, clone, comment, create, create-bulk, delete, edit, link, search, transition, unarchive, view, watcher
