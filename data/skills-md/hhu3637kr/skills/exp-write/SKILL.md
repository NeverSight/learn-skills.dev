---
name: exp-write
description: 记忆写入 Skill，将重大经验写入 spec/context/experience/ 或知识记忆写入 spec/context/knowledge/，并更新对应索引（不写 MEMORY.md）。触发场景：exp-reflect 确认后、手动添加经验或知识。仅处理经验记忆和知识记忆，程序记忆使用 skill-creator，工具记忆直接编辑 Skill。
allowed-tools: Read, Write, Edit, Glob
---

# exp-write - 记忆写入 Skill

## 概述

将记忆写入 `spec/context/` 目录，并更新索引文件。支持两种记忆类型：

1. **经验记忆**（困境-策略对）→ `spec/context/experience/`
2. **知识记忆**（项目理解/技术调研）→ `spec/context/knowledge/`

**职责边界**：
- ✅ 写入 `spec/context/experience/` 目录（经验详情 + 索引）
- ✅ 写入 `spec/context/knowledge/` 目录（知识详情 + 索引）
- ❌ 不写入 MEMORY.md（由 Claude Code Auto Memory 自主管理）
- ❌ 不写入 `.claude/rules/`（由 skill-creator 管理）

**注意**：本 Skill 仅处理经验记忆和知识记忆的写入。
- 程序记忆（SOP）→ 使用 `/skill-creator` 创建
- 工具记忆 → 直接编辑目标 Skill 文件末尾

## 触发场景

- `exp-reflect` 用户确认后自动调用
- 手动添加经验：`/exp-write type=experience`
- 手动添加知识：`/exp-write type=knowledge`

## 核心文件

**经验记忆**：
- **经验索引**：`spec/context/experience/index.md`
- **经验详情**：`spec/context/experience/exp-{ID}-{中文标题}.md`

**知识记忆**：
- **知识索引**：`spec/context/knowledge/index.md`
- **知识详情**：`spec/context/knowledge/know-{ID}-{中文标题}.md`

---

## 执行流程

```
写入流程：
- [ ] 步骤 0：确定记忆类型
      从调用参数获取 type（experience 或 knowledge）
      如果未指定，根据内容判断类型

- [ ] 步骤 1：确定记忆 ID
      根据类型读取对应索引文件：
      - experience → 读取 spec/context/experience/index.md，找到最大 EXP-ID
      - knowledge → 读取 spec/context/knowledge/index.md，找到最大 KNOW-ID
      新 ID = 最大 ID + 1
      格式：三位数字，如 001, 002, 003

- [ ] 步骤 2：生成文件名
      根据类型选择前缀：
      - experience → exp-{ID}-{中文标题}.md
      - knowledge → know-{ID}-{中文标题}.md

      示例：
      - exp-001-WebSocket连接超时.md
      - know-001-TeachingAnalyzer架构.md

- [ ] 步骤 3：写入详情文件
      根据类型选择路径和模板：
      - experience → spec/context/experience/exp-{ID}-{标题}.md（使用经验模板）
      - knowledge → spec/context/knowledge/know-{ID}-{标题}.md（使用知识模板）

- [ ] 步骤 4：更新索引文件
      在对应索引文件的表格中添加新条目：
      - experience → spec/context/experience/index.md
      - knowledge → spec/context/knowledge/index.md

- [ ] 步骤 5：确认完成
      告知用户记忆已保存
      说明如何检索：/exp-search <关键词>
```

---

## 文件格式

### 经验详情文件模板（experience）

```markdown
---
id: EXP-{ID}
title: {标题}
keywords: [{关键词1}, {关键词2}, {关键词3}]
scenario: {适用场景}
created: {YYYY-MM-DD}
---

# {标题}

## 困境

{描述遇到的问题或挑战}

## 策略

1. {解决步骤1}
2. {解决步骤2}
3. {解决步骤3}

## 理由

{为什么这个策略有效}

## 相关文件

- {涉及的文件路径1}
- {涉及的文件路径2}

## 参考

- {相关链接或文档}
```

### 知识详情文件模板（knowledge）

```markdown
---
id: KNOW-{ID}
title: {标题}
type: {项目理解 / 技术调研 / 代码分析}
keywords: [{关键词1}, {关键词2}, {关键词3}]
created: {YYYY-MM-DD}
---

# {标题}

## 概述

{简要说明这个知识点的核心内容}

## 详细内容

{根据类型组织内容}

### 项目理解类示例结构：
- 项目概述
- 核心架构
- 数据流
- 关键模块
- 技术栈

### 技术调研类示例结构：
- 背景
- 方案对比
- 优缺点分析
- 结论与建议

### 代码分析类示例结构：
- 模块职责
- 核心实现
- 设计模式
- 关键接口

## 相关文件

- {涉及的文件路径1}
- {涉及的文件路径2}

## 参考

- {相关链接或文档}
```

### 经验索引文件格式 (experience/index.md)

```markdown
# 经验索引

> 使用 `/exp-search <关键词>` 检索相关经验

## 索引表

| ID | 标题 | 关键词 | 适用场景 | 一句话策略 |
|----|------|--------|----------|-----------|
| EXP-001 | WebSocket 连接超时 | WebSocket, 超时, Nginx, 心跳 | 长时间任务连接断开 | 三层防护：Nginx超时+心跳+重连 |
| EXP-002 | 多角色页面一致性 | 多角色, 页面同步, 前端 | 修改共用页面 | 共用页面修改需同步所有角色 |

## 分类索引

### 前端相关
- [EXP-001] WebSocket 连接超时
- [EXP-002] 多角色页面一致性

### 后端相关
- [EXP-003] AgentScope Memory 管理

### 架构决策
- [EXP-004] 记忆系统架构设计
```

### 知识索引文件格式 (knowledge/index.md)

```markdown
# 知识索引

> 使用 `/exp-search <关键词>` 检索相关知识

## 索引表

| ID | 标题 | 类型 | 关键词 | 一句话概述 |
|----|------|------|--------|-----------|
| KNOW-001 | TeachingAnalyzer 数据流与架构 | 项目理解 | 数据流, 架构, MainAnalyzer | 完整的视频分析流水线，从 ASR 到结果上传 |
| KNOW-002 | AgentScope 框架对比 | 技术调研 | AgentScope, 多智能体, 框架 | 多智能体框架选型分析与建议 |

## 分类索引

### 项目理解
- [KNOW-001] TeachingAnalyzer 数据流与架构

### 技术调研
- [KNOW-002] AgentScope 框架对比

### 代码分析
- [KNOW-003] MainAnalyzer 编排机制
```

---

## 命名规范

### 记忆 ID

**经验记忆**：
- 格式：EXP-{三位数字}
- 示例：EXP-001, EXP-002, EXP-003
- 递增分配，不重复使用

**知识记忆**：
- 格式：KNOW-{三位数字}
- 示例：KNOW-001, KNOW-002, KNOW-003
- 递增分配，不重复使用

### 文件名

**经验记忆**：
- 格式：`exp-{ID}-{中文标题}.md`
- 标题使用中文，简短表达主题
- 示例：
  - `exp-001-记忆系统架构设计.md`
  - `exp-002-前端多角色页面一致性.md`
  - `exp-006-AgentScope-Memory管理.md`

**知识记忆**：
- 格式：`know-{ID}-{中文标题}.md`
- 标题使用中文，简短表达主题
- 示例：
  - `know-001-TeachingAnalyzer架构.md`
  - `know-002-AgentScope框架对比.md`
  - `know-003-MainAnalyzer编排机制.md`

---

## 更新模式

当需要更新现有记忆时：

```
更新流程：
- [ ] 步骤 1：读取现有记忆文件
      根据类型读取对应文件：
      - experience → spec/context/experience/exp-{ID}-{标题}.md
      - knowledge → spec/context/knowledge/know-{ID}-{标题}.md

- [ ] 步骤 2：合并新内容
      经验记忆：
      - 补充策略步骤
      - 添加新的相关文件
      - 更新理由说明

      知识记忆：
      - 补充详细内容
      - 更新架构图或数据流
      - 添加新的相关文件

- [ ] 步骤 3：更新索引（如果关键词或场景变化）
- [ ] 步骤 4：确认完成
```

---

## 输出确认

### 新增经验记忆

```markdown
✅ 经验已保存

**文件**：spec/context/experience/exp-003-agentscope-memory.md
**索引**：已更新 spec/context/experience/index.md

💡 如果这条经验中有日常编码技巧值得跨会话记住，Auto Memory 会自动处理，无需额外操作。

检索方式：
- `/exp-search AgentScope`
- `/exp-search Memory 超限`
```

### 新增知识记忆

```markdown
✅ 知识已保存

**文件**：spec/context/knowledge/know-001-teachinganalyzer架构.md
**索引**：已更新 spec/context/knowledge/index.md

检索方式：
- `/exp-search TeachingAnalyzer`
- `/exp-search 数据流`
```

### 更新经验记忆

```markdown
✅ 经验已更新

**文件**：spec/context/experience/exp-001-websocket-timeout.md
**变更**：
- 新增策略步骤：添加重试机制
- 补充相关文件：backend/utils/retry.py

检索方式：
- `/exp-search WebSocket`
```

### 更新知识记忆

```markdown
✅ 知识已更新

**文件**：spec/context/knowledge/know-001-teachinganalyzer架构.md
**变更**：
- 补充数据流图
- 新增模块说明：ResultUploader

检索方式：
- `/exp-search TeachingAnalyzer`
```

---

## 质量检查

写入前自动检查：

### 经验记忆检查项

| 检查项 | 要求 |
|--------|------|
| 标题 | 简短明确，描述问题而非解决方案 |
| 关键词 | 3-6 个，覆盖主要概念 |
| 适用场景 | 一句话描述何时使用 |
| 困境 | 清晰描述问题背景 |
| 策略 | 具体可执行的步骤 |
| 理由 | 解释为什么有效 |

### 知识记忆检查项

| 检查项 | 要求 |
|--------|------|
| 标题 | 简短明确，描述知识主题 |
| 类型 | 明确标注：项目理解/技术调研/代码分析 |
| 关键词 | 3-6 个，覆盖主要概念 |
| 概述 | 简要说明核心内容 |
| 详细内容 | 结构化组织，层次清晰 |
| 相关文件 | 列出涉及的关键文件 |

---

## 与其他 Skill 的协作

| 场景 | 协作 Skill |
|------|-----------|
| 接收经验草稿 | ← `/exp-reflect` 生成 |
| 接收知识草稿 | ← `/exp-reflect` 生成 |
| 写入后验证 | → `/exp-search` 测试检索 |
