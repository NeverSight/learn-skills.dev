---
name: resolving-merge-conflicts
description: "Resolve an in-progress Git merge or rebase conflict."
---

Use `/agent-watchdog` for another agent's branch/claim; `/plan-arbiter` when viable semantic choices remain.

1. Inspect merge/rebase state, history, conflicts.
2. Find primary intent sources: commits, PRs, issues/tickets, surrounding code.
3. Resolve hunks preserving both intents. If incompatible, choose the merge goal and note trade-off. If operation is wrong or intent remains ambiguous, show exact conflict and ask whether to abort; never abort unasked.
4. Run project checks, typically typecheck, tests, format; fix merge breakage.
5. Stage and finish merge, or continue rebase through all commits.
