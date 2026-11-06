---
name: visual-plan
description: Write the design decision for one change as one interactive HTML page — a zoomable map of the proposed design, the decisions with clickable options, a worked trace, constraints, scope — for the person who locks it. Use when invoked by name (/visual-plan, "make a visual plan", "visual plan for …"), or when a planning or explainer skill asks for its interactive page. Not a task list — the implementation plan is a separate document written after the lock.
---

# visual-plan

One page. One change. The person reads it, answers the open decisions, and locks it. After the lock, the
implementation plan (tasks, files, tests) is a different document, written by whichever planning skill the
setup uses.

```
<this skill's directory>/
  references/sections.md        ← the section contract: core, extras, what each holds, what each must not hold
  references/words.md           ← the writing rules (STE) and the badge vocabulary
  references/nodes.md           ← the node tree: views, depth, the Respond sheet, how to author the data
  runtime/visualplan.css  visualplan.js   ← one runtime; the pack inlines them
  runtime/pack.mjs              ← lint + compose → one self-contained HTML file
  runtime/vendor/js-yaml.js     ← the YAML parser (MIT), so the pack needs only node
  examples/example.yaml         ← a full synthetic plan, open: the content file
  examples/example.html         ← what `pack.mjs example.yaml` makes from it
```

## What the page is, and is not

- **It is the definitive design.** It is built around the target state: what will be built, where each
  part lives, and how the parts connect. Around that it says what breaks today, which decisions are taken
  and why, which are open, what is in and out, and how we know it is done. Decisions are one block, not
  the spine: a reader who skips them still learns the design.
- **It carries design, not implementation.** No code sketches, no classes, no file:line for code that does
  not exist yet, no task lists, no who-does-what. File references appear only as evidence about today's
  code: in *current state*, and in the *known* facts of a decision.
- **One fact, one place.** A rule lives in the zoom or block that owns it and nowhere else; the settled
  table holds only decisions that had a real alternative, the goal only acceptance checks, the scope only
  what is out. A focused page beats a complete-looking one.
- **It holds only what this plan does.** A related thing appears only when the plan depends on it, and
  only the part it uses: "the tray uses ACP's session/fork", not a tour of the gateway. So no box on the
  map for an unchanged neighbour (draw it as a labelled edge), no term the plan does not add or rename, no
  card that says a behaviour stays "as today", no limit the plan neither sets nor must obey. The current
  state is the one place for today, and it lists only what the plan replaces.
- **It is not a ledger.** No "was", "dropped", "previously", no dates or attributions in the body.
  History lives in the chat and in the version labels.
- **Nuance lives in the zoom.** A rule or a limit that belongs to one layer is explained in that layer's zoom, not in a separate prose section.
- **The person owns every fork.** Recommend; never preselect, never lock on their behalf.

## Sections

Core, always present, in this order: **opening** · **problem and current state** · **map** (with a two-line
walkthrough under it) · **decisions** · **goal** · **scope**.

Extras, dropped when empty: **examples strip** · **design reference** · **terms** · **traces** ·
**constraints** · **data models** · **risks and behaviour changes** · **reused**.

What each holds, and the mistakes each one exists to prevent, are in `references/sections.md`. Read it
before writing.

## The node tree

The page is data: the author writes one content file, `plan.yaml`, and the pack composes it with the runtime into one self-contained `plan.html`. The map inside it is a tree of nodes. Depth is capped at 3:
**map → zoom → detail**. The person can ask for more in a given plan.

Each node declares one or more **views**: `diagram` (an SVG with clickable shapes), `ports` (input · inside
· output, with one example), `calls` (a call tree, one call per line), `machine` (a state machine),
`table`, `options` (a decision with clickable option panels), `section` (prose cards). A shape in a
diagram, a part in a ports view, or a row in a table can open a deeper node, with breadcrumbs back.

Every tag is a **badge**: recommended, keep, flag, exists, new, open, settled, withheld, round trip,
failed, recovered. `references/nodes.md` has the data shape and one example of each view.

## Profiles

The content file's `profile` field selects the lint. `plan` is the default and is everything this file
describes. `explainer` is for a page about an existing system (for example, written by a companion explainer or review skill):
only `map` and `terms` are required, file references are allowed anywhere, the STE word checks are off,
and the page has no Lock. The explainer's own style rules come from the skill that writes it.

## Words

Write in ASD-STE100 Simplified Technical English: one topic per sentence, active voice, present tense,
*must* and *can*, approved words, no idioms, no -ing forms, no shorthand or lifecycle vocabulary. Use the
names of the source of truth for every component, field and role, and add an "older words" card when a
name changed during the work. Say what a thing **is** before what it **does**. `references/words.md`.

## Steps

**Who does what.** The page is built in a subagent, so the main context keeps the design and the
conversation, not the YAML, the HTML, or the lint rounds. When the runtime has subagents (Claude Code: the
Agent tool; Codex: a spawned agent), the main session does steps 1, 6, 7 and 8 and gives steps 2 to 5 to
one **page builder**:

- **It receives** the brief's content, not a draft page: the opening, the problem and today's parts it
  replaces (with file references), the design parts and how they connect, the decisions (settled, and open
  with their options and the recommendation), the goal, the scope, the retired terms, the output path, and
  this skill's directory.
- **It does** steps 2 to 5: reads `references/`, writes `plan.yaml`, packs, and fixes every lint error
  itself until the pack reports 0 errors.
- **It returns** only the path to `plan.html`, the titles of the open decisions, the lint result, and at
  most 150 words, plus any question it cannot settle from what it received. Never the YAML or the HTML.
- **The main session never opens** `plan.yaml` or `plan.html`. A Respond message is answered in chat
  first; then the main session sends the edit list to the page builder (the same one when the runtime can
  resume it, else a new one with the content file's path), which repacks and returns the same short report.

A runtime without subagents does steps 2 to 5 inline.

1. **Read first.** The current code the change touches, the platform's own documentation for every
   mechanism the plan names, in the platform's own words (never invent a mechanism the platform does not
   have), and the person's earlier choices. A mechanism you are about to drop: read its code before you call it a leftover.
2. **Write the core sections**, the map and its zooms as nodes, then the extras that are not empty.
3. **Sweep** for KISS, DRY and YAGNI before each publish: every custom mechanism, cache, probe, side table
   or classification needs a measured reason or goes. Then grep the page for every retired term.
4. **Pack.** `node <skill dir>/runtime/pack.mjs plan.yaml` runs the lint (no code in the plan, STE words,
   structure, retired terms) and writes `plan.html`, one self-contained file with the runtime inlined.
5. **Publish** the same packed `plan.html` to every target: opened from disk, served from a temp dir, hosted
   anywhere, or wrapped by a host such as the claude.ai Artifact tool. The hosted page or artifact tool of the
   setup is one target when available, republished to the same URL with a label per version. Never depend on
   a capability of that platform: the file alone must work. When a calling skill names the delivery, follow it.
6. **Hand over** with one line and the open list.
7. **While the page is open:** answer every question in chat first; an updated page is not an answer.
   Edit on request, or for a routine fix. Ask, with the structured question tool and with context and
   options, before adding a section or a mechanism. Recap after every publish: what changed, what is open.
8. **The lock.** The Respond sheet on the page returns picked options, struck rows and comments as one
   markdown the person pastes in chat. The lock button appears only when no decision is open. At the lock,
   save the final HTML where the calling skill says, or else beside the plan or the decision record in the
   repository, and hand over to the implementation-plan step.

## The two states of the page

A visual plan has two states, and the first is the one that matters.

- **Open.** One or more decisions are open. Each one is presented as a question in full: the context
  (the problem, why now, what is known with file references, who is affected), then the options, one
  line each, the recommendation first and badged, none preselected, each option opening its panel (How,
  Gains, Costs, Effort / risk, Reversible). The status badge counts the open decisions. This is how the
  person wants to be asked: never "A or B?", always the context and the trade-off of each option, on
  the page and in chat alike. The Respond sheet has no Lock button in this state.
- **Locked.** No decision is open. Every decision is in the settled table with what it follows from and
  what was considered. The status badge says locked and the date. The Lock button appears only here.

A plan moves from open to locked by answers, never by the agent's choice. A change after the lock
reopens a decision and the page goes back to the open state.

## Decisions on the page

Settled decisions: a table of decision · follows from · considered (the library, SDK or pattern adopted or
rejected). Open decisions, each: context (the problem, why now, what is known with file references, who is
affected), then options one line each, recommended first and badged, none preselected, each opening a
panel with How · Gains · Costs · Effort / risk · Reversible. Open questions and open decisions are one list.
A closed one moves into the settled table with its reason.

## Anti-patterns

Code in the plan · ledger wording · an invented platform mechanism · two vocabularies for one thing ·
marks on a trace when all code is new · a constraint without its reason · a mechanism dropped without
reading its code · mechanisms drawn beside the flow instead of in it · a tag that is not a badge · a
section added without asking.
