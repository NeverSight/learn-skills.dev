---
name: component-docs
description: Use to write one component's documentation entry from its code, stories and real call sites, such as "document the button", "write docs for Select", "what states does Toast have", or usage rules for a new or changed component. Not for foundations or pages that span components, which no skill here writes, nor for changing the component, which is build-design-system.
---

# Component docs

A draft entry for one component, built only from what its sources say. Gaps are marked, not filled. It does not judge the design and it publishes nothing. The heading order and a worked example are in `references/doc-format.md`.

## Steps

1. Paste the nine headings from `references/doc-format.md` into the draft, empty.
2. Find the component. Read its code, props type, styles and stories, and record each as a Sources line.
3. Find two real uses, by call-site search or from the ask. One real use or none changes the stop table below.
4. Trace which source gave each example, variant, prop, state and token. Every disagreement between sources is a line under Conflicts, with the quoted rule that settles it, or "no rule, not chosen".
5. Fill each section from sourced facts, copying token names and example code character for character.
6. Write Usage rules last. Each rule is `rule/<component>-<slug>`, a condition, an action, a reason, its evidence (two call sites, a measurement with its path, a named principle, or the person's words), and a `Don't:` line with real code that breaks it. A rule you cannot break with a snippet is cut.
7. Fill Guessed at, one line per judgement call. Reread the draft against the Done list below.

## Output

The entry, then Sources, Conflicts, Guessed at, and Gates (a question with its default) only where a rule adds one. Run on its own, it saves to `docs/system/<name>.md` with a draft comment on line 1 and writes each missing example file. The reply opens with the path, what the entry covers and its status, then up to three questions with defaults and one prompt the person can paste to take the next step.

## Stops

| Missing after searching | Why it stops |
|---|---|
| The code | Nothing else sources the variants, props or behaviour |
| The variant list (props type or stories) | A guessed list documents a different component |
| Any use, real or planned | Invented uses read like real ones and readers copy them first |

A props type with no variant prop is an empty list. Variants reads "None" and the run goes on. One real use, planned uses and a deprecated predecessor are marked as such, not stopped on. A stopped run returns the stop, the facts sourced so far by section, and the smallest reply that unblocks it ("one screen name, what put the component there, and which variant showed").

## Rules

- Never write a variant, prop, token name, example or use that has no listed source. A planned use says planned.
- Never invent a state or a precedence order to make a section look complete.
- A behaviour that looks like a bug is written as it is, followed by a `Defect:` line to the owner with what goes wrong for the user and the smallest fix.
- A part also used on its own gets a `### Parts` subsection under Description. A compound component (`Tabs` with `Tab`) is one entry.
- Do not edit the code, stories or spec being documented.
- Counts in the reply come from `grep -o` on the saved file, below the draft comment.

## Done

Every variant, prop, token and example has a Sources line. Every Usage rule has evidence and a `Don't:` line. Every conflict is shown. The nine headings are present in order, and a section with nothing sourced reads `Not applicable: <reason>`.
