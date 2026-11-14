---
name: merge-council
description: Run a merge council on a pull request only when the user, a task, or repository guidance explicitly asks for a merge council. Convenes the council skill's members on the PR, returns a merge verdict bound to the reviewed commits, and on the user's own open PRs fixes and pushes the findings every member agreed on.
---

# Merge Council

Run only on an explicit request for a merge council. A general request to review a PR belongs to other review skills.

A merge council is the `council` skill applied to one pull request, with two additions: a verdict tied to the reviewed commits, and fixes the members agree on. Requires the `council` skill; if it is missing, stop and say so. Use its member lineup and its Convene section to launch members.

The members decide. You coordinate: you freeze the subject, brief the members, pool their answers, and apply the rules below exactly. You never settle a finding, a remedy, or a vote yourself. Council's Synthesize step does not apply; this skill's verdict rules replace it.

## 1. Prepare

1. Resolve the PR URL: the argument, or `gh pr view --json url` for the current branch. If there is no PR, stop and say so. Pass the full URL to every `gh` command.
2. Use a checkout whose remotes include the PR's base repository: one the user named, the current checkout, or a clone at `${TMPDIR:-/tmp}/merge-council/clones/<owner>-<repo>`.
3. Choose the mode. **Fix mode** applies when the PR author is `gh api user --jq .login`, the PR is open, and `gh api repos/<head owner>/<head repo> --jq .permissions.push` is true. Every other case is **read-only**; record the reason.
4. Freeze the **subject**: fetch the PR head and base, and record the repository, PR number, head ref, head SHA, base ref, base SHA, and merge base. The head SHA must equal the PR's `headRefOid`. For an open PR, the base SHA is the fetched base ref's tip. For a merged PR, it is the first parent of the PR's merge commit; without a merge commit, the run is incomplete.
5. Create the run directory `${TMPDIR:-/tmp}/merge-council/<runId>/`, where `runId` is `mc-<pr>-<short head SHA>-<UTC timestamp>`, and a detached review worktree at the head SHA inside it. Install dependencies there with the repository's frozen-lockfile install; record a failure as a limitation. Afterwards, `git status --porcelain --untracked-files=no` in the worktree must print nothing; if the install changed tracked files, the run is incomplete.
6. List **changed instruction files**: names in `git diff --name-only <mergeBase> <headSha>` that are `AGENTS.md`, `CLAUDE.md`, or `CLAUDE.local.md` at any depth, or under `.claude/` or `.codex/`. A PR that changes one can steer its own reviewers.
7. Find a **prior run**: a record path the user names, otherwise the newest `${TMPDIR:-/tmp}/merge-council/*/record.json` for this repository and PR whose verdict is not `APPROVE`. Carry every finding it did not reject into the briefs, with its resolution and each ID prefixed `P-`, and record the user's decisions on them in the user's own words, keyed by the prefixed ID.

## 2. Review

1. **Round 1.** Launch every member in parallel with the review brief from [member brief](references/member-brief.md). Members are read-only and see only their brief.
2. **Round 2.** Pool the findings, group duplicates, and give each group a neutral ID (`F-1`, `F-2`, ...) so no ID reveals its author; keep the mapping to member IDs in the record. Send every member the reconciliation brief. Skip it only when every member raised the same findings with the same remedy, blocking class, and eligibility; then record `agree` on all four questions for every member, and the round 1 votes are the final votes.
3. A member attempt **fails** when it errors, reports a different `HEAD`, returns malformed JSON, or runs past 20 minutes, after you cancel it and confirm it stopped. Retry once; a successful retry replaces the failed attempt, and a second failure makes that member `ABSTAIN`. When the host reports that a member ran with a different model or effort than its target, the run is incomplete.
4. The run limit is 120 minutes. At the limit, cancel active work, start no fix, and finish with an incomplete record.

Give each finding exactly one status from the round 2 answers:

- **Agreed:** every member answers `agree` on the claim, remedy, and blocking class.
- **Rejected:** every member answers `disagree` on the claim.
- **Contested:** everything else, including a split vote.

## 3. Fix (fix mode only)

A finding is **fixable** when it is agreed, its eligibility is `eligible`, and every member answered `agree` on that eligibility. Send the fixable findings to the Routine implementer from the user's delegation policy, or the host's general-purpose agent, with the [fixer brief](references/fixer-brief.md).

- **Pushed:** the new head is a new subject. Keep the run ID, run directory, worktree, and push count. Repeat Prepare steps 4 and 6 for the new head, confirm the worktree's `HEAD` is that head, carry this run's findings as prior findings, and run the review again on the whole PR.
- **Not pushed:** stop fixing and record why.

Allow at most two pushes per run.

## 4. Verdict

Fetch the head and base again, then apply the first rule that matches:

1. **`NEEDS_HUMAN`** when the run is incomplete; a member abstained or did not meet coverage; a blocking finding is contested; an agreed blocking finding needs the user's decision; a fix was not pushed; the head or base moved without a council push; the PR changes an instruction file; or the review diff is empty.
2. **`CHANGES_REQUESTED`** when an agreed blocking finding is still open.
3. **`APPROVE`** when every member's final vote is `APPROVE` and no blocking finding is open.
4. **`NEEDS_HUMAN`** otherwise.

Non-blocking findings never prevent `APPROVE`.

## 5. Record and report

Write `<run dir>/record.json`, then remove the review worktree and leave the run directory:

```json
{
  "runId": "mc-182-1a2b3c4-20261109T1830Z",
  "previousRunId": null,
  "status": "complete | incomplete",
  "verdict": "APPROVE | CHANGES_REQUESTED | NEEDS_HUMAN",
  "mode": "fix | read-only",
  "subject": { "repo": "owner/name", "pr": 182, "headRef": "branch", "headSha": "", "baseRef": "main", "baseSha": "", "mergeBaseSha": "" },
  "members": [ { "name": "Astra", "model": "gpt-6-astra", "effort": "high", "vote": "APPROVE", "coverageMet": true } ],
  "findings": [ { "id": "F-1", "memberIds": { "Astra": "2" }, "status": "agreed | contested | rejected", "blocking": true, "eligibility": "eligible", "claim": "", "evidence": "path:line", "remedy": "", "dissent": "each member's reason for any disagree answer", "resolution": "fixed:<sha> | resolved | decided | open | needs-decision | closed" } ],
  "userDecisions": { "P-F-1": "the user's words" },
  "fixCommits": [ { "sha": "", "findings": ["F-1"] } ],
  "changedInstructionFiles": [],
  "ci": "pass | fail | pending | none",
  "limitations": []
}
```

`resolution` is `resolved` for a prior finding every member found resolved, `decided` for a finding the user decided that no member reopened, `needs-decision` for an agreed finding that is not fixable and has no such decision, `closed` for a rejected finding, and `open` otherwise. `status` is `incomplete` when a member abstained after its retry, or the run stopped early; an incomplete record always means `NEEDS_HUMAN`.

Then report:

```md
**Merge council: <VERDICT>.** <"Ready to merge." or the single main reason it is not>
<repo>#<pr> at `<short head>` · CI <state> · <n>/<members> approve<" · fixes pushed: <short sha>" when any>

**Before merging**
- **<id>** <what is wrong> (`<path:line>`). <the remedy, or the decision the user must make>

**Worth a look**
- **<id>** <non-blocking finding> (`<path:line>`)

Record: `<run dir>/record.json`
```

Omit **Before merging** on `APPROVE`. List at most three items under **Worth a look**.

## 6. Act

Before acting on `APPROVE`, confirm that the PR's head and base SHAs still match the record and CI passes. Where repository guidance allows merging on council approval, merge with `gh pr merge <PR URL> --match-head-commit <headSha>`. Otherwise report that the PR is ready. On any other verdict, the **Before merging** items are the hand-off; a later run on this PR continues from this record.
