---
name: babysit
description: "Use when asked to babysit a GitHub PR or wait for its CI or review checks."
---

# Babysit a PR

Check mergeability first, then run one `gh` watcher and wait for its process
to finish. Success means the intended checks completed for the current PR
head, with any failures or missing checks accounted for. Babysitting does not
authorize merging, bypassing gates, or posting review comments.

## Check for conflicts before waiting

Use an explicit PR number and repository throughout:

```sh
gh pr view <n> -R <owner/repo> --json state,url,headRefOid,baseRefName,baseRefOid,mergeable,mergeStateStatus,isDraft,reviewDecision
```

Record the head SHA, base branch, and base SHA. Stop watching if the PR is closed or
merged. Handle `mergeable` before starting a watcher:

- `CONFLICTING`: use [resolve-pr-conflicts](../resolve-pr-conflicts/SKILL.md)
  against this PR's current base, then repeat this inspection after pushing.
- `UNKNOWN`: GitHub has not established mergeability. Recheck after a short
  delay; if still unknown, inspect a fetched head/base locally or report the
  unresolved state. Do not assume it is conflict-free or loop indefinitely.
- `MERGEABLE`: proceed. Other merge gates can still block the PR;
  `mergeStateStatus: BLOCKED` alone does not establish a textual conflict.

GitHub does not run workflows triggered by `pull_request` while merge
conflicts exist. Resolving conflicts first prevents waiting for checks that
cannot start. See [GitHub's workflow troubleshooting](https://docs.github.com/en/actions/how-tos/troubleshoot-workflows).

## Let gh watch the checks

```sh
gh pr checks <n> -R <owner/repo> --watch --interval 10
```

The [PR checks command](https://cli.github.com/manual/gh_pr_checks) refreshes
every ten seconds by default and waits until the reported checks finish.
Use `--fail-fast` when a failure should return control immediately for repair.
Add `--required` only when the task concerns required checks alone; it can
exclude a review bot's optional check.

Run the command once as a long-running process. Use the execution tool's
completion notification or wait on the same session with long practical
waits. Do not alternate fresh `gh pr checks` calls with model-driven sleeps,
restart the watcher on each tool yield, or narrate unchanged refreshes.

This is CLI-managed polling, not a server event subscription. The
[implementation](https://github.com/cli/cli/blob/v2.99.0/pkg/cmd/pr/checks/checks.go)
refreshes while checks are pending and exits when none remain. It does not
stay subscribed for checks created later or for future review comments.

Inspect the final output and exit status. Failed checks return nonzero;
ordinary non-watch output uses exit code 8 for pending checks. Authentication,
API, and missing-check errors also need diagnosis. Use a separate snapshot
when structured details help:

```sh
gh pr checks <n> -R <owner/repo> --json name,bucket,state,workflow,link
```

Do not combine `--json` with `--watch`. JSON is a snapshot, and its successful
export does not prove checks passed. Inspect `bucket` values; cancelled or
skipped checks are not evidence that the intended tests ran.

## Handle checks that cannot finish

If no checks are reported, the watcher exits with an error rather than waiting
for their creation. If an expected check is missing, or a pending check has no
progress beyond its normal runtime, inspect the workflow and run details.
Check for conflicts again, trigger/path filters, skip annotations, workflow
approval, and unavailable runners as the evidence warrants. Do not repeatedly
restart a watcher for a workflow that cannot run. Resume once the blocker is
resolved; otherwise report the blocker.

For a known GitHub Actions run, use its specific ID:

```sh
gh run watch <run-id> -R <owner/repo> --exit-status --compact --interval 10
gh run view <run-id> -R <owner/repo> --log-failed
```

The [run watcher](https://cli.github.com/manual/gh_run_watch) covers one Actions
run, not every PR check. `--exit-status` makes run failure return nonzero.
It does not support fine-grained PAT authentication. Inspect failure logs when
needed; repair and push within the authorized task, then start with the
conflict check again. Do not rerun failures repeatedly without a diagnosis.

A review service that publishes a check can be watched through `gh pr checks`.
A service that only posts comments or reviews is outside these watchers.
Use that service's completion mechanism if available; otherwise report that
limitation rather than treating green CI as a completed review.

## Verify the result

Re-read the PR state, head SHA, base branch and SHA, and mergeability after the watcher
exits. Take a final checks snapshot and confirm the expected checks appeared.
If the head or base changed, or conflicts appeared, repeat the preflight and
watch the current checks before claiming success. A watcher exit alone does
not prove merge readiness or review approval.

Report the PR, verified head SHA, check results, and any review or workflow
blocker. Continue to merging only when the user's task authorizes it.
