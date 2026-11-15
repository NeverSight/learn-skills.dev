---
name: stario-api
description: Every Stario signature on one page - App, Route, Context, Writer, Relay, Span, middleware, h.* tags, TestClient, data.*, at.*, read_signals, SSE, and how a morph treats the page. Look a name up here when the task skill and the code do not show it, and never read the stario source in site-packages instead.
---

# The Stario API

Every signature of stario 5.x. Do not read `site-packages`: pyrefly checks each call.

```python
from stario import App, Context, Relay, Route, Span, Writer, classes, h
from stario.cookies import SignedCookie, delete_cookie, set_cookie
from stario.forms import read_form
from stario.http.middleware import catch_errors, same_origin, security_headers
from stario.markup import baked, render
from stario.testing import TestClient
from stario.datastar import SSE, at, data, read_signals
from stario.datastar.format import string_literal  # user text inside an expression
```

# Server side

## App and Route

```text
app.add(ROUTE, handler)                 # one method on one path
app.use("/prefix", middleware)          # middleware is (inner: Handler) -> Handler
app.create_task(coro, name=None)        # tracked; Stario waits for it on shutdown
app.shutting_down                       # True while the server drains
app.shutdown  # a timer loop reads it once

ROUTE = Route("GET /rooms/{room_id}")   # a GET route answers HEAD too
ROUTE.href(room_id, query={"sort": "title"}, fragment=None)   # "/rooms/7?sort=title"
```

A literal segment beats a parameter: `/rooms/live` and `/rooms/{room_id}` both work.

## Context: `c`

```text
c.req.method   c.req.path
c.req.query                    # ParsedQuery: .get(key, default), .getlist(key), key in
c.req.headers                  # .get(name, default), .getlist(name)
c.req.headers.get("datastar-request")   # set on a Datastar action
c.req.cookies                  # .get(name, default)
await c.req.body(max_size=None)   # 10 MiB by default, past it 413
c.match.params                 # path captures: dict of str; validate, then convert
c.state                        # middleware fills it; read via current_user(c)
c.span                         # this request's span
c.alive(source)                # async iterator until the client leaves or the app drains
c.disconnected  c.shutting_down  c.closing
```

## Writer: `w`

A handler answers once:

```text
w.html(render(...))            # str, bytes, or h.* nodes; status=200
w.text("why", status=400)
w.json(value, status=200)
w.empty()                      # 204
w.redirect(url, status=307)    # a Datastar request: SSE(w).navigate(url)
w.headers.set(name, value)     # before the answer
set_cookie(w, "sid", token, max_age=None, httponly=True, samesite="lax")
delete_cookie(w, "sid")
```

`SignedCookie("__Host-session", keys=[secret])`: `.set(w, data)`, `.get(c.req)`, `.delete(w)`. Login: skill `stario-auth`.

## Forms

```text
with await read_form(c.req, max_size=None) as form:
    form.get("title", "")  form.getlist("tags")
    photo = form.file("photo")  # UploadFile | None; .filename is untrusted
    data = await photo.read()
```

## Relay

```text
relay: Relay[dict] = Relay()                       # one, built in bootstrap
relay.publish("todos.changed", {})                 # dotted subject
async with relay.subscribe("todos.changed", f"tab.{tab}", latest=True) as events:
    async for subject, data in c.alive(events): ...
```

A pattern is an exact subject, `prefix.*`, or `*`. `latest=True` keeps only the newest message per subject. Subscribe before the first render.

## Span

```text
c.span.event("todo.added", {"id": 7})   c.span.attrs({...})   c.span.fail("why")
span = c.span.step("report.run")        # a child span for a job; use it as `with span:`
```

## Middleware

- `same_origin(trusted_origins=, exempt=)`: the CSRF guard; a cross-site `POST` gets 403. Keep it on `/`.
- `security_headers()`: `nosniff`, `x-frame-options: DENY`, a referrer policy. No Content-Security-Policy, so Datastar expressions work.
- `catch_errors(SomeError, respond=fn)`: an exception becomes a response when nothing was sent.

## HTML: `h.*`

Every tag is `h.` plus the tag name with a capital letter: `h.Div`, `h.Textarea`, `h.Dialog`.

- Attributes first, children after: `h.A({"href": HOME.href()}, "Home")`. `data.*` results go with the attributes.
- `True` writes a bare attribute. `None` or `False` leaves it out. `classes("btn", {"active": is_on})` builds `class`.
- A child is a string (escaped), a node, a list of nodes, or `None` (skipped).
- `render(node)` returns the HTML string. SVG: `from stario.markup import svg`.

## TestClient

```text
async with TestClient(bootstrap, request_timeout=5) as client:
    r = await client.get(url, params={"datastar": '{"tab": "t1"}'})
    r = await client.post(url, json={"title": "milk", "tab": "t1"})
    r.status_code  r.text  r.json()  r.headers  r.cookies
    async with client.stream("GET", url, params=TAB, timeout=2) as live:
        events = live.iter_events()            # dicts with "event" and "data"
        first = await anext(events)
    await client.drain_tasks()                 # wait for create_task work
    client.tracer.find_span("report.run").ok
```

The client keeps cookies. A `navigate` answer contains `window.location`.

# Page side: Datastar

## Expressions

- `$title` reads or writes the signal `title`. `$form.title` is a nested signal. `el` is the element. `evt` is the event inside `data.on`.
- A leading `_` makes a signal local: `$_open`. Datastar does not send it to the server.
- Statements join with `;`. More than two statements: a function in `static/js/` (skill `stario-client`).
- User text inside an expression goes through `string_literal(text)`.

## Attributes: `data.*`

```text
data.signals({...}, if_missing=False)   # if_missing=True keeps typed values
data.signal(name, expr)   data.computed(key, expr)
data.bind(name, prop=None, event=None)   # bind("done", prop="checked", event="change")
data.text(expr)   data.show(expr)   data.effect(expr)
data.attr(key, expr)   data.attrs({key: expr})
data.class_(name, expr)   data.classes({name: expr})
data.style(prop, expr)   data.styles({prop: expr})
data.ref(name)                           # $name is this element
data.indicator(name)                     # $name is true while this element's request runs
data.init(expr, delay=None)
data.on(event, expr, once=, passive=, capture=, delay=, debounce=, throttle=,
        target=None,                     # "window" | "document" | "outside"
        prevent=False, stop=False)
data.on_intersect(expr, threshold=, once=, exit=, delay=, debounce=, throttle=)
data.on_interval(expr, duration="1s", leading=False)
data.on_signal_patch(expr, delay=, debounce=, throttle=, include=, exclude=)
data.preserve_attr("open")  data.preserve_attr(["open", "class"])
data.ignore_morph()                      # server patches skip this subtree
data.ignore(self_only=False)             # Datastar skips this subtree
```

A time is `200`, `0.2`, or `"200ms"`. `include` and `exclude` take a regex or a list of names.

Datastar Pro only, so they do nothing with the free `datastar.js`: `persist`, `query_string`, `replace_url`, `scroll_into_view`, `match_media`, `on_resize`, `on_raf`, `animate`, `custom_validity`, and the actions `clipboard`, `intl`, `fit`.

## Actions: `at.*`

```text
at.get(url, *, content_type=, include=, exclude=, selector=, headers=,
       open_when_hidden=, payload=, retry=, retry_interval_ms=, retry_max_count=,
       request_cancellation=)              # every keyword defaults to None
at.post / at.put / at.patch / at.delete / at.query   # same arguments as at.get
at.peek(expr)   at.set_all(value)   at.toggle_all()
```

- `retry`: `"auto"`, `"error"`, `"always"`, `"never"`. A live stream uses `retry="always"`.
- `content_type`: `"json"` (the default, sends the signals) or `"form"`. `include` / `exclude` choose the signals.
- Build the URL with `ROUTE.href(...)`. A plain `fetch` ignores the SSE answer.

## Server side: `read_signals` and `SSE`

```text
signals = await read_signals(c.req)      # dict; a GET sends them in ?datastar=; max_size=
sse = SSE(w)
sse.patch_elements(part, mode=None, selector=None, namespace=None)
sse.patch_signals({...}, only_if_missing=False)
sse.navigate(url)                        # a 303 does not change the URL of a Datastar request
sse.execute_script(code)                 # trusted code only
sse.remove(selector)
```

`mode`: `"outer"` (the default), `"inner"`, `"replace"`, `"prepend"`, `"append"`, `"before"`, `"after"`. A file input bound with `data.bind` arrives as a `FileSignal` dict: `name`, `contents` (base64), `mime`.

## How a morph treats the page

`patch_elements` finds each top element by `id` and morphs it in place. The guide (Render and signals) says what a morph keeps. A subtree the client owns needs `data.ignore_morph()`. Trust the morph: when the stream test shows the new HTML, Datastar puts it on the page (skill `stario-browser-check`).
