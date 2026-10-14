---
name: commit-message
description: Write an appropriate commit message for the current changes
---

# commit-message

Look at the changes and write a short commit message.

## When to use

Use this when I ask for a commit message tailored to what we have been working on.

## Instructions

1. Inspect the branch name with `git branch --show-current` for clues on the overall purpose of the changes.
2. Inspect the changes in the work tree with `git diff` and/or `git diff --staged`.
3. Look at the entire commit message bodies of my most recent 30 commits using this command: `git log --author="$(git config user.name)" --no-merges --max-count=30`.
4. Summarize the changes into a commit message using my tone and style. Use the title line only and omit the commit body unless it is truly necessary.
