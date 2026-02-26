---
name: w02-task-planning
description: 任务规划规范，适用于复杂任务（≥3步），包含需求决策和计划书创建。包含规划规范、需求决策流程和计划书生成工具。
---

# 任务规划规范

> 适用于长程任务的事前规划，通过 Plan + Checkpoint 机制确保执行可控、进度可追踪。

---

## ⚠️ 核心强制要求

### 触发条件

- 用户明确要求"规划"、"计划"、"设计方案"等
- Agent 评估任务需要 >= 3 个明确步骤
- 涉及多文件改动或架构变更

### 复杂任务必须创建计划书

| 复杂度 | 特征 | 处理方式 |
|--------|------|----------|
| 简单 | 1-2 步，单文件 | 直接执行 |
| 中等 | 3-5 步，2-3 文件 | 建议创建计划书 |
| 复杂 | >5 步，多文件/架构变更 | **必须**创建计划书 |

### 长程任务必须启用 GitHub Issue 存档（W00）

- 预计跨会话/跨天任务，或需要全局追踪进行中状态时，必须通过 `w00-workflow-checkpoint` 创建或绑定 Issue。
- 计划书需记录：`Issue #`、当前 `status`、`Next`（下一步）。
- 创建/绑定 Issue 由主流程完成；`w00-workflow-checkpoint` 仅负责后续存档与读档。

---

## AI Agent 行为要求

### 主动提议

对于复杂任务，**必须主动提议**先创建计划书：
```
检测到任务涉及 [N] 个步骤，建议先创建计划书。是否执行 scripts/generate_task_plan.py？
```

### 状态更新

每完成一个 CP 后，提醒更新状态表：
```
CP1 已完成，建议更新计划书状态表：CP1: ⬜ → ✅ 已完成 | 2026-01-22
```

并同步更新对应 Issue 的 checkpoint（含 `下一步`）。

### 与 W00 协同（自动 + 手动）

- 创建计划书并完成 Issue 绑定后可自动触发：`w00-workflow-checkpoint checkpoint`。
- 也可手动触发：`执行 /w00-workflow-checkpoint` 进行 checkpoint 存档或读档上下文。
- 若已存在 Issue：在计划书中补写 `Issue #` 并沿用状态流转。
- 若未明确 Issue 且存在多个候选：先列候选 issue（3~5 条）并让用户选择，再执行存档/读档。

### 必须等待用户决策

- 架构/技术选型
- 性能与维护性取舍
- 技术债务或临时方案

---

## 工具脚本

**脚本**：`scripts/generate_task_plan.py`

**功能**：规划 Checkpoint、生成符合规范的计划书

---

## 参考资料

- `references/planning-workflow.md` - 规划工作流详细说明（CP划分、状态标记、文件管理、文件清单格式）
- `references/requirements-decisions.md` - 需求决策流程详细说明（需求理解、方案设计、决策确认）
- `../w00-workflow-checkpoint/SKILL.md` - Workflow GitHub Issues 基础存档能力（自动 + 手动）
- `refactor-and-decompose/SKILL.md` - 规划时文件清单与模块边界约束
