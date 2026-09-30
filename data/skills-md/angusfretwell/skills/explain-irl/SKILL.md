---
name: explain-irl
description: Explain a bug, edge case, limitation, or trade-off as a real-world scenario. Use when the user asks what one means in practice, or says they don't understand an explanation of one.
argument-hint: "[subject]"
---

A **scenario** follows one person in date order, until the reader sees what the subject does to them.

## 1. Pick the subject

Take the subject the invocation names. Otherwise take the last one raised in the session; when that message raised several, ask which with AskUserQuestion.

Done when one subject is named.

## 2. Cast and trace

Cast the **person** who feels the consequence, named in the project's vocabulary: a customer, an editor, a caller of the API. Give them a first name and a starting position in real units: a count, a size, a date. Invent the person and every value about them, even when real records are within reach.

Follow them down one path, or down several that differ in one thing:

- For a trade-off, one path per option.
- For a problem that bites only under some condition, the normal path beside the broken one.

**Trace** each path: run the person's inputs through the code that decides the outcome, and note what the system produces at each step. A number no code decides, such as how often the condition occurs, is **illustrative**; mark it so in the scenario.

Done when every number the system produces on each path is traced, and every other number is the person's invented input or marked illustrative.

## 3. Tell it

Tell the scenario in the conversation, as prose per `/humanize`. Bring the cause in at the moment it bites, in product terms: "the search index rebuilds overnight, so the listing she posts at 9am can't be found until tomorrow".

Bring in what fits the subject:

- When the system shows something wrong: what it shows beside what is true, what happens when they act on it, and whether the error is **loud** (someone complains) or **silent** (nobody reports a number that looks plausible).
- For a problem of uncertain reach, how often its condition occurs and how sure you are.

Done when the scenario ends on what happens to the person, and reads without the explanation it replaces.
