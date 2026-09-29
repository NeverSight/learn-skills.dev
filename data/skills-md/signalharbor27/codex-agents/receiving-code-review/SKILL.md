---
name: receiving-code-review
description: "Use when handling review comments from people or tools, especially disputed or unclear feedback; not for initiating a review of a diff."
---

# Receiving code review

## Overview

Test review feedback against this codebase before accepting or rejecting it. The reviewer's confidence does not replace local evidence.

## When to Use

- Receiving review comments from people or tools
- Sorting valid feedback from context-free or incorrect suggestions
- Planning the order of review-driven changes

## When Not to Use

- Use `engineering` when the question is pure design or implementation, not review response

## Minimal Workflow

1. Identify the reviewer's technical claim and the user's existing authorization. During authorized implementation, terse follow-ups such as "PR review comments" request investigation, valid fixes, and verification. Preserve explicit review-only restrictions. Ask only about missing acceptance criteria or material scope, product, architecture, cost, destructive, or external effects.
2. Trace the relevant code, callers, tests, and contracts until the claim is confirmed or contradicted.
3. Classify the feedback as valid, invalid, or unresolved. Give the evidence and the smallest appropriate response.
4. Apply valid fixes within existing authority, transitioning to `engineering` as primary when implementation becomes the main task. Do not ask again for authorized work. Explain invalid feedback with evidence; isolate any unresolved decision while continuing independent authorized fixes.
5. Close the loop after proof covers accepted changes and evidence explains rejected feedback. Reuse recorded proof across turns when the tested code and relevant state are unchanged; rerun checks affected by a fix.

## Reference Routing

- Use `engineering` after feedback is validated and the main task becomes implementation.

## Failure modes

- Implementing feedback before checking the codebase reality
- Arguing with correct feedback instead of verifying it
- Agreeing reflexively instead of evaluating the feedback technically
