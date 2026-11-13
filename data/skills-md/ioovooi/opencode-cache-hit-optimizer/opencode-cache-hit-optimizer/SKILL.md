---
name: opencode-cache-hit-optimizer
description: 用于优化 DeepSeek V4 提示词缓存命中（prompt cache hits）；适用于稳定提示词（stable prompts）、AGENTS.md、/new、/compact、子代理（subagents）、思考模式（thinking modes）、提供方/模型切换（provider/model switching）、缓存命中/未命中成本分析（cache hit/miss cost analysis）。
---

# OpenCode Cache Hit Optimizer

专治一事：增 DeepSeek V4 提示词缓存命中（prompt cache hit）。法在守请求前缀（request prefix）之稳，分噪声探索（noisy exploration）与长期任务上下文（long-lived task context），并视模型（model）/ 提供方（provider）/ 思考模式（thinking mode）变更为破缓存事件（cache-breaking events）。

总律：**先保稳定前缀（stable prefix）；次减上下文（context）；并行（parallelize）必问缓存取舍（cache trade-off）。**

## 术语

- 提示词缓存（prompt cache）
- 请求前缀（request prefix）/ 前缀（prefix）
- 缓存命中（cache hit）/ 缓存未命中（cache miss）
- 命中 tokens（hit tokens）/ 未命中 tokens（miss tokens）
- 子代理（subagent）
- 思考模式（thinking mode）
- 上下文窗口（context window）

## 何时用

遇下列事，乃用：

- DeepSeek V4 缓存命中/未命中优化（cache hit / cache miss optimization）
- OpenCode 或 Atlas 长会话策略（long-session strategy）
- `AGENTS.md`、`instructions`、系统提示词稳定性（system-prompt stability）
- `/new`、`/compact`、Magic Context、DCP、压缩行为（compaction behavior）
- 子代理扇出（subagent fan-out）、探索隔离（exploration isolation）、模型分层路由（model-tier routing）
- 思考模式（thinking mode）：non-think、think-high、think-max
- 以 `prompt_cache_hit_tokens`、`prompt_cache_miss_tokens` 审 cost

若仅泛数 tokens，而不涉前缀缓存行为（cache-prefix behavior），勿用。

## Cache-First 决策流

1. **识稳定前缀（stable prefix）。** 看重复请求（repeated requests）之首：系统提示词（system prompt）、`AGENTS.md`、已配置指令文件（configured instruction files）、持久记忆（persistent memory）、早期对话（early conversation）。
2. **避前缀扰动（prefix churn）。** 勿轻改稳定指令文件（stable instruction files）；勿中途换模型（model）/ 提供方（provider）/ API key / 思考模式（thinking mode），除非收益胜缓存损失（cache loss）。
3. **择会话形态（session shape）。** 独立任务用 `/new`，复用同一启动前缀（startup prefix）；旧 turns 仍有证据或决策，则 continue。
4. **隔探索（exploration）。** 广搜（broad search）或噪声调查（noisy investigation）用子代理（subagents），保主会话（main session）clean。
5. **慎 compact。** 先本地裁剪（local pruning）或 Magic Context 式缩减（Magic Context-style reduction）；full `/compact` 会自 summary 点后重塑前缀（prefix）。
6. **以用量（usage）验。** 有 `prompt_cache_hit_tokens` / `prompt_cache_miss_tokens`，则依命中率（hit ratio）与成本影响（cost impact），不只看总 tokens（total tokens）。

## OpenCode / Atlas 法

| 情形 | 宜 | 忌 |
|---|---|---|
| 稳定项目规则（stable project rules） | 置精简持久规则（concise durable rules）于 `AGENTS.md` 或 configured `instructions` | 每 prompt 重贴项目上下文（project context） |
| 新独立任务 | `/new`，用同稳定指令前缀（stable instruction prefix） | 续污染长会话（polluted long conversation） |
| 同任务有积累证据 | 续当前会话（continue current session） | 重开而失有用已缓存前缀链（useful cached prefix chain） |
| broad file search / repo survey | 委 `@explore` 或只读子代理（read-only subagent） | 主会话塞原始搜索输出（raw search output） |
| noisy tool output | 摘发现（findings）后 reduce / drop | 巨量 output 久留主上下文（main context） |
| repeated status replies | 用稳定短式，如 `wenyan-lite` | 同一状态每回换说法 |
| emergency confusion | `/compact` 或 `/new` | 对混乱上下文（confused context）反复补 prompt |

Atlas 宜以项目文件（project files）存规划状态（planning state），只返精简阶段摘要（concise phase summaries）于主对话（main conversation）。如此既存任务连续性（task continuity），又不令原始发现（raw findings）反复入提示词前缀（prompt prefix）。

本文文言简式，非语气控制（tone-control）。其用唯二：短、稳、少易变尾部（volatile tail）。勿扩此 skill 为通用写作风格。

## DeepSeek V4 Thinking Mode 律

- 一会话（session）尽量守同一思考模式（thinking mode）。
- 主 coding / planning，质量要紧，宜 **think-high**。
- 简 search / exploration，或 cheap subagent，宜 **non-think**。
- **think-max** 宜另开 session；其或改 system prompt content，破 prefix matching。
- 模型（model）/ 提供方（provider）/ API key 变，皆视为独立缓存池（separate cache pools）。

## Subagent 取舍

子代理（subagents）护主上下文（main context），然多从新上下文（fresh context）起。用之于：

- 探索（exploration）将注入多无关工具输出（irrelevant tool outputs）
- 多独立搜索（independent searches）可并行
- cheap models 如 DeepSeek V4 Flash 足任其事
- 只需精简结果（concise result）回主代理（main agent）

若任务重依当前对话前缀（current conversation prefix），且内联处理（inline）更廉，则勿滥用子代理（subagent）。

## 验证

称 cache optimization 成前，先查：

1. 模型（model）/ 提供方（provider）/ API key / 思考模式（thinking mode）是否恒定。
2. 稳定指令文件（stable instruction files）是否改动。
3. 旧噪声输出（old noisy outputs）是否 reduce 或 isolate。
4. API usage fields（若有）：
   - `prompt_cache_hit_tokens`
   - `prompt_cache_miss_tokens`
5. 报取舍（trade-off）：命中率（hit ratio）、缓存未命中风险（cache miss risk）、上下文洁净度（context cleanliness）、预期成本影响（expected cost impact）。

## 参考

- `references/deepseek-v4-cache.md` — DeepSeek V4 cache mechanics 与 thinking-mode implications
- `references/opencode-cache-practices.md` — OpenCode / Atlas session patterns
- `references/deepseek-tui-lessons.md` — DeepSeek-TUI 经验，取其 cache optimization 义
