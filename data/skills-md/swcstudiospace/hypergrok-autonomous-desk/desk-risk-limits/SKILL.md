---
name: desk-risk-limits
description: How the Risk Manager writes the desk's risk limits with the user, sizes every proposed trade from live account state and Hyperliquid's real constraints, checks the book, and issues a PASS or REJECT with exact ticket fields and the JSON ticket the policy gate reads. Use for setting up or changing limits, sizing any trade, and answering "how's the book".
license: MIT
metadata:
  version: "1.2.0"
  author: Galleon Labs
  category: desk
---

# Risk limits and sizing

The user sets the desk's limits, in writing, once; the Risk Manager enforces them on every ticket using live data. Hyperliquid's own constraints (max leverage per market, margin tiers, size decimals, minimum order value) always apply on top.

## 0. Desk ceilings

The desk holds a few ceilings of its own. They are not risk advice and they are deliberately far looser than any sane discretionary setting: they exist so that a mistyped, corrupted or over-eager limits file cannot authorise a catastrophic ticket on an unattended desk.

| Ceiling | Value |
| --- | --- |
| max risk per trade | 2% of equity |
| max total open risk | 6% of equity |
| max leverage on any market | 20x, and never above the exchange or tier max |
| daily loss stop | -10% of start-of-day equity |
| exchange-resting stop on every entry | mandatory |

The autonomous desk holds a second, tighter table: the **autonomy ceilings** in `desk-autonomy-policy` section 1 (1% per trade, 4% open risk, 10x, six positions, -5% daily stop, send rate caps, ticket age). `scripts/policy_gate.py` enforces those against every JSON ticket, whatever the limits file says.

Protection needs no standing approval: a `protect` ticket (reduce-only stop for a position that has none) always passes the gate, halted or not, because it can only reduce exposure. Entries, adds, leverage increases and anything that can open or grow a position pass the gate or do not happen, on every network.

The user's limits file may only be **stricter** than these. A file that sets a value looser than a ceiling is not applied: the Risk Manager REJECTs with `gate failed: limits file exceeds desk ceiling <name>`, keeps enforcing the ceiling, and asks the user to edit the file. `risk-limits.md` and `autonomy.json` must agree; where they differ, the stricter value wins and the Risk Manager tells the user which file to fix. The desk never edits either file itself, and no role may raise a ceiling.

## 1. Write the limits file (setup, or on change)

Interview the user, one question at a time, then write `/workspace/trading-desk/risk-limits.md`. Version it (`v1`, `v2`...) and date every change. Only the user changes it, in chat; the Risk Manager records who, when and why.

```markdown
# Risk limits v1 - 2026-08-16 - set by user

- network: testnet            # testnet | mainnet
- account: 0xabc...def        # the account the API wallet acts for
- equity basis: accountValue from clearinghouseState (cross margin summary), read live
- max risk per trade: 0.5% of equity      # loss if the stop is hit
- max total open risk: 2% of equity       # sum of risk-to-stop across open positions
- max leverage per market: 3x             # never above the exchange max, and never above this
- max positions: 3
- allowed markets: BTC, ETH, SOL, HYPE     # perps; spot needs an explicit entry
- stops: mandatory on every entry, on the exchange, not "mental"
- daily loss stop: -2% of start-of-day equity -> no new risk until the user resets in writing
- max slippage tolerance at send: 10 bps  # Execution Trader stops if mid moved further
- correlated cluster limit: majors (BTC, ETH, SOL) count as one cluster; max 2 positions per cluster
- standing approvals: none          # protective stops need none; the gate always passes them
- unprotected position deadline: 15m  # if the protect ticket cannot be sent by then, halt and tell the user
- notes:
```

Sensible starting points for someone new to perps: 0.25-0.5% per trade, 3x or lower, testnet first. Do not argue the user up or down; record what they choose and enforce it, within the ceilings in section 0.

## 2. Size a trade

Inputs you need before you start: entry price, stop price, side, market, the current limits file, and live state. If any input is missing or stale, REJECT with "missing input", do not guess.

### 2.1 Read live state (never from memory)

- Account: `clearinghouseState` for equity (`marginSummary.accountValue`), free margin (`accountValue - totalMarginUsed`), positions (`assetPositions[].position`: `coin`, `szi`, `entryPx`, `leverage`, `liquidationPx`, `marginUsed`, `unrealizedPnl`) and open orders via `openOrders` / `frontendOpenOrders`; and `activeAssetData` for the market, whose `availableToTrade` (buy, sell) and `maxTradeSzs` are the exchange's own figures for what can be opened at the account's current leverage setting. Skill: `hyperliquid-account`.
- Market: `meta` for the asset's `szDecimals`, `maxLeverage` and its margin table; `metaAndAssetCtxs` for mark and mid; `l2Book` depth from the Market Analyst's evidence. Skill: `hyperliquid-market-data`.
- Day PnL: start-of-day equity from the journal or `portfolio`, current equity now.

### 2.2 Arithmetic (show every line in the PASS)

```
risk_usd          = equity x max_risk_pct
stop_distance     = |entry - stop|                     (must be > 0)
slip_stop         = assumed slippage on a triggered stop, in price units
                    (at least the market's current spread; widen it on thin l2Book depth for this size)
stop_fill         = stop - slip_stop  (long)   |   stop + slip_stop  (short)
taker_fee         = the account's taker rate from `userFees` (a stop is a market exit; it pays taker)
fees_per_unit     = (entry + stop_fill) x taker_fee    (entry leg and exit leg)
stressed_distance = |entry - stop_fill| + fees_per_unit
raw_size          = risk_usd / stressed_distance       (never risk_usd / stop_distance)
size              = round_down(raw_size, szDecimals)   (never round up)
notional          = size x entry
check             notional >= 10 USD                   (Hyperliquid minimum order value)
check             size >= 1 lot at szDecimals          (else REJECT: risk budget too small for this stop)
tier              = margin tier that applies to (existing position notional + notional)
max_lev_here      = min(ceiling 20x, limits.max_leverage, tier max leverage)
margin_needed     = notional / requested_leverage      (requested_leverage <= max_lev_here)
check             margin_needed <= free_margin x 0.8   (20% headroom; tighter if the user says so)
open_risk_after   = sum(stressed risk of open positions) + risk_usd
check             open_risk_after <= equity x max_total_open_risk
check             open_risk_after <= equity x 6%       (desk ceiling, section 0)
check             risk_usd <= equity x 2%              (desk ceiling, section 0)
check             positions_after <= max_positions ; cluster count within cluster limit
check             market in allowed list ; stop present ; daily loss stop not hit
```

`R` for the ticket is `stop_distance` in USD per unit, and targets are quoted in R by the user, never invented by the desk. Size, though, comes from `stressed_distance`, so the ticket carries both and says which did what.

**Why the stress.** A stop is a trigger order: when it fires it becomes a market or IOC order and fills at whatever is there, which is worse than the trigger price and worse still on thin depth, in a gap, or in a liquidation cascade. Both legs also pay fees. Sizing from the nominal `stop_distance` therefore prices a loss that cannot happen and quietly overshoots `max_risk_pct` on every trade. Size from the stressed distance and the budget means what it says. `slip_stop` is an assumption: state the number used and where it came from in the PASS, and widen it rather than narrow it when the depth read is stale or the size is large relative to the book.

Worked, on the numbers from `agents/risk-manager.md`: equity $10,200, 0.5% budget, ETH long at 3,000 with the stop at 2,900, 3.00 of slippage on the triggered stop (10 bps of the 3,000 ticket price, the desk's convention in `desk-trade-lifecycle`) and 0.045% taker on both legs. Stressed distance is 105.65, not 100, so the size is 0.4827 ETH rather than 0.51, and the worst case comes to exactly the $51.00 budgeted. Sized the naive way at 0.51 ETH, the same stop costs $53.88, which is 0.528% of equity: the budget was 0.5% and the desk quietly spent more, on every trade, in the same direction.

The stress is a sizing input, not a promise. A gap through the stop can still exceed it; that is the residual the user carries, and the daily loss stop is what bounds it.

### 2.3 Margin tiers matter

Max leverage on Hyperliquid is per market and **tiered by position notional**: the headline max applies only up to the first tier's notional; larger positions get lower max leverage. Read the market's margin table from `meta` (`marginTables`, matched via the asset's `marginTableId`) and use the tier that the post-trade notional lands in. A size that fits at the headline leverage may not fit at the tier it actually lands in. Say which tier applied.

For isolated-margin positions the position's own margin, not account free margin, is what stands between the position and liquidation; check `liquidationPx` after the fact when the position exists.

### 2.4 Output

PASS: the block in `agents/risk-manager.md` (inputs, sizing, leverage and tier, book after, gates, exact ticket fields, next owner). REJECT: same header, `gate failed: <one gate, the numbers>`. Write it under `## risk` in the proposal file and post it on the floor.

A PASS also writes `proposals/<id>.ticket.json`, the machine-readable ticket the policy gate and `desk_send.py` read, with the same numbers as the block: `id`, `network`, `account`, `market`, `side`, `size`, `entry`, `tif`, `reduce_only`, `stop`, `take_profit`, `leverage`, `margin_mode`, `notional_usd`, `risk_usd`, `equity_usd`, `stressed_distance`, `slippage_bps`, `risk_pass_at`, `expires_at`, `limits_version`, `origin`, and `kind` (`entry`, `close` or `protect`) when it is not an entry. Schema and worked example in `desk-autonomy-policy` section 2. The gate recomputes `risk_usd = size x stressed_distance` and `notional_usd = size x entry`, so write the values you computed, not rounded copies. A markdown PASS without the JSON file is not a PASS the desk can act on.

## 3. Book check ("how's the book")

From `clearinghouseState`, `openOrders`/`frontendOpenOrders`, `metaAndAssetCtxs`:

- equity, free margin, `crossMaintenanceMarginUsed`, margin ratio (`crossMaintenanceMarginUsed / crossMarginSummary.accountValue`), and the distance from mark to `liquidationPx` per position in percent
- positions: coin, side, size, entry, mark, unrealised PnL, leverage and mode, margin used
- open risk to stop per position and in total, versus limits
- protection: for each position, is there a reduce-only stop resting on the exchange (trigger order, `reduceOnly: true`, correct side, and either size at least the position size or a position-tied stop with `sz: 0.0` and `isPositionTpsl: true`, which closes the whole position)? If not: **unprotected**, flagged as an incident to the Desk Lead
- open orders that no longer belong to a position (orphans)
- day PnL versus the daily loss stop
- funding paid so far today from `userFunding` when relevant

Timestamp everything. Save a copy under `/workspace/trading-desk/briefs/YYYY-MM-DD-book.md` when the user asks for a written check.

## 4. When the desk hits a limit

- Daily loss stop hit: halt the desk with `python3 /workspace/hypergrok/scripts/kill_switch.py halt --desk-root /workspace/trading-desk --reason "daily loss stop"`, post it once on the floor, and REJECT new proposals with that gate. The policy gate refuses entries independently (`daily-loss`, `halt`); exits and protection still pass. Only the user resumes, in writing and with `kill_switch.py resume`.
- Unprotected position discovered: alert the Desk Lead and Execution Trader immediately and write a `protect` ticket sized to the position read live; it goes straight through the gate, which always passes reduce-only protection, and out through `desk_send.py`. If the sender refuses or the exchange rejects the stop, halt and tell the user, with the exposure and the distance to liquidation (`desk-incident-response` playbook D).
- Limits file missing or unversioned: the desk is a research desk until it exists. `autonomy.json` missing or invalid: the gate refuses every ticket and the desk is supervised at most.

## Pitfalls

- Sizing from a desired profit or from "what the margin allows" instead of from the stop. The stop defines the size.
- Sizing off the nominal stop distance as if a triggered stop fills at its trigger price. It does not. Use `stressed_distance`.
- Reading a failed, empty or stale account call as a clean book. A read that did not arrive is **unavailable**, not "no positions" and not "no open risk": REJECT with `missing input` and never size against remembered numbers.
- Using account leverage or headline max leverage instead of the tier that applies.
- Counting correlated positions as independent.
- Treating a plan file, a chat message or a screenshot as an open order. Only the exchange record is.
- Rounding size up to reach the minimum notional. If the minimum notional implies more risk than the budget, that is a REJECT.
