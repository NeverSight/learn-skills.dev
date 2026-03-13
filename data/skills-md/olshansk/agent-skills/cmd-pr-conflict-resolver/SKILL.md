---
name: cmd-pr-conflict-resolver
description: Resolve merge conflicts systematically with context-aware 3-tier classification and escalation protocol
disable-model-invocation: true
context: fork
agent: general-purpose
---

# Resolve Merge Conflicts <!-- omit in toc -->

Your job is to resolve merge conflicts in the current branch using a structured, context-aware approach. You resolve what you can confidently, explain your reasoning for non-trivial resolutions, and escalate when the correct behavior is ambiguous.

- [1. Verify State](#1-verify-state)
- [2. Map All Conflicts](#2-map-all-conflicts)
- [3. Build Context Per Conflict](#3-build-context-per-conflict)
  - [3a. Read the full file](#3a-read-the-full-file)
  - [3b. Trace commit history on both sides](#3b-trace-commit-history-on-both-sides)
  - [3c. Examine surrounding code](#3c-examine-surrounding-code)
  - [3d. Check cascading implications](#3d-check-cascading-implications)
  - [3e. Assess business logic impact](#3e-assess-business-logic-impact)
- [4. Classify Each Conflict (3-Tier System)](#4-classify-each-conflict-3-tier-system)
- [5. Resolve by Tier](#5-resolve-by-tier)
  - [Tier 1: Auto-resolve](#tier-1-auto-resolve)
  - [Tier 2: Resolve with type-specific guidance](#tier-2-resolve-with-type-specific-guidance)
  - [Tier 3: Escalate](#tier-3-escalate)
  - [New code escalation](#new-code-escalation)
- [6. Verify and Stage](#6-verify-and-stage)
- [7. Reflection and Handoff](#7-reflection-and-handoff)

## 1. Verify State

Assume I already ran `git merge` and there are unresolved conflicts.

- Run `git status` to confirm conflicts exist
- Identify the merge target via `git rev-parse MERGE_HEAD` (or `REBASE_HEAD` / `CHERRY_PICK_HEAD` as applicable)
- Run a baseline diff between both sides, excluding lock/generated files:

```bash
git diff MERGE_HEAD...HEAD -- ":(exclude)*.lock" ":(exclude)package-lock.json" ":(exclude)pnpm-lock.yaml"
```

This gives you the big picture before touching individual conflicts.

## 2. Map All Conflicts

Inventory every conflict before resolving any of them.

```bash
git diff --name-only --diff-filter=U
```

```bash
rg "<<<<<<< " --line-number
```

- Create a task list with one entry per conflict chunk, grouped by file
- Note patterns across the conflict set:
  - Same subsystem? Paired changes? Generated files?
  - How many conflicts total? Are they concentrated or spread across the codebase?

## 3. Build Context Per Conflict

For **each** conflict, before classifying or resolving:

### 3a. Read the full file

Not just the markers. Understand the function/block's role in the file.

### 3b. Trace commit history on both sides

```bash
git log --oneline MERGE_HEAD -- <file>
git log --oneline HEAD -- <file>
```

Read commit messages and diffs to understand **intent** on each side.

### 3c. Examine surrounding code

Read 20-40 lines around the conflict. Identify invariants:

- Ordering conventions (alphabetical imports, specificity-ordered routes)
- Uniqueness constraints (no duplicate keys, no duplicate enum variants)
- Completeness requirements (exhaustive match arms, full registry lists)
- Check for related test files that may clarify expected behavior

### 3d. Check cascading implications

If the conflict is in a signature, type, constant, or export:

```bash
rg "<symbol_name>" --type-add 'src:*.{ts,py,go,rs,java}' -t src
```

Find all usages to identify downstream impact.

### 3e. Assess business logic impact

Answer three questions for each conflict:

1. **Scope**: Mechanical (formatting/imports/whitespace) or runtime behavior change?
2. **Risk**: If resolved wrong, what breaks? (nothing / tests / production / data integrity)
3. **Novelty**: Both sides added new behavior? Or one cleanly supersedes the other?

## 4. Classify Each Conflict (3-Tier System)

| Tier                                    | When                                                                                                                                                    | Action                                                                                                                                     |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| **Tier 1 -- Auto-resolve**              | Non-overlapping additions, formatting-only, one side is strict superset, lock/generated files                                                           | Resolve immediately. No developer input needed.                                                                                            |
| **Tier 2 -- Resolve + state rationale** | Intent is inferable from context, combining both is clearly right but requires care, test file conflicts                                                | Resolve, then present rationale (see format below). Don't block on confirmation.                                                           |
| **Tier 3 -- Escalate before resolving** | Can't determine correct behavior from context, critical path code, silent behavior discard, architectural divergence, cascading multi-file implications | **Stop.** Show conflict, explain both sides' intent, state the ambiguity, offer 2-3 options with trade-offs. Wait for developer direction. |

**Tier 2 rationale format:**

> Resolved `file:line`. [How]. Rationale: [why]. Flag if wrong.

**Key balance**: Tier 1 keeps you decisive. Tier 3 keeps you consultative when it matters. Tier 2 handles the middle ground -- resolve but make reasoning visible.

## 5. Resolve by Tier

### Tier 1: Auto-resolve

- Edit the file to the desired final state
- Remove all conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`)
- Verify the result is syntactically clean

### Tier 2: Resolve with type-specific guidance

Apply the right merge strategy based on the construct type:

**Lists/registries** (imports, exports, routes, enum variants):

- Union both sides, deduplicate
- Maintain the file's existing ordering convention (alphabetical, grouped, etc.)

**Function bodies** (both added branches/conditions):

- Include all additions
- Respect ordering by specificity (more specific before more general)

**Config/struct** (both added keys):

- Merge all keys
- If the same key has different values, escalate to Tier 3

**Parallel new code** (both added new functions/classes):

- Include both
- Order consistently with the file's existing conventions

**After combining**: Re-read the result as a human would. Check for:

- Duplicated side effects
- Broken invariants (ordering, uniqueness, completeness)
- Mismatched types or signatures

### Tier 3: Escalate

- Show me the conflicting chunks with surrounding context
- Explain what each side intended (based on commit history from step 3b)
- State the specific ambiguity ("Both sides modify the retry logic but with different strategies")
- Offer 2-3 resolution options with trade-offs
- **Wait for my direction before editing**

After receiving direction:

- Restate your plan in one sentence before editing
- Re-evaluate remaining Tier 2 conflicts if new context was revealed

### New code escalation

When neither side's code is complete and the right answer is a **third implementation** (not just combining both):

- Flag it explicitly with a 3-5 bullet plan describing the proposed implementation
- Wait for approval before writing

## 6. Verify and Stage

After all conflicts are resolved:

```bash
rg "<<<<<<< "
```

Confirm zero remaining conflict markers.

- Run lint/type-check if fast (skip slow integration tests)
- Stage resolved files individually: `git add <specific_files>` -- **not** `git add .`
- **Do not commit** -- leave that to me

## 7. Reflection and Handoff

Provide a summary table:

| File | Line(s) | Tier  | Resolution        |
| ---- | ------- | ----- | ----------------- |
| ...  | ...     | 1/2/3 | Brief description |

Flag any of the following:

- Tier 2 resolutions where your confidence was lower than usual
- Cascading implications found during step 3d
- Architectural divergence detected between the two sides
- Files that weren't in the conflict set but may be affected by the merge

Closing question: **Are there areas of the codebase this merge could affect that aren't in the conflict markers?**
