---
name: aile-pencil-design
description: 面向团队工作流的 Pencil 设计技能（阶段2）。基于需求与计划产出 design.pen（或声明无 UI 设计），并准备 G2 设计审查材料。
---

# Aile：Pencil 设计（aile-pencil-design）

## 概述

当 Story 涉及 UI/交互变更时，本技能用于阶段 2 产出可审查、可执行、可回溯的设计产物：

- `docs/plans/{Story-Key}/design.pen`（推荐）
- 在 `docs/plans/{Story-Key}/analysis.md` 回填 UI 设计章节与证据
- 若不产出 `.pen`，必须明确写出“本 Story 无 UI 设计”及原因

本技能采用 MCP-first 方式，核心目标是把“设计描述”升级为“设计执行规范 + 证据化门禁”。

## 来源原 Skill

- 来源：`skills/brainstorming/SKILL.md` + `skills/writing-plans/SKILL.md`
- 策略：保留原 Skill 作为基线与回退路径，本 Skill 复制改写并强化 Pencil MCP 执行规范。

## 何时使用 / 何时跳过

### 使用场景

- Story 新增页面、弹窗、关键交互流程
- 现有页面布局、状态展示、交互反馈发生变化
- 需求明确要求提供设计稿/画布/原型

### 跳过场景

- 纯后端、数据处理、脚本、配置调整且无可见 UI 变化

> 跳过时必须在 `analysis.md` 写明：**本 Story 无 UI 设计**，并给出理由。

## 输入契约（先定义再作图）

在开始 MCP 操作前，先固化以下输入：

1. 页面/模块边界：本次改动影响哪些页面或弹层
2. 状态矩阵：正常 / 空 / 加载 / 异常（必要时加权限态）
3. 交互路径：入口、主流程、失败回路、返回路径
4. 复用策略：优先复用现有组件，缺失时再新增

## 输出契约（必须遵守）

- 产物目录：`docs/plans/{Story-Key}/`
- 设计文件：`design.pen`（有 UI 变更时必需）
- `analysis.md` 的 UI 章节必须包含：
  - 页面结构
  - 核心交互流程
  - 状态设计（正常/空/加载/异常）
  - 与 PM UI 示意对照说明
  - 关键截图与布局检查结论

## 执行流程（MCP-first）

### Step 0：Pencil MCP 可执行性预检

执行前必须确认：

1. Pencil 已启动（桌面端或编辑器扩展）
2. MCP 已连接且工具可用
3. 目标文件位于项目工作区
4. 已约定保存策略（关键批次后手动保存）

若预检失败：

- 在 `analysis.md` 标记 `UI 设计阻塞`
- 记录阻塞原因、影响范围、恢复条件
- 输出最小线框说明和状态清单，待 MCP 恢复后补齐 `design.pen`

### Step 1：初始化设计上下文

按顺序调用最小工具链：

1. `open_document`
2. `get_editor_state`
3. `get_guidelines`（按场景选择）
4. `batch_get`（一次性检索可复用组件）
5. `get_variables`（缺失时再 `set_variables` 补齐最小 token）

### Step 2：分批构图（结构优先）

- 每次 `batch_design` 控制在 `<=25` 操作
- 先骨架后细节：布局框架 → 组件实例 → 文案与状态 → 视觉微调
- 推荐批次：
  - 批次 A：发现与复用
  - 批次 B：骨架搭建
  - 批次 C：核心状态（正常/空/加载/异常）
  - 批次 D：失败回路与返回路径

### Step 3：每批质量门禁（硬性）

每一批都必须完成以下检查后再进入下一批：

1. `snapshot_layout`（`problemsOnly=true`）检查重叠/裁剪/越界
2. `snapshot_layout`（常规）复核结构
3. `get_screenshot` 抽样关键节点截图（至少主流程 + 异常态）

未通过则立即修正，不允许带问题进入下一批。

### Step 4：回填计划文档

在 `analysis.md` 的 UI 小节回填：

- `.pen` 文件路径
- 状态覆盖清单（正常/空/加载/异常）
- 交互路径覆盖（入口、主流程、失败回路、返回路径）
- 遗留风险与后续动作

### Step 5：准备 G2 审查材料

PR 中至少包含：

- `analysis.md`
- `design.pen`（如有 UI 变更）
- `docs/templates/g2-design-review-checklist.md` 对应自检结果

## 失败兜底与恢复策略

1. MCP 不可用：标记阻塞并降级为线框说明，不得跳过 UI 章节
2. 权限/连接异常：先检查 Pencil 是否运行、MCP 是否可见、工作区权限是否正确
3. 保存风险：关键批次后立刻手动保存并落 Git 版本

## UI Definition of Done（DoD）

满足以下条件才允许进入开发阶段：

- 已产出并保存 `design.pen`，或明确“本 Story 无 UI 设计”
- 状态矩阵至少覆盖正常/空/加载/异常四态
- 主流程与失败回路均有可见反馈
- `snapshot_layout` 与 `get_screenshot` 验收通过
- `analysis.md` 的 UI 章节已完整回填
