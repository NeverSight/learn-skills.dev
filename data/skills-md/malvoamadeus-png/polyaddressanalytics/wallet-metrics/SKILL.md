---
name: wallet-metrics
description: "计算 Polymarket 钱包地址的 8 个核心交易指标（ROI、夏普比率、获利因子、最大回撤、胜率、仓位规模变异系数、HHI、当前持仓价值）。当用户提供钱包地址并询问指标、表现或交易统计时触发此技能。始终从 Polymarket API 获取最新数据。"
---

# Wallet Metrics Skill

## 目的

为单个 Polymarket 钱包地址快速计算 8 个核心交易指标，无需运行完整的数据管道或数据库存储。

**适用场景：**
- 用户提供钱包地址（0x... 格式）
- 用户询问该地址的交易表现、指标或统计数据
- 需要快速获取最新指标（10-20 秒内完成）

**不适用场景：**
- 策略分类分析（使用 polymarket-analyst 技能）
- 排行榜扫描或多账户比较
- 批量处理或数据库存储（使用根目录 Python 脚本）

---

## 快速工作流程

当用户请求钱包指标时：

1. **解析钱包地址**
   - 从用户输入中提取 0x 开头的以太坊地址
   - 验证地址格式（42 字符，0x 前缀）

2. **运行指标计算脚本**
   ```bash
   python .trae/skills/wallet-metrics/scripts/compute_wallet_metrics.py \
     --address <用户提供的地址> \
     --output /tmp/wallet_metrics.json
   ```

3. **读取并展示结果**
   - 读取 `/tmp/wallet_metrics.json`
   - 向用户展示结构化的指标数据
   - 如果有警告（如交易数量少），向用户说明

---

## 计算的指标

脚本输出 8 个核心指标：

### 1. ROI (投资回报率)
- **定义：** 总盈亏 / 成本基础
- **计算：** Total PnL / Sum(BUY USD_Spent)
- **解读：** 投资资本的百分比回报

### 2. Sharpe Ratio (夏普比率)
- **定义：** 风险调整后收益
- **计算：** Avg(daily PnL) / StdDev(daily PnL) × √365
- **解读：** 每单位风险的收益，> 1.0 为良好

### 3. Profit Factor (获利因子)
- **定义：** 总盈利 / 总亏损
- **计算：** Gross Profit / Gross Loss（按市场聚合 PnL）
- **解读：** 每亏损 1 美元赚取的美元数，> 2.0 为优秀

### 4. Max Drawdown (最大回撤)
- **定义：** 权益曲线的峰谷跌幅
- **计算：** (Peak - Trough) / Peak
- **解读：** 最坏连续亏损期，< 0.2 为良好

### 5. Win Rate (胜率)
- **定义：** 盈利交易占比
- **计算：** Winning Trades / Total Trades
- **解读：** 交易成功率，> 0.55 为良好

### 6. Position Size CV (仓位规模变异系数)
- **定义：** 下注金额的一致性
- **计算：** StdDev(BUY amounts) / Mean(BUY amounts)
- **解读：** 仓位管理纪律性，< 1.0 为一致

### 7. HHI (市场集中度指数)
- **定义：** 赫芬达尔-赫希曼指数
- **计算：** Σ(market_share²)
- **解读：** 市场分散度，< 0.25 为分散，> 0.5 为集中

### 8. Current Position Value (当前持仓价值)
- **定义：** 所有开仓持仓的 USD 价值
- **计算：** 从 Polymarket API 获取
- **解读：** 当前风险敞口

---

## 输出格式

脚本输出纯 JSON 格式：

```json
{
  "address": "0x...",
  "snapshot_date": "2026-03-02T12:34:56.789Z",
  "metrics": {
    "roi": 0.45,
    "sharpe_ratio": 1.23,
    "profit_factor": 2.15,
    "max_drawdown": 0.18,
    "win_rate": 0.62,
    "position_size_cv": 0.85,
    "hhi": 0.32,
    "current_position_value_usd": 3200.00
  },
  "summary": {
    "total_pnl": 12500.50,
    "total_trades": 145,
    "winning_trades": 90,
    "losing_trades": 55
  },
  "data_quality": {
    "trades_analyzed": 145,
    "date_range": "2024-01-15 to 2026-03-02",
    "warning": null
  }
}
```

**字段说明：**
- `metrics` — 8 个核心指标（可能为 null 如果数据不足）
- `summary` — 汇总统计（总盈亏、交易数、胜负场次）
- `data_quality` — 数据质量信息（分析的交易数、日期范围、警告）

---

## 错误处理

### 地址未找到
如果钱包地址没有交易历史：
- `data_quality.warning` 字段显示 "未找到交易历史"
- `metrics` 和 `summary` 为空对象
- 向用户说明该地址可能未在 Polymarket 交易过

### 交易数量少
如果交易数 < 20：
- `data_quality.warning` 字段显示警告信息
- 指标仍会计算，但向用户说明统计显著性可能不足

### API 速率限制
脚本复用根目录 `polymarket_metrics.py` 的速率限制器：
- Gamma API: 20 QPS
- Data API: 15 QPS
- CLOB API: 30 QPS
- User PnL API: 8 QPS

如果遇到速率限制，脚本会自动重试（指数退避）。

### 部分指标缺失
某些指标可能为 `null`：
- **Sharpe Ratio / Max Drawdown** — 如果 PnL 时间序列不可用
- **Position Size CV** — 如果 BUY 交易 < 2 笔
- **HHI** — 如果没有开仓持仓

向用户说明哪些指标不可用及原因。

---

## 执行时间

典型执行时间：**10-20 秒**

时间分布：
- 获取持仓数据：3-5 秒
- 获取 PnL 时间序列：2-4 秒
- 计算指标：1-2 秒
- 获取当前持仓价值：1-2 秒

---

## 与其他工具的区别

| 工具 | 用途 | 输出 | 执行时间 |
|------|------|------|----------|
| **wallet-metrics** (本技能) | 单地址快速指标 | 8 个核心指标（JSON） | 10-20 秒 |
| **polymarket-analyst** | 深度策略分析 | 25+ 指标 + 策略分类 | 30-60 秒 |
| **根目录 Python 脚本** | 批量处理 + 数据库 | SQLite + Supabase | 分钟级 |

---

## 示例对话

**用户：** "Get metrics for wallet 0x1234567890abcdef1234567890abcdef12345678"

**Claude 工作流程：**
1. 识别钱包地址
2. 运行 `compute_wallet_metrics.py --address 0x... --output /tmp/metrics.json`
3. 读取 JSON 输出
4. 向用户展示：
   - ROI: 45%
   - Sharpe Ratio: 1.23
   - Profit Factor: 2.15
   - Max Drawdown: 18%
   - Win Rate: 62%
   - Position Size CV: 0.85
   - HHI: 0.32 (分散)
   - Current Position Value: $3,200
   - 总盈亏: $12,500.50
   - 交易数: 145 笔（90 胜 / 55 负）

---

## 数据来源

所有数据来自 Polymarket 公开 API：
- **Gamma API** — 持仓数据
- **Data API** — 已平仓持仓
- **User PnL API** — PnL 时间序列
- **CLOB API** — 当前持仓价值

无需 API 密钥，所有端点均为公开访问。

---

## 限制

- **单地址查询** — 不支持批量或多账户比较
- **无策略分析** — 不进行策略分类或归因
- **无排行榜** — 不扫描或排名顶级交易者
- **无缓存** — 每次查询都获取最新数据（保证实时性）
- **JSON 输出** — 无人类可读的叙述性报告

如需上述功能，使用 `polymarket-analyst` 技能或根目录 Python 脚本。
