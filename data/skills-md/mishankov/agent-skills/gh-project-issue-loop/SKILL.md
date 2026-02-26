---
name: gh-project-issue-loop
description: Continuously process available GitHub Project items by preparing project context once and then implementing linked issues in a loop via the gh-issue-to-pr skill. Use when asked to clear backlog from a GitHub Project board, batch-deliver project issues, or repeatedly pick and implement open project issues with gh CLI.
---

# GitHub Project Issue Loop

Prepare once for a GitHub Project, then repeatedly pick an available project issue and complete it using `$gh-issue-to-pr`.

## Required Inputs

- `project_owner` (org/user login or `@me`)
- `project_number`
- `max_issues` (default `1` if not provided)
- Optional filters: `labels`, `exclude_labels`, `status`, `assignee_policy`, `issue_query`

## Algorithm

1. Get ready to do issues from project.
2. In a loop, do issues using `$gh-issue-to-pr`.

## Step 1: Get Ready Once

Run:

```bash
gh auth status
gh auth refresh -s project
gh project view <project_number> --owner <project_owner> --format json
```

Load project items:

```bash
gh project item-list <project_number> \
  --owner <project_owner> \
  --limit 200 \
  --format json
```

Define `available issue` as:
- Project item linked to an Issue (not draft issue, not PR-only item)
- Linked issue is open
- Not assigned to someone else (unless explicitly requested)
- Not blocked by labels like `blocked`, `waiting`, `wontfix`
- Matching requested labels/status/query constraints

## Step 2: Loop Through Issues

For each issue until `max_issues` is reached or queue is empty:

1. Pick next available project item (prioritize explicit project priority, otherwise oldest updated).
2. Resolve linked issue metadata from item content:
   - Extract `owner/repo` and `issue_number` from the linked issue URL.
3. Attempt to claim issue:
   - `gh issue edit <number> --repo <owner/repo> --add-assignee @me` (if allowed)
   - Optional claim comment to reduce duplicate work.
4. Invoke `$gh-issue-to-pr` with resolved `owner/repo` and `issue_number`.
5. Record result:
   - success: PR URL + branch
   - failure: reason and whether issue was skipped or blocked
6. Continue to next available project issue.

## Invocation Contract for `$gh-issue-to-pr`

Pass:
- Resolved `owner/repo` from project item
- Resolved `issue_number` from project item
- Workspace parent directory for clone/fork operations

Expect back:
- Fork URL
- Branch name
- Commit SHA(s)
- PR URL
- Checks/tests summary

## Stop Conditions

Stop loop when any is true:
- `max_issues` completed
- No available project issues remain
- Authentication/permission failure prevents further progress
- User-defined budget/time limit reached

## Failure Handling

- Project item is not a linked issue: skip and continue.
- Linked issue cannot be claimed: continue if implementation is still permitted; otherwise skip and log.
- Linked issue is ambiguous: mark as blocked and skip unless clarification is provided.
- `$gh-issue-to-pr` fails: capture error and continue with next issue unless failure is systemic.

## Output Contract

Return a batch summary:
- Project (`owner`, `number`, `url`)
- Total scanned
- Total attempted
- Total completed
- Total skipped/failed
- For each attempted item: `issue_url`, status, PR URL (if created), short note
