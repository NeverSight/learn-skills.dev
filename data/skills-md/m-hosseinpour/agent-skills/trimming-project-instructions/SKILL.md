---
name: trimming-project-instructions
description: Use when a project's instruction file — CLAUDE.md, AGENTS.md or whatever plays that role — has grown past what a session can hold, or when asked to shrink, split or reorganize one.
---

# Trimming Project Instructions

A project instruction file is loaded at the start of every session *in that project*. Its length is a tax paid there, on every task, whether or not the task touches the area a section covers.

**Core principle:** every section is either a **verdict** — a rule, a decision, a "do not re-open" — or **evidence**: how the verdict was reached. The verdict stays, with the shortest warrant that stops it being re-opened. The evidence — the gates, the measurements, the dates, the sequence — moves to a document.

## The one question

> Is this the verdict, or the evidence for it?

Adding without asking it is how the file grows. Trimming without asking it is how a rule disappears. Most sections are **half-live by construction** — a durable head and a narrative tail — so the work is *splitting* them, not relocating them whole.

**This is not the global file's problem.** There the destination is a skill, which loads on a trigger. Here the destination is a document, which nothing loads — so **the pointer is the trigger**, and **a moved rule nothing points at is a rule that gets re-derived**. (For the global tier, see `curating-global-instructions`.)

## The pointer rule

**A pointer names the trigger, never a bare "see Y".** *"Before touching X, read Y"* survives; *"see Y"* does not — the reader has no way to know they are in the situation Y covers.

## Mechanics

**Measure first.** Count characters per section, before and after. A section that "feels long" is not a measurement, and a total that moved without a per-section number cannot be reported.

**Extract mechanically.** Move text by line range or marker match with a script, never by retyping — thirty thousand characters retyped is thirty thousand chances to drop a clause.

**Verify every move.** Grep a distinctive sentence from each moved block in its destination. After a restructure, compare every substantive line of the old file against the new one and explain each absence.

**One destination per area**, and a table in the instruction file mapping each file to what it holds — that table is how a later session finds the evidence without reading the whole directory.

## Two operations, not one

**Splitting** is the per-section move above. **Regrouping** is the other, and it is worth doing deliberately: a file that grew a section at a time is organised by *when each thing was written*, not by what a session is looking for. That is how one heading ends up holding three unrelated concerns, how two headings end up holding the same kind of thing, and how a history comes to read as a rulebook. Group by what a session is looking for — what the project is, what is judged, what exists, what is decided, the rules, the settled work, the operations, the record map. **Regrouping is also what surfaces the defects, because moving a section is when a pointer breaks.**

## Where to stop

**The floor is where every remaining line is a rule, an invariant or a decided seam.** Past it, each character removed costs a rule, and a lost rule is not paid back by a shorter file. When a pass moves only a few hundred characters and every candidate left is a rule's own warrant, **stop and say so** — reporting the floor is the honest end of this work, not a failure to finish it.

## The defect class to hunt: dangling pointers

A move breaks four things, and no compiler catches any of them:

1. **A directional pointer that no longer points the right way** — "the section below" after the section moved above.
2. **A pointer to a heading the move deleted.**
3. **A cross-reference *inside* a moved block** that named its old neighbourhood — "removed above", "as noted earlier".
4. **An abbreviation or section number whose defining sentence was compressed away** — "§5d", "the ladder", "the second form".

Hunt all four deliberately after the pass; they are the failures this work actually produces.

## Do not weaken while compressing

A "never" can become a "prefer", a condition can drop, a scope can narrow — with no bullet deleted. **Check each prohibition by name after the pass**, and have an independent reader check the full diff when the change could weaken important rules. For small edits, compare the affected sections and verify the moved content directly.

## Common mistakes

| Mistake | Fix |
|---|---|
| Trimming by feel, or toward a target percentage | Measure per section; report the numbers |
| Deleting a rule because a document "covers that area" | Read the document — areas are not contents |
| Moving evidence and leaving no pointer | Name the trigger, or do not move it |
| Retyping moved prose | Extract it mechanically and verify it landed |
| Trusting the author's own read of the compression | Dispatch a reviewer against the whole diff |
