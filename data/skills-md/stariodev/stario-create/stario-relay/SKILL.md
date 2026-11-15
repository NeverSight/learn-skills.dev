---
name: stario-relay
description: A live Stario page on state in memory, or a command that tells only its own tab something (an error, a toast) - through one Relay and a tab id. Also an edit dialog that stays open and keeps what the user typed while other people change the list, and a value one tab remembers (a display name). Use for chat rooms, boards, or lists kept in memory, for a conflict or duplicate message, and for a dialog.
---

# Relay: state in memory and messages to one tab

`AGENTS.md` holds the rules. Look up a name in `stario-api` only when this skill and the code do not show it. Rows in SQLite with no message to one tab use `db.watch` (skill `stario-feature`), not this skill.

One `Relay[dict]` per app, built in `bootstrap`, shared by every page. Two kinds of subject:

- `notes.changed` carries `{}`. Each command publishes it after it changes the state. Each stream renders again.
- `tab.<id>` carries signals for one tab. Only the stream of that tab sends them.

## A live page in memory

Notes that several people rename at once. The edit dialog survives each repaint.

```python
# data.py
from dataclasses import dataclass, field
from itertools import count


@dataclass(slots=True)
class Note:
    id: int
    title: str


@dataclass(slots=True)
class Notes:
    rows: dict[int, Note] = field(default_factory=dict)
    ids: count[int] = field(default_factory=lambda: count(1))


def list_notes(notes: Notes) -> list[Note]:
    return sorted(notes.rows.values(), key=lambda n: n.id)


def get_note(notes: Notes, note_id: int) -> Note | None:
    return notes.rows.get(note_id)


def add_note(notes: Notes, title: str) -> Note:
    note = Note(next(notes.ids), title)
    notes.rows[note.id] = note
    return note
```

```python
# urls.py
NOTES = Route("GET /notes")
NOTES_LIVE = Route("GET /notes/live")
ADD_NOTE = Route("POST /notes")
RENAME_NOTE = Route("POST /notes/rename")
```

```python
# views.py
def render(notes: list[Note], tab: str) -> HtmlElement:
    return page(
        "Notes",
        h.Main(
            {"id": "notes"},
            data.signals(
                {"tab": tab, "title": "", "editing_id": 0, "new_title": "", "_error": ""},
                if_missing=True,
            ),
            data.init(at.get(NOTES_LIVE.href(), retry="always")),
            h.Form(
                data.on("submit", at.post(ADD_NOTE.href()), prevent=True),
                data.indicator("_adding"),
                h.Input({"type": "text", "required": True, "maxlength": 200}, data.bind("title")),
                h.Button({"type": "submit"}, data.attr("disabled", "$_adding"), "Add"),
                h.P({"role": "alert"}, data.show("$_error"), data.text("$_error")),
            ),
            h.Ul(*[item(n) for n in notes]),
            h.Dialog(
                data.ref("_edit"),
                data.preserve_attr("open"),
                h.Form(
                    data.on(
                        "submit", at.post(RENAME_NOTE.href()) + "; $_edit.close()", prevent=True
                    ),
                    h.Input({"type": "text", "required": True}, data.bind("new_title")),
                    h.Button({"type": "submit"}, "Save"),
                ),
            ),
        ),
    )


def item(n: Note) -> HtmlElement:
    return h.Li(
        n.title,
        h.Button(
            {"type": "button"},
            data.on(
                "click",
                f"$editing_id = {n.id}; $new_title = {string_literal(n.title)}; $_edit.showModal()",
            ),
            "Rename",
        ),
    )
```

```python
# handlers.py
import uuid
from dataclasses import dataclass

from stario import App, Context, Relay, Writer
from stario.datastar import SSE, read_signals

CHANGED = "notes.changed"


@dataclass(frozen=True, slots=True)
class NotesPage:
    notes: Notes
    relay: Relay[dict]

    def register(self, app: App) -> None:
        app.add(NOTES, self.show)
        app.add(NOTES_LIVE, self.live)
        app.add(ADD_NOTE, self.add)
        app.add(RENAME_NOTE, self.rename)

    async def show(self, c: Context, w: Writer) -> None:
        w.html(render(list_notes(self.notes), uuid.uuid7().hex))

    async def live(self, c: Context, w: Writer) -> None:
        tab = str((await read_signals(c.req)).get("tab", ""))
        if not (tab.isalnum() and len(tab) <= 32):
            w.text("tab must be a short id", status=400)
            return
        async with self.relay.subscribe(CHANGED, f"tab.{tab}", latest=True) as events:
            sse = SSE(w)
            sse.patch_elements(render(list_notes(self.notes), tab))
            async for subject, signals in c.alive(events):
                if subject == CHANGED:
                    sse.patch_elements(render(list_notes(self.notes), tab))
                else:
                    sse.patch_signals(signals)

    async def add(self, c: Context, w: Writer) -> None:
        title = str((await read_signals(c.req)).get("title", "")).strip()
        if not title or len(title) > 200:
            w.text("title must be 1 to 200 characters", status=400)
            return
        if any(n.title.lower() == title.lower() for n in list_notes(self.notes)):
            SSE(w).patch_signals({"_error": f"“{title}” is already on the list."})
            return
        SSE(w).patch_signals({"title": "", "_error": ""})
        add_note(self.notes, title)
        self.relay.publish(CHANGED, {})

    async def rename(self, c: Context, w: Writer) -> None:
        signals = await read_signals(c.req)
        note_id = signals.get("editing_id")
        title = str(signals.get("new_title", "")).strip()
        if type(note_id) is not int or (note := get_note(self.notes, note_id)) is None:
            w.text("no such note", status=404)
            return
        if not title or len(title) > 200:
            w.text("title must be 1 to 200 characters", status=400)
            return
        w.empty()
        note.title = title
        self.relay.publish(CHANGED, {})
```

```python
# app/main.py, inside bootstrap before yield
relay: Relay[dict] = Relay()
NotesPage(Notes(), relay).register(app)
```

- The page `GET` makes a new `tab`. The stream renders the same `tab`, so the `data-signals` text stays the same in every render.
- Subscribe before the first render, so no change falls between them.
- The duplicate check is a read, so it is part of validation. Its reply patches `_error` at once.
- `data.ref("_edit")` puts the dialog in the local signal `$_edit`. `preserve_attr("open")` keeps it open through a repaint. `if_missing=True` keeps what the user typed. The server never renders the dialog open.
- `type(...) is not int` also rejects `true`, which `isinstance` accepts.
- A value one tab remembers (a display name): one more signal in `data.signals`. Each command reads it like any input. A reload starts a new tab with empty signals.

## A message after the work

A command that learns something only after its reply (a unique index in SQLite, a job that fails) sends it through `tab.<id>`. The command reads `tab` from the signals and validates it like the stream does:

```python
SSE(w).patch_signals({"title": "", "_error": ""})
try:
    await self.db.write(add_todo, title)
except apsw.ConstraintError:
    c.span.event("todo.duplicate", {"title": title})
    self.relay.publish(f"tab.{tab}", {"_error": f"“{title}” is already on the list."})
    return
self.relay.publish(CHANGED, {})
```

The stream is the one above: it reads the rows again on `CHANGED`. Send every changed signal in one publish. `latest=True` keeps only the newest message for each subject.

A toast is the `_toast` signal. The shell of the scaffold already renders it and clears it after 4 seconds: `self.relay.publish(f"tab.{tab}", {"_toast": "Saved."})`.

## Tests

```python
TAB, OTHER = {"datastar": '{"tab": "t1"}'}, {"datastar": '{"tab": "t2"}'}


async def test_rename_repaints_every_tab(client):
    await client.post(ADD_NOTE.href(), json={"title": "milk"})
    async with (
        client.stream("GET", NOTES_LIVE.href(), params=TAB, timeout=2) as mine,
        client.stream("GET", NOTES_LIVE.href(), params=OTHER, timeout=2) as other,
    ):
        one, two = mine.iter_events(), other.iter_events()
        await anext(one)
        await anext(two)
        r = await client.post(RENAME_NOTE.href(), json={"editing_id": 1, "new_title": "eggs"})
        assert r.status_code == 204
        assert "eggs" in (await anext(one))["data"]
        assert "eggs" in (await anext(two))["data"]


async def test_a_duplicate_answers_its_own_tab(client):
    await client.post(ADD_NOTE.href(), json={"title": "milk"})
    r = await client.post(ADD_NOTE.href(), json={"title": "Milk"})
    assert "already on the list" in r.text
```

A message after the work arrives on the stream of its tab: `event["event"] == "datastar-patch-signals"`, and the other stream gets nothing. A bad `tab`, an unknown `editing_id`, and `"editing_id": true` each get a 4xx.
