---
name: jira-cli
description: Interact with Jira from the terminal using ankitpokhrel/jira-cli (the `jira` command). Covers issue CRUD, search, sprint management, status transitions, and linking. Use when the user mentions `jira` CLI, wants to create or view Jira issues, list sprints, move tickets, or manage Jira from the terminal without the Atlassian CLI (acli).
---

# jira-cli (ankitpokhrel/jira-cli)

## Auth

```bash
jira init          # Interactive setup — Cloud or Server, basic auth / PAT / mTLS
jira me            # Verify current user
```

## Issues: View & Search

```bash
jira issue view ISSUE-1
jira issue view ISSUE-1 --comments 5

jira issue list                              # Recent issues
jira issue list -a$(jira me)                # Assigned to me
jira issue list -s"In Progress"             # By status
jira issue list -yHigh -lbackend            # Priority + label
jira issue list --created -7d              # Last 7 days
jira issue list -q "summary ~ login"       # Raw JQL
jira issue list --raw                      # JSON output
```

## Issues: Create & Edit

```bash
# Create
jira issue create                                         # Interactive
jira issue create -tBug -s"Title" -yHigh -lbug --no-input
jira issue create -tStory -PEPIC-42                      # Under an epic

# Edit
jira issue edit ISSUE-1                                   # Interactive
jira issue edit ISSUE-1 -s"New title" -yHigh --no-input
jira issue edit ISSUE-1 --label -old --label new         # Swap labels

# Delete
jira issue delete ISSUE-1
jira issue delete ISSUE-1 --cascade                      # Include subtasks
```

## Issues: Workflow

```bash
jira issue move ISSUE-1 "In Progress"
jira issue move ISSUE-1 Done --comment "Shipped"
jira issue move ISSUE-1 Done -RFixed -a$(jira me)

jira issue assign ISSUE-1 "Jane Doe"
jira issue assign ISSUE-1 $(jira me)       # Assign to self
jira issue assign ISSUE-1 x               # Unassign

jira issue comment add ISSUE-1 "LGTM"
jira issue link ISSUE-1 ISSUE-2 Blocks
jira issue clone ISSUE-1 -s"Copy of title"
```

## Sprints & Boards

```bash
jira sprint list                           # All sprints (explorer view)
jira sprint list --current                 # Active sprint
jira sprint list --current -a$(jira me)   # My issues in active sprint
jira sprint add SPRINT_ID ISSUE-1 ISSUE-2

jira board list                            # All boards
jira project list                          # All projects
```

## Tips

- `jira open ISSUE-1` — open issue in browser
- `jira issue list --raw | jq '...'` — pipe JSON to jq for scripting
- Use `--no-input` with all required flags to skip interactive prompts in scripts
- JQL via `-q`: `assignee = currentUser() AND sprint in openSprints()`

## Bugs
In codex jira-cli authentication does not work in sandbox terminals
