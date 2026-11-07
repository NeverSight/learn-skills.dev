---
name: splitting-task-descriptions
description: Use when a long task or issue description needs a concise team-facing version for estimation while preserving full requirements in a standalone developer guide.
---

# Splitting Task Descriptions

## Overview

The team text gives enough scope to understand and estimate the work, without carrying every implementation detail. The developer guide preserves the source's full useful detail. Neither document presents a choice as settled unless the source does.

## Process

1. **Read the whole source first.** Do not ask about anything the source already answers.
2. **Ask only about real ambiguity**, one question at a time, and say why it matters. For terminology, ask the user which task-specific terms should be defined; offer a short set of relevant terms from the source for the user to choose from.
3. **Write the team text** (plain text, in a code block when shown in chat):
   - The content itself is plain text, both in the `.txt` file and inside the chat code block. Use unadorned titles, blank lines, and simple hyphen or numbered lists. No Markdown headings (`#`), bold (`**`), italics, tables, inline backticks, or Markdown links. The outer code fence is for chat presentation only; never save it in the file. A `.txt` extension alone does not make Markdown content plain text.
   - **Shape, in this order:**
     1. Title.
     2. The main technology as its own short paragraph (not in the title, not in parentheses): two or three plain sentences saying what it is, that it is open source (if it is), what problem it solves and what building blocks it offers, so someone who has never used it can follow the rest. This is an explanation, not a proposed requirement; write it directly without "suggested", "not from the source", or any disclaimer about its origin.
     3. Goal: two or three sentences covering what is built and the base flow, with only the numbers that drive the work.
     4. Short bullets covering the major work areas. Group related topics when they answer the same question; do not reproduce the source's section structure. Use broad concepts instead of inventories of fields, metrics or checks. Retain a specific detail only when it changes how the team understands or estimates the work.
     5. Deliverables in one line.
     6. Acceptance criteria in the source's own wording.
   - **Test for every detail:** if it disappeared, would the team's estimate or understanding of the problem change? If not, it belongs in the developer guide, not here.
    - About 400 words is a recommendation, not a limit or a reason to reject the text. Judge clarity and estimating value, not word count alone.
    - Preserve the source's level of obligation when summarizing: examples remain examples, optional alternatives remain alternatives, and illustrative lists do not become exhaustive scope. A configurable required value or range remains required and configurable; do not relabel it as a "default" unless the source calls it a default. Do not turn an example number into a mandatory range or imply that a later extension belongs to the initial pipeline.
   - A requirement already stated by an acceptance criterion needs only a short clause in its topic bullet.
   - Define only the terms the user selected, at first mention, in a short parenthetical. Do not define unselected terms.
4. **Write the developer guide:**
   - The developer reading it has neither the source nor the team text. It is a self-standing document: no mention of the source file, "the source", "the original text", "the Jira text" or the writing process, and no preface explaining where it came from.
   - Restate every requirement, metric and deliverable from the source.
   - First judge whether the source is already detailed enough to guide development. If it is, reuse its content as the guide with only needed edits for clarity or organization (title, tone, wording that points back to the source); do not rewrite it from scratch.
   - If the source is sparse, expand its stated requirements with explanatory detail that helps developers understand or carry them out. Do not introduce new requirements, technologies, structures, formats, defaults, or treat an unstated choice as settled.
   - Present examples that come from the source as examples ("for example"). Mark your own additions as "suggestion". Neither label mentions the source.
   - Analysis and questions are allowed. Choices are not.
   - Each requirement appears in one place, not repeated across sections.
5. **Review (mandatory)** with one independent subagent, using the brief below.
6. **Apply fixes with targeted edits**, not full rewrites.
7. **Save** next to the source file as `<name>-team.txt` and `<name>-developer-guide.md`, unless the user names other paths.

## Review Brief (mandatory, bounded)

Give the reviewer the source path, the two document paths, the user's terminology selections and any other agreed constraints. Have it read this skill's Process section before reviewing, so the author and reviewer use the same output contract. Apply these checks only:

- **A. Missing:** the developer guide independently contains every requirement, deliverable, metric and acceptance criterion in the source. Report the source section and the gap in the guide. The team text deliberately omits detail: do not ask to restore field lists, metric lists or test sub-cases there merely because the source contains them. Flag an omission in the team text only if it hides scope necessary to understand or estimate the work, and explain that effect.
- **B. Added:** flag an invented requirement or an unstated implementation choice presented as settled, including examples promoted to requirements, required configurable values relabelled as defaults, illustrative lists made exhaustive, and later extensions presented as initial scope. Explanations of the main technology and user-selected terminology are authorized, not new requirements; do not request "suggested" or "not from the source" labels for them. A suggestion label does not make an invented requirement acceptable.
- **C. Team text:** practical for estimation; related topics grouped at concept level rather than a miniature copy of all source sections; actual plain-text content in the file and chat code block (no `#` headings, `**` bold, italics, tables, inline backticks or Markdown links; simple hyphen and numbered lists are allowed); main technology explained in its own opening paragraph without parentheses or origin disclaimers; only user-selected definitions; acceptance meaning preserved; avoid unnecessary repetition. Length is advisory, not a pass/fail threshold. Markdown in the team text is a format defect, not an out-of-scope style preference.
- **D. Developer guide:** standalone, with no references to unavailable source files or commentary about the splitting process. Reusing an already complete source is valid; do not require rewriting or adding material to justify a separate guide.

Out of scope, and say so in the brief: writing style, spelling, character spacing, reformatting, and checking external technical facts. If a fact looks wrong, list it under "unverified" in one line and do not research it.

**Output:** report only real problems, grouped by check letter, each with the quoted phrase and a one-line fix. Skip what is fine. No preamble, no restating the documents, end with a one-line verdict.

## Review Rounds (at most two)

- **Round one:** the full brief above.
- **Round two (only if round one found problems you fixed):** if your environment can resume the same reviewer with its earlier context, do that; otherwise start a fresh reviewer. Either way, point it at the sections you changed and their matching source sections only, and say what you changed. Do not ask for a full re-audit.
- After round two, do not start a third review. List any remaining points to the user in a short list.

## Common Mistakes

| Mistake | Effect | Fix |
|---|---|---|
| Keeping every number from the source in the team text | Team reads detail it cannot use | Keep only numbers that change the estimate or the understanding |
| Treating the word target as a hard cap | Useful estimating detail gets cut | Keep to the shape; each detail passes the estimate test |
| Replacing dense paragraphs with many detailed bullets | Same excessive detail, only spread out | Group related work and retain only estimate-relevant specifics |
| One paragraph per source section naming every sub-item | Team cannot scan it | Summarize major work areas, not the source's table of contents |
| Technology definition squeezed into the title or a parenthetical | Reader gets one clause and still does not know the tool | Own opening paragraph, two or three plain sentences |
| "Suggested, not from the source" label on a technology definition | Makes an explanation look like a proposed requirement | Explain the technology directly, without an origin disclaimer |
| Restating acceptance criteria inside the topic bullets | Same requirement twice | Short clause in the bullet, full wording in the criterion |
| Developer guide that opens with "this guide is based on file X" | The developer does not have file X | Self-standing document, no preface about its origin |
| Reviewer restores all source detail to the team text | Undoes the summarization | Share the Process section and distinguish full guide coverage from estimate-relevant team scope |
| Open-ended "check everything" brief | Long tables, style nitpicks, unrequested fact checks | Use the scoped checks and the output rule |
| Full re-audit in round two | Doubles the time for the same ground | Verify only changed sections |
| Third review round | Reviewer always finds something; the loop never ends | Stop after round two and report to the user |
| Rewriting whole documents after each finding | Re-introduces issues, forces another review | Use targeted edits |
| Adding a "helpful" default (tech, folder layout, sample values) | Guide decides what the team should decide | Do not add it |
| Same requirement stated in several sections | Longer text and inconsistent wording over time | State it once per document |
