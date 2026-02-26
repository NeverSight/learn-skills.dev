---
name: akshare-stock
description: A股分析全能 Skill（实时行情、技术面、基本面、板块、衍生品与跨市场），基于 akshare + 自然语言路由
metadata:
  openclaw:
    emoji: "📈"
    requires:
      python_modules: ["akshare", "pandas", "numpy"]
---

# A股分析全能 Skill（AKShare）

目标：在 OpenClaw 中通过自然语言触发 A 股和相关市场分析，输出适配 QQ/Telegram 的紧凑文本。

- 运行环境：Mac + Python 3.9
- akshare 路径：`/Users/molezz/Library/Python/3.9/lib/python3.9/site-packages`
- Skill 入口建议：`python3 skills/akshare-stock/main.py --query "${USER_QUERY}"`

---

## 1) 整体架构设计

采用 `Router -> Service -> Analyzer -> Formatter` 四层结构，便于扩展和维护。

### A. 目录组织（建议）

```text
skills/akshare-stock/
  SKILL.md
  main.py                 # OpenClaw 调用入口
  router.py               # 意图识别 + 参数解析
  schemas.py              # 数据结构定义（dataclass）
  formatter.py            # QQ/Telegram 输出模板
  services/
    market_service.py     # 大盘/个股行情、K线、分时、涨跌停、资金流
    fundamental_service.py# 财务指标、财报、融资融券、龙虎榜
    sector_service.py     # 行业/概念板块、轮动、板块资金流
    cross_service.py      # 期货/期权、基金、可转债、港股/美股
  analyzers/
    kline_analyzer.py     # 均线、振幅、涨跌幅、量比等
    flow_analyzer.py      # 主力净流入、连续性、强弱排序
    rotation_analyzer.py  # 板块轮动强度、持续性
  adapters/
    akshare_adapter.py    # 封装 akshare 接口，隔离 API 变化
  utils/
    trading_calendar.py   # 交易日判断
    symbols.py            # 指数/股票/板块别名映射
    cache.py              # 短缓存（30~120 秒）
```

### B. 核心流程

1. `main.py` 接收自然语言 query。
2. `router.py` 输出结构化意图：`intent + symbols + timeframe + metric + top_n`。
3. `services/*` 拉取原始数据（只做数据获取和轻清洗）。
4. `analyzers/*` 做指标计算和结论生成。
5. `formatter.py` 按聊天平台压缩输出（短句、分段、emoji、重点数值）。

### C. 关键设计点

- **意图优先级**：先识别“任务类型”，再解析标的和参数，避免误判。
- **适配层隔离**：akshare 接口若改名，只需改 `adapters/akshare_adapter.py`。
- **容错回退**：实时接口失败时回退到最近交易日数据，并标注“非实时”。
- **缓存策略**：
  - 大盘/资金流：30~60 秒
  - 板块排行：60~120 秒
  - 财报/财务：当天缓存
- **消息长度控制**：单条建议 <= 1000 字符；超长自动拆分 2~3 条。

---

## 2) 触发词设计（自然语言路由）

建议采用“关键词 + 正则 + 别名词典”混合方式。

### A. 意图分类（Intent）

- `INDEX_REALTIME`：实时大盘
- `KLINE_ANALYSIS`：历史 K 线
- `INTRADAY_ANALYSIS`：分时分析
- `LIMIT_STATS`：涨跌停统计
- `MONEY_FLOW`：资金流向
- `FUNDAMENTAL`：财务指标 / 财报
- `MARGIN_LHB`：融资融券 / 龙虎榜
- `SECTOR_ANALYSIS`：行业/概念/轮动/板块资金
- `DERIVATIVES`：期货/期权
- `FUND_BOND`：基金净值 / 可转债
- `HK_US_MARKET`：港股 / 美股

### B. 触发词样例

- 实时大盘：`A股大盘` `上证现在多少` `沪深300实时`
- K线：`贵州茅台近60日K线` `宁德时代周线` `比亚迪月线复权`
- 分时：`看下000001分时` `平安银行今天分时走势`
- 涨跌停：`今日涨停统计` `跌停家数` `连板梯队`
- 资金流：`主力资金流入前十` `北向资金` `行业资金净流入`
- 基本面：`茅台财务指标` `宁德时代最新季报` `ROE和毛利率`
- 融资融券/龙虎榜：`中兴通讯融资融券` `今日龙虎榜`
- 板块：`行业板块涨幅榜` `概念轮动` `AI板块资金流`
- 其他市场：`IF主力合约` `300ETF期权` `基金净值` `可转债行情` `腾讯港股` `英伟达美股`

### C. 参数抽取规则

- 股票代码：`\b\d{6}\b`（如 `600519`）
- 日期：`YYYYMMDD` / `YYYY-MM-DD` / `今天/昨日/近N日`
- 周期：`1m/5m/15m/30m/60m/day/week/month`
- 排名：`前N`（默认 10）
- 复权：`前复权/后复权/不复权`

---

## 3) 各功能实现思路

下面是“功能 -> 推荐数据 -> 分析输出”的落地框架（接口以 akshare 当前版本为准，实际以 adapter 层统一封装）。

### 3.1 实时大盘行情（已有基础版，升级点）

- 数据：上证、深成指、创业板、沪深300、上证50、科创50。
- 增强：加入成交额、振幅、领涨板块、北向资金当日净流入。
- 输出：`指数点位 + 涨跌幅 + 市场情绪一句话`。

### 3.2 行情分析

- **历史K线**：
  - 数据：日/周/月 K 线（复权可选）。
  - 指标：近 N 日涨跌幅、5/10/20 日均线、量能变化、波动率。
  - 输出：趋势判断（多头/震荡/走弱）+ 关键位（支撑/压力）。
- **分时数据**：
  - 数据：分钟级行情。
  - 指标：VWAP 偏离、盘中高低点、午后资金回流。
- **涨跌停统计**：
  - 数据：涨停池、跌停池、连板梯队。
  - 指标：涨停家数、炸板率、最高连板、情绪评分。
- **资金流向**：
  - 数据：个股/行业/市场资金流。
  - 指标：主力净流入 TopN、连续净流入天数、资金集中度。

### 3.3 基本面分析

- **个股财务指标**：ROE、毛利率、净利率、资产负债率、经营现金流。
- **财报数据**：营收同比、净利润同比、扣非净利润同比、EPS。
- **融资融券**：融资余额、融券余额、日变动，识别杠杆偏好。
- **龙虎榜**：上榜原因、买卖前五席位净额、游资活跃度。
- 输出风格：`核心指标摘要 + 同比/环比 + 风险提示`。

### 3.4 板块分析

- **行业板块涨跌**：行业涨跌幅榜、成交额、上涨家数。
- **概念板块轮动**：近 5 日强度、持续性、日内切换速度。
- **板块资金流向**：行业/概念净流入排行 + 领涨龙头。
- 输出：`强势板块Top3 + 轮动结论 + 次日观察点`。

### 3.5 其他（跨市场）

- 期货/期权：主力合约价格、涨跌、持仓变化；期权 PCR（若可得）。
- 基金净值：开放式基金净值、估值偏离、近一周收益。
- 可转债：价格、溢价率、正股联动、成交额。
- 港股/美股：实时行情、近5日表现、与A股联动提示。

---

## 4) 代码示例框架（骨架）

> 说明：以下为可直接落地的最小框架，不含完整业务细节。

### `main.py`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from router import parse_query
from services.market_service import MarketService
from services.fundamental_service import FundamentalService
from services.sector_service import SectorService
from services.cross_service import CrossService
from formatter import render_output


def dispatch(intent_obj):
    intent = intent_obj.intent

    if intent in {"INDEX_REALTIME", "KLINE_ANALYSIS", "INTRADAY_ANALYSIS", "LIMIT_STATS", "MONEY_FLOW"}:
        data = MarketService().handle(intent_obj)
    elif intent in {"FUNDAMENTAL", "MARGIN_LHB"}:
        data = FundamentalService().handle(intent_obj)
    elif intent == "SECTOR_ANALYSIS":
        data = SectorService().handle(intent_obj)
    elif intent in {"DERIVATIVES", "FUND_BOND", "HK_US_MARKET"}:
        data = CrossService().handle(intent_obj)
    else:
        data = {"ok": False, "error": "未识别请求，请补充标的或时间范围"}

    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True, help="自然语言请求")
    parser.add_argument("--platform", default="qq", choices=["qq", "telegram"])
    args = parser.parse_args()

    intent_obj = parse_query(args.query)
    result = dispatch(intent_obj)
    text = render_output(intent_obj, result, platform=args.platform)
    print(text)


if __name__ == "__main__":
    main()
```

### `router.py`

```python
from dataclasses import dataclass, field
import re


@dataclass
class IntentObj:
    intent: str
    symbols: list = field(default_factory=list)
    timeframe: str = "day"
    days: int = 60
    top_n: int = 10
    date: str = ""
    raw_query: str = ""


def parse_query(query: str) -> IntentObj:
    q = query.strip()
    obj = IntentObj(intent="INDEX_REALTIME", raw_query=q)

    # 1) intent
    if any(k in q for k in ["K线", "日线", "周线", "月线"]):
        obj.intent = "KLINE_ANALYSIS"
    elif "分时" in q:
        obj.intent = "INTRADAY_ANALYSIS"
    elif any(k in q for k in ["涨停", "跌停", "连板"]):
        obj.intent = "LIMIT_STATS"
    elif "资金" in q:
        obj.intent = "MONEY_FLOW"
    elif any(k in q for k in ["财务", "财报", "ROE", "毛利率"]):
        obj.intent = "FUNDAMENTAL"
    elif any(k in q for k in ["融资融券", "龙虎榜"]):
        obj.intent = "MARGIN_LHB"
    elif any(k in q for k in ["板块", "行业", "概念", "轮动"]):
        obj.intent = "SECTOR_ANALYSIS"
    elif any(k in q for k in ["期货", "期权"]):
        obj.intent = "DERIVATIVES"
    elif any(k in q for k in ["基金", "净值", "可转债"]):
        obj.intent = "FUND_BOND"
    elif any(k in q for k in ["港股", "美股", "纳斯达克", "道琼斯"]):
        obj.intent = "HK_US_MARKET"

    # 2) symbol
    code_hits = re.findall(r"\b\d{6}\b", q)
    if code_hits:
        obj.symbols = code_hits

    # 3) topN
    m = re.search(r"前\s*(\d+)", q)
    if m:
        obj.top_n = int(m.group(1))

    return obj
```

### `adapters/akshare_adapter.py`

```python
import akshare as ak


class AkAdapter:
    def index_spot(self):
        return ak.stock_zh_index_spot_sina()

    def stock_kline(self, symbol: str, period: str = "daily", start_date: str = "", end_date: str = "", adjust: str = "qfq"):
        # 实际参数与函数名按本地 akshare 版本适配
        return ak.stock_zh_a_hist(symbol=symbol, period=period, start_date=start_date, end_date=end_date, adjust=adjust)

    def stock_intraday(self, symbol: str, period: str = "1"):
        return ak.stock_zh_a_minute(symbol=symbol, period=period)

    def limit_up_pool(self, date: str):
        return ak.stock_zt_pool_em(date=date)

    def limit_down_pool(self, date: str):
        return ak.stock_dt_pool_em(date=date)
```

### `formatter.py`

```python
from datetime import datetime


def render_output(intent_obj, result: dict, platform: str = "qq") -> str:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")

    if not result.get("ok", False):
        return f"⚠️ 请求失败\n原因: {result.get('error', '未知错误')}\n时间: {ts}"

    title = result.get("title", "A股分析")
    lines = result.get("lines", [])
    tips = result.get("tips", "")

    # QQ/Telegram 友好输出：短行 + 分段 + 关键数字优先
    text = [f"📊 {title}", f"🕒 {ts}", ""]
    text.extend(lines[:15])
    if tips:
        text.extend(["", f"💡 {tips}"])
    text.append("\n数据源: akshare")

    # 长度保护
    merged = "\n".join(text)
    return merged[:1000]
```

---

## 输出模板建议（QQ/Telegram）

建议统一为三段：`结论 -> 关键数据 -> 风险提示`。

示例：

```text
📊 A股午盘情绪
🕒 2026-02-18 11:31

- 上证指数 3210.35（+0.62%）
- 两市成交额 6821 亿，较昨日同期 +8.4%
- 涨停 52 / 跌停 7，连板高度 4
- 主力净流入前三：证券、AI算力、汽车零部件

💡 结论：指数偏强，情绪修复中；但午后关注高位分歧。
数据源: akshare
```

---

## 落地顺序（建议）

1. 保留现有实时大盘，抽象进 `MarketService.index_realtime()`。
2. 先补齐行情分析四件套：K线/分时/涨跌停/资金流。
3. 再加基本面与板块分析（中频请求，缓存收益高）。
4. 最后接入期货/期权/基金/可转债/港美股。
5. 每个模块都先做“可读文本输出”，再逐步增加指标深度。

该设计能保证你先快速可用，再逐步增强，不会一次性堆太多接口导致维护困难。
