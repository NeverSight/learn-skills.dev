---
name: address-pr-comments
description: Address a GitHub pull request's review comments and failing checks with the gh CLI. Fixes broken checks at the source; for every comment either fixes it (commit, push, reply citing the commit) or rebuts it in its own thread, then resolves the conversation. Use when asked to address, handle, answer or resolve PR comments, review feedback or failing PR checks.
---

# Address PR comments

Work through one pull request until every check is green and every comment is
answered and resolved. Run autonomously: triage, fix, push, reply and resolve
without pausing for approval.

## Rules

- **Reply where the comment lives.** A review thread gets a reply in that
  thread. A top-level comment or review summary gets its own quote-reply. Each
  comment gets its own reply; the PR body and any all-in-one summary comment
  stay untouched.
- **Every comment ends answered and closed:** threads resolved, top-level
  comments and review summaries minimized as `RESOLVED`.
- **Fix the source.** A red check turns green because the code, test or config
  is now correct. Skipping or deleting tests, `--no-verify`, `continue-on-error`,
  loosened lint rules, lowered thresholds and blindly regenerated snapshots are
  not fixes.
- **Push fast-forward only** to the PR's head branch. Never force-push.
- **Replies are short and specific:** what changed, or why not, with evidence.
  No filler, no thanks-for-the-catch.
- Prefer `gh` subcommands; use `gh api` / `gh api graphql` where `gh` has no
  subcommand (threads, replies, resolve, minimize). Write reply bodies to a
  file and pass them with `-F body=@file` so Markdown survives the shell.

## 1. Find the PR

With a PR number or URL from the user, use it. Otherwise ask `gh` for the PR of
the current branch:

```bash
gh pr view [<number>] --json number,url,state,headRefName,headRefOid,isCrossRepository,maintainerCanModify
```

`no pull requests found for branch` means there is none: ask the user for the
PR number. Owner and repo come from the URL
(`https://github.com/<owner>/<repo>/pull/<number>`); comments live on that
repository even when the head branch is in a fork. A PR that is not `OPEN`,
or a fork PR with `maintainerCanModify: false` that you did not author, cannot
take pushes: stop and tell the user.

Done when number, owner and repo are known and the PR accepts pushes.

## 2. Check out the head

`git status --porcelain` must be empty; uncommitted changes belong to the user,
so stop and ask if it is not. Then:

```bash
gh pr checkout <number>
git pull --ff-only
```

Done when `git rev-parse HEAD` equals `headRefOid`.

## 3. Build the inventory

Who you are: `gh api user --jq .login` (the *viewer*).

**Checks.** `gh pr checks <number> --json name,state,bucket,link,workflow`.
The command exits non-zero while checks fail (1) or are pending (8); read the
JSON regardless. Every `bucket: "fail"` goes in the inventory. Pending checks
are caught by step 8. `no checks reported on the '<branch>' branch` (no JSON)
means the repository runs no checks on this PR.

**Review threads.** Unresolved threads, skipping threads where every comment is
the viewer's:

```bash
gh api graphql --paginate -F owner=<owner> -F repo=<repo> -F number=<number> -f query='
query($owner: String!, $repo: String!, $number: Int!, $endCursor: String) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $number) {
      reviewThreads(first: 50, after: $endCursor) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id isResolved isOutdated viewerCanReply viewerCanResolve path line
          comments(first: 50) { nodes { author { login } body url } }
        }
      }
    }
  }
}' --jq '.data.repository.pullRequest.reviewThreads.nodes[] | select(.isResolved | not)'
```

**Top-level comments and review summaries.** Not minimized, not the viewer's,
non-empty body:

```bash
gh api graphql -F owner=<owner> -F repo=<repo> -F number=<number> -f query='
query($owner: String!, $repo: String!, $number: Int!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $number) {
      comments(first: 100) { nodes { id author { login } body url isMinimized } }
      reviews(first: 100) { nodes { id author { login } state body url isMinimized } }
    }
  }
}'
```

If a PR has more than 100 of either, page that connection with `after:`.

Read each thread in full: the ask is the latest unanswered request in it.
Comments that ask for nothing (approvals, praise, bot status reports, review
overviews) need no reply; record them as *informational*.

Done when every failing check and every comment has an inventory entry: id,
kind (check, thread, top-level, review), author, location and the ask.

## 4. Fix failing checks

For each failing check, get the failure from its `link`:

- `.../actions/runs/<run>/job/<job>`:
  `gh run view --job <job> --log-failed`.
- `.../runs/<check-run-id>` (a non-Actions app):
  `gh api repos/<owner>/<repo>/check-runs/<check-run-id> --jq .output`.

Find the command the check runs (`.github/workflows/`, Makefile, package
scripts), reproduce the failure locally, fix the cause and rerun the command
until it passes. A failure whose cause lies outside the repository (runner
outage, expired secret, flaky network) gets one `gh run rerun <run> --failed`;
if it fails again, record it for the report. Commit each check's fix
separately.

Done when every failing check either passes locally or is recorded as external.

## 5. Triage each comment: fix or rebut

Read the code the comment points at, at the current head (threads marked
`isOutdated` may already be fixed: then the outcome is *fix*, citing the commit
that fixed it).

- **Fix** when the comment is right: a bug, a missing case, a clearer name, a
  repo convention, a cheap and correct nit. A ```` ```suggestion ```` block is
  applied as written unless it is wrong.
- **Rebut** when it is wrong or does not belong in this PR: the code already
  handles it, it contradicts the repo's conventions or another reviewer, it is
  out of scope (name the follow-up), or the trade-off was deliberate. Questions
  get answered on this path too. Every rebuttal carries evidence: a permalink to
  the line, a test, a doc or a measurement.

Done when every non-informational comment is marked fix or rebut with a
one-line reason.

## 6. Fix and push

One commit per comment fixed; comments asking for the same change share a
commit. For each: make the change, run the tests and linters that cover it,
then commit with a message in the repository's style (`git log --oneline -20`)
that says what changed, not "address review".

```bash
git push
```

A rejected push means the branch moved: `git pull --rebase`, rerun the tests,
push again. Rebasing rewrites SHAs, so read the final ones after the push
succeeds: `git log --format='%H %s' -n <commits you made>`.

Done when the push succeeded and every fixed comment maps to a pushed full SHA.

## 7. Reply and resolve

Write each reply to a file, then post it.

- **Fix:** `Fixed in <full SHA>: <what changed>.` GitHub links the SHA.
- **Rebut:** the position and its evidence, in one to four sentences.

**Review thread:** reply in the thread, then resolve it.

```bash
gh api graphql -f threadId=<thread id> -F body=@reply.md -f query='
mutation($threadId: ID!, $body: String!) {
  addPullRequestReviewThreadReply(input: {pullRequestReviewThreadId: $threadId, body: $body}) {
    comment { url }
  }
}'
gh api graphql -f threadId=<thread id> -f query='
mutation($threadId: ID!) {
  resolveReviewThread(input: {threadId: $threadId}) { thread { isResolved } }
}'
```

**Top-level comment or review summary:** post a quote-reply that starts with
the quoted ask, the author's handle and a link to the original, then minimize
the original as resolved.

```markdown
> <the sentence being answered>

@<author> ([comment](<original url>)): <reply>
```

```bash
gh pr comment <number> --body-file reply.md
gh api graphql -f id=<comment or review node id> -f query='
mutation($id: ID!) {
  minimizeComment(input: {subjectId: $id, classifier: RESOLVED}) {
    minimizedComment { isMinimized }
  }
}'
```

A permission error on resolve or minimize (`viewerCanResolve: false`, or no
triage access) leaves the reply in place; record it for the report.

Done when rerunning step 3's queries returns no unresolved thread and no
unminimized comment other than informational ones and recorded permission
failures.

## 8. Watch checks

```bash
gh pr checks <number> --watch --fail-fast
```

With no checks reported in step 3, there is nothing to watch: skip this step.
Otherwise, right after a push the new head may report no checks yet; wait ten
seconds and retry. On a failure, run step 4 for it, push, and watch again. Stop
after three rounds of fixes.

Done when every check passes, or three rounds are spent.

## 9. Report

Tell the user, in chat, not on the PR:

- each comment: author, location, outcome (fixed in `<short SHA>`, or rebutted
  with the one-line reason);
- each check: final state, and the fix commit if it was red;
- anything left open: external check failures, permission failures, checks
  still red after three rounds, and informational comments that got no reply.
