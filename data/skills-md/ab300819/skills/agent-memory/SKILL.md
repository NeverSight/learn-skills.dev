---
name: agent-memory
description: Manage AI agent memory files (AGENTS.md/CLAUDE.md). Supports update and restructure modes. Use when users need to sync, update, or restructure agent memory files. Triggers on keywords like "记忆文件", "memory file", "AGENTS.md", "更新记忆", "重构记忆", "memory sync", "memory restructure".
allowed-tools: Read, Write, Glob, Grep, Edit, Bash, AskUserQuestion
---

# 记忆文件管理

管理 AI Agent 记忆文件（AGENTS.md / CLAUDE.md），支持更新和重构操作。

## 核心理念

### AGENTS.md 为唯一事实源

```text
项目信息源（代码库 + 文档）
    │
    │  提取精华（distill）
    ▼
AGENTS.md（精简、稳定、跨 AI 工具通用）← 通用信息唯一编辑点
    │
    ├── CLAUDE.md（@AGENTS.md 导入 + Claude Code 专属补充）
    ├── .claude/rules/devdocs-state.md（仅 DevDocs 项目，编号状态）
    └── 未来：.cursorrules / .windsurfrules（预留，不实现）
```

**原则**：
- AGENTS.md 保持工具无关，不包含特定 AI 工具的专属语法
- CLAUDE.md 通过 `@AGENTS.md` 导入通用信息，并可追加 Claude Code 专属补充
- 工具专属信息通过各自的规则文件补充（如 `.claude/rules/`）

### 最佳实践参照

[best-practices.md](templates/best-practices.md) 为所有模式的共享规范：
- 首次创建时：作为质量基准
- `--update` 更新时：作为内容筛选依据
- `--restructure` 重组时：作为结构验证和反模式检测标准

### 与 `/init` 的协作

各 AI 工具的 `/init` 行为不同（如 Claude Code 创建 CLAUDE.md）。本 skill 不假设 `/init` 产出什么文件，而是保证 AGENTS.md 架构正确：
- AGENTS.md 不存在时：自动从项目源扫描并创建
- `/init` 已创建 AGENTS.md 时：后续 `--update` 在此基础上增量更新
- [best-practices.md](templates/best-practices.md) 作为内容质量参考
- [memory-template.md](templates/memory-template.md) 作为 AGENTS.md 输出模板

## 语言规则

- 支持中英文提问
- 统一中文回复

## 运行模式

```bash
/agent-memory                    → 智能检测（AGENTS.md 存在？需要更新？）
/agent-memory --update           → 从项目源提取信息，更新 AGENTS.md
/agent-memory --restructure      → 按最佳实践重组现有 AGENTS.md
```

| 模式 | 读取项目 | 写入文件 | 适用场景 |
|------|----------|----------|----------|
| 智能检测 | 视情况 | 视情况 | 不确定时 |
| `--update` | ✅ | AGENTS.md + CLAUDE.md（若缺失） + devdocs-state.md（仅 DevDocs） | 阶段性工作完成后同步 |
| `--restructure` | ✅ | AGENTS.md + CLAUDE.md | 记忆文件结构混乱时重组 |

### 智能检测流程

```text
检测 AGENTS.md 是否存在
        │
        ├── 不存在 → 扫描项目源，首次创建 AGENTS.md + CLAUDE.md
        │
        └── 存在 → 分析内容状态
                    ├── 信息过时 → 建议 --update
                    └── 结构混乱 → 建议 --restructure
```

## 信息提取分层

### 通用提取（所有项目）

| 来源 | 提取内容 |
|------|----------|
| package.json / go.mod / Cargo.toml | 技术栈、运行命令 |
| README.md | 项目概述 |
| git log | 提交约定 |
| 代码结构 | 关键目录、入口文件 |

### DevDocs 增强提取（有 docs/devdocs/ 时）

| 来源 | 提取内容 |
|------|----------|
| 02-system-design.md | 技术栈、架构决策 (ADR) 摘要 |
| 01-requirements.md | 领域术语 |
| 04-dev-tasks.md | 活跃任务 + 进度 |
| 所有文档 | 编号状态（max F/US/AC/T/ADR） |

## `--update` 工作流程

```text
1. 扫描项目信息源
   ├── 通用提取（包管理器、README、git、代码结构）
   └── DevDocs 增强提取（若 docs/devdocs/ 存在）
   │
   ▼
1.5 检查 AGENTS.md 是否存在
   ├── 不存在 → 使用 memory-template.md 创建
   └── 存在 → 增量更新
   │
   ▼
2. 提取精华
   ├── 技术栈
   ├── ADR 摘要（若有；无 ADR 格式则从变更记录提取关键决策）
   ├── 领域术语
   ├── 活跃任务 + 进度
   ├── 编号状态（仅 DevDocs 项目）
   └── 运行命令
   │
   ▼
2.5 按 best-practices.md 筛选
   ├── 内容筛选标准：应写入 vs 不应写入
   └── 质量守则：6 条检查
   │
   ▼
3. 更新 AGENTS.md（使用 templates/memory-template.md）
   │
   ▼
4. 确保 CLAUDE.md 存在（若缺失则创建导入文件；已存在则跳过，不覆盖补充区）
   │
   ▼
5. 生成/更新 .claude/rules/devdocs-state.md（仅 DevDocs 项目）
```

### 分流规则

| 信息类型 | 目标位置 | 理由 |
|----------|----------|------|
| 技术栈、运行命令 | AGENTS.md | 跨工具通用，每次会话都需要 |
| 架构决策 (ADR) 摘要 | AGENTS.md | 防止重复询问 |
| 活跃任务 + 进度 | AGENTS.md | 即时行动上下文 |
| 领域术语、业务边界 | AGENTS.md | 高频稳定，防止误解 |
| 代码约定、提交格式 | AGENTS.md | 跨工具一致 |
| 编号状态 (max F/US/AC/T/ADR) | `.claude/rules/devdocs-state.md` | Claude 专属运行态 |
| 完整需求/设计/测试详情 | 留在 `docs/devdocs/` | 太详细，不适合记忆文件 |

## `--restructure` 工作流程

```text
1. 读取现有 AGENTS.md
   │
   ▼
2. 按 best-practices.md 检测不规范项
   ├── 行数限制（≤ 60 行）
   ├── 工具无关性
   ├── 章节顺序（对照结构规范）
   ├── 反模式检测
   └── 缺失章节
   │
   ▼
3. 按 templates/memory-template.md 重组
   │
   ▼
4. 展示重组方案，确认后写入
   │
   ▼
5. 确保 CLAUDE.md 存在（若缺失则创建导入文件；已存在则跳过）
```

## 输出文件

### AGENTS.md

- 位置：项目根目录
- 模板：[templates/memory-template.md](templates/memory-template.md)
- 约束：不超过 60 行，工具无关

### CLAUDE.md

- 位置：项目根目录
- 结构：`@AGENTS.md` 导入 + Claude Code 专属补充区
- 创建时机：AGENTS.md 首次生成时一并创建；已存在则不覆盖
- 补充区由用户手动维护，`/agent-memory` 不修改

### .claude/rules/devdocs-state.md

- 位置：`.claude/rules/devdocs-state.md`
- 模板：[templates/devdocs-state-template.md](templates/devdocs-state-template.md)
- 条件：仅 DevDocs 项目（docs/devdocs/ 存在时）

## 约束

### 内容约束

- [ ] **AGENTS.md 不超过 60 行**
- [ ] **AGENTS.md 不包含特定 AI 工具的专属语法**
- [ ] **CLAUDE.md 通过 @AGENTS.md 导入通用信息**（首次创建后不覆盖）
- [ ] **编号状态仅写入 `.claude/rules/devdocs-state.md`**

### 质量守则

写入 AGENTS.md 前按 [best-practices.md](templates/best-practices.md) 检查：
- 6 条守则（短而稳定 / 广泛适用 / 可执行 / 避免重复 / 详情留原地 / 工具无关）
- 内容筛选标准（应写入 vs 不应写入）
- 反模式清单

### 操作约束

- [ ] 不生成/不修改 `00-context.md`
- [ ] 可删则删，优先命令、约束、检查点
- [ ] `--restructure` 重组前必须确认

## Skill 协作

| 场景 | 协作 Skill | 说明 |
|------|-----------|------|
| 首次创建 | `/agent-memory` 自行完成 | 从项目源扫描创建；若 `/init` 已创建则增量更新 |
| 阶段性文档变更 | `/devdocs-onboard` | onboard 完成后建议运行 /agent-memory |
| 任务完成轻量更新 | `/devdocs-dev-workflow` | dev-workflow 步骤 6.5 内联更新"当前状态" |
| 上下文摘要 | `/devdocs-onboard` | onboard 生成 00-context.md，不涉及记忆文件 |

## 模板引用

- AGENTS.md 模板：[templates/memory-template.md](templates/memory-template.md)
- 编号状态模板：[templates/devdocs-state-template.md](templates/devdocs-state-template.md)
- 最佳实践：[templates/best-practices.md](templates/best-practices.md)
