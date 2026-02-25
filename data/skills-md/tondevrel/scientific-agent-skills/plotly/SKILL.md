---
name: plotly
description: A high-level interactive graphing library for Python. Ideal for web-based visualizations, 3D plots, and complex interactive dashboards. Built on plotly.js, it allows users to zoom, pan, and hover over data points in a browser-based environment. Use for interactive charts, web applications, Jupyter notebooks, 3D data visualization, geographic maps, financial charts, animations, time-series analysis, and building production-ready dashboards with Dash.
version: 5.18
license: MIT
---

# Plotly - Interactive Visualization

Plotly provides a wide range of interactive charts. Its "Plotly Express" API is designed for speed and ease of use with tidy DataFrames, while "Graph Objects" offers low-level control over every trace and attribute.

## When to Use

- Creating interactive charts for web applications or Jupyter notebooks
- Visualizing 3D data (surfaces, scatter, mesh)
- Geographic maps (scatter on maps, choropleths) with Mapbox integration
- Financial charts (candlestick, OHLC)
- Exploring large datasets where zooming into specific regions is required
- Creating animations (time-series sliders)
- Building production-ready dashboards (via Dash)

## Reference Documentation

**Official docs**: https://plotly.com/python/  
**Plotly Express**: https://plotly.com/python/plotly-express/  
**Search patterns**: `px.scatter`, `go.Figure`, `fig.update_layout`, `fig.write_html`, `px.choropleth`

## Core Principles

### Plotly Express (px) vs. Graph Objects (go)

| Feature | Plotly Express (px) | Graph Objects (go) |
|---------|---------------------|-------------------|
| Complexity | High-level, concise. | Low-level, verbose. |
| Data Format | Tidy (long-form) DataFrames. | Lists, Arrays, Dicts, or DataFrames. |
| Customization | Good (using update_*). | Maximum / Full control. |
| Speed of Dev | Very fast. | Slower. |

### Use Plotly For

- Interactive exploration (hover, zoom)
- 3D and Geospatial visualization
- Exporting to standalone interactive HTML files
- Integration with Dash

### Do NOT Use For

- Publication-quality static LaTeX plots (use Matplotlib)
- Very large static image generation (Matplotlib is faster)
- Low-memory environments (Plotly's JSON-based figures are memory-heavy)

## Quick Reference

### Installation

```bash
pip install plotly pandas
```

### Standard Imports

```python
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
```

### Basic Pattern - Plotly Express

```python
import plotly.express as px

# Load data
df = px.data.iris()

# Create interactive scatter plot
fig = px.scatter(df, x="sepal_width", y="sepal_length", 
                 color="species", size="petal_length",
                 hover_data=['petal_width'])

# Display
fig.show()
```

## Critical Rules

### ✅ DO

- Use Plotly Express first - 90% of tasks are easier with px
- Prefer Tidy Data - Ensure one row per observation for easy mapping to colors/axes
- Use update_layout - Cleanly modify titles, fonts, and background colors
- Save as HTML - Use `fig.write_html("plot.html")` to share interactive charts
- Leverage Hover Data - Add context to points without cluttering the plot
- Set Figure Templates - Use `template="plotly_dark"` or `"ggplot2"` for instant style
- Use marginal_x/y - In px.scatter, quickly add histograms or boxplots to margins

### ❌ DON'T

- Pass huge datasets to the browser - Plotting >50k points can lag the UI; use datashader or decimation
- Manual looping with go - If px can do it, don't use a for-loop to add traces in go
- Forget to set axis labels - px uses column names; rename them in the DataFrame for better labels
- Over-animate - Smooth animations are cool, but too many moving parts distract from the data

## Anti-Patterns (NEVER)

```python
# ❌ BAD: Over-complicating a simple plot with Graph Objects
fig = go.Figure()
for species in df['species'].unique():
    sub = df[df['species'] == species]
    fig.add_trace(go.Scatter(x=sub['sepal_w'], y=sub['sepal_l'], name=species))

# ✅ GOOD: Use Plotly Express (One line, automatic legend/colors)
fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species")

# ❌ BAD: Mixing list-style data with DataFrame-style data in px
px.scatter(x=[1,2,3], y=df['column']) # Can lead to alignment issues

# ✅ GOOD: Stick to the DataFrame
px.scatter(df, x="column_a", y="column_b")
```

## Plotly Express (px) Deep Dive

### Statistical Charts

```python
# Boxplot with points
fig = px.box(df, x="day", y="total_bill", color="smoker", points="all")

# Violin plot with box inside
fig = px.violin(df, x="day", y="total_bill", color="sex", box=True, points="all")

# Heatmap (Density Contour)
fig = px.density_heatmap(df, x="total_bill", y="tip", marginal_x="histogram", marginal_y="histogram")
```

### Time Series and Faceting

```python
df = px.data.stocks()
# Multiple lines from wide data
fig = px.line(df, x='date', y=["GOOG", "AAPL", "AMZN"], title="Tech Stocks")

# Faceting (Subplots by category)
df = px.data.tips()
fig = px.scatter(df, x="total_bill", y="tip", color="smoker", 
                 facet_col="day", facet_row="time")
```

## 3D Visualization

### Scatter, Lines, and Surfaces

```python
# 3D Scatter
fig = px.scatter_3d(df, x='sepal_length', y='sepal_width', z='petal_width', color='species')

# 3D Surface (Using Graph Objects)
z_data = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/api_docs/mt_bruno_elevation.csv')
fig = go.Figure(data=[go.Surface(z=z_data.values)])
fig.update_layout(title='Mt Bruno Elevation', autosize=False,
                  width=500, height=500, margin=dict(l=65, r=50, b=65, t=90))
```

## Geospatial Analysis

### Maps and Choropleths

```python
# Scatter on a map
df = px.data.gapminder().query("year == 2007")
fig = px.scatter_geo(df, locations="iso_alpha", color="continent",
                     hover_name="country", size="pop",
                     projection="natural earth")

# Detailed Mapbox Choropleth (Needs token or use open-street-map)
fig = px.choropleth_mapbox(df, geojson=counties, locations='fips', color='unemp',
                           color_continuous_scale="Viridis",
                           mapbox_style="carto-positron",
                           zoom=3, center = {"lat": 37.0902, "lon": -95.7129})
```

## Layout and Styling (fig.update_*)

### Fine-tuning the appearance

```python
fig = px.scatter(df, x="x", y="y")

# Global layout updates
fig.update_layout(
    title="Custom Styled Plot",
    xaxis_title="Dimension X",
    yaxis_title="Dimension Y",
    font=dict(family="Courier New, monospace", size=18, color="RebeccaPurple"),
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
    plot_bgcolor="white"
)

# Axis specific updates
fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightPink')
fig.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor='Black')
```

## Advanced Interaction: Animations

```python
df = px.data.gapminder()
fig = px.scatter(df, x="gdpPercap", y="lifeExp", animation_frame="year", 
                 animation_group="country",
                 size="pop", color="continent", hover_name="country",
                 log_x=True, size_max=55, range_x=[100, 100000], range_y=[25, 90])
```

## Practical Workflows

### 1. Interactive Scientific Report Export

```python
def create_interactive_report(df, filename="report.html"):
    """Generates a multi-chart HTML report."""
    fig1 = px.scatter(df, x="A", y="B", color="C")
    fig2 = px.histogram(df, x="A", color="C")
    
    with open(filename, 'a') as f:
        f.write(fig1.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig2.to_html(full_html=False, include_plotlyjs='cdn'))

# Useful for sharing findings with non-technical stakeholders
```

### 2. Financial Dashboard Fragment (Candlestick)

```python
import pandas as pd
from datetime import datetime

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')

fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                open=df['AAPL.Open'],
                high=df['AAPL.High'],
                low=df['AAPL.Low'],
                close=df['AAPL.Close'])])

# Remove rangeslider for cleaner look
fig.update_layout(xaxis_rangeslider_visible=False)
```

### 3. Mixing Subplots with go.Figure

```python
from plotly.subplots import make_subplots

fig = make_subplots(rows=1, cols=2, subplot_titles=("Plot A", "Plot B"))

fig.add_trace(go.Scatter(x=[1, 2, 3], y=[4, 5, 6]), row=1, col=1)
fig.add_trace(go.Bar(x=[1, 2, 3], y=[2, 3, 5]), row=1, col=2)

fig.update_layout(height=600, width=800, title_text="Side-by-Side Comparison")
```

## Performance Optimization

### WebGL for Large Datasets

```python
# For scatter plots with >10,000 points, use Scattergl (Graph Objects)
# or tell px to use webgl (available in newer versions)
fig = px.scatter(df, x="large_x", y="large_y", render_mode="webgl")

# WebGL drastically improves performance by using the GPU for rendering.
```

## Common Pitfalls and Solutions

### JSON Overhead in Notebooks

```python
# ❌ Problem: Notebook file size explodes to 50MB
# ✅ Solution: Display as static image (requires kaleido) or use a different renderer
# fig.show(renderer="png") # Static
# OR: Clear output after viewing
```

### Axis Scaling in Animations

```python
# ❌ Problem: Axes jump around during animation
# ✅ Solution: Manually fix the ranges
fig = px.scatter(df, x="x", y="y", animation_frame="time",
                 range_x=[0, 100], range_y=[0, 100])
```

### Handling Missing Categories in Legend

```python
# ❌ Problem: Colors change when filtering data because categories disappear
# ✅ Solution: Pass a category_orders dictionary
fig = px.scatter(df, x="x", y="y", color="category",
                 category_orders={"category": ["A", "B", "C", "D"]})
```

## Best Practices

1. **Use Plotly Express first** - Start with `px` for 90% of tasks; only use `go` when you need fine-grained control
2. **Work with tidy DataFrames** - Ensure one row per observation for easy mapping to visual attributes
3. **Use `update_layout` for styling** - Cleanly modify titles, fonts, and background colors without recreating figures
4. **Save as HTML for sharing** - Use `fig.write_html("plot.html")` to share interactive charts with stakeholders
5. **Leverage hover data** - Add context to points without cluttering the plot
6. **Set figure templates** - Use `template="plotly_dark"` or `"ggplot2"` for instant professional styling
7. **Use marginal plots** - In `px.scatter`, use `marginal_x` and `marginal_y` to quickly add histograms or boxplots
8. **Optimize for large datasets** - Use WebGL rendering or datashader for datasets with >50k points
9. **Fix axis ranges in animations** - Use `range_x` and `range_y` to prevent axes from jumping during animations
10. **Set category orders** - Use `category_orders` to maintain consistent colors when filtering data

Plotly bridges the gap between static analysis and interactive discovery. It is the best tool for moving scientific insights from a notebook to the web.
