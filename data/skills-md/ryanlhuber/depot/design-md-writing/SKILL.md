---
name: design-md-writing
description: "Writes a DESIGN.md, a single Markdown file stating a product's visual and interaction decisions so designers and AI agents build consistent interfaces from it. Use when a project needs its design decisions recorded in one readable, checkable file."
---

# DESIGN.md Writing

## Purpose
Produce a single Markdown file that states a product's visual and interaction decisions and tells a reader, human or AI agent, how to apply them, so interfaces built from it are consistent without rereading the sources.

## When to use
- Use when: a project has design decisions (tokens, components, voice) spread across files, tools, or heads, and needs one authoritative document.
- Use when: an existing DESIGN.md is out of date, contradicts the product, or is too vague to act on.
- Do not use when: the token values themselves do not exist yet and must be defined first; record that gap instead of inventing values.

## Inputs
- Required: the decisions to document (a token set or the visual values in use) and what the product is and who uses it.
- Optional: brand and voice material, component inventory, accessibility targets, platform and theme scope, an existing DESIGN.md, known inconsistencies.
- Assumptions: any value or rule not found in the inputs is marked as proposed, never presented as established.

## Process
1. Identify the readers (designers, developers, AI agents) and the decisions they most often get wrong. Scope the file to those.
2. Inventory the sources and note conflicts between them.
3. Write the overview: what the product is, who it serves, and the three to five principles that settle design disputes.
4. Document each foundation by role, not raw value alone: color roles, type scale, spacing, shape, elevation, and motion, with the value, its purpose, and where it must not be used.
5. Document component rules: which foundations a component uses, its states, and permitted variations.
6. State voice and interface-text rules only where the inputs support them.
7. State accessibility requirements as testable conditions, with the standard and level.
8. Write do and don't pairs for the highest-risk mistakes, and a short instruction block telling an agent how to use the file, including what to do when a decision is missing.
9. Record ownership, the process for changing the file, open questions, and proposed values awaiting confirmation.

## Rules and heuristics
- Required: every value and rule traces to a source or is labeled proposed. Do not describe aspiration as current fact.
- Required: separate requirements (binding), conventions (default), and preferences (flexible), and label each rule.
- Required: express decisions as capabilities and values, not as a particular framework, library, or tool. Stack-specific mapping belongs outside this file.
- Required: where sources conflict, report the conflict and the choice made, not a silent merge.
- Recommended: keep the file short enough to read in full; link to detail instead of copying it.
- Recommended: phrase agent instructions as checkable actions ("use a color role, not a raw value").

## Checks
- Every value matches its source or is marked proposed.
- Every rule can be checked by looking at a design or build.
- Contrast and size requirements are stated for the text and interactive pairings that matter.
- No two rules contradict each other.
- Omitted sections are listed with the reason.

## Output
Return the DESIGN.md, plus a list of proposed values, source conflicts and how they were resolved, assumptions, and open questions. Use the [DESIGN.md template](templates/design-md.md).

## Completion criteria
- A reader with only the file can apply the product's visual decisions, or knows the file is silent and what to do.
- Proposed and established content are distinguishable throughout.
