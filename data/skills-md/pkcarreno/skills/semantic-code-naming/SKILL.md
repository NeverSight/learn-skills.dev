---
name: semantic-code-naming
description: Apply semantic grammar rules, intent-based naming, and structural patterns (such as Action, High Context, Low Context or A/HC/LC) to variables, functions, and classes. Use this skill when writing new code, refactoring identifiers, or reviewing code for readability. Do not use this skill for formatting checks, indentation, or casing linters.
---

Define the intent and semantics of code identifiers to make code clear and maintainable.

## Scope

This skill evaluates the semantic meaning and intent of names. Linters must check typographical casing such as camelCase or snake_case.

## Philosophy

- S-I-D: Short, Intuitive, Descriptive.
- English: Maintain industry consistency.
- No Vague: Ban `foo`, `temp`, `data`, `a`, `x`.
- No Contractions: `onItemClick` > `onItmClk`.
- Clarity: Prioritize intent description over brevity.

## Rules & Grammar

- Variables: Nouns/Noun phrases (`userAge`, `totalSales`).
- Functions: Verbs/Verb phrases (`calculatePrice`, `handleLogin`).
- Booleans: Use positive phrasing (`isActive`, not `isNotInactive`). Prefixes: `is`, `has`, `can`, `should`.
- Cardinality: Singular for items (`user`), Plural for collections (`users`).
- Context: Avoid duplication. `User.save()`, not `User.saveUser()`.

## A/HC/LC Pattern

Structure: `[Prefix] + Action + HighContext + [LowContext]`

- `get`: Access data immediately.
- `set`: Declarative value assignment.
- `remove`: From collection (Counterpart: `add`).
- `delete`: Permanent erasure (Counterpart: `create`).
- `compose`: Create new data from existing.
- `handle`: Event callbacks.

## Vocabulary

- Suffixes: Manager, Handler, Provider, Builder, Factory, Cache, Proxy, Service.
- Modifiers: `-able` (capability), `-less` (absence), `-er/-or` (agent), `-ed` (state).
- Traits: Abstract, Base, Immutable, Core, Standalone, Scalable, Thread-Safe.

## Metaphors

- Use tangible analogies: _Honeypot_ (bait), _Sandbox_ (isolation), _Garbage Collector_ (cleanup), _Breadcrumb_ (navigation), _Tree_ (hierarchy).

---

**GOLDEN RULE**: A name must fully describe what the code represents or does.
