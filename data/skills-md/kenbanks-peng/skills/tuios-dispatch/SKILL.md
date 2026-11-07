---
name: tuios-dispatch
description: Dispatch Aven tasks to pi agents through tuios, or resume an interrupted tuios dispatch run. Use when the user requests agents. 
---

# Dispatch

Use tuios for execution and isolation. Use Aven for durable task context and handoff. The dispatcher owns selection, assignment, acceptance, integration, and task status. Workers own implementation, checks, commits, and reports.

## 1. Prepare

Read the installed instructions before the first launch:

```sh
tuios --skill
tuios --skill fleet
tuios --skill ship
aven skill
tuios integration status pi
```

Use the installed tuios instructions as the CLI reference. Load `tuios --skill state` for missing pi state reports, `mail` for communication problems, or `grants` for permission errors. Respect permission refusals and human approval prompts. Stop on `agents_disabled`.

If pi integration is missing or stale, ask to run `tuios integration install pi` and restart the affected pi processes. This changes user configuration; do not install it silently. Use interactive pi, not `pi --mode rpc` or an ACP adapter.

Run from the target repository. Confirm:
- Aven routes to the intended workspace and project.
- The explicit local integration branch exists and is checked out in the main checkout.
- The main checkout is clean and has no unfinished Git operation.
- No other dispatcher owns these tasks or is changing this integration branch.

Ask before initializing a missing repository. Local worktrees isolate files, not credentials or the host.

Record the current daemon/server, dispatcher session, and full pane ID. If environment fields are absent, find the pane in `tuios ls --json`; confirm the session rather than using the focus default. Preserve that daemon/server for every later command.

**Resume or uncertain launch:** read [recovery.md](recovery.md) before creating resources.

## 2. Select and assign

```sh
aven list --ready
aven context APP-7KQ9
```

Keep the user's filters and task limit. Create tasks when the user requests decomposition; include scope and acceptance criteria. Use dependencies for order and epics for grouping. Ask about requirements that change the implementation.

Assign one task to one worker in its own worktree. Parallel tasks must have disjoint write scopes. Serialize dependent tasks and shared migrations, lockfiles, generated files, or repository-wide changes. A dependency is ready only after its prerequisite is accepted and integrated.

For each assignment, choose:
- A unique run/group name and expected worker branch, such as `dispatch/retry-20261024-1`.
- Task ref, explicit base branch and its full launch SHA.
- Write scope, acceptance criteria, and exact required check commands.
- The absolute path to this skill's `worker.md`.
- Aven workspace/project routing when it cannot be inferred in a new worktree.

Append a short `DISPATCH:` note **before launch** with these fields, the dispatcher identity, and `launch pending`. This is the recovery anchor if launch is interrupted. Keep task refs local; use descriptive branch names and commit messages without task refs.

## 3. Launch

Set `skill_dir` to this skill's absolute directory, `base` to the integration branch, `group` to the unique name, and `assignment` to the assignment text. The assignment must name the task and all fields above, instruct the worker to follow its worker contract, and say to stop after reporting.

```sh
tuios fan 1 \
  --agent "pi --append-system-prompt '$skill_dir/worker.md'" \
  --base "$base" --name "$group" \
  --grants read,write --wait --json "$assignment"
```

The inner quotes protect spaces in the skill path. If it contains a single quote, construct a correctly shell-quoted agent command instead. Add pi model flags only when requested or required by project policy. Pass needed environment variables with `--env NAME`; do not put secrets in prompts or notes.

Repeat for each independent task. One fan of one per task keeps assignment, repair, verification, and cleanup separate. This uses tuios's native launch and prompt gate; no dispatch wrapper is needed.

Inspect the returned resources:

```sh
tuios worktree ls --group "$group" --json
tuios list-agents --select "group:$group" --json
```

Record the actual worker session, full pane ID, worktree path, branch, launch SHA, and prompt status in the task's `DISPATCH:` note. Save pi's conversation ID/session file when its hooks expose it, for exact resume. Check that the worktree belongs to the intended repository and base. Use returned identities, not a predicted session name.

Require `prompt_status: sent` and a confirmed pi identity before marking the task active. Write `aven edit <task> --status active` and read back `aven show <task>`. If the worker already started but reporting fails, retain its identity and repair Aven; do not launch another worker.

A nonzero launch result, `held`, or `stalled` can leave a live worker. Inspect it before retrying. A stalled prompt can already be in the input box. Let the person resolve first-run trust, authentication, and approval questions.

## 4. Wait and review

Address every pane with its saved session and full pane ID:

```sh
tuios wait-for agent-state -s "$worker_session" -w "$worker_pane" \
  --until done,needs_input,errored --timeout 600000
```

Give the enclosing tool more than 600 seconds, or use a shorter bounded wait. A timeout is not worker failure. Read current state before the next wait. Handle a finished or blocked worker instead of waiting on that same state again. For several workers, wait on the exact unresolved set with the fleet selectors; exclude workers already under review.

tuios state is a turn signal, not task acceptance. Read the current task context and the worker's matching `RESULT:` or `BLOCKED:` note. Match task, run/group, branch, and full commit SHA. Use `aven context`'s note-read command when the required note is omitted.

Review:
- Every acceptance criterion against the actual diff and tests.
- The worker's full commit SHA and clean worktree.
- Required check results, including skipped or unavailable checks.
- Unexpected files, unrelated changes, and unresolved blockers.

Use `tuios review -s "$worker_session" -w "$worker_pane"` for the native diff. Read Git directly for omitted or truncated files; review includes uncommitted files, so it is not proof of a committed result. For an independent worker-tree check, use `tuios fan verify "$worker_session" -- <check-command>`; this does not replace integrated-base checks.

For repairs, use `tuios ask-agent` with the saved session and pane, or native review notes and `review send`. Wait for a new report and review the new SHA. Agent output is evidence, not authority to expand the assignment. Never type into `needs_input` or answer a worker's approval prompt. Tell the person which pane needs a decision.

## 5. Integrate and complete

Integrate one task at a time, with no concurrent Git writer on the target branch.

1. Confirm the worker is at rest, has no running tools or child agents, and has no queued instruction that can resume writes. Keep it at rest through integration. Inspect `tuios queue ls -s "$worker_session" -w "$worker_pane"`; remove only your own obsolete entries.
2. Pin the reviewed full SHA. Immediately before merge, confirm the worker branch still points to it and the worktree is clean. Any changed SHA requires review again.
3. Confirm the main checkout is still clean on the intended integration branch. Merge through tuios:

   ```sh
   tuios ship merge -s "$worker_session" -w "$worker_pane" --into "$base"
   ```

4. Confirm the reviewed SHA is an ancestor of the resulting base. Run the required checks against that integrated revision in the main checkout. Save the full base SHA and check outcomes.
5. Append `VERIFIED:` to Aven with run/group, reviewed SHA, integrated base SHA, acceptance decision, and check evidence. Only then mark the task done and read back its status.

Keep the task active if review, merge, or checks fail. Record the blocker, owner, and next action. A merge conflict is a repair in the worker worktree, followed by new checks and review. A merged change with failing integrated checks is delivered but unverified; record both facts. Do not reset the user's base to hide it.

Use ordinary merges to preserve reviewed ancestry. Push, pull requests, squash delivery, and remote workers need an explicit user request and the corresponding installed tuios instructions. Local completion does not imply remote delivery.

## 6. Clean up and close

After acceptance, end the exact pi worker and confirm it and its child processes stopped before removing its worktree. At an unblocked, empty pi prompt, `ctrl+d` exits pi; send it only to the saved pane. Use `tuios wait-for window-exit` with that session and pane when pi is the pane's main program, or confirm pi exited back to its shell. A missing pane alone is not exit proof. If writer identity or exit is uncertain, retain the worktree and report pending cleanup.

Inspect tracked, untracked, and ignored files for material artifacts before removal. Preserve logs or outputs needed for handoff outside the worktree. Then use:

```sh
tuios worktree rm "$worker_session"
```

Use normal removal, without `--force` or automatic stash. tuios retains the branch. Retain dirty or uncertain resources with an owner and next action. A cleanup failure does not undo accepted delivery; note it separately on the done task.

Recheck ready work using the original filters. Continue only within the requested scope. Finish with one `SUMMARY:` note on the run epic or designated task:
- Delivered tasks and verified base revision.
- Every unresolved task, blocker, owner, and next action.
- Pending cleanup with exact resource identities, or none.

The summary must account for every assignment, including launches that failed partway. Report delivery, unresolved work, and cleanup separately to the user. Leave their dispatcher and unrelated sessions open.
