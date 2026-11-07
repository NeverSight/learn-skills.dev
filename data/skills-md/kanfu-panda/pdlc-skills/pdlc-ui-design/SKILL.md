---
name: pdlc-ui-design
description: 按 PRD 出 UI/UX 设计文档（页面线框、交互流程、四种状态）；要配色 / 字体 / 设计系统用 /pdlc-ui-design-pro
argument-hint: "<功能描述 | 页面名>"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
layer: 3
stage: design
produces:
  - docs/02_design/ui-ux/**
requires: []
next_step: null
terminal_state: null
---

# UI/UX 设计

<!-- @include templates/prompts/iron-law-tool.md（已内联于下方，无需另读） -->
⛔ **IRON LAW · 不可违反的硬门禁（工具型命令）**

本命令不是主链路上的阶段：**不追加 `history`，不改 `current_stage` / `next_step` / `last_phase_result`**，也不为此分配功能ID。以下规则不可协商：

1. **文件必须落盘**：正文要求创建的文件必须作为实际文件写入磁盘，不可仅在对话中输出（只要求在对话里输出的，照正文办）。
2. **自检必须执行**：产出后按本命令的自检项逐项核对，不得以"已经很好了"为由跳过。
3. **防循环**：修复只做一次，不递归。修不了的问题记进报告，继续往下走。

**违反任一条 = 立即中止当前命令，输出违规详情，等待人工介入。**
<!-- @include-end templates/prompts/iron-law-tool.md -->

根据需求文档，生成 UI/UX 设计方案，包含页面布局、交互流程、组件规范。

## PDLC 前置检查（必须执行，不可跳过）

1. 从用户输入中提取功能名称关键词
2. 在 `docs/01_requirements/prd/` 目录下搜索包含该关键词的 PRD 文档
   - 匹配新格式：`F<日期>-<编号>-*<关键词>*-prd.md`
   - 匹配旧格式：`YYYYMMDD-*<关键词>*-prd.md`
   - 同时检查文件内容中是否包含该关键词
3. **未找到** → 输出以下信息后**立即停止，不继续执行**：
   ```
   ⛔ PDLC 守卫：未找到与「<功能名>」相关的 PRD 文档。
   UI 设计必须基于已有的 PRD。请先运行：
   👉 /pdlc-prd <需求描述>
   ```
4. **找到** → 提取功能ID（如 `F20260326-090000`），读取该 PRD 内容，继续执行

## 工作流程

1. **阅读需求**: 阅读找到的 PRD 文档
2. **分析用户旅程**: 梳理核心用户操作路径，绘制用户旅程图
3. **页面结构设计**: 为每个页面输出 ASCII 线框图（Wireframe）
4. **交互流程设计**: 描述页面间跳转逻辑、状态变化
5. **组件清单**: 列出所需的 UI 组件及其属性
6. **输出设计文档**: 在 `docs/02_design/ui-ux/` 下创建 UI 设计文档

## 文档内容

- **文件名格式**: `<功能ID>-<功能名>-ui.md`（如 `F20260326-090000-user-auth-ui.md`）
  - 若 PRD 为旧格式无功能ID，则使用旧格式 `YYYYMMDD-<功能名>-ui.md`
- **文档顶部必须包含 PDLC 追溯头**：
  ```
  <!-- PDLC-TRACE -->
  <!-- 功能ID: F20260326-090000 -->
  <!-- 功能名称: user-auth -->
  <!-- 阶段: 设计 -->
  <!-- 前置文档: docs/01_requirements/prd/F20260326-090000-user-auth-prd.md -->
  ```
- 页面列表与层级关系
- 每个页面的 ASCII 线框图
- 交互状态说明（加载中、空状态、错误状态、成功状态）
- 响应式适配方案（如需要）
- 组件复用清单（标注哪些组件可复用已有组件）

## 线框图示例格式
```
┌─────────────────────────────────┐
│  顶部导航栏          [用户头像]  │
├─────────────────────────────────┤
│  侧边栏  │   主内容区域          │
│  ┌─────┐ │   ┌──────────────┐   │
│  │菜单1│ │   │  表格/列表    │   │
│  │菜单2│ │   │              │   │
│  │菜单3│ │   └──────────────┘   │
│  └─────┘ │   [分页器]           │
├─────────────────────────────────┤
│  底部信息栏                      │
└─────────────────────────────────┘
```

## 要求

<!-- @include templates/prompts/output-language.md（已内联于下方，无需另读） -->
🌐 **Output language for generated artifacts**

All generated artifacts (PRDs, design docs, code comments, review reports,
test plans, deployment manuals, changelog entries, etc.) follow this policy:

1. **Default — match the conversation language exactly**:
   - 用户用中文与 Claude 对话 → 产中文文档、中文代码注释、中文报告
   - User talks to Claude in English → produce English artifacts
   - User talks in another language → produce artifacts in that language
   - **Never silently default to a fixed language regardless of the user's input.**

2. **Explicit override always wins**: when the user specifies a language for
   an artifact (e.g. "write the PRD in English", "用英文写 API 设计文档",
   "output the deploy doc in Japanese"), use that language for that artifact,
   regardless of conversation language.

3. **Mixed-language requirements**: if the user wants some artifacts in one
   language and others in a different language (common: Chinese PRD + English
   API docs for partners), honour each per-artifact instruction.

4. **Uncertain**: if you cannot reliably detect the conversation language,
   ask once before producing the first artifact.

This policy applies to **content** (prose, comments, headings). It does
**not** override technical conventions like English variable names, English
git commit subjects, or English error codes when the project's conventions
require them.
<!-- @include-end templates/prompts/output-language.md -->
- 每个页面必须考虑 4 种状态：正常、加载中、空数据、异常
- 标注交互细节：按钮点击后的反馈、表单校验时机、确认弹窗等
- 如果是前端应用，同步在 `frontend/<分类>/<应用名>/docs/` 下放一份副本

设计目标: $ARGUMENTS

<!-- @include templates/prompts/handoff.md（已内联于下方，无需另读） -->
## 段四：交接（Handoff）

命令完成后必须输出以下格式的最终消息：

```
✅ <阶段名> 完成：<主要产出物路径>
📊 自检：<通过数>/<总数> 通过（若有未通过，附要点）
📦 状态快照：docs/.pdlc-state/<feature-id>.json
👉 下一步：/pdlc-<next_step>
   （如果有分叉）或 /pdlc-<alt>（条件：<选择依据>）
```

**规则：**
- 主流程命令（写状态机的命令；下一跳见正文里「本命令的状态机取值」）必须显式输出"下一步"，不可省略
- 工具型命令（Layer 3）可以没有 `next_step`，此时输出 `👉 下一步：（本次流程结束，无后续）`
- 分叉场景必须说明**选择条件**，例如"若需补充测试用例 → `/pdlc-tdd`；若测试已齐 → `/pdlc-review`"
<!-- @include-end templates/prompts/handoff.md -->

**本命令的 handoff 输出：**

```
✅ UI/UX 设计文档 完成
📦 产出：docs/02_design/ui-ux/<功能ID>-<功能名>-ui.md
👉 下一步：（本次流程结束，无后续）
```
