---
name: jj
description: "Jujutsu (jj) — the Git-compatible version control system. Activate ONLY when a .jj/ directory is present in the project or when jj/jujutsu is explicitly mentioned. Do NOT activate for plain git repos without .jj/. Use for any VCS operations in jj-managed projects: commit, push, pull, branch, bookmark, rebase, squash, merge, diff, log, status, working copy, change ID, revset, fileset, template, configuration, workspaces."
compatibility: "Requires a jj-managed repository (.jj/ directory present in project root)"
requires-path: ".jj/"
---

# Jujutsu (jj) Version Control

Jujutsu is a Git-compatible VCS with mutable commits, automatic change tracking, and an operation log that makes every action undoable.

**Target version: jj 0.36+**

## Topics

| I need to... | Deep dive |
|--------------|-----------|
| Understand how jj relates to Git, or use raw git in a jj repo | [git.md](git.md) |
| Write revset, fileset, or template expressions | [revsets.md](revsets.md) |
| Push, pull, manage bookmarks, or work with GitHub | [sharing.md](sharing.md) |
| Split, rebase, squash, or resolve conflicts | [history.md](history.md) |
| Run parallel agents with isolated working copies | [workspaces.md](workspaces.md) |
| Configure jj, set up aliases, or customize diffs | [config.md](config.md) |

## Mental Model

**The working copy is a commit.** No staging area. Every file change is auto-snapshotted into `@` when you run any `jj` command. Instead of "stage → commit," just code and describe.

**Change IDs are stable. Commit IDs are not.** Every commit has two identifiers:
- **Change ID** — Stable across rewrites. Letters k–z (e.g., `tqpwlqmp`). Prefer these.
- **Commit ID** — Content hash, changes on any rewrite. Hex digits. This is the Git commit ID in colocated repos.

**History is mutable.** Commits can be freely rewritten. Descendants auto-rebase. Old versions stay in the operation log.

**Bookmarks are not branches.** Bookmarks don't advance when new commits are created. They follow rewrites but must be explicitly set before pushing.
→ Deep dive: [sharing.md](sharing.md)

**Conflicts don't block.** jj allows committing conflicted files. Resolve at your convenience by editing conflict markers directly, then verify with `jj st`.
→ Deep dive: [history.md](history.md)

## Agent Rules

Non-negotiable when operating as an automated agent:

1. **Always use `-m` for messages.** Never invoke a command that opens an editor. Commands that need `-m`: `jj new`, `jj describe`, `jj commit`, `jj squash`.
2. **Never use interactive commands.** `jj split` (without file paths), `jj squash -i`, `jj resolve` — all hang. Use file-path args or `jj restore` workflows.
3. **Verify after mutations.** Run `jj st` after `squash`, `abandon`, `rebase`, `restore`, or any destructive op.
4. **Use change IDs, not commit IDs.** Change IDs survive rewrites.
5. **Quote revsets.** Always single-quote: `jj log -r 'mine() & ::@'`.

### Agent-Specific Configuration

```toml
# agent-jj-config.toml
[user]
name = "Agent"
email = "agent@example.com"

[ui]
editor = "TRIED_TO_RUN_AN_INTERACTIVE_EDITOR"
diff-formatter = ":git"
paginate = "never"
```

Launch with: `JJ_CONFIG=/path/to/agent-jj-config.toml <agent-harness>`
→ Deep dive: [config.md](config.md)

## Core Workflow

The daily loop: **describe → code → new → repeat.**

```bash
jj describe -m "feat: add user validation"
# make changes — auto-tracked, no `add` needed
jj st && jj diff
jj new -m "feat: add error handling"
```

### Curating History

```bash
jj squash -m "feat: final clean message"   # fold working copy into parent
jj absorb                                   # auto-distribute hunks to right ancestor
jj abandon @                               # drop a failed experiment
```
→ Deep dive: [history.md](history.md)

### Non-Linear Work

When new work doesn't depend on the current chain, branch off trunk:

```bash
# Create sibling from trunk (doesn't move @)
jj new trunk() --no-edit -m "fix: correct timezone handling"
jj edit <bugfix-change-id>
# ... fix the bug ...

# Return to original work
jj log -r 'heads(trunk()..)'
jj edit <feature-change-id>
```

**Agent rule:** Before creating a new commit, decide if it depends on the current chain. If not, branch off trunk and flag the divergence to the user.

### Pushing Changes

```bash
jj bookmark set feat -r @
jj git push -b feat
```

Bookmarks must be set before pushing — they don't auto-advance.
→ Deep dive: [sharing.md](sharing.md)

## Essential Commands

| Task | Command |
|------|---------|
| Check status | `jj st` |
| View diff / log | `jj diff` / `jj log` |
| Describe current commit | `jj describe -m "message"` |
| Start new work | `jj new -m "task description"` |
| Edit an older commit | `jj edit <change-id>` |
| Squash into parent | `jj squash` |
| Auto-distribute changes | `jj absorb` |
| Abandon a commit | `jj abandon <change-id>` |
| Undo last operation | `jj undo` |
| View operation history | `jj op log` |
| Restore to earlier state | `jj op restore <op-id>` |
| Create/move bookmark | `jj bookmark create <n> -r @` / `jj bookmark set <n> -r @` |
| Push / fetch | `jj git push -b <bookmark>` / `jj git fetch` |

For Git translations: [references/git-to-jj.md](references/git-to-jj.md)

## Recovery

```bash
jj undo                      # undo last op; repeatable
jj op log                    # full operation history
jj op restore <op-id>        # jump to any past state
jj evolog -r <change-id>     # see how a change evolved
```

## Detecting a jj Repo

`.jj/` directory = jj repo. Both `.jj/` and `.git/` = colocated repo. Always use `jj` commands. Git's "detached HEAD" is normal in colocated repos — use `jj log` for real state.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Omitting `-m` on commands | Always pass `-m` — editor hangs agents |
| Using `jj split` without file paths | Provide paths or use the `jj restore` workflow |
| Forgetting to set bookmark before push | `jj bookmark set <name> -r @` first |
| Using commit IDs instead of change IDs | Change IDs (letters k–z) survive rewrites |
| Unquoted revset expressions | Always single-quote: `'mine() & ::@'` |
| Confusing `::` vs `..` operators | `::` = ancestry path, `..` = range (see [revsets.md](revsets.md)) |
| Creating workspaces as subdirectories | Must be sibling dirs, not children |

## Reference Index

**Git Interop:**
- [references/git-to-jj.md](references/git-to-jj.md) — Git-to-jj command mapping
- [references/git-experts.md](references/git-experts.md) — Why jj improves on Git
- [references/git-compatibility.md](references/git-compatibility.md) — Git interop and colocated repos

**Commands:**
- [references/command-gotchas.md](references/command-gotchas.md) — Flag semantics, quoting, deprecated flags

**Revsets & Templates:**
- [references/revsets.md](references/revsets.md) — Complete revset language spec
- [references/filesets.md](references/filesets.md) — Complete fileset language spec
- [references/templates.md](references/templates.md) — Complete template language spec

**Sharing:**
- [references/bookmarks.md](references/bookmarks.md) — Complete bookmarks reference
- [references/github.md](references/github.md) — GitHub/GitLab workflow details

**History:**
- [references/conflicts.md](references/conflicts.md) — Conflict handling and marker formats
- [references/divergence.md](references/divergence.md) — Divergent changes guide

**Config:**
- [references/config-reference.md](references/config-reference.md) — Full configuration reference

**Workspaces:**
- [references/parallel-agents.md](references/parallel-agents.md) — Parallel agent setup guide
