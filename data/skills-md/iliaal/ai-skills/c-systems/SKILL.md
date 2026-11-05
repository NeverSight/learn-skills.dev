---
name: c-systems
class: language
description: >-
  C patterns for systems code, libraries, and native extensions: module
  layout, function decomposition, status-enum errors, memory safety, undefined
  behavior, and performance measurement. Use when writing, reviewing,
  refactoring, or debugging C, working with malloc lifetimes, buffer
  overflows, sanitizers, or Valgrind, or building native extensions. For C++,
  see ia-cpp-systems.
paths:
  - "**/*.c"
  - "**/*.h"
---

# C Systems & Native Code

Covers C11 and later for libraries, systems code, and native extensions. For C++ (RAII, templates, move semantics), see the `ia-cpp-systems` skill.

## Working rules

- Preserve the repository's sanctioned idioms and ABI; do not turn a scoped fix into a restyle.
- State ownership, check fallible calls, validate public boundaries, and assert internal invariants.
- **Preserve recovery outside optimizer assumptions.** An assertion that becomes an assumption can remove the branch handling its false case. Keep recoverable checks as runtime branches with diagnostic-only assertions behind a debug preprocessor guard. Exercise the fallback in an optimized release build.
- **Guard staged initialization against reentry.** Set an in-progress marker before callback-capable work on every constructor or factory path. Permit retry after failure only after fully releasing and resetting partial state. Test recursive entry and retry after failed initialization.
- Bound traversal of external input and check sizes before allocation or narrowing.
- Choose helpers only when they name a concept, own an error, or isolate a side effect.
- Verify the actual rebuilt artifact; use instrumented tests for safety and representative release builds for performance.

## Repo conventions outrank this skill

Read the repo's `AGENTS.md`/`CLAUDE.md`, its public headers, and two adjacent `.c` files before writing anything. Where they conflict with the rules below, they win, and the diff carries no note about it.

Do not skip this gate. Established C codebases sanction idioms these rules would otherwise flag:

| Local idiom | Where it is correct |
|---|---|
| Tab indentation | php-src and its extensions, Linux kernel |
| `goto cleanup` / `goto err` | Kernel, OpenSSL, curl, php-src: the dominant multi-resource release idiom |
| Macros containing `return` | `RETURN_*`/`RETVAL_*` in PHP extensions, `Py_RETURN_*` in CPython |
| Project status types | `zend_result`, `CURLcode`, `int` plus `errno`: do not invent a parallel enum beside one |

Never widen a scoped task into a repo-wide restyle because adjacent untouched C predates a rule here.

**When the target is a PHP extension** (`php_*.h`, `PHP_FUNCTION`, `zend_`, `config.m4`), load [php-extension-c.md](./references/php-extension-c.md) before applying any rule below. Layout, macros, the error model, memory, and assertions all carry extension-specific overrides, and the memory one in particular inverts the base guidance: extensions use a request-scoped allocator, not `malloc`/`free`.


## Verify

- Build passes under the repo's warning profile with zero newly introduced warnings (greenfield: the full `-Wall -Wextra -Werror -Wconversion -Wshadow` bundle, zero warnings)
- Test suite passes under `-fsanitize=address,undefined` with zero reports
- `valgrind --leak-check=full --error-exitcode=1` clean where the suite links under it
- Every new fallible call site checked; every new error value traced to one producer
- Every new state-mutating leaf carries an assert
- No new `goto` outside the repo's sanctioned form or the single-forward-jump cleanup; no recursion over external input; no loop over external input without a named bound

## Task-specific references

Read the relevant reference before implementing or reviewing the matching behavior:

- For module layout, naming, decomposition, control flow, errors, types, or macros: [implementation-structure.md](./references/implementation-structure.md).
- For memory, external input, assertions, ABI changes, or shared-helper contracts: [runtime-safety.md](./references/runtime-safety.md).
- For compiler setup, tests, build provenance, packaging, or performance claims: [build-and-measurement.md](./references/build-and-measurement.md).

Existing specialized references, when the corresponding topic applies:

- [php-extension-c.md](./references/php-extension-c.md).
- [memory-safety.md](./references/memory-safety.md).
- [correctness-traps.md](./references/correctness-traps.md).
- [legibility-standard.md](./references/legibility-standard.md).
