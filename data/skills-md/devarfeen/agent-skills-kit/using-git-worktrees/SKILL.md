---
name: using-git-worktrees
disable-model-invocation: true
description: "Set up or reuse a Git worktree when the user asks to work in a worktree, before the task skill runs. Not for branch-only requests, generic implementation, worktree questions, or cleanup alone."
metadata:
  version: "0.3.0"
---

# Using git worktrees

Establish a task checkout and return its verified location; setup does not implement or ship the task.

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

## Inputs

- Identify the target repository and requested task. In a workspace, use the Project Matrix to resolve the project; an ambiguous repository blocks creation, not independent inspection.
- Use `<project-repo>/.worktrees/<task-name>` for placement. Honor the user's branch and base revision when supplied. Otherwise follow applicable project conventions; default a new task branch to the current checkout's recorded `HEAD`, and state that assumption. If the task requires an unavailable base, resolve it before creating anything.
- The request to work in a worktree already authorizes setup. Do not ask for the same permission again. A request for only a new branch stays a branch operation; ambiguous isolation wording needs its form resolved before this skill runs.

## Rules

- **User invocation, workflow exceptions.** Direct use requires explicit user invocation; implicit discovery stays disabled. Explicitly user-started `/orchestrate-t3` and `/factory run` may read and follow these instructions for checkout setup only; never call a runtime Skill tool that rejects user-only targets. Other workflows use authorized Git setup or ask the user to run this skill when needed.

- **Preserve existing work.** Inspect staged, unstaged, and untracked changes in both the source and any reused checkout. Leave unrelated changes in place. Uncommitted source changes do not appear in a new worktree; if the task needs them, resolve a scoped transfer with the user before proceeding. Never stash, reset, overwrite, or copy the whole checkout as a shortcut.
- **Keep isolation binding.** A permission error, occupied branch, or failed setup is a blocked worktree step. Report it and pause dependent edits; never fall back to writing in the original checkout without the user's explicit change of scope.
- **Keep shipping separate.** Setup never stages or commits, even to record an ignore rule. It does not merge, push, delete branches, or remove worktrees. Leave the worktree available to the caller; later shipping and cleanup follow their own authorized workflow. For user-requested cleanup, verify integration and preserve needed tracked, untracked, and ignored files first; a push or issue closure alone is not integration proof. Cleanup is outside this setup skill.
- **Gate task writes.** Creation alone does not prove isolation. Before task edits, record and report the canonical checkout path, owning repository and common Git directory, branch or authorized detached state, starting commit, and baseline result. Pass this record and applicable instructions to every task skill and assigned worker. Before the first write and after a handoff, restart, or checkout change, verify the current Git root, common directory, branch, and worktree-list entry against that record. A mismatch blocks dependent writes until corrected; never fall back to the source checkout. Use an explicit working directory for every task shell command and absolute paths inside the verified checkout for file-edit tools; resolve symlinks before writes. Confirm containers and test runners use that checkout. Only the narrow source `.gitignore` setup edit is permitted outside it by this skill; other outside writes need their own scope. Subsequent authorized commits may advance HEAD; retain the starting commit as provenance rather than requiring HEAD to stay fixed.
- **Keep context attached.** Capture applicable workspace and project instructions before switching. A worktree may live outside their filesystem scope; pass those instructions and the verified checkout to any already-authorized local worker. Creating a worktree does not authorize delegation.

## Workflow

### 1. Resolve the checkout

Announce the skill, then inspect the target repository:

```bash
git rev-parse --show-toplevel
git rev-parse --path-format=absolute --git-dir --git-common-dir
git rev-parse --show-superproject-working-tree
git worktree list --porcelain
git status --short
git branch --show-current
git rev-parse HEAD
```

Use canonical paths. Different Git and common directories suggest linked-worktree isolation; verify against `git worktree list` before treating the current checkout as reusable. A `.git` file alone proves nothing: submodules also use one. A `prunable` or registered-but-missing entry blocks reuse at that path; report it — pruning is cleanup. A superproject result identifies a submodule; resolve which repository the task targets instead of accidentally isolating the wrong one.

Reuse an existing worktree only when it belongs to this task and matches the requested branch/base and lives under that project repository’s `.worktrees/`. A harness-created worktree counts; do not nest another by default. An explicit request for a new worktree still requires a new one. Leave unrelated or actively owned worktrees alone. For a suitable detached checkout, report detached state and preserve harness ownership; create a named branch only if the task requires one and the runtime permits it.

### 2. Prepare the destination

For a reusable checkout, perform the ignore checks below and skip creation. Otherwise select a creation mechanism.

Prefer an exposed native worktree tool when it can honor the requested repository, base, and path. Inspect its live schema; do not assume a tool exists or that its default base equals local `HEAD`. If no suitable native surface exists, use Git directly. Do not retry a denied native action through Git to evade a permission boundary.

Create each task checkout under **that project's own repository** at `.worktrees/<task-name>`. Resolve the owning repository root from the primary checkout in `git worktree list`; do not create a workspace-wide container, use a sibling project's repo, or nest `.worktrees/` inside a linked checkout. Multi-project tasks need one worktree per affected repository. A native tool qualifies only if it can use this placement; otherwise use Git directly within the same authorization.

Before creation or reuse, add `/.worktrees/` once to the owning repository's `.gitignore` and verify the actual destination is ignored, per [`references/ignore-rule.md`](references/ignore-rule.md). Tracked content under `.worktrees/` → stop setup and report it; never untrack or remove it automatically.

Choose a valid task branch and unused destination. Resolve the intended base to a commit first. For a new branch:

```bash
git worktree add -b "$task_branch" "$worktree_path" "$base_commit"
```

For an existing branch, use `git worktree add "$worktree_path" "$task_branch"` only after checking it is available and contains the task's expected history. If checked out elsewhere, inspect whether that checkout is reusable; otherwise resolve another branch with the caller. Never force-add or reset an existing branch. After any failure, inspect partial state before a corrected retry.

### 3. Verify inside the destination

Set an explicit working directory for every subsequent command; a shell's `cd` may not persist across tool calls. Confirm the destination appears in `git worktree list`, and check its repository root, branch or detached state, `HEAD`, and status. Compare a newly created branch's `HEAD` with the recorded base commit. Verify the source checkout's branch and pre-existing changes remain intact, apart from the reported additive `.gitignore` entry.

Mirror the rule into the destination's `.gitignore` per [`references/ignore-rule.md`](references/ignore-rule.md); never copy the source file wholesale.

Read destination-specific instructions and use the project's documented setup, lockfiles, package manager, and verification command. Reuse completed native setup; do not blindly install dependencies or copy secrets. Confirm containers and test runners mount or execute this checkout rather than the source checkout. Skip dependency setup in a docs-only repository when none is needed.

Before a baseline that starts services, check for collisions with the source checkout — fixed ports, a shared local database that migrations would change — and use the project's documented override, else report a blocker. Run the relevant baseline before task edits and record the command, checkout, and result. Missing tools or environment mean unverified, not passing. For baseline failures, continue only if existing user instructions already authorize working past those failures; otherwise report the evidence and ask whether to proceed or investigate. Unrelated repairs need their own scope.

## Output

Return at most three bullets, with the shortest decisive verification evidence:

- Worktree: `/workspace/api/.worktrees/fix-tax`; branch `fix-tax`; base `a1b2c3d`; newly created.
- Baseline: `bash tools/validate.sh` in that checkout — passed; source branch and pre-existing edits preserved.
- Handoff: bind task commands and edit paths to this verified checkout; recheck identity before the first write and after handoffs or restarts. Preserve workspace instructions; report source-only `.gitignore` edits.

On a blocker, replace the handoff with the blocked step and needed input. Stop setup here. After explicit invocation within an authorized task, or setup loaded by an authorized workflow exception, return the checkout record so that task continues without another permission prompt. A setup-only request ends here; recommend at most one next skill, never auto-chain a new workflow.

## Completion criteria

- [ ] Worktree-list entry, canonical path, branch/detached state, and revision recorded and matched to the task
- [ ] Owning repo `.gitignore` entry and destination ignore evidence captured; source branch and changes checked after setup
- [ ] Setup and baseline command results captured from the destination, or the exact blocker reported
- [ ] Caller and assigned workers have the checkout record and applicable instructions; task writes are bound to the verified destination, with rechecks after handoffs or restarts
- [ ] No task edits began before setup passed or a baseline exception was authorized
