---
name: devflow-jira
description: 操作内网 JIRA 系统（devflow CLI 版）。用于查询工单、创建任务、修改状态、工时记录、团队进度追踪等。当用户提到 JIRA、工单、任务、进度、团队工作情况时使用。
allowed-tools: Bash
argument-hint: "[任务描述]"
---

## JIRA 工具

调用方式：
```bash
kdev jira <命令> [参数]
```

所有输出均为 JSON，解读后用**中文**回复用户，不要把原始 JSON 直接展示。

---

## 鉴权

所有命令（`auth` 除外）在配置缺失时返回：
```json
{"error": "...", "code": "config"}
```

收到 `code: "config"` 或 `code: "auth"` 时，告知用户：
> 需要先在终端手动执行一次鉴权：`kdev jira auth`

**agent 不触发 auth**，引导用户自行执行后再继续。

---

## 命令列表

| 命令 | 参数 | 说明 |
|---|---|---|
| `whoami` | — | 返回当前登录用户信息，含 `.name`（username）字段 |
| `team-members` | — | 返回团队成员列表 |
| `team-add <username>` | — | 追加团队成员 |
| `team-remove <username>` | — | 移除团队成员 |
| `projects` | — | 列出所有可见项目 |
| `issue <key>` | — | 工单详情（含子任务、父任务） |
| `search <jql> [--max <n>]` | — | JQL 搜索，默认 50，上限 200 |
| `users <query>` | — | 按姓名搜索用户，获取 username |
| `permissions <key>` | — | 查询当前用户对工单的操作权限 |
| `transitions <key>` | — | 列出可用状态流转，返回 `[{id, name}]` |
| `transition <key> <transitionId>` | — | 按 ID 执行状态流转 |
| `create-fields <projectKey> [issueType]` | — | 查询创建所需字段及必填项 |
| `create <json>` | — | 创建工单，返回工单号和链接 |
| `update <key> <json>` | — | 更新工单字段 |
| `comment <key> <内容>` | — | 添加评论 |
| `delete <key>` | — | 删除工单（永久移除，内部先检查权限） |
| `worklog-get <key>` | — | 查看工时记录（预估/实际/剩余及明细），返回含 worklog id |
| `worklog-add <key> <时长> [日期]` | — | 记录用时，时长格式：`1w` `1d` `2h` `30m`，组合须空格分隔如 `1d 2h 30m`，不能连写如 ~~`2h30m`~~。 日期默认今天 |
| `worklog-delete <key> <worklogId>` | — | 删除工时记录，worklogId 从 worklog-get 获取 |
| `time-set <key> <预估> [剩余]` | — | 设置预估和剩余时间，时长格式同上 |

---

## 当前用户上下文

**JQL 查询**：直接使用 `currentUser()`，无需额外调用：
```bash
kdev jira search "assignee = currentUser() AND ..."
```

**创建/更新工单时填 assignee**：需要实际 username，调 `whoami` 取 `.name`：
```bash
kdev jira whoami   # → {"name": "zhangsan", "displayName": "张三", ...}
# 用 .name 字段填 assignee
```

**团队查询**：调 `team-members` 获取成员列表，拼入 JQL：
```bash
kdev jira team-members  # → [{username, displayName}, ...]
```

不要硬编码用户名。

---

## 查询场景参考

以下为常见场景的 JQL 策略，按用户意图灵活调整，不是硬规则：

| 场景 | JQL 策略 |
|---|---|
| 写日报 / 今天做了什么 / 今天的任务 | `assignee = currentUser() AND updated >= startOfDay() ORDER BY updated DESC` |
| 写周报 / 这周进度 / 本周的任务 | `assignee = currentUser() AND updated >= startOfWeek() ORDER BY updated DESC` |
| 我的待办 / 当前任务（无时间限定） | `assignee = currentUser() AND resolution = Unresolved AND updated >= -30d ORDER BY updated DESC` |
| 查全部（用户明确说"所有"/"包括旧的"）| 不加时间限制 |

**关键规则：有时间限定就不加 `resolution = Unresolved`**

用户说"今天"、"本周"、"昨天"等时间词时，查询的是"这段时间内有变动的工单"，**不区分是否已完成**。今天刚关掉的工单也是今天的工作成果，必须包含在内。

`resolution = Unresolved` 只用于没有时间语境的"我的待办"场景。

`updated` 涵盖状态变更、工时录入、评论、字段修改等所有操作，工单创建时间无关。

---

## 使用原则

### 修改状态

**必须两步走**，不做名称模糊匹配：

```bash
# 1. 获取可用流转列表
kdev jira transitions <key>
# 返回 [{id: "31", name: "待测试"}, ...]

# 2. 按 id 执行
kdev jira transition <key> <id>
```

状态名因项目而异，同名可能有多条，由 AI 根据用户意图匹配 id，歧义时向用户确认。

### 创建工单

```bash
# 1. 查询必填字段
kdev jira create-fields <projectKey> [issueType]

# 2. 创建
kdev jira create '{"project":{"key":"PROJ"},"summary":"...","issuetype":{"name":"任务"},"assignee":{"name":"username"}}'
```

- 用户未提供项目 key 时，先调 `projects` 按名称匹配，多个候选时列出让用户确认
- 用户未提供受理人时，询问是否分配给自己（调 `whoami` 取 `.name` 字段作为 username）
- 创建子任务需加 `"parent":{"key":"PROJ-123"}`，issuetype 为 `子任务`

### 查询我的工单

```bash
# 待办（默认过滤陈年工单）
kdev jira search "assignee = currentUser() AND resolution = Unresolved AND updated >= -30d ORDER BY updated DESC"
```

### 查询团队工单（按人分组）

```bash
# 1. 获取团队成员列表
kdev jira team-members
# → [{username: "lisi", ...}, {username: "wangwu", ...}]

# 2. 拼接 JQL（currentUser() 代表自己，无需单独调 me）
kdev jira search "assignee in (currentUser(), lisi, wangwu) AND resolution = Unresolved ORDER BY assignee, updated DESC" --max 200
```

在输出时按 assignee 字段分组展示。

### 团队进度汇总（今天/昨天/本周/指定日期）

```bash
# 先取团队成员，再拼 JQL（自己用 currentUser()）
kdev jira team-members
kdev jira search "assignee in (currentUser(), lisi, wangwu) AND updated >= startOfDay() ORDER BY assignee, updated DESC" --max 200
```

日期范围由 skill 计算，结果按人分组展示，包含工单状态和工时。

### 搜索工单

- 用户提供关键词：`text ~ "关键词"` 做全文搜索（标题、描述、评论）
- 用户提供模糊项目名：先调 `projects` 匹配，加 `project = KEY` 条件
- 复杂过滤直接拼 JQL

### 删除 vs 完成

- 用户说"删掉"→ `delete`（永久不可恢复，需权限）
- 用户说"关闭/完成/结束"→ 调 `transitions` 找终态，执行 `transition`
- 模糊时优先建议流转到终态，说明删除不可恢复

---

## 错误处理

| code | 处理方式 |
|---|---|
| `config` / `auth` | 提示用户运行 `kdev jira auth` |
| `not_found` | 告知对象不存在，确认 key/名称是否正确 |
| `permission` | 告知无权限，建议联系管理员 |
| `network` | 提示网络问题，建议检查内网连接 |
| `validation` | 说明参数格式问题，给出正确示例 |

---

## 安装说明

> **依赖**：需先全局安装 `@kmfe/devflow`（或本地 alias 指向构建产物）。
> 配置存储在 `~/.config/devflow/`，运行 `kdev jira auth` 完成初始化。
