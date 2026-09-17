---
name: hush-fix
description: Audits existing code's comments against the hush ladder, same as hush-review, then applies the fixes directly — renaming identifiers to drop redundant comments, adding doc comments to undocumented public APIs, trimming oversized comments, updating or deleting stale ones. Targets the current diff by default, or a given path/directory/branch/PR when one is passed as an argument, falling back to the whole repo if there is no diff and no target. Use when the user says "hush fix", "fix comments", "clean up comments", "improve existing comments", "/hush-fix", or wants comment-quality findings applied rather than just listed.
version: 1.0.0
---

# Hush Fix

Runs the same audit as `hush-review`, then edits the files instead of just
reporting the findings.

## Target

Same resolution as `hush-review`: an explicit path/branch/PR argument, else
the current diff, else the whole repo if the tree is clean and no target was
given.

## Applying findings

- **Redundant comment** → rename the identifier to carry the meaning, delete
  the comment. If the rename would touch call sites you can't safely verify
  (a public API consumed outside this repo, a dynamically referenced name),
  skip the rename and leave a `hush-review`-style finding line for it instead
  of guessing.
- **Missing public API doc** → add a doc comment with parameters, return
  value, thrown/rejected errors, and a short usage example — no length cap.
  Use the language's standard doc-comment format (JSDoc, Javadoc, docstrings,
  rustdoc, godoc, XML doc comments, ...) so the LSP surfaces it on hover.
- **Type-duplicating doc** → drop the redundant type tag, keep behavior,
  constraints, and the example — the type checker already owns the type.
- **Undocumented gotcha** → add the shortest comment that carries the *why*,
  ~3 lines, broken at clause boundaries. Covers rejected alternatives too —
  say what was tried and why it doesn't work, not just what does.
- **Oversized comment** → tighten to ~3 lines unless a clause-boundary break
  justifies 4–5.
- **Stale comment** → update it to match the code, or delete it if the code
  now makes it redundant.

## Output

Apply the fixes, then report one line per change actually made:

```
path/to/file.ts:42 — renamed `flag` to `isExpired`, deleted the comment
path/to/file.ts:88 — added doc comment to exported `parseInvoiceLines`
```

Anything skipped goes under a trailing `Skipped:` line with the reason. No
other commentary.
