---
name: create-issue-commit
description: Create GitHub issue for uncommited changes and commit.
disable-model-invocation: true
metadata:
  type: command
  invocation: human-only
  applies-to: [issues, commits, git, github]
---

# create-issue-commit

> **human-only.** Start this only when a human asks for it by name. If you arrived here from another skill, stop and get explicit confirmation before running any step.

Create appropriate GitHub issue using `gh` for uncommited changes. Commit current changes as a WIP commit.

Then commit the changes. You MUST invoke the `draft-commit-message` skill to draft the commit message.

