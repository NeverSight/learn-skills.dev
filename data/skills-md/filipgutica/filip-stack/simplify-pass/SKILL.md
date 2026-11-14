---
name: simplify-pass
description: Simplify the selected code while preserving its behavior, after three independent read-only reviews. Manual only, so invoke it with `/simplify-pass` or `$simplify-pass`.
disable-model-invocation: true
---

# Simplify Pass

Run only when the user invokes this skill. Improve clarity and remove needless complexity in the selected code without changing observable behavior.

## Scope and baseline

Use the target or range supplied with the invocation. Otherwise use code changed in the current task; if that is unclear, inspect staged and unstaged changes and relevant untracked files. Keep unrelated changes out of scope. If there is no identifiable target, ask for one before proceeding.

Read the affected code, its callers, project instructions, and the nearest existing tests. Identify the behavior that must remain: public APIs, outputs, side effects, errors, ordering, concurrency, and important edge cases. Run a focused existing check before editing when it gives a useful baseline.

## Independent review

Obtain three independent, read-only assessments through the host's delegation mechanism, using its reviewer routing when one is configured. Run them in parallel when capacity allows, otherwise one after another. Each child sees only its brief, so make each brief self-contained: the same bounded target, relevant project constraints, the read-only and no-delegation limits, and the return format. Ask for compact findings with file and line references, supporting evidence, and uncertainties; the first two assessments should also propose concrete changes. A brief does not make a child read-only on every host, so prefer a read-only reviewer role or sandbox when the host offers one.

1. **Reuse and ownership:** Find existing local helpers or patterns that can replace duplicate code. Flag abstractions that have no current need and suggest the simplest owner for the logic.
2. **Direct simplification:** Find redundant state, branches, nesting, indirection, comments, and unnecessary work. Favor clear, direct code over shorter code.
3. **Behavior contract:** Map observable behavior and tests that constrain a refactor. Report specific invariants and risk areas involving validation, errors, type safety, side effects, ordering, timing, security, and public interfaces.

Wait for a usable assessment from all three before editing. Retry a failed or missing assessment once with the same scope. If one is still unavailable, or the host cannot delegate, report the incomplete review and stop before editing.

## Apply and verify

Compare each proposed change with the contract map and live code. Apply only changes whose simplification benefit is concrete and whose behavior can be preserved. Resolve overlapping or conflicting proposals yourself; leave uncertain proposals unapplied. Keep one writer in the main thread and make the smallest focused edits. Preserve meaningful tests and error handling. Do not add an abstraction or dependency just to reduce line count.

Run the focused checks that cover the affected behavior, inspect the final diff for scope and accidental changes, and use an independent read-only reviewer for a substantive final diff. If a check fails or behavior preservation remains uncertain, fix the issue or report the incomplete result. Summarize what became simpler, the verification performed, and any proposals deliberately left unapplied.
