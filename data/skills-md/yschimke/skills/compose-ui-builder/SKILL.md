---
name: compose-ui-builder
description: Open and edit checked-in .uid designs, compare real renders against references, and implement them in application code. Author and edit a Compose UI design over MCP against a compose-preview serve deployment — create a screen or a Wear widget, insert and edit nodes, and export the Kotlin, PNG or SVG. Also use when no host exists and the builder must be run locally (ui-builder --no-project). Use when asked to build, change, or review a UI Builder design (a URL like /ui-builder/catalog/design-id), to explore alternative versions of one, to turn an approved design into Compose code or find the design a PR implements, or to collaborate with a designer on one.
---

# Compose UI Builder

The UI builder is an authoring surface served by `compose-preview serve`: a
design is a **document of catalog components**, edited by an operation log, and
exported as Compose Kotlin (or PNG/SVG). A person edits it in the browser at
`/ui-builder/<catalog>/<designId>`; you edit the same live document over the
server's MCP endpoint. Both land in one revision log, so you and a designer can
work on the same design at the same time.

A design can also live in a checked-in `.uid` file. For a repository design,
inspect its schema and follow [the local design-to-code workflow](references/local-design-to-code.md):
edit the canonical file, compare real design renders with references, adapt
exported Kotlin into the application, then render the affected `@Preview`s.
Use `compose-preview` alongside this skill when a composable already exists.

Maintained at [github.com/yschimke/skills](https://github.com/yschimke/skills)
under `skills/compose-ui-builder/`. The server ships from
[github.com/yschimke/compose-preview-server](https://github.com/yschimke/compose-preview-server);
people start at <https://ui.coo.ee/start>, and the longer guide is
[`docs/UI_BUILDER_GETTING_STARTED.md`](https://github.com/yschimke/compose-preview-server/blob/main/docs/UI_BUILDER_GETTING_STARTED.md).
The public host's MCP endpoint is `https://preview.coo.ee/mcp`: configure only
that URL ([mcp.md § Which MCP server](../compose-preview/references/mcp.md#which-mcp-server)).

## Firm collaboration contract

These rules apply before the creation and editing recipes below:

1. **Work at the recorded home.** For an existing server design, start with
   `ui_builder_get_design` and read its `home`. For a checked-in `.uid`, read
   the file and its recorded home first; a server lookup is not required. A server-homed design is edited
   on that server; a repo-homed design is edited at its recorded `.uid` path.
   Do not export a server design, edit the copy locally, and re-import it.
   Servers record `home` since compose-preview-server v3.76.0; if the response
   has none (an older host, or a design created before then), say that the
   canonical home cannot be verified. Do not infer or rewrite it.
2. **Keep discussion at the home.** For a server-homed design, call
   `ui_builder_list_comments` before the first edit, reply and resolve there,
   and check again before finishing. For a repo-homed design, use its linked PR
   or issue. Link to that discussion with `ui_builder_set_links`; do not split
   it across chat, an issue, and server comments.
3. **Use typed operations and validation.** Prefer `ui_builder_apply` and the
   tool schemas over editing document JSON. Call `ui_builder_check_design`
   (which runs `ui_builder_validate` plus accessibility checks) before showing
   or finishing, or `ui_builder_validate` on a host that has only that. If
   validation or a required schema is not available, say so; an export
   diagnostic is useful but is not a substitute for document validation. If hand-editing is unavoidable,
   validate before saving and render again afterwards.
4. **See the editor after each visible step.** Call `ui_builder_view`
   (compose-preview-server v3.89.0 and later): it draws the canvas as a person
   sees it, with selection, reference overlay and comment pins. On a host that
   does not advertise it, inspect PNG/SVG or native output, label it as not the
   editor viewport, give the browser URL, and never infer selection, overlays,
   or comment pins from JSON or an export.
5. **Close temporary copies.** A local copy may be used for a compile check or
   offline experiment only. Announce its path and purpose, keep its recorded
   home pointing at the canonical design, and save the result back to that home
   or discard the copy before finishing. Moving a design between server and
   repo homes requires explicit approval.

Before finishing, run `ui_builder_check_design`, look at the final editor view
and the device grid, and check for unread or unacknowledged comments at the
design's home. Hand back the link, the revision and whether a person has
approved it ([Approval and handoff to code](#approval-and-handoff-to-code)).
Report any capability that prevented one of those checks.

## Review design guidelines

When asked to review a design, follow the shared
[catalog guidelines checklist](../compose-preview/references/design-guidelines.md).
It ships beside this skill in the default bundle and works without a reviewer
agent or an OpenRouter key. Use advertised `ui_builder_guidelines_prompt`,
`ui_builder_get_guidelines` and `ui_builder_record_guidelines` tools; preserve
the prompt's revision and rules version, inspect its required pictures and
report unanswered rules. Recording a requested review is metadata at the home,
not an edit to nodes or a human approval. Keep model warnings advisory and
measured schema/accessibility checks separate.

**Working with platform skills.** When an official platform skill is loaded
(for example Android's Wear Compose Material 3 skill), it decides which
components and APIs are right. The builder's catalog decides what a design can
contain today. If they disagree, say so rather than picking silently. A catalog
renders one fixed library version, which may differ from the project that will
receive the exported Kotlin.

Return the canonical editor link and tell the person its **Issues** panel
shows a successfully recorded shared guideline result, its model and revision
freshness. Also return the compact verdict and coverage in chat. If recording
is unavailable, make that explicit and keep detailed findings at the design's
existing discussion home when authorized. Link to that discussion from chat;
never imply the panel contains an unsaved review or invent an audit-launch link.

## Viewer, prompts, and interactive decisions

The MCP Apps viewer, prompts and elicitation depend on the host as much as on
the server. Discover them from `tools/list` and the client's capabilities, and
use the text fallbacks in the
[catalog MCP reference](../compose-preview/references/catalog-mcp.md#draft-viewer-and-interactive-capability-fallbacks)
when they are absent.

## Core creation loop

Everything below is the long version. This compact example shows the core
creation calls; the home, comment, validation, and editor-view checks above
still apply:

```jsonc
// 1. request_access  — capabilities, not scope (see "Getting in")
{"capabilities": ["ui-builder-read", "ui-builder-write", "ui-builder-export"],
 "ttlSeconds": 14400,
 "label": "add a header row to the settings screen"}
// → show approveUrl + userCode to your human, then poll_access

// 2. ui_builder_create_design — a whole document; the starter below is known-good
{"designId": "settings-v2", "document": { …see "A document that works"… }}

// 3. ui_builder_apply — insert a column and a text into it, one operation
{"designId": "settings-v2", "operationId": "op-1", "baseRevision": 0, "operations": [
  {"type": "insertNode",
   "node": {"id": "col", "componentId": "layout/column", "slots": {"children": []}},
   "location": {"parent": {"nodeId": "root", "slot": "content"}}},
  {"type": "insertNode",
   "node": {"id": "title", "componentId": "m3/text",
            "properties": {"text": {"type": "string", "value": "Settings"}}},
   "location": {"parent": {"nodeId": "col", "slot": "children"}}}]}
// → {"outcome":{"type":"accepted","committedRevision":1, …}}   ← next baseRevision

// 4. ui_builder_check_design — schema, catalog/export gate and accessibility in one
{"designId": "settings-v2"}
// → {"summary": "…", "ok": false, "findings": [{"nodeId": "title", …}]}  ← fix with apply
//   pass "operations" (+ "baseRevision") instead to dry-run a batch before applying it
//   a `skipped` reason of "no native render was available" may hide a failed
//   compile on older hosts: call ui_builder_render_native to find out

// 5. ui_builder_render_design_matrix — every device the screen claims, one picture
{"designId": "settings-v2", "themes": ["light", "dark"], "fontScales": [1, 2]}

// 6. ui_builder_export — the Kotlin, or diagnostics saying why not
{"designId": "settings-v2", "format": "compose"}

// 7. tell your human where it is
// https://<host>/ui-builder/<catalogSystemId>/settings-v2
```

Read each reply's `summary` first; it is written to be enough on its own. Step 4
replaces a separate validate and accessibility pass, though not the editor
view: run it before you show a design to anybody, and fix its findings by `nodeId` through
`ui_builder_apply`. The device grid in step 5 is where a navigation rail that
never collapses, or text that clips at 200% font scale, shows up. Look at it
before calling the screen done.

Send that browser URL as soon as the design exists, then keep sending the
current revision, what just changed, the comment state, and the next action.
Do not make a person infer progress from a silent series of MCP calls. A useful
update is: “Desktop reference is at revision 4; the header and rails are in;
there are no open comments; next I am comparing it with the attached reference.”

Before creating or editing anything, orient yourself:

1. Look for an existing design or checked-in fixture with the requested name.
   Call `ui_builder_get_design`, read its recorded home and links, and read the
   discussion at that home before deciding to edit or create. Do not copy an
   existing design merely to avoid working at its home.
2. Open the canonical path URL returned by the design identity:
   `https://<host>/ui-builder/<catalogSystemId>/<designId>`. Do not invent an
   old query-string URL; the path carries both the catalog and design.
3. If the request names or attaches a visual reference, check whether one is
   already attached (`ui_builder_compare_reference`, or **Frame, density and
   reference** in the browser).
   The full reference workflow is under [Compare with a reference](#compare-with-a-reference).
4. Report the link, revision, open-comment count, and the first planned part
   before editing. This is the point where the person can correct the target
   while the correction is still cheap.

**Read [references/m3-catalog.md](./references/m3-catalog.md) rather than
calling `ui_builder_list_catalogs` to find out what to insert.** It carries the
component ids, slot names, required properties and enum values for
`m3-catalog`, and the pins for every catalog, which is what an insert needs. A
Wear app screen uses [wear-m3-catalog.md](./references/wear-m3-catalog.md) and
a Wear widget [remote-m3-catalog.md](./references/remote-m3-catalog.md). `list_catalogs` is the
authority and answers with far more — every component's parameters, adapter and
parity statuses — so reach for it when something is missing from the reference
file, and reduce it with the recipe at the bottom of that file.

## No host? Run one locally

Everything above assumes somebody is hosting the builder. If nobody is, you can
be the host — the editor, the design service and the MCP endpoint all ship
inside the server distribution `compose-preview` fetches on first use. This is
the path agents most often get wrong, so the wiring is spelled out.

### Start it

```sh
compose-preview ui-builder --no-project --no-open
#   Local:   http://127.0.0.1:8723/?token=…
#   Builder: http://127.0.0.1:8723/ui-builder/m3-catalog/?token=…
```

`--no-project` opens the builder against the **packaged** catalogs
(`m3-catalog`, `remote-m3`) with no Gradle project and no build host. Without
it, the server wants a project and a build host and says so. `--no-open` prints
the URL instead of launching a browser. Designs persist under
`~/.compose-preview/ui-builder-state`; `--ui-builder-state-dir <dir>` moves
that, and `--ui-builder-state-dir none` serves the editor with no design API.
PNG and SVG export need the JVM to be **Java 21+**; on an older JVM everything
else works and the startup log says which version it found.

The port is the server's default (`8723`) unless taken, in which case the next
free one is used — **read the printed URL, don't assume the port**.

### Reaching it from another device

The server binds **loopback** by default, so the printed `127.0.0.1` URL works
only on the machine that started it. Add `--lan` to bind all interfaces and
print the network URL too:

```sh
compose-preview ui-builder --no-project --no-open --lan
#   Local:   http://127.0.0.1:8723/?token=…
#   Network: http://192.168.0.36:8723/?token=…
```

Both URLs answer, including the machine's own name (`http://<host>.local:8723/`)
where mDNS resolves it. Two things to know before sharing one:

- **The token in the link is the only gate.** `--lan` prints a warning saying so;
  share the link only with people you would let see the previews.
- **A LAN address is not a secure context.** `localhost`, `127.0.0.1` and
  `*.localhost` are trusted by browsers; a machine name or a raw LAN IP over
  plain HTTP is not. Browser APIs that require a secure context — clipboard
  writes, `crypto.subtle`, service workers — are unavailable there, so a feature
  that works on the local URL can fail only on the network one. If the editor is
  blank or a control misbehaves on the machine name and works on `127.0.0.1`,
  check that before anything else. An HTTPS front (a reverse proxy or a tunnel)
  is what makes the network URL a secure context; `--lan` alone cannot.

### The flag that decides whether MCP works at all

A local session is closed by default:

| Symptom | Cause | Fix |
| --- | --- | --- |
| `POST /mcp` 404s | the aggregate MCP endpoint was never enabled | start with `--catalog-mcp`, which also requires `--agent-grants` |
| `/mcp` lists every `ui_builder_*` tool but each call answers *"the presented identity lacks the UI-builder read capability"* | the grant store's capability ceiling is empty, so no approval can carry them | add `--agent-grant-capabilities ui-builder-read,ui-builder-write,ui-builder-export` and restart |
| the approval page shows scopes but no capability checkboxes | same ceiling, seen from the human's side | same flag; the page will then offer them (and name them as withheld when it cannot) |

So the full local command is:

```sh
compose-preview ui-builder --no-project --no-open \
  --agent-grants --catalog-mcp \
  --agent-grant-capabilities ui-builder-read,ui-builder-write,ui-builder-export
```

The `?token=` in the printed Builder URL is the **operator** credential: it
authorizes browser routes and the approval page, and it is what makes you the
approver. It is not the MCP bearer and should not be sent as one.

### Get a grant

Same device-code flow as a deployed host, pointed at the local port:

```sh
compose-preview auth request --server http://127.0.0.1:8723 \
  --capability ui-builder-read --capability ui-builder-write --capability ui-builder-export \
  --label "local authoring session"
# prints approveUrl + userCode; open the URL, confirm the code, approve
```

Open the `approveUrl` with the operator token appended
(`?token=<the token from the Builder URL>`) when the box is gated, approve, and
the waiting command stores the grant. `compose-preview auth status --server …`
shows it; `compose-preview auth token --server …` prints it for anything else.
The request expires in ten minutes and a server restart drops the grant — a
sudden refusal after a restart is that, not a bug.

### Two ways to attach your MCP client

**Server aggregate MCP (Streamable HTTP).** `POST http://127.0.0.1:8723/mcp`
with `Authorization: Bearer <grant>` (a bare `GET /mcp` answers 405 — POST is
the transport). Tool names are the `ui_builder_*` family this skill uses
throughout, so everything below applies unchanged.

**Standalone stdio MCP.** `compose-preview mcp serve --ui-builder-url
http://127.0.0.1:8723`, with `COMPOSE_PREVIEW_UI_BUILDER_TOKEN` exported — it is
read from the environment and **never accepted as an argv value**. This server
speaks the versioned v1 design API, and its tools are named differently from the
aggregate endpoint:

| Tool | What it does |
| --- | --- |
| `list_components` | catalogs and capability schemas — read the current pin before creating |
| `create_design` | a whole v1 document, never overwriting an existing id |
| `open_design` | the latest committed snapshot |
| `apply_design_operations` | one v1 batch (shape below) |
| `render_design` / `export_svg` / `export_compose` | revision-pinned artifacts (the committed revision is required, as on the aggregate tools) |
| `get_revision_diff` | durable events after a sequence cursor |

`apply_design_operations` takes `{"submission": …}` and the submission is the
**batch envelope**: the `type` discriminator is required, `clientId` is required
(any stable string naming your session), and `actorId` must be **omitted** — it
is bound to the authenticated actor, and a different one is refused:

```json
{"type": "batch", "designId": "my-design", "operationId": "op-1",
 "clientId": "my-session", "baseRevision": 0,
 "operations": [
   {"type": "insertNode",
    "node": {"id": "col", "componentId": "layout/column", "slots": {"children": []}},
    "location": {"parent": {"nodeId": "root", "slot": "content"}}}]}
```

A decoder error naming a class discriminator, or `Field 'clientId' is required`,
means exactly those two fields — the same operations work once they are present.

### The shell verbs, against the local session

`compose-preview design list|get|render|export` are clients: they talk to a
server that is already up and exit. Point them at the session explicitly:

```sh
compose-preview design list --server http://127.0.0.1:8723
compose-preview design export my-widget -o Widget.kt --server http://127.0.0.1:8723
```

Two traps. The verbs read `$COMPOSE_PREVIEW_TOKEN` (or the older
`$COMPOSE_PREVIEW_UI_BUILDER_TOKEN`) rather than the `auth` store, so export the
token unless your CLI is new enough to bridge a stored grant for an explicit
`--server`. And with no credential they start an interactive device flow and
**wait** — pass `--no-authorize` in CI so they fail fast instead. The default
`--server` is the server's default port, so an auto-picked port needs the flag.

### Creating and rendering without MCP at all

The browser routes accept the operator token as `?token=`, which is enough for a
smoke test:

```sh
curl -X POST 'http://127.0.0.1:8723/ui-builder/designs?token=<operator-token>' \
  -d 'catalog=remote-m3&designId=my-widget&template=weather-widget'   # 303 → the design URL
curl -o design.svg \
  'http://127.0.0.1:8723/api/ui-builder/v1/designs/my-widget/export.svg?token=<operator-token>'
```

Template ids: `blank` for `m3-catalog`; `wear-widget-small`, `wear-widget-large`,
`hello-widget` and `weather-widget` for `remote-m3` — the last two are finished
worked designs, useful as a known-good starting document.

## Two habits worth keeping

**1. Follow Material guidance, responsive layout included.**

A screen that looks right at the frame you authored it at may still have work
left, so it is worth reaching for the catalog's adaptive components before
falling back to fixed layout:

- `layout/supporting-pane-scaffold` is `androidx.compose.material3.adaptive`'s
  own `SupportingPaneScaffold`. It gets a directive computed from the frame's
  constraints, so it collapses to one pane on a phone by itself — a good fit for
  list-detail and content-plus-context screens, better than a `row`.
- `layout/lazy-grid` with `{"type": "adaptiveGrid", "minimumCellWidthDp": N}` is
  `GridCells.Adaptive`, and reflows its column count with the width. Usually
  what you want wherever the item has a natural minimum size.
- Set `environment.exportDevices` to the devices the screen claims to work on,
  and try to look at each before calling it done — the set you look at is the
  set the export writes as `@Preview(device = …)`.

If you find yourself wanting to branch the document on width, that is usually a
sign an adaptive component fits better: the builder holds one document per
design, and two designs for two sizes is the thing adaptive layout saves you
from.

Then read the compact frame honestly. A navigation rail still 88dp wide at
411dp, a chip row squeezed to one letter per line, a tab row breaking its labels
over three lines — worth treating as findings rather than cosmetics, which leads
to the second habit.

**2. Report the gap before working around it, and say that you worked around it.**

When the catalog, the canvas or an exporter will not do the Material-correct
thing, the finding is often worth more than the screen. Roughly in order:

1. **File it**, with the node, the property, the message, and which lane
   refused — canvas, local export, server export; they do not always agree, and
   which ones disagree is half the report.

   Where it goes depends on what is missing, because the catalogs are their own
   projects on their own release trains:

   | The gap | Where it belongs |
   | --- | --- |
   | A component the catalog does not have, or one whose declared property it does not honour — no `NavigationSuiteScaffold`, no `FlowRow`, a `contentAlignment` nothing reads | the catalog's own repository: **m3-catalog**, **wear-m3-catalog** |
   | The builder, the canvas, an exporter or the wire — a shape the canvas draws and the exporter refuses, a validator that disagrees with the server, a dock that clears what you picked | [compose-preview-server](https://github.com/yschimke/compose-preview-server/issues) |

   Not always obvious which, and it is fine to say so: file where you can reach,
   name the component and the lane, and say which project you think owns it.

   A design comment pinned to the node with `ui_builder_post_comment` also puts
   it where the designer will see it. For a real gap, usually worth both.
2. **Then** author the stand-in, if the screen needs one — a `column` of icon
   buttons where a navigation rail should be, rows where a fixed grid should be.
3. **Say it is a stand-in**, in the comment and in whatever you hand back. An
   unlabelled workaround tends to read as the catalog's answer, which hides the
   gap from the next person.

"I used a Row because there is no FlowRow" is a useful sentence. A Row with no
explanation is a screen that looks finished and is not.

## Getting in

The `ui_builder_*` tools are gated on **capabilities** — `ui-builder-read`,
`ui-builder-write`, `ui-builder-export` — which are *not* implied by the
`preview` / `live` / `playground` scope ladder the catalog tools use. Asking for
`live` gets you nothing here. Ask for the three capabilities by name (and
`preview` scope, which costs nothing and lets you look at rendered catalogs).

A call without them fails with the flow spelled out:

> this tool needs a UI-builder read grant; none was presented. Call
> request_access with capability 'ui-builder-read' …

The handshake is the ordinary agent-grant one — see
[server-access.md](../compose-preview/references/server-access.md) and
[catalog-mcp.md](../compose-preview/references/catalog-mcp.md) in the
**compose-preview** skill; all of it applies. Two things specific to here:

- **Ask for all three capabilities at once.** Discovering `ui-builder-write` one
  `403` at a time costs a human round trip each time, and an approver can only
  grant what the server's own ceiling allows anyway.
- **Ask for enough time once.** An iterative authoring and review session often
  outlives the one-hour default. Request `ttlSeconds: 14400` (four hours) when
  the task includes reference comparison or live feedback, while keeping the
  grant limited to these three capabilities. The approver may shorten it. Do
  not ask for a longer grant merely to compensate for polling or idle waiting.
- **Pass the token as each tool's `token` argument.** An MCP client fixes its
  headers when it connects, so a token approved mid-session cannot become a
  header. Every gated tool takes `token` for exactly this reason.
- **Make the approve link one click.** Put the `approveUrl` on a line of its
  own, as a bare URL (and as a link card where the host can show one), with the
  `userCode` on the line above — never only inside a sentence, where a person has to
  ask for it again:

  ```
  Approve access (code <userCode>):
  https://<host>/agent-access/<request-id>
  ```
- **Collect approval in the background.** Immediately after `request_access`,
  relay its exact `approveUrl` and `userCode`, then start a bounded background
  task that calls `poll_access` with the returned request id and device secret.
  `poll_access` is interval polling rather than a server-held long poll, so
  obey `pollIntervalSeconds` and stop on approved, denied, expired or unknown;
  never spin. The collector should hand the token back to the active task
  without printing it and wake the edit automatically. Do not make the person
  return and say “done” merely to trigger the first poll. If the runtime cannot
  delegate background work, keep the current turn open and poll at the stated
  interval while doing any useful ungated or already-authorized preparation.
  The approval request itself normally expires after ten minutes, independently
  of the longer grant TTL being requested.

Grants live in memory: a redeploy drops yours mid-task. A sudden refusal is
that, not a bug — ask again the same way.

## A document that works

`create_design` takes either `fromDesignId` (copy an existing design) or a whole
`document`. Copying is safer *if you can see a design to copy* — but a fresh
grant usually sees none (`list_designs` shows only what your actor owns or was
shared), so you will be writing a document. These three are verified against the
live server; the only fields you should change are the ids, the title, the
environment and — for `wear-m3` only, which has no stable pin — the whole
`catalogPin`.

**A phone screen** (`m3-catalog`):

```json
{
  "schema": "compose-ui-builder-document/v1-candidate",
  "id": "<designId>",
  "title": "<title>",
  "revision": 0,
  "catalogPin": {"systemId": "m3-catalog", "catalogRevision": "candidate",
                 "capabilityDigest": "candidate", "nativeRuntimeId": "candidate"},
  "environment": {"widthDp": 412, "heightDp": 915, "density": 2, "theme": "light",
                  "locale": "en-US", "fontScale": 1, "layoutDirection": "ltr"},
  "roots": ["root"],
  "nodes": {"root": {"id": "root", "componentId": "m3/surface",
                     "properties": {}, "slots": {"content": []}}}
}
```

**A Wear widget** (`remote-m3`) — note the different `catalogRevision`, the
216×76dp (small) or 216×124dp (large) frame, and the scaffold's two slots:

```json
{
  "schema": "compose-ui-builder-document/v1-candidate",
  "id": "<designId>", "title": "<title>", "revision": 0,
  "catalogPin": {"systemId": "remote-m3", "catalogRevision": "wear-widget-scaffolds-v1",
                 "capabilityDigest": "candidate", "nativeRuntimeId": "candidate"},
  "environment": {"widthDp": 216, "heightDp": 76, "density": 2, "theme": "dark",
                  "locale": "en-US", "fontScale": 1, "layoutDirection": "ltr"},
  "roots": ["widget"],
  "nodes": {"widget": {"id": "widget", "componentId": "remote-m3/widget-container-small",
                       "properties": {}, "slots": {"background": [], "content": []}}}
}
```

**A Wear OS app screen** (`wear-m3`) — a round frame, a `screen-scaffold`
root whose `content` takes one child (usually a
`wear-m3/transforming-lazy-column`), and **no fixed pin**: `wear-m3` has no
`candidate` alias, so copy the whole `catalogPin` object from the `wear-m3`
entry of `ui_builder_list_catalogs`. The values below are what preview.coo.ee
served on 2026-10-11 and change with each catalog release:

```json
{
  "schema": "compose-ui-builder-document/v1-candidate",
  "id": "<designId>", "title": "<title>", "revision": 0,
  "catalogPin": {"systemId": "wear-m3",
                 "catalogRevision": "sha256:b37fb7ace974e9cd4b5a068d623487fe",
                 "capabilityDigest": "candidate",
                 "nativeRuntimeId": "wear-m3-p2-a70b6f2e1a9e"},
  "environment": {"widthDp": 227, "heightDp": 227, "density": 2, "theme": "dark",
                  "locale": "en-US", "fontScale": 1, "layoutDirection": "ltr"},
  "roots": ["root"],
  "nodes": {"root": {"id": "root", "componentId": "wear-m3/screen-scaffold",
                     "properties": {}, "slots": {"content": []}}}
}
```

The `catalogPin` is checked against what the server actually serves, and a pin
you invent is refused (`catalogUnavailable`) — which is why there is no "blank
template" argument on the tool. If a pin above stops working, copy the
catalog's `catalogPin` from `ui_builder_list_catalogs` unchanged. Run
`ui_builder_check_design` with the `document` before `create_design`: it
reports a refused pin without creating anything.

## The vocabulary

Four things have to be right, and all four are guessable-wrong:

**Component ids are slash-shaped**: `m3/text`, `layout/column`,
`m3/list-item` — not `m3.Text`, not `Text`. The full table is in
[references/m3-catalog.md](./references/m3-catalog.md).

**A child goes into a named slot of its parent**, never just "into" it:

```json
"location": {"parent": {"nodeId": "col", "slot": "children"}}
```

Slot names differ per component — `children` for `layout/column|row|box`,
`content` for `m3/surface|card|button`, `items` for the lazy containers,
`headline`/`supporting`/`trailing` for `m3/list-item`, `topBar`/`content` for
`layout/scaffold`. `afterNodeId` / `beforeNodeId` place a node among its
siblings. `location: {}` targets the root list — and a design has **at most one
root** (`a design has at most one root; found 2`), which the starter document
already supplies, so in practice every insert you write names a parent slot.

**Property values are wrapped, and the wrapper is the value's *kind*** —
`{"type": …, "value": …}`:

```json
"properties": {"text":     {"type": "string", "value": "Settings"},
               "style":    {"type": "enum",   "value": "headlineSmall"},
               "color":    {"type": "color",  "value": "#5F6368"},
               "maxLines": {"type": "int",    "value": 2},
               "verticalSpacingDp": {"type": "float", "value": 12},
               "enabled":  {"type": "bool",   "value": true}}
```

The reference tables give each property's kind. The three that a raw
`ui_builder_list_catalogs` listing hides, because it describes the JSON shape
(`string`, `number`) rather than the meaning:

- **A property with `allowedValues` is an `enum`** — `style`, `variant`,
  `contentScale`, the arrangements and alignments. A value outside the list is
  refused by name.
- **A colour is a `color`**, written `#RRGGBB` — `m3/text.color`,
  `m3/surface.containerColor`, `m3/icon.color`. A theme role is a `colorToken`
  (`{"type": "colorToken", "value": "outlineVariant"}`), which is the better
  choice when you want the design to follow the theme.
- **A dimension is a `float`**, in dp, and the property name says so
  (`sizeDp`, `verticalSpacingDp`, `shapeDp`).

**Edits name the node by id.** Besides `insertNode`, the operations an edit
loop uses are these (all verified against 3.121.0):

```json
{"type": "setProperty", "nodeId": "signin", "property": "style",
 "value": {"type": "enum", "value": "filledTonal"}}
{"type": "setProperty", "nodeId": "title", "property": "style", "value": {"type": "null"}}
{"type": "removeNodeProperty", "nodeId": "title", "property": "style"}
{"type": "deleteNode", "nodeId": "email"}
{"type": "moveNode", "nodeId": "title",
 "location": {"parent": {"nodeId": "col", "slot": "children"}, "afterNodeId": "signin"}}
```

- `setProperty` sets one property and leaves the others alone. Its `value` is
  wrapped like an inserted one.
- A `{"type": "null"}` value, or `removeNodeProperty`, unsets a property: the
  way back after trying one. Unsetting a required property (`m3/button`'s
  `style`) is refused, naming the node and the field.
- `deleteNode` removes the node and everything in its slots.
- `moveNode` takes the same `location` as an insert.

To swap a component for another (a filled field for an outlined one), do it in
one `apply` call: insert the new node next to the old one, `moveNode` each child
you want to keep into the new node's slots, then `deleteNode` the old one.
Deleting first loses the label, icons and anything else in its slots. To try a
batch first, pass the same `operations` to `ui_builder_check_design` with
`designId` and `baseRevision`: it applies them to a scratch copy and saves
nothing.

**Modifiers are a typed list**, replaced wholesale by `setModifiers`:

```json
{"type": "setModifiers", "nodeId": "col", "modifiers": [
  {"type": "fillMaxWidth"},
  {"type": "padding", "startDp": 16, "topDp": 24, "endDp": 16, "bottomDp": 16}]}
```

Others in use: `fillMaxSize`, `matchParentSize`, `size` (`widthDp`/`heightDp`),
`height`, `width`, `clip` (`shape`), `border`, `weight`, `testTag`. A
`background` takes a colour like any other — `{"type": "background", "color":
{"type": "color", "value": "#D7E3F4"}, "shape": "medium"}` — and `shape` is a
token (`medium`, `large`) or a corner radius in dp as a string (`"20"` on a 40dp
box is a circle, which is how you draw an avatar). Each component declares what
it accepts in `modifierCapabilities`.

## The edit loop

`ui_builder_apply` is the workhorse and the only cheap call:

- **Batch.** `operations` is an array; a scaffold, its column and three texts are
  one call, one revision, one undo step for the designer watching.
- **`operationId` is yours** and makes a retry idempotent — a replay answers
  `idempotentReplay: true` rather than inserting twice.
- **`baseRevision` is the revision you last saw.** The reply's
  `committedRevision` is your next one; track it locally rather than re-reading
  the design. A stale base is **not** automatically refused — the service rebases
  what does not collide and reports what does in `conflicts`, so check that array
  rather than assuming a rejection.
- **A batch is atomic.** One refused operation lands none of them, so a
  container and the child a slot requires can safely be inserted together.
- **A rejection is a normal reply, not an error.** It arrives as
  `{"outcome":{"type":"rejected","code":"invalidDocument","message":"required
  property text is missing","nodeId":"no-text","field":"text"}}` — code, node and
  field, precise enough to fix without a re-read. The three you will actually
  meet:

  | Message | What it means |
  | --- | --- |
  | `required property text is missing` | the component's `required` column |
  | `property style is outside its catalog allowed values` | not in `allowedValues` |
  | `slot content has 0 children; expected 1..unbounded` | that slot needs a child now |

### Keep the loop cheap

`apply` costs a few hundred bytes; a snapshot (`create_design`, `get_design`)
answers with the design **and** the catalog behind it, which is a much bigger
reply. So drive from `apply`: it tells you the new `committedRevision`, which is
the only thing you needed the snapshot for. Hold the node ids you are creating —
you chose them — and re-read the design when somebody else has edited it, not
after every change of your own.

If your host saves oversized tool results to a file, that is the cheap way to
read one: pull `state.document` out of the file rather than into the
conversation.

### Work in visible steps

One `apply` per part of the screen — shell, header, list, footer — rather than
one call for the lot. Each is its own revision, so:

- a rejection costs one part rather than the screen (the batch is atomic, so
  nothing lands and nothing is half-built);
- the designer watching in the browser sees the screen assemble in steps they
  can follow and undo individually;
- and when something looks wrong you know which step did it.

Batch *within* a part, though: a container and the child its slot requires go in
one call, because a slot with a minimum is refused while it is empty.

After each accepted part, perform the available visual check described in the
collaboration contract. State when the editor-view tool is absent, and do not
replace it with an inference from document JSON. Check server comments at the
same boundary so feedback lands before the next part.

## Export is also a check

A design and its Kotlin are two different deliverables, and a design can be
perfectly good without being exportable — the document holds what the catalog
declares, and the Compose generator writes what it has a record for. When the two
disagree the export says so per node, and the design itself is untouched:

```json
{"severity": "error", "code": "UNPROVEN_CALL_SITE",
 "message": "no component `m3/list-item` in this catalog"}
```

So decide which you are making, and act on it early:

- **Kotlin is the deliverable** → export after the first structural batch, not at
  the end. A diagnostic then costs one component swap; the same diagnostic after
  eighty nodes costs a rebuild. Empty `diagnostics` is a real check on the
  design, not a formatting step — but it is not a compile. The gate checks that
  each call has a record, not that the target classpath carries it: an icon key
  such as `pauseCircle` exports `Icons.Filled.PauseCircle`, which only
  `material-icons-extended` ships, with no diagnostic at all. Where it is
  advertised, `ui_builder_render_native` is the compile check: a
  `compileError` there (`Unresolved reference 'PauseCircle'`) is a real failure
  of the Kotlin, so fix it before handing the code over, or name the dependency
  it needs.
- **The design is the deliverable** — a mockup, a PNG, a screen a designer takes
  over → use whatever the catalog offers and read the diagnostics as a note about
  the generator rather than a problem with your design.
- **Server-driven UI is the deliverable** → on an A2UI-capable catalog pin,
  call `ui_builder_export` with `format: "json"` and read its diagnostics.
  Verify visuals separately with `format: "png"` or advertised native render;
  the viewer does not render A2UI. Return a `resource_link` only when supplied,
  and do not treat another JSON format as equivalent.

## Seeing what you built

- **`ui_builder_view`** — the editor canvas as a person sees it: overlays
  (`include`, for example `["reference"]`), `selection`, a past `revision`, and
  `renderer: "native"` where the host compiles. It returns a short-lived https
  link; `inline: true` adds the image to the reply. Where it is not advertised,
  say so; an export is not the editor view.
- **`ui_builder_render_design_matrix`** — one contact sheet of the design on
  several devices × themes × font scales, captioned per cell, from one call.
  Nothing is saved. Use it before calling a screen done: the compact frame and
  `fontScales: [1, 2]` are where layouts break.
- **`ui_builder_export` `format: "compose"`** — the generated Kotlin, plus
  `diagnostics` naming anything the generator refused. Empty diagnostics is the
  gate a designer sees in the browser's code pane, so it is a real check on the
  design, not just a formatting step.
- **`format: "png"`** (or `"svg"`) — base64 in `artifact.content`, a few KB for a
  simple screen and a reliable view of the rendered document. It does not show
  the editor viewport, selection, reference overlay, or comment pins. Needs the
  server on Java 21+; a host without it says so.
- **`ui_builder_render_native`** compiles the design with real Compose on the
  host and reports where each node drew (`nodeBounds`, `taggedNodeIds`). It is a
  compile, so it takes minutes and only exists where the host can run one — reach
  for it when you need the ground truth about layout, and `export png` for the
  ordinary "does this look right" loop. When Kotlin is the deliverable, run it
  once before handing over: it is the only tool that proves the export compiles.
  An empty `nodeBounds` with a `compileError` means the code did not build, and
  the overlay tools (`ui_builder_view` outlines) have nothing to draw.

**A Wear widget is not a watch screen.** A `remote-m3` design whose root is a
`remote-m3/widget-container-*` is shown by the launcher inside a widget frame,
not across a full round display. Do not judge it on the matrix's Wear presets
(`wear_small_round`, `wear_large_round`): they draw the 216×76 dp widget as a
band across a watch face, which is not how anyone sees it. Instead:

- Pass widget-sized `devices` to `ui_builder_render_design_matrix` — the
  container's own size (216×76 dp small, 216×124 dp large) as
  `{"widthDp": 216, "heightDp": 76, "label": "small widget"}` — with the font
  scales below.
- The host shapes the export targets are the Samsung round frame
  (`RoundSmallWidgetPreviewParams`), the Pixel Watch squircle
  (`SquircleSmallWidgetPreviewParams`) and the rectangular one
  (`RectangularSmallWidgetPreviewParams`), plus their large variants. The
  guidelines pictures (`ui_builder_guidelines_prompt`, `check_design` with
  `rendered: true`) are drawn in the Samsung and Pixel Watch frames; ask for
  those when you need to see the clip a frame imposes.
- A Wear **app** screen (`wear-m3`) is the opposite case: cover the small round
  device and the largest font scale.

**Render the large font scale yourself.** `ui_builder_check_design`'s
accessibility pass reasons from declared sizes and, with `rendered: true`,
measured touch targets; it does not see a line that wraps and pushes its
siblings out of a fixed 76 dp frame. Draw the design at the large scale (1.24×
for a Wear widget, 1.5× for a mobile one, 2× only when asked — at 2× a widget
clips so widely the findings bury everything else) and look at the picture
before calling it done. A widget whose brand line wraps at 1.5× and pushes the
title out of the frame passed both the accessibility check and
`wear.layout.no-clipping`.
- **The browser URL** — `https://<host>/ui-builder/<catalogSystemId>/<designId>`
  — is what you hand a person. Always give them this rather than describing the
  design.

## Compare with a reference

A reference is the picture a design is built against — a Figma frame, a
screenshot of a shipped screen, a mock. It is kept **beside** the design, not in
it: no node holds it, no export sees it, the revision does not move. That is
different from an `asset/image` node, and `ui_builder_put_asset` does not attach
one.

### Over MCP

Check `tools/list` for `ui_builder_set_reference` and
`ui_builder_compare_reference`. They need a compose-preview-server release that
carries them and a host that keeps reference overlays; when they are absent,
use the browser route below and say that the MCP lacks them.

1. **Get the picture.** From Figma, use your Figma tools to take a screenshot of
   the frame (the node the user linked) and note its export scale; from a file
   or an attachment, read the bytes. Never invent or redraw a reference.
2. **Ask before uploading.** The reference is stored on the remote host. A
   request to *look at* an attachment is not permission to upload it: say where
   it will be stored and get an explicit yes. Never print its base64.
3. **Attach it:** `ui_builder_set_reference` with `designId`, `imageBase64`,
   `density` (pixels per dp — 2 for a Figma 2x export, 2.625 for a Pixel
   screenshot) and `sourceUrl` (the Figma frame link, kept as provenance). Also
   record the frame with `ui_builder_set_links` (`reference`).
4. **Read the facts** in the reply before changing anything: the picture's size
   in dp, where its density came from, whether it is a `screen`, a `tallScreen`,
   or a `region` (a component crop), and `pixelComparable`. A region is only
   comparable at its `actual` size, and a picture of another shape is compared
   by eye only — say so rather than "fixing" what a misplaced picture shows.
5. **Measure:** `ui_builder_compare_reference` with `differences` reports the
   share of pixels that differ and up to eight regions in dp, each with the
   layer it falls in. Add `nodeIds` for the layers you want to line up: each
   comes back with where it sits in the reference, the `alignment` (move, size,
   font size) and the exact `operations` for `ui_builder_apply`. Matching layers
   needs the native render, which needs the `ui-builder-export` grant **and** a
   host that compiles the pinned catalog. `renderer` defaults to `native`
   whenever `nodeIds` is given, so on a host without one (`NO_NATIVE_CATALOG`;
   preview.coo.ee has none for `m3-catalog` as of 3.121.0) the call fails, and
   with `renderer: "export"` each layer comes back with no operations. There,
   measure with `differences` alone (it uses the PNG export), read the regions
   and their layers, write the alignment yourself, and say that layer matching
   was not available.
6. **Apply what you agree with** through `ui_builder_apply` (quote the current
   `baseRevision`), one layer or a few at a time so collaborators see progress,
   then compare again — a layer that lines up reports `alreadyAligned` — and
   look with `ui_builder_view` (`include: ["reference"]`). Treat
   `confident: false` as a hint to check, not an edit to make; when the words or
   content differ from the mock, ask the person to draw a box round the target
   in the editor (a box mark is the strongest evidence) and compare again.

Report what you changed in dp and sp ("title moved right 12 dp, font size 22 →
28 sp") and what still differs. Do not chase the last pixels of anti-aliasing,
a different font rendering, or a status bar the mock includes.

The CLI spellings are `compose-preview-server design reference <designId>
--attach <picture> [--density <n>] [--source-url <url>]` (or `--clear`) and
`design compare <designId> [--node <id>] [--fit contain|width|actual]`.

### In the browser

Open the design URL and select **Frame, density and reference** in the right
inspector rail. **Import…** a file, paste an image, **Snapshot** the design, or
fetch a link (a Figma frame link works on the desktop app with `FIGMA_TOKEN`;
on the web, copy the frame as PNG in Figma and paste it). The panel shows the
picture's size, density and kind, and the fit (**Fit**, **Fit width**, **Actual
size**) that lines it up. Choose the view that answers the current question:

- **Overlay** for alignment at an adjustable opacity.
- **Difference** to make matching pixels recede and expose mismatches (offered
  only when the picture lands dp for dp).
- **Split** for a movable before/after wipe.
- **Boxes** for layout guides extracted from a compatible SVG.

**Measure → Differences** outlines where the design differs; select a layer and
**Match** to get the same move/size/font-size proposal as the MCP tool, with
**Apply** writing it as one undoable edit. The same panel supports markup,
component pieces, erasing, promotion of captured catalog components, and
**Flatten**. The feature and its storage boundary are documented in
[`UI_BUILDER_REFERENCE_OVERLAY.md`](https://github.com/yschimke/compose-ui-builder/blob/main/docs/design/UI_BUILDER_REFERENCE_OVERLAY.md).

For a UI-builder-shell reference, explicitly account for the top command bar
(undo/redo, Design/Preview, code, share, renderer, new and overflow), both
action rails, the surface/properties bar, zoom/fit controls, and the bottom
revision/node/live status. Do not call the reference complete while those
controls are absent merely because the central canvas resembles the target.

## Working with a person on it

- **You are working as the person who approved your grant.** A design you create
  is **owned by them**, not by your grant — so it outlives the grant and the link
  you send them opens. Designs they already own are open to you, with the
  capabilities they ticked. `list_designs` shows the pair: `ownerActorId` is
  theirs, `requesterAccess.actorId` is yours. Your edits stay attributed to you.
- **Sharing** is per design and owner-only: `ui_builder_design_access` lists who
  can open one, `ui_builder_share_design` adds an actor id
  (`github:<login>`, `operator`, `agent:<fingerprint>`) as `viewer` (read and
  export) or `editor` (also write). Neither role can share it on. `GET
  /agent-access/whoami` tells you your own `actorId` and the
  `onBehalfOfActorId` you are acting for.
- **Comments are a conversation.** `ui_builder_list_comments` reads the threads a
  designer left, `ui_builder_post_comment` replies (pinned to a node, a markup
  stroke, or a point on the frame), `ui_builder_resolve_comment_thread` closes
  one. This is how you answer "why did you put the button there".
- **A design says what it is for.** `ui_builder_get_links` reads the record
  beside a design — the tracker `issue` it was drawn for, the `reference` frame
  in the design tool, the `pr` that implemented it, the chat `thread` it is
  being discussed in, and the `previous` design it continues. You rarely need
  to call it: the same object rides along on `ui_builder_get_design` as
  `links`, so the brief behind a screen arrives on the reply you are already
  reading. Read it before you redesign something — "make the header smaller" is
  a different task when the issue says the header is the complaint.
  `ui_builder_set_links` writes it back, and **replaces the whole record**, so
  send every link you want to keep and not only the one you are changing. All
  five are optional; everything but `previous` is an absolute `http(s)` URL.
  Writing takes the design's own write access, so a design shared with you as a
  viewer is readable and not writable.
- **A comment may leave the editor.** A host can be started with
  `--ui-builder-comment-webhook`, and then a new thread, a reply and a
  resolution are posted to a chat channel with a link back to the thread — the
  author's name, the first 160 characters of what was said, and where it is
  pinned. Reactions and acknowledgements are deliberately silent, so catching up
  on a thread never pages anybody. Write a comment as something a PM or an
  engineer might read in Slack rather than as a note to the designer alone, and
  say what you changed rather than only that you changed something. Your
  comments are marked `authorKind: agent`, so a channel can tell them from a
  person's.
- **Check comments at the edges of every visible step.** Read comments before
  the first edit and after every accepted `apply` or export. Acknowledge or
  answer new feedback before starting the next part, and report the open-thread
  count with the revision. This keeps a comment posted during a long build from
  sitting unseen until the final handoff.
- **Wait instead of polling.** `ui_builder_await_design` blocks until somebody
  else changes the design and returns what changed;
  `ui_builder_await_comments` does the same for the discussion. Both take a
  cursor you quote (`lastSequence` / `sequence`) and answer `timedOut` when
  nothing happens. Before a bounded wait, tell the person what link and revision
  are ready, which feedback you are waiting for, and how long you will wait.
  On timeout, say that no new comments arrived and either continue with the
  stated next step or hand back control; do not silently recurse forever. Reuse
  the same cursor for a later wait. This is cheaper and faster than re-reading
  the design in a loop, and it is what makes you a participant in a session
  rather than a poller.
- **Delegate a background watcher when the agent runtime supports it.** For an
  active collaborative session, give a background task the design id, host,
  current comment `sequence`, and a bounded window (30 minutes is a useful
  default). It should loop on `ui_builder_await_comments` with calls shorter
  than the host's request timeout, reuse the returned cursor, and notify only
  when a new comment arrives, the grant expires, a material error needs action,
  or the window ends. It must not mutate the design or discussion. Tell the
  person when the watcher starts and exactly when it stops, so “background”
  never implies an invisible permanent service. A delegated task belongs to
  the current agent task unless the runtime explicitly provides durable
  automations; it must not promise notification after that task is closed.

## Explore alternatives on branches

When the person wants options ("try a compact and a roomy header"), or you would
otherwise edit over somebody working live, branch rather than copy:

1. **Branch once per idea from the same revision.** Note the parent's current
   revision once, then call `ui_builder_branch_design` with `designId`, that
   `revision` (so an edit landing between calls cannot give the alternatives
   different baselines), a `name` that says what the alternative is, and your
   own `branchId` so a retry is idempotent. A branch is a design with its own id:
   edit it with `ui_builder_apply` exactly as above. Branches of a branch are
   refused.
2. **Show them side by side in one picture.** `ui_builder_compare_branches`
   renders the parent's head and each open branch into one numbered contact
   sheet (a short-lived https link) with what each changes. Post the picture
   and the numbered list; never describe the alternatives from their JSON.
3. **Let the person choose.** `ui_builder_pick_branch` shows a picker or form
   where the host has one. If it returns `ask-in-chat`, post its list and
   picture and wait for their number. Never pick for them, and treat `declined`
   as an answer.
4. **Merge the choice.** `ui_builder_merge_branch` with `dryRun: true` first,
   read the per-command report, then merge. Its open siblings are archived for
   you; `ui_builder_archive_branch` drops one without merging.

## Approval and handoff to code

A design is done when a person approves a revision, not when you stop editing.
The record lives beside the design, so the coding agent can pick it up later
without the chat.

- **Wait for approval instead of asking again.** Tell the person the link and
  revision, then `ui_builder_await_decision` with `designId`, that `revision`
  and the `afterSequence` you last saw (0 the first time). Without `revision`
  a verdict on an older revision would answer the wait. It returns when a
  *person* approves or rejects that revision, or `timedOut` after
  `waitSeconds`. If you edit after asking, the person is looking at a new
  revision: say so and wait on that one. `waitSeconds: 0` is a
  cheap poll for a routine that checks back later. Quote the reply's `sequence`
  next time. Your own `ui_builder_record_decision` is recorded as an agent's
  and does not answer a person's wait; never record an approval on their
  behalf.
- **Link the implementation.** When code lands, `ui_builder_set_implementation`
  with the PR URL, its `status` and the design `revision` it implements. After
  you have rendered the PR's `@Preview`s and compared them with the design, add
  `previewMatch` (`match`, `mismatch` or `unknown`, with an evidence link). It
  replaces the whole record.
- **Start the code side from the design.** In a coding session,
  `ui_builder_implementation_status` returns in one call the revision, its links,
  the implementation PR and whether its previews matched, the latest verdict, and
  the Compose export with its diagnostics. From a PR,
  `ui_builder_find_design_for_pr` finds the designs it implements. Implement the
  approved revision, not whatever the design holds now: if `summary` says the
  revision moved on or was never approved, say so before writing code.

## Keeping a design

A server-homed design remains canonical on its recorded server. The server repo
ships `scripts/ui-builder/design-sync.mjs`, which can make an operations fixture
for a compile check, review artifact, or explicitly approved move to a repo:

```sh
COMPOSE_PREVIEW_UI_BUILDER_TOKEN=… node scripts/ui-builder/design-sync.mjs export my-widget \
  --server https://<host> --out ui-builder/designs/my-widget.json
```

An app checkout keeps those under `ui-builder/designs/` with an `index.json`;
a host started with `--ui-builder-designs ./ui-builder/designs` lists them under
**From the projects** on `/admin/ui-builder`, ready to open again. That fixture
format (`compose-ui-builder-operations/v1-candidate`) is a **different envelope**
from the `DesignMutationV1` operations you send to `apply` — do not copy one into
the other; its `insertNode` puts the parent at the top level, `apply`'s puts it
under `location`.

Exporting this fixture does not move the design's home. Announce the temporary
copy and either apply its result back at the recorded home or discard it before
finishing. Changing the canonical home to the repo is a separate action that
requires the person's explicit approval and updates the recorded home rather
than silently creating two authoritative designs.

## Gotchas

- **A local session is closed until you open it.** `--agent-grants --catalog-mcp
  --agent-grant-capabilities ui-builder-read,ui-builder-write,ui-builder-export`
  is the difference between a working local MCP endpoint and one that 404s or
  refuses every call — see [No host? Run one locally](#no-host-run-one-locally).
- **Capabilities, not scope.** `live` does not include `ui-builder-read`.
- **`list_designs` can legitimately be empty.** It lists what *your actor* can
  see, not what is on the server.
- **A design id must be path-safe** and is chosen by you; creation never
  overwrites, so an id that exists answers "already exists" rather than replacing
  a design.
- **Presence never wakes `await_design`.** Somebody looking at the design, or
  moving their cursor, is deliberately not a change.
- **The tools are absent, not failing, on a box with no builder.** Read
  `tools/list`; `ui_builder_render_native` is likewise absent where the host
  cannot compile.
- **`setModifiers` replaces the whole list** for a node — there is no
  add-one-modifier operation, so send the modifiers you want the node to end up
  with.
- **An `assetKey` has to resolve on the host.** `asset/image` names an asset the
  server holds; on a host with no asset store there is nothing to name, and a
  coloured `layout/box` is the honest stand-in for a photograph in a mockup.
- **The frame's ground comes from `environment.theme`.** A surface's
  `containerColor` colours that surface; going dark is
  `{"type": "updateEnvironment", "changes": [{"type": "setTheme", "value": "dark"}]}`.
