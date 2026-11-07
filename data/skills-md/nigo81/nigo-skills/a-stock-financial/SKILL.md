---
name: a-stock-financial
description: A股上市公司财务报表查询与导出工具。支持资产负债表、利润表、现金流量表三大报表及财务摘要，按报告期/年度/单季度查询，可导出 Excel。触发词：查财报、财务报表、资产负债表、利润表、现金流量表、财务数据、上市公司财报、导出财报、年报、季报。当用户提到任何A股公司的财务数据、财报分析、三大报表时都应使用此 skill。
triggers:
  - 财报
  - 财务报表
  - 资产负债表
  - 利润表
  - 现金流量表
  - 财务数据
  - 上市公司
  - 三大报表
  - 年报
  - 季报
  - 导出财报
  - 导出Excel
slug: nigo-a-stock-financial
displayName: A股财报查询工具
version: 1.0.0
summary: A股上市公司财务报表查询与导出，支持资产负债表、利润表、现金流量表及财务摘要，按报告期/年度/单季度查询，可导出 Excel。
license: MIT
---

# A股上市公司财务报表查询

基于 AkShare（同花顺数据源）获取A股上市公司财务报表，支持查询和导出 Excel。

## 依赖

```bash
pip install akshare openpyxl
```

## 股票代码查询

**不要用 `stock_zh_a_spot_em()` 拉全市场行情（极慢，需1分钟+）。**

用户说公司名称而非代码时，用 WebSearch 搜索"XX 股票代码"即可。

## 可用数据

| 报表 | 列数 | 内容 |
|------|------|------|
| 资产负债表 | 80列 | 流动/非流动资产、流动/非流动负债、权益各明细 |
| 利润表 | 46列 | 营收→成本各项→营业利润→净利润→每股收益→综合收益 |
| 现金流量表 | 73列 | 直接法三大活动现金流 + 间接法补充资料 |
| 财务摘要 | 20+指标 | 净利率、毛利率、ROE、存货周转率、流动比率等 |

每个报表支持3个时间维度：`按报告期`（最全）、`按年度`（多年对比）、`按单季度`

## 工作流

### 1. 确认参数

- **股票代码**：用户给出代码直接用；说公司名则 WebSearch 搜索
- **报表类型**：默认查全部，用户指定则只查对应报表（balance/income/cashflow/abstract）
- **时间维度**：默认 `按报告期`，年报对比用 `按年度`，看季度用 `按单季度`
- **用户说"近N年/近N期"的映射**：
  - "近3年" = `--indicator 按年度 --last 3`（取最近3个年度）
  - "近4期" = `--indicator 按报告期 --last 4`（取最近4个报告期，含季报/半年报/年报）
  - "2025年报" = `--period 2025-12-31`
  - "2025三季报" = `--period 2025-09-30`

### 2. 查询报表

```bash
SCRIPT=~/.claude/skills/a-stock-financial/scripts/fetch_reports.py

# 查所有报表，按报告期，最近4期
python3 $SCRIPT <股票代码>

# 只查利润表，按年度，最近5年
python3 $SCRIPT <股票代码> --type income --indicator 按年度 --last 5

# 查资产负债表，指定报告期（只返回1期数据）
python3 $SCRIPT <股票代码> --type balance --period 2025-12-31

# 查财务摘要
python3 $SCRIPT <股票代码> --type abstract

# 输出为 JSON
python3 $SCRIPT <股票代码> --output json
```

`--type` 可选：`balance`、`income`、`cashflow`、`abstract`、`all`（默认）
`--indicator` 可选：`按报告期`（默认）、`按年度`、`按单季度`

### 3. 展示结果

以表格形式展示关键指标，并提供简要财务分析：
- 营收趋势、利润率变化
- 资产负债结构、偿债能力
- 现金流健康度
- 与往年数据的同比变化

### 4. 导出 Excel（用户要求时）

```bash
EXPORT=~/.claude/skills/a-stock-financial/scripts/export_excel.py

# 导出所有报告期（默认最近20期）
python3 $EXPORT <股票代码> <公司名称>

# 只导出2025年报（1期数据）
python3 $EXPORT 600326 西藏天路 --period 2025-12-31

# 导出最近3期
python3 $EXPORT 600326 西藏天路 --last 3

# 按年度导出，最近5年
python3 $EXPORT 600326 西藏天路 --indicator 按年度 --last 5

# 指定输出路径
python3 $EXPORT 600326 西藏天路 --output /tmp/财报.xlsx
```

导出文件包含4个 Sheet：资产负债表、利润表、现金流量表、财务摘要。

## 注意事项

- symbol 为 6 位股票代码（如 "600326"），不含交易所后缀
- 数据源为同花顺，完全免费无需 token
- 数据单位通常为"亿"，带 `*` 的是核心指标列
- 如果东财接口报错，同花顺接口（`_ths` 后缀）是稳定的备选


---

> 作者：nigo
> 微信公众号：逆行的狗
