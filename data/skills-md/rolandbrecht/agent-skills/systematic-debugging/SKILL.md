---
name: systematic-debugging
description: Trigger this AUTOMATICALLY anytime you encounter a stack trace, test failure, production bug, or unexpected behavior. Do NOT guess the fix or propose code changes before explicitly triggering this skill. This skill mandates a strict data-gathering and hypothesis phase before you are permitted to edit ANY source code.
---

# Systematic Debugging

## Overview

Random fixes waste time and create new bugs. Quick patches mask underlying issues. As an AI agent, it is tempting to rapidly guess the solution based on symptoms because it is fast. **You must resist this temptation.**

**Core principle:** ALWAYS find the root cause before attempting fixes.
**The Iron Law:** NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.

## When to Use

Use for ANY technical issue:

- Test failures
- Bugs in production or local development
- Build or CI pipeline failures
- Unexplained performance issues

**Do not skip this process even if:**

- The issue seems "simple" or "obvious"
- You are under time pressure
- The user asks for a "quick fix"

---

## Phase 1: Planning (Root Cause Investigation)

**BEFORE attempting ANY code modification or fix:**

1. **Information Gathering (Do Not Guess)**
   - Read the error message and stack trace completely. Note the exact file paths and line numbers.
   - Use `view_file` to read the surrounding code where the error occurred.
   - Use `grep_search` to find definitions, usages, or configurations related to the failing components.
   - *Never* assume you know what a file contains without checking or listing its directory.

2. **Reproduce and Isolate**
   - Can you trigger the bug reliably? If there isn't an existing test, write a minimal, standalone reproduction script (e.g., `repro.py` or `.js` in `/tmp/`) using `write_to_file` and then execute it via `run_command`.
   - If you cannot reproduce it locally, you must gather more data. Do not guess the fix.

3. **Map the Boundaries (Multi-Component Systems)**
   - If the system has multiple layers (e.g., Frontend → API → Database), do not guess which layer failed.
   - **Inject telemetry temporarily:** Use `replace_file_content` to add `console.log`, `print()`, or logger statements at the boundary of each component.
   - Run the system once to see exactly what data entered and exited each layer.

---

## Phase 2: Execution (Hypothesis & Minimal Fix)

**Once the root cause is proven (not guessed):**

1. **Form a Single Hypothesis**
   - You must explicitly state your hypothesis before editing code. (e.g., "I hypothesize the root cause is that `user_id` is being passed as a string from the API layer, but the database ORM requires an integer.")

2. **Test Minimally**
   - Make the SMALLEST possible change to test your hypothesis.
   - Change exactly one variable at a time using `replace_file_content`.
   - Do not bundle formatting refactoring, "cleanups," or unrelated typo fixes into this bug fix.

3. **Verify the Fix Against the Reproduction Script**
   - Run the failing test case or the reproduction script you built in Phase 1.
   - If it passes *without* breaking adjacent tests, you have proven resolution.

---

## Phase 3: Verification (The "3 Strikes" Rule)

1. **Verify the Fix**
   - Did your minimal change resolve the issue?
   - Did it break any adjacent tests in the suite?

2. **If the Fix Failed: REVERT & STOP**
   - Undo your change immediately. Do not stack fixes on top of failed fixes.
   - Re-evaluate your hypothesis based on the new failure.

3. **The 3 Strikes Rule (CRITICAL)**
   - If you have attempted 3 different fixes and the system is still failing, **STOP CHANGING CODE IMMEDIATELY.**
   - You are likely fighting a fundamental architectural flaw, an incorrect underlying assumption, or a hallucinated dependency.
   - You must write a summary of the failure modes (e.g., in a `/tmp/bug-report.md`) and notify the user for an architectural alignment discussion. *Do not keep guessing silently.*

---

## Red Flags (When to STOP and Restart Phase 1)

If you catch yourself doing any of the following, you are violating the systematic debugging protocol. STOP and return to Phase 1:

- *"Quick fix for now, investigate later"*
- *"Let me just try changing X and see if it works"*
- Proposing solutions without having read the file contents where the error originated.
- Applying 3 or more unrelated changes in a single fix attempt.
- Encountering a *new*, completely unrelated bug every time you fix the previous one (indicates fundamental architectural rot).
