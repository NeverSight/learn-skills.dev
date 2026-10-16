---
name: kstack-execute
description: Build reviewed tasks, integrate, and verify the result.
disable-model-invocation: true
---

# kstack execute

Shared rules: read `../kstack/SKILL.md` first.

Use the plan in this conversation. If lost, reconstruct it from the request, code, and recorded work. No push here. There is no worker cap; dispatch every ready task, using the shared collection rules.

## 1. Frame

- Resolve the requested or project-configured base, otherwise the repository's default branch. Record its SHA, create `kstack/<job>` from it, and run the baseline checks. Preserve existing job state on resume.
- Keep one coordinator-owned state table outside the repo: task, status, agent, branch, base/head SHA, verdict, evidence. Add lane results as they arrive. A baseline failure is not a new task failure; report it separately.

## 2. Build

- Ready means dependencies are integrated. Each task gets its own worktree and branch from `kstack/<job>`, with `python3 "$MODELS" cmd workers --index <task-number>`.
- Briefs stand alone: goal, owned files, acceptance criteria, check command, base SHA, dependency results, report format. No bare "continue" or competing implementations of one task.
- Workers implement, check, and commit. Use `../kstack-debug/SKILL.md` for bugs, `../kstack-perf/SKILL.md` for speed, and `../kstack-verify/SKILL.md` for behavior. Report `task | SHA | files | check + result | assumptions`.
- A missing or incomplete report gets one fresh attempt, only after the old writer has stopped. A second miss is a gap; skip its dependents and preserve the work.

## 3. Review each task

- The `reviewer` uses `../kstack-review/SKILL.md` on the frozen base/head pair. For a one-task job, include scope and regression audit so this review can also fill one final audit lane.
- FAIL returns to the worker. After `max_fails`, block the task and skip dependents. BLOCKED is not a strike; retry only after the environment is repaired, otherwise report partial.
- High-risk tasks also need `security_reviewer` PASS on the same revision. Reviewers never fix code.

## 4. Integrate

- After review, pause the worker and integrate serially: rebase, rerun the task check, then fast-forward. Conflicts go back to the worker; review any resolution before integration. Unlock dependents only after integration.
- Finish dispatch and collection: every task must be integrated, blocked, or skipped, and every started agent accounted for. Only then freeze the integration head as the code-ready SHA. Unfinished work makes the result partial.

## 5. Verification swarm

This section also verifies an existing branch for Finish without rebuilding it. Supply the request, base/head SHAs, acceptance criteria, scenarios with pass conditions, check commands, and any prior reports. Infer missing scenarios from the diff and repo; never invent a previous PASS.

Run independent lanes at the frozen head in detached worktrees (`git worktree add --detach <path> <sha>`). Give each the relevant evidence and a distinct focus. Verifiers never edit source. Select models with `python3 "$MODELS" cmd verifiers --index <lane>`.

| Lane | Required evidence |
|---|---|
| Audit | Two independent focused reviews using `../kstack-review/SKILL.md`. Prefer different models. |
| Gates | Run the full checks, lint, and typecheck once at this head; the coordinator can do this. |
| Live | `../kstack-verify/SKILL.md` for each changed user-visible behavior, with one main scenario compared against base. |
| Perf | Only for a speed target: measure using `../kstack-perf/SKILL.md`, without changing code. |

For a one-task job, reuse its task review as one audit only when the base/head pair and audit scope match. Choose the other verifier from the pool, preferably on a different model. Reuse gates only for the same SHA, commands, and environment; audits check their focused claims rather than rerunning unrelated suites.

- Every required lane returns `base SHA | head SHA | PASS/FAIL/BLOCKED | commands | evidence`. Missing evidence gets one retry, then a gap. An inapplicable check needs a reason; an unavailable required check stays BLOCKED. A gap never counts as PASS.
- Existing defects remain recorded against base unless the change copies, worsens, or newly exposes them. During Execute, new defects become repair tasks through steps 2-4 with one swarm repair round, then stop partial if anything remains. When verifying for Finish, return findings to its fixer loop instead; only its `finish.max_fix_rounds` budget applies.
- After small repairs or a rebase, one independent verifier at the new head checks the diff, reruns gates and affected or previously failed scenarios, and records which earlier results remain valid and why. New behavior or a large diff requires the full swarm again, within the same repair budget.

## 6. Report

Report complete only when acceptance criteria and all required lanes pass. Otherwise report partial. Keep task-to-SHA/check/verdict and lane-to-evidence tables in the job report, with open findings and checks not run. Preserve evidence and unmerged work; clean up only this job's idle agents and disposable worktrees.
