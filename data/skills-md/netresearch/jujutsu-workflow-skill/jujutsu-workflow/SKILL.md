---
name: jujutsu-workflow
description: "Use when a coding agent works in a repository where Jujutsu (jj) is available (a `.jj/` directory) — running jj commands, making speculative edits, splitting changes, recovering with the operation log (jj undo / jj op restore), handing off a PR to Git/GitHub/GitLab, updating a PR after review, or coordinating parallel agents. Uses jj as the local change-management layer while keeping Git as the canonical remote, PR, CI, and audit interface. Also use to avoid jj's agent footguns (pager/editor hangs, commit absorption, colocated git/jj desync) or to replace fragile git reset/checkout/stash/rebase recovery with reversible jj operations."
license: "(MIT AND CC-BY-SA-4.0). See LICENSE-MIT and LICENSE-CC-BY-SA-4.0"
compatibility: "Verified against jj 0.42.0 and 0.43.0. Re-check flags with `jj <cmd> --help` on other versions."
metadata:
  author: Netresearch DTT GmbH
  version: "1.0.0"
  repository: https://github.com/netresearch/jujutsu-workflow-skill
---

# Jujutsu Workflow

**Prefer `jj` (Jujutsu) over raw `git`** whenever a `.jj/` repo is present. Git stays the canonical remote/PR/CI/audit interface: mutate with `jj`, verify with read-only Git.

## 1. Detect & gate first

Run `${CLAUDE_SKILL_DIR}/scripts/detect_jj_state.sh`, or check manually:

- `.jj/` present → jj repo: use `jj`, never **mutating** raw `git`.
- `.jj/` **and** `.git/` → colocated: mutate with `jj`, read with git, never touch the git index/staging.
- only `.git/` → plain Git repo: do not introduce `jj` unless asked.
- in a git worktree, `jj root` ≠ `git rev-parse --show-toplevel` → **shadowed** (exit 3): jj answers for the parent repo. Run no `jj`; use git, then ask.

See [references/git-interop.md](references/git-interop.md).

## 2. Agent-safety rules (non-negotiable)

- Always `--no-pager` on commands that print. Do **not** write `ui.paginate` into the user's config — `--user` outlives the session and takes paging away from their interactive `jj` too.
- Always `-m`. **Never** run editor/TUI forms — bare `jj describe|commit|squash`, `jj split` (interactive), `jj squash -i`, `jj resolve`, `jj diffedit` — they hang agents.
- `jj` snapshots the working copy only when a jj command runs, **not** on every file write.

See [references/agent-safety.md](references/agent-safety.md).

## 3. Edit loop

```bash
jj --no-pager status
# edit files (snapshotted on the next jj command)
jj --no-pager diff
jj describe -m "<project-conventional message>"
jj new -m "<next unit>"     # one change per logical unit
```

Split non-interactively: `jj split <path> -m "<msg>"`. See [references/command-map.md](references/command-map.md).

## 4. Recover (reversible)

`jj --no-pager op log` → `jj undo` or `jj op restore <id>`. Conflicts are first-class: `jj status` flags them; edit markers, then verify. See [references/recovery-playbook.md](references/recovery-playbook.md).

## 5. Hand off via Git

```bash
jj git fetch
jj rebase -d <default-branch>
jj bookmark create <branch> -r @-    # every pushed commit needs a description
jj git push --bookmark <branch>      # new bookmarks push directly
```

Never push to a protected/default branch; never rewrite public history unless allowed. Open the PR with `gh`/`glab`. See [references/pr-handoff.md](references/pr-handoff.md).

## 6. Parallel agents

One `jj workspace` per concurrent agent — never share a working copy. See [references/parallel-agents.md](references/parallel-agents.md).

## 7. Verify before "done"

Run `${CLAUDE_SKILL_DIR}/scripts/verify_handoff.sh`, or report `jj --no-pager status`, `jj --no-pager log --limit 10`, `jj --no-pager diff --stat`, `git status --short --branch`. Never claim "done/tested/ready" without that output; disclose force-pushes, recoveries, conflicts.

**When jj helps, and when it doesn't**: [references/why-jj-for-agents.md](references/why-jj-for-agents.md).
