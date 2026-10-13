---
name: intentional-craft
description: "Develop or refine design and engineering ideas through Apple's Intention film: connect a human outcome to focused scope, implementation choices, and evidence of craft. Use when this lens is requested or a substantial idea needs an experience-led direction."
license: MIT
---

# Intentional Craft

Make the intended human experience a decision criterion from the first idea through the working result. This skill translates Apple's 2013 *Intention* film into contemporary design engineering practice. It does not prescribe an Apple visual style or claim to document Apple's internal process.

Read [source and translation notes](references/source-and-translation.md) when discussing the film, its wording, or the origin of a principle. The working method below is an editorial interpretation, not instructions quoted from Apple.

## Establish the intention

Infer the person, task, context, and constraints from the request and available work. Identify the practical outcome and the feeling it should support. Confidence, agency, relief, curiosity, or connection may fit; surprise is not desirable in every task.

Turn the feeling into an observable design promise. For example: someone finishing an important edit should know whether it is saved and how to recover if saving fails. Emotional intent without a behaviour that supports it is too vague to guide the work. Do not claim to have measured a feeling through a screenshot or a passing test.

Use the existing brief when it supplies this direction. Ask only when an unresolved choice would materially change the result. Scale the method to the task; a precise local edit does not require a new manifesto.

## Choose what deserves attention

Evaluate an idea against the intended experience, its frequency or consequence, and the cost of building and maintaining it. Prefer a coherent experience that fulfils the task over a larger set of incomplete promises.

For material choices, explain what earns inclusion and what can be deferred. A useful rejection names the competing user benefit, attention cost, or complexity it avoids. Do not manufacture a quota of rejected ideas or remove a requirement to make the result look simpler.

Compare the strongest plausible approaches when the choice is genuinely open. Keep the user's platform, brand, useful information density, and established conventions. More options can help experts; fewer options can obstruct them. Judge the quality of choice by what people can understand and accomplish.

## Carry the intention into construction

Trace the human promise into the design and engineering decisions that make it credible:

| Intended experience | Supporting decisions | Evidence to seek |
| --- | --- | --- |
| Confidence that work is safe | Accurate saving states, preserved input, and recoverable failures | Observe a successful save and an interrupted or failed save |
| Agency during a long operation | Understandable progress, cancellation where feasible, and an honest account of partial effects | Interrupt the operation and inspect the resulting state |
| Clarity when choosing | Meaningful labels, comparable information, and a useful default where appropriate | Walk through a representative decision using real content |
| Continuity across a task | Stable identity, retained context, and consistent state meanings | Leave and return, resize, or change input method as relevant |

These are examples, not mandatory features. For an API, workflow, or architecture idea, make the same connection through understandable contracts, predictable failure behaviour, and the effort imposed on its consumers. Internal elegance earns its place when it supports useful behaviour or maintainable delivery.

Inspect the seams: input to feedback, local state to persisted state, one screen to another, and a component to its other uses. Typography, layout, copy, motion, semantics, and runtime behaviour should support the same promise. Spend effort where a mismatch has a meaningful effect; invisible implementation complexity is acceptable when it makes use simpler and remains maintainable.

## Refine with a purpose

Prototype the uncertain experience before investing in a large implementation. Exercise the central task with representative content and the conditions most likely to challenge the promise. Change the responsible design or implementation, then recheck that task.

Simplify actual effort, ambiguity, or fragility. Retain labels, affordances, confirmation, and recovery when people need them. Restart a direction when evidence shows its premise is wrong; do not discard sound work because a new aesthetic is more exciting.

Allocate refinement by consequence and uncertainty. Stop when the agreed outcome is supported, the relevant checks pass, and further changes offer little benefit within the task's constraints. Record consequential limits rather than implying perfection.

## Deliver an accountable result

Match the deliverable to the request. An ideas request should receive concrete proposals, tradeoffs, and the cheapest useful experiment. A review should receive evidence and recommendations. An implementation request should receive scoped changes and verification.

Explain the intended experience, the consequential decisions, and the evidence that supports the result. Distinguish what was observed from what remains a hypothesis. For any reported bug, give a credible consumer use case, prerequisites and reproduction steps, expected and actual behaviour, and impact; do not claim reproduction without executing it.

Readiness means meeting the task's quality bar with honest evidence. It does not authorise publication or deployment.
