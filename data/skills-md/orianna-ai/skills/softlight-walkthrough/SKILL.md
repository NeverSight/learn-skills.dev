---
name: softlight-walkthrough
description: >-
  Use right after you open or push to a pull request in a repository Softlight reviews
  (softlight[bot] comments on its PRs), even if you were only asked to "put up a PR". Opening the PR
  is not the end of the task. Run the script's --watch in the background and tell the user when the
  walkthrough is ready (its direct /demo/... link), each issue a check finds, and when the review is
  complete, even if the PR merges mid-review. The user is whoever you report your work to: the
  person you're talking with, or another session your instructions name, such as a driver or
  orchestrator. Also use it instead of building, running or screenshotting the app when someone asks
  to see or demo a PR's change, or asks for its walkthrough, Softlight video, share or demo link, or
  what Softlight found. Only ever share the app.softlight.com/demo/... link it returns, never an
  app.softlight.com/api/softlight/walkthrough/... or /v/... waiting page, even when Softlight's own
  PR comment links one. Takes a PR URL, owner/repo#number, or a bare number in the current checkout.
---

# softlight-walkthrough

Softlight reviews each pull request: it films a walkthrough of the change, publishes it on a share
page, `https://app.softlight.com/demo/<owner>/<repo>/pr<number>/<token>`, and then runs checks on
it, one by one, on each device (desktop, tablet, phone). The token is random, so look the link up
with `get_walkthrough.sh` in this skill's directory; never build it yourself.

**Only ever give the user the `/demo/...` link.** Softlight also has a waiting page for every PR
(`app.softlight.com/api/softlight/walkthrough/...`, or a signed `app.softlight.com/v/...` link to it
from the PR's check). Never pass either on, even when Softlight's own PR comment, check or a PR
event links one ("Softlight has started its design review: ..."). Say the review has started and the
walkthrough link is coming. Paste the link bare, on its own line, not in code formatting.

## Who "the user" is

In this skill, "the user" is whoever you report your work to:

- If a person gave you the task, the user is that person. Reply in your conversation with them.
- If your instructions say to report to another session, such as a train driver, an orchestrator or
  a parent agent, the user is that session. Send every update there the same way you send your
  report, for example with the same `conductor message create --session <id>` command.

In the second case, nobody reads your own chat. A link you write only there reaches no one.

## What to do

| Situation                                                     | Do                                                                                |
| ------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| You just opened or pushed to a PR, or were asked to follow it | [Watch the review](#watch-the-review) in the background.                          |
| Someone wants to see a PR's change, or asks for its link      | Run `get_walkthrough.sh <pr>` and hand over the link it prints.                   |
| You pushed again while a watch on that PR is still running    | Leave it running: it follows the review onto the new commit. Don't start another. |

`<pr>` is `https://github.com/acme/web/pull/123`, `acme/web#123`, or `123` inside a checkout of
`acme/web`.

## Watch the review

The walkthrough is published about five minutes after a push; the checks take half an hour or more
after that. Never run the watch in the foreground: it would hold the user's turn until it returns.

1. Start `<skill dir>/get_walkthrough.sh --watch <pr>` so each line it prints reaches you as it's
   printed. In Claude Code that's the Monitor tool. Act on each line as it arrives (table below);
   don't wait for the next one.
2. Without waiting on it, tell the user now: give the PR link, and say you'll send the walkthrough
   link when it's ready and report what Softlight finds. If you report to another session, this is
   your usual report. Send it now; don't hold it for the link.
3. When it exits, act on its `complete:` line, or on its stderr ([When it ends](#when-it-ends)).

It prints one event per line:

```text
ready: https://app.softlight.com/demo/acme/web/pr123/AbCdEfGhIjKl
commit: 1a2b3c4
issue: P1 desktop — Removing a coupon — Checkout total doesn't update after removing a coupon (on 1a2b3c4)
issue: P2 phone — Removing a coupon — The coupon field is hidden behind the keyboard (on 1a2b3c4)
commit: 9f8e7d6
issue: P1 phone — Opening an empty cart — Empty cart shows a blank page (on 9f8e7d6)
complete: 1 issue found, 17 of 18 checks passed (2 not offered on a device, counted as passed) (on 9f8e7d6)
```

| Line                                                       | Means                                             | Tell the user                                                                                               |
| ---------------------------------------------------------- | ------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| `ready: <url>`                                             | The walkthrough is published.                     | It's ready, with the URL on its own line.                                                                   |
| `commit: <sha>`                                            | The review is checking `<sha>`.                   | Nothing the first time. After a push: Softlight has moved on to the new commit.                             |
| `issue: [level ][device ]— <check>[ — <issue>] (on <sha>)` | A check found an issue on that device and commit. | The issue (lead with it; `<check>` is what Softlight was trying), device, level (`P0` is worst) and commit. |
| `complete: <...> (on <sha>)`                               | The review is over.                               | It's complete, how many issues and checks passed on that commit, and the link again.                        |

Each issue is printed once per commit, check and device; a page that films one device leaves the
device out.

### Reporting what it finds

- **Read the commit off the line; never guess it.** The watch never reports a result the page still
  shows from an earlier commit as the current one's.
  - An issue on a commit you've since pushed past is about the old code. Say so, and wait for the
    newer commit's result before calling it fixed.
  - An issue on your newest commit is about the code as it is now, even if it looks like one you
    already fixed: the fix didn't hold, or caused it. Say so and look at it again.
- **Group issues that share a cause** (one check failing on several devices, or several checks
  failing on one device for one reason) and say which devices each is on: a phone-only issue usually
  needs a different fix.
- **Check the `complete:` count before you relay it**, against Softlight's own list of issues (the
  PR description, or its summary comment): the number of issues should match. The checks passed are
  counted as on the share page's score, one result per check and device, and a check a device
  doesn't offer counts as passed there. The PR description's `N/M UX checks passed` leaves those
  out, so it is lower by the "not offered" number in the `complete:` line; that difference is
  expected, so don't report it. If the issues disagree, report Softlight's numbers and its list of
  issues, and say the watch's count was off. An undercount reads as "the rest is fine".

### When the PR merges mid-review

A merge doesn't end the watch, even when the PR-activity system unsubscribes you: that covers CI and
review comments, not Softlight. Leave the watch running. The walkthrough is meant to be watched
after merging, and its findings become follow-ups on shipped code: report them as such, offer a
follow-up PR for the ones worth fixing, and say if the merge cut the checks short.

## When it ends

Exit `0` means success: the link on stdout, or with `--watch`, a `complete:` line. Exit `1` means
there's no walkthrough or result (yet); stderr is one line, `<state>: <why>`:

| State                           | Means                                                         | Do                                                                                                                         |
| ------------------------------- | ------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| `queued`, `indexing`, `running` | The video or the review isn't done yet (or the wait ran out). | Say it's on its way and offer to keep watching. Never hand over a waiting page instead. Don't restart a watch on your own. |
| `stopped`                       | The review ended without finishing its checks.                | Say so in its words, with what it found before then.                                                                       |
| `merged`                        | The PR merged before the video was finished: no walkthrough.  | Same as `none`.                                                                                                            |
| `none`                          | Softlight didn't film this PR.                                | Say nothing unless the user asked to see the change; then say there's no walkthrough.                                      |
| `video_only`                    | The video is in the PR description; there's no share page.    | Point the user to the PR description.                                                                                      |
| `unknown`                       | Softlight couldn't say just now.                              | Run it again in a few seconds.                                                                                             |

Exit `2` means bad input, a PR Softlight can't see (the app isn't installed, or the repository is
behind Softlight sign-in), or Softlight unreachable; stderr says which. For a repository behind
sign-in, tell the user to open the PR's Softlight check from a browser signed in to Softlight.

## Reference

```bash
<skill dir>/get_walkthrough.sh <pr>              # the link if it's published, else exit 1 at once
<skill dir>/get_walkthrough.sh --wait <pr>       # poll for the link, up to 15 minutes (--wait=SECONDS)
<skill dir>/get_walkthrough.sh --watch <pr>      # follow the review, up to an hour (--watch=SECONDS)
```

The script needs `curl`, `jq` and `awk`, and also reads the PR's checks with `gh` when it's signed
in.

**If nothing you have streams a command's output line by line**, use two background runs that tell
you when they exit, such as a background subagent told to run the command and return only its exit
code, stdout and stderr: first `--wait <pr>` (hand over the link as soon as it returns), then
`--watch <pr>` (report its issues and completion together when it exits). If you can't run anything
in the background, run the script once without flags: give the link if it's ready, else say the
video is still being made and offer to fetch it later.

**Without the script**, read the link from either of these:

1. The PR's Softlight check run (`Softlight Review`, or `Softlight video · ...`): once the video is
   published, its `details_url` is the `/demo/...` link (`gh pr checks <n> --repo <owner>/<repo>`,
   or the GitHub MCP `pull_request_read` with `method: get_check_runs`). Before that it's a `/v/...`
   waiting link; don't give that out.
2. `curl -sS https://app.softlight.com/api/softlight/walkthrough/<owner>/<repo>/<number>/status`
   returns `{"state": "ready", "url": "https://app.softlight.com/demo/...", ...}` once published;
   any other state is one in the table above. A `401` means the repository is behind sign-in.
