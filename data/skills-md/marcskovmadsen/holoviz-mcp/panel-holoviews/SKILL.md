---
name: panel-holoviews
description: Best practices for integrating HoloViews and hvPlot visualizations into Panel applications. Use when embedding HoloViews/hvPlot plots in Panel panes, preserving zoom/pan state across data refreshes with DynamicMap, composing DynamicMap overlays without type errors, using HoloViews streams (Selection1D, RangeXY, Tap, BoundsXY, Pipe, Buffer) with Panel, cross-filtering with link_selections, making HoloViews plots responsive in Panel layouts, or wiring Panel widgets to Bokeh plot properties with jslink.
metadata:
  version: "1.0.0"
  author: ahuang11
  category: web-development
  difficulty: intermediate
---

# Panel + HoloViews Integration Patterns

- DO let Panel control the renderer theme
  - DON'T set `hv.renderer('bokeh').theme = 'dark_minimal'`

---

## DynamicMap: Preserve Zoom/Pan Across Data Refreshes

When you set `pane.object = new_plot`, Bokeh resets all axes ranges. Wrap the plot function in `hv.DynamicMap` so Bokeh updates data in the existing figure rather than replacing it.

### DON'T: Replace chart object directly

```python
# BAD — zoom resets every refresh
self._chart_pane.object = df.hvplot.scatter(...)
```

### DO: Use DynamicMap with a trigger parameter

```python
class Monitor(pn.viewable.Viewer):
    _chart_trigger = param.Integer(default=0)

    def __init__(self, **params):
        super().__init__(**params)
        dmap = hv.DynamicMap(pn.bind(self._render_scatter, self.param._chart_trigger))
        self._chart_pane = pn.pane.HoloViews(dmap, sizing_mode="stretch_width")

    def _render_scatter(self, trigger):
        # Reads self.data directly; trigger is just a signal to re-invoke
        df = self.data
        if df is None or df.empty:
            return hv.Scatter([], kdims=['x'], vdims=['y']).opts(responsive=True, height=300)
        # Pass responsive and height directly to hvplot — see "Responsive Sizing" section
        return df.hvplot.scatter(x='x', y='y', responsive=True, height=300)

    def _on_data_changed(self, *events):
        # Increment trigger → DynamicMap re-invokes → Bokeh patches in place
        self._chart_trigger += 1
```

---

## One Element Per DynamicMap

Returning an `hv.Overlay` from a DynamicMap causes two problems:

1. **Type mismatch errors** — if you sometimes return `hv.Scatter` and sometimes `hv.Overlay`, DynamicMap raises `AssertionError: DynamicMap must only contain one type of object`.
2. **Lost hover tooltips** — when scatter + HLines are combined inside `hv.Overlay([...])`, the scatter's hover tool configuration doesn't propagate.

### DON'T: Return mixed types or Overlays from a single DynamicMap

```python
# BAD — type mismatch when data is empty vs populated
def render(trigger):
    if no_data:
        return hv.Text(0, 0, "empty")  # Text type
    plot = df.hvplot.scatter(...)
    return plot * hv.HLine(avg)  # Overlay type → AssertionError

# BAD — hover tooltips lost
def render(trigger):
    scatter = df.hvplot.scatter(..., tools=['hover'])
    return hv.Overlay([scatter, hv.HLine(avg)])  # hover doesn't propagate
```

### DO: Separate DynamicMap per element, combine with `*` at layout level

```python
def __init__(self, **params):
    super().__init__(**params)
    scatter_dmap = hv.DynamicMap(pn.bind(self._render_scatter, self.param._trigger))
    avg_dmap = hv.DynamicMap(pn.bind(self._render_avg_line, self.param._trigger))
    min_dmap = hv.DynamicMap(pn.bind(self._render_min_line, self.param._trigger))
    max_dmap = hv.DynamicMap(pn.bind(self._render_max_line, self.param._trigger))
    overlay = scatter_dmap * avg_dmap * min_dmap * max_dmap
    self._chart_pane = pn.pane.HoloViews(overlay, sizing_mode="stretch_width")
```

Each callback returns exactly **one element type**, always:

```python
def _render_scatter(self, trigger):
    completed = self._get_completed()
    if completed.empty:
        # Same type as the populated case — just no data
        return hv.Scatter([], kdims=['START_TIME'], vdims=['RUNTIME_SECONDS']).opts(
            bgcolor='#0d1015', height=180, responsive=True,
        )
    return completed.hvplot.scatter(x='START_TIME', y='RUNTIME_SECONDS')

def _render_avg_line(self, trigger):
    avg = self._stats().get('avg_runtime', 0)
    if avg > 0:
        return hv.HLine(avg).opts(color='orange', line_dash='dashed')
    # Invisible but valid — same type always
    return hv.HLine(0).opts(alpha=0)
```

Benefits:

- Each DynamicMap always returns the same HoloViews element type (no `AssertionError`)
- Scatter keeps its hover tools natively (tools are per-element, not per-overlay)
- Each layer updates independently
- Static layers (like a tile source) can be pulled out of DynamicMap entirely

Note: `Element * DynamicMap` or `DynamicMap * DynamicMap` yields a `DynamicMap`, not a static `hv.Overlay`. This is expected — Panel handles it the same way via `pn.pane.HoloViews`.

---

## Responsive Sizing

HoloViews `.opts(width=, height=, responsive=)` and Panel's `sizing_mode` on `pn.pane.HoloViews` are two separate sizing systems. They conflict if misconfigured.

### DO: Pass `responsive=True` and `height` directly to the hvplot call

```python
# hvplot: pass responsive and height as arguments so hvplot does NOT set a default fixed width
plot = df.hvplot.scatter(x='time', y='value', responsive=True, height=300)
pane = pn.pane.HoloViews(plot, sizing_mode="stretch_width")

# Pure HoloViews: .opts() is fine because HoloViews doesn't inject a default width
plot = hv.Curve(df, 'time', 'value').opts(responsive=True, height=300)
pane = pn.pane.HoloViews(plot, sizing_mode="stretch_width")
```

### DON'T: Use `.opts(responsive=True)` on an hvplot object

```python
# BAD — hvplot internally sets width=700; .opts(responsive=True) doesn't remove it.
# Bokeh sees both fixed width and responsive=True → warning + broken layout.
# Inside a DynamicMap the plot shrinks on every refresh.
plot = df.hvplot.scatter(x='time', y='value').opts(responsive=True, height=300)

# BAD — same problem with explicit fixed width
plot = df.hvplot.scatter(...).opts(width=600, height=300)
pane = pn.pane.HoloViews(plot, sizing_mode="stretch_width")
```

**Key rules**:

- **hvplot**: always pass `responsive=True` + `height=<int>` as **arguments to the hvplot call** (e.g. `df.hvplot.scatter(..., responsive=True, height=300)`), and `sizing_mode="stretch_width"` on the pane. Do NOT use `.opts()` for these — hvplot sets a default `width=700` internally and `.opts()` cannot remove it.
- **Pure HoloViews**: using `.opts(responsive=True, height=<int>)` is fine because HoloViews elements don't inject a default fixed width.
- For fixed size: set `width=<int>` + `height=<int>` in `.opts()`, omit `sizing_mode` on the pane
- DON'T mix fixed `width` in opts with `sizing_mode` on the pane — Panel overrides the width but emits a warning; the conflict makes behavior ambiguous
- Never set both `width` and `responsive=True` in `.opts()` — `width` wins and responsive is silently ignored

---

## HoloViews Streams with Panel

HoloViews streams let you react to user interactions on plots (clicks, selections, zoom) inside a Panel app. Attach streams to a DynamicMap; Panel wires up the callbacks automatically.

### Selection1D: React to selected points

```python
import holoviews as hv
from holoviews import streams

points = hv.Points(df, kdims=['x', 'y']).opts(tools=['tap', 'box_select'], size=8)
selection = streams.Selection1D(source=points)

def show_selected(index):
    if not index:
        return hv.Table(df.iloc[:0], kdims=['x', 'y'])
    return hv.Table(df.iloc[index], kdims=['x', 'y'])

table_dmap = hv.DynamicMap(show_selected, streams=[selection])
pn.Row(points, table_dmap).servable()
```

### RangeXY: React to zoom/pan range

```python
curve = hv.Curve(df, 'time', 'value')
range_stream = streams.RangeXY(source=curve)

def show_stats(x_range, y_range):
    if x_range is None:
        return hv.Text(0, 0, "Zoom to select range")
    x0, x1 = x_range
    subset = df[(df['time'] >= x0) & (df['time'] <= x1)]
    return hv.Text(0, 0, f"Mean: {subset['value'].mean():.2f}")

stats_dmap = hv.DynamicMap(show_stats, streams=[range_stream])
pn.Column(curve, stats_dmap).servable()
```

### Tap: React to click location

```python
points = hv.Points(df, kdims=['x', 'y']).opts(tools=['tap'], size=8)
tap_stream = streams.Tap(source=points)

def on_tap(x, y):
    if x is None:
        return hv.Text(0, 0, "Click a point")
    return hv.Text(x, y, f"({x:.1f}, {y:.1f})").opts(text_font_size='12pt')

tap_dmap = hv.DynamicMap(on_tap, streams=[tap_stream])
(points * tap_dmap).servable()
```

### Pipe / Buffer: Push streaming data

```python
from holoviews.streams import Pipe, Buffer

# Pipe — replace data entirely each push
pipe = Pipe(data=[])
# framewise=True: recompute axis ranges on each push (without it, axes lock to first frame)
pipe_dmap = hv.DynamicMap(hv.Curve, streams=[pipe]).opts(framewise=True)

def update():
    pipe.send(new_dataframe)

# Buffer — append data, keep last N rows
buffer = Buffer(df.iloc[:0], length=500)
buffer_dmap = hv.DynamicMap(hv.Curve, streams=[buffer]).opts(framewise=True)

def update():
    buffer.send(new_rows_df)
```

### Common stream pitfalls

- **Forgot tools**: `Selection1D` needs `tools=['tap', 'box_select']` in `.opts()` — without them no events fire
- **Unhandled None**: Stream callbacks receive `None`/empty values on first render — always guard with `if not index:` or `if x is None:`
- **Don't mix mechanisms**: Use either streams OR `param.depends`/`pn.bind` for a given plot — not both
- **Frozen axes with Pipe/Buffer**: By default DynamicMap locks axis ranges to the first frame. Use `.opts(framewise=True)` so axes update when data ranges change

---

## Linked Selections / Cross-Filtering

`hv.link_selections` provides automatic cross-filtering across plots. LLMs often try to build this manually with streams — use the built-in API instead.

### Basic usage

```python
import holoviews as hv
from holoviews.operation import histogram

ls = hv.link_selections.instance()

scatter = hv.Points(df, kdims=['x', 'y'])
# DO use hv.operation.histogram — preserves link to source data so
# link_selections can filter by all source dimensions (x AND y)
hist_x = histogram(scatter, dimension='x', num_bins=20)
hist_y = histogram(scatter, dimension='y', num_bins=20)

# Wrap each plot — selections in one propagate to all
layout = ls(scatter) + ls(hist_x) + ls(hist_y)
pn.pane.HoloViews(layout, sizing_mode="stretch_width").servable()
```

### Categorical bars: Custom Operation for categorical aggregation

`hv.operation.histogram` only works for **numeric** dimensions. For categorical bar charts
(e.g. counting trades per commodity, or computing mean P&L per region), you need a custom
`Operation` subclass. Because operations wrap the source element, `link_selections` can
"unwrap" them to access all original dimensions when resolving cross-filter expressions.

```python
from holoviews.core import Operation

class categorical_agg(Operation):
    """Aggregate a categorical dimension, returning Bars.

    Preserves data lineage back to the source element so that
    link_selections can resolve all source dimensions during cross-filtering.
    """

    dimension = param.String(doc="Categorical dimension to group by")
    value_dimension = param.String(
        default=None,
        allow_None=True,
        doc="Numeric dimension to aggregate. None means count rows.",
    )
    function = param.Callable(
        default=np.size,
        doc="Aggregation function (np.sum, np.mean, np.std, np.min, np.max, ...)",
    )
    label = param.String(
        default=None,
        allow_None=True,
        doc="Label for the value axis. Auto-generated if None.",
    )

    def _process(self, element, key=None):
        cat_vals = element.dimension_values(self.p.dimension, expanded=True)
        unique_cats = np.unique(cat_vals)

        if self.p.value_dimension is None:
            # Pure count
            _, counts = np.unique(cat_vals, return_counts=True)
            agg_label = self.p.label or "Count"
            data = list(zip(unique_cats, counts))
        else:
            num_vals = element.dimension_values(self.p.value_dimension, expanded=True)
            results = []
            for cat in unique_cats:
                mask = cat_vals == cat
                results.append(self.p.function(num_vals[mask]))
            func_name = getattr(self.p.function, "__name__", "agg")
            agg_label = self.p.label or f"{func_name}({self.p.value_dimension})"
            data = list(zip(unique_cats, results))

        return hv.Bars(data, kdims=[self.p.dimension], vdims=[agg_label])

# Usage with link_selections:
ls = hv.link_selections.instance()
points = hv.Points(df, kdims=['price', 'volume'],
                   vdims=['commodity', 'region', 'trade_type', 'pnl'])

hist_price = histogram(points, dimension='price', num_bins=20)           # numeric → histogram
bars_commodity = categorical_agg(points, dimension='commodity')          # categorical count (default)
bars_avg_pnl = categorical_agg(points, dimension='commodity',           # categorical mean
                               value_dimension='pnl', function=np.mean)

layout = ls(points) + ls(hist_price) + ls(bars_commodity) + ls(bars_avg_pnl)
```

**Why this works**: HoloViews operations maintain a reference to their source element.
When `link_selections` encounters a selection expression like `(dim('price') >= 50)`,
it recurses into the operation's source (`points`) where `price` exists, applies the
filter, then re-runs the operation on the filtered data. Pre-aggregated `hv.Bars` lack
this source reference, so the expression cannot resolve and raises `CallbackError`.

### DON'T: Use pre-binned histograms, pre-aggregated data, or histogram on categorical dimensions

```python
# BAD — pre-binned histogram loses data lineage; link_selections can't resolve
# the scatter's 'y' dimension on the histogram → CallbackError
hist = hv.Histogram(np.histogram(df['x'], bins=20), kdims='x')

# BAD — pre-aggregated bars lose the original x/y columns;
# selection expressions referencing those dimensions → CallbackError
bars = hv.Bars(df.groupby('cat').size().reset_index(name='n'), kdims='cat', vdims='n')

# BAD — histogram() only supports numeric dimensions;
# raises "Cannot create histogram from categorical data"
bars = histogram(points, dimension='commodity')

# BAD — hv.Bars(raw_df, kdims=['cat']) auto-detects ALL other columns as vdims,
# including datetime and string columns that cause DType errors during rendering
bars = hv.Bars(df, kdims=['commodity'])  # timestamp vdim → DTypePromotionError
```

### Accessing the selection for filtering

```python
ls = hv.link_selections.instance()
# ... build linked plots ...

# selection_expr is a HoloViews dim expression — apply it to a Dataset, not a raw DataFrame
ds = hv.Dataset(df, kdims=["x", "y"])
expr = ls.selection_expr
if expr is not None:
    mask = expr.apply(ds)        # returns a boolean numpy array
    filtered_df = df[mask]
```

**Key rules**:

- DO use `.instance()` to create the link_selections object — calling `hv.link_selections(plot)` directly returns a plot, not a reusable linker
- DO apply `selection_expr` to a `hv.Dataset`, not a pandas DataFrame — `expr.apply(df)` raises `AttributeError`
- DO use `hv.operation.histogram(source_element, dimension='x')` for histograms — this preserves the data lineage so `link_selections` can filter by all source dimensions. DON'T use `hv.Histogram(np.histogram(...))` — pre-binned histograms lose the source data link, and `link_selections` raises `CallbackError` when the selection expression references dimensions not present on the histogram
- DO use a custom `Operation` subclass (like `categorical_agg` above) for **categorical bar charts** — this preserves data lineage the same way `histogram` does for numeric dimensions. Supports count (default), sum, mean, std, min, max, or any custom callable via the `function` parameter. DON'T use `histogram()` on categorical dimensions (it raises an error) and DON'T use pre-aggregated `groupby().size()` bars (they lose the source data link)
- DON'T add selection tools manually — `link_selections` adds `box_select` and `lasso_select` automatically
- Each linked plot must share the same dimension names for cross-filtering to work
- **Dependencies**: `link_selections` requires `pyarrow` at runtime for selection display. Lasso selection additionally requires `shapely` (or `spatialpandas`). Install both: `pip install pyarrow shapely`. Without `pyarrow`, selections silently fail with `CallbackError`; without `shapely`, lasso raises `ImportError` while box-select still works

---

## Client-Side Interactions with `jslink`

For styling/visual controls that don't need Python computation, use `jslink` to wire Panel widgets directly to Bokeh properties. No server roundtrip, works in saved HTML files.

### Simple property binding

```python
# Float slider → glyph fill alpha (also works for size, line_width, fill_color, etc.)
widget = pn.widgets.FloatSlider(value=1, step=0.01)
plot = hv.Points((x, y)).opts(size=10)
widget.jslink(plot, value='glyph.fill_alpha')

# Text input → plot title
widget = pn.widgets.TextInput(value="Title")
plot = hv.Curve((x, y)).opts(title="Title")
widget.jslink(plot, value="plot.title.text")

# Text input → axis label
widget = pn.widgets.TextInput(value="X Label")
plot = hv.Curve((x, y)).opts(xlabel="X Label")
widget.jslink(plot, value="xaxis.axis_label")

# RadioButtonGroup → title alignment
widget = pn.widgets.RadioButtonGroup(options=["left", "center", "right"])
widget.jslink(plot, value="plot.title.align")
```

### JavaScript code callbacks

For transforms that need a bit of JS logic, use the `code` parameter:

```python
# Range slider → axis limits
widget = pn.widgets.RangeSlider(start=0, end=10)
plot = hv.Curve((x, y))
widget.jslink(plot, code={'value': """
    x_range.start = cb_obj.value[0];
    x_range.end = cb_obj.value[1];
"""})
```

**Bokeh property targets available via jslink**:

- `glyph.*` — fill_alpha, fill_color, size, line_width, line_color, etc.
- `plot.title.*` — text, text_font_size, align
- `xaxis.*` / `yaxis.*` — axis_label, etc.
- `x_range.*` / `y_range.*` — start, end
- `color_mapper.*` — low, high, palette

**When to use jslink vs DynamicMap**:

- `jslink` — pure visual/styling changes, axis limits, color tweaks. No Python needed.
- `DynamicMap` — data transformations, aggregations, anything that needs Python computation.

---

## `pn.pane.HoloViews` Configuration

| Parameter | Type | Description |
|---|---|---|
| `linked_axes` | bool (True) | Link axes ranges across plots in a layout |
| `widget_location` | str ('right') | Location of groupby/DynamicMap widgets: 'left', 'right', 'top', 'bottom', etc. |
| `center` | bool (False) | Center the plot in the pane |
| `theme` | str/Theme (None) | Bokeh theme override — use instead of `hv.renderer().theme` |
| `backend` | str ('bokeh') | HoloViews plotting backend |
| `sizing_mode` | str (None) | Panel sizing: 'stretch_width', 'stretch_both', 'fixed', etc. |

---

## Summary Checklist

| Pattern | Do | Don't |
|---|---|---|
| Preserve zoom | `hv.DynamicMap(pn.bind(fn, trigger))` | `pane.object = new_plot` |
| Overlay composition | One DynamicMap per element, `*` at layout | `hv.Overlay([...])` inside callback |
| Empty chart state | `hv.Scatter([], kdims=..., vdims=...)` | `hv.Overlay([])` or `hv.Text(...)` |
| Responsive width (hvplot) | `df.hvplot(..., responsive=True, height=N)` + `sizing_mode="stretch_width"` on pane | `.opts(responsive=True)` after hvplot (hvplot's default `width=700` persists, conflicts) |
| Responsive width (HoloViews) | `.opts(responsive=True, height=N)` + `sizing_mode="stretch_width"` on pane | Fixed `width` in opts (conflicts with responsive pane, emits warning) |
| React to selections | `streams.Selection1D(source=plot)` + DynamicMap | Manual click tracking with `param.depends` |
| Cross-filtering | `hv.link_selections.instance()` | Building manual stream wiring |
| Cross-filter categorical bars | `categorical_agg` `Operation` subclass on source element | Pre-aggregated `groupby().size()` bars or `histogram()` on categorical dims |
| Streaming data | `Pipe` (replace) or `Buffer` (append) streams | Replacing pane.object in a loop |
| Renderer theme | `pn.pane.HoloViews(plot, theme=...)` | `hv.renderer('bokeh').theme = ...` |
| Client-side styling | `widget.jslink(plot, value='glyph.fill_alpha')` | DynamicMap for pure visual tweaks |
