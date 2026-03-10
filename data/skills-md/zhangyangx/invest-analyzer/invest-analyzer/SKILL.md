---
name: invest-analyzer
version: 1.0.0
description: 投资分析工具 - 行情、技术指标与新闻资讯
---

# 股票分析 Skill

## 一、工作流程

1. 用户输入股票代码或股票名称
2. AI 调用 scripts 目录下的脚本获取数据
3. AI 输出结构化的 Markdown 分析报告

## 二、脚本列表

### 2.1 股票搜索 (`scripts/stock_search.py`)

根据关键词搜索股票代码。

**用法：**
```bash
python3 stock_search.py <关键词> [--source auto|sina|tencent] [--limit N]
```

**参数：**
- `keyword`（必填）：股票名称或代码
- `--source`（可选）：`auto`（默认）、`sina`、`tencent`
- `--limit`（可选）：最大结果数，默认 10，最多 50

**示例：**
```bash
python3 stock_search.py 贵州茅台
python3 stock_search.py 茅台 --source sina
python3 stock_search.py 6005 --limit 5
```

**输出（JSON）：**
```json
{
  "keyword": "贵州茅台",
  "source": "sina",
  "count": 1,
  "items": [
    {
      "name": "贵州茅台",
      "code": "600519",
      "symbol": "sh600519",
      "market": "SH",
      "type": "stock"
    }
  ]
}
```

---

### 2.2 实时行情 (`scripts/stock_quote.py`)

获取当前价格、涨跌幅、成交量等实时数据。

**用法：**
```bash
python3 stock_quote.py <股票代码>
```

**参数：**
- `stock_code`（必填）：6 位股票代码
  - 支持格式：`600519`、`sh600519`、`sz000001`
  - 自动识别市场前缀（60/68 开头为 sh，其他为 sz）

**示例：**
```bash
python3 stock_quote.py 600519
python3 stock_quote.py sh600519
```

**输出（JSON）：**
```json
{
  "name": "贵州茅台",
  "code": "600519",
  "symbol": "sh600519",
  "current": 1680.00,
  "prev_close": 1670.00,
  "open": 1675.00,
  "high": 1690.00,
  "low": 1670.00,
  "volume": 2500000,
  "amount": 4200000000,
  "change": 10.00,
  "pct_change": 0.60
}
```

---

### 2.3 K线数据 (`scripts/stock_kline.py`)

获取 K 线数据用于计算技术指标。

**用法：**
```bash
python3 stock_kline.py <股票代码> [周期] [数量]
```

**参数：**
- `stock_code`（必填）：股票代码
- `scale`（可选）：K 线周期（分钟），默认 `240`
- `count`（可选）：数据条数，默认 `120`

**时间周期说明：**
| Scale | 含义 | 用途 |
|-------|------|------|
| `5` | 5分钟K线 | 日内短线、分时走势 |
| `15` | 15分钟K线 | 短线参考 |
| `60` | 60分钟K线 | 日内波段 |
| `240` | 日K线（默认） | 中长期趋势 |

**示例：**
```bash
python3 stock_kline.py 600519
python3 stock_kline.py 600519 5 200
python3 stock_kline.py 600519 60 150
```

**输出（JSON）：**
```json
{
  "symbol": "sh600519",
  "scale": 240,
  "count": 120,
  "klines": [
    {
      "open": "1670.00",
      "high": "1690.00",
      "low": "1665.00",
      "close": "1680.00",
      "volume": "2500000"
    }
  ]
}
```

---

### 2.4 技术指标 (`scripts/stock_indicators.py`)

根据 K 线数据计算 MA/MACD/KDJ/RSI/BOLL 指标。

**用法：**
```bash
# 方法 1：从标准输入读取 K 线数据
python3 stock_kline.py 600519 | python3 stock_indicators.py

# 方法 2：从文件读取
python3 stock_indicators.py --file kline_data.json
```

**参数：**
- `--file <path>`（可选）：从文件读取 K 线 JSON

**输出（JSON）：**
```json
{
  "MA": {
    "MA5": {"history": [1660.5, 1662.3, ..., 1675.20], "current": 1675.20},
    "MA10": {"history": [1658.2, 1659.8, ..., 1672.50], "current": 1672.50},
    "MA20": {"history": [1655.1, 1656.5, ..., 1670.80], "current": 1670.80},
    "MA60": {"history": [1640.3, 1642.1, ..., 1665.40], "current": 1665.40},
    "MA120": {"history": [1620.5, 1622.3, ..., 1660.20], "current": 1660.20}
  },
  "MACD": {
    "DIF": {"history": [2.1, 3.5, ..., 5.23], "current": 5.23},
    "DEA": {"history": [1.8, 2.9, ..., 4.18], "current": 4.18},
    "MACD": {"history": [0.6, 1.2, ..., 2.10], "current": 2.10}
  },
  "KDJ": {
    "K": {"history": [55.2, 58.8, ..., 65.20], "current": 65.20},
    "D": {"history": [52.1, 54.5, ..., 60.15], "current": 60.15},
    "J": {"history": [61.4, 67.4, ..., 75.30], "current": 75.30}
  },
  "RSI": {
    "RSI6": {"history": [52.3, 55.1, ..., 58.20], "current": 58.20},
    "RSI12": {"history": [50.8, 53.2, ..., 55.40], "current": 55.40},
    "RSI24": {"history": [48.5, 50.9, ..., 52.80], "current": 52.80}
  },
  "BOLL": {
    "upper": {"history": [1680.5, 1682.3, ..., 1690.50], "current": 1690.50},
    "middle": {"history": [1665.2, 1667.1, ..., 1675.20], "current": 1675.20},
    "lower": {"history": [1650.1, 1652.2, ..., 1659.90], "current": 1659.90}
  },
  "volume": {
    "history": [2000000, 2100000, ..., 2500000],
    "current": 2500000
  }
}
```

**说明**：每个指标包含 `history`（历史序列）和 `current`（当前值），可用于判断趋势、交叉、背离等。

---

### 2.5 关键词扩展 (`scripts/keyword_expander.py`)

根据股票名称和主题生成新闻搜索关键词。

**用法：**
```bash
python3 keyword_expander.py --name <股票名称> [--topic <文本>] [--topic-en <文本>]
```

**参数：**
- `--name`（必填）：股票名称
- `--topic`（可选）：中文主题
- `--topic-en`（可选）：英文主题（AI 翻译提供）
- `--extra`（可选）：额外关键词，逗号分隔

**示例：**
```bash
python3 keyword_expander.py --name 贵州茅台
python3 keyword_expander.py --name "贵州茅台" --topic "财报,业绩"
python3 keyword_expander.py --name "贵州茅台" --topic-en "earnings"
```

**输出（JSON）：**
```json
{
  "keywords": [
    "贵州茅台",
    "财报",
    "贵州茅台 财报"
  ]
}
```

---

### 2.6 新闻获取 (`scripts/news_fetcher.py`)

通过 Google News RSS 获取相关新闻。

**用法：**
```bash
# 单关键词搜索
python3 news_fetcher.py --keyword "<英文关键词>" --hours 24 --limit 30

# 多关键词搜索
python3 news_fetcher.py --keywords "AAPL,Apple,iPhone" --hours 24
```

**参数：**
- `--keyword`（可选）：单个关键词
- `--keywords`（可选）：逗号分隔的多个关键词
- `--hours`（可选）：时间窗口（小时），默认 24
- `--limit`（可选）：最大新闻数，默认 30

**重要提示：**
- Google News RSS 对英文关键词支持最好
- AI必须将中文关键词翻译为英文后传入此脚本
- 例如：贵州茅台 → "Moutai" 或 "KWE"；财报 → "earnings"

**输出（JSON）：**
```json
{
  "items": [
    {
      "title": "Stock Market Hits Record High",
      "link": "https://example.com/article1",
      "source": "Google News",
      "time": "2026-02-05 18:30:00 +0800"
    }
  ],
  "count": 1
}
```

## 三、AI 使用指南

### 3.1 输入验证
- 6 位数字股票代码 → 直接处理
- 股票名称或关键词 → 调用 `stock_search.py` 解析
- 多个搜索结果 → 询问用户确认

### 3.2 核心分析流程
1. 调用 `stock_quote.py` 获取实时行情
2. **必须同时分析两个时间周期的 K 线和技术指标：**
   ```bash
   # 5分钟K线 + 指标（日内短线分析）
   python3 stock_kline.py 600519 5 200 | python3 stock_indicators.py

   # 日K线 + 指标（中长期趋势分析）
   python3 stock_kline.py 600519 240 120 | python3 stock_indicators.py
   ```
3. 输出报告需包含两个维度的技术分析

### 3.3 新闻搜索触发条件

仅在用户明确或隐式要求时触发新闻搜索：

**明确触发词：**
- 新闻、消息、资讯、事件、头条、情况

**隐式触发：**
- 询问最近国际形势、宏观环境、背景信息等

### 3.4 关键词生成与翻译规则
- 使用 `keyword_expander.py --name <股票名称>` 生成搜索关键词
- **有主题**：添加 `--topic <主题>` 或 `--topic-en <英文主题>`
- **AI翻译要求**：调用 `news_fetcher.py` 前，AI必须将所有中文关键词翻译成英文
  - 股票名称 → 英文代码或英文名（如：贵州茅台 → KWE 或 Moutai）
  - 主题词汇 → 英文财经术语（如：财报 → earnings，业绩 → performance）
- 每次请求最多 4-5 个关键词

### 3.5 新闻输出要求
- 英文标题翻译成中文
- 每条新闻提供一行中文摘要
- 标注影响判断（正面/负面/中性）

### 3.6 错误处理
- **无效股票代码**：提示用户并要求重新输入
- **网络/API 失败**：重试一次，失败后告知用户并继续使用已有数据
- **无新闻**：显示"过去 24 小时无相关新闻"并继续其他部分

## 四、技术指标解读规则

### 4.1 趋势指标（MA）

**当前状态判断**：
- **多头排列**：短期 MA > 长期 MA（MA5 > MA20 > MA60），看涨
- **空头排列**：短期 MA < 长期 MA，看跌
- **价格与 MA 关系**：
  - 价格 > MA5：短期强势
  - 价格 > MA20：中期强势
  - 价格 < MA60：中期偏弱

**趋势方向与强度**（基于 history 序列）：
- **MA 斜率**：比较最近 N 天的 MA 值变化
  - MA5 上升：短期上升趋势
  - MA5 下降：短期下降趋势
  - 斜率变大：趋势加速
  - 斜率变小：趋势减缓或反转
- **金叉**（MA5 上穿 MA20）：history 序列中 MA5 从低于 MA20 变为高于 MA20，买入信号
- **死叉**（MA5 下穿 MA20）：history 序列中 MA5 从高于 MA20 变为低于 MA20，卖出信号

### 4.2 动能指标（MACD、KDJ、RSI）

**MACD**：
- **当前状态**：
  - DIF > DEA：看涨状态
  - DIF < DEA：看跌状态
  - MACD > 0：上涨动能（柱状图为正）
  - MACD < 0：下跌动能（柱状图为负）
- **趋势与交叉**（基于 history 序列）：
  - **金叉**：DIF 上穿 DEA，买入信号
  - **死叉**：DIF 下穿 DEA，卖出信号
  - **背离**：
    - 顶背离：价格创新高但 DIF 未创新高，看跌
    - 底背离：价格创新低但 DIF 未创新低，看涨

**KDJ**：
- **当前状态**：
  - K > D：看涨/强势区域
  - K < D：看跌/弱势区域
  - K > 80：超买风险区
  - K < 20：超卖机会区
  - J > 100：极端超买，警惕回调
  - J < 0：极端超卖，可能反弹
- **趋势判断**（基于 history 序列）：
  - K 线上升：动能增强
  - K 线下降：动能减弱
  - K-D 差值扩大：趋势强化

**RSI**：
- **当前状态**：
  - RSI > 70：超买
  - RSI < 30：超卖
  - RSI 50 为多空分界
  - RSI 介于 30-70：正常波动区间
- **趋势判断**（基于 history 序列）：
  - RSI 上升趋势：多头增强
  - RSI 下降趋势：空头增强
  - **背离**：
    - 顶背离：价格创新高但 RSI 未创新高，看跌
    - 底背离：价格创新低但 RSI 未创新低，看涨

### 4.3 波动指标（BOLL）

**当前价格位置**：
- **上轨上方**：强势突破，注意回调风险
- **中轨附近**：震荡整理
- **下轨下方**：弱势下跌，关注反弹机会

**带宽变化**（基于 history 序列）：
- **带宽计算**：(上轨 - 下轨) / 中轨 × 100%
- **收窄**：带宽持续缩小，预示即将突破
- **扩张**：带宽持续扩大，趋势形成中
- **挤压**：带宽处于历史低位，变盘在即

### 4.4 量价关系（基于 volume history）

**量能状态**：
- **放量**：成交量 > 5 日均量，关注突破有效性
- **缩量**：成交量 < 5 日均量，关注变盘信号
- **量能比**：当日成交量 / 5 日均量

**量价配合**：
- **量增价涨**：健康上涨
- **量增价跌**：抛压加重
- **量缩价涨**：上涨乏力
- **量缩价跌**：空头衰竭
- **量价背离**：价格创新高/低但成交量未配合，警惕反转

### 4.5 日内分析（基于实时行情）

**K线形态**：
- **阳线**（收盘 > 开盘）：多头占优
- **阴线**（收盘 < 开盘）：空头占优
- **光头阳线**（收盘 = 最高）：强势上涨
- **光脚阴线**（收盘 = 最低）：强势下跌

**日内波动**：
- **振幅** = (最高 - 最低) / 昨收 × 100%
- 振幅 > 5%：剧烈波动
- 振幅 2-5%：正常波动
- 振幅 < 2%：窄幅震荡

## 五、评级与风险评估

### 5.1 评级标准

基于技术指标共识和新闻情绪：

| 评级 | 条件 |
|------|------|
| **买入** | MA 多头排列 AND（MACD 金叉 OR RSI 超卖回升 OR 突破 BOLL 上轨放量）AND 无重大利空 |
| **增持** | 至少 2 个趋势/动能指标看涨（MA 上升/DIF>DEA/RSI 中位向上）AND 无明确利空 |
| **持有** | 指标多空交织，方向不明或震荡整理 |
| **减持** | 至少 2 个趋势/动能指标看弱 OR 跌破关键支撑 |
| **卖出** | MA 空头排列 AND（MACD 死叉 OR RSI 超买回落 OR 跌破 BOLL 下轨放量）OR 重大利空 |

**注：**
- 重大新闻事件权重 > 技术指标
- 量价配合是验证信号的重要依据
- 背离信号（顶背离/底背离）优先于单一指标判断

### 5.2 风险提示
根据以下因素生成相关风险提示：
- **技术面风险**：
  - RSI 超买（>70）/超卖（<30）
  - BOLL 极端位置（突破上轨或跌破下轨）
  - KDJ 极端值（J > 100 或 J < 0）
  - 顶背离/底背离（价格与指标背离）
  - 量价背离（价格创新高/低但成交量未配合）
  - 日内振幅过大（>5%）
- **新闻面风险**：政策变化、业绩预警、法律诉讼、监管风险
- **市场风险**：大盘走势、行业波动、汇率/利率影响

## 六、输出模板

AI 必须严格按以下结构输出 Markdown 报告，**必须包含日线和5分钟两个周期的技术分析**：

```markdown
# 股票分析报告｜{股票代码} {股票名称}

## 一、摘要
| 维度 | 内容 |
|---|---|
| 当前价格 | {price} |
| 当日涨跌 | {change}（{pct_change}%） |
| 评级 | {rating} |
| 操作建议 | {one_line_conclusion} |

## 二、行情与走势
| 指标 | 数值 |
|---|---|
| 开盘/最高/最低 | {open} / {high} / {low} |
| 昨收 | {prev_close} |
| 成交量 | {volume} |
| 成交额 | {amount} |

## 三、日线技术分析
### 3.1 趋势类
| 指标 | 数值 | 解读 |
|---|---|---|
| MA5/10/20 | {ma5} / {ma10} / {ma20} | {ma_note} |
| MA60/120 | {ma60} / {ma120} | {ma_long_note} |

### 3.2 动能类
| 指标 | 数值 | 解读 |
|---|---|---|
| MACD | DIF {dif}, DEA {dea}, MACD {macd} | {macd_note} |
| KDJ | K {k}, D {d}, J {j} | {kdj_note} |
| RSI | RSI6 {rsi6}, RSI12 {rsi12}, RSI24 {rsi24} | {rsi_note} |

### 3.3 波动类
| 指标 | 数值 | 解读 |
|---|---|---|
| BOLL | 上 {boll_upper} / 中 {boll_mid} / 下 {boll_lower} | {boll_note} |

## 四、5分钟短线分析
### 4.1 趋势类
| 指标 | 数值 | 解读 |
|---|---|---|
| MA5/10/20 | {5m_ma5} / {5m_ma10} / {5m_ma20} | {5m_ma_note} |

### 4.2 动能类
| 指标 | 数值 | 解读 |
|---|---|---|
| MACD | DIF {5m_dif}, DEA {5m_dea}, MACD {5m_macd} | {5m_macd_note} |
| KDJ | K {5m_k}, D {5m_d}, J {5m_j} | {5m_kdj_note} |

### 4.3 日内走势解读
{intraday_analysis}

## 五、资讯与影响
| 时间 | 来源 | 主题标签 | 标题 | 摘要 | 影响判断 |
|---|---|---|---|---|---|
| {time} | {source} | {topic_tag} | {title_cn} | {summary_cn} | {impact} |

## 六、综合判断
### 6.1 技术面总结
{technical_summary}

### 6.2 结论与风险提示
| 项目 | 内容 |
|---|---|
| 投资建议 | {investment_advice} |
| 风险提示 | {risk_note} |
```

**注：**
- 第三部分「日线技术分析」基于日K线（scale=240）
- 第四部分「5分钟短线分析」基于5分钟K线（scale=5），用于日内走势判断
- 第五部分「资讯与影响」仅在触发新闻搜索时包含。如触发但无新闻，显示：`| - | - | - | 过去24小时无相关新闻 | - | - |`
