---
name: pragmatic-git-context
description: Inspect dirty worktrees, focused diffs, and Git provenance without loading broad history or overwriting user changes. Use when separating overlapping changes, reviewing a targeted delta, or answering a genuinely historical Git question.
metadata:
  author: code-dimension
  version: 1.0
---

# Pragmatic Git Context

Answer the current Git question with the smallest evidence surface. Current
state and invariants come before history.

## Start With The Question

Classify the need:

- current ownership map: which paths are dirty;
- focused delta: what changed in named paths or symbols;
- invariant: whether a project, alias, import, or rule exists now;
- provenance: when and why a specific line or symbol changed.

Do not use history for a current-state or invariant question.

## Dirty Worktree

Run `rtk git status --short` once to map staged, unstaged, deleted, and
untracked paths. Existing changes belong to the user unless proven otherwise.
Never normalize the tree with reset, checkout, clean, stash, or broad staging.

Avoid repository-wide `git diff HEAD`. Scope inspection to authorized paths:

```bash
rtk git diff --stat -- <paths>
rtk git diff -U1 -- <paths>
rtk git diff --word-diff=porcelain -- <path>
```

In a heavily modified file, prefer exact invariants over reconstructing every
prior edit:

```bash
rtk grep -n '<removed-or-retained-symbol>' <path>
rtk npx nx show project <name> --json
```

`apply_patch` is the authoritative record of the current agent's intended
manual edit. Inspect its target lines and resulting invariants; do not claim
ownership of other hunks merely because they appear in the same Git diff.

## Untracked And Deleted Paths

Inspect only untracked paths relevant to the task. For removals, prove the
result through consumers, resolution, graph, aliases, and configuration rather
than printing every deleted line.

## History Only When Needed

Use path- and symbol-bounded history:

```bash
rtk git log --oneline -- <path>
rtk git log -S'<symbol>' -- <path>
rtk git blame -L <start>,<end> -- <path>
```

Stop once the historical question is answered. Do not scan all commits,
branches, or files speculatively. History explains provenance; it does not
override current specifications or user authorization.

## Reporting

Report the current answer, exact paths/symbols inspected, and any attribution
uncertainty. Omit full diffs and log transcripts unless the user asks for
them.
