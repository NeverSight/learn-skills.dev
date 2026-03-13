---
name: cx-fix
description: >
  CX 工作流 — Bug 修复。
  当用户提到"修 bug"、"fix"、"有个问题"、"报错"、"不工作"、
  "出了问题"、"修复"、"debug" 时触发。
  轻量流程：调查→定位→修复→测试→提交。
---

# cx-fix — Bug 修复工作流

## 概述

cx-fix 是一个轻量级的 Bug 修复流程，专为快速问题诊断和修复设计。无需完整的需求→设计→计划流程，直接从问题出发、修复、验证、提交。

---

## 工作流程（6 步）

### Step 1: 理解 (Understand)

- 读取用户的 Bug 描述
- 了解：哪个功能受影响？何时出现？有错误日志吗？
- **协作模式特殊处理**：
  - `collab` 或 `full` 模式 → 用 `gh issue view <issue-num>` 读取完整 Issue 信息
  - `off` 或 `local` 模式 → 仅依赖用户当前描述
- 保存初步理解到临时记录

### Step 2: 调查 (Investigate)

- 启动 **Explore 子代理** 并行扫描：
  - 关键字搜索：错误堆栈、日志关键词、受影响的文件
  - 目标：追踪错误调用链、找到根因文件
  - 返回：相关文件清单、关键代码片段、测试位置
- Claude 分析子代理结果，定位根因

### Step 3: 修复 (Fix)

- 基于根因，编写修复代码
- 遵循项目规范（从 CLAUDE.md 读取）
- 修复原则：
  - **最小化改动**：仅修复根因，不做额外重构
  - **向后兼容**：避免破坏现有 API
  - **测试友好**：便于验证修复有效

### Step 4: 测试 (Test)

- 运行项目已有的测试套件：
  - 检查测试框架：`npm test` / `pytest` / `cargo test` / `go test`
  - 优先运行与修复相关的测试模块
  - 必须全部通过
- 如果新增测试，执行新增部分

### Step 5: 提交 (Commit)

- 使用 **Conventional Commits** 格式：
  ```
  fix(scope): brief description

  Detailed explanation (optional)
  ```
- 示例：`fix(auth): handle null token in login flow`
- `git add` + `git commit`
- (可选) `git push` 如果配置中启用

### Step 6: 闭环 (Close Loop)

根据 GitHub 同步模式决定后续行为：

| 模式 | 行为 |
|------|------|
| `off` | 本地记录：保存 fix.md 到 `.claude/cx/fixes/{dev_id}-{fix_slug}/` |
| `local` | 本地记录 + 创建本地 fix.md |
| `collab` / `full` | **关闭 GitHub Issue**：`gh issue close <issue-num>` |

最后：发送桌面通知（Notification hook）

---

## 输出物

### 修复记录文件

保存到：`.claude/cx/fixes/{dev_id}-{fix_slug}/fix.md`

```markdown
# Bug Fix: {bug_title}

## Issue
- 问题描述
- 影响范围
- 复现步骤

## Root Cause
- 根因分析
- 关键代码文件

## Solution
- 修复方案
- 关键改动（代码片段）

## Testing
- 运行的测试命令
- 测试结果（通过/失败）
- 新增测试（如有）

## Commit
- 提交 SHA
- 提交信息

## Mode
- 同步模式：{off|local|collab|full}
- 是否关闭 Issue：{yes|no}

---
timestamp: {YYYY-MM-DD HH:mm:ss}
```

### 不更新 CLAUDE.md

Bug 修复太轻量，不值得在 CLAUDE.md 中记录。仅保存本地 fix.md 记录。

---

## 关键配置

从 `.claude/cx/config.json` 读取：

- `github_sync`：同步模式（off/local/collab/full）
- `developer_id`：开发者标识（用于文件夹前缀）
- `hooks.notification`：是否启用桌面通知

---

## 异常处理

| 情况 | 处理 |
|------|------|
| 用户未提供充分信息 | 追问："能否提供错误日志或重现步骤？" |
| 测试失败 | 显示失败日志，询问："要继续修复还是回滚？" |
| Explore 子代理未找到相关文件 | 扩大搜索范围，提示用户手动指定 |
| Issue 不存在（collab/full 模式） | 降级到本地模式，提示用户 |

---

## Tips

1. **速度优先**：cx-fix 设计用于快速迭代，不需要漫长的设计过程
2. **保留上下文**：fix.md 记录便于后期追溯改动原因
3. **并行扫描**：充分利用 Explore 子代理加速根因定位
4. **测试守卫**：测试必须通过，否则不提交
5. **桌面通知**：修复完成后会收到系统通知
