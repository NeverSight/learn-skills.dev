---
name: git-jira-branch
description: Switches to the git branch for a Jira ticket. Searches for an existing branch prefixed with the ticket number; if none exists, runs `jiraSwitchToBranch <TICKET>` to create and switch to a new one. Use when the user mentions a Jira ticket number and wants to switch branches, start working on a ticket, check out a ticket branch, or says "switch to TICKET-1234".
---

# git-jira-branch

## Quick start

Given a ticket like `TICKET-1234`:

```bash
# 1. Look for an existing branch
git branch --list "TICKET-1234-*"

# 2a. Branch found — switch to it
git checkout TICKET-1234-my-feature

# 2b. No branch found — delegate to the helper script
jiraSwitchToBranch TICKET-1234
```

## Workflow

1. **Extract the ticket number** from the user's message (e.g. `PROJ-42`, `ABC-1234`).
2. **Search local branches** for a branch whose name starts with `<TICKET>-`:
   ```bash
   git branch --list "<TICKET>-*"
   ```
3. **If exactly one match** → check it out:
   ```bash
   git checkout <matched-branch>
   ```
4. **If multiple matches** → list them and ask the user which one to use.
5. **If no match** → run the helper:
   ```bash
   jiraSwitchToBranch <TICKET>
   ```
   The script handles branch creation and checkout automatically; report its output to the user.

## Notes

- Always search **local** branches first (`git branch --list`), not remote.
- The ticket prefix match is case-sensitive; use the ticket number exactly as provided.
- Do not create branches manually — `jiraSwitchToBranch` is the authoritative tool for that.
- `jiraSwitchToBranch` is not loaded in you environment, so run `sh ~/.config/helpers/switchToJiraBranch.sh`
