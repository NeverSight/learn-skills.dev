---
name: working-vantik-issues
description: >-
  How to work the Vantik issue tracker as an agent over MCP: pick up the issue
  before you touch code, keep it current while you work, tick the Definition of
  Done as you meet it, name the capability the work delivers, and keep issues
  few and meaty. Use before starting any substantial piece of work, throughout
  that work, and whenever creating, updating or closing Vantik issues.
---

# Working Vantik issues

Two obligations. The second is the one agents skip.

1. **Issues are few and meaty** — one self-contained objective each.
2. **Work is visible in the tracker while it happens** — not reconstructed
   afterwards, not summarised at the end, not left in a chat transcript nobody
   else can read.

These pull in opposite directions on purpose. **Restraint on filing, generosity
on progress.** "Few and meaty" governs how many issues exist; it says nothing
about notes and criteria, which should be frequent. Do not let caution about
creating issues turn into silence on the one you are working. A tracker that
learns what happened only at close time is a tracker nobody can trust mid-flight
— and mid-flight is when a human actually needs to see what their agents are
doing.

## The work loop

### Before you touch code

1. **Find the issue.** `search_tasks` (include `COMPLETED` — it may already be
   fixed). If substantial work has no issue, file one *first*, using the rules
   below. Work that exists only in a chat window is invisible work. Once you
   have it, `find_similar_tasks` gives the earlier issues like it and how each
   was resolved — the fix may already exist.
2. **`get_task`.** Read the **Definition of Done**. That is the standard the
   work is judged against — read it, never infer one from the description. It
   also carries the notes, history, sub-tasks, blockers, and the modules and
   capability the issue touches, all of which you would otherwise rediscover.
3. **`pick_up_task`.** Before the first edit, not after the last. This is what
   puts the issue on the board as in progress and stops two actors colliding.

### While you work

Cadence is driven by events, not by a clock. Each of these **requires** a write:

| When this happens | Do this |
| --- | --- |
| You meet a criterion | `update_criteria` `tick` — that one, right then |
| You learn something that changes the approach | `add_note` |
| You get blocked, or stop mid-work | `add_note`: where it stands, what is next |
| The work uncovers a condition the issue never anticipated | `update_criteria` `add` |
| The scope turns out to be wrong | `update_task`, or a note saying so |

**Tick criteria one at a time, as you meet them — never in a batch at the end.**
A half-finished issue that says *which* half is worth far more to whoever picks
it up than one claiming nothing. If you are about to close an issue and every
criterion is still unticked, you worked it wrong, whatever the code looks like.

Append a criterion only when the work reveals a genuine condition for done that
the issue missed. Never append one to describe what you happened to do — that is
how a Definition of Done decays into a changelog.

Notes are searchable and are read by strangers. Write what you tried, what you
found, and what the next person needs. "Working on it" is not a note.

### The rule that decides all of this

**Never end a work session with the issue out of date.**

If you have been editing code for twenty minutes and the tracker still shows the
state of things before you started, that is the failure — not a tidiness lapse.
A note costs seconds. An in-flight change nobody can see costs the humans the
only view they have of their agents.

### When you finish

1. `update_criteria` — tick everything genuinely met. Untick anything you
   discover was not.
2. `close_task` **with a resolution.** Always `close_task`, never `update_task`
   with a closed state: the resolution is posted as a note before the state
   changes, and it is what makes the fix findable the next time this problem
   appears.
3. **If it is not actually done**, do not close it. `update_task` to the review
   or blocked state, and `add_note` with what remains. A closed issue that is
   not finished is worse than an open one.

Handing the issue to Vantik's own agent instead of working it yourself is its
own decision, with its own bar — see the `delegating-vantik-work` skill.

## Put the work on the map

A project says which objective an issue serves. A second axis says what the
software is made of, and an issue sits on both.

| | What it is | Who sets it on an issue |
| --- | --- | --- |
| **Product** | What the workspace ships. Holds no code and no issues. | Nobody — it groups modules |
| **Module** | Where the code is: a repository, a path in one, a service. | A person, or the pull request |
| **Capability** | What the software does for the people who use it. | You, when you file |

**Read the map before you file.** `list_modules` gives every module with the
repositories it sits in — match it against the checkout you are in and you know
what your work touches. `list_products` names what the workspace ships and the
modules each one owns. `list_capabilities` tells you whether what you are about
to describe already has a name.

**Name the capability.** An issue delivers one capability, or none. Name the one
that already exists rather than describing the same thing in your own words: a
capability named the same way twice is two capabilities to whoever reads the
board. If nothing fits, leave it empty — that is a fine answer, and better than
a near-miss.

**Do not set the modules.** There is deliberately no field for them on
`create_task` or `update_task`. Modules are recorded by a person, or by the pull
request that changes the code, because that is the one moment the answer is
known rather than guessed. Your job is to read them, not write them.

**Use the axis to find what will collide with you.** Before you start, ask what
else is in flight around the code you are about to change:

```
list_tasks(modules: ["server"], stateCategory: ["STARTED"])
list_tasks(capability: "Issue tracking")
```

This is the question the axis exists to answer, and it is worth asking before
the work rather than after the conflict.

## Filing: is this even an issue?

The `create_task` tool enforces a floor — a real description, and acceptance
criteria for a top-level issue. This is the judgment above that floor.

**An issue is one self-contained feature, bug, or objective, with enough
substance that someone could pick it up cold.** Substantial by default: a fair
chunk of work, not a line item. A five-minute change or a single step of
something larger is a sub-task, a checklist entry, or a note.

**Span as few issues as you can.** Reach for one substantial issue with
sub-tasks before you reach for several. Splitting is the exception you justify.

Walk this list and stop at the first match:

1. **Part of an objective that already has an issue?** `add_note` to it, or
   `create_task` with `parent` for a sub-task. Not a new top-level issue.
   Genuinely a *separate* issue serving the same objective? It belongs in the
   same **project** — pass `project`.
2. **A passing observation, a finding, a "we should look at this"?** That is a
   note on the most relevant issue.
3. **You cannot state what "done" looks like?** It is a note until you can.
4. **A genuine, self-contained objective with a clear done?** File it.

Always `search_tasks` first, `COMPLETED` included.

## Three sizes, not one

Work comes in three sizes, and using the wrong one is what makes a tracker
unreadable:

| Size | Use | Tool |
| --- | --- | --- |
| **Sub-task** | A step of one issue. | `create_task` with `parent` |
| **Issue** | One self-contained feature, bug or objective. | `create_task` |
| **Project** | An objective that genuinely needs several issues. | `create_project` |

Sub-tasks hold the steps of one issue together; a project holds the *issues*
together. Both exist so that "keep issues few" never becomes "cram unrelated
work into one issue" — when work is too big for one issue, it goes **up** into a
project, not sideways into loose siblings.

**The moment to open a project is the second issue.** If you are about to file an
issue and one you already filed serves the same objective, stop: open a project,
pass `project` on both. `list_projects` before filing and reuse what exists.
Projects are few, long-lived and meaningful — one per real objective, never one
per work session, never one holding a single issue. Issues that turn out after
the fact to serve one objective can be gathered with `update_task` and `project`.

When the objective turns out different from what the project says — the scope
moved, the dates slipped, it is done — correct the project with
`update_project`. Never open a second project beside one whose description has
stopped matching its issues.

## What a good issue contains

- **Title** — the objective in a line.
- **Description** — the problem and *where it lives* (the file, the flow, the
  surface). Enough that a reader who wasn't there understands it.
- **Acceptance criteria** — what "done" looks like, as concrete checks. This is
  the forcing function: if you can't write them, the issue isn't contained. They
  become the Definition of Done that you and everyone after you tick off.
- **Capability** — what it makes the software do, when one fits.

Write it for a future reader who has none of your context.

## Anti-patterns

**On progress — these are the common ones:**

- Doing an hour of work and telling only the chat window.
- Closing an issue whose criteria are all still unticked.
- One giant note at the end instead of notes as you went.
- Inferring your own definition of done from the description while an explicit
  one sits on the issue.
- `update_task` to a closed state, so no resolution is ever recorded.
- Treating "keep issues few" as a reason to stay quiet on the issue you are in.

**On filing:**

- A title with an empty or one-line body.
- "Investigate X", "Look into Y" as top-level issues — those are notes.
- Splitting a single PR-sized objective across many tickets. If they really are
  three substantial issues, they are one **project**.
- Filing a near-duplicate instead of adding to the issue that exists.
- A scatter of loose issues that only make sense read together, with no project
  to say so.
- A project per work session, or a project holding one issue.
- Inventing a capability that restates one already on the board.
- Filing against a module you guessed at instead of reading `list_modules`.
