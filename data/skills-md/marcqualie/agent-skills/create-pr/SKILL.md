---
name: create-pr
description: Create a Pull Request using gh CLI
license: MIT
disable-model-invocation: true
allowed-tools: Bash(gh pr create:*) Bash(gh pr open:*) Bash(git add:*) Bash(git commit:*) Bash(git push:*)
---
Git commit a summary of work on this branch if not already committed.
Create a Draft GitHub Pull Request assigned to @me using `gh pr create --draft --assignee @me`.
Set the description as a summary of the changes on this branch.
Show the link to the PR after creation.
Open the PR in the browser using `gh pr open`.
