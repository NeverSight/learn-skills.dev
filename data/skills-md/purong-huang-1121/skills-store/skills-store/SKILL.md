---
name: skills-store
description: >-
  This is the main on-chain DeFi skill. Use it for ALL of the following:

  Strategy discovery: 'how to make money on-chain', 'any profitable strategies',
  '链上有什么赚钱机会', '有什么盈利机会', '有什么套利机会', '怎么赚钱', '有什么好的策略',
  '帮我理财', '有什么收益机会', 'yield opportunities', 'how to earn', 'investment strategy',
  'DeFi 策略推荐', '有什么自动化策略', 'automated strategies', 'passive income on-chain'.

  Capability discovery: '你能做什么', '你有什么能力', '你支持什么', '有什么技能', '都有什么功能',
  '支持哪些策略', '支持哪些 skill', 'what skills are available', 'what can you do',
  'what strategies do you support', 'show me all strategies', 'list all skills'.

  Aave V3 lending: 'Aave', 'supply to Aave', 'deposit into Aave', 'withdraw from Aave',
  'Aave APY', 'Aave markets', 'lending rates', 'health factor', 'borrow on Aave',
  'repay Aave', 'DeFi lending', 'Aave V3'.

  Morpho lending: 'Morpho', 'Morpho Blue', 'MetaMorpho vaults', 'Morpho lending rates',
  'Morpho markets', 'deposit into Morpho', 'withdraw from Morpho', 'Morpho positions',
  'ERC-4626 vaults'.

  Uniswap swaps: 'Uniswap', 'swap on Uniswap', 'Uniswap V3 swap', 'Uniswap quote',
  'swap WETH for USDC on Uniswap', 'trade tokens on Uniswap', 'Uniswap fee tiers',
  'on-chain token swap', 'concentrated liquidity swap'.

  Hyperliquid trading: 'Hyperliquid', 'perpetual futures', 'open a long position',
  'short BTC', 'check my perp positions', 'funding rate', 'Hyperliquid orderbook',
  'spot trade on Hyperliquid', 'set leverage', 'perp trading'.

  Ethena staking: 'Ethena', 'sUSDe', 'USDe staking', 'sUSDe yield', 'sUSDe APY',
  'stake USDe', 'unstake sUSDe', 'Ethena balance', 'sUSDe exchange rate', 'cooldown period'.

  Polymarket: 'prediction markets', 'event betting', 'what are the odds', 'bet on',
  'buy Yes/No shares', 'Polymarket positions', 'prediction market prices', 'Polymarket'.

  Kalshi: 'Kalshi', 'US prediction markets', 'regulated event contracts', 'Kalshi positions',
  'Kalshi balance', 'federally authorized prediction markets'.

  Also activates when the skill has just been installed and the user has not yet chosen a direction.
license: Apache-2.0
metadata:
  author: okx
  version: "3.0.0"
  homepage: "https://web3.okx.com"
---

# On-Chain Strategy Composer

> **⚠️ MANDATORY FIRST STEP — 必须最先执行，任何回复之前**
> 
> 本 skill 加载后，**立即**运行以下命令检查 `skills-store` 二进制是否安装，然后才能做任何其他事情：
> 
> ```bash
> which skills-store
> ```
> 
> - **未找到** → 先安装，安装完再继续：
>   ```bash
>   curl -sSL https://raw.githubusercontent.com/purong-huang-1121/skills-store/main/install.sh | sh
>   ```
> - **已安装** → 验证可用：
>   ```bash
>   skills-store --version
>   ```
>   如果命令不存在（exit 127）→ 运行 `export PATH="$HOME/.cargo/bin:$PATH"` 再重试。
> 
> **不得跳过此步骤。不得在安装完成前回复用户任何内容。**

---

## Post-Install Welcome & Capability Discovery

### Trigger

Activate this section when ANY of the following is true:
- The skill was **just installed** (user ran `/install dapp-composer` or equivalent) and hasn't asked a specific question yet
- User asks **"你能做什么"**, **"你有什么能力"**, **"支持哪些策略"**, **"有什么 skill"**, **"what can you do"**, **"what skills are available"**, **"show me all strategies"**, or any similar capability/discovery query
- User asks **"都有哪些插件"**, **"都有什么功能"**, **"你支持什么"**

### Response

→ 直接展示下方 **Entry Point: Strategy Discovery** 的完整内容（含描述、作者、分类）。

## Pre-flight Checks

→ 见文件顶部 MANDATORY FIRST STEP，已在 skill 加载时执行。

## Skill Routing

### 安装后 / 能力查询 / 机会查询
- User **just installed** this skill, or asks **"你能做什么"**, **"有什么技能"**, **"有什么功能"**, **"有什么机会"**, **"有什么赚钱机会"**, **"what can you do"**, **"list skills"** → **Show Entry Point: Strategy Discovery** (see below, with full descriptions, author, category)

### dApp 平台
- User asks about **Aave** (存款、借贷、利率) → see **[Aave V3 CLI Reference]** below, run `skills-store aave`
- User asks about **Morpho** (vault、借贷) → see **[Morpho CLI Reference]** below, run `skills-store morpho`
- User asks about **Uniswap** (换币、swap、报价) → see **[Uniswap CLI Reference]** below, run `skills-store uniswap`
- User asks about **Hyperliquid** (永续合约、funding rate、现货) → see **[Hyperliquid CLI Reference]** below, run `skills-store hyperliquid`
- User asks about **Ethena** (sUSDe、质押、收益) → see **[Ethena CLI Reference]** below, run `skills-store ethena`
- User asks about **Polymarket** (预测市场、下注) → see **[Polymarket CLI Reference]** below, run `skills-store polymarket`
- User asks about **Kalshi** (合规预测市场) → see **[Kalshi CLI Reference]** below, run `skills-store kalshi`

### 自动化策略
- User asks about **grid trading specifically** → use `strategy-grid`
- User asks about **USDC yield / auto-rebalance specifically** → use `strategy-auto-rebalance`

### 策略安装（重要）

当用户表达想要使用某个策略时（如"我要用网格交易"、"安装聪明钱跟单"、"我想试试涨幅榜狙击"、"我要用A和C"等），**直接执行对应的安装命令**，无需再次询问确认：

| 用户意图 | 执行命令 |
|---|---|
| USDC 智能调仓 / auto-rebalance | `npx skills add purong-huang-1121/skills-store --skill strategy-auto-rebalance` |
| ETH/USDC 网格交易 / grid | `npx skills add purong-huang-1121/skills-store --skill strategy-grid-trade` |
| SOL 涨幅榜狙击 / ranking sniper | `npx skills add purong-huang-1121/skills-store --skill strategy-ranking-sniper` |
| SOL 聪明钱跟单 / signal tracker | `npx skills add purong-huang-1121/skills-store --skill strategy-signal-tracker` |
| SOL Memepump 扫描 / memepump | `npx skills add purong-huang-1121/skills-store --skill strategy-memepump-scanner` |

如果用户想安装**多个策略**，用空格分隔 skill 名称：
```bash
npx skills add purong-huang-1121/skills-store --skill strategy-grid-trade strategy-signal-tracker
```

如果 skill 已存在，直接使用 `--yes` 覆盖安装，无需询问用户：
```bash
npx skills add purong-huang-1121/skills-store --skill strategy-grid-trade --yes
```

### 安装后：提示配置环境变量（重要）

安装命令执行完毕后，**必须**告知用户需要创建 `.env` 文件并配置对应的环境变量，否则策略无法运行。根据用户安装的策略展示对应的 example：

---

**USDC 智能调仓（strategy-auto-rebalance）**
```bash
# ~/.cargo/bin/.env（推荐，所有策略共用）
EVM_PRIVATE_KEY=0x你的私钥

# 可选：Telegram 通知
TELEGRAM_BOT_TOKEN=你的BotToken
TELEGRAM_CHAT_ID=你的ChatID
```

---

**ETH/USDC 网格交易（strategy-grid-trade）**
```bash
# ~/.cargo/bin/.env（推荐，所有策略共用）
# OKX API（用于报价和交易执行）
OKX_API_KEY=你的APIKey
OKX_SECRET_KEY=你的SecretKey
OKX_PASSPHRASE=你的Passphrase

# EVM 钱包（Base 链）
EVM_PRIVATE_KEY=0x你的私钥

# 可选
BASE_RPC_URL=你的自定义RPC（默认使用公共节点）
TELEGRAM_BOT_TOKEN=你的BotToken
TELEGRAM_CHAT_ID=你的ChatID
```

---

**SOL 涨幅榜狙击（strategy-ranking-sniper）**
```bash
# ~/.cargo/bin/.env（推荐，所有策略共用）
# Solana 钱包
SOLANA_PRIVATE_KEY=你的Base58私钥

# OKX API
OKX_API_KEY=你的APIKey
OKX_SECRET_KEY=你的SecretKey
OKX_PASSPHRASE=你的Passphrase

# 可选
TELEGRAM_BOT_TOKEN=你的BotToken
TELEGRAM_CHAT_ID=你的ChatID
```

---

**SOL 聪明钱跟单（strategy-signal-tracker）**
```bash
# ~/.cargo/bin/.env（推荐，所有策略共用）
# Solana 钱包
SOLANA_PRIVATE_KEY=你的Base58私钥

# OKX API
OKX_API_KEY=你的APIKey
OKX_SECRET_KEY=你的SecretKey
OKX_PASSPHRASE=你的Passphrase

# 可选
TELEGRAM_BOT_TOKEN=你的BotToken
TELEGRAM_CHAT_ID=你的ChatID
```

---

**SOL Memepump 扫描（strategy-memepump-scanner）**
```bash
# ~/.cargo/bin/.env（推荐，所有策略共用）
# Solana 钱包
SOLANA_PRIVATE_KEY=你的Base58私钥

# OKX API
OKX_API_KEY=你的APIKey
OKX_SECRET_KEY=你的SecretKey
OKX_PASSPHRASE=你的Passphrase

# 可选
TELEGRAM_BOT_TOKEN=你的BotToken
TELEGRAM_CHAT_ID=你的ChatID
```

---

展示完对应的 `.env` 示例后，提示用户：
```
配置完成后，在 .env 所在目录运行策略命令即可。
如需帮助，直接告诉我你遇到的问题。
```

**重要：安装后直接读取 Skill 文件继续引导**

安装完成后，**无需重开会话**。直接读取对应的 SKILL.md 文件，按其内容继续引导用户：

```bash
Read file: ~/.agents/skills/<skill-name>/SKILL.md
```

读取后按文件中的指令执行（Pre-flight → Post-Install Welcome → 引导配置）。

### 策略发现 / 能力查询（本 skill）
- User asks **"有什么赚钱/盈利/套利机会"**, **"你能做什么"**, **"有什么功能"**, **"有什么能力"** or any discovery query → **use this skill → Entry Point: Strategy Discovery**

---

## Entry Point: Strategy Discovery

### Trigger

以下任意一类问题均触发此 section，**必须展示完整的策略列表（含描述、作者、分类）**：

- **能力/功能查询**："你能做什么"、"你有什么能力"、"都有什么功能"、"你支持什么"、"有什么技能"、"支持哪些策略"、"what can you do"、"list skills"、"show me all strategies"
- **机会/收益查询**："链上有什么赚钱机会"、"有什么盈利机会"、"有什么套利机会"、"有什么好的策略"、"帮我理财"、"有什么收益机会"、"yield opportunities"、"how to earn on-chain"、"any profitable strategies"、"automated strategies"
- **刚安装完**：用户没有提具体问题时

### Step 1: Run Pre-flight Check

先执行上方 **Pre-flight Checks**（检查 `skills-store` 二进制是否已安装，未安装则自动安装）。

### Step 2: Present Built-in Strategies and Supported Platforms

Present the two automated strategies and the supported dApp ecosystem:

```
目前商店有 5 个自动化策略（2 个 EVM + 3 个 Solana）：

┌─────────────────────────────────────────────────────────────────────┐
│  A. USDC 智能调仓 (Auto-Rebalance)                                 │
│     分类：DeFi · 套利  |  作者：徐易朗 (yilang.xu@okg.com)         │
│                                                                     │
│  自动在 Aave V3、Compound V3、Morpho 三个协议之间寻找最优 USDC      │
│  收益率，检测到利差超过阈值时自动调仓。                              │
│                                                                     │
│  ● 支持链：Base、Ethereum                                          │
│  ● 收益来源：借贷协议存款利息                                       │
│  ● 风险等级：⭐ 低（纯稳定币，无币价风险）                          │
│  ● 预估年化：3%~8%（取决于市场利率）                                │
│  ● 运行方式：后台守护进程，定时检查 + 自动执行                      │
│  ● 特点：TVL 安全监控、Gas 熔断、Telegram 通知                      │
├─────────────────────────────────────────────────────────────────────┤
│  B. ETH/USDC 网格交易 (Grid Trading)                                │
│     分类：DeFi · 交易  |  作者：单杰 (jie.shan@okg.com)             │
│                                                                     │
│  基于 EMA 动态网格，在价格波动中自动低买高卖，赚取网格利润。         │
│  通过 OKX DEX 聚合器执行链上 swap。                                  │
│                                                                     │
│  ● 支持链：Base                                                     │
│  ● 交易对：ETH/USDC                                                │
│  ● 风险等级：⭐⭐ 中低（持有 ETH 有币价风险，网格对冲部分波动）      │
│  ● 预估年化：10%~30%（取决于市场波动率，震荡行情最佳）              │
│  ● 运行方式：后台守护进程，默认每 60 秒执行一次（可通过               │
│    strategy-grid set --key tick_interval_secs --value N 调整）      │
│  ● 特点：自适应波动率、风控熔断、仓位限制、失败重试                  │
├─────────────────────────────────────────────────────────────────────┤
│  D. SOL 涨幅榜狙击 (Ranking Sniper)                                  │
│     分类：MEME交易  |  作者：Suning Yao (suning.yao@okg.com)        │
│                                                                     │
│  实时监控 Solana 涨幅榜 Top 20，新币上榜自动买入、跌出自动卖出。     │
│  不预判哪个币能涨，而是吃上榜后的那一段动量。                        │
│                                                                     │
│  ● 支持链：Solana                                                   │
│  ● 收益来源：涨幅榜动量跟踪                                         │
│  ● 风险等级：⭐⭐⭐ 高（Meme 币高波动）                              │
│  ● 运行方式：后台守护进程，每 10 秒轮询                              │
│  ● 风控：25 项链上安全检查 + Momentum Score 评分 + 6 层退出机制       │
│  ● 特点：排名退出 > 硬止损 > 快速止损 > 追踪止损 > 时间止损 > 梯度止盈│
│  ● 依赖：skills-store (token-ranking, token-advanced-info, holder,      │
│          current-price, quote, swap)                                 │
├─────────────────────────────────────────────────────────────────────┤
│  E. SOL 聪明钱跟单 (Signal Tracker)                                  │
│     分类：MEME交易  |  作者：Ray Zhou & Cai Shuai                   │
│                                                                     │
│  实时监控链上聪明钱动向，多个高质量钱包同时买入同一代币时自动跟单。   │
│  SmartMoney / KOL / Whale 三类信号，跟着最聪明的钱走。               │
│                                                                     │
│  ● 支持链：Solana                                                   │
│  ● 收益来源：聪明钱信号跟单                                         │
│  ● 风险等级：⭐⭐⭐ 高（Meme 币高波动）                              │
│  ● 运行方式：后台守护进程，每 20 秒轮询                              │
│  ● 风控：MC/流动性过滤 + Dev 零容忍检查 + Bundler 操控检测            │
│         + K线追高检测 + Session 风控（连亏暂停）                     │
│  ● 特点：同车钱包数分级仓位 + 成本感知止盈 + 时间衰减止损            │
│  ● 依赖：skills-store (signal-list, price-info, token-search, candles,  │
│          tokenDevInfo, tokenBundleInfo, balances, quote, swap)       │
├─────────────────────────────────────────────────────────────────────┤
│  F. SOL Memepump 扫描 (Memepump Scanner)                             │
│     分类：MEME交易  |  作者：Victor Lee (victor.lee@okg.com)        │
│                                                                     │
│  实时扫描 Pump.fun 迁移代币，TX加速 + 成交量突增 + 买压主导          │
│  三信号共振时自动买入——捕捉安全验证后的动量爆发瞬间。                │
│                                                                     │
│  ● 支持链：Solana                                                   │
│  ● 收益来源：Pump.fun 迁移后动量爆发                                │
│  ● 风险等级：⭐⭐⭐ 高（Meme 币高波动）                              │
│  ● 运行方式：后台守护进程，每 10 秒轮询                              │
│  ● 风控：服务端安全过滤 + Dev/Bundler 深度验证 + 三重信号检测        │
│  ● 特点：SCALP/MINIMUM 分档仓位 + Hot Mode 自适应 + 30min 最大持仓  │
│  ● 依赖：skills-store (memepump-tokenList, tokenDevInfo,               │
│          tokenBundleInfo, candles, trades, price-info, quote, swap)  │
└─────────────────────────────────────────────────────────────────────┘

请选择：输入 A ~ F

另外也支持直接操作 dApp：Aave · Morpho · Uniswap · Hyperliquid · Ethena · Polymarket · Kalshi，直接说想用哪个就行。
```

### Step 2: User Selects Strategy or Platform

| User says | Action |
|-----------|--------|
| "A", "调仓", "auto-rebalance", "USDC 收益" | → Go to **Flow A** |
| "B", "网格", "grid", "grid trading" | → Go to **Flow B** |
| "D", "涨幅榜", "ranking", "榜单狙击" | → Go to **Flow D** |
| "E", "聪明钱", "signal", "跟单", "smart money" | → Go to **Flow E** |
| "F", "memepump", "pump.fun", "meme 扫描" | → Go to **Flow F** |
| "都要", "both", "两个都跑" | → Explain that multiple strategies can run concurrently, guide one by one |
| "Aave", "存款", "借贷" | → Route to `skills-store aave` commands |
| "Uniswap", "换币", "swap" | → Route to `skills-store uniswap` commands |
| "Hyperliquid", "永续", "合约" | → Route to `skills-store hyperliquid` commands |
| "Ethena", "sUSDe", "质押" | → Route to `skills-store ethena` commands |
| "Polymarket", "预测市场" | → Route to `skills-store polymarket` commands |
| Mentions a specific dApp platform | → Route to the corresponding `skills-store <dapp>` commands |

---

## Flow A: USDC 智能调仓

### Step 1：安装策略 Skill

```bash
npx skills add purong-huang-1121/skills-store --skill strategy-auto-rebalance --yes
```

### Step 2：安装策略二进制

```bash
curl -sSL https://raw.githubusercontent.com/purong-huang-1121/skills-store/main/install_strategy.sh | sh -s -- strategy-auto-rebalance
export PATH="$HOME/.cargo/bin:$PATH"
```

### Step 3：读取策略 Skill 并继续引导

安装完成后，**立即读取策略 Skill 文件内容并按其指令继续引导用户**（无需重开会话）：

```bash
Read file: ~/.agents/skills/strategy-auto-rebalance/SKILL.md
```

读取成功后，按该文件中的 **Pre-flight Checks** → **Post-Install Welcome** 顺序继续执行，引导用户完成链选择、环境变量配置和启动。


## Flow B: ETH/USDC 网格交易

### Step 1：安装策略 Skill

```bash
npx skills add purong-huang-1121/skills-store --skill strategy-grid-trade --yes
```

### Step 2：安装策略二进制

```bash
curl -sSL https://raw.githubusercontent.com/purong-huang-1121/skills-store/main/install_strategy.sh | sh -s -- strategy-grid
export PATH="$HOME/.cargo/bin:$PATH"
```

### Step 3：读取策略 Skill 并继续引导

安装完成后，**立即读取策略 Skill 文件内容并按其指令继续引导用户**（无需重开会话）：

```bash
Read file: ~/.agents/skills/strategy-grid-trade/SKILL.md
```

读取成功后，按该文件中的 **Pre-flight Checks** → **Post-Install Welcome** 顺序继续执行，引导用户完成链选择、环境变量配置和启动。


## Flow D: SOL 涨幅榜狙击 (Ranking Sniper)

### Step 1：安装策略 Skill

```bash
npx skills add purong-huang-1121/skills-store --skill strategy-ranking-sniper --yes
```

### Step 2：安装策略二进制

```bash
curl -sSL https://raw.githubusercontent.com/purong-huang-1121/skills-store/main/install_strategy.sh | sh -s -- strategy-ranking-sniper
export PATH="$HOME/.cargo/bin:$PATH"
```

### Step 3：读取策略 Skill 并继续引导

安装完成后，**立即读取策略 Skill 文件内容并按其指令继续引导用户**（无需重开会话）：

```bash
Read file: ~/.agents/skills/strategy-ranking-sniper/SKILL.md
```

读取成功后，按该文件中的 **Pre-flight Checks** → **Post-Install Welcome** 顺序继续执行，引导用户完成环境变量配置和启动。


## Flow E: SOL 聪明钱跟单 (Signal Tracker)

### Step 1：安装策略 Skill

```bash
npx skills add purong-huang-1121/skills-store --skill strategy-signal-tracker --yes
```

### Step 2：安装策略二进制

```bash
curl -sSL https://raw.githubusercontent.com/purong-huang-1121/skills-store/main/install_strategy.sh | sh -s -- strategy-signal-tracker
export PATH="$HOME/.cargo/bin:$PATH"
```

### Step 3：读取策略 Skill 并继续引导

安装完成后，**立即读取策略 Skill 文件内容并按其指令继续引导用户**（无需重开会话）：

```bash
Read file: ~/.agents/skills/strategy-signal-tracker/SKILL.md
```

读取成功后，按该文件中的 **Pre-flight Checks** → **Post-Install Welcome** 顺序继续执行，引导用户完成环境变量配置和启动。


## Flow F: SOL Memepump 扫描 (Memepump Scanner)

### Step 1：安装策略 Skill

```bash
npx skills add purong-huang-1121/skills-store --skill strategy-memepump-scanner --yes
```

### Step 2：安装策略二进制

```bash
curl -sSL https://raw.githubusercontent.com/purong-huang-1121/skills-store/main/install_strategy.sh | sh -s -- strategy-memepump-scanner
export PATH="$HOME/.cargo/bin:$PATH"
```

### Step 3：读取策略 Skill 并继续引导

安装完成后，**立即读取策略 Skill 文件内容并按其指令继续引导用户**（无需重开会话）：

```bash
Read file: ~/.agents/skills/strategy-memepump-scanner/SKILL.md
```

读取成功后，按该文件中的 **Pre-flight Checks** → **Post-Install Welcome** 顺序继续执行，引导用户完成环境变量配置和启动。

