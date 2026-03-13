---
name: commit-changes
description: Summarise then commit the changes in the current session.
license: MIT
disable-model-invocation: true
allowed-tools: Bash(git add:*) Bash(git commit:*) Bash(git diff:*)
---
Commit a detailed summary of the changes in the current session.
If there are unstaged changes that are not part of the session then prompt the user to confirm if they should be included in the commit or not.
