---
name: worktree-feature-execution
description: This skill should be used when the user asks to "implement a feature in an isolated worktree", "create a worktree from the current project branch", "open a PR from worktree changes", "merge feature PRs into main", "run multiple agents in parallel worktrees", or "handle worktree merge conflicts and incompatibilities".
version: 0.2.1
---

# Worktree Feature Execution

## Purpose

Execute feature delivery in isolated git worktrees with consistent automation for branch creation, synchronization, pull request creation, merge safety, and cleanup. Use this skill to reduce branch switching, minimize cross-feature interference, and maintain a clean integration path into `main`.

## Harness Contract

Read project instructions from `AGENTS.md` first. Read `project.yaml` second when present. Prefer AGENTS-defined conventions over CLAUDE-specific conventions.

Use this directory resolution priority unless the project explicitly overrides it:

1. Existing `.worktrees/`
2. Existing `worktrees/`
3. Config value from `project.yaml`
4. Default `.worktrees/`

For project-local roots (`.worktrees/` or `worktrees/`), verify ignore coverage before worktree creation. Add ignore entries when missing.

## Operating Principles

- Keep one feature per worktree and one branch per worktree.
- Keep branch names predictable and slug-safe.
- Keep PRs small and short-lived.
- Rebase frequently to reduce conflict depth.
- Run quality checks before PR creation and before merge.
- Avoid destructive git actions.

## Command Resources

Use bundled scripts in `scripts/` for deterministic execution:

- `scripts/preflight-check.sh` - repository, branch, remote, and `gh` readiness checks.
- `scripts/create-worktree.sh` - branch + worktree creation with ignore safeguards.
- `scripts/sync-worktree.sh` - fetch + rebase branch onto base branch.
- `scripts/generate-pr-body.sh` - compatibility-aware PR body generation.
- `scripts/open-pr.sh` - push and create or reuse pull requests.
- `scripts/merge-pr.sh` - merge pull request with checks and queue support.
- `scripts/cleanup-worktree.sh` - safe worktree removal and prune.
- `scripts/run-feature-flow.sh` - orchestration wrapper for preflight to PR (and optional merge).
- `scripts/windows/run-feature-flow.cmd` - Windows wrapper for safer script invocation.
- `scripts/windows/doctor.cmd` - Windows environment diagnostics for `git`, `gh`, and `bash`.

All core scripts support machine-readable output using `--json`.

## One-Command Orchestration

Run the complete flow from the repository root:

```bash
bash .agents/skills/worktree-feature-execution/scripts/run-feature-flow.sh \
  --feature "add billing retries" \
  --base "current-branch" \
  --pr-base "main" \
  --prefix "feat" \
  --summary "Improve retry reliability for transient payment failures"
```

Optional flags:

- `--draft` to create draft PR.
- `--merge --queue --merge-method squash` to queue merge after PR creation.
- `--no-pr` to stop after worktree creation and sync.
- `--setup auto|none|"<custom command>"` to control setup behavior.
- `--issue <number>` to append closing issue reference in PR body.

Windows invocation example:

```cmd
.agents\skills\worktree-feature-execution\scripts\windows\run-feature-flow.cmd --feature "add billing retries"
```

## Standard Workflow

### 1) Preflight

Run:

```bash
bash .agents/skills/worktree-feature-execution/scripts/preflight-check.sh
```

Verify:

- Current directory belongs to a git repository.
- Base branch can be resolved.
- `origin` remote exists.
- `gh` is installed and authenticated.
- `git` and `gh` executable paths resolve correctly.
- Current shell context is reported for diagnostics.

If authentication or permissions fail, stop and report the blocking condition.

### 2) Create Isolated Worktree

Run:

```bash
bash .agents/skills/worktree-feature-execution/scripts/create-worktree.sh \
  --feature "add billing retries" \
  --base "current-branch" \
  --prefix "feat"
```

Behavior:

- Resolve base branch from current branch when `--base current-branch`.
- Resolve worktree root using priority order.
- Ensure root is gitignored when local to repository.
- Create `feat/<slug>` branch if missing, or reuse existing branch.
- Create worktree path `<root>/<slug>`.

Useful flags:

- `--no-gitignore-edit` to fail instead of mutating `.gitignore`.
- `--print-ignore-patch` to display the exact ignore line before apply.

### 3) Implement Feature

Perform implementation inside the created worktree path only. Keep scope aligned with the feature statement.

Recommended checks:

- Type checks
- Unit/integration tests
- Build command

Record notable changes and compatibility concerns for PR body.

### 4) Sync With Base Branch

Run in the worktree:

```bash
bash .agents/skills/worktree-feature-execution/scripts/sync-worktree.sh \
  --base "main"
```

Behavior:

- Fetch remote updates.
- Rebase feature branch on top of latest base branch.
- Stop on conflicts and report exact conflict files.

### 5) Open Pull Request

Run in the worktree:

```bash
bash .agents/skills/worktree-feature-execution/scripts/open-pr.sh \
  --base "main" \
  --title "feat: add billing retry policy" \
  --body-file ".git/PR_BODY.md"
```

Behavior:

- Push branch with upstream tracking if needed.
- Reuse open PR when one already exists.
- Auto-generate PR body file when missing.
- Create PR when missing.
- Validate PR body is non-empty after create/update.
- Return PR URL.

### 5a) Generate PR Body Template

Run in the worktree:

```bash
bash .agents/skills/worktree-feature-execution/scripts/generate-pr-body.sh \
  --base "main" \
  --feature "add billing retries" \
  --risk "medium" \
  --output ".git/PR_BODY.md"
```

Behavior:

- Build compatibility-aware PR content from git diff context.
- Include commit and changed-file counts against base.
- Add risk and rollback sections.

### 6) Merge Pull Request

Run:

```bash
bash .agents/skills/worktree-feature-execution/scripts/merge-pr.sh \
  --pr "<url-or-number>" \
  --method "squash" \
  --queue
```

Behavior:

- Validate merge method.
- Confirm checks status.
- Queue merge (`--auto`) when requested.
- Delete remote branch after merge when supported.

### 7) Cleanup

Run:

```bash
bash .agents/skills/worktree-feature-execution/scripts/cleanup-worktree.sh \
  --path ".worktrees/add-billing-retries"
```

Behavior:

- Refuse cleanup when uncommitted changes exist unless `--force`.
- Remove worktree and prune stale metadata.

## Multi-Agent Coordination

Use one worktree per agent. Assign explicit ownership boundaries by directory, module, or capability.

Execution order:

1. Merge foundational PRs first.
2. Rebase dependent PRs after each upstream merge.
3. Re-run checks after every rebase.
4. Merge dependent PRs only after compatibility verification.

For shared contracts (API/schema/event payloads), include compatibility notes in PR body and require contract tests.

### Serialization Rule

Do not run mutating git commands in parallel. Serialize all operations that write git state (`add`, `commit`, `stash`, `checkout`, `worktree add/remove`, `rebase`, `merge`). Parallelize read-only commands only.

## Windows Compatibility

Prefer Git Bash for all `.sh` scripts on Windows. In restricted runners, use explicit wrapper commands under `scripts/windows/`.

Recommended sequence:

1. Run `scripts/windows/doctor.cmd`.
2. Fix PATH for `git`, `gh`, and `bash` if missing.
3. Run `scripts/windows/run-feature-flow.cmd`.

When `bash` is not in PATH, set `GIT_BASH` to an explicit `bash.exe` location.

### PATH-Degraded `cmd` Sessions

If `git --version` or `where git` returns "not recognized", treat this as a broken `PATH` session.

Run `scripts/windows/doctor.cmd --json`, resolve absolute executables, and execute with explicit paths only:

- `git`: `%LOCALAPPDATA%\Programs\Git\cmd\git.exe`, then `%ProgramFiles%\Git\cmd\git.exe`
- `bash`: `%LOCALAPPDATA%\Programs\Git\bin\bash.exe`, then `%ProgramFiles%\Git\bin\bash.exe`
- `gh`: `%USERPROFILE%\scoop\shims\gh.exe`, then `%ProgramFiles%\GitHub CLI\gh.exe`
- `bun`: `%USERPROFILE%\.bun\bin\bun.exe`

Set `GIT_EXE`, `BASH_EXE`, `GH_EXE`, and `BUN_EXE`, then run all workflow steps with those explicit binaries.

If any required executable cannot be resolved, stop and report the missing tool plus checked paths.

## Manual Fallback Checklist

Use this fallback path when orchestration cannot run end-to-end:

1. Run preflight.
2. Create worktree.
3. Sync worktree with base branch.
4. Generate PR body.
5. Open PR using `--body-file`.
6. Merge only after checks pass.
7. Clean up worktree.

## Edge Cases

### Detached HEAD

Resolve base branch using `origin/HEAD` fallback. Stop when neither current branch nor remote default branch can be resolved.

### Existing Branch Already Checked Out

If branch is already attached to another worktree, stop and select a new branch name or reuse that worktree.

### Worktree Path Exists

Refuse creation when target path exists and is non-empty.

### Missing Ignore Rule

Append missing root ignore entry to `.gitignore` before creating local worktree roots.

### Diverged Branches

Require rebase and conflict resolution before PR creation.

### Existing PR

Return existing PR URL instead of creating duplicate PR.

### CI Failures

Do not merge. Report failed checks and keep worktree active for remediation.

### Merge Queue Enabled

Use `--queue` flow and avoid direct merge bypass.

### Permission Errors

Stop and report required `gh` scope or repository role.

### PATH-Degraded Shell

On Windows `cmd`, if command discovery is unavailable, bypass PATH-dependent invocations and run with resolved absolute executable paths.

## Red Flags

Never:

- Run `git reset --hard` or force-push to `main`.
- Merge with known failing checks.
- Delete worktree containing uncommitted work without explicit force signal.
- Create worktrees in unignored project-local directories.

Always:

- Run preflight before worktree creation.
- Run sync before PR and before merge.
- Surface PR URL and merge status.
- Clean up merged worktrees.

## Additional Resources

Reference files:

- `references/branch-naming.md`
- `references/conflict-playbook.md`
- `references/merge-policy.md`
- `references/pr-template.md`
- `CHANGELOG.md`
- `VERSION`
