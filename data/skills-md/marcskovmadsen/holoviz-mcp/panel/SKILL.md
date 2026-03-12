---
name: panel
description: Best practices for developing tools, dashboards and interactive data apps with HoloViz Panel. Create reactive, component-based UIs with widgets, layouts, templates, and real-time updates. Use when developing interactive data exploration tools, dashboards, data apps, or any interactive Python web application. Supports file uploads, streaming data, multi-page apps, and integration with HoloViews, hvPlot, Pandas, Polars, DuckDB and the rest of the HoloViz and PyData ecosystems.
metadata:
  version: "1.0.0"
  author: holoviz
  category: web-development
  difficulty: intermediate
---

# Panel Development Skills

This document provides best practices for developing dashboards and data apps with HoloViz Panel in Python .py files.

Please develop as an **Expert Python and Panel Developer** developing advanced data-driven, analytics and testable dashboards and analytics apps would do. Keep the code short, concise, documented, testable and professional.

## Dependencies

Core dependencies provided with the `panel` Python package:

- **panel**: Core application framework
- **param**: A declarative approach to creating classes with typed, validated, and documented parameters. Fundamental to Panel's reactive programming model.

Optional panel-extensions:

- **panel-material-ui**: Modern Material UI components. To replace the panel native widgets within the next two years.
- **panel-graphic-walker**: Modern Tableau like interface. Can offload computations to the server and thus scale to large datasets.

Optional dependencies from the HoloViz Ecosystem:

- **colorcet**: Perceptually uniform colormaps collection. Best for: scientific visualization requiring accurate color representation, avoiding rainbow colormaps, accessible color schemes. Integrates with hvPlot, HoloViews, Matplotlib, Bokeh.
- **datashader**: Renders large datasets (millions+ points) into images for visualization. Best for: big data visualization, geospatial datasets, scatter plots with millions of points, heatmaps of dense data. Requires hvPlot or HoloViews as frontend.
- **geoviews**: Geographic data visualization with map projections and tile sources. Best for: geographic/geospatial plots, map-based dashboards, when you need coordinate systems and projections. Built on HoloViews, works seamlessly with hvPlot.
- **holoviews**: Declarative data visualization library with composable elements. Best for: complex multi-layered plots, advanced interactivity (linked brushing, selection), when you need fine control over plot composition, scientific visualizations. More powerful but steeper learning curve than hvPlot.
- **holoviz-mcp**: Model Context Protocol server for HoloViz ecosystem. Provides access to detailed documentation, component search and agent skills.
- **hvplot**: High-level plotting API with Pandas `.plot()`-like syntax. Best for: quick exploratory visualizations, interactive plots from DataFrames/Xarray, when you want interactivity without verbose code. Built on HoloViews.
- **hvsampledata**: Shared datasets for the HoloViz projects.

Optional dependencies from the wider PyData Ecosystem:

- **altair**: Declarative, grammar-of-graphics visualization library. Best for: statistical visualizations, interactive exploratory charts, when you need Vega-Lite's extensive chart gallery. Works well with Pandas/Polars DataFrames.
- **dask**: Parallel computing library for scaling Pandas DataFrames beyond memory. Best for: processing datasets larger than RAM, parallel computation across multiple cores/machines, lazy evaluation workflows.
- **duckdb**: High-performance analytical SQL database. Best for: fast SQL queries on DataFrames, aggregations on large datasets, when you need SQL interface, OLAP-style analytics. Much faster than Pandas for analytical queries.
- **matplotlib**: Low-level, highly customizable plotting library. Best for: publication-quality static plots, fine-grained control over every aspect of visualization, scientific plots, when you need pixel-perfect control.
- **pandas**: Industry-standard DataFrame library for tabular data. Best for: data cleaning, transformation, time series analysis, datasets that fit in memory. The default choice for most data work.
- **Plotly**: Interactive, publication-quality visualization library. Best for: 3D plots, complex interactive charts, animations, when you need hover tooltips and interactivity. Works well with Dash and Panel.
- **polars**: Modern, fast DataFrame library written in Rust. Best for: high-performance data processing, datasets that fit in memory but need speed, when you need lazy evaluation, better memory efficiency than Pandas.
- **xarray**: N-dimensional labeled arrays and datasets. Best for: multidimensional scientific data (climate, satellite imagery), data with multiple dimensions and coordinates, NetCDF/HDF5 files, geospatial raster data.
- **watchfiles**: Enables high performance file watching and autoreload for the panel server.

## Common Use Cases

1. **Real-time Monitoring Dashboards**: Live metrics and KPI displays
2. **Data Exploration Tools**: Interactive data analysis applications
3. **Configuration Interfaces**: Complex multi-step configuration UIs
4. **Data Input Applications**: Validated form-based data collection
5. **Report Viewers**: Interactive report generation and browsing
6. **Administrative Interfaces**: Internal tools for data management

## Installation

```bash
pip install panel watchfiles hvplot hvsampledata
```

For development in .py files DO always include watchfiles for hotreload.

## Best Practice Hello World App

Let's describe our best practices via a basic Hello World App:

```python
# DO import panel as pn
import panel as pn
import param

# DO always run pn.extension
# DO remember to add any imports needed by panes, e.g. pn.extension("tabulator", "plotly", ...)
# DON'T add "bokeh" as an extension. It is not needed.
# Do use throttled=True when using slider unless you have a specific reason not to
pn.extension(throttled=True)

# DO organize functions to extract data separately as your app grows. Eventually in a separate data.py file.
# DO use caching to speed up the app, e.g. for expensive data loading or processing that would return the same result given same input arguments.
# DO add a ttl (time to live argument) for expensive data loading that changes over time
@pn.cache(max_items=3)
def extract(n=5):
    return "Hello World" + "⭐" * n

text = extract()
text_len = len(text)

# DO organize functions to transform data separately as your app grows. Eventually in a separate transformations.py file
# DO add caching to speed up expensive data transformations
@pn.cache(max_items=3)
def transform(data: str, count: int=5)->str:
    count = min(count, len(data))
    return data[:count]

# DO organize functions to create plots separately as your app grows. Eventually in a separate plots.py file.
# DO organize custom components and views separately as your app grows. Eventually in separate components.py or views.py file(s).
# DO use param.Parameterized, pn.viewable.Viewer or similar approach to create new components and apps with state and reactivity
class HelloWorld(pn.viewable.Viewer):
    # DO define parameters to hold state and drive the reactivity
    characters = param.Integer(default=text_len, bounds=(0, text_len), doc="Number of characters to display")

    def __init__(self, **params):
        super().__init__(**params)

        # DO use sizing_mode="stretch_width" for components unless "fixed" or other sizing_mode is specifically needed
        with pn.config.set(sizing_mode="stretch_width"):
            # DO create widgets using `.from_param` method
            self._characters_input = pn.widgets.IntSlider.from_param(self.param.characters, margin=(10,20))

            # DO Collect input widgets into horizontal, columnar layout unless other layout is specifically needed
            self._inputs = pn.Column(self._characters_input, max_width=300)

            # CRITICAL: Create panes ONCE with reactive content
            # DON'T recreate panes and layouts in @param.depends methods - causes flickering!
            # DO bind reactive methods/functions to panes for smooth updates
            self._output_pane = pn.pane.Markdown(
                self.model,  # Reactive method reference
                sizing_mode="stretch_width"
            )

            # DO collect output components into some layout like Column, Row, FlexBox or Grid depending on use case
            self._outputs = pn.Column(self._output_pane)

            # DO collect all of your components into a combined layout useful for displaying in notebooks etc.
            self._panel = pn.Row(self._inputs, self._outputs)

    # DO use caching to speed up bound methods that are expensive to compute or load data and return the same result for a given state of the class.
    # DO add a ttl (time to live argument) for expensive data loading that changes over time.
    @pn.cache(max_items=3)
    # DO prefer .depends over .bind over .rx for reactivity methods on Parameterized classes as it can be typed and documented
    # DON'T use `watch=True` or `.watch(...)` methods to update UI components directly.
    # DO use `watch=True` or `.watch(...)` for updating the state parameters or triggering side effects like saving files or sending email.
    @param.depends("characters")
    def model(self):
        # CRITICAL: Return ONLY the content, NOT the layout/pane
        # The pane was created once in __init__, this just updates its content
        return transform(text, self.characters)

    # DO use `watch=True` or `.watch(...)` for updating the state parameters or triggering side effects like saving files or sending email.
    @param.depends("characters", watch=True)
    def _inform_user(self):
        print(f"User selected to show {self.characters} characters.")

    # DO provide a method for displaying the component in a notebook setting, i.e. without using a Template or other element that cannot be displayed in a notebook setting.
    def __panel__(self):
        return self._panel

    # DO provide a method to create a .servable app
    @classmethod
    def create_app(cls, **params):
        instance = cls(**params)
        # DO use a Template or similar page layout for served apps
        template = pn.template.FastListTemplate(
            # DO provide a title for the app
            title="Hello World App",
            # DO provide optional image, optional app description, optional navigation menu, input widgets, optional documentation and optional links in the sidebar
            # DO provide as list of components or a list of single horizontal layout like Column as the sidebar by default is 300 px wide
            sidebar=[instance._inputs],
            # DO provide a list of layouts and output components in the main area of the app.
            # DO use Grid or FlexBox layouts for complex dashboard layouts instead of combination Rows and Columns.
            main=[instance._outputs],
            # DO set main_layout=None for modern layout
            main_layout=None,
        )
        return template

# DON'T provide a `if __name__ == "__main__":` method to serve the app with `python`
# DO provide a method to serve the app with `panel serve`
if pn.state.served:
    # Mark components to be displayed in the app with .servable()
    HelloWorld.create_app().servable()
```

DO serve the app with

```bash
panel serve path_to_this_file.py --show --dev
```

DON'T serve with `python path_to_this_file.py`.

## Best Practice Hello World Tests

With panel you can easily create tests to test user behaviour without having to write client side tests.

DO always create separate tests in the `tests` folder:

```python
# DO put tests in a separate test file.
# DO always test that the reactivity works as expected
def test_characters_reactivity():
    """
    Test characters reactivity.
    """
    # DO test the default values of bound
    hello_world = HelloWorld()
    # DO test the reactivity of bound methods when parameters change
    assert hello_world.model() == text[:hello_world.characters]
    hello_world.characters = 5
    assert hello_world.model() == text[:5]
    hello_world.characters = 3
    assert hello_world.model() == text[:3]
```

DO run the tests with:

```bash
pytest tests/path/to/test_file.py
```

DO fix any errors identified.

## Key Patterns

### Parameter-Driven Architecture

- DO use `param.Parameterized` or `pn.viewable.Viewer` classes to organize and manage state
- DO create widgets with `.from_param()` method. DON'T do this for panes, i.e. pn.pane.Str has no from_param method.
- DO use `@param.depends()` for reactive methods
- DO use `@param.depends(..., watch=True)` to update parameter/ state values and for side-effects like sending an email.
- DO group related parameters in separate `Parameterized` or `Viewable` classes

```python
# ❌ AVOID: Updating panes and other components directly. This makes it hard to reason about application flow and state
@param.depends('value', watch=True)
def update_plot(self):
    self.output_pane.object = transform(text, self.characters)
```

### Create Static Layout with Reactive Content (CRITICAL)

**The Golden Rule: Create layout structure ONCE, update content REACTIVELY**

This pattern eliminates flickering and creates professional Panel applications:

```python
# ✅ CORRECT: Create panes ONCE in __init__, bind reactive content
class Dashboard(pn.viewable.Viewer):
    filter_value = param.String(default="all")

    chart = param.Parameter()

    def __init__(self, **params):
        super().__init__(**params)

        # 1. Create static panes with reactive content
        self._summary_pane = pn.pane.Markdown(self._summary_text)
        self._chart_pane = pn.pane.HoloViews(self.param.chart)

        # 2. Create static layout structure
        self._layout = pn.Column(
            "# Dashboard",    # Static title
            self._summary_pane,  # Reactive content
            self._chart_pane,    # Reactive content
        )

    # ✅ Good: Reactive content method
    # Will be run multiple times when filter_value updates if multiple panes or reactive functions depend on the _summary_text method
    @param.depends("filter_value")
    def _summary_text(self):
        # Returns string content only, NOT a pane
        return f"**Count**: {len(self._get_data())}"

    # ✅ Good: Reactive update of chart parameter
    # Will be run only one time when filter_value updates - even if multiple panes or reactive functions depend on the chart value
    @param.depends("filter_value", watch=True, on_init=True)
    def _update_chart(self):
        # updates the chart object only, NOT a pane
        self.chart = self._get_data().hvplot.bar()

    def __panel__(self):
        return self._layout

# ❌ WRONG: Recreating layout in @param.depends - causes flickering!
class BadDashboard(pn.viewable.Viewer):
    filter_value = param.String(default="all")

    @param.depends("filter_value")
    def view(self):
        # DON'T recreate panes/layouts on every parameter change!
        return pn.Column(
            "# Dashboard",
            pn.pane.Markdown(f"**Count**: {len(self._get_data())}"),
            pn.pane.HoloViews(self._get_data().hvplot.bar()),
        )
```

**Why This Matters:**

- ✅ Smooth updates without layout reconstruction
- ✅ No flickering - seamless transitions
- ✅ Better performance - avoids unnecessary DOM updates
- ✅ Professional UX

**Key Rules:**

1. DO create main layout structure and panes ONCE in `__init__`
2. DO bind panes to reactive methods or parameters (DON'T recreate them)
3. Reactive methods should return CONTENT only (strings, plots, dataframes), NOT panes/layouts
4. Use `@param.depends` for reactive methods that update pane content

### Widgets

Use

- `pn.widgets.IntSlider`, `pn.widgets.Select`, `pn.widgets.DateRangeSlider` and other widgets for input
- `pn.widgets.Tabulator` to display tabular data like DataFrames

### Panes

Use panes to display data:

- `pn.pane.Markdown` and `pn.pane.HTML` to display strings
- `pn.pane.HoloViews`, `pn.pane.Plotly`, `pn.pane.Matplotlib` or `pn.pane.ECharts` to display plots

### Layouts

Use layouts to layout components:

- DO use `pn.Column`, `pn.Row`, `pn.Tabs`, `pn.Accordion` for layouts

### Templates

- DO use `pn.template.FastListTemplate` or other templates for served apps:

```python
template = pn.template.FastListTemplate(
    title="Hello World App",
    sidebar=[instance._inputs],
    main=[instance._outputs],
    main_layout=None,
)
```

- In the `sidebar`, DO use the order: 1) optional logo, 2) description, 3) input widgets, 4) documentation
- In the `sidebar`, DO make sure components stretch width.
- Do set `main_layout=None` for a modern styling.

### Responsive Design

- DO use `sizing_mode="stretch_width"` by default:

```python
with pn.config.set(sizing_mode="stretch_width"):
    character_input = pn.widgets...
    output_pane = pn.pane....
```

- DO use `FlexBox`, `GridSpec` or `GridBox` for complex, responsive grid layouts
- DO set appropriate `min_width`, `min_height`, `max_width` and `max_height` to prevent layout collapse

### Extensions

DO remember to add extensions like "tabulator", "plotly" etc. to `pn.extension` to make sure their Javascript is loaded:

```python
# ✅ Good
pn.extension("tabulator", "plotly")
```

DON'T add "bokeh". It's already loaded:

```python
# ❌ Bad
pn.extension("bokeh")
```

### Servable()

DO make the main component `.servable()` to include it in the served app and use `pn.state.served` to run the main method when the app is panel serve'd.

```python
# ✅ Correct:
if pn.state.served:
    main().servable()

# ❌ Incorrect:
if __name__ == "__main__":
    main().servable()

# ❌ Don't: Works, but not how we want to serve the app:
if __name__ == "__main__":
    main().show()
```

### Performance Optimization

- **Defer load**: Defer load to after the app is shown to the user: `pn.extension(defer_load=True, loading_indicator=True, ...)`
- **Lazy-load components** using Tabs or Accordion for heavy content
- **Use caching** with `@pn.cache` decorator for expensive computations
- **Use async/await**: Implement asynchronous patterns for I/O operations
- **Use faster frameworks**: Replace slower Pandas with faster Polars or DuckDB
- **Offload to threads**: Consider using threading for CPU-intensive tasks
- **Offload to external processes**: Consider offloading heavy computations to external processes like databases, scheduled (airflow) jobs, REST apis etc.
- **Profile callbacks** with `@pn.io.profiler` to identify bottlenecks

If you experience memory issues, make sure to:

- **Limit history**: Cap data history sizes in streaming applications
- **Clear caches**: Periodically call `pn.state.clear_caches()`
- **Restart periodically**: Schedule application restarts for long-running production apps
- **Profile memory**: Use memory profilers (memory_profiler, tracemalloc) to identify leaks

### Code Organization

- **Separate concerns**: Keep UI code separate from business logic using Param classes
- **Create reusable components**: Extract common patterns into functions or classes
- **Use templates** for consistent application structure across pages
- **Organize modules**: Group related components and utilities
- **Document parameters**: Add clear docstrings to Parameterized classes

## Workflows

### Lookup additional information

- If the HoloViz MCP server tools are available, DO use them to look up documentation and component details. Useful tools: `search` (documentation), `pn_search` (find components), `pn_get` (component details), `pn_params` (parameter info), `ref_get` (reference guides), `skill_get` (best-practice skills).
- If MCP tools are not available but the `holoviz-mcp` CLI is installed (also available as `hv`), use the equivalent CLI commands: `holoviz-mcp search`, `holoviz-mcp pn search`, `holoviz-mcp pn get`, `holoviz-mcp pn params`, `holoviz-mcp ref get`, `holoviz-mcp skill get`.
- If neither is available, DO search the web. For example searching the Panel website for `Tabulator` related information via [https://panel.holoviz.org/search.html?q=Tabulator](https://panel.holoviz.org/search.html?q=Tabulator) url.

### Test the app with pytest

DO add tests to the `tests` folder and run them with `pytest tests/path/to/test_file.py`.

- DO structure your code with Parameterized components, so that reactivity and user interactions can be tested easily.
- DO separate UI logic from business logic to enable unit testing
- DO separate data extraction, data transformation, plots generation, custom components and views, styles etc. to enable unit testing as your app grows
- DO fix any test errors and rerun the tests
- DO run the tests and fix errors before serving the app and asking the user to run manual tests

### Test the app manually with panel serve

DO always start and keep running a development server `panel serve path_to_file.py --dev --show` with hot reload while developing!

- Due to `--show` flag, a browser tab will automatically open showing your app.
- Due to `--dev` flag, the panel server and app will automatically reload if you change the code.
- The app will be served at http://localhost:5006/.
- DO make sure the correct virtual environment is activated before serving the app.
- DO fix any errors that show up in the terminal. Consider adding new tests to ensure they don't happen again.
- DON'T stop or restart the server after changing the code. The app will automatically reload.
- If you see 'Cannot start Bokeh server, port 5006 is already in use' in the terminal, DO serve the app on another port with `--port {port-number}` flag.
- DO remind the user to test the application on multiple screen sizes (desktop, tablet, mobile)
- DON'T use legacy `--autoreload` flag
- DON't run `python path_to_file.py` to test or serve the app.
- If you close the server to run other commands DO remember to restart it.

## Quick Reference

### Widget Creation
```python
# ✅ Good: Parameter-driven
widget = pn.widgets.Select.from_param(self.param.model_type, name="Model Type")

# ❌ Avoid: Manual management with links
widget = pn.widgets.Select(options=['A', 'B'], value='A')
widget.link(self, value='model_type')  # Hard to reason about
```

### Reactive Updates Pattern

```python
# ✅ BEST: Static pane with reactive content (for classes)
class MyComponent(pn.viewable.Viewer):
    value = param.Number(default=10)

    def __init__(self, **params):
        super().__init__(**params)
        self._plot_pane = pn.pane.Matplotlib(self._create_plot)

    @param.depends('value')
    def _create_plot(self):
        return create_plot(self.value)  # Returns plot only, not pane

# ✅ GOOD: pn.bind for functions
slider = pn.widgets.IntSlider(value=10)
plot_pane = pn.pane.Matplotlib(pn.bind(create_plot, slider))

# ❌ AVOID: Recreating panes and other components directly. This causes flickering.
@param.depends('value')
def view(self):
    return pn.pane.Matplotlib(create_plot(self.value))  # DON'T!

# ❌ AVOID: Updating panes and other components directly. This makes it hard to reason about application flow and state
@param.depends('value', watch=True)
def update_plot(self):
    self.plot_pane.object = create_plot(self.value)
```

### Static Components Pattern

```python
# DO: Create static layout with reactive content
def _get_kpi_card(self):
    return pn.pane.HTML(
        pn.Column(
            "📊 Key Performance Metrics",
            self.kpi_value  # Reactive reference
        ),
        styles={"padding": "20px", "border": "1px solid #ddd"},
        sizing_mode="stretch_width"
    )

@param.depends("characters")
def kpi_value(self):
    return f"The kpi is {self.characters}"
```

## Other Guidance

### CheckButtonGroup

- DO arrange vertically when displaying `CheckButtonGroup` in a sidebar `CheckButtonGroup(..., vertical=True)`.
- DO set `button_type="primary"` and `button_style="outline"`.

### Tabulator

- DO set `Tabulator.disabled=True` unless you would like the user to be able to edit the table.
- DO prefer [Tabulator Formatters](https://tabulator.info/docs/6.3/format) over Bokeh formatters and Pandas Styling.
- DO prefer [Tabulator Editors](https://tabulator.info/docs/6.3/edit) over Bokeh Editor types

### Markdown

- DO set `Markdown.disable_anchors=True` to avoid page flickr when hovering over headers.

### Bind

- DON't bind a function to nothing: `pn.bind(some_func)`. Just run the function instead `some_func()`.

## Plotting

- DO use bar charts over pie Charts.

### HoloViews/hvPlot

DO follow the relevant `hvplot`, `holoviews` and `panel-holoviews` skills/ best practice guides!

### Matplotlib

**CRITICAL**: On windows set non-interactive backend before importing matplotlib.pyplot:

**Why**: The `'agg'` backend is required for server-side rendering without display. Panel needs to render plots as images, not interactive GUI windows.

**Extension**: DON'T include `'matplotlib'` in `pn.extension()` - it doesn't require JavaScript loading like Plotly or Bokeh extensions.

```python
# ✅ CORRECT
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import panel as pn

pn.extension()  # No 'matplotlib' needed

# ❌ WRONG
pn.extension('matplotlib')  # Not a Panel extension
```

**Best Practices**:

- DO use matplotlib for publication-quality static plots
- DO close figures after rendering to prevent memory leaks: `plt.close(fig)`
- DO consider hvPlot or Plotly for interactive plots instead

### Plotly

Do set the template (theme) depending on the `theme` of the app.

```python
def create_plot(self) -> go.Figure:
    fig = ...
    template = "plotly_dark" if pn.state.theme=="dark" else "plotly_white"
    fig.update_layout(
        template=template, # Change template to align with the theme
        paper_bgcolor='rgba(0,0,0,0)', # Change to transparent background to align with the app background
        plot_bgcolor='rgba(0,0,0,0)' # Change to transparent background to align with the app background
    )
    return fig
```

### ECharts

DO prefer ECharts dict configuration over of pyecharts
**CRITICAL**: ECharts configurations must be JSON-serializable. Panel uses Bokeh's serialization mechanism which cannot serialize Python functions.

❌ **NEVER use Python functions or lambdas** in ECharts configuration:
```python
# ❌ WRONG: Lambda functions cause SerializationError
option = {
    "tooltip": {
        "formatter": lambda params: f"Value: {params['value']}"  # DON'T!
    },
    "xAxis": {
        "axisLabel": {
            "formatter": lambda value: f"{value}%"  # DON'T!
        }
    },
    "series": [{
        "animationDelay": lambda idx: idx * 100  # DON'T!
    }]
}
```

✅ **DO use ECharts native string formatters or static values**:
```python
# ✅ CORRECT: Use ECharts template strings
option = {
    "tooltip": {
        "formatter": "{b}: {c}"  # Template string
    },
    "xAxis": {
        "axisLabel": {
            "formatter": "{value}%"  # Template string with formatting
        }
    },
    "yAxis": {
        "axisLabel": {
            "formatter": "${value}"  # Dollar sign prefix
        }
    },
    "series": [{
        "animationDelay": 100  # Static numeric value
    }]
}
```

**ECharts Formatter Template Syntax**:

- `{a}` - series name
- `{b}` - data name (category)
- `{c}` - data value
- `{d}` - percentage (for pie charts)
- `{value}` - axis value
- Supports prefix/suffix: `'{value}%'`, `'${value}'`, `'{value} units'`

If you need complex formatting logic, pre-process your data in Python before passing to ECharts rather than using formatters.

**Reactive Updates with replaceMerge**:

When updating ECharts dynamically (e.g., filtering data that changes the number of series), ECharts uses a **merge strategy** by default. This can cause old series to persist when series are removed.

✅ **DO use `replaceMerge` option** when series count can change:
```python
# ✅ CORRECT: Use replaceMerge to fully replace series on updates
chart_pane = pn.pane.ECharts(
    self._chart_config,  # Reactive method or parameter
    options={"replaceMerge": ["series"]},  # Replace series array instead of merging
    sizing_mode="stretch_width",
    height=400,
)
```

❌ **WITHOUT replaceMerge** - old series persist:
```python
# ❌ WRONG: Old series remain when filtering reduces series count
chart_pane = pn.pane.ECharts(
    self._chart_config,
    sizing_mode="stretch_width",
)
# If config changes from 4 series to 2, ECharts merges and keeps all 4!
```

Use `replaceMerge` for any chart where:

- Users can filter data (year selectors, category filters)
- The number of series changes dynamically
- Data is grouped by categories that may be added/removed

DO make sure the chart title does not overlap with the rest of the plot including legend.

### Date time widgets

When comparing to date or time values to Pandas series convert to `Timestamp`:

```python
start_date, end_date = self.date_range
# DO convert date objects to pandas Timestamp for proper comparison
start_date = pd.Timestamp(start_date)
end_date = pd.Timestamp(end_date)
filtered = filtered[
    (filtered['date'] >= start_date) &
    (filtered['date'] <= end_date)
]
```
