---
name: earnings-flash-dip-catch
description: |
  STOCK TRADING ONLY — Build a post-earnings "catch the flash dip, sell the strength"
  ladder (财报接飞刀 / 盘后捞货). Pulls latest + after-hours price, the key stats,
  option walls + max pain + the straddle expected move, finds the MOST-RECENT price
  shelf, and outputs tiered limit-buy catch levels + sell levels + a structural stop.
  Use when user asks Chinese: "$TICKER 财报接飞刀", "$TICKER 财报后怎么接", "盘后捞货",
  "$TICKER 闪跌接刀", "财报后抄底 $TICKER", "$TICKER 财报砸下来怎么买", or English:
  "catch the dip on $TICKER earnings", "$TICKER post-earnings flash dip", "where to buy
  $TICKER after earnings", "$TICKER earnings knife-catch ladder".

  DO NOT trigger for: code/CI "flaky test" catches, exception/error catching, fishing,
  or any non-equity topic. Requires a clear ticker + an earnings/post-earnings context.
---

# 财报接飞刀 — Post-Earnings Flash-Dip Catch

> **Purpose**: 财报夜股价插针,在高概率的位置接刀、在阻力位卖出。
> **The #1 rule (born from the MRVL $170 error)**: 接刀位锚定**最近的台阶**,
> 不是旧基座;并用 **实现波动 ≈ 隐含 × 0.65** 做硬校验。详见最后的 Post-Mortem。

---

## When to invoke

✅ Trigger when: a clear ticker + earnings/post-earnings context ("财报接飞刀",
"盘后捞货", "财报后怎么接", "catch the dip on X earnings").

❌ Do NOT trigger for: code "catch", error handling, flaky-test catches, or any
non-equity use of "catch/dip/knife".

---

## STEP 1 — Pull the data (exact tool calls)

Run these `mcp__yfmcp__*` tools. Do them in parallel where independent.

1. **`yfinance_get_ticker_info`** → read these fields:
   - `currentPrice`, `regularMarketPrice`, `previousClose`, `regularMarketDayLow/High`
   - `postMarketPrice`, `postMarketChangePercent`, `marketState` (`POST`/`PRE`/`REGULAR`)
   - `fiftyTwoWeekHigh`, `fiftyDayAverage`, `twoHundredDayAverage`
   - `forwardPE`, `trailingPE`, `priceToSalesTrailing12Months`, `targetMedianPrice`,
     `targetMeanPrice`, `numberOfAnalystOpinions`, `recommendationKey`
   - `earningsTimestamp` (when it reports), `beta`, `averageVolume`
2. **`yfinance_get_price_history`** with `period="5d", interval="30m", prepost=true`
   → this is the **after-hours tape**; read the actual flush low/high from the
   post-4pm-ET bars. Also pull `period="3mo", interval="1d"` for the shelf (Step 3).
3. **`yfinance_get_option_dates`** → pick the **weekly that expires just after the
   print** (for the straddle/expected move) AND the **next monthly** (for durable walls).
4. **`yfinance_get_option_chain`** for both dates. Option chains are large and will
   exceed the token limit → they save to a file. Parse with python/jq:
   - Top open-interest call strikes = **call walls** (resistance / sell-into).
   - Top open-interest put strikes = **put walls** (support / dip-catch).
   - ATM straddle mid (nearest-strike call_mid + put_mid) ÷ spot = **expected move %**.

**Caveat to always state**: the price-alert cron checker reads the *regular-session*
price (`regularMarketPrice`/`last_price`) — it will **NOT** see tonight's after-hours
flush. After-hours catching = broker extended-hours **limit** orders, not the bot.

---

## STEP 2 — Read the stats (what matters)

| Field | What it tells you |
|---|---|
| `postMarketPrice` vs `previousClose` | the actual earnings gap % (the move that happened) |
| straddle expected move % | what options PRICED IN (1σ). Realized ≈ this × 0.6–0.7 |
| `fiftyTwoWeekHigh`, run vs 50/200DMA | how extended → bigger run = bigger "sell the news" risk |
| `forwardPE`, `priceToSales`, `targetMedianPrice` | is it already above analyst targets? (premium = fragile) |
| `beta` | high beta (>2) = wider AH whipsaw |

---

## STEP 3 — Find the SHELF (the critical step I got wrong)

The primary catch is anchored to the **most-recent higher-low consolidation shelf** —
the last zone where price went sideways for 2–5 days building higher lows, *right
before* the final impulsive leg up into earnings.

**Algorithm:**
1. From the daily 3mo chart, walk BACK from the pre-earnings high.
2. Find the **last** multi-day base where the daily lows cluster (the launchpad of the
   final leg). That cluster's low = the **shelf floor** = primary catch.
3. **Use the MOST RECENT shelf. The base migrates UP with price.** If a new shelf
   formed 3 days ago, that is the anchor — NOT a shelf from 3 weeks ago.

**MANDATORY guardrail (this catches the MRVL error):**
> The shelf must be within ~1 realized move of the pre-earnings close, i.e.
> `shelf ≳ close × (1 − implied×0.65)`. If your candidate shelf is **more than ~1.3×
> the realized move** below the close, it is the WRONG (stale) shelf — go find the
> newer, higher one.

Example check: MRVL close $208, implied 13.3% → realized ≈ 8.6% → expected floor
~$190. A $170 "shelf" is −18% = **2× too far** → reject it, it's the old base.

---

## STEP 4 — The catch/sell formula

```
realized_move   = implied_straddle_pct × 0.65          # vol-risk-premium haircut
expected_floor  = pre_earnings_close × (1 − realized_move)

CATCH 1 (primary, ~50%) = the shallower (higher) of { most-recent shelf , expected_floor }
                          ≈ also the top put wall just under spot
CATCH 2 (deep, ~30%)    = next put-wall cluster below  (gap-fill; fills only if it keeps falling)
CATCH 3 (tail, ~20%)    = full 1σ implied straddle low  (rare; usually does NOT fill)

STOP                    = CLOSING break below the start of the latest leg up
                          (a structural level, NOT a vol-derived number)

SELL 1 / 2 / 3          = the stacked CALL walls above (trim 1/3 at each); max-pain
                          and prior 52wH/ATH are magnets
```

**Core mental model (never violate):**
- 跌多深取决于财报**质量**,而质量盘前**不可知** → **主仓必须放在高概率的台阶,
  绝不押在波动率尾部 (1σ)**。
- 好财报 → 跌到最近台阶就被买回(浅跌,接刀1 成交)。
- 烂财报 → 才会捅穿台阶到 1σ(接刀2/3 + 可能触发止损)。
- 所以"接刀1 成交、深接没成交"是**正常且正确**的——别去追那个不会来的深价。

---

## STEP 5 — Option walls & max pain (post-print nuance)

- **Call wall** (high call OI) = resistance the dealers defend → **sell-into** zone.
- **Put wall** (high put OI) = support the dealers defend → **dip-catch** zone.
- **Max pain** = strike where most options expire worthless = dealer magnet into OPEX.
- **After the print, the pre-earnings WEEKLY walls evaporate** (IV crush + those were
  earnings bets that close/expire). **Trust the MONTHLY walls** for durable structure;
  re-read max pain after the gap.
- Dealers can't fully hedge in the thin after-hours book → price **overshoots** the
  "fair" gamma level by a few %, then mean-reverts at the 9:30 ET open. That overshoot
  is the wick you catch with a **resting limit order**, not by watching.

---

## STEP 6 — Output template

```markdown
# $TICKER 财报接飞刀 — 接/卖阶梯

**现价**: $X (盘后 $Y, marketState)  · **前收**: $Z
**财报**: [beat+raise / in-line / miss] — [一句话实际数字]
**预期波动**: 隐含 ±A%(跨式) → 实现估计 ±B% (×0.65) → 预期下沿 ~$F
**最近台阶**: $S (建于 [日期区间])   **本段 leg 起点**: $L

| 触发 | 动作 | 依据 |
|---|---|---|
| 跌破 $CATCH1 | 接刀1 · 主仓 50% | 最近台阶 ∩ 实现波动下沿 ∩ put 墙 |
| 跌破 $CATCH2 | 接刀2 · 30% | 下一道 put 墙(仅大盘走弱) |
| 跌破 $CATCH3 | 接刀3 · 20% | 1σ 满幅(罕见,常不成交) |
| 收盘破 $STOP | 止损清仓 | 跌破本段 leg 起点 = 结构破坏 |
| 涨破 $SELL1/2/3 | 各减 1/3 | call 墙 / max pain / ATH 磁吸 |

**怎么挂**: 券商 extended-hours **限价**买单(别用市价),GTC,明早确认仍有效。
**一句话**: [浅跌买台阶 / 深跌看质量 / 破 leg 起点走人]
```

Then set the ladder as alerts in the private repo `ssurmic/invest-watchlist`
(`price-alert/scripts/add_alert.py TICKER below|above PRICE --note "..."`), commit + push.
NEVER push personal levels to the public `claude-investment-skills` repo.

---

## Worked example + POST-MORTEM (MRVL, 2026-05-27) — the guardrail

- Pre-earnings close $208 (ATH $218, ran +172% in 3mo). Weekly implied ±13.3%.
- **My error**: set CATCH 1 at **$170**, anchored to the stale 5/8–5/19 base, and
  treated the full 1σ ($174) as the expected drop. AH low was only **~$187–189** →
  never filled, missed nothing (the print was beat+raise so the dip was always going
  to be shallow).
- **Correct**: realized ≈ 13.3%×0.65 = 8.6% → floor ~$190; AND the most-recent shelf
  was **$188–190** (5/20–5/22). Both → **$190**, exactly where it bottomed. The user's
  "Jacko" call of ~$189 was right because it anchors to the recent shelf.
- **Lesson encoded**: the mandatory guardrail in Step 3 (`shelf ≳ close×(1−implied×0.65)`,
  reject anything >1.3× realized below close) makes the $170 anchor impossible.

---

## Anti-patterns (DO NOT)

- ❌ Anchor the catch to an **old/lower** base when a newer higher shelf exists.
  (The base migrates UP with price — always use the most recent shelf.)
- ❌ Put **primary size** at the full 1σ implied straddle low. That's a ~16%-probability
  tail; realized moves run ~0.65× implied. Primary goes at the shelf.
- ❌ Use the pre-earnings **weekly** option walls after the print (they evaporate).
- ❌ Use the cron alert bot to "catch" the after-hours flush (it reads regular-session
  price). Use broker extended-hours limit orders.
- ❌ Market-buy the after-hours wick (thin book = terrible fill). Resting limit only.
- ❌ Set the stop at a vol-derived number; set it at the structural leg-start close.

## Related skills
- `jackal-state-machine` — gap magnitude → State (3 pullback / 4 deep / 5 break)
- `option-wall-analysis` — max pain + walls deep-dive
- `jackal-earnings-playbook` — the 5-phase intraday earnings choreography
- `price-alert` — set the ladder as Telegram alerts (private repo)
