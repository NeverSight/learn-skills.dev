---
name: cleanup-merged-branches
description: Delete remote branches whose PR was merged. Read-only dry-run, then confirm, then delete.
disable-model-invocation: true
---

Delete remote branches that belong to a **merged** PR. Destructive, so it runs as a **dry-run** first and never deletes without explicit confirmation.

## Delete rule

A branch is deletable iff **all** hold — encoded in `scripts/plan.sh`, the single source of truth:

- it still exists on the remote,
- it has a merged PR,
- it has no open PR,
- it is not **protected**.

**Protected** = the default branch + `staging`. Never delete these, even if a merged PR points at them. A branch with no PR, or only a closed-unmerged PR, is not deletable (it never "belongs to a merged PR"). Extend the protected set in `is_protected()` inside `scripts/plan.sh`, nowhere else.

## Steps

1. **Dry-run.** Run `bash scripts/plan.sh` (pass a remote name as `$1` if not `origin`). It prints deletable branches as `<branch>  #<pr>  <title>`, and deletes nothing. Done when you have the list. Empty output → report "nothing to clean up" and stop.
2. **Show + confirm.** Show the full list to the user and ask for explicit go. Do not delete on a vague reply — only on a clear yes. This gate is mandatory every run.
3. **Delete.** For each confirmed branch: `git push origin --delete <branch>`. Nothing outside the plan's list may be deleted.
4. **Report.** List what was deleted; note any push that failed.

## Also: stale claims (the reaper)

Releases *abandoned* `in-progress` claims (agent crashed / session died / no PR ever opened) so a dead claim doesn't pin an issue as "taken" forever. See `docs/agents/triage-labels.md` for the label; `/implement` sets it, PR-open removes it, this reaps the leftovers.

**Stale rule.** An `in-progress` issue is stale iff **all** hold — encoded in `scripts/stale-claims.sh`, the single source of truth:

- it is open and labeled `in-progress`,
- it has **no open linked PR** (linked = an open PR referencing `#N` in title/body, or whose head branch == the branch named in the claim comment), and
- the `in-progress` label is older than the threshold (latest `labeled` timeline event): default **24h**, override via `$1`/`$STALE_CLAIM_HOURS`.

**Steps** (fold into the same run, on the same confirm gate as branch deletion):

1. **Dry-run.** Run `bash scripts/stale-claims.sh [hours]`. It prints stale claims as `#<n>  <title>` and changes nothing. Empty → nothing to reap. (Logic proof: `bash scripts/stale-claims.test.sh`.)
2. **Show + confirm.** Show the list; reap only on explicit go. Same mandatory gate.
3. **Reap.** For each confirmed issue: `gh issue edit N --remove-label in-progress --add-label ready-for-agent` (abandoned work re-enters the free queue). Nothing outside the printed list is touched.

## Also: stale-open issues

`Closes #N` only auto-closes on merge into the **default** branch — a PR merged into an integration branch (e.g. `rebuild/v1`) leaves #N open forever. For each merged PR you clean up here, check its linked issue: if the work is on the default branch but the issue is still open, hand-close it (`gh issue close #N --reason completed --comment "merged via #<pr>"`). Same misfire hides "done" issues as open — this is where to catch them.
