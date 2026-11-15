---
name: stario-feature
description: Add a live page to a Stario app - a list or board in SQLite that every tab sees change at once. Also a command that goes to the page it created, removing a page, and a folder that grew. Use when a page does not refresh in other tabs. Not for a static page (AGENTS.md). Sort, filter, search - stario-view. Memory or one-tab messages - stario-relay. Slow work - stario-jobs.
---

# Add a live page

`AGENTS.md` holds the rules. Look up a name in `stario-api` only when this skill and the code do not show it. To change a page, read its folder first.

## Steps

1. Decide the resource. The path names it: `/todos`, `/rooms/{room_id}`. One folder `app/features/<page>/`, named after the URL noun.
2. Decide the stream source. Rows in SQLite: `db.watch` (this skill). State in memory, or a message to one tab: skill `stario-relay`. Ask the developer before you add a database.
3. Write `__init__.py`, `urls.py`, `views.py`, `handlers.py`, and `data.py` when the page owns state.
4. In `app/main.py`, build the shared objects, then add `TodosPage(db).register(app)` under `# pages`. Add the schema function of the page to `schema(tx)`.
5. Add `(TODOS, "Todos")` to `LINKS` in `app/features/home/views.py`.
6. Write `tests/test_<page>.py`, then run `just check`. Fix every failure.

## A live page

A shared todo list in SQLite. The stream follows `db.watch`, so the commands only write. Nothing publishes.

```python
# urls.py
from stario import Route

TODOS = Route("GET /todos")
TODOS_LIVE = Route("GET /todos/live")
ADD_TODO = Route("POST /todos")
TOGGLE_TODO = Route("POST /todos/{todo_id}/toggle")
```

```python
# data.py
from dataclasses import dataclass

from litewriter import LiteWriter, Tx
from stario.json import dumps

COLUMNS = {
    "title": "TEXT AS (data->>'title')",
    "done": "INTEGER AS (data->>'done')",
}

ITEMS = "SELECT id, title, done FROM todos ORDER BY id"


@dataclass(frozen=True, slots=True)
class Todo:
    id: int
    title: str
    done: int


def schema(tx: Tx) -> None:
    tx.execute(
        "CREATE TABLE IF NOT EXISTS todos ("
        " id INTEGER PRIMARY KEY, data TEXT NOT NULL CHECK (json_valid(data)))"
    )
    have = {row[0] for row in tx.query("SELECT name FROM pragma_table_xinfo('todos')")}
    for name, column in COLUMNS.items():
        if name not in have:
            tx.execute(f"ALTER TABLE todos ADD COLUMN {name} {column} VIRTUAL")


def list_todos(db: LiteWriter) -> list[Todo]:
    return db.query(ITEMS, Todo)


def get_todo(db: LiteWriter, todo_id: int) -> Todo | None:
    return db.one("SELECT id, title, done FROM todos WHERE id = :id", Todo, id=todo_id)


def add_todo(tx: Tx, title: str) -> int:
    return tx.value(
        "INSERT INTO todos (data) VALUES (:data) RETURNING id",
        data=dumps({"title": title, "done": False}),
    )


def toggle_done(tx: Tx, todo_id: int) -> None:
    tx.execute(
        "UPDATE todos SET data = json_set(data, '$.done', json(iif(done, 'false', 'true')))"
        " WHERE id = :id",
        id=todo_id,
    )
```

```python
# views.py
from stario import h
from stario.datastar import at, data
from stario.markup import HtmlElement

from app.common.shell import page
from app.features.todos.data import Todo
from app.features.todos.urls import ADD_TODO, TODOS_LIVE, TOGGLE_TODO


def render(items: list[Todo]) -> HtmlElement:
    return page(
        "Todos",
        h.Main(
            {"id": "todos"},
            data.signals({"title": ""}, if_missing=True),
            data.init(at.get(TODOS_LIVE.href(), retry="always")),
            h.Form(
                data.on("submit", at.post(ADD_TODO.href()), prevent=True),
                data.indicator("_adding"),
                h.Input(
                    {"type": "text", "required": True, "maxlength": 200},
                    data.bind("title"),
                ),
                h.Button({"type": "submit"}, data.attr("disabled", "$_adding"), "Add"),
            ),
            h.Ul(*[item(t) for t in items]) if items else h.P("No todos yet."),
        ),
    )


def item(t: Todo) -> HtmlElement:
    return h.Li(
        h.Label(
            h.Input(
                {"type": "checkbox", "checked": bool(t.done)},
                data.on("click", at.post(TOGGLE_TODO.href(t.id)), prevent=True),
            ),
            h.S(t.title) if t.done else t.title,
        )
    )
```

```python
# handlers.py
from dataclasses import dataclass

from litewriter import LiteWriter
from stario import App, Context, Writer
from stario.datastar import SSE, read_signals

from app.features.todos.data import ITEMS, Todo, add_todo, get_todo, list_todos, toggle_done
from app.features.todos.urls import ADD_TODO, TODOS, TODOS_LIVE, TOGGLE_TODO
from app.features.todos.views import render


@dataclass(frozen=True, slots=True)
class TodosPage:
    db: LiteWriter

    def register(self, app: App) -> None:
        app.add(TODOS, self.show)
        app.add(TODOS_LIVE, self.live)
        app.add(ADD_TODO, self.add)
        app.add(TOGGLE_TODO, self.toggle)

    async def show(self, c: Context, w: Writer) -> None:
        w.html(render(list_todos(self.db)))

    async def live(self, c: Context, w: Writer) -> None:
        sse = SSE(w)
        async with self.db.watch(ITEMS, Todo) as rows:
            async for todos in c.alive(rows):
                sse.patch_elements(render(todos))

    async def add(self, c: Context, w: Writer) -> None:
        title = str((await read_signals(c.req)).get("title", "")).strip()
        if not title or len(title) > 200:
            w.text("title must be 1 to 200 characters", status=400)
            return
        SSE(w).patch_signals({"title": ""})
        await self.db.write(add_todo, title)

    async def toggle(self, c: Context, w: Writer) -> None:
        todo_id = c.match.params["todo_id"]
        if not todo_id.isdecimal() or get_todo(self.db, int(todo_id)) is None:
            w.text("no such todo", status=404)
            return
        w.empty()
        await self.db.write(toggle_done, int(todo_id))
```

`add` replies with `patch_signals` to clear the input, then awaits the write. The commit wakes the watch, and every open tab repaints.

## Tests

```python
# tests/test_todos.py
from app.features.todos.urls import ADD_TODO, TODOS, TODOS_LIVE, TOGGLE_TODO


async def test_add_shows_on_every_tab(client):
    async with (
        client.stream("GET", TODOS_LIVE.href(), timeout=2) as first,
        client.stream("GET", TODOS_LIVE.href(), timeout=2) as second,
    ):
        one, two = first.iter_events(), second.iter_events()
        assert 'id="todos"' in (await anext(one))["data"]
        assert 'id="todos"' in (await anext(two))["data"]
        r = await client.post(ADD_TODO.href(), json={"title": "milk"})
        assert r.status_code == 200
        assert "milk" in (await anext(one))["data"]
        assert "milk" in (await anext(two))["data"]


async def test_toggle_repaints_the_stream(client):
    await client.post(ADD_TODO.href(), json={"title": "milk"})
    async with client.stream("GET", TODOS_LIVE.href(), timeout=2) as live:
        events = live.iter_events()
        assert "checked" not in (await anext(events))["data"]
        assert (await client.post(TOGGLE_TODO.href(1))).status_code == 204
        assert "checked" in (await anext(events))["data"]


async def test_the_page_loads_and_bad_input_gets_4xx(client):
    assert 'id="todos"' in (await client.get(TODOS.href())).text
    assert (await client.post(ADD_TODO.href(), json={"title": " "})).status_code == 400
    assert (await client.post(TOGGLE_TODO.href(99))).status_code == 404
```

Read the first event, so the subscription is up. Send the command. Assert the next event. `timeout=2` fails a missing repaint in two seconds. This is the whole check for "the other tab never updates". Do not open a browser for it.

## Go to the page a command made

A command that creates a resource with its own page (a room, a document) writes first, because the URL needs the new id. Then it answers `navigate`:

```python
async def create(self, c: Context, w: Writer) -> None:
    name = str((await read_signals(c.req)).get("name", "")).strip()
    if not name or len(name) > 80:
        w.text("name must be 1 to 80 characters", status=400)
        return
    room_id = await self.db.write(add_room, name)
    SSE(w).navigate(ROOM.href(room_id))
```

A test asserts `"window.location" in r.text`.

## Remove a page

1. Delete `app/features/<page>/` and `tests/test_<page>.py`.
2. Remove the `register` call and the schema call from `app/main.py`.
3. Fix every import of the deleted `urls.py` or `data.py`. Pyrefly finds them.
4. Tables the page owned: ask the developer whether to drop them.
5. `just check`.

## When the folder grows

A `handlers.py` over about 300 lines or a `views.py` over about 400 lines usually hides a second resource. Split by URL noun, not by layer. Code with no URL moves to `app/<name>/` as plain functions, not into a service class.
