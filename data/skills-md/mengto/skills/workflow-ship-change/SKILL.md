---
name: workflow-ship-change
description: Ship every change the way the user requires, with the guardrails. Take screenshots of the start, the key moment and the result; give the change its own changelog version with pictures; verify with tests; commit only your own files; merge with the latest main and push as a fast-forward; publish that exact main live; confirm each step; and report measured sizes, asking before any upload over 50 MB. Use at the end of every change (feature, fix, tweak, art, balance, polish) and whenever the user says "ship it", "commit", "push", "merge", "publish", "deploy", "go live" or "update the changelog". Project specifics (hosting, the changelog pipeline, merge conflicts) go in an optional local references/<project>.md next to this skill.
---

# Workflow: ship a change

A change is **done** only when all of these are true, and the report shows each one:

1. **Screenshots** of the real rendered game: the start state, the key moment and the result. They're shown inline in the report.
2. **Its own changelog version**, with its pictures on the in-game changelog page.
3. **Verified**:
   - your own tests;
   - the tests of commits you merged in;
   - the asset checks;
   - the full suite, run on the pushed commit.
4. **Committed**: one cohesive commit, with only your own files staged.
5. **Pushed** to `main` as a fast-forward, and confirmed on GitHub.
6. **Live**: the build of that exact `main` is published, and confirmed working on the real domain.
7. **Measured**: the sizes of the commit, the push, any upload and the publish, all measured, never estimated.

Pushing and publishing are standing authorizations for the project's own repository and live site. So don't ask before them, **except** where a guardrail below says stop. Read the project's `AGENTS.md` before starting, and this skill's `references/<project>.md` if there is one. Project rules change often, and wherever they differ from this skill, they win.

## Guardrails: stop and ask the user

- **Any upload over 50 MB.** That covers a git push, a Netlify deploy, a media release, and files sent to any outside service.
  - Measure first (`upload-size.sh`, or the pack size `push-main.sh` prints), and state the size when asking.
  - Count the whole operation, and never split it to get under.
  - A full Supabase media release (about 861 MiB) always needs asking.
- **A force-push**, rewriting remote history, changing repository visibility, or pushing to another repository.
- **A new site or project**, or changing a site's access, domain or DNS, unless the task is exactly that and the user asked for it.
- **When the permission check blocks** a deploy, rollback or upload: stop. Don't retry it another way or through another thread. Tell the user the exact click path or command.
- **Live broken after your publish:** say so first in your report, with the measured evidence and the rollback click path. Don't bury it.

## Guardrails: never

- Never publish anything but the clean, pushed `origin/main`. No unmerged branch, no uncommitted file.
- Never deploy large media to Netlify as a fallback; media lives in Supabase Storage.
- Never publish to a host the project has retired, even if old scripts still point at it.
- Never run the broad image optimizer (`pnpm images:optimize`, or `optimize-images.py --apply`). It rewrites other sessions' pending images. Use `runtime-assets.py --only '<your glob>'`, then `--verify`.
- Never stage credentials, `.env*`, `node_modules`, caches or build output, and never use `git add -A` in a shared checkout.
- Never call a local commit pushed, or a deploy live, until you've confirmed it on the remote or the domain.
- Never kill a process you didn't start. Check its working folder first: `lsof -a -p <pid> -d cwd`.

## Steps

### 0. Before you start
- Run `git fetch`, then `git log origin/main --oneline -30`, and search for your area. Look in the sibling worktrees (`git -C <wt> diff --stat`) for someone already making the same edit.
- Work in your own worktree on a branch off `origin/main`. Other sessions edit the shared checkout live.

### 1. Screenshots
- Capture the real game at 1600×900 using the project's review fixtures (`?review=<name>`). Take the start, the key moment and the result.
- If the project names a capture tool, use it. Otherwise capture headlessly over CDP (see the `workflow-progress-screenshots` skill), and say which you used.
- Look at every picture before using it. Stray toasts, stale numbers, or the wrong scene mean recapture.
- Label them honestly: headless browser captures, and a phone-sized viewport is not a device test.
- Keep capture scripts in the worktree's gitignored `qa/captures/`; the session scratchpad is wiped on restart.

### 2. Changelog version
- Follow the project's changelog rules exactly: format, versioning, and how pictures are added.
- Write for players: what they can see or do now, with no file names or hashes.
- Changes to tests, tooling, docs or rules get no version.
- If another session took your version number, renumber yours on merge, and keep their entries.

### 3. Verify
- Run the suites your change touches as you go.
- After merging `main`, also run every test file the incoming commits touched: `git diff --name-only <old-base> <new-base> -- tests`.
- Run the image verify if images shipped.
- The full suite takes 10–40 minutes on a busy machine. Run it with `run_in_background` and read the log. Re-run a timeout-looking failure on its own before calling it real.
- Report honestly which runs were full and which were targeted, with pass and fail counts.

### 4. Commit
- `git diff --cached` must be empty before you start.
- Stage **explicit paths** only.
- Run `commit-size.sh` on the staged changes; its numbers go in the report.
- One commit per cohesive change. While still iterating, amend a single work-in-progress commit instead of piling up small ones.
- Write the message in the repo's style, ending with the attribution line the system gives you.

### 5. Merge and push
1. `git fetch`, then `git rebase origin/main` (or merge, on a shared branch).
2. Resolve conflicts keeping everyone's work. For generated JSON (image audit, manifests), take upstream's file, re-add your own records, and recompute totals with the project's tool.
3. `node --check` every `src` and `tests` file. Then run your tests plus the incoming commits' tests.
4. `push-main.sh`:
   - it refuses anything that isn't a fast-forward;
   - it measures the pack and stops over 50 MB;
   - it pushes with `--progress` and prints git's "Writing objects" line (the bytes sent);
   - it confirms `origin/main` equals HEAD.

   If `main` moved, go back to step 1.
5. Run the full suite on the pushed commit, and fix forward if it breaks.

### 6. Publish live
- Build in a checkout whose HEAD is exactly `origin/main` and whose tracked files are clean.
- If the build changes a tracked file, commit and push that file first, then build again.
- Measure what will be uploaded (`upload-size.sh dist`, plus any media release). Over 50 MB, stop and ask.
- **Deploy to a draft or preview URL first.** Run `verify-live.sh <draft-url>`: the page, its scripts and art, and the gate route. Promote to production only when it passes. This step exists because a production deploy once went out without its edge function: the site served its page but 404'd every image, and nobody could play.
- After promoting, run `verify-live.sh` on the real domain. Record the deploy ID, the publication time, the live game version, and the bytes sent.
- If another session published after you, that's fine as long as it also published `main`.

## Report

Short, in this order:

1. The commit hash, pushed and confirmed. Commit size: files, total size, largest files. Push size: the bytes sent.
2. Live: URL, deploy ID, time, live version, and the `verify-live.sh` result. Upload size: bytes sent, built-site size, and any media release. If you didn't publish, say why (for example "held: needs a media release over 50 MB; asking").
3. What changed, for a player, plus the changelog version and title.
4. Tests: which runs were full and which targeted, with pass and fail counts.
5. Screenshots with captions, labelled as headless captures.
6. Anything deferred or departed from, and why.
