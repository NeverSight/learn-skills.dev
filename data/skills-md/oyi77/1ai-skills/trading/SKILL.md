---
name: trading
description: Comprehensive trading skills system with multi-broker support, strategy execution, and autonomous trading capabilities
permissions:
  - fs
  - network
---

# Trading Skills System

Comprehensive trading automation system with multi-broker support, strategy development, and autonomous trading capabilities.

## Capabilities

### Broker Connectors
- **MetaTrader 5 (MT5)**: Full support for forex, commodities, stocks, indices
- **MetaTrader 4 (MT4)**: Legacy broker support
- **CCXT**: Cryptocurrency exchange integration (Binance, Bybit, OKX, KuCoin, etc.)

### Trading Modes
- **Backtest**: Historical strategy testing with detailed metrics
- **Paper Trade**: Virtual trading with real-time simulation
- **Real Trade**: Live execution with guardrails and safety checks

### Strategy Support
- **Crypto**: Cryptocurrency trading strategies
- **TradFi**:
  - Forex: Major, minor, and exotic pairs
  - Stocks: Individual equities
  - Commodities: Gold, silver, oil, etc.

### Trading Team
- **Researcher**: Market analysis and data collection
- **Strategist**: Strategy building and optimization
- **Risk Manager**: Position sizing and risk control
- **Executor**: Trade execution with broker integration
- **Orchestrator**: Team coordination for autonomous operations

## Commands

### `setup`
Initialize trading configuration and broker connection.

**Usage**: `setup broker=mt5 path=/path/to/mt5 terminal login=12345 password=xxx server=Broker-Server`

### `signal today`
Get trading signals for today.

**Usage**: `signal today symbol=XAUUSD timeframe=H1`

### `backtest`
Run historical backtest with full metrics.

**Usage**:
```bash
# Quick backtest (uses breakout strategy with Yahoo Finance data)
python scripts/xauusd_backtest.py --initial-balance 100 --start 2025-01-01 --end 2026-01-01

# With custom parameters
python scripts/xauusd_backtest.py --initial-balance 100 --start 2025-01-01 --end 2026-01-01 --lookback 20 --tp 0.02 --sl 0.01
```

**Output includes**:
- Initial Balance / Ending Balance
- Net PNL with Return %
- Max Drawdown (absolute + %)
- PNL in USD
- PNL in Points/Pips
- Avg Win/Loss
- Profit Factor
- Win Rate

**Quick Commands**:
```bash
cd C:\Users\EX PC\.openclaw\workspace\skills\1ai-skills\trading
.venv\Scripts\activate
python scripts\xauusd_backtest.py
```

### `summary`
Generate trading summary from CSV file.

**Usage**:
```bash
python scripts/backtest_summary.py --file trades.csv
python scripts/backtest_summary.py --file trades.csv --json
python scripts/backtest_summary.py --file trades.csv --initial-balance 5000
```

**Input Format** (CSV):
```csv
pair,pnl_usd,pnl_points,win
XAUUSD,27.00,2.7,True
XAUUSD,-45.00,-4.5,False
```

### `paper start`
Start paper trading mode.

**Usage**: `paper start symbol=XAUUSD`

### `paper status`
Check paper trading status.

**Usage**: `paper status`

### `paper stop`
Stop paper trading.

**Usage**: `paper stop`

### `real arm`
Arm real trading with guardrail check.

**Usage**: `real arm symbol=XAUUSD volume=0.01`

### `real status`
Check real trading status.

**Usage**: `real status`

### `real disarm`
Disarm real trading.

**Usage**: `real disarm`

### `export trades`
Export trade history.

**Usage**: `export trades format=csv`

## Strategies

### FOREX Strategies

#### `holy_grail`
Multi-timeframe trend-following strategy using EMA crossovers and ADX confirmation.

**Usage**: `signal today symbol=EURUSD strategy=holy_grail timeframe=H1`

**Parameters**:
- `ema_fast`: Fast EMA period (default: 9)
- `ema_slow`: Slow EMA period (default: 21)
- `adx_period`: ADX period for trend strength (default: 14)
- `adx_threshold`: Minimum ADX value to confirm trend (default: 25)

**Example**:
```bash
signal today symbol=GBPUSD timeframe=H1 ema_fast=12 ema_slow=26 adx_threshold=30
```

#### `momentum_elder`
Impulse system based on Elder Ray concept with volume confirmation.

**Usage**: `signal today symbol=USDJPY strategy=momentum_elder timeframe=H4`

**Parameters**:
- `ema_period`: EMA period for trend direction (default: 13)
- `bull_power_threshold`: Minimum bull power for long signals (default: 0.0001)
- `bear_power_threshold`: Maximum bear power for short signals (default: -0.0001)

**Example**:
```bash
signal today symbol=AUDUSD timeframe=D1 ema_period=21
```

#### `kumo_breakout`
Ichimoku Kumo breakout strategy with cloud analysis.

**Usage**: `signal today symbol=USDCAD strategy=kumo_breakout timeframe=H1`

**Parameters**:
- `tenkan_period`: Tenkan-sen period (default: 9)
- `kijun_period`: Kijun-sen period (default: 26)
- `senkou_span_b`: Senkou Span B period (default: 52)
- `cloud_threshold`: Cloud thickness filter (default: 0.0005)

**Example**:
```bash
signal today symbol=EURJPY timeframe=H4 tenkan_period=12 kijun_period=24
```

### CRYPTO Strategies

#### `funding_reversal`
Arbitrage strategy based on funding rate divergences across exchanges.

**Usage**: `signal today symbol=BTC/USDT strategy=funding_reversal exchange=binance`

**Parameters**:
- `funding_threshold`: Minimum funding rate difference (default: 0.01%)
- `holding_period`: Maximum holding period in hours (default: 24)
- `min_spread`: Minimum price spread between exchanges (default: 0.1%)

**Example**:
```bash
signal today symbol=ETH/USDT strategy=funding_reversal exchange=bybit funding_threshold=0.02%
```

#### `volume_momentum`
Volume-weighted momentum strategy with volume spike detection.

**Usage**: `signal today symbol=SOL/USDT strategy=volume_momentum timeframe=1h`

**Parameters**:
- `volume_ma_period`: Volume MA period (default: 20)
- `volume_multiplier`: Volume spike threshold (default: 2.0)
- `momentum_period`: Momentum calculation period (default: 14)

**Example**:
```bash
signal today symbol=DOGE/USDT strategy=volume_momentum timeframe=4h volume_multiplier=2.5
```

### STOCKS Strategies

#### `golden_cross`
Classic golden cross strategy with moving average crossovers.

**Usage**: `signal today symbol=AAPL strategy=golden_cross timeframe=D1`

**Parameters**:
- `fast_ma`: Fast moving average period (default: 50)
- `slow_ma`: Slow moving average period (default: 200)
- `ma_type`: MA type (SMA, EMA, WMA) (default: SMA)

**Example**:
```bash
signal today symbol=TSLA strategy=golden_cross timeframe=D1 fast_ma=50 slow_ma=200 ma_type=EMA
```

#### `rsi_divergence`
RSI divergence detection for reversal signals.

**Usage**: `signal today symbol=NVDA strategy=rsi_divergence timeframe=H1`

**Parameters**:
- `rsi_period`: RSI period (default: 14)
- `oversold`: Oversold threshold (default: 30)
- `overbought`: Overbought threshold (default: 70)
- `divergence_lookback`: Lookback period for divergence (default: 14)

**Example**:
```bash
signal today symbol=MSFT strategy=rsi_divergence timeframe=H4 rsi_period=21 oversold=25 overbought=75
```

### COMMODITY Strategies

#### `gold_silver_ratio`
Precious metals ratio trading strategy.

**Usage**: `signal today symbol=XAUUSD strategy=gold_silver_ratio timeframe=D1`

**Parameters**:
- `ratio_ma_period`: Ratio MA period (default: 50)
- `ratio_threshold`: Upper/lower threshold for signals (default: 80)
- `correlation_check`: Verify correlation before trading (default: true)

**Example**:
```bash
signal today symbol=XAGUSD strategy=gold_silver_ratio timeframe=D1 ratio_threshold=75
```

#### `seasonal`
Seasonal pattern strategy based on historical monthly performance.

**Usage**: `signal today symbol=CLNYMEX strategy=seasonal timeframe=D1`

**Parameters**:
- `lookback_years`: Years of historical data (default: 10)
- `min_win_rate`: Minimum historical win rate (default: 55%)
- `seasonal_month`: Specific month to trade (optional)

**Example**:
```bash
signal today symbol=GCNYMEX strategy=seasonal timeframe=D1 lookback_years=15 min_win_rate=60
```

## Configuration

### Session Settings
- `timezone`: Trading timezone (default: "Asia/Jakarta")
- `session_start`: Session start time (default: "07:00")
- `session_end`: Session end time (default: "15:00")

### Risk Settings
- `risk_mode`: "fixed_lot" or "fixed_risk_percent"
- `fixed_lot`: Fixed lot size (default: 0.01)
- `risk_percent`: Risk percentage per trade (default: 1.0)
- `rr_ratio`: Risk-reward ratio (default: 2.0)

### Execution Settings
- `max_spread_points`: Maximum spread allowed
- `one_trade_per_day`: Limit to one trade per day
- `cancel_opposite_on_trigger`: Cancel opposite pending order on trigger
- `cancel_all_at_session_end`: Cancel pending orders at session end

## Examples

### XAUUSD Asia Session Breakout
```
setup symbol=XAUUSD broker=mt5
signal today
backtest start=2024-01-01 end=2024-12-31
paper start
```

### Crypto Strategy
```
setup symbol=BTC/USDT broker=ccxt exchange=binance
signal today
backtest start=2024-01-01 end=2024-12-31
```

## Safety Guardrails

1. **Pre-trade validation**: Spread check, drawdown check, daily limit check
2. **Parameter confirmation**: Always show summary before real execution
3. **Hard limits**: 1 trade per day, max spread, max drawdown
4. **Opposite cancellation**: Cancel pending order when opposite triggers

## Quick Start

### 1. Setup Python Environment

```bash
# Windows
cd C:\Users\EX PC\.openclaw\workspace\skills\1ai-skills\trading
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install yfinance pandas pytz openpyxl

# Linux/Mac
cd /path/to/1ai-skills/trading
python3 -m venv .venv
source .venv/bin/activate
pip install yfinance pandas pytz openpyxl
```

### 2. Run Backtest

```bash
# XAUUSD backtest
python scripts/xauusd_backtest.py --initial-balance 100

# Custom period
python scripts/xauusd_backtest.py --start 2025-01-01 --end 2026-01-01 --initial-balance 100
```

### 3. Generate Summary from CSV

```bash
python scripts/backtest_summary.py --file your_trades.csv
```

## Available Scripts

| Script | Purpose |
|--------|---------|
| `xauusd_backtest.py` | Backtest XAUUSD using Yahoo Finance data |
| `backtest_summary.py` | Generate metrics summary from trade CSV |
| `xauusd_backtest.ps1` | PowerShell alternative (no Python deps) |

## Dependencies

### Required Packages

```bash
pip install yfinance pandas pytz openpyxl
```

### Optional Packages

```bash
pip install MetaTrader5  # For MT5 broker connection
pip install ccxt         # For crypto exchanges (Binance, Bybit, etc.)
```

### Note
- Run scripts from `trading/scripts/` directory
- Or from parent directory with: `python scripts/script_name.py`
- For MT5: requires Windows + MT5 terminal installed
