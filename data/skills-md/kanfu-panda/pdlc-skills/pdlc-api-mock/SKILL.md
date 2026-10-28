---
name: pdlc-api-mock
description: 按 API 设计文档生成 Mock 数据与 Mock 服务配置，供前端联调
argument-hint: "<接口路径 | OpenAPI 文件>"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
layer: 3
stage: engineering
produces: []
requires: []
next_step: null
terminal_state: null
---

# API Mock 数据生成

<!-- @include templates/prompts/iron-law-tool.md（已内联于下方，无需另读） -->
⛔ **IRON LAW · 不可违反的硬门禁（工具型命令）**

本命令不是主链路上的阶段：**不追加 `history`，不改 `current_stage` / `next_step` / `last_phase_result`**，也不为此分配功能ID。以下规则不可协商：

1. **文件必须落盘**：正文要求创建的文件必须作为实际文件写入磁盘，不可仅在对话中输出（只要求在对话里输出的，照正文办）。
2. **自检必须执行**：产出后按本命令的自检项逐项核对，不得以"已经很好了"为由跳过。
3. **防循环**：修复只做一次，不递归。修不了的问题记进报告，继续往下走。

**违反任一条 = 立即中止当前命令，输出违规详情，等待人工介入。**
<!-- @include-end templates/prompts/iron-law-tool.md -->

根据 API 设计文档生成 Mock 数据和 Mock 服务配置，供前端联调使用。

## 工作流程
1. **阅读 API 设计**: 阅读 `docs/02_design/api/` 下的 API 设计文档
2. **生成 Mock 数据**: 为每个接口生成符合数据模型的 Mock 响应
3. **生成 Mock 配置**: 根据技术栈生成对应的 Mock 服务文件
4. **输出到指定位置**: 前端应用的 `mock/` 或 `src/services/__mocks__/` 目录

## Mock 数据要求
- 数据要贴近真实场景，不要用 "test1"、"aaa" 之类的无意义数据
- 列表接口至少生成 5-10 条数据
- 覆盖各种状态：正常数据、边界数据、空数据
- 包含分页信息
- 错误响应也要生成 Mock

## 输出格式
```json
{
  "code": 0,
  "message": "成功",
  "data": { ... }
}
```

## 要求
- Mock 数据中的中文内容要有实际含义
- 时间字段使用合理的时间范围
- ID 字段使用合理的格式（UUID/数字）
- 生成完成后告知前端同学如何启用 Mock 服务

目标接口: $ARGUMENTS

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
✅ API Mock 数据 完成
📦 产出：（生成到前端应用 mock/ 目录）
👉 下一步：（本次流程结束，无后续）
```
