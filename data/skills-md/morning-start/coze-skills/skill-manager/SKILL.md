---
name: skill-manager
version: v1.5.0
author: skill-manager
description: 高阶技能管理系统，支持技能全生命周期管理、文档规范制定、技能整合拆分及工作流编排；提供简单/复杂技能文档编写标准，确保文档质量与可维护性
tags:
  [
    skill-management,
    documentation-standards,
    integration,
    decomposition,
    workflow,
  ]
---

# Skill Manager

## 任务目标

本 Skill 用于技能全生命周期管理，所有操作遵循**三步流程框架**：查阅信息 → 执行操作 → 检查验收。

### 核心能力

- **技能生命周期管理**: 创建新技能、修改现有技能、版本控制
- **文档规范制定**: 提供简单/复杂技能文档编写标准，指导文档分层组织
- **技能整合**: 将多个技能合并为一个新技能
- **技能拆分**: 将复杂技能拆分为多个独立技能
- **技能优化**: 应用设计模式提升技能质量

### 可选能力

- **工作流生成**: 根据技能生成标准化 WORKFLOW.md（仅在需要编排多个技能时使用）

### 触发条件

当需要创建、修改、整合、拆分或优化技能时触发。

---

## 三步流程框架

所有技能操作遵循统一的三步流程：

```
┌─────────────────────────────────────────────────────────────┐
│  第一步：查阅信息 (Research)                                  │
│  ├── 检查当前技能结构（如修改/优化现有技能）                  │
│  ├── 阅读 skill-standards.md 了解规范                        │
│  └── 理解技能目标和使用场景                                   │
├─────────────────────────────────────────────────────────────┤
│  第二步：执行操作 (Execute)                                   │
│  ├── 创建/修改/优化 SKILL.md                                 │
│  ├── 完善技能描述和能力定义                                   │
│  └── 编写使用示例和注意事项                                   │
├─────────────────────────────────────────────────────────────┤
│  第三步：检查验收 (Validate)                                  │
│  ├── 执行标准化检验（使用 skill-standards.md）              │
│  ├── 验证前言区字段完整性                                     │
│  └── 确认文档质量和一致性                                     │
└─────────────────────────────────────────────────────────────┘
```

---

## 场景操作指南

### 场景 A: 创建新技能

**生命周期**: 设计 → 开发 → 测试 → 发布
**参考文档**: [scenario-create.md](references/scenario-create.md)

### 场景 B: 修改技能

**生命周期**: 开发 → 测试 → 发布 → 维护
**参考文档**: [scenario-modify.md](references/scenario-modify.md)

### 场景 C: 优化技能

**生命周期**: 设计 → 开发 → 测试 → 发布
**参考文档**: [scenario-optimize.md](references/scenario-optimize.md)

### 场景 D: 整合技能

**生命周期**: 设计 → 开发 → 测试 → 发布
**参考文档**: [scenario-integrate.md](references/scenario-integrate.md)

### 场景 E: 拆分技能

**生命周期**: 设计 → 开发 → 测试 → 发布
**参考文档**: [scenario-decompose.md](references/scenario-decompose.md)

---

## 文档编写规范

### 简单技能 vs 复杂技能

根据技能复杂度选择合适的文档组织方式：

**简单技能**（功能单一、逻辑简单）:

- 直接在 `SKILL.md` 中完整描述所有功能
- 适用于：工具类技能、正文 < 300 行、无需复杂配置

**复杂技能**（多模块、逻辑复杂）:

- `SKILL.md` 仅作为概览和索引
- 详细内容拆分到 `references/` 子文件
- 适用于：多模块协作、需要详细文档、支持多人协作

**判断标准**:

- 功能数量：单一功能 vs 多个子功能
- 文档体量：< 300 行 vs ≥ 300 行
- 配置复杂度：简单 vs 复杂
- 依赖关系：无依赖 vs 需要编排

**详细规范**: 见 [skill-standards.md](references/skill-standards.md#agent-技能文档编写规范)

---

## 参考文档

| 文档                                                        | 用途                                 | 何时使用         |
| ----------------------------------------------------------- | ------------------------------------ | ---------------- |
| [skill-standards.md](references/skill-standards.md)         | 标准化规范 + 检验指南 + 文档编写规范 | 所有操作前查阅   |
| [scenario-create.md](references/scenario-create.md)         | 场景：创建新技能                     | 创建技能时       |
| [scenario-modify.md](references/scenario-modify.md)         | 场景：修改技能                       | 修改技能时       |
| [scenario-optimize.md](references/scenario-optimize.md)     | 场景：优化技能                       | 优化技能时       |
| [scenario-integrate.md](references/scenario-integrate.md)   | 场景：整合技能                       | 整合技能时       |
| [scenario-decompose.md](references/scenario-decompose.md)   | 场景：拆分技能                       | 拆分技能时       |
| [workflow-generation.md](references/workflow-generation.md) | 工作流生成（可选）                   | 需要编排工作流时 |

---

## 注意事项

- **核心原则**: 所有技能操作必须遵循"查阅-执行-检查"三步流程
- **标准化优先**: 创建/修改技能前务必阅读 skill-standards.md
- **质量保障**: 每个操作完成后必须执行标准化检验
- **版本控制**: 重要修改需更新版本号并记录变更
- **向后兼容**: 修改时尽量保持向后兼容

---

## 使用示例

### 示例: 创建新技能（完整三步流程）

**需求**: 创建数据清洗技能

**第一步：查阅信息**

```
1. 阅读 skill-standards.md
   - 命名规范：使用 data-cleaner
   - 前言区必需字段：name, version, author, description, tags
   - description 长度：100-150 字符

2. 阅读 scenario-create.md
   - 了解创建流程
   - 生命周期：设计→开发→测试→发布

3. 分析需求
   - 核心问题：清洗原始数据
   - 目标用户：数据分析师
   - 触发场景：获得原始数据需要预处理时
```

**第二步：执行操作**

```
1. 创建目录：mkdir data-cleaner

2. 编写 SKILL.md（包含完整元信息）：
   ---
   name: data-cleaner
   version: v1.0.0
   author: skill-manager
   description: 数据清洗技能，支持缺失值处理、去重和格式标准化
   tags: [data-cleaning, preprocessing, validation]
   ---

3. 编写正文内容（任务目标、操作步骤、示例、注意事项）

4. 创建版本标签：git tag -a v1.0.0
```

**第三步：检查验收**

```
□ 元信息完整性检查
  - name: data-cleaner（符合规范）
  - version: v1.0.0（格式正确）
  - author: skill-manager（存在）
  - description: 符合长度要求（100-150字符）
  - tags: 至少3个标签

□ 内容质量检查
  - 正文体量 < 500行
  - 包含所有必需章节
  - 示例完整可复制

检验结果: ✅ 通过
```
