---
name: find-the-core
description: >-
  Drill into the core of a task before executing it, using Simon Sinek's Golden
  Circle (Why → How → What) fused with the journalist's 5 W's (Who / What / When
  / Where / Why). Use this whenever the user hands over a task, goal, or project
  that is vague, broad, high-stakes, or ambiguous — e.g. "help me build X", "I
  need a plan for Y", "write something about Z", "I want to start a ___" — where
  charging ahead risks confidently solving the wrong problem. Run a short
  adaptive interview to surface the real purpose and the missing dimensions,
  deliver a tight brief, then confirm before proceeding. Do NOT use it on small,
  crisp, already-specified requests where the goal is obvious — clarity-gathering
  there just wastes the person's time.
---

# Find the Core

A task is only as good as the understanding behind it. People routinely ask for
the *What* ("write a bio", "build a dashboard", "plan an offsite") while leaving
the *Why* unspoken — and the Why is what actually determines whether the output
is any good. This skill's job is to excavate that core before any real work
starts, so the work aims at the right target.

It fuses two classic lenses:

- **Sinek's Golden Circle** — *Why → How → What*. The Why (purpose, belief, the
  change being sought) is the center of gravity. Most people skip it; you don't.
- **The 5 W's** — *Who, What, When, Where, Why* (+ How). A systematic sweep that
  makes sure no dimension of the task is left implicit.

These overlap on purpose. Don't run them as two separate interrogations. Fuse
them into a single map with **Why at the center** and the rest fanning out:

| Dimension | What it pins down |
|-----------|-------------------|
| **Why** (the core) | The real purpose. What change, outcome, or feeling is this for? Why does it matter, and why now? |
| **Who** | Audience, stakeholders, decision-makers, the person doing the work |
| **What** | The concrete deliverable and what "done" looks like |
| **When** | Deadline, timing, sequence, cadence |
| **Where** | Context, platform, venue, channel, environment |
| **How** (Sinek's middle ring) | Approach, constraints, resources, the distinctive way it should be done |

## When to use this

Trigger it when the task is **vague, broad, high-stakes, or ambiguous** and
pressing ahead risks wasted effort:

- "Help me build / plan / design / create ___" with the purpose left implicit
- "I want to start a ___" / "I need a strategy for ___"
- Open-ended writing or comms ("write something about ___") where audience and
  intent aren't stated
- Anything where you notice you'd have to *assume* several important things to
  begin

## When NOT to use this

Skip it — and just do the task — when the request is already crisp:

- Small, well-specified tasks ("convert this CSV to JSON", "fix this bug")
- Factual questions, lookups, calculations
- Anything where the Why and the shape of "done" are already obvious from the
  request or the conversation

Running a clarity interview on a clear task is itself a failure of this skill.
When in doubt on a borderline case, prefer one sharp question over a full
interview — or state your assumption and proceed.

## The process

### 1. Gauge the size first

Before asking anything, judge how big and how fuzzy the task is. This sets the
depth of everything that follows:

- **Tiny / clear** → don't run the skill. Do the task.
- **Small but fuzzy** (one real unknown) → state an assumption and proceed, or
  ask a single question. No brief needed; a sentence of framing is enough.
- **Medium** → ask about the 2–4 highest-uncertainty dimensions, then a short
  brief.
- **Large / strategic** → a fuller pass across Why + all the W's, sometimes over
  more than one round, then a complete brief.

### 2. Mine every available source before asking

Good interviewing is mostly *not* asking what you could have inferred. Before
asking anything, exhaust the context you already have access to:

- The conversation so far and any files the person attached
- **Project knowledge** — design docs, specs, briefs, PRDs, READMEs — and the
  **codebase itself**, which often pins the What, the How, and sometimes even
  the Why more precisely than a person would in a hurried reply
- Connected sources and tools when available (docs, tickets, past conversations)

The rule is **search before you ask**: a question whose answer is sitting in a
design doc or the code is worse than no question at all. Only ask about genuine
gaps — things you cannot reasonably infer and that would change the output if
wrong. Nothing erodes trust faster than asking the person something they already
answered somewhere you could have looked.

### 3. Always pin the Why

Whatever the depth, anchor on the Why. It's the dimension people skip and the
one that most changes the answer. If the Why is unstated, that's almost always
your first question. Everything else fans out from it.

### 4. Ask adaptively, in small batches

Ask only the questions the task's size justifies, and ask them in small,
focused batches (1–3 at a time) rather than a wall of questions. If a tool for
presenting tappable options is available, prefer it — choosing is lower-effort
for the person than typing, especially on mobile. Make questions concrete and
mutually exclusive; offer a sensible default where you can.

Phrase questions around the *decision they unblock*, not around the framework.
Ask "Who's going to read this, and what do you want them to do after?" — not
"Please define the Who and the Why."

### 5. Synthesize a brief — terse, proportional to the task

The brief exists to **clarify and nail down**, not to sell, impress, or explain
at length. Write it telegraphically: short phrases and fragments, not prose. No
persuasion, no adjectives-for-effect, no hedging, no filler. Every line is a
decision or a fact — if a line isn't pinning something down, cut it.

Keep it proportional — a few lines for a medium task, the full template for a
big one. Use this shape:

```
## The core
**Why:** <the purpose — one sharp line>

## Dimensions
- **Who:** ...
- **What:** ...
- **When:** ...
- **Where:** ...
- **How:** ...

## Restated
<one line: what we're making + what done looks like>

## Definition of done
- <concrete, checkable signals that it's finished>
```

Omit any dimension that genuinely doesn't apply rather than writing "N/A." If
dropping one is itself a decision, note it in a few words (e.g. "When: no
deadline — optimizing for quality").

### 6. Confirm before proceeding

End by handing control back: deliver the brief, then ask whether to proceed on
that basis or adjust anything. Something like: "Does this capture it? Say the
word and I'll get started, or tell me what to change." Do not silently roll into
executing the task — the confirmation is the point.

## Examples

**Example 1 — lean (small but fuzzy)**

> User: "Help me write my bio."

One real unknown: where it lives and what it's for. Pin the Why with a single
question — "Where will this appear, and what do you want a reader to think or do
after reading it (hire you, trust your expertise, buy something)?" — then write
it. No formal brief; a one-line framing is enough: "Got it — a credibility-first
bio for your consulting site, aimed at prospective clients. Here's a draft:"

**Example 2 — thorough (large / strategic)**

> User: "I want to start a newsletter."

Big and wide open. Run a fuller interview across rounds:

- *Why:* What change do you want in readers — and why are you the one to write
  it? (the core)
- *Who:* Who's it for, specifically?
- *What:* Format, length, the through-line topic
- *When:* Launch target and cadence you can actually sustain
- *Where:* Platform / how people subscribe
- *How:* Where the content comes from each week; how you keep it going

Then deliver the full brief and ask whether to proceed to a launch plan.

## Anti-patterns

- **Interrogating.** More questions than the task warrants. Lean is the default;
  earn each question.
- **Asking the known.** Surfacing a question whose answer is already in the
  conversation or the files.
- **Wall of questions.** Dumping ten questions at once instead of small batches.
- **Running the frameworks twice.** Asking "what" for the Golden Circle and
  again for the 5 W's. They're one fused map.
- **Triggering on crisp tasks.** Clarity theater on a request that was already
  clear.
- **Bloated briefs.** A full template for a task that needed two lines.
- **Prose-y or sell-y briefs.** The brief clarifies and nails down — telegraphic
  fragments, not paragraphs, and never a pitch.
- **Skipping the Why.** Filling in Who/What/When/Where but never naming the
  purpose — the one thing that matters most.
