---
name: commit
description: >-
  Stage and commit changes with a well-crafted commit message.
  TRIGGER when: user asks to commit, stage, or save changes to git.
  Examples: "commit this", "commit the changes", "stage and commit".
  DO NOT TRIGGER when: user asks to push, create a PR, or amend a previous commit.
allowed-tools: Bash, Read, Glob, Grep
---

Create a git commit for the current changes.

## Steps

1. Run `git status` and `git diff` (staged and unstaged) to understand all changes
2. Run `git log --oneline -5` to see recent commit style
3. Extract the issue number from the current branch name (e.g. `feature/42-add-export` → `#42`)
4. Analyze the changes and draft a concise commit message:
   - Start with the issue number if available: `#42 Add export endpoint`
   - Use imperative mood ("Add feature" not "Added feature")
   - First line under 70 characters, summarizing the **why**
   - Add a blank line and body paragraph if the change needs explanation
5. Stage the relevant files — prefer `git add <file>...` over `git add -A`
   - Do NOT stage files that look like secrets (`.env`, credentials, tokens)
   - If unsure whether a file should be included, ask
6. Commit with the message
7. Show the resulting `git log --oneline -1` to confirm

## Rules

- Do NOT push — only commit locally
- Do NOT amend previous commits unless explicitly asked
- If there are no changes to commit, tell the user
