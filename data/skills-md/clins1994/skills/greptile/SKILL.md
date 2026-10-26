---
name: greptile
description: How to work with Greptile, the AI code reviewer - on a pull request (find its score and comments, tell whether it reviews each push or waits to be asked, ask for a re-review, wait for it, resolve its threads) and locally before a pull request (the greptile CLI). clins:address-reviews uses this skill as its Greptile reviewer. Use whenever you read, trigger, wait for or answer a Greptile review, or run a local Greptile review.
user-invocable: true
argument-hint: "[local [base-branch] | <PR number or URL>]"
---

# /clins:greptile — Work with Greptile reviews

[Greptile](https://www.greptile.com) reviews pull requests and leaves a confidence score (`X/5`) and inline comments. This skill knows where those live and how to drive them. It does not decide what to fix: [`clins:address-reviews`](../address-reviews/SKILL.md) runs the fix loop and calls this skill for the Greptile parts.

Run on its own:

- `/clins:greptile <PR>`: report the latest Greptile score and the open comments on that PR. Change nothing.
- `/clins:greptile local [base-branch]`: review the current branch with the Greptile CLI, before a pull request exists. See "Local review".

## Rules

- Never merge, approve or close a PR.
- Ask for a review only as "Triggering" says. Do not post a review request when Greptile already reviews every push by itself: each request is a paid review.
- The repo's `AGENTS.md`, `CLAUDE.md` and Greptile config win over this file.

## Who Greptile is

- REST author: `greptile-apps[bot]` (a staging install uses `greptile-apps-staging[bot]`).
- GraphQL author (`author.login` in review threads): `greptile-apps`, or `greptile-apps-staging` for a staging install.
- Check run: a name that matches `greptile` (case-insensitive).

## Where the score is

Greptile writes its summary in one of three places, depending on the install. Read all three and use the newest:

1. **Issue comments.** `gh api --paginate "repos/<owner>/<repo>/issues/<n>/comments?per_page=100"`. Greptile edits the same summary comment on every review, so sort by `updated_at`, not `created_at`. Read its "Prompt to fix all with AI" section too: it can list issues that have no inline comment.
2. **Reviews.** `gh api repos/<owner>/<repo>/pulls/<n>/reviews`, the newest from a Greptile author.
3. **The PR body.** `gh pr view <n> --json body -q .body`, in a block Greptile appends below the footer. The body has no `updated_at` of its own. Use the block's "Last reviewed commit" link to see which commit it is for, and its "Reviews (N)" count to see that it changed.

The score is the first `N/5` in that summary (`Confidence Score: 4/5`). A score belongs to a commit: check that it is for the current `headRefOid` (the review's `commit_id`, the check run's `head_sha`, or the PR body's "Last reviewed commit"). A score for an older commit is stale. When two places disagree, use the one for the current head, then the one with the newer review.

## Open comments

Review threads, paginated:

```bash
gh api graphql -f query='
query($owner:String!, $repo:String!, $number:Int!, $cursor:String) {
  repository(owner:$owner, name:$repo) {
    pullRequest(number:$number) {
      reviewThreads(first:100, after:$cursor) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id isResolved isOutdated
          comments(first:1) { nodes { databaseId author { login } body path line } }
        }
      }
    }
  }
}' -F owner=<owner> -F repo=<repo> -F number=<n> \
  --jq '.data.repository.pullRequest.reviewThreads | {pageInfo, threads: [.nodes[]
    | select(.isResolved | not)
    | {id, isOutdated, c: (.comments.nodes[0] | {databaseId, author: .author.login, path, line,
        body: (.body | split("<details>")[0] | .[0:2000])})}]}'
```

The `--jq` keeps only open threads, and cuts each comment before its first `<details>` block. Greptile puts large "Fix in ..." links and an AI prompt there: about 90% of a typical comment. To read one comment in full, fetch it alone: `gh api repos/<owner>/<repo>/pulls/comments/<databaseId> -q .body`.

Keep threads where the first comment's author is `greptile-apps` or `greptile-apps-staging`, and `isResolved` is false. While `hasNextPage` is true, run again with `-F cursor=<endCursor>`. `databaseId` is the id that `clins:github` needs to reply in the thread.

Resolve threads in one call:

```bash
gh api graphql -f query='mutation {
  t1: resolveReviewThread(input:{threadId:"ID1"}) { thread { isResolved } }
  t2: resolveReviewThread(input:{threadId:"ID2"}) { thread { isResolved } }
}'
```

## Triggering

Find out once per PR whether Greptile reviews each push by itself:

1. Read the repo's Greptile config if there is one (`greptile.json` or `.greptile/` at the root). It can turn reviews of new commits on or off.
2. If the config does not say, look at the history of this PR and the last 3 merged PRs. Leave out the first Greptile check run on each PR: Greptile often reviews a PR when it opens, also on installs that do not review later pushes. For each later check run, look for a Greptile request comment (`@greptileai` or `@greptile`) between the push of the run's commit and the start of the run. The run's `head_sha` is that commit. GitHub creates the commit's check suites when the commit is pushed, so the earliest one is the push time: `gh api repos/<owner>/<repo>/commits/<sha>/check-suites --jq '[.check_suites[].created_at] | min'`. Do not use the committer date: a commit can be made long before it is pushed. Do not use a fixed window either: a requested review can start minutes after the request.
   - Later runs with no request in that span: Greptile reviews on push.
   - Every later run has a request before it, and pushes with no request got no run: Greptile waits to be asked.
   - No later runs to look at: go to step 3.
3. If you still do not know, push, then wait up to 3 minutes for a Greptile check run on the new head. If one appears, Greptile reviews on push. If none appears, it waits to be asked.

A review request is a command to the bot, not a post: do not write it with `clins:post`. To ask for a review, first make sure that no Greptile check run is queued or running on the head (`gh pr checks <n> --json name,state`). Then:

- After a fix round: `gh pr comment <n> --body "@greptileai follow-up review"`. A follow-up review checks what changed since the last review. It usually closes a PR in one or two rounds.
- For a full new review (for example when the user asks): `gh pr comment <n> --body "@greptileai review"`. A full review reads the whole PR again and often finds new small issues, so loops that use it every round run to their cap.

## Waiting for a review

After a push or a review request, wait for a **new** Greptile check run to complete. When you ask for a review without a new commit, the review runs on the same head, and the check run that is already there is the old review.

If you did neither (no new commit, and no request because Greptile reviews on push), no new review is coming. Do not run the wait below: use the review for the current head. If its check run is still queued or running, wait for that run to complete.

Before you push or ask for a review, record the ids of the Greptile check runs on the head, and the summary's `updated_at` (for a summary in the PR body, its "Reviews (N)" count):

```bash
greptile_runs() {   # prints "<id> <status>" for each Greptile check run on commit $1
  gh api "repos/<owner>/<repo>/commits/$1/check-runs" \
    --jq '.check_runs[] | select(.name | test("greptile"; "i")) | "\(.id) \(.status)"'
}
OLD_SHA=$(gh pr view <n> -R <owner>/<repo> --json headRefOid -q .headRefOid)
greptile_runs "$OLD_SHA" | cut -d' ' -f1 > before.txt    # in a temporary folder
echo 0 >> before.txt                                      # so the list is never empty
```

Then push or ask, and wait until a check run on the head that is not in `before.txt` completes:

```bash
HEAD_SHA=$(gh pr view <n> -R <owner>/<repo> --json headRefOid -q .headRefOid)
for i in $(seq 1 60); do                       # 60 x 10 s = 10 minutes
  greptile_runs "$HEAD_SHA" | grep -v -w -F -f before.txt | grep -q ' completed$' \
    && echo done && break
  sleep 10
done
```

- This takes up to 10 minutes. Run it as a background command, or give the shell call a 600000 ms timeout. A default two-minute timeout stops it early and looks like a missing review.
- If it times out, stop and report. Do not read the score or comments as if a review had come: they are from the previous review.
- Read the summary only after it changed: a newer `updated_at` on the comment or review, or for a summary in the PR body, a higher "Reviews (N)" count. Greptile edits the summary after the check run ends. If it has not changed yet, wait one more minute and read again.

## Done

Greptile is done with a PR when the score for the current head is `5/5` and no Greptile thread is open.

## Local review

Review the current branch before you open a pull request. The CLI reviews **committed** changes on the branch against its base, so commit first. It never pushes.

1. `command -v greptile`. If it is missing, ask the user to install it (`npm i -g greptile`), and stop.
2. `greptile whoami`. If nobody is signed in, ask the user to run `greptile login` in a terminal (it opens a browser), and stop. Show the signed-in organization: the review runs against that organization's index of the code, so the wrong organization gives findings about other code. If the repo names its Greptile organization, check it.
3. Make sure that you are not on the base branch, and that the base branch exists (`git rev-parse --verify <base>`).
4. Run the review. Give the call a 600000 ms timeout. Resume an interrupted review first:

   ```bash
   OUT=greptile-review.json        # in a temporary folder, not the repo
   # `2>&1 1>"$OUT"` sends stderr to RESUME_ERR and stdout to the file. Do not change the order.
   RESUME_ERR=$(greptile review --resume --json --no-color 2>&1 1>"$OUT") \
     || greptile review --json --no-color >"$OUT"      # add -b <base> to both if given
   ```

5. The JSON has `comments[]` (`path`, `startLine`, `endLine`, `severity`, `category`, `body`) plus `summary` and `confidence`. If the command failed or the file is empty or not JSON, report the error (and `RESUME_ERR`). A failed review is not a clean review.
6. Report the findings, most severe first. To fix them in a loop, use `clins:address-reviews local`.
