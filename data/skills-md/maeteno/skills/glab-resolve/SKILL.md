---
name: glab-resolve
description: Resolve GitLab MR review threads interactively. Use when the user wants to address MR comments, fix review feedback, resolve discussion threads, or work through code review issues on a GitLab merge request. Triggers on requests like "resolve MR comments", "fix review feedback", "address MR threads", "/glab-resolve", or "/glab-resolve <MR_ID>".
---

# GitLab Resolve

## Overview

逐一处理 GitLab MR 中的评论线程，按难易程度分类后规划执行任务，用户确认计划后按任务顺序依次解决并提交。

## Workflow

### Step 1: 确认 MR 与当前分支一致

获取当前分支并与目标 MR 的源分支对比：

```bash
# 获取当前分支
git branch --show-current

# 获取 MR 的源分支
glab mr view <MR_ID> --output json | jq -r '.source_branch'
```

若当前分支与 MR 的源分支**不一致**，提示用户：
- 确认 MR ID 是否正确
- 或切换到对应分支：`git checkout <source-branch>`

用户确认后再继续。

### Step 2: 获取 MR 评论

使用当前 skill 的 `scripts` 目录中的 `fetch_discussions.sh <MR_ID>` 拉取所有未处理的讨论线程, 执行脚本时不要输出结果到控制台。

脚本自动获取 URL 编码的项目路径并调用 `glab api --paginate`，输出过滤后的讨论线程 JSON 列表。

过滤条件：首条 note 的 `type == "DiffNote"`、`resolvable == true`、`resolved == false`，只保留未解决的 diff 评论线程。每条线程包含 `discussion_id`（用于后续 API resolve）、`author`、`comment`、`position`（文件与行号）、`replies`（回复列表）。

**前置依赖**：需安装 `glab`、`jq`、`uv`（用于执行 Python 脚本）。

#### 获取评论的错误和结果处理

- 若未提供 MR ID，询问用户。
- 若命令失败，提示用户检查 `glab auth status` 和项目权限。
- 如果获取到 JSON 列表，继续下一步。
- 如果是空列表，提示用户 MR 中没有未处理的 diff 评论线程，结束流程。

### Step 3: 分析并分类问题

按难度分类：

| 难度 | 描述 | 示例 |
|------|------|------|
| 简单 | 直接回答或小改动 | typo、添加注释、重命名 |
| 中等 | 需要分析，涉及逻辑调整 | 函数修改、逻辑重构 |
| 复杂 | 需深入分析，可能影响架构 | 设计变更、跨模块改动 |
| 其他 | 无需代码修改 | 已过期、需继续讨论 |

### Step 4: 规划执行任务

难度和合并是两个独立维度：

- **合并只能发生在同一难度内**，跨难度问题不可合并
- 将同一难度下关联紧密的问题合并为一个执行任务（如同一文件的多个 typo、同一模块的相关修改）
- **复杂问题默认不合并**，除非关联极为明显且改动范围确定
- commit 时机由用户决定，可单个任务提交，也可多个任务完成后统一提交

### Step 5: 展示分类概览

按难度分组展示所有问题，供用户了解全貌：

**简单问题**

| # | Thread ID | 问题摘要 | 解决方案 |
|---|-----------|---------|---------|
| 1 | #<id> | <摘要> | <方案，如：直接修正、添加注释> |

**中等问题**

| # | Thread ID | 问题摘要 | 解决方案 |
|---|-----------|---------|---------|
| 1 | #<id> | <摘要> | <方案，如：需要深入分析、重构逻辑> |

**复杂问题**

| # | Thread ID | 问题摘要 | 解决方案 |
|---|-----------|---------|---------|
| 1 | #<id> | <摘要> | <方案，如：需继续讨论、涉及架构调整> |

**其他问题**

| # | Thread ID | 问题摘要 | 解决方案 |
|---|-----------|---------|---------|
| 1 | #<id> | <摘要> | <方案，如：已过期、无需处理> |

所有难度组必须展示，无对应问题时表格内容显示一行 `- | - | 暂无 | -`。

### Step 6: 展示执行任务计划

将问题组织为有序的执行任务（Task），每个 Task 修复完成后可提交，也可跳过等多个 Task 完成后统一提交：

| 任务 | 难度 | 包含问题 | 修复说明 |
|------|------|---------|---------|
| Task 1 | 简单 | #12, #15 | 修正两处 typo |
| Task 2 | 简单 | #18 | 添加缺失注释 |
| Task 3 | 中等 | #22 | 重构校验逻辑 |
| Task 4 | 复杂 | #31 | 调整错误处理架构 |
| Task 5 | 复杂 | #35 | 优化模块依赖关系 |

**展示后等待用户确认或调整**，用户可以：
- 拆分某个 Task（将合并的问题分开）
- 合并某些 Task（前提：同一难度）
- 调整执行顺序

### Step 7: 按任务顺序循环执行

用户确认计划后，**严格按 Task 顺序逐一执行，不得跳跃或乱序**。立即从 Task 1 开始，每个 Task 无论是第几个，都必须独立展示方案并等待用户确认后才能执行——Step 6 的整体计划确认不能替代每个 Task 的执行确认。

#### 每个 Task 的执行流程

1. 展示当前 Task 的问题详情和建议的解决方案
2. **等待用户响应**，用户可以：
   - 直接确认方案，进入执行
   - 对方案提出细节调整或进行讨论，直到用户明确确认后才执行
   - 跳过当前 Task
3. 用户确认后，实施修改
4. **验证修改是否正确**（以下均通过才可继续）：
   - 编译通过：确保项目可以正常构建
   - 单元测试通过：运行受影响模块的相关测试
   - 若验证失败，修复问题后重新验证，不得跳过此步骤
5. 使用 `git-commit` skill 生成 commit 信息；若不可用，直接运行 `git commit`
   - commit 内容为**当前仓库所有未提交的变更**（可能包含多个 Task 的修改）
   - Footer 列出本次 commit 涵盖的所有 thread：`Resolve #<id1>, #<id2>, #<id3>`
   - 示例：`Resolve #12, #15, #18 修正 typo 并添加注释`
6. **等待用户确认是否提交**：
   - 确认：执行提交，再展示下一个 Task
   - 跳过：不提交，直接继续下一个 Task 的修复，累积变更留待后续统一提交

**严禁在完成修复或 commit 后自动跳入下一个 Task 的修复执行。每个 Task 必须经过用户明确确认方案后才能开始实施。**

### Step 8: 展示执行汇总

所有 Task 执行完毕后，展示汇总表格：

| 任务 | 难度 | 包含问题 | 状态 | 备注 |
|------|------|---------|------|------|
| Task 1 | 简单 | #12, #15 | ✅ 已完成 | commit abc1234 |
| Task 2 | 简单 | #18 | ⏭️ 已跳过 | 用户跳过 |
| Task 3 | 中等 | #22 | ✅ 已完成 | commit def5678 |
| Task 4 | 复杂 | #31 | ✅ 已完成 | commit ghi9012 |

**汇总统计：**
- 已完成：X 个 Task（涉及 N 个问题）
- 已跳过：X 个 Task（涉及 N 个问题）
- 总计：X 个 Task

展示汇总后，询问用户是否对本次所有变更进行整体 code review：

> 本次共完成 X 个 Task 的修改，是否需要对所有变更做一次整体 code review？

若用户确认，使用 `git diff <first-commit>^..HEAD` 展示本次全部改动，并逐文件进行 review 分析。

## 错误处理

- `glab` 命令失败：提示检查 `glab auth status` 和网络连接
- 无未解决线程：告知用户所有线程已解决
- 权限不足：提示用户确认是否有该项目的访问权限
