---
name: pcp-sprint-review
description: Sprint 结束后的 backlog 回顾。逐条询问用户是否将 backlog 项加入下一个 sprint，通过 pcp_promote / pcp_dismiss 处理每项。每条消息只问一个问题。
license: MIT
compatibility: opencode
---

## 依赖

需要 PCP OpenCode 插件（`pcp.ts`）提供 `pcp_backlog`、`pcp_promote`、`pcp_dismiss` 工具。
若尚未安装，先加载 skill `pcp-setup`。

---

## 目的

Sprint 完成后，逐条回顾 backlog 中的待处理项，决定每项的命运：
- **加入下一个 sprint** → `pcp_promote`
- **留待以后** → 跳过，保留在 backlog
- **永久忽略** → `pcp_dismiss`

---

## 前置条件

- 当前 sprint 已完成（`pcp_done` 或 git commit 触发）
- 调用 `pcp_backlog` 确认有待回顾项

---

## 执行步骤

### Step 1：获取 backlog

调用 `pcp_backlog()` 获取所有 pending 项。

若 backlog 为空 → 告知用户「Backlog 为空，可以直接开始下一个 sprint。」并结束。

---

### Step 2：宣布回顾开始

输出：
```
📋 Sprint 回顾开始，共 N 项待处理。逐条过一遍，每项你来决定。
```

---

### Step 3：逐条询问（每条消息只问一个问题）

对每个 pending backlog 项，格式如下：

```
[B001] 添加 OAuth 支持
（若有 detail 则显示）

要怎么处理？
  A) 加入下一个 sprint（立即开始做）
  B) 留着，以后再说
  C) 忽略，不做了
```

等待用户回复，然后执行：

| 用户选择 | 操作 |
|---------|------|
| A / 是 / 加入 | `pcp_promote(backlog_id)` |
| B / 以后 / 留着 | 跳过，不调用任何工具 |
| C / 忽略 / 不做 | `pcp_dismiss(backlog_id)` |

---

### Step 4：回顾结束，展示汇总

所有项处理完后输出：

```
✅ 回顾完成！

加入本次 sprint: N 项（T00X, T00Y...）
留待以后:       N 项
已忽略:         N 项
```

若有 promoted 项（加入 sprint 的）：
- 提示用户「已加入 sprint 作为子任务，可以开始工作了。」

若没有 promoted 项：
- 提示用户「可以调用 pcp_start 开始下一个 sprint 了。」

---

## 异常处理

| 情况 | 处理 |
|------|------|
| 用户说「全部加入」 | 依次调用 `pcp_promote` 处理所有 pending 项 |
| 用户说「全部忽略」 | 依次调用 `pcp_dismiss` 处理所有 pending 项 |
| 用户说「先跳过」 | 停止回顾，保留所有未处理项在 backlog |
| `pcp_promote` 失败（无活跃 sprint）| 先 `pcp_start` 创建新 sprint，再重试 |

---

## 示例

```
Agent: 📋 Sprint 回顾开始，共 3 项待处理。

[B001] 添加 OAuth 登录支持
要怎么处理？A) 加入下一个 sprint  B) 留着  C) 忽略

User: A

Agent: ✅ B001 已加入 sprint 作为子任务 [T006]

[B002] 优化首页加载速度（detail: 目前首页 LCP > 3s）
要怎么处理？A) 加入下一个 sprint  B) 留着  C) 忽略

User: B

Agent: 好的，B002 留待以后。

[B003] 重构日志模块
要怎么处理？A) 加入下一个 sprint  B) 留着  C) 忽略

User: C

Agent: ❌ B003 已忽略。

✅ 回顾完成！
加入本次 sprint: 1 项（T006）
留待以后:       1 项
已忽略:         1 项

B001 已作为子任务加入，可以开始工作了。
```
