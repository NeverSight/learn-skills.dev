---
name: hush
description: Enforces self-documenting naming and minimal, high-signal comments. Renames instead of commenting whenever a name alone can carry the meaning, caps ordinary comments at ~3 lines (more is fine when a clause-boundary line break pushes past that), writes full doc comments with usage examples only for public/exported API surfaces, always comments non-obvious behavior regardless of visibility, and comments a branch (if/for/while/switch) only when its condition or body can't be inferred from the names involved. Use on ANY coding task — writing, adding, refactoring, fixing, or reviewing code — and whenever the user says "hush", "comment style", "minimal comments", "self-documenting code", or complains about redundant comments, comment noise, or missing docs on a public API.
version: 1.0.0
---

<!-- RULE-SUMMARY:START -->
# Hush

Code that explains itself. A comment only earns its line when a name can't do the job.

## The ladder

Before writing or keeping a comment, run it down this list and stop at the first rung that applies:

1. **Can a rename remove the need for this comment?** Rename, delete the comment. A comment restating what `isExpired` already says is noise; a variable called `flag` needing a comment to explain it is a naming bug, not a documentation gap.
2. **Is this a public/exported surface** (library entry point, exported function/class/method, public API)? Write a full doc comment with a usage example. No length cap — see *Public API docs* below.
3. **Would misreading this line cause a bug** — a non-obvious side effect, an invariant the type system can't express, a workaround for a specific library/platform quirk, a "don't reorder this" constraint, or a tempting-looking alternative that was deliberately rejected? Comment it. This applies **regardless of public or private** visibility.
4. **Is this a branch** (`if`/`for`/`while`/`switch`/`case`) whose condition or body can't be inferred from the names of the variables/functions/methods it uses? Write one short comment on *why*, not *what*.
5. **None of the above** → no comment.

## Naming first

When writing new code, name for the reader who has no comment to lean on: a function called `retryWithBackoff` needs no comment explaining it retries with backoff; a function called `process` does — but the fix is renaming it to `parseInvoiceLines`, not adding a comment on top of `process`.

## Length and line breaks

- Ordinary comments (rungs 3 and 4): target **~3 lines**.
- Break lines at clause/phrase boundaries — wherever the reader's eye naturally pauses — never mid-thought just to hit a character count.
- A clear, meaning-preserving break that runs to 4–5 lines beats a cramped 3-line wrap that severs a clause. The 3-line target yields to line-break clarity, not the other way around.

## Public API docs

Exported functions, classes, methods, and other library-boundary surfaces are exempt from the length cap. Include what a caller needs to use it without reading the implementation — parameters, return value, thrown/rejected errors, and a short usage example. Running past 3 lines here is expected, not a violation.

Write it in the language's standard doc-comment format — JSDoc in JS/TS, Javadoc in Java, docstrings in Python, rustdoc in Rust, godoc in Go, XML doc comments in C# — whenever the language has one. That's what makes the LSP surface it as hover/autocomplete instead of leaving it as a comment only a source reader ever sees.

Don't restate what the type system already guarantees — skip type tags like `@param {string} name` in a language with static types. A doc that duplicates the signature rots the moment the signature changes and the doc doesn't; keep it to what the types can't say: behavior, constraints, an example.

## What always gets a comment, public or private

Non-obvious side effects, invariants the type system can't express, workarounds for a specific bug or library quirk, ordering constraints, a rejected alternative worth warning off, anything a careful reader could misread and break.

## What never gets a comment

Anything a rename would fix: restating the method name, narrating a straightforward loop (`// increment i`), echoing a type, describing what the next line obviously does.
<!-- RULE-SUMMARY:END -->

## Examples

**Naming replaces the comment**
```js
// bad: comment papers over a bad name
// check if the user can edit this document
if (u.r >= 2 && !d.locked) { ... }

// good: names carry the meaning, no comment needed
if (user.role >= Role.Editor && !document.locked) { ... }
```

**Branch that still needs a comment (rung 4)**
```python
# Stripe requires idempotency keys to be reused on retry, not regenerated,
# or a network retry after a successful charge double-bills the customer.
if attempt > 0 and cached_idempotency_key:
    key = cached_idempotency_key
```
Nothing in `attempt`, `cached_idempotency_key`, or the branch shape explains *why* — the comment carries the constraint the names can't.

**Public API doc (exempt from the 3-line cap)**
```ts
/**
 * Splits a monetary amount into equal integer shares without losing cents
 * to rounding — the classic "split $10 three ways" problem.
 *
 * @example
 * splitEvenly(1000, 3) // => [334, 333, 333]  (cents)
 */
export function splitEvenly(totalCents: number, parts: number): number[] { ... }
```

**Non-obvious gotcha (rung 3, private code, still commented)**
```go
// macOS coalesces SIGCHLD signals sent in quick succession, so a single
// handler invocation can represent multiple exited children.
for {
    pid, status := syscall.Wait4(-1, ...)
    ...
}
```

## Output

When editing existing code, delete comments that a rename now makes redundant — don't leave both. When the change is done, note in one line what was removed or added and why, if it isn't obvious from the diff.
