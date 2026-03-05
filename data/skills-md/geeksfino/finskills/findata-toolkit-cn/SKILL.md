---
name: findata-toolkit-cn
description: A股金融数据工具包。提供脚本获取A股实时行情、财务指标、董监高增减持、北向资金、宏观经济数据（LPR、CPI/PPI、PMI、社融、M2）。用于需要实时A股市场数据支撑投资分析时。所有数据源免费，无需API密钥。
license: Apache-2.0
---

# 金融数据工具包 — A股市场

自包含的数据工具包，提供A股市场实时金融数据和定量计算。所有数据源**免费**，**无需API密钥**。

## 安装

安装依赖（一次性）：

```bash
pip install -r requirements.txt
```

## 可用工具

所有脚本位于 `scripts/` 目录。从技能根目录运行。

### 1. A股数据 (`scripts/stock_data.py`)

通过 AKShare 获取A股基本面、行情、财务指标。

| 命令 | 用途 |
|------|------|
| `python scripts/stock_data.py 600519` | 基本信息（贵州茅台） |
| `python scripts/stock_data.py 600519 --metrics` | 完整财务指标（估值、盈利、杠杆、增长） |
| `python scripts/stock_data.py 600519 --history` | 历史OHLCV行情 |
| `python scripts/stock_data.py 600519 --financials` | 利润表、资产负债表、现金流量表 |
| `python scripts/stock_data.py 600519 --insider` | 董监高增减持数据 |
| `python scripts/stock_data.py --northbound` | 北向资金流向（沪股通/深股通） |
| `python scripts/stock_data.py 600519 000858 --screen` | 批量筛选 |

### 2. 宏观数据 (`scripts/macro_data.py`)

通过 AKShare 获取中国宏观经济指标。

| 命令 | 用途 |
|------|------|
| `python scripts/macro_data.py --dashboard` | 完整宏观仪表盘 |
| `python scripts/macro_data.py --rates` | 利率数据（LPR、Shibor） |
| `python scripts/macro_data.py --inflation` | CPI/PPI数据 |
| `python scripts/macro_data.py --pmi` | PMI数据（制造业/非制造业） |
| `python scripts/macro_data.py --social-financing` | 社会融资规模 + M2 |
| `python scripts/macro_data.py --cycle` | 经济周期阶段判断 |

## 数据来源

| 来源 | 数据内容 | API密钥 |
|------|----------|---------|
| AKShare | A股行情、财务数据、董监高交易、北向资金、宏观指标 | 无需 |

## 输出格式

所有脚本以 **JSON** 输出到标准输出，便于解析。错误信息输出到标准错误。

## 配置

可选：编辑 `config/data_sources.yaml` 自定义速率限制或添加付费数据源API密钥。
