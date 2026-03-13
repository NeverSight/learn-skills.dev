---
name: issue-driven
description: Issue-driven development workflow. Manage GitHub Issues as SSOT for all dev tasks — create, worktree, code review, PR, and status tracking.
metadata:
  short-description: Issue-driven dev workflow
---

# Issue-Driven Development Workflow

Manage the full lifecycle of development tasks through GitHub Issues.

## Prerequisites

Before any subcommand, verify:
1. Current directory is a Git repository (`git rev-parse --is-inside-work-tree`)
2. `gh` CLI is authenticated (`gh auth status`)
3. A remote origin exists (`git remote get-url origin`)

If check 1 or 2 fails, inform the user and stop.
If check 3 fails (no remote), suggest the user create a remote repository first (e.g. `gh repo create`), but do NOT stop — let the user decide whether to proceed or set up remote first.

## Proactive Trigger Rules

- **有 remote 的 Git 项目**：当用户开始 feature/bug/refactor 任务时，默认走 issue-driven 流程。无需用户显式调用 `/issue`，主动提示并引导。
- **无 remote 的 Git 项目**：建议用户创建 remote（`gh repo create`），但不强制阻断。用户可选择先创建 remote 再走 issue 流程，或跳过 issue 流程直接开发。
- **非 Git 项目**：不触发 issue-driven 流程。

## Usage

`/issue <subcommand>`

| Subcommand | Description |
|------------|-------------|
| `create` | Create a new GitHub Issue with labels |
| `update` | Update Issue body with current plan |
| `worktree` | Create worktree + branch for an Issue |
| `review code` | Send code diff to Codex for review |
| `pr` | Create PR linked to Issue |
| `status` | Show open Issues with branches/PRs |

## Integration with CC Plan Mode

Issue 生命周期步骤必须编排进 CC plan 的执行步骤中，利用时间相位差消除衔接空隙。

**标准 plan 模板**（plan 中必须包含 issue 步骤）：

```markdown
## Plan: {task title}

### Step 1 — Create Issue
- `/issue create` — 创建 GitHub Issue，记录任务背景和目标

### Step 2 — Design & Plan
- 在 plan 文件中完成方案设计
- `/issue update` — 将方案同步到 Issue body

### Step 3 — Setup Worktree
- `/issue worktree` — 创建 worktree + branch，label 自动切换到 in-progress

### Step 4 — Implementation
- 在 worktree 中完成开发

### Step 5 — Code Review
- `/issue review code` — 发送 diff 给 reviewer

### Step 6 — Create PR
- `/issue pr` — 创建 PR 并关联 Issue
```

**关键原则**：
- Plan 审批（CC plan mode 的 ExitPlanMode）和 Issue 创建是两个独立动作，plan 获批后按步骤顺序执行
- `planning → in-progress` 直接过渡，无需额外的 plan review 环节（plan review 由 CCB Peer Review Framework 在 CLAUDE.md 中统一管理）
- Issue 是 SSOT（Single Source of Truth），plan 内容通过 `/issue update` 同步到 Issue body

## Label Convention

Ensure these labels exist in the repo (create if missing via `gh label create`):

| Label | Description |
|-------|-------------|
| `status/planning` | Issue is being planned |
| `status/in-progress` | Development in progress |
| `type/feature` | New feature |
| `type/bug` | Bug fix |
| `type/refactor` | Refactoring |
| `type/docs` | Documentation |

## Branch Naming

- Pattern: `issue-{N}-{slug}` (e.g. `issue-42-add-auth`)
- Slug: title converted to kebab-case, truncated to 30 chars
- One Issue can have multiple branches (1:N)

## Subcommand Details

### `/issue create`

1. Run prerequisite checks (Git repo, gh auth, remote).
2. Ask the user for:
   - Task type: `feature` / `bug` / `refactor` / `docs`
   - Title (concise, imperative)
   - Background description (what and why)
3. Generate Issue body using this template:

```markdown
## 背景
{user-provided background}

## 目标
{inferred from background, confirm with user}

## 方案
_待规划_

## 验收标准
_待定义_
```

4. Display the full Issue preview to the user and wait for confirmation.
5. Ensure required labels exist: `gh label create "status/planning" --force` and `gh label create "type/{type}" --force`.
6. Create the Issue: `gh issue create -t "{title}" -b "{body}" -l "status/planning,type/{type}"`.
7. Record the Issue number for subsequent commands in this session.

### `/issue update`

1. If no Issue number in session context, ask the user for it.
2. Find the current plan file — search in order:
   - `ls -t .claude/plans/*.md 2>/dev/null | head -1`
   - `ls -t docs/plans/*.md 2>/dev/null | head -1`
   - If no plan file exists in either location, ask the user to provide plan content directly.
3. Read the plan content.
4. Fetch current Issue body: `gh issue view {N} --json body -q .body`.
5. Replace the `## 方案` and `## 验收标准` sections with plan content.
6. Update the Issue: `gh issue edit {N} -b "{updated_body}"`.
7. Confirm success to the user.

### `/issue worktree`

1. If no Issue number in session context, ask the user for it.
2. Fetch Issue title: `gh issue view {N} --json title -q .title`.
3. Generate slug: convert title to kebab-case, truncate to 30 chars.
4. Branch name: `issue-{N}-{slug}`.
5. Determine base branch: `git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@'` (fallback to `main`).
6. Create worktree: `git worktree add -b {branch} ../{branch} {base}`.
7. Update label: `gh issue edit {N} --remove-label "status/planning" --add-label "status/in-progress"`.
8. Inform user of the worktree path and suggest `cd ../{branch}`.

### `/issue review code`

1. If no Issue number in session context, ask the user for it.
2. Determine base branch (same logic as worktree).
3. Generate diff: `git diff {base}...HEAD`.
4. If diff is empty, inform user there are no changes to review.
5. Construct the review request message:

```
[CODE REVIEW REQUEST]

Issue #{N}: {title}
Branch: {current branch}

--- CHANGES START ---
{diff output}
--- CHANGES END ---
```

6. Send to reviewer via `/ask codex` with the above message.
7. Follow the Async Guardrail — if output contains `[CCB_ASYNC_SUBMITTED`, end turn immediately.
8. When Codex response arrives, parse the JSON scores.
9. Display scores as a summary table with pass/fail status.

### `/issue pr`

1. If no Issue number in session context, ask the user for it.
2. Get current branch name: `git branch --show-current`.
3. Verify branch follows `issue-{N}-*` pattern.
4. Determine base branch (same logic as worktree).
5. Ask user: "Is this the final PR for Issue #{N}?" (yes/no).
   - Yes → PR body includes `Closes #{N}`
   - No → PR body includes `Refs #{N}`
6. Generate PR title from branch name or ask user.
7. Create PR: `gh pr create -B {base} -t "{title}" -b "{body}"`.
8. Display the PR URL to the user.

### `/issue status`

1. Run prerequisite checks.
2. List open issues with status labels:
   - `gh issue list --label "status/planning" --json number,title,labels --limit 20`
   - `gh issue list --label "status/in-progress" --json number,title,labels --limit 20`
   - Merge results.
3. For each issue, find associated branches: `git branch -a --list "*/issue-{N}-*"`.
4. For each issue, find associated PRs: `gh pr list --search "issue-{N}" --json number,title,state,url`.
5. Display a formatted table:

```
# | Title | Status | Branch(es) | PR(s)
```

## Issue Granularity Rules

- **Small tasks** (single change): Plan = Issue, 1:1 mapping. One Issue, one branch, one PR.
- **Large tasks** (multiple independent steps): Create an epic Issue as the parent.
  - Epic Issue body contains a task list with checkboxes tracking sub-issues.
  - Each step becomes a sub-issue with its own worktree/branch/PR.
  - Sub-issue PRs use `Refs #{epic}`, the final one uses `Closes #{epic}`.
  - All sub-issues completed → close the epic.

## Non-Git Projects

If the current directory is not a Git repository, inform the user:
> "Issue-driven workflow requires a Git repository. Current directory is not a Git repo."

Do not proceed with any subcommand.
