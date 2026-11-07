---
name: ds-watch-pr
description: "Watches a pull request through CI and review, fixes real findings and stops when it is ready, merged or blocked. Use when the user asks to watch, monitor or babysit a PR, or /ds-watch-pr."
---

Keep one PR moving until it is green and reviewed, with as little noise as possible.

The watcher is `scripts/watch_pr.py` in this skill's folder. Call it by absolute path. It needs `python3` and a logged-in `gh`.

```bash
python3 <skill>/scripts/watch_pr.py <pr> [--repo owner/name] [--until ready|green|any] [--interval 30] [--max-minutes 60]
```

It prints one line per new check failure, finished check run, comment or review, then a final `stop:` line. Exit 0 means the condition is met or the PR merged. Exit 1 means you must act. Exit 2 means bad input. `ready` waits for green checks, a mergeable branch and no change request. `green` waits for checks only.

## Steps

1. Handle what already exists: failed checks and comments newer than the last push.
2. Start the watcher. Run it in the harness's background or monitor tool if it has one, so each line wakes you. Otherwise run it as one long foreground command.
3. On each event, read the source before you change code. Decide if the finding is real.
4. For a real bug or CI failure: make the smallest fix, run the failing check locally, push, then restart the watcher.
5. For a false positive or out-of-scope request: reply with a short reason through `ds-pr-comments`, resolve the thread and list it as a follow-up.
6. Tell real test failures apart from infrastructure flakes. Re-run a flake once before you call it a flake.
7. If the base branch moved or the branch is behind, rebase, push with `--force-with-lease` and restart.
8. Before you call the PR ready, `git fetch` and read the PR again. It must not be BEHIND or DIRTY.

## Stop when

- The watcher exits 0. Report the PR as ready, or merged.
- Five fix-and-push cycles pass without exit 0. Report what still fails.
- Another PR makes this one obsolete. Stop and ask before closing it.
- `gh` reports a rate limit. Check `gh api rate_limit` and wait for the reset once. Do not loop.

## Rules

- One watcher per PR. Never write your own sleep or polling loop.
- When an event needs no action, say nothing. No "still waiting" messages.
- Merge only if the user asked for it. Otherwise report ready.
- Keep the PR small. Prefer fixes that delete or narrow code.
