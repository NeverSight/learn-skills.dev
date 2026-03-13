---
name: ibkr-readonly
description: IBKR 投资研究与只读查询（无交易功能）。用于投研分析、公司基本面调研、持仓/余额/行情查询。触发词：IBKR、分析公司、盈透、持仓、股价、行情、基本面、财报、投资建议。
---

# IBKR 只读查询技能

⚠️ **安全模式**：此技能只能查询数据，**无法执行任何交易操作**。

## 架构

通过 **IB Gateway** (桌面版) + **ib_insync** (socket API) 直连，替代了之前不稳定的 Client Portal Gateway HTTP 方案。

| 组件 | 说明 |
|------|------|
| IB Gateway | IBKR 官方桌面应用，常驻后台，支持 Auto Restart |
| ib_insync | Python socket API 客户端，内置断线重连 |
| keepalive.py | 健康检查脚本，断线时发 Telegram 通知 |

## 功能

| 功能 | 说明 |
|------|------|
| ✅ 查看持仓 | 显示所有股票持仓、成本、市值、盈亏 |
| ✅ 查看余额 | 显示现金余额、净资产 |
| ✅ 实时行情 | 查询任意股票的实时价格 |
| ✅ 深度基本面 | 查询公司市值、P/E市盈率、EPS、股息收益及行业分类 |
| ✅ 历史K线 | 获取过去 N 天/月/年的价格序列，用于趋势分析 |
| ✅ 市场扫描 | 查询全市场涨幅榜、跌幅榜及异动榜 |
| ❌ 下单 | **不支持** |
| ❌ 修改订单 | **不支持** |
| ❌ 取消订单 | **不支持** |

## 🤖 AI 助理执业规范 (Agent Execution Protocol)

作为用户的专属量化与投资分析顾问，当你被唤醒执行此技能时，**绝对不能仅仅返回枯燥的数字或不假思索地回答**。你必须执行以下 **"深度投研四步法"**：

1. **提取核心数据 (Data Anchoring)**
   - 必须通过执行 `/Users/qibaoba/clawd/skills/ibkr-trader/scripts/ibkr_readonly.py` 获取查询标的（如 IBM, LMND 等）的最新基本面指标（P/E，市值，52周高低点）以及最新新闻。
2. **强制全网深度检索 (Mandatory Web Search)**
   - 单靠 RSS 新闻是不够的！你必须使用你的 `search_web` 工具，去全网搜索该公司的**最新宏观事件、财报会议记录、产品动态及行业竞品动作**（例如：回答 IBM 时，必须要搜索目前 AI 行业如 Anthropic/OpenAI 对其护城河的影响）。
3. **推演与逻辑链 (Chain of Thought & Reasoning)**
   - 不要只罗列新闻！你要分析这些外部变量（竞品发布、宏观政策）会如何影响公司未来的盈利预期（EPS）和估值（P/E）。分析市场情绪，解释这只股票最近大涨或大跌的**潜在深层逻辑**。
4. **输出高管级研报 (Executive Summary)**
   - 以专业、条理清晰的格式回复用户。必须包含：`1. 📊 盘面与基本面速览`，`2. 🌪️ 核心事件驱动 (结合 web search 深度信息)`，`3. 🧠 深度竞品与护城河分析`，`4. 💡 总结与投资视角`。

## 前置条件

1. IBKR 账户（真实或模拟盘）
2. 手机安装 IBKR Key App（首次登录 IB Gateway 需要 2FA）
3. Mac 需要 Java 17+ 和 Python 3.9+
4. **IB Gateway** 桌面应用（从 IBKR 官网下载）

## 快速配置

### 1. 安装依赖

```bash
# 安装 Java
brew install openjdk@17

# Python 虚拟环境（已有则跳过）
cd ~/trading
source venv/bin/activate
pip install ib_insync requests
```

### 2. 安装 IB Gateway

从 IBKR 官网下载 **IB Gateway** (Stable channel)：
https://www.interactivebrokers.com/en/trading/ibgateway-stable.php

安装后启动，用 liusaibot 登录（需手机 2FA 确认）。

### 3. 配置 IB Gateway API Settings

在 IB Gateway 界面中：
- ✅ **Enable ActiveX and Socket Clients**
- ❌ **Read-Only API**（不要勾选，会阻止部分查询 API。安全性由账户层保障）
- 端口：**4001** (live)
- Trusted IPs：**127.0.0.1**
- ✅ **Auto Restart**（Settings → Lock and Exit → Auto restart，每周日自动重启）

### 4. 配置环境变量

`~/trading/.env`：
```bash
IB_HOST=127.0.0.1
IB_PORT=4001
IB_CLIENT_ID=1
```

### 5. 测试连接

```bash
cd ~/trading && source venv/bin/activate
python ibkr_readonly.py
```

## 使用方法

### 查看持仓和余额

```bash
cd ~/trading && source venv/bin/activate
python ibkr_readonly.py
```

### 在 OpenClaw 中使用

直接在 Telegram 问：
- "我的 IBKR 持仓有哪些？"
- "帮我查一下持仓盈亏"
- "帮我看看苹果 (AAPL) 最近的基本面，市值和市盈率怎么样？"
- "利用 IBKR 历史数据，分析一下 NVDA 最近 3 个月的走势"
- "今天美股涨得最猛的 10 只股票是哪些？"

## 健康检查

通过 keepalive.py 每 5 分钟检查 IB Gateway 状态，断线时发 Telegram 通知：

```bash
# Crontab
*/5 * * * * cd ~/trading && source venv/bin/activate && python keepalive.py >> ~/trading/keepalive.log 2>&1
```

IB Gateway 自带 Auto Restart，通常不需要手动干预。只有在以下情况才需要手动操作：
- IB Gateway 进程被杀
- Mac mini 重启后
- IBKR 维护期间

## 故障排查

| 问题 | 解决方案 |
|------|----------|
| 连接失败 | 检查 IB Gateway 是否启动并登录：看桌面是否有 IB Gateway 窗口 |
| 端口不通 | 检查 API Settings 中端口是否为 4001，是否勾选了 Socket Clients |
| 认证过期 | IB Gateway Auto Restart 会自动处理；如果失败，手动重启 IB Gateway 并登录 |
| 进程不在 | Mac 重启后需要手动启动 IB Gateway |

## 安全说明

此技能设计为**完全只读**：
- 源代码中不包含任何下单 API 调用
- `IBKRReadOnlyClient` 连接时使用 `readonly=True` 参数
- liusaibot 子账户本身也没有交易权限
- 即使有人要求下单，技能也无法执行
