---
name: cx-status
description: >
  CX 工作流 — 进度查看。从本地配置读取当前活跃功能和任务状态，
  展示完成进度、当前任务详情、最近修复记录。
  触发词：进度、状态、做到哪了、还剩什么、怎样了、当前任务。
  自动触发当用户询问工作流进度相关问题。
---

# cx-status — 查看工作流进度

## 概述

读取本地 `.claude/cx/` 配置和状态文件，展示：
- 当前活跃功能及其整体进度
- 当前功能的任务列表和完成情况
- 最近的 Bug 修复记录

## 执行流程

### Step 1: 定位 CX 配置目录

```bash
GIT_ROOT=$(git rev-parse --show-toplevel)
CX_DIR="${GIT_ROOT}/.claude/cx"

if [ ! -d "$CX_DIR" ]; then
  echo "❌ 工作流未初始化。请先运行 /cx-init"
  exit 1
fi
```

### Step 2: 读取 config.json

从 `${CX_DIR}/config.json` 读取：
- `developer_id` — 开发者标识
- `current_feature` — 当前活跃功能 slug（可能为空）
- `github_sync` — GitHub 同步模式
- `code_review` — 是否启用代码审查

```json
{
  "version": "2.0",
  "developer_id": "cx",
  "github_sync": "collab",
  "current_feature": "cx-payment",
  "code_review": true,
  ...
}
```

### Step 3: 读取全局 status.json

从 `${CX_DIR}/status.json` 读取全局状态：

```json
{
  "initialized_at": "2026-02-06T10:30:00Z",
  "last_updated": "2026-02-06T15:45:30Z",
  "current_feature": "cx-payment",
  "features": {
    "cx-payment": {
      "status": "in_progress",
      "created_at": "2026-02-06T10:35:00Z",
      "last_updated": "2026-02-06T15:45:30Z",
      "tasks_total": 5,
      "tasks_completed": 2,
      "tasks_in_progress": 1,
      "tasks_pending": 2
    },
    "cx-auth": {
      "status": "done",
      "created_at": "2026-02-05T08:00:00Z",
      "last_updated": "2026-02-06T12:00:00Z",
      "tasks_total": 4,
      "tasks_completed": 4,
      "tasks_in_progress": 0,
      "tasks_pending": 0
    }
  },
  "fixes": [
    {
      "id": "fix-001",
      "description": "修复支付页面加载超时",
      "created_at": "2026-02-06T14:00:00Z",
      "status": "done"
    }
  ]
}
```

### Step 4: 展示当前状态

#### 情况 A：无活跃功能

```
📊 CX 工作流状态

❌ 当前无活跃功能

已完成的功能:
┌─────────────┬──────────┬────────────┐
│ 功能名       │ 状态     │ 完成时间   │
├─────────────┼──────────┼────────────┤
│ cx-auth     │ 完成 ✅  │ 2026-02-06 │
└─────────────┴──────────┴────────────┘

下一步操作:
• /cx-prd <功能名> — 开始新功能需求收集
• /cx-fix <bug描述> — 修复 Bug
• /cx-help — 显示工作流帮助
```

#### 情况 B：有活跃功能（进行中）

```
📊 CX 工作流状态 — {developer_id}

🎯 当前功能: cx-payment
├─ 状态: 进行中 🔄
├─ 完成度: 2/5 (40%) ▓▓░░░
├─ 开始时间: 2026-02-06 10:35
└─ 最后更新: 2026-02-06 15:45

📋 任务进度
┌─────────────────────────────┬─────────┐
│ 任务                        │ 状态    │
├─────────────────────────────┼─────────┤
│ #1 [完成] DB 表结构设计     │ ✅ done │
│ #2 [完成] 后端支付 API      │ ✅ done │
│ #3 [进行] 前端支付页面      │ 🔄 in   │
│ #4 [待处理] 前端集成测试    │ ⏳ pend │
│ #5 [待处理] 安全审计        │ ⏳ pend │
└─────────────────────────────┴─────────┘

📌 当前任务详情
Task #3: 前端支付页面
├─ 类型: 前端开发
├─ 开始时间: 2026-02-06 14:30
├─ API 契约: POST /api/v1/payment/create
│            GET /api/v1/payment/status/{id}
├─ 验收标准:
│  ✓ 表单验证完整
│  ✓ 加载状态显示
│  ✓ 错误提示清晰
│  • 支付结果回调处理（进行中）
└─ 关键代码路径: src/pages/Payment/

🐛 最近修复
┌──────────┬──────────────────────┬────────────┐
│ ID       │ 描述                 │ 完成时间   │
├──────────┼──────────────────────┼────────────┤
│ fix-001  │ 修复支付页面加载超时 │ 2026-02-06 │
└──────────┴──────────────────────┴────────────┘

💡 建议
• 继续 /cx-exec 完成任务 #3
• 任务完成后可选进行代码审查（当前 code_review=true）
• 所有任务完成后运行 /cx-summary 汇总发布
```

### Step 5: 读取功能级 status.json

如果有活跃功能，还需读取 `${CX_DIR}/features/{feature_name}/status.json`：

```json
{
  "feature": "cx-payment",
  "scope": "M",
  "prd_completed_at": "2026-02-06T10:40:00Z",
  "design_completed_at": "2026-02-06T11:00:00Z",
  "plan_completed_at": "2026-02-06T11:30:00Z",

  "tasks": [
    {
      "number": 1,
      "title": "DB 表结构设计",
      "status": "done",
      "team": "backend",
      "started_at": "2026-02-06T11:35:00Z",
      "completed_at": "2026-02-06T12:30:00Z",
      "contract_snippet": "关键 API 契约摘要..."
    },
    {
      "number": 2,
      "title": "后端支付 API",
      "status": "done",
      "team": "backend",
      "started_at": "2026-02-06T12:35:00Z",
      "completed_at": "2026-02-06T14:00:00Z",
      "contract_snippet": "..."
    },
    {
      "number": 3,
      "title": "前端支付页面",
      "status": "in_progress",
      "team": "frontend",
      "started_at": "2026-02-06T14:30:00Z",
      "contract_snippet": "..."
    }
  ],

  "last_updated": "2026-02-06T15:45:30Z"
}
```

### Step 6: 读取 fix-records.json（如果存在）

在 `${CX_DIR}/features/{feature_name}/fix-records.json` 中记录该功能下的 Bug 修复：

```json
[
  {
    "id": "fix-001",
    "feature": "cx-payment",
    "description": "修复支付页面加载超时",
    "severity": "high",
    "reported_at": "2026-02-06T13:00:00Z",
    "fixed_at": "2026-02-06T14:00:00Z",
    "commit": "5a7c2d1",
    "github_issue": "#42"
  }
]
```

### Step 7: 组织并展示信息

#### 7.1 功能概览

```
当前功能: {feature_name}
规模: {scope} ({scope_description})
进度: {completed}/{total} 任务完成 ({percent}%)
    ▓▓░░░ ({visual_progress})
```

#### 7.2 任务列表

按状态分组展示任务：

```
✅ 已完成 ({n} 个):
  • Task #1: {title} (耗时: 55 min)
  • Task #2: {title} (耗时: 85 min)

🔄 进行中 ({n} 个):
  • Task #3: {title} (开始于: {time} ago)
    API 契约: {contract_summary}

⏳ 待处理 ({n} 个):
  • Task #4: {title}
  • Task #5: {title}
```

#### 7.3 当前任务详情

如果有 in_progress 的任务，展示详细信息：

```
📌 当前任务: Task #{number} - {title}

├─ 团队: {team} (frontend/backend/qa)
├─ 开始: {started_at} (已用时 {duration})
├─ 关键代码路径: {related_files}
├─ API 契约摘要:
│  POST /api/v1/{endpoint}
│  Request: {request_schema}
│  Response: {response_schema}
├─ 验收标准:
│  ✓ {standard1}
│  ✓ {standard2}
│  • {standard3} (进行中)
└─ 提示: 继续 /cx-exec 完成此任务
```

#### 7.4 Bug 修复历史

```
🐛 本功能下的 Bug 修复历史:
┌──────────────────────────────────────┬──────────────┬────────┐
│ 描述                                 │ 严重程度     │ 状态   │
├──────────────────────────────────────┼──────────────┼────────┤
│ fix-001: 修复支付页面加载超时       │ 🔴 high     │ ✅ done│
└──────────────────────────────────────┴──────────────┴────────┘
```

### Step 8: 快速操作提示

根据当前状态，提示用户可以执行的命令：

```
💡 快速操作

根据当前状态，你可以:

如果有待处理任务:
  • /cx-exec — 继续执行下一个任务

如果有进行中的任务:
  • /cx-exec — 继续当前任务
  • /cx-status — 刷新进度

如果所有任务完成:
  • /cx-summary — 生成汇总发布

其他:
  • /cx-fix <bug描述> — 修复新的 Bug
  • /cx-prd <功能名> — 开始新功能
  • /cx-config — 调整配置
```

## 边界情况处理

### 情况 1: 工作流未初始化

```
❌ 工作流未初始化

请运行: /cx-init

然后可以:
• /cx-prd <功能名> — 开始新功能需求收集
• /cx-fix <bug描述> — 修复 Bug
```

### 情况 2: config.json 损坏或缺失

```
⚠️ 配置异常

config.json 文件损坏或不存在。

恢复方法:
1. 检查 .claude/cx/config.json 是否存在
2. 如果缺失，运行 /cx-init 重新初始化
3. 或手动编辑 config.json，确保 JSON 格式正确
```

### 情况 3: 多个功能并行

如果 `current_feature` 为空或有多个活跃功能，展示所有功能的进度表：

```
📊 工作流状态 — 多功能进度

当前活跃功能: (无)

所有功能进度:
┌─────────────┬────────┬──────────┬────────┐
│ 功能名       │ 规模   │ 进度     │ 状态   │
├─────────────┼────────┼──────────┼────────┤
│ cx-payment  │ M      │ 2/5 (40%)│ 🔄 in  │
│ cx-auth     │ S      │ 4/4 (100)│ ✅ done│
│ cx-refund   │ M      │ 0/6 (0%) │ ⏳ pend│
└─────────────┴────────┴──────────┴────────┘

选择功能查看详情: /cx-status {feature_name}
设置当前活跃功能: /cx-config → 修改 current_feature
```

## 文件结构参考

```
.claude/cx/
├── config.json              # 全局配置
├── status.json              # 全局状态（所有功能汇总）
├── context-snapshot.md      # 上下文快照（compaction 前）
└── features/
    ├── cx-payment/
    │   ├── prd.md           # 需求文档
    │   ├── design.md        # 设计文档
    │   ├── plan.md          # 任务计划
    │   ├── status.json      # 功能级进度
    │   └── fix-records.json # 修复记录
    └── cx-auth/
        └── ...
```

## 常见问题

**Q: 为什么显示"无活跃功能"？**
A: `current_feature` 为空。运行 `/cx-prd <功能名>` 开始新功能，或 `/cx-fix <bug>` 修复 Bug。

**Q: 如何查看其他功能的进度？**
A: `/cx-status {feature_name}` 查看特定功能。

**Q: 进度百分比如何计算？**
A: 完成任务数 / 总任务数。显示为百分比和进度条可视化。

**Q: 当前任务显示了哪些信息？**
A: 任务号、标题、团队、开始时间、API 契约摘要、验收标准和关键代码路径。

**Q: Bug 修复也会显示在状态中吗？**
A: 会。fix-records.json 中的修复记录会单独列出，便于查看修复历史。
