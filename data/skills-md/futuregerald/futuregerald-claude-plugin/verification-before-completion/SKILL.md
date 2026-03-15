---
name: verification-before-completion
description: Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming output before making any success claims; evidence before assertions always
tags: [workflow, quality]
languages: [any]
---

# Verification Before Completion

**Never declare work complete without running verification commands and confirming their output.** Evidence before assertions, always.

## Core Rule

Before claiming ANY of the following, you MUST run the relevant verification commands and confirm their output:

- "Tests pass"
- "The fix works"
- "Build succeeds"
- "Everything is green"
- "Ready to commit/push/merge"
- "Done" / "Complete" / "Finished"

## What Counts as Verification

**Acceptable evidence:**
- Running the test suite and seeing the output (pass count, zero failures)
- Running the build command and seeing "build succeeded" or equivalent
- Running typecheck/lint and seeing zero errors
- Reproducing the specific scenario that was broken and confirming it now works
- Running the specific test that was failing and confirming it now passes

**NOT acceptable evidence:**
- "I think this works based on the code I wrote"
- "This should fix it" (without running anything)
- "The logic looks correct" (code reading alone)
- Committing without running tests
- Declaring done because the implementation matches the plan

## Workflow

1. **Before claiming tests pass:** Run the test command. Read the output. Confirm zero failures.
2. **Before claiming a fix works:** Reproduce the original failure scenario. Confirm it no longer fails.
3. **Before claiming the build succeeds:** Run the build command. Read the output. Confirm no errors.
4. **Before committing:** Run tests + typecheck + lint. All must pass.
5. **Before creating a PR:** Run the full verification suite. Confirm CI-equivalent checks pass locally.

## Red Flags

Stop and verify if you catch yourself:

- Saying "I believe this works" without having run it
- Committing immediately after writing code
- Skipping tests because "it's a small change"
- Declaring a bug fixed without reproducing the original issue
- Saying "tests should pass" instead of "tests pass — here's the output"
- Trusting that your code is correct because it looks right

## The Mantra

**"Show me the output."** Every claim of completion must be backed by command output you have actually seen in this session.
