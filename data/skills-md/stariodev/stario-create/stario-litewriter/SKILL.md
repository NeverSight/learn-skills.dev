---
name: stario-litewriter
description: SQLite in a Stario app through litewriter (one writer thread, group commit, watch). The recommended store when a Stario app needs persistent data. Use when the user asks for a database, SQLite, persistence, data that survives a restart, a new table or field, an index, or a live page that repaints when rows change.
---

# SQLite with litewriter

litewriter is the SQLite store for a Stario app, when the developer wants data on disk. One SQLite file. One writer thread. Reads from any thread. `watch` wakes a stream after a commit changes the rows it reads.

```bash
uv add "litewriter>=0.3.2,<0.4"
```

Source: https://github.com/Bobowski/litewriter

## API at a glance

Verified against litewriter 0.3.2. Do not grep site-packages for signatures.

```text
async with LiteWriter(path, schema=schema, claim=30) as db:
# one LiteWriter per file: claims, runs schema, serves, drains, closes

rows = await db.write(fn)        # fn(tx) on the writer thread; returns its value
db.push(fn)                      # fire and forget; errors go to on_error
db.submit(fn).result()           # the same write from a plain thread

db.query(sql, **params)          # rows, on any thread
db.one(sql, **params)            # one row or None; db.value -> a scalar, raises on none
await db.aquery(sql)             # async forms: aquery, aone, avalue (worker thread)
tx.query  tx.one  tx.value       # the same three inside a write fn

async with db.watch(query, into, **params) as rows:  # async iterator; one wake
    async for rows in rows:                          # per touching commit

apsw.ConstraintError             # a taken unique value; catch it in the command
LiteError                        # base of QueryError, StateError, ClaimBusy
```

## Open the file in bootstrap

```python
from litewriter import LiteWriter, Tx
from stario import App, Relay, Span

from app.assets import ASSETS
from app.config import Config
from app.features.todos import data as todos_data
from app.features.todos.handlers import TodosPage


def schema(tx: Tx) -> None:
    todos_data.schema(tx)


async def bootstrap(app: App, span: Span):
    config = Config.from_env()
    async with LiteWriter(config.db_path, schema=schema, claim=30) as db:
        span.attrs(await ASSETS.attach(app))
        TodosPage(db, Relay[dict]()).register(app)
        yield
```

`config.db_path` is `app.sqlite3` in `config.data_dir`: `$PROJECT_DATA_DIR` (Yard: `/data`, kept across deploys), or `./data` on a laptop. An upload also goes in `config.data_dir`. `async with` claims the file, runs `schema` in one transaction, serves, then drains and closes after `yield`. `claim=30` makes a second process wait 30 seconds, then raise `ClaimBusy`. Each page with tables adds one line to `schema`. Pass `db` to each page class. No wrapper goes around it.

## Tables: `id` plus `data`

A table holds a key and one JSON document. A field that a query filters, sorts, joins, or keeps unique becomes a virtual column, computed from `data`, with an index. A real column is for a key that the table is about: `id`, `user_id`, `room_id`.

```python
COLUMNS = {
    "title": "TEXT AS (data->>'title')",
    "done": "INTEGER AS (data->>'done')",
}


def schema(tx: Tx) -> None:
    tx.execute(
        "CREATE TABLE IF NOT EXISTS todos ("
        " id INTEGER PRIMARY KEY, data TEXT NOT NULL CHECK (json_valid(data)))"
    )
    have = {row[0] for row in tx.query("SELECT name FROM pragma_table_xinfo('todos')")}
    for name, column in COLUMNS.items():
        if name not in have:
            tx.execute(f"ALTER TABLE todos ADD COLUMN {name} {column} VIRTUAL")
    tx.execute("CREATE INDEX IF NOT EXISTS todos_done ON todos(done)")
    tx.execute("CREATE UNIQUE INDEX IF NOT EXISTS todos_title ON todos(lower(title))")
```

Why this shape:

- A new field needs no migration. The code writes it into `data`, and old rows read it as `NULL`.
- A new filter or sort is one entry in `COLUMNS` and one index. SQLite computes a virtual column from `data`, so no row is rewritten.
- A field that no query uses again: remove it from `COLUMNS`, then drop its index and its column once, in `schema`:

```python
if "done" in have:
    tx.execute("DROP INDEX IF EXISTS todos_done")
    tx.execute("ALTER TABLE todos DROP COLUMN done")
```

- `pragma_table_xinfo` lists virtual columns. `pragma_table_info` does not.
- `->>` returns SQL values: a JSON `true` reads as `1`. Type the dataclass field as `int`.

Write a document with `stario.json.dumps`. Change one field with `json_set`:

```python
from stario.json import dumps


def add_todo(tx: Tx, title: str) -> int:
    data = dumps({"title": title, "done": False})
    return tx.value("INSERT INTO todos (data) VALUES (:data) RETURNING id", data=data)


def set_title(tx: Tx, todo_id: int, title: str) -> None:
    tx.execute(
        "UPDATE todos SET data = json_set(data, '$.title', :title) WHERE id = :id",
        id=todo_id,
        title=title,
    )
```

A JSON literal goes through `json(...)` as a direct argument: `json_set(data, '$.done', json('true'))`.

## Reads

Reads are plain calls on the loop thread. They do not queue behind the writer.

```python
rows = db.query("SELECT id, title, done FROM todos ORDER BY id", Todo)
row = db.one("SELECT id, title, done FROM todos WHERE id = :id", Todo, id=3)
count = db.value("SELECT count(*) FROM todos")
```

`:name` in the SQL takes the keyword argument `name`. `one` returns `None` when there is no row; `value` raises. The second positional argument builds each row. A large read (an export) awaits `db.aquery(...)` on a worker thread. Every outside value is a `:name` parameter. An f-string may paste only a constant of the same file.

## Writes

A write is a plain `def` whose first argument is `tx`, in the page's `data.py`. The writer runs it in one transaction and commits in a batch. You do not commit. A command reads, validates, replies, and then writes:

- `await db.write(fn, ...)` is the default. The browser has its answer already, so the wait (up to 1/60 s) costs it nothing. The handler gets the result or the exception, and a failure reaches the request span.
- `db.push(fn, ...)` returns before the commit, so a read soon after it can miss the row. A failure goes to the `litewriter` logger. Push only a counter or a last-seen stamp.
- On a plain thread: `db.submit(fn, ...).result()`. On the loop it raises `StateError`.

Rules for a write function:

- It holds the whole batch. No network, no sleep, no password hash inside it.
- Read inside it with `tx.query`, `tx.one`, `tx.value`, never `db.query`. Do not keep `tx`.
- Each write runs in its own savepoint. When it raises, only that write is undone.
- Related changes go in one write function.
- A taken unique value raises `apsw.ConstraintError`. A command catches it and sends the message to its tab.

## The stream: `watch`

`watch` is the default source for a live page whose state is rows. The commands only write; nothing publishes.

```python
async def live(self, c: Context, w: Writer) -> None:
    view = TodosView.from_query(c.req.query)
    sse = SSE(w)
    most = 0 if view.hide_done else 1
    async with self.db.watch(SORTED[view.sort], Todo, most=most) as rows:
        async for todos in c.alive(rows):
            sse.patch_elements(render(todos, view))
```

- The first iteration gives the rows now. Each later one comes after a commit that writes a table and column that the query reads.
- The watch wakes only for columns that its query reads. A new field that the query does not select repaints nothing: add it to the query.
- Equal rows after a commit do not wake. A slow stream gets the newest rows, not a backlog.
- Values are parameters: `db.watch(SQL, Todo, most=0)`. `ORDER BY` and column names cannot be parameters. Keep one fixed SQL text per sort key and pick it from the view: `SORTED = {"new": "... ORDER BY id DESC", "title": "... ORDER BY lower(title)"}` (skill `stario-view`).
- Only commits through this `LiteWriter` wake a watch. A write from another process does not.

**Rows and messages to one tab: `Relay`.** The stream subscribes to `CHANGED` and `tab.<id>` and reads the rows again on each event. Each command awaits its write and then publishes (skill `stario-relay`).

## Rules

- One `LiteWriter` per file per process. The claim is an `flock`: a `ClaimBusy` means the holder is still alive.
- On dev reload the old process must die before the new one claims. Run the watcher so the app is its direct child: `uv run watchfiles 'python -m app.main' app/ static/`. A `ClaimBusy` in dev means an orphan: find it with `lsof <db>.sqlite3-claim` and kill it.
- The scaffold's `tests/conftest.py` points `PROJECT_DATA_DIR` at `tmp_path`, so each test gets its own file.
- `IF NOT EXISTS` on every `CREATE`. The schema function runs again on every start.
