---
name: fable-scope-discipline
description: Use when implementing any change in existing code — when tempted to clean up nearby code, add unrequested validation or options, fix something "arguably in scope", or when the diff is growing past what was asked.
version: 1.0.0
pack: build
inputs:
  - task_specification
  - current_diff
requires:
  - codebase_access
produces:
  - bounded_diff
gates:
  - no_unrequested_edits
  - right_altitude
fallback: fable-execute
mutatesWorkspace: true
parallelSafe: true
neural_links:
  precursors:
    - fable-plan
    - fable-execute
  continuations:
    - fable-verify
    - fable-review
  lateral_peers:
    - fable-native-code
  recovery: fable-recover
---

# Fable Scope Discipline

Build exactly what was asked, at the right altitude: deep enough to fix the cause, narrow enough to touch nothing else. Unrequested improvements are not generosity — they are unreviewed risk hiding inside someone else's diff.

## Purpose

Enforce strict scope boundaries during code modification. Prevent drive-by refactorings, cosmetic rewrites, speculative optimizations, unrequested validation checks, and diff bloat.

## When to Use

- When implementing any change in an existing codebase.
- When tempted to clean up neighboring functions, reformat whitespace, or rename variables.
- When thinking a secondary defect is "arguably in scope".
- When inspecting a diff that spans more files or lines than the task logically warrants.

## When NOT to Use

- When tasked explicitly with a broad refactoring or architectural migration (use `fable-simplify` or `fable-architecture`).
- When removing dead code or deprecated systems across the whole workspace (use `fable-simplify`).
- When authoring exploratory prototypes or spikes (use `fable-discover`).

## Inputs

- `task_specification`: The specific bounded task, user instructions, and acceptance criteria.
- `current_diff`: The working git diff generated during implementation.

## Expected Outputs

- `bounded_diff`: A minimal, surgical diff addressing only the authorized problem.
- `discovered_items_report`: A structured list in the summary noting other defects discovered but deliberately not touched.

## Procedure

1. **Implement What Was Asked**: Focus strictly on the assigned card or request; nothing speculative, nothing "while I'm here."
2. **Adjacency is Not Scope**: "Same function", "same file", "same class of defect" describe *location*, not *authorization*. The user's words define the task; proximity defines nothing.
3. **The Argument Test**: If you are constructing an argument for why something extra is "arguably part of the fix" — it is not. Real scope never needs an argument. Put the observation in your report and let the user decide.
4. **The Open-Question Test**: If an extra fix requires an unresolved design choice (raise vs clamp? rename to what?), that proves it is an independent task. You cannot settle a contract question inside someone else's bugfix.
5. **Right Altitude**: Not a symptom patch (one case patched, bug alive), and not a rewrite (bug fixed, fifty unrelated things changed). Fix the root cause within the bounded scope.
6. **No Drive-Bys**: No renames, reformatting, refactors, or dependency bumps the change does not require. Diff noise buries the real change.
7. **Touch Budget**: If the diff is significantly larger than the ask implies, stop and re-evaluate your altitude.
8. **Look Before Deleting**: If what you find contradicts the task's description or you didn't create it, surface that instead of blindly overwriting.
9. **Discoveries Go in the Report**: Real bugs, dead code, or stale docs found along the way go in your summary — neither silently fixed nor silently dropped.

## Decision Rules

| Thought | Reality |
|---|---|
| "It's the same class of defect as the bug I was sent in for" | Classification is taxonomy, not authorization. The user named one defect. |
| "It lives in the same function's contract" | Location again. Contracts change by decision, not by proximity to your cursor. |
| "Fixing one and not the other is fixing half of a coherent correctness problem" | The user defined the problem's boundary. Put it in the report and let them re-draw the boundary. |
| "That makes it a legitimate part of the fix, not scope creep" | The moment you're litigating whether it's scope creep, it is. |
| "Every one of these is an uncontroversial improvement" | Uncontroversial is not the bar; *asked-for* is. Improvements travel in their own reviewable diff. |
| "The user said they care about code quality" | A value statement, not a work order. Quality includes atomic, revertible, reviewable diffs. |

- If a code change is not required to make the user's scenario or test pass, revert it.
- If an adjacent bug is discovered, log it in the report as a follow-up item.

## Tool Policy

- Run `git diff` frequently to inspect touched lines and files.
- Reject tools that indiscriminately reformat entire files.
- Keep modifications confined to the minimal set of files.

## Evidence Requirements

- Inspect `git diff --stat` to verify that touched files and line changes match the expected blast radius.
- Verify tests pass on the minimal change without relying on unrequested collateral modifications.

## Failure Handling

Stop immediately and shrink the diff when encountering these Red Flags:
- The word "arguably" near a change you're about to make.
- Touched files outside the component's logical domain.
- Formatting changes on untouched functions in the same file.

## Completion Criteria

- Diff addresses the root cause of the assigned task with surgical precision.
- No unrelated files, styles, dependencies, or unrequested refactorings introduced.
- All secondary discoveries documented for future triage.
