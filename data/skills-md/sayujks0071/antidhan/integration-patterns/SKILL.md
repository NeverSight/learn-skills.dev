---
name: integration-patterns
description: OpenAlgo-AITRAPP integration patterns, adapters, mocks, and strategy conversion. Use when integrating strategies with AITRAPP backtest engine, creating adapters, mocking OpenAlgo APIs, or converting strategies between systems.
---

# Integration Patterns

## Overview

This repository integrates **OpenAlgo** (live trading platform) with **AITRAPP** (backtest engine) through adapters and mocks.

**Architecture:**
```
OpenAlgo Strategy → Adapter → AITRAPP Backtest Engine
                ↓
         Mock OpenAlgo API
```

## Key Components

### Integration Utilities

**Location:** `openalgo/strategies/utils/`

- `aitrapp_integration.py` - Sets up AITRAPP path and imports
- `openalgo_mock.py` - Mocks OpenAlgo API for backtesting
- `strategy_adapter.py` - Base adapter for strategy conversion
- `aitrapp_utils.py` - Helper functions for integration

### AITRAPP Core

**Location:** `AITRAPP/AITRAPP/packages/core/`

- `backtest.py` - Main backtest engine
- `historical_data.py` - Historical data loader
- `strategies/base.py` - Strategy interface
- `risk.py` - Risk management module
- `exits.py` - Exit management

## Strategy Adapter Pattern

### Base Adapter Structure

```python
from AITRAPP.AITRAPP.packages.core.strategies.base import BaseStrategy
from openalgo.strategies.utils.openalgo_mock import MockOpenAlgoAPI

class OpenAlgoStrategyAdapter(BaseStrategy):
    """
    Adapter to convert OpenAlgo strategy to AITRAPP format.
    """
    def __init__(self, openalgo_strategy_class, symbol, params):
        super().__init__(symbol)
        self.openalgo_strategy = openalgo_strategy_class(symbol, params)
        self.mock_api = MockOpenAlgoAPI()
        
        # Initialize OpenAlgo strategy with mock API
        self.openalgo_strategy.client = self.mock_api
    
    def on_bar(self, bar):
        """
        AITRAPP callback for each bar.
        Convert bar to OpenAlgo format and run strategy.
        """
        # Convert AITRAPP bar to OpenAlgo format
        openalgo_data = self._convert_bar(bar)
        
        # Update strategy data
        self.openalgo_strategy.data = openalgo_data
        
        # Run strategy logic
        self.openalgo_strategy.calculate_indicators()
        self.openalgo_strategy.check_signals()
        
        # Extract signals
        return self._extract_signals()
    
    def _convert_bar(self, bar):
        """Convert AITRAPP bar to pandas DataFrame"""
        import pandas as pd
        
        df = pd.DataFrame([{
            'open': bar.open,
            'high': bar.high,
            'low': bar.low,
            'close': bar.close,
            'volume': bar.volume,
            'datetime': bar.timestamp
        }])
        
        return df
    
    def _extract_signals(self):
        """Extract trading signals from OpenAlgo strategy"""
        signals = []
        
        if self.openalgo_strategy.position != 0:
            signal = {
                'side': 'BUY' if self.openalgo_strategy.position > 0 else 'SELL',
                'price': self.openalgo_strategy.data.iloc[-1]['close'],
                'quantity': abs(self.openalgo_strategy.position)
            }
            signals.append(signal)
        
        return signals
```

## OpenAlgo API Mock

### Mock Implementation

```python
class MockOpenAlgoAPI:
    """
    Mock OpenAlgo API for backtesting.
    Mimics OpenAlgo API responses without actual broker calls.
    """
    def __init__(self):
        self.orders = []
        self.positions = []
        self.historical_data = {}
    
    def history(self, symbol, exchange="NSE", interval="5m", start_date=None, end_date=None):
        """
        Mock historical data fetch.
        In real backtest, this would load from AITRAPP historical data.
        """
        # Load from AITRAPP historical data loader
        from AITRAPP.AITRAPP.packages.core.historical_data import HistoricalDataLoader
        
        loader = HistoricalDataLoader()
        data = loader.load(
            symbol=symbol,
            exchange=exchange,
            interval=interval,
            start_date=start_date,
            end_date=end_date
        )
        
        # Convert to OpenAlgo format (pandas DataFrame)
        import pandas as pd
        df = pd.DataFrame(data)
        
        return df
    
    def placesmartorder(self, strategy, symbol, action, exchange, price_type, product, quantity, position_size):
        """
        Mock order placement.
        In backtest, this records the order for execution simulation.
        """
        order = {
            'strategy': strategy,
            'symbol': symbol,
            'action': action,
            'exchange': exchange,
            'price_type': price_type,
            'product': product,
            'quantity': quantity,
            'position_size': position_size,
            'timestamp': datetime.now()
        }
        
        self.orders.append(order)
        
        # Return mock response
        return {
            'status': 'success',
            'order_id': f"MOCK_{len(self.orders)}",
            'message': 'Order placed (mock)'
        }
    
    def get_positions(self):
        """Mock positions fetch"""
        return self.positions
    
    def get_orderbook(self):
        """Mock orderbook fetch"""
        return self.orders
```

## Strategy Conversion Workflow

### Step 1: Create Adapter

```python
# File: openalgo/strategies/adapters/mcx_momentum_adapter.py

from openalgo.strategies.utils.strategy_adapter import BaseStrategyAdapter
from openalgo.strategies.scripts.mcx_commodity_momentum_strategy import MCXMomentumStrategy

class MCXMomentumAdapter(BaseStrategyAdapter):
    def __init__(self, symbol, params):
        super().__init__(MCXMomentumStrategy, symbol, params)
```

### Step 2: Register with Backtest Engine

```python
# File: openalgo/strategies/scripts/run_backtest_ranking.py

from openalgo.strategies.adapters.mcx_momentum_adapter import MCXMomentumAdapter

strategies = [
    MCXMomentumAdapter("NATURALGAS24FEB26FUT", PARAMS),
    # Add more strategies
]

# Run backtest
from AITRAPP.AITRAPP.packages.core.backtest import BacktestEngine

engine = BacktestEngine(
    strategies=strategies,
    start_date="2025-08-15",
    end_date="2025-11-10",
    capital=1000000
)

results = engine.run()
```

## Data Format Conversion

### AITRAPP Bar to OpenAlgo DataFrame

```python
def convert_aitrapp_bar_to_openalgo(bar):
    """
    Convert AITRAPP bar object to OpenAlgo DataFrame format.
    """
    import pandas as pd
    
    df = pd.DataFrame([{
        'datetime': bar.timestamp,
        'open': bar.open,
        'high': bar.high,
        'low': bar.low,
        'close': bar.close,
        'volume': bar.volume
    }])
    
    df.set_index('datetime', inplace=True)
    return df
```

### OpenAlgo Signal to AITRAPP Signal

```python
def convert_openalgo_signal_to_aitrapp(signal):
    """
    Convert OpenAlgo signal format to AITRAPP signal format.
    """
    from AITRAPP.AITRAPP.packages.core.strategies.base import Signal
    
    return Signal(
        symbol=signal['symbol'],
        side=signal['side'],  # 'BUY' or 'SELL'
        quantity=signal['quantity'],
        entry_price=signal['price'],
        stop_loss=signal.get('stop_loss'),
        take_profit=signal.get('take_profit')
    )
```

## Historical Data Integration

### Loading Historical Data

```python
from AITRAPP.AITRAPP.packages.core.historical_data import HistoricalDataLoader

loader = HistoricalDataLoader()

# Load data for backtesting
data = loader.load(
    symbol="NIFTY",
    exchange="NSE",
    interval="5m",
    start_date="2025-08-15",
    end_date="2025-11-10"
)

# Convert to OpenAlgo format
import pandas as pd
df = pd.DataFrame(data)
```

### Data Format Requirements

**AITRAPP Format:**
```python
{
    'timestamp': datetime,
    'open': float,
    'high': float,
    'low': float,
    'close': float,
    'volume': int
}
```

**OpenAlgo Format:**
```python
DataFrame with columns:
- datetime (index)
- open
- high
- low
- close
- volume
```

## Risk Management Integration

### Using AITRAPP Risk Manager

```python
from AITRAPP.AITRAPP.packages.core.risk import RiskManager

risk_manager = RiskManager(
    account_size=1000000,
    max_heat=0.02,  # 2% portfolio heat
    daily_loss_limit=-0.025  # -2.5% daily loss limit
)

# Check signal before entry
is_approved, reason = risk_manager.check_signal(signal)

if not is_approved:
    logger.warning(f"[REJECTED] {reason}")
    return
```

### Exit Management Integration

```python
from AITRAPP.AITRAPP.packages.core.exits import ExitManager

exit_manager = ExitManager(
    stop_loss_type='ATR',  # 'FIXED' or 'ATR'
    take_profit_levels=[0.5, 1.0, 1.5],  # Staged TP
    trailing_stop=True,
    eod_exit_time='15:25'  # IST
)

# Check exit conditions
exit_signal = exit_manager.check_exit(position, current_bar)

if exit_signal:
    # Execute exit
    pass
```

## Backtest Integration

### Running Backtest with Adapter

```python
from AITRAPP.AITRAPP.packages.core.backtest import BacktestEngine
from openalgo.strategies.adapters.your_strategy_adapter import YourStrategyAdapter

# Create adapter
adapter = YourStrategyAdapter("SYMBOL", PARAMS)

# Initialize backtest engine
engine = BacktestEngine(
    strategies=[adapter],
    start_date="2025-08-15",
    end_date="2025-11-10",
    capital=1000000
)

# Run backtest
results = engine.run()

# Get metrics
print(f"Total Return: {results['total_return']:.2f}%")
print(f"Win Rate: {results['win_rate']:.2f}%")
print(f"Max Drawdown: {results['max_drawdown']:.2f}%")
```

## Common Integration Patterns

### Pattern 1: Direct Adapter

```python
# Simple adapter that wraps OpenAlgo strategy
class SimpleAdapter(BaseStrategy):
    def __init__(self, openalgo_strategy):
        self.strategy = openalgo_strategy
    
    def on_bar(self, bar):
        # Convert and run
        pass
```

### Pattern 2: Enhanced Adapter

```python
# Adapter with additional AITRAPP features
class EnhancedAdapter(BaseStrategy):
    def __init__(self, openalgo_strategy, risk_manager, exit_manager):
        self.strategy = openalgo_strategy
        self.risk_manager = risk_manager
        self.exit_manager = exit_manager
    
    def on_bar(self, bar):
        # Run strategy with risk and exit management
        pass
```

### Pattern 3: Strategy Wrapper

```python
# Wrapper that converts strategy logic
class StrategyWrapper:
    def __init__(self, openalgo_strategy_class):
        self.strategy_class = openalgo_strategy_class
    
    def create_aitrapp_strategy(self, symbol, params):
        # Create AITRAPP-compatible strategy
        pass
```

## Troubleshooting

### Import Errors

**Issue:** Cannot import AITRAPP modules

**Solution:**
```python
# Add AITRAPP to path
import sys
from pathlib import Path

aitrapp_path = Path(__file__).parent.parent.parent / "AITRAPP" / "AITRAPP"
sys.path.insert(0, str(aitrapp_path))
```

### Data Format Mismatches

**Issue:** Data format doesn't match expected format

**Solution:**
- Check data conversion functions
- Verify column names and types
- Ensure datetime index is set correctly

### Mock API Not Working

**Issue:** Mock API not returning expected data

**Solution:**
- Verify mock implementation matches real API
- Check data loading from AITRAPP
- Ensure proper error handling

## Best Practices

1. **Separate concerns** - Keep adapters focused on conversion only
2. **Preserve strategy logic** - Don't modify original strategy code
3. **Test adapters** - Verify adapter works with sample data
4. **Handle errors** - Graceful fallbacks for missing data
5. **Document conversions** - Clear documentation of format conversions
6. **Reuse mocks** - Share mock implementations across adapters

## Additional Resources

- Integration guide: `openalgo/strategies/AITRAPP_INTEGRATION_GUIDE.md`
- Adapter examples: `openalgo/strategies/adapters/`
- Mock implementations: `openalgo/strategies/utils/openalgo_mock.py`
- AITRAPP core: `AITRAPP/AITRAPP/packages/core/`
