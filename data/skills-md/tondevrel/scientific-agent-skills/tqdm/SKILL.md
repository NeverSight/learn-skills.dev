---
name: tqdm
description: A fast, extensible progress bar for Python and CLI. Instantly makes your loops show a smart progress meter with ETA, iterations per second, and customizable statistics. Minimal overhead. Use for monitoring long-running loops, simulations, data processing, ML training, file downloads, I/O operations, command-line tools, pandas operations, parallel tasks, and nested progress bars.
version: 4.66
license: MIT / MPL-2.0
---

# tqdm - Intelligent Progress Bars

tqdm is the standard tool for monitoring long-running loops in Python. It has negligible overhead (about 60ns per iteration) and works everywhere: in the console, in Jupyter notebooks, and even in GUIs.

## When to Use

- Monitoring long-running loops (simulations, data processing, ML training).
- Tracking progress of file downloads or I/O operations.
- Providing visual feedback in command-line tools.
- Integrating progress tracking into pandas operations (progress_apply).
- Monitoring parallel tasks in concurrent.futures or multiprocessing.
- Creating nested progress bars for hierarchical tasks (e.g., epochs and batches).

## Reference Documentation

**Official docs**: https://tqdm.github.io/  
**GitHub**: https://github.com/tqdm/tqdm  
**Search patterns**: `from tqdm import tqdm`, `tqdm.pandas()`, `tqdm.notebook`, `tqdm.contrib`

## Core Principles

### Iterative Wrapper
The simplest way to use tqdm is to wrap any iterable: `for item in tqdm(iterable):`. It automatically calculates the length and estimates the time remaining.

### Low Overhead
tqdm is written to be extremely fast. It uses smart algorithms to limit the number of display updates so it doesn't slow down your actual computation.

### Integration
tqdm has specialized modules for different environments (Jupyter, Keras, Pandas, Slack/Telegram notifications).

## Quick Reference

### Installation

```bash
pip install tqdm
```

### Standard Imports

```python
from tqdm import tqdm
import time

# For Jupyter Notebooks specifically:
# from tqdm.notebook import tqdm
```

### Basic Pattern - Automatic Loop Tracking

```python
import time
from tqdm import tqdm

# Just wrap the range or list
for i in tqdm(range(1000)):
    time.sleep(0.01) # Simulate work
```

## Critical Rules

### ✅ DO

- **Use desc** - Add a description to the bar so you know exactly which process is running (`tqdm(range(10), desc="Processing")`).
- **Use leave=False for nested loops** - This cleans up the inner bars after they finish, preventing console clutter.
- **Use the notebook version** - In Jupyter, use `from tqdm.notebook import tqdm` for pretty HTML bars.
- **Set total manually** - If your iterator doesn't have a `__len__`, provide the `total` parameter manually.
- **Integrate with Pandas** - Use `tqdm.pandas()` to see progress on `.progress_apply()`.
- **Close manual bars** - If using the manual `pbar = tqdm(...)` approach, always use a `with` statement or call `pbar.close()`.

### ❌ DON'T

- **Update too often** - Avoid manual updates in tight loops (e.g., millions of updates per second); tqdm handles this automatically if you wrap the iterator.
- **Print to console inside tqdm** - Standard `print()` will break the bar. Use `tqdm.write("message")` instead.
- **Ignore overhead** - While low, if your loop body is sub-microsecond, any overhead matters; process in batches instead.
- **Forget ascii=True** - If working on old terminals or Windows CMD without Unicode support, use `ascii=True` to avoid garbled characters.

## Anti-Patterns (NEVER)

```python
from tqdm import tqdm
import time

# ❌ BAD: Mixing print() and tqdm (Corrupts the bar)
for i in tqdm(range(5)):
    print(f"Doing step {i}") # Bar jumps to next line
    time.sleep(0.1)

# ✅ GOOD: Use tqdm.write()
for i in tqdm(range(5)):
    tqdm.write(f"Doing step {i}") # Bar stays at the bottom
    time.sleep(0.1)

# ❌ BAD: Manual update without closing (Potential memory leak/UI hang)
pbar = tqdm(total=100)
for i in range(100):
    pbar.update(1)
# Missing pbar.close()!

# ✅ GOOD: Use context manager
with tqdm(total=100) as pbar:
    for i in range(100):
        pbar.update(1)

# ❌ BAD: Wrapping an iterator with no length without 'total'
# tqdm(my_generator) # Shows count but no progress bar/ETA
```

## Advanced Usage and Customization

### Descriptions and Statistics

```python
pbar = tqdm(range(100))
for i in pbar:
    # Update description dynamically
    pbar.set_description(f"Processing Step {i}")
    
    # Add custom stats (e.g., loss in ML)
    pbar.set_postfix(loss=0.5/(i+1), accuracy=i/100)
    time.sleep(0.05)
```

### Manual Control (For Non-Iterative Work)

```python
# Useful for tracking bytes in file I/O or API calls
with tqdm(total=1024, unit='B', unit_scale=True, desc="Downloading") as pbar:
    # Simulate chunked download
    for chunk_size in [256, 128, 512, 128]:
        time.sleep(0.5)
        pbar.update(chunk_size)
```

## Integration with Ecosystems

### Pandas Integration

```python
import pandas as pd
from tqdm import tqdm

# Initialize tqdm for pandas
tqdm.pandas(desc="Cleaning Data")

df = pd.DataFrame({'val': range(10000)})

# Use progress_apply instead of apply
result = df['val'].progress_apply(lambda x: x**2)
```

### Nested Progress Bars

```python
# Perfect for Epochs vs Batches in deep learning
for epoch in tqdm(range(3), desc="Epochs"):
    for batch in tqdm(range(10), desc="Batches", leave=False):
        time.sleep(0.05)
```

### Parallel Processing (concurrent.futures)

```python
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

def work(n):
    time.sleep(0.1)
    return n * 2

data = range(50)
with ThreadPoolExecutor() as executor:
    # Use tqdm to monitor map results
    results = list(tqdm(executor.map(work, data), total=len(data)))
```

## Practical Workflows

### 1. Large File Reader with Progress

```python
import os

def read_large_file(filepath):
    """Read a file while showing a progress bar based on bytes."""
    file_size = os.path.getsize(filepath)
    with tqdm(total=file_size, unit='B', unit_scale=True, unit_divisor=1024) as pbar:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                # Process chunk
                pbar.update(len(chunk))
```

### 2. Scientific Simulation Suite

```python
def run_simulation_suite(configs):
    """Run multiple simulations and log failures."""
    results = []
    with tqdm(configs, desc="Suite") as pbar:
        for config in pbar:
            try:
                res = run_single_sim(config)
                results.append(res)
            except Exception as e:
                tqdm.write(f"Error in config {config}: {e}")
            pbar.set_postfix(success=len(results))
    return results
```

### 3. Training Loop with Custom Postfix

```python
def train_model(epochs, data_loader):
    pbar = tqdm(range(epochs), desc="Training")
    for epoch in pbar:
        loss = compute_loss() # dummy
        acc = compute_acc()   # dummy
        
        # Update the bar with current metrics
        pbar.set_postfix(loss=f"{loss:.4f}", acc=f"{acc:.2%}")
```

## Performance Optimization

### The mininterval parameter

By default, tqdm updates every 0.1 seconds. If your terminal is slow (e.g., over SSH or a legacy GUI), increase `mininterval` to 1.0 or 5.0 to reduce network/I/O traffic.

```python
for i in tqdm(range(1000000), mininterval=1.0):
    pass
```

### Disabling tqdm in Production

You can globally disable bars (e.g., when running in a CI/CD environment or a non-interactive log) by setting `disable=True`.

```python
import os
# Check for environment variable
is_ci = os.environ.get('CI') == 'true'
for i in tqdm(range(100), disable=is_ci):
    pass
```

## Common Pitfalls and Solutions

### The "Double Bar" Glitch

In Jupyter, sometimes bars don't close properly, leading to stacks of red/green bars.

```python
# ✅ Solution: Always use a 'with' statement or try-finally
# Or clear all instances if stuck:
from tqdm import tqdm
tqdm._instances.clear()
```

### Unicode Error on Windows

Windows CMD (non-Terminal) often struggles with the smooth progress blocks.

```python
# ✅ Solution: Use ASCII characters only
for i in tqdm(range(100), ascii=True):
    pass
```

### Multiple Bars Alignment

If your bars are overlapping or jumping:

```python
# ✅ Solution: Specify the position explicitly
# Useful for manual multi-threading
pbar1 = tqdm(total=100, position=0)
pbar2 = tqdm(total=100, position=1)
```

tqdm is a small addition to a script that provides immense psychological relief. It provides the "pulse" of your code, ensuring you are always aware of how your long-running scientific tasks are progressing.
