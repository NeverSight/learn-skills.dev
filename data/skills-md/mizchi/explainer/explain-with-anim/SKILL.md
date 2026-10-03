---
name: explain-with-anim
description: Answer "how does this work / how is this structured / what does this change" with a drawn figure and a narration that follows it — a module map from the code's own imports, a walked request, a state machine, an algorithm step by step, the change map of a branch — produced with `vlmkit-anim`, checked against the facts it draws, and delivered as an SVG / GIF next to the prose. Use whenever the user asks to explain, walk through, show the structure of, or illustrate code, a repository, a flow, a protocol, a PR, or a bug, and a picture with four or more things and their relations would carry the answer better than a paragraph. The explanation is the deliverable; the picture is its evidence. Scene mechanics are in `explanatory-animation`.
---

# explain-with-anim

The user asked a question. Answer it with a picture and the words that walk
the picture — not a picture instead of an answer, and not a paragraph with
a decorative diagram after it. The figure is drawn from the code (or the
facts) by `vlmkit-anim`, checked, and delivered as a file; the prose follows
the figure beat by beat and names the things in it by their ids.

Read `explanatory-animation` for how to write and check a scene. This skill
is about **what to draw, from what, and how to explain with it**.

## First: does a picture help?

Draw when the answer has **things and relations** — four or more modules,
states, participants, steps — or an **order in time**, or a **before and
after**. Do not draw for a one-line answer, a single function's body, or a
question about a value. If in doubt, write the answer first; if it needs a
list of more than four named things that point at each other, draw them.

## Choose the picture from the question

| The user asks… | Draw | From |
|---|---|---|
| "How is this repo / package / directory structured?" | `kind: modules` — a module map, containers per area | `vlmkit-anim facts <dir> --depth 1 --out f.expect.json` (the import graph), then the map, then `check --expect f.expect.json`; for the whole workspace `vlmkit-anim repo --out <dir>` draws it and writes its own sheet |
| "How does a request / event / message flow through it?" | `modules` with a `sequence` that walks the path (`highlight`, `flow`), or `kind: sequence` when the participants and their calls are the point | the code path you read; the map from `facts`; each hop a beat with a caption saying why |
| "How does this algorithm / data structure work?" | the kind that owns it: `sort`, `array`, `tree`, `heap`, `stack`, `queue`, `list`, `matrix`, `graph` | the function's own steps; small concrete values (five to eight) so every beat is readable |
| "What states can this be in? What happens on X?" | `kind: state-machine` with a `trace` of the events that matter | the enum / reducer / status field and its transitions |
| "How do these services talk? What if one is slow / lost?" | `kind: distributed` (nodes, messages, a lost one) or `kind: sequence` (frames for retry / alt) | the protocol as implemented; the failure the user asked about as the trace |
| "Why does it go this way here?" (a decision) | `kind: flowchart` with the walked path | the branch conditions, as their labels |
| "What does this branch / PR change?" | `vlmkit-anim pr --base origin/main --out .vlmkit-anim/pr` — one beat per commit; or `vlmkit-anim diff before.json after.json` for two maps | git; `<name>.md` is paste-ready |
| "What is the schedule / what slipped?" | `kind: gantt` | the plan, the slips as `slip` ops |
| "The docs already have a mermaid diagram" | `vlmkit-anim import mermaid page.md --out scene.json`, then finish it | the diagram; read its `dropped / changed:` list |
| "Give me a D2 file" / "something I can paste in the README as ASCII" / the repo keeps `.d2` diagrams | `d2-diagram` — D2 text laid out by TALA, rendered in the terminal | the same `facts` sheet, drawn by hand into D2; say in the prose that nothing checks the D2 against the code |

One picture per question. Two aspects that both matter (structure and a
walk) are one `modules` scene with a `sequence`, or `kind: compose` — not
two files.

## Ground it in the source, not in memory

- A map of code is drawn from the code: `facts` for a directory, `repo` for
  the workspace, the import list or `package.json` files by hand when
  neither fits. Then `check --expect`. A map drawn from memory and not
  checked is a guess with a border round it.
- A walk is drawn from the path you read: cite the file and function each
  beat corresponds to in the caption or in the prose ("`handle()` in
  `router.ts` → `dispatch`").
- Anything you could not verify goes in the prose as "not drawn: …", never
  in the picture.

## Produce

```
1. write <name>.scene.json            in the repo's docs/ or .vlmkit-anim/, or the scratch dir if it is not to be kept
2. vlmkit-anim check <name>.scene.json [--expect <name>.expect.json]
3. vlmkit-anim layout <name>.scene.json               must report no issue; `why` when the canvas warning names a pair
4. vlmkit-anim still <name>.scene.json --out <name>.svg      a still (structure, a map, a state diagram)
   vlmkit-anim video <name>.scene.json --out <name>.gif --width 640   a walk (a request, an algorithm, a trace)
5. vlmkit-anim explain <name>.scene.json              the beats — this is the skeleton of your prose
```

Five rounds of edit → `check` at most. If it is not clean by then, deliver
the explanation in words, say the figure did not converge and which line
stopped it, and keep the scene file for the reader.

## Write the explanation

1. **One sentence of what the picture is** and what it was drawn from
   ("the packages under `packages/`, from their imports, 12 modules, 19
   dependencies").
2. **The beats, in order**, one short paragraph or bullet each, reworded
   from `explain` — say *why* at each step, not what moved. Name things by
   the ids in the picture so the reader can find them.
3. **What the picture leaves out** and where to read it (a file, a
   function, a config).
4. **The files**: the SVG / GIF path, the scene, the fact sheet.

Do not describe the picture's geometry ("on the left", "the blue box") —
layout is the compiler's and may move on the next edit. Say the id.

## Deliver

- In a chat: the prose, then the figure as a file the user can open
  (`SendUserFile` when available; otherwise the path). A GIF for a walk,
  an SVG for a structure.
- In a PR or issue: paste the `<name>.md` that `pr` / `repo` write, or the
  figure with the beats under it. If the repository already posts
  `vlmkit-anim pr --mermaid` on every PR (vlmkit's `pr-visual` workflow does), do not post a second one.
- In docs: a ```` ```vlm-anim ```` fence (the animation) or ```` ```vlm-anim still ````
  (the figure) with the scene inline, so the page stays checkable; or the
  SVG committed next to the page.

## Done condition

- `check` green (and `--expect` green when a sheet exists), `layout` clean.
- Every id named in the prose is in the picture, and every beat in the
  prose is a step in `explain`.
- The user can answer their own question from the figure alone; the prose
  says why each step is there.

## Anti-patterns

- **A figure after the answer, unreferenced.** If the prose never names an
  id from the picture, the picture is decoration; drop it or rewrite.
- **Drawing what you believe the structure is.** Run `facts` first. Two of
  five green module maps in one evaluation round were wrong about a real
  dependency.
- **Coordinates.** A scene with x / y is a drawing, not an explanation, and
  cannot be re-edited by the next reader. Use the kind that owns the things.
- **Twelve beats where four would do.** Pick the values and the trace that
  show the one mechanism the question is about.
- **Skipping `layout` because `check` was green.** Lines through labels are
  what a reader sees first.
