---
name: create-pr-for-branch
description: Create a pull request for the current branch.
disable-model-invocation: true
metadata:
  type: command
  invocation: human-only
  applies-to: [prs, github, github-api]
---

# create-pr-for-branch

> **human-only.** Start this only when a human asks for it by name. If you arrived here from another skill, stop and get explicit confirmation before running any step.

Check if package has `prepublishOnly` script. If so, run first. 

If that passes or you've been instructed to ignore prepublishOnly, create a pull request for the current branch using `gh`.

If the branch is meant to close issues, put `Closes #{issue}` in the PR body — one line per issue.

Provide both URL and markdown link to the PR.


