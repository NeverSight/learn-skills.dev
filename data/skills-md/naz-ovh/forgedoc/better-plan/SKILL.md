---
name: better-plan
description: Write a planning document as ForgeDoc markup — a readable HTML page the reader can answer inside — and build it to one HTML file, with an offline option for self-contained delivery. Use when asked to plan work, propose an approach, write a design doc or an RFC, revise a plan, or collect decisions from a human reviewer.
---

# Better plans with ForgeDoc

## What a plan is for

A plan gets an idea out of your head and into the reader's, then asks them what
you cannot decide alone. Everything in it serves one question the reader keeps
asking: **"I don't understand this yet — what is going on here?"**

ForgeDoc delivers the plan as an HTML page the reader can answer inside. Its
`doc-*` tags — **elements** — are a toolkit: each one is a ready-made way to
show something, cheap to write, styled and themed by the runtime, and wired
into the feedback box the reader pastes back to you. Use them to save tokens,
not as a cage. The runtime supplies design, layout, dark mode, numbering,
anchors and motion. You supply the meaning.

## Pick the form that clears the confusion

For each idea, ask what would make it click for this reader, then use that.
Sometimes it is one plain sentence. Sometimes a table, a picture, a short
animation, something they can click, or a block you design yourself.

- Do not default to one format, and do not aim for a "balance" of formats.
  A plan that is all prose and a plan that is all widgets fail the same way.
- Short text is fine when text is the clearest. Many points need nothing more.
- Avoid long walls of text. If a paragraph keeps growing, the idea probably
  wants a different shape — or a `doc-collapse` for the detail few will read.
- Each element earns its place by explaining something. Remove the ones that
  only decorate.

### When each form helps

A menu, not a mapping. Reach for one when it fits; ignore the rest.

| When the reader needs to… | This often helps |
| --- | --- |
| follow an argument, a reason, a caveat | plain sentences, `<ul>` |
| see something **happen** — a request accepted or refused, data moving between tables, state changing over steps | `doc-walkthrough` |
| follow a short, straight sequence | `doc-flow` |
| see the whole shape of a change at once, then open the parts they care about | `doc-mindmap` |
| weigh two or three shapes side by side | `doc-compare` |
| look up exact values — columns, cookies, mappings | `<table>` in `doc-table` |
| see the order of delivery | `doc-roadmap` (or `doc-timeline` for dates) |
| see which files move | `doc-tree`, or `doc-files` for collapsible groups by area |
| read numbers that matter | `doc-stats` |
| judge risks or ownership on a grid | `doc-matrix` |
| read exact code or a change to it | `doc-code`, `doc-diff` |
| try something, or see an idea no element shows well | `doc-custom` |
| be told something is stuck, and what unsticks it | `doc-blocker` |

**Walkthroughs.** A `doc-walkthrough` is a small animated stage: actors as
cards, and scenes that move a token between them or change one. The reader
presses Play, or steps with arrows and dots. It helps most when something
_moves, branches, fails or changes state_ — the exact things a paragraph makes
the reader simulate in their head. Keep captions to a sentence or two; the
motion carries the meaning. For a sequence that is just "A, then B, then C",
`doc-flow` or a sentence is clearer.

**Mind maps.** A `doc-mindmap` is an overview the reader can open up: a
title card, and `doc-node` cards branching from it, each with a little rich
text, an icon or an image. `expand` sets how many levels start open, and the
reader opens the rest with a click or the arrow keys, pans and zooms, and gets
an indented outline on a phone. It suits a picture of where a change reaches —
the database, the server, the apps, and what moves in each.

**Custom blocks.** When no element explains the idea well, design one inside
`<doc-custom>`: your own HTML, a `<style>` and a `<script type="forgedoc">`.
Styles stay inside the block, the `--doc-*` tokens keep it on theme and in
dark mode, and it takes comments like any other block. Keep it small and
specific — a toggle that shows a constraint passing or failing, a slider, a
little diagram. If you notice you are rebuilding a table or a flow, use the
element instead.

**File paths** can open in the reader's editor: set `files-root` on `doc-page`
(add `files-wsl` for a WSL project) and write paths relative to it in
`doc-file` or the inline `doc-path`. The reader picks their editor in a small
picker.

**Mermaid** (`doc-figure type="mermaid"`) suits a small static picture. Dense
graphs are hard to read at page width; split them, or play them as a
walkthrough when they describe something that happens.

## Look the vocabulary up

`CHEATSHEET.md` beside this file is the whole vocabulary on one page. Read it
before writing markup. When it leaves a question open:

```sh
npx forgedoc search <words>          # which element does X?
npx forgedoc info doc-walkthrough    # attributes, rules and an example
```

An invented tag or a guessed attribute fails the build.

## Elements go where the content is

A question goes right after the thing that raises the doubt — not in a list at
the end. A walkthrough goes where you would otherwise say "picture this". A
blocker goes inside the section it blocks. No required order, no required
sections. Two plans about two problems should not look alike.

```html
<doc-section title="How a request finds its account">
  <p>The vendor below is also staff — the case the old role check got wrong.</p>

  <doc-walkthrough title="One cookie, one surface">
    <doc-actor name="panel" label="Vendor panel" kind="app" tone="cyan"></doc-actor>
    <doc-actor name="vendor-guard" label="authenticateVendor" kind="service"></doc-actor>
    <doc-actor name="admin-guard" label="authenticateAdmin" kind="service" tone="violet"></doc-actor>
    <doc-scene title="A vendor route">
      <doc-move from="panel" to="vendor-guard" token="ub_vendor_session" result="accept"></doc-move>
      <p>The vendor guard reads only the vendor cookie, and finds vendor 42.</p>
    </doc-scene>
    <doc-scene title="Wrong door">
      <doc-move from="panel" to="admin-guard" token="ub_vendor_session" result="reject"></doc-move>
      <doc-change actor="admin-guard" set="401" tone="bad"></doc-change>
      <p>The admin guard never reads it, so it sees no session: 401.</p>
    </doc-scene>
  </doc-walkthrough>

  <doc-choice mode="single" question="Someone who is vendor and admin: one login or two?">
    <doc-option recommended>
      Two logins, one per surface
      <p slot="desc">Matches the tables. Staff sign in twice.</p>
    </doc-option>
    <doc-option>
      One login, linked accounts
      <p slot="desc">Friendlier, but brings back a shared identity.</p>
    </doc-option>
  </doc-choice>
</doc-section>
```

One sentence sets the scene, the walkthrough shows the part that is hard to
picture, and the question sits where the doubt appears. The next section might
be a single table, or two sentences. Copy the judgement, not the shape.

Close every tag explicitly — `<doc-actor …></doc-actor>`, never `<doc-actor/>`.
HTML has no self-closing custom elements, and the build rejects them in a
walkthrough.

## Questions

Ask when the answer changes the work. Mark your suggestion `recommended`, and
give each option its real cost in one line. Decisions already made belong in
the plan as statements, with the reasoning behind them — a `doc-chips` row
under the header is a good home for the settled ones.

You never need a question to invite feedback — the reader can select any
sentence, or press Comment on any card, scene or block.

## The file

Name it `PLAN_<name>.html`, or `DOC_<name>.html` for documentation. Two lines are
required byte for byte: the style in `<head>`, the script last in `<body>`.

```html
<style>/*@DOC_CSS@*/</style>
<script>//@DOC_JS@</script>
```

Everything else sits inside one `<doc-page doc-id="a-unique-slug">`. The `doc-id`
is required — it is the key the reader's answers are stored under. Outside a
`doc-custom` block, write no `<style>`, `<script>`, `class=`, `role=` or
`aria-*`: the runtime owns those.

```sh
npx forgedoc build PLAN_<name>.html
```

**The build rewrites that same file.** One document, one file, for its whole
life. To revise, edit it and build again: the build reads its own output. Never
write a copy, a second file, or a version number into the name — the reader's
link keeps working because the document never moves.

Titles, questions, sections and scenes produce their own headings, numbers,
anchors, option letters, controls and contents entries, so none of those are
yours to type. Themes, offline delivery and keeping past versions are in
`BUILDING.md`.

## Before you hand it over

Read it as the reviewer, top to bottom, and find where they would stall:

1. **Where would they reread?** That spot needs a different form — fewer words,
   a table, a walkthrough, a custom block — whichever clears it.
2. **What is there only to look busy?** An element that explains nothing, or a
   paragraph that repeats a picture, comes out.
3. **Is every open decision a `doc-choice`,** placed where its doubt arises,
   with your recommendation marked?

Spend your effort on understanding. The runtime owns the design.

## When the reader answers

They send a block starting `=== FB v1 ·`. Read `FEEDBACK.md` beside this file
before interpreting it.
