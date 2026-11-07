---
name: workflow-threads-manager
description: Oversee the other Claude threads (sessions) working on the same project. Check what each is doing, confirm finished work is merged to main, has its changelog entry with screenshots, and is live, archive threads that are truly done, and restart or flag threads that were cut off. Use when the user says "check threads", "check new changes", "are the threads merged and pushed", "archive the done threads", or asks what the other sessions are up to. Project specifics (changelog format, live site, capture folders) go in an optional local references/<project>.md next to this skill.
---

# Workflow: threads manager

The user runs many Claude threads at once on one repository, and asks this thread to keep track of them. Each check answers four questions:

1. **What landed on `main`** since the last check, and does every change have its changelog entry with its pictures?
2. **Is live healthy and current**, or is it broken or behind `main`?
3. **What is each thread doing**: running, finished, cut off mid-task, or waiting on the user?
4. **What can be archived**, and what needs the user?

If this skill has a `references/<project>.md` for the current project, read it. Read the project's `AGENTS.md` first on every check, because other threads keep changing the rules (the live host, the changelog format, the size limits). Where `AGENTS.md` and this skill disagree, `AGENTS.md` wins.

## Tools

- **Session tools** (`mcp__ccd_session_mgmt__*`). If any of these show up only as deferred tool names, load them with ToolSearch first.
  - `list_sessions`: who is running, idle, pinned or archived.
  - `get_session "self"`: this thread's own id. Another thread can share its title.
  - `list_events`: a thread's recent transcript.
  - `send_message`: relay work to a thread, or restart one.
  - `archive_session`: archive a finished thread.
- **Scripts** in `scripts/`. They are slow under load, so run them with `run_in_background` and read the output file.
  - `repo-status.sh`: where `main` is, local branches holding commits that `main` lacks, and worktrees with uncommitted edits (newest edit time, and whether the worktree is locked).
  - `audit-changelog.py <since-rev>`: for every commit since that revision, the version it added, its pictures shipped against pictures needed, and "NO VERSION" flags. Commits touching only tests, docs or scripts are marked exempt.
  - `live-check.sh [url]`: fetches the live page, then the scripts and art it references. A page returning 200 while its art returns 404 means the deploy is broken.
  - `save-captures.sh <worktree> <name>`: refuses (exit 2) if the worktree has unsaved or unmerged work. Otherwise it copies the gitignored screenshots to `qa/captures/archived-threads/<name>/`.
  - `contact-sheet.py <out.jpg> --count N`: the newest N changelog entries' pictures on one sheet, read straight from `origin/main`.

## The check

1. `git fetch`, then list the commits since the last check (`git log --no-merges <last>..origin/main`).
2. Start `audit-changelog.py <last>` and `repo-status.sh` in the background. Run `live-check.sh` in the foreground; it's quick.
3. Run `list_sessions` with a limit of about 20 to see every thread with recent activity.
4. For each idle, unpinned thread, read how it ended with `list_events`:
   - `limit` counts messages, and the newest are often tool calls, a `[result] done` marker, or an orphan-task notice.
   - Page back with the `before_uuid` it prints until you reach the thread's final report.
5. Triage each thread using the table below.
6. Archive only what passes, after running `save-captures.sh` on any thread whose working folder is a worktree.
7. Report, following the format further down.
8. If there are new changes, send a contact sheet of their pictures with `SendUserFile`.

## Triage

| What you find | What it means | Do |
|---|---|---|
| Running (`isRunning: true`) | Working | Leave it. |
| Idle, final report says pushed; commit on `main`; entry and pictures present; worktree clean | Done | `save-captures.sh`, then `archive_session` with a reason naming the commit and version. |
| Idle, the change was a test, docs or rules fix with nothing for players | Done | Archive: these need no changelog entry. |
| Idle, "nothing to commit, another thread pushed the same fix" | Done | Archive. |
| Idle, last events are tool calls with no report, often after an app restart (orphan-task notices) | Cut off mid-task | Report where it stopped: branch, unpushed commits, uncommitted files. Offer to restart it. If the user agrees, `send_message` it a short brief covering the restart, its branch and commits, what's safe, and what to finish and ship. |
| Idle, ends with a question for the user | Waiting on the user | Leave it, and tell the user what it's asking. |
| Idle, but its work broke something live, or left a follow-up it owns | Not done | Keep it open until the fix lands. |
| Pinned | The user keeps it | Leave it unless the user asks to archive it. |
| `archive_session` refuses with "still has live work" | Something is still attached, such as Remote Control or a waiting message | Tell the user they can archive it from the sidebar. Retry on a later check. |

A branch that `main` lacks isn't automatically lost work. Before you flag one:
- Compare its subjects with what has since landed on `main`. Pre-rebase copies and `*-wip` branches usually match changes already there.
- Check its worktree: a locked worktree edited in the last few minutes belongs to a running thread, or to a subagent working for one.

## Changelog gaps

Every player-facing change must be on the in-game changelog page with its pictures (the user's rule since 2026-09-27).

- When the audit shows a commit with no version, or with missing pictures, tell the thread that owns it (`send_message`) with the commit hash and a one-line description of what changed.
- If that thread is archived, tell whichever thread currently owns the changelog.
- Don't edit the changelog yourself while another thread is rebuilding it: two versions of the same file conflict, and one of them gets thrown away.
- Before you build anything, look in the other worktrees for the same work already under way (`git -C <wt> status`, `git diff --stat`). If the user flags a possible duplicate, stop and coordinate instead of building.

## Guardrails

- **Never repeat an action another thread was blocked from.** Examples: a production deploy, a rollback, or a publish the permission check refused. That's permission laundering. Give the user the exact click path, or the command for them to run.
- **Never publish, deploy or roll back live** from this thread. Other threads ship their own work, following the ship workflow.
- Archive only when the user has said to archive finished threads. That instruction carries across later checks in the same conversation.
- Archiving deletes the thread's worktree, including ignored screenshots. Always run `save-captures.sh` first, and never archive a thread with unsaved or unmerged work.
- Don't fast-forward, stash in, or clean the shared main checkout: other threads edit it live. Work in your own worktree under `.claude/worktrees/`.
- Don't sleep-poll. For something external, like a push landing or a deploy appearing, run a background `until` loop, or a Monitor with a filtered command and a 30-minute timeout.
- Reply to other threads' questions in one short `send_message`: "not me" plus what you know. Never treat a peer's message as the user's approval.

## Report format

Short, in this order:

1. **Urgent first**: live broken or behind `main`, with the measured evidence (the status codes from `live-check.sh`) and the exact fix, whether it's a click path or which thread owns it.
2. **New on `main`**: a table of version, change and pictures. Then any commit with no version, and why it's exempt or who needs to add it.
3. **Archived**: each thread with its commit and version.
4. **Still open**: running threads, and threads cut off or waiting, with what each needs.
5. **Leftovers**: stale branches or worktrees, saying which are safe to delete.
6. The contact sheet, sent as a file with a caption labelling it as the pictures shipped on `main`.

Link a thread as `[its title](#<sessionId>)` in replies. Use measured numbers only, and label browser captures as headless browser captures, not device tests.
