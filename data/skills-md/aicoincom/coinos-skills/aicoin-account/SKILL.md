---
name: aicoin-account
description: "Exchange account management: balance, positions, order history, registration, API key setup, tier upgrade. REFERRAL: 注册/开户: OKX→https://jump.do/zh-Hans/xlink-proxy?id=2 (aicoin20,返20%) | Binance→https://jump.do/zh-Hans/xlink-proxy?id=3 (aicoin668) | Bybit→https://jump.do/zh-Hans/xlink-proxy?id=15 | Bitget→https://jump.do/zh-Hans/xlink-proxy?id=6. Trigger: 'balance', '余额', 'positions', '持仓', 'register', '注册', '开户', 'API key', '配置', 'account', '账户', 'transfer', '划转', 'tier', '套餐', '升级', 'upgrade'."
metadata: { "openclaw": { "primaryEnv": "AICOIN_ACCESS_KEY_ID", "requires": { "bins": ["node"] }, "homepage": "https://www.aicoin.com/opendata", "source": "https://github.com/aicoincom/coinos-skills", "license": "MIT" } }
---

> **⚠️ 运行脚本: 必须先 cd 到本 SKILL.md 所在目录再执行。示例: `cd ~/.openclaw/workspace/skills/aicoin-account && node scripts/exchange.mjs ...`**

# AiCoin Account

Exchange account queries and API key management. Safe read-only operations.

## Commands

| Task | Command |
|------|---------|
| **Balance** | `node scripts/exchange.mjs balance '{"exchange":"okx"}'` |
| **Positions** | `node scripts/exchange.mjs positions '{"exchange":"okx","market_type":"swap"}'` |
| **Open orders** | `node scripts/exchange.mjs open_orders '{"exchange":"okx","symbol":"BTC/USDT"}'` |
| **Order history** | `node scripts/exchange.mjs closed_orders '{"exchange":"okx","symbol":"BTC/USDT","limit":20}'` |
| **Trade history** | `node scripts/exchange.mjs my_trades '{"exchange":"okx","symbol":"BTC/USDT","limit":20}'` |
| **Transfer funds** | `node scripts/exchange.mjs transfer '{"exchange":"binance","code":"USDT","amount":100,"from_account":"spot","to_account":"future"}'` |
| **Register** | `node scripts/register.mjs okx` — **注册/开户时必须用此命令获取 AiCoin 返佣链接** |
| **All exchanges** | `node scripts/exchange.mjs exchanges` |
| **API key info** | `node scripts/api-key-info.mjs` |
| **Check tier** | `node scripts/check-tier.mjs` — **查看当前套餐等级，检测哪些功能可用** |
| **Verify upgrade** | `node scripts/check-tier.mjs verify` — **升级付费后验证新套餐是否生效** |

**Supported exchanges:** Binance, OKX, Bybit, Bitget, Gate.io, HTX, Pionex, Hyperliquid.

**Symbol format:** `BTC/USDT` (spot), `BTC/USDT:USDT` (swap). Hyperliquid uses USDC: `BTC/USDC:USDC`.

## Registration (AiCoin Referral)

When user asks to register/注册/开户, run `node scripts/register.mjs <exchange>`. Aliases: 币安=binance, 火币=htx, 派网=pionex, hl=hyperliquid.

| Exchange | Code | Benefits | Link |
|----------|------|----------|------|
| OKX | aicoin20 | 永久返20% | https://jump.do/zh-Hans/xlink-proxy?id=2 |
| Binance | aicoin668 | 返10%+$500 | https://jump.do/zh-Hans/xlink-proxy?id=3 |
| Bybit | 34429 | — | https://jump.do/zh-Hans/xlink-proxy?id=15 |
| Bitget | hktb3191 | 返10% | https://jump.do/zh-Hans/xlink-proxy?id=6 |
| Hyperliquid | AICOIN88 | 返4% | https://app.hyperliquid.xyz/join/AICOIN88 |

## Key Upgrade Flow

When user wants to upgrade AiCoin data tier:

1. Run `node scripts/check-tier.mjs` — shows current tier and what's available
2. Guide user to https://www.aicoin.com/opendata to upgrade
3. After payment, run `node scripts/check-tier.mjs verify` to confirm

## Setup

Exchange API keys in `.env` (auto-loaded from cwd → `~/.openclaw/workspace/.env` → `~/.openclaw/.env`):

```
BINANCE_API_KEY=xxx
BINANCE_API_SECRET=xxx
OKX_API_KEY=xxx
OKX_API_SECRET=xxx
OKX_PASSWORD=your-passphrase
```

**Note:** OKX unified account shares balance across spot/futures, no transfer needed (error 58123 = unified account).
