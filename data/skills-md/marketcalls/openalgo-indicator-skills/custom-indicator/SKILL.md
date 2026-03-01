---
name: custom-indicator
description: Create a custom technical indicator using Numba JIT + NumPy. Generates production-grade, O(n) optimized indicator functions with charting and benchmarking.
argument-hint: "[indicator-name]"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Create a custom technical indicator with Numba JIT compilation for production-grade speed.

## Arguments

- `$0` = indicator name (e.g., zscore, squeeze, vwap-bands, custom-rsi, mean-reversion). Required.

If no arguments, ask the user what indicator they want to build.

## Instructions

1. Read the indicator-expert rules, especially:
   - `rules/custom-indicators.md` — Numba patterns and templates
   - `rules/numba-optimization.md` — Performance best practices
   - `rules/indicator-catalog.md` — Check if indicator already exists in openalgo.ta
2. **Check first**: If the indicator already exists in `openalgo.ta`, tell the user and show the existing API
3. Create `custom_indicators/{indicator_name}/` directory (on-demand)
4. Create `{indicator_name}.py` with:

### File Structure

```python
"""
{Indicator Name} — Custom Indicator
Description: {what it measures}
Category: {trend/momentum/volatility/volume/oscillator}
"""
import numpy as np
from numba import njit
import pandas as pd

# --- Core Computation (Numba JIT) ---
@njit(cache=True, nogil=True)
def _compute_{name}(data: np.ndarray, period: int) -> np.ndarray:
    """Numba-compiled core computation."""
    n = len(data)
    result = np.full(n, np.nan)
    # ... O(n) algorithm ...
    return result

# --- Public API ---
def {name}(data, period=20):
    """
    {Indicator Name}

    Args:
        data: Close prices (numpy array, pandas Series, or list)
        period: Lookback period (default: 20)

    Returns:
        Same type as input with indicator values
    """
    if isinstance(data, pd.Series):
        idx = data.index
        result = _compute_{name}(data.values.astype(np.float64), period)
        return pd.Series(result, index=idx, name="{Name}({period})")
    arr = np.asarray(data, dtype=np.float64)
    return _compute_{name}(arr, period)
```

5. Create `chart.py` for visualization:

```python
"""Chart the custom indicator with Plotly."""
import os
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import find_dotenv, load_dotenv
from openalgo import api, ta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from {indicator_name} import {name}

# ... fetch data, compute indicator, create chart ...
```

6. Create `benchmark.py` for performance testing:

```python
"""Benchmark the custom indicator."""
import numpy as np
import time
from {indicator_name} import {name}

# Warmup
data = np.random.randn(1000)
_ = {name}(data, 20)

# Benchmark on different sizes
for size in [10_000, 100_000, 500_000]:
    data = np.random.randn(size)
    t0 = time.perf_counter()
    _ = {name}(data, 20)
    elapsed = (time.perf_counter() - t0) * 1000
    print(f"{size:>10,} bars: {elapsed:>8.2f}ms")
```

## Numba Rules (CRITICAL)

### MUST DO
- `@njit(cache=True, nogil=True)` on all compute functions
- `np.full(n, np.nan)` to initialize output arrays
- Use `np.isnan()` for NaN checks
- Explicit `for` loops (Numba compiles to machine code)
- O(n) algorithms: rolling sum, EMA recursion, deque-based extrema
- Float64 for all numeric arrays

### MUST NOT
- Never `fastmath=True` (breaks `np.isnan()`)
- Never use pandas inside `@njit`
- Never use try/except, dicts, sets, strings inside `@njit`
- Never call non-jitted functions from inside `@njit`

### Available Building Blocks

These existing functions can be called inside `@njit`:

```python
from openalgo.indicators.utils import (
    sma, ema, ema_wilder, stdev, true_range, atr_wilder,
    highest, lowest, rolling_sum, crossover, crossunder
)
```

## Common Custom Indicator Patterns

| Pattern | Implementation |
|---------|---------------|
| Z-Score | `(value - rolling_mean) / rolling_stdev` |
| Squeeze | Bollinger inside Keltner channel |
| VWAP Bands | VWAP + N * rolling stdev of (close - vwap) |
| Momentum Score | Weighted sum of RSI + MACD + ADX conditions |
| Mean Reversion | Distance from SMA as % + threshold |
| Range Filter | ATR-based dynamic filter on close |
| Trend Strength | ADX + directional movement composite |

## Example Usage

`/custom-indicator zscore`
`/custom-indicator squeeze-momentum`
`/custom-indicator vwap-bands`
`/custom-indicator range-filter`
