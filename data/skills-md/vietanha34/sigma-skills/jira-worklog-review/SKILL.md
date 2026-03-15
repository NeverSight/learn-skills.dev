---
name: jira-worklog-review
description: Review daily Jira worklogs, calculate logged time vs 8h target, suggest existing issues, or create new TL issues and log work when needed.
---

# Jira Worklog Review

Use this skill to review Jira worklog for a target day, compute total logged time, and close the 8-hour gap with either existing issues or a create-new-issue workflow.

## Trigger Phrases
- "Review my worklog"
- "Check my jira hours"
- "Did I log enough time today?"
- "Review worklog for [date]"
- "Suggest what to log if I am under 8h"
- "Create a new Jira task and log work"

## Tools
This skill relies on Atlassian Jira MCP (Jira toolset):
- `mcp_mcp-atlassian_jira_search`
- `mcp_mcp-atlassian_jira_get_worklog`
- `mcp_mcp-atlassian_jira_get_user_profile` (optional)
- `mcp_mcp-atlassian_jira_add_worklog`
- `jira_search_fields`
- `jira_get_field_options`
- Jira create issue tool in the same MCP set (for creating issues in `TL`)

## Preconditions
- User can access Jira and has permission to read issues/worklogs.
- User can create issues in project `TL` and log work.
- Field `(BU) Project` exists as custom field `customfield_10232`.

## Guardrails
- Default to read/analyze first; only create issue or add worklog after explicit confirmation from user input.
- Keep date explicit (`YYYY-MM-DD`) and compute total by `timeSpentSeconds`.
- If under 8h, keep iterating suggestions/actions until total reaches or exceeds 8h, or user stops.
- If a required Jira tool call fails, show the exact failed step and ask for the minimum missing info/permission.

## Workflow Router
1. Resolve inputs:
   - `date` (default: today)
   - `user` (default: `currentUser()`, resolve accountId when filtering worklog entries)
2. Load `references/workflows/01-review-daily-worklog.md`.
3. If total `< 8h`, load `references/workflows/02-suggestions-under-8h.md`.
4. If user chooses create-new flow, load `references/workflows/03-create-issue-and-log-work.md`.
5. Repeat suggestion loop until total `>= 8h` or user stops.
6. Render final response using `references/templates/worklog-review-response-template.md`.

## Minimal Response Contract
Always return:
- `Date`: target review date.
- `Total logged`: hours and minutes.
- `Gap to 8h`: remaining duration (or `0`).
- `Actions taken`: issue keys logged/created and durations.
- `Next options`: continue suggestions loop or stop.

## Failure Handling
- `(BU) Project` field not found or mismatched metadata: stop create-new flow, show returned fields, and ask user/admin to confirm field mapping.
- No available `(BU) Project` options: stop create flow and request Jira configuration check.
- Create issue or add worklog failed: report exact tool step and error, then offer existing-issue logging as fallback.
