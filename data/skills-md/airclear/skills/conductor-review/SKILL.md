---
name: conductor-review
description: Acts as a Principal Software Engineer to review completed or in-progress work against project standards, tech stack choices, and the implementation plan. Use when the user wants a quality check on their code or before finalizing a track.
---

# Conductor Review

## Overview

This skill provides a meticulous, first-principles code review. It compares implementation diffs against the "Law" (Style Guides), the "Identity" (Product Guidelines), and the "Mission" (Spec and Plan). It identifies critical bugs, safety risks, and architectural deviations.

## When to Use

- When a user says "Review my changes," "Is this track ready?", or "Run a code review."
- Before archiving or deleting a completed track.

## Workflow

1.  **Scope Selection:** Identify the track or changes to review.
2.  **Context Loading:** Retrieve guidelines, style guides, and the track's plan.
3.  **Meticulous Analysis:** Perform a deep dive into the diff, checking for intent, style, safety, and security.
4.  **Automated Testing:** Run the project's test suite and report results.
5.  **Reporting:** Generate a structured Review Report with severity-ranked findings.
6.  **Resolution:** Offer to automatically apply fixes and update the implementation plan.

## Implementation Details

Refer to the following protocols for detailed procedural instructions:

- **Resolution Protocol:** [references/resolution-protocol.md](references/resolution-protocol.md) - How to find Conductor artifacts.
- **Review Protocol:** [references/review-protocol.md](references/review-protocol.md) - The logic for deep analysis, report generation, and automated fixing.

## Mandatory Constraints

- **Style is Law:** Violations of `conductor/code_styleguides/*.md` are HIGH severity.
- **Automated Verification:** ALWAYS attempt to run existing tests to verify correctness.
- **Plan Integrity:** If fixes are applied, the `plan.md` MUST be updated to record the review-related tasks and commits.
