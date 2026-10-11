---
name: jackal-price-ladder
description: |
  STOCK TRADING ONLY — Builds a 16-level price ladder for a stock (8 resistance levels
  above current price + 8 support levels below) with order-flow interpretation for
  each level. Annotates each level by type (psychological / MA / Fib / cluster /
  rejection / EMA / jump-up base), strength, and the actual order-flow meaning (e.g.,
  "$210 = 20EMA = trend follower algo trigger"). Use when user asks English: "price
  ladder for $TICKER", "support and resistance for NVDA", "key levels on MRVL",
  "what are the supports below $TICKER", "Jackal ladder $TICKER", or Chinese:
  "$TICKER 的阻力支撑价位", "$TICKER 的 price ladder", "$TICKER 上下关键 level",
  "$TICKER 上方阻力下方支撑", "Jackal 价格阶梯 $TICKER".

  DO NOT trigger for: pricing ladders in SaaS pricing strategy, salary ladders, career
  ladders, abstraction ladders, or any non-equity-market topic. If "ladder" or
  "support" appears without a stock ticker, do NOT invoke.
---

# Jackal Price Ladder — 16-Level 阻力支撑 + Order Flow 解读

> **Source**: Jackal Quant 深度研报 (2026-05-17) — IREN 关键 price level 的 order flow 拆解 + MRVL 价格阶梯
> **Purpose**: 每个 price level 背后**有不同的 order flow 含义**，知道这些含义才能精确加仓/减仓
> **Edge**: 90% 散户只画水平线，不解读「为什么这个 level 重要」。本 skill 让你每个 level 都有「谁在这个价位有 buy/sell limit order」的清晰认知。

---

## When to invoke (CRITICAL — 防误触)

### ✅ Trigger when ALL:
1. 明确 **stock ticker** (e.g., `MRVL`, `IREN`, `$NVDA`)
2. 用户问 阻力 / 支撑 / level / price ladder / 加仓位 / 减仓位 in equity context

### ❌ Do NOT trigger when:
- "ladder" 出现在 SaaS pricing tier / career growth / corporate ladder 上下文
- "support" 指 customer support / IT support 而非股价支撑
- 没有 ticker
- User is in coding flow

If ambiguous: 问 "你想要哪个 ticker 的 price ladder?"

---

## Level 类型 (Type Catalog)

每个 price level 都有一个或多个 type, 不同 type 代表不同的 order flow 含义:

### 1. Psychological Level (心理整数关口)
**例**: $50, $100, $150, $200
**Order flow 含义**:
- 散户的 buy limit 和 stop loss 集中在整数附近 (e.g., $50.00, $49.95)
- Algo 的 round-number trigger 也在这里
- 因此整数关口经常 act as magnet 或 strong S/R
**强度**: 中等

### 2. MA Levels (20EMA / 50MA / 200MA)
**Order flow 含义**:
- **20EMA** = trend follower systematic strategy 的 trigger level. 所有用 20EMA 做 bench 的 algo 会在这里 trigger 调整 position
- **50MA** = CTA (managed futures) + risk parity funds 的 trend health check. 跌破 50MA = institutional algo 的 first 减仓信号
- **200MA** = institutional bear/bull line. 跌破 200MA = 大型机构 (pension, sovereign wealth) 才会触发的 mandate-driven 减仓
**强度**: 高 (50MA, 200MA 是机构 grade)

### 3. Cluster of Past Trading Activity (历史成交密集区)
**Order flow 含义**: 这个区间在过去几周/几月反复成交, 意味着大量散户和 swing trader 的 cost basis 在此. 他们要么在这里 take profit (上行), 要么 cut loss (下行)
**强度**: 中-高
**识别方法**: Volume profile 高峰区 / 多日 candle 收盘在窄区间

### 4. Rejection Zone (拒绝区)
**Order flow 含义**: 这个 level 在过去 2-3 个交易日内被价格 touch 后立刻被拒绝, 形成 upper shadow 或 lower shadow. 大量机构 limit order 挂在这里
**强度**: 高 (短期)
**例**: MRVL $190-191 被两次 reject → strong sell wall

### 5. Fib Retracement (38.2% / 50% / 61.8%)
**Order flow 含义**: 这些是技术分析师 + algo 的常用 entry/exit level. 跌到 38.2% 是 healthy correction; 跌到 50-61.8% 是 deeper correction; 跌破 61.8% 是 trend 可能反转
**强度**: 中

### 6. Jump-up Base (跳空缺口起点)
**Order flow 含义**: 跳空 gap 之前的 base 是 "如果跌回这里, 趋势就真的结束了" 的位置. 跌破伴随放量 = structural break
**强度**: 极高 (long-term)

### 7. UBS/Analyst Target (分析师目标价)
**Order flow 含义**: 当价格接近分析师 target, 会有大量机构 trigger profit taking (target reached) 或 add (above target = momentum extension). 这是 institutional bench
**强度**: 中

### 8. Blow-off Top / Capitulation Low
**Order flow 含义**: Pattern 极端的位置. Blow-off top 是 momentum buyer 全部认清 = 上方稀薄阻力; Capitulation low 是 panic seller 全部卖光 = 下方稀薄支撑. 这种位置 V-reverse 概率 70%+
**强度**: 极高 (events-driven)

---

## 输入参数 (Inputs)

最少: **1 个 ticker** (e.g., `MRVL`)

可选:
- 当前价格 (若未提供, 用 yfinance fetch)
- Lookback (default 90 days)
- Timeframe (daily 默认, weekly 用于更长期 level)
- 是否要 LEAPS 相关 level (option Max Pain, Put/Call Walls)

---

## 执行流程 (Algorithm)

```
Step 1: Validate (ticker + equity context)

Step 2: Pull data via yfinance
  - 90-day OHLCV
  - Compute 20EMA, 50MA, 200MA
  - Find swing highs/lows (last 90 days)
  - Identify volume profile peaks (high-volume zones)
  - Get analyst target prices

Step 3: Identify 8 levels above current price (resistance)
  - Nearest swing high
  - Round number above ($X.00)
  - 20EMA (if above price, else skip)
  - Latest 1-2 day high (today + yesterday)
  - 50MA (if above)
  - Cluster of past trading (any volume peaks above)
  - Analyst target (if above)
  - 52W high
  - Recent rejection zones

Step 4: Identify 8 levels below current price (support)
  - Recent intraday low
  - Round number below
  - 20EMA (if below)
  - 50MA + 200MA cluster
  - Jump-up base
  - 4-month cluster
  - Fib retracement levels (from latest swing)
  - 200MA
  - 38.2% Fib of bull run

Step 5: Annotate each level with type + order flow meaning + strength
  - Multiple types can apply to same level (stacking = strongest)
  - Order flow meaning is the KEY differentiator from a regular S/R chart

Step 6: Output 2 stacked tables (resistance above, support below)
```

---

## 输出格式 (Output Template)

```markdown
# $TICKER · Jackal Price Ladder

**现价**: $XXX.XX
**Timeframe**: daily, 90-day lookback
**当前 Jackal State**: State N (from jackal-state-machine)

## 上方阻力 (Resistance) — 8 levels

| 价格 | 距现价 | Type | Order Flow 含义 | 强度 |
|------|--------|------|----------------|------|
| $X.XX | +0.X% | 1日盘中高 + 5日开盘价 | 最近 supply zone, day trader 集中 | 中 |
| $X.XX | +X.X% | Cup with Handle target + rejection zone | 已被 touch + rejected; 第二次到这里若再 reject 形成 double top | 高 |
| $X.XX | +X.X% | UBS target | 分析师目标价; touch 后机构 trigger profit taking | 中 |
| ... | ... | ... | ... | ... |

## 下方支撑 (Support) — 8 levels

| 价格 | 距现价 | Type | Order Flow 含义 | 强度 |
|------|--------|------|----------------|------|
| $X.XX | -X.X% | 最近 daily low + short-term 心理位 | 最近关键支撑 | 中 |
| $X.XX | -X.X% | 20EMA | 激进派加仓第一信号; trend follower algo trigger | 高 |
| $X.XX | -X.X% | 50MA + 200MA "双线握手" | 50MA/200MA 都用作 trigger; CTAs + risk parity funds 在这里 | 极高 |
| $X.XX | -X.X% | Jump-up base | 跌破 = 整个上升结构失效, structural break | 极高 |
| ... | ... | ... | ... | ... |

## 价格阶梯使用指南

### 加仓决策
- 价格在 [level X-Y] 之间: 激进派 [%] / 标准派 [%] / 保守派 [%]
- 价格跌穿 [critical level]: 转向 [State 5 清仓 / 等 Phase 5 / 重新评估]
- 价格突破 [critical level]: 转向 [追涨 breakout pullback / next target Y]

### 减仓决策
- 价格冲到 [level A]: 第一档减仓 [%]
- 价格冲到 [level B]: 第二档减仓 [%]
- 价格冲到 [level C]: 锁定大部分利润

### 关键 catalyst-dependent level
- 财报 [DATE] 后 Scenario A (Beat): 关键 level 升级为 [...]
- 财报 [DATE] 后 Scenario C (Miss): 关键 support 是 [...]
```

---

## 真实案例 (Real Case — IREN, 2026-05-17)

### 上方阻力
| 价格 | Order Flow 含义 |
|------|----------------|
| $56-58 | 5/13-14 反复被拒的实际成交集中区, **upper rejection zone**. 散户在 $54-56 之上挂 limit sell order. 突破需要 3+ 连续收盘 + 单日 volume > 60M shares |
| $61.20-61.72 | **双重 blow-off top**. 5/8 + 5/11 两次 intraday 冲高被打回. Institutional consensus 上限是 $61. 突破需要 Q4 FY26 earnings beat 或 Anthropic/Google 新合同 |
| $64 | 1月底/5月初的"horizontal resistance". 长中线投资者的 profit taking trigger |
| $76.41 | **去年 11 月全年高点**. 突破 $76 意味着脱离 bitcoin miner 标签升级为 AI infrastructure peak valuation |

### 下方支撑
| 价格 | Order Flow 含义 |
|------|----------------|
| $52.02 | **20-day EMA**. 所有用 20EMA 的 algo 都会在这里调整 position |
| $50 | 心理整数关口. 散户 stop loss + 抄底买单集中 |
| $47-48 | **第四个圆弧底**预期底部, "institutional bid stacking" (机构 limit buy order 集中在此) |
| $44.72-$43.86 | **50MA + 200MA "双线握手"**. 极重要的支撑 — 跌穿这里就别说自己看好这只票了 |
| $42.86 | 4 月底 swing low. 跌破 = "higher lows" 结构性 thesis 被打破 |
| $33-36 | 4 月低点 + 12 月低点区域. **value investor 的 absolute floor**. 对 IREN 长期信仰的 fund 都在此 level 大量建底 |

### 阶梯使用指南
- 现价 $52.94: 已贴 20EMA $52.02, **第四个圆弧底 forming**
- 跌到 $47-50 (第四圆弧底): 激进派 60-80%, 标准派 50% 仓位入场
- 跌到 $44-45 (双线握手): institutional algo 必然 defend, 加仓的最佳 level
- 跌破 $42: 4 月底 swing low 被破, 重新审视 thesis
- 突破 $58: cup with handle 完成, 准备追到 $64

---

## 反例 (Anti-patterns — DO NOT)

- ❌ 把所有 level 都当成 "S/R 线" 处理, 不知道每个 level 的 order flow 来源不同
- ❌ 忽略 stack (e.g., 50MA + 200MA + Fib 50% 同时在 $X 附近 = 极强支撑)
- ❌ 用 weekly 时间框架做 day trader 决策 (反之亦然)
- ❌ 没有 ticker / 代码上下文就触发本 skill

---

## 与其他 skills 的关系

- 配合 `jackal-state-machine` → 当前 state 决定使用哪段 ladder (State 3 看下方, State 1 看上方)
- 配合 `jackal-tech-scan` → 验证 level 的 institutional flow
- 配合 `jackal-earnings-playbook` → Phase 3 / Phase 5 入场用此 ladder 精确化
- 配合 `option-wall-analysis` → 期权 Max Pain + Gamma Walls 也是 price ladder 的一种

---

**最后**: 这个 ladder 不是静态的。每次 earnings、major event、200MA 移动后都要重新生成。把每个 level 的 order flow 含义内化 → 你才能在恐慌中不接刀, 在贪婪时不追高。
