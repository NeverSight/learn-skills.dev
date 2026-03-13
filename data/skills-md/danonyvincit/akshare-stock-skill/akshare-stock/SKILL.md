---
name: akshare-stock
description: 使用 AKShare 库获取和分析中国 A 股市场数据。AKShare 是免费开源的 Python 金融数据接口库，无需注册或 Token。支持：股票实时行情、历史K线、财务报表、估值指标、资金流向、技术指标、定时任务等。当用户需要获取 A 股股价、分析个股基本面、查询财务数据、计算技术指标、分析资金流向时使用此 skill。
---

# AKShare A股数据分析 Skill

使用 AKShare 库获取中国 A 股市场数据并进行分析。AKShare 是**免费开源**的金融数据接口，无需注册或 Token。

## 快速开始

### 环境准备

```bash
pip install akshare pandas numpy pyyaml
```

### 使用脚本

```bash
cd e:\AIproJect\A_Share\.agent\skills\akshare-stock\scripts

# 智能投资分析（推荐）
python analyze_investment.py 002475

# 实时行情
python get_realtime_quote.py 002475

# 历史K线
python get_history_kline.py 002475 --days 60

# 技术指标
python calc_technical.py 002475

# 综合分析报告
python stock_analyzer.py 002475 -o report.md
```

## 脚本列表

### 数据获取脚本

| 脚本 | 功能 | 示例 |
|------|------|------|
| `get_realtime_quote.py` | 实时行情 | `python get_realtime_quote.py 002475` |
| `get_history_kline.py` | 历史K线 | `python get_history_kline.py 002475 --days 60` |
| `get_valuation.py` | 估值指标 | `python get_valuation.py 002475` |
| `get_fund_flow.py` | 资金流向 | `python get_fund_flow.py 002475 --days 10` |
| `get_financial.py` | 财务数据 | `python get_financial.py 002475` |
| `get_shareholders.py` | 股东信息 | `python get_shareholders.py 002475` |
| `get_dividend.py` | 分红数据 | `python get_dividend.py 002475` |

### 分析脚本

| 脚本 | 功能 | 说明 |
|------|------|------|
| `analyze_investment.py` | 智能投资分析 | 多维度评分 + 投资建议 |
| `calc_technical.py` | 技术指标计算 | MA/MACD/RSI/KDJ/BOLL |
| `stock_analyzer.py` | 综合分析报告 | 合并所有数据的完整报告 |

### 工具脚本

| 脚本 | 功能 | 说明 |
|------|------|------|
| `cache_manager.py` | 数据缓存 | SQLite 本地缓存 |
| `scheduler.py` | 定时任务 | 自动获取数据和生成报告 |

## 核心功能

### 1. 智能投资分析

```bash
python analyze_investment.py 002475
```

自动分析：
- 📊 估值分析（PE/PB/股息率）
- 📈 成长性分析（营收/利润增速）
- 💵 资金面分析（主力资金流向）
- 📉 技术面分析（均线/MACD/RSI）
- 综合评分 + 投资建议

### 2. 技术指标

```bash
python calc_technical.py 002475
```

支持指标：
- **MA**: 5/10/20/60日均线
- **MACD**: DIF, DEA, MACD柱
- **RSI**: 6/12/24日
- **KDJ**: K, D, J
- **BOLL**: 上轨/中轨/下轨

### 3. 数据缓存

自动缓存避免重复请求：
- 实时行情：1分钟
- 日K线：1小时
- 财务数据：7天
- 股东数据：30天

### 4. 定时任务

```bash
# 立即执行
python scheduler.py --run-now

# 后台运行调度器
python scheduler.py
```

配置 `config.yaml` 设置监控股票和执行时间。

## 输出格式

所有脚本默认输出 **Markdown** 格式，可直接预览或保存：

```bash
python analyze_investment.py 002475 -o 分析报告.md
```

## 文件结构

```
akshare-stock/
├── SKILL.md                 # 本文档
├── config.yaml              # 配置文件
├── references/
│   ├── api_reference.md     # API 参考
│   └── official_docs.md     # 官方文档索引
└── scripts/
    ├── analyze_investment.py   # 智能分析
    ├── calc_technical.py       # 技术指标
    ├── cache_manager.py        # 数据缓存
    ├── scheduler.py            # 定时任务
    ├── stock_analyzer.py       # 综合分析
    ├── get_realtime_quote.py   # 实时行情
    ├── get_history_kline.py    # 历史K线
    ├── get_valuation.py        # 估值指标
    ├── get_fund_flow.py        # 资金流向
    ├── get_financial.py        # 财务数据
    ├── get_shareholders.py     # 股东信息
    └── get_dividend.py         # 分红数据
```

## 参考资源

- [API 参考文档](references/api_reference.md)
- [AKShare 官方文档](references/official_docs.md)
- **官网**: https://akshare.akfamily.xyz
- **GitHub**: https://github.com/akfamily/akshare
