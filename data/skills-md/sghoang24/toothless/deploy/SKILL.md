---
name: deploy
description: "You MUST use this to take an approved, verified release to production - the workflow's final phase. The goal is to ship the proven candidate on explicit human approval, with a known rollback, then smoke the live system and roll back fast if it fails. You are not allowed to deploy on your own initiative; explicit approval, green e2e on the merge candidate, and a written rollback are preconditions. Trigger phrases: deploy, ship it, release, go live, promote to prod."
argument-hint: "Point at the release, e.g. 'release v0.1' or 'P2 to production'."
---

# Deploy

`Review` judges the change, `verify` proves the suite green, and `e2e-testing` proves the assembled product works. Deploy is the last node of the spine: it takes that proven artifact and puts it **in front of real users**, where a mistake is costly and hard to undo.

It is the one phase hardest to reverse and most visible, so it has the strictest gate: **explicit
human approval, every time.** Like merging a branch, it never happens on your own initiative. Use it
whether or not `fight` is driving.

## The Model

| Thing         | What it is                                               | Where it lives            |
| ------------- | -------------------------------------------------------- | ------------------------- |
| **Release**   | The artifact + version being deployed.                   | tag / build / image       |
| **Candidate** | The exact build proven green (e2e + tests) — what ships. | CI artifact, not "latest" |
| **Gate**      | The preconditions that must be true before deploy.       | this skill                |
| **Smoke**     | A fast post-deploy check that the live system works.     | the running environment   |
| **Rollback**  | The known way back to the last good version.             | documented before deploy  |

Deploy ships **the proven candidate**, not a fresh build. If what you deploy isn't what passed the gates, the gates proved nothing.

## When to Use

- A milestone/release is done: e2e green, tests green, branches landed (via the MR, on approval).
- The human explicitly says to deploy, ship, release, or go live.

**Do NOT use** on your own initiative, without explicit approval, or before the preconditions are met. Do NOT use to _prove_ the product (that's `e2e-testing`) or to merge a branch (that's `finishing-a-development-branch`). Deploy is the step after those, and only on the human's word.

## Core Rules

- **Explicit human approval is required — every time.** Per `AGENTS.md`, never deploy on your own. Silence is not approval; "looks good" on a design or diff is not approval. Only a clear "deploy it" unlocks this.
- **Deploy the proven candidate.** The artifact that runs is the one e2e + tests passed on. Don't deploy "latest" or build fresh at the last second — that ships unproven code.
- **Green e2e is a precondition.** `e2e-testing` green on the merge candidate, plus the project's declared test command (`AGENTS.md`), gate the deploy.
- **Have the rollback ready before you start.** Know the last good version and the exact command/step to return to it. A deploy without a rollback is a bet, not a plan.
- **Smallest reversible step.** Prefer a canary/staged rollout or a behind-a-flag release over an all-at-once flip when the system supports it. Reduce the blast radius.
- **Smoke the live system, then watch.** After deploy, verify the running system (health, the core journey) — not just that the deploy script exited 0. Keep watching the signals for a window.
- **Fail fast, roll back without ego.** If smoke fails or error rates spike, roll back first, diagnose second. A clean rollback is a good outcome, not a defeat.
- **Report what actually happened.** State the deployed version, the evidence, and the result as it is. A rolled-back deploy is reported, not hidden.
- **Update the record.** Tag the release, and when a phase ships append it to the project ledger `specs/_status.md` (a row per PR).

## Procedure

### 1. Confirm the gate (before touching production)

Check every precondition and say so: explicit human approval in hand; `e2e-testing` green on the **merge candidate**; the project's test command (`AGENTS.md`) green; all branches landed through reviewed MRs; the rollback step known and written down. If any is not true, **stop** — it isn't deployable.

### 2. Identify the exact candidate

Pin the artifact: the version/tag/image/commit that passed the gates. Deploy that. Confirm it's the same artifact e2e ran against — not a rebuild.

### 3. Deploy the smallest reversible step

Run the project's deploy path (its `make deploy`, pipeline, or platform command). Where the system allows, do a canary / staged rollout / flag-on rather than a full flip — so a problem hits a fraction, not everyone.

### 4. Smoke the live system

Against the **real, running** environment, check health and walk the core journey (per `e2e-testing`'s critical few). Confirm the observed version matches the candidate. A green deploy command with a broken live app is a failed deploy.

### 5. Watch, then decide

Watch the error/latency/business signals for an agreed window. If they hold, the deploy stands. If smoke failed or signals moved, **roll back now** (step 6) — don't debug live.

### 6. Roll back on failure

Return to the last good version with the pre-written step. Confirm the live system is healthy again. The failure goes back to the normal loop — the fix is built and re-proven before the next deploy attempt (use `debugging` if you need the root cause first).

### 7. Record and report

Tag the release; when the milestone closes, append the shipped PRs to `specs/_status.md` and advance the phase in `specs/_roadmap.md` / `specs/_state.md`. Report to the human: the deployed version, the evidence (smoke results, signals watched), on whose approval, and what's next.

## Red Flags

| Thought                                      | Reality                                                                        |
| -------------------------------------------- | ------------------------------------------------------------------------------ |
| "They said it looks good, I'll deploy"       | Design/diff approval is not deploy approval. Only an explicit "deploy it".     |
| "It's a small change, I'll deploy it myself" | Deploy always needs explicit approval (`AGENTS.md`). Size doesn't change that. |
| "I'll build fresh and deploy latest"         | That ships code the gates never proved. Deploy the proven candidate.           |
| "Tests passed a while ago, good enough"      | Green must be on _this_ candidate, fresh. Re-confirm if it's stale.            |
| "The deploy command succeeded, we're live"   | Exit 0 ≠ working app. Smoke the running system.                                |
| "Something's off — let me debug on prod"     | Roll back first, diagnose after. Prod is not a debugger.                       |
| "We can always fix forward"                  | Fix-forward is not a rollback plan. Have the way back before you start.        |
| "Rolling back looks bad"                     | A clean rollback is a good outcome. Shipping a broken app is not.              |
| "It's late, ship it and watch tomorrow"      | Watch the window now, or don't claim it's deployed.                            |

## Completion Check

A deploy is done correctly when ALL are true:

- [ ] The human gave **explicit approval** to deploy; it was not done on your own initiative.
- [ ] `e2e-testing` was green on the **merge candidate**, plus the project's declared test command (`AGENTS.md`); all branches landed through reviewed MRs.
- [ ] The **exact proven artifact** was deployed (version/tag/image pinned), not a fresh build.
- [ ] A **rollback** step was known and written down before the deploy started.
- [ ] The deploy was the **smallest reversible step** the system allows (canary/staged/flag where possible).
- [ ] The live system was **smoked** (health + core journey) and the running version matches the candidate.
- [ ] Signals were watched for the agreed window; on failure the deploy was **rolled back** and the failure returned to the loop.
- [ ] The release was tagged, `specs/_status.md` updated, and the human told what shipped, on whose approval, with the evidence.
