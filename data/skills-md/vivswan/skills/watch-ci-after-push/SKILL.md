---
name: watch-ci-after-push
description: Use when pushing commits to a remote with CI, merging a PR, or when asked whether a pipeline passed, so every push and merge gets a background watcher.
license: SEE LICENSE IN LICENSE.md
metadata:
  author: Vivswan
---

# Watch CI After Push

Every push gets a **background watcher** that reports pass/fail with failing-job logs. Never fire-and-forget a push. Never watch CI inline: an inline watch blocks the session for minutes while a background watcher costs nothing.

## When to Apply

- A `git push` just ran (any branch with CI)
- A PR just merged: watch the mainline tip, not the topic HEAD (recipe below)
- "did CI pass?" / "watch the pipeline" / "check the build"

## Workflow

### 1. Find the runs the push triggered

- Poll until the runs appear: they can take a few seconds to register after the push. The bundled script does this itself (up to five reads 3 s apart).
- Always pass the **FULL 40-character SHA**: the GraphQL `object(oid:)` lookup rejects short SHAs outright.
- Read through GraphQL, never `gh run list`: the Actions REST endpoints are a separate rate bucket (Polling Budget below). One query returns every workflow run on the commit with its status:

```bash
sha="$(git rev-parse HEAD)"   # full SHA: object(oid:) rejects short ones
gh api graphql -f owner=<owner> -f name=<repo> -f oid="$sha" -f query='
  query($owner: String!, $name: String!, $oid: GitObjectID!) {
    repository(owner: $owner, name: $name) { object(oid: $oid) { ... on Commit {
      checkSuites(first: 100) { nodes { status conclusion app { slug } workflowRun { databaseId workflow { name } } } }
    } } } }' \
  --jq '.data.repository.object.checkSuites.nodes[]? | select(.app.slug == "github-actions" and .workflowRun != null) | "\(.workflowRun.databaseId)\t\(.status)\t\(.conclusion)\t\(.workflowRun.workflow.name)"'
```

Suites without a `workflowRun` belong to external apps (CodeQL, Semgrep) and are not workflow runs. The filter drops them.

The snippet reads the first 100 suites. The bundled script pages through `pageInfo` so a run past the first page is still judged, and it confirms a multi-page snapshot with an identical second read (one page is atomic, several are not).

Still empty after ~15s? That usually means no workflow triggers on this ref. Say so and stop (include the repo's Actions URL).

### 2. Watch in the background

Preferred: spawn a **background subagent** with this brief, then keep working. Never sleep or poll waiting for it. Act on its report when the completion notification arrives:

```text
Watch the CI runs for commit <full-sha> on <repo>: run
"<skill-dir>/scripts/watch-ci.sh <full-sha>" from the repo root and
report its full output. Exit 0: all green (skipped runs count as
pass). Say so in one line. Exit 1: some workflow's latest run ended
with any non-success, non-skipped conclusion (e.g.
failure/cancelled/timed_out). Include the FAIL lines and the log
excerpts. Exit 2: discovery or gh itself failed, or the expected
workflow (default: the one named "CI") never registered a run on
the SHA. Report that as tooling trouble, NEVER as a red pipeline.
Report even on success; never go silent. You watch and report ONLY:
never fix, commit, or push from this role.
```

Fallback without subagents: run the bundled `scripts/watch-ci.sh` as a background shell command. It does discovery, watching, and the failure report in one command.

The path is relative to the installed skill folder, not the repo under review. Redirect its output to a file, and read that file when it exits:

```bash
bash "<skill-dir>/scripts/watch-ci.sh" "$(git rev-parse HEAD)" > /tmp/ci-watch.out 2>&1
# exit 0: latest run per workflow green (older re-triggered runs are reported
# as superseded, not judged); 1: some latest run ended with a non-success,
# non-skipped conclusion (log excerpts in the file); 2: no runs registered or
# gh failed, or the expected workflow never registered a run
```

The script refuses a vacuous green: the expected workflow (by default the one named `CI`) must be among the discovered runs, or it exits 2 naming what it did find.

A repo whose gate workflow has a different name passes `--expect-workflow <name>` (repeatable or comma-separated) before the SHA. Names match exactly and case-sensitively, so a comma or newline can never be part of an expected name. When the push event dropped the run, dispatch the missing workflow by hand, e.g. `gh workflow run ci.yml --ref <branch>`.

Transient gh or network errors mid-watch are retried (3 attempts with a short backoff) before the script concludes anything. Only a persistent failure exits 2.

The exit codes are ranked, not independent: a red run (exit 1) outranks a missing expected workflow, which outranks a gh error (both exit 2). A missing gate workflow plus a red bystander therefore exits 1, with the missing-workflow message still printed. Clear the red run, then watch again for the gate.

In this skill's home repository, a drift test (`tests/doc-drift.test.ts`) pins these citations (the invocation shape, the GraphQL discovery, the exit semantics, the expected-workflow gate, the superseded/FAIL/skip lines) to `scripts/watch-ci.sh`. A rename on either side fails CI until doc and script move together.

### 3. Report

- All green: one line ("CI passed: <workflow names>").
- Any failure: the failing workflow and job names, the log excerpt that shows the actual error, and the run URL. Excerpt, not the full log.

## After a Merge

A merge is a push to the mainline by other hands, and nothing above covers it by accident. After `gh pr merge`, `git rev-parse HEAD` in the checkout still names the TOPIC branch's tip, while the squash or merge commit is a new SHA that exists only on the mainline. A watcher started on the topic tip proves nothing about the merged pipeline.

With a merge queue, `gh pr merge` can return success on ENQUEUE, before the commits reach the mainline. Wait until the PR is actually merged (`mergedAt` set) before fetching, or the fetch grabs the pre-merge tip. Then resolve the mainline tip and run the same workflow (discovery, background watch, report) on that SHA:

```bash
git fetch <base-remote> <mainline>    # origin in a plain clone; in a fork checkout, the
#                                       canonical remote the PR merged into, never the fork
sha="$(git rev-parse FETCH_HEAD)"     # the merged mainline tip, not the topic HEAD
```

## Polling Budget

GitHub throttles in separate buckets. The core REST bucket is 5000 authenticated requests per hour per user. The Actions REST endpoints (`gh run list`, `gh run watch`, `gh run view`) are additionally throttled as a secondary bucket.

Ten sessions on one account locked that secondary bucket for over an hour with 403 "API rate limit exceeded" while core still read 5000/5000, and every REST-based CI verdict was blind. GraphQL has its own bucket and kept answering throughout. Earlier, `gh run watch` at its 3 s default refresh across parallel watchers drained core and blinded every verdict for 45 minutes.

Three rules follow:

- **Discover and poll through GraphQL, never the Actions REST endpoints.** The bundled scripts read every workflow run on the commit, with its status and conclusion, in one `gh api graphql` request per page of 100 check suites per poll, and touch REST only for failed-job logs (`gh run view <id> --log-failed`, once per failed run).
- **One CI poller per session at a time.** Queue the next push behind the running watcher. When the branch's runs share a `concurrency` group key, watch only the newest mainline tip instead: an older tip's watcher can end with no verdict to report (the group behavior is spelled out below).
- **The sustained poll interval is at least 60 s.** The bundled script sleeps 60 s between polls (`poll_interval=60`).

A hand-rolled watcher follows the same rules: discovery through the query in step 1, and never `gh run watch` at its 3 s default. A rate-limited GraphQL answer is tooling trouble (exit 2), never a reason to fall back to REST.

The script's two bounded bursts are not what the interval rule is about and stay as they are: registration polling (up to five reads 3 s apart, until the runs appear) and the transient-failure retries (up to three attempts 2 s apart) each spend a handful of requests once. The minutes-long watch is where the budget goes.

Stacked pushes also lose verdicts on GitHub's side. When a workflow's runs share a `concurrency` group key (commonly the workflow plus the branch), GitHub keeps at most one running plus one pending run per key.

A newer push cancels the pending run (and the running one too where `cancel-in-progress` evaluates true), so that SHA never gets a verdict, which the script reports as `FAIL(cancelled)` on a latest run. Two landings in one session needed reruns for exactly this. Wait for the running watcher's verdict before pushing again.

## Sleeping on PR Activity

Waiting for a review, a reply, or a merge after the push? Never poll the PR from the session: every poll spends tokens on "nothing changed yet".

Run the bundled waiter as a background shell command (same pattern as the CI watcher above) and act when it exits:

```bash
bun "<skill-dir>/scripts/wait-for-pr-event.mts" <pr-number> --repo <owner/name> > /tmp/pr-wait.out 2>&1
```

- `--until` picks the watched events from `comment,review,checks,merge` (default: `comment,review`).
- `--interval` sets seconds between polls (default 60, minimum 60: the Polling Budget floor above), but a failed poll retries after 2 seconds instead of waiting the full interval.
- `--timeout` sets seconds before giving up (default 1800).
- The waiter reads a complete baseline first, all through GraphQL, and exits 2 instead of waiting when that read fails. The baseline holds comment, thread-reply, and review-thread counts via `isResolved`, the latest review, per-check conclusions from the head commit's `statusCheckRollup` paged past 100 contexts, and merged state.
- At the deadline it makes one final bounded read, so the closing snapshot is current and a delta landing in the last window still exits 0.

| Exit | Meaning |
| --- | --- |
| 0 | a watched event happened; the output names it (`new review by <login>`, `unresolved threads 0 -> 2`, `check <name> -> failure`, merged) |
| 1 | the PR merged or closed while that outcome was not watched; the wait's job ended - on a merge, watch the mainline tip per "After a Merge" above |
| 2 | usage or tooling error (bad args, gh missing or failing); it never retries forever |
| 3 | timeout with no watched change; the baseline and final snapshots are in the output |

Worked example, babysitting a PR between review rounds:

```bash
bun "<skill-dir>/scripts/wait-for-pr-event.mts" 123 --until comment,review --timeout 3600 > /tmp/pr-123-wait.out 2>&1
# read /tmp/pr-123-wait.out when it exits:
#   exit 0 -> handle the named event (reply, fix, push, re-request review)
#   exit 1 -> the PR merged or closed; stop babysitting (a merge still gets the "After a Merge" watch above)
#   exit 3 -> no activity this hour; re-arm the waiter or escalate to the user
```

The drift test also pins this waiter's invocation, its `--until` set, and all four exit codes to `scripts/wait-for-pr-event.mts`.

## Fallback Without gh

- `gh` unavailable or unauthenticated: report the push and give the commit's checks URL (`https://github.com/<owner>/<repo>/commit/<sha>/checks`). Do not silently skip the watch.
- Non-GitHub CI: use that system's equivalent watch command. The rule is the same: background watcher, report pass/fail with failing logs.
