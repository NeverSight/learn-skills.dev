---
name: trade-prediction-markets
description: "Build and test Polymarket prediction market trading strategies for YES/NO token trading. Provides 6 tools: get_all_prediction_events (browse markets, $0.001), get_prediction_market_data (analyze price history, $0.001), create_prediction_market_strategy (generate code, $1-$4.50), run_prediction_market_backtest (test performance, $0.001). Trade on real-world events (politics, economics, sports, crypto). Currently simulation only (live deployment coming soon)."
persona: ["trader", "researcher"]
risk_level: "medium"
cost_profile: "$0.001 for data, $1.00-$4.50 for strategy creation"
tools:
  - mcp__workbench__get_all_prediction_events
  - mcp__workbench__get_prediction_market_data
  - mcp__workbench__create_prediction_market_strategy
  - mcp__workbench__run_prediction_market_backtest
  - mcp__workbench__get_data_availability
  - mcp__workbench__get_latest_backtest_results
related_skills:
  prerequisite: browse-robonet-data
  next_steps:
    - build-trading-strategies
    - test-trading-strategies
---

# Trade Prediction Markets

## Quick Start

This skill enables trading on Polymarket prediction markets (YES/NO tokens) for real-world events.

**Load the tools first**:
```
Use MCPSearch to select: mcp__workbench__get_all_prediction_events
Use MCPSearch to select: mcp__workbench__get_prediction_market_data
Use MCPSearch to select: mcp__workbench__create_prediction_market_strategy
```

**Basic workflow**:
```
1. Browse markets:
   get_all_prediction_events(market_category="crypto_rolling")
   → See BTC/ETH price prediction markets

2. Analyze market data:
   get_prediction_market_data(condition_id="0x123...")
   → Study YES/NO token price history

3. Create strategy:
   create_prediction_market_strategy(
       strategy_name="PolymarketArb_M",
       description="Buy YES when price <40%, sell at 55%"
   )

4. Test strategy:
   run_prediction_market_backtest(
       strategy_name="PolymarketArb_M",
       ...
   )
```

**When to use this skill**:
- Trading on real-world events (elections, Fed decisions, sports)
- Want binary outcome exposure (YES/NO)
- Interested in probability-based trading
- Exploring prediction market opportunities

## Available Tools (6)

### get_all_prediction_events

**Purpose**: Browse available Polymarket prediction markets

**Parameters**:
- `active_only` (optional, boolean): Only active events (default: true)
- `market_category` (optional, string): Filter by category

**Categories**:
- `crypto_rolling`: Crypto price predictions (BTC >$100k in next hour?)
- `politics`: Elections, policy decisions
- `economics`: GDP, inflation, Fed decisions
- `sports`: Game outcomes, championships
- `entertainment`: Awards, box office results

**Returns**: List of events with names, categories, markets, condition IDs, resolution status

**Pricing**: $0.001

**Use when**: Discovering trading opportunities, browsing available markets

### get_prediction_market_data

**Purpose**: Analyze YES/NO token price history for specific market

**Parameters**:
- `condition_id` (required): Polymarket condition ID
- `start_date` (optional): Filter from date (YYYY-MM-DD)
- `end_date` (optional): Filter to date (YYYY-MM-DD)
- `timeframe` (optional): Candle timeframe (1m, 5m, 15m, 30m, 1h, 4h, default: 1m)
- `limit` (optional, 1-10000): Max candles per token (default: 1000)

**Returns**: Market metadata, YES token price timeseries, NO token price timeseries

**Pricing**: $0.001

**Use when**: Analyzing market price history, researching token behavior, validating strategy concepts

### create_prediction_market_strategy

**Purpose**: Generate Polymarket strategy code with YES/NO trading logic

**Parameters**:
- `strategy_name` (required): Strategy name (follow pattern: Name_RiskLevel)
- `description` (required): Detailed requirements for YES/NO logic, exit criteria, position sizing

**Returns**: Complete Python PolymarketStrategy code

**Pricing**: Real LLM cost + margin (max $4.50)

**Execution Time**: ~30-60 seconds

**Use when**: Building new Polymarket strategies

### run_prediction_market_backtest

**Purpose**: Test prediction market strategy on historical data

**Parameters**:
- `strategy_name` (required): PolymarketStrategy to test
- `start_date` (required): Start date (YYYY-MM-DD)
- `end_date` (required): End date (YYYY-MM-DD)
- `condition_id` (for single market): Specific condition ID
- `asset` (for rolling markets): Asset symbol ("BTC", "ETH")
- `interval` (for rolling markets): Market interval ("15m", "1h")
- `initial_balance` (optional): Starting USDC (default: 10000)
- `timeframe` (optional): Execution timeframe (default: 1m)

**Returns**: Backtest metrics (profit/loss, win rate, position history)

**Pricing**: $0.001

**Execution Time**: ~20-60 seconds

**Use when**: Validating prediction market strategies

### get_data_availability

**Purpose**: Check available data ranges for Polymarket markets

**Parameters**:
- `data_type`: "polymarket" or "all"
- `asset` (optional): Filter by asset
- `include_resolved` (optional): Include resolved markets

**Returns**: Data availability with date ranges

**Pricing**: $0.001

**Use when**: Before backtesting (verify sufficient data)

### get_latest_backtest_results

**Purpose**: View recent prediction market backtest results

**Parameters**:
- `strategy_name` (optional): Filter by strategy
- `limit` (optional): Number of results

**Returns**: Recent backtest records

**Pricing**: Free

**Use when**: Checking existing backtest results

## Core Concepts

### Prediction Market Mechanics

**YES/NO Token Structure**:
```
Event: "Will BTC exceed $100,000 by end of hour?"

YES Token:
- Pays $1.00 if event occurs
- Pays $0.00 if event doesn't occur
- Current price = Market's implied probability
- Example: YES token at $0.65 = 65% implied probability

NO Token:
- Pays $1.00 if event DOESN'T occur
- Pays $0.00 if event occurs
- Current price = 1 - YES price
- Example: NO token at $0.35 = 35% implied probability

Total: YES price + NO price ≈ $1.00 (arbitrage if not)
```

**How trading works**:
```
Scenario: YES token at $0.40

Buy YES token:
- Pay $0.40 now
- If event occurs: Receive $1.00 (profit $0.60 = 150% return)
- If event doesn't occur: Lose $0.40 (-100% return)

Risk/Reward:
- Risking $0.40 to make $0.60
- 1.5:1 reward:risk ratio
- Need >40% win rate to break even
```

### Market Categories

**Crypto Rolling Markets** (high frequency):
```
Type: Continuous prediction markets
Frequency: Every 15m, 1h, 4h, etc.
Question: "Will BTC price increase next [interval]?"

Example:
- 1h BTC rolling market
- New market every hour
- Predict if BTC closes higher than current price

Use case: Short-term price speculation
Trading style: Active, high frequency
```

**Politics** (event-driven):
```
Type: One-time events
Frequency: Varies (elections, policy decisions)
Timeline: Days to months until resolution

Examples:
- "Will candidate X win election?"
- "Will bill Y pass Congress by date Z?"
- "Will Fed cut rates in next meeting?"

Use case: Event speculation
Trading style: Position trading, hold until resolution
```

**Economics** (data release):
```
Type: Scheduled data releases
Frequency: Monthly, quarterly
Timeline: Fixed resolution dates

Examples:
- "Will CPI exceed 3.5% next month?"
- "Will GDP growth exceed 2% this quarter?"
- "Will unemployment rate decrease?"

Use case: Economic data predictions
Trading style: Position before release, exit at resolution
```

**Sports** (scheduled events):
```
Type: Game outcomes, championships
Frequency: Varies by sport
Timeline: Hours to months

Examples:
- "Will Team X win game tonight?"
- "Will Player Y score >25 points?"
- "Will Team Z win championship?"

Use case: Sports betting alternative
Trading style: Event-based positions
```

### Strategy Types

**Probability Arbitrage** (mean reversion):
```
Concept: Buy underpriced probabilities, sell when corrected

Example:
- Event has ~60% true probability
- YES token priced at $0.45 (implies 45%)
- Buy YES (underpriced)
- Sell when price reaches $0.60 (fair value)

Advantages: Mathematical edge if probability estimation accurate
Disadvantages: Requires good probability estimation
```

**Trend Following** (momentum):
```
Concept: Follow YES/NO token price momentum

Example:
- YES token price rising from $0.30 → $0.45
- Buy YES (momentum continuing)
- Exit when momentum fades

Advantages: Captures strong moves
Disadvantages: Late entries, whipsaws
```

**Mean Reversion** (range trading):
```
Concept: Fade extreme probability movements

Example:
- YES token spikes to $0.85 (85% implied)
- Seems too high, buy NO token ($0.15)
- Exit when reverts toward mean

Advantages: Profits from overreactions
Disadvantages: Catching falling knives (sometimes market is right)
```

**Event-Driven** (catalyst trading):
```
Concept: Trade based on news/catalysts

Example:
- Positive news for candidate X
- Buy YES token before market fully reacts
- Exit after market prices in news

Advantages: Early mover advantage
Disadvantages: Requires fast news reaction
```

### Rolling Markets

**How rolling markets work**:
```
BTC 1h Rolling Market:

Hour 1 (12:00-13:00):
- Market created at 12:00
- Question: "Will BTC close higher at 13:00 than 12:00?"
- YES/NO tokens trade 12:00-13:00
- Resolves at 13:00 based on price change

Hour 2 (13:00-14:00):
- New market created at 13:00
- Previous market resolved
- Profits/losses settled
- Process repeats

Strategy rolls from market to market automatically
```

**Advantages of rolling markets**:
- Continuous trading opportunities
- More data for backtesting (many markets)
- Predictable resolution times
- Suitable for algorithmic trading

**Disadvantages**:
- Higher frequency = more fees
- Requires active monitoring
- Shorter time to resolution (less time to be right)

### Polymarket Strategy Framework

**Required methods**:
```python
class MyPolymarketStrategy(PolymarketStrategy):
    def should_buy_yes(self) -> bool:
        """Check if conditions met for YES token purchase"""
        # Return True to buy YES token

    def should_buy_no(self) -> bool:
        """Check if conditions met for NO token purchase"""
        # Return True to buy NO token

    def go_yes(self):
        """Execute YES token purchase with position sizing"""
        # Calculate position size
        # Buy YES token

    def go_no(self):
        """Execute NO token purchase with position sizing"""
        # Calculate position size
        # Buy NO token
```

**Optional methods**:
```python
    def should_sell_yes(self) -> bool:
        """Exit YES position"""
        # Return True to sell YES tokens

    def should_sell_no(self) -> bool:
        """Exit NO position"""
        # Return True to sell NO tokens

    def on_market_resolution(self):
        """Handle market settlement"""
        # Called when market resolves
        # Settle P&L
```

## Best Practices

### Market Selection

**Choose liquid markets**:
```
High liquidity: >$50k volume
- Tight spreads
- Easy entry/exit
- Reliable pricing

Low liquidity: <$10k volume
- Wide spreads
- Difficult exits
- Slippage risk

Recommendation: Start with high-volume markets
```

**Prefer clear resolution criteria**:
```
GOOD: "Will BTC close above $100k at 5pm EST on Jan 1, 2025?"
- Objective resolution source (price data)
- Specific date and time
- No ambiguity

BAD: "Will crypto have a good year in 2025?"
- Subjective ("good" is undefined)
- Ambiguous resolution criteria
- Dispute risk
```

**Avoid ambiguous outcomes**:
```
Check resolution source:
- Data-driven (prices, scores, votes) → Good
- Subjective judgment → Bad
- "Community decides" → High dispute risk

Research past market resolutions:
- Were resolutions fair?
- Any disputed outcomes?
- Market maker credibility
```

### Strategy Development

**Define clear probability thresholds**:
```
Example: Probability arbitrage strategy

Entry logic:
- Buy YES if price <40% (undervalued)
- Buy NO if price <40% (YES >60%, overvalued)

Exit logic:
- Sell YES at 55% (15% profit target)
- Sell NO at 55% (symmetric)
- Stop loss at 25% (37.5% loss, preserve capital)
```

**Include position sizing**:
```
Fixed percentage:
- 5% of capital per market
- Max 10 simultaneous positions = 50% deployed
- Conservative, predictable

Kelly Criterion:
- Size based on edge and odds
- More aggressive, optimal growth
- Requires accurate probability estimation
```

**Set exit criteria**:
```
Profit targets:
- Sell at X% gain (e.g., 15% above entry)

Time-based exits:
- Close position Y hours before resolution
- Avoid last-minute volatility

Stop losses:
- Sell if price drops below Z% (e.g., 60% of entry)
- Preserve capital on wrong predictions
```

### Risk Management

**Position limits**:
```
Per market: 5-10% of capital
- Limits single-market exposure
- Diversifies risk

Total exposure: 50-70% of capital
- Leaves cash buffer
- Allows for new opportunities
- Prevents overtrading
```

**Market diversification**:
```
Don't concentrate in one category:
- 3 crypto markets
- 2 politics markets
- 2 sports markets
→ Diversified across event types

Avoid:
- 10 BTC rolling markets
→ All correlated, high concentration risk
```

**Liquidity monitoring**:
```
Check before entry:
- Current volume
- Bid/ask spread
- Order book depth

If liquidity drops:
- May be unable to exit
- Accept mark-to-market loss
- Or hold until resolution
```

## Common Workflows

### Workflow 1: Exploring Rolling Markets

**Goal**: Find BTC rolling market trading opportunities

```
1. Browse crypto rolling markets:
   get_all_prediction_events(market_category="crypto_rolling")
   → Lists BTC, ETH rolling markets with intervals

2. Check data availability:
   get_data_availability(data_type="polymarket", asset="BTC")
   → Verify sufficient history for backtesting

3. Analyze specific market:
   get_prediction_market_data(
       condition_id="0x123...",
       timeframe="1m",
       limit=5000
   )
   → Study YES/NO token price patterns

4. Identify strategy:
   - YES token often overshoots (>60%)
   - Mean reversion opportunity
   - Buy NO when YES >65%, exit at 55%

5. Create strategy:
   create_prediction_market_strategy(
       strategy_name="BTCRollingMeanRev_M",
       description="Buy NO token when YES >65%, exit at 55%..."
   )

6. Backtest strategy:
   run_prediction_market_backtest(
       strategy_name="BTCRollingMeanRev_M",
       asset="BTC",
       interval="1h",
       start_date="2024-01-01",
       end_date="2024-12-31"
   )
```

**Cost**: ~$2.50 ($0.003 data + $2.50 strategy creation)

### Workflow 2: Event-Driven Politics Trading

**Goal**: Trade on election prediction market

```
1. Browse politics markets:
   get_all_prediction_events(market_category="politics")
   → Find election markets

2. Analyze candidate X market:
   get_prediction_market_data(condition_id="election_123")
   → Study YES token price leading up to election

3. Identify pattern:
   - YES token very volatile
   - Spikes on good news, drops on bad news
   - Opportunities to buy dips, sell spikes

4. Create strategy:
   create_prediction_market_strategy(
       strategy_name="ElectionDipBuy_M",
       description="Buy YES when price drops >15% in 24h,
                   sell when recovers to pre-drop level..."
   )

5. Backtest (limited data for one-time events):
   - May have insufficient data for thorough backtest
   - Analyze manually or use similar past events

6. Trade carefully:
   - Event markets have less data
   - Higher uncertainty
   - Start with smaller position sizes
```

**Cost**: ~$2.50

### Workflow 3: Multi-Market Portfolio

**Goal**: Build diversified prediction market portfolio

```
1. Identify multiple opportunities:
   - BTC 1h rolling (crypto)
   - Fed decision (economics)
   - Championship game (sports)

2. Create strategies for each:
   - Strategy 1: BTC rolling mean reversion
   - Strategy 2: Fed decision probability arbitrage
   - Strategy 3: Sports underdog value

3. Backtest all strategies:
   run_prediction_market_backtest(...) for each

4. Allocate capital:
   - BTC rolling: 15% (more data, higher confidence)
   - Fed decision: 10% (one-time event, moderate confidence)
   - Sports: 5% (less data, lower confidence)
   Total: 30% deployed, 70% cash

5. Monitor performance:
   - Track each strategy independently
   - Rebalance based on results
   - Stop underperformers
```

**Cost**: ~$7.50 (3 strategies)

## Troubleshooting

### "No Prediction Events Found"

**Issue**: get_all_prediction_events returns empty

**Solutions**:
- Try `active_only=False` to see resolved markets
- Check different market_category
- Markets may be temporarily unavailable

### "Insufficient Market Data"

**Issue**: Not enough history for backtesting

**Solutions**:
- Prediction markets have shorter history than crypto
- Use shorter backtest periods (1-3 months)
- Focus on rolling markets (more data points)
- Some events are one-time (limited data)

### "Strategy Performs Poorly"

**Issue**: Backtest shows losses

**Solutions**:
- Prediction markets are efficient (hard to beat)
- Check if probability estimation is accurate
- Verify strategy logic makes sense
- Consider fees and slippage
- May need more sophisticated approach

## Next Steps

**After creating prediction market strategies**:

**Test thoroughly**:
- Use `test-trading-strategies` for backtesting
- Validate on multiple markets
- Check win rate and profit factor

**Refine strategies**:
- Use `improve-trading-strategies` to refine
- Optimize thresholds and parameters
- Test improvements

**Live deployment** (when supported):
- Currently simulation only
- Live Polymarket deployment coming soon
- Will use `deploy-live-trading` when available

## Summary

This skill provides **Polymarket prediction market trading**:

- **6 tools**: Events browsing, data analysis, strategy creation, backtesting
- **Cost**: $0.001 for data, $1-$4.50 for strategy creation
- **Markets**: Politics, economics, sports, crypto rolling
- **Status**: Simulation only (live deployment coming)

**Core principle**: Prediction markets trade YES/NO tokens on real-world events. Success requires accurate probability estimation and disciplined risk management.

**Best practices**: Choose liquid markets with clear resolution criteria, diversify across event types, use proper position sizing (5-10% per market), set profit targets and stop losses.

**Current limitation**: Live deployment not yet supported. Use for backtesting and strategy development. Live trading will be available in future updates.

**Note**: Prediction markets are efficient. Beating them consistently is difficult. Start with simulation, validate edge thoroughly before risking capital (when live deployment available).
