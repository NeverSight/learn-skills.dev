---
name: backtesting-analysis
description: Run backtests, analyze strategy performance, compare strategies, and generate ranking reports. Use when backtesting strategies, analyzing performance metrics, comparing strategy variants, or generating backtest reports.
---

# Backtesting & Analysis

## Quick Start

When running backtests:

1. Use the backtest engine or AITRAPP integration
2. Configure date range, capital, and parameters
3. Run backtest and collect metrics
4. Analyze results and compare strategies
5. Generate ranking reports

## Backtest Execution

### Simple Backtest Engine

**Location:** `openalgo/strategies/utils/simple_backtest_engine.py`

```python
from openalgo.strategies.utils.simple_backtest_engine import SimpleBacktestEngine
from openalgo.strategies.scripts.your_strategy import YourStrategy

# Initialize engine
engine = SimpleBacktestEngine(
    strategy_class=YourStrategy,
    symbol="NIFTY",
    start_date="2025-08-15",
    end_date="2025-11-10",
    capital=1000000
)

# Run backtest
results = engine.run()

# Get metrics
print(f"Total Return: {results['total_return']:.2f}%")
print(f"Win Rate: {results['win_rate']:.2f}%")
print(f"Profit Factor: {results['profit_factor']:.2f}")
print(f"Max Drawdown: {results['max_drawdown']:.2f}%")
```

### AITRAPP Backtest Integration

**Location:** `openalgo/strategies/scripts/run_backtest_ranking.py`

```bash
cd openalgo/strategies
python3 scripts/run_backtest_ranking.py \
    --symbol NIFTY \
    --start-date 2025-08-15 \
    --end-date 2025-11-10 \
    --capital 1000000
```

**Output:**
- CSV report: `backtest_results/ranking_report_{symbol}_{date}.csv`
- JSON report: `backtest_results/ranking_report_{symbol}_{date}.json`
- Comparison table with all strategies

## Performance Metrics

### Key Metrics

**Returns:**
- Total Return (%)
- Annualized Return (%)
- Monthly Return (%)

**Risk Metrics:**
- Max Drawdown (%)
- Average Drawdown (%)
- Volatility (%)

**Trade Statistics:**
- Win Rate (%)
- Profit Factor (Gross Profit / Gross Loss)
- Average Win / Loss
- Largest Win / Loss
- Total Trades

**Risk-Adjusted:**
- Sharpe Ratio
- Sortino Ratio
- Calmar Ratio (Return / Max Drawdown)

### Metric Calculation

```python
def calculate_metrics(trades, equity_curve):
    """Calculate comprehensive performance metrics"""
    if not trades:
        return {}
    
    wins = [t for t in trades if t.pnl > 0]
    losses = [t for t in trades if t.pnl < 0]
    
    total_return = (equity_curve[-1] - equity_curve[0]) / equity_curve[0] * 100
    win_rate = len(wins) / len(trades) * 100 if trades else 0
    
    gross_profit = sum(t.pnl for t in wins)
    gross_loss = abs(sum(t.pnl for t in losses))
    profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0
    
    max_dd = calculate_max_drawdown(equity_curve)
    
    return {
        'total_return': total_return,
        'win_rate': win_rate,
        'profit_factor': profit_factor,
        'max_drawdown': max_dd,
        'total_trades': len(trades)
    }
```

## Strategy Comparison

### Ranking Criteria

Strategies are ranked by composite score:

```python
def calculate_composite_score(metrics):
    """Calculate composite ranking score"""
    # Weighted components
    return_score = metrics['total_return'] * 0.30
    sharpe_score = metrics['sharpe_ratio'] * 0.25
    win_rate_score = metrics['win_rate'] * 0.20
    profit_factor_score = metrics['profit_factor'] * 10 * 0.15
    drawdown_penalty = metrics['max_drawdown'] * -0.10
    
    return return_score + sharpe_score + win_rate_score + profit_factor_score + drawdown_penalty
```

### Comparison Table Format

```
Strategy Name          | Return  | Win Rate | PF    | Max DD  | Score
-----------------------|---------|----------|-------|---------|-------
MCX Advanced           | 15.2%   | 58.3%    | 1.85  | -8.5%   | 8.2
NIFTY Greeks Enhanced  | 12.8%   | 62.1%    | 2.10  | -6.2%   | 8.5
ML Momentum            | 18.5%   | 55.0%    | 1.65  | -12.3%  | 7.8
```

## Parameter Optimization

### Grid Search

```python
from openalgo.strategies.utils.parameter_space import ParameterSpace

param_space = {
    'adx_threshold': [20, 25, 30],
    'rsi_overbought': [70, 75, 80],
    'risk_per_trade': [0.01, 0.02, 0.03]
}

best_params = None
best_score = -float('inf')

for params in ParameterSpace(param_space):
    strategy = YourStrategy(symbol, params)
    results = engine.run()
    score = calculate_composite_score(results)
    
    if score > best_score:
        best_score = score
        best_params = params
```

### Walk-Forward Analysis

```python
def walk_forward_optimization(start_date, end_date, window_months=3):
    """Optimize parameters using walk-forward analysis"""
    results = []
    
    current_start = start_date
    while current_start < end_date:
        current_end = current_start + timedelta(days=window_months * 30)
        
        # Optimize on training period
        best_params = optimize_parameters(current_start, current_end)
        
        # Test on out-of-sample period
        test_results = backtest(best_params, current_end, current_end + timedelta(days=30))
        results.append(test_results)
        
        current_start = current_end
    
    return aggregate_results(results)
```

## Report Generation

### CSV Report

```python
import pandas as pd

def generate_csv_report(results, filename):
    """Generate CSV report from backtest results"""
    df = pd.DataFrame([{
        'strategy': r['name'],
        'return_pct': r['total_return'],
        'win_rate': r['win_rate'],
        'profit_factor': r['profit_factor'],
        'max_drawdown': r['max_drawdown'],
        'sharpe_ratio': r['sharpe_ratio'],
        'total_trades': r['total_trades']
    } for r in results])
    
    df = df.sort_values('composite_score', ascending=False)
    df.to_csv(filename, index=False)
```

### JSON Report

```python
import json

def generate_json_report(results, filename):
    """Generate detailed JSON report"""
    report = {
        'backtest_period': {
            'start': start_date,
            'end': end_date
        },
        'capital': capital,
        'strategies': results,
        'summary': {
            'best_strategy': max(results, key=lambda x: x['composite_score']),
            'worst_strategy': min(results, key=lambda x: x['composite_score'])
        }
    }
    
    with open(filename, 'w') as f:
        json.dump(report, f, indent=2)
```

## Common Analysis Tasks

### Equity Curve Analysis

```python
import matplotlib.pyplot as plt

def plot_equity_curve(equity_curve, dates):
    """Plot equity curve over time"""
    plt.figure(figsize=(12, 6))
    plt.plot(dates, equity_curve)
    plt.title('Equity Curve')
    plt.xlabel('Date')
    plt.ylabel('Portfolio Value')
    plt.grid(True)
    plt.show()
```

### Drawdown Analysis

```python
def calculate_drawdowns(equity_curve):
    """Calculate drawdown periods"""
    peak = equity_curve[0]
    drawdowns = []
    
    for value in equity_curve:
        if value > peak:
            peak = value
        
        dd = (peak - value) / peak * 100
        drawdowns.append(dd)
    
    return drawdowns
```

### Trade Distribution Analysis

```python
def analyze_trade_distribution(trades):
    """Analyze distribution of trade outcomes"""
    pnls = [t.pnl for t in trades]
    
    print(f"Mean PnL: {np.mean(pnls):.2f}")
    print(f"Median PnL: {np.median(pnls):.2f}")
    print(f"Std Dev: {np.std(pnls):.2f}")
    print(f"Skewness: {scipy.stats.skew(pnls):.2f}")
    print(f"Kurtosis: {scipy.stats.kurtosis(pnls):.2f}")
```

## Troubleshooting

### No Trades Generated

Check:
1. Date range has sufficient data
2. Entry conditions are not too strict
3. Market hours filter is correct
4. Symbol/instrument is valid

### Unrealistic Results

Verify:
1. Transaction costs are included (slippage, commissions)
2. Position sizing is realistic
3. Data quality (no gaps, correct prices)
4. Market impact is considered for large orders

### Slow Backtests

Optimize:
1. Reduce date range for initial testing
2. Use lower resolution data (15m instead of 5m)
3. Cache indicator calculations
4. Parallelize strategy runs

## Additional Resources

- Backtest engine: `openalgo/strategies/utils/simple_backtest_engine.py`
- AITRAPP integration: `openalgo/strategies/AITRAPP_INTEGRATION_GUIDE.md`
- Results location: `openalgo/strategies/backtest_results/`
- Ranking script: `openalgo/strategies/scripts/run_backtest_ranking.py`
