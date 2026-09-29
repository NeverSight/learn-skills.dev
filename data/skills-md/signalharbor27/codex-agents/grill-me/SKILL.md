---
name: grill-me
description: "Use when the user asks to be grilled or interviewed, or coupled user-owned choices materially affect the deliverable, acceptance criteria, or costly commitments; not for routine, factual, or settled choices."
---

# Grill me

## Overview

This skill owns the interview procedure in a local reference. An existing primary skill can load it when inspection reveals the trigger and retain ownership of the task.

## When to Use

- Coupled consequential product, scope, architecture, or behavior choices belong to the user, including plausible interpretations that change the deliverable or acceptance criteria while leaving coding technically possible
- The user asks to be grilled, interviewed, or interactively pressure-tested, including through `$grill-me`

## When Not to Use

- Keep routine choices, already-settled work, and one unresolved user-owned decision with the current primary skill
- Use the relevant research, review, or debugging skill when the unresolved issue is factual rather than a user decision
- Do not use it as an implementation skill or as authority to change files, branch state, external services, or live state

## Minimal Workflow

1. Read [the dependency-frontier grilling procedure](references/frontier.md) before asking a question or taking any other task action.
2. Follow the procedure within the user's authority. End a standalone interview with settled decisions. If another primary skill loaded it during authorized work, resume that work when decisions are settled. Ask only about unresolved consequential choices or missing authority; routine inferences do not require confirmation.

## Reference Routing

- Read [references/frontier.md](references/frontier.md) for every invocation
- Existing primary skills may load the same reference when inspection reveals its trigger; they retain primary ownership

## Failure modes

- Failing to invoke `grill-me` because the user did not use its name even though the work meets its trigger
- Invoking it for routine, factual, single-decision, or already-settled work
- Starting the interview before reading the procedure completely
- Duplicating or overriding the interview behavior in this entrypoint or a consumer skill
- Treating settled discussion as implementation authority or changing state under the interview's authority
