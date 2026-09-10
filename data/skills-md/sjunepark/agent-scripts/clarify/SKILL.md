---
name: clarify
description: "Clarify a task's omitted intent and consequential unknowns before work. Explicit request only."
---

# Clarify

Treat the request supplied in the same prompt as `$clarify` as the agenda. A prompt is a compressed map of what the user wants; recover the intention and consequential unknowns this map leaves out before entering the territory.

## Find Load-Bearing Unknowns

1. Make the request in the invoking prompt the entire agenda. Use earlier conversation and workspace context only to interpret that request, avoid repeated questions, and investigate facts.
2. Identify only gaps whose answers could materially change the goal, scope, approach, constraints, or success criteria.
3. Use the unknowns lens selectively:
   - **Known unknowns:** ask directly about gaps the user already recognizes.
   - **Unknown knowns:** offer concrete alternatives or examples the user can react to when their criteria are easier to recognize than describe.
   - **Unknown unknowns:** briefly explain consequential blind spots found in the environment or domain before asking what they imply for the task.

Treat this lens as a way to find load-bearing questions, not as a checklist to exhaust. If the request is already well specified, move to a compact readback with at most one consequential question.

## Stay at Intent Altitude

Clarify the motivation, desired outcome, scope boundaries, hard constraints, priorities, quality bar, and success criteria.

Leave stacks, libraries, patterns, naming, file layout, algorithms, and other implementation choices to the implementer. Ask about a technical choice only when it is externally visible, hard to reverse, or one the user has signaled they want to own.

## Ask Efficiently

1. Anchor each round with what is already understood and why the remaining questions matter.
2. Ask a small group of tightly related questions. Include concise background when the user needs it to answer well.
3. Ask only questions whose answers change the task. Use a structured question tool for genuinely enumerable choices when available; otherwise use numbered plain text.
4. Follow an answer when it conflicts with earlier context, changes the task, or exposes another load-bearing unknown. Stop following the branch when what remains is implementation-level or cheap to reverse.

## Confirm the Recovered Intent

Stop asking when you can state the user's goal, motivation, scope, constraints, and success criteria in words they are likely to endorse.

Give a compact readback and label consequential assumptions. Treat clear answers
and established constraints as settled. Ask for confirmation or correction only
where the readback introduces an unresolved consequential assumption or changes
the understood intent. Once those gaps are resolved, proceed with the original
authorized task. When clarification itself is the request, the settled readback
is the deliverable.
