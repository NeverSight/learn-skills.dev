---
name: browse-robonet-data
description: "Fast, low-cost exploration of Robonet trading resources. Browse 8 data tools to explore available trading pairs, technical indicators, Allora ML topics, existing strategies, and backtest results. All tools execute in <1 second with minimal cost (free to $0.001). Use this skill first before building or testing strategies to understand what resources are available."
persona: ["analyst", "researcher", "developer", "trader"]
risk_level: "none"
cost_profile: "Free to $0.001 per query"
tools:
  - mcp__workbench__get_all_strategies
  - mcp__workbench__get_strategy_code
  - mcp__workbench__get_strategy_versions
  - mcp__workbench__get_all_symbols
  - mcp__workbench__get_all_technical_indicators
  - mcp__workbench__get_allora_topics
  - mcp__workbench__get_data_availability
  - mcp__workbench__get_latest_backtest_results
related_skills:
  next_steps:
    - design-trading-strategies
    - build-trading-strategies
    - test-trading-strategies
---

# Browse Robonet Data

## Quick Start

This skill provides fast, read-only access to explore Robonet's trading resources before building anything. All tools execute in under 1 second and cost little to nothing.

**Load the tools first**:
```
Use MCPSearch to select: mcp__workbench__get_all_symbols
Use MCPSearch to select: mcp__workbench__get_all_technical_indicators
Use MCPSearch to select: mcp__workbench__get_data_availability
```

**Common starting pattern**:
```
1. get_all_symbols → See available trading pairs (BTC-USDT, ETH-USDT, etc.)
2. get_all_technical_indicators → Browse 170+ indicators (RSI, MACD, Bollinger Bands)
3. get_data_availability → Check data ranges before backtesting
```

**When to use this skill**:
- Start every workflow by exploring available resources
- Check data availability before building strategies
- Review existing strategies and their performance
- Understand what ML predictions are available (Allora topics)
- Audit recent backtest results

## Available Tools (8)

### Strategy Exploration Tools

**`get_all_strategies`** - List your trading strategies with optional backtest results
- **Parameters**:
  - `include_latest_backtest` (optional, boolean): Include latest backtest summaries
- **Returns**: List of strategies with names, components, and optionally performance metrics
- **Pricing**: $0.001
- **Use when**: Finding existing strategies to review, enhance, or compare

**`get_strategy_code`** - View Python source code of a strategy
- **Parameters**:
  - `strategy_name` (required, string): Name of the strategy
- **Returns**: Complete Python source code
- **Pricing**: Free
- **Use when**: Learning from existing strategies, reviewing before modification, debugging

**`get_strategy_versions`** - Track strategy evolution across versions
- **Parameters**:
  - `base_strategy_name` (required, string): Base name without version suffixes
- **Returns**: List of all versions with creation dates and modification history
- **Pricing**: $0.001
- **Use when**: Understanding how a strategy evolved, comparing versions, auditing changes

### Market Data Tools

**`get_all_symbols`** - List tradeable pairs on Hyperliquid Perpetual
- **Parameters**:
  - `exchange` (optional, string): Filter by exchange name
  - `active_only` (optional, boolean): Only return active symbols (default: true)
- **Returns**: List of symbols with exchange, symbol name, active status, backfill status
- **Pricing**: $0.001
- **Use when**: Choosing which assets to trade, checking what's available before building strategies

**`get_data_availability`** - Check data ranges before backtesting
- **Parameters**:
  - `data_type` (optional, string): Type of data (crypto, polymarket, all)
  - `symbols` (optional, array): Specific crypto symbols to check
  - `exchange` (optional, string): Filter crypto by exchange
  - `asset` (optional, string): Filter Polymarket by asset
  - `include_resolved` (optional, boolean): Include resolved Polymarket markets
  - `only_with_data` (optional, boolean): Only show items with available data
- **Returns**: Data availability with date ranges, candle counts, backfill status
- **Pricing**: $0.001
- **Use when**: Before backtesting (verify sufficient data), choosing test date ranges, checking market coverage

### Indicator & ML Tools

**`get_all_technical_indicators`** - Browse 170+ indicators available in Jesse framework
- **Parameters**:
  - `category` (optional, string): Filter by category (momentum, trend, volatility, volume, overlap, oscillators, cycle, all)
- **Returns**: List of indicators with names, categories, and parameters
- **Pricing**: $0.001
- **Use when**: Exploring indicators for strategy ideas, checking parameter requirements, learning what's available

**`get_allora_topics`** - List Allora Network ML prediction topics
- **Parameters**: None
- **Returns**: List of topics with asset names, network IDs, prediction horizons, and prediction types
- **Pricing**: $0.001
- **Use when**: Planning ML enhancement, checking prediction coverage, understanding available horizons (5m, 8h, 24h, 1 week)

### Backtest Results Tool

**`get_latest_backtest_results`** - View recent backtest performance
- **Parameters**:
  - `strategy_name` (optional, string): Filter by strategy name
  - `limit` (optional, integer, 1-100): Number of results (default: 10)
  - `include_equity_curve` (optional, boolean): Include equity curve timeseries
  - `equity_curve_max_points` (optional, integer, 50-1000): Maximum points for equity curve
- **Returns**: List of backtest records with metrics (Sharpe, drawdown, win rate, total return, profit factor)
- **Pricing**: Free
- **Use when**: Checking if backtest already exists, comparing strategy performance, avoiding redundant backtests

## Core Concepts

### Symbol Coverage

**Crypto Perpetuals** (Hyperliquid):
- **Major pairs**: BTC-USDT, ETH-USDT, SOL-USDT, NEAR-USDT
- **Data history**: BTC-USDT and ETH-USDT have longest history (2020-present)
- **Typical range**: Most symbols have 6-24 months of data
- **Data quality**: 1-minute candles available for all symbols

**Best practices**:
- Use `get_all_symbols` to see complete list
- Check `get_data_availability` for specific symbol history
- BTC-USDT and ETH-USDT recommended for initial strategy development (longest history)

### Technical Indicators

**170+ indicators organized by category**:

- **Momentum** (16 indicators): RSI, MACD, Stochastic, ADX, CCI, MFI, ROC, Williams %R, Ultimate Oscillator, etc.
- **Trend** (12 indicators): EMA, SMA, DEMA, TEMA, WMA, Supertrend, Parabolic SAR, VWAP, HMA, etc.
- **Volatility** (8 indicators): Bollinger Bands, ATR, Keltner Channels, Donchian Channels, Standard Deviation, etc.
- **Volume** (10 indicators): OBV, Volume Profile, Chaikin Money Flow, Volume Weighted indicators, etc.
- **Overlap** (8 indicators): Various moving averages and envelopes
- **Oscillators** (6 indicators): Specialized momentum oscillators
- **Cycle** (4 indicators): Market cycle detection indicators

**How to use**:
```
1. get_all_technical_indicators(category="momentum") → Browse momentum indicators
2. Pick indicators for your strategy concept
3. Reference indicators in strategy description when building
```

**Note**: All indicators are from the Jesse framework (`jesse.indicators`). Use exact names when creating strategies.

### Allora Network ML Predictions

**Prediction Coverage**:
- **Assets**: BTC, ETH, SOL, NEAR
- **Horizons**: 5 minutes, 8 hours, 24 hours, 1 week
- **Prediction types**:
  - Log return (percentage change prediction)
  - Absolute price (future price prediction)
- **Networks**:
  - Mainnet: 10 production topics
  - Testnet: 26 experimental topics

**Topic structure**:
```
Asset: BTC
Horizon: 24h
Type: Log return
Network: mainnet
```

**How to use**:
```
1. get_allora_topics() → See all available predictions
2. Match prediction horizon to your strategy timeframe
3. Use enhance_with_allora (from improve-trading-strategies skill) to integrate predictions
```

**Best practices**:
- Match prediction horizon to strategy timeframe (don't use 5m predictions for daily strategy)
- Mainnet topics are production-ready, testnet topics are experimental
- Check topic availability before planning ML enhancement

### Backtest Result Interpretation

**Key Metrics**:

**Sharpe Ratio** (risk-adjusted return):
- **>2.0**: Excellent performance
- **1.0-2.0**: Good performance
- **0.5-1.0**: Acceptable performance
- **<0.5**: Poor performance

**Max Drawdown** (largest peak-to-trough decline):
- **<10%**: Conservative risk profile
- **10-20%**: Moderate risk profile
- **20-40%**: Aggressive risk profile
- **>40%**: Very risky (reconsider strategy)

**Win Rate** (percentage of profitable trades):
- **45-65%**: Realistic for most strategies
- **>70%**: Suspicious (possible overfitting or unrealistic fills)
- **<40%**: Needs improvement

**Profit Factor** (gross profit / gross loss):
- **>2.0**: Excellent
- **1.5-2.0**: Good
- **1.2-1.5**: Acceptable
- **<1.2**: Marginal (risky to deploy)

**How to use backtest results**:
```
1. get_latest_backtest_results(strategy_name="MyStrategy") → Check recent tests
2. Review metrics against benchmarks above
3. If metrics good: consider deployment
4. If metrics poor: refine strategy or try different approach
```

## Best Practices

### Exploration Workflow

**Start every strategy development with data exploration**:

```
1. Explore available assets
   get_all_symbols() → What can I trade?
   get_data_availability(data_type="crypto") → How much history?

2. Understand available tools
   get_all_technical_indicators(category="momentum") → What indicators?
   get_allora_topics() → What ML predictions available?

3. Review existing work
   get_all_strategies(include_latest_backtest=true) → What's already built?
   get_strategy_code(strategy_name="Existing") → Learn from existing code

4. Plan your strategy
   → Use insights from exploration to inform strategy design
```

### Data Availability Checks

**Always verify sufficient data before backtesting**:

```
Problem: Backtest fails with "No data available"
Solution:
  1. get_data_availability(symbols=["BTC-USDT"], only_with_data=true)
  2. Check date range returned
  3. Use date range within available data for backtest
```

**Minimum data requirements**:
- **Quick test**: 1-3 months (limited validation)
- **Standard test**: 6-12 months (recommended minimum)
- **Robust test**: 12-24 months (ideal for validation)

### Cost Optimization

**All tools in this skill are cheap (free to $0.001)**:
- Use liberally during exploration
- No need to batch queries or optimize calls
- Better to over-explore than under-explore

**Cost-saving pattern**:
```
1. Browse data (this skill, <$0.01) → Explore thoroughly
2. Generate ideas (design-trading-strategies, $0.05-$1.00) → Cheap exploration
3. Build strategy (build-trading-strategies, $1-$4.50) → Expensive, be sure first
```

Spending 2-3 minutes exploring data (costs <$0.01) can save dollars in wasted strategy generation.

### Learning from Existing Strategies

**Use existing strategies as templates**:

```
1. get_all_strategies(include_latest_backtest=true)
   → Find high-performing strategies (Sharpe >1.5)

2. get_strategy_code(strategy_name="HighPerformer")
   → Study the code structure

3. Identify patterns:
   - How are entry conditions structured?
   - What indicators are used?
   - How is position sizing calculated?
   - How is risk management implemented?

4. Apply learnings to new strategy design
```

### Indicator Research

**Find the right indicators for your strategy concept**:

```
Strategy Type → Indicator Categories to explore:
- Trend Following → trend, momentum
- Mean Reversion → oscillators, momentum
- Breakout → volatility, volume
- Scalping → momentum, volume
- Swing Trading → trend, overlap
```

**Example exploration**:
```
Building a mean reversion strategy:
1. get_all_technical_indicators(category="oscillators") → See oscillators
2. get_all_technical_indicators(category="momentum") → See momentum indicators
3. Pick RSI (overbought/oversold) + Bollinger Bands (deviation from mean)
4. Use these indicator names when building strategy
```

## Common Workflows

### Workflow 1: Pre-Strategy Exploration

**Goal**: Understand what's available before building anything

```
1. get_all_symbols()
   → Review available trading pairs
   → Note which symbols interest you

2. get_data_availability(symbols=["BTC-USDT", "ETH-USDT"], only_with_data=true)
   → Check data ranges for chosen symbols
   → Verify sufficient history (6+ months preferred)

3. get_all_technical_indicators(category="all")
   → Browse all 170+ indicators
   → Note which indicators fit your strategy idea

4. get_allora_topics()
   → See ML prediction coverage
   → Check if your asset has predictions available
   → Note prediction horizons

5. Ready to build:
   → If exploring ideas: Use design-trading-strategies skill
   → If ready to code: Use build-trading-strategies skill
```

**Cost**: ~$0.005 (essentially free)

### Workflow 2: Strategy Audit

**Goal**: Review existing strategies and their performance

```
1. get_all_strategies(include_latest_backtest=true)
   → See all strategies with performance data

2. Identify interesting strategies:
   → High Sharpe ratio (>1.5)
   → Acceptable drawdown (<20%)
   → Realistic win rate (45-65%)

3. get_strategy_code(strategy_name="TopPerformer")
   → Review implementation details
   → Understand why it performs well

4. get_strategy_versions(base_strategy_name="TopPerformer")
   → See how strategy evolved
   → Identify what improvements were made

5. Apply learnings:
   → Use as template for new strategies
   → Or enhance further with improve-trading-strategies skill
```

**Cost**: Free to $0.003

### Workflow 3: Data Coverage Check

**Goal**: Verify data availability before backtesting

```
1. Choose your strategy parameters:
   Symbol: BTC-USDT
   Timeframe: 1h
   Test period: 6 months

2. get_data_availability(symbols=["BTC-USDT"], only_with_data=true)
   Returns: "BTC-USDT available from 2020-01-01 to 2025-02-02"

3. Verify coverage:
   ✓ Has 6+ months of data
   ✓ Covers desired test period
   ✓ Ready to backtest

4. If insufficient data:
   → Try shorter test period
   → Or choose different symbol (BTC-USDT and ETH-USDT have longest history)

5. Proceed to testing:
   → Use test-trading-strategies skill to run backtest
```

**Cost**: $0.001

### Workflow 4: Indicator Research

**Goal**: Find the right indicators for your strategy concept

```
Strategy Concept: Mean reversion on cryptocurrency

1. get_all_technical_indicators(category="momentum")
   → Browse momentum indicators (RSI, Stochastic, etc.)

2. get_all_technical_indicators(category="volatility")
   → Browse volatility indicators (Bollinger Bands, ATR, etc.)

3. Select indicators for mean reversion:
   → RSI (identify overbought/oversold)
   → Bollinger Bands (measure deviation from mean)
   → ATR (position sizing based on volatility)

4. Note exact indicator names:
   → "RSI" (not "rsi" or "RelativeStrengthIndex")
   → "BollingerBands" (not "BB" or "bollinger")
   → "ATR" (not "AverageTrueRange")

5. Use exact names in strategy description:
   → When using build-trading-strategies skill
   → Reference indicators precisely: "Use RSI with period 14"
```

**Cost**: $0.002

## Advanced Usage

### Filtering and Optimization

**Efficient querying**:
```
# Get only active symbols
get_all_symbols(active_only=true)

# Filter indicators by category
get_all_technical_indicators(category="momentum")

# Check specific symbols only
get_data_availability(symbols=["BTC-USDT", "ETH-USDT"], only_with_data=true)

# Limit backtest results
get_latest_backtest_results(limit=5)
```

### Backtest Result Analysis

**Detailed equity curve analysis**:
```
get_latest_backtest_results(
    strategy_name="MyStrategy",
    include_equity_curve=true,
    equity_curve_max_points=500
)
```

Returns equity curve data for visualizing strategy performance over time.

**Use cases**:
- Identify periods of strong/weak performance
- Detect regime changes (strategy works in trending vs ranging markets)
- Compare multiple strategies visually

### Cross-Asset Research

**Compare data availability across assets**:
```
1. get_data_availability(data_type="crypto", only_with_data=true)
   → See all crypto pairs with data

2. Compare:
   - Which symbols have longest history?
   - Which symbols have most recent backfills?
   - Which timeframes are well-covered?

3. Choose optimal symbols for strategy development:
   → BTC-USDT, ETH-USDT: Longest history, most reliable
   → Altcoins: Shorter history, higher risk, potentially higher returns
```

## Troubleshooting

### "No Strategies Found"

**Issue**: `get_all_strategies` returns empty list

**Solutions**:
- Strategies are linked to your API key's wallet
- Ensure you're using the correct API key
- If new account, you haven't created strategies yet (use build-trading-strategies skill to create first strategy)

### "Symbol Not Found"

**Issue**: `get_data_availability` doesn't show expected symbol

**Solutions**:
- Use `get_all_symbols()` to see complete list of available symbols
- Check spelling (BTC-USDT not BTC-USD or BTCUSDT)
- Some symbols may not have data backfilled yet (check `active_only=false` to see inactive symbols)

### "No Indicator Matches Description"

**Issue**: Can't find indicator you're looking for

**Solutions**:
- Use `get_all_technical_indicators(category="all")` to browse complete list
- Search for similar names (RSI vs RelativeStrengthIndex)
- Check category filter (momentum indicator won't show if filtering by trend)
- Jesse framework uses specific names - use exact names returned by tool

### "Backtest Results Missing"

**Issue**: `get_latest_backtest_results` doesn't show expected backtest

**Solutions**:
- Check strategy name spelling (case-sensitive)
- Backtest may still be running (wait 20-60 seconds)
- Backtest may have failed (check for error messages)
- Use `limit` parameter to retrieve more results (default is 10)

## Next Steps

After exploring data with this skill:

**Generate strategy ideas**:
- Use `design-trading-strategies` skill to generate AI-powered strategy concepts
- Cost: $0.05-$1.00 per idea generation (cheapest AI tool)
- Best when: You want to explore creative concepts before committing to development

**Build strategies directly**:
- Use `build-trading-strategies` skill to generate complete strategy code
- Cost: $1.00-$4.50 per strategy (most expensive AI tool)
- Best when: You already know what you want to build

**Test existing strategies**:
- Use `test-trading-strategies` skill to backtest strategies
- Cost: $0.001 per backtest
- Best when: You have strategy code and want to validate performance

**Improve strategies**:
- Use `improve-trading-strategies` skill to refine, optimize, or enhance with ML
- Cost: $0.50-$4.00 per operation
- Best when: You have an existing strategy that needs improvement

**Prediction market trading**:
- Use `trade-prediction-markets` skill for Polymarket YES/NO token strategies
- Cost: $0.001-$4.50 depending on operation
- Best when: You want to trade on real-world events (politics, economics, sports)

## Summary

This skill provides **fast, cheap, read-only access** to Robonet's trading resources:

- **8 data tools** covering strategies, symbols, indicators, ML topics, and backtest results
- **<1 second execution** for all tools
- **Free to $0.001 cost** (essentially free to explore)
- **Zero risk** (read-only operations, no modifications or executions)

**Core principle**: Explore thoroughly before building. Spending 2-3 minutes browsing data (costs <$0.01) can save dollars in wasted strategy generation and prevent costly mistakes.

**Best practice**: Start every workflow with this skill, then progress to design → build → improve → test → deploy based on your findings.
