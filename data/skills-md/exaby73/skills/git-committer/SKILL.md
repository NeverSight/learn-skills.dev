---
name: git-committer
description: Generates conventional one line commit messages from a git diff
---

# Generating a git commit message

## Instructions

1. Run `git status --short`, `git diff`, and `git diff --staged` to gather current changes, including untracked files
1. If there are staged files, generate commit message suggestions using only staged changes (including staged newly added files)
1. If there are no staged files, include unstaged diff changes and untracked files in the suggestion context
1. For untracked files, inspect file names and content (for example with `git status --short` and `cat`/`sed`) so they are represented in the suggested message
1. For more context, get the last 5 to 10 commit messages as well
1. Suggest a commit message:
    - The commit message should be a single line
    - The commit message should be a summary of the changes
    - The commit message should follow conventional commit conventions
    - If there too many changes, suggest multiple commit messages with a split of files between each commit message

## Best practices

1. Use present tense
1. After the tag (e.g. `feat:`), the first letter should be capitalized, unless it's a symbol like a function name
