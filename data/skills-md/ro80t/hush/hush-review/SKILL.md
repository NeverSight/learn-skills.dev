---
name: hush-review
description: Audits existing code's comments against the hush ladder (rename-over-comment, no name-restating, ~3-line cap, public API doc coverage, non-obvious-behavior coverage) and reports findings without changing anything. Reviews the current diff by default, or a given path/directory/branch/PR when one is passed as an argument, falling back to the whole repo if there is no diff and no target. Use when the user says "hush review", "review comments", "audit comments", "check comment quality", "/hush-review", or asks to find redundant/missing/stale comments without fixing them yet.
version: 1.0.0
---

# Hush Review

Read-only audit. Never edits a file — output is a findings list only. Run
`hush-fix` to apply what this surfaces.

## Target

- No argument → the current change set (`git diff`, staged + unstaged).
- A path, directory, branch, or PR passed as an argument → review that
  instead (diff against its base for a branch/PR, direct read for a path).
- No argument and no diff (clean tree) → fall back to the whole repo rather
  than reporting nothing to review.

## What counts as a finding

Walk every comment in the target through the hush ladder:

1. **Redundant** — a rename would remove the need for it: restates the
   identifier, narrates an obvious line, echoes a type.
2. **Missing** — a public/exported surface with no usage-bearing doc comment
   in the language's standard format (JSDoc, Javadoc, docstrings, rustdoc,
   godoc, XML doc comments, ...), the format an LSP will actually surface.
3. **Type-duplicating** — a doc comment restating what the type system
   already guarantees (e.g. a `@param {string}` tag in a typed language),
   which rots the moment the signature changes and the doc doesn't.
4. **Undocumented gotcha** — a non-obvious side effect, invariant, workaround,
   ordering constraint, or rejected alternative worth warning off, with no
   comment at all.
5. **Oversized** — an ordinary comment (not a public API doc) that runs well
   past ~3 lines without a clause-boundary reason.
6. **Stale** — a comment that no longer matches the code beside it.

## Output

One line per finding, most-severe first, grouped by file:

```
path/to/file.ts:42 — redundant — restates `isExpired`; delete after no rename needed
path/to/file.ts:88 — missing — exported `parseInvoiceLines` has no doc comment
```

End with one summary line: `N findings across M files`. Nothing else — no
prose recap, no fixes applied.
