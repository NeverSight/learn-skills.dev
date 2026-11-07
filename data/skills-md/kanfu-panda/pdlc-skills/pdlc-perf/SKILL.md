---
name: pdlc-perf
description: 性能优化——先测基线，再逐项改、同一命令复测，报告写优化前后的实测数字；测不了就只出分析
argument-hint: "<功能ID | 优化目标>"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
layer: 3
stage: quality
produces:
  - docs/04_testing/perf/<feature-id>-report.md
requires: []
next_step: null
terminal_state: null
---

# 性能优化

<!-- @include templates/prompts/iron-law-tool.md（已内联于下方，无需另读） -->
⛔ **IRON LAW · 不可违反的硬门禁（工具型命令）**

本命令不是主链路上的阶段：**不追加 `history`，不改 `current_stage` / `next_step` / `last_phase_result`**，也不为此分配功能ID。以下规则不可协商：

1. **文件必须落盘**：正文要求创建的文件必须作为实际文件写入磁盘，不可仅在对话中输出（只要求在对话里输出的，照正文办）。
2. **自检必须执行**：产出后按本命令的自检项逐项核对，不得以"已经很好了"为由跳过。
3. **防循环**：修复只做一次，不递归。修不了的问题记进报告，继续往下走。

**违反任一条 = 立即中止当前命令，输出违规详情，等待人工介入。**
<!-- @include-end templates/prompts/iron-law-tool.md -->

对指定服务或应用进行性能分析并提出优化方案。

## 分析维度

### 后端性能
- **数据库层**: 慢查询、N+1 问题、缺失索引、全表扫描
- **缓存层**: 缓存命中率、缓存策略（过期/淘汰）、缓存穿透/击穿/雪崩
- **接口层**: 响应时间、并发处理、连接池配置
- **代码层**: 算法复杂度、内存泄漏、不必要的序列化/反序列化

### 前端性能
- **加载性能**: 首屏时间、资源体积、代码分割、懒加载
- **运行时性能**: 不必要的重渲染、大列表虚拟滚动、防抖/节流
- **网络优化**: 请求合并、资源压缩、CDN 配置
- **缓存策略**: 浏览器缓存、Service Worker、本地存储

## 工作流程

> 没有测量就没有优化：**改代码之前先有基线，改完之后用同一把尺子复测**。

1. **定指标与测量手段**：要优化的指标（接口 p50 / p95 延迟、吞吐、查询耗时、首屏时间、包体积、内存）及能**重复执行**的测量命令——
   项目已有的 benchmark / 压测脚本、`EXPLAIN ANALYZE`、Lighthouse CLI、`hyperfine`、`time` 等。
   **找不到可重复的测量手段** → 只做分析、给方案，**不改代码**，报告里标「未测量」
2. **测基线**：同一命令至少跑 3 次取中位数，记下环境（机器、数据量、并发数）
3. **识别瓶颈**：有 profile / 慢查询日志 / 火焰图就以它为准，读代码推测只作补充，并注明是推测
4. **一次只改一项**：按投入产出比排序，逐项实施
5. **复测**：同一命令、同一环境、同样次数；**没有可测提升的改动回退**，不留「理论上更快」的改动
6. **确认行为不变**：跑 `docs/00_standards/test-commands.yml` 的 `unit`，测试必须仍然通过
7. **【必须创建文件】** 在 `docs/04_testing/perf/` 下创建性能优化报告：`<功能ID>-report.md`（不针对具体功能时用 `YYYYMMDD-<服务名>-report.md`）

> ⚠️ **必须创建文件，不可仅在对话中输出。**

## 报告格式

**文档顶部包含 PDLC 追溯头**：
```
<!-- PDLC-TRACE -->
<!-- 功能名称: <服务名> -->
<!-- 阶段: 性能优化 -->
<!-- 创建时间: <ISO 8601> -->
```

**报告内容**：

| 序号 | 位置 | 问题描述 | 优化方案 | 测量命令 | 优化前 | 优化后 | 结论 |
|------|------|----------|----------|----------|--------|--------|------|

> 「优化前 / 优化后」填实测中位数（带单位与环境）；没测的填「未测量」，结论写「未验证」，不得填预期值冒充。

**创建后验证**：确认文件已存在于 `docs/04_testing/perf/` 目录

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
- 优化方案按投入产出比排序（性价比高的优先）
- 给出优化前后的代码对比
- 不要为了优化而牺牲代码可读性

优化目标: $ARGUMENTS

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
✅ 性能优化报告 完成
📦 产出：docs/04_testing/perf/<feature-id>-report.md
👉 下一步：（本次流程结束，无后续）
```
