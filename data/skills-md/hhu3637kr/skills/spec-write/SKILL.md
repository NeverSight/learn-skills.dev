---
name: spec-write
description: >
  撰写代码实现计划（plan.md）。由角色 spec-writer 调用。
  触发条件：(1) 角色 spec-writer 需要创建设计方案、API 规范、数据模型、架构设计、重构方案，
  (2) 用户说"创建 Spec"/"撰写设计文档"/"写技术规格"/"设计方案"，
  (3) spec/ 目录下需要新建 plan.md。
  注意：v2.0 起 plan.md 不含测试计划章节（由 spec-tester 用 spec-test 单独创建），
  execution_mode 固定为 single-agent。
  如果目录下已有 summary.md，应使用 spec-update 而非本 Skill。
---

# Spec Write

## 核心规则

### 用户确认（必须执行）

> [!important] 完成 plan.md 撰写后，**必须**使用 `AskUserQuestion` 工具等待用户确认。

```python
AskUserQuestion(
    questions=[{
        "question": "plan.md 已创建完成，请确认设计方案是否可以开始实现？",
        "header": "确认方案",
        "multiSelect": false,
        "options": [
            {
                "label": "确认，开始实现",
                "description": "设计方案正确，可以开始执行实现"
            },
            {
                "label": "需要修改",
                "description": "设计方案需要调整，请说明修改要求"
            }
        ]
    }]
)
```

### 分类目录与命名规范

| 目录 | 用途 | 适用场景 |
|------|------|----------|
| `01-项目规划` | PRD、流程设计、项目规划 | 新项目启动、功能规划 |
| `02-架构设计` | 架构、数据模型、服务层设计 | 架构设计、数据结构 |
| `03-功能实现` | 功能实现、API、集成方案 | 新功能开发、API 接口 |
| `04-问题修复` | Bug 修复、重构方案 | Bug 修复、代码重构 |
| `05-测试文档` | 测试计划、测试报告 | 测试准备、测试总结 |
| `06-已归档` | 已完成的 Spec（自动移动） | 由 spec-execute 归档 |

**文件夹命名**：`YYYYMMDD-HHMM-任务描述`（任务描述**必须中文**）

**路径示例**：
```
✅ spec/03-功能实现/20260104-0900-专业评价Agent设计/plan.md
❌ spec/20260104-design/plan.md          （未放入分类目录）
❌ spec/03-功能实现/20260104-feature/plan.md  （任务描述必须中文）
```

## 工作流程

| 步骤 | 操作 | 要点 |
|------|------|------|
| 1 | 读取 exploration-report.md（如有） | 了解背景、现状、历史经验 |
| 2 | 与 spec-tester 讨论接口边界 | 确认异常处理、验收边界 |
| 3 | 确定文档类型和分类目录 | 根据需求类型选择 01-05 目录 |
| 4 | 确定文件夹命名 | `YYYYMMDD-HHMM-中文任务描述` |
| 5 | 创建文件夹 | `mkdir -p "spec/分类目录/文件夹名"` |
| 6 | 选择模板 | 详见 [references/templates.md](references/templates.md) |
| 7 | 撰写 plan.md | 详见 [references/plan-template.md](references/plan-template.md) |
| 8 | 验证路径和命名 | 分类目录正确、日期时间当前、任务描述中文 |
| 9 | 保存文件 | `Write` 工具保存到目标路径 |
| 10 | 等待用户确认 | **必须**使用 `AskUserQuestion` 工具 |

### 步骤 7：plan.md 内容要求（v2.0）

> [!important] v2.0 变更：移除测试计划章节
> plan.md **不再包含**测试计划章节（由 spec-tester 用 spec-test 单独创建 test-plan.md）。
> `execution_mode` **固定为 `single-agent`**（不再使用 agent-teams 模式）。

**必须包含的章节**：
1. 概述（背景、目标、范围）
2. 需求分析
3. 设计方案
4. 执行模式（固定 single-agent，说明理由）
5. 实现步骤
6. 风险和依赖
7. 文档关联

Frontmatter 格式和字段说明详见 [references/plan-template.md](references/plan-template.md)。

## 禁止与推荐

**禁止**：
- ❌ Spec 确认前开始编写代码
- ❌ 在 plan.md 中包含测试计划章节（v2.0 起移除）
- ❌ 将 execution_mode 设为 agent-teams
- ❌ 直接在 `spec/` 下创建文件夹（必须放入分类目录）
- ❌ 任务描述使用英文
- ❌ 跳过用户确认步骤

**推荐**：
- ✅ 先读取 exploration-report.md 了解背景
- ✅ 与 spec-tester 讨论接口边界
- ✅ 使用 Obsidian Callout 和双链增强文档

## 后续流程

1. 等待用户确认 plan.md
2. 通知 TeamLead，TeamLead 触发实现阶段（spec-execute）
3. 如果是功能更新，使用 `spec-update` 执行
