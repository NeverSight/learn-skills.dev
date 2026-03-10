---
name: matplotlib-pro
description: Professional sub-skill for Matplotlib focused on high-performance animations, complex multi-figure layouts (GridSpec), interactive widgets, and publication-ready typography (LaTeX/PGF).
version: 3.8
license: PSF
---

# Matplotlib - Professional Viz & Animation

Beyond static plots, Matplotlib is a powerful engine for dynamic data visualization and scientific storytelling. This guide focuses on the "Pro" features: blitting for speed, Artist hierarchy for control, and LaTeX integration for papers.

## When to Use

- Creating high-FPS animations for simulations (Fluid dynamics, N-body).
- Building custom interactive tools inside Jupyter or a GUI.
- Generating pixel-perfect figures for academic journals.
- Visualizing real-time data streams from sensors.

## Core Principles

### 1. The Artist Hierarchy

Everything you see is an Artist. Figures contain Axes, Axes contain Lines, Text, Patches. Pro-level control means manipulating these objects directly instead of using high-level `plt` commands.

### 2. Blitting (The Secret to Speed)

Standard animation redraws the whole figure every frame (slow). Blitting only redraws the parts that changed (e.g., the moving line), while keeping the axes and labels cached as a background image.

### 3. Backend Mastery

- **Agg**: High-quality static PNGs.
- **PDF/PGF**: Vector-based for LaTeX.
- **TkAgg/QtAgg**: Interactive windows.

## High-Performance Animation

### Using FuncAnimation with Blitting

```python
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2) # Returns the Line2D artist

def init():
    ax.set_xlim(0, 2*np.pi)
    ax.set_ylim(-1, 1)
    return line, # Note the comma

def update(frame):
    x = np.linspace(0, 2*np.pi, 100)
    y = np.sin(x + frame/10.0)
    line.set_data(x, y)
    return line,

# blit=True is critical for performance
ani = FuncAnimation(fig, update, frames=100, init_func=init, blit=True)
plt.show()
```

## Publication Standards

### 1. LaTeX & PGF Backend (For Papers)

```python
import matplotlib as mpl

mpl.use("pgf") # Use PGF for perfect LaTeX integration
mpl.rcParams.update({
    "pgf.texsystem": "pdflatex",
    "font.family": "serif",
    "text.usetex": True,
    "pgf.rcfonts": False,
})

fig.savefig("figure.pgf") # Import this directly into your LaTeX doc
```

### 2. Complex GridSpec Layouts

```python
import matplotlib.gridspec as gridspec

fig = plt.figure(constrained_layout=True)
gs = gridspec.GridSpec(3, 3, figure=fig)

ax_main = fig.add_subplot(gs[0:2, :]) # Top 2/3rds
ax_hist_x = fig.add_subplot(gs[2, 0:2]) # Bottom left
ax_hist_y = fig.add_subplot(gs[2, 2]) # Bottom right
```

## Interactive Widgets

### Custom Sliders and Buttons

```python
from matplotlib.widgets import Slider

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)
line, = ax.plot(x, np.sin(x))

ax_freq = plt.axes([0.25, 0.1, 0.65, 0.03])
slider = Slider(ax_freq, 'Freq', 0.1, 30.0, valinit=1.0)

def update(val):
    line.set_ydata(np.sin(slider.val * x))
    fig.canvas.draw_idle() # Optimized redraw

slider.on_changed(update)
```

## Critical Rules

### ✅ DO

- **Use fig.canvas.draw_idle()** - It tells Matplotlib to redraw only when the event loop is free, preventing UI lag.
- **Vectorize Text** - Save as `.svg` or `.pdf` to ensure labels don't pixelate in reports.
- **Close your animations** - Use `plt.close()` to prevent memory leaks in notebooks.
- **Use ArtistAnimation** - If you already have all frames calculated as images, ArtistAnimation is faster than FuncAnimation.

### ❌ DON'T

- **Don't use plt.pause() in heavy loops** - It's inefficient; use the animation framework.
- **Don't hardcode "inches"** - Use `fig.get_size_inches()` and scale relative to the figure size for portability.
- **Don't ignore Tight Layout** - Overlapping subplots are a common "amateur" mistake. Use `fig.set_constrained_layout(True)`.

Matplotlib Pro is the bridge between data and insight. Mastering the blitting engine and the PGF backend allows scientists to create dynamic evidence that is as visually compelling as it is mathematically rigorous.
