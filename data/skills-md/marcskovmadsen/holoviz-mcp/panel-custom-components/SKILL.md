---
name: panel-custom-components
description: Build custom Panel components using JSComponent (vanilla JS, web components), ReactComponent (React/JSX), AnyWidgetComponent (AnyWidget spec for cross-platform), or MaterialUIComponent (Material UI themed). Use when wrapping JS libraries, creating interactive widgets, or building themed components. Includes decision guide, best practices, DOs/DON'Ts, and Playwright UI testing patterns.
metadata:
  version: "1.0.0"
  author: holoviz
  category: web-development
  difficulty: advanced
---

# Panel Custom Components

This skill covers building custom Panel components that bridge Python and JavaScript. Use it when you need to:

- Wrap JavaScript libraries (D3, Leaflet, Chart.js, etc.)
- Create interactive widgets with custom UI behavior
- Create Material UI themed components for `panel-material-ui` apps

**Prerequisites:** Solid JavaScript and React knowledge assumed.


## 1. Decision Guide - Which Component Type to Use

### Comparison Table

| Criteria | JSComponent | ReactComponent | AnyWidgetComponent | MaterialUIComponent |
|----------|-------------|----------------|-------------------|---------------------|
| **Best For** | Vanilla JS libs, Web Components, D3, Leaflet, simple widgets | React ecosystem, complex state, MUI/Chakra libs | Cross-platform (Jupyter+Panel), community sharing | `panel-material-ui` apps, MUI theming |
| **JS Pattern** | DOM manipulation | React/JSX | AnyWidget AFM spec | React/JSX + MUI |
| **State Sync** | `model.on('param', cb)` | `model.useState("param")` | `model.get/set/save_changes` | `model.useState("param")` |
| **Export** | `export function render({model, el})` | `export function render({model, el})` | `export default { render }` | `export function render({model, el})` |
| **Base Import** | `panel.custom.JSComponent` | `panel.custom.ReactComponent` | `panel.custom.AnyWidgetComponent` | `panel_material_ui.MaterialUIComponent` |

### Decision Flow

```
┌─────────────────────────────────────────────────────────────────┐
│ Need Material UI theming / using panel-material-ui?             │
│   YES → MaterialUIComponent                                      │
│   NO  ↓                                                          │
├─────────────────────────────────────────────────────────────────┤
│ Need Jupyter compatibility / sharing community widgets?          │
│   YES → AnyWidgetComponent                                       │
│   NO  ↓                                                          │
├─────────────────────────────────────────────────────────────────┤
│ Using React libraries or need complex state management?          │
│   YES → ReactComponent                                           │
│   NO  ↓                                                          │
├─────────────────────────────────────────────────────────────────┤
│ Vanilla JS, Web Components, or simple DOM manipulation?          │
│   YES → JSComponent                                              │
└─────────────────────────────────────────────────────────────────┘
```


## 2. Development Workflow

> **Important:** Build custom components in two phases. By experience, getting JS imports and responsive sizing to work can take significant debugging effort.

### Phase 1: POC (Proof of Concept)

Before building the full component, create a minimal example **using your actual target library** that validates:

1. **JS imports work** - The library loads without "Unexpected token 'export'" or CORS errors
2. **Library renders something** - You can see actual output from the library (a chart, a map, a widget, etc.)
3. **Python-JS connection works** - State syncs bidirectionally via `model.on()` / `model.useState()`
4. **Element displays responsively** - Component fills container and handles resize events

**The goal is to see your library working** in a Panel component before investing time in the full implementation. Use the template below as a starting point, but replace the placeholder library with your actual library and render something real from it.

**Minimal POC template:**

```python
import param
from panel.custom import JSComponent

class MyComponentPOC(JSComponent):
    """Minimal POC to validate imports and responsiveness.

    Replace 'my-lib' with your actual library and render something from it!
    """

    value = param.String(default="Hello")

    _importmap = {
        "imports": {
            # Replace with your actual library
            "my-lib": "https://esm.sh/my-lib@1.0.0",
        }
    }

    _esm = """
    import myLib from 'my-lib';

    export function render({ model, el }) {
        // 1. Verify import works
        console.log('Library loaded:', myLib);

        // 2. Render something from the library!
        // Replace this with actual library usage, e.g.:
        //   - myLib.createChart(el, data)
        //   - new myLib.Map(el)
        //   - myLib.render(<Component />, el)
        const div = document.createElement('div');
        div.id = 'poc-element';
        div.textContent = model.value;

        // 3. Verify Python-JS sync
        model.on('value', () => { div.textContent = model.value; });

        // 4. Verify responsive sizing
        div.style.cssText = 'width:100%;height:100%;background:#f0f0f0;';
        model.on('resize', () => {
            console.log('Resize:', el.clientWidth, el.clientHeight);
        });

        el.appendChild(div);
    }
    """

# Test with explicit dimensions first, then responsive
poc = MyComponentPOC(value="Test", height=200, sizing_mode="stretch_width")
poc.servable()
```

ALWAYS test the UI via Playwright smoke tests! (see details below)

**POC validation checklist:**

- [ ] No console errors (especially import/CORS errors)
- [ ] Library object logs correctly in console
- [ ] **Library renders visible output** (chart, map, widget, etc.)
- [ ] Changing `poc.value = "New"` updates the display
- [ ] Component has non-zero dimensions
- [ ] Resize events fire when browser window changes

### Phase 2: Finalize

Once the POC validates all three concerns, build out the full component:

1. Add all parameters and their JS sync handlers
2. Implement the full library integration
3. Add error handling and edge cases
4. Add CSS styling via `_stylesheets`

## 3. Core Patterns (All Component Types)

### Python Class Structure

All custom components inherit from a base class and use `param` for state:

```python
import param
from panel.custom import JSComponent  # or ReactComponent, AnyWidgetComponent
from pathlib import Path

class MyComponent(JSComponent):
    """A custom component with Python-JS state synchronization."""

    # Define parameters that sync with JavaScript
    value = param.Integer(default=0, bounds=(0, 100), doc="Current value")
    label = param.String(default="Click me", doc="Button label")

    # ESM code (inline string or external file)
    _esm = Path(__file__).parent / "my_component.js"

    # Optional: CDN imports
    _importmap = {
        "imports": {
            "lodash": "https://esm.sh/lodash@4.17.21",
        }
    }

    # Optional: CSS styles
    _stylesheets = [
        Path(__file__).parent / "my_component.css",
        # Or inline CSS string
    ]
```

### ESM Export Pattern

All component types export a `render` function:

```javascript
// JSComponent / ReactComponent / MaterialUIComponent
export function render({ model, el }) {
    // model: access to Python parameters
    // el: DOM element to render into
}

// AnyWidgetComponent uses default export
export default {
    render({ model, el }) {
        // Same signature
    }
}
```

### Import Maps for CDN Dependencies

```python
_importmap = {
    "imports": {
        # Basic import
        "canvas-confetti": "https://esm.sh/canvas-confetti@1.6.0",

        # Namespace import (trailing slash)
        "@mui/material/": "https://esm.sh/@mui/material@5.16.7/",

        # Shared dependencies with ?external=
        "my-react-lib": "https://esm.sh/my-react-lib?external=react,react-dom",
    }
}
```

### Child and Children Parameters

Nest Panel components inside custom components:

```python
from panel.custom import JSComponent, Child, Children

class Container(JSComponent):
    header = Child()           # Single child
    items = Children()         # Multiple children

    _esm = """
    export function render({ model, el }) {
        const header = model.get_child("header");
        el.appendChild(header);

        for (const item of model.get_child("items")) {
            el.appendChild(item);
        }
    }
    """
```

### Event Handling

**JavaScript → Python:**

```javascript
// In JavaScript
button.onclick = () => {
    model.send_event('button_click', { timestamp: Date.now() });
};
```

```python
# In Python
class MyComponent(JSComponent):
    def _handle_button_click(self, event):
        print(f"Button clicked at {event.data['timestamp']}")
```

**Python → JavaScript:**

```python
# In Python
class MyComponent(JSComponent):
    def trigger_animation(self):
        self.send_msg({'action': 'animate', 'duration': 500})
```

```javascript
// In JavaScript
model.on('msg:custom', (event) => {
    if (event.data.action === 'animate') {
        runAnimation(event.data.duration);
    }
});
```

## 4. JSComponent Patterns

JSComponent is the foundation for building custom Panel components with vanilla JavaScript. Use it for DOM manipulation, Web Components, and wrapping libraries like D3, Leaflet, or Chart.js.

### Basic Structure

```python
import param
from panel.custom import JSComponent

class CounterButton(JSComponent):
    """A simple counter button component."""

    value = param.Integer(default=0, doc="Current count")

    _esm = """
    export function render({ model, el }) {
        const button = document.createElement('button');
        button.id = 'counter-btn';

        function update() {
            button.textContent = `Count: ${model.value}`;
        }

        button.onclick = () => {
            model.value += 1;
        };

        model.on('value', update);
        update();  // Initialize

        el.appendChild(button);
    }
    """
```

### State Synchronization

**Reading and Writing Parameters:**

```javascript
// Direct property access
const currentValue = model.value;
const label = model.label;

// Direct assignment syncs to Python
model.value = 42;
model.label = "New Label";
```

**Subscribing to Changes:**

```javascript
export function render({ model, el }) {
    const display = document.createElement('div');

    // Subscribe to changes
    model.on('value', () => {
        display.textContent = model.value;
    });

    // Initialize with current value
    display.textContent = model.value;

    el.appendChild(display);
}
```

### Lifecycle Hooks

```javascript
// render - Initial render (called once)
export function render({ model, el }) {
    // Setup DOM, event listeners
}

// after_render - Post-render (useful for measurements)
export function after_render({ model, el }) {
    const { width, height } = el.getBoundingClientRect();
    initChart(el, width, height);
}

// resize - Size changes
model.on('resize', ({ width, height }) => {
    canvas.width = width;
    canvas.height = height;
    redraw();
});

// remove - Cleanup
model.on('remove', () => {
    clearInterval(interval);
    document.removeEventListener('keypress', handler);
});
```

### External Libraries Example (D3)

```python
class D3BarChart(JSComponent):
    data = param.List(default=[10, 20, 30, 40, 50])

    _importmap = {
        "imports": {
            "d3": "https://esm.sh/d3@7"
        }
    }

    _esm = """
    import * as d3 from 'd3';

    export function render({ model, el }) {
        const svg = d3.select(el)
            .append('svg')
            .attr('width', 400)
            .attr('height', 200);

        function update() {
            const bars = svg.selectAll('rect').data(model.data);

            bars.enter()
                .append('rect')
                .merge(bars)
                .attr('x', (d, i) => i * 50)
                .attr('y', d => 200 - d * 3)
                .attr('width', 40)
                .attr('height', d => d * 3)
                .attr('fill', 'steelblue');

            bars.exit().remove();
        }

        model.on('data', update);
        update();
    }
    """
```

## 4.1. Wrapping Third-Party Web Components

When wrapping existing web components, follow these patterns:

### Custom Element Lifecycle

**Recommended: Use ESM imports** instead of `__javascript__` to avoid race conditions and timing issues. ESM imports guarantee the web component is fully loaded before your `render()` function executes.

**JavaScript with ESM import:**

```javascript
// Import ensures web component is registered before render executes
import "https://esm.sh/@google/model-viewer@3.4.0";

export function render({ model, el }) {
    const viewer = document.createElement('model-viewer');
    viewer.id = 'model-viewer';
    viewer.style.display = "block";
    viewer.style.width = "100%";
    viewer.style.height = "100%";

    // Safe to set attributes immediately - component is guaranteed loaded
    viewer.alt = model.alt;
    if (model.src) viewer.setAttribute("src", model.src);
    if (model.auto_rotate) viewer.setAttribute("auto-rotate", "");
    if (model.camera_controls) viewer.setAttribute("camera-controls", "");

    el.appendChild(viewer);

    // Handle parameter changes - add/remove boolean attributes
    model.on('auto_rotate', () => {
        if (model.auto_rotate) viewer.setAttribute("auto-rotate", "");
        else viewer.removeAttribute("auto-rotate");
    });

    // Error handling
    viewer.addEventListener('error', (event) => {
        console.error("Component error:", event.detail);
    });
}
```

> **Why avoid `__javascript__`?** The `__javascript__` class attribute loads scripts asynchronously in parallel with your ESM code. This creates a race condition where `render()` may execute before the custom element is registered, causing `document.createElement('model-viewer')` to create a generic `HTMLElement` instead of the proper web component. ESM imports are resolved before your module executes, eliminating this timing issue.

**Fallback: Using `customElements.whenDefined()`**

If you must use `__javascript__` (e.g., for libraries without ESM builds), protect against race conditions with `customElements.whenDefined()`:

```javascript
export function render({ model, el }) {
    const viewer = document.createElement('model-viewer');

    // Set attributes BEFORE adding to DOM (available during upgrade)
    if (model.auto_rotate) {
        viewer.setAttribute('auto-rotate', '');
    }

    el.appendChild(viewer);

    // Wait for custom element to be defined, then set properties
    customElements.whenDefined('model-viewer').then(() => {
        viewer.autoRotate = model.auto_rotate;  // Property access now works
    });

    // Handle parameter changes
    model.on('auto_rotate', () => {
        viewer.setAttribute('auto-rotate', model.auto_rotate ? '' : null);
        if (typeof viewer.autoRotate !== 'undefined') {
            viewer.autoRotate = model.auto_rotate;
        }
    });
}
```

## 5. ReactComponent Patterns

ReactComponent enables building custom Panel components with React and JSX. Use it for complex state management and React library integration.

### Basic Structure

```python
import param
from panel.custom import ReactComponent

class CounterButton(ReactComponent):
    """A simple counter button using React."""

    value = param.Integer(default=0, doc="Current count")

    _esm = """
    export function render({ model }) {
        const [value, setValue] = model.useState("value");

        return (
            <button id="counter-btn" onClick={() => setValue(value + 1)}>
                Count: {value}
            </button>
        );
    }
    """
```

### State Hooks

**`model.useState()` - Synced State:**

```javascript
export function render({ model }) {
    // Syncs bidirectionally with Python's self.value
    const [value, setValue] = model.useState("value");
    const [name, setName] = model.useState("name");

    return (
        <div>
            <input value={name} onChange={(e) => setName(e.target.value)} />
            <p>Value: {value}</p>
        </div>
    );
}
```

**`React.useState()` - Local State:**

```javascript
export function render({ model }) {
    const [synced, setSynced] = model.useState("value");  // Syncs to Python
    const [local, setLocal] = React.useState(false);       // UI-only

    return (
        <div>
            <input
                value={synced}
                onChange={(e) => setSynced(e.target.value)}
                onFocus={() => setLocal(true)}
                onBlur={() => setLocal(false)}
            />
            {local && <span>Editing...</span>}
        </div>
    );
}
```

### React Hooks

All standard React hooks are available via the global `React` object:

```javascript
export function render({ model }) {
    const inputRef = React.useRef(null);
    const [data, setData] = model.useState("data");
    const [loading, setLoading] = React.useState(true);

    React.useEffect(() => {
        fetchData().then(result => {
            setData(result);
            setLoading(false);
        });
        return () => console.log("Cleanup");
    }, []);

    const filteredData = React.useMemo(() => {
        return data.filter(item => item.active);
    }, [data]);

    if (loading) return <div>Loading...</div>;
    return <DataDisplay data={filteredData} />;
}
```

### External React Libraries

```python
class ChartComponent(ReactComponent):
    _importmap = {
        "imports": {
            # React libraries need ?external=react,react-dom
            "recharts": "https://esm.sh/recharts@2?external=react,react-dom",
        }
    }

    _esm = """
    import { LineChart, Line, XAxis, YAxis } from 'recharts';

    export function render({ model }) {
        const [data] = model.useState("data");

        return (
            <LineChart width={400} height={300} data={data}>
                <XAxis dataKey="name" />
                <YAxis />
                <Line type="monotone" dataKey="value" stroke="#8884d8" />
            </LineChart>
        );
    }
    """
```


## 6. AnyWidgetComponent Patterns

AnyWidgetComponent enables building custom Panel components using the AnyWidget specification for cross-platform compatibility (Jupyter + Panel).

### Basic Structure

```python
import param
from panel.custom import AnyWidgetComponent

class CounterButton(AnyWidgetComponent):
    """A simple counter using AnyWidget API."""

    value = param.Integer(default=0, doc="Current count")

    _esm = """
    export default {
        render({ model, el }) {
            const button = document.createElement('button');
            button.id = 'counter-btn';

            function update() {
                button.textContent = `Count: ${model.get("value")}`;
            }

            button.onclick = () => {
                model.set("value", model.get("value") + 1);
                model.save_changes();  // Required!
            };

            model.on("change:value", update);
            update();

            el.appendChild(button);
        }
    }
    """
```

### AnyWidget Model API

**Reading Values:**

```javascript
const value = model.get("value");
const name = model.get("name");
```

**Writing Values (must call `save_changes()`):**

```javascript
model.set("value", 42);
model.set("name", "Alice");
model.save_changes();  // Required to sync to Python!
```

**Listening for Changes:**

```javascript
model.on("change:value", () => {
    console.log("Value changed to:", model.get("value"));
});

// Multiple parameters
["name", "count"].forEach(param => {
    model.on(`change:${param}`, updateUI);
});
```

### React with AnyWidget

```python
class ReactCounter(AnyWidgetComponent):
    value = param.Integer(default=0)

    _importmap = {
        "imports": {
            # Pin to React 18.2.0 (most stable) and bundle deps together
            # Using ?deps= ensures consistent internal references
            "@anywidget/react": "https://esm.sh/@anywidget/react@0.2?deps=react@18.2.0,react-dom@18.2.0",
            "react": "https://esm.sh/react@18.2.0",
        }
    }

    _esm = """
    import * as React from "react";  /* mandatory import */
    import { createRender, useModelState } from "@anywidget/react";

    const render = createRender(() => {
        const [value, setValue] = useModelState("value");

        return (
            <button onClick={() => setValue(value + 1)}>
                Count: {value}
            </button>
        );
    });

    export default { render };
    """
```

> **Important:** Always pin React versions when using `@anywidget/react`. Use `?deps=react@18.2.0,react-dom@18.2.0` to bundle dependencies together with specific versions. Without version pinning, esm.sh serves React 19 which has breaking changes.

## 7. MaterialUIComponent Patterns

MaterialUIComponent enables building custom components that integrate with `panel-material-ui` theming.

> **Note:** MaterialUIComponent uses `_esm_base` (not `_esm`) because it builds on the existing panel-material-ui JavaScript bundle which includes React and MUI dependencies. For complete examples, see the [panel-material-ui custom components guide](https://panel-material-ui.holoviz.org/how_to/custom.html).

### Server Mode Workaround for Inline ESM

Inline `_esm_base` strings have a known issue in **server mode** (`panel serve`) where the `ThemedTransform` adds `./utils` imports that aren't properly resolved. External `.jsx` files work without this issue.

**Apply this one-time patch at module load to fix inline `_esm_base` in server mode:**

```python
import re
from panel_material_ui import MaterialUIComponent

def patch_material_ui_inline_esm():
    """
    Temporary fix for inline _esm_base in server mode.
    Apply once at module load. See: issue #563
    """
    original = MaterialUIComponent._render_esm_base

    @classmethod
    def patched(cls):
        esm = original.__func__(cls)
        # Replace ./utils import:
        # - install_theme_hooks: from bundle
        # - apply_global_css: no-op (only for global CSS styling)
        return re.sub(
            r'import\s+\{[^}]*\}\s+from\s+"\.\/utils";?\s*',
            'import pnmui from "panel-material-ui"; const install_theme_hooks = pnmui.install_theme_hooks; const apply_global_css = () => {};\n',
            esm
        )

    MaterialUIComponent._render_esm_base = patched

# Apply at module load
patch_material_ui_inline_esm()
```

After applying the patch, all MaterialUIComponent subclasses with inline `_esm_base` work in server mode without any code changes. This workaround is tracked in [panel-material-ui#563](https://github.com/panel-extensions/panel-material-ui/issues/563).

### Basic Structure

```python
import param
from panel_material_ui import MaterialUIComponent

class StyledButton(MaterialUIComponent):
    """A custom button with Material UI styling."""

    label = param.String(default="Click me", doc="Button label")
    variant = param.Selector(default="contained", objects=["text", "outlined", "contained"])

    _esm_base = """
    import Button from "@mui/material/Button";

    export function render({ model }) {
        const [label] = model.useState("label");
        const [variant] = model.useState("variant");

        return (
            <Button
                id="styled-btn"
                variant={variant}
                onClick={() => model.send_event("click", {})}
            >
                {label}
            </Button>
        );
    }
    """

    def _handle_click(self, event):
        print("Button clicked!")
```

### MUI Component Imports

MaterialUIComponent has `@mui/material/` pre-configured:

```javascript
// Individual imports
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import Card from "@mui/material/Card";

// Layout
import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import Grid from "@mui/material/Grid";

// Feedback
import Alert from "@mui/material/Alert";
import CircularProgress from "@mui/material/CircularProgress";
```

### Theming

MaterialUIComponent automatically inherits the theme from `Page`:

```python
import param
import panel as pn
from panel_material_ui import Page, MaterialUIComponent

class ThemedCard(MaterialUIComponent):
    title = param.String(default="Card Title")

    _esm_base = """
    import Card from "@mui/material/Card";
    import CardContent from "@mui/material/CardContent";
    import Typography from "@mui/material/Typography";
    import { useTheme } from "@mui/material/styles";

    export function render({ model }) {
        const [title] = model.useState("title");
        const theme = useTheme();

        return (
            <Card>
                <CardContent>
                    <Typography variant="h5" color="primary">
                        {title}
                    </Typography>
                </CardContent>
            </Card>
        );
    }
    """

# Theme applied automatically via Page
page = Page(main=[ThemedCard(title="Hello World")], title="My App", dark_theme=True)
page.servable()
```

### Using MUI Icons

Use **explicit icon imports** (not trailing slash) with `?external=react` to share the React instance with panel-material-ui:

```python
class IconComponent(MaterialUIComponent):
    _importmap = {
        "imports": {
            # Explicit import for each icon used - ?external=react shares React instance
            "@mui/icons-material/Favorite": "https://esm.sh/@mui/icons-material@5.16.7/Favorite?external=react",
            # Add more icons as needed:
            # "@mui/icons-material/Delete": "https://esm.sh/@mui/icons-material@5.16.7/Delete?external=react",
        }
    }

    _esm_base = """
    import IconButton from "@mui/material/IconButton";
    import FavoriteIcon from "@mui/icons-material/Favorite";

    export function render({ model }) {
        // Use inline style for icon dimensions - MUI CSS classes may not load properly
        return (
            <IconButton id="icon-btn" color="primary" style={{ padding: '8px' }}>
                <FavoriteIcon style={{ width: '24px', height: '24px', fill: 'currentColor' }} />
            </IconButton>
        );
    }
    """
```

> **Important:**
> - Do NOT use the trailing slash pattern (`@mui/icons-material/`) with query parameters - importmaps require values ending in `/` when keys end in `/`, which breaks `?external=react`. Use explicit imports for each icon instead.
> - Use inline `style` props for icon dimensions (`width`, `height`) because MUI CSS classes may not load properly with custom MaterialUIComponent.


## 8. Best Practices

### DOs

1. **Use external `.js`/`.jsx` files for development**
   ```python
   _esm = Path(__file__).parent / "component.js"
   ```
   Then run `panel serve app.py --dev` for hot reload.

2. **Use `_importmap` with `?external=` for shared dependencies**
   ```python
   _importmap = {
       "imports": {
           "my-lib": "https://esm.sh/my-lib?external=react,react-dom",
       }
   }
   ```

3. **Clean up resources in the `remove` lifecycle**
   ```javascript
   export function render({ model, el }) {
       const interval = setInterval(updateData, 1000);
       model.on('remove', () => clearInterval(interval));
   }
   ```

4. **Use `panel compile` for production bundling**
   ```bash
   panel compile my_component.py
   ```

5. **Define proper `param` types with metadata**
   ```python
   value = param.Integer(default=0, bounds=(0, 100), doc="Slider value")
   ```

6. **Use descriptive element IDs for testing**
   ```javascript
   button.id = "submit-button";
   input.id = "username-input";
   ```

7. **Handle initial state in render**
   ```javascript
   export function render({ model, el }) {
       el.textContent = model.value;  // Initialize
       model.on('value', () => {
           el.textContent = model.value;
       });
   }
   ```

### DON'Ts

1. **Don't mix API patterns between component types**
   ```javascript
   // WRONG: Using AnyWidget API in ReactComponent
   const value = model.get("value");  // Don't do this!

   // RIGHT: Use hooks in ReactComponent
   const [value] = model.useState("value");
   ```

2. **Don't forget `model.save_changes()` in AnyWidgetComponent**
   ```javascript
   // WRONG: Changes won't sync to Python
   model.set("value", newValue);

   // RIGHT: Always call save_changes after set
   model.set("value", newValue);
   model.save_changes();
   ```

3. **Don't import React manually in ReactComponent**
   ```javascript
   // WRONG: React is already globally available
   import React from 'react';

   // RIGHT: Use React directly (it's in scope)
   const [state, setState] = React.useState(0);
   ```

4. **Don't use deprecated `ReactiveHTML`**
   ```python
   # WRONG: Deprecated
   from panel.reactive import ReactiveHTML

   # RIGHT: Use ESM components
   from panel.custom import JSComponent
   ```

5. **Don't inline large ESM in production**
   ```python
   # WRONG: Large inline strings are slow
   _esm = """... 500 lines of code ..."""

   # RIGHT: External file + compile
   _esm = Path(__file__).parent / "component.js"
   # Then: panel compile component.py
   ```

6. **Don't forget to handle resize events for responsive components**
   ```javascript
   model.on('resize', ({ width, height }) => {
       chart.resize(width, height);
   });
   ```

7. **Don't use `_` prefix for parameters needed in JavaScript**
   ```python
   # WRONG: Private parameters don't sync
   _computed = param.String()  # Undefined in JS

   # RIGHT: Public parameters sync
   computed = param.String()   # Available as model.computed
   ```

8. **Prefer ESM imports over `__javascript__` - ESM imports are synchronous, `__javascript__` is not**
   ```python
   # WRONG: __javascript__ loads asynchronously - render() may run before library is ready
   __javascript__ = ["https://unpkg.com/@google/model-viewer@3.4.0/dist/model-viewer.min.js"]

   # RIGHT: ESM import guarantees library loads before render() executes
   _esm = """
   import "https://esm.sh/@google/model-viewer@3.4.0";

   export function render({ model, el }) {
       // model-viewer custom element is guaranteed to be registered
       const viewer = document.createElement('model-viewer');
       ...
   }
   """
   ```

   > **Why?** `__javascript__` loads scripts asynchronously. This causes race conditions where `render()` executes before the library finishes loading - especially problematic for web components that must register custom elements before you can create them.

## 9. Testing with Playwright

Custom components should be tested using Playwright for UI testing. Panel provides test utilities that make this straightforward.

### Setup

```bash
pip install panel pytest pytest-playwright pytest-xdist
playwright install chromium
```

### Test Utilities from Panel

Panel provides test utilities in `panel.tests.util` for serving components during Playwright tests:

- **`serve_component(page, app)`** - Serves a component and navigates the browser to it. Returns `(msgs, port)` tuple with console messages and server port.
- **`wait_until(fn, page, timeout=5000)`** - Polls a function until it returns `True` or times out. Essential for JS → Python sync tests.

### Complete Example Test File

This complete, working example demonstrates all key testing patterns:

```python
"""Tests for Panel custom components with Playwright."""

import pytest

pytest.importorskip("playwright")

import panel as pn
import param
from panel.custom import JSComponent
from panel.tests.util import serve_component, wait_until
from playwright.sync_api import expect

pytestmark = pytest.mark.ui

# Timeout constants
DEFAULT_TIMEOUT = 2_000  # Standard operations (clicks, text assertions)
LOAD_TIMEOUT = 5_000  # Initial page/component load
NETWORK_TIMEOUT = 5_000  # External resources (CDN libraries)


# =============================================================================
# Test Components
# =============================================================================


class CounterButton(JSComponent):
    """A simple counter button component for testing."""

    value = param.Integer(default=0, doc="Current count")

    _esm = """
    export function render({ model, el }) {
        const button = document.createElement('button');
        button.id = 'counter-btn';

        function update() {
            button.textContent = `Count: ${model.value}`;
        }

        button.onclick = () => {
            model.value += 1;
        };

        model.on('value', update);
        update();

        el.appendChild(button);
    }
    """


class DisplayComponent(JSComponent):
    """A simple display component for testing Python → JS sync."""

    text = param.String(default="", doc="Text to display")

    _esm = """
    export function render({ model, el }) {
        const display = document.createElement('div');
        display.id = 'display';

        function update() {
            display.textContent = model.text;
        }

        model.on('text', update);
        update();

        el.appendChild(display);
    }
    """


class TextInput(JSComponent):
    """A simple text input for testing JS → Python sync."""

    value = param.String(default="", doc="Input value")

    _esm = """
    export function render({ model, el }) {
        const input = document.createElement('input');
        input.id = 'text-input';
        input.type = 'text';
        input.value = model.value;

        input.oninput = (e) => {
            model.value = e.target.value;
        };

        model.on('value', () => {
            if (input.value !== model.value) {
                input.value = model.value;
            }
        });

        el.appendChild(input);
    }
    """


# =============================================================================
# Fixtures - CRITICAL: Always reset state to properly shuts down all threaded Panel
# servers, allowing pytest to exit cleanly after tests complete.
# =============================================================================

# ALWAYS INCLUDE THIS FIXTURE!
@pytest.fixture(autouse=True)
def server_cleanup():
    """Clean up Panel state after each test."""
    try:
        yield
    finally:
        pn.state.reset()


# =============================================================================
# Smoke Test - CRITICAL: ALWAYS Verify Panel/Bokeh infrastructure works before other tests!
# =============================================================================

# ALWAYS INCLUDE THIS TEST!
def test_no_console_errors(page):
    """Smoke test: Verify no JavaScript errors during component load."""
    component = CounterButton(value=0)
    msgs, _port = serve_component(page, component)

    # Check for Bokeh document idle message (confirms Panel loaded successfully)
    # Example: "[bokeh 3.8.2] document idle at 16 ms"
    info_messages = [m for m in msgs if m.type == "info"]
    assert any("document idle" in m.text.lower() for m in info_messages), \
        f"Expected Bokeh 'document idle' message not found. Got: {[m.text for m in info_messages]}"

    # Check for no errors (ignore favicon 404s)
    error_messages = [m for m in msgs if m.type == "error"]
    real_errors = [m for m in error_messages if "favicon" not in m.text.lower()]
    assert len(real_errors) == 0, f"JavaScript errors found: {[m.text for m in real_errors]}"


# =============================================================================
# Basic Test Patterns
# =============================================================================


def test_component_renders(page):
    """Test that component renders correctly."""
    counter = CounterButton(value=42)
    serve_component(page, counter)

    expect(page.locator("#counter-btn")).to_have_text("Count: 42", timeout=LOAD_TIMEOUT)


def test_component_interaction(page):
    """Test user interaction updates state."""
    counter = CounterButton(value=0)
    serve_component(page, counter)

    page.locator("#counter-btn").click()
    wait_until(lambda: counter.value == 1, page)
    expect(page.locator("#counter-btn")).to_have_text("Count: 1", timeout=DEFAULT_TIMEOUT)


# =============================================================================
# State Sync Tests
# =============================================================================


def test_python_to_js_sync(page):
    """Test Python → JS state synchronization."""
    display = DisplayComponent(text="Initial")
    serve_component(page, display)

    expect(page.locator("#display")).to_have_text("Initial", timeout=LOAD_TIMEOUT)

    # Update from Python
    display.text = "Updated"

    expect(page.locator("#display")).to_have_text("Updated", timeout=DEFAULT_TIMEOUT)


def test_js_to_python_sync(page):
    """Test JS → Python state synchronization."""
    text_input = TextInput(value="")
    serve_component(page, text_input)

    page.locator("#text-input").fill("Hello World")

    wait_until(lambda: text_input.value == "Hello World", page)
    assert text_input.value == "Hello World"


def test_bidirectional_sync(page):
    """Test bidirectional state synchronization."""
    counter = CounterButton(value=5)
    serve_component(page, counter)

    # Verify initial state
    expect(page.locator("#counter-btn")).to_have_text("Count: 5", timeout=LOAD_TIMEOUT)

    # JS → Python: Click button
    page.locator("#counter-btn").click()
    wait_until(lambda: counter.value == 6, page)

    # Python → JS: Update from Python
    counter.value = 100
    expect(page.locator("#counter-btn")).to_have_text("Count: 100", timeout=DEFAULT_TIMEOUT)

    # JS → Python: Click again
    page.locator("#counter-btn").click()
    wait_until(lambda: counter.value == 101, page)
```

### Key Testing Patterns

| Pattern | Use Case |
|---------|----------|
| `msgs, port = serve_component(page, component)` | Serve component, get console messages |
| `expect(locator).to_have_text("text", timeout=X)` | Assert element text |
| `wait_until(lambda: condition, page)` | Wait for Python state change (JS → Python) |
| `page.locator("#id").click()` / `.fill("text")` | Simulate user interaction |

### Testing Components with External Resources

Components loading external resources (CDN libraries, 3D models) need longer timeouts and explicit dimensions:

```python
def test_component_with_external_resources(page):
    viewer = ModelViewer(
        src="https://example.com/model.glb",
        # IMPORTANT: Set explicit dimensions - 100% width/height collapses to 0px
        style={"min-height": "400px", "min-width": "400px"},
    )
    serve_component(page, viewer)
    expect(page.locator("#model-viewer")).to_be_visible(timeout=NETWORK_TIMEOUT)
```

### Running Tests

```bash
# Run UI tests in parallel for faster feedback (recommended)
pytest path/to/test_file.py -n auto

# Run UI tests sequentially (exit on first failure)
pytest path/to/test_file.py -x
```

- Use `-n auto` (pytest-xdist) to run tests in parallel for faster feedback
- Run headless unless users ask for headed mode
- Use `-x` (exit on first failure) for sequential runs
- Use `--headed --slowmo 500` for debugging if the users asks for this

## 10. Complete Examples

### JSComponent Counter

```python
import param
from panel.custom import JSComponent

class CounterButton(JSComponent):
    value = param.Integer(default=0, doc="Current count")

    _esm = """
    export function render({ model, el }) {
        const button = document.createElement('button');
        button.id = 'counter-btn';

        function update() {
            button.textContent = `Count: ${model.value}`;
        }

        button.onclick = () => { model.value += 1; };
        model.on('value', update);
        update();

        el.appendChild(button);
    }
    """
```

### ReactComponent Counter

```python
import param
from panel.custom import ReactComponent

class CounterButton(ReactComponent):
    value = param.Integer(default=0, doc="Current count")

    _esm = """
    export function render({ model }) {
        const [value, setValue] = model.useState("value");

        return (
            <button id="counter-btn" onClick={() => setValue(value + 1)}>
                Count: {value}
            </button>
        );
    }
    """
```

### AnyWidgetComponent Counter

```python
import param
from panel.custom import AnyWidgetComponent

class CounterButton(AnyWidgetComponent):
    value = param.Integer(default=0, doc="Current count")

    _esm = """
    export default {
        render({ model, el }) {
            const button = document.createElement('button');
            button.id = 'counter-btn';

            function update() {
                button.textContent = `Count: ${model.get("value")}`;
            }

            button.onclick = () => {
                model.set("value", model.get("value") + 1);
                model.save_changes();
            };

            model.on("change:value", update);
            update();

            el.appendChild(button);
        }
    }
    """
```

### Test for All Versions

```python
import pytest
pytest.importorskip("playwright")

from playwright.sync_api import expect
from panel.tests.util import serve_component, wait_until

pytestmark = pytest.mark.ui

@pytest.mark.parametrize("CounterClass", [
    pytest.param("counter_js.CounterButton", id="js"),
    pytest.param("counter_react.CounterButton", id="react"),
    pytest.param("counter_anywidget.CounterButton", id="anywidget"),
])
def test_counter(page, CounterClass):
    import importlib
    module_name, class_name = CounterClass.rsplit(".", 1)
    module = importlib.import_module(module_name)
    Counter = getattr(module, class_name)

    counter = Counter(value=0)
    serve_component(page, counter)

    button = page.locator("#counter-btn")
    expect(button).to_have_text("Count: 0")

    button.click()
    wait_until(lambda: counter.value == 1, page)
    expect(button).to_have_text("Count: 1")
```


## 11. Troubleshooting

### Component Not Rendering

1. Check browser console for JavaScript errors
2. Verify `_esm` path is correct (use `Path(__file__).parent`)
3. Ensure export function is named `render` (or `default` for AnyWidget)
4. Check import map URLs are accessible

### State Not Syncing

1. **JSComponent:** Ensure `model.on('param', callback)` is registered
2. **ReactComponent:** Use `model.useState()` not `React.useState()` for synced state
3. **AnyWidgetComponent:** Call `model.save_changes()` after `model.set()`
### Import Errors

1. Verify CDN URLs in `_importmap` are correct
2. For React libraries, add `?external=react,react-dom`
3. Check for CORS issues with custom CDN URLs

### Styles Not Applied

1. Check `_stylesheets` paths are correct
2. For inline CSS, ensure it's a list of strings
3. CSS is scoped to shadow DOM - use `:host` for root styling


## 12. Common Patterns

### Debouncing User Input

```javascript
let timeout;
input.oninput = (e) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => {
        model.value = e.target.value;
    }, 300);
};
```

### Loading External Data

```javascript
export async function render({ model, el }) {
    el.textContent = "Loading...";

    const data = await fetch(model.data_url).then(r => r.json());

    el.textContent = "";
    renderChart(el, data);
}
```

### Responsive Component Sizing

Custom components should fill their parent container (`el`) and respond to size changes. Panel controls `el`'s dimensions via `sizing_mode` and related parameters.

**Key Concepts:**

1. **Panel sizes the container (`el`)** - Set `sizing_mode` in Python to control how `el` fills available space
2. **`model.width`/`model.height`** - Access the component's dimensions in JavaScript
3. **Use lifecycle hooks** - `after_render` for initial setup, `resize` for size changes

**Pattern 1: Fixed Dimensions**

For components with known size requirements:

```python
class Canvas(JSComponent):
    _esm = "canvas.js"

canvas = Canvas(width=400, height=400)  # Fixed size
```

```javascript
export function render({ model, el }) {
    const canvas = document.createElement('canvas');
    canvas.width = model.width;
    canvas.height = model.height;
    el.appendChild(canvas);
}
```

**Pattern 2: Responsive Width, Fixed Height**

Most common pattern - component stretches horizontally:

```python
class Chart(JSComponent):
    _esm = "chart.js"

chart = Chart(height=400, sizing_mode="stretch_width")
```

```javascript
export function render({ model, el }) {
    const container = document.createElement('div');
    container.style.width = '100%';
    container.style.height = '100%';
    el.appendChild(container);

    // Initialize with current dimensions
    const chart = createChart(container, el.clientWidth, model.height);

    // Handle resize
    model.on('resize', () => {
        chart.resize(el.clientWidth, model.height);
    });
}
```

**Pattern 3: Fully Responsive (Stretch Both)**

For components that fill all available space:

```python
class Map(JSComponent):
    _esm = "map.js"

map_component = Map(min_height=400, sizing_mode="stretch_both")
```

```javascript
export function render({ model, el }) {
    const container = document.createElement('div');
    container.style.width = '100%';
    container.style.height = '100%';
    el.appendChild(container);

    const map = createMap(container);

    // Use after_render when library needs DOM dimensions
    model.on('after_render', () => {
        map.invalidateSize();  // Recalculate size after layout
    });

    model.on('resize', () => {
        map.invalidateSize();
    });
}
```

**Pattern 4: Libraries with Built-in Responsive Support**

Some libraries handle resizing internally:

```javascript
// ChartJS with responsive options
const chart = new Chart(canvas, {
    ...model.object,
    options: {
        responsive: true,
        maintainAspectRatio: false,
    }
});
```

**Common `sizing_mode` Configurations:**

| Use Case | Python Configuration |
|----------|---------------------|
| Fixed size | `width=400, height=300` |
| Fill width, fixed height | `height=400, sizing_mode="stretch_width"` |
| Fill height, fixed width | `width=400, sizing_mode="stretch_height"` |
| Fill container | `sizing_mode="stretch_both"` (set `min_height` for safety) |
| Fill with constraints | `sizing_mode="stretch_both", min_width=200, max_width=800` |

> **Tip:** When using `sizing_mode="stretch_both"`, always set `min_height` to prevent the component from collapsing to zero height when the parent has no explicit height.

### Two-Way Binding with Validation

```python
class ValidatedInput(JSComponent):
    value = param.String(default="")
    error = param.String(default="")

    @param.depends('value', watch=True)
    def _validate(self):
        if len(self.value) < 3:
            self.error = "Must be at least 3 characters"
        else:
            self.error = ""
```

```javascript
export function render({ model, el }) {
    const input = document.createElement('input');
    const error = document.createElement('span');
    error.className = 'error';

    input.oninput = (e) => { model.value = e.target.value; };

    model.on('value', () => { input.value = model.value; });
    model.on('error', () => { error.textContent = model.error; });

    // Initialize
    input.value = model.value;
    error.textContent = model.error;

    el.append(input, error);
}
```


## 13. Learning More

### Finding Documentation

Use the `search` tool to find relevant documentation:

```python
search("JSComponent lifecycle hooks", project="panel")
search("ReactComponent useState", project="panel")
search("AnyWidget model API", project="panel")
```

### Official Documentation

- **Panel Custom Components**: <https://panel.holoviz.org/how_to/custom_components/index.html>
- **Panel Material UI Custom Components**: <https://panel-material-ui.holoviz.org/how_to/custom.html>
- **AnyWidget Specification**: <https://anywidget.dev/>

### External Resources

For integrating specific JavaScript libraries:

1. Search the web for "[library name] ESM import" to find CDN URLs
2. Check esm.sh for React-compatible bundles: `https://esm.sh/[package]`
3. Check jsDelivr for UMD bundles: `https://cdn.jsdelivr.net/npm/[package]`
