---
name: pdlc-standard
description: 管理 00_standards 规范型 surface 产物（add/edit/archive/index）
argument-hint: "<add|edit|archive|index> [args]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
layer: 3
stage: engineering
artifact_type: surface
produces:
  - docs/00_standards/**
requires: []
next_step: null
terminal_state: null
---

# 规范文档管理（surface 型）

<!-- @include templates/prompts/iron-law-tool.md（已内联于下方，无需另读） -->
⛔ **IRON LAW · 不可违反的硬门禁（工具型命令）**

本命令不是主链路上的阶段：**不追加 `history`，不改 `current_stage` / `next_step` / `last_phase_result`**，也不为此分配功能ID。以下规则不可协商：

1. **文件必须落盘**：正文要求创建的文件必须作为实际文件写入磁盘，不可仅在对话中输出（只要求在对话里输出的，照正文办）。
2. **自检必须执行**：产出后按本命令的自检项逐项核对，不得以"已经很好了"为由跳过。
3. **防循环**：修复只做一次，不递归。修不了的问题记进报告，继续往下走。

**违反任一条 = 立即中止当前命令，输出违规详情，等待人工介入。**
<!-- @include-end templates/prompts/iron-law-tool.md -->

管理 `docs/00_standards/` 下的团队规范（编码约定 / API 约定 / 命名规则等）。这类产物是 **surface 型**——描述"当前规范是什么"的状态快照，**就地编辑**而非 ledger 累积。

## ⛔ surface 铁律（不可违反）

1. **不允许版本化文件名**：禁止 `coding-style-v2.md` / `coding-style-2026-Q1.md` 这类 ledger 绕路。一个主题永远一个文件，就地改。
2. **就地编辑 + `_changelog.md`**：每次修改在同目录 `_changelog.md` 追加一条（日期 / 命令 / 变更摘要）。
3. **git log 是真实审计链**：演进历史靠 `git log <file>` 看，不靠多份文件。
4. **归档不删除**：废弃的规范用 `archive` 子命令移到 `docs/.archive/standards/`（与 `/pdlc-arch` 共用统一 archive 根 `docs/.archive/`），留 stub 指向新位置。

## 段一：执行子命令

从本命令的参数解析：

### `add <category>/<name>`
新建规范。`category` 如 `coding` / `api` / `naming`。
1. 在 `docs/00_standards/<category>/<name>.md` 创建（**确认不存在同名 v2 变体**）
2. 文件顶部加 `<!-- artifact_type: surface -->` 标记
3. 同目录 `_changelog.md` 追加创建记录
4. 更新 `docs/00_standards/_index.md`

### `edit <path> <change>`
就地编辑已有规范。改完在 `_changelog.md` 追加变更摘要。**禁止**另存为新版本文件。

### `archive <path>`
移到 `docs/.archive/standards/`，原位置留 stub（一行指向新位置 + 废弃原因）。

### `index`
扫描 `docs/00_standards/**`，重新生成 `_index.md`（按 category 分组列出所有规范 + 一句话摘要）。

## 段二：自检（强制）

<!-- @include templates/prompts/self-audit.md（已内联于下方，无需另读） -->
## 段二：自检（强制）

重新阅读本次产出物，按质量关卡清单逐项检查。勾选已通过，标注未通过原因。

> **注意**：自检清单的具体内容由各命令自行定义，本片段只规定结构。

## 段三：修复（单次，不递归）

针对自检段标注为未通过的项：

- **可自动修复**：直接修复（如补缺字段、修正格式、补齐缺失段落）
- **修复后回验**：再次运行自检，确认被修复项现在通过
- **无法自动修复**：记录到自审报告，不再尝试，流程继续

⚠️ 单次修复原则：若一轮修复后仍有项未通过，**不再递归修复**，防止死循环。
<!-- @include-end templates/prompts/self-audit.md -->

### 规范管理自检清单

- [ ] 无版本化文件名泄漏（`*-v[0-9]` / `*-20[0-9][0-9]*` 模式不存在）
- [ ] 本次涉及的 `_changelog.md` 已追加记录
- [ ] 新建/修改的规范文件含 `artifact_type: surface` 头标记
- [ ] `_index.md` 与实际文件一致（无遗漏 / 无悬空条目）

## 段三：修复（单次，不递归）

<!-- @include templates/prompts/loop-prevention.md（已内联于下方，无需另读） -->
## 防循环规则

本命令所有的自检-修复循环均受以下约束：

1. **单次检查**：同一个自检清单在本次命令执行中只跑一次（起始 + 修复后验证共两次读）
2. **单次修复**：发现的问题只尝试修复一轮
3. **不递归**：修复后不再重新触发自检的全量重跑
4. **失败降级**：无法自动修复的问题 → 记录到自审报告 → 流程继续 → 最终报告标注待人工处理

这是为了防止 agent 在"修完再查、查完再修"的往返中陷入死循环。
<!-- @include-end templates/prompts/loop-prevention.md -->

- 可自动修复（漏更 `_changelog.md` / `_index.md` 不一致）→ 直接补
- 发现版本化文件名 → 提示用户合并到主文件（不自动合并，避免丢内容）

## 段四：交接

> **状态机豁免**：本命令非 feature-scoped，不更新 `<feature-id>.json`。同 `/pdlc-changelog`。

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
✅ 规范操作完成：<子命令> <参数>
📦 已更新：docs/00_standards/<...> + _changelog.md + _index.md
👉 下一步：本次流程结束
```

---

**规范操作**: $ARGUMENTS
