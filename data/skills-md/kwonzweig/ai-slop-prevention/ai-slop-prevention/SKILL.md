---
name: ai-slop-prevention
license: MIT
description: 'Use before showing any deliverable to a person or handing it to another agent, and when reviewing one: a UI screen, mockup, or prototype; a document, message, prompt, or spec; game content; a data model or code. Triggers include a card or caption that lists several fields on one line, a template or report format with no list of its fields and their types, an id shown as a label, an edit or delete rendered as text, a sentence in an interface that explains the interface, a builder''s test status or report in the deliverable, a lock or disabled control used to say "read only", a list, count, or detail copied from something that already has an owner, and a stack or library chosen because the project is small or agents know it best.'
---

# AI slop prevention

Read the reference for the medium you are producing. Each one ends with a check to run before the work is shown.

| Deliverable | Read |
| --- | --- |
| A screen, card, list, form, caption, button, empty state, or prototype | [references/ui.md](references/ui.md) |
| Prose a person reads: document, message, spec, template or report format, commit, release note, in-game text | [references/prose.md](references/prose.md) |
| A data model, schema, API, or code structure | [references/code.md](references/code.md) |

## The habits, in one place

| Habit | What a person sees | Do instead |
| --- | --- | --- |
| Field mash | `Owner · Claude Code · 2026-11-09 · Snapshot`: fields of different kinds chained with dots, pipes, or spaces; a template or report format with no list of its fields | One field per labeled line or cell. Dots only between items of the same kind. A template or report format opens with its fields and their types. See prose.md. |
| Metadata nobody uses | Record ids, internal kinds, and numbers on the screen (`R-007`, `T-RG-003`, `worker-agent`) | Nothing a person does not act on. Ids live in the API; a thing is shown by its name. |
| Title that repeats the body | A header line and a body that say the same text | Collapsed shows the text truncated; expanded shows it in full. A title appears only when someone wrote one. |
| Words for standard actions | "Edit Delete Save Cancel" as text links | Icon buttons with the standard glyphs, each with an accessible name and a tooltip. |
| Interface that explains itself | "Suggested prompts. Tap one to send it as a request, with what you have typed added to its fixed sentence." | Form shows behaviour. When words are needed, an info icon with a hover tooltip. |
| Permission theatre | A lock glyph or greyed control to say "you can't edit this" | Show the value as plain text. Nothing editable-looking that isn't. |
| Coached empty states | "No requests yet. Write your first request below." | State the fact. The composer is already visible. |
| Off-target entries | A result that answers a question carries things that do not meet it, often with a note that says so: a catalog snapshot listed as "no source list here" in a reply about where the sources are | The result holds every entry that meets the question, and only those. The rest of the investigation stays in the notes. See prose.md. |
| Work notes in the deliverable | Builder test status, implementation narration, or a work report in the product | Keep work notes in the workspace. Show the data and actions the user needs for the task. See [ui.md](references/ui.md#work-notes-stay-in-the-workspace). |
| Grey on grey | Every icon, status, and action in the same muted grey; a confirm row where check and cross look identical | Semantic color from products of the same type: positive green, destructive red, selected accent. See ui.md. |
| Floating text | Captions, metadata, and button rows laid bare between other elements, so nobody can tell where one thing ends | Every text block and control group in its own card, panel, or boxed caption. |
| Template chrome | Cream background with serif and terracotta, purple gradient hero, numbered 01/02/03 markers, emoji headings, cards on everything | Choose for the subject. Structure only where it carries information. |
| Staged prose | not X but Y, one-line closers, forced triads, dashes everywhere, bold labels, "I hope this helps" | Say the thing once, plainly. See prose.md. |
| Hard-coded snapshot | What an owner holds, copied as it stood at one moment: a README naming six of a catalog's seven sources, "buy meat" passed on as three cuts, a second schema or term for a concept that has one | A pointer to the owner, plus only what the reader cannot get by following it. See below; for schemas, code.md. |
| Legacy default | The option most common in training data (Express, Bootstrap) proposed as the simple choice, with "the project is small" or "agents know it best" as the reason; or the decision framed inside a layer that demand has left | Check first whether demand has moved to a component that removes the layer, and decide there. Then rank the candidates by the standard in `find-tools`. Project size is never the reason for an older one. See code.md. |

## Hard-coded snapshot

When the thing already has an owner the reader can reach (a file, a catalog, a table, a type, a skill, the words of whoever asked), point to it and add only what the reader cannot get by following the pointer. "Use X" stays "use X", in an instruction, README, skill, prompt, data record, or diagram alike. A copied detail is a second source: it goes stale when the owner changes, and the next reader takes it as complete. When the reader cannot reach the owner, copy, and name the owner and the date beside the copy.

First caught: a README naming six of a catalog's seven sources, 2026-11-10.

## What this skill owns, and what it points to

This skill owns Field mash through Work notes in the deliverable. No published skill checked on 2026-11-09 had rules for field mash, metadata nobody uses, text for standard actions, self-explaining interfaces, or permission theatre. For the rest it points to skills that already do the work, when they are installed:

| Slice | Skill |
| --- | --- |
| Prose tells | `humanizer` (blader/humanizer) |
| Visual tells of generated pages: gradients, kicker labels, fake stats, card nesting | `antislop-ui` (miqdadbadjuber/anti-slop) or `hallmark` (Nutlope/hallmark, whose floor rule 10 bans middle-dot meta strings) |
| UX copy that restates the control or exposes internal codes | `impeccable` clarify reference (pbakaus/impeccable) |
| Comment hygiene and over-engineering in code | `antislop-code` (miqdadbadjuber/anti-slop), `unslop-ai-code` (JCarterJohnson/vibecoded-design-tells) |
| Stack and tool choice | `find-tools` (kwonzweig/there-is-a-tool-for-that) |

## Adding a habit

A habit enters this skill when the owner of a deliverable names it, or when a with-skill test shows agents producing it. The entry records what a person sees, what to do instead, and the first place it was caught, in the medium's reference file and as one row in the table above. The engine or product skill that was being built does not get the rule; it points here. Push, then refresh wherever the skill is installed (company skill sources, local skill folders).

## When a rule seems to block the task

A rule here is a default, not a law of the medium. The owner of the work may ask for text buttons, a visible explanation, a dot-joined meta line, or a table per variant. Deliver the version this skill describes, say in one line what the asked-for version would cost, and build it their way if they repeat the request. What never wins is the habit arriving on its own, and what never happens is a silent refusal.
