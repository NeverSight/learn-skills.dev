---
name: fiftyone-develop-plugin
description: Develops custom FiftyOne plugins (operators and panels) from scratch. Use when creating plugins, extending FiftyOne with custom operators, building interactive panels, or integrating external APIs.
---

# Develop FiftyOne Plugins

## Key Directives

**ALWAYS follow these rules:**

### 1. Understand before coding
Ask clarifying questions. Never assume what the plugin should do.

### 2. Plan before implementing
Present file structure and design. Get user approval before generating code.

### 3. Search existing plugins for patterns
```bash
# Clone official plugins for reference
git clone https://github.com/voxel51/fiftyone-plugins.git /tmp/fiftyone-plugins 2>/dev/null || true

# Search for similar patterns
grep -r "keyword" /tmp/fiftyone-plugins/plugins/ --include="*.py" -l
```

```python
list_plugins(enabled=True)
list_operators(builtin_only=False)
get_operator_schema(operator_uri="@voxel51/brain/compute_similarity")
```

### 4. Test locally before done

```bash
# Get plugins directory
PLUGINS_DIR=$(python -c "import fiftyone as fo; print(fo.config.plugins_dir)")

# Develop plugin in plugins directory
cd $PLUGINS_DIR/my-plugin
```

Write tests:
- **Python**: `pytest` for operators/panels
- **JavaScript**: `vitest` for React components

Verify in FiftyOne App before done.

### 5. Iterate on feedback

Run server separately to see logs:
```bash
# Terminal 1: Python logs
python -m fiftyone.server.main

# Terminal 2: Browser at localhost:5151 (JS logs in DevTools console)
```

```bash
fiftyone app debug          # logs printed to shell; use with a dataset:
fiftyone app debug <dataset-name>
```

For automated iteration, use Playwright e2e tests:
```bash
npx playwright test
```

Refine until the plugin works as expected.

## Critical Patterns

### Operator Execution
```python
# Chain operators (non-delegated operators only, in execute() only, fire-and-forget)
ctx.trigger("@plugin/other_operator", params={...})

# UI operations
ctx.ops.notify("Done!")
ctx.ops.set_progress(0.5)
```

### View Selection
```python
# Use ctx.target_view() to respect user's current selection and filters
view = ctx.target_view()

# ctx.dataset - Full dataset (use when explicitly exporting all)
# ctx.view - Filtered view (use for read-only operations)
# ctx.target_view() - Filtered + selected samples (use for exports/processing)
```

### Store Keys (Avoid Collisions)
```python
# Use namespaced keys to avoid cross-dataset conflicts
def _get_store_key(self, ctx):
    plugin_name = self.config.name.split("/")[-1]
    return f"{plugin_name}_store_{ctx.dataset._doc.id}_{self.version}"

store = ctx.store(self._get_store_key(ctx))
```

### Panel State vs Execution Store
```python
# ctx.panel.state - Transient (resets when panel reloads)
# ctx.store() - Persistent (survives across sessions)

def on_load(self, ctx):
    ctx.panel.state.selected_tab = "overview"  # Transient
    store = ctx.store(self._get_store_key(ctx))
    ctx.panel.state.config = store.get("user_config") or {}  # Persistent
```

### Delegated Execution
Use for operations that: process >100 samples or take >1 second.

```python
@property
def config(self):
    return foo.OperatorConfig(
        name="heavy_operator",
        allow_delegated_execution=True,
        default_choice_to_delegated=True,
    )
```

### Progress Reporting
```python
@property
def config(self):
    return foo.OperatorConfig(
        name="progress_operator",
        execute_as_generator=True,
    )

def execute(self, ctx):
    total = len(ctx.target_view())
    for i, sample in enumerate(ctx.target_view()):
        # Process sample...
        yield ctx.trigger("set_progress", {"progress": (i+1)/total})
    yield {"status": "complete"}
```

### Custom Runs (Auditability)
Use Custom Runs for operations needing reproducibility and history tracking:

```python
# Create run key (must be valid Python identifier - use underscores, not slashes)
run_key = f"my_plugin_{self.config.name}_v1_{timestamp}"

# Initialize and register
run_config = ctx.dataset.init_run(operator=self.config.name, params=ctx.params)
ctx.dataset.register_run(run_key, run_config)
```

See [PYTHON-OPERATOR.md](PYTHON-OPERATOR.md#custom-runs-auditable-operations) for full Custom Runs pattern.
See [EXECUTION-STORE.md](EXECUTION-STORE.md) for advanced caching patterns.
See [HYBRID-PLUGINS.md](HYBRID-PLUGINS.md) for Python + JavaScript communication.

## Workflow

### Phase 1: Requirements

Understand what the user needs to accomplish:

1. "What problem are you trying to solve?"
2. "What should the user be able to do?" (user's perspective)
3. "What information does the user provide?"
4. "What result does the user expect to see?"
5. "Any external data sources or services involved?"
6. "How will this fit into the user's workflow?"

### Phase 2: Design

1. Search existing plugins for similar patterns
2. For panels, default to **hybrid** (Python + JavaScript). See [HYBRID-PLUGINS.md](HYBRID-PLUGINS.md).
3. Create plan with:
   - Plugin name (`@org/plugin-name`)
   - File structure
   - Operator/panel specs
   - Input/output definitions
3. **Get user approval before coding**

See [PLUGIN-STRUCTURE.md](PLUGIN-STRUCTURE.md) for file formats.

### Phase 3: Generate Code

Create these files:

| File | Required | Purpose |
|------|----------|---------|
| `fiftyone.yml` | Yes | Plugin manifest |
| `__init__.py` | Yes | Python operators/panels |
| `requirements.txt` | If deps | Python dependencies |
| `package.json` | JS only | Node.js metadata |
| `src/index.tsx` | JS only | React components |

Reference docs:
- [PYTHON-OPERATOR.md](PYTHON-OPERATOR.md) - Python operators
- [PYTHON-PANEL.md](PYTHON-PANEL.md) - Python panels
- [JAVASCRIPT-PANEL.md](JAVASCRIPT-PANEL.md) - React/TypeScript panels
- [HYBRID-PLUGINS.md](HYBRID-PLUGINS.md) - Python + JavaScript communication
- [EXECUTION-STORE.md](EXECUTION-STORE.md) - Persistent storage and caching

**For JavaScript panels with rich UI**: Invoke the `fiftyone-voodo-design` skill for VOODO components (buttons, inputs, toasts, design tokens). VOODO is FiftyOne's official React component library.

### Phase 4: Validate & Test

#### 4.1 Validate Detection
```python
list_plugins(enabled=True)  # Should show your plugin
list_operators()  # Should show your operators
```

**If not found:** Check fiftyone.yml syntax, Python syntax errors, restart App.

#### 4.2 Validate Schema
```python
get_operator_schema(operator_uri="@myorg/my-operator")
```

Verify inputs/outputs match your expectations.

#### 4.3 Test Execution
```python
set_context(dataset_name="test-dataset")
launch_app()
execute_operator(operator_uri="@myorg/my-operator", params={...})
```

**Common failures:**
- "Operator not found" → Check fiftyone.yml operators list
- "Missing parameter" → Check resolve_input() required fields
- "Execution error" → Check execute() implementation

### Phase 5: Iterate

1. Get user feedback
2. Fix issues (sync source and plugins directory if separate)
3. Restart App if needed
4. Repeat until working

## Quick Reference

### Plugin Types

| Type | Language | Use Case |
|------|----------|----------|
| Operator | Python | Data processing, computations |
| Panel | Hybrid (default) | Python backend + React frontend (recommended) |
| Panel | Python-only | Simple UI without rich interactivity |

### Operator Config Options

| Option | Default | Effect |
|--------|---------|--------|
| `dynamic` | False | Recalculate inputs on change |
| `execute_as_generator` | False | Stream progress with yield |
| `allow_immediate_execution` | True | Execute in foreground |
| `allow_delegated_execution` | False | Background execution |
| `default_choice_to_delegated` | False | Default to background |
| `unlisted` | False | Hide from operator browser |
| `on_startup` | False | Execute when app starts |
| `on_dataset_open` | False | Execute when dataset opens |

### Panel Config Options

| Option | Default | Effect |
|--------|---------|--------|
| `allow_multiple` | False | Allow multiple panel instances |
| `surfaces` | "grid" | Where panel can display ("grid", "modal", "grid modal") |
| `category` | None | Panel category in browser |
| `priority` | None | Sort order in UI |

### Input Types

| Type | Method |
|------|--------|
| Text | `inputs.str()` |
| Number | `inputs.int()` / `inputs.float()` |
| Boolean | `inputs.bool()` |
| Dropdown | `inputs.enum()` |
| File | `inputs.file()` |
| View | `inputs.view_target()` |

## Minimal Example

**fiftyone.yml:**
```yaml
name: "@myorg/hello-world"
type: plugin
operators:
  - hello_world
```

**__init__.py:**
```python
import fiftyone.operators as foo
import fiftyone.operators.types as types

class HelloWorld(foo.Operator):
    @property
    def config(self):
        return foo.OperatorConfig(
            name="hello_world",
            label="Hello World"
        )

    def resolve_input(self, ctx):
        inputs = types.Object()
        inputs.str("message", label="Message", default="Hello!")
        return types.Property(inputs)

    def execute(self, ctx):
        print(ctx.params["message"])
        return {"status": "done"}

def register(p):
    p.register(HelloWorld)
```

## Debugging

### Where Logs Go

| Log Type | Location |
|----------|----------|
| Python backend | Terminal running the server |
| JavaScript frontend | Browser console (F12 → Console) |
| Network requests | Browser DevTools (F12 → Network) |
| Operator errors | Operator browser in FiftyOne App |

### Running in Debug Mode (Recommended for Development)

```bash
fiftyone app debug                    # server logs printed to shell
fiftyone app debug <dataset-name>     # with a dataset pre-loaded
```

### Python Debugging

```python
def execute(self, ctx):
    # Use print() for quick debugging (shows in server terminal)
    print(f"Params received: {ctx.params}")
    print(f"Dataset: {ctx.dataset.name}, View size: {len(ctx.view)}")

    # For structured logging
    import logging
    logging.info(f"Processing {len(ctx.target_view())} samples")

    # ... rest of execution
```

### JavaScript/TypeScript Debugging

```typescript
// Use console.log in React components
console.log("Component state:", state);
console.log("Panel data:", panelData);

// Check browser DevTools:
// - Console: JS errors, syntax errors, plugin load failures
// - Network: API calls, variable values before/after execution
```

### Common Debug Locations

- **Operator not executing**: Check Network tab for request/response
- **Plugin not loading**: Check Console for syntax errors
- **Variables not updating**: Check Network tab for payload data
- **Silent failures**: Check Operator browser for error messages

## Troubleshooting

**Plugin not appearing:**
- Check `fiftyone.yml` exists in plugin root
- Verify location: `~/.fiftyone/plugins/`
- Check for Python syntax errors
- Restart FiftyOne App

**Operator not found:**
- Verify operator listed in `fiftyone.yml`
- Check `register()` function
- Run `list_operators()` to debug

**Secrets not available:**
- Add to `fiftyone.yml` under `secrets:`
- Set environment variables before starting FiftyOne

## Advanced

### Programmatic Operator Execution
```python
# For executing operators outside of FiftyOne App context
import fiftyone.operators as foo
result = foo.execute_operator(operator_uri, ctx, **params)
```

## Resources

- [Plugin Development Guide](https://docs.voxel51.com/plugins/developing_plugins.html)
- [Developing Panels](https://docs.voxel51.com/plugins/developing_plugins.html#developing-panels)
- [Developing JS Plugins](https://docs.voxel51.com/plugins/developing_plugins.html#developing-js-plugins)
- [Panel Examples (reference implementations)](https://github.com/voxel51/fiftyone-plugins/blob/main/plugins/panel-examples/__init__.py)
- [FiftyOne Plugins Repo](https://github.com/voxel51/fiftyone-plugins)
- [Operator Types API](https://docs.voxel51.com/api/fiftyone.operators.types.html)
