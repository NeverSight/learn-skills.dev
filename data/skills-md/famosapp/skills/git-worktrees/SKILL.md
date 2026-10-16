---
name: git-worktrees
description: |
  Create, manage, compare, and merge Git worktrees for isolated parallel
  development: feature/hotfix branches, PR review without stashing, side-by-side
  diffs, and agent task isolation. Prefers native platform worktree tools; falls
  back to `git worktree`. Default dirs use gold-standard `.worktrees/<X>-<Y>/`
  naming (type-slug) to avoid collisions. Includes critical / recommended / nit
  review checklist.

  Trigger when the user asks to use worktrees, isolate a branch, avoid stashing,
  review a PR in parallel, compare implementations across branches, set up
  `.worktrees/`, or run git worktree add/list/remove/prune/repair.

  Keywords: git worktree, linked worktree, branch lock, .worktrees, X-Y naming,
  isolation, parallel development, PR review, hotfix, compare, merge, cherry-pick,
  prune, EnterWorktree, orca worktree
version: 1.1.0
license: Apache-2.0
metadata:
  author: famosapp
  stack: git-2.23+, optional-orca-cli, cursor-native-worktree
  preferred_location: .worktrees/
  dir_naming: X-Y  # .worktrees/<type>-<slug>/
---

# Git Worktrees

Production worktree isolation for this stack. **Non-negotiables override casual
`git worktree` habits.** Read the linked reference before inventing layout.

**Announce when activating:** "Using the git-worktrees skill to set up / manage
an isolated workspace."

## When to load which reference

| Need | Read |
|------|------|
| Rules & hard bans | [non-negotiable.md](references/non-negotiable.md) |
| Already isolated? Create safely | [detection.md](references/detection.md), [create.md](references/create.md) |
| Commands & flags | [commands.md](references/commands.md) |
| Feature / hotfix / PR / compare / merge | [workflows.md](references/workflows.md) |
| Deps install & baseline tests | [setup.md](references/setup.md) |
| Pitfalls | [gotchas.md](references/gotchas.md) |
| Branch naming & path layouts | [types-and-layouts.md](references/types-and-layouts.md) |
| Review / PR feedback | [review-checklist.md](references/review-checklist.md) |
| Copy-paste recipes | [examples.md](references/examples.md) |
| DO / DON'T full list | [do-dont.md](references/do-dont.md) |

---

## Core rules

1. **Detect isolation first** — never nest a worktree inside an existing linked worktree. See [detection.md](references/detection.md).
2. **Prefer native tools** over raw `git worktree` when the harness provides them (Cursor worktree APIs, `orca worktree`, `/worktree`, etc.). Never fight the harness.
3. **One branch ↔ one worktree.** A branch can be checked out in only one worktree at a time.
4. **Project-local paths under `.worktrees/<X>-<Y>/`** (ignored) — **X** = canonical type, **Y** = topic slug — to avoid duplicate names across kinds. Honor explicit user preference first.
5. **Verify ignore** before creating project-local worktrees — never commit worktree contents.
6. **Remove with `git worktree remove`** (or native equivalent) — never `rm -rf` as the primary cleanup.
7. **Setup + baseline** after create: install deps, run tests, report pass/fail before implementing.
8. **Clean up promptly** when the task/PR/hotfix is done; prune stale metadata.

---

## Non-negotiable

Full contract: [non-negotiable.md](references/non-negotiable.md).

| Rule | Requirement |
|------|-------------|
| Detection first | Run Step 0 isolation check before any `worktree add` |
| Native > git | Use platform/Orca/Cursor worktree tools when available |
| Consent | Ask before creating a worktree unless user already requested isolation / declared preference |
| Location priority | Explicit user path → existing `.worktrees/` or `worktrees/` → default `.worktrees/` |
| Dir naming | **`X-Y` only:** `.worktrees/<type>-<slug>/` (e.g. `feature-auth-system`). Never slug-only. Canonical X tokens; collision → `-2`, `-3`, … |
| Ignore gate | `git check-ignore` must pass for project-local dirs (add to `.gitignore` + commit if not) |
| Branch lock | Never force the same branch into two worktrees |
| No nested worktrees | Do not create linked worktrees inside another linked worktree |
| Cleanup API | `git worktree remove` / native remove; `prune` only after manual dir loss |
| Submodule guard | `GIT_DIR != GIT_COMMON` inside a submodule ≠ linked worktree — treat as normal repo |
| Sandbox fallback | If create is permission-blocked, work in place and say so — do not fake success |

---

## Git / Worktree “Gotchas”

Summary — details in [gotchas.md](references/gotchas.md).

- **Branch already checked out** elsewhere → `git worktree list`, then use that path or remove it.
- Shared object DB: commits in any worktree are visible to all; working trees are independent.
- `GIT_DIR != GIT_COMMON` also true in **submodules** — check `--show-superproject-working-tree`.
- Deleting the directory with `rm -rf` leaves stale admin files → `git worktree prune`.
- Manual `mv` of a worktree breaks links → `git worktree move` or `git worktree repair`.
- Soft assumptions from other skills do not apply: worktree remove is **hard** filesystem removal of that checkout.
- Detached HEAD worktrees need a branch created before “finish/PR” if commits must be kept.
- Project-local worktrees **must** be gitignored or they pollute `git status`/commits.

---

## Branch & ref types

| Type | When | Branch pattern | Notes |
|------|------|----------------|-------|
| Feature | New work | `feature/<name>` or `feat/<name>` | Default if no type word |
| Fix | Non-urgent bug | `fix/<name>` | |
| Hotfix | Prod emergency | `hotfix/<name>` | Base from `main`/`master` |
| Review | PR inspection | `review/pr-<n>` or fetch `pull/<n>/head` | Temporary; remove after |
| Spike / experiment | Throwaway | `spike/<name>` or `--detach` | Prefer detach if no keep |
| Refactor / chore / docs / test | As named | `<type>/<name>` | |
| Release | Cut/ship | `release/<name>` | |
| Detached | Compare / bisect / try | no branch | `git worktree add --detach` |

Name normalization: lowercase, spaces → `-`, strip unsafe chars. Full rules:
[types-and-layouts.md](references/types-and-layouts.md).

---

## Worktree & directory types

### Main vs linked

| Kind | Description |
|------|-------------|
| **Main worktree** | Original clone/`git init` checkout |
| **Linked worktree** | Extra directory via native tool or `git worktree add` |
| **Detached worktree** | Linked checkout not on a branch |

### Location layouts (pick one policy per repo)

| Layout | Path pattern | Use |
|--------|--------------|-----|
| **Project-local (default)** | `.worktrees/<X>-<Y>/` | **X** = type (`feature`, `fix`, `hotfix`, …), **Y** = slug; must be ignored |
| **Sibling** | `../<project>-<X>-<Y>/` | Same naming beside the clone |
| **Native/Orca-managed** | Harness-chosen path | When Step 1a native tool owns lifecycle |

```
repo/                          # main worktree
repo/.worktrees/
  feature-auth-system/         # branch feature/auth-system
  fix-auth/                    # branch fix/auth — distinct from feature-auth*
  hotfix-critical-bug/
```

Never place linked worktrees as tracked subdirectories of source (`src/…`).
Never use slug-only dirs (`.worktrees/auth-system/`) — they collide across types.
Full naming + collision policy: [types-and-layouts.md](references/types-and-layouts.md).

---

## DO and DON'T

| DO | DON'T |
|----|--------|
| Run isolation detection first | Nest worktrees inside linked worktrees |
| Prefer native worktree tools | Blindly `git worktree add` when harness provides isolation |
| Use `.worktrees/<X>-<Y>/` + verify ignore | Slug-only dirs or committing worktree contents |
| One branch per worktree | Checkout the same branch in two places |
| `git worktree remove` then prune if needed | `rm -rf` as primary cleanup |
| Install deps + baseline tests after create | Start coding on a broken baseline silently |
| `--detach` for throwaways | Leave dozens of stale feature worktrees |
| `git worktree list` before troubleshooting | Assume path/branch mapping from memory |
| Ask consent if preference unknown | Force worktrees when user wants in-place work |

Complete list: [do-dont.md](references/do-dont.md).

---

## Examples

Recipes in [examples.md](references/examples.md):

1. Detect + create under `.worktrees/<X>-<Y>/` with new branch
2. Hotfix while feature is in progress (`hotfix-<Y>`)
3. PR review without stashing (`review-pr-<n>`)
4. Parallel `feature-auth` + `fix-auth` (no collision)
5. Compare two worktrees / `git diff --stat`
6. Selective file merge / cherry-pick
7. Remove + prune cleanup

---

## Critical / Recommended / Nits

Full checklist: [review-checklist.md](references/review-checklist.md).

Report as `path:line: <severity>: <problem>. <fix>.` (or command/context when no file).

### Critical (block)

| Fail if… |
|----------|
| Created worktree without Step 0 detection / nested inside linked worktree |
| Used raw `git worktree add` despite available native tool |
| Project-local dir not ignored (trackable worktree contents) |
| Slug-only `.worktrees/<Y>/` instead of required `<X>-<Y>/` |
| Overwrote occupied `X-Y` dir belonging to another branch |
| Same branch forced into two worktrees |
| `rm -rf` used as cleanup leaving / risking corruption |
| Proceeded on failing baseline tests without user consent |
| Submodule misclassified as “already in worktree” |

### Recommended (should fix)

| Prefer… |
|---------|
| `.worktrees/<X>-<Y>` (canonical type + slug); descriptive branch `type/name` |
| `--track` when creating from remote; base hotfixes from `main` |
| Setup deps + report test baseline; lock long-lived reference worktrees |
| Prompt cleanup after merge/review; `prune --dry-run` before prune |
| Compare before selective merge |

### Nits (optional)

| Nice… |
|-------|
| Consistent `X-Y` naming; porcelain list in scripts; lock reason strings |
| Sibling vs `.worktrees` consistency with repo docs |
| Detach experiments instead of `tmp-*` branches; prefer `spike-<Y>` when kept |

---

## Design / create workflow

1. **Detect** — [detection.md](references/detection.md). Already linked? → setup only.
2. **Consent / preference** — honor declared path; else ask.
3. **Native tool?** — use it; else git fallback [create.md](references/create.md).
4. **Ignore gate** for `.worktrees/` / `worktrees/`.
5. **Add** worktree (existing branch / `-b` new / `--detach` / track remote).
6. **Setup** deps — [setup.md](references/setup.md).
7. **Baseline tests** — report; ask if red.
8. **Implement** in the worktree path only.
9. **Finish** — commit/PR from that branch; `remove` + optional `prune`; verify against [review-checklist.md](references/review-checklist.md).
