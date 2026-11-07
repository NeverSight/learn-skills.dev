---
name: glyph-kit
description: Draws product-design figures and one-page readouts, dashboards and status updates as text with block (░▒▓█) and box-drawing characters - research and survey results, funnels and A/B tests, UX flows and state machines, roadmaps, screen wireframes, design-system docs, handoff and QA checklists, motion specs and moving diagrams. Use for an ASCII or Unicode diagram, text wireframe, sparkline or bar chart in Markdown, a PR, a ticket or a doc; a design review deck; a report or audit as a PDF; or turning a text wireframe into an HTML prototype or components from the project's design system. Draws from a small JSON spec with real, sourced data and exports Markdown, MDX, HTML, SVG, PNG and PDF.
license: MIT
metadata:
  version: "0.3.0"
  author: Alexander Traykov
  homepage: https://traykov.cc/glyph-kit
---

# Glyph kit

You write a **spec**, a small JSON object; a script with no dependencies draws it. The kit lays out every figure, so its output always lines up: never draw a figure by hand when a type covers it.

Work in the user's folder, not this skill's, so specs and outputs land there. `<skill>` below is this skill's folder; file paths in this guide are relative to it.

## Make one

1. **Pick the type** from this table; it goes in the spec's `kind` field.

   | The task is about | Types |
   |---|---|
   | Interviews, surveys, usability tests, quotes | `likert` `themeMatrix` `affinity` `quoteCard` `taskStats` `emotionCurve` |
   | Funnels, retention, A/B results, metrics, charts | `funnel` `cohort` `abResult` `metricPanel` `barChart` `compare` `forecast` `meter` `sparkline` `heatmap` `calendarStrip` |
   | Flows with decisions, state machines, journeys, sitemaps | `flow` `branchFlow` `stateMachine` `journeyMap` `tree` |
   | Roadmaps, priorities, ownership, timelines, decisions | `board` `impactEffort` `swimlane` `gantt` `statusKey` `decisionLog` |
   | Screens: one screen, an app shell, a card grid, list and detail, a modal | `screen` `responsive` `appShell` `cardGrid` `listDetail` `modal` |
   | Tokens, scales, colour, contrast, component states, layers | `spacingScale` `typeScale` `palette` `colourRoles` `contrast` `stateMatrix` `layerStack` `tokenTable` `table` |
   | Redlines, QA checklists, component anatomy, before and after | `redline` `qaChecklist` `anatomy` `compare` |
   | Motion intent, timing, transitions, stagger, easing | `motionTiming` `intentCard` `transitionSpec` `stagger` `filmstrip` `easingTable` |
   | Work moving over time: rework loops, state machines, queues, rollouts, loading | `loop` `states` `queue` `rollout` `loading` |
   | A whole deliverable on one page: readout, dashboard, PR summary, design review, status update | `readout` `dashboard` `prSummary` `designReview` `statusUpdate` |

   Unsure between two? Read the area's guide, `reference/areas/<area>.md` (research, metrics, flows, planning, wireframes, systems, handoff, motion, process, layouts): it shows each type drawn.
2. **Get its data shape**: `node <skill>/scripts/glyph-kit.mjs guide <kind>` prints the kind's example spec and what to watch for. Copy that shape; don't read the scripts.
3. **Write the spec** as JSON next to the document that uses it:

   ```json
   {
     "kind": "funnel",
     "title": "Signup to paid, last 30 days",
     "intent": "Find the step where most people leave.",
     "source": "Product analytics export, 2026-10-15",
     "data": [{ "label": "Visited pricing", "value": 12400 }, { "label": "Paid", "value": 610 }]
   }
   ```

   Data comes from the user or their files (`"data": "@results.csv"` reads a file next to the spec), never from you. If numbers are missing, ask. Only if the user wants a sketch anyway, start `source` with "Illustrative": every format then carries a SAMPLE DATA stamp. A spec with numbers and no `source` is refused.
4. **Render, fix, render again** in one command:

   ```bash
   node <skill>/scripts/glyph-kit.mjs render spec.json --to markdown > figure.md
   ```

   The kit refuses a spec it can't draw truthfully and says why in a sentence. Labels over the limit (usually 24 cells) are cut with "…", and the kit lists each one on stderr with its limit. Shorten those labels and render again: a figure with "…" loses words.
5. **Put the conclusion in the sentence around the figure.** The figure supports it.

Kit output needs no further checking: frames close and widths fit by construction. When a spec is refused, run `check spec.json` to see every problem at once instead of fixing them one draw at a time. Run `node <skill>/scripts/lint.mjs <file.md>` only on figures drawn by hand.

## Other outputs

Every command is `node <skill>/scripts/glyph-kit.mjs <command>`.

| Output | Command | Read first |
|---|---|---|
| Text, Markdown | `render spec.json [--to text\|markdown]` | nothing |
| HTML page; a `screen` becomes a working prototype | `render spec.json --to html [--map design-system.map.json]` | `reference/fidelity.md` for prototypes and code |
| Deck | `deck deck.json > deck.html` | `guide deck` |
| Report (cover, summary, sections) | `export report.json --to html\|pdf` | `guide report` |
| MDX, SVG, PNG, PDF of anything | `export <file> --to md\|mdx\|html\|svg\|png\|pdf` | `reference/export.md` |
| Every problem with a spec at once | `check spec.json` or `check notes.md` | nothing |
| A figure that stays editable in Markdown | `render spec.json --to markdown --with-spec`, then `redraw notes.md` after a spec change or `read notes.md` after a drawing edit | `reference/editing.md` |
| Your colours, or a palette | `--theme ink`, `--theme theme.json` or `--theme mixed:#7a5cff`; roles from your tokens with `--map` | `reference/colour.md` |
| Moving diagram: a process over time | `live spec.json --to html` (or `--to markdown` for its still) | `reference/live.md` |
| Several layouts as one document | `export layouts.json --to html\|pdf`, a layout to a page | `reference/areas/layouts.md` |

Decks and reports open with the kit's logo: ░▒▓█ side by side, in that order and in one colour. Keep it that way when you edit their HTML or draw a title card or still yourself.

HTML outputs are self-contained (font, styles and, for moving pages, the player inlined): 40–200 KB. Don't read them back to check them; render the same spec `--to text` instead. PDF and PNG use a Chromium browser already on the machine; everything else needs nothing.

When another agent or a later turn needs the figure, pass the spec (a few hundred bytes), not the drawing. If a drawing must go into a model's context, add `--compact` (plain ASCII, same layout).

## Rules

1. **Every glyph has a referent**: a number, a state or a structure. No decoration, no green-on-black or glyph rain unless the product is a terminal.
2. **One meaning per glyph per document.** `█` measured or done, `░` projected or the empty part of a scale, `·` an empty cell.
3. **To call something out, use `focus`, never a colour.** "Highlight the drop-off", "show where it fails": name it as drawn in `focus.on`, pick a tone, and say the point in `focus.say` (`reference/spec.md`). It colours, recedes the rest and arrives last in every form, and the text keeps a `►` line.
4. **Numbers are printed as text** next to the glyphs, and every figure with numbers shows its source.
5. **Labels may use any script.** Width is counted in cells: CJK takes two. Set `lang` for casing and number format. Font and right-to-left limits: `reference/characters.md`.
6. **Every type moves in HTML and decks.** The processes and a test result with readings over time keep moving; every other type arrives once, in the order that carries its point, then stays still. Each keeps a still that makes the same point; it is what reduced motion, print and Markdown show. Say what the motion shows in the sentence next to it.
7. **Drawing by hand** (only when no type fits): use the glyphs in `reference/characters.md`, follow `reference/layout.md` (two cells of padding inside a box, four between boxes, at most 80 columns), then lint.
8. **Going up in fidelity** (prototype, production code): use only the components and tokens the design-system map names, and ask when it has no entry. `reference/spec.md` describes the spec fields and the map.

If figures look misaligned where the user reads them, the font is drawing a glyph at the wrong width: suggest Departure Mono (free, departuremono.com), never require it.
