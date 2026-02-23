---
name: git-spice
description: Use git-spice to manage stacked branches and GitLab/GitHub merge requests. Covers setup, daily workflow, staging rules, MR descriptions, issue closing, amending, and merging stacks bottom-up. Invoke when working with stacked PRs/MRs or whenever the user mentions gs, git-spice, or stacked branches.
---

# git-spice

git-spice is a CLI tool for managing stacks of dependent branches and their corresponding pull/merge requests. It removes the friction of rebasing and updating dependent MRs as you iterate.

**When in doubt, consult the built-in help generously.** Every command and subcommand has detailed help:

```bash
git-spice -h                    # all top-level commands
git-spice stack -h              # stack subcommands
git-spice branch -h             # branch subcommands
git-spice <command> -h          # any command
```

## When to use

- Working on a feature that spans multiple logical commits or MRs
- Keeping a chain of dependent branches in sync after rebases
- Creating, updating, or merging a stack of GitLab or GitHub MRs
- Amending commits in the middle of a stack and propagating changes upward
- Any time the user mentions `git-spice`, `gs` (deprecated alias), or "stacked branches/PRs"

## Instructions

### 1. Before you start

Run `git-spice -h` to see all available commands. Command names and flags evolve — always verify against the installed version rather than guessing. The help output is concise and authoritative.

> **Note:** As of v0.24.0, the binary was renamed from `gs` to `git-spice`. To keep using the short form, add `alias gs='git-spice'` to your shell config.

### 2. One-time setup

Initialize git-spice in a repository once:

```bash
git-spice repo init --trunk main --remote origin
```

For GitLab (self-hosted), also set the forge URLs and authenticate:

```bash
git config spice.forge.gitlab.url https://gitlab.example.com
git config spice.forge.gitlab.apiURL https://gitlab.example.com/api/v4
git-spice auth login --forge=gitlab          # uses a Personal Access Token
```

For GitHub (public), authentication works out of the box via `git-spice auth login`.

### 3. Core concepts

- **Branch**: a single node in the stack, backed by a Git branch
- **Stack**: the ordered chain of branches from trunk to the current branch
- **Trunk**: the base branch (usually `main`) — never modified by `git-spice`
- **Submit**: pushes all branches in the stack and creates/updates MRs on the forge

`git-spice` tracks the stack in `.git/spice/` — this metadata is local and not pushed.

### 4. Staging rules — read this carefully

**`git-spice bc -a` only stages tracked modified files**, just like `git commit -a`. It does NOT pick up new untracked files.

**`git-spice commit amend` does NOT auto-stage anything** — it amends whatever is currently staged.

**Always run `git add` explicitly before any `git-spice` commit operation:**

```bash
git add <new-or-modified-files>
git-spice bc -m "feat: my feature"           # create branch + commit staged changes
```

```bash
git add <changed-files>
git-spice commit amend --no-edit             # amend the current branch's commit
```

Forgetting this is the most common source of empty or incomplete commits.

### 5. Daily workflow

#### Create branches in a stack

```bash
# On trunk or any branch — stage first, then create
git add src/feature.py tests/test_feature.py
git-spice bc feature-part-1 -m "feat: add core feature logic"

# Continue stacking
git add src/more.py
git-spice bc feature-part-2 -m "feat: add API layer"
```

`git-spice bc` creates the branch, commits staged changes, and records the parent relationship.

#### Navigate the stack

```bash
git-spice log short              # visual overview of the entire stack
git-spice up                     # move up one branch toward the tip
git-spice down                   # move down one branch toward trunk
git-spice top                    # jump to the top of the stack
git-spice bottom                 # jump to the bottom (first branch above trunk)
```

#### Check current state

```bash
git-spice branch show            # current branch details and parent
git-spice stack show             # full stack with MR status (if submitted)
```

### 6. Submitting the stack

Push all branches and create MRs on the forge in one command:

```bash
git-spice stack submit --fill --no-draft
```

- `--fill` populates MR title and description from the commit message
- `--no-draft` marks MRs as ready for review immediately
- Re-run after amending to update existing MRs: `git-spice stack submit --update-only`

To submit only the current branch's MR:

```bash
git-spice branch submit --fill --no-draft
```

### 7. MR descriptions and issue closing

**Do not use `git-spice bs --body "..."` to set issue-closing phrases.** It is silently ignored when there are no new commits to push ("CR is up-to-date").

**Use `glab mr update` instead — it always works:**

```bash
glab mr update <mr-id> --description "## Summary

Implements XYZ.

Closes #42"
```

This updates the description on GitLab immediately. When the MR is merged, GitLab reads the description and auto-closes the linked issue.

For GitHub, use `gh pr edit <number> --body "..."`.

### 8. Amending commits in the stack

To change the current branch's commit (fix a bug, address review feedback):

```bash
git add <changed-files>
git-spice commit amend --no-edit            # or: git-spice ca --no-edit
```

Then push the updated stack:

```bash
git-spice stack submit --update-only
```

`--update-only` skips creating new MRs and only updates existing ones. It will force-push rebased branches as needed.

To amend a commit that is **not** at the top of the stack:

```bash
git-spice down                              # navigate to the target branch
git add <files>
git-spice ca --no-edit
git-spice stack submit --update-only        # propagates rebase upward automatically
```

### 9. Merging a stack

Always merge **bottom-up**: the lowest branch (closest to trunk) first. Merging out of order causes rebase conflicts.

#### Option A: Full stack merge via forge (preferred)

When landing an entire stack, merge all MRs via GitLab without any local restacks between them. GitLab automatically retargets each upstream MR when its target branch is merged. One final sync at the end cleans up local tracking.

```bash
# Merge each MR bottom-up via GitLab — no local ops between merges
glab mr merge <mr-1> --remove-source-branch --yes
glab mr merge <mr-2> --remove-source-branch --yes
glab mr merge <mr-3> --remove-source-branch --yes
# ... repeat for the full stack

# One sync at the end to clean up local branch tracking
git-spice repo sync --restack
```

Or use the GitLab web UI to merge each MR in order, then run the final sync.

**Why:** every `git-spice repo sync --restack` between merges force-pushes all remaining branches to the forge, triggering a new pipeline run for each. For a stack of N MRs this creates O(N²) unnecessary pipeline runs.

**Never use `-m "custom message"`** with `glab mr merge`. It overrides the merge commit message, which discards `Closes #XX` from the MR description. Omit `-m` so GitLab uses its default merge commit, which includes the MR body.

#### Option B: Single MR merge (continuing development)

When merging one MR from the bottom of the stack while keeping the rest in development:

```bash
glab mr merge <lowest-mr-id> --remove-source-branch --yes
git-spice repo sync --restack               # pulls trunk, rebases remaining branches
git-spice stack submit --update-only        # updates MR targets on the forge
```

The restack is necessary here because you're continuing to work on the remaining branches and they need to be based on the updated trunk.

#### After-rebase 405 errors

When a branch is force-pushed (after `git-spice repo sync --restack`) and you immediately try to merge, GitLab may return 405. Wait a few seconds and retry — it resolves on its own.

### 10. Other useful commands

```bash
git-spice branch onto main                  # re-parent a branch directly onto trunk
git-spice branch delete <name>              # delete a branch and its stack tracking
git-spice branch rename <old> <new>         # rename a branch
git-spice repo sync                         # pull trunk and update stack metadata (no restack)
git-spice repo sync --restack               # pull trunk + rebase entire stack on top
git-spice stack restack                     # rebase stack without pulling trunk
```

### 11. Anti-patterns

- **Forgetting `git add` before `git-spice bc` or `git-spice ca`** — produces empty or partial commits. Always stage explicitly.
- **`glab mr merge -m "..."`** — overrides the merge commit message, losing `Closes #XX` linkages.
- **`git-spice bs --body "Closes #XX"` without code changes** — silently no-ops. Use `glab mr update --description` instead.
- **Merging top-down** — always merge the bottom of the stack first. Top-down causes conflicts.
- **Manually rebasing instead of `git-spice stack restack`** — breaks git-spice's branch tracking metadata.
- **Running `git-spice repo sync --restack` between merges when landing a full stack** — force-pushes all remaining branches on every iteration, creating O(N²) unnecessary pipeline runs. Merge all MRs via the forge bottom-up first, then run one final sync. See Section 9 Option A.
- **Guessing flag names** — run `git-spice <command> -h` before using any unfamiliar flag. git-spice's CLI is well-documented and the help is always accurate.
