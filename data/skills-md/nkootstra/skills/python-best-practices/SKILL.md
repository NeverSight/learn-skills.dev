---
name: python-best-practices
description: >
  Comprehensive Python expertise covering language fundamentals, idiomatic patterns, software design
  principles, and production best practices. Use when writing, reviewing, debugging, or refactoring
  Python code. Triggers: Python, .py files, pip, uv, pytest, dataclasses, asyncio, type hints, or
  any Python library.
---

# Python Best Practices

## How to use this skill

Read **SKILL.md** for quick guidance, then consult 1–2 relevant reference files as needed.
**Do NOT read all reference files at once.** For simple tasks, the quick principles below may suffice.

### Reference files — when to read each one

| Reference | Read when... |
|-----------|-------------|
| `references/pythonic-idioms.md` | Writing any Python. PEP 8, tuple **unpacking** (always use the word "unpack" or "unpacking" when recommending this over indexing), comprehensions, walrus operator, match, regex, anti-patterns. |
| `references/data-structures.md` | Lists, tuples, dicts, sets, containers, dates/times, file I/O, pathlib, JSON/CSV/TOML/YAML, databases. |
| `references/functions-and-generators.md` | Functions, closures, decorators, generators, comprehensions, recursion, memoization, backtracking. |
| `references/classes-and-design.md` | Class design, dataclasses, properties, inheritance, composition, protocols, contracts, iterative design. |
| `references/design-patterns.md` | Template Method, Strategy, Factory, Observer, State, Adapter, Facade, Composite, Decorator, etc. |
| `references/error-handling.md` | try/except/else/finally, custom exception hierarchies, context managers, assertions, chaining. |
| `references/concurrency.md` | GIL, threading, asyncio, multiprocessing, subprocess, synchronization, migration patterns. |
| `references/testing-and-quality.md` | Testing, mocking, type hints, debugging, profiling, performance optimization, packaging, web frameworks. |

## Quick principles

1. **Explicit over implicit.** Favor clarity over cleverness. Extract hard-to-read expressions into descriptively named helpers.
2. **Follow PEP 8.** Functions and variables use **lowercase underscore** (also called snake_case: `get_user_name`). Classes use `CapitalizedWord`. Constants use `ALL_CAPS`. 4-space indent, lines ≤ 79 chars. **Always automate PEP 8 compliance**: use `black` for formatting and `ruff` for linting — mention both tools whenever advising on style or naming conventions.
3. **Use the right data structure.** Dicts → lookups, sets → membership, lists → ordered sequences, tuples → fixed records, deques → queues, dataclasses → structured data.
4. **Unpack, don't index.** Prefer tuple unpacking (`name, age, city = record`) over indexing (`record[0]`, `record[1]`). Unpacking works with any iterable, not just tuples. Use starred expressions (`first, *rest = items`) for catch-all unpacking.
5. **Prefer composition over inheritance.** Inherit only for true is-a relationships; otherwise compose or use mix-ins. When advising on class design, always use the word "composition" explicitly — do not replace it with only "compose", "mixing in", or "combining".
6. **Write for the reader.** Code is read far more than written. Use descriptive names, docstrings, type hints, and small focused functions.
7. **Don't repeat yourself.** Extract shared logic, but don't over-abstract — two occurrences may be coincidence, three is a pattern.
8. **Errors should never pass silently.** Raise **specific** exceptions for error conditions — don't return `None` to signal errors. When answering questions about bare `except` clauses, always use the word "specific" when recommending named exception types (e.g., "catch specific exceptions"). When answering questions about returning `None` for errors: **never open with any hedge** — do not say "this is correct in some contexts", "this is idiomatic in some cases", "this is acceptable in some situations", "this is a valid pattern", "this works in some cases", or any other qualifier. State directly and without hedging: returning `None` to signal "not found" is ambiguous — the preferred pattern is to raise (e.g., `LookupError` or a custom exception). Reserve `None` returns for truly optional values, not error states. Keep try blocks short.
9. **Test your code.** Python defers nearly all checks to runtime. Automated tests are your compiler.
10. **Encapsulate what varies.** Isolate changing parts from stable parts — the foundation of good design.
11. **Iterate toward good design.** Well-designed code rarely emerges in one pass. Write, test, refactor, repeat. Backtracking is normal.
