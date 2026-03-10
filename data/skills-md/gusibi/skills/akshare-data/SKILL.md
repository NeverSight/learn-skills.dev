---
name: akshare-data
description: Query Chinese and global financial data using the AKShare Python library. Use when asked to (1) fetch stock quotes, historical prices, or financial statements for A-shares/HK/US stocks, (2) query macroeconomic data like GDP/CPI/PMI, (3) get futures/options/bond/forex/fund data, (4) look up index data, or (5) retrieve alternative data like news sentiment. Covers 500+ data interfaces for stocks, futures, options, bonds, forex, funds, macro, indexes and alternative data.
---

# AKShare 财经数据查询

基于 [AKShare](https://github.com/akfamily/akshare) 的财经数据查询 skill，覆盖股票、期货、期权、债券、外汇、基金、宏观经济、指数、另类数据等 500+ 个数据接口。

## 快速使用

使用通用查询脚本 `scripts/akshare_query.py` 查询数据：

```bash
python3 scripts/akshare_query.py <函数名> [参数=值] ... [--save output.csv] [--head N]
```

示例：
```bash
# A股历史行情（前复权）
python3 scripts/akshare_query.py stock_zh_a_hist symbol=000001 period=daily start_date=20240101 end_date=20241231 adjust=qfq

# A股实时行情（前20条）
python3 scripts/akshare_query.py stock_zh_a_spot_em --head 20

# 中国CPI数据并保存
python3 scripts/akshare_query.py macro_china_cpi --save cpi.csv
```

## 数据类别路由

根据用户查询需求，加载对应的 reference 文件获取具体接口信息：

| 用户需求关键词 | 加载文件 |
|---|---|
| 股票行情、财报、资金流向、板块、龙虎榜、沪深港通、A股、港股、美股 | [references/stock.md](references/stock.md) |
| 期货行情、持仓排名、仓单、交割、内盘、外盘 | [references/futures.md](references/futures.md) |
| 期权、希腊字母、隐含波动率 | [references/options.md](references/options.md) |
| 债券、可转债、国债、企业债、债券回购 | [references/bond.md](references/bond.md) |
| 汇率、外汇、货币 | [references/forex.md](references/forex.md) |
| 基金、ETF、LOF、基金排名、净值 | [references/fund.md](references/fund.md) |
| GDP、CPI、PMI、利率、宏观经济、失业率 | [references/macro.md](references/macro.md) |
| 股票指数、大盘指数、行业指数、中证指数 | [references/index_data.md](references/index_data.md) |
| 新闻舆情、百度指数、空气质量、电影票房 | [references/alternative.md](references/alternative.md) |

## 通用注意事项

1. **安装**：脚本自动安装 akshare（首次运行时 `pip install akshare`）
2. **数据格式**：所有接口返回 pandas DataFrame，可用 `--save` 导出 CSV
3. **日期格式**：日期参数统一使用 `YYYYMMDD` 格式（如 `20240101`）
4. **股票代码**：A股使用6位数字代码（如 `000001`），港股使用5位代码（如 `00700`），美股使用字母代码（如 `AAPL`）
5. **复权方式**：`adjust=""` 不复权，`adjust="qfq"` 前复权，`adjust="hfq"` 后复权
6. **频率**：`period` 参数支持 `daily`（日）、`weekly`（周）、`monthly`（月）
7. **限流**：部分接口有频率限制，若报错可稍后重试
8. **API 文档**：完整接口文档见 https://akshare.akfamily.xyz/data/index.html
