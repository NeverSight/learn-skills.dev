---
name: jackal-tech-scan
description: |
  STOCK TRADING ONLY — Multi-indicator technical deep-scan combining MA alignment,
  RS Line divergence, MACD convergence, volume signature, and 200-MA deviation extremity
  check to infer institutional money flow direction. Outputs "smart money is doing X"
  conclusion with transparent reasoning. Use when user asks English: "tech scan $TICKER",
  "technical analysis NVDA", "institutional flow MRVL", "is smart money buying $TICKER",
  "Jackal tech scan", or Chinese: "$TICKER 技术面深度扫描", "看一下 $TICKER 机构资金流",
  "$TICKER 的 RS line / MA / MACD 综合判断", "Jackal 技术分析 $TICKER".

  DO NOT trigger for: code "tech debt scan", "tech stack analysis", security scans,
  vulnerability scans, dependency scans, or any non-equity technical analysis. If
  "tech scan" appears without a stock ticker, do NOT invoke.
---

# Jackal Tech Scan — 多指标技术面深度扫描

> **Source**: Jackal Quant 深度研报 (2026-05-17) — Marvell & IREN 技术面分析章节
> **Purpose**: 用 5 个独立指标交叉验证一个核心问题 — **机构资金现在在买还是在卖？**
> **Edge**: 99% 散户只看 K 线和 MA。Volume signature + RS Line 是 institutional money 留下的指纹。

---

## When to invoke (CRITICAL — 防误触)

### ✅ Trigger when:
1. 明确的 **stock ticker** (e.g., `MRVL`, `NVDA`, `$IREN`)
2. User asks for 技术面/机构资金/RS line/MA/MACD/volume analysis in equity context

### ❌ Do NOT trigger when:
- "tech scan" 出现在代码/安全/devops 上下文 (security scan, vulnerability scan, npm audit, code quality)
- 没有 ticker
- User is in coding flow (`cr-review`, `playwright-cli`, `design-doc`)
- 询问 sector / macro 技术面而非个股

If ambiguous: 问 "你想扫的是哪个 ticker？是技术面分析还是别的？"

---

## 5 个核心指标 (五个面)

### 指标 1 · MA 多头排列 + 200MA 偏离度
**做什么**：
- 检查 Price / 20EMA / 50MA / 200MA 的排列
- 计算价格距 200MA 的偏离 %

**判读规则**:
- 完美多头: `Price > 20EMA > 50MA > 200MA` → bullish trend follower 都在做多
- 偏离 200MA **+90% or more** = historic top 1% → **强警告**，平均 45 个交易日内回到 200MA + 50% 内
- 偏离 < +30% = healthy trend
- 价格跌破 50MA = trend follower 第一次担忧
- 价格跌破 200MA = institutional algo 大幅减仓

**输出**: bullish stack / aging trend / extreme extension / breaking down

---

### 指标 2 · RS Line (Relative Strength vs SPY/VTI) — 最重要的领先指标
**做什么**：
- 计算个股相对 Vanguard Total Stock Market (VTI) 或 SPY 的 RS Line
- 比较「RS line 创新高」 vs 「价格创新高」是否同步

**判读规则** (这是机构 rotation 的指纹):
- RS Line 与价格同步创新高 = healthy uptrend
- 价格创新高但 **RS Line 未创新高** = **bearish divergence** (机构 quietly rotating out, 领先价格 1-3 周)
- RS Line 从 historic high 回落 5-15% 但仍在 high range = warning, not exit
- RS Line 跌破自己的 50DMA = institutional money 转向出 (sell signal)

**历史案例 reference**:
- TSLA 2021 年 11 月见顶: RS Line 前 2 周开始走弱
- SMCI 2024 年 7 月见顶: RS Line 前 3 周见顶
- 这种 pattern 非常 consistent

---

### 指标 3 · MACD (12,26,9) Convergence
**做什么**:
- 看 MACD line, Signal line, Histogram 三个数值
- 关注 convergence (收敛) 和 divergence (背离)

**判读规则**:
- 两条线都在下降 + Histogram 收窄但仍为正 = **bearish convergence in uptrend** (momentum 在衰减，但还没翻转)
- 两条线都在上升 + Histogram 扩大 = strong bullish momentum
- Histogram 从负转正 = momentum 转向上 (买入信号)
- Histogram 从正转负 = momentum 转向下 (减仓信号)
- MACD 出现 bearish divergence (价格新高但 MACD 未新高) = warning

---

### 指标 4 · Volume Signature — 机构 vs 散户的指纹
**做什么**:
- 拉过去 10-15 个交易日 volume
- 标注每天 volume / 30 日 average ratio
- 与当日 price action 配对判读

**核心 patterns**:

**Accumulation signature (机构在买)**:
- 连续 3-5 个 spike day, volume 2-3x average, **全部放量上涨**
- volume profile 是阶梯式抬升
- 这是 institutional money 在分批建仓 (bull trend 起点)

**Distribution day (机构在卖)**:
- 单日 volume 3-4x average, 价格下跌或先涨后跌
- 这是 institutional money 在 unload
- 1 周内出现 2-3 个 distribution day = institutional 系统性减仓

**Selling exhaustion (卖盘衰竭, 买入信号)**:
- 连续 3 次放量下跌, volume 递减 (e.g., 37M → 30M → 24M)
- 这是典型的 selling exhaustion 前兆
- 5-8 个交易日内反弹 3-8% 概率约 75%

**Buyer-led vs Seller-led market**:
- 综合过去 10 次 volume spike → 几个是放量上涨 / 几个是放量下跌
- 比例 7:3+ = buyer-led; 4:6+ = seller-led

---

### 指标 5 · 200-MA Deviation Extremity Check
**做什么**:
- 计算当前价格 / 200MA 的比例 - 1
- 与该 ticker 过去 20 年的历史偏离分布对比 (用 percentile)

**判读规则**:
- 偏离 > +90% = **historic 前 1% 极端水平** → 平均 45 个交易日内回到 +50% 以内
- 偏离 +60% ~ +90% = 警告区，但不是 sell signal
- 偏离 +30% ~ +60% = healthy uptrend
- 偏离 < +30% = 还有上行空间
- 偏离 < -10% = 进入 oversold territory

**用法**: 即便 fundamentals 没问题，技术面会告诉你 margin of safety 已经接近 0

---

## 综合判断 (Synthesis)

把 5 个指标分别打分后，做加权综合判断:

### Bull Conclusion (机构在买)
- MA 多头排列 ✅
- RS Line 同步创新高 ✅
- MACD 上升收敛 ✅
- Volume 持续 accumulation ✅
- 偏离 200MA < +60% ✅

→ **结论**: institutional money 在 accumulation 阶段，可加仓 (配合 State Machine)

### Bear Warning (机构在悄悄出货)
- MA 还在多头但价格跌破 20EMA ⚠️
- **RS Line 比价格领先 1-3 周走弱** ⚠️
- MACD bearish convergence ⚠️
- 最近出现 2+ distribution day ⚠️
- 偏离 200MA > +90% ⚠️

→ **结论**: 机构在 rotate out, 减仓而不是清仓; 等下一个 State 3 重新进

### Capitulation Signal (恐慌底)
- 跌破 50MA 但站住 200MA
- RS Line 也在历史低位
- MACD 已经跌到极端低位
- **Volume 出现 selling exhaustion pattern (递减放量下跌)**
- 单日 -10%+ panic sell

→ **结论**: institutional money 即将抄底，3-5 个交易日内大概率反弹 (75%+)

---

## 输入参数 (Inputs)

最少：**1 个 ticker** (e.g., `MRVL`, `NVDA`, `IREN`)

可选:
- Timeframe (daily / weekly, default daily)
- Lookback (default 90 days for context)
- 是否要对比 SPY (default yes)

---

## 执行流程 (Algorithm)

```
Step 1: Validate (ticker + equity context, NOT code)

Step 2: Pull data via mcp__yfmcp__yfinance_get_price_history
  - 200 days of OHLCV
  - Compute 20EMA, 50MA, 200MA
  - Compute MACD(12,26,9)
  - Compute RSI(14)
  - Compute RS Line = ticker_price / SPY_price × 100

Step 3: Run 5 sub-analyses
  - Sub 1: MA stack + 200MA deviation
  - Sub 2: RS Line trend + divergence vs price
  - Sub 3: MACD convergence pattern
  - Sub 4: Volume signature (last 10 days spike analysis)
  - Sub 5: Deviation extremity percentile vs 20yr history

Step 4: Synthesize
  - Score each indicator: bullish / neutral / bearish (-1, 0, +1)
  - Weighted sum: RS Line 30%, Volume 25%, MA 20%, MACD 15%, Deviation 10%
  - Map to: Strong Bull / Bull / Neutral / Bear / Strong Bear / Capitulation

Step 5: Output with reasoning + divergence flags
```

---

## 输出格式 (Output Template)

```markdown
# $TICKER · Jackal Tech Scan

**现价**: $XXX.XX · **时间**: $YYYY-MM-DD
**综合判断**: [Strong Bull / Bull / Neutral / Bear / Strong Bear / Capitulation]
**置信度**: High / Medium / Low

## 5 指标分别打分

### 1. MA 排列 + 200MA 偏离
- Price $X | 20EMA $Y | 50MA $Z | 200MA $W
- 排列: [完美多头 / 部分破损 / 完全瓦解]
- 200MA 偏离: +XX% [percentile rank vs 20yr: PP%]
- 判读: ...

### 2. RS Line (vs SPY)
- 当前 RS: XX | 30 天前: YY | 90 天前: ZZ
- 与价格关系: [同步创新高 / 背离 / 弱于价格]
- 判读: ...

### 3. MACD
- MACD line: X.XX | Signal: Y.YY | Histogram: Z.ZZ
- Pattern: [bullish convergence / bearish convergence / strong momentum]
- 判读: ...

### 4. Volume Signature (过去 10 天)
- spike days: N (放量上涨 vs 放量下跌)
- 最近 pattern: [accumulation / distribution / exhaustion]
- 判读: ...

### 5. 200MA Deviation Extremity
- 当前偏离 +XX% (历史前 PP%)
- 判读: [extreme / warning / healthy / oversold]

## 综合结论

[Strong Bull / Bull / Neutral / Bear / Strong Bear / Capitulation]
- 看涨依据: ...
- 看跌依据: ...
- 关键 divergence: ...

## 1 周 watchlist

- 如果 ___ 发生 → 升级为 ___
- 如果 ___ 发生 → 降级为 ___
```

---

## 真实案例 (Real Example, Marvell, 2026-05-17)

**MRVL 5 指标拆解**:
1. MA 排列: ✅ 多头 (Price $176 > 20EMA $161 > 50MA $128 > 200MA $93) — 但偏离 200MA **+90%**, historic 前 1%
2. RS Line: ⚠️ 从 +96.71% 跌到 **+82.95%**, 一周丢了 14 个百分点 — **明确 institutional rotation 警告**
3. MACD: bearish convergence (两条线下降, histogram -0.634 收窄)
4. Volume: 5/7-5/15 出现 3 次 distribution day (volume 递减但全是放量下跌) = selling exhaustion 开始
5. 200MA 偏离 +90% = 极端警告

**综合结论**: **Bear Warning** (smart money 已在 5 月初开始减仓; 部分散户还在追高)
- 5/7 first warning shot (-7.1%)
- 5/15 distribution restart (-3.12%)
- 等 selling exhaustion 完成后会出现 State 3 黄金加仓

---

## 反例 (Anti-patterns — DO NOT)

- ❌ 只看 1 个指标做结论 (e.g., 只看 MACD 翻多就买)
- ❌ 忽略 RS Line divergence — 这是最强的领先指标
- ❌ 忽略 200MA deviation extremity — 即使 fundamentals 好，过度偏离也会反向
- ❌ 把 distribution day 当成 healthy correction (区别在 volume profile)
- ❌ 在无 ticker / 代码语境下触发本 skill

---

## 与其他 skills 的关系

- 配合 `jackal-state-machine` → 拿到 5 state 中的具体位置
- 配合 `jackal-price-ladder` → 拿到具体阻力支撑位
- 财报前用 `jackal-earnings-playbook` 推演
- 入场后用 `price-alert` 设定 RS Line 跌破阈值的提醒

---

**最后**: 这 5 个指标不是相互独立的，**RS Line + Volume signature 是 80% 的 alpha**，其他 3 个是 confirmation。如果时间紧，先看这两个。
