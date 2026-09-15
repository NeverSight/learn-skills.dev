---
name: pineapple-stock-summary
description: Fetches real-time stock quotes, earnings info, and market news for a fixed ticker list (^VIX, ^TNX, QQQM, NVDA, AAPL, TSLA, AMD, MU, OXY, INTC, DRAM) and formats them into a structured Chinese summary. Use this whenever the user asks about "stock information", "today's stocks", "股票信息", "股市新闻", or "财报".
---

# Pineapple Stock Summary Workflow

When the user asks for stock information, their portfolio update, or market news, follow this workflow to provide a consistent summary.
You are strictly prohibited from replying in advance; you must wait until the data query is complete before responding.

## Tickers to Track
- ^VIX (CBOE Volatility Index / 标普恐慌指数)
- ^TNX (10-Year Treasury Note Yield / 美国10年期国债收益率)
- QQQM (Nasdaq 100 ETF)
- NVDA (NVIDIA)
- AAPL (Apple)
- TSLA (Tesla)
- AMD (Advanced Micro Devices)
- MU (Micron / Storage sector proxy)
- OXY (西方石油)
- INTC (英特尔)
- DRAM (DRAM)

## Step 1: Fetch Quotes via Script
Use the provided `scripts/get_stocks.py` to fetch stock data in one go instead of manually chaining quote lookups.
```bash
~/.hermes/skills/custom-skill/pineapple-stock-summary/scripts/get_stocks.py ^VIX ^TNX QQQM NVDA AAPL TSLA AMD MU OXY INTC DRAM
```
This returns a JSON array containing `price`, `dailyChange`, `weeklyChange`, and `monthlyChange` for each ticker. Note that for ^TNX, the "price" is actually the yield percentage (e.g., 4.25 means 4.25%).

## Step 2: Fetch Earnings Information
Use Hermes built-in web search instead of any external Tavily wrapper script.

Search for the upcoming earnings release dates for the companies in the tracked list that actually publish earnings (NVDA, AAPL, TSLA, AMD, MU, OXY, INTC).
If any of these companies released earnings yesterday or today, search specifically for that earnings report and summarize the key metrics (Revenue, EPS, Guidance) and the market reaction.

Recommended search patterns:
- `NVDA OR AAPL OR TSLA OR AMD OR MU OR OXY OR INTC next earnings date 2026`
- `[Ticker] earnings report summary [today/yesterday date]`
- `[Ticker] Q1 2026 earnings revenue EPS guidance`

Use `web_extract` on the most relevant result when you need more detail than the search snippet provides.

## Step 3: Fetch Market, Macro, and Geopolitical News
Use Hermes built-in `web_search` and `web_extract` tools directly. Do **not** call `tavily_news_fetcher.py` or rely on a separate Tavily API setup for this skill.

Search for:
1. Recent news impacting these specific stocks or sectors today.
2. Key news related to the broader technology sector and Nasdaq market trends.
3. Frontier technology news from major tech companies (e.g., AI advancements, new product launches).
4. The latest updates on **Federal Reserve interest rate decisions or expectations** (e.g., "Federal Reserve interest rate decisions 2026", "美联储利率决议 2026").
5. The latest **war / geopolitical conflict news** that could affect risk assets, oil, yields, semiconductors, or big tech sentiment (e.g., Middle East conflict, Ukraine war, US-China military tensions, shipping disruptions, sanctions, cyberattacks).

When querying war-related news, prioritize market-relevant angles instead of pure battlefield updates. Focus on whether the conflict is affecting:
- oil and energy prices
- Treasury yields / safe-haven flows
- semiconductor supply chains
- large-cap tech sentiment
- sanctions, export controls, shipping routes, or macro risk appetite

Recommended search patterns:
- `war news today market impact oil yields semiconductors`
- `Middle East conflict market impact tech stocks oil`
- `Ukraine war market impact commodities semiconductors`
- `US China tensions chips export controls market impact`
- `May 2026 stock market today Nasdaq Fed oil AI semiconductors`

Execution guidance:
- Prefer `web_search` first to gather current candidates.
- Use `web_extract` for 1-3 strongest sources when you need fuller context.
- Favor major financial outlets, company IR pages, Federal Reserve pages, and Reuters/CNBC/Yahoo Finance summaries when available.
- If a first query is weak, retry with narrower wording instead of stopping early.

## Step 4: Format the Output
Generate a detailed Chinese summary, not a terse morning brief. The emphasis should be on **why the market moved** and the **news drivers behind U.S. equities**, especially:
- war / geopolitics
- Federal Reserve / rates / yields / inflation
- frontier technology / AI / semiconductors / large-cap tech developments
- sector rotation and risk appetite

Do not collapse the response into a minimal template unless the user explicitly asks for a short version. By default, include enough detail for the user to understand the main market-moving narratives behind the quotes.

For the ^VIX (CBOE Volatility Index), evaluate the current `[Price]` and append its meaning based on this scale:
- **< 15**: 贪婪/极度乐观 (波动极低，市场情绪平稳，但需警惕高位回调)
- **15 - 20**: 正常/温和 (市场情绪健康，处于常态波动)
- **20 - 30**: 恐慌蔓延/高波动 (避险情绪升温，波动加剧，建议防守或分批定投)
- **> 30**: 极度恐慌 (危机模式，通常伴随暴跌，但往往也是长线资金的左侧“黄金坑”)

### 🌡️ 市场情绪 (Market Sentiment)：
- **^VIX (标普恐慌指数):** [Price]点 (单日: [+/-]% | 本周累计: [+/-]% | 本月累计: [+/-]%)
  👉 **当前情绪与策略:** [Insert the interpretation from the scale above]

  *(附：标普恐慌指数 VIX 情绪对照表)*
  - *< 15：贪婪/极度乐观 (波动极低，需警惕高位回调)*
  - *15 - 20：正常/温和 (市场情绪健康，常态波动)*
  - *20 - 30：恐慌蔓延/高波动 (避险情绪升温，建议防守或分批定投)*
  - *> 30：极度恐慌 (危机模式，通常伴随暴跌，左侧建仓黄金坑)*

### 🏦 宏观利率与美联储动态 (Macro & Fed Rates)：
- **^TNX (10年期美债收益率):** [Price]% (单日: [+/-]% | 本周累计: [+/-]% | 本月累计: [+/-]%)
  👉 **加息/降息预期:** [Summarize the latest news on Federal Reserve rate cuts/hikes, including current market probability, inflation data impact, or recent Fed speeches]

### 📊 你关注的股票与 ETF 最新行情：
- **[Ticker] ([Name]):** $[Price] (单日: [+/-]% | 本周累计: [+/-]% | 本月累计: [+/-]%)
...

### 📅 财报动态 (Earnings Updates)：
- **[Ticker 1]**: 📅 下一次财报预计：[Date]. (If reported recently: [Brief summary of the report: EPS, Revenue, and market reaction])
- **[Ticker 2]**: 📅 下一次财报预计：[Date].
...

### 📰 市场新闻与影响分析：
This section is important and should usually be the most informative part of the reply.

Cover the major market-moving narratives in a more detailed way:
1. **美联储 / 利率 / 通胀**: Explain what the latest macro news suggests for rate cuts, bond yields, liquidity, and valuation pressure on U.S. equities.
2. **战争 / 地缘政治**: Explain whether the latest conflict developments are pushing oil, defense sentiment, safe-haven flows, sanctions risk, shipping risk, or semiconductor supply-chain concerns.
3. **前沿科技 / AI / 半导体**: Summarize the latest important developments in AI, chips, hyperscalers, devices, or cloud capex, and explain which tickers or sectors benefit or suffer.
4. **个股 / 板块驱动**: Add any stock-specific or sector-specific news that materially explains the moves in NVDA, AAPL, TSLA, AMD, MU, OXY, INTC, or QQQM.

Use 3-5 numbered items when there is enough news flow. Each item should explain both:
- what happened
- why it matters for U.S. stocks

If there is a meaningful war or geopolitical development that day, you should explicitly include it in the final summary. If there is no material conflict update affecting markets, you may omit it rather than forcing a weak item.

Also, when relevant, explicitly connect the news to these market effects:
- Nasdaq / growth-stock valuation
- semiconductor and AI supply chains
- oil and energy equities
- Treasury yields and Fed expectations
- market risk appetite / volatility

(Do not include technical execution details in the final output, just the formatted summary.)