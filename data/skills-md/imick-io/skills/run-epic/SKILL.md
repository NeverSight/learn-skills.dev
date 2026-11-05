---
name: run-epic
description: Build every ticket of one epic inside this Claude Code session, the way the agent loop would (claim, branch, implement, review, land, next), one ticket at a time until the epic is built and its PR is open. Use when the user wants an epic built here without the Docker loop, says "run the epic", "build the epic's tickets", or "run-epic 42".
disable-model-invocation: true
argument-hint: "<epic number> [--force]"
---

# Run epic

The agent loop's pipeline, in a session, on one epic. You coordinate; one subagent per step builds. The loop runs the same pipeline in Docker sandboxes on the epics it owns; this skill is for an epic labelled `manual`, which the loop never touches, when the user would rather watch it being built here than build it by hand with `/claim`. A ticket built either way is indistinguishable: the same claim and branch rules, the loop's own prompts, the same landing.

[scripts/run-epic.mjs](./scripts/run-epic.mjs) does every deterministic step; run it from the repo root as `node <this skill>/scripts/run-epic.mjs <command>`. Below, `run-epic` means that.

## 0. Before the first ticket

1. **`run-epic check <epic>`.** It stops when the checkout is dirty, `gh` is logged out, or the epic isn't `manual` (exit 2). On exit 2, ask the user to add the `manual` label and run again; if they refuse, stop. `--force` runs a non-manual epic only when the user says the loop is off.
2. **Permissions.** This run is unattended and lasts hours. Ask the user, once: is the session in a mode where tool calls won't prompt (auto mode, or an allowlist covering `git`, `gh`, the package manager and the test runners)? If not, stop and ask them to switch (`shift+tab` or `/permissions`); never change settings yourself.
3. **Services.** `check` prints what `.sandcastle/sandbox-setup.sh` starts in a sandbox and the project's dev-up command. Check they are running on this machine (a quick port probe or the project's own status command). If not, **ask before starting them**; start them only on a yes, with the project's own command.
4. Tell the user the plan in three lines: the epic, how many tickets are ready now and blocked, and that you will report at the end (and in Slack when `check` shows a webhook). Then start; don't ask again until the epic is built.

## 1. One ticket, start to finish

Take the first ticket of `frontier.ready` (`run-epic frontier <epic>` re-reads it; the order is the loop's: oldest first). Then:

1. **`run-epic prepare <ticket>`.** Claims it (assignee), merges `main` into the epic branch and pushes, creates or reuses `agent/issue-<n>` off it in a worktree under `.claude/worktrees/run-epic-<n>`, installs dependencies there. Read the JSON: `install` must say ok; `branchNote` tells you whether earlier work exists.
2. **Build.** `run-epic prompt implement <ticket>` (`prompt bug` for a bug) prints the loop's own prompt, filled in, with a RUN-EPIC preamble naming the worktree. Dispatch **one subagent** (general-purpose) with that text as its whole prompt. Wait for it. Never build two tickets at once: they share this machine's database, ports and CPU.
3. **`run-epic commits <ticket>`.** `0` means the agent couldn't build it and has said why on the issue: `run-epic handback <ticket> "<its reason, one line>"`, then **go to the next ticket**. Don't retry, don't fix it yourself: the loop gives one attempt, and so do you.
4. **Review.** `run-epic prompt review <ticket>`; dispatch one subagent with it. Wait.
5. **`run-epic land <ticket>`.** Merges onto the epic branch, pushes, closes the ticket with the loop's wording, deletes the branch and worktree, rebuilds the tracker, posts to the Slack feed. Once the epic's PR is open (fixes after `/verify-epic`), each push runs the project's CI, so the script batches them as the loop does: while more of the epic's tickets are ready, or this one unblocks another, the push says `[skip ci]`, and the last one runs CI. **Exit 3** is a merge conflict with work landed since the branch was cut: as the loop does, `run-epic prepare <ticket> --retry` (drops the branch, recreates it on the latest epic branch) and build once more from step 2. A second conflict is a hand-back.
6. Note one line for the final report: landed or handed back, and why.

Then `run-epic frontier <epic>` again: landing unblocks tickets. Repeat until `ready` is empty.

**If a step fails for another reason** (a push refused, `gh` down, a subagent that died): hand the ticket back with the error as the reason and continue. The run is unattended; a stuck ticket must never stop the others.

## 2. When the frontier is empty

`run-epic finish <epic>`:

- **`done: true`** with a `pr`: every ticket of the milestone is closed. It merged `main` in once more and opened the epic's PR to `main` (tickets listed, `Closes #<epic>`). Tell the user to run `/verify-epic` on it before merging; don't run it yourself.
- **`done: false`** with `open`: tickets remain that this run can't take (handed back, blocked by a hand-back, claimed by someone else). No PR yet.
- **`ciRun: true`**: the batch ended on a `[skip ci]` push (its last ticket was handed back), so `finish` pushed an empty commit to run CI once on everything that landed. Mention it in the report.

## 3. Report

One message, standing on its own, since the user may have been away: the epic, each ticket landed with its commit, each ticket handed back with its reason and a link, the PR or what still blocks it, and anything the agents flagged (a failing check that predates the run, a service they missed). `run-epic notify feed "<the same, in three lines>"` when `check` showed a webhook. Leave no worktree of yours behind: `land` and `handback` remove theirs.

## Rules

- **Reuse the loop, don't improvise.** The prompts are the loop's (`.sandcastle/*-prompt.md`, else this repo's templates); if a step needs something they don't say, that is a change to the loop's prompts, not to this run.
- **Subagents commit; you land.** No subagent pushes, opens a PR, closes or labels an issue. Everything on GitHub goes through the script.
- **One attempt, one ticket at a time, no questions mid-run.** The hand-back is the question: it reaches the user on the issue, in the tracker and in Slack, and the run goes on.
- **Never re-run CI by hand mid-run.** The batch's last push runs it; a re-run before that tests a branch that's about to change.
- **`main` stays untouched.** The checkout never changes branch; all work is in worktrees and pushed to the epic branch.
