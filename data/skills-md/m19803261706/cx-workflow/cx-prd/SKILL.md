---
name: cx-prd
description: >
  CX 工作流 — 需求收集与规模评估。当用户提到"新功能"、"需求"、"PRD"、
  "我想做一个"、"帮我规划"、"收集需求"、"功能规划"时触发。
  多轮对话收集需求，自动评估规模 S/M/L，保存到本地
  .claude/cx/features/{dev_id}-{feature}/prd.md，
  根据规模智能路由：S→cx-plan，M/L→cx-design。
---

# cx-prd: 需求收集与规模评估

多轮对话收集功能需求，自动评估规模，决定后续工作流路径。

## 使用方法

```
/cx-prd {功能名}       # 指定功能开始需求收集
/cx-prd               # 提示输入功能名
```

## 核心步骤

### Step 0: 初始化本地环境

```bash
PROJECT_ROOT=$(git rev-parse --show-toplevel)
CONFIG="$PROJECT_ROOT/.claude/cx/config.json"
DEVELOPER_ID=$(jq -r '.developer_id' "$CONFIG" 2>/dev/null || echo "cx")
FEATURE_SLUG="{feature_name_slugified}"
FEATURE_DIR="$PROJECT_ROOT/.claude/cx/features/${DEVELOPER_ID}-${FEATURE_SLUG}"
mkdir -p "$FEATURE_DIR"
```

### Step 1: 项目识别

自动检测技术栈（Python/Node/Java/Rust/Go、框架等）。保存到 prd.json 中供后续参考。

### Step 2: 代码结构与关联代码扫描

启动 Explore subagent（通过 Task tool）：
- 项目目录树
- 技术栈细节
- 搜索关键词相关的已有代码
- 找出可复用模块、接口、数据结构

输出供用户在对话中参考的上下文摘要。

### Step 3: 多轮对话收集需求

**第一轮**：基础信息
```json
{
  "questions": [
    {
      "question": "这个功能的核心用户场景有哪些？",
      "header": "场景",
      "multiSelect": true,
      "options": [
        {"label": "用户交互", "description": "终端用户直接使用"},
        {"label": "系统处理", "description": "后台自动处理"},
        {"label": "数据管理", "description": "数据存储和查询"},
        {"label": "外部对接", "description": "与第三方集成"}
      ]
    },
    {
      "question": "预计影响哪些代码层？",
      "header": "代码层",
      "multiSelect": true,
      "options": [
        {"label": "前端界面"},
        {"label": "后端服务"},
        {"label": "数据层"},
        {"label": "基础设施"}
      ]
    }
  ]
}
```

**循环对话**：每轮收集后展示理解，询问是否有补充或修正，直到用户确认无误。

### Step 4: 优先级确认

```json
{
  "questions": [
    {
      "question": "这个功能的优先级？",
      "header": "优先级",
      "multiSelect": false,
      "options": [
        {"label": "P0 紧急", "description": "阻塞其他工作"},
        {"label": "P1 高", "description": "当前迭代必须完成"},
        {"label": "P2 中", "description": "近期完成"},
        {"label": "P3 低", "description": "可延后"}
      ]
    }
  ]
}
```

### Step 5: 保存到本地

生成 prd.md 保存到 `.claude/cx/features/{dev_id}-{feature}/prd.md`。

**模板**：
```markdown
# PRD: {功能名}

## 基本信息
- **创建时间**: {ISO 时间}
- **优先级**: P0/P1/P2/P3
- **技术栈**: {自动检测结果}

## 功能概述
{多轮对话生成的完整描述}

## 用户场景
{场景列表及详细描述}

## 详细需求
{整理后的需求，按逻辑分组}

## 现有代码基础
{代码扫描发现的可复用模块、接口、数据结构}

## 代码影响范围
{受影响的代码层和模块}

## 验收标准
- [ ] {标准1}
- [ ] {标准2}
```

同时生成 prd.json 记录元数据：
```json
{
  "feature_name": "{feature}",
  "slug": "{feature_slug}",
  "priority": "P1",
  "tech_stack": ["node", "react"],
  "created_at": "2024-01-15T10:00:00Z",
  "github_issue": null,
  "scale": null
}
```

### Step 6: 自动规模评估

基于 PRD 内容综合评估：

| 维度 | S（小） | M（中） | L（大） |
|------|---------|---------|---------|
| 影响文件数 | 1-3 | 4-10 | 10+ |
| 涉及层级 | 单层 | 前后端 | 全栈 |
| 新增 API | 0 | 1-3 | 4+ |
| 新增表 | 0 | 1-2 | 3+ |
| 架构变更 | 无 | 小调整 | 新技术 |

**评分规则**：
```
影响层级: 单层+0, 前后端+1, 全栈+2
新增 API: 0个+0, 1-3个+1, 4+个+2
数据库: 无+0, 1-2张+1, 3+张+2
架构变更: 无+0, 有+2

总分: 0-1→S, 2-4→M, 5+→L
```

保存评估结果到 prd.json。

### Step 7: GitHub 同步（可选）

根据 `config.github_sync`：
- **off**：仅保存本地
- **local/collab/full**：创建 GitHub Issue（标签 `doc:prd`），记录 Issue 编号

### Step 8: 规模路由

显示评估结果和建议流程：

```
规模评估: {S/M/L}
  影响层级: {层级}
  新增 API: {数量}
  数据库变更: {是/否}

建议流程: {根据规模给出}
```

```json
{
  "questions": [
    {
      "question": "是否继续下一步？",
      "header": "下一步",
      "multiSelect": false,
      "options": [
        {"label": "继续 {S→规划|M/L→设计} (推荐)", "description": "自动执行下一个 skill"},
        {"label": "仍要完整流程", "description": "所有规模都走 Design→Plan→Exec"},
        {"label": "稍后处理", "description": "先 review PRD"}
      ]
    }
  ]
}
```

## 规模特定路由

**S 规模**：PRD → cx-plan（跳过 Design）
```
原因: 变更范围小，无需前后端对齐文档
```

**M 规模**：PRD → cx-design（需要 API 契约）
```
原因: 前后端都有变更，需要 API 契约对齐
```

**L 规模**：PRD → cx-design + cx-adr（完整链路）
```
原因: 全栈变更，需要完整设计和架构决策
```

## Explore Subagent 使用

Step 2 启动代码扫描：

```
Task tool 参数:
  subagent_type: "Explore"
  description: "扫描项目结构、技术栈、关联代码"
  prompt: "列出项目目录树、检测技术栈、找出与 {关键词} 相关的已有代码"
```

## 进度追踪

本地 prd.json 记录完整元数据，供后续 skills 读取。

## 与 cx-scope 的关联

如果 cx-scope 已有功能方案记录，自动读取 scope.md 作为 PRD 对话的上下文，避免重复讨论。
