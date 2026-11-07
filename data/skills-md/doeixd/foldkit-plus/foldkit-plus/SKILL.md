---
name: foldkit-plus
description: Explains Foldkit Plus packages (foldkit-surface, foldkit-remote, -server, -drizzle, foldkit-sync, foldkit-durable, foldkit-mirror, foldkit-site, foldkit-ssr, foldkit-agent and adapters, foldkit-mixins and -ui, foldkit-react, foldkit-bundle, foldkit-primitives, foldkit-entity, foldkit-guard, foldkit-auth, foldkit-form, foldkit-crud, foldkit-cms, foldkit-data-grid, foldkit-media, foldkit-richtext, foldkit-composition), which owns which state, basic use. Use when starting a new Foldkit app, writing or reviewing one with a foldkit-* package, picking one for server data, live lists, offline writes or sync, URL or storage state, server rendering, AI agent tools, view styling, reusable Submodels, domain entities, authorization, Yielded Auth, forms, a data grid, a CMS, rich text, images, or when the user names Foldkit Plus, Surface, Projection, Remote, Data.query, Sync, Mirror, Site.target, Agent.expose, Mixins, Bundle, Entity.select, Guards.declare, Form.make, Crud.editor, DataGrid.make, or Cms.content.
license: MIT
metadata:
  version: '0.38.0'
  repository: https://github.com/doeixd/foldkit-plus
---

# Foldkit Plus

Foldkit Plus is a set of packages that extend a [Foldkit](https://foldkit.dev/)
application to agents, servers, other devices, the URL, and design systems
**without adding a second place to keep state**. The application stays one state
machine: a Schema-typed **Model**, a **Message** union, and one pure **`update`**.

Every package keeps that rule: an agent sends only Messages `update` handles;
server data and replicas' edits are reduced by `update`; the URL and storage
mirror a slice of the Model, never own it; views are extended from outside.

Targets Foldkit `0.170.x` and Effect 4.1, tested on `effect@4.1.1`. APIs are
`0.x` and may break between minors. Two whole apps show the packages together:
[`examples/chirp`](https://github.com/doeixd/foldkit-plus/tree/main/examples/chirp), a Twitter clone with one file per package, and
[`examples/reference`](https://github.com/doeixd/foldkit-plus/tree/main/examples/reference), the recommended stack on one Worker over D1.

## Pick the package by who owns the data

| The state or job | Owner | Package | Reference |
| --- | --- | --- | --- |
| What a feature may observe and which Messages it may cause | the application | `foldkit-surface` | [surface.md](references/surface.md) |
| Facts a server owns: entities, queries, live rows and lists, writes (queued across reloads with `durable`) | the server | `foldkit-remote` (+ `-server`, `-drizzle`; live reads, the outbox and persistence from entries of their own, which install what they need on the domain) | [remote.md](references/remote.md) |
| Client-authored edits that must survive offline and converge across devices | the durable log | `foldkit-sync` + `foldkit-durable` | [sync.md](references/sync.md) |
| A filter in the URL, a draft or preference remembered on a device, a cart a server renders from a cookie | the local Model | `foldkit-mirror` | [mirror.md](references/mirror.md) |
| Where the application is: route nodes in a hierarchy, typed targets, titles, history intent | the tree, as data; the route value stays in the local Model | `foldkit-site` (early) | [site.md](references/site.md) |
| What an AI agent may see and do, over MCP, WebMCP, A2A, or Agent Native | the application | `foldkit-agent` + one adapter | [agent.md](references/agent.md) |
| Restyling or adding behaviour to views, including `@foldkit/ui`; ready components (`Picker`, a window-scrolled `WindowList`) | the view contract; a component's state is the parent Model's | `foldkit-mixins` (+ `-surface`, `-ui`) | [mixins.md](references/mixins.md) |
| A reusable Submodel placed several times or per key, with every part wired | the parent Model | `foldkit-bundle` (+ `-surface`) | [bundle.md](references/bundle.md) |
| Responsive images (widths, `srcset`, formats, placeholders) and icons as data | the image's source; variants are a cache | `foldkit-media` (+ `Image`, `Icon` in `foldkit-mixins-ui`; early) | [media.md](references/media.md) |
| A media query, presence, timer, pagination, undo history, socket, resize, clipboard, or a virtual list's measured rows | the parent Model | `foldkit-primitives` | [primitives.md](references/primitives.md) |
| A React component in a Foldkit view, a Foldkit program in a React app, or views compiled to TSX | the Model / the embedded program | `foldkit-react` (+ `-codegen`) | [react.md](references/react.md) |
| Typed facts a package attaches to another package's declaration (package authors only) | the key's package | `foldkit-metadata` (re-exported by `foldkit-surface`) | [surface.md](references/surface.md) |
| A domain entity's fields, relations and derived members, its invariants, and writes declared as data | the domain declaration; the server's writer enforces it where it commits | `foldkit-entity` | [entity.md](references/entity.md) |
| Who may do what, on reads, writes, Sync edits, agents and uploads | the domain declaration, decided on the server; the client's `may` is only a hint | `foldkit-guard` (`/server`, `/drizzle`, `/sync`, `/agent`) | [guard.md](references/guard.md) |
| Who is signed in: a Yielded Auth session as the principal a Remote or Sync host answers as | Yielded Auth's session; the principal is the application's | `foldkit-auth` (+ `/server`; early) | [auth.md](references/auth.md) |
| A form: drafts, validation, and a decoded value handed to the parent | the parent Model | `foldkit-form` (+ `foldkit-mixins-form` to draw it, `foldkit-form-recipes` for dates, money, addresses) | [form.md](references/form.md) |
| An edit or create screen, or a list over a query | Remote and the form; the editor only joins them | `foldkit-crud` (+ `foldkit-mixins-crud`) | [crud.md](references/crud.md) |
| An interactive data grid over rows the application supplies | the grid owns geometry and interaction; the application owns the rows | `foldkit-data-grid` (+ `foldkit-mixins-data-grid`; experimental) | [data-grid.md](references/data-grid.md) |
| Drafts, revisions, a schedule, and what a visitor may see | the application's tables; a draft is kept beside the row | `foldkit-cms` + `foldkit-cms-drizzle` | [cms.md](references/cms.md) |
| What crosses from a server render to the browser, instead of rerunning `init` | the application, in a resume plan | `foldkit-ssr` (early) | [ssr.md](references/ssr.md) |
| What a page is: Blocks in Regions, stored as a Document checked against a Catalog; editing it | the Document, as a stored field; the Builder, as one form key | `foldkit-composition` + `foldkit-builder` (+ `foldkit-mixins-builder`; experimental) | [composition.md](references/composition.md) |
| A rich-text document and its commands; the `contenteditable` island, editor chrome, Markdown, code highlighting | the local Model; the DOM adapter only edits the island; tokens are derived | `foldkit-richtext` (+ `-dom`, `foldkit-mixins-richtext`, `-markdown`, `-code`, `-code-shiki`; early) | [richtext.md](references/richtext.md) |
| Every package above in one install, each under a subpath, and a project-specific setup guide | nothing: it re-exports the packages | `foldkit-plus` | this file |
| The route, a selection, a transient error | the local Model (topology in `foldkit-site`) | none: plain Foldkit | — |

Remote and Sync both keep writes across a reload: Remote's `durable` outbox
holds a write until the server judges it, and the answer is the truth; Sync's
log holds client-authored edits every replica replays in the log's order.

Read only the reference for the package at hand; its first line names the
versions it was checked against. For one symbol or topic in the installed
release, `npx foldkit-plus docs Data.preload` (or `"optimistic delete"`) prints
the best README sections with the declaration; `docs --list remote`, an outline.
An application's `AGENTS.md` takes the block in [agents-md.md](references/agents-md.md).

## How they connect

```text
Foldkit app (Model · Message · update)
  └─ foldkit-surface: Projection, Surface, MessageSet, Module (Metadata from foldkit-metadata)
       ├─ foldkit-agent ─ webmcp · mcp · a2a · native
       ├─ foldkit-remote ─ foldkit-remote-server ─ foldkit-remote-drizzle
       ├─ foldkit-sync ─ foldkit-durable (server journal)
       │    └─ foldkit-sync/remote: edits to server rows (foldkit-sync/entity) drawn as foldkit-remote overlays
       └─ foldkit-mirror · foldkit-site · foldkit-mixins-surface
foldkit-mixins, foldkit-bundle (standalone) ─ their -surface packages join Surface; -ui, -form, -crud draw the others
foldkit-entity (standalone) ─ the domain, read by remote, remote-drizzle, form, crud and cms
foldkit-guard ─ rules over foldkit-entity, enforced by its subpaths in remote-server, -drizzle, sync and agent
foldkit-auth ─ the Yielded Auth session remote-server's and sync's hosts resolve as the principal
foldkit-crud, foldkit-cms (+ -drizzle) ─ join form, remote and entity: editors, drafts beside the row
```

`foldkit-surface` is the shared seam: most packages consume a Projection (what
to read) and a Message subset (what may happen).

## The one-screen example: Surface, where almost every integration starts

```ts
import { Schema } from 'effect'
import { defineMessageUnion } from 'foldkit/message'
import { modifyFields } from 'foldkit/struct'
import { Surface } from 'foldkit-surface'

const Todo = Schema.Struct({ id: Schema.String, title: Schema.String })
const Model = Schema.Struct({ todos: Schema.Array(Todo), filter: Schema.String })
const Message = defineMessageUnion({
  CreatedTodo: { id: Schema.String, title: Schema.String },
  ChangedFilter: { filter: Schema.String },
})

// Still the ordinary application: one Model, one Message union, one update.
const App = Surface.application({
  Model,
  Message,
  initial: { todos: [], filter: 'all' },
  update: (model, message) =>
    Message.match(message, {
      CreatedTodo: ({ id, title }) => ({
        model: modifyFields(model, { todos: todos => [...todos, { id, title }] }),
      }),
      ChangedFilter: ({ filter }) => ({ model: modifyFields(model, { filter: () => filter }) }),
    }),
})

// A named boundary: what this feature reads and the Messages it may send.
const TodoList = App.surface('TodoList', {
  model: ({ model }) => ({ todos: model.todos }),
  messages: [Message.CreatedTodo],
})
```

From here: `Sync.forApplication(App)`, `Agent.forApplication(App)`, `Remote.make({ model:
App.model.<field>, … })`, `Mirror.url(App, …)`, and `SurfaceView.define(TodoList, …)`.

## Rules that apply to every package

- **One owner per datum.** Never keep a fact in the Model and in a package-side
  cache, a URL store, or a second reducer. Pick the owner from the table.
- **Rendering performs no I/O.** Fetching, syncing, and mirroring run in
  Commands and Subscriptions derived from the Model.
- **Join integrations through one wiring list.** `Page.assemble` takes placements
  and wirings (`Data.wiring(…)`, `….wiring('UrlChanged')`, `….wiring()`); routing,
  startup Commands, Subscriptions and the Module derive from it (`bundle.md`).
- **Install** with `npx --legacy-peer-deps foldkit-plus setup`, which prints the
  steps for its project: Effect pins at 4.1.1, or a later 4.1 patch an npm
  lockfile already holds (Foldkit takes `~4.1.0`), the `add` command, a `.gitattributes`. With `foldkit-plus`, import each
  package through its subpath (`foldkit-plus/remote-server`); the snippets
  name each package itself, as installed alone. Adapters with a library of their own
  (`foldkit-auth`, `foldkit-react`, the Drizzle packages, `foldkit-mixins-ui`,
  `-richtext-code-shiki`, `-agent-native`) go beside it. `foldkit-durable`
  needs Node >= 22.
- **A new application** starts with the user, not code: brief, look, domain
  rounds, then an agreed plan. Follow [greenfield.md](references/greenfield.md).

## More

- Repository and guides: https://github.com/doeixd/foldkit-plus
- Examples, each with a pinned transcript: https://github.com/doeixd/foldkit-plus/tree/main/examples
- How failures work across the packages (who owns each, what the reader sees, `Diagnostics`): https://github.com/doeixd/foldkit-plus/blob/main/docs/errors.md
- Versions and publish matrix: https://github.com/doeixd/foldkit-plus/blob/main/docs/releases.md
