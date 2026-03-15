---
name: stock-briefing
description: 股市简报 - 零依赖增强版。行情+成交量趋势+资金流向+北向资金+多源新闻+量价分析，不需要任何API Key。当蟹大爷说"来份股市简报"、"股市简报"时使用。
allowed-tools:
  - Bash(python:*)
  - Read
---

# 股市简报

零依赖的股市简报生成器。不需要 tushare、不需要 API Key，任何环境都能跑。

## 使用方法

```bash
python3 scripts/stock_briefing.py
```

**把脚本输出原样发给蟹大爷，不要修改、不要补充、不要总结。**

## 报告内容

1. 📈 大盘收盘概况（三大指数+沪深成交额）
2. 📊 近5日成交量趋势柱状图（自动标注放量/缩量）
3. 📋 自选股行情（A股+港股，自动标注涨跌最大）
4. 💰 资金流向（大盘主力+北向资金+自选股主力资金）
5. 📰 今日要闻（财联社早间精选，备用新浪7x24）
6. 💡 小结（量能分析+资金面分析+趋势判断，全规则化）

## 数据来源

- A股大盘指数+成交额：东方财富 push2his API
- A股个股行情：腾讯日K线 web.ifzq.gtimg.cn
- 港股行情：腾讯日K线 + 实时接口（名称）
- 资金流向（大盘+个股主力）：东方财富 fflow API
- 北向资金（沪/深股通）：东方财富 kamt API
- 财经新闻：财联社电报 API（优先）+ 新浪7x24财经（备用）

## 零依赖

- 不需要 pip install 任何包
- 不需要任何 API Key 或 Token
- 只用 Python 标准库（urllib, json, re, datetime）

## 自选股修改

编辑 `scripts/stock_briefing.py` 顶部的 `A_STOCKS` 和 `HK_STOCKS` 列表。
