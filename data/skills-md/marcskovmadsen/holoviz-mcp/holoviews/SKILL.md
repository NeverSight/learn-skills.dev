---
name: holoviews
description: Best practices for developing advanced, interactive, and publication-quality data visualizations using HoloViz HoloViews
metadata:
  version: "1.0.0"
  author: holoviz
  category: data-visualization
  difficulty: intermediate
---


# HoloViews Development Skills

This document provides best practices for developing plots and charts with HoloViz HoloViews in notebooks and .py files.

Please develop as an **Expert Python Developer** developing advanced data-driven, analytics and testable data visualisations, dashboards and applications would do. Keep the code short, concise, documented, testable and professional.

## Dependencies

Core dependencies provided with the `holoviews` Python package:

- **holoviews**: Declarative data visualization library with composable elements. Best for: complex multi-layered plots, advanced interactivity (linked brushing, selection), when you need fine control over plot composition, scientific visualizations. More powerful but steeper learning curve than hvPlot. hvPlot is built upon holoviews.
- **colorcet**: Perceptually uniform colormaps
- **panel**: Provides widgets and layouts enabling tool, dashboard and data app development.
- **param**: A declarative approach to creating classes with typed, validated, and documented parameters. Fundamental to the reactive programming model of hvPlot and the rest of the HoloViz ecosystem.
- **pandas**: Industry-standard DataFrame library for tabular data. Best for: data cleaning, transformation, time series analysis, datasets that fit in memory. The default choice for most data work.

Optional dependencies from the HoloViz Ecosystem:

- **hvplot**: Easy to use plotting library with Pandas `.plot` like API. Built on top of HoloViews.
- **datashader**: Renders large datasets (millions+ points) into images for visualization. Best for: big data visualization, geospatial datasets, scatter plots with millions of points, heatmaps of dense data. Requires hvPlot or HoloViews as frontend.
- **geoviews**: Geographic data visualization with map projections and tile sources. Best for: geographic/geospatial plots, map-based dashboards, when you need coordinate systems and projections. Built on HoloViews, works seamlessly with hvPlot.
- **holoviz-mcp**: Model Context Protocol server for HoloViz ecosystem. Provides access to detailed documentation, component search and agent skills.
- **hvsampledata**: Shared datasets for the HoloViz projects.

## Installation for Development

```bash
pip install holoviews hvsampledata panel watchfiles
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
import holoviews as hv

# DO always run hv.extension() to load the HoloViews javascript extensions
# DO specify the backend you intend to use (e.g., "bokeh", "matplotlib", "plotly")
hv.extension("bokeh")

# Do keep the extraction, transformation and plotting of data clearly separate
# Extract: earthquakes sample data
data = hvsampledata.earthquakes("pandas")

# Transform: Group by mag_class and count occurrences
mag_class_counts = data.groupby('mag_class').size().reset_index(name='counts')

# DO Specify an *element* type. Here its hv.Bars, i.e. a Bar plot.
plot = hv.Bars(
    # DO provide the data explicitly
    data = mag_class_counts,
    # DO always specify the key dimensions (kdims) and value dimensions (vdims) as a single value or a list of values
    kdims='mag_class',
    vdims='counts'
).opts(
    # DO specify optional styling options using .opts()
    line_color=None,
    # DO specify optional plot options using .opts()
    title='Earthquake Counts by Magnitude Class'
)
# If working in notebook DO output to plot:
plot
# If working in .py file DO use panel:
import panel as pn

# DON'T provide a `if __name__ == "__main__":` method to serve the app with `python`
# Instead provide pn.state.served check
if pn.state.served:
    # DO always run pn.extension() to load panel javascript extensions
    pn.extension()
    # DO remember to add .servable to the panel components you want to serve with the app
    pn.panel(plot, sizing_mode="stretch_both").servable()
```

If working in a .py file DO serve the plot with hotreload:

```bash
panel serve path/to/file.py --dev --show
```

DONT serve with `python path_to_this_file.py`.

## Reference Group By

In this example we also groupby `depth_class`, i.e. a dropdown widget is added to select the `depth_class` to filter by.

```python
import hvsampledata
import holoviews as hv

hv.extension("bokeh")

data = hvsampledata.earthquakes("pandas")

mag_class_counts = data.groupby(['mag_class', 'depth_class']).size().reset_index(name='counts')
print(mag_class_counts)

plot = hv.Bars(
    data = mag_class_counts,
    kdims=['mag_class','depth_class'],
    vdims='counts',
).groupby(
    "depth_class"
).opts(
    # DO specify optional styling options using .opts()
    line_color=None,
    # DO specify optional plot options using .opts()
    title='Earthquake Counts by Magnitude Class and Depth Class',
    width=800,
)
# If working in notebook DO output to plot:
plot
# If working in .py file DO use panel:
import panel as pn

# DON'T provide a `if __name__ == "__main__":` method to serve the app with `python`
# Instead provide pn.state.served check
if pn.state.served:
    # DO always run pn.extension() to load panel javascript extensions
    pn.extension()
    # DO remember to add .servable to the panel components you want to serve with the app
    pn.panel(plot, sizing_mode="stretch_both").servable()
```

If we add `.layout` the data will be visualized as 3 individual plots (one per depth_class):

```python
import hvsampledata
import holoviews as hv

hv.extension("bokeh")

data = hvsampledata.earthquakes("pandas")

mag_class_counts = data.groupby(['mag_class', 'depth_class']).size().reset_index(name='counts')
print(mag_class_counts)

plot = hv.Bars(
    data = mag_class_counts,
    kdims=['mag_class','depth_class'],
    vdims='counts',
).groupby(
    "depth_class"
).opts(
    # DO specify optional styling options using .opts()
    line_color=None,
    width=800,
).layout()
# If working in notebook DO output to plot:
plot
# If working in .py file DO use panel:
import panel as pn

# DON'T provide a `if __name__ == "__main__":` method to serve the app with `python`
# Instead provide pn.state.served check
if pn.state.served:
    # DO always run pn.extension() to load panel javascript extensions
    pn.extension()
    # DO remember to add .servable to the panel components you want to serve with the app
    pn.panel(plot, sizing_mode="stretch_both").servable()
```

If instead of `.layout()` we add `.overlay()`, one plot will be created, but the depth_class'es will be visualized by different colors.

```python
import hvsampledata
import holoviews as hv

hv.extension("bokeh")

data = hvsampledata.earthquakes("pandas")

mag_class_counts = data.groupby(['mag_class', 'depth_class']).size().reset_index(name='counts')
print(mag_class_counts)

plot = hv.Bars(
    data = mag_class_counts,
    kdims=['mag_class','depth_class'],
    vdims='counts',
).groupby(
    "depth_class"
).opts(
    # DO specify optional styling options using .opts()
    line_color=None,
    width=800,
).overlay()
# If working in notebook DO output to plot:
plot
# If working in .py file DO use panel:
import panel as pn

# DON'T provide a `if __name__ == "__main__":` method to serve the app with `python`
# Instead provide pn.state.served check
if pn.state.served:
    # DO always run pn.extension() to load panel javascript extensions
    pn.extension()
    # DO remember to add .servable to the panel components you want to serve with the app
    pn.panel(plot, sizing_mode="stretch_both").servable()
```

Note: This works better for Curve or Scatter plots

## Reference Publication Quality Bar Chart

```python
# ============================================================================
# Publication-Quality Bar Chart - HoloViews Best Practices Example
# ============================================================================
# Demonstrates:
# - Data extraction, transformation, and visualization separation
# - Custom Bokeh themes for consistent styling
# - Interactive tooltips with formatted data
# - Text annotations on bars
# - Professional fonts, grids, and axis formatting
# - Panel integration for web serving
# ============================================================================

import hvsampledata
import panel as pn
from bokeh.models.formatters import NumeralTickFormatter
from bokeh.themes import Theme

import holoviews as hv
from holoviews.plotting.bokeh import ElementPlot

# ============================================================================
# BOKEH THEME SETUP - Define global styling
# ============================================================================

ACCENT_COLOR = '#007ACC'  # Professional blue
FONT_FAMILY = 'Roboto'

def create_bokeh_theme(font_family=FONT_FAMILY, accent_color=ACCENT_COLOR):
    """Create custom theme with specified font. Default: Roboto"""
    return Theme(json={
        'attrs': {
            'Title': {
                'text_font': font_family,
                'text_font_size': '16pt',
                'text_font_style': 'bold'
            },
            'Axis': {
                'axis_label_text_font': font_family,
                'axis_label_text_font_size': '12pt',
                'axis_label_text_font_style': 'bold',
                'major_label_text_font': font_family,
                'major_label_text_font_size': '10pt',
                'major_tick_line_color': "black",  # Remove tick marks
                'minor_tick_line_color': None
            },
            'Plot': {
                'background_fill_color': '#fafafa',
                'border_fill_color': '#fafafa'
            },
            'Legend': {
                'label_text_font': font_family,
                'label_text_font_size': '10pt'
            },
            'Toolbar': {
                "autohide": True,
                "logo": None,
                "stylesheets": [
                    f"""
                    .bk-OnOffButton.bk-active{{
                        border-color: {accent_color} !important;
                    }}
                    """
                ]
            },
            # Does not work via Theme, so added here for reference purposes until I figure out how to do it
            'Tooltip': {
                "stylesheets": [f"""
                    .bk-tooltip-row-label {{
                        color: {ACCENT_COLOR} !important;
            }}"""]

            }
        }
    })

# Apply theme globally - affects all plots
hv.renderer('bokeh').theme = create_bokeh_theme()

# ============================================================================
# HOLOVIEWS OPTS SETUP - Define global configuration
# ============================================================================

GLOBAL_BACKEND_OPTS={
    'plot.xgrid.visible': False,           # Only horizontal grid lines
    'plot.ygrid.visible': True,
    'plot.ygrid.grid_line_color': "black",
    'plot.ygrid.grid_line_alpha': 0.1,
    'plot.min_border_left': 80,            # Add padding on left (for y-axis label)
    'plot.min_border_bottom': 80,          # Add padding on bottom (for x-axis label)
    'plot.min_border_right': 30,           # Add padding on right
    'plot.min_border_top': 80,             # Add padding on top
}

ElementPlot.param.backend_opts.default = GLOBAL_BACKEND_OPTS
ElementPlot.param.yformatter.default = NumeralTickFormatter(format='0a')  # 1k, ...

hv.opts.defaults(
    hv.opts.Bars(
        color=ACCENT_COLOR,           # Professional blue
        line_color=None,            # Remove bar borders
    ),
    hv.opts.Labels(
        text_baseline='bottom',
        text_font_size='11pt',
        text_font_style='normal',
        text_color='#333333',
    ),
)
hv.Cycle.default_cycles["default_colors"] = [ACCENT_COLOR, '#00948A', '#7E59BD', '#FFA20C', '#DA4341', '#D6F1FF', '#DAF5F4', '#F0E8FF', '#FFF8EA', '#FFF1EA', '#001142', '#003336', '#290031', '#371F00', '#3A0C13']

# ============================================================================
# DATA PIPELINE - Separate extraction, transformation, and plotting
# ============================================================================

def get_earthquake_data():
    """Extract raw earthquake data from sample dataset"""
    return hvsampledata.earthquakes("pandas")


def aggregate_by_magnitude(earthquake_data):
    """Transform: Group earthquakes by magnitude class with statistics"""
    # Aggregate: count events and calculate average depth per magnitude class
    aggregated = (
        earthquake_data
        .groupby('mag_class', observed=True)
        .agg({'mag': 'count', 'depth': 'mean'})
        .reset_index()
        .rename(columns={'mag': 'event_count', 'depth': 'avg_depth'})
        .sort_values('event_count', ascending=False)
    )

    # Add percentage column for tooltips
    aggregated['percentage'] = (
        aggregated['event_count'] / aggregated['event_count'].sum() * 100
    )

    return aggregated


def create_bar_chart(aggregated_data):
    """Create publication-quality bar chart with labels and tooltips"""
    default_tools=['save']

    # Main bar chart with professional styling
    bar_chart = hv.Bars(aggregated_data, kdims='mag_class', vdims=['event_count', 'percentage', 'avg_depth']).opts(
        # Titles and labels
        title='Earthquake Distribution by Magnitude',
        xlabel='Magnitude',
        ylabel='Number of Events',

        # Interactivity
        # hover_cols = ["mag_class", "event_count", "percentage", "avg_depth"],
        hover_tooltips=[
            ('Magnitude', '@mag_class'),
            ('Events', '@event_count{0,0}'),      # Format: 1,234
            ('Percentage', '@percentage{0 a}%'), # Format: 45%
            ('Avg Depth', '@avg_depth{0f} km')  # Format: 99 km
        ],
        default_tools=default_tools
    )

    # Add text labels above bars
    labels_data = aggregated_data.copy()
    labels_data['label_y'] = labels_data['event_count'] + 20  # Offset above bars

    text_labels = hv.Labels(labels_data, kdims=['mag_class', 'label_y'], vdims=['event_count', 'percentage', 'avg_depth']).opts(
        hover_tooltips=[
            ('Magnitude', '@mag_class'),
            ('Events', '@event_count{0,0}'),      # Format: 1,234
            # tooltips below do currently not work on Labels
            # ('Percentage', '@percentage{0 a}%'), # Format: 45%
            # ('Avg Depth', '@avg_depth{0f} km'),  # Format: 99 km
        ],
        default_tools=default_tools
    )

    # Overlay: bar chart * text labels
    return bar_chart * text_labels


def create_plot():
    """Main function: Extract → Transform → Plot"""
    # Extract: Get raw data
    earthquake_data = get_earthquake_data()

    # Transform: Aggregate and calculate statistics
    aggregated = aggregate_by_magnitude(earthquake_data)

    # Visualize: Create publication-quality chart
    chart = create_bar_chart(aggregated)

    return chart


# ============================================================================
# PANEL APP SETUP
# ============================================================================

# Serve the chart when running with Panel
if pn.state.served:
    # Load Panel JavaScript extensions
    pn.extension()

    # Apply custom Bokeh theme (override the global theme)
    # Create and serve the chart
    plot = create_plot()
    pn.panel(plot, sizing_mode="stretch_both", margin=25).servable()
```

## General Instructions

- In a notebook always run `hv.extension()` to load any Javascript dependencies.

```python
import holoviews as hv

hv.extension()
...
```

- Prefer Bokeh > Plotly > Matplotlib plotting backend for interactivity
- DO use bar charts over pie Charts. Pie charts are not supported.
- DO use NumeralTickFormatter and 'a' formatter for easy axis formatting:

```python
from bokeh.models.formatters import NumeralTickFormatter

plot.opts(
    yformatter=NumeralTickFormatter(format='0.00a'),  # Format as 1.00M, 2.50M, etc.
)
```


| Input | Format String | Output |
| - |  - | - |
| 1230974 | '0.0a' | 1.2m |
| 1460 | '0 a' | 1 k |
| -104000 | '0a' | -104k |

## Saving a plot

You can save a plot to html with `hv.save`:

```python
hv.save(some_plot, 'some_plot.html')
```

## Recommended Plot Types

Curve - Line plots for time series and continuous data
Scatter - Scatter plots for exploring relationships between variables
Bars - Bar charts for categorical comparisons
Histogram - Histograms for distribution analysis
Area - Area plots for stacked or filled visualizations

## Workflows

### Lookup additional information

- If the HoloViz MCP server tools are available, DO use them: `search` (documentation), `hv_list` (available elements), `hv_get` (docstrings and options), `skill_get` (best-practice skills).
- If MCP tools are not available but the `holoviz-mcp` CLI is installed (also available as `hv`), use the equivalent CLI commands: `holoviz-mcp search`, `holoviz-mcp hv list`, `holoviz-mcp hv get`.
- If neither is available, DO search the web. For example searching the HoloViews website for relevant information via https://holoviews.org url.

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
