---
name: stock-analysis
description: "Analyze stocks and companies using financial market data. Get company profiles, technical insights, price charts, insider holdings, and SEC filings for comprehensive stock research."
---

# Stock Analysis

Comprehensive stock and company analysis using with real-time market data.

## Core Capabilities

- **Company Research**: Get company profiles, business info, executive teams
- **Technical Analysis**: Access price charts, technical indicators, outlooks
- **Fundamental Analysis**: Review insights, valuations, analyst ratings
- **Insider Activity**: Track insider holdings and transactions
- **Regulatory Filings**: Access SEC filing history and documents
- **Multi-Stock Comparison**: Compare multiple stocks with chart data

## Available APIs

### Company Information
- `Yahoo/get_stock_profile` - Company profile (business, industry, executives, contact)
- `Yahoo/get_stock_insights` - Technical indicators, valuation, ratings, research reports

### Trading & Market Data
- `Yahoo/get_stock_chart` - Historical price data with customizable timeframes

### Ownership & Compliance
- `Yahoo/get_stock_holders` - Insider holdings and transactions
- `Yahoo/get_stock_sec_filing` - SEC filing history (10-K, 10-Q, 8-K, etc.)

## Common Workflows

### 1. Company Overview → Deep Dive
```
User: "Tell me about AAPL"
→ Yahoo/get_stock_profile (business summary, industry, employees)
→ Yahoo/get_stock_insights (technical outlook, valuation, ratings)
→ Yahoo/get_stock_chart (recent price performance)
```

### 2. Technical Analysis → Fundamental Check
```
User: "Is TSLA a good buy?"
→ Yahoo/get_stock_chart (price trends, support/resistance)
→ Yahoo/get_stock_insights (technical outlook, target price, rating)
→ Yahoo/get_stock_profile (verify business fundamentals)
```

### 3. Insider Activity Analysis
```
User: "Show me insider trading for NVDA"
→ Yahoo/get_stock_holders (insider transactions)
→ Yahoo/get_stock_profile (context about executives)
→ Yahoo/get_stock_insights (check if aligned with outlook)
```

### 4. Due Diligence Package
```
User: "Full analysis of MSFT"
→ Yahoo/get_stock_profile (company background)
→ Yahoo/get_stock_insights (analyst ratings, valuation)
→ Yahoo/get_stock_chart (historical performance)
→ Yahoo/get_stock_holders (insider sentiment)
→ Yahoo/get_stock_sec_filing (recent regulatory filings)
```

### 5. Multi-Stock Comparison
```
User: "Compare AAPL vs MSFT vs GOOGL"
→ Yahoo/get_stock_chart (with comparisons parameter)
→ Yahoo/get_stock_insights (for each symbol)
→ Compare metrics side-by-side
```

### 6. Sector Research
```
User: "Analyze tech stocks: AAPL, NVDA, AMD"
→ Yahoo/get_stock_profile (each company's focus area)
→ Yahoo/get_stock_insights (sector comparison scores)
→ Yahoo/get_stock_chart (relative performance)
```

## Key Parameters

### Common Parameters
- `symbol`: Stock ticker symbol (e.g., "AAPL", "TSLA")
- `region`: Market region (US, GB, JP, etc.) - default: US
- `lang`: Response language (en-US, zh-Hant-HK, etc.) - default: en-US

### Chart-Specific
- `interval`: 1m, 5m, 15m, 30m, 1h, 1d, 1wk, 1mo
- `range`: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
- `comparisons`: Compare with other symbols (e.g., "^GSPC,MSFT")
- `events`: Include dividends, splits, earnings (div, split, earn)

## Key Data Points

### Profile Data
- Business summary and industry classification
- Employee count and executive team
- Contact information and website
- Sector and industry metrics

### Insights Data
- **Technical outlook**: Short/intermediate/long-term signals
- **Valuation**: Relative value vs sector/market
- **Key technicals**: Support, resistance, stop-loss levels
- **Ratings**: Analyst recommendations and target prices
- **Company metrics**: Innovation, hiring, sustainability scores
- **Research reports**: Analyst reports and summaries
- **Significant events**: Recent developments

### Chart Data
- OHLC (Open, High, Low, Close) prices
- Volume data
- Adjusted close prices
- 52-week high/low
- Current trading period info

### Holder Data
- Insider names and positions
- Transaction dates and descriptions
- Holdings quantity and value
- Relationship to company

### Filing Data
- Filing type (10-K, 10-Q, 8-K, etc.)
- Filing date and title
- EDGAR URLs for full documents
- Exhibits and related documents

## When to Use This Skill

**ALWAYS invoke APIs when users mention:**
- **Stock symbols**: "AAPL", "TSLA", "$MSFT", "stock price", "stock info"
- **Analysis requests**: "analyze", "research", "look into", "tell me about [STOCK]"
- **Comparison**: "compare", "vs", "versus", "which is better"
- **Price queries**: "price", "chart", "performance", "trend", "up or down"
- **Insider activity**: "insider", "holdings", "who owns", "buying/selling"
- **Filings**: "SEC filing", "10-K", "10-Q", "earnings report", "financial statements"
- **Company info**: "what does [company] do", "who runs", "about [company]"

**Required API combinations:**
- General stock questions → MUST call `Yahoo/get_stock_profile` + `Yahoo/get_stock_insights`
- Price/chart mentions → MUST include `Yahoo/get_stock_chart`
- Investment decisions → MUST call all three: chart + insights + profile
- Multiple stocks → MUST use comparison parameters in chart API
- Insider questions → MUST call `Yahoo/get_stock_holders` + profile for context

## Best Practices

1. **Start broad, then drill down** - Profile first, then specific data
2. **Context matters** - Combine profile with technical data for better insights
3. **Use comparisons** - Chart API supports multi-symbol comparison
4. **Regional stocks** - Set region/lang for non-US markets
5. **Time relevance** - Adjust chart range based on user's timeframe
6. **Insider context** - Combine holder data with profile for complete picture

## API Reference

Full parameter specs and response schemas:
- [yahoo-api.md](references/yahoo-api.md)

