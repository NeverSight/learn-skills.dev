---
name: jackal-earnings-playbook
description: |
  STOCK TRADING ONLY — Pre-simulate the 5-phase intraday price action that typically
  unfolds after a stock's earnings release or major binary catalyst event. Maps 3
  earnings scenarios (Beat / In-line / Miss) × 5 phases (Phase 1 First Drop / Phase 2
  Fake Bounce / Phase 3 Second Drop = Golden Entry #1 / Phase 4 Midday / Phase 5
  Closing = Golden Entry #2) with specific dollar entry zones and 40/40/20 budget
  allocation. Use when user asks English: "earnings playbook for $TICKER",
  "5-phase plan for $TICKER earnings", "how to play $TICKER earnings", "Jackal earnings
  $TICKER", or Chinese: "$TICKER 财报怎么操作", "$TICKER 财报当天的 5 phase", "$TICKER
  财报盘中怎么打", "$TICKER 财报后入场计划".

  DO NOT trigger for: agile/scrum playbooks, DevOps runbooks, incident response
  playbooks, code playbooks (Ansible), or any non-equity earnings topic. If "earnings"
  or "playbook" appears without a stock ticker, do NOT invoke.
---

# Jackal Earnings Playbook — 财报当天的 5-Phase 推演

> **Source**: Jackal Quant 深度研报 (2026-05-17) — IREN 5/15 case study + Q4 FY26 earnings 推演
> **Purpose**: 每次重要财报前 1-3 天用此 skill 推演 3 种结果 × 5 phase 的具体走势，提前布置 limit order
> **Edge**: 95% 散户在 Phase 1-2 错误入场，被套；正确的 entry 是 Phase 3 (10:30-12:00) 和 Phase 5 (14:00-16:00)

---

## When to invoke (CRITICAL — 防误触)

### ✅ Trigger when ALL:
1. 明确 **stock ticker** 在上下文 (e.g., `MRVL`, `NVDA`, `IREN`, `$AAPL`)
2. 用户提到 earnings / 财报 / Q1/Q2/Q3/Q4 / binary event / 重要数据公布
3. 是 equity 市场上下文

### ❌ Do NOT trigger when:
- "playbook" 出现在 DevOps / Ansible / incident-response 上下文
- "earnings" 指普通 "earnings = income" (员工薪资、business earnings call) 而非财报
- 没有 ticker
- User is in `cr-review`, `design-doc`, `init`, `publish-cr` flow
- 询问 macro 事件（如 Fed meeting）— 用其他 skill

If ambiguous: "你想推演哪个 ticker 的财报？"

---

## 5 Phase 框架核心理论

财报是 **binary event**。盘后 release 之后，next trading day 的盘中走势遵循非常 consistent 的 5 phase pattern：

### Phase 1 · 9:30-9:45 First Drop / Pop
**机制**: Overnight 累积的所有买卖单在开盘 15 分钟内集中释放。机构和散户的 panic / euphoria 同时爆发。
**特征**: 价格剧烈波动，单日 high 或 low 常在此 phase 第一根 K 线出现
**操作纪律**: **绝对禁止入场**。无论价格多有诱惑力。

### Phase 2 · 9:45-10:30 First Bounce / Pullback (假反弹/假下挫)
**机制**: Algo 进场做 short-term 反方向，散户跟随。
**特征**: Phase 1 跌的: 价格反弹到跌幅的 50-70% retracement; Phase 1 涨的: 价格回调到涨幅的 50%
**操作纪律**: **不追**。这是 fake bounce / fake dip。判断方法:
- 反弹幅度 < 2% 且 volume 萎缩 → 大概率假反弹
- 反弹回到跌幅一半上方 + volume 放大 → 可能真反弹 (但仍不是最佳入场点)

### Phase 3 · 10:30-12:00 Second Drop / Pop → **🥇 第一黄金入场**
**机制**: 第一波反弹失败后，剩下的 panic seller 和 stop loss triggered position 集中出货。Phase 3 的低点通常比 Phase 1 还低 3-5%。
**特征 (4 个 confirmation):**
1. 价格创当日新低 (or 新高对 beat scenario)
2. Volume 比 Phase 2 阻力放大
3. 5 分钟图 RSI 进入 oversold (<25) 或 overbought (>75)
4. 成交单笔规模变小 (panic 完成的标志)

**操作纪律**: **第一黄金补仓位**。激进派可用预算金的 40% 买入。
- 用 limit order 不要 market order (volatile day 滑点大)
- Phase 3 必须有 confirmation: 价格 ≥ Phase 3 低点 + volume ≥ Phase 2 高点 + 5min RSI <25
- 设硬性 hourly stop: 补仓后 1 小时内若再跌 3%, 减仓 1/2, 立刻认错

### Phase 4 · 12:00-14:00 Midday Digestion (午间消化)
**机制**: 机构完午饭后重新评估; 如果 Phase 3 低点能 hold, 价格通常在 Phase 3 低点 +2-4% 的 range 震荡
**特征**: Volume 萎缩，价格在窄区间运动
**操作纪律**: **观察，不动作**。看 Phase 3 低点会不会被破。
- 如果 Phase 3 低点被破 → 等 Phase 5 看新的低点
- 如果稳住 → 准备 Phase 5 second entry

### Phase 5 · 14:00-16:00 Closing Direction → **🥈 第二黄金入场**
**机制**: 14:30-15:30 是机构补仓黄金时段; 15:30-16:00 是 day trader 必须 close position 的最后理性挣扎
**两种 sub-scenario**:
- **Scenario A (60%)**: Phase 3 低点 hold 住，午后反弹，收盘价创开盘后近期高度。14:30-15:30 是第二个黄金补仓位，bottom 已 confirmed
- **Scenario B (40%)**: Phase 3 低点 hold 住，尾盘缓慢创新低，15:30-16:00 有最后一次抄底机会，day trader close position，会形成最后一波非理性抛售

**操作纪律**: **第二黄金补仓位**，预算金的 40%
- 14:30-15:30 是 Scenario A 反弹的 best entry
- 15:30-15:50 是 Scenario B capitulation 最后入场点
- 留 20% 给次日 confirm 入场

---

## 3 种财报 Scenario × 5 Phase 推演框架

### Scenario A: Beat + Raise Guide (35% 概率)
- Phase 1: gap up 12-18%, 这 15 分钟绝对不入场
- Phase 2: 进一步推高到 gap up 涨幅的 110-115% (上轨)
- Phase 3: profit taking 回到 gap up 开盘前的 102-108% 区间
  → **如果你在 gap up 当天没仓位, Phase 3 是唯一的黄金补仓位**
- Phase 4-5: 午后到尾盘大概率震荡消化, 收盘在 gap up 后 +3 to +8% 区间

### Scenario B: In-line (40% 概率, 最常见)
- Phase 1: gap up 5-8% (mild positive reaction)
- Phase 2: First Bounce 到 gap up 顶部
- Phase 3: 回到接近 gap up 开盘价或之下, **buy the dip 最佳时机** (基本面没坏, 只是预期没超预期)
  → R/R 3-4 倍, 非常优秀的入场
- Phase 4: 午盘震荡, Phase 3 低点 hold
- Phase 5: 14:30-15:30 反弹回到 gap up middle, 收盘 +2 to +4%

### Scenario C: Miss (25% 概率)
- Phase 1: gap down 15-25%, 这是最危险的 15 分钟
- Phase 2: First Bounce 反弹 30-40% retracement → fake bounce
- Phase 3: 进一步下探 to 4 月或近期支撑 (常对应 50MA + 200MA 双线握手区)
  → **这种 scenario 下探是「institutional grade」入场, R/R 接近 4 倍**
- Phase 4: 午后能 hold, 大概率反弹到 Phase 1 跌幅 70% retracement
- Phase 5: 如果 Phase 3 低点守住, 尾盘大概率反弹到 -15 to -20% 之间收盘 (vs 开盘 -25%)

---

## 输入参数 (Inputs)

最少:
- **Ticker** (e.g., `MRVL`)
- **Earnings date** (e.g., 2026-05-27)

可选:
- 之前的 implied move from options (用 `option-wall-analysis` skill 拉)
- Pre-earnings price action (是否已经 priced in 过多预期)
- 用户的现有仓位 (决定是 add / hold / trim 策略)
- 用户风格 (Aggressive / Standard / Conservative)

---

## 执行流程 (Algorithm)

```
Step 1: Validate (ticker + earnings context)

Step 2: Pull pre-earnings data
  - 当前价格、20EMA、50MA、200MA
  - Forward EPS consensus + revenue consensus
  - Options ATM straddle → implied move %
  - Past 8 quarters earnings reaction (历史 Beat/Miss 反应)
  - 当前 Jackal State (用 jackal-state-machine 调用)

Step 3: Build 3 scenarios
  - Scenario A (Beat + Raise): probability + gap up range + 5 phase prices
  - Scenario B (In-line): probability + mild gap + 5 phase prices
  - Scenario C (Miss): probability + gap down range + 5 phase prices

Step 4: For each scenario, output 5-phase timing & price tier
  - Phase 3 entry zone: $X-$Y (40% budget)
  - Phase 5 entry zone: $A-$B (40% budget)
  - 20% reserved for next-day confirm

Step 5: Output execution plan
  - Pre-earnings: trim 20-30% locked profit (if held)
  - Pre-earnings: prep cash for Phase 3 and Phase 5
  - Day-of: phase-by-phase action checklist
  - Day-after: confirm vs revise thesis
```

---

## 输出格式 (Output Template)

```markdown
# $TICKER · Earnings Playbook · $DATE

**现价**: $XXX.XX · **财报日**: $DATE
**Implied Move**: ±X.X% (来自 ATM straddle)
**当前 Jackal State**: State N

## 前 1 周 De-risking

- 减仓 XX% locked profit (binary 风险不能 100% 承受)
- 现金弹药 = $XXX
- 已设定 Phase 3 / Phase 5 limit orders

## 3 Scenario × 5 Phase 推演

### Scenario A: Beat + Raise (35%)
| Phase | Time | 价格区间 | 操作 |
|-------|------|---------|------|
| 1 | 9:30-9:45 | gap up 到 $X-$Y | 禁止入场 |
| 2 | 9:45-10:30 | 推高到 $A-$B | 不追 |
| 3 | 10:30-12:00 | 回踩到 **$M-$N** | 🥇 40% 仓位 |
| 4 | 12:00-14:00 | $M+0~3% 震荡 | 观察 |
| 5 | 14:00-16:00 | 收盘 $P-$Q | 🥈 40% 仓位 |

### Scenario B: In-line (40%)
(同样格式)

### Scenario C: Miss (25%)
(同样格式)

## 操作纪律

第一: 不在 Phase 1 / Phase 2 操作
第二: Phase 3 必须 4 个 confirmation 同时成立才入场
第三: Phase 5 中 Scenario A 在 14:30-15:30 反弹, Scenario B 在 15:30-15:50 抄底
第四: 预算分配 Phase 3 用 40%, Phase 5 用 40%, 20% 留给次日 confirm

## 关键关注 metric (财报当天)

- Revenue / EPS 是否 beat
- Forward Guide raise / cut / maintain
- Pre-announcement 是否已 leak
- Conference call 关键 phrase
- Implied 8% move vs actual move

## 散户关注什么 (Sentiment Watch)

- Reddit / X 主流叙事
- Pre-mkt 移动 vs implied 比例
- Institutional 持仓变化 (13F 最近)
```

---

## 真实案例 (Real Case, IREN 5/15 -9.35%)

5 Phase 实际走势 (case study):
- **Phase 1 (9:30-9:45)**: 开盘 $56.74 → 冲到 $56.79 → 一路跌到 $54.50 → 第一根 K 线就是当日 high
- **Phase 2 (9:45-10:30)**: 反弹只 1.1%, volume 萎缩 → **典型 fake bounce, 不追**
- **Phase 3 (10:30-12:00)**: 一路跌到 $53.20 区间 → 测试 MA(50)=$53.33 → 精确止跌
  - 在 11:00-11:30 的 $53.20-$53.50 区间买入: 比开盘 $56.74 便宜 **6%**, 比 Phase 2 高点 $54.80 便宜 3%
- **Phase 4 (12:00-14:00)**: 反弹到 $54.30-$54.50 → 撞 EMA(20)=$52.92 上方 = 假希望
- **Phase 5 (15:00-16:00)**: 慢慢跌回 $53.20 重测 → 突然崩盘到 $52.86 → **被迫平仓最后一波**
  - 15:30-15:50 是 day trader 必须 close 的时段
  - 当日真正最低 $52.86 = 散户最后非理性抛售制造的

**结论**: 这样的 case 配 Phase 3 + Phase 5 双入场, 平均成本 ~$53, 远比开盘 $56.74 优秀

---

## 反例 (Anti-patterns — DO NOT)

- ❌ 在 Phase 1 (开盘前 15 分钟) 入场 — 这是当日最危险时段
- ❌ 在 Phase 2 高点追入 — 这是 fake bounce
- ❌ 一次性 all-in — 必须 40/40/20 分批
- ❌ 用 market order — Volatile day 滑点惊人
- ❌ Phase 3 / 5 入场后不设 hourly stop
- ❌ 没有 ticker / 财报 context 就触发本 skill

---

## 与其他 skills 的关系

- 配合 `earnings-prep` → 拿到 implied move + 历史反应
- 配合 `option-wall-analysis` → 期权 Max Pain 帮助判断 dealer pin
- 配合 `jackal-state-machine` → 判断 pre-earnings 是 State 1/2/3
- 配合 `jackal-price-ladder` → Phase 3/5 入场价位精确化
- 财报后用 `jackal-tech-scan` → 验证 institutional flow

---

**最后**: 这套 framework 适用于任何 binary event — 财报、FDA 批准、并购公告、Fed 决议、macro data release 都遵循类似 5 phase pattern。把它纳入你的肌肉记忆，赢率会显著提升。
