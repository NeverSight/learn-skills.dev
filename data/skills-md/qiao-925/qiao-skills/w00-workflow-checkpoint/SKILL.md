---
name: w00-workflow-checkpoint
description: Workflow Checkpoint 基础能力（聚焦存档与读档）：在 GitHub Issues 中记录 checkpoint 进展并读档上下文。适用于任意 workflow 阶段，支持自动触发与手动高频调用。关键词：存档、读档、checkpoint、issue。
metadata:
  type: procedural
---

# W00 Workflow Checkpoint（仅存档 + 读档）

> 这是独立于 `w01~w05` 的基础能力层，只负责两件事：**存档（checkpoint）** 和 **读档（resume）**。

---

## ⚠️ 核心强制要求

### 职责边界（严格）

- `w00-workflow-checkpoint` **只负责**：
  - 存档：写入/更新 checkpoint
  - 读档：读取并恢复最近 checkpoint 上下文
- `w00-workflow-checkpoint` **不负责**：
  - 初始化 issue（由 `w01/w02` 等主流程阶段触发）
  - 关闭任务（由 `w05-task-closure` 触发）

### 术语约定（避免歧义）

- **存档**：默认指 checkpoint 更新（不是关闭任务）
- **读档**：默认指恢复 checkpoint 上下文
- **归档/收尾**：由 `w05-task-closure` 处理，不属于本 skill

### 触发方式（自动 + 手动）

- **自动触发**：主流程阶段在关键节点自动调用本 skill 执行“存档/读档”。
- **手动触发（高频）**：用户说 `存档`、`读档` 时触发。
- **额外条件（存档兜底）**：执行“存档”时，若上下文无可更新 issue（未提供 `#issue`、无绑定 `Issue #`、候选 0 条），允许直接创建 issue 并写入首个 checkpoint（创建并存档）。

---

## 管理对象

- 仓库：无固定默认值，按上下文解析（用户显式指定 > 当前 Git 仓库远程 > 用户选择）
- 示例仓库：`qiao-925/qiao-skills`（仅示例，不作为默认值）
- 任务标题：`[<repo>] <目标短句>`（示例：`[qiao-skills] 优化 W00 自动存档触发`）
- 仓库名写法：沿用仓库原始定义，不额外做大小写转换
- 标签：`status:*` + `type:*` + `repo:*` + `wf:*`（可选：`term:*`）
- `wf:*` 规范：使用完整阶段名（示例：`wf:w02-task-planning`）
- 最小字段：`Goal / Next`

---

## AI Agent 行为要求

### 两个标准动作

1. **存档（checkpoint）**
   - 写入：`已完成 / 阻塞 / 下一步`
   - 若阻塞：状态建议更新为 `status:blocked`

2. **读档（resume）**
   - 读取 issue + 最近 checkpoint
   - 返回：最后状态 + 下一步

### 存档判定流程（更新哪一个）

1. 用户给出 `#issue`：直接更新该 issue。
2. 上下文有绑定 `Issue #`：更新该 issue。
3. 否则拉取当前仓库候选 issue（open + `repo:*`）。
4. 分支：
   - 0 条：触发下文“额外条件（创建并存档）”。
   - 1 条：自动选中并回报。
   - 2+ 条：列出 3~5 条候选让用户选择；未选择前不写入。

### 读档判定流程（读哪一个）

1. 用户给出 `#issue`：直接读档。
2. 上下文有绑定 `Issue #`：优先读档该 issue。
3. 否则列出当前仓库候选（优先 `status:in-progress` / `status:blocked`）。
4. 确定后输出读档摘要。

### 命令参考（统一使用 `gh issue` 原生命令）

- 存档：`gh issue comment <id> -R <owner>/<repo> --body "检查点 YYYY-MM-DD HH:mm\n已完成: ...\n阻塞: ...\n下一步: ..."`
- 读档：`gh issue view <id> -R <owner>/<repo> --comments`
- 候选列表：`gh issue list -R <owner>/<repo> --state open --label "repo:<repo>" --limit 20 --json number,title,updatedAt,labels,url`

### 输出规范

- 每次调用后返回：执行动作、Issue 编号/链接、当前状态、下一步建议。
- 多候选时必须先列候选并请求用户选择。

### 一行回执模板（强制）

- **存档回执**：
  - `已存档 #<issue> | 状态:<status> | 下一步:<next> | <url>`
- **读档回执**：
  - `已读档 #<issue> | 状态:<status> | 下一步:<next> | <url>`

字段规则：
- `status` / `next` 若缺失，使用 `-` 占位，不省略字段。
- 回执必须为单行，便于快速扫读与复制。

### 额外条件（创建并存档）

- 该条件仅在执行“存档”时生效，属于兜底分支，不改变“仅存档 + 读档”的主职责。
- 触发条件：未提供 `#issue`、无绑定 `Issue #`、候选 issue 为 0 条。
- 执行动作：创建 issue 后立即写入首个 checkpoint（不要求用户先手动初始化）。
- 回执：沿用存档回执模板（`已存档 #<issue> | 状态:<status> | 下一步:<next> | <url>`）。

---

## 与 W01~W05 的关系

- `w01/w02`：负责初始化或绑定 issue；随后调用 W00 存档。
- `w03/w04`：执行中高频调用 W00 存档/读档。
- `w05`：负责关闭任务；必要时调用 W00 补最后一次存档。

## 手动调用示例

- `存档`
- `读档`

> 交互规则：用户只需输入关键词；issue 选择、字段补齐与候选列表由系统自动判定并交互确认。

## 边界情况

- 未提供 issue 且无候选：触发“额外条件（创建并存档）”。
- 候选过多：仅展示最近更新的 3~5 条。
- 仓库上下文不明确：先要求用户确认 `<owner>/<repo>`，再执行存档/读档。
- `gh` 未登录：提示 `gh auth login`。
- 不使用 alias，统一按上文原生命令执行。
