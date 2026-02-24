---
name: robonet-workbench
description: "Use Robonet's MCP server to build, backtest, optimize, and deploy trading strategies. Provides 24 specialized tools for crypto and prediction market trading: (1) Data tools for browsing strategies, symbols, indicators, Allora topics, and backtest results, (2) AI tools for generating strategy ideas and code, optimizing parameters, and enhancing with ML predictions, (3) Backtesting tools for testing strategy performance on historical data, (4) Prediction market tools for Polymarket trading strategies, (5) Deployment tools for live trading on Hyperliquid, (6) Account tools for credit management. Use when: building trading strategies, backtesting strategies, deploying trading bots, working with Hyperliquid or Polymarket, or enhancing strategies with Allora Network ML predictions."
---

# Robonet MCP Integration

## Overview

Robonet provides an MCP server that enables AI assistants to build, test, and deploy trading strategies. The server offers 24 tools organized into 6 categories: Data Access (8), AI-Powered Strategy Generation (6), Backtesting (2), Prediction Markets (3), Deployment (4), and Account Management (2).

## Quick Start

Load the required MCP tools before using them:

```
Use MCPSearch to select: mcp__workbench__get_all_symbols
Use MCPSearch to select: mcp__workbench__create_strategy
Use MCPSearch to select: mcp__workbench__run_backtest
```

After loading, call the tools directly to interact with Robonet.

## Tool Categories

### 1. Data Access Tools (Fast, <1s execution)

Browse available resources before building strategies:

- **`get_all_strategies`** - List your trading strategies with optional backtest results
- **`get_strategy_code`** - View Python source code of a strategy
- **`get_strategy_versions`** - Track strategy evolution across versions
- **`get_all_symbols`** - List tradeable pairs on Hyperliquid (BTC-USDT, ETH-USDT, etc.)
- **`get_all_technical_indicators`** - Browse 170+ indicators (RSI, MACD, Bollinger Bands, etc.)
- **`get_allora_topics`** - List Allora Network ML prediction topics
- **`get_data_availability`** - Check data ranges before backtesting
- **`get_latest_backtest_results`** - View recent backtest performance

**Pricing**: Most $0.001, some free. Use these liberally to explore.

**When to use**: Start every workflow by checking available symbols, indicators, or existing strategies before generating new code.

### 2. AI-Powered Strategy Tools (20-60s execution)

Generate and improve trading strategies:

- **`generate_ideas`** - Get AI-generated strategy concepts based on market data
- **`create_strategy`** - Generate complete Python strategy from description
- **`optimize_strategy`** - Tune parameters for better performance
- **`enhance_with_allora`** - Add Allora Network ML predictions to strategy
- **`refine_strategy`** - Make targeted code improvements
- **`create_prediction_market_strategy`** - Generate Polymarket YES/NO trading logic

**Pricing**: Real LLM cost + margin ($0.50-$4.50 typical). These are the most expensive tools.

**When to use**: After understanding available resources, use these to build or improve strategies. Always backtest after generation.

### 3. Backtesting Tools (20-40s execution)

Test strategy performance on historical data:

- **`run_backtest`** - Test crypto trading strategies
- **`run_prediction_market_backtest`** - Test Polymarket strategies

**Pricing**: $0.001 per backtest

**Returns**: Performance metrics (Sharpe ratio, max drawdown, win rate, total return, profit factor), trade statistics, equity curve data

**When to use**: After creating or modifying a strategy, always backtest before deploying. Use multiple time periods to validate robustness.

### 4. Prediction Market Tools

Build Polymarket trading strategies:

- **`get_all_prediction_events`** - Browse available prediction markets
- **`get_prediction_market_data`** - Analyze YES/NO token price history
- **`create_prediction_market_strategy`** - Generate Polymarket strategy code

**Pricing**: $0.001 for data tools, Real LLM cost + margin for creation

**When to use**: For prediction market trading strategies on Polymarket (politics, crypto price predictions, economics events)

### 5. Deployment Tools

Deploy strategies to live trading on Hyperliquid:

- **`deployment_create`** - Launch live trading agent (EOA or Hyperliquid Vault)
- **`deployment_list`** - Monitor active deployments
- **`deployment_start`** - Resume stopped deployment
- **`deployment_stop`** - Halt live trading

**Pricing**: $0.50 to create, free for list/start/stop

**Constraints**:
- EOA (wallet): Max 1 active deployment per wallet
- Hyperliquid Vault: Requires 200+ USDC in wallet, unlimited deployments

**When to use**: After thorough backtesting shows positive results. Never deploy without backtesting first.

### 6. Account Tools

Manage credits and view account info:

- **`get_credit_balance`** - Check available USDC credits
- **`get_credit_transactions`** - View transaction history

**Pricing**: Free

**When to use**: Check balance before expensive operations. Monitor spending via transaction history.

## Common Workflows

### Workflow 1: Create and Test New Strategy

```
1. get_all_symbols → See available trading pairs
2. get_all_technical_indicators → Browse indicators
3. create_strategy → Generate Python code from description
4. run_backtest → Test on 6+ months of data
5. If promising: optimize_strategy → Tune parameters
6. If excellent: enhance_with_allora → Add ML signals
7. run_backtest → Validate improvements
8. If ready: deployment_create → Deploy to live trading
```

**Cost**: ~$1-5 depending on optimization and enhancement

### Workflow 2: Enhance Existing Strategy

```
1. get_all_strategies (include_latest_backtest=true) → Find strategy
2. get_strategy_code → Review implementation
3. refine_strategy (mode="new") → Make targeted improvements
4. run_backtest → Test changes
5. If better: enhance_with_allora → Add ML predictions
6. run_backtest → Final validation
```

**Cost**: ~$0.50-2.00

### Workflow 3: Prediction Market Trading

```
1. get_all_prediction_events → Browse markets
2. get_prediction_market_data → Analyze price history
3. create_prediction_market_strategy → Build YES/NO logic
4. run_prediction_market_backtest → Test performance
5. If profitable: deployment_create → Deploy (when supported)
```

**Cost**: ~$0.50-5.00

### Workflow 4: Explore Ideas Before Building

```
1. get_all_symbols → Check available pairs
2. get_allora_topics → See ML prediction coverage
3. generate_ideas (strategy_count=3) → Get AI concepts
4. Pick favorite idea
5. create_strategy → Implement chosen concept
6. run_backtest → Validate
```

**Cost**: ~$0.50-4.50 (use generate_ideas to explore cheaply)

## Strategy Development Best Practices

### Start with Data Exploration

Always check availability before building:
- Use `get_data_availability` to verify symbol has sufficient history
- Check `get_allora_topics` if planning ML enhancement
- Review `get_all_technical_indicators` to know what's available

### Always Backtest

Never deploy without backtesting:
- Test on 6+ months of data minimum
- Use multiple time periods (train vs validation)
- Check metrics: Sharpe >1.0, max drawdown <20%, win rate 45-65%
- Compare performance across different market conditions

### Cost Management

Tools are priced in tiers:
1. **Data tools** ($0.001 or free) - Use liberally
2. **Backtesting** ($0.001) - Use frequently
3. **AI generation** (LLM cost + margin) - Most expensive
4. **Deployment** ($0.50) - One-time per deployment

**Cost-saving tips**:
- Use `generate_ideas` ($0.05-0.50) before `create_strategy` ($1-4)
- Check `get_latest_backtest_results` (free) before running new backtest
- Use `refine_strategy` ($0.50-1.50) instead of regenerating with `create_strategy`
- Review `get_strategy_code` (free) before modifying

### Strategy Naming Convention

Follow this pattern: `{Name}_{RiskLevel}[_suffix]`

Examples:
- `RSIMeanReversion_M` - Base strategy, medium risk
- `MomentumBreakout_H_optimized` - After optimization, high risk
- `TrendFollower_L_allora` - With Allora ML, low risk

Risk levels: H (high), M (medium), L (low)

## Technical Details

### Strategy Framework

Strategies use the Jesse trading framework with these required methods:
- `should_long()` - Check if conditions met for long entry
- `should_short()` - Check if conditions met for short entry
- `go_long()` - Execute long entry with position sizing
- `go_short()` - Execute short entry with position sizing

Optional methods:
- `on_open_position(order)` - Set stop loss, take profit after entry
- `update_position()` - Trailing stops, position management
- `should_cancel_entry()` - Cancel unfilled orders

### Available Indicators

170+ technical indicators via `jesse.indicators`:
- **Momentum**: RSI, MACD, Stochastic, ADX, CCI, MFI
- **Trend**: EMA, SMA, Supertrend, Parabolic SAR, VWAP
- **Volatility**: Bollinger Bands, ATR, Keltner Channels
- **Volume**: OBV, Volume Profile, Chaikin Money Flow
- And many more...

Use `get_all_technical_indicators` to see the full list.

### Allora Network Integration

Add ML price predictions to strategies:
- **Prediction types**: Log return (percentage change) or absolute price
- **Horizons**: 5m, 8h, 24h, 1 week
- **Assets**: BTC, ETH, SOL, NEAR
- **Networks**: Mainnet (10 topics) and Testnet (26 topics)

Use `enhance_with_allora` to automatically integrate predictions, or manually add via `self.get_predictions()` in strategy code.

### Deployment Options

**EOA (Externally Owned Account)**:
- Direct wallet trading
- Max 1 active deployment per wallet
- Immediate deployment
- Lower setup complexity

**Hyperliquid Vault**:
- Requires 200+ USDC in wallet
- Unlimited deployments
- Professional vault setup
- Public TVL and performance tracking

## Troubleshooting

### "Insufficient Credits" Error

Check balance: `get_credit_balance`
Purchase credits in Robonet dashboard if needed

### "No Data Available" for Backtest

Use `get_data_availability` to check symbol coverage
Try shorter date range or different symbol
BTC-USDT and ETH-USDT have longest history (2020-present)

### "No Trades Generated" in Backtest

Entry conditions may be too restrictive
Try longer test period or adjust thresholds
Use `get_strategy_code` to review logic

### Backtest Takes >2 Minutes

Long date ranges (>2 years) or high-frequency timeframes (1m) are slow
Use shorter ranges or lower frequency timeframes

### Strategy Not Showing in Web Interface

Strategies are linked to API key's wallet
Ensure logged into same account that owns the API key
Refresh "My Strategies" page

## Complete Tool Reference

For detailed parameter documentation on all 24 tools, see:
- [../../shared-references/tool-catalog.md](../../shared-references/tool-catalog.md)

The catalog includes:
- Full parameter specifications with types and defaults
- Return value descriptions
- Pricing for each tool
- Execution time estimates
- Usage examples

## Example Prompts

**Create a simple strategy:**
```
Use Robonet MCP to create a momentum strategy for BTC-USDT on 4h timeframe that:
- Enters long when RSI crosses above 30 and price is above 50-day EMA
- Exits with 2% stop loss or 4% take profit
- Uses 95% of available margin
```

**Backtest existing strategy:**
```
Backtest my RSIMeanReversion_M strategy on ETH-USDT 1h timeframe from 2024-01-01 to 2024-06-30
```

**Optimize parameters:**
```
Optimize the RSI period and stop loss percentage for my MomentumBreakout_H strategy on BTC-USDT 4h from 2024-01-01 to 2024-12-31
```

**Add ML predictions:**
```
Enhance my TrendFollower_M strategy with Allora predictions for ETH-USDT 8h timeframe and compare performance
```

**Deploy to live trading:**
```
Deploy my RSIMeanReversion_M_allora strategy to Hyperliquid on BTC-USDT 4h with 2x leverage using EOA deployment
```

## Security & Access

- All tools require valid API key from Robonet
- Strategies are wallet-scoped (only creator can access)
- Credits reserved atomically before execution
- API keys never committed to version control
- Use environment variables or secure config for API keys

## Resources

- **Robonet Dashboard**: [robonet.finance](https://robonet.finance)
- **API Key Management**: Dashboard → Settings → API Keys
- **Credit Purchase**: Dashboard → Settings → Billing
- **Jesse Framework Docs**: [jesse.trade](https://jesse.trade)
- **Allora Network**: [allora.network](https://allora.network)
- **Hyperliquid**: [hyperliquid.xyz](https://hyperliquid.xyz)
- **Support**: [Discord](https://discord.gg/robonet) or support@robonet.finance
