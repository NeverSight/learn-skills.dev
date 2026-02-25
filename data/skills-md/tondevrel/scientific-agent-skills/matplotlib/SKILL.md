---
name: matplotlib
description: The foundational library for creating static, animated, and interactive visualizations in Python. Highly customizable and the industry standard for publication-quality figures. Use for 2D plotting, scientific data visualization, heatmaps, contours, vector fields, multi-panel figures, LaTeX-formatted plots, custom visualization tools, and plotting from NumPy arrays or Pandas DataFrames.
version: 3.8
license: PSF
---

# Matplotlib - Data Visualization

The most widely used library for 2D (and basic 3D) plotting. It provides full control over every element of a figure, from line styles to axis spines.

## When to Use

- Creating publication-quality 2D plots (Line, Scatter, Bar, Hist)
- Visualizing scientific data (Heatmaps, Contours, Vector fields)
- Generating complex multi-panel figures
- Fine-tuning plots for papers/reports (LaTeX support)
- Building custom visualization tools and dashboards
- Plotting data directly from NumPy arrays or Pandas DataFrames

## Reference Documentation

**Official docs**: https://matplotlib.org/stable/index.html  
**Gallery**: https://matplotlib.org/stable/gallery/index.html (Essential for finding examples)  
**Search patterns**: `plt.subplots`, `ax.set_title`, `ax.legend`, `plt.savefig`, `matplotlib.colors`

## Core Principles

### Two Interfaces: Choose Wisely

| Interface | Method | Use Case |
|-----------|--------|----------|
| Object-Oriented (OO) | `fig, ax = plt.subplots()` | Recommended. Best for complex, reproducible plots. |
| Pyplot (State-based) | `plt.plot(x, y)` | Quick interactive checks. Avoid for scripts/modules. |

### Use Matplotlib For

- High-level control over figure layout.
- Precise styling for publication.
- Embedding plots in GUI applications.

### Do NOT Use For

- Interactive web dashboards (use Plotly or Bokeh).
- Rapid statistical exploration (use Seaborn — it's built on Matplotlib but simpler for stats).
- Very large datasets (>1M points) in real-time (use Datashader or VisPy).

## Quick Reference

### Installation

```bash
pip install matplotlib
```

### Standard Imports

```python
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import gridspec
```

### Basic Pattern - The OO Interface (The "Proper" Way)

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)

# 1. Create Figure and Axis objects
fig, ax = plt.subplots(figsize=(8, 5))

# 2. Plot data
ax.plot(x, y, label='Sine Wave', color='tab:blue', linewidth=2)

# 3. Customize
ax.set_xlabel('Time (s)')
ax.set_ylabel('Amplitude')
ax.set_title('Oscillation Example')
ax.legend()
ax.grid(True, linestyle='--')

# 4. Show or Save
plt.show()
# fig.savefig('plot.pdf', dpi=300, bbox_inches='tight')
```

## Critical Rules

### ✅ DO

- Use the OO interface (`ax.method()`) - It prevents errors in multi-plot scripts.
- Use `bbox_inches='tight'` - When saving, to ensure labels aren't cut off.
- Set dpi - Use 300+ for print, 72-100 for web.
- Close figures - Use `plt.close('all')` in loops to avoid memory leaks.
- Label everything - Every axis must have a label and units.
- Vector formats - Save as `.pdf` or `.svg` for academic papers (lossless scaling).
- Colorblind-friendly - Use `tab10` or `viridis` colormaps.

### ❌ DON'T

- Mix `plt.` and `ax.` - It leads to "hidden state" bugs.
- Use `plt.show()` in loops - It blocks execution; use `fig.savefig()` instead.
- Manual legend placement - Let `ax.legend(loc='best')` try first.
- Hardcode font sizes - Use `plt.rcParams.update({'font.size': 12})` for consistency.
- Use "Rainbow" (Jet) - It creates false gradients; use perceptually uniform maps like `magma` or `inferno`.

## Anti-Patterns (NEVER)

```python
# ❌ BAD: Mixing interfaces (State-based + OO)
plt.figure()
ax = plt.gca()
plt.plot(x, y) # Confusing state
ax.set_title('Test')

# ✅ GOOD: Consistent OO interface
fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_title('Test')

# ❌ BAD: Overlapping subplots
fig, axs = plt.subplots(2, 2)
# Plots look squashed and titles overlap

# ✅ GOOD: Use constrained_layout or tight_layout
fig, axs = plt.subplots(2, 2, constrained_layout=True)
```

## Anatomy of a Plot

### Labels, Ticks, and Styles

```python
fig, ax = plt.subplots()

ax.plot(x, y, 'o-', color='red', markersize=4, alpha=0.7)

# Explicitly setting limits
ax.set_xlim(0, 10)
ax.set_ylim(-1.5, 1.5)

# Controlling Ticks
ax.set_xticks([0, 2.5, 5, 7.5, 10])
ax.set_xticklabels(['Start', '1/4', 'Mid', '3/4', 'End'])

# Spines (Box around the plot)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Adding text and arrows
ax.annotate('Local Max', xy=(1.5, 1), xytext=(3, 1.2),
             arrowprops=dict(facecolor='black', shrink=0.05))
```

## Advanced Layouts

### Subplots and GridSpec

```python
# Simple 2x2 grid
fig, axs = plt.subplots(2, 2, figsize=(10, 10))
axs[0, 0].plot(x, y) # Top left
axs[1, 1].scatter(x, y) # Bottom right

# Complex grid (Uneven sizes)
fig = plt.figure(figsize=(10, 6))
gs = gridspec.GridSpec(2, 2, width_ratios=[2, 1], height_ratios=[1, 2])

ax1 = fig.add_subplot(gs[0, 0]) # Top left (large width)
ax2 = fig.add_subplot(gs[0, 1]) # Top right
ax3 = fig.add_subplot(gs[1, :]) # Bottom spanning all columns
```

## Scientific Plot Types

### Heatmaps and Colorbars

```python
data = np.random.rand(10, 10)

fig, ax = plt.subplots()
im = ax.imshow(data, cmap='viridis', interpolation='nearest')

# Add colorbar
cbar = fig.colorbar(im, ax=ax, label='Intensity [a.u.]')

# Proper alignment of colorbar
from mpl_toolkits.axes_grid1 import make_axes_locatable
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)
fig.colorbar(im, cax=cax)
```

### Histograms and Error Bars

```python
# Histogram
data = np.random.normal(0, 1, 1000)
ax.hist(data, bins=30, density=True, alpha=0.6, color='g', edgecolor='black')

# Error bars
x = np.arange(10)
y = x**2
yerr = np.sqrt(y)
ax.errorbar(x, y, yerr=yerr, fmt='o', capsize=5, label='Data with noise')
```

### 3D Plotting

```python
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

X = np.arange(-5, 5, 0.25)
Y = np.arange(-5, 5, 0.25)
X, Y = np.meshgrid(X, Y)
R = np.sqrt(X**2 + Y**2)
Z = np.sin(R)

surf = ax.plot_surface(X, Y, Z, cmap='coolwarm', linewidth=0, antialiased=False)
fig.colorbar(surf, shrink=0.5, aspect=5)
```

## Formatting for Publication

### Using LaTeX and RcParams

```python
# Global styling
plt.style.use('seaborn-v0_8-paper') # or 'ggplot', 'bmh'

# LaTeX for labels
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],
    "axes.labelsize": 14,
})

fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_xlabel(r'$\alpha_{i} + \beta \sin(\omega t)$') # LaTeX string
```

## Practical Workflows

### 1. Multi-dataset Comparison Workflow

```python
def plot_comparison(datasets, labels):
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = plt.cm.viridis(np.linspace(0, 1, len(datasets)))
    
    for data, label, color in zip(datasets, labels, colors):
        ax.plot(data['x'], data['y'], label=label, color=color, lw=1.5)
        ax.fill_between(data['x'], data['y']-data['std'], data['y']+data['std'], 
                        alpha=0.2, color=color)
    
    ax.set_title('Experiment Results Comparison')
    ax.legend(frameon=False)
    return fig, ax
```

### 2. Monitoring Real-time Data (Interactive)

```python
# Use this in a Jupyter environment or script
plt.ion() # Interactive mode on
fig, ax = plt.subplots()
line, = ax.plot([], [])

for i in range(100):
    new_data = np.random.rand(10)
    line.set_data(np.arange(len(new_data)), new_data)
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.pause(0.1)
```

### 3. Creating a Cluster Map / Correlation Matrix

```python
import pandas as pd

df = pd.DataFrame(np.random.rand(10, 4), columns=['A', 'B', 'C', 'D'])
corr = df.corr()

fig, ax = plt.subplots()
im = ax.imshow(corr, cmap='RdBu_r', vmin=-1, vmax=1)
ax.set_xticks(np.arange(len(corr.columns)), labels=corr.columns)
ax.set_yticks(np.arange(len(corr.index)), labels=corr.index)

# Loop over data dimensions and create text annotations.
for i in range(len(corr.index)):
    for j in range(len(corr.columns)):
        text = ax.text(j, i, f"{corr.iloc[i, j]:.2f}",
                       ha="center", va="center", color="black")
```

## Performance Optimization

### Plotting Large Data

```python
# 1. Use 'agg' backend for non-interactive rendering
import matplotlib
matplotlib.use('Agg')

# 2. Use PathCollection for scatter plots with many points
ax.scatter(x, y, s=1) # slow for 1M points

# 3. Use marker='' (none) and only lines for speed
ax.plot(x, y, marker=None)

# 4. Decimate data before plotting
ax.plot(x[::10], y[::10]) # Plot every 10th point
```

## Common Pitfalls and Solutions

### Date/Time Axis issues

```python
# ❌ Problem: Dates look like a black blob
# ✅ Solution: Use AutoDateLocator and AutoDateFormatter
import matplotlib.dates as mdates

fig, ax = plt.subplots()
ax.plot(dates, values)
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
fig.autofmt_xdate() # Rotates labels
```

### Multiple Legends on one plot

```python
# ❌ Problem: Calling ax.legend() twice replaces the first one
# ✅ Solution: Manually add the first artist back
fig, ax = plt.subplots()
line1, = ax.plot([1, 2], [1, 2], label='Line 1')
line2, = ax.plot([1, 2], [2, 1], label='Line 2')

first_legend = ax.legend(handles=[line1], loc='upper left')
ax.add_artist(first_legend) # Add back
ax.legend(handles=[line2], loc='lower right')
```

### Image Saving Quality (Clipping)

```python
# ❌ Problem: Legend or Axis title is cut off in the .png file
# ✅ Solution:
fig.savefig('output.png', bbox_inches='tight')
```

## Best Practices

1. **Always use the OO interface** (`fig, ax = plt.subplots()`) for scripts and modules
2. **Save figures with appropriate formats** - Use PDF/SVG for publications, PNG for web
3. **Set DPI appropriately** - 300+ for print, 72-100 for screen
4. **Use `bbox_inches='tight'`** when saving to prevent clipping
5. **Close figures in loops** to prevent memory leaks
6. **Use colorblind-friendly colormaps** - Avoid 'jet', prefer 'viridis', 'plasma', 'inferno'
7. **Label all axes** with descriptive names and units
8. **Use `constrained_layout=True`** for subplots to prevent overlap
9. **Configure global styles** with `plt.rcParams` for consistency
10. **Test plots at target resolution** before finalizing
