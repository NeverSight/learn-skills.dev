---
name: stario-view
description: Choose what one tab of a Stario page sees - a sort, a filter, paging, or a search as you type. Use when the user asks to sort or filter a list, to page through it, for a per-person or per-tab sort that still updates live, or for a search box that filters while the user types. The view lives in the URL as a View dataclass; the search is a GET that patches one part.
---

# A view in the URL, and search as you type

`AGENTS.md` holds the rules. Skill `stario-feature` has the live page that this skill extends. Look up a name in `stario-api` only when this skill and the code do not show it.

Two kinds of "what this tab sees":

- **A view**: a sort, a filter, a page number. It is in the query of the URL, so a reload, a shared link, and the back button show the same thing. Each tab has its own URL, so each tab has its own sort. A `View` dataclass in `urls.py` reads and writes it.
- **A private read**: a result that only this tab needs while the user types. A `GET` reads the signals and patches one part. It keeps nothing.

## A view

```python
# urls.py
from dataclasses import dataclass

from stario import Route
from stario.http.query import ParsedQuery

TODOS = Route("GET /todos")
TODOS_LIVE = Route("GET /todos/live")
ADD_TODO = Route("POST /todos")
TOGGLE_TODO = Route("POST /todos/{todo_id}/toggle")

SORTS = ("new", "old", "title")


@dataclass(frozen=True, slots=True)
class TodosView:
    sort: str = "new"
    hide_done: bool = False

    @classmethod
    def from_query(cls, query: ParsedQuery) -> TodosView:
        sort = query.get("sort", "new")
        return cls(sort if sort in SORTS else "new", query.get("hide_done") == "1")

    def query(self) -> dict[str, str]:
        return {"sort": self.sort, "hide_done": "1" if self.hide_done else "0"}
```

An unknown value falls back to the default, so an old link still opens.

```python
# data.py: one fixed SQL text per sort; a filter is a parameter
SORTED = {
    "new": "SELECT id, title, done FROM todos WHERE done <= :most ORDER BY id DESC",
    "old": "SELECT id, title, done FROM todos WHERE done <= :most ORDER BY id",
    "title": "SELECT id, title, done FROM todos WHERE done <= :most ORDER BY lower(title)",
}


def list_todos(db: LiteWriter, view: TodosView) -> list[Todo]:
    return db.query(SORTED[view.sort], Todo, most=0 if view.hide_done else 1)
```

`ORDER BY` cannot be a parameter. Thus each sort key picks one constant SQL text. Every outside value is a `:name` parameter.

```python
# views.py: each choice is a link to a new URL
def render(todos: list[Todo], view: TodosView) -> HtmlElement:
    return page(
        "Todos",
        h.Main(
            {"id": "todos"},
            data.signals({"title": ""}, if_missing=True),
            data.init(at.get(TODOS_LIVE.href(query=view.query()), retry="always")),
            h.Nav(
                *[
                    h.A(
                        {
                            "href": TODOS.href(query=replace(view, sort=s).query()),
                            "aria-current": "true" if s == view.sort else None,
                        },
                        s,
                    )
                    for s in SORTS
                ],
                h.A(
                    {"href": TODOS.href(query=replace(view, hide_done=not view.hide_done).query())},
                    "Show done" if view.hide_done else "Hide done",
                ),
            ),
            h.Ul(*[item(t) for t in todos]),
        ),
    )
```

`replace` is `dataclasses.replace`. `item` is the row of skill `stario-feature`. The stream URL carries the view, so the `data.init` text is the same in every render of this tab.

```python
# handlers.py: the page GET and the stream read the same view
async def show(self, c: Context, w: Writer) -> None:
    view = TodosView.from_query(c.req.query)
    w.html(render(list_todos(self.db, view), view))


async def live(self, c: Context, w: Writer) -> None:
    view = TodosView.from_query(c.req.query)
    sse = SSE(w)
    most = 0 if view.hide_done else 1
    async with self.db.watch(SORTED[view.sort], Todo, most=most) as rows:
        async for todos in c.alive(rows):
            sse.patch_elements(render(todos, view))
```

A new sort is a link. The browser loads the new URL, opens a new stream with the new query, and closes the old one. The commands do not change.

```python
# tests/test_todos.py
async def test_the_view_follows_the_query(client):
    for title in ("a", "b"):
        await client.post(ADD_TODO.href(), json={"title": title})
    r = await client.get(TODOS.href(query={"sort": "old"}))
    assert r.text.index(">a<") < r.text.index(">b<")
    r = await client.get(TODOS.href(query={"sort": "nonsense"}))
    assert r.text.index(">b<") < r.text.index(">a<")


async def test_a_sorted_stream_still_repaints(client):
    url = TODOS_LIVE.href(query={"sort": "title", "hide_done": "0"})
    async with client.stream("GET", url, timeout=2) as live:
        events = live.iter_events()
        await anext(events)
        await client.post(ADD_TODO.href(), json={"title": "milk"})
        assert "milk" in (await anext(events))["data"]
```

Paging is the same: `page: int = 1` in the view, validated with `isdecimal()`, and `LIMIT 20 OFFSET :offset` in the SQL.

## Search as you type

The result only this tab needs. It changes no state, so it needs no stream.

```python
# urls.py
SEARCH = Route("GET /search")
SEARCH_RESULTS = Route("GET /search/results")
```

```python
# views.py: the page, and the part that the read replaces
def results(matches: list[str], total: int) -> HtmlElement:
    return h.Div({"id": "results"}, h.P(f"{total} matches"), h.Ul(*[h.Li(m) for m in matches]))


def render(matches: list[str], total: int) -> HtmlElement:
    return page(
        "Search",
        h.Main(
            {"id": "search"},
            data.signals({"q": ""}, if_missing=True),
            h.Input(
                {"type": "search"},
                data.bind("q"),
                data.on("input", at.get(SEARCH_RESULTS.href()), debounce="200ms"),
            ),
            results(matches, total),
        ),
    )
```

```python
# handlers.py
@dataclass(frozen=True, slots=True)
class SearchPage:
    cities: tuple[str, ...]

    def register(self, app: App) -> None:
        app.add(SEARCH, self.show)
        app.add(SEARCH_RESULTS, self.results)

    async def show(self, c: Context, w: Writer) -> None:
        w.html(render(list(self.cities[:20]), len(self.cities)))

    async def results(self, c: Context, w: Writer) -> None:
        q = str((await read_signals(c.req)).get("q", "")).strip().lower()
        found = [city for city in self.cities if q in city.lower()]
        SSE(w).patch_elements(results(found[:20], len(found)))
```

Test it with `client.get(SEARCH_RESULTS.href(), params={"datastar": '{"q": "par"}'})` and assert the matches in `r.text`.

- Patch the results, never the input. A repaint of a control loses what the user typed.
- A text too long for a URL: `POST` with the same handler shape. It still changes no state.
- A search that must survive a reload or a shared link is a view: a `<form method="get">` reloads the page with `?q=`.
