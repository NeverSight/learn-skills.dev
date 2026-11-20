---
name: show-me
description: >
  Use when the user says "show me", asks to see or visualise a change, an
  architecture, a data flow, or a design, or wants proof of the work in a
  form a person can take in at a glance. Covers ASCII, Markdown, and HTML
  views. Not for writing the PR itself or for prose explanations.
argument-hint: "[subject: path | area | change] [focus: data flow | architecture | ...] [ascii | markdown | html]"
---

# show-me

Show the work so a person understands it in one look, and can trust it. Pick
the smallest view that makes the point. Every box, arrow, and line in the view
comes from something you read in this session.

## 1. Read the ask

Take each part from the user's words. A part the user named wins over every
default below.

- **Subject** — what to show: a path, an area ("the backend service"), a
  change, a concept. It bounds what you read.
- **Focus** — what about it: data flow, architecture, call flow, state, what
  changed, a comparison. It picks the view.
- **Altitude** — how far up. "High-level" means modules, services, stores,
  and the seams between them; a single file means its functions and calls.
- **Format** — ASCII, Markdown, or HTML, if named.

When a part is missing:

- **No focus** — take it from the subject: a change → what changed; a file →
  its structure and calls; an area → its architecture.
- **No altitude** — match the subject: an area is high-level, a file is
  detailed.
- **No subject** — make the best guess, first hit wins: the branch against its
  base; uncommitted changes (`git diff HEAD` plus `git status --short` for
  untracked files); the topic of this conversation. Nothing fits → ask what to
  show. Say in the first line which guess you took.

Then write one sentence: what should the reader understand after looking? A
view without a point is decoration. Several points get one view each, in the
order the story needs them.

## 2. Read the evidence

Read inside the subject, as far as the focus and altitude need, from the
source, not from memory:

- **A change** — a ref or path the user named; else the branch against its
  base (`git diff <base>...HEAD`); else `git diff HEAD` plus untracked files.
- **A flow or structure** — start at the subject and trace outward: entry
  point, calls, data, and where state lives. Read the code at each hop. Stop
  at the altitude asked.
- **An architecture** — the deployable units and modules, their entry
  points, stores, queues, and external calls. Read manifests, config, and
  entry files before inner code.
- **A design or plan** — the doc, ADR, or spec it comes from.

A read-only run — a dry run, a query, `--help` — is the strongest evidence.
Run nothing that writes. Use the project's names from `GLOSSARY.md` when it
exists. Done when every element you plan to draw has a `file:line`, a
document, or the command whose output showed it.

## 3. Pick the view

The focus picks the view:

| Focus | View |
|---|---|
| Architecture | Module map: boxes for modules, stores, and external systems; arrows for calls and data |
| Data flow | Source → transform → sink, with the data shape on each arrow |
| Call flow | Call tree (indented) |
| Who talks to whom, in what order | Sequence diagram |
| Logic or an algorithm | Pseudocode |
| Which file owns what | Shallow file tree with `#` notes |
| UI structure, state | Component tree |
| Types, tables, contracts | The shape itself (type, schema, endpoint) |
| What changed in an existing shape | `diff` block of that shape |
| What changed across many files | File tree with status (`A`, `M`, `D`) and `#` notes |
| A shape that is mostly new | The full target shape |
| A comparison or a decision | Table, one row per option |

Use one view or several; rarely all. Keep only the modules, calls, files,
fields, and states the point needs. Put each view next to the one or two
sentences it supports.

## 4. Pick the format by where it goes

- **ASCII** — the terminal. The default. Box-drawing characters, indented
  trees, `diff` blocks, tables in a plain fenced block. Lines under 100
  characters.
- **Markdown** — a PR/MR body, an issue, or a doc. Fenced blocks with a
  language tag, and Mermaid for sequence and flow diagrams; GitHub and GitLab
  render it.
- **HTML** — the view is too dense for text: a UI or layout, a state
  comparison, a large flow, or a short walk-through of slides. One
  self-contained file that works on a phone and a desktop. Scaffold, diagram
  patterns, and style: [`references/html.md`](references/html.md).

Write HTML to the OS temp directory (`$TMPDIR`, falling back to `/tmp`) as
`show-me-<topic>-<YYYYMMDD-HHMMSS>.html`, open it (`open` on macOS, `xdg-open`
on Linux, `start` on Windows), and print the absolute path. Nothing lands in
the repo unless the user asks.

## 5. Mark what is proven

- Under each view, cite its sources: `file:line` ranges, the document, or the
  command. Views that share sources share one line.
- Mark any element you inferred rather than read with `(inferred)`, and say
  what reading would confirm it.
- End with one line on what the view leaves out — the paths, cases, or files
  not drawn — so the reader knows its edge.

Keep prose short. The view carries the point; the text names the point and
the proof.
