---
name: starhtml
description: Builds reactive web applications with StarHTML, a Python-first framework over Datastar. Use when writing StarHTML components, signals, event handlers, reactive attributes, conditional helpers, CSS classes, computed signals, HTTP actions, SSE endpoints, or plugins (persist, scroll, resize, drag, canvas, motion, markdown, katex, mermaid, split, nodegraph). For UI components, use StarUI (shadcn/ui for Python). After generating any StarHTML file, run `starhtml-check <file.py>` to validate.
---

# StarHTML — Core Skill

StarHTML = Python objects that compile to reactive Datastar HTML.

**After generating any component, validate with:** `starhtml-check <file.py>`

> If `starhtml-check` is not installed:
> ```bash
> curl -L https://raw.githubusercontent.com/renatocaliari/starhtml-skill/main/starhtml_check.py \
>   -o /usr/local/bin/starhtml-check && chmod +x /usr/local/bin/starhtml-check
> ```

> **UI Components:** For production-ready UI, use **[StarUI](https://ui.starhtml.com/)** — shadcn/ui for Python.
> See [`./reference/starui.md`](./reference/starui.md) for all 34+ components (Button, Card, Dialog, Table, etc.)

> **Sub-references** (load when needed, same directory as this file):
> `./reference/starui.md` · `./reference/icons.md` · `./reference/js.md` · `./reference/handlers.md` · `./reference/slots.md` · `./reference/demos.md`
>
> **Official demos** (canonical runnable examples, always from official framework repo):
> `https://raw.githubusercontent.com/banditburai/starHTML/main/web/demos/NN_name.py`

---

## The 6 Rules You Must Not Break

**R1 — No f-strings in reactive attributes (they become static)**

    # WRONG — evaluated once in Python, never updates in browser:
    data_text=f"Count: {counter}"

    # RIGHT — reactive, updates when signal changes:
    data_text="Count: " + counter           # for 1-2 signals
    data_text=f("Count: {c}", c=counter)    # for 3+ signals
    # f() requires: from starhtml.datastar import f

**R2 — data_show always needs flash prevention**

    # WRONG — element flashes visible before JS loads:
    Div("modal content", data_show=is_open)

    # RIGHT — hidden by default, shown reactively:
    Div("modal content", style="display: none", data_show=is_open)
    # Alternatives:
    Div("modal content", cls="hidden", data_class_hidden=~is_open)
    Div("modal content", style="opacity:0;transition:opacity .3s",
        data_style_opacity=is_open.if_("1", "0"))

**R3 — Positional arguments BEFORE keyword arguments**

    # WRONG — SyntaxError at runtime:
    Div(cls="container", "Hello World")

    # RIGHT:
    Div("Hello World", cls="container")

    # Rule: content/signals first, then attributes/handlers

**R4 — Signal names must be snake_case**

    # WRONG — will error at runtime:
    (myCounter := Signal("myCounter", 0))

    # RIGHT:
    (my_counter := Signal("my_counter", 0))

**R5 — Walrus operator := must be wrapped in outer parentheses**

    # WRONG — won't register as positional argument:
    name := Signal("name", "")

    # RIGHT — works as positional argument in HTML elements:
    (name := Signal("name", ""))

**R6 — Signals are reactive state references, NOT data containers**

    # ❌ WRONG — Signals are NOT for storing/accessing data:
    todos = Signal("todos", [])
    todos.value.append(item)  # .value does NOT exist!
    print(len(todos))         # Signals don't support len()!

    # ✅ RIGHT — Use plain Python variables for data:
    todos_data = []           # Python variable for the actual data
    (todos_count := Signal("todos_count", 0))  # Signal for reactive UI state

    # Add item to data:
    todos_data.append({"id": 1, "text": "Buy milk"})

    # Update Signal (syncs to frontend, can be received in backend):
    yield signals(todos_count=len(todos_data))

---

## Understanding Signals vs Data

**Signals** are reactive state references that sync between frontend (`$signalName` in JS) and backend (Python `Signal` objects). They are **NOT** Python containers for data.

**Data** lives in **regular Python variables** (lists, dicts, strings, etc.).

### Pattern: Python Data + Reactive Signals

```python
# State management with pure Python
todos_data = []      # The actual data (Python list)
next_id = 1          # Counter (Python int)

# Signals for reactive state (frontend + backend)
(todos_count := Signal("todos_count", 0))
(is_loading := Signal("is_loading", False))

@rt("/todos/add", methods=["POST"])
@sse
def add_todo(todo_text: str):
    global next_id

    # 1. Update Python data (always use variables for data)
    todos_data.append({"id": next_id, "text": todo_text})
    next_id += 1

    # 2. Send updated UI to client
    yield elements(render_todo_item(todos_data[-1]), "#todo-list", "append")

    # 3. Update Signals (syncs to frontend AND can be received in backend)
    yield signals(todos_count=len(todos_data), is_loading=False)
```

### Signals Can Flow Both Ways

```python
# Frontend → Backend: Signal as parameter
@rt("/api/search")
@sse
def search(req, query: Signal):  # Receives Signal from frontend
    results = db.search(query)   # Can read Signal in backend
    yield signals(results_count=len(results))
```

### Frontend-Only Signals (optional `_` prefix)

```python
# Signal with _ prefix = frontend-only by convention
# (no backend parameter, not received in SSE handlers)
(_animation_state := Signal("_animation_state", "idle"))

# With _ref_only=True, Signal is excluded from data-signals HTML attribute
(_cache := Signal("_cache", {}, _ref_only=True))
```

### ⚠️ Common Signal Mistakes

**Mistake 1: f-string with Signal — displays `$signal_name` literal**

```python
(thought_count := Signal("thought_count", 5))

# ❌ WRONG — f-string converts Signal to literal string "$thought_count"
Div(f"{thought_count} thoughts captured")  # Shows: "$thought_count thoughts captured"

# ✅ RIGHT — Signal as argument (concatenates value)
Div(thought_count, " thoughts captured")  # Shows: "5 thoughts captured"

# ✅ RIGHT — Reactive attribute (updates dynamically)
Span(data_text=thought_count)
```

**Mistake 2: Signal in Python conditional — always truthy**

```python
(is_saving := Signal("is_saving", False))

# ❌ WRONG — Signal object is always truthy in Python
Button("Save" if not is_saving else "Saving...")  # Always shows "Saving..."

# ✅ RIGHT — Use reactive attribute
Button(
    "Save this thought",
    data_text=is_saving.if_("Saving...", "Save this thought")
)
```

**Key points:**
- Never try to read `signal.value` or use `len(signal)` — Signals are not containers
- Store data in Python variables; use Signals for reactive state that syncs UI
- Signals without `_` prefix automatically sync to backend via parameters
- In SSE: always `yield signals(...)` at the end to reset state
- **NEVER use f-strings with Signals — use arguments or `data_text`**
- **NEVER use Signals in Python conditionals — use reactive attributes

---

## Quick Reference

    from starhtml import *

    # Define reactive state — walrus := always in outer ()
    (counter  := Signal("counter", 0))
    (name     := Signal("name", ""))
    (visible  := Signal("visible", True))

    # Reactive attributes
    data_show=visible              # show/hide element
    data_text=name                 # display signal value as text
    data_bind=name                 # two-way binding (inputs)
    data_class_active=visible      # toggle class "active"

    # Events
    data_on_click=counter.add(1)
    data_on_input=(search_fn, {"debounce": 300})    # wait 300ms after typing
    data_on_scroll=(update_fn, {"throttle": 16})    # max 60fps
    data_on_submit=(post("/api/save"), {"prevent": True})

    # Signal operations
    counter.add(1)                 # increment: $counter + 1
    counter.set(0)                 # assign: $counter = 0
    visible.toggle()               # flip boolean: !$visible
    name.upper()                   # string method: $name.toUpperCase()
    count.default(0)               # nullish fallback: $count ?? 0
    count.default(0).clamp(0, 99)  # chain with other methods
    theme.one_of("light","dark")   # constrain to valid values
    sig.then(action)               # conditional execute if truthy

    # Value guards (chainable)
    status.one_of("draft", "published")     # validate enum
    theme.one_of("light", "dark", default="light")

    # Logical operators
    name & email                   # → $name && $email
    ~is_visible                    # → !$is_visible
    all(a, b, c)                   # → !!$a && !!$b && !!$c  (preferred for 3+)
    any(a, b)                      # → $a || $b
    age >= 18                      # → $age >= 18

📄 Runnable example: `01_basic_signals.py` (fetch from demos URL above)

---

## Conditional Helpers

| Helper | Behavior | Use for |
|--------|----------|---------|
| `sig.if_("a", "b")` | exclusive — one result | simple true/false choice |
| `match(sig, a="x", default="z")` | exclusive — maps value to output | value-based mapping |
| `switch([(cond, "msg"), ...], default="")` | exclusive — first match wins | validation chains |
| `collect([(cond, "cls"), ...])` | **inclusive** — ALL true combined | CSS class building |

    # EXCLUSIVE — only one result ever returned
    data_text=status.if_("Active", "Inactive")

    data_attr_class=match(theme,
        light="bg-white text-black",
        dark="bg-gray-900 text-white",
        default="bg-white")

    msg = switch([
        (~name, "Name is required"),
        (name.length < 2, "Name too short"),
        (~email.contains("@"), "Invalid email"),
    ], default="")

    # INCLUSIVE — combines ALL true conditions (correct for CSS classes)
    data_attr_class=collect([
        (True, "btn"),
        (is_primary, "btn-primary"),
        (is_large, "btn-lg"),
        (is_disabled, "opacity-50 cursor-not-allowed"),
    ])

    # WRONG: using collect() for exclusive logic (use switch or if_ instead)
    # WRONG: using switch() to combine CSS classes (use collect instead)

📄 See: `06_control_attributes.py`, `25_advanced_toggle_patterns.py`, `28_datastar_helpers_showcase.py`

---

## Forms and Binding

    Form(
        (name  := Signal("name", "")),
        (email := Signal("email", "")),
        (valid := Signal("valid", all(name, email.contains("@")))),

        Input(type="text",  data_bind=name,  placeholder="Name"),
        Span(
            data_text=switch([(~name, "Required"), (name.length < 2, "Too short")],
                             default=""),
            data_show=~name, style="display:none"
        ),

        Input(type="email", data_bind=email, placeholder="Email"),

        Button("Submit",
               data_attr_disabled=~valid,
               type="submit"),

        data_on_submit=(is_valid.then(post("/api/submit", name=name, email=email)),
                        {"prevent": True})
    )

📄 See: `03_forms_binding.py`

---

## HTTP Actions and SSE

    # HTTP actions — pass signals as params, never f-strings
    data_on_click=get("/api/data")
    data_on_click=post("/api/submit", name=name_sig, email=email_sig)
    data_on_click=is_valid.then(post("/api/submit"))         # conditional
    data_on_click=delete("/api/item")

    # Conditional execution with .then()
    data_on_click=is_confirmed.then(delete("/api/item"))     # only if confirmed
    data_effect=is_form_complete.then(auto_save)             # side effect

    # WRONG — f-string URL is Python-static, signal value not reactive:
    data_on_click=get(f"/api/{item_id}")
    # RIGHT — pass signal as parameter:
    data_on_click=get("/api/item", id=item_id_sig)

### ⚠️ POST Endpoint Data Parsing (Critical!)

**Datastar sends JSON by default, NOT form data.**

```python
# ❌ WRONG — Datastar sends JSON, req.form() returns empty!
@rt("/todos", methods=["POST"])
def create(req):
    form = req.form()  # Returns empty dict!
    text = form.get("text", "")  # Always empty
    mood = form.get("mood", "")

# ✅ RIGHT — Parse JSON first (Datastar default)
@rt("/todos", methods=["POST"])
def create(req):
    import json
    data = json.loads(req.body())
    text = data.get("text", "")
    mood = data.get("mood", "")

# ✅ RIGHT — Support both JSON and form data (defensive)
@rt("/todos", methods=["POST"])
def create(req):
    import json
    try:
        data = json.loads(req.body())
        text = data.get("text", "")
        mood = data.get("mood", "")
    except (json.JSONDecodeError, ValueError):
        # Fallback for traditional form submissions
        form = req.form()
        text = form.get("text", "")
        mood = form.get("mood", "")
```

**Why this happens:**
- Datastar uses `fetch()` with `Content-Type: application/json`
- Traditional HTML forms use `Content-Type: application/x-www-form-urlencoded`
- StarHTML/StarUI components send JSON by default

**Best Practice:** Always parse JSON first, optionally fallback to form data for compatibility.

    # SSE endpoint — always yield signals() at end to reset client state
    @rt("/send", methods=["POST"])
    @sse
    def send():
        yield signals(is_sending=True)
        yield elements(Div("msg", cls="msg"), "#chat", "append")  # append mode
        yield elements(Div("x", id="chat"), "#chat")              # replace/morph mode
        yield signals(is_sending=False, message="")               # REQUIRED: reset state

    # Hypermedia morph rule: returned element id MUST match the target selector
    @rt("/partial")
    def partial():
        return Div("new content", id="target")   # id="target" matches get("/partial") target

    # SSE Best Practices:
    # 1. Always yield signals() at end to reset client state
    # 2. For replace-mode: preserve id attribute for future targeting
    # 3. Use append/prepend for lists, replace for single elements

📄 See: `02_sse_elements.py`, `04_live_updates.py`, `05_background_tasks.py`, `08_routing_patterns.py`

---

## Styling

### SSR vs Reactive Attributes

| Use Case | SSR Needed? | Pattern |
|----------|-------------|---------|
| Toggle single class | No | `data_class_active=signal` |
| Tailwind special chars | No | `data_attr_class=signal.if_("hover:bg-blue-500", "")` |
| **Show/hide elements** | **Yes** | `style="display: none"` + `data_show=signal` |
| Base + toggle classes | Yes | `cls="base"` + `data_class_*` |
| Base + dynamic classes | Yes | `cls="base"` + `data_attr_cls=reactive` |

### CSS Classes

    # Simple class names (no special characters) → data_class_*
    data_class_active=is_active          # adds/removes class "active"
    data_class_hidden=~is_visible        # adds/removes class "hidden"

    # Special characters (:  /  [  ]) in class names → data_attr_class
    # WRONG — colon in keyword name is a Python parse error:
    data_class_hover:bg-blue=sig
    # RIGHT:
    data_attr_class=is_active.if_("hover:bg-blue-500 focus:ring-2", "")
    data_attr_class=is_loading.if_("bg-blue-500/50", "bg-blue-500")
    data_attr_class=is_custom.if_("bg-[#1da1f2]", "bg-gray-500")

    # data_attr_cls vs data_attr_class — DIFFERENT behaviors:
    # data_attr_cls   = ADDITIVE — merges with base cls= classes
    # data_attr_class = REPLACES — sets the full class attribute

    Button("OK",
           cls="btn",                                        # base classes
           data_attr_cls=is_valid.if_("btn-success", "btn-error"))  # additive

    Button("OK",
           data_attr_class=collect([(True, "btn"),
                                    (is_primary, "btn-primary")]))  # replaces

    # Dictionary syntax for conditional classes
    data_class={"active selected": role == "admin", "disabled": role == "guest"}

### CSS Properties

    # Static CSS (SSR)
    style="background-color: red; font-size: 16px"

    # Reactive CSS properties
    data_style_width=progress + "px"
    data_style_opacity=is_visible.if_("1", "0")

    # CSS template with multiple signals
    from starhtml.datastar import f
    data_attr_style=f("color: {c}; opacity: {o}", c=theme_color, o=opacity)

---

## Computed Signals and Effects

    # Computed Signal — pass expression (not literal) as initial value
    # auto-updates whenever dependencies change
    (first := Signal("first", ""))
    (last  := Signal("last", ""))
    (full_name := Signal("full_name", first + " " + last))       # string computed
    (is_valid  := Signal("is_valid", all(name, email)))          # boolean computed
    (total     := Signal("total", price * quantity))             # math computed

    # data_effect — side effects when signals change (assignments, not return values)
    data_effect=total.set(price * quantity)
    data_effect=[
        total.set(price * quantity),
        tax.set(total * 0.1),
        final.set(total + tax),
    ]

    # Performance: exclude internal-only signals from HTML output
    (cache := Signal("cache", {}, _ref_only=True))

📄 See: `27_nested_property_chaining.py`

---

## Plugins

Each plugin requires import from `starhtml.plugins` and registration with the app.
Fetch the demo file for the exact integration pattern — demo files are complete, runnable examples.

Base URL for all demos: `https://raw.githubusercontent.com/banditburai/starHTML/main/web/demos/`

```python
from starhtml.plugins import persist, scroll, resize, drag, canvas, position, motion, markdown, split

app, rt = star_app()
app.register(persist)   # register each plugin you need
app.register(motion)
```

| Plugin | Demo file(s) | What it does |
|--------|-------------|--------------|
| persist | `09_persist_plugin.py` | Sync signals to localStorage/sessionStorage |
| scroll | `10_scroll_plugin.py` | Track scroll position, page progress |
| resize | `11_resize_plugin.py` | Window/element resize events |
| drag | `12_drag_plugin.py`, `16_freeform_drag.py` | Drag and drop, sortable lists |
| canvas | `17_canvas_plugin.py`, `18_canvas_fullpage.py`, `29_drawing_canvas.py` | Canvas drawing |
| position | `20_position_plugin.py` | Element positioning |
| motion | `23_motion_plugin.py`, `24_motion_svg_plugin.py` | CSS/SVG animations (enter, exit, hover, in_view) |
| markdown | `13_markdown_plugin.py` | Render markdown content via `data_markdown` |
| katex | `14_katex_plugin.py` | Math / LaTeX rendering |
| mermaid | `15_mermaid_plugin.py` | Diagram rendering |
| split | `21_split_responsive.py`, `22_split_universal.py` | Resizable split panes |
| nodegraph | `19_nodegraph_demo.py` | Node graph UI |

Also fetch: `07_todo_list.py` (complete real-world app), `30_debugger_demo.py` (debugger tool)

For full demo index with descriptions: see `./reference/demos.md`
For Icon() component: see `./reference/icons.md`
For js(), f(), regex(): see `./reference/js.md`
For plugins API (persist, scroll, resize, drag, canvas, position, motion): see `./reference/handlers.md`
For slot system: see `./reference/slots.md`

---

## Common Errors (and How to Fix Them)

| Error | Cause | Solution |
|-------|-------|----------|
| `Signal has no len()` or `AttributeError: 'Signal' object has no attribute 'value'` | Treating Signal as data container (Signals are reactive state, not data) | Use Python variables for data: `todos_data = []` instead of `Signal("todos", [])` |
| `signals() takes 0 to 1 positional arguments` | Passing positional args to `signals()` | Use kwargs: `yield signals(count=1, status="done")` not `signals(count, status)` |
| `Method not found on $signal` (JS console) | Using plugin attributes without registering | Import and register: `app.register(persist)` |
| `NameError: name 'xyz' is not defined` | Using Signal without walrus `:=` parentheses | Wrap in parens: `(xyz := Signal("xyz", 0))` |
| `SyntaxError: positional argument follows keyword argument` | Wrong argument order | Content first, attributes after: `Div("text", cls="class")` |
| **Displays `$signal_name` literal** | f-string with Signal — converts to string | Use arguments: `Div(count, " items")` or `data_text=count` |
| **Button always shows wrong text** | Signal in Python conditional — always truthy | Use reactive: `data_text=is_saving.if_("Saving...", "Save")` |
| Element flashes before hiding on load | Missing flash prevention | Add `style="display:none"` with `data_show` |
| Form submits and reloads page | Missing `{"prevent": True}` | Add: `data_on_submit=(post("/api"), {"prevent": True})` |
| **POST returns 400 Bad Request** | Datastar sends JSON, not form data | Parse JSON: `data = json.loads(req.body())` |
| SSE endpoint leaves UI in loading state | Missing `yield signals()` reset | Always end with: `yield signals(loading=False)` |
| Signal value not updating in backend handler | Trying to read `signal.value` | Receive Signal as parameter: `def handler(req, my_sig: Signal)` |
| **Direct Datastar import** | Importing `@getdatastar/datastar` manually | **Remove it** — StarHTML manages Datastar automatically |

---

## Checker Tool

The checker is a standalone CLI (zero dependencies, stdlib only) that validates StarHTML components.

### Install (one-time)

**Check if installed:**
```bash
starhtml-check --help || echo "Not installed"
```

**Install if missing:**
```bash
# macOS / Linux - global install (recommended)
curl -L https://raw.githubusercontent.com/renatocaliari/starhtml-skill/main/starhtml_check.py \
  -o /usr/local/bin/starhtml-check && chmod +x /usr/local/bin/starhtml-check

# Or user-local (no sudo required)
curl -L https://raw.githubusercontent.com/renatocaliari/starhtml-skill/main/starhtml_check.py \
  -o ~/.local/bin/starhtml-check && chmod +x ~/.local/bin/starhtml-check
```

**Verify installation:**
```bash
starhtml-check --version  # Should show help
```

### Updating

Once installed, update to the latest version anytime:

```bash
starhtml-check --update
```

This fetches the latest version from GitHub, creates a backup (`.bak`), and updates automatically.

### Usage

```bash
# After generating StarHTML code, always run:
starhtml-check component.py           # full analysis
starhtml-check --summary f.py         # compact output (fewer tokens)
starhtml-check --update               # check for updates and update
```

**Development Loop:** write → check → fix ERRORs → re-run → ✓ no issues

### Output Levels

- **ERRORS** — must fix, will break runtime or reactivity
- **WARNINGS** — should fix, may cause subtle bugs or UX issues
- **SUMMARY** — signal inventory + total counts
