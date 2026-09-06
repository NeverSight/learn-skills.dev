---
name: git-shortcuts
description: >
  Translates shorthand git/GitHub workflow commands into the correct sequence of actions.
  ALWAYS trigger when the user's message contains a "--" prefixed shorthand like:
  "--c", "--p", "--cp", "--pr", "--prm", "--cppr", "--cpprm", "--ff", "--release", "--pub", "--close" — with or without a trailing "?".
  The "--" prefix is required — do NOT trigger on bare letters like "c" or "pr" appearing in normal sentences.
  NEVER invoke this skill autonomously — it MUST always be user-invoked via an explicit "--" shorthand in their message.
---

# Git Shortcuts

> **SAFEGUARD: This skill must NEVER be invoked autonomously by the assistant. It is exclusively user-invoked — only run when the user explicitly types a `--` prefixed shorthand (e.g. `--cp`, `--cppr`) in their message. The assistant must never decide on its own to call this skill.**

Map each letter to an action and execute them in sequence.

## Branch model

Trunk-based: `ticket → main`, or `ticket → epic/<name> → main` when a feature spans several tickets. Merging into the trunk ships **nothing** — `--release` does that.

**First, check the repo has migrated.** A repo that still has a `staging` branch runs the old one-directional model and none of the rules below apply to it:

```bash
git ls-remote --exit-code --heads origin staging > /dev/null 2>&1 && echo LEGACY
```

`LEGACY` → tell the user, then read `LEGACY-STAGING.md` next to this file and follow it instead. Never silently target the trunk in such a repo.

**Base branch: never hardcode it.** Prefer the repo's own helper when it has one:

```bash
branch=$(git symbolic-ref --short HEAD)
trunk=$(git symbolic-ref --short refs/remotes/origin/HEAD 2> /dev/null | sed 's|^origin/||')
trunk=${trunk:-main}

if [ -f .agents/hooks/lib/branch-name.sh ]; then
  . .agents/hooks/lib/branch-name.sh
  base=$(branch_base "$branch")
else
  base=$(git config "branch.${branch}.laicaBase" 2> /dev/null)
  case "$base" in
    epic/*) git rev-parse --verify --quiet "refs/remotes/origin/$base" > /dev/null || base=$trunk ;;
    *) base=$trunk ;;
  esac
fi
```

`$trunk` is the repo's default branch — `main` everywhere so far, but read, not assumed. `$base` is what `pr` targets: the trunk, or the epic the ticket was cut from.

A wrong base produces a *smaller* diff, and a small diff is what a review reports as clean — so an `epic/*` base that cannot be verified on `origin` falls back to the trunk. Never the other way round.

## Shorthand map

| Letter | Action                                                                                                                             |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------- |
| `c`    | Commit — invoke the `/commit` skill (stage relevant files, write a conventional commit message, create the commit)                 |
| `p`    | Push — `git push origin <current-branch>`                                                                                          |
| `pr`   | Create PR — `gh pr create` following the PR creation protocol (title + body, `--base "$base"`)                                     |
| `m`    | Merge — `gh pr merge --squash`, **except** an `epic/*` branch merging into the trunk, which uses `gh pr merge --merge`. Nothing more — do NOT add `--delete-branch`. Then offer a Slack summary (see below) |

Squash is right for a ticket branch: it dies after merge. An epic merges with a merge commit — squashing would collapse the per-ticket commits that were the reason to open an epic, and release-please reads those commit messages to build the changelog.

## Rules

- **Never delete branches.** Do not pass `--delete-branch` to any `gh` command. Do not run `git branch -d` or `git push origin --delete`. If a tool or command would delete a branch, skip that flag or step entirely. GitHub deletes the remote head branch itself on merge (`delete_branch_on_merge`) — that is the repo setting doing it, not you, and it is not a reason to start passing the flag.
- Execute steps in the order they appear in the shorthand (left to right).
- If a step fails, stop and report — don't continue to the next step.
- For `c`: follow the full commit protocol, but **scope the staged files to only the work done in this conversation**. Derive the relevant file set from the conversation context — which files were read, edited, or created during this session. Run `git status` to see everything dirty, then stage only the files that belong to this task. If there are other dirty files unrelated to the current task (e.g. from parallel agent sessions), leave them unstaged. If you're unsure whether a file is in scope, exclude it and mention it. Never use `git add .` or `git add -A`. Before staging, output a scoping summary in this exact format:

  ```
  In scope:
  • src/foo/bar.ts
  • src/foo/baz.ts

  Excluded:
  • src/other/thing.ts  (reason)
  ```

## Valid combinations

All inputs must be prefixed with `--`.

| Input     | Steps                                                                            |
| --------- | -------------------------------------------------------------------------------- |
| `--c`     | commit                                                                           |
| `--p`     | push                                                                             |
| `--cp`    | commit → push                                                                    |
| `--pr`    | create PR                                                                        |
| `--prm`   | create PR → merge                                                                |
| `--cppr`  | commit → push → create PR                                                        |
| `--cpprm` | commit → push → create PR → merge                                                |
| `--ff`    | fast-forward the current branch from its remote (see below)                      |
| `--release` | ship the open release PR (see below). `--pub` is the old name and does the same thing |
| `--close` | dispose of the current worktree — teardown + remove (see below). No-op under Superset |

Other combinations (e.g. `--m` alone) are unusual — ask the user to confirm before proceeding.

## Slack summary after merge

After every successful `m` (merge):

1. **Resolve the author's Slack user ID:**
   - Check if `SLACK_USER_ID` is set in the environment (`echo $SLACK_USER_ID`).
   - If not set: ask the user "Was ist dein Slack-Handle? (z.B. `tim`)" → call `mcp__slack__lookup_user_by_email` or `mcp__slack__users_lookupByUsername` to resolve to a user ID → then ask "Soll ich die ID als `SLACK_USER_ID=<id>` in `.env` speichern?" If yes, append the line to `.env`.

2. Fetch the merged PR details: `gh pr view --json title,url,body`

3. Compose a one-liner (see below), then show it as a preview:

   > Slack #dev: @tim: repo-name -> PostHog läuft jetzt via Reverse Proxy unter `/_s` — kein Adblocker-Problem mehr. <PR-URL>
   > Posten?

4. If yes: post via `mcp__slack__post_message` with `channel: "#dev"`, using `<@USER_ID>` for the mention so Slack renders it as a clickable @-mention. If no: skip silently.

5. **Wait for the user's response to step 3/4, then stop.** The merge is finished. Do not offer `--close` or any other follow-up — nothing needs cleaning up after a merge.

**Message format:** `<@USER_ID>: <repo-name> -> <one-liner> <PR-URL>`

**Composing the one-liner:** One sentence, present tense, German. Lead with what changed in practice, not the commit type. Append the PR URL after the sentence (not embedded). No bullet points, no emoji unless the PR clearly calls for celebration.

**Example:**

- PR title: `feat: add reverse proxy for PostHog`
- Body: routes `/_s` to PostHog, avoids adblockers
- → `<@U0123ABCD>: colin -> PostHog läuft jetzt via Reverse Proxy unter /_s — kein Adblocker-Problem mehr. https://github.com/…`

## The `--ff` command

Fast-forwards the current branch to its remote counterpart: `git pull --ff-only`.

- No upstream configured → `git fetch origin`, then `git merge --ff-only origin/<branch>` if that ref exists. Missing on origin → report and stop.
- Fast-forward not possible (local and remote diverged) → git aborts on its own; report the divergence and stop. **Never** fall back to a merge or rebase to force it through.
- Uncommitted changes are fine — git refuses the update only if they collide; then report and stop.
- Touches no other branches, ships nothing.

## The `--release` command

Ships whatever has been merged into the trunk since the last release. `--pub` is the old name for it and behaves identically.

The skill does not compute a version, create a tag, or merge branches. release-please keeps one release PR open against the trunk and rewrites it on every merge; this command reviews that PR and merges it. Merging it runs the repo's release workflow, which tags, migrates production and deploys.

No branch guard — can be run from any branch.

**Preflight** — find the release workflow: `wf=$(grep -rl release-please .github/workflows/ 2> /dev/null | head -1)`. Empty → this repo has no release automation. Stop and report that merging to the trunk is all there is here. **Never tag or deploy by hand.**

**Steps:**

1. **Find the release PR** — `gh pr list --base "$trunk" --state open --label "autorelease: pending" --json number,title,url,headRefName`
   - Not found → stop and report: "Kein offener Release-PR. Es wurde seit dem letzten Release nichts nach `<trunk>` gemerged, oder release-please läuft noch — prüf die Actions."
   - **Never create it by hand.** A hand-made PR carries no version bump and no changelog.

2. **Show what would ship** — `gh pr diff <number> -- CHANGELOG.md` and print the new version from the PR title. Ask: "Release `<version>` mit diesen Änderungen veröffentlichen?" Wait for the answer.

3. **Check mergeability** — `gh pr view <number> --json mergeable,mergeStateStatus`
   - `MERGEABLE` → proceed.
   - `CONFLICTING` → stop and report. Do not resolve conflicts in a release PR by hand — release-please regenerates it; fix the cause on the trunk instead.
   - `UNKNOWN` → re-poll up to 3 times (5 s apart). If still `UNKNOWN`, report and stop.

4. **Squash merge** — `gh pr merge <number> --squash`

5. **Watch the run this merge created.** `gh run list --limit 1` still returns the *previous* release run until the new one is queued, and watching that one reports a stale success. Pin the run to the merge commit:

   ```bash
   sha=$(gh pr view <number> --json mergeCommit --jq '.mergeCommit.oid')
   for _ in $(seq 12); do
     id=$(gh run list --workflow="$(basename "$wf")" --json databaseId,headSha \
            --jq ".[] | select(.headSha==\"$sha\") | .databaseId" | head -1)
     [ -n "$id" ] && break
     sleep 10
   done
   [ -n "$id" ] && gh run watch "$id" || echo "Kein Release-Run für $sha nach 2 min — prüf die Actions."
   ```

   Report the outcome. If the deploy step failed after the tag was created, tell the user the repair path: Actions → the release workflow → Run workflow → enter the tag.

6. **Slack summary** — same protocol as after `m` (see above), with the version in the one-liner.

7. **Deploy annotation** — if the repo annotates deploys in its analytics, remind the user: `[DEPLOY] <tag>` per the repo's analytics conventions.

## The `--close` command

Disposes of the current worktree: stops its dev servers, releases its database branch, removes the directory. What it has to do depends on who owns the worktree — **check that first**.

1. **Not a worktree?** If the main checkout is the current directory (`git rev-parse --git-common-dir` resolves inside it), there is nothing to close. Report and stop.

2. **Superset-owned worktree — do nothing.** The path lives under `~/.superset/worktrees/`. Superset runs `.superset/teardown.sh` and removes the worktree when the session closes, so `--close` has no work left. Report that and stop.

   Only exception: the user wants the database branch released *now* while keeping the session open → run the repo's teardown script (`bash scripts/teardown.sh` — always exits 0, safe to run twice) and leave the directory alone.

3. **Anywhere else — one command, run from the main checkout:**

   ```bash
   cd "$(git rev-parse --path-format=absolute --git-common-dir)/.." && yarn wt:remove <worktree-path>
   ```

   `worktree-remove.sh` already chains both halves: it runs `teardown.sh` inside the worktree, then `git worktree remove`. Do not call `teardown.sh` separately first.

**The repo has to provide those scripts.** Check before running — `git grep -q '"wt:remove"' -- package.json`, or `test -f scripts/worktree-remove.sh` in a repo without `package.json`. Missing → **stop and hand the user the setup template in `WORKTREE-SETUP.md` next to this file.** Do not improvise a bare `git worktree remove`: it skips teardown and leaks whatever the worktree held — running dev servers, an undropped database branch.

Two things to get right:

- **Run it from the main checkout, not from inside the worktree.** The command deletes the directory it is pointed at; standing in that directory leaves the shell with no working directory and every later command fails.
- **`--close` ends the session's work.** Nothing can run afterwards — the working tree is gone. Finish everything else first, report, and treat it as the last action.

`git worktree remove` refuses a worktree with uncommitted changes. Commit or discard them first; do **not** reach for `--force`, which throws the work away.

**It touches no branches.** Nothing to delete — GitHub removes the remote branch on merge (`delete_branch_on_merge`), and the local branch goes with the worktree.

**Never offer `--close` unprompted.** It is not a step in any workflow — only run it when the user types it. Merging a PR does not call for it.

**If the branch was an `epic/*`** — its database branch is shared and outlives the worktree, so teardown leaves it alone. Offer: "Neon-Branch `epic/<name>` auch löschen? (`yarn neon branches delete epic/<name>`)". It has no TTL, so nothing removes it on its own. Wait for the answer.

## The `?` modifier

Appending `?` to the end of any shorthand replaces the **last action** with an inspection instead of execution. All preceding steps in the chain still run normally.

`?` can only appear at the very end — `--cp?r` is invalid.

| Last action | `?` behaviour                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `c`         | Show uncommitted changes: run `git status` and `git diff --stat`, summarise what would be staged and committed. Do not commit.                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `p`         | No-op — nothing useful to show beyond what the commit message already says. Skip silently.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `pr`        | Check whether a PR is open for the current branch (`gh pr view --json state,mergeable,url`) and report its status and merge-readiness. Do not create a PR.                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `m`         | Report the PR's merge state instead of merging: `gh pr view --json state,mergeable,mergeStateStatus,baseRefName` plus the merge method that would be used (`--squash`, or `--merge` for an epic into the trunk). Do **not** poll Vercel — a merge deploys nothing.                                                                                                                                                                                                                                                                                    |
| `ff`        | Report how far the branch is behind/ahead of its remote without updating: `git fetch origin`, then `git rev-list --left-right --count <branch>...origin/<branch>`. Say whether a fast-forward is possible. Do not pull.                                                                                                                                                                                                                                                                                          |
| `release`   | Inspect the open release PR: version, changelog diff, `mergeable` status. Do not merge. `--pub?` is the same command.                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `close`     | Report what would be disposed: the worktree path, whether Superset owns it, uncommitted changes, and whether the repo provides `wt:remove`. Remove nothing.                                                                                                                                                                                                                                                                                                                                                                                                    |

**Examples:**

- `--c?` → summarise uncommitted changes
- `--cp?` → commit, then skip (p? is a no-op)
- `--cppr?` → commit → push → inspect PR status (don't create)
- `--cpprm?` → commit → push → create PR → report merge readiness (don't merge)
- `--ff?` → show how far behind the remote the branch is (don't pull)
- `--release?` → show what the next release would contain
- `--close?` → show what closing would tear down

