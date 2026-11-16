---
name: craft-states
description: Use when designing or redesigning a screen, flow or component, when asked to cover all states or find missing ones, or before handing a screen to code. Also use when a design only shows the happy path, uses short tidy sample data, or assumes a single user.
---

# Screen states

## Overview

A screen is not designed until every state it can be in is designed. The happy path is one state out of twenty. **List the states in words first, get the list approved, then draw.** Agreeing on a list costs a minute. Discovering a missing state in code costs a day.

## When to use

- A new screen, flow or component, or a redesign of one.
- "Cover all the states", "what are we missing?", "is this ready for dev?"
- The design shows one perfect case: three orders, short names, everything loaded.

## When NOT to use

- A small edit to an existing screen ("make the button 2px taller", "fix this typo"). Make the edit and stop.
- Pure copy changes, or a question about the design.

## Before you start

0. Read `DESIGN.md` at the project root if it exists: it is the project's design brief.
1. Read the project's design system and existing screens. They win on look: reuse their empty state, banner and loading pieces instead of inventing new ones.
2. Pick your tool's adapter in `references/adapters/` (`paper.md`, `figma.md`, `html.md`). If no adapter matches your tool, do the same verbs in your tool and say which you mapped by hand. With no design tool at all, build in HTML (`html.md`). If an image is all you have, say that values read from it are estimates.
3. Know the screen's job: who uses it, what they came to do, and what the one next action is.

## Steps

1. **Write the state list.** Walk every group in [the state catalogue](references/state-catalog.md): Data, System, Activity, People, Interaction. Mark each item in one of three ways:
   - **applies**, with a one-line description of what the screen shows;
   - **doesn't apply**, with a reason;
   - **open question** for the person.

   **Stop and show the person the list.** Do not draw yet.
2. **Draw the main state** with realistic invented data: the most complex realistic case, not the tidiest. Use long names, many items, and mixed statuses. Build it one section at a time, and check each section rendered before the next.
3. **Draw every other state that applies:**
   - a state that changes the whole screen (empty, offline, couldn't load) gets a full board;
   - a state that changes one part (a failed row, a saving button, a stale banner) goes on a state sheet that shows just that part.
4. **Check every state:**
   - Does it offer the action that resolves it, and say who does it?
   - Does moving between states keep the layout still (same widths and heights, no jumping)?
5. **Name and order the boards** as described in [naming and sheets](references/naming-and-sheets.md): `<number> · <screen> · <state>`, the main state first, the other states next, sheets last, and a cover note at the start of each row.
6. **Look at what you made.** Screenshot or render every board and compare it with the list. If you cannot render, say so plainly, and name what wasn't checked.

## Rules

| Rule | Why |
|---|---|
| The list comes before any drawing, and the person approves it | It's the cheapest moment to find a missing state or one that doesn't apply |
| Sample data is long, many and messy | Short tidy data hides truncation, overflow and wrapping bugs |
| Assume more than one person uses it | "Someone else already did it" and "changed while you looked" happen every day |
| No state without a way out: what to do next and who does it | A dead end makes people call support |
| A failure is worded as a failure, never as a deliberate pause | "Stopped" reads like someone chose it; "Couldn't save" tells the truth |
| One standard empty-state piece across the product | Ten bespoke empty states drift apart and cost ten times more |
| A whole-app problem goes in a top banner; a problem with one item goes inline on that item | A banner for one row's error shouts at everyone about nothing |
| Loading and label swaps keep the element's size | Layout shift makes people click the wrong thing |
| Interaction states (hover, focus, disabled…) come from the design system's states matrix | Redrawing them on every screen creates drift; draw them once, in the system |

## Done when

Every catalogue item is drawn, marked "doesn't apply" with a reason, or listed as an open question. The boards are named and ordered, and you looked at each one or said which you couldn't.

## Common mistakes

| Thought | Reality |
|---|---|
| "I'll just design all the states in one go, it's faster" | Without an approved list you draw states nobody needs and miss the ones they do. List, stop, then draw. |
| "Three sample orders show the idea" | Show forty, and show a customer called "Maria Fernanda de Albuquerque Santos". The overflow state is a real state. |
| "Loading, empty, error, offline: covered" | Those are four of the catalogue's groups' easiest items. Also check many/overflow, long text, someone-else-did-it, changed-while-viewing, permissions and slow. |
| "I'll put all the states on one page" | An unnamed pile can't be reviewed or handed off. Name and order the boards. |
| "I couldn't render it, but it's fine" | Say what you couldn't check. Unverified layout is a guess. |

## Red flags: stop and go back to step 1

- You are drawing and no state list was approved.
- Every name in the mock fits on one line.
- The design never mentions a second person.
