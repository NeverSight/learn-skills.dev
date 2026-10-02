---
name: clean-code
description: Clean Code. Enforce Martin's naming, function, comment, error, test, and smell rules on every change. Use when writing, editing, reviewing, or refactoring any source file, or when the user mentions naming, functions, comments, duplication, Boy Scout, smells, or clean code.
---

# Clean Code

Mandatory on every change to source. Repository conventions win where they conflict. Do not
explain the book. Apply the rules. Pair with `tdd` when changing behavior and with
`typescript-best-practices` on `.ts` / `.tsx`.

## Before you edit

1. Read the surrounding file, its callers, and its tests.
2. Name the unit's job in one sentence without "and", "also", or "then". If you cannot, split it
   before adding behavior.
3. Search for an existing implementation. Extend it. Do not invent a parallel helper.

## Enforce these rules

| Rule | You must |
| --- | --- |
| Intent-revealing names | Name the domain concept. No `data`, `info`, `stuff`, `manager`, `helper`, `util`, `temp`, `obj`. One word per concept. Booleans read as predicates (`isActive`, `hasItems`). Function names disclose side effects (`saveInvoice`, not `handleInvoice`). |
| Small functions | One thing, one abstraction level, top-to-bottom. Few arguments. No boolean flags that switch behavior. Command or query, not both. Extract a nested conditional into a named predicate. |
| Comments | Explain why, or delete. No commented-out code. No comments that restate the next line. No journal logs. Public API docs only where the project already uses them. |
| Objects vs data | Objects hide data and expose behavior. Data structures expose data. Do not reach through `a.b.c.d`. Ask the object. |
| Errors | Fail fast. Preserve the cause. Keep the happy path readable. Never swallow. Do not return a silent default for a real failure. |
| Boundaries | Wrap third-party APIs behind a type you own. Validate at the edge. |
| Tests | Tests specify behavior at a public seam. They stay green while internals move. Do not weaken, skip, or delete a failing test to get green. |
| Emergence | In this order: tests pass; no duplicated knowledge; intent is obvious; fewest elements. Stop at the first failure. |
| Boy Scout | Leave the lines you already touched cleaner. Do not widen the diff to clean unrelated files. Report leftover smells. |

Smell IDs for review: [`references/smells.md`](references/smells.md).

## Forbidden in the diff

- A `_v2`, `_new`, `_final`, `_copy`, or date-suffixed sibling of an existing file.
- New files in `utils`, `helpers`, `common`, or `misc` without a domain name.
- An unreferenced new file, route, or export.
- Regenerating a whole file when a targeted edit would do.
- Mixing a behavior change and a refactor in one step when they can be separated.

## Done

Do not claim the change is finished until:

- [ ] Every new or grown function passes the one-sentence test.
- [ ] Names in the diff say what the value is and what the function does, including side effects.
- [ ] No comment in the diff restates code. No commented-out code remains.
- [ ] Errors are handled where a decision can be made, with the cause preserved.
- [ ] Tests or checks match the behavior changed, and none were weakened.
- [ ] Touched lines are cleaner than before, and the diff did not grow to mop the rest of the file.
