---
name: define-errors-out
description: Reduce exception and error-handling complexity by redefining semantics so errors cannot occur, masking them at a low level, aggregating handlers, or crashing (Ousterhout's "define errors out of existence"). Use when the user says error handling is messy, there are too many try/catch or `if err != nil` branches, asks whether a function should throw or return an error, or is designing an API's error cases. Not for debugging a specific failure (diagnosing-bugs).
---

# Define Errors Out of Existence

Throwing is easy; handling is hard. Every exception is part of the interface, and it spreads to every caller. The goal is **fewer places where errors must be handled**.

## For each error site, try in order

1. **Define it away.** Change the semantics so that the normal behavior covers the case.
   - `unset(x)` means "ensure x doesn't exist", so a missing x is a no-op.
   - `substring(a, b)` returns the chars in range ∩ string. Out-of-range bounds give an empty or truncated result.
   - Unix delete on an open file marks it for deletion. No error for the deleter or the readers.
   - Idempotent create or delete. Empty collections instead of null.
2. **Mask it low.** Handle it inside the module so no caller sees it (retry like TCP, fall back, recompute). Best when a library used by many callers can absorb it.
3. **Aggregate it high.** Let errors propagate to one handler, for example a request dispatcher. Put the user-facing message in the error at the throw site, so the top handler stays generic. Promote rare small errors into one existing recovery path.
4. **Just crash.** If the error is rare and there's no sensible recovery (OOM, corrupted internal state, most local I/O failures in a CLI), abort with a clear message through one helper (`must(...)`, `ckalloc`).

## Too far

Don't hide errors callers must act on. A network module that silently swallows lost messages makes robust callers impossible. Before hiding an error, ask: *does anyone outside need this information?* If yes, expose it, but at as few sites as possible.

## Output

A table of error sites with columns **site | current handling | technique (1–4 or keep) | new behavior**. Then the proposed changes: new semantics, written into the interface comment, plus the removed handlers. Handler code is rarely executed, so it tends to be broken, and deleting it is a feature.
