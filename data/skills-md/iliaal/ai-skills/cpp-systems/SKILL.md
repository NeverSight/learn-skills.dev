---
name: cpp-systems
class: language
description: >-
  Modern C++ patterns: RAII and ownership, rule of zero/five, exceptions and
  error handling, API and ABI boundaries, templates, and CMake tooling. Use when
  writing, reviewing, refactoring, or debugging C++, working with smart pointers,
  move semantics, memory leaks, template errors, or gtest. For plain C, see
  ia-c-systems.
paths:
  - "**/*.cpp"
  - "**/*.hpp"
  - "**/*.cc"
  - "**/*.hh"
  - "**/*.cxx"
  - "**/*.h"
  - "**/CMakeLists.txt"
  - "**/*.cmake"
---

# C++ Systems & Libraries

Covers C++17 as the baseline, with C++20 features called out where a project's standard allows them. For plain C (manual lifetimes, status enums, native extensions), see the `ia-c-systems` skill.

## Working rules

- Make resource ownership explicit and use RAII for release on every exit path.
- Keep borrowed views within backing-storage lifetimes and review copy/move behavior when special members change.
- Follow the project's error model and supported language standard.
- Preserve ABI and avoid invoking unknown callbacks while holding locks or invalidatable container iterators.

## Repo conventions outrank this skill

Check `CMakeLists.txt` for `CXX_STANDARD`, read `.clang-format` and `.clang-tidy`, and read two adjacent translation units before writing. Where they conflict with the rules below, they win.

The conflicts that actually happen:

| Local constraint | Consequence |
|---|---|
| `-fno-exceptions` | Error handling is codes or `expected`-alikes. Constructors cannot report recoverable failure, so use a fallible factory or construct a valid fallback state. `new (std::nothrow)` only where the project's OOM policy is to observe null and recover; plain `new` is fine where the policy is termination |
| Standard pinned below C++17 | No `std::optional`/`string_view`/structured bindings/`if constexpr`; check before using any |
| Public header is ABI-stable | No layout changes, no inline-function changes, no added virtuals: load the ABI reference |
| Embedded or freestanding target | No RTTI, no dynamic allocation in hot paths, possibly no STL containers |


## Ownership and RAII

Every resource has exactly one owner, and that owner is an object whose destructor releases it. A raw `new` or `delete` in application code is a defect.

- `std::unique_ptr<T>` for sole ownership. It is the default; it costs nothing over a raw pointer.
- `std::shared_ptr<T>` only where lifetime is genuinely shared and cannot be expressed as "the owner outlives the users". Reach for it third, not first.
- `std::weak_ptr<T>` to break ownership cycles. LeakSanitizer does report a cycle that is unreachable from any root, but not one still reachable from a global or other registered root, and detection varies by platform and configuration. Do not rely on the sanitizer to find these.
- Raw `T*` and `T&` mean **non-owning observation**, and are correct in that role. A parameter taking `unique_ptr` by value is announcing that it consumes ownership; one taking `T*` is announcing it does not.
- `std::span<T>` (C++20) or a pointer-plus-length pair for a borrowed contiguous range **in a new public API**, since `const std::vector<T>&` there refuses every other container. On a C++17 baseline, or for internal code whose callers all hold vectors anyway, `const std::vector<T>&` is fine and simpler.

**Rule of zero**: a class that owns nothing declares no destructor, no copy, and no move. Composing members that manage themselves gets all five special members correct for free. **Rule of five**: declaring any one of destructor, copy constructor, copy assignment, move constructor, or move assignment obliges the author to reason about all five. A user-declared destructor suppresses the implicit move operations, so a class that gained a destructor silently started deep-copying where it used to move.


## Discipline

- Preserve behavior and API compatibility unless a break was requested. A public header change is a decision, not a cleanup.
- Do not introduce a template, an inheritance hierarchy, or a policy parameter for a single call site.
- `#include` what the file uses; do not rely on transitive includes from another header.
- No `using namespace` at namespace scope in a header. Fully qualify instead, or scope the `using` to a function body.
- When a constraint forces a deviation, comment at the deviation site and state the constraint.


## Verify

- Build clean with `-Wall -Wextra -Wpedantic -Wshadow -Wconversion -Werror`
- `clang-tidy` reports no new findings on the diff
- Tests pass under `-fsanitize=address,undefined` with zero reports
- Any threaded code touched by the change exercised under TSan with zero reports; the warning bundle above does not catch lock misuse
- `clang-format --dry-run --Werror` produces no diff
- No new raw `new`/`delete`, no new `shared_ptr` where `unique_ptr` suffices
- Any class that gained a destructor has its move operations reviewed

## Task-specific references

Read the relevant reference before implementing or reviewing the matching behavior:

- For constness, errors, API/ABI changes, templates, or standard-library behavior: [value-and-interface-design.md](./references/value-and-interface-design.md).
- For threading, compiler setup, tests, or build analysis: [concurrency-and-verification.md](./references/concurrency-and-verification.md).

Existing specialized references, when the corresponding topic applies:

- [api-and-abi.md](./references/api-and-abi.md).
- [cmake-and-tooling.md](./references/cmake-and-tooling.md).
- [legibility-standard.md](./references/legibility-standard.md).
