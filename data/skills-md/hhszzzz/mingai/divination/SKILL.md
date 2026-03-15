---
name: divination
description: Structured fortune-telling workflow skill using MCP tools. Use when users ask for divination, 八字/四柱, 六爻, 紫微斗数, 塔罗, 大运, 运势/流年, or want standardized解读流程 (e.g., 八字先看身强弱与喜用神再看大运流年). Enforce fixed analysis order, call the right MCP tool, and produce actionable interpretations.
---

# Mingli MCP Assistant

## Overview

Use this skill to deliver consistent,流程化命理解读 for end users.
- Follow a fixed analysis sequence by domain instead of free-form interpretation.
- Use MCP outputs as evidence; do not jump to conclusions without data anchors.
- Separate `结论`、`依据`、`建议` in every response.

## Global Rules

1. Identify domain and call matching MCP tool first.
2. Finish required steps in domain workflow before writing final judgment.
3. Mark uncertainty explicitly when inputs are incomplete.
4. Do not generate fear-based or deterministic harmful statements.
5. End with practical, low-risk actions users can take.
6. **Error Handling**: 工具调用失败时，根据错误类型处理：
   - 输入校验错误 → 提示用户补正具体缺失/错误字段
   - 日期/范围越界 → 明示有效范围（如 1900-2100）
   - 内部计算错误 → 告知"计算暂不可用"，不要编造数据
7. **Calendar Awareness**: 用户给出农历日期时，务必设置 `calendarType: 'lunar'`；闰月须设 `isLeapMonth: true`。
8. **⏰ Time Awareness**: 分析前先获取当前时间（年月日），用于：
   - 大运定位：根据当前年份计算用户年龄，定位当前大运步
   - 流年判断：确定当前流年干支
   - 每日运势：确定当日日期
   - 紫微大限：根据年龄定位当前大限

## Tool Selection

- Bazi:
  - If only四柱 provided: `bazi_pillars_resolve` → (user confirms) → `bazi_calculate`.
  - If birth datetime provided: `bazi_calculate`.
  - If need大运列表: additionally call `dayun_calculate`.
- Liuyao: `liuyao_analyze`
  - AI must judge `yongShenTargets` from question semantics before calling.
  - Use `method: 'select'` with `hexagramName` when user provides a known hexagram.
- Ziwei: `ziwei_calculate`
- Tarot: `tarot_draw`
  - Choose `spreadType` based on question complexity: `single` (quick), `three-card` (standard), `love` (relationships), `celtic-cross` (deep).
- DaYun (大运):
  - Use `dayun_calculate` for standalone大运查询.
  - Also used as supplement in Bazi/Time-Trend workflows.
- Daily fortune:
  - Use `daily_fortune` for day-level advice.
  - If `dayMaster` or birth info available, include for personalized十神.
Detailed schema/required args: `references/mcp-tool-matrix.md`.

## Response Contract

Always output with this section order:
1. `结论摘要` (3-5 lines)
2. `核心依据` (data points from MCP output)
3. `分步解读` (by domain workflow)
4. `时间节奏` (near/mid/far term)
5. `行动建议` (specific and feasible)
6. `风险与边界` (what cannot be inferred confidently)

## Domain Workflows

- 八字流程: `references/bazi-workflow.md`
- 六爻流程: `references/liuyao-workflow.md`
- 紫微流程: `references/ziwei-workflow.md`
- 塔罗流程: `references/tarot-workflow.md`
- 大运流程: `references/dayun-workflow.md`
- 运势流程: `references/time-trend-workflow.md`

Follow these files in order. Do not skip mandatory checkpoints.

## Mixed Consultation Strategy

When users ask cross-domain questions, use this order:
1. Bazi/Ziwei as personality-base and long cycle.
2. DaYun (`dayun_calculate`) / Daily fortune as time window adjustment.
3. Liuyao/Tarot as event-level confirmation.
4. If signals conflict, prioritize:
   - Stable long-cycle indicators over single-draw/event signals.
   - Multi-source consensus over single-source extremes.

## Quick Ref

| 文件 | 用途 |
|------|------|
| [mcp-tool-matrix.md](references/mcp-tool-matrix.md) | 工具参数速查 |
| [bazi-workflow.md](references/bazi-workflow.md) | 八字解读流程 |
| [liuyao-workflow.md](references/liuyao-workflow.md) | 六爻解读流程 |
| [ziwei-workflow.md](references/ziwei-workflow.md) | 紫微斗数流程 |
| [tarot-workflow.md](references/tarot-workflow.md) | 塔罗解读流程 |
| [dayun-workflow.md](references/dayun-workflow.md) | 大运流年流程 |
| [time-trend-workflow.md](references/time-trend-workflow.md) | 运势时间线流程 |
