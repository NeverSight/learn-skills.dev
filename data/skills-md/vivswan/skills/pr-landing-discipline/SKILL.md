---
name: pr-landing-discipline
description: Use when a review round lands on an open PR, when flipping its draft state, deciding who merges, or landing a change by PR merge or direct push.
license: SEE LICENSE IN LICENSE.md
metadata:
  author: Vivswan
---

# PR Landing Discipline

> A PR is live work until it lands. Draft while commits are pending, ready the moment it converges. Every review round triaged the cycle it appears, the line counts read against the stated purpose, and the merge left to a human by default.

These rules apply to any session that carries a change from "opened" to "landed": a PR through its review rounds to the merge, or a patch to a direct push.

"The author" below is whoever prepared the change, human or agent, working alone or in a multi-agent session. Writing the PR body or an issue is the `/pr-and-issue-discipline` skill's moment. This skill starts once the PR exists.

## When to Apply

- A review round just landed on an open PR
- A PR converges, or new commit-requiring work appears on a ready PR
- A change is about to land, by PR merge or direct push
- Deciding who merges a converged PR

## Draft Discipline

- **Open every PR as a DRAFT**, and keep it draft through its review loop.
- **Flip READY the moment it converges**: never batched, never held back. Flip only after the body re-read the `/pr-and-issue-discipline` skill defines, since the body was written at open and the diff has moved since.
- **Flip BACK TO DRAFT** the moment new commit-requiring work appears on a ready PR (a fresh valid review comment, a gate finding), before the fix round starts.
- **Draft state tracks pending commits.** CONVERGENCE gates the merge offer. A fresh comment needing only a reply does not bounce a ready PR back to draft, since its reply-and-resolve lands the same cycle, no commit. A PR is offered for merge only while the full converged definition below holds.

**Converged** means the review has converged as the `/rubber-duck-review` skill defines it (step 7 owns the single definition), plus the PR-specific bar: CI fully green and every review thread resolved (fixed or answered).

Fully green counts EVERY check on the PR, required or not, and on every PR in its dependency chain. A residue red from an un-retargeted base disqualifies ready even when the required gate passes.

READY also requires that nothing the PR publishes carries PII. The title, body, commit messages, added lines of the diff, and review, issue, and CI comments tell a reader nothing about who the author is, how they work, or how their machine is set up. The `/pr-and-issue-discipline` skill's redaction rule owns the definition, the substitutes, and the contract exception.

The grep below catches identifiers and the figures of a replaced real-data fixture. A quoted real configuration, log, or transcript is the review's read, and a blocking finding. The check reads all of it from the PR itself, never from local HEAD, and greps with a needle file of fixed strings:

- **The author's real identifiers**, one per line, every spelling the author has published under. The six below are placeholders for the name, employer, login, username, email, and machine name.
- **The provenance phrases** a real-data fixture carries (`measured from`, `real logs`).
- **When the PR replaces a fixture that was measured from real data:** every full-precision ratio and every integer of 4+ digits in the whole OLD file, so the old figures cannot ride into the new fixture, the body, or a comment.

The OLD file is read from the repository's API at the PR's merge base: the compare endpoint names it, and the contents endpoint serves the file there. So nothing is fetched locally, and a retained figure is a needle too.

```sh
n=<pr number>; out="$(mktemp)"; diff="$(mktemp)"; shas="$(mktemp)"; old="$(mktemp)"; needles="$(mktemp)"
fixture='<path/to/replaced-fixture.json>'   # only when a real-data fixture is being replaced; with none, drop this line and every line that uses $fixture, $mb, $old, or $head
printf '%s\n' 'Real Name' 'ExampleCorp' 'real-login' 'realuser' 'real.name@example.net' 'MacBook-Pro' 'measured from' 'real logs' > "$needles"
head="$(gh pr view "$n" --json headRefOid -q .headRefOid)" &&
mb="$(gh api "repos/{owner}/{repo}/compare/$(gh pr view "$n" --json baseRefOid -q .baseRefOid)...$head" -q .merge_base_commit.sha)" &&
gh api -H 'Accept: application/vnd.github.raw+json' "repos/{owner}/{repo}/contents/$fixture?ref=$mb" > "$old" &&
{ grep -oE '[0-9]+\.[0-9]{3,}|[0-9]{4,}' "$old" >> "$needles" || test $? -eq 1; } &&   # no distinctive figure in the old file adds no needles and is not a stop; exit 2 (a read error) is
gh api -H 'Accept: application/vnd.github.raw+json' "repos/{owner}/{repo}/contents/$fixture?ref=$head" > "$out" &&
gh api --paginate "repos/{owner}/{repo}/pulls/$n/commits" -q '.[].sha' > "$shas" &&
test "$(wc -l < "$shas")" -eq "$(gh api "repos/{owner}/{repo}/pulls/$n" -q .commits)" &&   # the listing stops at 250 commits; a short list is a stop, not a sample
xargs -I{} gh api -H 'Accept: application/vnd.github.diff' "repos/{owner}/{repo}/commits/{}" < "$shas" > "$diff" &&
{ gh pr view "$n" --json title,body -q '.title, .body' &&
  gh api --paginate "repos/{owner}/{repo}/pulls/$n/commits" -q '.[].commit.message' &&
  sed -n '/^+/p' "$diff" &&
  gh api --paginate "repos/{owner}/{repo}/pulls/$n/reviews" -q '.[].body' &&
  gh api --paginate "repos/{owner}/{repo}/pulls/$n/comments" -q '.[].body' &&
  gh api --paginate "repos/{owner}/{repo}/issues/$n/comments" -q '.[].body' &&
  xargs -I{} gh api --paginate "repos/{owner}/{repo}/commits/{}/comments" -q '.[].body' < "$shas"; } >> "$out" &&
  { grep -n -i -F -f "$needles" "$out"; echo "grep exit $?"; }
rm -f "$out" "$diff" "$shas" "$old" "$needles"
```

`grep exit 1` is clean. `grep exit 0` lists the hits, each read before it is called. The permitted matches are a product file name that carries a vendor's word, and the repository's own `owner/repo` coordinate in its install command.

A 4+ digit needle that coincides with a year, a sha fragment, or a port in an unrelated line is dismissed with that reading named. Every other hit is a blocking finding. A hit on a provenance phrase is a finding against the fixture it describes, whose fix is a hand-written fixture.

No `grep exit` line means a read failed somewhere in the chain, and the run says nothing about the PR. A wrong fixture path is a 404, and a cut-off read is a nonzero exit. A commit listing shorter than the PR's commit count fails its `test`, and `xargs` exits nonzero when any commit read fails.

An old fixture with no figure the fingerprint pattern matches adds no needles. The replacement is then read by eye against the old file, since the grep has nothing distinctive to look for.

What the block reads, and why:

- **Every commit's own added lines**, never only the net diff. A fixture added in one commit and deleted in the next is still published by the first, and a rebase or merge-commit landing keeps both. Added lines only, because the removed lines of a PR that redacts PII carry the PII by definition.
- **The whole new fixture at the PR head**, not just its changed lines. An old figure kept unchanged in the replacement is exactly the ride-through the fingerprints exist to catch.
- **Every comment: review, issue, and commit comments, CI comments included.** A CI comment that carries a figure derived from real data is a finding against the check that posted it, not only against the PR.

## Babysit to Comment Convergence

An open PR is live work until it merges. Bot reviewers (e.g. Copilot code review) and humans leave comments on every push. Per PR, loop until quiescent:

1. Every push gets a CI watcher (Companion Gates, below).
2. When a review lands, triage EVERY comment the same cycle it appears, never batched:
   - A valid finding is fixed in that same round.
   - An invalid or not-valid-here comment gets a reply stating why, and its thread resolved. A comment with nothing to answer (praise, a restated diff) is resolved without one.
3. Before the fix push, the body gets the per-round edit the `/pr-and-issue-discipline` skill defines: edit in place, overwrite counts, re-run the size check.
4. A fix push restarts the loop: new CI watch, re-gate on the changed content, and the bot may re-review.

**Bot comments are advisory.** A non-human reviewer (Copilot code review, any review bot) follows a repository's review instructions inconsistently, and many repositories have none. So the author runs each bot comment through the filter those instructions would have applied: comment only on a defect you can demonstrate.

- **Earns a fix:** the comment names a concrete input or state and the wrong output, crash, or data loss it produces in this diff. Fixed in the round.
- **Speculative hardening:** a hostile caller who cannot reach the code, "consider validating", "for robustness", a race in a single-user tool, a check for an input the code never receives. Declined in one sentence and recorded, not built (the `/rubber-duck-review` skill's step 6 carries the exception for repositories over 100 stars). A comment that names the input and the damage is the first bullet, whatever its wording.
- **Hand-rolls what a library does:** a comment that names the library and what it covers earns the replacement, per the `/code-standards` skill. A large library or an unclear fit goes to the owner as a question. A comment that names no library is the next bullet.
- **Style, naming, or structure opinions** the repository's linter and formatter do not enforce, and rewording that says the same thing: declined in one sentence. An opinion the linter already reports is resolved without a reply, since the red check carries it.
- **Restating the diff, praise, a summary:** resolved, no reply.

The one-sentence decline IS the thread's convergence. The bot's summary verdict ("Changes recommended") is not a gate, and the bot never substitutes for the blocking review under Companion Gates.

**Toil budget.** When rounds keep yielding one finding at a time (around ten rounds in), stop fixing instances one at a time. Enumerate the recurring finding classes, sweep each whole class across the change in one pass, then resume the loop. One 35-round convergence collapsed to a few batch sweeps once the finding classes were enumerated.

Read thread state via GraphQL, never from comment timestamps (a thread with no new comments can still be unresolved):

```text
reviewThreads(first: 100) { nodes { isResolved } pageInfo { hasNextPage endCursor } }
```

Paginate with `after: <endCursor>` while `hasNextPage` is true. A fixed first page is not the full set.

Bot reviews that do not fire automatically on drafts are requested explicitly (e.g. add Copilot as a reviewer on the draft, and prefer balanced or high reasoning where the repo exposes the setting). Requesting a Copilot review via the REST reviewers endpoint takes the reviewer login `Copilot`, exactly. `copilot-pull-request-reviewer[bot]` silently no-ops (a 201 response with empty `requested_reviewers`).

GraphQL `reviewRequests` hides a pending Copilot request either way, so the issue timeline is the only confirmation the request registered. Between rounds, never poll. Where the `/watch-ci-after-push` skill is installed, sleep on its `wait-for-pr-event` script, a background waiter whose exit wakes the session and names what changed.

Production shape of one round:

- "empty manifest passes vacuously": valid. Fixed with a regression test in the same cycle.
- "script not wired into the docs": sequencing by design. Replied with the plan (a docs pass wires all scripts post-merge) and resolved.
- "symlink following": split. The leaf-fidelity half was fixed after confirming it empirically, and the escape half was declined with the recorded design rationale.
- "verify the manifest's provenance before applying it" from Copilot, on a script with one caller inside CI reading a file the same workflow wrote: declined as speculative hardening. Replied in one sentence and resolved. The round's "Changes recommended" verdict held no merge.
- "add a regression test" on a deletion with no behavior of its own: declined. The comment named no fact the test would pin that the source does not say (the `/rubber-duck-review` skill's standing test question), and the body's census is the proof. Replied with the rule and resolved.

## Companion Gates

- **After every push, a background CI watcher.** Where installed, the `/watch-ci-after-push` skill defines it. A MERGE is watched the same way, on the mainline tip's SHA (fetch the mainline from the remote the PR merged into and watch `FETCH_HEAD`). After `gh pr merge`, `git rev-parse HEAD` still names the topic tip, and the squash or merge commit exists only on the mainline.
- **Before anything lands, an independent review that can block the landing.** It is scoped to the exact content being landed, never the working tree: the branch or PR diff (`base...HEAD`) once committed, the staged diff before that. Where installed, the `/rubber-duck-review` skill defines that review and its convergence.
- **Local runs before a push are targeted.** Typecheck plus the tests the change and its proof touch, with an explicit timeout on a long run, and a process stopped by the PID you spawned, never by pattern. The full suite and the lint-plus-build sweep are the CI watcher's to judge, never run locally when CI runs them anyway.
- **A personal private repository meters CI minutes**, so there the full check runs locally before the push instead. Not sure which kind it is, ask the user, or the lead when one briefed you.

## Line Accounting Before Landing

Before a change lands, the author reads its additions and deletions per kind of file and checks the sums against the change's stated purpose. The purpose is the title's type plus the body's first heading, or the commit subject's type when there is no PR.

The count is a signal, not the verdict. It catches the rewrite as large as what it replaced that every reviewer read as clean, and it asks why.

Whether the change is good is the judgment, and a good change lands whatever the count says. What it never does is land with the surprise unexplained.

```bash
git diff --cached --numstat                          # landing a still-uncommitted patch
git diff --numstat "<base-remote>/<base>...HEAD"     # a branch; the remote the PR merges into, never a fork remote
gh api --paginate "repos/<owner>/<repo>/pulls/<n>/files" --jq '.[] | "\(.additions)\t\(.deletions)\t\(.filename)"'   # an open or landed PR
```

Sum the rows per kind. The kinds are whatever the repository keeps apart: source, scripts, tests, docs, workflows, and generated files (lockfiles, snapshots, rendered output).

Generated files and binary rows (`-` in both columns) are named and left out of every sum. A rename row (`{old => new}`) counts only its edited lines, so leave rename detection on.

The TARGET below is the kind the purpose acts on: source for a library change, scripts for a script rewrite, workflows for a CI change. The rows are the usual shapes, read the way a reviewer would read them, not a law. A purpose that fits none is read on its own terms.

| Stated purpose | Expected shape | Asks why when |
| --- | --- | --- |
| Simplification, consolidation, retirement | target net negative; tests down only for the behavior removed | target net zero or up |
| Bug fix | target touched at the defect site; tests up by the regression case | target grows well past the defect site, or tests +0 |
| Feature | target and tests both up | tests +0 |
| Behavior-preserving refactor | existing tests pass unchanged (restructuring or strengthening them is fine) | an existing test now expects a different output: the behavior changed, so the purpose is misstated |
| Docs or contract change | only docs and contract files change | executable code changes |

Where a row says tests +0, naming the existing test that already covers the change answers it: a fix an existing assertion now pins, a feature an existing data-driven suite already exercises. Tests +0 on a deletion with no behavior of its own needs no words when the body carries the census (grep counts of the removed thing, before and after). The `/code-standards` skill's `references/tests.md` sets the census.

A test written so the row has something to show is the defect the count exists to catch, never an answer to it.

A mismatch is a question the author answers before the landing, not a stop. Either the change is trimmed, or it is judged good as it is and the growth is explained at whatever grain makes it checkable (per function for a rewrite, per file for a sweep).

More lines for a better change is a fine answer. "Cleaner" alone is not.

Two explanations recur, and each is checked rather than taken. One is a staged cutover whose deletion lands in a named sibling PR (the pair's sums are read together). The other is a guard or rule the purpose never stated (then the title is wrong: fix it, and the row it now falls under applies).

Where the sums go depends on what they say. A count that fits its row needs no words. If carried at all, it sits in the PR body's technical-details section.

A count that went against the purpose is part-one material. The reader's assumption (a consolidation shrinks) was wrong, so the sums and the reason stand in the human part where the user sees them, under the `/pr-and-issue-discipline` skill's Readability rules, and the user is told when the change is offered. With no PR, both go in the landing report.

```markdown
## Line accounting

- **Source +41 -12, tests +30 -0.** The consolidation grew source by 29: the merged entry point carries a guard the three old paths each skipped. The three paths themselves go with the sibling PR #N (-88), so the pair is net -59.
```

Production: a release-script rewrite retiring a build-branch chain deleted 18 functions and added 18, leaving the script the same size. The review read every replacement as clean. Only the count raised the question, and the answer was that nothing had been retired.

A pass over the 68 PRs landed around it, one `pulls/<n>/files` call each, found none the same size. It found four that grew by a guard no title mentioned or a deletion staged into a sibling PR.

## Who Merges

The human, by default. A PR exists to put a human gate before the mainline: the author prepares it (push, gates green, a "ready to merge" report) and the human merges.

Where a merge queue owns the ordering, the author's prepared action is enqueueing the converged PR. Enqueue is not merged, so watch until the commit actually lands. Two standing exceptions, each only when the user has granted it:

- **A trivial mechanical fix.** A change of a few lines that alters no behavior, flow, or procedure (a type narrowing, a typo, a rename with no semantic edge) merges directly once its gates are green. The human gate is reserved for changes worth human attention. When in doubt about "trivial", it is not trivial.
- **A pipeline blocked on a merge.** When a converged PR gates queued work and the human is not acting, merge it and say so in the next report. Waiting idle on a merge the author could perform is the defect, and the notification preserves the human's oversight.

**The `merge-when-green` label is the owner's standing approval on one PR, for that PR's whole life.** The repository owner applies it, never an agent, and no later push or force-push voids it. A PR without the label follows the rules above.

The label hands the operator the MERGE, not a verdict on the content. The owner agreed with the PR's idea and shape, at craft time or before, and may not have read the code. So the operator stands in for the owner on the exact head that lands:

- the head is converged as defined above
- its line accounting is read against the purpose (above)
- its body is re-read against the diff
- the gate review with blocking power ran on THIS head

Those checks are the same on every PR. The depth of reading is not: a typo fix gets a glance at the diff, and a rewrite of the release script gets the diff read end to end. The gates in this skill are the toolbox for that judgment, not a checklist the label unlocks. Two confirmations precede the merge:

```bash
head="$(gh pr view <n> --json headRefOid --jq .headRefOid)"   # first: a push after this fails the merge below
gh api --paginate "repos/<owner>/<repo>/issues/<n>/timeline" --jq '.[]
  | select((.event == "labeled" or .event == "unlabeled") and .label.name == "merge-when-green")
  | "\(.created_at) \(.event) \(.actor.login)"'
```

```text
1. the LAST line is a labeled event by the repository owner
   -> labeled by anyone else: remove the label, report who set it, the owner re-applies it
   -> unlabeled, or no line at all: no approval; the rules above apply
2. the operator's gate review ran on THIS head and its findings are triaged
   -> the head moved since the review: re-read head, re-review the head with the delta named, then merge
```

**Folding PRs and the label.** The approval covers the idea and shape the owner agreed to on THAT PR. Folding another PR into a labeled one brings in content the owner never agreed to.

So a label that predates the fold stays only when every PR folded in passes check 1 on its own timeline (an owner-set label, not merely a label). Otherwise the operator removes it, says so, and the owner re-applies after reading the folded content.

A label the owner set after the fold is that approval, whatever the folded PRs carried. A fresh combined PR starts unlabeled like any PR.

The PR's own review rounds (new commits on the same branch) are not a fold, so they keep the label. Prefer stacking or a fresh PR over folding into a labeled PR.

The operator removes the label in exactly two cases: set by someone other than the owner, or a fold that brought in unapproved content. A red check, an open thread, a gate finding, or a moved head never removes it. They hold the merge, not the approval.

Both confirmations hold and the head is converged: merge with `gh pr merge <n> --squash --match-head-commit "$head"`, so a push racing the merge fails it instead of landing, and report. Check 1 fails: the label comes off and the rules above apply. Check 2 or convergence fails: the finding is triaged under Draft Discipline (a commit-requiring finding flips the PR back to draft), the label stays, and the report says why.

**The landing action is exit-conditioned, never chained**, for a PR merge and a direct push alike. Read the gate's own verdict and STOP, landing in a separate command only after the gate itself reports green. Green means the gate's exit code AND its verdict, and a review gate is green only when its findings are triaged, not merely when its process exits 0.

```bash
tail gate.log; git merge && git push    # WRONG: the merge runs whatever the log said
tail gate.log && git merge && git push  # WRONG: && conditions on tail printing the log,
                                        # not on the gate's verdict; a red log still merges
```
