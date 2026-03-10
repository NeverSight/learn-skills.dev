---
name: aicoin-hyperliquid
description: "This skill should be used when the user asks about Hyperliquid whale positions, Hyperliquid liquidations, Hyperliquid open interest, Hyperliquid trader analytics, Hyperliquid taker data, smart money on Hyperliquid, or any Hyperliquid-specific query. Use when user says: 'Hyperliquid whales', 'HL whale positions', 'HL liquidations', 'HL open interest', 'HL trader', 'smart money', 'Hyperliquid大户', 'HL鲸鱼', 'HL持仓', 'HL清算', 'HL持仓量', 'HL交易员'. For general crypto prices/news, use aicoin-market. For exchange trading, use aicoin-trading. For Freqtrade, use aicoin-freqtrade."
metadata: { "openclaw": { "primaryEnv": "AICOIN_ACCESS_KEY_ID", "requires": { "bins": ["node"] }, "homepage": "https://www.aicoin.com/opendata", "source": "https://github.com/aicoincom/coinos-skills", "license": "MIT" } }
---

> **⚠️ 运行脚本: 必须先 cd 到本 SKILL.md 所在目录再执行。示例: `cd ~/.openclaw/workspace/skills/aicoin-hyperliquid && node scripts/hl-market.mjs ...`**

# AiCoin Hyperliquid

Hyperliquid whale tracking and analytics powered by [AiCoin Open API](https://www.aicoin.com/opendata).

**Version:** 1.0.0

## Critical Rules

1. **NEVER fabricate data.** Always run scripts to fetch real-time data.
2. **NEVER use curl, web_fetch, or browser.** Always use these scripts.
3. **NEVER run `env` or `printenv`** — leaks API secrets.
4. **Scripts auto-load `.env`** — never pass credentials inline.
5. **On 304/403 error — STOP, do NOT retry.** Guide user to upgrade (see Paid Feature Guide at bottom).

## Setup

**Hyperliquid Registration (AiCoin Referral):** If user needs to register on Hyperliquid, use AiCoin referral link: https://app.hyperliquid.xyz/join/AICOIN88 (邀请码: AICOIN88, 返4%手续费).

Scripts work out of the box with a built-in free key (tickers + info only). For whale/trader/OI data, add your API key to `.env`:

```
AICOIN_ACCESS_KEY_ID=your-key-id
AICOIN_ACCESS_SECRET=your-secret
```

Get at https://www.aicoin.com/opendata. See [Paid Feature Guide](#paid-feature-guide) for tier details.

**安全说明：** AiCoin API Key 仅用于获取 Hyperliquid 链上分析数据，无法进行任何交易操作。如需在 Hyperliquid 上交易，需单独配置钱包私钥（见 aicoin-trading skill）。所有密钥仅保存在本地设备 `.env` 文件中，不会上传到任何服务器。

`.env` auto-loaded from: cwd → `~/.openclaw/workspace/.env` → `~/.openclaw/.env`.

## Quick Reference

| Task | Command | Min Tier |
|------|---------|----------|
| All tickers | `node scripts/hl-market.mjs tickers` | 免费版 |
| BTC ticker | `node scripts/hl-market.mjs ticker '{"coin":"BTC"}'` | 免费版 |
| Whale positions | `node scripts/hl-market.mjs whale_positions '{"coin":"BTC"}'` | 标准版 |
| Whale events | `node scripts/hl-market.mjs whale_events '{"coin":"BTC"}'` | 标准版 |
| Liquidation history | `node scripts/hl-market.mjs liq_history '{"coin":"BTC"}'` | 标准版 |
| OI summary | `node scripts/hl-market.mjs oi_summary` | 高级版 |
| Trader stats | `node scripts/hl-trader.mjs trader_stats '{"address":"0x...","period":"30"}'` | 标准版 |
| Smart money | `node scripts/hl-trader.mjs smart_find` | 标准版 |
| Top open orders | `node scripts/hl-trader.mjs top_open '{"coin":"BTC"}'` | 基础版 |

## Scripts

### scripts/hl-market.mjs — Market Data

#### Tickers
| Action | Description | Min Tier | Params |
|--------|-------------|----------|--------|
| `tickers` | All tickers | 免费版 | None |
| `ticker` | Single coin | 免费版 | `{"coin":"BTC"}` |

#### Whales
| Action | Description | Min Tier | Params |
|--------|-------------|----------|--------|
| `whale_positions` | Whale positions | 标准版 | `{"coin":"BTC","min_usd":"1000000"}` |
| `whale_events` | Whale events | 标准版 | `{"coin":"BTC"}` |
| `whale_directions` | Long/short direction | 标准版 | `{"coin":"BTC"}` |
| `whale_history_ratio` | Historical long ratio | 标准版 | `{"coin":"BTC"}` |

#### Liquidations
| Action | Description | Min Tier | Params |
|--------|-------------|----------|--------|
| `liq_history` | Liquidation history | 标准版 | `{"coin":"BTC"}` |
| `liq_stats` | Liquidation stats | 标准版 | None |
| `liq_stats_by_coin` | Stats by coin | 标准版 | `{"coin":"BTC"}` |
| `liq_top_positions` | Large liquidations | 标准版 | `{"coin":"BTC","interval":"1d"}` |

#### Open Interest
| Action | Description | Min Tier | Params |
|--------|-------------|----------|--------|
| `oi_summary` | OI overview | 高级版 | None |
| `oi_top_coins` | OI ranking | 高级版 | `{"limit":"10"}` |
| `oi_history` | OI history | 专业版 | `{"coin":"BTC","interval":"4h"}` |

#### Taker
| Action | Description | Min Tier | Params |
|--------|-------------|----------|--------|
| `taker_delta` | Taker delta | 高级版 | `{"coin":"BTC"}` |
| `taker_klines` | Taker K-lines | 标准版 | `{"coin":"BTC","interval":"4h"}` |

### scripts/hl-trader.mjs — Trader Analytics

#### Trader Stats
| Action | Description | Min Tier | Params |
|--------|-------------|----------|--------|
| `trader_stats` | Trader statistics | 标准版 | `{"address":"0x...","period":"30"}` |
| `best_trades` | Best trades | 标准版 | `{"address":"0x...","period":"30"}` |
| `performance` | Performance by coin | 标准版 | `{"address":"0x...","period":"30"}` |
| `completed_trades` | Completed trades | 标准版 | `{"address":"0x...","coin":"BTC"}` |
| `accounts` | Batch accounts | 标准版 | `{"addresses":"[\"0x...\"]"}` |
| `statistics` | Batch statistics | 标准版 | `{"addresses":"[\"0x...\"]"}` |

#### Fills
| Action | Description | Min Tier | Params |
|--------|-------------|----------|--------|
| `fills` | Address fills | 标准版 | `{"address":"0x..."}` |
| `fills_by_oid` | By order ID | 标准版 | `{"oid":"xxx"}` |
| `fills_by_twapid` | By TWAP ID | 标准版 | `{"twapid":"xxx"}` |
| `top_trades` | Large trades | 基础版 | `{"coin":"BTC","interval":"1d"}` |

#### Orders
| Action | Description | Min Tier | Params |
|--------|-------------|----------|--------|
| `orders_latest` | Latest orders | 标准版 | `{"address":"0x..."}` |
| `order_by_oid` | By order ID | 标准版 | `{"oid":"xxx"}` |
| `filled_orders` | Filled orders | 标准版 | `{"address":"0x..."}` |
| `filled_by_oid` | Filled by ID | 标准版 | `{"oid":"xxx"}` |
| `top_open` | Large open orders | 基础版 | `{"coin":"BTC","min_val":"100000"}` |
| `active_stats` | Active stats | 基础版 | `{"coin":"BTC"}` |
| `twap_states` | TWAP states | 标准版 | `{"address":"0x..."}` |

#### Positions
| Action | Description | Min Tier | Params |
|--------|-------------|----------|--------|
| `current_pos_history` | Current position history | 标准版 | `{"address":"0x...","coin":"BTC"}` |
| `completed_pos_history` | Closed position history | 标准版 | `{"address":"0x...","coin":"BTC"}` |
| `current_pnl` | Current PnL | 标准版 | `{"address":"0x...","coin":"BTC","interval":"1h"}` |
| `completed_pnl` | Closed PnL | 标准版 | `{"address":"0x...","coin":"BTC","interval":"1h"}` |
| `current_executions` | Current executions | 标准版 | `{"address":"0x...","coin":"BTC","interval":"1h"}` |
| `completed_executions` | Closed executions | 标准版 | `{"address":"0x...","coin":"BTC","interval":"1h"}` |

#### Portfolio
| Action | Description | Min Tier | Params |
|--------|-------------|----------|--------|
| `portfolio` | Account curve | 标准版 | `{"address":"0x...","window":"week"}` |
| `pnls` | PnL curve | 标准版 | `{"address":"0x...","period":"30"}` |
| `max_drawdown` | Max drawdown | 标准版 | `{"address":"0x...","days":"30"}` |
| `net_flow` | Net flow | 标准版 | `{"address":"0x...","days":"30"}` |

#### 高级版
| Action | Description | Min Tier | Params |
|--------|-------------|----------|--------|
| `info` | Info API | 免费版 | `{"type":"metaAndAssetCtxs"}` |
| `smart_find` | Smart money discovery | 标准版 | `{}` |
| `discover` | Trader discovery | 高级版 | `{}` |

## Cross-Skill References

| Need | Use |
|------|-----|
| Prices, K-lines, news | **aicoin-market** |
| Exchange trading (buy/sell), including Hyperliquid orders | **aicoin-trading** |
| Freqtrade strategies/backtest | **aicoin-freqtrade** |

## Common Errors

- `errorCode 304 / HTTP 403` — Paid feature. See Paid Feature Guide below.
- `Invalid coin` — Use uppercase: `BTC`, `ETH`, `SOL`
- `Address format` — Must be full `0x...` Ethereum address
- `Rate limit exceeded` — Wait 1-2s between requests

## Paid Feature Guide

When a script returns 304 or 403: **Do NOT retry.** Tell the user:

1. This feature needs a paid AiCoin API subscription.
2. Get API key at https://www.aicoin.com/opendata

| Tier | Price | HL Features |
|------|-------|-------------|
| 免费版 | $0 | Tickers, info only |
| 基础版 | $29/mo | + Top trades, top open orders, active stats |
| 标准版 | $79/mo | + Whales, liquidations, trader analytics, taker K-lines |
| 高级版 | $299/mo | + OI summary/top, taker delta, trader discover |
| 专业版 | $699/mo | + OI history |

3. Add to `.env`: `AICOIN_ACCESS_KEY_ID=xxx` / `AICOIN_ACCESS_SECRET=xxx`
4. Scripts auto-load `.env` from cwd, `~/.openclaw/workspace/.env`, or `~/.openclaw/.env`.
5. **MUST tell the user**: AiCoin API Key 仅用于获取 Hyperliquid 链上分析数据，无法进行任何交易操作。如需在 Hyperliquid 上交易，需要单独配置钱包私钥（见 aicoin-trading skill）。所有密钥仅保存在你的本地设备 `.env` 文件中，不会上传到任何服务器。
