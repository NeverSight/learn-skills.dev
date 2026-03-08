---
name: tradingview-quantitative
description: >
  Professional quantitative investment analysis system based on TradingView data.
  Provides intelligent stock screening, technical pattern recognition, market review,
  risk management, and event-driven analysis with multi-factor scoring and trading strategies.
---

# Quantitative Investment Analysis Expert

Professional quantitative investment analysis system based on TradingView MCP tools providing insights and decision recommendations.

## Core Rules

### Metadata First Principle

**Before calling `tradingview_get_leaderboard`, you must first call `tradingview_get_metadata` to get parameter values:**

1. `type='markets'` → Get `market_code` (required for stock leaderboard)
2. `type='tabs'` + `asset_type` → Get available `tab` values
3. `type='columnsets'` → Get available `columnset` values

Complete metadata dictionary (market codes, tabs, columnsets, exchanges) see `references/api-documentation.md`.

### Tool Selection Quick Reference

| Need | Tool | Key Parameters |
|------|------|---------|
| Search instruments | `search_market` | query, filter(stock/crypto/forex...) |
| Real-time quotes | `get_quote` / `get_quote_batch` | symbol, session |
| K-line data | `get_price` / `get_price_batch` | symbol, timeframe(1/5/15/30/60/240/D/W/M), range(max 500) |
| Technical analysis | `get_ta` | symbol, **include_indicators=true for detailed indicators** |
| Leaderboard | `get_leaderboard` | asset_type, tab, market_code, **columnset**(overview/performance/valuation/dividends/profitability/income_statement/balance_sheet/cash_flow/technical) |
| News | `get_news` / `get_news_detail` | market_country, lang(zh-Hans/en/ja), symbol |
| Economic calendar | `get_calendar` | type(economic/earnings/revenue/ipo), from/to(Unix seconds), market |
| Metadata | `get_metadata` | type(markets/tabs/columnsets/languages/exchanges) |

## Workflows

For detailed steps, see `workflows/ directory:

### Core Analysis
- **`deep-stock-analysis.md`** - Deep individual stock analysis (combine quote + price multi-timeframe + ta detailed indicators + news + calendar)
- **`smart-screening.md`** - Smart stock screening (leaderboard multi-columnset + ta + price)
- **`fundamental-screening.md`** - Fundamental screening (leaderboard valuation/profitability/dividends columnsets)
- **`pattern-recognition.md`** - Technical pattern recognition (price + ta + pattern-library reference)
- **`multi-timeframe-analysis.md`** - Multi-timeframe trend confirmation (price D/W/M + ta multi-period)

### Market & Sectors
- **`market-review.md`** - Market review (leaderboard gainers/losers + news)
- **`sector-rotation.md`** - Sector rotation analysis (leaderboard performance columnset + multi-sector comparison)
- **`news-briefing.md`** - Financial news briefing (news + news_detail, supports multi-country multi-language)

### Risk & Events
- **`risk-assessment.md`** - Risk assessment (price historical data + quote + volatility calculation)
- **`event-analysis.md`** - Event-driven analysis (calendar + news + search)
- **`calendar-tracking.md`** - Calendar event tracking (calendar 4 types)

### Quotes & Search
- **`symbol-search.md`** - Instrument search (search_market)
- **`realtime-monitor.md`** - Real-time quote monitoring (quote / quote_batch)
- **`multi-symbol-analysis.md`** - Multi-instrument batch analysis (quote_batch + price_batch + ta)
- **`exchange-overview.md`** - Exchange overview (metadata exchanges/markets/tabs)

## Reference Knowledge Base

For professional methodologies and data dictionaries, see `references/` directory:

- **`api-documentation.md`** - Complete TradingView API documentation (endpoints, parameters, metadata dictionary: market codes/tabs/columnsets/exchanges, search keywords: `Market Codes`, `Asset Types and Tabs`, `Column Sets`, `Supported Languages`)
- **`mcp-tools-guide.md`** - MCP tools usage guide (tool combination patterns, metadata-first rules, best practices for various scenarios)
- **`technical-analysis.md`** - Technical analysis methodology (comprehensive scoring model, trend/momentum/pattern/support-resistance scoring, search keywords: `comprehensive scoring model`, `RSI`, `MACD`, `support resistance`)
- **`pattern-library.md`** - Pattern recognition library (classic patterns, recognition algorithms, success rate statistics, search keywords: `double bottom`, `head and shoulders`, `triangle`, `flag`, `candlestick patterns`)
- **`risk-management.md`** - Risk management system (position management, stop-loss strategies, portfolio management, search keywords: `Kelly formula`, `volatility`, `stop loss take profit`, `batch position building`)
- **`china-a-stock-examples.md`** - China A-share practical cases (stock screening, pattern analysis, market review output examples)

## Disclaimer

The analysis and recommendations provided by this Skill are **for reference only** and do not constitute investment advice. Investing involves risks; decisions should be made cautiously.
