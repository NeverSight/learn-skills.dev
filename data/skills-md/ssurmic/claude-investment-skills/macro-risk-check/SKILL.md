---
name: macro-risk-check
description: Daily/weekly macro risk radar. Checks VIX, MOVE, yields, USD/JPY, market breadth, CTA positioning, credit spreads. Outputs red/yellow/green regime signal with specific action thresholds. Triggers in English ("macro check", "regime read", "is the market safe", "risk on or off", "should I add now") or Chinese ("看一下宏观", "市场风险怎么样", "现在能加仓吗", "regime", "宏观扫一下").
---

# Macro Risk Check — Daily/Weekly Radar

## Goal

Catch the next **2024/8/5 (yen carry)** or **1973 (oil + inflation)** event BEFORE it happens. Provide a binary "go / slow / stop" signal for adding risk.

## The 8 Indicators (run all in parallel)

### 1. Volatility Indices
| Indicator | Healthy | Warning | Crisis | Action |
|---|---|---|---|---|
| **VIX** | <18 | 18-22 | >22 | >22 → reduce risk 25% |
| **VVIX** (VIX of VIX) | <90 | 90-105 | >105 | >105 → tail risk rising |
| **MOVE** (bond vol) | <80 | 80-100 | >100 | >100 → bond market panic, equity follows |

**Tools:**
- `mcp__yfmcp__yfinance_get_ticker_info` for `^VIX`, `^VVIX`, `^MOVE`
- WebSearch: "VIX MOVE current level"

### 2. Treasury Yields
| Indicator | Healthy | Warning | Crisis | Action |
|---|---|---|---|---|
| **10Y yield** | <4.5% | 4.5-5.0% | >5.0% | >5% → growth stocks 杀估值 |
| **30Y yield** | <5.0% | 5.0-5.3% | >5.3% | >5.3% = term premium unwind |
| **10Y-2Y spread** | >0 (steepener) | flat | inverted | Bear steepener (long up, short flat) = stagflation警报 |
| **3M-10Y spread** | positive | inverted | deeply inverted | Inversion = recession 6-12mo |

**Tools:** `^TNX`, `^TYX`, `^FVX`, `^IRX` via yfmcp

### 3. Currency / Carry Trade
| Indicator | Healthy | Warning | Crisis | Action |
|---|---|---|---|---|
| **USD/JPY** | <155 | 155-160 | >160 (干预红线) | <153 = yen carry unwind 启动 |
| **DXY** | 95-100 | <95 or >102 | >105 | >105 = EM 危机 |
| **CNH/USD** | <7.30 | 7.30-7.35 | >7.40 | >7.40 = 中国资本外流 |

**Tools:** `JPY=X`, `DX-Y.NYB`, WebSearch

### 4. Credit Spreads
| Indicator | Healthy | Warning | Crisis | Action |
|---|---|---|---|---|
| **HYG (High Yield ETF)** | rising or flat | falling | <52W low | <52W low = credit panic |
| **JNK** | same | same | same | 同上 |
| **HY-IG OAS spread** | <300 bps | 300-400 | >450 | >450 = recession risk |
| **CDX HY** | <400 | 400-500 | >500 | 同上 |

**Tools:** `HYG`, `JNK`, `LQD` via yfmcp

### 5. Market Breadth
| Indicator | Healthy | Warning | Crisis | Action |
|---|---|---|---|---|
| **% S&P > 200DMA** | >70% | 50-70% | <50% | <60% with SPX at ATH = 顶部背离 |
| **% S&P > 50DMA** | >65% | 40-65% | <40% | 同上 |
| **NYSE A/D line** | rising | flat | falling | Falling A/D + index up = distribution |
| **New highs vs lows** | >2:1 | 1:1 | <1:1 | <1:1 = breadth dying |
| **RSP/SPY ratio** | rising | flat | falling | Falling = mega-cap concentration |

**Tools:** WebSearch "S&P 500 percent above 200DMA today"

### 6. Positioning / Flows
| Indicator | Healthy | Warning | Crisis | Action |
|---|---|---|---|---|
| **CTA SPX exposure** | <60th %ile | 60-85th %ile | >85th %ile | >85th = forced unwind risk |
| **HF gross leverage** | <290% | 290-310% | >310% | GS PB metric, >310% = 拥挤 |
| **HF net leverage** | <50th %ile | 50-90th %ile | >90th %ile | 同上 |
| **NAAIM Exposure** | <80 | 80-95 | >95 | >95 = manager all-in |
| **AAII Bull** | 25-45% | <25% or 45-60% | >60% | >60% = 散户 euphoria |
| **CBOE Put/Call** | 0.7-1.0 | <0.5 or >1.3 | <0.4 | <0.4 = call buying euphoria |

**Tools:** WebSearch (CTA + HF data are private, dealers publish weekly)

### 7. Specific Asset-Class Crowding
- **SOXL AUM** (3x semi ETF): >$10B = 散户进场 verge
- **TQQQ AUM**: 同上
- **NVDA single-stock weight in ETFs**: >20% in QQQ/SMH
- **Mag 7 % S&P**: >32% = 1999 类似集中

### 8. Geopolitical / Event Risk Calendar
**This week / next 30 days:**
- Fed FOMC meeting
- BOJ policy meeting (yen carry trigger)
- ECB meeting
- OPEC+ meeting
- Trump-Xi summits, G20
- Major elections (Taiwan, US states)
- Iran/Hormuz tension
- Major earnings (NVDA, AAPL, MSFT, GOOGL, META, AMZN, AMD, AVGO, ORCL)

**Tools:** `WebSearch`: "Fed meeting [next month]", "BOJ meeting [next month]"

## Composite Score & Action

Count how many indicators are in **WARNING** or **CRISIS**:

| Warning + Crisis count | Regime | Action |
|---|---|---|
| 0-2 | 🟢 GREEN | Normal allocation, can add |
| 3-5 | 🟡 YELLOW | Slow, no new adds, trim leverage |
| 6-9 | 🟠 ORANGE | Active reduce 20%, raise cash to 30% |
| 10+ | 🔴 RED | Crisis stance, cash 50%+, hedge with puts |
| Any in CRISIS | 🔴 RED | Override above |

## The "Trigger" hierarchy (in order of severity)

1. **VIX > 25 + MOVE > 100 same week** = Volmageddon precedent
2. **USD/JPY < 153** = Yen carry unwind 启动
3. **HYG < 52W low + 30Y > 5.3%** = Credit + duration 双杀
4. **% S&P > 200DMA < 50% while SPX at ATH** = 顶部分发
5. **OPEC cut + Iran/Hormuz** = 1973 重演
6. **CTA at 95th %ile + breadth dying** = 强制平仓 setup

## Output format

```markdown
# Macro Risk Check — [Date]

## Verdict: [🟢/🟡/🟠/🔴]

[One paragraph: regime + recommended action]

## 8-Indicator Dashboard

| # | Indicator | Value | Status | Triggered? |
| 1 | VIX | XX.XX | 🟢/🟡/🔴 | |
| ... | ... | ... | ... | ... |

## Triggers Activated
- [List any specific triggers from the hierarchy]

## Macro Events Next 30 Days
| Date | Event | Why it matters |

## Recommended Action
- Cash level: X%
- Hedges: [SPY puts? Yen call? Gold?]
- Don't add: [list sectors]
- Can add: [list sectors if any]

## Watch list (next 7 days)
- [Specific levels to watch]
```

## Hard rules

1. **Run all 8 indicators every time.** Don't cherry-pick.
2. **CRISIS in any one indicator overrides composite.** Single point of failure principle.
3. **Compare to historical analogs.** 2018/2 (Volmageddon), 2020/3 (COVID), 2022 (rate shock), 2024/8/5 (yen carry), 2025/4 (DeepSeek+tariffs).
4. **Be specific.** "Macro looks bad" ≠ analysis. "VIX 22.5 + MOVE 95 + USD/JPY 156 + CTA 87th %ile = 3 yellow + 1 orange = ORANGE regime, raise cash to 30%."
5. **Cite sources.** WebSearch results need URL.
6. **Don't anchor to bull narrative.** If 6+ indicators flash, the answer is RED regardless of how good the AI story is.

## Schedule recommendation

This skill should run **automatically every Monday morning** via `schedule` skill. Cadence:
- Daily: if any indicator was ORANGE+ last check
- Weekly: default
- Pre-event: 24h before Fed/BOJ/major earnings
- Pre-Trump-Xi summit / OPEC / major catalyst: 24h before

## Historical regime examples

| Date | Regime | What happened |
|---|---|---|
| 2018/2/5 | 🔴 RED | Volmageddon, S&P -10% in 1 week |
| 2020/2/24 | 🟠→🔴 | COVID, S&P -34% over 5 weeks |
| 2022/1 | 🔴 RED | Tech crash, NDX -33% over year |
| 2024/8/5 | 🔴 RED | Yen carry unwind, NDX -13% in 3 weeks |
| 2025/4 | 🟠 | DeepSeek + tariffs, NVDA -27% |
| 2026/5 (now) | ? | (compute fresh) |
