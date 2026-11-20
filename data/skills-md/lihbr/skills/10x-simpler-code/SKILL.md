---
name: 10x-simpler-code
description: Use when the user says "10x simpler", "simplify 10x", "distill", "condense", "shrink", or asks to make code radically simpler or more minimal. Code only. For PR descriptions, comments, or other prose, use 10x-simpler-prose.
argument-hint: "[path | staged | unstaged | branch | commit-range | PR#]"
---

# 10x simpler, for code

Rewrite the target so it is as small and as simple as it can honestly be. This is not a cleanup pass — question whether each function, layer, and file needs to exist at all.

## Resolve the target

If an argument is given, interpret it: a file or directory path, `staged`, `unstaged`, `branch` (diff vs the merge-base with the default branch), a commit range, or a PR number.

With no argument, pick the first that applies:
1. Staged changes, if any
2. Unstaged changes, if any
3. The branch diff vs the merge-base with the default branch

State the resolved target in one line before editing (e.g. "Distilling: branch diff vs main, 4 files") so a wrong guess is caught immediately.

## What "simple" means

Fewer concepts, not fewer characters. Line count is the score; comprehension is the constraint. A reader new to the file must understand it in one pass. Never code-golf: no dense one-liners, no ternary chains, no cleverness that trades clarity for lines.

In rough order of impact:

1. **Delete before rewriting.** Dead branches, unused parameters, speculative flexibility, config nothing sets, wrappers that wrap one thing, abstractions with one caller.
2. **Collapse layers.** Inline single-use helpers, single-use variables, and pass-through functions. An abstraction earns its keep only with multiple real callers today.
3. **Use the platform.** Prefer the standard library or an already-present dependency over hand-rolled machinery.
4. **Flatten.** Early returns over nesting. One obvious path over branching cleverness.
5. **Condense style.** Direct expressions, no intermediate names that add nothing, consistent with the surrounding codebase's idiom.

## Comments

Delete comments that restate the code. A comment survives only if it states a constraint the code cannot show (a *why*, an external quirk, a spec requirement). Before keeping one, try renaming or restructuring so it becomes unnecessary.

## Guardrails

- **Behavior preservation is non-negotiable.** Same public API, same observable behavior, same error handling. Never drop validation or error paths to save lines.
- Stay inside the target. If nearby code begs for the same treatment, list it as a suggestion — do not touch it.
- If a big win requires a behavior or API change, do not make it; report it as a suggested follow-up.
- After editing, verify: run the project's type-check or build, and its test suite if one exists and runs quickly. Report results honestly, including failures.

## Process

1. Read the full target and every file it touches — understand before deleting.
2. Do a deep reduction pass.
3. Re-read the result and ask "what is still removable?" Repeat until a pass changes nothing, max 3 passes. The second pass often finds collapses the first one created.
4. Verify (see guardrails).
5. Close with a short report: LOC before → after per file, total reduction, verification results, and any suggested follow-ups you deliberately did not apply.
