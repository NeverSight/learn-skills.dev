---
name: commit-with-issue
description: Commit using specified issue number.
argument-hint: "The issue number to reference"
metadata:
  type: command
  invocation: skill-callable
  applies-to: [commits, git, issues]
---

# commit-with-issue

Commit the changes. You MUST invoke the `draft-commit-message` skill to draft the commit message, noting the issue using that guidance. 
