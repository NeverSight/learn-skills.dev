---
name: github-sync
description: 规范 GitHub 操作与 Taskmaster 任务同步规则，确保所有 GitHub 动作与任务管理同步。
---

# GitHub 同步技能

## 核心原则

> **"所有 GitHub 操作完成后必须同步更新 Taskmaster"**

---

## 同步规则表

| GitHub 操作 | Taskmaster 动作 | 优先级 |
|-------------|-----------------|--------|
| 创建 Issue | 创建对应任务 | P0 |
| 关闭 Issue | 更新任务状态为 done | P0 |
| 合并 PR | 更新任务状态为 done | P0 |
| 创建 Commit | 记录任务进度（可选） | P1 |

---

## 场景：创建 Issue

```bash
# 1. 创建 Issue
gh issue create --title "功能描述" --body "详细描述"

# 2. 创建 Taskmaster 任务
task-master add-task --prompt="功能描述 (Issue #123)

详细说明...

Ref: https://github.com/lwpk110/sprout-chat/issues/123" --priority=P1

# 3. 提交同步记录
git commit --allow-empty -m "docs: Issue #123 已同步到 Taskmaster"
```

---

## 场景：关闭 Issue

```bash
# 1. 关闭 Issue
gh issue close 123

# 2. 更新 Taskmaster 任务状态
task-master set-status --id=LWP-X --status=done

# 3. 提交关闭记录
git commit --allow-empty -m "docs: Issue #123 已关闭，任务完成"
```

---

## 优先级映射

| Issue 标签 | 任务优先级 |
|------------|-----------|
| bug, critical | P0 |
| enhancement, feature | P1 |
| documentation | P2 |
| backlog | P3 |

---

## 相关技能
- `git-commit` - 提交信息规范
- `tdd-cycle` - TDD 开发流程
