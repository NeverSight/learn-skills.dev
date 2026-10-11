---
name: jackal-state-machine
description: |
  STOCK TRADING ONLY — Classify a stock's current price action into 1 of 5 states
  (Breakout / Range / Pullback / Deep-Correction / Structural-Break) from Jackal Quant's
  framework, and output the corresponding position-sizing playbook. Use when user types
  English: "what state is $TICKER in", "state classify NVDA", "Jackal state for MRVL",
  "5-state $TICKER", or Chinese: "$TICKER 现在是哪个 state", "$TICKER 在哪个阶段",
  "$TICKER 的 5态分类", "用 Jackal 框架看 $TICKER".

  DO NOT trigger for: software state machines, code state diagrams, finite-state
  automata, React state, Redux state, or any non-equity-market query. If "state" appears
  without a ticker symbol or market context, do NOT invoke.
---

# Jackal 5-State Machine — 股票价格状态分类

> **Source**: Jackal Quant 深度研报 (2026-05-17)
> **Purpose**: 每天看盘前花 5 分钟判断个股处于哪个 state，对应执行哪套操作。
> **Edge**: 散户最大的 alpha 杀手是「在 State 2 当成 State 1 追、在 State 3 当成 State 5 割」。Identify the state correctly = avoid 80% of position-sizing mistakes.

---

## When to invoke (CRITICAL — 防误触)

### ✅ Trigger when ALL of these are true:
1. A clear **stock ticker** is mentioned (`$TICKER`, `NVDA`, `MRVL`, "苹果", "英伟达") OR a stock/options/equity context is established
2. User asks "state", "阶段", "状态", "5态", "Jackal" in equity-market context

### ❌ Do NOT trigger when:
- User is writing/reviewing **code** (React state, useState, state machines, FSM, XState)
- User mentions "state" in a software/devops/AI agent context
- User talks about US states (California state, Texas state)
- No ticker or market context is clear
- User is in `cr-review`, `design-doc`, `playwright-cli`, `humanize-tone` flow

If ambiguous, ask: "你是问 $TICKER 股票的 5-state 分类吗？还是软件 state machine？"

---

## The 5 States (核心定义)

### State 1 · 突破并站稳 (Breakout & Hold)
**判断标准 (ALL of):**
- 价格突破前期关键阻力位 (e.g., 52W high, multi-month resistance)
- 连续 2 个交易日收盘高于突破位
- 突破日 volume ≥ 30 日平均的 1.5x (理想 2x+)
- MACD histogram 转正
- MA 排列: Price > 20EMA > 50MA > 200MA (完美多头)

**少数能成立的 state**（每年 <15% 时间）
**操作**: 用「突破回踩 (breakout pullback)」策略，**不要**直接追涨
- 激进派 (Aggressive): 30% 仓位在突破日尾盘买
- 标准派 (Standard): 30% 等回踩到突破位 +0-3% 范围买
- 保守派 (Conservative): 20% 等突破后整理 3-7 天再买

### State 2 · 区间震荡 (Range-bound) — 最常见 60% 概率
**判断标准:**
- 价格在前期高点的 5-15% 区间内 oscillate
- volume 萎缩到 30 日平均的 0.7x 或以下
- MACD histogram 在 zero line 附近反复
- 缺少明确 breakout 方向

**操作**: 轻仓试探，等催化剂
- 激进派: 可在区间下沿 15-20% 仓位小仓试探
- 标准派 / 保守派: **完全按兵不动**

### State 3 · 回踩支撑 (Pullback to Support) — 最优加仓机会
**判断标准 (ALL of):**
- 价格从近期高点回撤至 20EMA / 50MA / 关键密集成交区
- volume 萎缩到 30 日平均的 0.6x 以下
- 5min RSI 回到 40-50 区间 (从超买回归中性)
- 价格未跌破上升趋势线

**操作**: 这是 Jackal 框架里 **R/R 最好的入场**
- 激进派: 40% 目标仓位
- 标准派: 50% 目标仓位
- 保守派: 20% 试探仓 (其余等 State 4)

### State 4 · 深度回调 (Deep Correction) — 年 1-2 次的绝佳 BUY
**判断标准 (任一即可):**
- 触发: earnings miss / 宏观恐慌 / sector-wide selloff
- 单日跌幅 ≥ 10%, volume 巨量 ≥ 30 日平均 4 倍
- 价格深度回调至历史关键支撑 (200MA, jump-up base, 38.2-61.8% Fib retracement)
- 短期 RSI < 25 (oversold)

**操作**: 绝佳的 buy opportunity，**所有风格都该建仓**
- 激进派: 60-80% 目标仓位
- 标准派: 60-80% 目标仓位
- 保守派: 60-80% 目标仓位

**注意**: 这种 capitulation scenario 一年只有 1-2 次，错过非常可惜。

### State 5 · 跌破结构性破坏 (Structural Break)
**判断标准 (ALL of):**
- 跌破 jump-up base 或前期 4 月密集区下沿
- 跌破伴随 volume 放大
- 出现真实 fundamentals 负面事件 (e.g., guidance cut, major customer loss, accounting issue)
- 200MA 趋势线开始 roll over

**操作**: 清仓离场。两周不看盘让情绪 reset，再决定要不要重新参与。
- 所有风格: 清仓 0% 仓位

---

## 输入参数 (Inputs)

最少需要：**1 个 ticker symbol** (e.g., `MRVL`, `NVDA`, `IREN`)

可选附加：
- 当前价格 (current price) — 若未提供，调用 `mcp__yfmcp__yfinance_get_ticker_info`
- 时间框架 (timeframe, default = daily)
- 用户风格 (Aggressive / Standard / Conservative — 默认按用户偏好或问)

---

## 执行流程 (Algorithm)

```
Step 1: Validate trigger
  - 确认 ticker 存在 (yfinance lookup)
  - 确认是 equity context (NOT code, NOT US states)

Step 2: Pull data
  - Current price, prev close
  - 20EMA, 50MA, 200MA
  - 52W high/low
  - 30-day average volume, last 5 days volume
  - MACD (12,26,9) histogram + signal/macd lines
  - RSI(14) daily + 5min if intraday data available
  - 1-2 月前的关键 resistance / support cluster

Step 3: Score each state
  - State 1 checklist (5 conditions) → boolean each
  - State 2 checklist (4 conditions)
  - State 3 checklist (4 conditions)
  - State 4 checklist (4 conditions, any one trigger)
  - State 5 checklist (4 conditions)

Step 4: Pick the state with MOST conditions met
  - If tied between 2 and 3, default to 2 (most conservative)
  - If State 5 has any trigger, override (worst-case first)
  - If State 4 has any trigger, prioritize buy opportunity

Step 5: Output playbook
  - Current state + confidence (high/medium/low)
  - Conditions met / not met (transparent reasoning)
  - Aggressive / Standard / Conservative action
  - Specific entry zones (use Jackal-price-ladder if needed)
```

---

## 输出格式 (Output Template)

```markdown
# $TICKER · Jackal State Machine 判断

**现价**: $XXX.XX (后市 $XXX.XX, $YYYY-MM-DD)
**判断状态**: **State N · [状态名]**
**置信度**: High / Medium / Low

## 触发条件 check (N/M 满足)

✅ 条件 1: ...
✅ 条件 2: ...
❌ 条件 3: ...
...

## 操作建议

| 风格 | 仓位 | 入场区域 | Stop |
|------|------|----------|------|
| Aggressive | XX% | $A-$B | $S1 |
| Standard | XX% | $A-$B | $S1 |
| Conservative | XX% | $A-$B | $S1 |

## 接下来 1-2 周看什么

- 关键 level: $X (上方阻力) / $Y (下方支撑)
- 关键 catalyst: [财报日 / 宏观事件 / 行业新闻]
- 状态转换信号: 突破 $X → State 1; 跌破 $Y → State 5

## 一句话
[Plain English/Chinese summary]
```

---

## 真实案例 (Real Example, 来自原文)

**MRVL 在 2026-05-17 的判断**:
- 现价: $176.89
- State: **State 2 · 区间震荡**
- 理由: 5/13 attempted breakout $190.39 failed → rejected → 5/15 -3.12% to $176.89
- 操作: 轻仓试探 OK，all-in 不行
- 最佳 alpha: 等 5/27 财报后的 State 3 (回踩 $150-155) 或 State 4 (跌到 $128-135)

**IREN 在 2026-05-17 的判断**:
- 现价: $52.94
- State: **第 4 个圆弧底 forming** (State 3 边缘)
- 理由: 已测试 20EMA $52.02 成功, volume 衰竭 pattern 明显
- 操作: 第 4 圆弧底底部预期 $47-50, 是 institutional grade entry

---

## 反例 (Anti-patterns — DO NOT)

- ❌ 在 State 1 突破日中盘市价单追入 (用 breakout pullback)
- ❌ 在 State 2 震荡区上沿激进加仓 (等 State 3)
- ❌ 在 State 5 跌破后抄底 ("跌这么多总该反弹" = 接刀)
- ❌ 没有 ticker 或 market context 就触发本 skill

---

## 与其他 skills 的关系

- 配合 `jackal-price-ladder` → 拿到具体入场价位
- 配合 `jackal-tech-scan` → 验证机构资金流方向
- 财报前用 `jackal-earnings-playbook` 推演 5 phase
- 入场后用 `price-alert` 设触发提醒

---

**最后**: 这个 state 不是静态的，每天/每周都要重新判断。市场告诉你「现在是什么 state」，不是你预设的 state。
