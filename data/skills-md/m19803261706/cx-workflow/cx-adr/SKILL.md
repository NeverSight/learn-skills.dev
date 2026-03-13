---
name: cx-adr
description: >
  CX 工作流 — 架构决策记录。当用户提到"架构决策"、"技术选型"、
  "ADR"、"为什么选择 X"、"架构方案对比"时可能触发（通常由 cx-design 自动调用）。
  记录 Architecture Decision Records，保存到本地
  .claude/cx/features/{dev_id}-{feature}/adr.md。
  手动触发或由 cx-design 在检测到架构决策时自动触发。
---

# cx-adr: 架构决策记录

记录技术选型和架构决策，为大规模功能（L）提供完整决策档案。

## 使用方法

```
/cx-adr <决策标题>     # 记录一个架构决策
/cx-adr               # 提示输入决策标题
```

## 何时需要 ADR

- 引入新技术、框架或库
- 选择数据存储方案（SQL vs NoSQL、缓存策略等）
- 选择通信协议（REST vs WebSocket vs gRPC）
- 重大架构变更（微服务拆分、单体合并）
- 数据流或状态管理方案选择
- 有多个可行方案且各有 trade-off

## 核心步骤

### Step 0: 初始化本地环境

```bash
PROJECT_ROOT=$(git rev-parse --show-toplevel)
DEVELOPER_ID=$(jq -r '.developer_id' "$PROJECT_ROOT/.claude/cx/config.json" 2>/dev/null || echo "cx")
FEATURE_DIR="$PROJECT_ROOT/.claude/cx/features/${DEVELOPER_ID}-{feature_slug}"
```

### Step 1: 收集决策上下文

```json
{
  "questions": [
    {
      "question": "这个决策要解决什么问题？",
      "header": "决策类型",
      "multiSelect": false,
      "options": [
        {"label": "技术选型", "description": "选择使用哪个技术/框架/库"},
        {"label": "架构变更", "description": "系统架构层面的调整"},
        {"label": "方案选择", "description": "多个可行方案需要取舍"},
        {"label": "规范制定", "description": "确立技术规范或标准"}
      ]
    }
  ]
}
```

### Step 2: 关联文档查找

从本地查找关联的 prd.md 和 design.md（如果有）。

### Step 3: 技术调研

根据决策类型，使用 Context7（如需）查阅相关技术文档：
- 候选技术对比
- 最佳实践
- 项目约束和兼容性

扫描项目现有代码理解技术栈和约束。

### Step 4: 生成 ADR

**模板**：

```markdown
# ADR: {决策标题}

## 状态
**Proposed** — 待确认

## 关联
${design_number:+Design Doc: #$design_number}
${prd_number:+PRD: #$prd_number}

## 背景
{为什么需要做这个决策，问题描述}

## 决策驱动因素
- {因素1：如性能要求}
- {因素2：如团队熟悉度}
- {因素3：如维护成本}

## 候选方案

### 方案 A: {方案名}

{方案描述}

- 优势:
  - {优势1}
  - {优势2}
- 劣势:
  - {劣势1}
  - {劣势2}
- 适用场景: {说明}

### 方案 B: {方案名}

{方案描述}

- 优势:
  - {优势1}
  - {优势2}
- 劣势:
  - {劣势1}
  - {劣势2}
- 适用场景: {说明}

## 对比

| 维度 | 方案 A | 方案 B |
|------|--------|--------|
| 性能 | {评估} | {评估} |
| 复杂度 | {评估} | {评估} |
| 维护成本 | {评估} | {评估} |
| 学习曲线 | {评估} | {评估} |
| 团队熟悉度 | {评估} | {评估} |

## 建议

**推荐方案 {X}**

{推荐理由，基于决策驱动因素的分析}

## 影响

- 对现有代码: {影响说明}
- 对后续开发: {影响说明}
- 迁移成本: {评估}
- 回退成本: {评估}

## 实施计划

{何时实施、分阶段计划、依赖条件}

---
> CX 工作流 | ADR
```

保存到 `.claude/cx/features/{dev_id}-{feature}/adr.md`。

### Step 5: 决策确认

```json
{
  "questions": [
    {
      "question": "选择哪个方案？",
      "header": "决策",
      "multiSelect": false,
      "options": [
        {"label": "方案 A", "description": "{方案A简述}"},
        {"label": "方案 B", "description": "{方案B简述}"},
        {"label": "需要更多信息", "description": "补充调研后再决定"},
        {"label": "暂时搁置", "description": "先不做决定"}
      ]
    }
  ]
}
```

### Step 6: GitHub 同步（可选）

根据 `config.github_sync`：
- **off/local**：仅保存本地
- **collab/full**：创建 GitHub Issue（标签 `doc:adr`），记录 Issue 编号

更新 ADR 状态为 **Accepted**（如用户确认）或 **Proposed**（如待定）。

### Step 7: 返回调用者

如果由 cx-design 触发，返回 Design Doc 流程继续。
如果是手动调用，询问下一步。

## 本地文件结构

```
.claude/cx/features/{dev_id}-{feature}/
├── adr.md             ← ADR 文档
├── adr.json           ← Issue 编号（可选）、决策元数据
└── ...
```

## ADR 管理

本地 adr.json 记录所有 ADR：

```json
{
  "adr_list": [
    {
      "id": 1,
      "title": "选择 React 而非 Vue",
      "status": "Accepted",
      "decided_at": "2024-01-15T10:00:00Z",
      "recommendation": "方案 A"
    }
  ]
}
```

## 与 Design Doc 的关联

- Design Doc 在生成过程中会检测是否涉及架构决策
- 如检测到，会自动询问是否需要 ADR
- cx-design 完成后，用户可以运行 `/cx-adr` 补充决策记录

## 与 cx-plan 的衔接

- **输入**：design.md（来自 cx-design）
- **输出**：adr.md（供 cx-plan 参考）
- cx-plan 在生成任务时会引用 ADR 决策作为技术背景

## L 规模功能的必需项

对于 L（大规模）功能：
- Design Doc 是强制项
- ADR 是强制项（如有架构决策）
- cx-plan 生成的每个子任务都会关联相关 ADR 决策

## 决策的可追溯性

每个 ADR 记录完整的决策过程，供后续团队成员、审查者或未来维护者参考，形成项目的架构决策历史档案。
