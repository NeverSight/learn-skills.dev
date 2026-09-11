---
name: stacked-prs
description: Create and manage dependent GitHub pull requests with gh stack. Use for stacked PRs, dependent branch chains, incremental review layers, or splitting a large change into ordered PRs.
---

Use `gh stack`; [REFERENCE.md](REFERENCE.md) covers commands, external-link mode, and recovery.

## Contract

- Each layer is independently reviewable against its parent.
- One Conductor workspace owns one stack; unrelated work uses another.
- Test each layer, review `<parent>...HEAD`, and report `gh stack view --json`.
- Honor the requested plan, local, push, draft, open, or merge endpoint.

## Establish mode

Check `gh`, auth, repo support, branch, remotes, cleanliness, and `git worktree list --porcelain`. If missing, suggest `gh extension install github/gh-stack`; never install without permission. With multiple remotes, pass `--remote origin`.

Default to native mode: one workspace owns and switches the whole stack. Before structural commands run:

```bash
"${CLAUDE_PLUGIN_ROOT:-.}/scripts/stack-worktree-conflicts.sh"
```

Exit 2 reports `branch<TAB>path`; do not steal branches, remove worktrees, or cascade. Use external-link mode only for deliberate worktree-per-layer setups:
`gh stack link --base <trunk> --remote origin <bottom> ... <top>`. Coordinate those worktrees before cascades.

## Plan and develop

Show a bottom-to-top table with objective, branch, parent, scope, and verification. Dependencies belong at or below their consumer. Confirm only agent-proposed boundaries.

Require a clean tree for structural commands. Start with `gh stack init --base <trunk> <bottom>`. Implement RED -> GREEN -> REFACTOR, verify, and commit. Add one coherent concern with `gh stack add <next>`. Use explicit branches and file adds, not `git add -A`.

Use `gh stack checkout <branch>` and `gh stack view --json`; avoid argumentless/TUI commands.

## Review and publish

```bash
BASE=$("${CLAUDE_PLUGIN_ROOT:-.}/scripts/resolve-pr-base.sh")
git diff "$BASE"...HEAD
git log "$BASE"..HEAD --oneline
```

Verify and dogfood every layer before publication. Whole-stack submission defaults to drafts: `gh stack submit --auto --remote origin`; add `--open` only when requested. A single-PR request never publishes other layers.

Apply [PR evidence](../commit-push-pr/REFERENCE.md) per layer: `/quantify-impact`, embedded before/after, and passing visual tests for visible changes. Compare with its parent; prepare bodies before submit, verify afterward. Cascades invalidate evidence.

## Feedback, sync, merge

Fix feedback on its owning branch and verify. Cascades rewrite upper branches. A user-owned stack in this workspace may rebase and force-with-lease without another permission prompt; report it. Ask when ownership is unclear or a default, shared, foreign, or concurrent branch would change. Use `gh stack rebase --upstack --remote origin`, then `gh stack push --remote origin`; `gh stack sync --prune --remote origin` has the same boundary.

Continue conflicts with `gh stack rebase --continue`; abort only on request. External-link mode coordinates worktrees first.

Never merge as a publish side effect. Explicit merge intent covers only the named contiguous range. Recheck approvals, checks, history, comments, and todos; use `gh stack merge <stack-or-pr> --yes --merge-method <squash|rebase|merge>`, never `gh pr merge`.

Report trunk, ordered layers, current layer, PR states/URLs, verification, conflicts, rewrites, and next bottom-up action.
