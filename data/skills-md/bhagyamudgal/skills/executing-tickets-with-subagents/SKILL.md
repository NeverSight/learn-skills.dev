---
name: executing-tickets-with-subagents
description: Orchestrate ledger-tracked work through subagents. Use for a bundled GitHub ticket with 3+ sub-issues, a request for subagent-driven execution, resuming such a run after compaction, or explicit away/keep-going delegation even when only one task remains.
---

# Executing tickets with subagents

## Overview

The main conversation only orchestrates. Every edit, review, and QA pass runs in a dispatched subagent. Durable state lives on disk and GitHub. Compaction cannot reach either place, so the run survives it.

## Select the run branch

- **Unattended.** When the user explicitly says they are stepping away and asks work to continue, read `${CLAUDE_SKILL_DIR}/references/unattended-scheduler.md` in full before the first dispatch. Its scheduling, transition, update, and handoff contract applies even to one task. Use the phases below only when the work is also a bundled GitHub ticket.
- **Bundled ticket.** Use the phases below for the ticket's intake, waves, and endgame.

Record the selected branch in the ledger before dispatching work. That is the gate.

## Phase 0: Intake

1. **Resume check.** When a ledger exists for this ticket, read it before anything else and execute its NEXT ACTION. The ledger is the only source of run state. Conversation memory is not. Reconcile all four trackers before the next wave: the todo list, the checklist comment, the harness tasks, and the ledger.
2. **Fetch the full issue thread.** Read `${CLAUDE_SKILL_DIR}/../audit-ticket/references/ticket-evidence.md` in full and the authenticated, fail-fast image-download guidance in `${CLAUDE_SKILL_DIR}/../audit-ticket/SKILL.md`, then fetch structured issue JSON with `gh issue view <n> --json number,title,body,author,createdAt,updatedAt,state,assignees,url,comments`. Build the source map from the issue body and every comment's `body`, `author`, `createdAt`, and `url`. Download every attached image with authentication and an HTTP-error exit, check that exit before opening the file, and actually read each successful image. Record a failed download as `image <i> unavailable`. Never open or hash its error body as image evidence. Comments routinely override or extend the original body, and an unread comment is a spec you do not have.
3. **Research the codebase.** Verify claims against the code before bringing questions to the user.

## Phase 1: Lock, plan, instrument

1. **Explore** the code with parallel read-only agents. Produce a per-sub-issue verdict of already-done, partially-done, or not-started, each with file:line evidence.
2. **Grill the user.** Run `grill-me` on task order, PR strategy, done-bar per task, tracking method, and anything user-owned such as migrations and commit policy. Grilling ends when every item above has a locked answer written into the ledger. Locked answers are law for every later dispatch.
3. **Spec then plan.** Write one brief per sub-issue and cover every sub-issue, each with exact code and 2-3 named risks the reviewer must check. Briefs locate by symbol, because line numbers drift as tasks land. Then run the `grill-me` verification pass against the brief set before task 1.
4. **Instrument tracking** before task 1:
   - Keep a ledger, for example `docs/<ticket>-progress.md`. It is the recovery map, and the contract below defines it.
   - Keep the `tasks/todo.md` checklist.
   - Keep one editable GitHub checklist comment on the issue. It carries status plus root cause per item. Save its comment id in the ledger and update it via `gh api ... -X PATCH -F body=@file`. Render the complete initial comment to a file and freeze its SHA-256. Immediately before creating it, refresh the issue's URL, `updatedAt`, body, state, assignees, and comments. Confirm the intended checklist is still absent, then invoke `preflight-mutations` with those guards, the exact frozen file and digest, the locked tracking decision, the expected resulting comment body, and the authoritative comment read-back. Apply its result contract before continuing. Read back the created comment by ID and require its complete body to equal the frozen content. Retry only when authoritative read-back proves no effect. Empty stdout is not failure.
   - Keep the harness todo list with `TodoWrite`.

## Ledger contract

Write the ledger for a reader with zero context. Assume the next writer remembers nothing. Update it after EVERY wave. It must contain per-task status with commit SHAs, the current NEXT ACTION stated imperatively, accumulated deferred Moderate and Minor findings awaiting triage, standing process rules, and locations of briefs and artifacts plus the ticket source map. The standing rules cover granted permissions, environment quirks and fallbacks, and QA credentials and data notes.

## Phase 2: The wave (one per task)

1. **Brief to scratchpad.** When HEAD moved since planning, run an Explore drift-check and write an addendum. The addendum wins.
2. **Fresh implementer agent.** The orchestrator dispatches, the agent edits. Bug fixes are TDD. Write the failing test first and watch it fail. Format and run the task's type-check loop, then leave the task diff uncommitted for independent review. Dispatch prompts are self-contained: paths, env, locked decisions, verification commands, intended commit format, report format, and environment-quirk fallbacks. The agent has no other context.
3. **Two-stage review, separate subagents.** One combined reviewer anchors on whichever lens it starts with. Two fresh ones do not. A review is two reports, one per stage:
   - **Stage 1, spec compliance.** The reviewer gets the task brief plus the diff, and the named risks to verify. Its inputs are exactly those two. It returns verdicts against the ticket requirements, one of Missing, Extra, or Misunderstood, each with file:line evidence.
   - **Stage 2, code quality.** An independent reviewer checks correctness, error handling, tests that assert real behavior, and structure. It ranks findings Critical, Serious, Moderate, or Minor. `parallel-review` runs alongside and covers style and convention. Stage 1 is what catches spec violations.
4. **Triage every finding.** FIX-NOW means a fix agent repairs it, then both stages re-review until spec passes and quality approves, and a task closes at zero open Critical and Serious findings. DISMISS needs a verified rationale, so check the locked design or brief first, because reviewers re-litigate settled decisions. DEFER covers Moderate and Minor only, and you log those in the ledger. Once review is clear, run the task's applicable `done` lanes over the uncommitted diff. Let `done` invoke `git-commit` for the single verified task commit and record its SHA. When the locked wave strategy includes a push, invoke `preflight-mutations` afterward with the exact remote branch, local and upstream SHAs and commit range, PR base and head and dependencies, and the locked push permission before pushing.

   Treat every report as unverified. Only evidence clears one: SHAs, counts, file:line references, and what ran versus what you only inspected.
5. **`browser-qa`** for UI tasks. It records original data, restores it, and proves the restoration. Its artifacts go to scratchpad only. Run it between waves, with no implementer active. Hot reload contaminates the session mid-test.
6. **Bookkeeping.** Tick `tasks/todo.md`. Immediately before each wave's checklist PATCH, invoke `preflight-mutations` with the exact issue and comment IDs, the replacement body, the current comment version and body, the locked tracking permission, and the read-back, then apply its result contract. Update the harness todo list and the ledger before the next task.

Retire a wedged agent instead of re-nudging it. Record its terminal status or successful interrupt, preserve its worktree and diff location, then move the task from active to ready and dispatch a fresh owner. When you cannot prove inactivity, mark the task blocked instead of assigning a second owner.

## Phase 3: Endgame

1. **Final whole-branch review** from the recomputed merge-base. Recompute it because it moves, and exclude generated files. Report every cross-task interaction found, or state explicitly that none were. Triage all ledger minors as FIX-NOW, FOLLOW-UP, or DROP.
2. Fix pass, then `fix-pr-review` to reply and resolve every external review thread citing commit SHAs or rationale.
3. Render the complete final PR body to a file and freeze its SHA-256. Immediately before updating the body or marking the PR ready, refresh the exact PR URL, current title and body, base and head SHA, draft state, and dependent PRs and workflows. Invoke `preflight-mutations` for that external-metadata batch with those target guards, the frozen body path and digest, the exact resulting body and ready state, the update and ready actions, and the user's ready approval. Apply its result contract, recheck the guards and digest before each write, and require authoritative read-back of the complete body and draft state. Watch CI on the final head. Drafts and merge conflicts silently skip `pull_request` workflows, so "no failures" may mean "never ran". Confirm the workflow ran on the final head, then confirm it passed.
4. **Manual-QA handoff doc.** This is the standard closing artifact for bundled bug-fix tickets. Per fixed item, link the originating issue comment, describe what was wrong before versus what changed in plain language, and give step-by-step testing instructions so the user can validate each fix.
5. **Every stray finding leaves as its own ticket.** Small ones go into one consolidated follow-up ticket. Major findings get a dedicated issue each. Every successor carries `--label ai-created` per `file-issue` section 6. Before composing any rewritten, split, or follow-up issue, reread `${CLAUDE_SKILL_DIR}/../audit-ticket/references/ticket-evidence.md`. Its provenance graph and rendered closeout gate apply to the original and every successor. Apply `file-issue`'s two-vocabulary duplicate search to every proposed successor and resolve every match before staging it. Render every final body first and record its path and SHA-256 digest. Immediately before the first write, refresh the original issue's `updatedAt` and invoke `preflight-mutations` once for the complete batch: exact repository, current original issue state and guards, the original issue's complete frozen investigation update or comment payload, every frozen successor title, body path, digest, `ai-created` label, and create option, duplicate-search queries and resolutions, original-to-successor, successor-to-predecessor, and dependency-relevant sibling links, source finding and evidence IDs, assignees, authorization, and the rendered issue-and-image read-back plan. Apply its result contract, recheck the guards and payload digests before each write, then execute only the writes in that batch. Re-fetch and reread the rendered issue set and images against the source map before reporting the tickets complete. An ambiguous create result follows `preflight-mutations`'s `reconcile-required` contract instead of retrying.

## Hard rules

| Rule | Why |
|---|---|
| Wedged agent → retire, preserve, then replace | Re-nudging wastes time; replacing without proof creates two owners |
| User-owned territory such as migrations, merges, or un-drafting → ask | One approval does not extend to the next category |
