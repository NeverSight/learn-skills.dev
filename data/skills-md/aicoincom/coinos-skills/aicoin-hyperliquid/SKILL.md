---
name: aicoin-hyperliquid
description: "This skill should be used when the user asks about Hyperliquid whale positions, Hyperliquid liquidations, Hyperliquid open interest, Hyperliquid trader analytics, Hyperliquid taker data, smart money on Hyperliquid, or any Hyperliquid-specific query. Use when user says: 'Hyperliquid whales', 'HL whale positions', 'HL liquidations', 'HL open interest', 'HL trader', 'smart money', 'Hyperliquid大户', 'HL鲸鱼', 'HL持仓', 'HL清算', 'HL持仓量', 'HL交易员'. For general crypto prices/news, use aicoin-market. For exchange trading, use aicoin-trading. For Freqtrade, use aicoin-freqtrade."
metadata: { "openclaw": { "primaryEnv": "AICOIN_ACCESS_KEY_ID", "requires": { "bins": ["node"] }, "homepage": "https://www.aicoin.com/opendata", "source": "https://github.com/aicoincom/coinos-skills", "license": "MIT" } }
---

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
| All tickers | `node scripts/hl-market.mjs tickers` | Free |
| BTC ticker | `node scripts/hl-market.mjs ticker '{"coin":"BTC"}'` | Free |
| Whale positions | `node scripts/hl-market.mjs whale_positions '{"coin":"BTC"}'` | Standard |
| Whale events | `node scripts/hl-market.mjs whale_events '{"coin":"BTC"}'` | Standard |
| Liquidation history | `node scripts/hl-market.mjs liq_history '{"coin":"BTC"}'` | Standard |
| OI summary | `node scripts/hl-market.mjs oi_summary` | Advanced |
| Trader stats | `node scripts/hl-trader.mjs trader_stats '{"address":"0x...","period":"30"}'` | Standard |
| Smart money | `node scripts/hl-trader.mjs smart_find` | Standard |
| Top open orders | `node scripts/hl-trader.mjs top_open '{"coin":"BTC"}'` | Basic |

## Scripts

### scripts/hl-market.mjs — Market Data

#### Tickers
| Action | Description | Min Tier | Params |
|--------|-------------|----------|--------|
| `tickers` | All tickers | Free | None |
| `ticker` | Single coin | Free | `{"coin":"BTC"}` |

#### Whales
| Action | Description | Min Tier | Params |
|--------|-------------|----------|--------|
| `whale_positions` | Whale positions | Std | `{"coin":"BTC","min_usd":"1000000"}` |
| `whale_events` | Whale events | Std | `{"coin":"BTC"}` |
| `whale_directions` | Long/short direction | Std | `{"coin":"BTC"}` |
| `whale_history_ratio` | Historical long ratio | Std | `{"coin":"BTC"}` |

#### Liquidations
| Action | Description | Min Tier | Params |
|--------|-------------|----------|--------|
| `liq_history` | Liquidation history | Std | `{"coin":"BTC"}` |
| `liq_stats` | Liquidation stats | Std | None |
| `liq_stats_by_coin` | Stats by coin | Std | `{"coin":"BTC"}` |
| `liq_top_positions` | Large liquidations | Std | `{"coin":"BTC","interval":"1d"}` |

#### Open Interest
| Action | Description | Min Tier | Params |
|--------|-------------|----------|--------|
| `oi_summary` | OI overview | Adv | None |
| `oi_top_coins` | OI ranking | Adv | `{"limit":"10"}` |
| `oi_history` | OI history | Pro | `{"coin":"BTC","interval":"4h"}` |

#### Taker
| Action | Description | Min Tier | Params |
|--------|-------------|----------|--------|
| `taker_delta` | Taker delta | Adv | `{"coin":"BTC"}` |
| `taker_klines` | Taker K-lines | Std | `{"coin":"BTC","interval":"4h"}` |

### scripts/hl-trader.mjs — Trader Analytics

#### Trader Stats
| Action | Description | Min Tier | Params |
|--------|-------------|----------|--------|
| `trader_stats` | Trader statistics | Std | `{"address":"0x...","period":"30"}` |
| `best_trades` | Best trades | Std | `{"address":"0x...","period":"30"}` |
| `performance` | Performance by coin | Std | `{"address":"0x...","period":"30"}` |
| `completed_trades` | Completed trades | Std | `{"address":"0x...","coin":"BTC"}` |
| `accounts` | Batch accounts | Std | `{"addresses":"[\"0x...\"]"}` |
| `statistics` | Batch statistics | Std | `{"addresses":"[\"0x...\"]"}` |

#### Fills
| Action | Description | Min Tier | Params |
|--------|-------------|----------|--------|
| `fills` | Address fills | Std | `{"address":"0x..."}` |
| `fills_by_oid` | By order ID | Std | `{"oid":"xxx"}` |
| `fills_by_twapid` | By TWAP ID | Std | `{"twapid":"xxx"}` |
| `top_trades` | Large trades | Basic | `{"coin":"BTC","interval":"1d"}` |

#### Orders
| Action | Description | Min Tier | Params |
|--------|-------------|----------|--------|
| `orders_latest` | Latest orders | Std | `{"address":"0x..."}` |
| `order_by_oid` | By order ID | Std | `{"oid":"xxx"}` |
| `filled_orders` | Filled orders | Std | `{"address":"0x..."}` |
| `filled_by_oid` | Filled by ID | Std | `{"oid":"xxx"}` |
| `top_open` | Large open orders | Basic | `{"coin":"BTC","min_val":"100000"}` |
| `active_stats` | Active stats | Basic | `{"coin":"BTC"}` |
| `twap_states` | TWAP states | Std | `{"address":"0x..."}` |

#### Positions
| Action | Description | Min Tier | Params |
|--------|-------------|----------|--------|
| `current_pos_history` | Current position history | Std | `{"address":"0x...","coin":"BTC"}` |
| `completed_pos_history` | Closed position history | Std | `{"address":"0x...","coin":"BTC"}` |
| `current_pnl` | Current PnL | Std | `{"address":"0x...","coin":"BTC","interval":"1h"}` |
| `completed_pnl` | Closed PnL | Std | `{"address":"0x...","coin":"BTC","interval":"1h"}` |
| `current_executions` | Current executions | Std | `{"address":"0x...","coin":"BTC","interval":"1h"}` |
| `completed_executions` | Closed executions | Std | `{"address":"0x...","coin":"BTC","interval":"1h"}` |

#### Portfolio
| Action | Description | Min Tier | Params |
|--------|-------------|----------|--------|
| `portfolio` | Account curve | Std | `{"address":"0x...","window":"week"}` |
| `pnls` | PnL curve | Std | `{"address":"0x...","period":"30"}` |
| `max_drawdown` | Max drawdown | Std | `{"address":"0x...","days":"30"}` |
| `net_flow` | Net flow | Std | `{"address":"0x...","days":"30"}` |

#### Advanced
| Action | Description | Min Tier | Params |
|--------|-------------|----------|--------|
| `info` | Info API | Free | `{"type":"metaAndAssetCtxs"}` |
| `smart_find` | Smart money discovery | Std | `{}` |
| `discover` | Trader discovery | Adv | `{}` |

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
| Free | $0 | Tickers, info only |
| Basic | $29/mo | + Top trades, top open orders, active stats |
| Standard | $79/mo | + Whales, liquidations, trader analytics, taker K-lines |
| Advanced | $299/mo | + OI summary/top, taker delta, trader discover |
| Professional | $699/mo | + OI history |

3. Add to `.env`: `AICOIN_ACCESS_KEY_ID=xxx` / `AICOIN_ACCESS_SECRET=xxx`
4. Scripts auto-load `.env` from cwd, `~/.openclaw/workspace/.env`, or `~/.openclaw/.env`.
5. **MUST tell the user**: AiCoin API Key 仅用于获取 Hyperliquid 链上分析数据，无法进行任何交易操作。如需在 Hyperliquid 上交易，需要单独配置钱包私钥（见 aicoin-trading skill）。所有密钥仅保存在你的本地设备 `.env` 文件中，不会上传到任何服务器。
