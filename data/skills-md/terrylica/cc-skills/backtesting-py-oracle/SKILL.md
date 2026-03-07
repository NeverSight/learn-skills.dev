---
name: backtesting-py-oracle
description: backtesting.py configuration for SQL oracle validation and range bar pattern backtesting. Use when running backtesting.py against ClickHouse SQL results, configuring Backtest() constructor, handling overlapping trades, multi-position mode, rolling quantile NaN handling, trade sorting, or oracle gate validation. TRIGGERS - backtesting.py, Backtest(), hedging, exclusive_orders, multi-position, overlapping trades, oracle validation, SQL vs Python, trade comparison, entry price mismatch, signal count mismatch, rolling quantile NaN, ExitTime sort, stats._trades, gen600_strategy, champion_strategy, gen300_strategy, barrier setup.
allowed-tools: Read, Bash, Grep, Glob
---

# backtesting.py Oracle Validation for Range Bar Patterns

Configuration and anti-patterns for using backtesting.py to validate ClickHouse SQL sweep results. Ensures bit-atomic replicability between SQL and Python trade evaluation.

**Companion skills**: `clickhouse-antipatterns` (SQL correctness, AP-16) | `sweep-methodology` (sweep design) | `rangebar-eval-metrics` (evaluation metrics)

**Validated**: Gen600 oracle verification (2026-02-12) — 3 assets, 5 gates, ALL PASS.

---

## Critical Configuration (NEVER omit)

```python
from backtesting import Backtest

bt = Backtest(
    df,
    Strategy,
    cash=100_000,
    commission=0,
    hedging=True,           # REQUIRED: Multiple concurrent positions
    exclusive_orders=False,  # REQUIRED: Don't auto-close on new signal
)
```

**Why**: SQL evaluates each signal independently (overlapping trades allowed). Without `hedging=True`, backtesting.py skips signals while a position is open, producing fewer trades than SQL. This was discovered when SOLUSDT produced 105 Python trades vs 121 SQL trades — 16 signals were silently skipped.

---

## Anti-Patterns (Ordered by Severity)

### BP-01: Missing Multi-Position Mode (CRITICAL)

**Symptom**: Python produces fewer trades than SQL. Gate 1 (signal count) fails.

**Root Cause**: Default `exclusive_orders=True` prevents opening new positions while one is active.

**Fix**: Always use `hedging=True, exclusive_orders=False`.

### BP-02: ExitTime Sort Order (CRITICAL)

**Symptom**: Entry prices appear mismatched (Gate 3 fails) even though both SQL and Python use the same price source.

**Root Cause**: `stats._trades` is sorted by ExitTime, not EntryTime. When overlapping trades exit in a different order than they entered, trade[i] no longer maps to signal[i].

**Fix**:

```python
trades = stats._trades.sort_values("EntryTime").reset_index(drop=True)
```

### BP-03: NaN Poisoning in Rolling Quantile (CRITICAL)

**Symptom**: Cross-asset tests fail with far fewer Python trades. Feature quantile becomes NaN and propagates forward indefinitely.

**Root Cause**: `np.percentile` with NaN inputs returns NaN. If even one NaN feature value enters the rolling window, all subsequent quantiles become NaN, making all subsequent filter comparisons fail.

**Fix**: Skip NaN values when building the signal window:

```python
def _rolling_quantile_on_signals(feature_arr, is_signal_arr, quantile_pct, window=1000):
    result = np.full(len(feature_arr), np.nan)
    signal_values = []
    for i in range(len(feature_arr)):
        if is_signal_arr[i]:
            if len(signal_values) > 0:
                window_data = signal_values[-window:]
                result[i] = np.percentile(window_data, quantile_pct * 100)
            # Only append non-NaN values (matches SQL quantileExactExclusive NULL handling)
            if not np.isnan(feature_arr[i]):
                signal_values.append(feature_arr[i])
    return result
```

### BP-04: Data Range Mismatch (MODERATE)

**Symptom**: Different signal counts between SQL and Python for assets with early data (BNB, XRP).

**Root Cause**: `load_range_bars()` defaults to `start='2020-01-01'` but SQL has no lower bound.

**Fix**: Always pass `start='2017-01-01'` to cover all available data.

### BP-05: Margin Exhaustion with Overlapping Positions (MODERATE)

**Symptom**: Orders canceled with insufficient margin. Fewer trades than expected.

**Root Cause**: With `hedging=True` and default full-equity sizing, overlapping positions exhaust available margin.

**Fix**: Use fixed fractional sizing:

```python
self.buy(size=0.01)  # 1% equity per trade
```

### BP-06: Signal Timestamp vs Entry Timestamp (LOW)

**Symptom**: Gate 2 (timestamp match) fails because SQL uses signal bar timestamps while Python uses entry bar timestamps.

**Root Cause**: SQL outputs the signal detection bar's `timestamp_ms`. Python's `EntryTime` is the fill bar (next bar after signal). These differ by 1 bar.

**Fix**: Record signal bar timestamps in the strategy's `next()` method:

```python
# Before calling self.buy()
self._signal_timestamps.append(int(self.data.index[-1].timestamp() * 1000))
```

---

## 5-Gate Oracle Validation Framework

| Gate | Metric          | Threshold | What it catches                      |
| ---- | --------------- | --------- | ------------------------------------ |
| 1    | Signal Count    | <5% diff  | Missing signals, filter misalignment |
| 2    | Timestamp Match | >95%      | Timing offset, warmup differences    |
| 3    | Entry Price     | >95%      | Price source mismatch, sort ordering |
| 4    | Exit Type       | >90%      | Barrier logic differences            |
| 5    | Kelly Fraction  | <0.02     | Aggregate outcome alignment          |

**Expected residual**: 1-2 exit type mismatches per asset at TIME barrier boundary (bar 50). SQL uses `fwd_closes[max_bars]`, backtesting.py closes at current bar price. Impact on Kelly < 0.006.

---

## Strategy Architecture: Single vs Multi-Position

| Mode            | Constructor                            | Use Case              | Position Sizing                |
| --------------- | -------------------------------------- | --------------------- | ------------------------------ |
| Single-position | `hedging=False` (default)              | Champion 1-bar hold   | Full equity                    |
| Multi-position  | `hedging=True, exclusive_orders=False` | SQL oracle validation | Fixed fractional (`size=0.01`) |

### Multi-Position Strategy Template

```python
class Gen600Strategy(Strategy):
    def next(self):
        current_bar = len(self.data) - 1

        # 1. Register newly filled trades and set barriers
        for trade in self.trades:
            tid = id(trade)
            if tid not in self._known_trades:
                self._known_trades.add(tid)
                self._trade_entry_bar[tid] = current_bar
                actual_entry = trade.entry_price
                if self.tp_mult > 0:
                    trade.tp = actual_entry * (1.0 + self.tp_mult * self.threshold_pct)
                if self.sl_mult > 0:
                    trade.sl = actual_entry * (1.0 - self.sl_mult * self.threshold_pct)

        # 2. Check time barrier for each open trade
        for trade in list(self.trades):
            tid = id(trade)
            entry_bar = self._trade_entry_bar.get(tid, current_bar)
            if self.max_bars > 0 and (current_bar - entry_bar) >= self.max_bars:
                trade.close()
                self._trade_entry_bar.pop(tid, None)

        # 3. Check for new signal (no position guard — overlapping allowed)
        if self._is_signal[current_bar]:
            self.buy(size=0.01)
```

---

## Data Loading

```python
from data_loader import load_range_bars

df = load_range_bars(
    symbol="SOLUSDT",
    threshold=1000,
    start="2017-01-01",      # Cover all available data
    end="2025-02-05",        # Match SQL cutoff
    extra_columns=["volume_per_trade", "lookback_price_range"],  # Gen600 features
)
```

---

## Project Artifacts (rangebar-patterns repo)

| Artifact                    | Path                                              |
| --------------------------- | ------------------------------------------------- |
| Oracle comparison script    | `scripts/gen600_oracle_compare.py`                |
| Gen600 strategy (reference) | `backtest/backtesting_py/gen600_strategy.py`      |
| SQL oracle query template   | `sql/gen600_oracle_trades.sql`                    |
| Oracle validation findings  | `findings/2026-02-12-gen600-oracle-validation.md` |
| Backtest CLAUDE.md          | `backtest/CLAUDE.md`                              |
| ClickHouse AP-16            | `.claude/skills/clickhouse-antipatterns/SKILL.md` |
| Fork source                 | `~/fork-tools/backtesting.py/`                    |
