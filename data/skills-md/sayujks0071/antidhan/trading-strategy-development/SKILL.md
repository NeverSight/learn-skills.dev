---
name: trading-strategy-development
description: Create and modify trading strategies for OpenAlgo with proper structure, risk management, entry/exit logic, and position management. Use when developing new strategies, modifying existing ones, debugging strategy logic, or implementing trading signals.
---

# Trading Strategy Development

## Quick Start

When creating or modifying a trading strategy:

1. Use the standard strategy class structure
2. Implement entry/exit logic with proper risk management
3. Add position tracking and state management
4. Include structured logging with `[ENTRY]`, `[EXIT]`, `[REJECTED]`, `[POSITION]`, `[METRICS]` tags
5. Configure strategy parameters for backtesting

## Strategy Structure Template

```python
#!/usr/bin/env python3
"""
Strategy Name - Brief Description
"""
import os
import time
import logging
import pandas as pd
import numpy as np
import requests
from datetime import datetime
from pathlib import Path

# Configuration
SYMBOL = "REPLACE_ME"  # Injected by strategy manager
API_HOST = os.getenv('OPENALGO_HOST', 'http://127.0.0.1:5001')
API_KEY = os.getenv('OPENALGO_APIKEY', 'demo_key')

# Strategy Parameters
PARAMS = {
    'risk_per_trade': 0.02,  # 2% of capital
    'stop_loss_pct': 1.5,
    'take_profit_pct': 3.0,
    # Add strategy-specific parameters
}

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(f"Strategy_{SYMBOL}")

class StrategyName:
    def __init__(self, symbol, params):
        self.symbol = symbol
        self.params = params
        self.position = 0
        self.data = pd.DataFrame()
        self.entry_price = 0.0

    def fetch_data(self):
        """Fetch market data from OpenAlgo API"""
        # Implementation here
        pass

    def calculate_indicators(self):
        """Calculate technical indicators"""
        # RSI, MACD, ADX, ATR, VWAP, etc.
        pass

    def check_signals(self):
        """Check entry and exit conditions"""
        if self.data.empty:
            return

        current = self.data.iloc[-1]
        prev = self.data.iloc[-2]

        # Entry Logic
        if self.position == 0:
            if self._entry_conditions_met(current, prev):
                self.entry("BUY", current['close'])

        # Exit Logic
        elif self.position != 0:
            if self._exit_conditions_met(current, prev):
                self.exit("SELL", current['close'])

    def entry(self, side, price):
        """Execute entry signal"""
        logger.info(f"[ENTRY] {side} {self.symbol} at {price:.2f}")
        # Place order via API
        self.position = 1 if side == "BUY" else -1
        self.entry_price = price

    def exit(self, side, price):
        """Execute exit signal"""
        pnl = self._calculate_pnl(price)
        logger.info(f"[EXIT] {side} {self.symbol} at {price:.2f} | PnL: {pnl:.2f}")
        self.position = 0
        self.entry_price = 0.0

    def run(self):
        """Main strategy loop"""
        logger.info(f"Starting strategy for {self.symbol}")
        while True:
            self.fetch_data()
            self.calculate_indicators()
            self.check_signals()
            time.sleep(60)  # Check every minute
```

## Common Patterns

### Entry Conditions

**Momentum Strategy:**
```python
if (current['adx'] > 25 and
    current['rsi'] > 50 and
    current['close'] > prev['close'] and
    current['volume'] > prev['volume'] * 1.2):
    self.entry("BUY", current['close'])
```

**Mean Reversion Strategy:**
```python
if (current['rsi'] < 30 and
    current['close'] < current['lower_bb'] and
    current['close'] < current['vwap']):
    self.entry("BUY", current['close'])
```

**Breakout Strategy:**
```python
if (current['close'] > current['resistance'] and
    current['volume'] > current['avg_volume'] * 1.5 and
    current['adx'] > 20):
    self.entry("BUY", current['close'])
```

### Exit Conditions

**Stop Loss:**
```python
if self.position > 0:
    stop_loss = self.entry_price * (1 - self.params['stop_loss_pct'] / 100)
    if current['close'] < stop_loss:
        self.exit("SELL", current['close'])
```

**Take Profit:**
```python
if self.position > 0:
    take_profit = self.entry_price * (1 + self.params['take_profit_pct'] / 100)
    if current['close'] > take_profit:
        self.exit("SELL", current['close'])
```

**Trailing Stop:**
```python
if self.position > 0:
    trailing_stop = current['close'] - (2 * current['atr'])
    if trailing_stop > self.entry_price:
        self.exit("SELL", current['close'])
```

### Technical Indicators

**RSI:**
```python
delta = df['close'].diff()
gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
rs = gain / loss
df['rsi'] = 100 - (100 / (1 + rs))
```

**ATR:**
```python
high_low = df['high'] - df['low']
high_close = np.abs(df['high'] - df['close'].shift())
low_close = np.abs(df['low'] - df['close'].shift())
ranges = pd.concat([high_low, high_close, low_close], axis=1)
true_range = np.max(ranges, axis=1)
df['atr'] = true_range.rolling(window=14).mean()
```

**VWAP (Intraday):**
```python
df['tp'] = (df['high'] + df['low'] + df['close']) / 3
df['pv'] = df['tp'] * df['volume']
df['cum_pv'] = df.groupby(df['datetime'].dt.date)['pv'].cumsum()
df['cum_vol'] = df.groupby(df['datetime'].dt.date)['volume'].cumsum()
df['vwap'] = df['cum_pv'] / df['cum_vol']
```

## Risk Management

### Position Sizing

```python
def calculate_position_size(self, entry_price, stop_loss_price):
    """Calculate position size based on risk per trade"""
    risk_amount = ACCOUNT_SIZE * self.params['risk_per_trade']
    risk_per_unit = abs(entry_price - stop_loss_price)
    
    if risk_per_unit == 0:
        return 0
    
    quantity = int(risk_amount / risk_per_unit)
    return max(quantity, 1)  # Minimum 1 unit
```

### Portfolio Heat Limits

```python
def check_portfolio_heat(self):
    """Check total portfolio risk exposure"""
    total_risk = sum(self._calculate_position_risk(pos) for pos in self.positions)
    max_heat = ACCOUNT_SIZE * 0.02  # 2% max portfolio heat
    
    if total_risk >= max_heat:
        logger.warning("[REJECTED] Portfolio heat limit reached")
        return False
    return True
```

### Time-Based Exits

```python
from datetime import time
import pytz

def is_market_closing_soon(self):
    """Check if market is closing soon (exit before 15:15 IST)"""
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist).time()
    return now >= time(15, 15)  # Exit 15 minutes before market close
```

## Logging Standards

Use structured logging tags:

- `[ENTRY]` - Entry signal generated
- `[EXIT]` - Exit signal generated
- `[REJECTED]` - Signal rejected (risk limits, filters, etc.)
- `[POSITION]` - Position update
- `[METRICS]` - Performance metrics

Example:
```python
logger.info(f"[ENTRY] BUY {self.symbol} @ {price:.2f} | RSI={rsi:.1f} ADX={adx:.1f}")
logger.info(f"[EXIT] SELL {self.symbol} @ {price:.2f} | PnL={pnl:.2f}")
logger.warning(f"[REJECTED] Entry blocked: Portfolio heat limit")
logger.info(f"[METRICS] Win Rate: {win_rate:.1f}% | Profit Factor: {pf:.2f}")
```

## Strategy Types

### Equity Strategies
- Location: `openalgo/strategies/scripts/`
- Examples: `advanced_equity_strategy.py`, `sector_momentum_strategy.py`
- Focus: NSE stocks, sector rotation, momentum

### Options Strategies
- Location: `openalgo/strategies/scripts/`
- Examples: `advanced_options_ranker.py`
- Focus: IV rank, Greeks, spread strategies, delta neutrality
- Use port 5002 (Dhan broker)

### MCX Strategies
- Location: `openalgo/strategies/scripts/`
- Examples: `mcx_commodity_momentum_strategy.py`, `mcx_advanced_strategy.py`
- Focus: Commodities, futures, global arbitrage

## Common Issues

### Strategies Not Placing Orders

Check:
1. Entry conditions are too strict (relax filters)
2. Risk limits blocking entries (check portfolio heat)
3. Market hours validation (ensure market is open)
4. API connectivity (verify OpenAlgo server is running)

### Position Tracking Issues

Use `PositionManager` from `trading_utils.py`:
```python
from openalgo.strategies.utils.trading_utils import PositionManager

pm = PositionManager(symbol)
if not pm.has_position():
    pm.update_position(qty, price, 'BUY')
```

## Testing

Before deploying:
1. Test with paper trading mode
2. Verify entry/exit logic with historical data
3. Check risk management limits
4. Validate logging output
5. Test API connectivity

## Additional Resources

- Strategy examples: `openalgo/strategies/scripts/`
- Utility functions: `openalgo/strategies/utils/trading_utils.py`
- Backtest framework: `openalgo/strategies/utils/simple_backtest_engine.py`
- Integration guide: `openalgo/strategies/AITRAPP_INTEGRATION_GUIDE.md`
