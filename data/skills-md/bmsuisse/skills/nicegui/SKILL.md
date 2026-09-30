---
name: nicegui
plugin: coding
description: >
  Build Python web UIs with NiceGUI — covering layout, widgets, data binding, routing, and the AgGrid
  data grid. Use this skill whenever the user mentions NiceGUI, wants to build a Python web app,
  dashboard, or internal tool, asks about ui.aggrid, ui.page, or any NiceGUI component.
  Triggers on: "nicegui", "ui.aggrid", "ui.page", "NiceGUI app", "python web ui",
  "python dashboard", "aggrid python", "build a web interface in python".
---

# NiceGUI

NiceGUI is a Python framework that renders a reactive web UI in the browser, backed by FastAPI and Vue/Quasar. Python code runs server-side; the browser is a thin client that re-renders on state changes.

## Two modes

**Script mode** (prototypes/simple apps) — write top-level code, executed once per connection:
```python
from nicegui import ui
ui.label('Hello world')
ui.run()
```

**Page mode** (multi-page apps) — each decorated function is a private page per user:
```python
from nicegui import ui

@ui.page('/')
def index():
    ui.label('Home')

@ui.page('/dashboard')
def dashboard():
    ui.label('Dashboard')

ui.run()
```

## Auto-context

Elements are automatically added to the currently active `with`-context — no explicit parent parameter needed:

```python
with ui.card():
    ui.label('Inside card')
    ui.button('Click me', on_click=lambda: ui.notify('Hi!'))
```

## Layout elements

| Element | Description |
|---------|-------------|
| `ui.row()` | Flex row (horizontal), `wrap=True` by default |
| `ui.column()` | Flex column (vertical) |
| `ui.card()` | Card with drop shadow |
| `ui.grid(columns=3)` | CSS grid |
| `ui.tabs()` / `ui.tab_panels()` | Tab navigation |
| `ui.splitter()` | Resizable split panes (`.before` / `.after` slots) |
| `ui.expansion('Title')` | Accordion |
| `ui.scroll_area()` | Custom scrollbar container |
| `ui.dialog()` | Modal dialog |
| `ui.header()` / `ui.footer()` | Page header/footer |
| `ui.left_drawer()` / `ui.right_drawer()` | Side drawers |

```python
with ui.tabs().classes('w-full') as tabs:
    one = ui.tab('One')
    two = ui.tab('Two')
with ui.tab_panels(tabs, value=two).classes('w-full'):
    with ui.tab_panel(one):
        ui.label('First tab')
    with ui.tab_panel(two):
        ui.label('Second tab')
```

## Styling

- Tailwind CSS: `.classes('text-xl font-bold text-red-500 w-full')`
- Inline CSS: `.style('color: red; font-size: 20px')`
- Quasar props: `.props('flat color=primary dense')`

## Common widgets

```python
ui.label('text')
ui.button('Label', on_click=handler)
ui.input('Placeholder', on_change=handler)           # value via .value
ui.number('Label', min=0, max=100, value=50)
ui.checkbox('Label', on_change=handler)
ui.switch('Label')
ui.slider(min=0, max=10, step=0.5)
ui.select(['A', 'B', 'C'], label='Pick one')
ui.toggle({1: 'A', 2: 'B', 3: 'C'})
ui.date(on_change=handler)
ui.textarea('Notes')
ui.icon('home')
ui.image('https://...')
ui.markdown('**Bold** text')
ui.notify('Message', type='positive')   # type: positive|negative|warning|info
```

## Data binding

Bind UI element properties to Python objects — updates propagate both ways automatically:

```python
class State:
    name: str = 'Alice'

state = State()
ui.input('Name').bind_value(state, 'name')
ui.label().bind_text_from(state, 'name', backward=lambda n: f'Hello {n}')
```

**`@binding.bindable_dataclass`** — all fields become reactive properties (most efficient):
```python
from nicegui import binding, ui

@binding.bindable_dataclass
class State:
    count: int = 0

s = State()
ui.number().bind_value(s, 'count')
ui.label().bind_text_from(s, 'count', backward=lambda v: f'Count: {v}')
```

**`bind_value`** — two-way binding  
**`bind_value_from`** / **`bind_value_to`** — one-way  
**`bind_visibility_from(obj, 'flag')`** — show/hide element

Bind to `app.storage.user` for persistence across page loads:
```python
from nicegui import app, ui
ui.textarea().bind_value(app.storage.user, 'note')
```

## Events

```python
ui.button('Save', on_click=lambda: save())

# Async handler — use for awaitable grid methods etc.
async def handle():
    rows = await grid.get_selected_rows()
    ui.notify(str(rows))

ui.button('Selected', on_click=handle)

# Any AG Grid or DOM event
grid.on('cellClicked', lambda e: ui.notify(e.args['value']))
```

## Timers

```python
ui.timer(1.0, callback, once=False)   # recurring; once=True fires once
```

## Navigation

```python
ui.navigate.to('/other')
ui.navigate.to('https://example.com')
ui.navigate.back()
ui.navigate.reload()
```

## Custom FastAPI integration

```python
from nicegui import app
@app.get('/api/data')
def get_data():
    return {'value': 42}
```

---

## ui.aggrid — AG Grid

For detailed reference see `references/aggrid.md`. Key points:

```python
grid = ui.aggrid({
    'columnDefs': [
        {'headerName': 'Name', 'field': 'name'},
        {'headerName': 'Age', 'field': 'age'},
    ],
    'rowData': [
        {'name': 'Alice', 'age': 18},
        {'name': 'Bob', 'age': 21},
    ],
    'rowSelection': {'mode': 'multiRow'},  # or 'singleRow'
})
```

**Update data** — mutate `grid.options['rowData']` and call `grid.update()`:
```python
grid.options['rowData'].append({'name': 'Carol', 'age': 42})
grid.update()
```

**Selection** (async):
```python
async def show_selected():
    rows = await grid.get_selected_rows()    # list[dict]
    row  = await grid.get_selected_row()     # dict | None (first selected)
```

**Run AG Grid API methods**:
```python
grid.run_grid_method('selectAll')
grid.run_grid_method('setColumnsVisible', ['parent'], True)
await grid.run_grid_method('getSelectedRows')  # await to get return value
```

**Update a single row** (preserves selection):
```python
# requires ':getRowId' option
grid = ui.aggrid({
    ...,
    ':getRowId': '(params) => params.data.name',
})
grid.run_row_method('Alice', 'setDataValue', 'age', 99)
```

**From DataFrame**:
```python
import pandas as pd
df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
ui.aggrid.from_pandas(df)

import polars as pl
df = pl.DataFrame({'col1': [1, 2]})
ui.aggrid.from_polars(df)
```

**Filters**:
```python
{'headerName': 'Name', 'field': 'name',
 'filter': 'agTextColumnFilter', 'floatingFilter': True}
```

**Conditional cell styling** (Tailwind classes):
```python
{'field': 'age', 'cellClassRules': {
    'bg-red-300': 'x < 21',
    'bg-green-300': 'x >= 21',
}}
```

**Render column as HTML**:
```python
ui.aggrid({...}, html_columns=[1])  # column index 1 renders raw HTML
```

**Themes**: `'quartz'` (default), `'balham'`, `'material'`, `'alpine'`
```python
ui.aggrid({...}, theme='balham')
grid.theme = 'alpine'  # change dynamically
```

**Get/sync client edits** (when `'editable': True`):
```python
data = await grid.get_client_data()          # get without changing server state
await grid.load_client_data()                # sync edits back to options['rowData']
```

**Direct JS access**:
```python
row = await ui.run_javascript(
    f'return getElement({grid.id}).api.getDisplayedRowAtIndex(0).data'
)
```

**Enterprise** (optional):
```python
bundle_url = f'https://cdn.jsdelivr.net/npm/ag-grid-enterprise@{ui.aggrid.VERSION}/+esm'
ui.aggrid.set_module_source(bundle_url)
ui.aggrid({...}, modules='enterprise')
```

> **Gotcha**: Row data keys must not contain periods — use nested objects and dot-notation field paths (`'field': 'name.first'`) instead.

---

## ui.run() parameters

```python
ui.run(
    host='0.0.0.0',
    port=8080,
    title='My App',
    dark=None,           # None=auto, True=dark, False=light
    reload=True,         # auto-reload on file changes (dev mode)
    show=True,           # open browser on start
    storage_secret='secret_key',  # required for app.storage.user
    binding_refresh_interval=0.1,
)
```
