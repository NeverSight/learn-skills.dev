---
name: trading-quant
description: "量化交易数据分析工具。A股/美股/港股/贵金属实时行情，多维度评分(技术面+资金面+基本面)，涨跌停池，北向资金，分钟级资金流。Use when: (1) 查询任何股票实时行情和评分, (2) 分析A股涨跌停异动, (3) 查看北向资金流向, (4) 美股港股贵金属行情, (5) 全球市场概览, (6) 个股资金流分析。"
---

# 量化交易数据分析

通过腾讯/新浪/东财/同花顺多数据源获取实时行情，提供5维评分体系。

## 工具列表

所有工具统一入口:
```bash
python3.12 {baseDir}/scripts/quant.py <tool> [args...]
```

### A股分析
```bash
python3.12 {baseDir}/scripts/quant.py stock_analysis [codes]
python3.12 {baseDir}/scripts/quant.py intraday_snapshot
```

### 全球市场
```bash
python3.12 {baseDir}/scripts/quant.py us_stock [symbols]
python3.12 {baseDir}/scripts/quant.py hk_stock [codes]
python3.12 {baseDir}/scripts/quant.py commodity [codes]
python3.12 {baseDir}/scripts/quant.py global_overview
```

### 市场数据
```bash
python3.12 {baseDir}/scripts/quant.py market_anomaly
python3.12 {baseDir}/scripts/quant.py market_scan
python3.12 {baseDir}/scripts/quant.py top_amount [N]
python3.12 {baseDir}/scripts/quant.py capital_flow [codes]
python3.12 {baseDir}/scripts/quant.py northbound_flow
python3.12 {baseDir}/scripts/quant.py gold_analysis
python3.12 {baseDir}/scripts/quant.py margin_data [code]
python3.12 {baseDir}/scripts/quant.py lhb [date]
python3.12 {baseDir}/scripts/quant.py main_flow [codes]
```

### 维护
```bash
python3.12 {baseDir}/scripts/quant.py warm_klines
python3.12 {baseDir}/scripts/quant.py save_daily
python3.12 {baseDir}/scripts/quant.py system_health
```

## 评分体系

| 维度 | 权重 | 指标 |
|------|------|------|
| 技术面 | 25% | MACD/RSI/KDJ/均线/布林 |
| 资金面 | 30% | 量比/换手率/量价/主力资金 |
| 基本面 | 10% | PE/PB/市值 |
| 消息面 | 20% | LLM 根据新闻原文判断 |
| 情绪面 | 15% | LLM 根据市场数据判断 |

### 信号等级
STRONG_BUY(>=80) > BUY(>=65) > WATCH(>=50) > HOLD(>=35) > SELL(>=20) > STRONG_SELL(<20)

## 数据源

| 市场 | 主源 | 降级链 |
|------|------|--------|
| A股 | 腾讯 | 新浪→东财→同花顺 |
| 美股 | 腾讯 | yfinance |
| 港股 | 腾讯 | - |
| 商品 | 新浪期货 | - |

## 规则

1. 必须使用工具获取数据，禁止凭记忆回答行情
2. PE>100 或 PB<0.8 时必须标注风险
3. 涨停>30只时提示市场情绪亢奋
4. 北向净流出>50亿时提示外资撤离
