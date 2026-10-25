---
name: design-spec-intake
description: "Reads design material before implementation (decision documents, requirements, token definitions, state and behavior specifications, layouts, copy) and reports what is decided, proposed, open, conflicting, or missing, and what can be built now. Use when implementation is about to start from design artifacts, or when a handoff must be checked for build-readiness."
---

# Design Spec Intake

## Purpose
Turn design material into a build-readiness report so implementation starts only on decided items and every gap becomes a question or a labeled assumption instead of a guess.

## When to use
- Use when: implementation of a screen, component, or flow is about to start from design artifacts.
- Use when: a design handoff arrived and it is unclear whether it is complete or consistent.
- Do not use when: no design material exists. Define requirements first.
- Do not use to judge design quality or to fill gaps. Deciding belongs to the people who own the design.
- Pairs with: `design-to-implementation-qa` checks the finished build against the same material.

## Inputs
- Required: the design material in scope, in any form (decision documents, requirements, token definitions, state and behavior specifications, layouts, copy), and what is to be built.
- Optional: supported browsers and devices, codebase conventions, existing components and tokens, a previous intake report.
- Assumptions: anything the material does not state is reported as missing. It is not filled in.

## Process
1. Inventory every artifact: name, scope, status (approved, draft, unknown), and version or date when given.
2. Extract the items that affect the build, grouped as structure and content, components and variants, visual values, states, behavior and interaction, responsive behavior, accessibility requirements, and copy. Cite the source of each item.
3. Give each item one status: **decided** (an authoritative source states it), **proposed** (draft or suggestion), **open** (explicitly undecided), or **missing** (needed to build and absent).
4. Find conflicts, both between artifacts and within one, such as a value that differs between a layout and a token file, or a state in a flow that no state specification covers. Record both sources.
5. Check coverage of what a build always needs: states beyond the ideal case, behavior at other viewport sizes and zoom, keyboard interaction, long, empty, and missing content, error and loading behavior, and each required theme.
6. Match decided items to existing components and tokens when the codebase is known. Mark them as reuse candidates and do not redesign them.
7. Rank each unresolved item as **blocking** (the affected part cannot be built), **risky** (can be built on an assumption that is costly to reverse), or **minor** (cheap to change later). Write one question for each, with an owner when known.
8. List what can be built now using only decided items.

## Rules and heuristics
- Required: never fill a gap with an invented value, state, behavior, or text. A default may be offered only as a labeled proposal and is not built until approved.
- Required: separate what a source says from what it implies. An implication is an inference, labeled with its reasoning.
- Required: a layout image or mockup shows one state at one size. Do not generalize it to other states, sizes, or behavior.
- Required: values read by eye from an image are unmeasured. Ask for the source value, or record the value as approximate and unverified.
- Recommended: raise the fewest questions that unblock the work, grouped by owner.
- Recommended: treat approved material as authoritative over drafts, and say when two statuses conflict.

## Checks
- Every in-scope artifact appears in the inventory, and every extracted item cites a source.
- Every item has exactly one status, and every conflict names both sources.
- Every blocking item has a question, and the build-now list contains only decided items.
- No value, state, or text in the report came from guessing. Inferences and proposals are labeled.

## Output
Return the readiness report: inventory, decided items by group, conflicts, gaps with rank and question, labeled proposals, reuse candidates, the build-now scope, and assumptions. Use the [readiness report](templates/readiness-report.md).

## Completion criteria
- An implementer can start on the build-now scope without rereading the originals.
- Every gap has a question or a labeled assumption.
- Nothing is presented as decided that the sources do not support.
