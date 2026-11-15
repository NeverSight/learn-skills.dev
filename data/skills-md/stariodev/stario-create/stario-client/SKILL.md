---
name: stario-client
description: Client behaviour in a Stario app - where JavaScript goes and how Python calls it. Use before you write any JavaScript, a <script>, addEventListener, or a data.on expression longer than two statements, and when a page needs drag, swipe, a picker or ruler, keyboard or viewport handling, clipboard, dictation, a file preview, or a theme toggle.
---

# Client behaviour

Every `data.*` and `at.*` signature is in skill `stario-api`.

The server renders the state. JavaScript is for what HTML and Datastar cannot express. It lives in `static/js/<name>.js` and Python calls it from Datastar attributes. It never lives in a Python string.

## Pick the first layer that does the job

1. **The server.** A search, a filter, or a list is a `GET` that patches its part, not JavaScript over a JSON copy of the data.
2. **HTML and CSS.** `<dialog>`, `<details>`, `popover`, `:has()`, scroll-snap.
3. **A Datastar attribute** with a short expression: one or two statements over signals, `el`, `evt`, and `app.*` calls. `data.bind` on `<input type="file">` already gives `[{name, contents, mime}]`; `@post` already follows `navigate`.
4. **A function in `static/js/<name>.js`**, called from an attribute. Math, measuring, pointer physics, the browser APIs (`visualViewport`, `SpeechRecognition`, clipboard).

## A file

Each file is a classic script (not a module). It defines one namespace, named after the file, and nothing else at the top level. Top-level `const`, `let`, and `function` are shared by every classic script on the page.

A namespace is a plain object literal. Methods call each other with `this`; state is a property.

```js
// static/js/share.js
window.app ??= {};
app.share = {
  copy(url, done) {
    navigator.clipboard.writeText(url).then(() => {
      done(true);
      setTimeout(() => done(false), 1600);
    });
  },
};
```

```python
h.Button(
    {"type": "button", "data-url": share_url},
    data.on("click", "app.share.copy(el.dataset.url, v => $_copied = v)"),
    h.Span(data.text("$_copied ? 'Copied' : 'Copy'")),
)
```

A factory exists only when each element needs its own state (a ruler, a wheel, a drag). It listens on its own `el`, so its listeners die with the element:

```js
// static/js/ruler.js
window.app ??= {};
app.ruler = (el, write) => {
  const min = Number(el.dataset.min), max = Number(el.dataset.max), step = Number(el.dataset.step);
  const valueAt = () => min + Math.round(el.scrollLeft / 10) * step;
  let dragging = false;
  el.addEventListener("pointerdown", (evt) => { dragging = true; el.setPointerCapture(evt.pointerId); });
  el.addEventListener("pointerup", () => { dragging = false; });
  el.addEventListener("scroll", () => dragging || write(valueAt()), { passive: true });
  return {
    show(value) { /* return early when value is already shown; else scroll to it */ },
    step(dir) { write(Math.min(max, Math.max(min, valueAt() + dir * step))); },
  };
};
```

```python
h.Div(
    {"data-min": 30, "data-max": 200, "data-step": 0.1},
    data.ref("_weight_ruler"),
    data.init("el.ruler ??= app.ruler(el, v => $weight_kg = v)"),
    data.effect("el.ruler.show($weight_kg)"),
    *ticks,
)
h.Button({"type": "button"}, data.on("click", "$_weight_ruler.ruler.step(1)"), "+")
```

## Loading

`app/assets.py` lists the files; the shell loads them before Datastar, so `app` exists when Datastar runs the first `data-init`:

```python
SCRIPTS = tuple(ASSETS.href(f"js/{name}.js") for name in ("theme", "share", "ruler"))
```

```python
h.Head(
    h.Link({"rel": "stylesheet", "href": STYLE_CSS}),
    *[h.Script({"src": src, "defer": True}) for src in SCRIPTS],
    ModuleScript(DATASTAR_JS),
)
```

Every page loads every file; `Assets` fingerprints them, so the browser caches them. A large file that one page uses may load from that page's head instead.

## Rules

- `security_headers()` sets no Content-Security-Policy. An inline `<script>`, a `static/js/` file, and Datastar expressions all run.
- **Datastar adds the listeners that the app reacts to.** `data.on("click", ...)`; `target="window"`, `"document"`, or `"outside"` for a page-wide event. Datastar removes them when the element leaves. A file never calls `addEventListener` on `window` or `document`. The one exception is `visualViewport`, from one `data.init` on the shell.
- **Page-wide listeners sit on the shell element**, in one place:

  ```python
  h.Body(
      data.on("resize", "app.viewport.sync()", target="window"),
      data.on("storage", "app.theme.storage(evt)", target="window"),
      data.on("focusin", "app.viewport.reveal(evt.target)", target="document"),
  )
  ```

- **Signals carry state between JavaScript and HTML.** A function returns a value (`$t = app.clock.now()`) or calls a callback the expression gives it (`v => $weight_kg = v`). HTML renders the result with `data.show`, `data.class_`, `data.attr`, `data.text`.
- **JavaScript does not build HTML.** Tailwind scans only `app/**/*.py`, and a repaint removes what the server did not render. Render the markup on the server and toggle it with signals.
- **UI state that a click toggles is a local signal.** A QR panel, a "Copied" label, a pressed button: `$_qr = !$_qr` with `data.show("$_qr")` and `data.attr("aria-pressed", "$_qr")`, not `el.hidden = ...` in a file.
- **A repaint copies every attribute from the server HTML.** An element whose `style` or `class` JavaScript writes during an interaction (a drag offset) gets `data.preserve_attr("style class")`.
- **`data.init` runs again when its text changes.** Keep the text constant (server values go in `data-*` attributes) and write `el.x ??= app.x(el, ...)`, so the factory runs once per element.
- **Guard an index read with the length.** Reading `$files[2]` when the list is shorter makes Datastar create the entry as `""`, so `$files.length` grows. Write `$files.length > 2 && $files[2].name`, and the same guard in `data.attr` and `data.text`.
- **A checkbox group bound to one signal is positional.** Predefine the signal as an array (`"scope": []`). `data.bind("scope")` on four checkboxes then gives `["", "saved", "", ""]`: the value when checked, `""` when not. The server drops the empty strings before it uses the list.
- **A part that a `GET` patches is not patched again for its own controls.** Re-rendering a checked checkbox from the server unchecks it, and the signal keeps the old value. Patch the results; leave the controls to the client.
- **Another element is a ref, not an id lookup.** `data.ref("_edit")` on the dialog, `$_edit.showModal()` on the button. A ref name starts with `_`, so the element is not sent to the server.
- **Server values reach JavaScript as signals or `data-*` attributes.** When an expression needs a literal, use `string_literal` from `stario.datastar.format`. Never build JavaScript with an f-string or `.replace`.
- **`sse.execute_script(...)` is for an action, not for text**: `app.list.focus()`. A server value in it goes through `string_literal`, which escapes `<` from stario 5.2, so it cannot end the script tag. Text for the user goes in a signal (`_toast`, `_error`).
- **The only inline `<script>` is the theme restore in `<head>`.** It is one constant line and must run before the first paint (skill `stario-tailwind-daisyui`).
- **Write the logic, not the defence.** No fallback for a `data-*` value the server always renders, no `if (!el) return` for an element the expression just passed, no `try` around an API the app's browsers have. Keep `try` where an API throws in normal use (`releasePointerCapture`, `navigator.share` cancel). The server validates input again.
- **No method that only forwards** to another function, and no IIFE that returns an object.

## The check

`tests/test_js.py` collects every `app.<name>.<method>` in the strings of `app/**/*.py` and asserts that `static/js/<name>.js` defines it. A rename or a typo fails `just check`. `stario-create new` writes it; copy it from a new app into an older one.

A file that holds state (a drag, a ruler) is the one case for a browser (skill `stario-browser-check`). Check that one interaction, then stop.

## Common mistakes

| Avoid | Do |
| --- | --- |
| JavaScript in a Python string, `h.Script(SafeString(...))` | a function in `static/js/<name>.js` |
| `window.myThing = ...`, `if (window.x) return` guards | `app.<name>` in its own file |
| `addEventListener` on `window` or `document` | `data.on(..., target="window")` |
| `DOMContentLoaded`, `dataset.bound` guards | `data.init` on the element |
| `document.getElementById(...)` in an expression | `data.ref("_name")` and `$_name` |
| JavaScript that filters a JSON copy of server data | a `GET` that patches its part |
| JavaScript that builds HTML | server HTML plus `data.show` / `data.class_` |
| A five-statement `data.on` expression | an `app.<name>.<method>` call |
| A Python helper that returns a JavaScript string | the expression inline, or a function in the file |
