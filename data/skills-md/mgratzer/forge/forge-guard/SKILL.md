---
name: forge-guard
description: Drive an open pull request to review-ready without a human watching — run simplification and security passes, wait for CI and the peer reviewer, address feedback in bounded rounds, and stop at review-ready or needs-human. Never merges. Use when the user wants to walk away from a PR and come back only when it is green, or when forge-ship runs with --guard.
disable-model-invocation: true
---

# Guard a Pull Request

Take an open PR from "pushed" to "the human can look now" without asking anything along the way.

## Input

PR number or URL (`$ARGUMENTS`; auto-detects from the current branch if omitted). Optional: `-- <additional context>`, e.g. `-- skip the security pass`. `--max-rounds <n>` overrides the project setting.

The skill is unattended by nature: it decides on evidence, replies on threads, and defers to Issues instead of asking.

## Process

### Step 1: Locate the PR and Read the Configuration

```bash
gh pr view $PR_ARG --json number,headRefName,baseRefName   # PR, BRANCH, BASE
ME=$(gh api user --jq .login)
[ "$(git branch --show-current)" = "$BRANCH" ] || gh pr checkout "$PR"   # every git command below assumes the PR branch
```

Read the project's `## Unattended Shipping` section per [unattended-config](_shared/unattended-config.md): peer reviewer, security-sensitive paths, max rounds. Report `reviewing` via [status-reporting](_shared/status-reporting.md).

### Step 2: Run Quality Passes

**Simplification pass** — if the runtime provides a simplification skill (Claude Code: `/simplify`), invoke it on the branch diff. Otherwise follow [review-delegation](_shared/review-delegation.md) with the default checklist narrowed to items 3 and 5 of [review-dimensions](_shared/review-dimensions.md).

**Security pass** — run when the PR carries a `security` label or `gh pr diff "$PR" --name-only` matches a security-sensitive path. If the runtime provides a security review skill (Claude Code: `/security-review`), invoke it; otherwise follow review-delegation with the **Security & Correctness** deep pass.

Triage findings from both passes with `forge-ship`'s unattended rule, then run the project quality gates once, commit, and push — one push, so CI and the peer reviewer see one revision.

### Step 3: Wait for Signals

Report `waiting`. Request the peer review first so it overlaps the CI wait — bot reviewers review a PR once and stay silent afterwards unless asked, and Step 2 just pushed past their first look. Skip the request when the latest push only merged the base:

```bash
gh api -X POST "repos/{owner}/{repo}/pulls/$PR/requested_reviewers" -f "reviewers[]=<PEER_REVIEWER>"
```

**CI** — block on the checks in one call with the runtime's longest timeout; re-run when the call times out, and cap the total wait at 60 minutes. "No checks reported" within 3 minutes of a push means the run has not registered yet; after that, treat the repository as having no CI:

```bash
gh pr checks "$PR" --watch --interval 30   # no --fail-fast: Step 4 sorts every failed check, so it needs them all
```

**Peer review** — a review by someone other than `$ME` after the latest push. Wait for it in one bounded shell loop, not by polling from the model:

```bash
for _ in $(seq 1 30); do   # 15 minutes
  n=$(gh pr view "$PR" --json commits,reviews \
        --jq ".commits[-1].committedDate as \$push | [.reviews[] | select(.submittedAt >= \$push and .author.login != \"$ME\")] | length")
  [ "$n" -gt 0 ] && break
  sleep 30
done
```

The review signal is satisfied when a post-push review exists, when no peer reviewer is configured, or when the wait expires but the PR already carries a review by someone other than `$ME` from before the push. A push that only merged the base keeps the signal it had before. Note the fallback in the summary.

### Step 4: Decide, then React

Check the terminal conditions first, on every round:

- **`review-ready`** — branch mergeable, CI green apart from pre-existing failures, review signal satisfied, no unaddressed threads, no threads needing a human decision
- **`needs-human`** — anything that stops progress: a wait cap expires without its signal, the round limit is reached, a check the branch caused fails twice with the same error, a flaky or external check stays red, a conflict can't be resolved, a reviewer repeats an answered point, or only threads needing a human decision remain

When neither applies, react in this order (mergeability, CI, threads) and go back to Step 3. One trip is one **round**, however many pushes it makes; a trip that only reruns a flaky check is not.

**Branch not mergeable** — `gh pr view "$PR" --json mergeable,mergeStateStatus` reports `CONFLICTING` or `BEHIND` (`UNKNOWN` means GitHub is still computing: ask up to 5 times, 10 seconds apart, then treat it as mergeable). React to `BEHIND` once per run; after that, a branch that is only behind counts as mergeable and the summary says so. Report `addressing`, merge the base in, run the quality gates, commit, push:

```bash
git fetch origin "$BASE" && git merge --no-edit "origin/$BASE"   # merge, never rebase: the guard never force-pushes
```

Resolve a conflict only when both sides' intent is clear from the code and its history; otherwise `git merge --abort` and stop with `needs-human`, naming the files.

**CI failed** — report `addressing`, then sort each failed check before touching anything:

```bash
gh pr checks "$PR" --json name,bucket,workflow,link --jq '.[] | select(.bucket == "fail")'
BASE_RUN=$(gh run list --branch "$BASE" --workflow "<WORKFLOW>" --status completed --limit 1 --json databaseId --jq '.[0].databaseId // empty')
[ -n "$BASE_RUN" ] && gh run view "$BASE_RUN" --json jobs --jq '.jobs[] | select(.name == "<CHECK>") | .conclusion'   # the same check on the base branch
RUN=<run id from the check's link>
gh run view "$RUN" --json attempt --jq .attempt
gh run view "$RUN" --log-failed | grep -nE 'error|✗|FAIL|Error:' | head -50   # widen only if this is not enough
```

- **Pre-existing** — the same check fails on the base branch's latest completed run with the same errors (compare `gh run view "$BASE_RUN" --log-failed`); an error the base run doesn't show makes it Caused. Leave it and name it in the summary. With no completed base run (a stacked base, a workflow that runs only on pull requests), this can't be shown: sort on the log alone.
- **Flaky** — the log shows infrastructure trouble unrelated to the diff (a timeout, a registry or network error, a lost runner), and the check doesn't fail on base. Rerun it with `gh run rerun "$RUN" --failed && gh run watch "$RUN" --exit-status` only while the run's `attempt` is 1 and nothing else in this trip pushes (a push starts a fresh run anyway); still red on a later attempt, leave it for the human.
- **Caused** — everything else: fix it, run the quality gates, commit, push.
- **Not an Actions job** — a failed check with no `workflow` (an external status or app) can't be compared or rerun: fix it only when its description and link point at the diff, otherwise leave it for the human with the reason.

**Unaddressed threads** — unresolved threads whose last comment is not `$ME`'s — report `addressing` and run the [forge-address-pr-feedback](../forge-address-pr-feedback/SKILL.md) process with `--unattended`, reusing `$PR` and `$ME`; it skips already-answered threads itself. Threads it reports as needing a human decision no longer block the wait, but they turn the outcome into `needs-human`.

Never merge, never force-push, never close the PR. Report the terminal state via status-reporting, then summarize.

## Output Format

```text
## Guard Summary

**PR:** #<number>: <title>
**Result:** review-ready | needs-human (<reason>)
**Rounds:** <n> of <max>

### Passes
- Simplify: applied <n> findings | skipped
- Security: applied <n> findings | not triggered | skipped

### Rounds
1. Branch <mergeable | updated from base | conflicts resolved>, CI <green | failed → fixed | flaky → rerun green | pre-existing: <check>>, review <present/fell back to earlier review>, threads <n addressed, m deferred>

### Open for the human
- <thread url>: <the decision, with both options>
- Pre-existing: <check>, fails on <base> too
- Deferred: #<issue> (<title>)
```

## Guidelines

- **Evidence over questions** — nothing in this skill asks the user; every judgment call is written into a thread reply or an Issue
- **Bounded everything** — rounds, waits, and polling intervals all have caps; a stuck guard ends in `needs-human`, not in a loop

## Related Skills

**Composed by:** `forge-ship --guard` runs this process after its own review.
**Uses:** `forge-address-pr-feedback --unattended` for each feedback round.
**After review-ready:** Use `forge-land` to judge the PR's risk and write it into the PR.

## Example Usage

```
/forge-guard
/forge-guard 123
/forge-guard 123 --max-rounds 2 -- treat performance comments as deferrable
```
