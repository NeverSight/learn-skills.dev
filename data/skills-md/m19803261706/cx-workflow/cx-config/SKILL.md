---
name: cx-config
description: >
  CX 工作流 — 配置管理。查看、修改 config.json 中的配置字段，如 developer_id、
  github_sync 模式、代码审查开关、agent 团队模式、自动格式化等。
  触发词：配置、config、设置、修改配置、改模式。
  仅在用户明确调用 /cx-config 时执行。不要自动触发。
---

# cx-config — 工作流配置管理

## 概述

查看和修改 CX 工作流的核心配置，包括开发者标识、GitHub 同步模式、功能开关等。所有配置存储在 `${GIT_ROOT}/.claude/cx/config.json` 中。

## 执行流程

### Step 1: 定位配置文件

```bash
GIT_ROOT=$(git rev-parse --show-toplevel)
CONFIG_FILE="${GIT_ROOT}/.claude/cx/config.json"

if [ ! -f "$CONFIG_FILE" ]; then
  echo "❌ 工作流未初始化"
  echo "请先运行: /cx-init"
  exit 1
fi
```

### Step 2: 读取当前配置

```json
{
  "version": "2.0",
  "developer_id": "cx",
  "github_sync": "collab",
  "current_feature": "cx-payment",

  "agent_teams": false,
  "background_agents": false,
  "code_review": true,

  "auto_format": {
    "enabled": true,
    "formatter": "auto"
  },

  "hooks": {
    "session_start": true,
    "pre_compact": true,
    "prompt_refresh_interval": 5,
    "stop_verify": true,
    "post_edit_format": true,
    "notification": true,
    "permission_auto_approve": true
  }
}
```

### Step 3: 展示当前配置

```
⚙️ CX 工作流 — 当前配置

📋 基本配置
├─ developer_id: cx
├─ github_sync: collab
└─ current_feature: cx-payment

🤖 AI 功能
├─ agent_teams: false
├─ background_agents: false
└─ code_review: true

🎨 代码处理
├─ auto_format.enabled: true
└─ auto_format.formatter: auto

🔧 Hooks 开关
├─ session_start: true
├─ pre_compact: true
├─ prompt_refresh_interval: 5
├─ stop_verify: true
├─ post_edit_format: true
├─ notification: true
└─ permission_auto_approve: true

修改配置: /cx-config <字段> <值>
或者: /cx-config (进入交互式菜单)
```

### Step 4: 交互式修改菜单

使用 **AskUserQuestion** 展示菜单让用户选择要修改的配置：

```
选择要修改的配置项:

【基本配置】
  1. developer_id (当前: cx)
  2. github_sync (当前: collab)
  3. current_feature (当前: cx-payment)

【AI 功能】
  4. agent_teams (当前: false)
  5. background_agents (当前: false)
  6. code_review (当前: true)

【代码处理】
  7. auto_format.enabled (当前: true)
  8. auto_format.formatter (当前: auto)

【Hooks 开关】
  9. session_start (当前: true)
  10. pre_compact (当前: true)
  11. prompt_refresh_interval (当前: 5)
  12. stop_verify (当前: true)
  13. post_edit_format (当前: true)
  14. notification (当前: true)
  15. permission_auto_approve (当前: true)

  0. 返回

选择 (输入数字或直接输入字段名):
```

## 配置项详解

### 1. developer_id

**类型**: 字符串
**默认值**: 首次 /cx-init 时设置
**说明**: 开发者标识，用于：
- 功能目录命名前缀
- Git commit author 前缀
- 日志和通知中的身份标识

**修改示例**:
```
当前: developer_id = "cx"
修改为: "alice"

功能目录: features/alice-payment/ (而非 cx-payment/)
```

### 2. github_sync

**类型**: 枚举
**可选值**: `off` | `local` | `collab` | `full`
**默认值**: `collab`

#### 各模式对比

| 模式 | 文档 Issue | 任务 Issue | PR | 适用场景 |
|------|----------|----------|-------|---------|
| `off` | ❌ | ❌ | ❌ | 单人项目、内部测试 |
| `local` | ❌ | ❌ | ❌ | 单人回顾、记录 |
| `collab` | ✅ (PRD/Design) | ❌ | ✅ (Summary) | **2-5 人团队推荐** |
| `full` | ✅ (全部) | ✅ (全部) | ✅ | 大团队、严格流程 |

**修改示例**:
```
当前: github_sync = "collab"
修改为: "off"

效果: cx-summary 后续不创建 GitHub Issue，仅生成本地 summary.md
```

**修改流程** (AskUserQuestion):
```
当前 GitHub 同步模式: collab

选择新模式:
① off — 纯本地，不创建任何 GitHub Issue/PR
② local — 完成时创建汇总 Issue
③ collab — PRD/Design Doc 创建 Issue，summary 创建 Issue+PR (推荐)
④ full — 所有文档都创建 Issue

选择 (1-4):
```

### 3. current_feature

**类型**: 字符串
**默认值**: 空字符串
**说明**: 当前活跃的功能 slug。手动设置用于：
- /cx-status 查看该功能进度
- /cx-exec 默认执行该功能的任务
- 会话 SessionStart hook 自动加载该功能上下文

**修改示例**:
```
当前: current_feature = "cx-payment"
修改为: "cx-refund"

效果: 下次 /cx-exec 执行 cx-refund 相关任务
      /cx-status 展示 cx-refund 的进度
```

### 4. agent_teams

**类型**: 布尔值
**默认值**: `false`
**说明**: 是否启用 Agent Teams 模式（前后端契约协作）

**启用条件**:
- Claude Code 必须支持 Agent Teams 特性（目前实验性）
- 项目有明确的前后端分工
- 需要通过 API 契约锁定前后端对齐

**启用后的效果**:
```
cx-plan 执行时:
  └─ 自动识别前端/后端任务分组

cx-exec 执行时:
  ├─ 启动 frontend-agent（处理前端任务）
  ├─ 启动 backend-agent（处理后端任务）
  └─ SubagentStop hook 校验双方契约一致性
```

**修改示例**:
```
当前: agent_teams = false
修改为: true

提示: 启用后需要 Claude Code 支持 Agent Teams，建议咨询文档
```

### 5. background_agents

**类型**: 布尔值
**默认值**: `false`
**说明**: 是否允许后台 agent 运行

**启用后的效果**:
```
cx-summary 生成后:
  ├─ 本地汇总立即完成（用户可继续操作）
  └─ GitHub 同步（Issue/PR 创建）在后台运行
```

**禁用时的行为** (默认):
```
cx-summary 生成后:
  ├─ 本地汇总执行
  ├─ GitHub 同步阻塞等待
  └─ 完成后返回
```

### 6. code_review

**类型**: 布尔值
**默认值**: `true`
**说明**: cx-exec 全部任务完成后，是否智能询问代码审查

**启用时** (true):
```
所有任务完成后，提示用户:
"所有任务已完成。是否进行代码审查？"

用户可选:
① 全面审查 (逻辑 bug + 安全 + 质量 + 清理)
② 快速检查 (仅逻辑 bug)
③ 跳过
```

**禁用时** (false):
```
任务完成后直接进入 cx-summary
跳过代码审查流程
```

**修改示例**:
```
当前: code_review = true
修改为: false

效果: 后续执行不再询问代码审查
```

### 7. auto_format.enabled

**类型**: 布尔值
**默认值**: `true`
**说明**: PostToolUse hook 是否自动格式化写入的文件

**启用时** (true):
```
Edit/Write 工具执行后，自动运行：
├─ JavaScript/TypeScript → prettier
├─ Python → black
├─ Go → gofmt
├─ Rust → rustfmt
└─ 其他 → 按 formatter 检测
```

**禁用时** (false):
```
文件不自动格式化，需要手动运行 format 命令
```

### 8. auto_format.formatter

**类型**: 枚举
**可选值**: `auto` | `prettier` | `black` | `gofmt` | `rustfmt`
**默认值**: `auto`
**说明**: 自动格式化工具选择

| 值 | 说明 |
|----|------|
| `auto` | 自动检测，根据文件类型选择 |
| `prettier` | 强制使用 prettier (JS/TS/JSON) |
| `black` | 强制使用 black (Python) |
| `gofmt` | 强制使用 gofmt (Go) |
| `rustfmt` | 强制使用 rustfmt (Rust) |

**修改示例**:
```
当前: auto_format.formatter = "auto"
修改为: "prettier"

效果: 所有可格式化文件都用 prettier 处理
```

### 9. hooks.session_start

**类型**: 布尔值
**默认值**: `true`
**说明**: SessionStart hook 是否启用

**启用时** (true):
```
每次会话开始时自动执行:
├─ 读取 status.json
├─ 检测中断任务
├─ 加载上下文摘要
└─ 提示用户可用操作
```

**禁用时** (false):
```
会话不自动加载上下文
需要手动 /cx-status 查询进度
```

### 10. hooks.pre_compact

**类型**: 布尔值
**默认值**: `true`
**说明**: PreCompact hook 是否启用

**启用时** (true):
```
compaction 前自动执行:
└─ 生成 context-snapshot.md
   ├─ 当前任务号
   ├─ 契约摘要
   └─ 进度信息

compaction 后恢复时使用 snapshot 快速恢复上下文
```

### 11. hooks.prompt_refresh_interval

**类型**: 整数
**默认值**: `5`
**说明**: UserPromptSubmit hook 每隔多少轮注入目标刷新

**值含义**:
- `0` — 禁用目标刷新
- `N > 0` — 每 N 轮注入一次："当前任务: #{n}, 剩余: X"

**修改示例**:
```
当前: prompt_refresh_interval = 5
修改为: 3

效果: 每 3 轮对话自动注入一次进度提醒
```

### 12. hooks.stop_verify

**类型**: 布尔值
**默认值**: `true`
**说明**: Stop hook 是否启用

**启用时** (true):
```
用户要离开时自动检查:
├─ 读取 status.json
├─ 检测是否有 in_progress 但未完成的任务
└─ 如果有，提醒用户确认
```

**禁用时** (false):
```
用户可直接离开，不提醒
```

### 13. hooks.post_edit_format

**类型**: 布尔值
**默认值**: `true`
**说明**: PostToolUse hook 自动格式化是否启用

**启用时** (true):
```
每次 Edit/Write 后自动执行：
└─ 调用 auto_format.formatter 格式化文件
```

**禁用时** (false):
```
不自动格式化
与 auto_format.enabled 结合使用
```

### 14. hooks.notification

**类型**: 布尔值
**默认值**: `true`
**说明**: 是否启用桌面通知

**启用时** (true):
```
以下事件发送桌面通知:
├─ cx-exec 全部任务完成
├─ cx-fix 完成修复
└─ cx-summary 汇总完成
```

**通知方式** (自动检测):
- macOS: `osascript`
- Linux: `notify-send`
- Windows: PowerShell MessageBox

**禁用时** (false):
```
不发送任何桌面通知
```

### 15. hooks.permission_auto_approve

**类型**: 布尔值
**默认值**: `true`
**说明**: 是否自动放行安全操作

**启用时** (true):
```
PermissionRequest hook 自动批准以下命令:
├─ git add/commit/push/checkout/branch
├─ gh issue/pr/project
└─ npm test / pytest / cargo test / go test
```

**禁用时** (false):
```
所有命令都需要用户手动确认
```

## 修改方式

### 方式 1: 交互式菜单（推荐）

```
/cx-config
→ 显示当前配置
→ 提示选择要修改的项
→ 根据字段类型提供输入/选择界面
```

### 方式 2: 直接命令

```
/cx-config developer_id alice
/cx-config github_sync off
/cx-config code_review false
/cx-config hooks.notification true
```

**参数验证**:
- 必须是有效的配置字段
- 值必须与字段类型匹配
- 枚举字段只接受允许的值

### 方式 3: 手动编辑

```bash
vim ${GIT_ROOT}/.claude/cx/config.json
```

**注意**: 手动编辑后需要确保 JSON 格式正确。

## 配置修改后的效果

### 立即生效的配置

```
- developer_id: 下次创建功能时使用
- current_feature: 下次 /cx-exec 立即生效
- code_review: 下次 cx-exec 完成后立即生效
- auto_format.enabled/formatter: 下次 Write/Edit 后立即生效
- hooks.prompt_refresh_interval: 下次 UserPromptSubmit 立即生效
```

### 需要重新运行命令的配置

```
- github_sync: 下次 /cx-summary 时生效
- agent_teams: 需要重新 /cx-plan 才能应用新的任务分组
- background_agents: 下次 /cx-summary 时生效
```

### Hooks 开关

```
- 修改后立即生效于下次对应 hook 触发
- 关闭 hook 后不会逆序清理（如 session_start=false 后
  已加载的上下文继续有效）
```

## 完整配置备份与恢复

### 备份当前配置

```bash
cp ${GIT_ROOT}/.claude/cx/config.json \
   ${GIT_ROOT}/.claude/cx/config.json.backup
```

### 从备份恢复

```bash
cp ${GIT_ROOT}/.claude/cx/config.json.backup \
   ${GIT_ROOT}/.claude/cx/config.json
```

## 配置验证

修改配置时自动检查：

| 字段 | 有效值 | 说明 |
|------|--------|------|
| `developer_id` | 非空字符串 | 最多 32 字符，仅英数下划线 |
| `github_sync` | off/local/collab/full | 必须为允许值 |
| `current_feature` | 字符串 | 可为空 |
| `agent_teams` | true/false | 布尔值 |
| `background_agents` | true/false | 布尔值 |
| `code_review` | true/false | 布尔值 |
| `auto_format.enabled` | true/false | 布尔值 |
| `auto_format.formatter` | auto/prettier/... | 必须为允许值 |
| `hooks.*` | 布尔值/整数 | 根据字段类型 |

## 常见修改场景

### 场景 1: 从单人模式切换到团队协作

```
当前配置:
  github_sync: off
  code_review: false

修改为:
  github_sync: collab
  code_review: true

结果: 后续开发会创建 GitHub Issue 供 review，支持团队协作
```

### 场景 2: 禁用自动格式化

```
修改:
  auto_format.enabled: false

结果: 写入的代码不自动格式化
```

### 场景 3: 关闭桌面通知

```
修改:
  hooks.notification: false

结果: 任务完成不再发送通知
```

### 场景 4: 加速大规模开发

```
修改:
  agent_teams: true (启用前后端并行)
  background_agents: true (后台 GitHub 同步)
  hooks.prompt_refresh_interval: 10 (降低刷新频率)

结果: 多 agent 并行开发，减少人工等待时间
```

## 故障排查

| 问题 | 解决方案 |
|------|---------|
| 修改后不生效 | 检查是否需要重新运行命令，或重新启动会话 |
| config.json 格式错误 | 使用 `jq` 验证: `jq . config.json` |
| 无法写入 config | 检查文件权限: `chmod 644 config.json` |
| GitHub 同步不工作 | 确保 `github_sync` 不是 `off`，且有有效的 GitHub token |
