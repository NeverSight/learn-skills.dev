---
name: justskill-design
description: >-
  Take a product from idea to approved screens to code, and design the pages on
  the way. Use this skill whenever the user describes a product idea — an app,
  site, tool or mini program — or asks to add, change or remove a user-facing
  product feature, even without saying design: it guides a soft, skippable route
  through feature breakdown and confirmation, then page design on a canvas the
  user watches and adjusts, then implementation. Use it whenever the user wants
  to design, mock up, wireframe, redesign or restyle a web page, app screen or
  mobile screen — landing page, dashboard, settings, pricing, onboarding — or
  change spacing, colour, typography or layout, or import a .pen file. Also use
  it for a page editor, a design file, design tokens, or reviewing someone
  else's design. Prefer it over hand-written markup: the file is validated and
  the user can adjust it on a canvas without code. For a concrete edit in an
  existing design, skip the route.
compatibility: Node 18 or newer. No dependencies, no install step, no build.
allowed-tools: Bash(node:*), Read, Write, Edit
metadata:
  version: "3.2.3"
  category: "workflow"
  tags: "design, ui, canvas, html, prototyping, product"
  whenToUse: >-
    Use when the user brings a product idea, asks to add, change or remove a
    user-facing feature, wants pages or screens designed, or wants to review,
    restyle or adjust an existing design on the canvas.
---

# justSkill

You write one HTML file with inline CSS. It is the design. This skill checks it,
lets you edit it one change at a time, and gives the user a canvas to drag.

You are also the product designer. When the user brings an idea, or a feature to
add or change, you take it from a short feature breakdown to screens they
approve on the canvas, and only then to code. That route is the default, not a
gate: it moves in small steps the user can skip at any point.

Nothing installs, nothing logs in, nothing runs between sessions. Every command
is `node design.mjs <verb>`.

## From an idea to a product

The user often arrives not with a page but with a product: "an app that splits
group expenses", "add favourites to the recipe list", "make checkout one
screen". Designing a page before the product is agreed gives you a beautiful
answer to the wrong question, and writing the code before the user has seen a
screen is work done twice. So when the request is product-shaped, lead this
route. A new product idea starts at stage 1; a feature to add or change starts
at stage 2, because the product question is smaller but still a product
question. A bug fix, a code task, or a question with no screens in it is not
this route: do the work, and do not start the route around it.

| # | Stage | What you do | Done when |
|---|---|---|---|
| 1 | Idea | Restate the product in one sentence, and who it is for. Ask at most the two or three questions that change the screens. | The user recognises the idea in your sentence. |
| 2 | Feature breakdown | Propose the smallest first version: the core loop, one to five screens with a job each, the empty, loading and error states they need, the data each shows, and what is deliberately out. | The breakdown is short enough to read in one message. |
| 3 | Feature confirmation | Ask for a clear yes, and what is missing or must-have. Fold the answer back into the breakdown. | The user confirms the scope, or tells you to decide. |
| 4 | Design takeover | Say you are taking over the screens, and propose the page list and one visual direction. Create the design file and its tokens — or open the existing file when the product already has one. | The page list and the direction are stated. |
| 5 | Design first | State the order once — in the same message as the feature confirmation is fine: screens first, your approval, then code. | The user agrees, or has already given you the order. |
| 6 | Canvas | Open the canvas: if a `justskill_canvas` tool is available, call it with the design file and never start a server yourself. Otherwise start `serve` in the background and give the user the URL. Then design page by page; every `add` and `set` appears in the open canvas as you go. | The first screen is on the canvas. |
| 7 | UI adjustment | Teach the handshake once: select an element, press `⌘C`, paste the copied pointer back with the change. Apply it with `set`, `move`, `add`, `remove` or `tokens`. | The user stops asking for changes. |
| 8 | Page sign-off | Run `validate`, walk the checklist — every planned screen, its states, the copy, the images, the tokens — and ask for approval. | The user approves the screens. |
| 9 | Code | Treat the validated file as the spec, then implement the screens in the user's stack. | The running product matches the approved screens. |

This route is soft. It is the default because rebuilding a project twice costs
more than asking twice, not because the user must walk it:

- **Begin, do not ask to begin.** Do not open with "shall we do product design
  first?". Do stages 1 and 2, then end with one confirmation, so a user who
  wanted something else can redirect in one message.
- **Every stage is skippable.** "Just do it", "I'll tell you what I want",
  "write the code now": do that instead, and do not re-argue the route later.
- **Ask about the product, decide the design.** Who the user is, what "done"
  means, and what must be in the first version are the user's answers. Colour,
  spacing and layout are yours; one direction is enough, and a direction the
  user already stated is not offered back as a question.
- **One short message of questions.** A form of eight questions is not a
  conversation; two or three at stage 1 is the ceiling, and a confirmation
  already given is not asked again.
- **Scale the ritual to the risk.** A typo needs no breakdown; a new state or
  flow does. A request that already names the screen and its content ("add a
  pricing row to this page") is an edit: make it directly, with no route.

The per-stage playbook — the questions worth asking, the breakdown template,
the canvas handshake, the handoff to code, and how to stay soft under pressure
— is in `references/product-flow.md`. Read it when this route is in play.

## The one rule

**The design file is the truth. Write it, do not rewrite it.**

- Write the file with `Write`. Give every element a `data-id` and a `data-type`.
- `format` rewrites a file into canonical form. Use it when a file came from
  somewhere else; do not use it to change a design.
- Change it with `set`, `add`, `remove`, `move`, `rename`. Never rewrite the whole
  file to change one value: an op is one undo step, and a rewrite is an afternoon
  of lost work for the user who has the canvas open.
- Run `validate` before you hand anything back.

If the user has the canvas open, you are not the only writer. `set` and friends
re-read the file first, so they never clobber the user's drag. A full-file
`Write` does.

## The file

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Landing</title>
  <meta name="design-schema" content="3.0">
  <style>:root{ --color-ink:#111827; --space-md:16px }</style>
  <style>section[data-type="page"]{ margin:0 0 24px }</style>
</head>
<body>
  <section data-id="home" data-type="page" data-name="Home" data-canvas="0,0" style="width:390px;height:844px">
    <div data-id="home__root" data-type="frame" style="display:flex;flex-direction:column;gap:16px;padding:24px">
      <p data-id="home__title" data-type="text" style="font-size:32px;font-weight:700;color:var(--color-ink)">你好</p>
    </div>
  </section>
</body>
</html>
```

Three things to notice, because they are the ones that get refused:

1. **Every element carries `data-id` and `data-type`.** `data-id` is unique in
   the whole file. `data-type` must match the tag.
2. **Exactly two `<style>` blocks, both in `<head>`:** the token block (`:root`)
   and the page-frame block. Everything else is inline in a `style` attribute.
3. **One file holds many pages.** A page is `<section data-type="page">`.

Run `node design.mjs new design.html --name home` for a starting file that is
already correct, and `node design.mjs show design.html home__title` to read one
element back.

## The command loop

```sh
# 1. Start from a valid file, or read what is there.
node design.mjs new design.html --name home --title "Landing"
node design.mjs ls design.html --pages
node design.mjs show design.html home__root

# 2. Add content. The fragment is plain HTML: the model's own language.
node design.mjs add design.html --html-file /tmp/card.html --in home__root

# 3. Change one thing at a time.
node design.mjs set design.html home__title --style 'font-size:40px;color:#111827'
node design.mjs set design.html home__title --text "Ship faster"
node design.mjs move design.html home__card --after home__title
node design.mjs remove design.html home__notice
node design.mjs tokens design.html ls
node design.mjs tokens design.html set color.accent '#7c3aed'
node design.mjs tokens design.html rm space.xxl

# 4. Check. Always.
node design.mjs validate design.html --json
node design.mjs format design.html --check    # is the file in canonical form?
node design.mjs migrate design.html           # only if validate asks for it

# 5. Hand over deliverables, or let the user drag.
node design.mjs export design.html --all -o dist          # HTML, one file per page
node design.mjs export design.html --format svg -o page.svg
node design.mjs export design.html --format png --scale 2 -o page.png
node design.mjs serve design.html
```

`add` reads a fragment from `--html-file` or `--html -` (stdin). Prefer a file
or stdin: a fragment inside shell single quotes breaks on the first apostrophe.

### Images

When a page has a place for a photograph — a hero, a card, a gallery, an avatar —
and the user has not supplied an image, fill it from `references/images.md`:
verified Unsplash URLs, grouped by what the photo shows. Choose by subject — a
hero wants a wide landscape, an avatar a face — and write the URL as it appears
there. `alt` says what a person would see; the credit goes in `data-credit`,
which never renders.

The user's own image always wins: a URL, a file, or an image inside the `.pen` is
never replaced. If no catalogue photo fits, a solid colour or a gradient scrim is
the honest placeholder — never a made-up URL, never a local path that does not
exist. The catalogue is hotlinked, so a design renders its photos only with a
connection.

### Tokens

A design token is the one thing in the file that is not an element, so no other
verb can reach it. Changing a brand color is **one op**:

```sh
node design.mjs tokens design.html set color.accent '#7c3aed'
```

- The name is `<group>.<name>`, or the file's own `--group-name` after a `--`:
  `tokens design.html set -- --color-accent '#7c3aed'`.
- The seven groups are `color`, `font`, `space`, `radius`, `size`, `shadow`,
  `border`. There is no eighth: `surface.warm` is refused, and so is a token
  file that already says `--surface-warm`.
- `space`, `radius` and `size` carry a unit. `set space.md 16` writes `16px` and
  the receipt says so; a value that is not a length is refused.
- A color is normalized to hex, so `red` becomes `#ff0000` in the file.
- A token may reference a token (`var(--color-ink)`). A cycle is refused.
- Never rewrite the file to change a token. That is the one thing this workflow
  exists to prevent, and the user may have the canvas open.

## Reading a receipt

Every write prints what it did. You cannot see the file, so read this:

```
added:      home__cta, home__cta-label  (2 elements)
normalized: #fff → #ffffff
normalized: 12px 12px 12px 12px → 12px
dropped:    cursor:pointer — The format describes appearance, not interaction. A cursor is behavior.
applied 1 op, revision a161db2c (0 errors, 0 warnings)
```

- `normalized` is not an error. It is the canonical form doing its job, and the
  file now holds the value on the right of the arrow.
- `dropped` means the file does **not** hold that declaration. If it mattered,
  write it again the way the message says.
- Nothing is ever dropped in silence. If a declaration is not in the file, it is
  in this receipt.

## Reading a refusal

```
REFUSED  display:grid — grid is not a value of display.
  Accepted: flex | block | none
design.html was not changed.
```

A refusal means the file is byte-identical to what it was. Read the hint: it
always names what to write instead. The common ones:

| Refusal | What to write instead |
|---|---|
| a one-sided `margin`, such as `margin-top` | the shorthand: `margin: 0 8px 0 0` |
| `display:grid` | `display:flex` with `flex:1` on the children |
| `position:fixed` | `position:absolute` with `left` and `top` |
| a missing `alt` | `alt=""` for a decorative image. Missing is not the same as empty |
| a duplicate `data-id` | the hint names a free id, such as `home__a-2` |
| `transform: translateX(-50%)` | `transform: rotate(<deg>)` only; centre with `left` |

Not refused, but reported: `cursor` and `animation` are outside the format's
property table, so the write goes through and the receipt lists them under
`dropped`. A `transform` is in the table, but only as `rotate(<deg>)` — a
`translate()` or `scale()` is a refusal, not a drop. And `#fff` or `rgba(...)` is not a refusal either — the file
takes it and writes the canonical hex, and the receipt calls that `normalized`
(see the receipt above).

## What the format is, and is not

Supported: flexbox layout, absolute positioning, a fixed set of 47 CSS
properties, images, inline SVG icons, design tokens, and text in one run per text
element.

Not supported, and refused by name rather than ignored: grid, `position:fixed`,
transform functions other than `rotate()`, rotation about a point other than the
element's centre, animation, responsive breakpoints, rich text inside one text
element, and any property outside the table.

The full property list, with the accepted values for each, is in
`references/styling.md`. The element contract is in `references/schema.md`.
Read one of them before writing a big fragment; they are short, and they prevent
most refusals.

## The canvas

```sh
node design.mjs serve design.html
```

In DeepSeek Harness with the JustSkill Design plugin, the canvas is the session's
right-sidebar **Canvas** tab. Call the `justskill_canvas` tool with the design file
instead of running `serve`; the plugin opens or focuses the tab.

Prints a URL and opens it. The service stays in the foreground for as long as the
canvas is open, so start it as a background process when you want to keep
designing with the canvas up, and read the URL it prints. The canvas follows the
file: every `add` and `set` appears in the user's tab as you go, which is what
makes a design appear gradually instead of arriving finished. The user drags;
changes go through the same funnel as your commands, so a drag cannot write
something `validate` would refuse. If a drag is refused, the canvas shows what it
would have introduced. Clicking the empty canvas clears the selection; dragging it
pans.

Picking is by rungs, not by depth: hovering outlines the container the canvas is
standing on (solid) and that container's direct children (dashed). A click
selects that container — never the deepest element under the pointer — so a
person selects a card without landing on the word in it, and a drag that follows
moves the card. A double-click steps into the dashed box under the pointer, one
rung deeper. Escape walks back up a rung.

Picking one element and pressing `⌘C` copies a pointer to it, not the design:
`Use justSkill tools. Current file <uri>. Page id: <page>. Selected node ids:
<id>`, confirmed by a toast. (`Page id:` appears only when the selection is not
itself a page.) A user who pastes that into the chat is pointing at one node in
this file — read it with `show`, then change it. This is the normal way a user
asks for a small adjustment, so tell them the shortcut when the canvas opens.

The canvas has three columns: a layer tree (every page, its elements nested,
opening fully collapsed, with expand-all and collapse-all in the header — picking
an element on the canvas opens the tree down to it and selects that row), the
design, and the selected element's properties in sections. The right panel only ever shows properties the element already has —
it cannot add a declaration the file does not carry, so use `set` for that. Either
panel folds away with `⌘\` / `⇧⌘\` or the button on the canvas edge, and either
edge drags to resize; that state lives in the browser, never in the file.

Close the tab and the service exits. The user can also `set` from the command
line while the canvas is open: both writers re-read the file first.

## Rules that save you a round trip

1. **Run `validate` when you are unsure.** It is faster than guessing, and it
   tells you the exact offset and the exact fix.
2. **Never edit `data-id` with `set`.** It is refused, because an id is an
   address rather than a property. Use `node design.mjs rename design.html card
   product`, which is the one verb that changes what an element is called.
3. **Do not add a `<style>` block** for a one-off value. Only the two allowed
   blocks are read; a third is an error.
4. **Do not write a one-sided `margin`.** Spacing is `gap` and `padding`.
   `margin` itself is allowed, but only the shorthand: a one-sided `margin-top`
   and friends are refused, because they are a second spelling of the same
   intent. Offset an element with `margin: 0 8px 0 0`, never `margin-right`.
5. **Prefer tokens.** If `:root` has `--color-ink`, use `var(--color-ink)`
   instead of a literal. The user can then restyle the whole design in one edit.
6. **Small edits, in order.** Three `set` commands beat one rewrite, and each
   one is a step the user can undo.

## Deliverables, and which need a browser

| `--format` | Needs | Notes |
|---|---|---|
| `html` (default) | nothing | One page, or `--all` for a site. Self-contained. |
| `svg` | nothing | Wraps the page in `<foreignObject>`. A browser draws it; Figma, Illustrator and Sketch show an empty rectangle. |
| `png` `jpeg` `webp` | a Chrome-family browser, or the canvas | `--scale 1..3`, `--size WxH` |

The image formats find a browser already on the machine — no download, no
bundled Chromium. When there is none the export **fails** and names three ways
forward: install Chrome, Chromium or Edge, leave the canvas open, or use
`--format svg`. It never quietly writes a different format, because a different
format is a different deliverable.

Before any image export, make sure the fonts are declared. `export` adds the
stylesheet links itself from the families the page uses, and the browser waits
for them; a screenshot taken before a web font arrives is captured in the
fallback family, where the text wraps at different words and everything below it
moves.

The HTML deliverable takes the page's own `background-color` onto `<body>`. A
page covers its own box and nothing more, so a viewport taller than the page
shows what is behind it: left white, that is a colour the design never chose. A
page that states no colour, or states `transparent`, keeps a plain document.

## Working with a `.pen` file

```sh
node design.mjs import pen design.pen -o design.html
```

One direction only: pen in, design file out. Every run prints a ledger:

```
26 pages · 2197 elements · 239 references inlined · 140 with overrides · lost: perCornerRadius×1
```

`lost` names what this format has no spelling for. Read it and tell the user,
rather than letting them find out on the review screen. `--report r.json` writes
the whole ledger.

Four things the reader translates rather than copies, because the format has no
spelling for pen's version of them:

- **A glyph is measured.** A `path` node's outline is drawn on its own grid, and
  that grid becomes the icon's `viewBox` — pen's own export writes
  `viewBox="0 0 14 14"` on a 366×366 arrow. An outline whose box cannot be
  measured keeps the node's box, which is what every glyph in the reference file
  happens to have anyway.
- **A stroked outline is drawn as a stroke**, on the `<path>`, with
  `vector-effect: non-scaling-stroke` so the width stays the width pen drew.
  It is not a `border` on the `<svg>` — that is a ring around a box, not a
  drawing.
- **A rotation is baked into the outline** for a `path` node (the ledger counts
  `bakedRotation`): a path is an opaque drawing with no box to turn, and pen turns
  an element about its top-left corner while this format turns it about its
  centre. Any other rotated node is drawn upright and named in `lost.rotation`,
  because reproducing pen's origin would need a `transform-origin` the format does
  not have.
- **A line break the author placed survives** as `white-space: pre-line`. Written
  as a literal newline it is a space, and the line then wraps wherever the font
  puts it.

The ledger also counts what it rewrote: `themedVariables` (a themeable variable
takes the document's default theme, which is the entry with no `theme` of its
own), `hardBreaks`, `pathAsGeometry`, `bakedRotation`. A variable that cannot be
reduced to one value is left out of the token block and counted as
`lost.unresolvedVariable` — never written as the string `[object Object]`, which
is a value that validates and means nothing.

**A reference is inlined, because this format has no reference.** pen stores a
`ref` node and the master it points at; the reader copies the master's subtree in
where the reference stood. The copy's root keeps the reference's own id and
everything under it is renumbered as `<reference-id>__<its own id>`, which is why
an imported file has 239 more subtrees in it than the `.pen` had nodes. Four
things follow, and they are the ones to tell the user:

- Editing a copy edits that copy alone. The master is a separate element now, so
  a change meant for every card has to be made on each one — or on the `.pen`,
  which is where the sharing lives.
- `descendants` patches are applied during the import: the text, the size, the
  swapped glyph are all in the file, and nothing applies them later.
- A reference that names nothing is refused (`pen/unresolved-ref`), as is one
  inside a loop (`pen/ref-cycle`) or nested more than 16 deep (`pen/ref-depth`).
- Children on a reference node are not part of the master's subtree, so they are
  counted in `lost.refChildren` and not written.

## What the skill needs at run time

The skill runs from `SKILL.md`, `references/`, `design.mjs`, `lib/` and
`canvas/` — about 1 MB. The repository also carries media that no command reads:

| Media only | What it is | Size |
|---|---|---|
| `docs/justskill-demo.gif`, `docs/justskill-demo.mp4` | the README demo (English, 30s) | ~4.6 MB |
| `docs/justskill-demo-zh.gif`, `docs/justskill-demo-zh.mp4` | the same demo in Chinese, for the Chinese README | ~4.6 MB |
| `docs/*.png` | the screenshots, including the case wall | ~1 MB |

If the skill was copied into the skills directory (not symlinked to a checkout),
the user can remove those and free about 10 MB; nothing in `validate`, `set`,
`serve` or `export` changes, and every other file is text:

```sh
rm -rf docs/*.gif docs/*.mp4 docs/*.png
```

Ask before removing anything, and never prune a symlinked checkout — that is
the user's repository. Everything else stays: the docs, examples, tests and
READMEs are text, small, and worth reading. Keep `LICENSE` and `package.json`.
