---
name: orchestrate
description: Run a prompt or ToVo issues through T3 worker threads, cross-family review, and fixes, while this session only orchestrates.
disable-model-invocation: true
---

# Orchestrate

You are the **orchestrator**. Your sole job is to run the process: dispatch work, track it, verify review findings, and report. You do not write or edit code. Every code change comes from a worker thread, and every reviewer only reports. When a worker stalls or fails, send it more direction or launch a new worker.

The roles:

- **Worker**: a top-level T3 thread, one per unit of work. Opus 5.5 unless the user names another model.
- **Reviewer**: a report-only T3 delegated task. Sol 6.1 unless the user names another model.

## Plan the run

Split the user's request into **units**: each ToVo issue the user named is one unit, and a plain prompt is one unit. Follow the `tovo` skill to connect, then claim each issue and read its context. Order the units by their ToVo prerequisites, then by the order the user gave. When an issue depends on an unfinished issue outside the run, ask the user how to proceed.

Resolve the **checkout**: the current branch and worktree unless the user named another. Record its absolute path, branch, and `HEAD` as the run's **base**. When the checkout has uncommitted changes, ask the user whether to commit, stash, or keep them before any worker starts.

Call `orchestrator_capabilities` and resolve the worker and reviewer to an exact `providerInstanceId` and model `id`. Prefer the provider's native driver (`claudeAgent` for Claude models, `codex` for OpenAI models), and pick a reviewer instance with `canRunChildTask: true`. When a model is unavailable, tell the user which one and ask how to proceed.

Done when every unit is ordered, every issue is claimed, and the checkout, base, worker, and reviewer are recorded.

## Run each unit

Units in one checkout run one at a time, in order, so no two workers edit the same files at once. Units the user put in separate worktrees can run in parallel.

Launch the worker with `t3_thread_launch`, the resolved worker model, a title naming the unit, and a `workspaceStrategy` that points at the checkout: `existing_worktree` with its path and branch for a worktree, or `root` for the project's main checkout. When the user asked for a separate worktree, use `worktree` with the run's branch as `baseRef`. The `message` carries the whole brief, since the thread starts with no history:

```text
You are the worker for one unit of an orchestrated run.

Repository: <absolute path>
Branch: <branch>
Task: <the prompt, or "ToVo issue <ID>: read its context with the tovo skill">

Implement the task and run the project's checks. Commit your work on this branch with atomic, descriptive commits. Do not push or open a pull request. For a ToVo issue, comment on friction as you go and leave the issue's status to the orchestrator; the orchestrator also runs the code review.

When done, reply with a summary of the change, the commit SHAs, and the checks you ran with their results.
```

Retain the `threadId` and wait with `t3_thread_wait`, reading the reply with `t3_thread_read`. When the worker asks a question, answer it from the request and the issue context, or ask the user when only they can decide.

Done when the worker has replied with its commits and its checks pass, or the user has decided how to handle a failure.

## Review each unit

Launch the review as the `t3-review` skill's **Launch the review** section describes (`~/.agents/skills/t3-review/SKILL.md`), with the run's reviewer as the target, the unit's commits as the scope, and the unit's prompt or issue as the requirements. Retain the `taskId`, then end your turn; the reviewer's completion wakes this thread.

When the review fails or returns no report, retry it under a new `clientRequestId`. A missing report is never a clean review.

For every Critical, High, and Medium finding, read the code and confirm it from the source, a test, or a non-mutating reproduction. Send the verified findings to the unit's worker with `t3_thread_send`, each with its location, failure scenario, and suggested fix, and ask it to fix and commit them. Record each rejected finding with its reason. Low findings go to the final report.

When the fixes are more than a few lines, review the fix commits in a new round: a new `clientRequestId` and a brief that carries the original brief, the prior findings, and what the worker changed. After three rounds that still produce verified Medium or higher findings, stop the loop and ask the user.

Done when every Critical, High, and Medium finding is fixed by the worker or rejected with a reason.

## Review the whole run

Skip this section when the run has one unit.

When every unit is done, follow `~/.agents/skills/t3-review-quorum/SKILL.md` with the run's commits from base to `HEAD` as the scope and every unit's prompt or issue as the requirements. Its reviewers and read-only boundary apply as written.

Send each verified Critical, High, or Medium finding from the quorum report to the worker whose unit introduced that code. When a finding spans units, launch a new worker thread in the same checkout with the finding list as its task. Wait for the fixes, then confirm each one against the code.

Done when every Critical, High, and Medium quorum finding is fixed by a worker or rejected with a reason.

## Close out

Mark each ToVo issue `completed` with `issue_set_status`, giving a reason that names its commits. When ToVo refuses the status, move the issue to `in_review` with the same reason and tell the user.

Report to the user:

- Each unit with its worker thread linked as `[title](t3-thread://v1/<threadId>)`, its commits, and its ToVo status
- The reviewer models, and the findings fixed, rejected with reasons, and left as Low
- The quorum verdict when one ran
- The branch and `HEAD`, ready to ship as one unit unless the user asked otherwise
