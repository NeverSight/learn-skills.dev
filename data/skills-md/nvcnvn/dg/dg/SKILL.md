---
name: dg
description: Create, edit, check and export diagrams with dg, a diagram-as-code tool with an HCL model, automatic layout and routed arrows, through its command line or MCP tools. Use whenever a project holds dg.hcl or views/*.layout.yaml, whenever the user mentions dg, and whenever they ask for an architecture, C4, infrastructure, network, flowchart, swimlane, entity-relationship, class or state machine diagram and the project doesn't already use another diagram tool.
---

# dg

dg draws diagrams from files. HCL says what exists, layout files say where things sit, and arrows
are routed each time a view is drawn. Every command takes `-C <dir>`, the project directory. If
`dg` is missing, see <https://nvcnvn.github.io/dg/docs/getting-started#command-line>.

dg is for things and how they connect. Where position is data (sequence diagrams, Gantt charts,
timelines, charts, Venn diagrams), say dg doesn't fit and use another tool.

## Workflow

1. `dg vocabulary` lists the kinds, edge kinds, tags and views this project defines, as JSON. Read
   it rather than guessing a kind: packs and the project's `spec.hcl` add their own.
2. Make the change. For a new diagram, write `model.hcl` directly. For an existing one, prefer
   `dg op`: it updates every reference, keeps comments, and refuses a change that would add an
   error, writing nothing.
3. `dg check` validates. It needs no browser, so run it after every change.
4. `dg export --format png --scale 2 --out /tmp/view.png`, then look at the picture. Export reports
   what check can't, such as a label that overflows a pinned node, but neither reports crowded
   labels or hooked arrows: only the picture shows those. It needs Chrome or Chromium.

The MCP server (`dg mcp`) has the same four steps as tools: `vocabulary`, `op`, `check`, `export`.
Its `export` returns the picture as an image.

## Model

```hcl
node "backend" {
  kind  = "group"             # a container; a child's parent must be one
  label = "Backend"
}

node "api" {
  kind   = "service"
  label  = "API"
  parent = node.backend
  tags   = ["critical"]
}

node "orders" {
  kind = "table"              # table and class hold rows
  row "id" {
    type = "uuid"
    key  = "PK"
  }
}

edge "api-orders" {
  from  = node.api
  to    = node.orders.row.id  # also node.x.port.y
  kind  = "async"
  label = "writes"
}
```

The model never holds a color, shape, position or file path, so `color = "red"` is an error. Give
a node a kind or a tag, and style that in `style.hcl`. The label is a bare kind, `tag.<tag>` or
`node.<id>`, never `kind.<kind>`:

```hcl
style "tag.critical" {
  fill       = "#D93025"      # a stroke alone barely shows
  text_color = "#FFFFFF"
}

edge_style "async" {
  stroke_width = 2
}
```

A project without `views.hcl` has one view, `main`, showing everything, and `--view` defaults to
it. `dg op create_view` keeps `main`. A hand-written `views.hcl` doesn't, so declare it there:

```hcl
view "main" {
  include = [all]
}

view "overview" {
  include   = [all]
  collapse  = [node.backend]  # drawn as one box, its edges lifted to it
  direction = "right"         # down (default), right, up or left
}

view "backend" {
  of = node.backend           # drill-down into a container
}
```

## Operations

`dg op --help` lists them all and `dg op <operation> --help` shows one's flags and JSON form.

```sh
dg op rename_id --old api --new gateway --type node
dg op delete_node --id orders
dg op update_view --id overview --direction down
```

`dg op batch --file ops.json` applies a list as one change, all or nothing. Name your IDs so later
operations can refer to them. JSON differs from the flags for `connect`, whose ends are objects
and whose labels sit under `labels`:

```json
[
  {"op": "create_node", "id": "web", "kind": "service", "label": "Web"},
  {"op": "connect", "from": {"node": "web"}, "to": {"node": "orders", "row": "id"},
   "kind": "async", "labels": {"mid": "HTTPS"}}
]
```

`dg op` has no undo. Git is its undo, so commit before a large change.

## Layout

With nothing pinned, dg lays the view out automatically and deterministically, and nothing is
saved. Keep that unless the user asks for a placement or the picture looks wrong. To fix a picture,
try the view's `direction` first, since it keeps everything automatic, then pin.

Pinning is all or nothing in practice. Once a view has one pinned node, every other node leaves the
automatic layout and is placed around it, so a single `move` can scatter the picture and push nodes
to negative coordinates. To adjust a layout:

1. Read `frame` and `rel` of each node from `dg export --format json`.
2. In one batch, `move` every node to its `rel`, with your change applied. `rel` starts inside the
   `frame`'s padding, so it isn't `x` minus the container's `x`; use it as given. Values snap to the
   project's grid (10 by default).
3. Skip nodes marked `ordered_in`: a stack or grid container places them, `move` refuses them, and
   `reorder` sets their order.

Arrows are never stored. To steer one, use `set_edge_hint` (side and via points). People arrange
views by dragging in the VS Code panel or `dg serve`, which write the same layout files.

## More

Read these only when the task needs them, at <https://nvcnvn.github.io/dg/docs/>:

- `reference/language`: packs, kinds, ports, properties, IDs and validation.
- `reference/styles`: style properties, shapes, arrow markers, animation, the generic pack.
- `reference/views`: selectors, overlays, layout files, container policies, decorations.
- `reference/operations`: every operation's flags and JSON.
- `examples`: one worked project per diagram type.
