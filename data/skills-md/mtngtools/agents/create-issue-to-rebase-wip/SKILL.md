---
name: create-issue-to-rebase-wip
description: Create GitHub issue for prior WIP commit, rebase with issue number referenced.
argument-hint: "The issue title, if you want to set it"
disable-model-invocation: true
metadata:
  type: command
  invocation: human-only
  applies-to: [issues, git, rebase, wip]
---

# create-issue-to-rebase-wip

> **human-only.** Start this only when a human asks for it by name. If you arrived here from another skill, stop and get explicit confirmation before running any step.

Read back in prior git commits for the recent "wip" commit. 

Create github issue using 'gh' referencing the summary only of what the commit changed.

Then rebase these wip commits with that issue, but not closing it, as we probably will have additional changes.

You MUST invoke the `draft-commit-message` skill to draft/edit the commit message for the rebase, remembering to include the issue number at the end of the first line and at the bottom of the commit message.