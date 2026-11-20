---
name: cleanup
description: Cleanup cruft from a diff, or from a project's current state.
argument-hint: "([<range>] [<path>...] | snapshot [<path>...]) [focus: <text>]"
---

# Cleanup

## Scope

**Diff** (default). Take uncommitted changes against `HEAD`, so staged work is included. A range argument (diff scope only, never with `snapshot`) replaces that diff. Bare `main` or `master` means `<base>...HEAD`; prefer `main` when both exist. A path or glob limits you to matching files in the diff. Empty diff: stop. If an explicit path matches nothing in the diff, ask which scope to use.

**Tree.** The word "snapshot" as the first argument selects this scope and defaults to the full state of the current codebase. A path limits scope to that path's current contents.

## Cruft

Focus is free text after `focus:` and replaces the list below. With no focus, clean:

- Unused symbols (imports, bindings, types, exports, re-exports) and uncalled test scaffolding
- Commented-out code and unreachable branches
- Debug logging (`console.log`, `debugger`, temporary prints)
- Unreferenced files and barrels, including empty stubs
- Duplicate helpers, folded into the existing one
- One-off helpers with a single in-scope caller, inlined there
- Duplicate code paths, collapsed into one (near-identical branches, repeated reads of the same value, thin wrappers over an existing reader)

In a diff, only cruft the change introduced or left behind.

Delete code only when a repo search shows it is unused. Keep public or compatibility APIs and intentional branches (feature flags, documented fallbacks, platform splits) even when nothing in the repo calls them.

## Edit

Change only those removals and simplifications and the call sites they affect. Keep formatting and names unchanged. Keep behavior identical across every branch the simplification touches.

Run the linters or tests covering touched files and fix failures the edit caused.

## Report

- Scope (diff or tree) and any focus
- Files touched
- What you removed, inlined, or simplified, and why
- What you kept on purpose, or could not decide
- Checks you ran, and any failure or check you could not run
