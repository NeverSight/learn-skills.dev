---
name: pdlc-arch
description: 架构分析（生成/更新 docs/ARCHITECTURE.md 系统架构总览 · surface 型）
argument-hint: "<项目 | 模块范围>"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
layer: 3
stage: design
artifact_type: surface
produces:
  - docs/ARCHITECTURE.md
requires: []
next_step: null
terminal_state: null
---

# 架构分析

<!-- @include templates/prompts/iron-law-tool.md（已内联于下方，无需另读） -->
⛔ **IRON LAW · 不可违反的硬门禁（工具型命令）**

本命令不是主链路上的阶段：**不追加 `history`，不改 `current_stage` / `next_step` / `last_phase_result`**，也不为此分配功能ID。以下规则不可协商：

1. **文件必须落盘**：正文要求创建的文件必须作为实际文件写入磁盘，不可仅在对话中输出（只要求在对话里输出的，照正文办）。
2. **自检必须执行**：产出后按本命令的自检项逐项核对，不得以"已经很好了"为由跳过。
3. **防循环**：修复只做一次，不递归。修不了的问题记进报告，继续往下走。

**违反任一条 = 立即中止当前命令，输出违规详情，等待人工介入。**
<!-- @include-end templates/prompts/iron-law-tool.md -->

对当前项目架构进行全面分析，输出架构评估报告。

## 分析维度

### 1. 服务拆分合理性
- 各微服务的职责边界是否清晰
- 是否存在循环依赖
- 服务粒度是否合适（过大/过小）
- 数据归属是否明确

### 2. 通信机制
- 服务间通信方式（同步REST/gRPC、异步消息队列）
- 是否存在分布式事务问题
- 接口版本管理策略
- 错误传播和容错机制

### 3. 数据架构
- 数据库拆分策略（每服务独立数据库 vs 共享）
- 数据一致性方案
- 缓存策略
- 数据备份与恢复

### 4. 可观测性
- 日志规范（结构化日志、链路追踪ID）
- 监控指标（RED指标：Rate/Errors/Duration）
- 告警策略
- 分布式追踪

### 5. 可扩展性
- 水平扩展能力
- 负载均衡策略
- 容量规划

<!-- @include templates/prompts/layout-detect.md（已内联于下方，无需另读） -->
## 先探测项目布局（不要套用写死的目录）

下文出现的 `backend/services/`、`frontend/web/` 等路径只是**空项目时的默认布局**。动手创建或扫描目录之前，先看项目实际长什么样：

1. **monorepo 标志**：`pnpm-workspace.yaml`、`turbo.json`、`nx.json`、`lerna.json`、`package.json` 的 `workspaces`、
   `go.work`、`Cargo.toml` 的 `[workspace]`、`settings.gradle(.kts)` 的 `include` → 按其中声明的目录（如 `apps/`、`packages/`、`services/`、`crates/`）理解布局
2. **已有单元的位置**：在 `backend/services/`、`services/`、`apps/`、`packages/`、`cmd/`、`crates/` 下找已存在的服务 / 应用，新单元放在**同级**，命名与目录结构照着已有的来
3. **单体与全栈框架**：只有一个 `src/`，或是框架默认结构（`manage.py` + 各 app、Rails 的 `app/`、Next.js 的 `app/` / `pages/`、Spring Boot 单模块）→ 按框架约定放，**不要**新建 `services/` 一类平行目录
4. **空项目或判断不了** → 才用下文的默认布局；执行前把将要创建的路径列给用户确认（`--autonomous` 下记入 `auto_decisions[]`）

把探测结论写进本次报告：**布局类型 + 依据的文件 + 新内容的落点**。判断错了的代价是在用户仓库里长出一套平行目录，比多问一句贵得多。
<!-- @include-end templates/prompts/layout-detect.md -->

## 工作流程

> **架构总览是 surface 型产物**：`docs/ARCHITECTURE.md` 描述"系统当前长什么样"，**就地覆盖更新**，不按日期累积多份文件。演进历史靠 `git log docs/ARCHITECTURE.md` 追溯。这与 per-feature 的 `docs/02_design/architecture/F-xxx-arch.md`（ledger 型，记录"为某个 feature 为什么改架构"）分工互补。

1. 扫描 `backend/` 和 `frontend/` 下的所有服务和应用
2. 阅读 `docs/02_design/architecture/` 下的 per-feature 架构 ledger（若有）
3. 分析代码中的依赖关系和调用链路
4. **遗留检测**：若发现旧版按日期命名的 `*-arch-analysis.md`（散落在 `docs/02_design/architecture/` 或旧 review 目录，即 v1.0 的 v1..v5 累积模式），提示并移到 `docs/.archive/architecture/`，以最新一份作为 `ARCHITECTURE.md` 的起点
5. **【必须创建/更新文件】** 就地生成/覆盖 `docs/ARCHITECTURE.md`（参考 本 skill 目录下的 `assets/architecture-overview-template.md`）

> ⚠️ **必须写入磁盘，不可仅在对话中输出。**

## 输出格式

文件路径：`docs/ARCHITECTURE.md`（固定，就地覆盖）

**文档顶部包含 PDLC 追溯头 + surface 标记**：
```
<!-- artifact_type: surface -->
<!-- PDLC-TRACE -->
<!-- 功能名称: 架构总览 -->
<!-- 阶段: design -->
<!-- 创建时间: <执行时的实际 ISO 8601 时间戳> -->
```

**报告内容**：
- 架构全景图（文本描述 / mermaid）
- 服务拆分 / 通信 / 数据 / 可观测性 / 可扩展性 各维度评分（1-5）
- 问题清单与改进建议

**创建后验证**：确认 `docs/ARCHITECTURE.md` 已存在且为本次内容

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
- 评价要客观，给出依据
- 建议要可操作，标注优先级
- surface 铁律：不创建带日期/版本号的架构文件，永远就地覆盖 `ARCHITECTURE.md`

$ARGUMENTS

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
✅ 架构总览已更新：docs/ARCHITECTURE.md
📦 surface 型就地覆盖（历史见 git log docs/ARCHITECTURE.md）
👉 下一步：（本次流程结束，无后续）
```
