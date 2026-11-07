---
name: pdlc-changelog
description: 未发版时按 git 记录手动刷新 CHANGELOG 的 [未发布] 段；正式发版由 /pdlc-ship 一并处理
argument-hint: "[版本号]"
allowed-tools: Read, Write, Edit, Bash
layer: 3
stage: engineering
produces:
  - CHANGELOG.md
requires: []
next_step: null
terminal_state: null
---

# 更新变更日志

<!-- @include templates/prompts/iron-law-tool.md（已内联于下方，无需另读） -->
⛔ **IRON LAW · 不可违反的硬门禁（工具型命令）**

本命令不是主链路上的阶段：**不追加 `history`，不改 `current_stage` / `next_step` / `last_phase_result`**，也不为此分配功能ID。以下规则不可协商：

1. **文件必须落盘**：正文要求创建的文件必须作为实际文件写入磁盘，不可仅在对话中输出（只要求在对话里输出的，照正文办）。
2. **自检必须执行**：产出后按本命令的自检项逐项核对，不得以"已经很好了"为由跳过。
3. **防循环**：修复只做一次，不递归。修不了的问题记进报告，继续往下走。

**违反任一条 = 立即中止当前命令，输出违规详情，等待人工介入。**
<!-- @include-end templates/prompts/iron-law-tool.md -->

根据最近的 git 提交记录，更新指定服务或应用的 CHANGELOG.md。

## 工作流程
1. 运行 `git log` 查看最近的提交记录
2. 按约定式提交分类：feat / fix / docs / chore / refactor / test
3. 更新对应服务/应用的 `CHANGELOG.md`，使用 本 skill 目录下的 `assets/changelog-template.md` 作为格式与分节模板
4. 遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/) 格式

## 分类规则
- **新增（Added）**: feat 类型的提交
- **修复（Fixed）**: fix 类型的提交
- **变更（Changed）**: refactor 类型的提交
- **移除（Removed）**: 删除功能相关的提交
- **文档（Docs）**: docs 类型的提交

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
- 每条记录简洁明了，描述"做了什么"和"为什么"
- 如果涉及破坏性变更，需特别标注

目标: $ARGUMENTS

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
✅ 变更日志 完成
📦 产出：CHANGELOG.md
👉 下一步：（本次流程结束，无后续）
```
