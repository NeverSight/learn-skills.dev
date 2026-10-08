---
name: autopilot
description: "Plan, implement, validate, push, and create a PR for the accompanying prompt, then return to main. Use only when explicitly invoked as `autopilot` or `$autopilot`."
---

# Autopilot

Manual invocation only. Treat the accompanying prompt as the task. Invocation authorizes implementation, task-scoped commits, pushing, PR creation, and returning to `main`; no separate approval needed.

## Prepare

Read repository instructions. Inspect Git status, branch, upstream, and remotes; preserve unrelated work. Resolve detached HEAD or missing context first. Check that `wt` is available on `PATH` before starting the task. If missing, ask the user to install the Worktrunk CLI (`wt`) and make it available on `PATH`; resume once available. If on `main`, identify its upstream remote (use `origin` if no upstream is configured), run `git fetch <remote>`, then run `wt switch --create codex/<task> --base <remote>/main` to create a descriptive branch in a new worktree from the fetched remote `main`, even when local `main` is stale, and switch to its directory before starting the task. Otherwise continue in the current branch and worktree. Use Worktrunk (`wt`), never Git commands, to create or switch worktrees. Confirm the resulting directory and branch; run subsequent commands from that worktree directory explicitly. If fetching or `wt` fails, report the blocker; do not continue from a stale base or fall back to Git worktree commands.

## Plan — condensed plan-mode

- Keep this phase read-only: inspect code, callers, configs, schemas, tests, and tooling; no implementation or plan-file writes yet.
- Resolve discoverable facts locally. Ask about unresolved intent, preferences, scope, behavior, interfaces, or acceptance criteria; explain meaningful alternatives and tradeoffs. Do not invent user decisions.
- Present a decision-complete plan: title, summary, surgical changes and affected files, verification, user decisions, relevant risks and tradeoffs, and independent work. End with unresolved questions or `None`.
- Once meaningful ambiguity is resolved, proceed automatically. If saving a plan, write it only after finalizing, immediately before implementation.

## Implement — condensed execute-plan

- Follow the finalized plan and repository conventions; keep edits minimal and task-scoped. Coordinate independent tasks through background agents when supported.
- Respect tool permissions; never bypass unavailable or denied capabilities. Report blockers and ask for direction.
- If execution requires a changed approach, stop dependent work, explain alternatives, and resolve the decision with the user. Update the plan and any saved copy with approved changes, reasons, tradeoffs, and risks.
- Run relevant local tests and required lint, type, and build checks. Add meaningful behavior tests where warranted. Fix task-related failures; report unresolved failures before publishing. Review the final diff.
- Summarize changed files, decisions, tradeoffs, commands run, and actual validation results.

## Push and PR — condensed gh-create-pr

- Verify Git, `gh`, authentication, repository, push destination, head, base, and parent branch. Check for an existing open PR, including fork ownership; reuse the task PR instead of duplicating it.
- Stage only task changes; commit concisely. Fetch relevant refs and inspect the full committed diff against the PR base. Stop if there are no changes to propose.
- Check ancestry against the remote counterpart, parent, and base. Rebase stale branches in that order; never add merge commits. Record starting HEAD and fetched remote head. Ask before handling an existing rebase or obstructing local changes; never discard or stash them automatically. On conflicts, abort the attempted rebase, report files, and ask before resolving.
- After rebasing, review the final diff and rerun affected checks. Write a brief `<type>: <description>` title and bullets connecting concrete changes to why needed and what they fix; include actual validation results.
- Push explicitly with upstream tracking. If published history was rewritten, disclose it and obtain authorization; use an explicit lease against the fetched remote head, never plain force.
- Recheck for an existing PR. Create non-interactively with explicit repository, base, head, title, and `--body-file`; default to `--draft` unless ready mode was requested. Update an existing task PR instead. Attach the PR when supported.

## Return to main

After PR creation or update succeeds, run `wt switch main` to return to the `main` branch directory. Confirm the resulting directory and branch. Preserve local changes; never discard or stash unrelated work to force the switch. Report PR URL, validation, final branch, and any blocker.
