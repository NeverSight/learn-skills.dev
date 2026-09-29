---
name: finishing-a-development-branch
description: "Use when the user requests merging, opening a PR, preserving, discarding, or cleaning up completed branch work; not as an automatic implementation tail."
---

# Finishing a development branch

## Overview

Verify the branch state and carry out the authorized integration choice. Ask only when the choice is still open. Preserve work until cleanup is explicitly authorized.

## When to Use

- Implementation is complete and the next step is merge, PR, keep, or discard
- A worktree or branch needs explicit cleanup or preservation

## When Not to Use

- Mid-task execution
- Ordinary implementation without a requested integration or cleanup step

## Minimal Workflow

1. Inspect the branch, worktree, dirty state, commits, and relevant checks. Do not present an integration option as ready unless its required checks have passed.
2. Use the integration choice already authorized by the user. If none is settled, present only viable choices: merge, open a PR, keep the branch, or discard it. State what each would change.
3. Complete authorized preparation before asking about a remaining boundary. Carry out the selected action once its required checks pass and authority covers its effects; do not ask the user to repeat a choice. Publishing, discard, and destructive cleanup need existing or explicit authority. A merge or PR request does not by itself authorize deleting the branch or worktree.
4. Preserve the worktree for PR and keep-as-is choices unless its cleanup is separately authorized. Finish when the selected action is complete and the resulting branch and worktree state are verified.

## Reference Routing

- Reuse recorded proof across turns when the tested code and relevant state are unchanged. Run missing checks or repeat affected checks when code, state, or integration requirements change.
- Use `describe-pr` when the next step is writing or updating the PR summary.
- For authorized workspace removal, follow [using-git-worktrees](../using-git-worktrees/SKILL.md#authorized-cleanup).

## Failure modes

- Offering completion choices without verification
- Deleting a worktree needed for an open PR
- Treating discard as a normal cleanup step
