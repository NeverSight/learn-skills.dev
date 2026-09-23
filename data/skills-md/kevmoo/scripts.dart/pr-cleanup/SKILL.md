---
name: pr-cleanup
description: >-
  Orchestrates multi-repo GitHub pull request, Gerrit CL, local Git worktree,
  and branch cleanup sweeps alongside active open-PR next-step triage. Use when
  asked to run a PR cleanup sweep, prune merged worktrees or branches, review
  open PRs and next steps across repositories, or reconcile local checkouts in
  ~/github against GitHub, Gerrit, and active Jetski sessions. Don't use for
  triaging inline review comments or CI failures on a single PR (use
  github-pr-triage or pr-loop), creating new worktrees (use new-worktree), or
  Google3 Piper CL triage (use cl-triage).
compatibility: "Requires kscripts (kevmoo_scripts via dart install) and local checkouts in ~/github"
metadata:
  author: kevmoo
  target_environment: personal
---

# PR & Worktree Cleanup Sweep (`pr-cleanup`)

> [!NOTE] This skill targets the personal repository layout (`~/github` and
> `~/github/kevmoo/*`) and invokes the unified `kscripts` AOT CLI.

## Quick Start & Prerequisites

Ensure `kscripts` is installed and up to date on `PATH`. If `kscripts` is
missing, install it from the canonical Git remote:

```bash
dart install 'kevmoo_scripts@{git: https://github.com/kevmoo/scripts.dart}'
```

Thereafter `upkeep update dart_install` keeps it current -- it re-reads the
source descriptor from the installed bundle's own `pubspec.lock` and reinstalls
from the same remote.

> [!WARNING] Do **not** run `dart install ~/github/kevmoo/scripts.dart`.
> Installing from a local path builds whatever branch that checkout is on, and
> it _replaces_ the `app-bundles/kevmoo_scripts/git/<sha>/` bundle with a
> `local/` one -- which permanently repoints `upkeep update dart_install` at
> that checkout instead of the remote. Only use a path install to test
> uncommitted work, and reinstall from Git afterwards.

## 1. Read-Only Pre-Flight Sweep (Always Start Read-Only)

Never pass `--apply` on the initial scan. Execute the 3 read-only collectors in
parallel to build a unified view of `~/github`:

1. **Merged/Closed PRs, Stale Worktrees & Dangling Remote Branches**:
   ```bash
   kscripts gh-clean -l 50 --markdown
   ```
2. **Open Active GitHub PRs & Reviewer/CI Next Steps**:
   ```bash
   kscripts gh-view -d 14 --markdown
   ```
   _(Omit `-d 14` if the user asks for all open PRs regardless of recency, or
   adjust `-d <days>` to match the user's window)._
3. **Dart SDK Gerrit Worktrees & CL Status** _(when `~/github/dart-sdk`
   exists)_:
   ```bash
   kscripts gerrit-view -p ~/github/dart-sdk
   ```
   _(Automatically resolves `~/github/dart-sdk/core/main/sdk` on bare-clone
   layouts and fetches Gerrit refs from `upstream` / `dart-googlesource`)._
4. **Open Assigned GitHub Issues** _(optional — run when asked for broader
   backlog/next-steps triage)_:
   ```bash
   kscripts gh-issues --linked-prs --markdown
   ```

## 2. Active Session & PM-OS Ownership Cross-Reference

Before proposing to delete any worktree, local branch, or unpushed commit:

1. **Inspect Dirty / Unpushed Worktrees**:
   - For any worktree flagged by `kscripts gh-clean` as having uncommitted
     changes or unpushed commits, run:
     ```bash
     git -C <worktree_path> status -s
     git -C <worktree_path> log -n 2 --oneline
     ```
   - **Squash-Merge Ancestry Check**: If a merged PR branch still reports
     unpushed commits past PR HEAD, fetch `origin/main` first and check whether
     the branch is an ancestor of `origin/main`:
     ```bash
     git -C <repo_path> fetch origin main --quiet
     git -C <repo_path> rev-list --count origin/main..<branch>
     ```
     If the count is `0`, the branch was reset onto the squash-merge commit and
     is safe to delete via `git -C <repo_path> branch -D <branch>`.
2. **Cross-Reference Active Jetski Conversations & PM-OS Tasks (Bounded
   Lookup)**:
   - Use the `grep_search` tool on `~/.gemini/jetski/annotations` (or run
     `pm-status pickup`) to identify active (`🟢` / `🧪`) or waiting (`⏳` /
     `🔔`) sessions. Do **not** run shell `grep` or unbounded scans across all
     `~/.gemini/jetski/brain/*/transcript.jsonl` files; only inspect
     `transcript.jsonl` for specific active/waiting conversation IDs when
     `.pbtxt` titles do not already identify the worktree.
   - If a worktree belongs to an **active (`🟢` / `🧪`)** sister session or an
     open PR/CL, classify it in **Bucket A (`🚫 DO NOT TOUCH`)**.
   - If a worktree belongs to a **waiting (`⏳` / `🔔`)** session whose PR/CL
     has already **merged**, include pruning its VCS state in **Bucket B** and
     queue an `agentapi send-message` wake-up to that sister session so it can
     verify follow-ups, docs, and PM-OS tasks before marking itself `--done`.

## 3. Three-Bucket Classification & Report

Present the findings in a structured Markdown report (or artifact for large
sweeps) divided into 3 buckets:

- **Bucket A — `🚫 Active / Hands-Off` (Open PRs, Active Gerrit CLs, In-Flight
  Worktrees)**:
  - List open PRs from `kscripts gh-view` and active Gerrit CLs from
    `kscripts gerrit-view` with their CI status, reviewer state (`⏳ Awaiting`
    vs `🔔 Ping Reviewer` vs `❌ Action Needed`), and local worktree mapping.
- **Bucket B — `✅ Safe to Prune Immediately` (Merged PRs/CLs & Clean
  Worktrees)**:
  - Clean worktrees (`git worktree remove`), merged local feature branches
    (`git branch -D`), dangling remote head branches on writable repos, and
    trunk fast-forwards (`--ff-only`).
  - List any waiting Jetski conversations whose PRs have landed so they can be
    messaged via `agentapi send-message` after VCS cleanup.
- **Bucket C — `⚠️ Requires Explicit Confirmation` (Closed-Unmerged PRs, Dirty
  Worktrees, Unpushed Experiments)**:
  - Detail the exact modified/untracked files (`git status -s`) or unmerged
    commits so the user can decide whether to discard or keep each item.

## 4. Approval Gate & Execution

Gate execution via `ask_question` with explicit bucket choices:

- `(Recommended) Execute Bucket B only (prune merged PRs, clean worktrees & remote branches)`
- `Execute Bucket B + Bucket C (also force-remove dirty/closed-unmerged worktrees)`
- `Stop here (keep read-only report only)`

Once approved:

1. **Execute Bucket B Pruning**:
   - If **any** merged-PR worktree was held back in **Bucket A** (because an
     active sister session is still using it), run
     `kscripts gh-clean -R <owner/repo> --apply` for each approved Bucket B
     repository individually so the Bucket A worktree is not touched.
   - Only run unscoped `kscripts gh-clean -l 50 --apply` when **zero** merged-PR
     worktrees were reclassified into Bucket A.
2. **Execute Bucket C Pruning** _(only if Bucket C was explicitly approved)_:
   - Run `git -C <parent_repo> worktree remove --force <worktree_path>` and
     `git -C <parent_repo> branch -D <branch>`.
3. **Message Waiting Sister Sessions (`agentapi send-message`)**:
   - Do **not** directly mark a waiting sister session `--done` from the
     `pr-cleanup` orchestrator. Instead, send a message
     (`agentapi send-message --title="PR Landed & Cleaned Up" <conversation_id> "..."`)
     informing the sister session that its PR landed and its local/remote
     worktree and branch were pruned, and instructing that session to
     double-check any needed follow-up, documentation/memory updates, or PM-OS
     tasks (`pm-work complete`) and then mark itself `--done`.
