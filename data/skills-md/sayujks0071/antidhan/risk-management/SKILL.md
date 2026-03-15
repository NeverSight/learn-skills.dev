---
name: risk-management
description: Implement and review risk controls, position sizing, portfolio heat limits, stop losses, and risk monitoring. Use when implementing risk management, reviewing risk controls, calculating position sizes, or analyzing portfolio risk exposure.
---

# Risk Management

## Core Principles

### Risk Limits

**Per-Trade Risk:**
- Default: 0.5-2.0% of capital per trade
- Maximum: 2.5% per trade (hard limit)

**Portfolio Heat:**
- Maximum: 2.0% of capital at risk simultaneously
- Monitors aggregate exposure across all positions

**Daily Loss Limit:**
- Hard stop: -2.5% of capital
- Triggers automatic position flattening

**Time-Based Exits:**
- EOD auto square-off: 15:25 IST
- Prevents overnight risk

## Position Sizing

### Risk-Based Position Sizing

```python
def calculate_position_size(entry_price, stop_loss_price, account_size, risk_pct=0.02):
    """
    Calculate position size based on risk per trade.
    
    Args:
        entry_price: Entry price
        stop_loss_price: Stop loss price
        account_size: Total account size
        risk_pct: Risk percentage per trade (default 2%)
    
    Returns:
        Quantity to trade
    """
    risk_amount = account_size * risk_pct
    risk_per_unit = abs(entry_price - stop_loss_price)
    
    if risk_per_unit == 0:
        return 0
    
    quantity = int(risk_amount / risk_per_unit)
    return max(quantity, 1)  # Minimum 1 unit
```

### ATR-Based Position Sizing

```python
def calculate_atr_position_size(entry_price, atr, account_size, risk_pct=0.02, atr_multiplier=2.0):
    """
    Calculate position size using ATR-based stop loss.
    
    Args:
        entry_price: Entry price
        atr: Average True Range
        account_size: Total account size
        risk_pct: Risk percentage per trade
        atr_multiplier: ATR multiplier for stop loss (default 2.0)
    
    Returns:
        Quantity to trade
    """
    stop_loss_price = entry_price - (atr * atr_multiplier)
    return calculate_position_size(entry_price, stop_loss_price, account_size, risk_pct)
```

### Options Position Sizing

```python
def calculate_options_position_size(option_ltp, lot_size, account_size, risk_pct=0.02, sl_pct=0.20):
    """
    Calculate options position size.
    
    Args:
        option_ltp: Option last traded price
        lot_size: Lot size (e.g., 50 for NIFTY)
        account_size: Total account size
        risk_pct: Risk percentage per trade
        sl_pct: Stop loss percentage (default 20% for options)
    
    Returns:
        Number of lots
    """
    risk_amount = account_size * risk_pct
    risk_per_lot = option_ltp * lot_size * sl_pct
    
    if risk_per_lot == 0:
        return 0
    
    lots = int(risk_amount / risk_per_lot)
    return max(lots, 1)  # Minimum 1 lot
```

## Portfolio Heat Management

### Heat Calculation

```python
class PortfolioRiskManager:
    def __init__(self, account_size, max_heat=0.02):
        self.account_size = account_size
        self.max_heat = max_heat  # 2% max portfolio heat
        self.positions = []
    
    def calculate_position_risk(self, position):
        """Calculate risk for a single position"""
        if position['side'] == 'LONG':
            risk = abs(position['entry_price'] - position['stop_loss']) * position['quantity']
        else:  # SHORT
            risk = abs(position['stop_loss'] - position['entry_price']) * position['quantity']
        
        return risk
    
    def calculate_portfolio_heat(self):
        """Calculate total portfolio heat"""
        total_risk = sum(self.calculate_position_risk(pos) for pos in self.positions)
        heat_pct = total_risk / self.account_size
        return heat_pct
    
    def can_add_position(self, new_position_risk):
        """Check if new position can be added"""
        current_heat = self.calculate_portfolio_heat()
        new_heat = (current_heat * self.account_size + new_position_risk) / self.account_size
        
        return new_heat <= self.max_heat
```

### Heat Monitoring

```python
def check_portfolio_heat(positions, account_size, max_heat=0.02):
    """
    Check if portfolio heat is within limits.
    
    Returns:
        (is_ok, current_heat, max_heat)
    """
    total_risk = sum(
        abs(pos['entry_price'] - pos['stop_loss']) * pos['quantity']
        for pos in positions
    )
    
    current_heat = total_risk / account_size
    
    if current_heat > max_heat:
        logger.warning(f"[REJECTED] Portfolio heat limit: {current_heat:.2%} > {max_heat:.2%}")
        return False, current_heat, max_heat
    
    return True, current_heat, max_heat
```

## Stop Loss Management

### Fixed Percentage Stop Loss

```python
def calculate_stop_loss(entry_price, side, stop_loss_pct=1.5):
    """
    Calculate stop loss price.
    
    Args:
        entry_price: Entry price
        side: 'BUY' (long) or 'SELL' (short)
        stop_loss_pct: Stop loss percentage
    
    Returns:
        Stop loss price
    """
    if side == 'BUY':
        return entry_price * (1 - stop_loss_pct / 100)
    else:  # SELL (short)
        return entry_price * (1 + stop_loss_pct / 100)
```

### ATR-Based Stop Loss

```python
def calculate_atr_stop_loss(entry_price, atr, side, atr_multiplier=2.0):
    """
    Calculate ATR-based stop loss.
    
    Args:
        entry_price: Entry price
        atr: Average True Range
        side: 'BUY' (long) or 'SELL' (short)
        atr_multiplier: ATR multiplier (default 2.0)
    
    Returns:
        Stop loss price
    """
    stop_distance = atr * atr_multiplier
    
    if side == 'BUY':
        return entry_price - stop_distance
    else:  # SELL (short)
        return entry_price + stop_distance
```

### Trailing Stop Loss

```python
class TrailingStop:
    def __init__(self, initial_stop, trailing_pct=0.5):
        self.initial_stop = initial_stop
        self.trailing_pct = trailing_pct
        self.current_stop = initial_stop
        self.highest_price = initial_stop  # For long positions
    
    def update(self, current_price, side='BUY'):
        """Update trailing stop based on current price"""
        if side == 'BUY':
            if current_price > self.highest_price:
                self.highest_price = current_price
                self.current_stop = current_price * (1 - self.trailing_pct / 100)
        else:  # SELL (short)
            if current_price < self.lowest_price:
                self.lowest_price = current_price
                self.current_stop = current_price * (1 + self.trailing_pct / 100)
        
        return self.current_stop
    
    def is_stopped_out(self, current_price, side='BUY'):
        """Check if stop loss is hit"""
        if side == 'BUY':
            return current_price <= self.current_stop
        else:  # SELL (short)
            return current_price >= self.current_stop
```

## Take Profit Management

### Fixed Take Profit

```python
def calculate_take_profit(entry_price, side, take_profit_pct=3.0):
    """
    Calculate take profit price.
    
    Args:
        entry_price: Entry price
        side: 'BUY' (long) or 'SELL' (short)
        take_profit_pct: Take profit percentage
    
    Returns:
        Take profit price
    """
    if side == 'BUY':
        return entry_price * (1 + take_profit_pct / 100)
    else:  # SELL (short)
        return entry_price * (1 - take_profit_pct / 100)
```

### Staged Take Profit

```python
class StagedTakeProfit:
    def __init__(self, entry_price, side, tp_levels=[0.5, 1.0, 1.5]):
        """
        Staged take profit with multiple levels.
        
        Args:
            entry_price: Entry price
            side: 'BUY' (long) or 'SELL' (short)
            tp_levels: List of take profit percentages
        """
        self.entry_price = entry_price
        self.side = side
        self.tp_levels = sorted(tp_levels)
        self.levels_hit = []
    
    def calculate_tp_prices(self):
        """Calculate take profit prices for all levels"""
        tp_prices = []
        for level in self.tp_levels:
            if self.side == 'BUY':
                tp_price = self.entry_price * (1 + level / 100)
            else:  # SELL (short)
                tp_price = self.entry_price * (1 - level / 100)
            tp_prices.append(tp_price)
        return tp_prices
    
    def check_tp_levels(self, current_price):
        """Check which take profit levels are hit"""
        tp_prices = self.calculate_tp_prices()
        hit_levels = []
        
        for i, tp_price in enumerate(tp_prices):
            if i in self.levels_hit:
                continue
            
            if self.side == 'BUY' and current_price >= tp_price:
                hit_levels.append(i)
            elif self.side == 'SELL' and current_price <= tp_price:
                hit_levels.append(i)
        
        self.levels_hit.extend(hit_levels)
        return hit_levels
```

## Daily Loss Limits

### Daily Loss Tracking

```python
class DailyLossTracker:
    def __init__(self, account_size, daily_loss_limit=-0.025):
        self.account_size = account_size
        self.daily_loss_limit = daily_loss_limit  # -2.5%
        self.starting_balance = account_size
        self.current_balance = account_size
        self.trades_today = []
    
    def update_balance(self, new_balance):
        """Update current balance"""
        self.current_balance = new_balance
    
    def add_trade(self, trade_pnl):
        """Add trade PnL"""
        self.trades_today.append(trade_pnl)
        self.current_balance += trade_pnl
    
    def check_daily_loss(self):
        """Check if daily loss limit is exceeded"""
        daily_pnl = self.current_balance - self.starting_balance
        daily_pnl_pct = daily_pnl / self.starting_balance
        
        if daily_pnl_pct <= self.daily_loss_limit:
            logger.error(f"[RISK] Daily loss limit hit: {daily_pnl_pct:.2%}")
            return True
        
        return False
    
    def reset_daily(self):
        """Reset for new trading day"""
        self.starting_balance = self.current_balance
        self.trades_today = []
```

## Risk Monitoring

### Real-Time Risk Check

```python
def check_signal_risk(signal, portfolio_manager, account_size):
    """
    Comprehensive risk check before entering trade.
    
    Returns:
        (is_approved, rejection_reason)
    """
    # 1. Per-trade risk check
    position_risk = calculate_position_risk(signal)
    risk_pct = position_risk / account_size
    
    if risk_pct > 0.025:  # 2.5% max per trade
        return False, "Per-trade risk limit exceeded"
    
    # 2. Portfolio heat check
    can_add, current_heat, max_heat = check_portfolio_heat(
        portfolio_manager.positions,
        account_size
    )
    
    if not can_add:
        return False, f"Portfolio heat limit: {current_heat:.2%} > {max_heat:.2%}"
    
    # 3. Daily loss check
    if portfolio_manager.daily_loss_tracker.check_daily_loss():
        return False, "Daily loss limit exceeded"
    
    # 4. Position limit check
    if len(portfolio_manager.positions) >= MAX_POSITIONS:
        return False, "Maximum position limit reached"
    
    return True, None
```

## Risk Reporting

### Risk Metrics Report

```python
def generate_risk_report(portfolio_manager, account_size):
    """Generate comprehensive risk report"""
    report = {
        'account_size': account_size,
        'current_balance': portfolio_manager.current_balance,
        'portfolio_heat': portfolio_manager.calculate_portfolio_heat(),
        'max_heat_limit': 0.02,
        'daily_pnl': portfolio_manager.daily_loss_tracker.current_balance - portfolio_manager.daily_loss_tracker.starting_balance,
        'daily_loss_limit': account_size * -0.025,
        'positions': len(portfolio_manager.positions),
        'max_positions': MAX_POSITIONS,
        'total_exposure': sum(pos['quantity'] * pos['entry_price'] for pos in portfolio_manager.positions)
    }
    
    return report
```

## Best Practices

1. **Always use stop losses** - Never enter a trade without a defined stop loss
2. **Respect portfolio heat** - Monitor aggregate risk across all positions
3. **Scale position sizes** - Reduce size during drawdowns, increase during winning streaks
4. **Time-based exits** - Always exit before market close (15:25 IST)
5. **Daily loss limits** - Hard stop at -2.5% to prevent catastrophic losses
6. **Regular monitoring** - Check risk metrics throughout the trading day
7. **Document exceptions** - Log any risk limit overrides with justification

## Additional Resources

- AITRAPP risk module: `AITRAPP/AITRAPP/packages/core/risk.py`
- Trading utils: `openalgo/strategies/utils/trading_utils.py`
- Risk documentation: `AITRAPP/AITRAPP/SECURITY.md`
