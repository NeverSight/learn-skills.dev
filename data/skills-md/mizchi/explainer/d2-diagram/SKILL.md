---
name: d2-diagram
description: >-
  Draw a software architecture, system, data-model or call-flow diagram as D2 text laid out by TALA (D2's whiteboard-style engine, open source since D2 0.9), look at it in the terminal before anyone opens an image, and check that the picture says what it claims — `d2 --layout=tala x.d2 x.txt` renders the layout as Unicode box drawing, `--ascii-mode standard` as plain ASCII for a README, and `assets/d2-facts.mjs` reads the drawn boxes and arrows back out of the render and holds them to a fact sheet. Loop: write `.d2` → `d2 fmt --check` / `validate` → facts → terminal render → PNG → fix the text. Use when asked for a D2 diagram, an architecture diagram kept as editable text in the repo, a TALA layout, a diagram that shows in a terminal or a code block, or when the repo already has `.d2` files. Not for animations or figures with a moving walk (`explanatory-animation`, `explain-with-anim`).
---

# d2-diagram

Paths below: `<skill>` is this skill's directory and `<skills>` the directory the skills are
installed in (`skills/` in mizchi/explainer, `.claude/skills/` in a project that installed them).

A D2 file is the diagram; the picture is a render of it. The writer's job is the
text — ids, labels, containers, connections — and TALA's job is where the boxes
go and how the lines bend. The terminal render exists so the writer reads the
picture on every round without leaving the shell, and so the diagram can live in
a README code block, a PR comment, or a `--help` text.

```d2
direction: right
web: Web frontend
api: API server
db: PostgreSQL {shape: cylinder}
web -> api: HTTPS
api -> db: SQL
```

```
                                                          .-‾‾‾‾‾‾-.
                                                         │╲-______-╱│
                    HTTPS                        SQL     │          │
┌─────────────┐──────────────▶┌───────────┐─────────────▶│          │
│Web frontend │               │API server │              │PostgreSQL│
│             │               │           │              │          │
└─────────────┘               └───────────┘               ╲-______-╱
```

(`d2 --layout=tala x.d2 x.txt`, verbatim, D2 0.8.1-HEAD.)

This skill is for a diagram whose deliverable is **D2 text**: someone will edit
it later, TALA lays it out, and it renders wherever D2 does. A step-by-step
walk (an algorithm, a request) is not animated: draw the structure once and
number the steps in the prose. To ground the D2 in the code, list the modules
and dependencies from the code first (imports, `package.json`), write them into
the fact sheet, and draw exactly those.

## Invocation

```bash
d2 layout                                   # must list `tala (bundled)`. That, not the version
                                            # string, is the gate: v0.8.1-HEAD already bundles it.

d2 --layout=tala arch.d2 arch.txt && cat arch.txt        # the terminal render (Unicode box drawing)
d2 --layout=tala --ascii-mode standard arch.d2 arch.txt  # plain ASCII (+ - | / < > v) for a README
d2 --layout=tala arch.d2 --stdout-format ascii -         # to stdout, for a pipe or a PR comment
d2 --layout=tala arch.d2 arch.svg                        # the figure for docs
d2 --layout=tala arch.d2 arch.png                        # a raster to LOOK at (see the loop, step 5)

d2 validate arch.d2                         # syntax only; exit 1 with file:line:col
d2 fmt --check arch.d2                      # formatted? exit 1 and names the file, changes nothing
d2 fmt arch.d2                              # ...and this rewrites it in place

node <skill>/assets/d2-facts.mjs arch.d2               # what the picture DRAWS
node <skill>/assets/d2-facts.mjs arch.d2 --expect f.json   # ...held to a sheet
LC_ALL=C.UTF-8 wc -L arch.txt               # the width in columns — the locale matters, see below
```

Install when `d2` is missing — never drive the diagram through an online
playground:

```bash
curl -fsSL https://d2lang.com/install.sh | sh -s --      # the installer; it rejects the obsolete --tala flag
brew install d2                                          # macOS
go install github.com/d2lang/d2@latest                   # Go 1.27+; what to do when the install script gets a 403 through a proxy
```

`D2_LAYOUT=tala` in the environment is the same as the flag. `vars: { d2-config:
{ layout-engine: tala } }` inside the file is honoured for `.svg` / `.png` **and
not for `.txt`** on the build measured (0.8.1-HEAD: the text render fell back to
dagre and came out 163 columns instead of 120), so pass the flag anyway; keep the
config in the file so the next person's SVG gets the same engine. A
`sequence_diagram` is the exception that proves the rule — it lays itself out, so
its text render came out byte-identical with and without the flag.

## Nothing in D2 tells you the picture is wrong

`validate` reads syntax. The renderers draw whatever the file says. There is no
`--expect`, no layout report, and **no error for a reference to an id that is not
in scope — it creates a new shape.** So this is a silently wrong diagram:

```d2
edge:    { cdn; gateway }
cluster: { orders; inventory }
gateway -> orders        # ← two NEW empty boxes at the root; the real ones keep no arrow
```

A writer in this skill's own validation round shipped exactly that: `d2 validate`
0, `d2 fmt` clean, 94 columns, and its log said "can trace all connections". The
render had **four duplicated boxes**, two orphans, and the system's entry call
drawn as a floating pair outside every region
([report](https://github.com/mizchi/vlmkit/blob/main/docs/reports/2026-09-14-d2-diagram-v1.md)).

**Write cross-container connections at the root, with full paths.** That is the
one form that always works and the one every writer in the round that got this
right used:

```d2
edge.gateway -> cluster.orders          # at the root: full path on both ends
cluster: {
  billing -> _.outside.stripe           # from INSIDE: `_` is this container's parent
}
```

`_` is **one level and only valid inside a container**. From inside `cluster`,
`_` is the root, so a shape in a sibling container is `_.outside.stripe` — not
`_.stripe`, which invents a root-level `stripe` (that was the round's fourth
phantom). At the root `_` has no parent to mean: `d2` fails the compile with
`invalid underscore`, which a later writer hit and read as the escape being
broken.

`assets/d2-facts.mjs` is the check D2 does not have. It renders the file and
reads the picture back out of the SVG — d2 writes every shape's and every
connection's fully-qualified id into it — so what it reports is what a reader
sees, not what the source seems to say. No dependencies; copy it next to your
diagrams in another repo.

```bash
node assets/d2-facts.mjs arch.d2               # boxes, containers and their members, labels, edges, columns
node assets/d2-facts.mjs arch.d2 --expect arch.facts.json
node assets/d2-facts.mjs arch.d2 --seeds 4,5,6 # the seed the final render will use, so the width it reports is real
node assets/d2-facts.mjs --from-svg arch.svg --from-txt arch.txt   # read renders that already exist, no d2 run
```

The last form is how the checker is itself gated: `tests/d2/d2-facts.test.mjs` drives
it over renders committed under `tests/d2/fixtures/d2-scenario/` with no `d2` installed,
so the phantom-box, truncation, reversed-edge and width lines each have a test
that fails if they stop firing. It is also the way to check a render somebody
else produced, or a `.svg` in a PR you are reviewing.

It fails on its own, with no sheet, for three defects that are always defects:
**a name drawn twice** (the scoping trap above), a box that overlaps a sibling or
escapes its container, and **a truncated terminal render** — a `top` / `left`
pin can push shapes off the ascii canvas, and `d2` exits 0 on a text file
holding a fragment. One writer's five-table schema passed at "71 columns" with
three of the five tables missing from the render it had just measured, which is
why the box-by-box comparison exists. It warns about a box nothing connects to.
With a sheet it also checks:

```json
{
  "boxes": ["gateway", "orders", "broker"],
  "deps": ["gateway->orders", "orders->broker"],
  "forbidden": ["orders->billing"],
  "containers": { "cluster": ["orders", "inventory"] },
  "order": ["browser->gateway", "gateway->orders"],
  "exhaustive": true,
  "maxColumns": 100,
  "allowOrphans": ["legend"]
}
```

- `deps` are checked **with direction**: a reversed arrow reads `✗ edge
  reversed: the sheet says broker->billing, the picture draws billing->broker`.
- `exhaustive` makes an edge the sheet does not list an error, not a warning.
- `order` reads a sequence diagram's messages back by their y position — the one
  place D2 makes order visible.
- Names match an id's last segment **or its label**, so a sheet says `gateway`
  for a file that wrote `gw: API gateway`.
- It cannot see inside a `sql_table`: a column-level edge
  (`orders.customer_id -> customers.id`) is reported as `orders->customers`.
  Constraint badges are not checked either; count them with
  `grep -o '>FK</text>' arch.svg | wc -l` (`grep -c` counts *lines*, and an SVG
  is one line, so it prints 1 however many badges there are) and read the PNG
  for which row each arrow actually leaves.

Write the sheet from the brief **before** the diagram, the way a test comes
first. It is the only artifact that survives a TALA reflow.

## How a sheet name finds its shape

A name in a sheet is not matched on the id alone; the search widens until
exactly one shape matches:

1. the **last segment of an id** — `orders` finds `cluster.orders`
2. an exact **label** — `gateway` finds `gw: API gateway`
3. a **substring** of an id, or of a label, when exactly one shape matches

Step 3 is generous on purpose and it will surprise you. A box called `pg`
labelled `Postgres orders (authoritative until cutover)` **is** a sheet's
`orders`, so `forbidden: ["checkout->orders"]` fires on an edge into it. That is
not a bug in either the sheet or the figure — they disagree about a name — so
every line that turns on a loose match now says which match it used:

```
✗ forbidden edge drawn: checkout->orders (orders matched no id — it is a
  substring of box pg's label "Postgres orders (authoritative until cutover)")
```

Read that clause before editing anything: with it, the choice is between
scoping the sheet and fixing the figure. Without it, a writer relabelled a
correct box to satisfy the checker
(`tests/d2/fixtures/d2-scenario/v2/label-substring/`).

## Why TALA, and when not

TALA (Terrastruct's AutoLayout Algorithm) is D2's own engine for software
architecture diagrams, open-sourced under MPL-2.0 and bundled with D2 (0.9.0 is
the release the announcement names; the 0.8.1-HEAD build measured here has it
too — ask `d2 layout`, not the version). Where dagre and ELK lay a directed graph
out in layers, TALA arranges boxes the way a whiteboard drawing does —
orthogonal, symmetric where it can be, clustered by container — and it is the
only engine that honours every D2 feature: `direction` per container, `width` /
`height` on containers, `near: <other shape>`, and `top` / `left` to pin a shape
while the engine places the rest.

| The diagram is… | Engine |
|---|---|
| Boxes in containers with connections in several directions (an architecture, a deployment, a data model) | **tala** |
| One flow with a clear direction, many hops (a pipeline, a DAG) | tala with `direction: right`; if it still reads badly, `elk` — the announcement is explicit that TALA does less well on flowing graphs |
| Thirty-plus shapes | Split by container into two files. TALA's runtime is nonlinear in size: 30 nodes took 0.94s here where ELK took 0.05s; layouts that size also read badly whatever the engine |

**Randomness, made reproducible.** TALA tries three seeds (`--tala-seeds`,
default `1,2,3`) and keeps the best complete result, so the same file renders the
same picture twice — measured identical. A label change can still cascade into a
different arrangement, so never describe the geometry in prose ("the box on the
left"); name ids. Two measured caveats before you reach for seeds:

- **A different seed set often changes nothing.** One writer swept twelve seed
  sets over a five-table schema and got the identical 109-column layout every
  time; another moved 113 → 100 columns with `--tala-seeds 4,5,6`. Try it once,
  keep the number you measured, and do not plan on it.
- **Seeds cannot live in the file.** `d2 layout tala` says "Diagram data under
  tala-seeds takes precedence over the command-line flag", but
  `vars.d2-config.tala-seeds` is rejected at compile time. A committed diagram
  whose layout depends on a seed only renders that way if every render passes the
  flag — so write the flag into the script or the Makefile target, or do not rely
  on it.

## Route by task

| Task shape | Write |
|---|---|
| "Draw the architecture / how the services fit" | Containers per area (`cluster: our cluster { orders; inventory }`), connections between children at the **root** (`edge.gateway -> cluster.orders`) or with `_.` from inside. `direction: right` at the root; per-container `direction` on the fullest container is the width lever, see below |
| "Draw the data model / tables" | `shape: sql_table` with `id: int {constraint: primary_key}` and `customer_id: int {constraint: foreign_key}` rows; connect the columns (`orders.customer_id -> customers.id`) |
| "Draw the request / call flow between components" | `shape: sequence_diagram` at the root; actors in first-use order; one message per line with its label. D2 has no return or async arrow and the terminal render drops every style, so the distinction lives in the label — as a **bare marker of four characters or fewer, no punctuation**, at the start or the end (`ret 201 Created`, `order.placed async`), glossed in the prose above the figure. `reserved (ret)` does not survive: the render overwrites the parentheses with line characters and a label that fills the lane leaves the arrow with **no head at all**. A legend inside the diagram is not an option either — `shape: text` renders as an empty box |
| "Draw the classes" | `shape: class` with `+method(): type` / `-field: type` lines |
| "Draw the deployment / network" | Containers for hosts and zones; `shape: cylinder` for stores, `shape: cloud` for external services, `shape: queue` for brokers |
| "We already have a `.d2`" | Edit it; `d2 fmt --check`; render before and after; do not switch its engine or theme without saying so |
| "Put it in the README / a code block / a PR comment" | The `standard` ASCII render inside a fenced block; measure the width as below; keep the `.d2` next to it |
| "It has to be checked against the code" | List the modules and deps from the code (imports, `package.json`) into the sheet first, draw exactly those, then `d2-facts --expect` |

## The loop

```
1. write arch.facts.json                             the boxes, edges and width the brief asks for
2. write arch.d2                                     ids ASCII; the label after the colon is what the reader sees
3. d2 fmt --check arch.d2 && d2 validate arch.d2     syntax; exit 1 names file:line:col
4. node assets/d2-facts.mjs arch.d2 --expect arch.facts.json
                                                     duplicates, missing / reversed / invented edges,
                                                     container members, overlaps, order, width
5. d2 --layout=tala arch.d2 arch.png                 then READ arch.png with your file-reading tool — you can
                                                     look at an image, and this is the only step that shows
                                                     labels, shapes, key badges and which row an arrow leaves.
                                                     Both writers who skipped it reported the same thing:
                                                     "a PNG read would have answered this"
6. d2 --layout=tala arch.d2 arch.txt && cat arch.txt the deliverable, if it is going in a terminal
7. fix the text; go to 3
```

Five rounds at most. Each step answers a different question: 3 is "does it
compile", 4 is "does it say what I meant", 5 is "does it read", 6 is "does it fit
where it is going". A compile error is one line —
`arch.d2:2:9: invalid style keyword: "colour"`, `2:1: connection missing
destination` — fix the line it names.

## Done condition

- `d2 validate` exits 0 and `d2 fmt --check` exits 0.
- `d2 layout` listed `tala (bundled)` and the render used it.
- `d2-facts --expect` exits 0: no duplicate name, no truncated render, every
  listed box and edge drawn with its direction, no forbidden edge, the width
  inside budget — measured with the same `--seeds` the final render will use.
- You read the PNG once, and it is one of the deliverables.
- Every shape and connection in the prose is named by its id, and every id in
  the prose is in the file.
- The `.d2` is committed where the SVG is; the SVG is a build output or is
  committed next to it — never only pasted.

## Width: measure it the way a terminal sees it

```bash
LC_ALL=C.UTF-8 wc -L arch.txt      # 122 — correct, and CJK-aware
wc -L arch.txt                     # 120 in the C locale: an undercount, and 87 vs 111 on a Japanese figure
awk '{if(length($0)>m)m=length($0)}END{print m}' arch.txt   # 338 — BYTES. Never this.
```

`d2-facts.mjs` prints the same number as `columns`, which is the one to quote.
Two writers hit the undercount independently; one spent a round shrinking a
render that was already inside budget.

**The levers are not monotone. Measure after every one.** Measured on two
different diagrams in the same round:

| Lever | Diagram A | Diagram B |
|---|---|---|
| root `direction: right` → `down` | 144 → **145** (worse) | 148 → **109** (the win) |
| shorter labels | 144 → **146** (worse) | 109 → **135** (worse) |
| per-container `direction` on the fullest container | 146 → **113** (the win) | — |
| `--tala-seeds 4,5,6` | 113 → **100** | no change across 12 seed sets |
| `top` / `left` pin on one shape | 113 → **74** | 102 → **75** |

So: set the root `direction`, then the **own `direction` of the container holding
the most boxes** — that is the first thing to try, not the last — and re-measure
after each. Shortening labels is as likely to make it wider, because TALA reflows
the whole picture. `--scale` does not change the text render at all. None of this
applies to a `sequence_diagram`, which lays itself out: there the only lever is
label length, and it moves the width by a column or two in either direction.

Two caveats on the escape hatches:

- **Per-container `direction` is often ignored.** Setting it on two containers
  produced byte-identical renders; on the fullest one it moved 33 columns. TALA
  appears to honour it only where the container's internal flow is ambiguous.
- **`top` / `left` are SVG pixels, not columns**, and both must be set together
  (TALA only). Roughly 11.5px per terminal column on a 100-column figure, but
  every writer who used it found its numbers by trying three to five values.
  Pin the one or two shapes whose place matters, comment why, and expect the pin
  to need re-tuning after the next label change.
- **A pin can truncate the terminal render, and that looks like a win.** One
  writer pinned a table, watched the width fall 113 → 71, and the number was a
  fragment: the pin had pushed shapes off the ascii canvas and three of five
  tables were gone from the text while the SVG had grown. `d2` exits 0 on it.
  `d2-facts` now reports it as an error; if you pin, re-read the render.
- **The budget may be unreachable without a pin.** On five `sql_table`s no
  documented lever got under 100 columns: `direction: down` reached 113, shorter
  labels 127, a wrapping container 121, and only the unsafe pin went lower. When
  that happens, split the diagram by container into two files, or keep the wider
  figure and say in the prose that the terminal version is 113 columns — do not
  buy the number with a pin you have not re-read.

## Reading the terminal render

Measured on 0.8.1-HEAD. Read **structure** here; read **labels and shapes** on
the PNG.

- **Edge labels are written onto the line** and their spaces become line
  characters (`vlmkit check integrity─page─html`, `201─Created`). Keep
  terminal-bound edge labels to one or two words.
- **Every connection style is dropped.** `stroke-dash`, `stroke`, `bold` render
  as a plain line: a writer diffed its styled render against a style-free copy
  and they were **identical**. Dashed-means-async does not survive, so carry the
  distinction in the label.
- **Arrowheads are unreliable on long labels.** A label long enough to fill the
  lane can leave the arrow with no head at all, and `<<` in a label is eaten
  outright. Which character the line eats is not stable either: the same file
  lost a label's parentheses on one round and its full stop on the next
  (`order.placed` → `order─placed`). Probe the spelling you land on, and prefer
  one short word with no punctuation.
- **`shape: text` and `|md …|` blocks render as empty boxes.** A title, a legend
  or a paragraph belongs in the prose around the render, or in a variant of the
  file rendered only to SVG.
- **`sql_table` rows render, their constraint badges do not.** PK / FK markers
  are visible only in the SVG / PNG, and a column-level edge attaches to the
  wrong row in the text view often enough that you cannot read it there.
- **An edge label can land on a box or container border** (`┌────sync call────┐│`),
  which reads as two boxes merged. Where it lands is **positional, not
  length-driven**: a writer whose connection was already at the root both
  shortened and lengthened the label and it stayed on the same border row at the
  same width. The levers that do move it are the ones that reflow the picture —
  the container's `direction`, a different seed — so treat it as a layout outcome
  to check on the PNG, not a label to trim.
- **CJK labels pad every glyph** (`ウ  ェ  ブ`) and misalign the box that holds
  them. Ids stay ASCII always; for a figure that will be read in a terminal keep
  the labels ASCII too and put the Japanese in the surrounding text. The SVG and
  PNG render Japanese correctly.
- **`standard` mode** keeps the same layout with `+ - | / < > v` only — the
  version for a README read on GitHub, where box-drawing glyphs in a code block
  depend on the viewer's font.
- **Icons and images are dropped**; sequence diagrams, `sql_table` and `class`
  shapes render, with their rows.

## Rules the writer keeps

- Ids are ASCII and stable (`api`, not `API server`); the label goes after the
  colon. Abbreviating an id is fine — `d2-facts` matches on the label too — but
  the next editor reads the id first.
- **A cross-container connection is written at the root or with `_.`**, and `_`
  is one level: from inside `cluster`, the root is `_`, so a shape in a sibling
  container is `_.outside.stripe`. Never let an out-of-scope name stand: it
  becomes a new box (see above).
- One root `direction`; a container that must flow the other way sets its own
  (TALA only, and only sometimes honoured).
- Connections read as sentences: `a -> b: verb`. `--` is undirected, `<->` both
  ways. A style on a connection (`{style.stroke-dash: 3}`) is invisible in the
  terminal — if the distinction matters there, put it in the label.
- `vars: { d2-config: { layout-engine: tala } }` at the top of every file, so a
  render without the flag still gets TALA for the SVG.
- No coordinates unless a shape must be pinned; then `top` and `left` together,
  on that shape only, and a comment saying why.

## Deliver

- In a chat: the terminal render in a fenced block (it *is* the picture in a
  terminal), the ids named in the prose, the `.d2` and the PNG / SVG as files
  (`SendUserFile` when available).
- In a PR or issue: the `standard` render in a fenced block, or the SVG committed
  and linked. The `.d2` in the diff is the review target.
- In docs: the `.d2` committed next to the page and the SVG generated by the
  build (`d2 --layout=tala docs/arch.d2 docs/arch.svg` in a script), or the SVG
  committed when the site has no build step.

## Failure modes

- `d2: command not found` → install (above); do not draw it in another tool.
- `d2 layout` does not list `tala` → an old release; upgrade. The installer's
  `--tala` flag no longer exists and is rejected.
- **A box appears twice, or an arrow you wrote is nowhere** → an out-of-scope
  reference created a phantom. `d2-facts` names it; the fix is a full path or
  `_.`, not another arrow.
- The text render came out dagre-shaped and wide though the file says
  `layout-engine: tala` → the `.txt` path ignores the in-file config on some
  builds; pass `--layout=tala`.
- `"tala-seeds" needs a value` / `is not a valid config` → seeds are a flag only.
- `connection missing destination`, `maps must be terminated with }` → the line
  and column are named; usually a trailing `->` or an unclosed brace.
- `invalid style keyword` → D2 spells `color`, `stroke`, `stroke-dash`, `fill`,
  `font-size`, `bold`, `opacity`, `shadow`, `3d`, `multiple`.
- Every round moves the boxes though you changed one label → TALA reflowed. Pin
  the few shapes whose place matters, or accept it and stop describing positions.
- Two boxes look like they touch and you cannot tell → `d2-facts` reports
  sibling overlaps in px²; D2 itself has no collision report.

`assets/vlmkit-workspace.d2` is vlmkit's workspace (mizchi/vlmkit) as a D2 file, and
`assets/vlmkit-workspace.txt` is its TALA terminal render — what a clean round
looks like. The validation round that produced the numbers above is
`tests/d2/fixtures/d2-scenario/` and
[`docs/reports/2026-09-14-d2-diagram-v1.md`](https://github.com/mizchi/vlmkit/blob/main/docs/reports/2026-09-14-d2-diagram-v1.md).
