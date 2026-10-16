---
name: doc-comments
description: Use when writing, editing, or reviewing doc comments — JSDoc, docstrings, rustdoc, godoc, or similar.
---

Doc comments serve callers, not readers of the implementation. Visibility decides whether an identifier gets a doc comment at all; complexity decides how deep that comment goes.

Visibility is determined by the language's visibility mechanism, not by current usage. An identifier exported but unused elsewhere still has an audience and still needs documenting.

## Glossary

- **identifier**: a name that can be documented — variables, constants, functions, methods, classes, interfaces, structs, types, and similar forms from language to language.
- **private**: not referenceable outside its module or package, per the language's visibility mechanism — unexported, non-capitalized (Go), or leading underscore (Python). In Go, an unexported identifier is private even when other files in the same package use it.
- **public**: referenceable outside its module or package.

## Rules

1. Private identifiers MUST NOT have doc comments. Readers with access can see the implementation.
2. Public identifiers MUST have doc comments. Depth scales with the complexity of what is being described.

Before writing a file, classify every identifier as private or public, then judge the complexity of each public one.

## How to determine complexity

### Functions

Factors in judging the complexity of a function. These are usually correlated.

1. **Length**. Probably the best signal. A one-liner has much less to document than a 100-liner.
2. **Nesting**. A function with loops four levels deep is much more complex than one that never nests more than one level.
3. **Parameters**. One or two parameters is generally less complex than many.
4. **Concurrency**. One async call, or delegation to a function that makes one, is not highly complex. Multiple async calls are more complex, particularly in parallel. A function that spawns threads or processes MUST thoroughly spell out the logic being invoked.

Some things MUST be documented regardless of the above.

1. **Surprising mutations**. Assume a function does not mutate data-structure arguments; adjust the typing to say so if you can. If it _does_ mutate, document it — it breaks an implicit contract.
2. **Stack overflow**. Recursive functions MUST document conditions that may trigger stack overflow.
3. **Preconditions, invariants, and assertions**. MUST be explained in doc comments.

When one of these MUSTs applies to behavior implemented inside a private identifier, document it on the public identifier affected. State the behavior — "deeply nested input can overflow the stack" — not the private helper. Ask what the public function can do to its callers, not which private helper implements it.

Avoid documenting things that can be inferred from the name and types unless there's no other option.

## What depth looks like

A simple public identifier gets one or two sentences stating purpose. As complexity grows, add only what callers cannot see from the name and types: error conditions (what raises, throws, or rejects, and when), side effects callers must know (mutation, I/O, persistence), and edge cases (empty input, rounding, overflow).

An identity function or no-op gets exactly that: `/** Identity function. */` — there is nothing else true to say.

Structured tags such as `@param`, `@returns`, and `@throws` are part of depth, not a default. Add a tag only when it says something the signature cannot — units, formats, valid ranges, default values, or the condition under which an error is raised. A tag that restates a parameter's name or type is noise; simple identifiers usually need no tags at all.

A high-complexity doc comment opens with a one- or two-sentence summary, then gives each facet of the contract its own short labeled paragraph — for example Concurrency, Mutation, Errors — rather than interleaving facets in one prose block.

## Examples

Public identifiers at low and high complexity; private identifiers get nothing either way:

```ts
// private — no doc comment, however complex
function normalizeSku(raw: string): string { ... }

// public, simple — one sentence
/** Round fractional cents half-up to the nearest whole cent. */
export function roundCents(cents: number): number { ... }

// public, complex — full contract, one labeled paragraph per facet
/**
 * Reserves the given SKUs atomically.
 *
 * Concurrency: fetches stock levels for all SKUs in parallel.
 *
 * Mutation: mutates `cart` in place, removing reserved items.
 *
 * Errors: rejects when any SKU has insufficient stock; completed
 * reservations are rolled back before rejecting.
 */
export function reserveCart(cart: Cart, skus: string[]): Promise<void> { ... }
```

In Python, docstrings are doc comments and these rules apply. A leading underscore marks private.

```python
# private — no docstring
def _validate_sku(sku: str) -> None: ...

# public, simple — one sentence
def round_cents(cents: int) -> int:
    """Round fractional cents half-up to the nearest whole cent."""

# public, complex — full contract
def load_inventory(path: Path) -> Inventory:
    """Load an Inventory from *path*.

    Creates an empty inventory bound to *path* if the file does not
    exist. Raises ValueError if the file is not a JSON object of
    SKU to non-negative integer quantities.
    """
```

## Justification table

If asked for justification, print a table with one row per identifier in the file:

| Identifier    | Visibility | Complexity | Doc comment?          | Justification                                                                     |
| ------------- | ---------- | ---------- | --------------------- | --------------------------------------------------------------------------------- |
| `roundCents`  | Private    | —          | No                    | Not exported; readers with access can see the implementation.                      |
| `roundCents2` | Public     | Low        | Yes — one sentence    | Exported; simple enough that purpose is all callers need.                          |
| `reserveCart` | Public     | High       | Yes — full contract   | Exported; parallel calls, mutation, and rollback are invisible from the signature. |

## Gotchas

- Documenting a private helper because it is "complex" — if it is not visible outside the package, complexity is the implementation's problem.
- Judging visibility by usage ("nothing imports it yet") or by file boundaries — the language's visibility mechanism decides.
- Documenting a private helper because its behavior surfaces through an exported function — document the behavior on the exported member instead.
- A one-line summary on a complex public identifier — depth must scale up with complexity.
- Narrating the documentation decision — section comments like "private helpers: no doc comments per policy" — comments describe the code, not the rules that produced it. Only add such markers where the codebase or its style rules already use them.

## Conventions and style rules

Language conventions and style rules MUST supersede these instructions. Where a project's style guide, linter, or language conventions dictate their own doc comment rules, follow those instead.
