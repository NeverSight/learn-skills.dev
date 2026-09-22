---
name: ci-speedup
description: Cuts the wait from push to green by measuring a pipeline's critical path from run timestamps, then splitting, sharding, trimming setup and sharing test module state, with a before/after ledger. Use when asked to "speed up CI", "CI is slow", "why does a PR take 15 minutes", "CI is the bottleneck", or when agents merge faster than checks finish. For a red build use pr-babysitter; for a new package's pipeline use scaffold-cli.
compatibility: Reads run and job timings through the GitHub CLI or a GitHub MCP server; other CI hosts need their equivalent API. Local re-timing needs the repo's toolchain installed.
---

# CI Speedup

Make the wait from push to green shorter, measured, and written down.

- **IS:** measuring a pipeline's critical path from run timestamps, choosing the levers that shorten it, changing workflow and test configuration, and recording before and after with the trend that says when the next round is due.
- **IS NOT:** getting a red build green (`pr-babysitter`), writing a pipeline for a package that has none (`scaffold-cli`), or general repository hygiene.

## What Changes the Number

Wall-clock is the slowest chain of dependent jobs, not their sum. The number is push to green for one pull request, median and p90 over recent runs. Around five minutes an agent loop stops waiting on checks and the bottleneck moves to deploy and review. A lever that saves runner minutes off the critical path is a cost saving, and the ledger records it as one.

Three ratios decide what to do next:

- **Setup tax.** Checkout, runtime, dependencies, and service boot, per job. 110 seconds of setup around 60 of work is a batching candidate; around 400 it is a sharding candidate. Each shard adds a setup, so cut setup before adding shards.
- **Import versus test.** When Vitest's import plus environment figures exceed its tests figure, the suite pays to boot the module graph per file. A shared registry or a lighter environment moves that; more shards only spread it.
- **Gate versus work.** Change detection, matrix computation, and cache saves sit on the chain. Anything they do beyond deciding is paid by every job behind them.

## Reference Files

| File | Read when |
|------|-----------|
| `references/measuring.md` | Step 1: run, job, and step timings; percentiles; the critical path; test-runner duration lines; the baseline table. Step 4: the rules that decide whether the after-run credits a lever |
| `references/levers.md` | Step 2: the lever catalogue by class, what each needs to be true, expected gain, how each has failed |
| `references/ledger.md` | Step 5: the ledger, its trend table, and the instruction-file lines that stop the layout regressing |
| `scripts/ci-timings.sh` | Step 1: one run's jobs, steps and critical path, or `--runs N` for median and p90 per job; `--help` gives the forms |

`evals/evals.json` holds scenarios and the with-versus-without comparison for changing this skill; it never loads during a task.

## Workflow

Copy this checklist to track progress:

```text
CI speedup progress:
- [ ] Step 1: Baseline (median and p90 over recent runs, per-step table for the longest job, critical path)
- [ ] Step 2: Choose levers by gain on the critical path, with a predicted chain
- [ ] Step 3: Change the pipeline; re-time locally what can be re-timed
- [ ] Step 4: Push, read the branch's own runs as the after-measurement, iterate
- [ ] Step 5: Ledger with trend, instruction-file lines, and the queue of what is left
```

Done means a mergeable pipeline change, a ledger whose after column comes from runs on the branch, and instruction-file lines for the layout and the test defaults. Reading runs, re-timing locally, and pushing to the working branch need no check-in; spending money (paid runners, more parallel jobs on a metered plan) and merging are the user's.

### Step 1: Baseline from timestamps

Use the run and job API, never memory or the workflow file. `scripts/ci-timings.sh --runs 20 --workflow ci.yml --branch main` gives median and p90 per job; the single-run form on one default-branch run and one pull request gives the steps and the chain. Name the critical path in a sentence: which jobs, in what order, minutes from run start to the last job's end. Pull the slowest test step's log for the runner's own breakdown, and classify every minute on the path as toolchain, gating, setup, or execution before proposing anything.

### Step 2: Choose levers

Pick from `references/levers.md` by gain on the chain from Step 1. Write the predicted new chain with its minutes; a plan without a number cannot be checked. Prefer levers the suite itself proves safe (a sharded run passes or does not) over ones that need judgement per file. Runner minutes may rise when wall-clock falls; say by roughly how much, and whether the repository pays for minutes.

### Step 3: Change the pipeline and re-time locally

Edit the workflow and test configuration in one branch. Measure locally whatever can be measured without pushing, with the current and the new configuration. A change that makes a shard fail is a finding, not a reason to skip that shard.

Keep the guards. Change detection, merge-DAG checks, concurrency groups, and deploy gates exist because of a past incident; move them, do not drop them, and keep the comment that cites the incident next to the guard.

### Step 4: Push and read the after-measurement

The branch's own runs are the after-measurement. Read them as in Step 1, put the numbers beside the baseline, and apply the verification rules in `references/measuring.md` before crediting a lever. When predicted and measured disagree, find out why before adding another lever. Repeat until the path stops moving or the remaining levers need a decision the user owns.

### Step 5: Ledger and guardrails

Write the ledger from `references/ledger.md` into the repository's docs: before, changes, after with run ids, a trend row with when the next round is due, and the queue of levers not taken with what each waits on. Add the instruction-file lines for the layout and for how a new test lands in the fast path. Done when the after column comes from real runs, not the prediction.

## Gotchas

- `cancel-in-progress: true` on the default branch cancels the superseded run's deploy mid-rollout. Cancel on pull requests only; default-branch pushes queue.
- The same setting cancels your own measurement: a push to the pull request while its run is in flight throws that run away. Hold docs-only commits until the measured run completes.
- A queued default-branch run that gets replaced never runs its checks, so change detection against the previous commit skips work that never passed. Compare against the last commit that finished successfully.
- Every workspace's tests in one job through a task runner with no remote cache is oversubscription, not caching: twenty test processes on four cores, each with its own workers. A 0:47 suite took 3:04 there. Read the per-workspace duration lines before blaming the tests.
- A `Duration` line where import plus environment is several times the tests figure says the suite boots the module graph per file. Sharding halves that bill without lowering it; `isolate: false` on the files that tolerate it does.
- Under a shared registry the files that break are rarely at fault. `vi.mock`, fake timers and `vi.stubGlobal` registered by one file outlive it, and the failures land in later files with no mocks of their own (31 of 222 failed, most of them victims). Isolate by the calls a file makes, not by which files went red.
- A restored dependency cache can be slower than a fresh install (Linear measured restore at four times the install). Time both; a 2.6 GB `node_modules` is not worth trying.
- Excluding containers from a service stack saves their pulls, not the boot: seven fewer Supabase containers took the step from 2:47 to 2:11, and database init and health waits were the rest. Predict from the step's log, not the container count.
- Overlapping two IO-bound steps on a hosted runner returns less than their sum: a background service boot cut the post-install wait from 2:11 to 0:34 while the install grew from 1:32 to 2:28.
- A background boot must resolve its project the way the reading step does. `supabase start --workdir <dir>` booted a default project under another container name and `supabase status` found nothing.
- Vitest and Playwright shard by file count, so two shards differ by a minute and the same shard varies by a minute between runs. Read median and p90 before adding a shard; splitting the long files rebalances, another shard does not.
- A job that `needs` a job skipped by an `if` skips too. Where a deploy must run past an optional job, gate on `always()` and the specific results.
- Matrix jobs default to `fail-fast: true`; one red shard cancels the rest and hides how many are red. Set `fail-fast: false` on test shards.
- A format check with `--check .` on the whole tree makes docs-only commits ineligible for `paths-ignore`; only extensions the formatter never matches can be skipped.
- A Docker registry cache pushed to the same tag as the image never hits: the push overwrites the cache manifests and `cache-from` finds a regular image. The cache ref is its own tag.
- `RUN --mount=type=cache` without an `id` shares one directory between parallel builds of different images and corrupts it under the default `sharing=shared`. Name every mount.
- Editing the deploy line in the workflow does nothing when it calls a wrapper script that owns the real command. Find where the command runs before re-timing.
- `turbo run typecheck`, `lerna run`, and `npm run -ws --if-present` silently skip workspaces that lack the script; a green root command proves nothing about a workspace that never ran. Validate per workspace.

## Related Skills

- `pr-babysitter` for a run that is red rather than slow, and for watching the pull request this work opens.
- `pr-creator` for the pull request; the ledger's before and after tables belong in its body.
- `agents-md` when the instruction-file lines from Step 5 grow into a wider AGENTS.md pass.
- `scaffold-cli` and `scaffold-nextjs` when the repository has no pipeline yet; this skill starts from timestamps, which a new repository lacks.
