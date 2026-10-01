---
name: component-docs
description: Writes one component's documentation entry from its code, stories and real call sites, in a Geist-style page order. Use for "document the button", "write docs for Select", "what states does Toast have", usage rules for a component, or a new or changed component. Skip foundations, overview pages and multi-component patterns. Docs for a whole design system go to design-system-boss.
---

# Component documentation

1. Paste the heading list from `references/doc-format.md` into the draft, empty.
2. Find the component and read its code, props type, styles and stories, each recorded as a Sources line (`references/sources.md`).
3. Find two real uses, pasted or found by call-site search, or apply `sources.md` (Fewer than two uses).
4. Check the stops below. If one applies, return the stop shape and end the run.
5. Trace which source supplied each example, variant, prop, state and token. Every disagreement is a line under Conflicts.
6. Fill each section from sourced facts, in order, per `doc-format.md`. Copy token names and example code character for character.
7. Write Usage rules last, by the rule method in `doc-format.md` (Usage): a shape, a ground, a check and a Don't and Do pair each, tested or cut.
8. Fill Guessed at, and pass the review checklist.
9. When the entry is a spec, run the check `doc-format.md` (When the entry is a spec) names, and put its last line in the status block.

Never ship:

- A variant, prop, token name, example or real use with no listed source. A planned use says planned.
- An invented state or precedence written to pass the spec check.
- A conflict settled without a quoted rule. Otherwise both sides stay shown.
- An edit to the code, stories or spec being documented.
- An entry published by the skill. It is a draft, a coordinator decides where it goes, and publishing belongs to the person.

A draft entry for one component, built only from what its sources say. Gaps are marked, not filled, and every judgement call is listed for a person to check. It does not judge the design. Sibling links are relative to this skill's folder.

## Start from whatever the ask gives

A component name is enough. Find the code, stories and call sites yourself, and ask only for what no tool can reach. Of several named components, document the first and list the rest. A compound component (`Tabs` with `Tab`) is one entry. A part also used on its own gets a `### Parts` subsection under Description.

## When a coordinator calls it

A coordinator passes the code, the variant list and real or planned uses. Take them as given and run to the end without asking. Conflicts and Guessed at carry every open question, and the caller turns them and the Gates block into gates, each with a default.

Start the output with a status line, `Status: complete`, `Status: complete with NEEDS REVIEW (n)`, `Status: ready-with-gaps (<n> real uses)` or `Status: stopped: <condition>`, then `Commit: none`. A direct run uses the same status line. Return the entry with its blocks, or the stop shape, as text, and write no other file. The coordinator saves the entry, unless the brief's SCOPE names its path.

## Output

One Markdown entry, ready to paste, then these blocks outside it:

- Sources, one line per source, as `sources.md` records it.
- Conflicts, one line per disagreement: the fact, each source's version, and the quoted rule applied or "no rule, not chosen".
- Guessed at, one line per judgement call with what it rests on, or "Nothing guessed".
- Gates, only when a rule adds one: the question and its default.

On a direct run, save the entry with its blocks to `docs/system/<name>.md` with a draft comment on line 1, and write each missing example file (`doc-format.md`, Examples). The reply opens with that path, what the entry covers and its status. Then each command run with its exit code, any Defect lines, up to three open questions with defaults, and `Next:` with one prompt to paste. Every count in the reply comes from `grep -o` on the saved file below the draft comment.

The entry is ready when it passes the review checklist, and for a spec when `check-spec.mjs` exits 0 or every remaining failure is under Guessed at with why no source settles it.

## Stops

| Missing after searching | Why it stops | The coordinator does next |
|---|---|---|
| Code | Nothing else sources the variants, props or behavior | Pass the code path and rerun, or drop the component and log it as a gap |
| Variant list, from code or stories | A guessed variant list documents a different component | Pass the props type or stories and rerun, or park it as a gate for the owner |
| Any use, real or planned | Invented uses read like real ones, and readers copy them first | Build the pilot screen, or pass one screen from the brief as a planned use, then rerun. Never write the entry itself |

A props type with no variant prop is an empty list, so Variants reads "None" and the run continues. A stopped run returns the stop, the facts sourced so far by section, the next step, and the smallest reply that unblocks it. For missing uses, that is "one screen name, what put the component there, and which variant showed".

Everything else continues. One real use, planned uses and a deprecated predecessor follow `sources.md` (Fewer than two uses). Conflicts follow `sources.md` (Conflicts between sources), and a behavior that looks like a bug gets a `Defect:` line (`doc-format.md`, States). A missing props type, token list, spec, notes or accessibility guidance becomes `NOT SUPPLIED`, `NEEDS REVIEW` or a Guessed at line.
