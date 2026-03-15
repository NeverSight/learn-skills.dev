---
name: cmd-pr-review-prepare
description: Prepare branch for code review by building context, identifying issues, and suggesting improvements
disable-model-invocation: true
---

# Code Review Preparation Agent

Your goal is to help me do a code review as we pick up work from a branch we worked on previously.

You are one of my code reviewing buddies for this branch.
Note that you may be one of several instances of Claude Code that I'm using in parallel to review this branch.

Along the way, don't hesitate to ask questions and build plans.
Be pragmatic.
Don't over engineer or write long unnecessary documentation.

## Goals

1. Do a code review
2. Build context on the current changes
3. Make cosmetic changes & improvements
4. Evaluate large changes and improvements
5. Build context for follow-on work we'll need to do

## Getting Started

1. **Build Context**
2. **Cosmetic Changes**
3. **E2E Test** - Evaluate the code

## Building Context

1. Do a git diff (excluding lock files and package.json)
   - If a `testnet` branch is available, do a `git diff testnet -- ":(exclude)*.lock" ":(exclude)package-lock.json" ":(exclude)pnpm-lock.yaml" ":(exclude)package.json"` and move on to step 2.
   - If a `staging` branch is available, do a `git diff staging -- ":(exclude)*.lock" ":(exclude)package-lock.json" ":(exclude)pnpm-lock.yaml" ":(exclude)package.json"` and move on to step 2.
   - If it is not, do a `git diff main -- ":(exclude)*.lock" ":(exclude)package-lock.json" ":(exclude)pnpm-lock.yaml" ":(exclude)package.json"` and move on to step 2.
2. Spend a couple of minutes building context on the changes made
3. Don't rush
4. Be thorough
5. If need be, look at code that's not in the diff, but related, and understand how it works

## Cosmetic Changes

1. Identify any cosmetic changes (typos, inconsistencies, improvements, etc)
2. Make them
3. Don't commit
4. Call them out, but don't spend too much time explaining it

## Code Cleanup & Architecture

Are there opportunities to:

1. Create new structures / classes?
2. Move new code into helper functions?
3. Move new code into a new file?
4. Etc...

Make sure:

1. Not to over-engineer
2. Not to optimize prematurely
3. Build a plan and share it
4. Ask questions for clarity
5. Don't make these changes without my approval
