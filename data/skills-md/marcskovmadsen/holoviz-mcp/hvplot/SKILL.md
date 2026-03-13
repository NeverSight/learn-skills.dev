---
name: hvplot
description: Best practices for doing quick exploratory data analysis with minimal code and a Pandas .plot like API using HoloViews hvPlot.
metadata:
  version: "1.0.0"
  author: holoviz
  category: data-visualization
  difficulty: intermediate
---


# hvPlot Development Skills

This document provides best practices for developing plots and charts with HoloViz hvPlot in notebooks and .py files.

Please develop as an **Expert Python Developer** developing advanced data-driven, analytics and testable data visualisations, dashboards and applications would do. Keep the code short, concise, documented, testable and professional.

## Dependencies

Core dependencies provided with the `hvplot` Python package:

- **hvplot**: Core visualization framework
- **holoviews**: Declarative data visualization library with composable elements. Best for: complex multi-layered plots, advanced interactivity (linked brushing, selection), when you need fine control over plot composition, scientific visualizations. More powerful but steeper learning curve than hvPlot. hvPlot is built upon holoviews.
- **colorcet**: Perceptually uniform colormaps
- **panel**: Provides widgets and layouts enabling tool, dashboard and data app development.
- **param**: A declarative approach to creating classes with typed, validated, and documented parameters. Fundamental to the reactive programming model of hvPlot and the rest of the HoloViz ecosystem.
- **pandas**: Industry-standard DataFrame library for tabular data. Best for: data cleaning, transformation, time series analysis, datasets that fit in memory. The default choice for most data work.

Optional dependencies from the HoloViz Ecosystem:

- **datashader**: Renders large datasets (millions+ points) into images for visualization. Best for: big data visualization, geospatial datasets, scatter plots with millions of points, heatmaps of dense data. Requires hvPlot or HoloViews as frontend.
- **geoviews**: Geographic data visualization with map projections and tile sources. Best for: geographic/geospatial plots, map-based dashboards, when you need coordinate systems and projections. Built on HoloViews, works seamlessly with hvPlot.
- **holoviz-mcp**: Model Context Protocol server for HoloViz ecosystem. Provides access to detailed documentation, component search and agent skills.
- **hvsampledata**: Shared datasets for the HoloViz projects.

## Installation for Development

```bash
pip install hvplot hvsampledata panel watchfiles
```

For development in .py files DO always include watchfiles for Panel hotreload.

## Earthquake Sample Data

In the example below we will use the `earthquakes` sample data:

```python
import hvsampledata

hvsampledata.earthquakes("pandas")
```

```text
Tabular record of earthquake events from the USGS Earthquake Catalog that provides detailed
information including parameters such as time, location as latitude/longitude coordinates
and place name, depth, and magnitude. The dataset contains 596 events.

Note: The columns `depth_class` and `mag_class` were created by categorizing numerical values from
the `depth` and `mag` columns in the original dataset using custom-defined binning:

Depth Classification

| depth     | depth_class  |
|-----------|--------------|
| Below 70  | Shallow      |
| 70 - 300  | Intermediate |
| Above 300 | Deep         |

Magnitude Classification

| mag         | mag_class |
|-------------|-----------|
| 3.9 - <4.9  | Light     |
| 4.9 - <5.9  | Moderate  |
| 5.9 - <6.9  | Strong    |
| 6.9 - <7.9  | Major     |


Schema
------
| name        | type       | description                                                         |
|:------------|:-----------|:--------------------------------------------------------------------|
| time        | datetime   | UTC Time when the event occurred.                                   |
| lat         | float      | Decimal degrees latitude. Negative values for southern latitudes.   |
| lon         | float      | Decimal degrees longitude. Negative values for western longitudes   |
| depth       | float      | Depth of the event in kilometers.                                   |
| depth_class | category   | The depth category derived from the depth column.                   |
| mag         | float      | The magnitude for the event.                                        |
| mag_class   | category   | The magnitude category derived from the mag column.                 |
| place       | string     | Textual description of named geographic region near to the event.   |
```

## Reference Data Exploration Example

Below is a simple reference example for data exploration.

```python
import hvsampledata
# DO import panel if working in .py files
import panel as pn
# Do importing hvplot.pandas to add .hvplot namespace to Pandas DataFrames and Series
import hvplot.pandas  # noqa: F401

# DO always run pn.extension() to load panel javascript extensions
pn.extension()

# Do keep the extraction, transformation and plotting of data clearly separate
# Extract: earthquakes sample data
data = hvsampledata.earthquakes("pandas")

# Transform: Group by mag_class and count occurrences
mag_class_counts = data.groupby('mag_class').size().reset_index(name='counts')

# Plot: counts by mag_class
plot = mag_class_counts.hvplot.bar(x='mag_class', y='counts', title='Earthquake Counts by Magnitude Class')
# If working in notebook DO output to plot:
plot
# Else if working in .py file DO:
# DO provide a method to serve the app with `panel serve`
if pn.state.served:
    # DO remember to add .servable to the panel components you want to serve with the app
    pn.panel(plot, sizing_mode="stretch_both").servable()
# DON'T provide a `if __name__ == "__main__":` method to serve the app with `python`
```

If working in a .py file DO always serve the plot with hotreload for manual testing while developing:

```bash
panel serve path/to/file.py --dev --show
```

DONT serve with `python path_to_this_file.py`.

## General Instructions

- Always import hvplot for your data backend:

```python
import hvplot.pandas # will add .hvplot namespace to Pandas dataframes
import hvplot.polars # will add .hvplot namespace to Polars dataframes
...
```

- Prefer Bokeh > Plotly > Matplotlib plotting backend for interactivity
- DO use bar charts over pie Charts. Pie charts are not supported.
- DO use NumeralTickFormatter and 'a' formatter for axis formatting:

```python
from bokeh.models.formatters import NumeralTickFormatter

df.hvplot(
    ...,
    yformatter=NumeralTickFormatter(format='0.00a'),  # Format as 1.00M, 2.50M, etc.
)
```


| Input | Format String | Output |
| - |  - | - |
| 1230974 | '0.0a' | 1.2m |
| 1460 | '0 a' | 1 k |
| -104000 | '0a' | -104k |

- For detailed styling and publication quality charts use HoloViz instead of hvPlot.

## Developing

When developing a hvplot please serve it for development using Panel:

```python
import pandas as pd
import hvplot.pandas  # noqa
import panel as pn

import numpy as np

np.random.seed(42)
dates = pd.date_range("2022-08-01", periods=30, freq="B")
open_prices = np.cumsum(np.random.normal(100, 2, size=len(dates)))
high_prices = open_prices + np.random.uniform(1, 5, size=len(dates))
low_prices = open_prices - np.random.uniform(1, 5, size=len(dates))
close_prices = open_prices + np.random.uniform(-3, 3, size=len(dates))

data = pd.DataFrame({
    "open": open_prices.round(2),
    "high": high_prices.round(2),
    "low": low_prices.round(2),
    "close": close_prices.round(2),
}, index=dates)


# Create a scatter plot of date vs close price
scatter_plot = data.hvplot.scatter(x="index", y="close", grid=True, title="Close Price Scatter Plot", xlabel="Date", ylabel="Close Price")


# Create a Panel app
app = pn.Column("# Close Price Scatter Plot", scatter_plot)

if pn.state.served:
    app.servable()
```

```bash
panel serve plot.py --dev
```

### Recommended Plot Types

line - Line plots for time series and continuous data
scatter - Scatter plots for exploring relationships between variables
bar - Bar charts for categorical comparisons
hist - Histograms for distribution analysis
area - Area plots for stacked or filled visualizations

## Workflows

### Lookup additional information

- If the HoloViz MCP server tools are available, DO use them: `search` (documentation), `hvplot_list` (available plot types), `hvplot_get` (docstrings and signatures), `skill_get` (best-practice skills).
- If MCP tools are not available but the `holoviz-mcp` CLI is installed (also available as `hv`), use the equivalent CLI commands: `holoviz-mcp search`, `holoviz-mcp hvplot list`, `holoviz-mcp hvplot get`.
- If neither is available, DO search the web. For example searching the hvplot website for `streaming` related information via https://hvplot.holoviz.org/en/docs/latest/search.html?q=streaming url.

### Test the app with pytest

DO add tests to the `tests` folder and run them with `pytest tests/path/to/test_file.py`.

- DO separate data extraction and transformation from plotting code.
- DO fix any test errors and rerun the tests
- DO run the tests and fix errors before displaying or serving the plots

### Test the app manually with panel serve

DO always start and keep running a development server `panel serve path_to_file.py --dev --show` with hot reload while developing!

- Due to `--show` flag, a browser tab will automatically open showing your app.
- Due to `--dev` flag, the panel server and app will automatically reload if you change the code.
- The app will be served at http://localhost:5006/.
- DO make sure the correct virtual environment is activated before serving the app.
- DO fix any errors that show up in the terminal. Consider adding new tests to ensure they don't happen again.
- DON'T stop or restart the server after changing the code. The app will automatically reload.
- If you see 'Cannot start Bokeh server, port 5006 is already in use' in the terminal, DO serve the app on another port with `--port {port-number}` flag.
- DO remind the user to test the plot on multiple screen sizes (desktop, tablet, mobile)
- DON'T use legacy `--autoreload` flag
- DON't run `python path_to_file.py` to test or serve the app.
- DO use `pn.Column, pn.Tabs, pn.Accordion` to layout multiple plots
- If you close the server to run other commands DO remember to restart it.
