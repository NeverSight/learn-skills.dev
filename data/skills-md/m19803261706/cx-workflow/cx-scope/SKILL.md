---
name: cx-scope
description: >
  CX 工作流 — 项目蓝图探讨。当用户提到"蓝图"、"整体规划"、"项目范围"、
  "scope"、"项目探讨"、"功能方案"时触发。多轮对话探讨项目或功能方案，
  将结果保存到本地 .claude/cx/features/{dev_id}-{feature}/scope.md，
  可选同步到 GitHub Issue（基于 config.github_sync 模式）。
---

# cx-scope: 项目与功能探讨

在需求分析前的探讨阶段，理清项目定位、目标用户、功能模块、优先级和技术边界。

## 使用方法

```
/cx-scope                  # 项目级蓝图探讨
/cx-scope {功能名}          # 功能级方案探讨
```

## 核心步骤

### Step 0: 初始化本地环境

```bash
PROJECT_ROOT=$(git rev-parse --show-toplevel)
DEVELOPER_ID=$(jq -r '.developer_id' "$PROJECT_ROOT/.claude/cx/config.json" 2>/dev/null || echo "cx")

# 创建功能目录
FEATURE_SLUG="{feature_name_slugified}"
FEATURE_DIR="$PROJECT_ROOT/.claude/cx/features/${DEVELOPER_ID}-${FEATURE_SLUG}"
mkdir -p "$FEATURE_DIR"
```

### Step 1: 判断探讨模式

- **项目级**：整体项目规划，输出项目蓝图（模块、优先级、技术栈）
- **功能级**：某个功能的方案探讨（目标、流程、边界、技术方案）

### Step 2: 环境扫描

使用 Explore subagent（通过 Task tool）扫描项目结构、技术栈、已有相关代码。输出供用户参考的上下文摘要。

### Step 3: 多轮对话收集

自由对话，不限制轮数，直到用户表示"确定了"。提问方向：

**项目级**：
- 项目定位与目标用户
- 核心功能模块清单
- 功能优先级划分（MVP vs Phase 2/3）
- 技术边界和约束
- 参考产品

**功能级**：
- 功能目标与成果
- 用户流程与关键步骤
- 与现有功能的关系（依赖、影响、复用）
- 边界情况与异常处理
- 技术方案倾向

每 2-3 轮后整理一次当前共识，标注分歧点，让用户选择。

### Step 4: 确认收敛

```json
{
  "questions": [
    {
      "question": "探讨内容是否可以定稿？",
      "header": "确认",
      "multiSelect": false,
      "options": [
        {"label": "确认定稿", "description": "保存到本地并可选上云"},
        {"label": "继续探讨", "description": "还有内容需要补充"},
        {"label": "部分确认", "description": "先记录已确认的部分"}
      ]
    }
  ]
}
```

### Step 5: 保存到本地

生成结构化 scope.md 文档，保存到 `.claude/cx/features/{dev_id}-{feature}/scope.md`。

**项目级模板**：
```markdown
# 项目蓝图: {项目名}

## 项目定位
...

## 目标用户与场景
...

## 功能模块总览
| 序号 | 模块 | 优先级 | 状态 | 说明 |
|------|------|--------|------|------|
| 1 | {模块} | P0/P1/P2 | 待开发 | {说明} |

## 技术架构（概要）
...

## 开发路线
Phase 1 (MVP): ...
Phase 2: ...

## 探讨记录
{关键决策点和分歧解决方式}
```

**功能级模板**：
```markdown
# 功能探讨: {功能名}

## 功能目标
{达到什么效果}

## 用户流程
{关键步骤}

## 方案概要
{最终确认的方案}

## 与现有功能的关系
- 依赖: ...
- 影响: ...
- 复用: ...

## 边界和约束
- 技术限制
- 业务规则

## 开放问题
{尚未确定的细节，留给 PRD 阶段}
```

### Step 6: GitHub 同步（可选）

根据 `config.github_sync`：
- **off**：仅保存本地，不创建 Issue
- **local/collab/full**：创建 GitHub Issue（标签 `doc:scope`），并在 .claude/cx/features/{dev_id}-{feature}/scope.json 中记录 Issue 编号

### Step 7: 下一步引导

```json
{
  "questions": [
    {
      "question": "下一步？",
      "header": "下一步",
      "multiSelect": false,
      "options": [
        {"label": "开始 PRD", "description": "运行 /cx-prd {功能名}"},
        {"label": "继续探讨", "description": "再开一轮"},
        {"label": "保存稍后", "description": "先 review scope.md"}
      ]
    }
  ]
}
```

如果选择开始 PRD，自动执行 `/cx-prd {功能名}`（会自动读取本地 scope.md 作为上下文）。

## 本地文件结构

```
.claude/cx/features/
└── {dev_id}-{feature}/
    ├── scope.md           ← Scope 文档
    ├── scope.json         ← Issue 编号（仅 collab/full 模式）
    ├── prd.md            ← PRD（后续）
    ├── design.md         ← Design Doc（后续）
    ├── tasks/            ← 任务文件（后续）
    └── status.json       ← 整体进度（后续）
```

## Explore Subagent 使用

cx-scope 在 Step 2 中调用 Explore subagent 扫描代码结构。

```
Task tool 参数:
  subagent_type: "Explore"
  description: "扫描项目结构和技术栈"
  prompt: "列出项目目录树、检测技术栈、找出已有相关模块"
```

返回的信息用于增强对话的上下文感知。

## 进度追踪

使用本地 `status.json` 记录 Scope 状态：

```json
{
  "scope_status": "in_progress|completed",
  "created_at": "2024-01-15T10:00:00Z",
  "last_updated": "2024-01-15T10:30:00Z",
  "mode": "project|feature",
  "github_issue": null
}
```

## 与 cx-plan 的闭环

当所有功能完成后，cx-exec 会自动检测 Scope 中的模块状态，更新状态为已完成。所有模块完成时，关闭 Scope Issue。
