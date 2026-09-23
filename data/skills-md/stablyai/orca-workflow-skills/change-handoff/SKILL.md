---
name: change-handoff
description: Prepare a precise handoff for unfinished repository work.
---

# Change handoff

Use this skill when work must continue in another session or with another engineer.

1. Record the branch, clean or dirty status, and the latest relevant commit.
2. Summarize the intended outcome before implementation details.
3. List completed behavior with concrete file or test evidence.
4. List remaining work in dependency order, including the first safe command to run.
5. Call out security, compatibility, migration, and release risks explicitly.
6. Include the exact validation commands already run and their outcomes.

Do not claim a check passed unless its command completed successfully in the current worktree.
