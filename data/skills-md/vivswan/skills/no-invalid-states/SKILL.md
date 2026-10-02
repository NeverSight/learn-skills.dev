---
name: no-invalid-states
description: Use when code or a design guards invariants with repeated runtime checks, lifecycle flags, or the same guard at every consumer, or when asked to make invalid states unrepresentable or parse-don't-validate.
license: SEE LICENSE IN LICENSE.md
metadata:
  author: Vivswan
---

# No Invalid States

Review and refactor a codebase so that correctness constraints are carried by the strongest mechanism the language provides. Scattered defensive checks are not that mechanism.

The core principle:

> Validate at boundaries, convert into stronger representations, and make invalid internal states difficult or impossible to construct.

This is the "parse, don't validate" discipline:

- Each fact is checked **once**, at the edge.
- The result is encoded in a representation the rest of the program can trust.
- Runtime validation is not deleted: checks on external, dynamic, or untrusted data stay.

## When to Apply

Use this skill when the code shows any of these signals:

- repeated runtime checks of the same condition (`if !initialized`, `if value is None`, `assert ready`)
- booleans that encode lifecycle or mutually exclusive states
- several optional fields that must always appear or be absent together
- methods that are only valid after another method has been called
- comments such as "must call X before Y" or "only valid when connected"
- functions re-validating data that a caller already validated
- structs, classes, or interfaces that permit contradictory field combinations
- incorrect operation ordering that could be rejected statically
- casts, non-null assertions, or type ignores used to quiet the checker

Do not use this skill to add abstraction to code that is already simple, or in place of a bug hunt. It improves representation, not behavior.

## Guiding Principle

Before adding another defensive check, ask: can this invalid state be removed from the program's representation instead? Use the strongest idiomatic mechanism the language offers. Keep the design simpler, not more complicated, than the problem itself.

## Workflow

### 1. Find candidate invariants

Search for the telltale patterns:

```text
if !initialized        if value is None         state === ...
if !connected          if value === undefined   is_ready / is_valid
assert ready           has_loaded               instanceof / isinstance chains
```

Also inspect:

- boolean lifecycle flags and state enums surrounded by unrelated optionals
- constructors that produce partially valid objects
- public setters that can break an invariant after construction
- methods that fail only because another method was not called first
- unchecked casts or assertions that exist to convince the type checker

For each candidate, write the invariant as one sentence. For example: "a connection may only send data after it has successfully connected."

If you cannot state the invariant, you cannot encode it. Skip it.

### 2. Classify each invariant: static or dynamic

- **Static**, internal invariants belong in the program's structure. Examples: initialized vs uninitialized, authenticated vs unauthenticated, parsed vs raw, validated ID vs arbitrary string, mutually exclusive states.
- **Dynamic**, external conditions keep their runtime checks. Types cannot prove that an HTTP request succeeded, a file still exists, a token has not expired, user input is well-formed, or a service is reachable.

The target shape is a one-way pipeline:

```text
untrusted or raw value
  -> validate / parse once, at the boundary
  -> strong internal representation
  -> trusted internal APIs (no re-checking)
```

### 3. Resolve at the ownership level

Before choosing a representation, find who **mutates** the state behind the invariant. The resolution belongs at those mutation points, not at the consumers.

The telltale: N call sites carrying the same guard, or a flag that every consumer must remember to honor. That is validation at N read points where prevention at the few write points would do.

Worked example: a stored credential goes stale when its associated endpoint URL changes.

- **Consumer-side design:** all six request paths check a `staleCredential` flag before using it. Six guards, six error surfaces, and every future request path must remember the check.
- **Owner-side design:** every URL change (settings UI save, config file edit, import) goes through one owning transition. It resolves the question at that moment ("keep this credential for the new endpoint?").
- **Afterwards:** no request path needs a staleness guard. Runtime authentication failures stay handled, as the dynamic condition they are.

Two rules make the owner-side fix sound:

- **Enumerate all mutation points** before claiming completeness. A consumer-side check accidentally covers write paths you forgot, but an owner-side fix must route each one through the owning transition explicitly. A GUI and the settings file it edits are two paths, not one.
- **The resolution at the mutation point need not be a type.** A validating transition, a normalization, or a question put to the user at the moment the intent is expressed all work. The next step covers the cases where a stronger representation is the right mechanism.

### 4. Choose the strongest idiomatic representation

Pick by situation, not by favorite mechanism:

| Situation | Representation |
| --- | --- |
| State changes at runtime and code inspects which state it is in | Sum type: enum with data, discriminated union, sealed class |
| Available operations depend on state; wrong ordering should fail to compile | Typestate: state-parameterized types, consuming transitions |
| A primitive has special meaning or is validated once then trusted | Newtype or branded type behind a smart constructor |
| Two states carry meaningfully different data; optionals encode which one | Separate types per state |
| An invariant spans construction (fields must agree) | Private fields, factory or constructor that validates, immutability |
| The invariant is really about the data store | Schema constraints: NOT NULL, CHECK, foreign keys, unique |

Detailed, idiomatic guidance with code examples lives in the per-language references:

- [references/rust.md](references/rust.md): enums, newtypes, typestate with `PhantomData`, consuming `self`, `TryFrom` boundaries
- [references/typescript.md](references/typescript.md): discriminated unions, branded types, exhaustive `never` checks, boundary schemas
- [references/python.md](references/python.md): state-specific frozen dataclasses, `Literal` unions, `NewType`, `assert_never`, strict typing
- [references/other-languages.md](references/other-languages.md): Go, Java, Kotlin, C#, Swift, functional languages, dynamic languages, and databases

If the language at hand is not covered, map the situation table onto whatever the language offers. Sealed hierarchies, smart constructors, immutability, and module privacy exist almost everywhere in some form.

### 5. Refactor

For each accepted candidate, work through this checklist:

1. State the invariant and the invalid state currently representable.
2. Introduce the stronger representation.
3. Put validation at the boundary: one parser or factory that turns raw data into the strong type, with a real error path.
4. Change internal APIs to accept the strong type, so downstream code cannot receive an unvalidated value.
5. Remove checks the new representation makes logically impossible.
6. Keep, and briefly justify, checks that remain because they are dynamic.

Rules while refactoring:

- **Make illegal construction hard:** private fields, validating constructors, factory functions, state-transition functions, frozen or readonly data.
- **Validate once.** `validate -> use, validate -> use` becomes `parse once -> use, use, use`.
- **Never silence the type checker** with broad casts, `any`, non-null assertions, or ignore comments to force a refactor through.
- **Preserve existing behavior** unless you have confirmed a bug. If you find one, report it separately rather than fixing it silently.
- **Respect public API compatibility** where practical: strengthen internals first, then widen outward.
- **Make the smallest architectural change** that removes the invalid state. Do not convert every boolean into a state machine.
- **A refactor is worthwhile only when** it eliminates repeated checks, prevents wrong ordering, removes impossible field combinations, or clarifies the API contract. Readability beats type-system cleverness.

### 6. Test and verify

Update or add tests for:

- valid state transitions
- rejected boundary input
- exhaustive state handling
- behavior preservation

Add compile-fail or type-level tests only if the project already has a mechanism for them.

Then run the repository's own tooling. Inspect the project configuration (`package.json` scripts, `Makefile`, `Cargo.toml`, `pyproject.toml`, CI workflows) rather than assuming command names. Typical gates:

- Rust: `cargo fmt --all -- --check`, `cargo clippy --workspace --all-targets -- -D warnings`, `cargo test --workspace`
- TypeScript: the project's typecheck, lint, test, and build scripts
- Python: the configured ruff / pyright / mypy / pytest setup
- anything else: whatever the repo's CI runs

Do not introduce a new type checker or dependency just for this skill unless that is genuinely appropriate for the repository.

### 7. Report

When asked to modify code, implement the changes rather than describing them. At completion, report:

- **Invariants improved:** what was previously enforced by convention or runtime checks
- **Invalid states removed:** what contradictory data or wrong ordering was previously possible
- **New representation:** which mechanism now carries each invariant (for example: Rust typestate, TypeScript discriminated union, Python NewType)
- **Runtime validation retained:** which checks stay because they depend on external or dynamic information
- **Files changed** and why
- **Verification:** the exact formatter, type-checker, lint, build, and test commands run, and whether they passed

## Review Criteria

Skills that run code reviews (such as `/rubber-duck-review`) expand this section into their reviewer prompt when this skill is installed. Ask the reviewer to flag:

- invariants enforced only by runtime checks or convention:
  - boolean lifecycle flags
  - optional fields that must appear or be absent together
  - "must call X before Y" ordering enforced at runtime
  - repeated validation of already-validated values
  - field combinations that should be impossible to represent
- consumer-side guards that an owner-side resolution would remove: the same check repeated at N call sites, or a flag every consumer must remember to honor. This applies when the state has enumerable mutation points where the question could be resolved once
- for each finding, the stronger representation (sum type, newtype, typestate, validating constructor) or owner-side resolution that would remove the invalid state

Triage the resulting findings with the workflow above.
